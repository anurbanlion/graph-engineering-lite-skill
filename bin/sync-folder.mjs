#!/usr/bin/env node

import { access, cp, mkdir, readFile, rm, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const repositoryDirectory = resolve(scriptDirectory, "..");
const environmentFile = join(repositoryDirectory, ".env");

// Report a clear error and terminate with a non-zero exit code.
function fail(message) {
  console.error(`sync-folder: ${message}`);
  process.exit(1);
}

function parseEnvironmentFile(content) {
  const values = new Map();

  for (const [index, rawLine] of content.split(/\r?\n/).entries()) {
    const line = rawLine.trim();

    if (!line || line.startsWith("#")) {
      continue;
    }

    const separatorIndex = line.indexOf("=");

    if (separatorIndex <= 0) {
      fail(`invalid .env entry on line ${index + 1}`);
    }

    const key = line.slice(0, separatorIndex).trim();
    let value = line.slice(separatorIndex + 1).trim();

    if (!/^[A-Z][A-Z0-9_]*$/.test(key)) {
      fail(`invalid .env key on line ${index + 1}: ${key}`);
    }

    if (
      value.length >= 2 &&
      ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'")))
    ) {
      value = value.slice(1, -1);
    }

    values.set(key, value);
  }

  return values;
}

async function readConfiguration() {
  let content;

  try {
    content = await readFile(environmentFile, "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") {
      fail(`configuration file not found: ${environmentFile}. Copy .env.example to .env and configure it.`);
    }

    throw error;
  }

  const configuration = parseEnvironmentFile(content);
  const sourcePathValue = configuration.get("SYNC_SOURCE_PATH");
  const destinationPathValue = configuration.get("SYNC_DESTINATION_PATH");

  if (!sourcePathValue) {
    fail("SYNC_SOURCE_PATH MUST be set in .env");
  }

  if (!destinationPathValue) {
    fail("SYNC_DESTINATION_PATH MUST be set in .env");
  }

  return { sourcePathValue, destinationPathValues: parseDestinationPaths(destinationPathValue) };
}

// Accept a single destination for compatibility, or a JSON array for fan-out syncs.
function parseDestinationPaths(value) {
  if (!value.startsWith("[")) {
    return [value];
  }

  let destinations;

  try {
    destinations = JSON.parse(value);
  } catch {
    fail("SYNC_DESTINATION_PATH MUST be an absolute path or a JSON array of absolute paths");
  }

  if (
    !Array.isArray(destinations) ||
    destinations.length === 0 ||
    destinations.some((destination) => typeof destination !== "string" || !destination.trim())
  ) {
    fail("SYNC_DESTINATION_PATH JSON array MUST contain one or more non-empty paths");
  }

  return destinations.map((destination) => destination.trim());
}

// Require an existing directory and explain whether it is missing or invalid.
async function requireDirectory(path, label) {
  try {
    const pathStat = await stat(path);

    if (!pathStat.isDirectory()) {
      fail(`${label} is not a directory: ${path}`);
    }
  } catch (error) {
    if (error?.code === "ENOENT") {
      fail(`${label} does not exist: ${path}`);
    }

    throw error;
  }
}

// Check whether a path exists without treating a missing path as an error.
async function pathExists(path) {
  try {
    await access(path, constants.F_OK);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") {
      return false;
    }

    throw error;
  }
}

// Determine whether childPath is located inside parentPath.
function isInside(parentPath, childPath) {
  const pathFromParent = relative(parentPath, childPath);

  return (
    pathFromParent !== "" &&
    !pathFromParent.startsWith(`..${sep}`) &&
    pathFromParent !== ".." &&
    !isAbsolute(pathFromParent)
  );
}

async function syncFolder() {
  if (process.argv.length > 2) {
    fail("this script does not accept arguments; configure .env in the repository root");
  }

  const { sourcePathValue, destinationPathValues } = await readConfiguration();
  const sourcePath = isAbsolute(sourcePathValue)
    ? resolve(sourcePathValue)
    : resolve(repositoryDirectory, sourcePathValue);

  const destinationPaths = destinationPathValues.map((destinationPathValue) => {
    if (!isAbsolute(destinationPathValue)) {
      fail(`SYNC_DESTINATION_PATH MUST be absolute: ${destinationPathValue}`);
    }

    return resolve(destinationPathValue);
  });

  // Step 3: validate the source before modifying the destination.
  await requireDirectory(sourcePath, "source folder");

  // Prevent destructive configurations that could remove the source itself.
  for (const destinationPath of destinationPaths) {
    if (sourcePath === destinationPath) {
      fail("source and destination resolve to the same folder");
    }

    if (isInside(destinationPath, sourcePath)) {
      fail("source folder is inside the destination folder; deleting the destination would remove the source");
    }

    if (isInside(sourcePath, destinationPath)) {
      fail("destination folder must not be inside the source folder");
    }
  }

  for (let index = 0; index < destinationPaths.length; index += 1) {
    for (let otherIndex = index + 1; otherIndex < destinationPaths.length; otherIndex += 1) {
      const destinationPath = destinationPaths[index];
      const otherDestinationPath = destinationPaths[otherIndex];

      if (
        destinationPath === otherDestinationPath ||
        isInside(destinationPath, otherDestinationPath) ||
        isInside(otherDestinationPath, destinationPath)
      ) {
        fail("destination paths MUST be distinct and MUST NOT contain one another");
      }
    }
  }

  for (const destinationPath of destinationPaths) {
    // Remove each destination only after every configured path has been validated.
    if (await pathExists(destinationPath)) {
      await requireDirectory(destinationPath, "destination folder");
      await rm(destinationPath, { recursive: true, force: false });
    }

    await mkdir(dirname(destinationPath), { recursive: true });

    await cp(sourcePath, destinationPath, {
      recursive: true,
      errorOnExist: false,
      force: true,
      preserveTimestamps: true,
    });
  }

  // Step 7: report the completed synchronization and resolved folder paths.
  console.log("Folder synchronized successfully.");
  console.log(`Source: ${sourcePath}`);
  for (const destinationPath of destinationPaths) {
    console.log(`Destination: ${destinationPath}`);
  }
}

try {
  await syncFolder();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

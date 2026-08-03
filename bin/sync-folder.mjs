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

  return { sourcePathValue, destinationPathValue };
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

  const { sourcePathValue, destinationPathValue } = await readConfiguration();
  const sourcePath = isAbsolute(sourcePathValue)
    ? resolve(sourcePathValue)
    : resolve(repositoryDirectory, sourcePathValue);

  if (!isAbsolute(destinationPathValue)) {
    fail(`SYNC_DESTINATION_PATH MUST be absolute: ${destinationPathValue}`);
  }

  const destinationPath = resolve(destinationPathValue);

  // Step 3: validate the source before modifying the destination.
  await requireDirectory(sourcePath, "source folder");

  // Prevent destructive configurations that could remove the source itself.
  if (sourcePath === destinationPath) {
    fail("source and destination resolve to the same folder");
  }

  if (isInside(destinationPath, sourcePath)) {
    fail("source folder is inside the destination folder; deleting the destination would remove the source");
  }

  if (isInside(sourcePath, destinationPath)) {
    fail("destination folder must not be inside the source folder");
  }

  // Step 4: remove the destination only when it already exists.
  if (await pathExists(destinationPath)) {
    await requireDirectory(destinationPath, "destination folder");
    await rm(destinationPath, { recursive: true, force: false });
  }

  // Step 5: create any missing parent directories for the destination.
  await mkdir(dirname(destinationPath), { recursive: true });

  // Step 6: copy the complete source folder to the destination path.
  await cp(sourcePath, destinationPath, {
    recursive: true,
    errorOnExist: false,
    force: true,
    preserveTimestamps: true,
  });

  // Step 7: report the completed synchronization and resolved folder paths.
  console.log("Folder synchronized successfully.");
  console.log(`Source: ${sourcePath}`);
  console.log(`Destination: ${destinationPath}`);
}

try {
  await syncFolder();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

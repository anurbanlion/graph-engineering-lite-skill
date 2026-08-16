#!/usr/bin/env node

import { access, cp, mkdir, readFile, rm, stat } from "node:fs/promises";
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { constants } from "node:fs";
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

  return {
    sourceEntries: parseSourceEntries(sourcePathValue),
    destinationPathValues: parseDestinationPaths(destinationPathValue),
  };
}

function parseJsonArray(value, variableName) {
  let parsed;

  try {
    parsed = JSON.parse(value);
  } catch {
    fail(`${variableName} MUST be a path or a JSON array`);
  }

  if (!Array.isArray(parsed) || parsed.length === 0) {
    fail(`${variableName} JSON array MUST contain one or more entries`);
  }

  return parsed;
}

function parseSourceEntry(entry) {
  if (typeof entry === "string") {
    const path = entry.trim();

    if (!path) {
      fail("SYNC_SOURCE_PATH entries MUST be non-empty paths");
    }

    return { path, destinationName: basename(path) };
  }

  if (entry && typeof entry === "object" && !Array.isArray(entry)) {
    const path = typeof entry.path === "string" ? entry.path.trim() : "";
    const destinationName =
      typeof entry.destinationName === "string" ? entry.destinationName.trim() : basename(path);

    if (!path) {
      fail("SYNC_SOURCE_PATH object entries MUST include a non-empty path");
    }

    if (!destinationName || destinationName.includes("/") || destinationName.includes("\\")) {
      fail(`SYNC_SOURCE_PATH destinationName MUST be a single file or folder name: ${destinationName}`);
    }

    return { path, destinationName };
  }

  fail("SYNC_SOURCE_PATH JSON array entries MUST be paths or objects with path and destinationName");
}

// Accept a single source for compatibility, or a JSON array for multi-source syncs.
function parseSourceEntries(value) {
  const entries = value.startsWith("[") ? parseJsonArray(value, "SYNC_SOURCE_PATH") : [value];
  return entries.map(parseSourceEntry);
}

// Accept a single destination for compatibility, or a JSON array for fan-out syncs.
function parseDestinationPaths(value) {
  const destinations = value.startsWith("[") ? parseJsonArray(value, "SYNC_DESTINATION_PATH") : [value];

  if (destinations.some((destination) => typeof destination !== "string" || !destination.trim())) {
    fail("SYNC_DESTINATION_PATH entries MUST be non-empty paths");
  }

  return destinations.map((destination) => destination.trim());
}

async function requireExistingPath(path, label) {
  try {
    return await stat(path);
  } catch (error) {
    if (error?.code === "ENOENT") {
      fail(`${label} does not exist: ${path}`);
    }

    throw error;
  }
}

// Require an existing directory and explain whether it is missing or invalid.
async function requireDirectory(path, label) {
  const pathStat = await requireExistingPath(path, label);

  if (!pathStat.isDirectory()) {
    fail(`${label} is not a directory: ${path}`);
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

function resolveSourcePath(sourcePathValue) {
  return isAbsolute(sourcePathValue)
    ? resolve(sourcePathValue)
    : resolve(repositoryDirectory, sourcePathValue);
}

function resolveDestinationRoot(destinationPathValue) {
  if (!isAbsolute(destinationPathValue)) {
    fail(`SYNC_DESTINATION_PATH MUST be absolute: ${destinationPathValue}`);
  }

  return resolve(destinationPathValue);
}

function validateDistinctPaths(paths, message) {
  for (let index = 0; index < paths.length; index += 1) {
    for (let otherIndex = index + 1; otherIndex < paths.length; otherIndex += 1) {
      const path = paths[index];
      const otherPath = paths[otherIndex];

      if (path === otherPath || isInside(path, otherPath) || isInside(otherPath, path)) {
        fail(message);
      }
    }
  }
}

async function syncFolder() {
  if (process.argv.length > 2) {
    fail("this script does not accept arguments; configure .env in the repository root");
  }

  const { sourceEntries, destinationPathValues } = await readConfiguration();
  const sources = [];

  for (const sourceEntry of sourceEntries) {
    const sourcePath = resolveSourcePath(sourceEntry.path);
    const sourceStat = await requireExistingPath(sourcePath, "source path");

    sources.push({ ...sourceEntry, sourcePath, isDirectory: sourceStat.isDirectory() });
  }

  validateDistinctPaths(
    sources.map((source) => source.sourcePath),
    "source paths MUST be distinct and MUST NOT contain one another",
  );

  const destinationRoots = destinationPathValues.map(resolveDestinationRoot);
  validateDistinctPaths(
    destinationRoots,
    "destination paths MUST be distinct and MUST NOT contain one another",
  );

  const plannedCopies = [];
  const plannedDestinationPaths = [];

  for (const destinationRoot of destinationRoots) {
    for (const source of sources) {
      const destinationPath = resolve(destinationRoot, source.destinationName);

      if (!isInside(destinationRoot, destinationPath)) {
        fail(`resolved destination MUST stay inside destination root: ${destinationPath}`);
      }

      for (const otherSource of sources) {
        if (destinationPath === otherSource.sourcePath || isInside(destinationPath, otherSource.sourcePath)) {
          fail("destination path must not contain a source path");
        }

        if (isInside(otherSource.sourcePath, destinationPath)) {
          fail("destination path must not be inside a source path");
        }
      }

      plannedCopies.push({ ...source, destinationRoot, destinationPath });
      plannedDestinationPaths.push(destinationPath);
    }
  }

  validateDistinctPaths(
    plannedDestinationPaths,
    "resolved destination paths MUST be distinct and MUST NOT contain one another",
  );

  for (const destinationRoot of destinationRoots) {
    await mkdir(destinationRoot, { recursive: true });
    await requireDirectory(destinationRoot, "destination root");
  }

  for (const plannedCopy of plannedCopies) {
    if (await pathExists(plannedCopy.destinationPath)) {
      await rm(plannedCopy.destinationPath, { recursive: true, force: false });
    }

    await mkdir(dirname(plannedCopy.destinationPath), { recursive: true });
    await cp(plannedCopy.sourcePath, plannedCopy.destinationPath, {
      recursive: plannedCopy.isDirectory,
      errorOnExist: false,
      force: true,
      preserveTimestamps: true,
    });
  }

  console.log("Sources synchronized successfully.");
  for (const plannedCopy of plannedCopies) {
    console.log(`Source: ${plannedCopy.sourcePath}`);
    console.log(`Destination: ${plannedCopy.destinationPath}`);
  }
}

try {
  await syncFolder();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

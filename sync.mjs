#!/usr/bin/env node

import { access, cp, mkdir, rm, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";

// Report a clear error and terminate with a non-zero exit code.
function fail(message) {
  console.error(`sync: ${message}`);
  process.exit(1);
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
  // Step 1: read the only two supported inputs: source and destination folders.
  const [sourcePathArgument, destinationPathArgument, ...extraArguments] =
    process.argv.slice(2);

  if (!sourcePathArgument || !destinationPathArgument || extraArguments.length > 0) {
    fail("usage: node sync.mjs <source-path> <destination-path>");
  }

  // Step 2: require explicit absolute paths from the wrapper and normalize them.
  if (!isAbsolute(sourcePathArgument)) {
    fail(`source path must be absolute: ${sourcePathArgument}`);
  }

  if (!isAbsolute(destinationPathArgument)) {
    fail(`destination path must be absolute: ${destinationPathArgument}`);
  }

  const sourcePath = resolve(sourcePathArgument);
  const destinationPath = resolve(destinationPathArgument);

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

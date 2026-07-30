#!/usr/bin/env node

import { access, cp, mkdir, rm, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";

// Report a clear error and terminate with a non-zero exit code.
function fail(message) {
  console.error(`sync-folder: ${message}`);
  process.exit(1);
}

// Validate that the requested folder path is relative and cannot traverse
// outside either project through ".." segments.
function validateRelativePath(value) {
  if (!value || isAbsolute(value)) {
    fail("the folder path must be a non-empty relative path");
  }

  const segments = value.split(/[\\/]+/);

  if (segments.some((segment) => segment === "..")) {
    fail("the folder path must not contain '..' segments");
  }
}

// Confirm that a resolved child path remains inside its expected project root.
function isInside(parentPath, childPath) {
  const pathFromParent = relative(parentPath, childPath);
  return (
    pathFromParent === "" ||
    (!pathFromParent.startsWith(`..${sep}`) && pathFromParent !== ".." && !isAbsolute(pathFromParent))
  );
}

// Require an existing directory and provide a specific error for missing or
// invalid source and destination locations.
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

// Check whether the destination folder already exists without treating a
// missing path as an error.
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

async function syncFolder() {
  // Step 1: read and validate the three arguments supplied by the shell wrapper.
  const [sourceProjectArgument, destinationProjectArgument, relativeFolderArgument] =
    process.argv.slice(2);

  if (!sourceProjectArgument || !destinationProjectArgument || !relativeFolderArgument) {
    fail(
      "usage: node sync-folder.mjs <source-project-absolute-path> <destination-project-absolute-path> <folder-relative-path>"
    );
  }

  if (!isAbsolute(sourceProjectArgument)) {
    fail("the source project path must be absolute");
  }

  if (!isAbsolute(destinationProjectArgument)) {
    fail("the destination project path must be absolute");
  }

  validateRelativePath(relativeFolderArgument);

  // Step 2: normalize both project roots and resolve the same relative folder
  // inside the source and destination projects.
  const sourceProject = resolve(sourceProjectArgument);
  const destinationProject = resolve(destinationProjectArgument);
  const sourceFolder = resolve(sourceProject, relativeFolderArgument);
  const destinationFolder = resolve(destinationProject, relativeFolderArgument);

  // Step 3: verify both project roots exist and are directories.
  await requireDirectory(sourceProject, "source project");
  await requireDirectory(destinationProject, "destination project");

  // Step 4: protect against any path that resolves outside its project root.
  if (!isInside(sourceProject, sourceFolder)) {
    fail("the source folder resolves outside the source project");
  }

  if (!isInside(destinationProject, destinationFolder)) {
    fail("the destination folder resolves outside the destination project");
  }

  // Step 5: verify the source folder before modifying the destination. If the
  // source is missing or invalid, the script stops without deleting anything.
  await requireDirectory(sourceFolder, "source folder");

  if (sourceFolder === destinationFolder) {
    fail("source and destination folders resolve to the same path");
  }

  // Step 6: remove the destination folder only when it already exists.
  if (await pathExists(destinationFolder)) {
    await rm(destinationFolder, { recursive: true, force: false });
  }

  // Step 7: create intermediate directories required by the relative path.
  await mkdir(dirname(destinationFolder), { recursive: true });

  // Step 8: copy the complete source folder into the destination project while
  // preserving timestamps and replacing files when necessary.
  await cp(sourceFolder, destinationFolder, {
    recursive: true,
    errorOnExist: false,
    force: true,
    preserveTimestamps: true,
  });

  // Step 9: report the completed synchronization and the resolved paths.
  console.log("Folder synchronized successfully.");
  console.log(`Source: ${sourceFolder}`);
  console.log(`Destination: ${destinationFolder}`);
}

try {
  await syncFolder();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

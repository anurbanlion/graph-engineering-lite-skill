#!/usr/bin/env node

import { access, cp, mkdir, rm, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";

function fail(message) {
  console.error(`sync-folder: ${message}`);
  process.exit(1);
}

function validateRelativePath(value) {
  if (!value || isAbsolute(value)) {
    fail("the folder path must be a non-empty relative path");
  }

  const segments = value.split(/[\\/]+/);

  if (segments.some((segment) => segment === "..")) {
    fail("the folder path must not contain '..' segments");
  }
}

function isInside(parentPath, childPath) {
  const pathFromParent = relative(parentPath, childPath);
  return (
    pathFromParent === "" ||
    (!pathFromParent.startsWith(`..${sep}`) && pathFromParent !== ".." && !isAbsolute(pathFromParent))
  );
}

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

  const sourceProject = resolve(sourceProjectArgument);
  const destinationProject = resolve(destinationProjectArgument);
  const sourceFolder = resolve(sourceProject, relativeFolderArgument);
  const destinationFolder = resolve(destinationProject, relativeFolderArgument);

  await requireDirectory(sourceProject, "source project");
  await requireDirectory(destinationProject, "destination project");

  if (!isInside(sourceProject, sourceFolder)) {
    fail("the source folder resolves outside the source project");
  }

  if (!isInside(destinationProject, destinationFolder)) {
    fail("the destination folder resolves outside the destination project");
  }

  // The source is checked before the destination is removed. If the source is
  // missing or is not a directory, the script stops without modifying anything.
  await requireDirectory(sourceFolder, "source folder");

  if (sourceFolder === destinationFolder) {
    fail("source and destination folders resolve to the same path");
  }

  if (await pathExists(destinationFolder)) {
    await rm(destinationFolder, { recursive: true, force: false });
  }

  await mkdir(dirname(destinationFolder), { recursive: true });
  await cp(sourceFolder, destinationFolder, {
    recursive: true,
    errorOnExist: false,
    force: true,
    preserveTimestamps: true,
  });

  console.log(`Folder synchronized successfully.`);
  console.log(`Source: ${sourceFolder}`);
  console.log(`Destination: ${destinationFolder}`);
}

try {
  await syncFolder();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}

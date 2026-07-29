#!/usr/bin/env node

// scripts/list-graphs.mjs

import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "list-graphs";
const paths = resolvePaths(import.meta.url);
const graphsDirectory = join(paths.skillDirectory, "graphs");

async function listGraphs() {
  const entries = await readdir(graphsDirectory, {
    withFileTypes: true,
  });

  return entries
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

try {
  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
  });

  const graphs = await listGraphs();

  if (graphs.length === 0) {
    console.log("No graphs available.");
    process.exit(0);
  }

  console.log(graphs.join("\n"));
} catch (error) {
  if (error?.code === "ENOENT") {
    console.log("No graphs directory found.");
    process.exit(0);
  }

  console.error("Failed to list graphs:", error);
  process.exit(1);
}
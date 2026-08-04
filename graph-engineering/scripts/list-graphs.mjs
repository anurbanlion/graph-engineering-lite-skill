#!/usr/bin/env node

// scripts/list-graphs.mjs

import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { findGraphPaths } from "./lib/graphs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "list-graphs";
const paths = resolvePaths(import.meta.url);

async function main() {
  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
  });

  const graphs = findGraphPaths(paths.graphsDirectory).sort();

  if (graphs.length === 0) {
    console.log("No graphs available.");
    process.exit(0);
  }

  console.log(graphs.join("\n"));
}

try {
  await main();
} catch (error) {
  if (error?.code === "ENOENT") {
    console.log("No graphs directory found.");
    process.exit(0);
  }

  console.error("Failed to list graphs:", error);
  process.exit(1);
}

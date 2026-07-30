#!/usr/bin/env node

// scripts/read-graphs.mjs

import { readFile } from "node:fs/promises";
import { join, resolve, sep } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "read-graphs";
const paths = resolvePaths(import.meta.url);
const graphsDirectory = join(paths.skillDirectory, "graphs");
const graphNames = process.argv.slice(2);

function getGraphFile(graphName) {
  if (
    !graphName ||
    graphName === "." ||
    graphName === ".." ||
    graphName.includes("/") ||
    graphName.includes("\\")
  ) {
    throw new Error(`Invalid graph name: ${graphName}`);
  }

  const graphsRoot = resolve(graphsDirectory);
  const graphDirectory = resolve(graphsRoot, graphName);
  const allowedPrefix = `${graphsRoot}${sep}`;

  if (!graphDirectory.startsWith(allowedPrefix)) {
    throw new Error(`Invalid graph path: ${graphName}`);
  }

  return join(graphDirectory, "GRAPH.json");
}

async function readGraph(graphName) {
  try {
    return await readFile(getGraphFile(graphName), "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new Error(`Graph not found: ${graphName}`);
    }

    throw error;
  }
}

await writeExecutionLog({
  scriptName: SCRIPT_NAME,
  logsDirectory: paths.logsDirectory,
  logFile: paths.logFile,
  metadata: {
    graphs: graphNames,
  },
});

if (graphNames.length === 0) {
  console.error(
    "Usage: node scripts/read-graphs.mjs <graph-name> [additional-graph-name...]"
  );
  process.exit(1);
}

let hasErrors = false;

for (const graphName of graphNames) {
  try {
    const definition = await readGraph(graphName);

    console.log(`===== GRAPH: ${graphName} =====`);
    console.log(definition.trim());
    console.log(`===== END GRAPH: ${graphName} =====`);
  } catch (error) {
    hasErrors = true;
    console.error(error.message);
  }
}

if (hasErrors) {
  process.exit(1);
}
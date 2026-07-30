#!/usr/bin/env node

// scripts/list-jobs.mjs

import { readdir } from "node:fs/promises";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "list-jobs";
const paths = resolvePaths(import.meta.url);

async function listJobs() {
  const entries = await readdir(paths.jobsDirectory, {
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

  const jobs = await listJobs();

  if (jobs.length === 0) {
    console.log("No jobs available.");
    process.exit(0);
  }

  console.log(jobs.join("\n"));
} catch (error) {
  if (error?.code === "ENOENT") {
    console.log("No jobs directory found.");
    process.exit(0);
  }

  console.error("Failed to list jobs:", error);
  process.exit(1);
}
#!/usr/bin/env node

// scripts/read-jobs.mjs

import { readFile } from "node:fs/promises";
import { isAbsolute, join, relative, resolve, sep } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "read-jobs";
const paths = resolvePaths(import.meta.url);

// Resolves a relative job path without allowing it to escape jobs/.
function getJobFile(jobPath) {
  if (!jobPath || isAbsolute(jobPath)) {
    throw new Error(`Invalid job path: ${jobPath}`);
  }

  const jobsRoot = resolve(paths.jobsDirectory);
  const jobDirectory = resolve(jobsRoot, jobPath);
  const pathFromJobsRoot = relative(jobsRoot, jobDirectory);

  if (
    !pathFromJobsRoot ||
    pathFromJobsRoot === ".." ||
    pathFromJobsRoot.startsWith(`..${sep}`)
  ) {
    throw new Error(`Invalid job path: ${jobPath}`);
  }

  return join(jobDirectory, "JOB.md");
}

// Reads one job definition from a path relative to jobs/.
async function readJob(jobPath) {
  try {
    return await readFile(getJobFile(jobPath), "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new Error(`Job not found: ${jobPath}`);
    }

    throw error;
  }
}

async function main() {
  const jobPaths = process.argv.slice(2);

  // Record the requested paths before reading their JOB.md files.
  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      jobs: jobPaths,
    },
  });

  if (jobPaths.length === 0) {
    console.error(
      "Usage: node scripts/read-jobs.mjs <job-path> [additional-job-path...]"
    );
    process.exit(1);
  }

  let hasErrors = false;

  for (const jobPath of jobPaths) {
    try {
      const definition = await readJob(jobPath);

      console.log(`===== JOB: ${jobPath} =====`);
      console.log(definition.trim());
      console.log(`===== END JOB: ${jobPath} =====`);
    } catch (error) {
      hasErrors = true;
      console.error(error.message);
    }
  }

  if (hasErrors) {
    process.exit(1);
  }
}

try {
  await main();
} catch (error) {
  console.error("Failed to read jobs:", error);
  process.exit(1);
}

#!/usr/bin/env node

// scripts/read-jobs.mjs

import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolveJobPath } from "./lib/jobs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "read-jobs";
const paths = resolvePaths(import.meta.url);

// Resolves a unique job name to its JOB.md file.
function getJobFile(jobName) {
  return join(
    paths.jobsDirectory,
    resolveJobPath(paths.jobsDirectory, jobName),
    "JOB.md"
  );
}

// Reads one job definition by name, regardless of its group.
async function readJob(jobName) {
  try {
    return await readFile(getJobFile(jobName), "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new Error(`Job not found: ${jobName}`);
    }

    throw error;
  }
}

async function main() {
  const jobNames = process.argv.slice(2);

  // Record the requested job names before reading their JOB.md files.
  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      jobs: jobNames,
    },
  });

  if (jobNames.length === 0) {
    console.error(
      "Usage: node scripts/read-jobs.mjs <job-name> [additional-job-name...]"
    );
    process.exit(1);
  }

  let hasErrors = false;

  for (const jobName of jobNames) {
    try {
      const definition = await readJob(jobName);

      console.log(`===== JOB: ${jobName} =====`);
      console.log(definition.trim());
      console.log(`===== END JOB: ${jobName} =====`);
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

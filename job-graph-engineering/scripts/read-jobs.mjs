#!/usr/bin/env node

// scripts/read-jobs.mjs

import { readFile } from "node:fs/promises";
import { join, resolve, sep } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "read-jobs";
const paths = resolvePaths(import.meta.url);
const jobNames = process.argv.slice(2);

function getJobFile(jobName) {
  if (
    !jobName ||
    jobName === "." ||
    jobName === ".." ||
    jobName.includes("/") ||
    jobName.includes("\\")
  ) {
    throw new Error(`Invalid job name: ${jobName}`);
  }

  const jobsRoot = resolve(paths.jobsDirectory);
  const jobDirectory = resolve(jobsRoot, jobName);
  const allowedPrefix = `${jobsRoot}${sep}`;

  if (!jobDirectory.startsWith(allowedPrefix)) {
    throw new Error(`Invalid job path: ${jobName}`);
  }

  return join(jobDirectory, "JOB.md");
}

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
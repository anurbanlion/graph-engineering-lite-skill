#!/usr/bin/env node

import { mkdir } from "node:fs/promises";
import { join } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "resolve-output-path";
const paths = resolvePaths(import.meta.url);

const [runName, jobName] = process.argv.slice(2);

function validateName(value, label) {
  const kebabCasePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

  if (!value || !kebabCasePattern.test(value)) {
    throw new Error(
      `${label} MUST be a non-empty kebab-case identifier.`
    );
  }
}

function getGmtMinusFiveTimestamp() {
  const adjustedTime = new Date(Date.now() - 5 * 60 * 60 * 1000);

  const year = adjustedTime.getUTCFullYear();
  const month = String(adjustedTime.getUTCMonth() + 1).padStart(2, "0");
  const day = String(adjustedTime.getUTCDate()).padStart(2, "0");
  const hour = String(adjustedTime.getUTCHours()).padStart(2, "0");
  const minute = String(adjustedTime.getUTCMinutes()).padStart(2, "0");

  return `${year}${month}${day}-${hour}${minute}`;
}

async function resolveOutputPath() {
  validateName(runName, "run-name");
  validateName(jobName, "job-name");

  const outputDirectory = join(
    paths.projectDataDirectory,
    "runs",
    runName,
    jobName
  );

  const outputFile = join(
    outputDirectory,
    `OUTPUT-${getGmtMinusFiveTimestamp()}.md`
  );

  await mkdir(outputDirectory, { recursive: true });

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      run: runName,
      job: jobName,
      output: outputFile,
    },
  });

  console.log(outputFile);
}

try {
  await resolveOutputPath();
} catch (error) {
  console.error(`Failed to resolve output path: ${error.message}`);
  process.exit(1);
}
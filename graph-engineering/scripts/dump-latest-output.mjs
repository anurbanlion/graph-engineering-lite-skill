#!/usr/bin/env node

import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "dump-latest-output";
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

async function dumpLatestOutput() {
  validateName(runName, "domain");
  validateName(jobName, "job-name");

  const outputDirectory = join(
    paths.projectDataDirectory,
    "runs",
    runName,
    jobName
  );

  let files;
  try {
    files = await readdir(outputDirectory);
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new Error(`No outputs found for domain "${runName}" and job "${jobName}".`);
    }
    throw error;
  }

  const outputFiles = files
    .filter((f) => f.startsWith("OUTPUT-") && f.endsWith(".md"))
    .sort()
    .reverse();

  if (outputFiles.length === 0) {
    throw new Error(`No output files found for domain "${runName}" and job "${jobName}".`);
  }

  const latestFile = join(outputDirectory, outputFiles[0]);
  const content = await readFile(latestFile, "utf8");

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      domain: runName,
      job: jobName,
      latestOutput: latestFile,
    },
  });

  console.log(`===== LATEST MANAGED OUTPUT: ${runName} / ${jobName} (${outputFiles[0]}) =====`);
  console.log(content.trim());
  console.log(`===== END LATEST MANAGED OUTPUT =====`);
}

try {
  await dumpLatestOutput();
} catch (error) {
  console.error(`Failed to dump latest output: ${error.message}`);
  process.exit(1);
}

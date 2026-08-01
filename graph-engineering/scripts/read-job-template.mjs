#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "read-job-template";
const paths = resolvePaths(import.meta.url);

async function readJobTemplate() {
  const templatePath = join(
    paths.skillDirectory,
    "templates",
    "job-template.md"
  );

  let content;
  try {
    content = await readFile(templatePath, "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new Error(`Job template file not found at: ${templatePath}`);
    }
    throw error;
  }

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      templatePath,
    },
  });

  console.log("===== JOB TEMPLATE =====");
  console.log(content.trim());
  console.log("===== END JOB TEMPLATE =====");
}

try {
  await readJobTemplate();
} catch (error) {
  console.error(`Failed to read job template: ${error.message}`);
  process.exit(1);
}

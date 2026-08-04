#!/usr/bin/env node

// Lists job directory names so callers can choose a valid job before reading it.

import { existsSync, readdirSync } from "node:fs";
import { join, relative } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

// Identifies this invocation in the skill's execution log.
const SCRIPT_NAME = "list-jobs";

// `import.meta.url` is the absolute file URL of this module, e.g. `"file:///C:/Users/.../graph-engineering/"`
// `resolvePaths` contains every path this script needs, e.g. `paths.jobsDirectory`
const paths = resolvePaths(import.meta.url);

function findJobs(directory) {
  // A directory with JOB.md is a job; otherwise, search its child directories.
  return readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const jobDirectory = join(directory, entry.name);

      if (existsSync(join(jobDirectory, "JOB.md"))) {
        return relative(paths.jobsDirectory, jobDirectory);
      }

      return findJobs(jobDirectory);
    })
    .flat();
}

async function main() {
  // Record the invocation, then print every job path relative to jobs/.
  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
  });

  const jobs = findJobs(paths.jobsDirectory).sort();

  if (jobs.length === 0) {
    // An empty jobs directory is a valid state, not an execution failure.
    console.log("No jobs available.");
    process.exit(0);
  }

  // Print one name per line so the output can be used directly as a job list.
  console.log(jobs.join("\n"));
}

try {
  await main();
} catch (error) {
  // A missing jobs directory is treated like an empty registry. Other errors
  // (such as permission failures) remain failures and preserve their context.
  if (error?.code === "ENOENT") {
    console.log("No jobs directory found.");
    process.exit(0);
  }

  console.error("Failed to list jobs:", error);
  process.exit(1);
}

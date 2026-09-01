#!/usr/bin/env node

import { readdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { writeExecutionLog } from "../lib/activity-logs.mjs";
import { resolvePaths } from "../lib/resolve-paths.mjs";

const SCRIPT_NAME = "compile-application-journeys";
const JOURNEY_SUFFIX = "-journey";

const paths = resolvePaths(import.meta.url);
const [outputPathArgument] = process.argv.slice(2);

/**
 * Compiles the application's journey names from existing run directories.
 *
 * Flow:
 * - Resolve the managed runs directory from the current project folder.
 * - Read only directory entries inside `.job-graph-engineering/runs`.
 * - Select directory names ending in `-journey`.
 * - Remove the `-journey` suffix and discard empty names.
 * - Sort the resulting journey names alphabetically.
 * - Format the names as the job's Markdown output.
 * - Write the output to the path previously resolved by
 *   `resolve-output-path.mjs`.
 * - Print one structured JSON result for downstream graph jobs.
 */
async function findJourneys() {
  const runsDirectory = join(paths.projectDataDirectory, "runs");

  try {
    const entries = await readdir(runsDirectory, { withFileTypes: true });

    return entries
      .filter(
        (entry) => entry.isDirectory() && entry.name.endsWith(JOURNEY_SUFFIX)
      )
      .map((entry) => entry.name.slice(0, -JOURNEY_SUFFIX.length))
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b));
  } catch (error) {
    if (error?.code === "ENOENT") {
      return [];
    }

    throw error;
  }
}

function formatOutput(journeys) {
  const lines =
    journeys.length > 0
      ? journeys.map((journey) => `- ${journey}`)
      : ["No journeys found."];

  return `# Application Journeys\n\n${lines.join("\n")}\n`;
}

async function compileApplicationJourneys() {
  if (!outputPathArgument) {
    throw new Error(
      "Usage: node scripts/custom/compile-application-journeys.mjs <output-path>"
    );
  }

  const outputPath = resolve(outputPathArgument);
  const journeys = await findJourneys();
  const content = formatOutput(journeys);

  await writeFile(outputPath, content, "utf8");

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      output: outputPath,
      journeys,
    },
  });

  console.log(JSON.stringify({ outputPath, journeys }));
}

try {
  await compileApplicationJourneys();
} catch (error) {
  console.error(`Failed to compile application journeys: ${error.message}`);
  process.exit(1);
}

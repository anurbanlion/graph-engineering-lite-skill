#!/usr/bin/env node

import { readdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { writeExecutionLog } from "../lib/activity-logs.mjs";
import { resolvePaths } from "../lib/resolve-paths.mjs";

const SCRIPT_NAME = "list-application-journeys";
const JOURNEY_SUFFIX = "-journey";

const paths = resolvePaths(import.meta.url);
const [outputPathArgument] = process.argv.slice(2);

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

async function listApplicationJourneys() {
  if (!outputPathArgument) {
    throw new Error(
      "Usage: node scripts/custom/list-application-journeys.mjs <output-path>"
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

  process.stdout.write(content);
  console.log(outputPath);
}

try {
  await listApplicationJourneys();
} catch (error) {
  console.error(`Failed to list application journeys: ${error.message}`);
  process.exit(1);
}

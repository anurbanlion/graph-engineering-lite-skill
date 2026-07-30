#!/usr/bin/env node

import { mkdir, readdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { writeExecutionLog } from "../lib/activity-logs.mjs";
import { resolvePaths } from "../lib/resolve-paths.mjs";

const SCRIPT_NAME = "list-application-journeys";
const JOB_NAME = "list-application-journeys";
const DEFAULT_DOMAIN = "global-designs";
const JOURNEY_SUFFIX = "-journey";

const paths = resolvePaths(import.meta.url);
const [domainArgument] = process.argv.slice(2);
const domain = domainArgument || DEFAULT_DOMAIN;

function validateDomain(value) {
  const kebabCasePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

  if (!kebabCasePattern.test(value)) {
    throw new Error("domain MUST be a non-empty kebab-case identifier.");
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

async function findJourneys() {
  const runsDirectory = join(paths.projectDataDirectory, "runs");

  try {
    const entries = await readdir(runsDirectory, { withFileTypes: true });

    return entries
      .filter((entry) => entry.isDirectory() && entry.name.endsWith(JOURNEY_SUFFIX))
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
  const lines = journeys.length > 0
    ? journeys.map((journey) => `- ${journey}`)
    : ["No journeys found."];

  return `# Application Journeys\n\n${lines.join("\n")}\n`;
}

async function listApplicationJourneys() {
  validateDomain(domain);

  const journeys = await findJourneys();
  const outputDirectory = join(
    paths.projectDataDirectory,
    "runs",
    domain,
    JOB_NAME
  );
  const outputPath = join(
    outputDirectory,
    `OUTPUT-${getGmtMinusFiveTimestamp()}.md`
  );
  const content = formatOutput(journeys);

  await mkdir(outputDirectory, { recursive: true });
  await writeFile(outputPath, content, "utf8");

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      domain,
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

#!/usr/bin/env node

import { mkdir, open, stat } from "node:fs/promises";
import { dirname, join } from "node:path";
import { writeExecutionLog } from "../lib/activity-logs.mjs";
import { resolvePaths } from "../lib/resolve-paths.mjs";

const SCRIPT_NAME = "scaffold-journey-architecture";
const IDENTIFIER_PATTERN = /^[a-z]+(?:-[a-z]+)*$/;

const paths = resolvePaths(import.meta.url);

function fail(message) {
  throw new Error(message);
}

function parseJourneys(argumentsList) {
  const journeys = [];

  for (let index = 0; index < argumentsList.length; index += 1) {
    const option = argumentsList[index];

    if (option !== "--journey") {
      fail(`Unknown option: ${option}`);
    }

    const journey = argumentsList[index + 1];

    if (!journey || journey.startsWith("--")) {
      fail('Each "--journey" option MUST be followed by an identifier.');
    }

    if (!IDENTIFIER_PATTERN.test(journey)) {
      fail(`Invalid journey identifier: ${journey}`);
    }

    journeys.push(journey);
    index += 1;
  }

  if (journeys.length === 0) {
    fail('At least one "--journey <identifier>" input is required.');
  }

  return [...new Set(journeys)];
}

function getJourneyFiles(journey) {
  const journeyRoot = join(paths.projectDirectory, "apps", "storefront", "apis", journey);

  return [
    join(journeyRoot, "index.ts"),
    join(journeyRoot, "domain", "contracts", `${journey}.contract.ts`),
    join(
      journeyRoot,
      "infrastructure",
      "services",
      `${journey}.service.const.ts`
    ),
    join(
      journeyRoot,
      "infrastructure",
      "services",
      `${journey}.mock.service.ts`
    ),
    join(
      journeyRoot,
      "infrastructure",
      "services",
      `${journey}.service.ts`
    ),
    join(
      journeyRoot,
      "infrastructure",
      "repository",
      `${journey}.factory.ts`
    ),
    join(
      journeyRoot,
      "infrastructure",
      "repository",
      `${journey}.repository.ts`
    ),
    join(
      journeyRoot,
      "infrastructure",
      "repository",
      `${journey}.mock.repository.ts`
    ),
    join(
      journeyRoot,
      "application",
      "use-cases",
      `${journey}.use-case.ts`
    ),
  ];
}

async function ensureEmptyFile(filePath) {
  await mkdir(dirname(filePath), { recursive: true });

  try {
    const handle = await open(filePath, "wx");
    await handle.close();
    return "created";
  } catch (error) {
    if (error?.code !== "EEXIST") {
      throw error;
    }

    const fileStat = await stat(filePath);

    if (!fileStat.isFile()) {
      fail(`Expected a file but found another resource: ${filePath}`);
    }

    return "existing";
  }
}

async function scaffoldJourneyArchitecture() {
  const journeys = parseJourneys(process.argv.slice(2));
  let createdCount = 0;
  let existingCount = 0;

  for (const journey of journeys) {
    for (const filePath of getJourneyFiles(journey)) {
      const result = await ensureEmptyFile(filePath);

      if (result === "created") {
        createdCount += 1;
      } else {
        existingCount += 1;
      }
    }
  }

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      journeys,
      filesCreated: createdCount,
      filesAlreadyExisting: existingCount,
    },
  });

  console.log(
    createdCount === 0
      ? "Journey architecture already exists."
      : "Journey architecture ensured successfully."
  );
  console.log(`Journeys processed: ${journeys.join(", ")}.`);
  console.log(`Files created: ${createdCount}.`);
  console.log(`Files already existing: ${existingCount}.`);
}

try {
  await scaffoldJourneyArchitecture();
} catch (error) {
  console.error(
    `Failed to scaffold journey architecture: ${
      error instanceof Error ? error.message : String(error)
    }`
  );
  process.exit(1);
}

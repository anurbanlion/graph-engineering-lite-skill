#!/usr/bin/env node

import { readdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { writeExecutionLog } from "../lib/activity-logs.mjs";
import { resolvePaths } from "../lib/resolve-paths.mjs";

const SCRIPT_NAME = "compile-application-use-cases";
const SOURCE_JOB_NAME = "analyze-journey-use-cases";

const paths = resolvePaths(import.meta.url);
const [outputPathArgument] = process.argv.slice(2);

async function getLatestOutput(runName) {
  const sourceDirectory = join(
    paths.projectDataDirectory,
    "runs",
    runName,
    SOURCE_JOB_NAME
  );

  try {
    const entries = await readdir(sourceDirectory);

    const latestOutput = entries
      .filter((name) => /^OUTPUT-\d{8}-\d{4}\.md$/.test(name))
      .sort()
      .at(-1);

    if (!latestOutput) {
      return null;
    }

    const sourcePath = join(sourceDirectory, latestOutput);

    return {
      runName,
      sourcePath,
      content: await readFile(sourcePath, "utf8"),
    };
  } catch (error) {
    if (error?.code === "ENOENT") {
      return null;
    }

    throw error;
  }
}

async function findLatestOutputs() {
  const runsDirectory = join(paths.projectDataDirectory, "runs");

  const entries = await readdir(runsDirectory, {
    withFileTypes: true,
  });

  const outputs = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }

    const output = await getLatestOutput(entry.name);

    if (output) {
      outputs.push(output);
    }
  }

  return outputs.sort((a, b) =>
    a.runName.localeCompare(b.runName)
  );
}

async function compileApplicationUseCases() {
  if (!outputPathArgument) {
    throw new Error(
      "Usage: node scripts/compile-application-use-cases.mjs <output-path>"
    );
  }

  const outputPath = resolve(outputPathArgument);
  const sourceOutputs = await findLatestOutputs();

  if (sourceOutputs.length === 0) {
    throw new Error(
      `No outputs were found for ${SOURCE_JOB_NAME}.`
    );
  }

  const compiledContent = sourceOutputs
    .map(({ runName, content }) => {
      return `# ${runName}\n\n${content.trim()}`;
    })
    .join("\n\n");

  await writeFile(outputPath, `${compiledContent}\n`, "utf8");

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      output: outputPath,
      sources: sourceOutputs.map(({ runName }) => runName),
    },
  });

  console.log(outputPath);
}

try {
  await compileApplicationUseCases();
} catch (error) {
  console.error(
    `Failed to compile application use cases: ${error.message}`
  );

  process.exit(1);
}
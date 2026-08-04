#!/usr/bin/env node

// scripts/validate-graph.mjs

import { readFile } from "node:fs/promises";
import { join, resolve, sep } from "node:path";
import { writeExecutionLog } from "./lib/activity-logs.mjs";
import { resolveJobPath } from "./lib/jobs.mjs";
import { resolvePaths } from "./lib/resolve-paths.mjs";

const SCRIPT_NAME = "validate-graph";
const SUPPORTED_VERSION = "1.0";
const TERMINAL_OUTCOMES = new Set(["complete", "abort"]);

const paths = resolvePaths(import.meta.url);
const [requestedVersion, graphName] = process.argv.slice(2);

function validateResourceName(value, label) {
  const kebabCasePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

  if (!value || !kebabCasePattern.test(value)) {
    throw new Error(
      `${label} MUST be a non-empty kebab-case identifier.`
    );
  }
}

function getGraphFile(name) {
  validateResourceName(name, "graph-name");

  const graphDirectory = resolve(paths.graphsDirectory, name);
  const allowedPrefix = `${resolve(paths.graphsDirectory)}${sep}`;

  if (!graphDirectory.startsWith(allowedPrefix)) {
    throw new Error(`Invalid graph path: ${name}`);
  }

  return join(graphDirectory, "GRAPH.json");
}

async function readGraph(name) {
  const graphFile = getGraphFile(name);

  try {
    const content = await readFile(graphFile, "utf8");

    return {
      graphFile,
      graph: JSON.parse(content),
    };
  } catch (error) {
    if (error?.code === "ENOENT") {
      throw new Error(`Graph not found: ${name}`);
    }

    if (error instanceof SyntaxError) {
      throw new Error(`Invalid JSON in graph: ${name}`);
    }

    throw error;
  }
}

// -----------------------------------------------------------------------------
// 1. Structural validation
// -----------------------------------------------------------------------------

function validateStructure(graph, version) {
  const errors = [];

  if (!graph || typeof graph !== "object" || Array.isArray(graph)) {
    return ["The graph definition MUST be a JSON object."];
  }

  if (typeof graph.name !== "string" || graph.name.length === 0) {
    errors.push('"name" MUST be a non-empty string.');
  }

  if (typeof graph.version !== "string" || graph.version.length === 0) {
    errors.push('"version" MUST be a non-empty string.');
  }

  if (typeof graph.initial !== "string" || graph.initial.length === 0) {
    errors.push('"initial" MUST be a non-empty string.');
  }

  if (
    !graph.jobs ||
    typeof graph.jobs !== "object" ||
    Array.isArray(graph.jobs)
  ) {
    errors.push('"jobs" MUST be a non-null object.');
    return errors;
  }

  if (Object.keys(graph.jobs).length === 0) {
    errors.push('"jobs" MUST contain at least one job.');
  }

  if (version !== SUPPORTED_VERSION) {
    errors.push(
      `Unsupported requested version "${version}". Supported version: "${SUPPORTED_VERSION}".`
    );
  }

  if (graph.version !== version) {
    errors.push(
      `Graph version "${graph.version}" does not match requested version "${version}".`
    );
  }

  if (graph.name !== graphName) {
    errors.push(
      `Graph name "${graph.name}" does not match directory name "${graphName}".`
    );
  }

  for (const [jobName, jobDefinition] of Object.entries(graph.jobs)) {
    try {
      validateResourceName(jobName, `job name "${jobName}"`);
    } catch (error) {
      errors.push(error.message);
    }

    if (
      !jobDefinition ||
      typeof jobDefinition !== "object" ||
      Array.isArray(jobDefinition)
    ) {
      errors.push(`Job "${jobName}" MUST be an object.`);
      continue;
    }

    if (
      typeof jobDefinition.onDone !== "string" ||
      jobDefinition.onDone.length === 0
    ) {
      errors.push(`Job "${jobName}" MUST define a non-empty "onDone".`);
    }

    if (
      typeof jobDefinition.onError !== "string" ||
      jobDefinition.onError.length === 0
    ) {
      errors.push(`Job "${jobName}" MUST define a non-empty "onError".`);
    }

    if (jobDefinition.instructions !== undefined) {
      const instructionsAreValid =
        typeof jobDefinition.instructions === "string" ||
        (
          Array.isArray(jobDefinition.instructions) &&
          jobDefinition.instructions.length > 0 &&
          jobDefinition.instructions.every(
            (instruction) =>
              typeof instruction === "string" &&
              instruction.trim().length > 0
          )
        );

      if (!instructionsAreValid) {
        errors.push(
          `Job "${jobName}" instructions MUST be a non-empty string or a non-empty array of strings.`
        );
      }
    }
  }

  return errors;
}

// -----------------------------------------------------------------------------
// 2. Internal reference validation
// -----------------------------------------------------------------------------

function validateReferences(graph) {
  const errors = [];

  if (
    !graph.jobs ||
    typeof graph.jobs !== "object" ||
    Array.isArray(graph.jobs)
  ) {
    return errors;
  }

  const graphJobNames = new Set(Object.keys(graph.jobs));

  if (
    typeof graph.initial === "string" &&
    !graphJobNames.has(graph.initial)
  ) {
    errors.push(
      `"initial" references undefined graph job "${graph.initial}".`
    );
  }

  for (const [jobName, jobDefinition] of Object.entries(graph.jobs)) {
    if (
      !jobDefinition ||
      typeof jobDefinition !== "object" ||
      Array.isArray(jobDefinition)
    ) {
      continue;
    }

    for (const transitionName of ["onDone", "onError"]) {
      const target = jobDefinition[transitionName];

      if (typeof target !== "string" || target.length === 0) {
        continue;
      }

      const referencesGraphJob = graphJobNames.has(target);
      const referencesTerminal = TERMINAL_OUTCOMES.has(target);

      if (!referencesGraphJob && !referencesTerminal) {
        errors.push(
          `Job "${jobName}" has a dangling "${transitionName}" reference to "${target}".`
        );
      }
    }
  }

  return errors;
}

// -----------------------------------------------------------------------------
// 3. Job store validation
// -----------------------------------------------------------------------------

async function validateJobStore(graph) {
  const errors = [];

  if (
    !graph.jobs ||
    typeof graph.jobs !== "object" ||
    Array.isArray(graph.jobs)
  ) {
    return errors;
  }

  for (const jobName of Object.keys(graph.jobs)) {
    try {
      resolveJobPath(paths.jobsDirectory, jobName);
    } catch (error) {
      errors.push(error.message);
    }
  }

  return errors;
}

async function validateGraph() {
  if (!requestedVersion || !graphName) {
    throw new Error(
      "Usage: node scripts/validate-graph.mjs <version> <graph-name>"
    );
  }

  const { graphFile, graph } = await readGraph(graphName);

  const structuralErrors = validateStructure(
    graph,
    requestedVersion
  );

  const referenceErrors = validateReferences(graph);
  const jobStoreErrors = await validateJobStore(graph);

  const errors = [
    ...structuralErrors,
    ...referenceErrors,
    ...jobStoreErrors,
  ];

  await writeExecutionLog({
    scriptName: SCRIPT_NAME,
    logsDirectory: paths.logsDirectory,
    logFile: paths.logFile,
    metadata: {
      version: requestedVersion,
      graph: graphName,
      valid: errors.length === 0,
    },
  });

  if (errors.length > 0) {
    console.error(`Graph validation failed: ${graphName}`);

    for (const error of errors) {
      console.error(`- ${error}`);
    }

    process.exit(1);
  }

  console.log(`Graph is valid: ${graphName}`);
  console.log(`Version: ${requestedVersion}`);
  console.log(`Definition: ${graphFile}`);
}

try {
  await validateGraph();
} catch (error) {
  console.error(`Failed to validate graph: ${error.message}`);
  process.exit(1);
}

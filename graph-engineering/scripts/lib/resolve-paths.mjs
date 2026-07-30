// scripts/lib/resolve-paths.mjs

import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PROJECT_DATA_DIRECTORY = ".job-graph-engineering";

export function resolvePaths(importMetaUrl) {
  const scriptDirectory = dirname(fileURLToPath(importMetaUrl));
  const skillDirectory = resolve(scriptDirectory, "..");

  const projectDirectory = resolve(
    process.env.JGE_PROJECT_ROOT || process.cwd()
  );

  const projectDataDirectory = join(
    projectDirectory,
    PROJECT_DATA_DIRECTORY
  );

  const logsDirectory = join(projectDataDirectory, "logs");

  return {
    skillDirectory,
    scriptDirectory,
    projectDirectory,
    projectDataDirectory,
    jobsDirectory: join(skillDirectory, "jobs"),
    graphsDirectory: join(skillDirectory, "graphs"),
    logsDirectory,
    logFile: join(logsDirectory, "activity.log"),
  };
}
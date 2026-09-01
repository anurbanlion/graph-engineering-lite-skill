import { existsSync, readdirSync } from "node:fs";
import { join, relative, sep } from "node:path";

// Returns every job directory as a path relative to jobs/.
export function findJobPaths(jobsDirectory, directory = jobsDirectory) {
  return readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const jobDirectory = join(directory, entry.name);

      if (existsSync(join(jobDirectory, "JOB.md"))) {
        return relative(jobsDirectory, jobDirectory);
      }

      return findJobPaths(jobsDirectory, jobDirectory);
    })
    .flat();
}

// Resolves a unique job name, regardless of which group contains it.
export function resolveJobPath(jobsDirectory, jobName) {
  const matches = findJobPaths(jobsDirectory)
    .filter((jobPath) => jobPath.split(sep).at(-1) === jobName)
    .sort();

  if (matches.length === 0) {
    throw new Error(`Job "${jobName}" not found.`);
  }

  if (matches.length > 1) {
    throw new Error(
      `Job "${jobName}" is ambiguous:\n${matches
        .map((jobPath) => `- ${jobPath}`)
        .join("\n")}`
    );
  }

  return matches[0];
}

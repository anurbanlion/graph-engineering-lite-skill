import { existsSync, readdirSync } from "node:fs";
import { join, relative, sep } from "node:path";

// Returns every graph directory as a path relative to graphs/.
export function findGraphPaths(graphsDirectory, directory = graphsDirectory) {
  return readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const graphDirectory = join(directory, entry.name);

      if (existsSync(join(graphDirectory, "GRAPH.json"))) {
        return relative(graphsDirectory, graphDirectory);
      }

      return findGraphPaths(graphsDirectory, graphDirectory);
    })
    .flat();
}

// Resolves a unique graph name, regardless of which group contains it.
export function resolveGraphPath(graphsDirectory, graphName) {
  const matches = findGraphPaths(graphsDirectory)
    .filter((graphPath) => graphPath.split(sep).at(-1) === graphName)
    .sort();

  if (matches.length === 0) {
    throw new Error(`Graph "${graphName}" not found.`);
  }

  if (matches.length > 1) {
    throw new Error(
      `Graph "${graphName}" is ambiguous:\n${matches
        .map((graphPath) => `- ${graphPath}`)
        .join("\n")}`
    );
  }

  return matches[0];
}

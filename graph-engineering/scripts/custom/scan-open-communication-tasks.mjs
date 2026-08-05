import { readdir, readFile } from "node:fs/promises";
import { relative, resolve } from "node:path";

const runsDirectory = resolve(process.cwd(), ".graph-engineering/runs");
const initiativeFilters = new Set(process.argv.slice(2));
const taskPattern = /^- \[ \] Communication \(([^)]+)\): (.+)$/gm;

async function directoriesAt(path) {
  const entries = await readdir(path, { withFileTypes: true });
  return entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name);
}

async function latestOutput(path) {
  const entries = await readdir(path, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isFile() && /^OUTPUT-\d{8}-\d{4}\.md$/.test(entry.name))
    .map((entry) => entry.name)
    .sort()
    .at(-1);
}

const candidates = [];

try {
  for (const initiative of await directoriesAt(runsDirectory)) {
    if (initiativeFilters.size > 0 && !initiativeFilters.has(initiative)) continue;

    const followUpDirectory = resolve(runsDirectory, initiative, "follow-up-activity");
    let outputName;
    try {
      outputName = await latestOutput(followUpDirectory);
    } catch {
      continue;
    }
    if (!outputName) continue;

    const sourcePath = resolve(followUpDirectory, outputName);
    const content = await readFile(sourcePath, "utf8");
    for (const match of content.matchAll(taskPattern)) {
      candidates.push({
        initiative,
        sourcePath: relative(process.cwd(), sourcePath),
        owner: match[1],
        task: match[2],
      });
    }
  }
  process.stdout.write(`${JSON.stringify(candidates, null, 2)}\n`);
} catch (error) {
  process.stderr.write(`Unable to scan communication tasks: ${error.message}\n`);
  process.exitCode = 1;
}

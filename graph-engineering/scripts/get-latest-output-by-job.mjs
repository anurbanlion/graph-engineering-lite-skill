import fs from 'node:fs';
import path from 'node:path';

function parseArgs(args) {
  const result = { job: null };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if ((arg === '--job' || arg === '--job-identifier' || arg === '--source-job-identifier') && i + 1 < args.length) {
      result.job = args[++i];
    }
  }
  return result;
}

function main() {
  const { job } = parseArgs(process.argv.slice(2));

  if (!job) {
    console.error('Error: --job, --job-identifier or --source-job-identifier parameter is required.');
    process.exit(1);
  }

  const resolvedRunsRoot = path.resolve(process.cwd(), '.graph-engineering/runs');
  if (!fs.existsSync(resolvedRunsRoot)) {
    process.exit(0);
  }

  const domains = fs.readdirSync(resolvedRunsRoot, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  const outputs = [];

  for (const domain of domains) {
    const jobDir = path.join(resolvedRunsRoot, domain, job);
    if (fs.existsSync(jobDir) && fs.statSync(jobDir).isDirectory()) {
      const files = fs.readdirSync(jobDir)
        .filter(f => f.startsWith('OUTPUT-') && f.endsWith('.md'))
        .sort()
        .reverse();

      if (files.length > 0) {
        const latestFile = files[0];
        const absolutePath = path.join(jobDir, latestFile);
        const relativePath = path.relative(process.cwd(), absolutePath).replace(/\\/g, '/');
        outputs.push(relativePath);
      } else {
        console.error(`Warning: Directory exists for domain "${domain}" and job "${job}", but no OUTPUT-*.md files were found.`);
      }
    }
  }

  for (const outPath of outputs) {
    console.log(outPath);
  }
}

main();

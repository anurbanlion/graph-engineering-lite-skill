import fs from 'node:fs';
import path from 'node:path';

function parseArgs(args) {
  const result = { domain: 'global', paths: [], output: null, sourceJobIdentifier: 'create-initiatives' };
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg === '--domain' && i + 1 < args.length) {
      result.domain = args[++i];
    } else if (arg === '--output' && i + 1 < args.length) {
      result.output = args[++i];
    } else if (arg === '--source-job-identifier' && i + 1 < args.length) {
      result.sourceJobIdentifier = args[++i];
    } else if (arg === '--paths') {
      i++;
      while (i < args.length && !args[i].startsWith('--')) {
        result.paths.push(args[i]);
        i++;
      }
      continue;
    } else if (!arg.startsWith('--')) {
      result.paths.push(arg);
    }
    i++;
  }
  return result;
}

function parseFrontmatterOrMarkdown(content) {
  const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const metadata = {};

  if (frontmatterMatch) {
    const yamlLines = frontmatterMatch[1].split(/\r?\n/);
    for (const line of yamlLines) {
      const colonIdx = line.indexOf(':');
      if (colonIdx !== -1) {
        const key = line.slice(0, colonIdx).trim();
        const value = line.slice(colonIdx + 1).trim().replace(/^['"]|['"]$/g, '');
        metadata[key] = value;
      }
    }
  }

  let title = metadata.title || null;
  let description = metadata.description || null;

  if (!title) {
    const h1Match = content.match(/^#\s+(.+)$/m);
    if (h1Match) {
      title = h1Match[1].trim();
    }
  }

  if (!description) {
    const lines = content.replace(/^---\r?\n[\s\S]*?\r?\n---/, '').split(/\r?\n/);
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && !trimmed.startsWith('-') && !trimmed.startsWith('|')) {
        description = trimmed;
        break;
      }
    }
  }

  return { title, description, metadata };
}

function getDomainFromPath(filePath) {
  const normalized = filePath.replace(/\\/g, '/');
  const match = normalized.match(/\.graph-engineering\/runs\/([^/]+)\//);
  if (match) {
    return match[1];
  }
  const parts = normalized.split('/');
  return parts.length > 2 ? parts[parts.length - 3] : 'unknown';
}

function getTimestamp() {
  const now = new Date();
  const pad = n => String(n).padStart(2, '0');
  const yyyy = now.getFullYear();
  const mm = pad(now.getMonth() + 1);
  const dd = pad(now.getDate());
  const hh = pad(now.getHours());
  const min = pad(now.getMinutes());
  return `${yyyy}${mm}${dd}-${hh}${min}`;
}

function main() {
  const { domain, paths, output, sourceJobIdentifier } = parseArgs(process.argv.slice(2));

  const included = [];
  const skipped = [];

  for (const relPath of paths) {
    const fullPath = path.resolve(process.cwd(), relPath);
    const domainName = getDomainFromPath(relPath);

    if (!fs.existsSync(fullPath)) {
      skipped.push({ domain: domainName, source: relPath, reason: 'File does not exist' });
      continue;
    }

    try {
      const content = fs.readFileSync(fullPath, 'utf8');
      const { title, description } = parseFrontmatterOrMarkdown(content);

      if (title) {
        included.push({
          domain: domainName,
          title: title,
          description: description || 'N/A',
          source: relPath
        });
      } else {
        skipped.push({
          domain: domainName,
          source: relPath,
          reason: 'No title or YAML frontmatter title found'
        });
      }
    } catch (err) {
      skipped.push({
        domain: domainName,
        source: relPath,
        reason: `Read error: ${err.message}`
      });
    }
  }

  const markdownLines = [
    '---',
    `source_job_identifier: ${sourceJobIdentifier}`,
    `included_count: ${included.length}`,
    `skipped_count: ${skipped.length}`,
    '---',
    '',
    '# Compiled Initiatives',
    '',
    '## Included',
    '',
    '| Domain | Title | Description | Source |',
    '| --- | --- | --- | --- |'
  ];

  if (included.length === 0) {
    markdownLines.push('| - | None | No included initiatives found | - |');
  } else {
    for (const item of included) {
      const cleanTitle = item.title.replace(/\|/g, '\\|');
      const cleanDesc = item.description.replace(/\|/g, '\\|');
      markdownLines.push(`| ${item.domain} | ${cleanTitle} | ${cleanDesc} | ${item.source} |`);
    }
  }

  markdownLines.push('', '## Skipped', '', '| Domain | Source | Reason |', '| --- | --- | --- |');

  if (skipped.length === 0) {
    markdownLines.push('| - | - | None |');
  } else {
    for (const item of skipped) {
      markdownLines.push(`| ${item.domain} | ${item.source} | ${item.reason} |`);
    }
  }

  markdownLines.push('');

  const markdownContent = markdownLines.join('\n');

  let targetOutputPath = output;
  if (!targetOutputPath) {
    const timestamp = getTimestamp();
    targetOutputPath = path.join('.graph-engineering', 'runs', domain, 'compile-initiatives', `OUTPUT-${timestamp}.md`);
  }

  const resolvedOutputPath = path.resolve(process.cwd(), targetOutputPath);
  fs.mkdirSync(path.dirname(resolvedOutputPath), { recursive: true });
  fs.writeFileSync(resolvedOutputPath, markdownContent, 'utf8');

  const relOutputPath = path.relative(process.cwd(), resolvedOutputPath).replace(/\\/g, '/');
  console.log(relOutputPath);
}

main();

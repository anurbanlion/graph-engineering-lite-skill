import { appendFile, mkdir } from "node:fs/promises";

function getGmtMinusFiveTimestamp() {
  const now = new Date();
  const adjustedTime = new Date(now.getTime() - 5 * 60 * 60 * 1000);

  return adjustedTime
    .toISOString()
    .replace("T", " ")
    .replace("Z", " GMT-05:00");
}

function formatMetadata(metadata) {
  return Object.entries(metadata)
    .filter(([, value]) => {
      if (Array.isArray(value)) {
        return value.length > 0;
      }

      return value !== undefined && value !== null && value !== "";
    })
    .map(([key, value]) => {
      const formattedValue = Array.isArray(value)
        ? value.join(",")
        : String(value);

      return `${key}=${formattedValue}`;
    })
    .join(" | ");
}

export async function writeExecutionLog({
  scriptName,
  logsDirectory,
  logFile,
  metadata = {},
}) {
  if (!scriptName) {
    throw new Error("scriptName is required.");
  }

  const metadataText = formatMetadata(metadata);

  const entry = [
    getGmtMinusFiveTimestamp(),
    scriptName,
    metadataText,
  ]
    .filter(Boolean)
    .join(" | ");

  await mkdir(logsDirectory, { recursive: true });
  await appendFile(logFile, `${entry}\n`, "utf8");
}
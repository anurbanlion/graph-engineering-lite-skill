#!/usr/bin/env python3

import re
import sys
from datetime import datetime, timezone, timedelta

from lib.errors import fail
from lib.paths import get_project_root


def validate_name(value, label):
    """Validate that the value is a non-empty kebab-case identifier."""
    if not value or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value):
        fail(f"{label} MUST be a non-empty kebab-case identifier.")


def get_gmt_minus_five_timestamp():
    """Return current timestamp in GMT-5 formatted as YYYYMMDD-HHMM."""
    tz = timezone(timedelta(hours=-5))
    now = datetime.now(tz)
    return now.strftime("%Y%m%d-%H%M")


def main() -> int:
    if len(sys.argv) != 3:
        fail("Usage: python3 resolve_output_path.py <domain> <job-name>")

    domain = sys.argv[1]
    job_name = sys.argv[2]
    if not domain:
        return 2

    validate_name(domain, "run-name")
    validate_name(job_name, "job-name")

    project_root = get_project_root()
    output_dir = project_root / ".graph-engineering" / "runs" / domain / job_name

    timestamp = get_gmt_minus_five_timestamp()
    output_file = output_dir / f"OUTPUT-{timestamp}.md"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        fail(f"Failed to create directory {output_dir}: {e}")

    print(str(output_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

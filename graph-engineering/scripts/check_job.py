#!/usr/bin/env python3

import sys

from lib.paths import get_project_root
from lib.paths import get_project_root
from lib.resolve_job import JobResolutionError, resolve_job


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return 1

    try:
        resolve_job(argv[1], get_project_root())
    except JobResolutionError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

import json
import sys


def fail(message):
    """Print a JSON error to stderr and exit with code 1."""
    print(
        json.dumps({"error": message}, indent=2),
        file=sys.stderr,
    )
    sys.exit(1)

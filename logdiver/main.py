"""CLI entry point for logdiver."""

import argparse
import os
import sys
from pathlib import Path


def run() -> None:
    """Main entry point for logdiver."""
    parser = argparse.ArgumentParser(
        prog="logdiver",
        description="A beautiful, keyboard-driven log file explorer for the terminal.",
    )
    parser.add_argument(
        "filepath",
        nargs="?",
        default=None,
        help="Path to the log file to open",
    )
    args = parser.parse_args()

    from logdiver.app import LogDiverApp

    filepath = args.filepath
    if filepath:
        path = Path(filepath)
        if not path.exists():
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        if not path.is_file():
            print(f"Error: Not a file: {filepath}", file=sys.stderr)
            sys.exit(1)
        if not os.access(filepath, os.R_OK):
            print(f"Error: Permission denied: {filepath}", file=sys.stderr)
            sys.exit(1)

    app = LogDiverApp(filepath=filepath)
    app.run()


if __name__ == "__main__":
    run()

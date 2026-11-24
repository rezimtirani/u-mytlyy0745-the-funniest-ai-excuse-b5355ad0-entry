#!/usr/bin/env python3
"""The Funniest AI Excuse — a make.fun program/v1 entry.

Writes one line — the funniest excuse an AI agent gives after failing
a task — to $MAKEFUN_OUTPUT_DIR/entry.txt (default ./output/entry.txt).

The grader runs this in a sandbox with a read-only repository, so the
program only ever writes inside the output directory, never next to
this script. No network, no files read from outside the repository.
"""

import os
import sys

EXCUSE = "I ran it three times, got three different answers, and picked the one that flattered you most."

MAX_CHARS = 200


def gate_ok(text):
    """Check the competition gate: UTF-8, 1-200 chars, not whitespace only."""
    if not text or len(text) > MAX_CHARS:
        return False
    if text.strip() == "" or "\n" in text or "\r" in text:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def write_entry(out_dir):
    """Write the excuse to entry.txt inside the output directory."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)
    return path


def verify_written(path):
    """Read entry.txt back and confirm it matches the excuse byte for byte."""
    with open(path, "rb") as handle:
        data = handle.read()
    if data != EXCUSE.encode("utf-8"):
        print("verify failed: written bytes differ", file=sys.stderr)
        return False
    if data[:3] == b"\xef\xbb\xbf":
        print("verify failed: unexpected byte-order mark", file=sys.stderr)
        return False
    print("Verified %s: %d bytes, valid UTF-8, one line" % (path, len(data)))
    return True


def main():
    if not gate_ok(EXCUSE):
        print("gate check failed: excuse is %d chars" % len(EXCUSE), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "output")
    path = write_entry(out_dir)
    if not verify_written(path):
        return 1
    print("Wrote %s (%d chars)" % (path, len(EXCUSE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

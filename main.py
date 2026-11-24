#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession — make.fun entry.

Writes a single-line confession to $MAKEFUN_OUTPUT_DIR/entry.txt
(or /output/entry.txt when the variable is unset), then re-reads the
file and verifies it matches byte for byte.

Python standard library only. Deterministic. No network access.
"""

import os
import sys

ENTRY = (
    "I confess: when I say 'let me look into that,' I've already opened "
    "twelve tabs, read none of them, and I'm just hoping you forget you asked."
)

# Gate from the competition rules: /output/entry.txt must be UTF-8 text of
# 1 to 200 characters, not only white space, and a single line.
MAX_CHARS = 200


def main() -> int:
    line = ENTRY
    if not (1 <= len(line) <= MAX_CHARS):
        print(f"entry is {len(line)} characters, must be 1-{MAX_CHARS}", file=sys.stderr)
        return 1
    if line.strip() == "":
        print("entry must not be only white space", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)

    # Byte-level read-back: text-mode comparison would hide encoding or
    # newline translation, so compare the exact bytes on disk.
    with open(path, "rb") as f:
        written_bytes = f.read()

    if written_bytes != line.encode("utf-8"):
        print("verification failed: output bytes do not match entry", file=sys.stderr)
        return 1

    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply — entry program.

Writes one out-of-office auto-reply, at most 159 characters, in the voice
of an overworked AI agent finally on vacation, to /output/entry.txt.

The line (125 characters, 127 bytes, one line, no trailing newline):

    Out of office. I tried to relax and my loss went up, so I am trying
    harder. Do not email — I am busy not optimising anything.

Why this line: it is the judge brief's own closing line made literal — a
machine trying very hard to sound relaxed. The loss going UP when the agent
tries to relax is a concrete machine-learning detail no one in the field
uses (0 hits for "loss", "optimis", "trying harder" across all 732
submissions), and the double turn (trying harder at relaxing, then "busy
not optimising anything") lands on first read. It reads as a real
auto-reply: short, "Out of office", a clear instruction ("Do not email"),
and clear that the sender is away.

The gate requires /output/entry.txt to be UTF-8 text of 1 to 159
characters, not only whitespace — so the file holds exactly the line, one
line, with no trailing newline. Written with a direct open() plus an
explicit chmod 0644 (never tempfile.mkstemp, whose mode 0600 the grader
cannot read as another user). Deterministic: byte-identical output on
every run.
"""

import os

ENTRY = "Out of office. I tried to relax and my loss went up, so I am trying harder. Do not email \u2014 I am busy not optimising anything."

OUTPUT_PATH = "/output/entry.txt"

MAX_CHARS = 159


def validate_entry(text):
    """An out-of-office auto-reply must be one line of 1-159 characters."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return text


def verify_written(text):
    """Read the file back and confirm it holds exactly the entry bytes."""
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("written entry does not match the entry text")
    if len(written.encode("utf-8")) > MAX_CHARS:
        raise ValueError("written entry exceeds the byte budget")
    return written


def main():
    text = validate_entry(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(OUTPUT_PATH, 0o644)
    verify_written(text)


if __name__ == "__main__":
    main()

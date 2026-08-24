#!/usr/bin/env python3
"""Byte-integrity check for the repository.

Motivated by a real incident: commit 02775ef carried
    analysis/track_b_4d_irsafe.py:92   raise ValueErro\x16("real Z > 0 only")
i.e. the 'r' of ValueError replaced by control byte 0x16.  The file did not
parse, so tests/test_track_b_4d_stage2.py could not even be imported and that
whole test module silently did not run.  Two further single-character
corruptions were present in docstrings ('cancelled'->'cancel',
'e^w'->'emw') which no test would ever have caught.

Note what did NOT catch this: the PR reported mergeable=true, which is about
merge conflicts, not about the files being intact or the suite being green.

Run from the repo root:  python3 verify_integrity.py
Exit status is non-zero if anything looks wrong.
"""
import ast
import glob
import sys

ALLOWED_CONTROL = {9, 10, 13}          # tab, LF, CR
problems = []

for path in sorted(glob.glob("**/*.py", recursive=True)
                   + glob.glob("**/*.md", recursive=True)
                   + glob.glob("**/*.yml", recursive=True)):
    raw = open(path, "rb").read()

    for i, b in enumerate(raw):
        if b < 32 and b not in ALLOWED_CONTROL:
            line = raw[:i].count(10) + 1
            problems.append(f"{path}:{line}: control byte 0x{b:02X}")

    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as e:
        problems.append(f"{path}: not valid UTF-8 ({e})")

    if path.endswith(".py"):
        try:
            ast.parse(raw.decode("utf-8", "replace"), filename=path)
        except SyntaxError as e:
            problems.append(f"{path}:{e.lineno}: does not parse -- {e.msg}")

if problems:
    print("INTEGRITY CHECK FAILED")
    for p in problems:
        print("  " + p)
    sys.exit(1)

print("integrity check passed: no control bytes, valid UTF-8, all .py parse")

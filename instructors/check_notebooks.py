#!/usr/bin/env python3
"""Compile-check every code cell in every lab notebook.

Executing a notebook to find a typo costs minutes; this costs a second. Run it
after regenerating a notebook and before running one.

    python3 instructors/check_notebooks.py
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(path):
    problems = []
    nb = json.load(open(path))
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        # IPython line magics (%matplotlib) are not valid Python on their own.
        src = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("%"))
        try:
            compile(src, "%s[cell %d]" % (path, i), "exec")
        except SyntaxError as exc:
            problems.append("  cell %d: %s (line %s)" % (i, exc.msg, exc.lineno))
    missing = [i for i, c in enumerate(nb["cells"]) if "id" not in c]
    if missing:
        problems.append("  %d cells have no id field (nbformat 4.5 requires one)"
                        % len(missing))
    # A student receives a blank report to fill in. Verify a notebook by
    # executing it to a scratch copy (nbconvert --output), never --inplace,
    # then regenerate the shipped file from its builder.
    stored = sum(len(c.get("outputs", [])) for c in nb["cells"])
    if stored:
        problems.append("  %d stored outputs -- the shipped notebook must be "
                        "unexecuted; regenerate it from its builder" % stored)
    return problems


def main():
    paths = sorted(glob.glob(os.path.join(ROOT, "lab*", "lab?.ipynb")))
    if not paths:
        print("no notebooks found under %s" % ROOT, file=sys.stderr)
        return 2
    bad = 0
    for p in paths:
        problems = check(p)
        rel = os.path.relpath(p, ROOT)
        if problems:
            bad += 1
            print("FAIL %s" % rel)
            print("\n".join(problems))
        else:
            print("ok   %s" % rel)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

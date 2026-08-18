# Instructor material

Reference solutions for the labs. Two uses:

1. **Figure generation.** Every schematic and layout figure in the manual is
   captured from these files, so the figures show a design that actually works.
2. **Completability checks.** `scripts/verify_solutions.sh <labdir> <name>`
   lays these files over a scratch copy of the lab and runs the full
   netlist → simulate chain. If that fails, the lab as written cannot be
   finished, whatever the manual claims.

Student files are never modified by either use.

## Not for the student release

This directory is removed from the branch students receive. Lab 2's NAND2
layout in particular is the exercise, and the legacy handout printed the
finished layout as a figure while still expecting the student to redraw it.

To cut a student release:

    git rm -r --cached instructors && rm -rf instructors

## Layout

    instructors/lab0/xschem/    inverter, NAND2 and pulse generator, gate level
    instructors/lab1/xschem/    completed Lab 1 DUTs

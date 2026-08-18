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
    instructors/lab2/           NAND2 layout build script and the built .mag
    instructors/lab3/xschem/    completed AOI21
    instructors/lab4/xschem/    completed 6T SRAM cell

## Generators

Anything with more than a handful of instances is generated rather than drawn,
because a schematic wired by name is netlisted, simulated, and silently wrong
when a terminal coordinate is off by ten units. Declaring the pin offsets once
and computing every position from them removes that whole class of mistake, and
makes the result reviewable as a diff.

    build_dff.py                common/xschem/dff.sch
    build_lab4_xschem.py        the Lab 4 SRAM cell, periphery and testbench
    build_lab1_notebook.py      lab1_spice/lab1.ipynb
    build_lab2_notebook.py      lab2_layout/lab2.ipynb
    build_lab3_notebook.py      lab3_digital/lab3.ipynb
    build_lab4_notebook.py      lab4_sram/lab4.ipynb

Two rules the generators encode, both learned the hard way:

- A wire's `lab=` field is only XSchem's cached display value. It does **not**
  name the net. A wire takes its name from a `lab_pin` or a port sitting on it;
  a wire with neither is netlisted as `net1`, `net2`, ...
- A `gnd` symbol and a `lab_pin` cannot share a point. XSchem keeps the
  `lab_pin` name and the ground connection is lost, which leaves the supplies
  floating. Use a 0 V source instead.

## Schematic figures

    figures/export_schematic.sh <cell.sch> <out.png> [density]

Renders a schematic to a figure through XSchem's own `--pdf` export: vector, on
white, already zoomed to fit, no window chrome and no dark canvas. It is the
student's own schematic rather than a redrawing of it, so a figure cannot drift
away from the cell it documents.

`--pdf` is the only export that works headless. It sets its own viewport and
calls `zoom_full` itself. `--svg` and `--png` both wait on a visible `.drw`
widget and export whatever is in the viewport, which is nothing under `-x`.

Use a real screenshot only for figures whose subject is the *interface* — a
menu, a dialog, a plot window.

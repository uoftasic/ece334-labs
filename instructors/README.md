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
    build_lab3_xschem.py        the Lab 3 AOI21 reference solution
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
- XSchem's `--pdf` page fit computes its bounding box from symbols and wires
  only. A title placed above the drawing is silently cropped in the exported
  figure, so anchor title text inside the geometry.

## Checks

    python3 instructors/check_notebooks.py

Compile-checks every code cell in every notebook and confirms each carries the
`id` field nbformat 4.5 wants. Executing a notebook to find a typo costs
minutes; this costs a second. Run it after regenerating a notebook.

Notebooks ship **unexecuted**: a student receives a blank report to fill in.
Verify one by executing it to a scratch copy rather than in place, then
regenerate the shipped file:

    jupyter nbconvert --to notebook --execute --output /tmp/check.ipynb lab4.ipynb
    python3 instructors/build_lab4_notebook.py lab4_sram/lab4.ipynb

    scripts/verify_solutions.sh <labdir> <name>

Lays the reference solutions over a scratch copy of the lab and runs the full
netlist to simulate chain. `verify_lab.sh` on a student tree is *expected* to
report "the DUT has not been built yet" -- the stubs ship empty on purpose.

## Uplifting the Docker image

The image tag is pinned in four places: `scripts/start_vnc.sh`,
`scripts/start_vnc.bat`, `scripts/start_x.sh` and
`.devcontainer/devcontainer.json`. `pdk/volare.lock` records the PDK build that
came with it, and `docs/getting-started` quotes the tag and the disk figures.

Before changing any of them, get a numeric baseline:

    python3 instructors/golden_numbers.py > /tmp/golden-old.txt   # old image
    python3 instructors/golden_numbers.py > /tmp/golden-new.txt   # new image
    diff /tmp/golden-old.txt /tmp/golden-new.txt

That script re-measures every quantity the manuals publish -- 35 of them across
all four labs, including the Lab 2 DRC count, the LVS verdict and the five-point
PEX sweep. Anything that moves is either a manual that now lies to students or a
real behavioural change to explain. Going 2026.04 -> 2026.08, 30 of 35 came out
bit-identical despite ngspice 46 -> 47 and a different open_pdks build; the five
that moved were all magic's parasitic extraction.

Two things the oracle CANNOT catch, both of which bit us on this uplift:

- **A blocker in a tool the oracle does not drive.** netgen 1.5.323 started
  choking on the commented `**.subckt` block XSchem writes for a top-level
  wrapper. `scripts/run_lvs.sh` strips it now.
- **A manual whose copy-pasteable commands are wrong.** The oracle runs decks
  directly; it never types what the manual tells a student to type. Lab 4's L1
  loop had never worked (it moved the deck to `/tmp` and broke its relative
  `.include`), and Lab 0's Magic recipe left 16 `li.5` violations while the text
  told students to reach zero. Both were years old and only surfaced when the
  manuals were worked through line by line, typing exactly what they say.

So: run the oracle for the numbers, and separately execute the manuals verbatim.

## Launchers

Launchers fire only when **the selection is exactly one object** and **the
pointer did not move between button press and release**. Both conditions fail
silently. Measured on this build, three attempts each:

| gesture | result |
|---|---|
| Ctrl-click, pointer perfectly still | fires |
| Ctrl-click, pointer drifts 3 px | **does nothing** |
| click to select, then `Ctrl-H` | fires, even after a sloppy click |
| anything else also selected, then `Ctrl-H` | **does nothing** |

A hand on a mouse drifts more than 3 px, so XSchem's documented Ctrl-click
misses most of the time. Every testbench therefore carries a note telling
students to click the arrow and press `Ctrl-H`, and the manuals lead with the
menubar's Netlist and Simulate buttons, which have no such conditions.

The relevant source is `xschem/src/callback.c` (the `state == (Button1Mask |
ControlMask) && xctx->mouse_moved == 0` test in `handle_button_release`) and
`xschem/src/actions.c` (`launcher()` returns immediately unless
`xctx->lastsel == 1`).

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

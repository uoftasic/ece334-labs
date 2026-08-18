# Include-only netlists

Subcircuit definitions pulled in with `.include`. They carry no analysis
statement, so they are not runnable decks and `verify_lab.sh` does not try to
simulate them.

`dff.spice` is the Lab 3 flip-flop, netlisted as a subcircuit. Regenerate it
after changing the flip-flop:

```bash
. /foss/designs/common/.designinit
xschem -n -s -q -x -o . /foss/designs/instructors/lab4/xschem/dff_wrap.sch
mv dff_wrap.spice include/dff.spice
```

Netlisting `dff.sch` directly will not do: XSchem emits its devices at the top
level with no `.subckt`, so `.include` has nothing to instantiate.

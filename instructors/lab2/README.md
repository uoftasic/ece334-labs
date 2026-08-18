# Lab 2 reference material

| File | Purpose |
|------|---------|
| `build_nand2.tcl` | Builds the reference NAND2 layout from paint commands, runs DRC, declares ports, and writes both the LVS and PEX netlists |
| `magic/nand2.mag` | The built layout. Figure source; **not** shipped to students |
| `xschem/nand2_lvs.sch` | Wrapper that instantiates `nand2.sym` so XSchem emits a `.subckt` for netgen |

Rebuild and re-verify:

```bash
. /foss/designs/common/.designinit
mkdir -p /tmp/n && cd /tmp/n
echo "source $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc" > .magicrc
magic -dnull -noconsole -T sky130A < /foss/designs/instructors/lab2/build_nand2.tcl
```

Expect `DRC_COUNT=0` and `.subckt nand2 a b out vdd vss`.

## Verified results

- DRC: 0 errors.
- LVS against `common/xschem/nand2.sch`: **Circuits match uniquely.**
- Extraction: 4 devices, 6 nets. PEX at `cthresh 0` adds 14 coupling caps.
- Sizing is `Wn = 2`, `Wp = 3`, `L = 0.5`, matching the Lab 1 cell. That is the
  legacy handout's 24:16 ratio at this lab's channel length.

### Pre- versus post-PEX, t_pHL

| C_load | ideal | extracted | change |
|--------|-------|-----------|--------|
| 0      | 100.0 ps | 105.8 ps | +5.8 % |
| 1 fF   | 104.0 ps | 109.8 ps | +5.6 % |
| 5 fF   | 120.0 ps | 125.7 ps | +4.8 % |
| 20 fF  | 177.1 ps | 182.7 ps | +3.2 % |
| 100 fF | 467.8 ps | 473.5 ps | +1.2 % |

The parasitics contribute a roughly fixed ~6 ps, so they matter in proportion
to how they compare with the load being driven.

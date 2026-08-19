# Lab 1 — starter files

Work in this folder (mounted at `/foss/designs/lab1_spice` inside the container).

**Lab manual:** https://uoftasic.com/ece334-docs/labs/lab1/

## What's here

| Path | Purpose |
|------|---------|
| `xschem/rc_tb.sch` | RC step-response testbench (launcher buttons) |
| `xschem/diode_tb.sch` | diode-connected device extraction testbench |
| `xschem/inv_tb.sch` | CMOS inverter testbench with a DUT placeholder |
| `xschem/dut_inv.{sym,sch}` | the DUT you build your inverter into (pins `in`/`out`/`vdd`/`vss`) |
| `xschem/dut_diode.{sym,sch}` | the DUT you build your test device into (pins `g`/`s`) |
| `lab1.ipynb` | analysis notebook — loads results and measures them with `ece334lib` |
| `spice/` | plain reference decks, if you prefer the command line |

## Getting started

```bash
. /foss/designs/common/.designinit   # sets PDK, PYTHONPATH (ece334lib), and the `jlab` alias
cd /foss/designs/lab1_spice
jlab                                  # launch JupyterLab, then open lab1.ipynb
```

In XSchem, open a `*_tb.sch` and press the **Netlist & Simulate** button; then run the
matching section of `lab1.ipynb`. Full walkthrough in the lab manual linked above.

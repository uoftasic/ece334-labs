# ECE334 — Digital Electronics: lab workbench

Your working copy. Clone it, start the container, and do the labs here; your
edits stay in your clone.

**Lab manuals, setup guide, and cheatsheets:**
<https://uoftasic.github.io/ece334-docs/>

## Quick start

1. Install **Docker Desktop** (per-OS instructions are in the setup guide).
2. Clone this repository.
3. Start the environment:
   - macOS / Linux: `./scripts/start_vnc.sh`
   - Windows: double-click `scripts/start_vnc.bat`
4. Open <http://localhost/> (password `abc123`).
5. In the desktop terminal:

   ```bash
   . /foss/designs/common/.designinit
   /foss/designs/scripts/smoke_test.sh
   ```

Source `.designinit` once per terminal. It sets the PDK, puts `ece334lib` on
`PYTHONPATH`, and installs the course XSchem configuration at
`~/.xschem/xschemrc`. It is idempotent — re-run it if a tool stops resolving
symbols.

## Layout

| Path | Contents |
|------|----------|
| `common/.designinit` | Environment setup, sourced once per terminal |
| `common/xschemrc` | XSchem library paths, layered over the PDK's own file |
| `common/ngspice/.spiceinit` | ngspice defaults for SKY130 |
| `common/xschem/` | Cells shared across labs (`inv`, `nand2`) |
| `common/ece334lib/` | Python helpers: load results, measure, plot |
| `lab0_setup/` … `lab4_sram/` | Per-lab files |
| `instructors/` | Reference solutions — not part of the student release |
| `scripts/` | Launch, verification, and figure-generation scripts |
| `pdk/volare.lock` | Pinned SKY130 version |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/start_vnc.sh` / `.bat` | Start the container |
| `scripts/smoke_test.sh` | Check the tools are working |
| `scripts/verify_lab.sh <lab>` | Netlist **and simulate** every testbench and deck in a lab |
| `scripts/verify_solutions.sh <lab> <ref>` | Staff: check a lab is completable, using `instructors/` |
| `scripts/make_figures.sh` | Staff: regenerate the manual's tool screenshots |
| `scripts/install_capture_deps.sh` | Staff: install the screenshot tooling |

`verify_lab.sh` is the one worth knowing. Run it before a demo:

```bash
. /foss/designs/common/.designinit
/foss/designs/scripts/verify_lab.sh lab1_spice
```

It fails on an unbuilt DUT, because a testbench with an empty DUT netlists
without complaint and only fails later at `write`.

## Notebooks

Each lab ships `labN.ipynb`. It is your report: hand analysis, measurements, and
your written answers in one file. Start JupyterLab with `jlab` after sourcing
`.designinit`, then open the printed URL.

Commit notebooks with outputs cleared:

```bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to notebook --inplace labN.ipynb
```

## Conventions

- Supply 1.8 V, teaching length L = 0.5 µm, process `sky130A`.
- Widths and lengths are **unitless microns**: `W=1`, `L=0.5`. A `u` suffix
  breaks model binning.
- Net names: `in`, `out`, `vdd`, `vss`, plus whatever a lab documents.
- `XSCHEM_LIBRARY_PATH` is one flat namespace and the first match wins. Cells
  used by more than one lab belong in `common/xschem/`.

# ECE334 — Digital Electronics: Lab Workbench

This repository is your **workbench**. Fork or clone it, start the container, and do your lab
work here — your edits live in your clone and persist on your computer.

> 📖 **All lab manuals, the full setup guide, and cheatsheets are online:**
> **https://ece334.github.io/ece334-docs/**

## Quick start

1. Install **Docker Desktop** (see the setup guide on the docs site for per-OS instructions).
2. Clone this repository.
3. Start the environment:
   - **macOS / Linux:** `./scripts/start_vnc.sh`
   - **Windows:** double-click `scripts/start_vnc.bat`
4. Open **http://localhost/** in your browser (password `abc123`) for the EDA desktop.
5. In the desktop terminal, verify your tools:
   ```bash
   . /foss/designs/common/.designinit
   /foss/designs/scripts/smoke_test.sh
   ```

## What's here

| Path | Purpose |
|------|---------|
| `.devcontainer/` | VS Code Dev Containers config |
| `scripts/` | Container launch & helper scripts |
| `common/` | Shared environment (`.designinit`, `xschemrc`) |
| `pdk/` | Pinned SKY130 PDK version (`volare.lock`) |
| `lab0_setup/` … `lab4_sram/` | Per-lab starter files |

Full instructions, troubleshooting, and the lab manuals are on the docs site linked above.

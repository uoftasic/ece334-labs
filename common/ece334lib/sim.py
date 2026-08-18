"""Drive simulations from Python: load results, run decks, sweep a parameter.

Two ways to get data into a notebook:

1. **Press the XSchem button**, then load what it wrote::

       raw = sim.run("xschem/inv_tb.raw")

2. **Run a deck from Python** (lets you script sweeps the buttons can't)::

       raw = sim.run_deck("spice/inv_tb.spice", output="inv_tran.txt", fmt="wrdata")
       df  = sim.sweep("spice/inv_tb.spice", "Wp", ["2u","3u","6u"],
                       lambda w: {"tpd": measure.prop_delay(w, "in", "out", 1.8)},
                       output="inv_tran.txt", fmt="wrdata")

Decks/harnesses must write a **named** output file (the data-flow contract). For
``fmt="raw"`` the deck should ``set filetype=ascii`` before ``write``.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

from . import waves


def _read(path, fmt, names=None):
    if fmt == "raw":
        return waves.read_raw(path)
    if fmt == "wrdata":
        return waves.read_wrdata(path, names=names)
    raise ValueError(f"unknown fmt {fmt!r}; use 'raw' or 'wrdata'")


def run(path, fmt="raw", names=None):
    """Load an already-produced ngspice output file into a :class:`Wave`."""
    return _read(path, fmt, names=names)


def _ngspice(deck, cwd):
    exe = shutil.which("ngspice")
    if exe is None:
        raise RuntimeError("ngspice not found on PATH (run inside the lab container)")
    proc = subprocess.run(
        [exe, "-b", deck],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"ngspice failed (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}"
        )
    return proc


def run_deck(deck, output, fmt="raw", names=None, cwd=None):
    """Run ngspice on ``deck`` and parse the ``output`` file it writes.

    ``cwd`` defaults to the deck's directory, so ``output`` is resolved relative
    to it (matching how the deck's ``.control`` block writes the file).
    """
    deck = os.path.abspath(deck)
    cwd = cwd or os.path.dirname(deck)
    _ngspice(deck, cwd)
    out_path = output if os.path.isabs(output) else os.path.join(cwd, output)
    if not os.path.exists(out_path):
        raise FileNotFoundError(
            f"deck ran but did not produce {out_path!r} — check the .control "
            f"block writes this file"
        )
    return _read(out_path, fmt, names=names)


def sweep(deck_template, param, values, measure_fn, output, fmt="raw",
          names=None):
    """Sweep one parameter through ``values`` and tabulate measured scalars.

    The template deck must contain the token ``@param@`` (e.g. ``@Wp@``) where
    the value goes. For each value the token is substituted, the deck is run, and
    ``measure_fn(wave) -> dict`` is called. Returns a pandas ``DataFrame`` with a
    ``param`` column plus one column per measured key.
    """
    import pandas as pd  # lazy: only sweep needs pandas

    with open(deck_template) as fh:
        template = fh.read()
    token = f"@{param}@"
    if token not in template:
        raise ValueError(f"token {token!r} not found in {deck_template!r}")

    rows = []
    src_dir = os.path.dirname(os.path.abspath(deck_template))
    for val in values:
        with tempfile.TemporaryDirectory(dir=src_dir or None) as td:
            deck = os.path.join(td, "sweep.spice")
            with open(deck, "w") as fh:
                fh.write(template.replace(token, str(val)))
            wave = run_deck(deck, output=output, fmt=fmt, names=names, cwd=td)
            row = {param: val}
            row.update(measure_fn(wave))
            rows.append(row)
    return pd.DataFrame(rows)


def netlist_and_run(sch, output, fmt="raw", names=None):
    """Netlist an XSchem schematic headlessly, then simulate the result.

    Convenience for fully scripted flows. Most of the time you'll press the
    schematic's **Netlist & Simulate** button and call :func:`run` on the
    ``.raw`` it writes instead.
    """
    exe = shutil.which("xschem")
    if exe is None:
        raise RuntimeError("xschem not found on PATH (run inside the lab container)")
    sch = os.path.abspath(sch)
    cwd = os.path.dirname(sch)
    netlist = os.path.splitext(os.path.basename(sch))[0] + ".spice"
    proc = subprocess.run(
        [exe, "-n", "-s", "-q", "-x", "-o", cwd, sch],
        cwd=cwd, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"xschem netlist failed:\n{proc.stdout}\n{proc.stderr}")
    return run_deck(os.path.join(cwd, netlist), output=output, fmt=fmt,
                    names=names, cwd=cwd)


SIM_DIR = os.environ.get(
    "ECE334_SIM_DIR", "/foss/designs/.xschem/simulations"
)


def raw(name, fmt="raw", names=None):
    """Load a result file written by an XSchem launcher button.

    The buttons netlist and simulate into one shared directory (``netlist_dir``
    in ``common/xschemrc``), so a notebook refers to a result by bare filename
    and does not care which directory XSchem was started from::

        rc = sim.raw("rc_tb.raw")

    Falls back to the current working directory, so a deck run by hand from a
    lab folder still resolves.
    """
    if os.path.isabs(name) and os.path.exists(name):
        return _read(name, fmt, names=names)
    for base in (SIM_DIR, os.getcwd()):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return _read(path, fmt, names=names)
    raise FileNotFoundError(
        f"{name!r} not found in {SIM_DIR} or {os.getcwd()}. Press "
        f"'Netlist & Simulate' in the testbench first, and check the schematic's "
        f".control block writes exactly this filename."
    )

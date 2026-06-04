"""Load ngspice output into a light, numpy-backed ``Wave`` container.

Two readers cover everything the ECE334 testbenches produce:

* :func:`read_raw`     — ngspice **ASCII** rawfile (``set filetype=ascii`` then
  ``write foo.raw``). Carries every saved signal with its name.
* :func:`read_wrdata`  — column text files written by ngspice ``wrdata``.

A :class:`Wave` looks signals up tolerantly, so ``w["out"]``, ``w["v(out)"]`` and
``w["V(OUT)"]`` all return the same array. The first column (``w.x``) is the
independent axis — time for a ``.tran``, the swept source for a ``.dc``.
"""
from __future__ import annotations

import re

import numpy as np


def _norm(name: str) -> str:
    """Normalise a signal name for tolerant matching."""
    s = name.strip().lower()
    # v(out) / i(vdd) -> out / vdd ; leave bare names alone
    m = re.fullmatch(r"[vi]\((.+)\)", s)
    return m.group(1) if m else s


class Wave:
    """A set of named, equal-length signals sharing one independent axis."""

    def __init__(self, names, columns):
        self.names = list(names)
        self._cols = {n: np.asarray(columns[n], float) for n in self.names}
        # normalised lookup: bare name -> canonical name (first wins)
        self._index = {}
        for n in self.names:
            self._index.setdefault(_norm(n), n)

    @property
    def xname(self) -> str:
        return self.names[0]

    @property
    def x(self) -> np.ndarray:
        return self._cols[self.names[0]]

    def __contains__(self, key) -> bool:
        return _norm(key) in self._index or key in self._cols

    def __getitem__(self, key) -> np.ndarray:
        if key in self._cols:
            return self._cols[key]
        canon = self._index.get(_norm(key))
        if canon is None:
            raise KeyError(
                f"signal {key!r} not found; available: {', '.join(self.names)}"
            )
        return self._cols[canon]

    def __repr__(self) -> str:
        npts = len(self.x) if self.names else 0
        return f"Wave({self.names}, {npts} points)"


def read_raw(path: str) -> Wave:
    """Parse an ngspice ASCII rawfile into a :class:`Wave` (real data only)."""
    with open(path, "r") as fh:
        text = fh.read()

    # header: variable names, point/var counts
    nvars = int(re.search(r"No\. Variables:\s*(\d+)", text).group(1))
    npts = int(re.search(r"No\. Points:\s*(\d+)", text).group(1))
    if re.search(r"Flags:.*complex", text, re.I):
        raise ValueError("complex rawfiles are not supported (use real analysis)")

    vars_block = text.split("Variables:", 1)[1].split("Values:", 1)[0]
    names = []
    for line in vars_block.strip().splitlines():
        parts = line.split()
        # each line: <index> <name> <type>
        if len(parts) >= 2 and parts[0].isdigit():
            names.append(parts[1])
    if len(names) != nvars:
        raise ValueError(f"expected {nvars} variables, parsed {len(names)}")

    # values: a flat stream of "index v0 v1 ... v(nvars-1)" per point
    values = text.split("Values:", 1)[1].split()
    nums = np.array([float(tok) for tok in values], float)
    expected = npts * (nvars + 1)
    if nums.size != expected:
        raise ValueError(f"expected {expected} value tokens, got {nums.size}")
    table = nums.reshape(npts, nvars + 1)[:, 1:]  # drop per-point index column

    cols = {name: table[:, i] for i, name in enumerate(names)}
    return Wave(names, cols)


def read_wrdata(path: str, names=None) -> Wave:
    """Parse an ngspice ``wrdata`` text file.

    ``wrdata`` writes each requested signal as an *(x, y)* pair, so a file made
    with ``wrdata f.txt v(in) v(out)`` has columns ``x v(in) x v(out)``. The
    shared x-axis is taken from the first pair. Provide ``names`` to label the y
    columns; the x column is always called ``time``.
    """
    raw = np.loadtxt(path)
    if raw.ndim == 1:
        raw = raw.reshape(1, -1)
    ncol = raw.shape[1]
    if ncol % 2 != 0:
        raise ValueError(f"wrdata expects x/y column pairs; got {ncol} columns")
    nsig = ncol // 2
    if names is None:
        names = [f"y{i}" for i in range(nsig)]
    if len(names) != nsig:
        raise ValueError(f"got {nsig} signals but {len(names)} names")

    cols = {"time": raw[:, 0]}
    out_names = ["time"]
    for i, nm in enumerate(names):
        cols[nm] = raw[:, 2 * i + 1]
        out_names.append(nm)
    return Wave(out_names, cols)

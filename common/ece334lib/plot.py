"""Two small matplotlib wrappers so notebooks plot in one line.

matplotlib is imported lazily, so ``waves``/``measure`` stay dependency-light for
testing and headless use.
"""
from __future__ import annotations


def transient(wave, signals, ax=None, time_unit="n"):
    """Plot one or more signals against the time axis.

    ``signals`` is a name or list of names (tolerant lookup). ``time_unit`` is
    one of 'p','n','u','m' for ps/ns/µs/ms tick scaling, or '' for seconds.
    """
    import matplotlib.pyplot as plt

    scale = {"": 1, "m": 1e3, "u": 1e6, "n": 1e9, "p": 1e12}[time_unit]
    if isinstance(signals, str):
        signals = [signals]
    if ax is None:
        _, ax = plt.subplots()
    t = wave.x * scale
    for s in signals:
        ax.plot(t, wave[s], label=s)
    ax.set_xlabel(f"time ({time_unit}s)" if time_unit else "time (s)")
    ax.set_ylabel("voltage (V)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax


def vtc(wave, vin, vout, ax=None, unity_line=True):
    """Plot a DC transfer curve Vout vs Vin, optionally with the unity line."""
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()
    vi = wave[vin]
    ax.plot(vi, wave[vout], label="VTC")
    if unity_line:
        ax.plot(vi, vi, "k--", lw=0.8, alpha=0.6, label="$V_{out}=V_{in}$")
    ax.set_xlabel("$V_{in}$ (V)")
    ax.set_ylabel("$V_{out}$ (V)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax

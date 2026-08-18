"""ECE334 course helper library.

A deliberately small toolkit so lab notebooks read as intent, not plumbing:

    from ece334lib import sim, measure, plot

    raw   = sim.run("xschem/inv_tb.raw")        # load a sim the XSchem button made
    tpd   = measure.prop_delay(raw, "in", "out", vdd=1.8)
    plot.transient(raw, ["in", "out"])

Modules
-------
waves    : load ngspice output (.raw / wrdata) into a numpy-backed ``Wave``
measure  : digital metrics (edges, propagation delay, noise margins, trip
           point, RC time constant, pulse width)
sim      : run ngspice / netlist XSchem schematics; parameter sweeps
plot     : a couple of matplotlib wrappers (transient, VTC)
"""
from . import measure, waves
from .waves import Wave

__all__ = ["waves", "measure", "sim", "plot", "Wave"]
__version__ = "0.1.0"

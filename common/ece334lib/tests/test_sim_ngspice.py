"""End-to-end test through real ngspice (no PDK needed).

Runs an RC step deck, parses the ASCII rawfile, and checks the measured 10–90 %
rise time against the analytic value tau*ln(9). Skipped if ngspice is absent.
"""
import shutil
import textwrap

import numpy as np
import pytest

from ece334lib import measure, sim

pytestmark = pytest.mark.skipif(
    shutil.which("ngspice") is None, reason="ngspice not installed"
)

RC_DECK = textwrap.dedent("""\
    * RC step response -- tau = R*C = 1k * 1p = 1ns
    V1 in 0 PWL(0 0 1p 1.8)
    R1 in out 1k
    C1 out 0 1p
    .control
    set filetype=ascii
    tran 1p 15n
    write rc.raw v(out) v(in)
    .endc
    .end
    """)


def test_rc_rise_time_through_ngspice(tmp_path):
    deck = tmp_path / "rc.spice"
    deck.write_text(RC_DECK)
    w = sim.run_deck(str(deck), output="rc.raw", fmt="raw")
    assert "v(out)" in w
    t_rise, _ = measure.edges_10_90(w, "out", vdd=1.8)
    tau = 1e-9
    assert abs(t_rise - tau * np.log(9)) / (tau * np.log(9)) < 0.02

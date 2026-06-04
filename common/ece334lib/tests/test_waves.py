"""Unit tests for ece334lib.waves — file parsing + tolerant signal lookup.

Run from the repo root (or anywhere on PYTHONPATH that exposes ece334lib):
    pytest common/ece334lib
"""
import textwrap

import numpy as np

from ece334lib import waves


# --- ngspice ASCII rawfile parsing ------------------------------------------

ASCII_RAW = textwrap.dedent("""\
    Title: * test deck
    Date: Thu Jun  4 00:00:00 2026
    Plotname: Transient Analysis
    Flags: real
    No. Variables: 3
    No. Points: 3
    Variables:
    \t0\ttime\ttime
    \t1\tv(in)\tvoltage
    \t2\tv(out)\tvoltage
    Values:
    0\t0.000000000000000e+00\t0.000000000000000e+00\t1.800000000000000e+00
    1\t1.000000000000000e-09\t1.800000000000000e+00\t0.000000000000000e+00
    2\t2.000000000000000e-09\t0.000000000000000e+00\t1.800000000000000e+00
    """)


def test_read_raw_parses_names_and_shape(tmp_path):
    p = tmp_path / "t.raw"
    p.write_text(ASCII_RAW)
    w = waves.read_raw(str(p))
    assert w.names == ["time", "v(in)", "v(out)"]
    assert len(w["time"]) == 3
    np.testing.assert_allclose(w["time"], [0, 1e-9, 2e-9])
    np.testing.assert_allclose(w["v(out)"], [1.8, 0.0, 1.8])


def test_x_is_first_column(tmp_path):
    p = tmp_path / "t.raw"
    p.write_text(ASCII_RAW)
    w = waves.read_raw(str(p))
    assert w.xname == "time"
    np.testing.assert_allclose(w.x, [0, 1e-9, 2e-9])


def test_tolerant_lookup(tmp_path):
    p = tmp_path / "t.raw"
    p.write_text(ASCII_RAW)
    w = waves.read_raw(str(p))
    # all of these should resolve to v(in)
    for key in ["v(in)", "V(IN)", "in", "IN", " v(in) "]:
        np.testing.assert_allclose(w[key], [0.0, 1.8, 0.0]), key


def test_missing_signal_raises(tmp_path):
    p = tmp_path / "t.raw"
    p.write_text(ASCII_RAW)
    w = waves.read_raw(str(p))
    try:
        _ = w["v(nope)"]
    except KeyError as e:
        assert "nope" in str(e)
    else:
        raise AssertionError("expected KeyError for missing signal")


# --- wrdata column files -----------------------------------------------------

def test_read_wrdata(tmp_path):
    # wrdata writes interleaved x/y per signal; here a simple 2-column case
    # produced by `wrdata f.txt v(in) v(out)` -> time v(in) time v(out)
    txt = "0 0.0 0 1.8\n1e-9 1.8 1e-9 0.0\n2e-9 0.0 2e-9 1.8\n"
    p = tmp_path / "f.txt"
    p.write_text(txt)
    w = waves.read_wrdata(str(p), names=["v(in)", "v(out)"])
    assert w.xname == "time"
    np.testing.assert_allclose(w["time"], [0, 1e-9, 2e-9])
    np.testing.assert_allclose(w["v(in)"], [0.0, 1.8, 0.0])
    np.testing.assert_allclose(w["v(out)"], [1.8, 0.0, 1.8])

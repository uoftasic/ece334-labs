"""Digital-circuit metrics computed from a :class:`ece334lib.waves.Wave`.

The vocabulary a student needs for Lab 1–3: edge times, propagation delay, and
the DC transfer-curve figures (trip point, noise margins). Pure numpy — every
function works on synthetic arrays in tests and on real ngspice output alike.
"""
from __future__ import annotations

import numpy as np


def _crossings(x, y, level):
    """Linear-interpolated crossings of ``y(x) == level``.

    Returns ``(xs, dirs)`` where ``dirs`` is +1 for an upward crossing and -1
    for a downward one, in order of increasing index.
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    above = y >= level
    idx = np.nonzero(above[:-1] != above[1:])[0]
    xs, dirs = [], []
    for i in idx:
        y0, y1 = y[i], y[i + 1]
        if y1 == y0:
            continue
        frac = (level - y0) / (y1 - y0)
        xs.append(x[i] + frac * (x[i + 1] - x[i]))
        dirs.append(1 if y1 > y0 else -1)
    return np.array(xs), np.array(dirs, int)


def edges_10_90(wave, sig, vdd):
    """(t_rise, t_fall) measured between 10 % and 90 % of ``vdd``.

    Each is ``None`` if that edge is absent. Uses the first rising/falling edge.
    """
    t = wave.x
    y = wave[sig]
    lo, hi = 0.1 * vdd, 0.9 * vdd
    x_lo, d_lo = _crossings(t, y, lo)
    x_hi, d_hi = _crossings(t, y, hi)

    t_rise = _edge(x_lo, d_lo, x_hi, d_hi, rising=True)
    t_fall = _edge(x_lo, d_lo, x_hi, d_hi, rising=False)
    return t_rise, t_fall


def _edge(x_lo, d_lo, x_hi, d_hi, rising):
    want = 1 if rising else -1
    los = x_lo[d_lo == want]
    his = x_hi[d_hi == want]
    if los.size == 0 or his.size == 0:
        return None
    if rising:
        t10 = los[0]
        later = his[his >= t10]
        return float(later[0] - t10) if later.size else None
    else:
        t90 = his[0]
        later = los[los >= t90]
        return float(later[0] - t90) if later.size else None


def prop_delay(wave, vin, vout, vdd):
    """First-edge propagation delay: input 50 % crossing to output 50 % crossing."""
    t = wave.x
    half = vdd / 2.0
    xi, _ = _crossings(t, wave[vin], half)
    xo, _ = _crossings(t, wave[vout], half)
    if xi.size == 0 or xo.size == 0:
        raise ValueError("no 50% crossing found on input and/or output")
    ti = xi[0]
    later = xo[xo >= ti]
    to = later[0] if later.size else xo[0]
    return float(abs(to - ti))


def extract_square_law(vgs, idd, wl, vmin, vmax):
    """Extract K_P and V_t from a diode-connected device sweep.

    In saturation $I_D = \\tfrac12 K_P (W/L)(V_{GS}-V_t)^2$, so $\\sqrt{I_D}$ is
    linear in $V_{GS}$. Fits a line over the strong-inversion window
    ``[vmin, vmax]``; the slope gives $K_P$ and the x-intercept gives $V_t$.

    Returns a dict with ``KP, Vt, slope, intercept``. Pass arrays (e.g.
    ``wave["g"]``, ``wave["id"]``) and the device ``wl`` = W/L.
    """
    vgs = np.asarray(vgs, float)
    idd = np.asarray(idd, float)
    sid = np.sqrt(np.clip(idd, 0.0, None))
    sel = (vgs >= vmin) & (vgs <= vmax)
    if np.count_nonzero(sel) < 2:
        raise ValueError("fit window [vmin, vmax] selects fewer than 2 points")
    slope, intercept = np.polyfit(vgs[sel], sid[sel], 1)
    return {
        "KP": 2.0 * slope ** 2 / wl,
        "Vt": -intercept / slope,
        "slope": float(slope),
        "intercept": float(intercept),
    }


def _sorted_vtc(wave, vin, vout):
    vi = wave[vin]
    vo = wave[vout]
    order = np.argsort(vi)
    return vi[order], vo[order]


def vtc_trip(wave, vin, vout):
    """Switching threshold V_M: the input where Vout == Vin."""
    vi, vo = _sorted_vtc(wave, vin, vout)
    xs, _ = _crossings(vi, vo - vi, 0.0)
    if xs.size == 0:
        raise ValueError("VTC never crosses the unity line")
    return float(xs[0])


def noise_margins(wave, vin, vout):
    """Noise margins from a VTC via the unity-gain (slope = -1) definition.

    Returns a dict with ``VIL, VIH, VOL, VOH, NMH, NML, VM``.
    """
    vi, vo = _sorted_vtc(wave, vin, vout)
    slope = np.gradient(vo, vi)
    xs, _ = _crossings(vi, slope, -1.0)
    if xs.size < 2:
        raise ValueError("could not locate two unity-gain points on the VTC")
    vil, vih = float(xs.min()), float(xs.max())
    voh = float(np.interp(vil, vi, vo))
    vol = float(np.interp(vih, vi, vo))
    return {
        "VIL": vil,
        "VIH": vih,
        "VOH": voh,
        "VOL": vol,
        "NMH": voh - vih,
        "NML": vil - vol,
        "VM": vtc_trip(wave, vin, vout),
    }

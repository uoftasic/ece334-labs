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


def prop_delays(wave, vin, vout, vdd):
    """``(t_pHL, t_pLH)``: 50 % input crossing to the output crossing it causes.

    Named for what the OUTPUT does, which is the convention the labs use:
    ``t_pHL`` is the delay to the output's falling edge and ``t_pLH`` to its
    rising edge. Either is ``None`` if that edge does not occur.

    :func:`prop_delay` returns the first edge only, whichever way it goes; use
    this when you need both, as Labs 2 and 3 do.
    """
    half = vdd / 2.0
    t = wave.x
    xi, _ = _crossings(t, wave[vin], half)
    xo, do = _crossings(t, wave[vout], half)
    if xi.size == 0 or xo.size == 0:
        raise ValueError("no 50% crossing found on input and/or output")

    def first(direction):
        for to, d in zip(xo, do):
            if d != direction:
                continue
            # The input crossing that caused it is the last one before it.
            before = xi[xi <= to]
            if before.size:
                return float(to - before[-1])
        return None

    return first(-1), first(+1)


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


def tau_from_step(wave, sig, v_final=None):
    """Time constant of a step response: the 63.2 % crossing time.

    Assumes the step is applied at ``t = 0`` and ``sig`` moves monotonically
    toward ``v_final``. ``v_final`` defaults to the last sample, which is only
    correct if the response has settled inside the simulated window -- pass it
    explicitly when it has not.

    The result is only as good as the step origin. A stimulus with a finite rise
    time has no single origin, and the answer is then biased by roughly half the
    input ramp. For a source with a non-zero ``tr``, prefer the reference-free
    form ``edges_10_90(...)[0] / log(9)``.
    """
    t = wave.x
    y = wave[sig]
    if v_final is None:
        v_final = float(y[-1])
    xs, dirs = _crossings(t, y, 0.632 * v_final)
    want = 1 if v_final >= y[0] else -1
    for x, d in zip(xs, dirs):
        if d == want:
            return float(x)
    raise ValueError(
        f"{sig!r} never reaches 63.2 % of {v_final:g} V "
        f"(peak {float(np.max(y)):g} V) -- check v_final or extend .tran"
    )


def pulse_width(wave, sig, vdd, polarity="low"):
    """50 %-to-50 % width of the first pulse on ``sig``.

    ``polarity="low"`` measures a low-going pulse: the falling 50 % crossing to
    the next rising one. This is what the pulse generator produces, because its
    output stage is a NAND. ``polarity="high"`` measures a high-going pulse.
    """
    if polarity not in ("low", "high"):
        raise ValueError(f"polarity must be 'low' or 'high', got {polarity!r}")
    open_dir = 1 if polarity == "high" else -1
    xs, dirs = _crossings(wave.x, wave[sig], 0.5 * vdd)
    for i, d in enumerate(dirs):
        if d != open_dir:
            continue
        for x2, d2 in zip(xs[i + 1:], dirs[i + 1:]):
            if d2 == -open_dir:
                return float(x2 - xs[i])
        raise ValueError(
            f"{sig!r} opens a {polarity}-going pulse at {xs[i]:g} s but never "
            f"returns -- extend .tran past the closing edge"
        )
    raise ValueError(f"no {polarity}-going pulse found on {sig!r} at 50 % of {vdd} V")

"""Unit tests for ece334lib.measure — digital timing & DC metrics.

Synthetic numpy waveforms with known analytic answers; no ngspice needed.
"""
import numpy as np

from ece334lib import measure
from ece334lib.waves import Wave


VDD = 1.8


def _wave(**cols):
    names = list(cols.keys())
    return Wave(names, {k: np.asarray(v, float) for k, v in cols.items()})


# --- edges_10_90 -------------------------------------------------------------

def test_rise_time_of_ideal_rc():
    # RC charging: v = VDD*(1 - exp(-t/tau)). 10->90% takes tau*ln(9).
    tau = 1e-9
    t = np.linspace(0, 10 * tau, 20001)
    v = VDD * (1 - np.exp(-t / tau))
    w = _wave(time=t, **{"v(out)": v})
    t_rise, t_fall = measure.edges_10_90(w, "out", vdd=VDD)
    assert t_rise is not None
    assert abs(t_rise - tau * np.log(9)) / (tau * np.log(9)) < 1e-3
    assert t_fall is None  # purely rising signal


def test_fall_time_of_ideal_rc():
    tau = 2e-9
    t = np.linspace(0, 10 * tau, 20001)
    v = VDD * np.exp(-t / tau)  # discharge
    w = _wave(time=t, **{"v(out)": v})
    t_rise, t_fall = measure.edges_10_90(w, "out", vdd=VDD)
    assert t_fall is not None
    assert abs(t_fall - tau * np.log(9)) / (tau * np.log(9)) < 1e-3


# --- prop_delay --------------------------------------------------------------

def test_prop_delay_of_delayed_step():
    # input rises through 50% at t=1ns; output (inverted) falls through 50% at t=1.4ns
    t = np.linspace(0, 4e-9, 40001)
    vin = np.clip((t - 0.5e-9) / 1e-9, 0, 1) * VDD       # ramp 0.5n->1.5n, 50% @1.0n
    vout = VDD - np.clip((t - 0.9e-9) / 1e-9, 0, 1) * VDD  # 50% @1.4n
    w = _wave(time=t, **{"v(in)": vin, "v(out)": vout})
    tpd = measure.prop_delay(w, "in", "out", vdd=VDD)
    assert abs(tpd - 0.4e-9) < 5e-12


# --- VTC: noise margins + trip point ----------------------------------------

def _symmetric_vtc(vm=VDD / 2, gain=20.0, n=4001):
    vin = np.linspace(0, VDD, n)
    vout = VDD / 2.0 * (1 - np.tanh(gain * (vin - vm) / VDD))
    return _wave(**{"v(in)": vin, "v(out)": vout})


def test_trip_point_symmetric():
    w = _symmetric_vtc(vm=VDD / 2)
    vm = measure.vtc_trip(w, "in", "out")
    assert abs(vm - VDD / 2) < 1e-2


def test_noise_margins_symmetric_are_balanced_and_positive():
    w = _symmetric_vtc(vm=VDD / 2)
    nm = measure.noise_margins(w, "in", "out")
    assert nm["NMH"] > 0 and nm["NML"] > 0
    assert abs(nm["NMH"] - nm["NML"]) < 1e-2          # symmetry
    assert nm["VIL"] < VDD / 2 < nm["VIH"]            # ordering
    assert nm["VOH"] > 0.9 * VDD and nm["VOL"] < 0.1 * VDD


def test_extract_square_law_recovers_kp_vt():
    # synthetic diode sweep: Id = 0.5*KP*(W/L)*(Vgs-Vt)^2 in saturation
    KP_true, Vt_true, WL = 120e-6, 0.42, 10 / 2
    vgs = np.linspace(0, 1.8, 1801)
    idd = np.where(vgs > Vt_true, 0.5 * KP_true * WL * (vgs - Vt_true) ** 2, 0.0)
    res = measure.extract_square_law(vgs, idd, wl=WL, vmin=1.0, vmax=1.7)
    assert abs(res["Vt"] - Vt_true) < 5e-3
    assert abs(res["KP"] - KP_true) / KP_true < 0.02


def test_noise_margins_skew_with_trip_point():
    # raising VM should grow NML and shrink NMH
    bal = measure.noise_margins(_symmetric_vtc(vm=VDD / 2), "in", "out")
    hi = measure.noise_margins(_symmetric_vtc(vm=0.7 * VDD), "in", "out")
    assert hi["NML"] > bal["NML"]
    assert hi["NMH"] < bal["NMH"]


# --- tau_from_step -----------------------------------------------------------

def test_tau_from_step_recovers_rc_time_constant():
    # v = Vf*(1 - exp(-t/tau)); the 63.2 % crossing is t = tau.
    tau, vf = 1e-9, 1.2
    t = np.linspace(0, 10 * tau, 20001)
    v = vf * (1 - np.exp(-t / tau))
    w = _wave(time=t, **{"v(out)": v})
    assert abs(measure.tau_from_step(w, "out") - tau) / tau < 0.02


def test_tau_from_step_uses_explicit_final_value():
    # A step that has not settled by the end of the window: the final sample is
    # not the asymptote, so v_final must be supplied.
    tau, vf = 1e-9, 1.2
    t = np.linspace(0, 1.5 * tau, 5001)
    v = vf * (1 - np.exp(-t / tau))
    w = _wave(time=t, **{"v(out)": v})
    assert abs(measure.tau_from_step(w, "out", v_final=vf) - tau) / tau < 0.02


def test_tau_from_step_raises_when_never_reached():
    t = np.linspace(0, 1e-9, 101)
    w = _wave(time=t, **{"v(out)": np.zeros_like(t)})
    try:
        measure.tau_from_step(w, "out", v_final=1.2)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for a signal that never rises")


# --- pulse_width -------------------------------------------------------------

def test_pulse_width_low_going():
    # The pulse generator output is low-going (its last stage is a NAND).
    t = np.linspace(0, 10e-9, 100001)
    v = np.where((t >= 4e-9) & (t < 5.5e-9), 0.0, VDD)
    w = _wave(time=t, **{"v(out)": v})
    got = measure.pulse_width(w, "out", vdd=VDD, polarity="low")
    assert abs(got - 1.5e-9) < 20e-12


def test_pulse_width_high_going():
    t = np.linspace(0, 10e-9, 100001)
    v = np.where((t >= 2e-9) & (t < 2.8e-9), VDD, 0.0)
    w = _wave(time=t, **{"v(out)": v})
    got = measure.pulse_width(w, "out", vdd=VDD, polarity="high")
    assert abs(got - 0.8e-9) < 20e-12


def test_pulse_width_rejects_bad_polarity():
    t = np.linspace(0, 1e-9, 101)
    w = _wave(time=t, **{"v(out)": np.zeros_like(t)})
    try:
        measure.pulse_width(w, "out", vdd=VDD, polarity="sideways")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for an invalid polarity")

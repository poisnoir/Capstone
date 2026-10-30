#!/usr/bin/env python3
import os, math, cmath
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from parse_raw import read_raw

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(BASE, "figs")
os.makedirs(FIG, exist_ok=True)

def save(fig, name):
    path = os.path.join(FIG, name)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)

# 1. Filter Bode
r = read_raw(os.path.join(BASE, "filter_ac.raw"))
f = np.array([z.real if isinstance(z, complex) else z for z in r["x"]], dtype=float)
y = np.array(r["cols"][r["vars"].index("V(out)")], dtype=complex)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.semilogx(f, 20*np.log10(np.abs(y)))
ax1.axvline(34e3, color="gray", ls=":", lw=1)
ax1.axvline(165.8e3, color="red", ls="--", lw=1)
ax1.set_ylabel("Gain (dB)")
ax1.set_title("LTC1563-2 4th-order Butterworth, fc = 60 kHz")
ax1.grid(True, which="both", alpha=0.3)
ax1.set_ylim(-80, 5)
ax2.semilogx(f, np.degrees(np.unwrap(np.angle(y))))
ax2.axvline(34e3, color="gray", ls=":", lw=1)
ax2.axvline(165.8e3, color="red", ls="--", lw=1)
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Phase (deg)")
ax2.grid(True, which="both", alpha=0.3)
save(fig, "fig_filter_bode.png")

# 2. Filter Monte Carlo
fcs = [58.8, 60.0, 61.2]
img = [-36.05, -35.35, -34.66]
ph = [-91.8, -89.7, -87.8]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(fcs, img, "o-", label="image at 165.8 kHz (dB)")
ax.set_xlabel("LTC1563-2 fc (kHz)")
ax.set_ylabel("Image attenuation (dB)")
ax.grid(True, alpha=0.3)
ax2 = ax.twinx()
ax2.plot(fcs, ph, "s--", color="tab:red", label="phase at 34 kHz (deg)")
ax2.set_ylabel("Phase at 34 kHz (deg)")
ax.set_title("Filter tolerance: fc ±2%")
ax.legend(loc="lower left", fontsize=8)
ax2.legend(loc="lower right", fontsize=8)
save(fig, "fig_filter_mc.png")

# 3. Summer 8-tone EVM
r = read_raw(os.path.join(BASE, "summer_8tone_eval.raw"))
t = np.array(r["x"], dtype=float)
v = np.array(r["cols"][r["vars"].index("V(out)")], dtype=float)
n0 = int(len(t)*0.2); n1 = len(t); N = n1-n0
win = 0.5 - 0.5*np.cos(2*np.pi*np.arange(N)/(N-1))
def dft(freq):
    ph = 2*np.pi*freq*t[n0:n1]
    return 2*np.sum(v[n0:n1]*win*np.exp(-1j*ph))/N
ideal = -0.212j
tones = [20,22,24,26,28,30,32,34]
evm = [20*np.log10(abs(dft(k*1e3)-ideal)/0.212) for k in tones]
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([str(k) for k in tones], evm, "o-")
ax.axhline(-60, color="red", ls="--", label="-60 dBc target")
ax.set_ylabel("8-tone EVM (dBc)")
ax.set_xlabel("Tone (kHz)")
ax.set_title("Summer 8-tone EVM, a3 for -110 dB single-tone THD")
ax.set_ylim(-80, -55)
ax.grid(True, axis="y", alpha=0.3)
ax.legend()
save(fig, "fig_summer_evm.png")

# 4. Gain sweep
gains = [2.0103, 1.5, 1.0]
vals = [-61.86, -66.96, -73.98]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(gains, vals, "o-")
ax.axhline(-60, color="red", ls="--", label="-60 dBc")
ax.set_xlabel("Summer gain")
ax.set_ylabel("24 kHz product (dBc)")
ax.set_title("Summer gain vs 24 kHz product (7-tone)")
ax.grid(True, alpha=0.3); ax.legend()
save(fig, "fig_gain_sweep.png")

# 5. INL sweep
nc = [1,2,3,5,7,11,17,31,63,127,257,511,1023]
inl = [-43.38,-43.38,-43.68,-45.99,-50.02,-55.51,-57.96,-66.47,-71.92,-76.19,-81.34,-86.31,-39.67]
fig, ax = plt.subplots(figsize=(7, 4))
ax.semilogx(nc, inl, "o-")
ax.axhline(-60, color="red", ls="--", label="-60 dBc")
ax.set_xlabel("INL pattern cycles across the code range")
ax.set_ylabel("24 kHz product (dBc)")
ax.set_title("DAC one-channel 8-tone stress vs INL pattern (1 LSB)")
ax.grid(True, which="both", alpha=0.3); ax.legend()
save(fig, "fig_inl_sweep.png")

# 6. Crosstalk
xt = [-60, -80, -100]
prod = [-122.74, -110.80, -85.43]
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar([str(x) for x in xt], [p + 130 for p in prod], bottom=-130, color="tab:green")
ax.axhline(-60, color="red", ls="--", label="-60 dBc")
ax.set_xlabel("Crosstalk level (dB)")
ax.set_ylabel("24 kHz product (dBc)")
ax.set_title("DAC crosstalk + INL sensitivity")
ax.set_ylim(-130, -50)
ax.grid(True, axis="y", alpha=0.3); ax.legend()
save(fig, "fig_crosstalk.png")

# 7. CRLB
labels = ["100B", "150B", "200B"]
req250_015 = [58, 26, 11]
req250_03 = [116, 52, 22]
actual = 5.3
x = np.arange(len(labels)); w = 0.35
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(x-w/2, req250_015, w, label="required, 0.15 mm @250 mA")
ax.bar(x+w/2, req250_03, w, label="required, 0.3 mm @250 mA")
ax.axhline(actual, color="red", ls="--", label="B air + INA163 ~5.3 pT")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("sigma_B (pT)")
ax.set_yscale("log")
ax.set_title("CRLB noise requirement vs coil/amp noise")
ax.grid(True, axis="y", which="both", alpha=0.3); ax.legend(fontsize=8)
save(fig, "fig_crlb.png")

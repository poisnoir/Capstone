#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 160)
ax.set_ylim(0, 100)
ax.axis("off")

def box(x, y, w, h, title, lines, fc, ec="#444444", fs=7):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=0.6",
                       linewidth=1.0, edgecolor=ec, facecolor=fc, zorder=1)
    ax.add_patch(p)
    ax.text(x + w/2, y + h - 1.6, title, ha="center", va="top",
            fontsize=fs + 0.5, fontweight="bold", zorder=2)
    for i, line in enumerate(lines):
        ax.text(x + w/2, y + h - 4.4 - i*2.7, line, ha="center", va="top",
                fontsize=fs, zorder=2)

def arrow(x1, y1, x2, y2, label="", color="#333333", rad=0.0, fs=6.5, lx=None, ly=None):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12,
                        linewidth=1.3, color=color, zorder=3,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    if label:
        if lx is None: lx = (x1 + x2) / 2
        if ly is None: ly = (y1 + y2) / 2 + 1.2
        ax.text(lx, ly, label, ha="center", va="bottom", fontsize=fs,
                color=color, zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

# Clock tree
box(2, 84, 36, 14, "Clock tree — one 32.768 MHz XO", [
    "XO 32.768 MHz → ADC MCLK + DDS",
    "PLL ×3 = 98.304 → ÷2 = 49.152 MHz SPI",
    "÷164 = 199.805 kSPS DAC update",
    "÷128 = 256 kSPS ADC ODR",
], "#eeeeee")

# FPGA
box(2, 26, 36, 56, "FPGA — Artix-7 XC7A35T: PL (pose)", [], "#dbe9f6")
box(4, 68, 32, 11, "DDS 8× 32-bit", [
    "FTW k×262144; LUT 4096×16",
    "16-bit amp + phase per tone",
], "#c9daf8")
box(4, 56, 32, 10, "SPI master 49.152 MHz", [
    "8×24-bit + TRIGGER = 216 bits",
    "software LDAC (0x05 bit 4); 199.805 kSPS",
], "#c9daf8")
box(4, 44, 32, 10, "ADC capture 4 lanes", [
    "DCLK 8.192 MHz; 4×DOUT; DRDY 256k",
    "ping-pong 4×512×32 bit",
], "#c9daf8")
box(4, 32, 32, 10, "Goertzel 8×4 + LM/TRF 8×5", [
    "J = 40…68; 2 ms frame",
    "pose/status 115–151 Hz",
], "#c9daf8")
ax.text(20, 29.2, "Host PC (USB-UART): log / cal / camera",
        ha="center", va="center", fontsize=6.3, zorder=2)
ax.text(20, 27.2, "PL → Pico 2 UART: pose + STOP",
        ha="center", va="center", fontsize=6.3, zorder=2)

# DAC
box(50, 64, 18, 16, "DAC80508", [
    "16-bit, 8 ch", "0–5 V, internal 2.5 V",
    "SPI 49.152 MHz", "199.805 kSPS",
], "#d9ead3")

# Filter
box(76, 62, 18, 20, "8× LTC1563-2", [
    "4th-order", "Butterworth 60 kHz",
    "one R per channel", "−35 dB @ 165.8 kHz",
], "#fce5cd")

# Current loop
box(102, 62, 18, 20, "8× current loop", [
    "OPA192 + LMH6321", "1 Ω sense, 100 µF",
    "150/250 mA RMS", "midrail 7.5 V",
], "#f4cccc")

# FG coils
box(128, 62, 20, 20, "8× FG coils", [
    "20–34 kHz", "one tone per coil",
    "B 0.1–5.76 µT", "150 mm cube",
], "#d9d2e9")

# ADC
box(76, 40, 18, 14, "AD7768-4", [
    "4 ch, 24-bit", "256 kSPS",
    "4 DOUT lanes", "SYNC/START/DRDY",
], "#cfe2f3")

# Summer
box(50, 38, 18, 14, "Current-sense summer", [
    "8× R_store 1 Ω", "×2.0103",
    "Ch0 = Y_I", "8 tones",
], "#fff2cc")

# Pen
box(102, 36, 22, 18, "Pen coil B", [
    "319 T, 804 µH", "INA163 G = 35",
    "ADA4940-2 G = 2", "ADC Ch1–3",
], "#e6b8af")

# E-stop
box(128, 22, 22, 10, "E-stop / watchdog", [
    "NC mushroom + relay", "opto status; stop ≤100 ms",
], "#f4cccc")

# Pico
box(2, 10, 36, 12, "Pico 2 — follower motor controller", [
    "step/dir + encoder loop", "homing/limits/local stop",
    "receives pose + STOP from PL",
], "#d9d2e9")

# Arrows
arrow(20, 84, 20, 82, "", color="#666666")
arrow(38, 71, 50, 72, "SPI 49.152 MHz\n216 bits, SW LDAC", color="#1f4e79", lx=44, ly=74.5)
arrow(68, 72, 76, 72, "0–5 V\n8 tones", color="#333333", lx=72, ly=74.5)
arrow(94, 72, 102, 72, "4th-order", color="#333333", lx=98, ly=74.5)
arrow(120, 72, 128, 72, "", color="#990000")
arrow(138, 62, 118, 55, "B field", color="#674ea7", rad=0.15, lx=130, ly=57)
arrow(111, 62, 62, 52, "R_store 0.15–0.5 V/tone", color="#990000", rad=-0.05, lx=85, ly=58)
arrow(68, 45, 76, 46, "Ch0", color="#333333", lx=72, ly=47.5)
arrow(102, 46, 94, 46, "Ch1–3", color="#333333", lx=98, ly=47.5)
# ADC -> FPGA capture: route below the summer
ax.plot([85, 85, 38], [40, 35.5, 35.5], color="#1f4e79", lw=1.3, zorder=3)
arrow(38, 35.5, 36, 48, "", color="#1f4e79")
ax.text(61, 34.0, "DCLK 8.192 / 4×DOUT / DRDY", ha="center", va="top",
        fontsize=6.5, color="#1f4e79", zorder=4,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
arrow(20, 26, 20, 22, "PL → Pico: UART\npose + STOP, 116 Hz", color="#333333", lx=20, ly=23.2, fs=6.0)
arrow(128, 27, 38, 30, "status", color="#990000", rad=0.1, lx=82, ly=28)
arrow(139, 32, 120, 62, "", color="#990000")
ax.text(141, 45, "enable", rotation=90, ha="center", va="center", fontsize=6.5,
        color="#990000", zorder=4,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

# Legend
ax.text(2, 5.5, "Protocols: one SPI (49.152 MHz, 8×24-bit + TRIGGER = 216 bits) to DAC80508; one ADC (DCLK 8.192 MHz, 4 lanes, 256 kSPS); "
        "one 32.768 MHz XO; DAC update 199.805 kSPS (÷164); DDS 32-bit; 8 tones 20–34 kHz.",
        fontsize=7, color="#444444")
ax.text(2, 2.5, "M16 section — FPGA → DAC80508 → 8× LTC1563-2 60 kHz → 8× LMH6321 current loop → 8 FG coils; "
        "current-sense Ch0 and pen Ch1–3 return to the AD7768-4.",
        fontsize=7, color="#444444")
ax.text(2, 0.2, "Handoff: m16-fpga-handoff.md — PL = pose; host PC = log/cal; Pico 2 = motor control. "
        "The handoff and this diagram are cross-referenced.",
        fontsize=7, color="#444444")

plt.tight_layout()
out = Path(__file__).resolve().parents[2] / "docs/handoff"
out.mkdir(parents=True, exist_ok=True)
plt.savefig(out / "m16-section-diagram.png", dpi=180, bbox_inches="tight")
plt.savefig(out / "m16-section-diagram.svg", bbox_inches="tight")
print("saved")

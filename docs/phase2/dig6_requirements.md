# Phase 2 — DIG-6 digital, demod, timing requirements

**Status:** DIG-6 requirements **PROPOSED 2026-10-27**, pending team approval.
These are the requirements that the RTL/HLS implementation and the bench gate
must meet. Bench timing, integer-J leakage, and the 1-hour run remain
verification gates.

**Sources:** `docs/phase2/tone_plan.md`; `docs/phase2/adc_interface_closure.md`;
`docs/phase2/design_order.md` §8; `docs/phase2/fpga_justification_and_requirements.md`;
`docs/phase2/fpga_vs_mcu_compute_budget.md`; `software/anser-matlab-ref/README.md`;
AD7768-4 Rev.D datasheet; `simulations/field_jacobian.py`.

---

## 1. Clock tree (one clock, integer divides)

One 32.768 MHz CMOS XO (Citizen CSX750FBC32.768M-UT, 3.3 V) feeds the ADC
MCLK and the FPGA. The ADC/DAC rates are integer divides; the SPI is a
3/2 PLL ratio (98.304 MHz ÷2):

| Rate | Divide | Value | Use |
|---|---|---|---|
| XO / ADC MCLK | ÷1 | 32.768 MHz | AD7768-4 MCLK; FPGA DDS clock |
| DAC SPI SCLK | ×3/2 (98.304 ÷2) | **49.152 MHz** | DAC80508 SCLK; 216-bit burst |
| DAC update | ÷164 | **199.805 kSPS** | 8 DAC words per 5.005 µs period |
| ADC ODR | ÷128 | 256 kSPS | 4-channel frames |
| Frame | N=512 | 2.000 ms | integer-J observation window |

Why this is exact: the tones are \(f_k=2\,\mathrm{kHz}\cdot k\), \(k=10\ldots17\).
With a 32.768 MHz clock,

\[
f_k=\frac{32.768\ \mathrm{MHz}\cdot k}{16384},
\qquad
\mathrm{FTW}_k=k\cdot\frac{2^{32}}{16384}=k\cdot 262144.
\]

The 32-bit tuning words are exact integers:

| Tone | k | FTW (decimal) | FTW (hex) |
|---|---|---|---|
| 20 kHz | 10 | 2,621,440 | 0x00280000 |
| 22 kHz | 11 | 2,883,584 | 0x002C0000 |
| 24 kHz | 12 | 3,145,728 | 0x00300000 |
| 26 kHz | 13 | 3,407,872 | 0x00340000 |
| 28 kHz | 14 | 3,670,016 | 0x00380000 |
| 30 kHz | 15 | 3,932,160 | 0x003C0000 |
| 32 kHz | 16 | 4,194,304 | 0x00400000 |
| 34 kHz | 17 | 4,456,448 | 0x00440000 |

No fractional tuning word, no DDS/ADC beat, no per-frame phase reset. The ADC
sample clock is 32.768 MHz/128 = 256 kSPS; the ADC frame is 512 DRDY pulses =
2.000 ms; the tones land on bins \(J_k=f_k/500=40,44,\ldots,68\).

---

## 2. DDS requirements

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| DIG-01a | 8 independent 32-bit phase accumulators at 32.768 MHz; exact FTWs above; per-tone 16-bit phase offset and 16-bit amplitude | Independent amplitude/phase per coil for κ/field calibration; exact integer tones | Two-tone/8-tone FFT; phase at each tone |
| DIG-01b | One shared 4096×16 sine LUT; 12-bit phase truncation; 16-bit amplitude multiplier per tone | 12-bit truncation gives ≈72 dBc phase-truncation spurs, below the −60 dBc spur budget; 4096×16 = 64 kb = 2 BRAM36 | Spur FFT; LUT utilization |
| DIG-01c | DDS update at **199.805 kSPS (÷164)**; one SPI at **49.152 MHz**, 24-bit frame per channel, 8 data frames + 24-bit TRIGGER (0x05 bit 4) = **216 bits** | 216 bits at 49.152 MHz = **4.394 µs** < 5.005 µs; the software LDAC removes inter-channel skew; ≥1 µs between output updates is met | Logic-analyser capture; DAC update rate |
| DIG-01d | Amplitude/phase words double-buffered; update on frame boundary, not mid-frame | No phase discontinuity or amplitude step in the observation window | Frame-boundary scope/FFT |
| DIG-01e | DDS output disabled/zero on fault or E-stop, independent of the solver | Fail-safe stop; no residual field | Fault injection |

**DAC interface.** 1× DAC80508 (16-bit, 8 channels, 200 kSPS, SPI) + 8×
LTC1563-2 (4th-order Butterworth, 60 kHz, one resistor per channel). One 24-bit
frame per channel; 8 channels = **192 bits**; at **49.152 MHz** the burst is
**3.906 µs** inside the **5.005 µs** update period. The DAC80508 has **no LDAC
pin**: send a 9th 24-bit frame writing **TRIGGER (0x05) bit 4 = 1** (216 bits =
**4.394 µs**). Write SYNC (0x02) = 0x00FF once at init to select synchronous mode.
Leave one idle SCLK period on each side of every frame (`tCSH` ≥ 10 ns, `tCSHIGH` ≥ 15 ns), so the
real burst is **4.720 µs**; do not stream the 216 bits back-to-back. At 49.152 MHz the DAC hold
spec (`tSDIH` = 10 ns) leaves only **0.17 ns**, so delay the SDI output ~2.5 ns to balance
setup/hold at 2.67 ns each, and keep the SPI on-board
(`docs/handoff/m16-fpga-handoff.md` §4.5). The 4th-order filter gives **−35.3 dB**
at 165.8 kHz; the AD7768 digital filter stopband starts at 127.7 kHz, so the
199.805 kSPS images do not fold into the tone bins. The DAC words are decimated
by 164 from the 32.768 MHz DDS; the tones stay exact (FTW k×262144).

---

## 3. ADC capture requirements

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| DIG-02a | 4 channels, 32-bit frames, 256 kSPS; 4 DOUT lanes; DCLK 8.192 MHz | 4 × 32 × 256 k = 32.768 Mbit/s; 4 lanes = 8.192 MHz | 1-hour capture; drop counter |
| DIG-02b | One-time START/SYNC after power-up; discard the first 68 samples (266 µs); count DRDY; never pulse SYNC per frame | AD7768 wideband filter settling; preserve integer-J phase | Scope/counter |
| DIG-02c | Ping-pong BRAM: 4 ch × 512 samples × 32 bit = 64 kb per frame; 2 frames = 128 kb (4 BRAM36) | One frame is demodulated while the next is captured | BRAM utilization; no overwrite |
| DIG-02d | Frame boundary at DRDY count 512; timestamp from a free-running 32-bit counter | Deterministic latency and log timestamps | Timestamp check |
| DIG-02e | Lane/pin: 4 DOUT + DCLK + DRDY + SYNC/START + MCLK + RESET + SPI config = 2×8/custom header | 2×6 Pmod is insufficient | Pin-budget review |

---

## 4. Demodulation requirements

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| DIG-03a | Goertzel per tone per channel: 8 tones × 4 channels = 32 complex outputs per frame | Each coil transmits one tone; all tones are present at the pen; Ch0 is the current reference | Golden comparison |
| DIG-03b | Rectangular + integer-J primary; Hamming fallback; no per-frame window change without a flag | Rectangular is orthogonal at exact bins; Hamming fallback for interference | Leakage test, both windows |
| DIG-03c | \(Y_I\) from Ch0 (summed current) per tone; \(Y_V\) from the pen channel per tone; phase sign and fixed group-delay offset | κ/\(A_{sens}\) calibration absorbs the fixed offset; no per-frame phase search | Phase sweep; κ stability |
| DIG-03d | Output: 8 complex \(Y_V\), 8 complex \(Y_I\), per-frame timestamp, status | Solver and calibration consume the same record | Record format check |

Processing load: 32 Goertzels × 512 samples = 16,384 real multiplies per frame;
at 115.8 Hz = 1.90 M multiply/s, trivial for the PL.

---

## 5. Solver requirements

| ID | Requirement | Rationale | Verification |
|---|---|---|---|
| DIG-04a | 5-DOF state \((x,y,z,\theta,\phi)\); 8×5 Jacobian; bounds \(lb\le p\le ub\); no roll | Single coil cannot sense roll | Golden comparison |
| DIG-04b | Filament model Eq.(3.17)–(3.18): 800 segments/evaluation (8 coils × 25 turns × 4 traces); parallel/pipelined kernel | Dipole model invalid close to the planar coils | ≤20% vs field probe/golden |
| DIG-04c | LM/TRF with warm start, retry \(+[0,0,0,\pi,\pi]\), relaxed tolerance, bounded iterations | Null/hemisphere ambiguity at \(\theta=0\); worst-case deadline | Retry count; worst-case timing |
| DIG-04d | Cost \(F=V_d-\kappa V_m\); κ per coil/tone; zOffset; calibration record versioned | Eq.(3.26)–(3.27); κ absorbs gain/phase/current scaling | 7×7 κ fit residuals |

Compute: 800 segments × 6 forward-difference evaluations × 10 LM iterations =
48,000 filament evaluations per pose; at 115.8 Hz ≈ 5.6 M/s. The parallel kernel
covers this; the earlier 2.5–5.8 GFLOP/s estimate is the conservative bound.

---

## 6. Timing, latency, stop

| Term | Value | Note |
|---|---|---|
| Acquisition \(N/F_s\) | 2.000 ms | 512 / 256 k |
| ADC group delay | 0.133 ms | 34/ODR |
| Demod | 0.500 ms | 32 Goertzels, ping-pong |
| Solver | 5.000 ms | 10 LM iterations, warm start |
| Overhead (status, output, DMA) | 1.000 ms | — |
| **Pose period** | **8.633 ms** | **115.8 Hz** |
| Filter-off latency | ≈9.1 ms | Pose period + 0.5 ms output |
| Filter-on latency | ≤100 ms | Kalman group delay; measure |
| Stop (E-stop) | <1 ms hardware | NC button cuts driver enable |
| Stop (tracking lost/fault) | ≤100 ms | Watchdog + follower |

The 10 ms / 100 Hz requirement has 1.367 ms margin. If the solver exceeds 5 ms,
the fallbacks are: reduce LM iterations with warm start, relax tolerance, or
move the filament kernel to more parallel lanes. Do not lengthen the frame
without re-running SC-03/SC-01d.

---

## 7. Verification / exit gate

1. 8-tone FFT at the DAC output and at the current-sense Ch0: tones on bins,
   phase-truncation/DAC spurs ≤−60 dBc, no images in the 20–34 kHz band.
2. Integer-J leakage: rectangular vs Hamming; tone-to-tone leakage below the
   spur budget.
3. ADC capture: 4 lanes, 32.768 Mbit/s, 1-hour run, zero dropped frames.
4. Golden demod: FPGA I/Q vs MATLAB/Python for a prerecorded frame; amplitude
   and phase within tolerance.
5. Golden solver: pose vs MATLAB for the 98-point grid; worst-case retry count.
6. Timed loop: 8.633 ms worst case at 115.8 Hz; latency filter-off ≤20 ms;
   filter-on ≤100 ms; stop ≤100 ms.
7. 1-hour moving-sensor run: no lock loss, no retry storm, no dropped frame.

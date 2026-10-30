# Phase 2 — FPGA core justification and technical requirements

**Purpose.** This is the Phase 2 report section for the FPGA core: the component-level
alternative analysis, the full-FPGA decision, the technical requirements, the design
development plan, verification, schedule/budget impact, risks, and open items. It expands
`docs/phase2/fpga_vs_mcu_compute_budget.md` into the Phase 2 deliverable.

**Scope.** The FPGA pose pipeline: DDS excitation, ADC sync/capture, Goertzel demodulation,
filament field model, LM/TRF pose solver, calibration hooks, pose output, and safety
status. The host does logging, calibration UI, and visualization only. Motor firmware on
the Pico 2 boards is a separate subsystem.

**Sources.** Phase 1 report (specs #1–25); `Capstone_Manual_2026.pdf` pp.13–14;
`AGENTS.md` (2026-10-12 full-FPGA decision); `docs/phase2/README.md`;
`docs/phase2/design_order.md`; `docs/phase2/tone_plan.md`; `docs/phase2/adc_justification.md`;
`docs/phase2/fpga_vs_mcu_compute_budget.md`; `docs/phase2/anser-baseline-findings.md`;
`HAJ_Thesis_2018.pdf` §3–4; `AnserEMT-onlineversion.pdf`;
`Catheter Position Tracking ... ODonoghue et al.pdf`; AD7768/AD7768-4 Rev.D datasheet.

**Status.** Phase 2 design baseline. The FPGA board/part is **not frozen** (per
`AGENTS.md`); resource and timing numbers are estimates until synthesis/place-and-route.

---

## 1. Phase 2 requirement, Phase 1 deviation, and decision summary

### 1.1 What Phase 2 requires

The Phase 2 report must contain component-level alternatives (OIQ `{3.1.2}`), a design
review with block diagrams, the selected design, design development, deviations from
Phase 1, and an updated schedule/budget (`docs/phase2/README.md` §1; manual pp.13–14). This
document supplies the FPGA-core part of those sections.

### 1.2 Phase 1 deviation

Phase 1 §1 placed the pose solver on a PC. `AGENTS.md` (2026-10-12) overrides that:

> **Full-FPGA pose:** DDS excitation + ADC sync + demodulation + LM/TRF pose solver all
> in HDL/HLS on the FPGA. No PC-side pose solver; no MATLAB-in-loop.

The Phase 2 report must carry this as an explicit deviation with rationale. The reason is
the pose-rate requirement: the ancestor paper reached 15 Hz, MATLAB reached 50–72 Hz, and
Python reached ~138 Hz only in static tests. A 15 Hz system has a 7.5 Hz Nyquist limit and
misses the 6–12 Hz tremor band; the ≥100 Hz requirement needs a different architecture.

### 1.3 Decision

**Selected: full-FPGA programmable-logic pose pipeline.** The FPGA owns the common clock,
DDS, ADC capture, demodulation, filament model, and LM/TRF solver. The host is limited to
logging, calibration UI, and visualization. The motor/Pico firmware consumes the pose and
status.

The FPGA board/part remains **TBD**. Do not pin drivers, constraints, or a specific device
until the team freezes the board (`AGENTS.md`).

---

## 2. Ancestor heritage versus our design

### 2.1 Measured ancestor pose rates

| System / frame length | Hardware | Pose rate | Notes |
|---|---|---|---|
| AnserEMT paper (2017) | PC + NI DAQ | **15 Hz** | Nyquist 7.5 Hz; misses 6–12 Hz tremor |
| MATLAB, L=250 | PC + NI-6216 | **72 Hz static / 64 Hz dynamic** | Ttotal 13.9 ms; solve+overhead ≈11.4 ms |
| MATLAB, L=500 | PC + NI-6216 | 70 / 61 Hz | larger frame |
| MATLAB, L=1000 | PC + NI-6216 | 65 / 62 Hz | — |
| MATLAB, L=2000 | PC + NI-6216 | 50 / 50 Hz | Linux NI-DAQmx Base buffer bug forces large L empirically |
| MATLAB, L=5000 | PC + NI-6216 | 20 / 20 Hz | chosen for accuracy, not rate |
| Python, static | PC | up to ~138 Hz | static only; dynamic lower; no worst-case guarantee |
| **Our design target** | **FPGA** | **≥100 Hz** | 2 ms acquisition + 7.87 ms budget |

The best ancestor dynamic rate is **64–72 Hz**. The 138 Hz Python figure is static and does
not represent the moving-sensor/worst-case path. The ancestor’s own goal was a visualizer,
not a tremor-control loop.

### 2.2 Why the ancestor stopped at 72 Hz

At MATLAB L=250/Fs=100 kSPS:

\[
T_{total}=T_{acq}+T_{solve}+T_{overhead}
=2.5\ \mathrm{ms}+11.4\ \mathrm{ms}=13.9\ \mathrm{ms}
\;\Rightarrow\;72\ \mathrm{Hz}
\]

The acquisition is only 2.5 ms. The solver plus overhead is 11.4 ms. For 100 Hz the solve
must be under ~7.5 ms. Our design uses a 2 ms frame and a 7.87 ms budget; the gap to close
is the **solver**, not the ADC.

### 2.3 Ancestor limitations and our fixes

| Ancestor limitation | Consequence | Our fix |
|---|---|---|
| Separate DDS and ADC clocks | spectral leakage; practical L≥250; no exact integer-J | one TCXO → PLL → clk_dds + MCLK_adc |
| Muxed 16-bit NI-6216 | mux skew; phase calibration; 100 kS/s/ch | AD7768-4 simultaneous 24-bit, 256 kSPS/ch |
| Bulk matrix demodulation | memory/MAC heavy; L×8 | streaming Goertzel per tone |
| No parallel filament kernel | ~800 segments/eval serial | 800-segment parallel/pipelined kernel |
| Large frames for accuracy | 20–50 Hz at L=2000–5000 | 512-sample frames, 2 ms, 500 raw frames/s |
| Visualizer goal | no tremor loop, no deterministic deadline | 100 Hz pose target with worst-case timing |

### 2.4 The 2 ms frame is not the ADC’s conversion time

The 2 ms frame is the observation window:

\[
T_{frame}=\frac{N}{F_s}=\frac{512}{256{,}000}=2.000\ \mathrm{ms}
\]

The ADC produces a sample every \(1/256{,}000=3.906\ \mu s\) and streams continuously.
The 133 µs digital-filter group delay is latency, not the frame cadence. The FPGA counts
512 `DRDY` pulses; the frame is deterministic.

| Quantity | Value |
|---|---|
| ADC ODR | 256 kSPS per channel |
| Sample period | 3.906 µs |
| Frame length | 512 samples |
| Frame time | 2.000 ms |
| ADC group delay | 133 µs |
| Raw frame rate | 500 frames/s |
| DAQ heritage | 16-bit muxed, 100 kS/s/ch; 512 samples = 5.12 ms; L=250 = 2.5 ms |
| ADC vs DAQ | 24-bit simultaneous; 3-channel aggregate 768 kSPS; 2 ms frame |

N=256 would give a 1 ms frame, but only 2 bins between tones and no Hamming fallback;
N=1024 would give 4 ms. The 2 ms is a **tone-plan choice**, not an ADC limit. The ADC is
faster than the heritage DAQ in the actual 3-channel simultaneous case.

### 2.5 Raw frames versus poses

- Raw frames: **500 frames/s** (one 512-sample frame every 2 ms).
- Pose target: **≥100 poses/s**.
- At 100 Hz there are **5 raw frames per pose**, but the solver uses **one frame per
  solve**; the other four are decimated/discarded or used for monitoring.
- If the solver finishes in under 2 ms, the pose rate could approach 500 Hz; the current
  budget does not assume that.
- The pose rate is solver-limited, not ADC-limited.

---

## 3. Component-level alternatives (OIQ `{3.1.2}`)

### 3.1 Options

| Option | Description |
|---|---|
| **A. Full-FPGA** | DDS, ADC sync, demod, filament model, and LM/TRF solver in FPGA PL; host logs/visualizes only |
| **B. MCU-only** | High-end MCU captures ADC, demodulates, runs the solver; no FPGA |
| **C. PC/host solver** | PC or host CPU runs the solver; FPGA/MCU only capture; Phase 1 default (stale) |
| **D. Hybrid FPGA+MCU** | FPGA does capture/demod/filament kernel; MCU runs the 5×5 solver and I/O |

### 3.2 Weighted matrix

Weights reflect the Phase 1 specs and the Phase 2 risk. Scores are 1–5 (5 best).

| Criterion (weight) | Wt | A. Full-FPGA | B. MCU-only | C. PC/host | D. Hybrid |
|---|---|---|---|---|---|
| Worst-case pose rate ≥100 Hz | 0.30 | 5 | 2 | 3 | 4 |
| Determinism / latency | 0.20 | 5 | 2 | 2 | 4 |
| Phase/timing accuracy | 0.15 | 5 | 3 | 3 | 4 |
| Development effort / risk | 0.10 | 3 | 4 | 5 | 2 |
| Cost / board availability | 0.10 | 4 | 5 | 2 | 3 |
| Power / thermal | 0.05 | 4 | 5 | 1 | 3 |
| Flexibility / upgrade | 0.10 | 3 | 4 | 5 | 4 |
| **Weighted total (/5)** | **1.00** | **4.45** | **3.00** | **3.00** | **3.65** |

**Score rationale.** The pose-rate, determinism, and phase-accuracy weights total 0.65,
reflecting the Phase 1 hard specs. The full-FPGA total remains ahead even if its
development and flexibility scores drop by one point (4.45 → 4.25), while MCU-only and
hybrid stay below. Scores are team judgements, not measured values.

**Notes.**

- **A. Full-FPGA** wins on the hard requirements: parallel filament kernel, common-clock
  simultaneous capture, deterministic worst-case, no OS/USB in the loop. It loses on
  development effort and flexibility because HDL/HLS is harder to change than C.
- **B. MCU-only** is cheap, low-power, and easy to develop, but its serial FPU cannot
  guarantee the 100 Hz worst case and is far from 500 Hz. It may reach ~100 Hz only with
  an analytic Jacobian, no retries, and a reduced model.
- **C. PC/host** is easiest to develop but has OS/USB jitter, a muxed 16-bit DAQ, and no
  deterministic embedded path. The ancestor’s MATLAB path reached 72 Hz; the requirement
  is ≥100 Hz. It is also not a product architecture.
- **D. Hybrid** is viable and would score better than MCU-only, but it adds two platforms,
  an FPGA↔MCU interface, and still requires the FPGA. It is a fallback, not the baseline.

### 3.3 Decision

Select **A. Full-FPGA**. The weighted total is 4.45/5 versus 3.65 for the hybrid, 3.00 for
MCU-only, and 3.00 for PC/host. The decision is driven by the worst-case ≥100 Hz
requirement, deterministic timing, and phase accuracy, not by average throughput.

---

## 4. Compute justification summary

The full calculation is in `docs/phase2/fpga_vs_mcu_compute_budget.md`. The key results:

### 4.1 Workload

| Item | Value |
|---|---|
| Filament segments per field evaluation | 8 coils × 100 segments = **800** |
| FLOPs per segment | ≈58 (50–60 used) |
| FLOPs per field evaluation | **50–58 kFLOP** (20% overhead included) |
| Jacobian | forward difference: 1 base + 5 perturbations = **6 evals/iteration** |
| Nominal iterations | 20 → **120 evaluations/pose** |
| Nominal FLOPs/pose | **6–7 MFLOP** |
| `MaxFunEvals`/retry worst | **25–58 MFLOP/pose** |

### 4.2 Sustained throughput

| Case | 100 poses/s | 500 poses/s |
|---|---|---|
| 20 iter FD, nominal | **0.60–0.70 GFLOP/s** | 3.0–3.5 GFLOP/s |
| 40 iter FD | 1.2–1.4 GFLOP/s | 6.0–7.0 GFLOP/s |
| `MaxFunEvals` | 2.5–2.9 GFLOP/s | 12.5–14.5 GFLOP/s |
| Retry worst | **5.0–5.8 GFLOP/s** | 25–29 GFLOP/s |
| Analytic 20 iter | 0.20–0.46 GFLOP/s | 1.0–2.3 GFLOP/s |

The demod adds ~8 MFLOP/s; the ADC capture is data movement. The solver dominates.

### 4.3 MCU versus FPGA

| Platform | Effective FP32 | 100 Hz worst (FD) | 100 Hz analytic | 500 Hz nominal |
|---|---|---|---|---|
| Pico 2 / RP2350 | 0.05–0.1 GFLOP/s | no | no | no |
| STM32H7 / Teensy 4.1 | 0.2–0.6 GFLOP/s | no | borderline | no |
| i.MX RT1176 (1 GHz M7) | 0.5–0.7 GFLOP/s | no | marginal (≈1×) | no |
| STM32MP1 (A7 + NEON) | 0.65–0.9 GFLOP/s | no | yes (≈1.5×) | no |
| Mid-size FPGA (parallel kernel) | 2–40 GFLOP/s | yes | yes | yes/plausible |

Two cases, not one:

- **Finite-difference worst case (2.5–5.8 GFLOP/s at 100 Hz):** every MCU fails, 5–30× short.
- **Analytic 20-iteration (0.20–0.46 GFLOP/s):** a 1 GHz M7 or an A7 can meet it, but at only
  ~1–1.5× margin with no retry headroom. MCU-only is therefore viable **only with an analytic
  Jacobian**, and even then it has no worst-case margin.

The FPGA wins on **determinism**, not raw FLOPs: it makes the 8.633 ms period by construction,
while an MCU meets it on average and loses it on a cache miss or one extra iteration. See
`fpga_vs_mcu_compute_budget.md` §4.

### 4.4 Latency versus throughput

If acquisition and solve are sequential:

\[
T_{pose}=2.133\ \mathrm{ms}+T_s
\]

If pipelined, throughput is \(1/\max(2.133\ \mathrm{ms},T_s)\), but latency remains
\(2.133\ \mathrm{ms}+T_s\). The 100 Hz gate uses the sequential sum; a pipelined design can
raise throughput but cannot reduce latency.

---

## 5. FPGA architecture

```
TCXO ──→ PLL ──→ clk_dds ──→ 8-tone DDS ──→ DAC ──→ reconstruction ──→ coil driver
  │                └──→ MCLK_adc ──→ AD7768-4 ──→ DCLK/DOUT capture
  │                                      │
  │                                      └──→ 8-tone Goertzel ──→ B vector
  │                                                               │
  │                                      ┌──→ filament model (8×100) ──→ B, J
  │                                      │                               │
  └──→ sync/reset ──→ frame timing ──────┘                               ▼
                                                          LM/TRF 5-DOF solver
                                                                  │
                                                    pose (x,y,z,θ,φ) + status
                                                                  │
                                      ┌───────────────────────────┼───────────────┐
                                      ▼                           ▼               ▼
                              motor/Pico link              host log/UI      safety/watchdog
```

### 5.1 Modules

| Module | Function |
|---|---|
| Clock/reset | TCXO → PLL → `clk_dds`, `MCLK_adc`; one-time ADC sync; integer-J frame counter |
| DDS/excitation | 8 tones, 20–34 kHz @2 kHz, 32-bit accumulator, amplitude/phase control |
| DAC/reconstruction | 8-tone analog excitation; part/filter TBD |
| ADC capture | 3 active channels, 24-bit, DCLK/DOUT, 256 kSPS, 512-sample frames, ping-pong BRAM/DMA |
| Demod | 8 Goertzel tones; rectangular primary, Hamming fallback; \(Y_I/Y_V\), phase sign, fixed group-delay offset |
| Filament model | 8 coils, 100 segments/coil, Eq.3.17–3.18; parallel/pipelined B and Jacobian |
| Solver | LM/TRF, 5 DOF, bounds, warm start, retry, residual gate |
| Calibration | κ per coil/tone, 7×7 grid, 98 points, per-sensor switch |
| Output/status | 5-DOF pose + timestamp + tracking status; host and motor links |
| Safety/watchdog | tracking-lost, out-of-volume, fault, comm-loss; stop ≤100 ms |

### 5.2 Data flow and timing

1. The DDS streams the 8 tones continuously; the ADC streams at 256 kSPS.
2. The FPGA counts 512 `DRDY` pulses; the frame is 2 ms; the group delay is 133 µs.
3. The Goertzel demod runs on the frame; the B vector is available at the frame boundary.
4. The filament model and LM/TRF solve produce the pose; the result is timestamped and
   sent to the motor/host.
5. The next frame is acquired in ping-pong while the solver runs (pipelining) to preserve
   throughput.

---

## 6. Technical requirements

Status tags: `LOCKED` (source-backed), `PROPOSED` (needs approval/test), `TBD`.

### 6.1 Functional

| ID | Requirement | Threshold | Rationale | Verification |
|---|---|---|---|---|
| FPGA-F01 | 8-tone DDS | 20–34 kHz, 2 kHz spacing, 32-bit accumulator, continuous phase, amplitude control | `docs/phase2/tone_plan.md` | 8-tone FFT; phase continuity |
| FPGA-F02 | Common clock | One TCXO → PLL → `clk_dds` + `MCLK_adc`; integer-J; one-time sync | Removes DDS/ADC leakage; common-clock architecture | Clock-phase sweep; integer-J leakage |
| FPGA-F03 | ADC capture | 3 active channels; 24-bit; DCLK/DOUT; 256 kSPS; 512 samples/frame; DRDY; ping-pong; zero drops | AD7768-4; frame timing | 1-hour capture; drop counter |
| FPGA-F04 | Demod | 8 Goertzel tones; rectangular primary, Hamming fallback; \(Y_I/Y_V\); phase sign; fixed group-delay offset | Tone plan; `fSysGetField.m` | MATLAB golden comparison |
| FPGA-F05 | Filament model | 8 coils × 100 segments; Eq.3.17–3.18; parallel; B and Jacobian | Thesis §3; `spiralCoilFieldCalcMatrix.m` | Golden comparison; field probe |
| FPGA-F06 | Solver | LM/TRF; 5 DOF; bounds; warm start; retry; residual gate | Thesis Eq.3.26–3.27; `fSysDecodeField.m` | Golden; 98-point accuracy |
| FPGA-F07 | Calibration | κ per coil/tone; 7×7 grid; 98 points; per-sensor switch | Jaeger §7.2.2 | Calibration run; residuals |
| FPGA-F08 | Pose output | 5-DOF + timestamp + status; ≥100 Hz; host/motor links | Phase 1 #1–2, #16 | Timed run; log rate |

### 6.2 Performance

| ID | Requirement | Threshold | Rationale | Verification |
|---|---|---|---|---|
| FPGA-P01 | Pose rate | **≥100 poses/s worst-case**, including `MaxFunEvals`/retry; 500 raw frames/s; 500 Hz pose stretch | Phase 1 #16 | Worst-case timed run; drop counter |
| FPGA-P02 | Latency/stop | Filter-off ≤20 ms; filter-on ≤100 ms; stop ≤100 ms | Phase 1 #14–15, #17 | Onset/stop timing |
| FPGA-P03 | Timing budget | Acquisition 2.000 ms; group delay 0.133 ms; demod+solve <7.87 ms sequential | `docs/phase2/tone_plan.md`; 10 ms budget | Timed measurement |
| FPGA-P04 | Solver throughput | 2.5–5.8 GFLOP/s worst-case at 100 Hz; FPGA margin | `fpga_vs_mcu_compute_budget.md` | HLS/benchmark |
| FPGA-P05 | Tone accuracy/stability | TCXO ppm; integer-J; phase noise within budget | Tone plan | Spectrum/phase test |
| FPGA-P06 | Spur/leakage | 60–70 dB below tone; rectangular/Hamming | `docs/phase2/anser-baseline-findings.md` | 8-tone FFT |

### 6.3 Interface

| ID | Requirement | Threshold | Rationale | Verification |
|---|---|---|---|---|
| FPGA-I01 | ADC header | 3 active channels; 4/2 DOUT lanes; DCLK 6.144/12.288 MHz; 2×8/custom header, not 2×6 Pmod | AD7768-4 pin count | Pin-budget review; capture |
| FPGA-I02 | DAC/excitation | 8 tones; M16 DAC80508 (16-bit, 8 ch, 200 kSPS) + 8× LTC1563-2 (4th-order, 60 kHz); SPI 49.152 MHz; DAC update 199.805 kSPS | Driver interface | Two-tone/8-tone FFT; filter/image/EVM |
| FPGA-I03 | Host link | ≥100 Hz pose log; calibration UI; no pose solve on host | Full-FPGA decision | Log rate; host review |
| FPGA-I04 | Motor/Pico link | Pose/status; engage/stop; ≤100 ms | Phase 1 #17 | Integration test |
| FPGA-I05 | Clock/jitter | MCLK 32.768 MHz; jitter ≤30 ps for 104 dB (or system target) | RQ-A4 correction | Jitter measurement |

### 6.4 Resource and implementation

| ID | Requirement | Threshold | Rationale | Verification |
|---|---|---|---|---|
| FPGA-R01 | DSP/BRAM/LUT | 800-segment kernel + 8-tone Goertzel + solver; ≤70% utilisation; board TBD | Compute budget | Synthesis/place-and-route |
| FPGA-R02 | Memory | Frames, geometry, calibration; ping-pong BRAM/DDR; no drops | 500 frames/s | Resource report; soak test |
| FPGA-R03 | Timing closure | 100–200 MHz PL clock; CDC clean; deterministic | Real-time pipeline | Static timing analysis |
| FPGA-R04 | Toolchain | HLS/HDL flow; float/fixed decision; reproducible build | Development plan | Build log; review |

### 6.5 Safety and reliability

| ID | Requirement | Threshold | Rationale | Verification |
|---|---|---|---|---|
| FPGA-S01 | Fault/tracking loss | Status + stop ≤100 ms | Phase 1 #17 | Fault injection |
| FPGA-S02 | Watchdog/comm loss | Safe state; no motion on loss | Phase 1 non-functional | Fault injection |
| FPGA-S03 | Pose-path integrity | No single point of failure; self-test/CRC | Safety review | Review/test |

### 6.6 Acceptance criteria

- ≥100 poses/s **worst-case**, including `MaxFunEvals` and retry.
- 2.000 ms frame; 500 raw frames/s; zero dropped frames over 1 hour.
- Filter-off latency ≤20 ms; filter-on ≤100 ms; stop ≤100 ms.
- 5-DOF accuracy/repeatability per Phase 1 #5–6, #11; 98-point RMS Eq.7.10.
- ICNIRP ≤27 µT at accessible points; thermal/EMC per Phase 1 #20–25.
- 500 Hz pose is a stretch goal, not the baseline.

---

## 7. Design development plan

### 7.1 Work packages

| WP | Deliverable | Depends on | Status |
|---|---|---|---|
| WP-1 | System contract (SC-0): frame/volume, tone plan, ADC contract, budget | — | Tone plan locked; ADC datasheet in place; contract TBD |
| WP-2 | DDS + clock/PLL + DAC interface | SC-0, board | TBD |
| WP-3 | ADC capture (DCLK/DOUT, DRDY, ping-pong) | ADC-5, board | TBD |
| WP-4 | Goertzel demod + \(Y_I/Y_V\) + golden comparison | WP-3, tone plan | TBD |
| WP-5 | Parallel filament kernel (B, J) | FG-1 model | TBD |
| WP-6 | LM/TRF solver + calibration hooks | WP-4/5 | TBD |
| WP-7 | Pose output/status/host/motor | WP-6 | TBD |
| WP-8 | Worst-case/latency/1-hour verification | all | TBD |

### 7.2 Development method

1. Freeze the MATLAB/Python golden outputs for demod and solver on prerecorded frames.
2. Implement the DDS/clock/capture in RTL; verify on the board with a logic analyser.
3. Implement the Goertzel demod; compare against the golden matrix/Goertzel.
4. Implement the filament kernel in HLS/HDL; verify B/J against MATLAB at 66/100/150 mm.
5. Implement the solver; compare poses on the 98-point grid.
6. Run the worst-case `MaxFunEvals`/retry test and the 1-hour moving run.
7. Document resource/timing and update the Phase 2 report.

### 7.3 Stage gates

- **SC-0:** frame/volume, tone plan, ADC contract, budget.
- **DIG-6:** integer-J, lane rate, worst-case solver, ≥100 Hz.
- **INT-7:** κ, 98-point accuracy, latency/stop, ICNIRP, thermal/EMC.

---

## 8. Verification and acceptance

| Test | What it proves | Pass criterion |
|---|---|---|
| 8-tone FFT | DDS/demod/spur | 60–70 dB below tone; rectangular/Hamming |
| Integer-J on/off | Clock coherence | Leakage delta ≥10 dB |
| MATLAB golden | Demod/solver correctness | Pose/B vector within tolerance |
| Filament B/J | Model correctness | ≤20% vs field probe / golden |
| Worst-case solver | 100 Hz guarantee | ≥100 poses/s with retry |
| 1-hour moving run | Determinism | Zero dropped frames |
| Latency/stop | Real-time safety | ≤20/100 ms; stop ≤100 ms |
| 98-point RMS | Accuracy | Eq.7.10 target |
| ICNIRP/thermal/EMC | Safety/environment | Phase 1 #20–25 |

The DIG-06 gate replaces the compute estimates with measured cycles/evaluation and solver
time. The 500 Hz pose is a separate stretch goal.

---

## 9. Schedule and budget impact

### 9.1 Schedule

Phase 1 Gantt (Sept 2026–Apr 2027): Sept–Oct research/architecture; Oct–Nov component
select/procure; Oct–Jan FPGA + Kalman; Nov–Jan firmware/host; Dec assembly; Jan–Feb
integration; Feb 15 pre-demo; Mar 22 demo; Apr 2 report.

FPGA-specific milestones (dates to be set with the team):

| Milestone | Target | Status |
|---|---|---|
| SC-0 contract | Phase 2 design start | Tone plan locked; ADC datasheet in place |
| DDS/clock/capture bring-up | — | TBD |
| Demod golden match | — | TBD |
| Filament/solver golden match | — | TBD |
| Worst-case ≥100 Hz | DIG-6 | TBD |
| 98-point/ICNIRP | INT-7 | TBD |

The Phase 2 report must show the revised Gantt and any slippage with corrective action.

### 9.2 Budget

- The FPGA is on BRD-01 (XC7A35T-1FTG256C, ~$70 CAD) plus config flash and a USB-UART bridge;
  the Phase 1 "owned dev board, no BOM line" assumption is superseded by decision #26.
- Current BOM slices: ADC-01 ≈$122 CAD; PEN-ANA-01 ≈$68 CAD; system-to-date ≈$190 CAD
  against the ≤$1000 CAD/pair target.
- If the board changes, add the board/toolchain cost and update the BOM.
- The FPGA development effort (HLS/HDL, verification) is the main schedule cost, not
  parts.

### 9.3 Deviation to report

The Phase 1 “pose on PC” statement is replaced by the full-FPGA architecture. The report
must state the ancestor rates (15/72/138 static), the 100 Hz target, and the common-clock/
parallel-kernel rationale.

---

## 10. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| FPGA board/part not frozen | resource/timing unknown; schedule | freeze board early; keep RTL/HLS portable; ask before pinning |
| HLS resource/timing | may not fit or close timing | parallel/pipelined kernel; float/fixed study; synthesis early |
| Solver worst-case/retry | misses 100 Hz | warm start; analytic Jacobian; relaxed tolerance; cap retries; MATLAB golden |
| ADC header/pin count | 2×6 Pmod insufficient | use 2×8/custom header; verify pin budget |
| Clock jitter | SNR/phase degradation | TCXO/PLL selection; measure; 30 ps target for 104 dB |
| DAC part/reconstruction | excitation/spur | early DAC selection; 8-tone FFT |
| Thermal/power | board/enclosure | thermal test; power budget |
| Schedule/learning curve | integration slip | early prototype; simulation; staged gates |

**Fallbacks.** If the FPGA resource/timing fails, use a larger FPGA or the hybrid
FPGA+MCU split (FPGA capture/demod/filament, MCU 5×5 solver). A PC solver is not a
product fallback; it is only a development reference.

---

## 11. Open items

1. FPGA board/part and toolchain (do not pin until frozen).
2. HLS versus RTL split; float versus fixed point.
3. DAC part and reconstruction filter.
4. ADC header/pin budget (2×8/custom; not 2×6 Pmod).
5. TCXO/PLL jitter measurement and clock tree.
6. Resource/timing estimate and place-and-route.
7. Solver precision/tolerance and worst-case retry policy.
8. Host link/protocol and pose-log format.
9. Test data: prerecorded frames, 98-point grid, field-probe data.
10. Phase 2 report contribution summary for the FPGA owners.

---

## 12. Phase 2 report mapping

| Report section | This document |
|---|---|
| §3 system design review / block diagrams | §5 architecture; §4 timing |
| §4 component-level alternatives (OIQ 3.1.2) | §3 weighted matrix |
| §5 design development | §6 requirements; §7 plan; §8 verification |
| §6 deviations from Phase 1 | §1.2; §9.3 |
| §7 updated schedule/budget | §9 |
| §8 Phase 3 plan | §7/§10/§11 |
| Per-student contributions | FPGA lead; Phase 1 Table 8 owners (Kevin/William) |

**References.** `AGENTS.md`; `docs/phase2/README.md`; `docs/phase2/design_order.md`;
`docs/phase2/tone_plan.md`; `docs/phase2/adc_justification.md`;
`docs/phase2/fpga_vs_mcu_compute_budget.md`; `docs/phase2/anser-baseline-findings.md`;
`HAJ_Thesis_2018.pdf` §3–4; `AnserEMT-onlineversion.pdf`;
`Catheter Position Tracking ... ODonoghue et al.pdf`; `Capstone_Manual_2026.pdf`
pp.13–14; Phase 1 report; OIQ GPP; AD7768/AD7768-4 Rev.D datasheet.

---

## Appendix A — heritage rate table

| Frame length L | Acquisition \(L/F_s\) at 100 kSPS | Static rate | Dynamic rate |
|---|---|---|---|
| 250 | 2.5 ms | 72 Hz | 64 Hz |
| 500 | 5.0 ms | 70 Hz | 61 Hz |
| 1000 | 10.0 ms | 65 Hz | 62 Hz |
| 2000 | 20.0 ms | 50 Hz | 50 Hz |
| 5000 | 50.0 ms | 20 Hz | 20 Hz |

Paper: 15 Hz. Python static: up to ~138 Hz. The MATLAB L=250 solve+overhead is ~11.4 ms;
100 Hz needs <7.5 ms. Our design’s 2 ms acquisition leaves 7.87 ms.

## Appendix B — compute summary

| Case | FLOPs/pose | 100 Hz | 500 Hz |
|---|---|---|---|
| 20 iter FD, nominal | 6–7 M | 0.6–0.7 GFLOP/s | 3.0–3.5 GFLOP/s |
| 40 iter FD | 12–14 M | 1.2–1.4 GFLOP/s | 6.0–7.0 GFLOP/s |
| `MaxFunEvals` | 25–29 M | 2.5–2.9 GFLOP/s | 12.5–14.5 GFLOP/s |
| Retry worst | 50–58 M | 5.0–5.8 GFLOP/s | 25–29 GFLOP/s |

Detailed derivation: `docs/phase2/fpga_vs_mcu_compute_budget.md`.

## Appendix C — Phase 1 traceability

| Phase 1 spec | FPGA requirement |
|---|---|
| #1–2 pens/5-DOF | FPGA-F08; solver 5 DOF |
| #3–4 volume/angle | FPGA-F05/06; FG-1 model |
| #5–6 hand accuracy | FPGA-F05/06/07; 98-point |
| #9–10 tool accuracy | FPGA-P01/P03; solver |
| #12–13 tremor | FPGA-P01; 100 Hz pose |
| #14–16 latency/rate | FPGA-P01/P02/P03 |
| #17 stop | FPGA-S01/S02 |
| #20 ICNIRP | FG-1; INT-7 |
| #24 cost | §9.2 |

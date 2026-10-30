# FPGA vs MCU — pose-solver compute budget

**Purpose.** Quantify the 5-DOF pose-solver workload and justify the full-FPGA
architecture over an MCU for the **>100 poses/s** requirement. The ancestor (Anser)
pose-rate heritage is included as the baseline. This is an engineering estimate, not a
benchmark; the DIG-06 gate measures the real number.

**Phase 2 report section:** the full justification and technical requirements are in
`docs/phase2/fpga_justification_and_requirements.md`; this file is the detailed calculation
appendix.

**Sources.** `software/anser-matlab-ref/` (`fSysSetup.m`, `fSysDecodeField.m`,
`objectiveCoilSquareCalc3D.m`, `spiralCoilFieldCalcMatrix.m`);
`docs/phase2/anser-baseline-findings.md` §4–5, §9; `HAJ_Thesis_2018.pdf` §3–4;
`AnserEMT-onlineversion.pdf`; `docs/phase2/tone_plan.md`; `docs/phase2/design_order.md`.

**Status.** `PROPOSED` estimate. Assumptions are listed in §10; measured values replace
them at DIG-06.

**Bottom line.** The nominal finite-difference pose is ~6–7 MFLOP; the 100 Hz worst case
with `MaxFunEvals`/retry is 2.5–5.8 GFLOP/s. A high-end MCU’s effective FP32 throughput
is ~0.2–0.5 GFLOP/s; a mid-size FPGA’s parallel filament kernel is ~2–40 GFLOP/s. The
FPGA is required to guarantee ≥100 Hz worst-case; an MCU is only plausible for an
analytic, no-retry, ~100 Hz case. A 500 Hz pose needs the FPGA.

---

## 1. Requirement and timing frame

| Item | Value | Source |
|---|---|---|
| Pose rate | **≥100 poses/s** | Phase 1 #16 |
| Pose period at 100 Hz | 10 ms | — |
| Filter-off latency | ≤20 ms | Phase 1 #14 |
| Filter-on latency | ≤100 ms | Phase 1 #15 |
| DOF | 5: x, y, z, pitch, yaw | Phase 1 #1–2 |
| Transmitters | 8 coils, one tone each | `docs/phase2/tone_plan.md` |
| ADC frame | 512 samples at 256 kSPS = **2.000 ms** | `docs/phase2/tone_plan.md` |
| ADC group delay | 0.133 ms | AD7768-4 datasheet |
| Remaining for demod + solve | **7.867 ms** | 10 ms budget |
| Raw frame rate | 500 frames/s | 256 kSPS / 512 |
| Pose frames per solve | **1** | the solver uses one 512-sample frame, not 5 |

The raw 500 frames/s gives headroom for decimation/averaging/validation, but it is not a
500 poses/s guarantee. A 500 Hz pose would require the solver to finish in under 2 ms.

---

## 2. Ancestor heritage: what Anser actually achieved

| System / frame length | Hardware | Pose rate | Notes |
|---|---|---|---|
| AnserEMT paper (2017) | PC + NI DAQ | **15 Hz** | Nyquist 7.5 Hz; misses the 6–12 Hz tremor band |
| MATLAB, L=250 | PC + NI-6216 | **72 Hz static / 64 Hz dynamic** | Ttotal 13.9 ms; solve+overhead ≈11.4 ms |
| MATLAB, L=500 | PC + NI-6216 | 70 / 61 Hz | larger frame, more acquisition |
| MATLAB, L=1000 | PC + NI-6216 | 65 / 62 Hz | — |
| MATLAB, L=2000 | PC + NI-6216 | 50 / 50 Hz | Linux NI-DAQmx Base buffer bug forces large L empirically |
| MATLAB, L=5000 | PC + NI-6216 | 20 / 20 Hz | chosen for accuracy, not rate |
| Python, static | PC | up to ~138 Hz | static only; dynamic lower; deterministic rate not shown |
| **Our design target** | **FPGA** | **≥100 Hz** | 2 ms acquisition + 7.87 ms budget |

The key comparison is the MATLAB L=250 row: **2.5 ms acquisition + 11.4 ms solve+overhead
= 72 Hz**. The acquisition is not the gap; the solver is. To hit 100 Hz the solve must be
under ~7.5 ms; our budget allows 7.87 ms. The ancestor’s PC/MATLAB path does not meet the
requirement, and the 138 Hz Python figure is static, not a worst-case dynamic rate.

The ancestor also had separate DDS/ADC clocks, bulk matrix demodulation, and no parallel
filament kernel. Our design fixes those with a common clock, integer-J frames, streaming
Goertzel, and a parallel filament kernel — which is why the FPGA is the enabler.

---

## 3. Workload model

### 3.1 Filament kernel cost per evaluation

The objective function `objectiveCoilSquareCalc3D.m` calls
`spiralCoilFieldCalcMatrix.m` for all 8 coils. Each coil is a 25-turn spiral with
`4N + 1 = 101` points, i.e. **100 segments**. Total:

\[
8\ \text{coils}\times100\ \text{segments} = 800\ \text{segments per field evaluation}
\]

The per-segment operation count in `spiralCoilFieldCalcMatrix.m` is approximately:

| Operation | FLOPs |
|---|---|
| a, b, c differences (3 vectors) | 9 sub |
| \(\lvert b\rvert\), \(\lvert c\rvert\) (2 norms) | 12 |
| \(a\cdot b\), \(a\cdot c\) (2 dots) | 10 |
| \(c\times a\) | 9 |
| \(\lvert c\times a\rvert^2\) | 5 |
| scalar ratio (2 divides, 1 sub, 1 divide) | 4 |
| H contribution and accumulation | 9 |
| **Total per segment** | **≈58** |

Using 50–60 FLOPs/segment including loads/indexing:

\[
800 \times 50 = 40{,}000\ \text{FLOPs/eval}
\]
\[
800 \times 60 = 48{,}000\ \text{FLOPs/eval}
\]

Add ~20% for the cost/flux model, loop overhead, and coordinate updates:

\[
W_{eval} \approx 48{,}000\text{–}58{,}000\ \text{FLOPs/eval}
\]

Use **\(W_{eval}\approx50\ \text{kFLOP}\)** as the nominal figure.

### 3.2 Solver evaluations per pose

The heritage solver is `lsqnonlin` with 5 parameters and options
`TolFun=1e-16, TolX=1e-6, MaxFunEvals=500, MaxIter=40`
(`fSysSetup.m:184`). With the default forward-difference Jacobian, each iteration costs:

\[
1\ \text{base} + 5\ \text{perturbations} = 6\ \text{field evaluations}
\]

A 20-iteration solve therefore costs 120 evaluations; 40 iterations cost 240. The
`MaxFunEvals=500` cap allows more if line search/retries occur. `fSysDecodeField.m:25-32`
adds a **second full solve** from a mirrored initial estimate if the residual exceeds
1e-15, so the absolute worst case is ~1000 evaluations.

An optimised analytic Jacobian would cost roughly 2–4 field-evaluation equivalents per
iteration (one field + one gradient, with the gradient itself 1–3× the field cost). That
is the optimistic case; the heritage finite-difference case is the conservative one.

| Scenario | Evaluations/pose | Notes |
|---|---|---|
| 10 iterations, FD Jacobian | 60 | fast/typical |
| 20 iterations, FD | 120 | nominal |
| 40 iterations, FD | 240 | MaxIter |
| MaxFunEvals | 500 | line-search worst |
| Retry | 1000 | two solves |
| 20 iterations, analytic | 40–80 eval-equiv | optimised |
| 40 iterations, analytic | 80–160 eval-equiv | optimised worst |

### 3.3 FLOPs per pose

Using \(W_{eval}=50\text{–}58\ \text{kFLOP}\):

| Evaluations/pose | FLOPs/pose | Notes |
|---|---|---|
| 60 | **3.0–3.5 MFLOP** | 10 iter FD |
| 120 | **6.0–7.0 MFLOP** | 20 iter FD, nominal |
| 240 | **12–14 MFLOP** | 40 iter FD |
| 500 | **25–29 MFLOP** | MaxFunEvals |
| 1000 | **50–58 MFLOP** | retry worst |
| 40–80 (analytic) | **2.0–4.6 MFLOP** | optimised |
| 80–160 (analytic) | **4.0–9.3 MFLOP** | optimised worst |

The nominal finite-difference pose is **~6–7 MFLOP**; the worst-case retry is
**~50–58 MFLOP**.

### 3.4 Sustained throughput

| Case | FLOPs/pose | At 100 poses/s | At 500 poses/s |
|---|---|---|---|
| 10 iter FD | 3.0–3.5 M | **0.30–0.35 GFLOP/s** | 1.5–1.75 GFLOP/s |
| 20 iter FD (nominal) | 6.0–7.0 M | **0.60–0.70 GFLOP/s** | 3.0–3.5 GFLOP/s |
| 40 iter FD | 12–14 M | **1.2–1.4 GFLOP/s** | 6.0–7.0 GFLOP/s |
| MaxFunEvals | 25–29 M | **2.5–2.9 GFLOP/s** | 12.5–14.5 GFLOP/s |
| Retry worst | 50–58 M | **5.0–5.8 GFLOP/s** | 25–29 GFLOP/s |
| Analytic 20 iter | 2.0–4.6 M | **0.20–0.46 GFLOP/s** | 1.0–2.3 GFLOP/s |
| Analytic 40 iter | 4.0–9.3 M | **0.40–0.93 GFLOP/s** | 2.0–4.6 GFLOP/s |

The demod adds about 8 MFLOP/s (8 tones × 512 samples × 500 frames/s), negligible. The
ADC capture is data movement, not FLOPs. The pose solver dominates.

These are **solver throughputs**, not end-to-end pose rates. Sequential pose period is
\(T_{pose}=2.133\ \mathrm{ms}+T_s\); a pipelined design has throughput
\(1/\max(2.133\ \mathrm{ms},T_s)\) but latency \(2.133\ \mathrm{ms}+T_s\). The 100 Hz
gate uses the sequential sum; pipelining can raise throughput but cannot reduce latency.

---

## 4. MCU capability

| Device class | Core / clock | Peak FP32 | Effective FP32 | 100 Hz worst (2.5–5.8 GFLOP/s) | 100 Hz analytic (0.20–0.46 GFLOP/s) | 500 Hz nominal (3.0–3.5 GFLOP/s) |
|---|---|---|---|---|---|---|
| Pico 2 / RP2350 | 2× Cortex-M33, 150 MHz | ~0.15–0.3 GFLOP/s | 0.05–0.1 | no | no | no |
| STM32H7 | Cortex-M7, 480 MHz | ~0.5–1.0 | 0.2–0.5 | no | borderline | no |
| Teensy 4.1 | Cortex-M7, 600 MHz | ~0.6–1.2 | 0.3–0.6 | no | borderline | no |
| Dual-core H7 | 2× Cortex-M7, 480+240 | ~1–2 | 0.3–0.6 | no | borderline | no |
| i.MX RT1176 | Cortex-M7, 1 GHz | ~1.5–2.0 | 0.5–0.7 | no | marginal (≈1×) | no |
| STM32MP1 | Cortex-A7, 650 MHz + NEON | ~2.6 | 0.65–0.9 | no | yes (≈1.5×) | no |

The effective numbers account for FPU latency, divides/sqrts in the filament model,
memory/cache stalls, ADC/DMA interrupts, and demod/control overhead. Double precision
is slower again. The heritage solver’s `TolFun=1e-16` is double precision; a single-
precision MCU port would need a relaxed tolerance and re-validation.

**What an MCU could do.** A high-end H7/Teensy might reach 100 Hz in the **analytic,
20-iteration, no-retry** case (0.20–0.46 GFLOP/s), which is at the edge of its effective
throughput. A 1 GHz M7 (RT1176) or an A7 (STM32MP1) can meet that case at ~1–1.5× margin.
None of them can guarantee the **finite-difference/40-iteration/MaxFunEvals/retry** worst
case (1.2–5.8 GFLOP/s at 100 Hz), and none is close to 500 Hz. The Pico 2 is a motor
controller, not a solver candidate.

**The decisive difference is determinism, not throughput.** The FPGA makes the 8.633 ms
period by construction; an MCU meets it on average and misses it on a cache miss or one
extra iteration. MCU-only is viable only with an analytic Jacobian and no retry headroom.

---

## 5. FPGA capability

A mid-size FPGA with 100–500 DSP slices at 100–200 MHz provides 10–100 GMAC/s
(20–200 GFLOP/s peak). Even at 10–50% effective utilisation for floating-point HLS, that
is 2–100 GFLOP/s — enough for the 100 Hz worst case and, with a larger device, the 500 Hz
case.

The structural advantage is the **800-segment parallel kernel**:

- 800 independent segments, one per lane or a few per DSP.
- Each segment ~50–60 FLOPs.
- One field evaluation is ~40–48 kFLOPs.
- 120 evaluations/pose = ~6 MFLOP/pose.
- At 500 poses/s, ~3 GFLOP/s; even a small FPGA can hold this with pipelining.
- The serial LM iterations are a control FSM; the 5×5 matrix algebra is trivial compared
  with the filament kernel.

A rough resource check: 220 DSPs at 200 MHz = 44 GMAC/s. If each segment takes ~20
cycles on a DSP, 800 segments / 220 DSPs ≈ 4 segments per DSP, ~80 cycles per evaluation;
120 evaluations ≈ 9,600 cycles ≈ 48 µs at 200 MHz. That leaves the 2 ms/500 Hz frame
period almost entirely free; the real limit becomes memory/pipeline/solver control, not
raw DSP throughput. The exact placed-and-routed number is TBD, but the margin is large.

### 5.1 Memory and data bandwidth (not the bottleneck)

| Item | Value |
|---|---|
| Coil geometry | 8 coils × 101 points × 3 coords × 4 B ≈ **9.7 kB** |
| Per-evaluation intermediates | 800 segments × 6 floats × 4 B ≈ **19.2 kB** |
| ADC frame (3 channels, 24-bit) | 3 × 512 × 24 bits ≈ **4.6 kB** |
| ADC data rate at 500 frames/s | ≈ **2.3 MB/s**; 18.4 Mbit/s |
| DCLK, 4 lanes / 2 lanes | 6.144 MHz / 12.288 MHz |
| Goertzel demod | 8 × 512 × 500 ≈ 2.05M complex MAC/s ≈ **8.2 MFLOP/s** |
| Solver state | 5 parameters + 8×5 Jacobian + 8 residuals: **<1 kB** |

All of this fits in FPGA BRAM/registers or MCU SRAM. The problem is arithmetic
throughput and deterministic scheduling, not memory capacity.

---

## 6. Side-by-side conclusion

| Platform | Parallelism | Effective compute | 100 Hz worst case | 500 Hz nominal | Verdict |
|---|---|---|---|---|---|
| Pico 2 | serial | 0.05–0.1 GFLOP/s | no | no | motor control only |
| High-end MCU | serial FPU | 0.2–0.5 GFLOP/s | no | no | maybe analytic 100 Hz, not guaranteed |
| Mid-size FPGA | 800-segment parallel | 2–40 GFLOP/s | yes | yes/plausible | **selected** |
| PC/MATLAB heritage | serial/interpreted | measured 72 Hz | no | no | not embedded |
| PC/Python heritage | serial | measured ~138 Hz static | static only | no | not worst-case/dynamic |

The requirement is **≥100 Hz as a minimum**, not an average. The finite-difference
heritage solver plus retry needs 2.5–5.8 GFLOP/s at 100 Hz; a high-end MCU’s effective
0.2–0.5 GFLOP/s is roughly 5–30× short. The FPGA’s parallel kernel covers the worst case
with margin. At 500 Hz, the MCU is not viable at all; the FPGA is the realistic path.

---

## 7. Determinism, capture, and interface

- **Deterministic timing.** The FPGA pipeline has no cache, no interrupt jitter, and a
  fixed frame cadence. The MCU’s cache, DMA arbitration, and interrupts make the
  worst-case solver time variable; a retry can miss the 10 ms pose deadline even if the
  average looks acceptable. The 100 ms stop/tracking-lost requirement also needs a
  deterministic worst case.
- **ADC capture.** The AD7768-4 data path is DCLK/DOUT lanes at 18.4 Mbit/s (3 channels,
  24-bit, 256 kSPS), not SPI. The FPGA captures it in logic and frames it with DRDY. An
  MCU would need a parallel capture peripheral (DCMI/FlexIO) plus DMA; the CPU then also
  runs the demod and solver.
- **Demod.** Eight Goertzel tones × 512 samples at 500 frames/s ≈ 2M complex MAC/s.
  This is small, but it is another deterministic real-time task that the FPGA does in
  logic while the MCU would do on the CPU.
- **DDS/ADC common clock.** The FPGA owns the integer-J framing and DDS phase; the MCU
  would have to service the ADC and DDS without breaking the phase lock.

---

## 8. What would change the conclusion

An MCU could become viable at ~100 Hz if one or more of these hold:

1. **Analytic Jacobian** and a converged 10–20-iteration solver with no retries.
2. **Reduced filament count** (fewer segments/turns) with calibration, or a precomputed
   field/gradient grid with interpolation.
3. **Single-precision** solver with relaxed tolerance, validated against the 2 mm/1°
   accuracy target.
4. **Pose rate requirement lowered** to ~50 Hz.
5. **Hybrid FPGA+MCU**: FPGA does capture/demod/filament kernel, MCU does the 5×5
   solver. This still requires the FPGA, so it does not replace it.

For **500 Hz pose**, none of these make an MCU sufficient; the FPGA (or a larger
FPGA/SoC) is required. The current design target remains 100 Hz, with 500 Hz raw frames
as headroom, not a 500 Hz pose promise.

---

## 9. Verification plan (DIG-06)

1. Instrument the MATLAB/Python golden solver to count function evaluations, iterations,
   and retries over the 98-point calibration grid (85.6/152 mm).
2. Port the objective to C and run on a high-end MCU (H7/Teensy) and the Pico 2; measure
   cycles/evaluation and effective GFLOP/s.
3. HLS the filament kernel for the target FPGA; measure cycles/evaluation, DSP/BRAM
   utilisation, and the full solver loop.
4. Measure the **worst case**, including `MaxFunEvals` and the mirrored retry, not just
   the average.
5. Run the 1-hour moving-sensor test at ≥100 Hz with a drop counter; confirm zero dropped
   frames and the ≤100 ms stop.
6. Report the measured pose rate, latency, and solver eval count in the Phase 2 report.

**Acceptance:** ≥100 poses/s worst-case; raw frame capture at 500 frames/s; zero dropped
frames; latency and stop within Phase 1 #14–17. A 500 Hz pose is a separate stretch goal.

---

## 10. Assumptions and caveats

- 800 segments/evaluation (8 coils × 100 segments; `4N+1` points, N=25).
- 50–60 FLOPs/segment; the operation count is an estimate, not an instruction count.
- Forward-difference Jacobian: 6 evaluations/iteration; analytic: 2–4 equivalents.
- 10–40 iterations; `MaxFunEvals=500`; retry doubles to ~1000.
- 20% solver/loop overhead included in the 50–58 kFLOP/evaluation figure.
- MCU/FPGA effective throughput is an order-of-magnitude estimate; no benchmark yet.
- The FPGA device is not frozen; resource/timing numbers are illustrative.
- The tone plan changes acquisition, not the solver’s segment count or iteration count.

---

## Appendix A — per-segment FLOP derivation

From `spiralCoilFieldCalcMatrix.m`:

\[
\mathbf{B}=\frac{\mu_0 I}{4\pi}\,
\frac{\mathbf{c}\times\mathbf{a}}{|\mathbf{c}\times\mathbf{a}|^2}
\left(\frac{\mathbf{a}\cdot\mathbf{c}}{|\mathbf{c}|}
-\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{b}|}\right)
\]

| Step | Count |
|---|---|
| \(\mathbf{a}=\mathbf{p}_2-\mathbf{p}_1\), \(\mathbf{b}=\mathbf{p}_2-\mathbf{P}\), \(\mathbf{c}=\mathbf{p}_1-\mathbf{P}\) | 9 sub |
| \(\lvert\mathbf{b}\rvert\), \(\lvert\mathbf{c}\rvert\) | 2×(3 mult + 2 add + 1 sqrt) = 12 |
| \(\mathbf{a}\cdot\mathbf{b}\), \(\mathbf{a}\cdot\mathbf{c}\) | 2×(3 mult + 2 add) = 10 |
| \(\mathbf{c}\times\mathbf{a}\) | 6 mult + 3 sub = 9 |
| \(\lvert\mathbf{c}\times\mathbf{a}\rvert^2\) | 3 mult + 2 add = 5 |
| scalar ratio | 2 div + 1 sub + 1 div = 4 |
| H contribution + accumulation | ≈9 |
| **Total** | **≈58** |

## Appendix B — solver settings and retry path

- `fSysSetup.m:184`: `optimset('TolFun',1e-16,'TolX',1e-6,'MaxFunEvals',500,'MaxIter',40,'Display','off')`.
- `fSysDecodeField.m:25`: first `lsqnonlin` from `sys.estimateInit`.
- `fSysDecodeField.m:27-32`: if `resnorm > 1e-15`, second `lsqnonlin` from
  `sys.estimateInit + [0,0,0,pi,pi]`; if still above, return the initial estimate.
- `fSysSetup.m:204-205`: `MA_length=5` moving average of **pose estimates** for warm
  start, not five raw frames per pose.

## Appendix C — heritage pose-rate table

| Frame length L | Acquisition \(L/F_s\) at 100 kSPS | Static rate | Dynamic rate |
|---|---|---|---|
| 250 | 2.5 ms | 72 Hz | 64 Hz |
| 500 | 5.0 ms | 70 Hz | 61 Hz |
| 1000 | 10.0 ms | 65 Hz | 62 Hz |
| 2000 | 20.0 ms | 50 Hz | 50 Hz |
| 5000 | 50.0 ms | 20 Hz | 20 Hz |

Paper rate: 15 Hz. Python static: up to ~138 Hz. The MATLAB L=250 solve+overhead is
~11.4 ms; 100 Hz needs <7.5 ms. Our design’s 2 ms acquisition leaves 7.87 ms; the FPGA
parallel kernel is the mechanism that closes the gap.

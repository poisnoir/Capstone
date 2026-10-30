# Solver algorithm handoff — FPGA 5-DOF pose solve

**Project:** EM AccuBot, Team 25 (ELEC/COEN 490), Phase 2
**Audience:** FPGA/numerics owner validating the pose-solver feasibility
**Status:** Feasibility **proposal**, 2026-10-29. Does not reopen the full-FPGA-Pose
architecture lock (`AGENTS.md`) or the M16 excitation. DIG-04 is the requirement this
must close against; this file is the design being validated.
**Scope:** the pose solve only. DDS, DAC/SPI, ADC capture and Goertzel are **out of
scope** except where they define this block's inputs.
**Target:** XC7A35T-1FTG256C baseline (33k LC, 90 DSP48, 50 BRAM36); XC7A50T same
footprint is the escape (decision #26).
**Budget:** solve ≤ **5.0 ms** inside the **8.633 ms / 115.8 Hz** pose period
(`docs/phase2/dig6_requirements.md` §5–6).

---

## 1. Claim being validated, in one paragraph

The solve is a **5-parameter, 8-residual bounded nonlinear least-squares problem** whose
cost is dominated by an **800-segment filament field model**, not by the optimiser. On the
35T the model is estimated at ~**0.3–1.1 ms/pose** with 3–6 pipelined float32 MAC lanes,
against a 5.0 ms allocation. The optimiser (5×5 damped normal equations + Cholesky,
fixed λ ladder, fixed iteration cap) is a few kLUT of control and contributes no
meaningful cost. The claim to validate is therefore: **the filament kernel fits and
closes timing with ≥3× margin, and the fixed-budget solver reproduces the double-precision
golden model within the 2 mm / 1° spec.** The optimiser is not the risk; the float
dataflow, the division strategy, and convergence on hard frames are.

## 2. What this is not

- Not a re-derivation of the physics. The model is a port of thesis Eq. (3.17)–(3.25).
- Not an MCU-vs-FPGA argument. The solve is cheap; the FPGA is justified upstream
  (integer-J DDS, 4-lane ADC deserialisation, gapless 49.152 MHz DAC SPI, stop path).
  See §7 for the numbers behind this.
- Not the M16 interface work — see `docs/handoff/m16-fpga-handoff.md`.

---

## 3. Reference formulation (frozen — port, do not re-derive)

Thesis Eq. (3.26)–(3.27), `docs/extracts/Jaeger2018_filament-sensor-model_Ch3_extract.txt:234-256`:

$$
F(p) = V_d - \kappa \cdot V_m(p), \qquad p = (x, y, z, \theta, \phi)
$$

$$
\text{minimise } \|F(p)\|^2 \quad \text{subject to } lb \le p \le ub
$$

| Element | Definition | Source |
|---|---|---|
| \(V_d\) | 8 signed amplitudes, one per coil/tone | `software/anser-matlab-ref/user/system/fSysGetField.m:48` |
| \(V_m\) | filament model, 800 segments/eval (8 coils × 100) | Eq. (3.17)–(3.18), Ch.3 extract |
| \(\kappa\) | per-coil scalar from the 7×7 positive-Z calibration fit | thesis Sec. 7.2.2 |
| DOF | 5 by physics — a single coil cannot sense roll | `AGENTS.md` gotchas |

**Measurement handling.** The golden code does **not** use a complex residual. It reduces
each tone to a *signed amplitude*:

```matlab
BField = sign(Phase1)'.*MagY(2,:)'./sys.Asens';   % fSysGetField.m:48
```

So the FPGA needs only \(|V|\) from the Goertzel and the **sign** of the I/Q phase
difference, which is a 2×2 determinant of the \(I,Q\) pairs after a fixed calibration
rotation. **No atan2, no CORDIC.** The 8-real-residual structure in DIG-04a is faithful to
the golden model.

**Golden solver settings** (`software/anser-matlab-ref/fSysSetup.m:184`, `fSysDecodeField.m:25-32`):

| Item | Golden value |
|---|---|
| Solver | `lsqnonlin`, bounded → **trust-region-reflective** |
| Jacobian | **finite differences** (none supplied) |
| Tolerances | `TolFun=1e-16`, `TolX=1e-6` |
| Caps | `MaxIter=40`, `MaxFunEvals=500` |
| Retry | from \(+\,[0,0,0,\pi,\pi]\) if `resnorm > 1e-15`; else hold the prior estimate |
| Warm start | 5-tap moving average of past solutions (`fSysSetup.m:246-266`) |
| Bounds | \(x,y \in \pm0.25\) m, \(z \in [0,0.5]\), \(\theta,\phi \in \pm2\pi\) |

Note: the prose says "LM/TRF"; the bounded `lsqnonlin` path actually runs **TRF**. Do not
describe the golden model as LM.

---

## 4. Proposed FPGA numerics (the design under validation)

| Item | Proposal | Deviation from golden | Why |
|---|---|---|---|
| Jacobian | **analytic** | golden uses FD | ~2× cheaper; removes the float32 FD step-size trap |
| Precision | float32, normalised coords/field | golden is float64 | 1e-7 relative vs 2 % required |
| Iteration | damped GN, **fixed λ ladder** (accept λ/10, reject λ×10, ≤2 rejects), cap 4–10 iters | golden adapts until TolFun/TolX | static worst-case cycle count |
| Linear solve | 5×5 normal equations + Cholesky, λ floor | golden TRF subproblem | 5×5 is trivial; λ floor keeps it PD at \(\theta\to0\) |
| Bounds | canonical \(\theta\in[0,\pi]\), \(\phi\in[-\pi,\pi]\); vertex clamp on output | golden \(\theta,\phi\in\pm2\pi\) | removes a redundant branch; π-retry still covers the other one |
| Retry | at most one full re-solve; watchdog expires to last estimate + `degraded` flag | same retry vector, unbounded in time | never block the frame |
| Transcendentals | rewrite the segment kernel as **rsqrt + Newton–Raphson**, no divides | golden uses `/` and `sqrt` | 5 transcendentals → 3 rsqrt + 1 mul |

**Analytic Jacobian.** \(\Phi = k\,\mathbf{B}(p)\cdot\hat n(\theta,\phi)\), so
\(\partial\Phi/\partial\theta\) and \(\partial\Phi/\partial\phi\) are dot products against
the already-computed \(\mathbf{B}\) — effectively free. Only the three position
derivatives need the differentiated Biot–Savart kernel, and they share the per-segment
intermediates. Cost ≈ **3 eval-equivalents/iteration** vs 6 for forward differences.

**rsqrt reformulation.** Per segment the golden form has 2 `sqrt` + 3 `/`.
Writing \(r_b = \text{rsqrt}(|b|^2)\), \(r_c = \text{rsqrt}(|c|^2)\) and
\(r_s = \text{rsqrt}(|c\times a|^2)\) removes every divide:

$$
\mathbf{B} = \frac{\mu_0 I}{4\pi}\,(\mathbf{c}\times\mathbf{a})\,r_s^2
\left((\mathbf{a}\cdot\mathbf{c})\,r_c - (\mathbf{a}\cdot\mathbf{b})\,r_b\right)
$$

Three rsqrt per segment, one square. This is the single highest-leverage micro-decision in
the block; a naive HLS `/` per lane will serialise and consume the margin.

---

## 5. Cost model and budget

| Quantity | Nominal | Worst (6 iters + retry) |
|---|---|---|
| Segments per evaluation | 800 | 800 |
| MAC per segment | ~30 | ~30 |
| MAC per evaluation | 24 kMAC | 24 kMAC |
| Evaluations per pose | 12 (4 iters × 3) | 36 |
| MAC per pose | 288 kMAC | 864 kMAC |
| Rate at 115.8 Hz | 33 MMAC/s ≈ 67 MFLOP/s | 100 MMAC/s ≈ 200 MFLOP/s |
| rsqrt per pose | 28,800 | 86,400 |
| Solve time @131.07 MHz, 3 lanes | ~1.0 ms | ~2.2 ms |
| Solve time @131.07 MHz, 6 lanes | ~0.5 ms | ~1.1 ms |

**Clock.** The solver must **not** run in the 32.768 MHz XO domain — at 32.768 MHz the
nominal solve is ~2.4 ms and the margin story collapses. One MMCM with VCO 786.432 MHz
(= 32.768 × 24, legal for a −1 device) yields 49.152 MHz (÷16), 98.304 MHz (÷8) and
131.07 MHz (÷6) from the same XO. Put the solve in the 131.07 MHz domain.

**Reset of a stale number.** `docs/phase2/fpga_vs_mcu_compute_budget.md` §5 sanity-checks with
"220 DSPs at 200 MHz" and §6 claims the MCU is "5–30× short". Both are computed against
the FD / 40-iteration / `MaxFunEvals=500` heritage configuration, not this design. The
real worst case is ~0.2 GFLOP/s, i.e. *inside* an STM32H7's effective throughput. The
FPGA is still the right choice (integration, determinism, no extra part), but the report
should not claim the MCU is 30× short. **Action for the team:** correct §5/§6 or note the
assumption explicitly, before a reviewer does the arithmetic.

---

## 6. Resource estimate (pre-synthesis — replace with real numbers)

| Block | Est. DSP48 | Est. LUT | Notes |
|---|---|---|---|
| 3–6 float32 MAC lanes | 18–30 | ~1.8k | 3 DSP/MAC if the adder lives in LUTs, 5 if in DSPs |
| 3 rsqrt + NR units | 3–6 | ~2.5k | BRAM LUT + 1–2 NR steps, II≈1 |
| 5×5 normal eq. + Cholesky | 1–2 | ~1.5k | time-multiplexed; 1 MAC is plenty |
| Control FSM, λ ladder, watchdog | 0 | ~1k | |
| **Solver total** | **~25–40** | **~7k** | ≈ 30–45 % DSP, ~35 % LUT of a 35T |

The rest of the design (8-tone DDS, 216-bit SPI, 4-lane capture, 32 Goertzels) is
estimated at <20 BRAM36 and a few kLUT (`docs/phase2/driver_power_requirements.md:212-214`).
DSP pressure from the other blocks is negligible (Goertzel ≈ 1.9 MMAC/s, DDS amplitude is
16-bit integer). The solver is the only consumer of the float DSP farm, and it needs
roughly a third of it.

**Do not** instantiate the PG060 divider at II≈8: at 0.5 ms/solve that needs 6–8 instances
and blows the LUT budget. Use LUT+NR at II≈1, one unit per two MAC lanes.

---

## 7. Why the solve belongs here (and not on an MCU)

Short version, so the validator does not relitigate it: the solve is small; the FPGA is
mandatory for the *other* blocks. Marginal cost of hosting the solve in fabric is
~25–40 DSP and ~7k LUT on a device already being bought for the excitation and capture.
Moving it to an MCU would add a part, a link and a protocol to save fabric that is
already paid for, and would put the pose outside the stop-path clock domain.

| | STM32H7 @480 MHz | Artix-7 @131 MHz |
|---|---|---|
| Nominal (4 iter) | ~2.4 ms | ~0.5 ms |
| Worst (6 iter + retry) | ~5–7 ms | ~1.1 ms |
| Budget | 7.87 ms | 7.87 ms |
| Tail | 65–90 % utilised, cache/DMA jitter | static, ~15 % utilised |
| Algorithm change | 30 s rebuild | 20 min P&R, may not fit |

The MCU *fits*; it has no tail margin. That is the whole argument, and it is a margin
argument, not a feasibility one. Keep the framing honest in the report.

---

## 8. Validation tasks

### V1 — Algorithmic (no FPGA, ~1 day) — **do this first**

Port the solver to float32 C (or numpy with explicit casts): analytic Jacobian, fixed λ
ladder, iteration cap, canonical bounds, one retry. Run:

- the 98-point calibration grid (49 points × 85.6 / 152 mm, Eq. 7.10);
- a moving trajectory at 115.8 Hz frame rate with warm start;
- the acquisition case (cold start from \((0,0,0.15,0,0)\)).

Report against the **double-precision MATLAB golden**:

| Metric | Pass |
|---|---|
| Pose error over the grid | ≤ 2 mm / ≤ 1° |
| Iteration histogram | median ≤ 4 |
| **Fraction of frames hitting the cap** | reported, not gated |
| Retry rate | reported |
| Condition number of \(J^T J\) | reported at \(\theta\to0\) and volume boundary |
| Residual agreement vs golden | within the pose-error bound |

This step also produces the golden vectors for the HLS testbench. It is the cheapest
de-risking available and it doubles as the C fallback if synthesis fails.

### V2 — Kernel synthesis

HLS the single-segment evaluator + tree reduction for the 35T. Report DSP/LUT/BRAM, II,
cycles/evaluation, and Fmax after place-and-route.

| Metric | Pass |
|---|---|
| Cycles/evaluation | ≤ 2,200 (nominal 12 evals ≤ 0.5 ms) |
| DSP48 | ≤ 40 |
| LUT | ≤ 8k |
| Timing | closes at 131.07 MHz, −1 grade, worst-case corner |

### V3 — Numerics sign-off

- Confirm the rsqrt/NR reformulation matches the golden segment formula to ≤1e-6 relative.
- Confirm float32 Cholesky of \(J^TJ\) is PD with the λ floor across the grid; escalate to
  Givens QR of the 8×5 only if V1 says so.
- Confirm coordinate/field normalisation keeps the dynamic range inside float32 across the
  full 150 mm volume (field spans ~decades as \(1/r^3\)).

### V4 — Clock and domain crossing

Confirm MMCM VCO 786.432 MHz → 49.152 / 98.304 / 131.07 MHz is legal on the −1 part and
that the solve domain's interface (demod results in, pose out, stop/heartbeat) has defined
CDC with no lost-frame path.

### V5 — Bench timing

Timed loop on hardware: 8.633 ms worst case at 115.8 Hz, filter-off latency ≤20 ms,
retry count, cap-hit fraction over a 1-hour moving run, zero dropped frames.
(`docs/phase2/dig6_requirements.md` §7.)

---

## 9. Acceptance for this handoff

All of:

1. V1 pose error ≤2 mm / ≤1° vs golden, grid + trajectory + cold start.
2. V2 resource ≤70 % of the 35T post-synthesis, timing closed at 131.07 MHz.
3. V5 worst case ≤5.0 ms **including one retry**, measured not estimated.
4. Cap-hit fraction reported and the degraded-pose path demonstrated (flag raised, frame
   not stalled).
5. The stale throughput numbers in `fpga_vs_mcu_compute_budget.md` §5/§6 either corrected
   or annotated with the assumption they depend on.

## 10. What would falsify this

- V2 shows >70 % of the 35T, or fails timing at 131.07 MHz → **50T** in the same
  footprint (no board change), then fewer lanes / longer solve.
- V1 shows the fixed cap loses pose accuracy on realistic frames → raise the cap at the
  expense of margin, or add a residual-triggered second stage; do not adopt an unbounded
  line search.
- V1 shows float32 conditioning is marginal near \(\theta=0\) → Givens QR of the 8×5
  (~50 extra cycles, negligible) before considering float64 anywhere.
- The analytic Jacobian lands in a different local minimum near \(\theta\approx0\) or the
  boundary often enough to matter → investigate the π-retry ordering before changing the
  Jacobian.
- Everything fails → hybrid (FPGA capture/demod/filament, MCU 5×5). This is an
  architecture change from `AGENTS.md`; it is the last resort, not a design option.

## 11. Risks the validator should opine on

| Risk | Why it matters |
|---|---|
| Analytic-J path reaches a different local minimum than FD | the problem is multimodal by construction (π-retry exists for a reason) |
| float32 conditioning with wide κ spread across coils | normal equations square the condition number |
| Golden `TolFun=1e-16` vs a 4–10 iteration cap | acquisition and boundary frames are the ones that will differ |
| HLS float32 dataflow bloat on a 35T | the known schedule risk, not a compute risk |
| Algorithm churn after HLS is frozen | every iteration-count change is a P&R cycle |

## 12. Handoff checklist

- [ ] Read Ch.3 extract §3.6–3.7 and `fSysDecodeField.m` / `fSysSetup.m:184-266`.
- [ ] Confirm the 8-real-residual / signed-amplitude measurement model (§3).
- [ ] Run V1 and report the table in §8.
- [ ] Synthesise V2 on the 35T and report resource + Fmax.
- [ ] Sign off or reject the rsqrt reformulation and the λ ladder (§4).
- [ ] Confirm the 131.07 MHz domain and CDC (V4).
- [ ] Confirm the corrected compute-budget numbers (§5) with the report owner.
- [ ] Update DIG-04 to match whatever survives: analytic Jacobian, float32, fixed λ
      ladder, iteration cap, watchdog-with-flag.

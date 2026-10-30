# AnserEMT tracker baseline — session findings (2026-10-13)

Consolidated from Jaeger 2018 + OSF snapshot + Phase 1 report comparison.
Frozen refs: `HAJ_Thesis_2018.pdf`, `AnserEMT-onlineversion.pdf`,
`Phase 1 Report - Team 25 (ELEC-COEN 490).docx` (local-only), `vendor/anser-osf/` (never edit).
Working extracts: `docs/extracts/Jaeger2018_bespoke-sensor_Ch7_extract.txt`,
`docs/extracts/Jaeger2018_filament-sensor-model_Ch3_extract.txt`.
Golden code: `software/anser-matlab-ref/` (port map in its README).

## 1. Coil sensors: Jaeger Ch.7 vs OSF

Ch.7 is the coil itself; OSF is amp + solver that assumes a coil.

- Theory Ch.7 Eq.7.1–7.9: `vs=-dΦ/dt`, `vs=-N d/dt ∫B·dA` (7.2), small-coil
  `vs=-µ0 N Ac dH/dt` (7.3), ferrite `µa=µr/(1+kd(µr-1))` (7.5),
  `kd≈(dc²/lc²)[2ln(2lc/dc)-1]` (7.7), sinusoidal (7.9). Ferrite = +gain,
  −linearity, +Barkhausen.
- Coils A–E (Table 7.1): 12 mm long Delrin formers, hand-wound, magnet tape
  per layer, twisted pair to miniXLR RT5FC-B. A:321T/0.19mm/604µH,
  B:319T/804µH, C:120T/0.32mm/91µH, D:216T/425µH, E:417T/1018µH.
  Ferrite option in C/D/E only: 12×6 mm 3C90, µr=2300. Resonance
  ~485 kHz air → ~290 kHz ferrite; linear at 20–30 kHz.
- Cal/test: 7×7 grid on FG at 85.6 + 152 mm = 98 pts, per-coil κ fit,
  RMS Eq.7.10–7.11. Air: A 1.89, B 1.59, C 2.48, D 1.98, E 1.70 mm.
  Ferrite: C 1.90 (−23%), D 1.62 (−18%), E 1.58 (−7%) mm. NDI 610099
  0.5 mm ref 1.79 mm in same rig. FFT +10 dB from ferrite (µa≈3 measured
  vs ~10 predicted, ~5 with corrected kd≈0.2).
- OSF `Design Files/Sensor Amplifier/CAD/Sensor Amplifier PCB (Eagle).zip`
  (E301 2.0/3.0) is INA128U + 3296Y trimmers + 1206 passives only.
  No coil geometry. `fSysSetup.m:5-7,35` assumes external probe + ref
  sensor on DAQ ch `[0,1,4]` (ch0 = current sense); sensor+amp collapsed
  into `Asens(f)` (Helmholtz + GP102) and per-emitter `BScale κ (8×1)` +
  `zOffset` via `user/calibration/fCalibrate.m:29-46`, switched by
  `user/system/fSysSensor.m:8-22`. Solver model is point-sensor
  Φ=µa·B·A·n̂ (Ch.3 Eq.3.19–3.25); Ch.3 p.55 keeps FG model separate so
  sensor models are interchangeable — the hook Ch.7 uses.

## 2. Accuracy vs precision (scaled teleop)

- `tool_error = hand_error / S`, S = 20–1000 (default 100).
  2 mm hand /100 = 20 µm tool (passes ≤25 µm); /20 = 100 µm (borderline).
- Visual-servoed 9/10×200 µm targets tolerate smooth bias (operator adapts
  to 2–3 mm) but not non-linear distortion changing >0.5–1 mm over a few
  mm travel, nor jitter/drift/latency. So: precision/repeatability/jitter/
  drift/latency dominate; absolute trueness bounded by
  `hand_RMS_max ≈ S·20µm` (100:1→2 mm, 20:1→0.4 mm).
- Tremor needs resolution, not accuracy: 2 mm DC offset + 0.5 mm 10 Hz
  wobble is filterable; 2 mm random 10 Hz jump is not. Need in-band
  (6–12 Hz) jitter ≈0.1–0.2 mm RMS hand-side, pose ≥100 Hz.

## 3. Resolution achievable

No smallest-step spec published; jitter is the floor (Hummel, NDI 610099,
150 samples @15 Hz): bottom 0.13±0.11, middle 0.15±0.10, top 0.29±0.34 mm;
accuracy 0.82/1.14/1.98 mm; rotation 0.04° perp / 0.09° coplanar.
Thesis Table 4.5/4.7 = paper Table 3/4. `TolX=1e-6` in `fSysSetup.m:184`
is optimizer step (1 µm), not system resolution (150× smaller than noise).
Tool-side at S=100: 0.15 mm → 1.5 µm jitter, fine vs 10 µm repeatability
and 25 µm budget. Bespoke coils have no jitter table; assume worse than
NDI until measured (large Ac needs integrated Eq.7.9 + ferrite noise).

## 4. Phase 1 comparison (Tables 0–2 vs Anser)

| Spec | Phase 1 | Anser | Verdict |
|---|---|---|---|
| Hand acc | 1 typ / 2 max mm | 0.82/1.14/1.98 mm NDI; 1.58–2.48 bespoke | NDI passes lower 2/3 vol; C 2.48 fails max |
| Orientation | ≤1° | 0.04/0.09° | Pass ~10× |
| Jitter | implicit (10 µm tool) | 0.13/0.15/0.29 mm → 1.5 µm tool @100:1 | Pass |
| Tool err | 25 µm@100:1, 100 µm@20:1 | 11.4/57 µm middle, 19.8/99 µm top; bespoke worst 24.8/124 µm | NDI passes; bespoke fails @20:1 |
| Pose rate | ≥100 Hz | 15 Hz paper, 50–72 Hz Matlab / up to ~138 Hz Python static | Fail — Nyquist 7.5 Hz misses tremor band |
| Tremor | 20 dB / 3 dB | none (only MA_length=5) | To implement on FPGA |
| Latency | 20 off / 100 on ms | acq 2.5–50 ms + lsqnonlin MaxIter 40 | Pass on, tight off |
| Volume/metal | 100 mm min / 150 mm target, 150 mm clear | 250 mm cube; Al cylinder → 27 mm error | Validates rule |

## 5. Pose rate limits

`user/tracking/fGetSensorPosition.m:21-24` per pose: `fSysDAQUpdate` →
`fSysGetField` (`Y=(X.*G)*E`, G=chebwin L−1, E=L×8) → `fSysDecodeField`
(`lsqnonlin` LM/TRF, TolFun 1e-16, MaxIter 40, MaxFunEvals 500, retry
+[0,0,0,π,π] if resnorm>1e-15) → `fSphericalToMatrix`. Each eval calls
`model/spiralCoilFieldCalcMatrix.m` (~800 filament segs, Eq.3.17–3.18)
via `user/objective/objectiveCoilSquareCalc3D.m:22-32`.
- Acq floor: Fs=100 kHz NI max; Lmin=50 (ΔF=2 kHz, w=Fs/L, fn=J/L
  Eq.3.8/3.12) but separate DDS/ADC clocks → leakage Fig.3.12 → practical
  L=250 + Hamming (780 Hz lobe). TL=L/Fs=2.5 ms min.
- At L=250,72 Hz: Ttotal 13.9 ms − TL 2.5 ms = Tsolve+overhead ~11.4 ms.
  Need <7.5 ms for 100 Hz. Moving sensor (>50 cm/s) breaks warm-start
  estimateInit → more iterations (72→64 Hz).
- Linux NI-DAQmx Base buffer bug forces Tad>Tsolv (empirically L=2000).
- Creators did sweep L=250–5000 × Win/Linux × Matlab/Python ×
  static/dynamic (Tables 3.4/3.5); chose large L for Hummel accuracy.
  Goal was visualizer, not tremor loop.
- FPGA fix (AGENTS.md): common-clock DDS+ADC, Goertzel vs bulk matrix,
  parallel filament kernel, relaxed TolFun, ping-pong acq/solve, Fs>100 kHz.

## 6. Common clock, part selection, DDS

- Common clock = one TCXO → FPGA PLL → clk_dds + clk_adc (CONVST/SCLK).
  DDS accumulators + DAC + ADC all frequency-locked; J integer every
  frame; analog group delay (µs) is constant → one `DAQ_phase_offset`
  (`fSysSetup.m:174`) + κ calibration absorbs it. Not generate-then-read
  per cycle; both stream continuously (1000 master ticks per ADC sample
  at 100 MHz/100 kHz).
- Parts: ADC must take external CONVST/SCLK/MCLK (reject internal-only);
  prefer simultaneous over muxed (removes 2πF/400k skew). DAC likewise
  externally clocked. Jitter need is ns-level, not ps. One sync reset for
  DDS+ADC dividers, then calibrate. Closed-loop current driver first
  (O'Donoghue §II), coherence second.
- FPGA DDS suitable: fout=tuning_word·fclk/2^N (32-bit @100 MHz = 0.023 Hz
  steps). 12–14-bit LUT + 12–16-bit DAC + 50–100 kHz RC + coil inductance
  + narrowband DFT easily reach spur budget below. Original used AD DDS
  [16], worse than FPGA+DAC. Check sense-resistor FFT: harmonics >60 dB down.

## 7. Exact spur budget (worked example, z-coil, 1-D LS)

σx=σV/||J||, J[i]=∂Bz,i/∂x from Python port of
`model/spiralCoilDimensionCalc.m` + `spiralCoilFieldCalcMatrix.m`
(N=25, l=70 mm, centres per `fSysSetup.m:99-105`).

| z | ‖Jx‖ T/A/m | Vall=0.15mm·‖J‖ re Brms | per-tone −18 dB (RSS7+1/3 margin) |
|---|---|---|---|
| 66 mm ctr | 5.43e-04 | −35.6 dB (x), −48.2 dB (z) | −53.6 dB |
| 100 mm ctr | 2.28e-04 | −41.4 dB (x), −46.0 dB (z) | −59.4 dB |
| 150 mm ctr | 0.69e-04 | −46.6 dB (x), −45.6 dB (z) | −64.6 dB |
| 200 mm ctr | 0.26e-04 | −50.2 dB (x), −46.8 dB (z) | −68.2 dB |

Off-centre 50,50 mm within 1–2 dB. Fractional dV/V per coil unusable
(nulls → 10⁶ %/mm); joint LS used. Full 5-DoF 8×5 Jacobian tightens
~2–3 dB. Script: `simulations/field_jacobian.py`.
Quoted 60–70 dB = Vall(−35…−51 dB) − 8.45 dB (7 aggressors) − 9.5 dB
(spur < ⅓ jitter). Recompute with pen N/Ac and Iout/Rstore when FG changes.

## 8. Measuring dB/dp (J) on bench

1. Helmholtz-calibrate pen+INA128 as unit: Asens(f)=V/B per
   `fSysSetup.m:33-35`. 2. Single coil on, closed-loop I logged.
   Non-metal stage (Duplo coarse + micrometer fine + USB microscope).
   L=5000, Fs=100 kHz, demod per `fSysGetField.m:20`, B=|Y|/Asens.
   Cal κ/zoff via `fCalibrate` 7×7 first. 3. Finite difference
   Jx,i=[Bz,i(x+Δx)−Bz,i(x−Δx)]/2Δx, Δx=0.5 mm, at 66/100/150 mm.
   Compare to §7 table; >20 % mismatch = current/metal/κ issue.
   Spur check (all coils on): SFDR=20log(Vi/Vspur) from raw-volts FFT;
   need §7 last column.

## 9. Goertzel vs L×8 matrix

Matrix `Y=(X.*G)*E`: buffer frame, bulk dot vs 8 templates. L×8 complex
MACs + L×8 coeff store (~80k floats at L=5000). Goertzel per tone:
`s[n]=w[n]x[n]+2cos(2πFi/Fs)s[n−1]−s[n−2]`, read
`Y=s[L−1]−e^{−j2πFi/Fs}s[L−2]`. Same MAC count, streaming: 2 states +
1 coeff/tone, TL+2 cycles latency, ping-pong N/N+1, no BRAM burst.
Matrix for Python golden-check, Goertzel in HDL.

## 10. TL vs L vs Fs; choosing TL

TL=L/Fs (thesis 3.9 prints Fs·L — OCR drop; 5000/100 kHz=50 ms proves
division). Fs=hardware (DAQ/ADC max + Nyquist 68 kHz for 34 kHz).
L=choice (w=Fs/L < ΔF/2, coherence J integer, Hamming 780 Hz lobes
non-overlapping). TL=consequence; Fsystem,max=1/TL, measured lower.
Bound now (Fs=100 kHz, L≥250 → TL 2.5–10 ms); lock after FG+DAC/ADC
built by sweeping L=50–2000 and plotting SFDR/Brms/‖J‖/σr(Eq.6.10)/
rate. Smallest L with σr≤0.15 mm + spur<Vtone + TL+Tsolv<10 ms moving
wins. No such L → fix current/noise/clock/ADC, not L.

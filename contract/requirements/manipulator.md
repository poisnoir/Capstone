# Phase 2 — Manipulator requirements (XYZ + pitch/yaw follower)

**Canonical location:** `contract/requirements/manipulator.md` · **Contract version:** 1.0.0
**Change process:** `contract/README.md`.

This doc tells the stage builders what the follower must do, and tells the
examiner where every number came from. No invented numbers.

Reading guide: Part A reads cover-to-cover in plain English. Part B is the
formal reference (IDs, full sources, test hooks) you cite in the report.

Traces to: `docs/phase2/README.md` §§2–6 (specs #1–25), AGENTS.md full-FPGA
override, Jaeger 2018 Eqs.(3.17)–(3.27), (7.1)–(7.9).

Test conditions for every row unless stated: indoor lab, 18–28 °C,
30–60% humidity, no metal except the system within 150 mm of the tracking
volume, pen inside the volume, scale 100:1, tremor filter on, wall power.

What we are building: a small robot that copies the surgeon's hand at
reduced size. Hand moves millimetres, tool moves micrometres. It also copies
tilt (pitch/yaw) one-to-one. It does not copy twist (roll) — a single coil
cannot sense twist, so roll is locked by design.

---

# Part A — readable main

## 1. Where the numbers come from (short version)

Hand speeds and shaking come from eye-surgery measurements (Micron team,
CMU/Johns Hopkins). Tracker speed-vs-accuracy comes from hospital EM-tracker
studies (Aurora/3D Guidance). Our own tracker baseline is 1.14 mm / 0.04°
from the Anser paper, best case, not across the whole volume. Wrist ranges
are anatomy textbooks. Full citations are in Appendix B — the body below only
uses numbers those sources support.

## 2. Scale, in plain English

Scale (S) means: tool movement = hand movement divided by S.

$$
v_{tool} = v_{hand} / S,\quad S = 20\ \mathrm{to}\ 1000,\ \mathrm{normally}\ 100
$$

In words: at 20:1 a 20 mm hand move becomes 1 mm at the tool. At 100:1 it
becomes 0.2 mm. At 1000:1 it becomes 0.02 mm.

Worked examples (speed divides the same way):

- 50 mm/s hand at 20:1 → 2.5 mm/s tool. This sizes the motors: they must keep
  up with this.
- Same 50 mm/s hand at 100:1 → 0.5 mm/s tool.
- Same hand at 1000:1 → 0.05 mm/s (50 µm/s) tool.
- Fine work: 2 mm/s hand at 1000:1 → 2 µm/s tool. This sizes smoothness:
  the stage must glide at 2 µm/s without juddering.

Tilt is not scaled. 10° of hand tilt = 10° of tool tilt. All tilt numbers in
this doc are 1:1.

Rule that follows: there is no single tool speed limit. The limit depends on
the active scale:

$$
limit_{tool}(S) = \min(motor\_max,\ hand\_cutoff / S)
$$

In words: whichever is smaller wins — what the motors can physically do, or
what the hand cutoff allows at this scale. The controller recomputes this
every time S changes.

## 3. What the hand does

- Holding still: 90% of the time the hand drifts under 2 mm/s. Even so, a
  1 mm/s limiter trips 30% of the time — holding still is not still.
- Fine surgery: deliberate hand motion about 2–10 mm/s.
- Moving between targets: 10–50 mm/s, with brief bursts to ~130 mm/s far
  from tissue (provisional — source PDF still to confirm).
- Above 50 mm/s sustained: not surgery, clamp the tool command.
- Above 100 mm/s, a jump over 10 mm in one 10 ms frame, or lost tracking:
  not surgery, stop within 100 ms and wait for re-engage.

Why two levels: clamp keeps following but capped; stop locks the brakes.
Fast moves plus 100 ms delay means overshoot — the cap keeps overshoot
inside tissue-safe distance.

## 4. What the tool must do at each scale

Commanded tool speeds (filter on, tracking normally):

| Scale | fine hand 2–10 mm/s becomes | gross hand 10–50 mm/s becomes | burst 130 mm/s becomes | motors must |
|---|---|---|---|---|
| 20:1 | 0.10–0.50 mm/s | 0.50–2.50 mm/s | 6.5 mm/s | keep up with 2.5 mm/s, survive 6.5 mm/s |
| 100:1 (normal) | 0.02–0.10 mm/s | 0.10–0.50 mm/s | 1.3 mm/s | keep up with 0.5 mm/s, survive 1.3 mm/s |
| 1000:1 | 2–10 µm/s | 10–50 µm/s | 130 µm/s | glide smoothly at 2 µm/s |

A motor stack that is fast but jumpy fails the last row. A piezo that is
smooth but only travels 0.4 mm fails the first row. Both rows must pass.

Workspace catch: the hand volume is **100 mm minimum, 150 mm target, 200 mm
stretch**. At 100:1 that is only 1 mm at the tool (1.5 mm at 150 mm), but the
spec asks for a 5 mm cube. So at 100:1 and 1000:1 the surgeon must clutch (lift,
relocate, re-engage — tool stays put while disengaged) to cover 5 mm. Only at
20:1 does one sweep cover it. The 150–200 mm target reduces the clutching
burden; the 100 mm minimum remains the fallback. The clutch hold must not drift
more than 10 µm.

Error-budget catch: hand error ≤2 mm divided by S. At 20:1 that is 100 µm —
the whole tool budget gone before the stage moves. At 100:1 it is 20 µm,
leaving 5 µm for the stage against the 25 µm spec. At 1000:1 the hand
contributes 2 µm and the stage dominates. One budget number cannot fit all
scales — verify at 20:1 and 100:1 separately.

## 5. Each movement direction, plainly

- Side-to-side (X) and front-to-back (Y): work range ±2.5 mm about the setup
  point; build extra travel to ±5 mm for setup. Clamp position in software,
  back it with a hard endstop. Clamp speed per the table above.
- Up-down (Z): same travel, but downward speed capped at half of X/Y.
  Down is the puncture direction and fights gravity — a missed step down
  hurts, a missed step up does not.
- Tilt (pitch, yaw): normal work ±20°, tolerated to ±45°. Normal tilt rate
  under 30°/s, fine work under 10°/s, brief to 60–90°/s. Beyond 45° or
  90°/s sustained: freeze tilt at last good value, keep XYZ if valid, flag
  it — do not copy. Reason: at steep angles the sensor signal fades toward
  zero, the sign can flip, and one bad frame can mirror the solution by tens
  of degrees. Also 1° of tilt on a 20 mm tool swings the tip 349 µm — fourteen
  times the 25 µm budget.
- Twist (roll): locked. Not sensed, not driven.

Tilt pivot: rotation must be about the tool tip. If tilting about the wrong
point drags the tip sideways more than 25 µm over ±20°, either move the
hardware pivot or compensate in software to the same residual.

## 6. What the follower must do (human sentences, IDs in brackets)

1. Cover a 5 mm cube at the tip, using clutch above 20:1, without drifting
   while clutched. (RQ-M1)
2. Copy scaled hand position within 100 µm at 20:1 and 25 µm at 100:1.
   (RQ-M2)
3. Return to the same spot within 10 µm over 10 tries. (RQ-M3)
4. Move in steps of 2 µm or smaller, tilt in steps of 0.05° or smaller, with
   no dead zone bigger than the budget. (RQ-M4)
5. When reversing direction, lose less than 5 µm / 0.1° to backlash.
   (RQ-M5)
6. Keep up with the speed table in §4 without skipping steps. (RQ-M6)
7. Clamp fast hands, stop on withdrawal/jump/loss within 100 ms, cap Z-down
   at half speed, freeze bad tilt. Recompute caps when scale changes.
   (RQ-M7)
8. Tilt within 0.5° (repeat 0.2°) over ±30°, flagged-degraded to ±45°.
   (RQ-M8)
9. Tilt about the tip: sideways drag ≤25 µm over ±20°. (RQ-M9)
10. No wobble where tremor lives: first resonance above 50 Hz, motor ripple
    in 6–12 Hz at least 20 dB below budget. (RQ-M10)
11. Accept pose updates at 100–250 Hz, hold full accuracy at ≥100 Hz; if
    pushed faster and noise rises, mark tilt stale and filter harder —
    never feed raw noise to the motors. (RQ-M11)
12. React within 20 ms filter-off / 100 ms filter-on; stop within 100 ms.
    (RQ-M12)
13. With filter on: shrink 6–12 Hz shaking by ≥20 dB, leave deliberate
    motion below 1 Hz nearly untouched (≤3 dB). (RQ-M13)
14. Deterministic FPGA-to-motor path; log every pose at ≥100 Hz with time
    stamps; always show state: tracking / out-of-volume / stopped / fault;
    camera view magnified ≥50×. (RQ-M14)
15. Motors and brackets must not distort tracking: prove with a fixed-distance
    two-sensor test while motors switch on/off; hold calibration 18–28 °C;
    drive coils with closed-loop current. (RQ-M15)
16. Follower is bench gear (the 50 g limit is the pen, not this); its cable
    must not drag the pen; wall power only; one pen+follower pair ≤1000 CAD.
    (RQ-M16)
17. Field at the operator ≤27 µT everywhere in the volume. (RQ-M17)

Why tilt accuracy is load-bearing, not a stretch goal: at 20 mm tool length,
0.5° alone is ~175 µm of tip error — seven budgets. The 25 µm spec is
impossible without RQ-M8+M9 passing.

## 7. Stop / clamp behavior

Each 10 ms frame: measure hand speed from tracker deltas, divide by active
scale for tool command, measure tilt rate from tip-direction-arrow deltas.
Over 50 mm/s for longer than 100 ms → cap at 50/scale and flag `clamped`.
Over 100 mm/s, jump over 10 mm, or tracking lost → brakes on, flag
`stopped`, require re-engage, all inside 100 ms. Z-down caps at half. Tilt
past 45° or 90°/s → hold last good tilt, flag `tilt-stale`. Log every event
with its pose and timestamp.

---

# Part B — formal reference (cite this in the report)

## B1. Formal shall table

| Req ID | Shall | Rationale / source | Verify |
|---|---|---|---|
| RQ-M1 workspace+clutch | Follower workspace ≥5 mm cube at tool tip; at S=100/1000 via clutch with tool stationary on disengage, drift ≤10 µm | #8; 100 mm / S paradox | micrometer travel; clutch hold-drift |
| RQ-M2 tool accuracy | Tool error ≤100 µm @20:1, ≤25 µm @100:1 vs scaled hand motion, default conditions | #9–10; §4 budget; Jaeger Eq.(7.10) | scaled follow error on grid, both S |
| RQ-M3 repeatability | ≤10 µm over 10 approaches, filter settled | #11 | 10-approach spread |
| RQ-M4 resolution | Steps ≤2 µm XYZ / ≤0.05° tilt, no deadband over budget | S=1000 fine row; Anser 0.04° best-case | single-step response under load |
| RQ-M5 backlash | Reversal ≤5 µm / ≤0.1° at tip (length-compensated) | 0.1° at 15 mm = 26 µm | bidirectional indicator test |
| RQ-M6 velocity | Track §4 continuous column at active S; survive transient column | §3 anchors; torque falloff | constant-velocity follow S=20/100/1000 |
| RQ-M7 cutoff | Clamp / halt per §7 incl. Z 50% + tilt freeze ≤100 ms | tissue + stage + EM jump | overspeed/jump/loss injection timing |
| RQ-M8 orientation | Tilt error ≤0.5°, repeat ≤0.2° over ±30°; flagged to ±45° | #5–6 at 1:1; Ch.7 edge degradation | tilt test at 85.6/152 mm heights |
| RQ-M9 pivot point | Tilt about tool tip: parasitic shift ≤25 µm over ±20° (hardware or software RCM) | lever-arm budget | pure-rotation tip indicator |
| RQ-M10 dynamics | Resonance >50 Hz; 6–12 Hz ripple ≥20 dB below budget | #12–13 split | tap + run-up spectra loaded |
| RQ-M11 tracker link | Accept 100–250 Hz; full accuracy ≥100 Hz; stale+filter above knee; zero retry storms at ≥100 Hz | Yaniv tradeoff; 8-tone SNR; Nyquist >24 Hz | rate-vs-noise curve, retry counter |
| RQ-M12 latency/stop | Onset ≤20 ms off / ≤100 ms on; stop ≤100 ms | #14–15, #17; JND 15–20 ms | onset-to-onset + watchdog timing |
| RQ-M13 tremor | ≥20 dB @6–12 Hz, ≤3 dB <1 Hz (0.5 + 1 Hz sines) at tool | #12–13; Wells; shelving fL=0.15 fH=2 kS=1/3 | sine sweep in/out dB |
| RQ-M14 interfaces | Deterministic pose→motor path; step rate covers RQ-M6; ≥50× view; ≥100 Hz timestamped log; tracking/out-of-volume/stopped/fault | #16, #18, full-FPGA | timed loop + drop counter; screen calibration |
| RQ-M15 metal/thermal | Fixed-separation test unaffected by motors energized; 18–28 °C cal; closed-loop coil current | 150 mm rule; κ drift O'Donoghue §II / thesis §4.3.3 | separation test + κ recheck |
| RQ-M16 mass/power/cost | Bench follower; tether unloads pen; outlet only; ≤1000 CAD/pair | #19–21; C$962+C$75+15% envelope | scale; outlet; BOM |
| RQ-M17 field | ≤27 µT at operator anywhere in volume | #20 ICNIRP | AC probe sweep |

Budget equation (default 100:1, hand typical 1 mm → 10 µm):

$$
e_{tool}^2 \approx (e_{hand}/S)^2 + e_{stage}^2 + (L\cdot e_{ang})^2 + e_{noise}^2 + e_{pivot}^2 \le (25\ \mu m)^2
$$

$L$ = tool length, angles in radians.

## B2. Full source table

| Domain | Source | Number used |
|---|---|---|
| Hold velocity | MacLachlan et al. 2012 [PMC3459596] Fig.3 | 90% <2 mm/s; wander+jerk dominate |
| Limiter | Same Table II §II.F | 1 mm/s limiter trips 30%; shelving 0.15/2 Hz, 1/3 |
| Eye-hand loop | Same §I.B | critical 0.5–2 Hz; <1 Hz corner feels bouncy, <0.5 Hz unusable |
| Tremor in vivo | Wells et al. 2013 [PMC3989364] | RMS 144/258/285 µm; max 379/647/696 µm; 1–3 + 6–12 + 20–40 Hz |
| Baseline tremor | Same citing Elble/Stiles; Singh 2002 | RMS 50–200 µm, 8–12 Hz; often ≥50 µm p-p |
| In-situ tremor | Kilthub vitreoretinal sensing | to 50 µm p-p, 7–13 Hz |
| Fine tool speed | PMC8973184 + refs | typical maneuver 0.1–0.5 mm/s tool |
| Gross speed | ASTEMA HAL-03606236 (snippet, to confirm) | to 130 mm/s far from vessel |
| EM rate/accuracy | Yaniv et al. 2009 [PMC2673677] | Aurora 40 Hz single, 20–25 Hz dual; defaults 40/68 Hz optimal; 25–30 Hz enough for human, more for robots; JND 15–20 ms; ideal 100 Hz / 0.1 mm / 0.1°; report 95th percentile + variability over 225 pts |
| Own baseline | AnserEMT-onlineversion.pdf | 1.14 mm / 0.04°, 8 freqs 20.5–27.5 kHz @1 kHz, closed-loop driver |
| Model/solver | Jaeger Ch.3 (3.17)–(3.27), Ch.7 (7.1)–(7.9) | `Φ` point-sensor + filament; cost `F = Vd − κ·Vm`; κ 7×7 grid; RMS 98 pts @85.6/152 mm Eq.(7.10); Table 7.1 coils |
| Wrist anatomy | PMC4117694 | extension ~71°, flexion ~101°, pro/sup 77–93° — ±45° is procedure cap, not anatomy |
| Wrist maxima | CDC cdc_204524; PMC5260637 | ~1049°/s industrial, 50 rad/s sports — ceiling only; surgical cap is intent-based |
| Stage benchmark | Micron §II.B | piezo 400 µm, >1 N, >100 Hz, slew >100 mm/s; optical truth 4 µm @2000/s; tip noise 5.7 full / 1.8 @100 Hz µm RMS |
| Force sense | Micron §I.C | 75% contacts <7.5 mN, felt by 19% — position cutoff is the safety |
| Frozen specs | docs/phase2/README §2 | #3–#25 as listed in header |

Translations for newcomers: scale (S) = hand-to-tool divisor; tip direction
arrow = unit vector `n̂=[sinθcosφ,sinθsinφ,cosθ]` pointing along the coil;
per-coil calibration number (κ) = scalar absorbing gain/phase per frequency;
in-step sampling = frame length equals a whole number of drive cycles so
tones land exactly in demod bins; pivot point (RCM) = the point that stays
put while tilting — wanted at the tool tip.

## B3. Test hooks (manual: every spec needs one)

Reference-grid sweep (7×7 κ + 98-pt RMS @85.6/152 mm) at S=20/100 → RQ-M2/M8.
Rate-vs-noise 40–250 Hz with retry count → RQ-M11 knee. Velocity follow per
§4 table → RQ-M6. Bidirectional + pure-rotation + single-step → RQ-M3–M5/M9.
0.5/1 Hz + 6–12 Hz sweeps → RQ-M13. Onset and stop timing → RQ-M12/M7.
Two-sensor separation with motors on/off → RQ-M15. 9/10 × 200 µm targets on
≥50× view only at 100:1 filter-on (success gate). BOM + probe + temp log →
RQ-M16/M17.

## B4. What each requirement rejects (buyer's filter)

- Fails §4 fast row and smooth row together → reject (travel vs smoothness).
- Tilt backlash >0.1°, pivot drag >25 µm, or resonance in 6–12 Hz → reject.
- Fails separation test with motors on → relocate/shield/de-ferrous or reject.
- Needs >250 Hz pose to stay stable → reject (assumes SNR the link has not got).
- Jittered / muxed feedback into pose loop → reject (breaks in-step lock, blows latency).

## B5. Open decisions (do not procure until closed)

1. Tilt pivot: hardware tip-pivot vs base wrist + software compensation.
2. Confirm 130 mm/s burst from full ASTEMA PDF.
3. Dynamic tracing speeds to replace hold-still CDF for fine/gross rows.
4. Tilt-rate cap 60 vs 90°/s — needs far-plane (152 mm) tilt-noise data.
5. Clutch switch placement + hold-drift budget.

# Phase 2 — Design order and technical requirements

**Purpose.** Fix the dependency order for the hardware/signal-chain design and state the
technical requirements that must be met at each gate. This is a gate document, not a
waterfall: a stage may start only when the upstream outputs are frozen, and parallel
branches are allowed only where marked. Every requirement has a verification; a
requirement without a test is not frozen.

**Sources.** Phase 1 report specs #1–25; `docs/phase2/README.md`; `docs/phase2/adc_justification.md`;
`docs/handoff/system-flowchart-handoff.md`; `HAJ_Thesis_2018.pdf` §4.2–4.8; Jaeger Ch.3/Ch.7
(Eq.3.17–3.27, 7.1–7.9); `simulations/field_jacobian.py`.

**Status tags.**

- `LOCKED` — source-backed decision; do not reopen without a written deviation.
- `PROPOSED` — needs team approval/test; numbers may move.
- `TBD` — blocked by a missing input or datasheet.

---

## 0. Dependency graph

```
SC-0  System contract
 ├─ FG-1  Field / ICNIRP / current / volume
 │   ├─ DRV-2  Driver + power + PSU ─────────────┐
 │   └─ PEN-3  Pen coil + amp-floor verification │
 │        └─ FE-4  Receiver front end            │
 │             └─ ADC-5  ADC interface verification
 │                  └─ DIG-6  Digital / demod / timing
 │                       └─ INT-7  Integration / calibration / acceptance
 └─ (SC-0 also fixes tone plan, ADC contract, clock tree, budget gate)
```

**Interface edges:** DRV-2 → DIG-6 (DAC + current-sense); ADC-5 → DIG-6 (data lanes);
PEN-3 → FE-4 → ADC-5 (signal chain).

**Critical path:** SC-0 → FG-1 → PEN-3 → FE-4 → ADC-5 → DIG-6 → INT-7.
**Parallel branch:** DRV-2 starts after FG-1 and runs alongside PEN-3/FE-4.
**Early-start/late-close:** DIG-6 math (DDS/Goertzel) may start after SC-0, but closes
only after ADC-5.

**Dependency rules (hard):**

1. No FG design before SC-01/03/04/05 are frozen.
2. No driver/power design before FG-02/03/06/07 are frozen.
3. No pen-coil choice before FG-04/05 (field and conditioning) are frozen.
4. No front-end design before PEN-03/04 and SC-05 (ADC contract) are frozen.
5. No ADC interface verification before FE-04 (output stage) exists.
6. No digital closure before SC-03/05, ADC-04/05, and DRV-01/08 are frozen.
7. No integration before all upstream gates are signed.

---

## 1. Stage summary

| Stage | What it decides | Must be frozen before it starts | Hard gate before next stage |
|---|---|---|---|
| **SC-0** | Frame, volume, tone plan, ICNIRP rule, ADC contract, clock tree, budget | Nothing | `contract/system_contract.md` signed; D1-B/D3-A/D4 locked; tone plan SC-03; ADC input/clock/lane contract; budget |
| **FG-1** | Coil geometry, current, field, ICNIRP, thermal, current-sense, κ | SC-0 | Field map + ICNIRP closure + Jacobian conditioning + thermal + current-sense; `docs/phase2/fg_requirements.md` |
| **DRV-2** | DAC/reconstruction, driver topology, power/PSU, protection | FG-1 (R/L, current, current-sense) | Driver **A** locked; power **C1** locked; current-sense **A+** locked; **DAC/filter M16 locked (DAC80508 + 8× LTC1563-2)**; one box + E-stop locked; 150 mA first; **BOM/schematic Rev 0.02 issued**; **Pmod DA4 allowed as a 12-bit functional stand-in (182 kSPS, different 32-bit protocol), not for accuracy**; **16-bit bench option: TI DAC80508-04EVM (~$59 USD), functional/INL only, not 49 MHz timing**; **open: DAC placement — prefer on the FPGA board (49 MHz SPI hold margin 0.17 ns over the 2×20 + 0.5 m cable)** |
| **PEN-3** | \(N\), \(A\), \(\mu_a\), air vs ferrite, source impedance, \(\sigma_B\)/CRLB | FG-1 (field at pen) | **B air-core LOCKED**; INA163 recommended; `A_sens(f)`; \(\sigma_B\)/weighted CRLB; `pen_link_budget.md` |
| **FE-4** | Gain, noise, CMRR, input protection, differential output stage | PEN-3 + SC-0 (ADC contract) | AD7768-4 locked; **INA163 + ADA4940-2 locked**; gain/CMRR/σ_B/phase verified; output drives AD7768 RC/input |
| **ADC-5** | Input network, drive, reference, clocking, lane rate, pin count | FE-4 + SC-0 (ADC contract) | 4 ch/4 lanes/8.192 MHz/2×8 header proposed; code density, FFT/SINAD/THD, CMRR, ref noise, lane capture, zero dropped frames |
| **DIG-6** | SYNC/START/DRDY, integer-J, Goertzel, solver, latency/rate | ADC-5 + SC-0 (tone plan) | M16 clock/SPI locked; requirements proposed; 8.633 ms/115.8 Hz budget; integer-J leakage, golden comparison, 1-hour run at test |
| **INT-7** | κ calibration, 98-point accuracy, tremor, latency, stop, ICNIRP scan | All upstream | Phase 1 specs #1–25; test report; Phase 2 report |

---

## 2. Stage SC-0 — System contract

**Purpose.** Freeze the interfaces and units that every later stage consumes. This is the
stage that prevents the two big circular dependencies: FG current ↔ volume/ICNIRP, and
tone plan ↔ integer-J/frame length.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| SC-01 | Coordinate frame: origin at FG PCB centre, +z normal to board, right-handed, SI units; tracking volume = **100 mm minimum / 150 mm target / 200 mm stretch**; **D1-B: 150 mm cube at \(z=85.6\ldots235.6\) mm**; 100 mm fallback at 85.6–185.6; 200 mm stretch at 85.6–285.6 | Thesis §4.8 (origin at PCB centre); Phase 1 #3 (100 mm min); `contract/system_contract.md` D1 | LOCKED datum; D1-B LOCKED; SC-01d may demote | Drawing + simulation datum |
| SC-01d | Volume acceptance gate: final volume = largest candidate (100/150/200 mm) with ICNIRP pass, full 8×5 rank 5/no simultaneous null over the cube and ±45°, 95th-percentile CRLB position jitter ≤0.15 mm and orientation ≤0.1°, and 85.6/152 mm calibration planes inside. 100 mm min; **150 mm/B locked baseline; 200 mm only if the gate passes**; a failure demotes to 100 mm, not a bottom-face move. | Phase 1 #5–6/#11; `docs/phase2/anser-baseline-findings.md`; `simulations/field_jacobian.py`; D1/D4 decisions | PROPOSED test gate; baseline 150/B | CRLB/jitter run + field probe |
| SC-01e | CRLB noise target: 150 mm/B \(\sigma_B\le26\) pT, 100 mm/B ≤58 pT, 200 mm/B ≤11 pT; PEN-3 measures per-tone \(A_{sens}(f)\)/noise and re-runs the weighted CRLB | CRLB scan 2026-10-27; `field_jacobian.py` | PROPOSED; verify in PEN-3 | Noise-floor + weighted CRLB |
| SC-02 | Calibration/test planes at 85.6 mm and 152 mm from board top; 7×7 grid = 98 points; non-metal fixture | Jaeger Ch.7 §7.2.2; `docs/phase2/anser-baseline-findings.md` | LOCKED method, PROPOSED datum | 7×7 grid drawing + fixture check |
| SC-03 | Tone plan: 8 tones at 20, 22, 24, 26, 28, 30, 32, 34 kHz (2 kHz spacing); ADC ODR 256 kSPS, N=512 default (J=40..68, 4 bins); rectangular + integer-J primary, Hamming fallback; N=1024 Hamming fallback; per-coil assignment; frequency accuracy/stability; phase reference | Decision 2026-10-26, `docs/phase2/tone_plan.md`; thesis §3 2 kHz; AD7768 256 kSPS | LOCKED | 8-tone FFT + integer-J leakage; rectangular vs Hamming (DIG-05) |
| SC-04 | ICNIRP: 27 µT RMS, general public, 3 kHz–10 MHz; multi-tone linear sum; assessment surface **B = any accessible point** per `contract/system_contract.md` D2 | ICNIRP 2010 Table 4, Eq.5; Phase 1 #20 | LOCKED number/rule + surface B | Field-probe scan (FG-06/INT-06) |
| SC-04b | ICNIRP guard: **non-metal access barrier, not an EMF shield**; open-top ring/fence/spacer at the ~57 mm contour, no metal within 150 mm, plastic fasteners, removable; does not reduce the 150 mm volume (28.6 mm below the B cube bottom) | D2 decision 2026-10-27; Phase 1 #20; 150 mm metal-free rule | LOCKED | Field probe at accessible boundary + guard check |
| SC-05 | ADC contract: AD7768-4, differential ±VREF (±4.096 V), VCM output, input network (precharge buffer, external RC/charge reservoirs, drive/settling); preamp input capacitance ≤20 pF in the coil budget; ADR434 4.096 V reference, MCLK ≤32.768 MHz, ODR 256 kSPS, DCLK/DOUT lanes, SYNC/START/DRDY, SPI configuration only | AD7768 datasheet; `BOM_ADC-01`; correct stale RQ-A4/A5/A6 | LOCKED part, PROPOSED interface corrections | Datasheet + bench (ADC-5) |
| SC-06 | Channel map = **D3-A**: Ch0 current-sense, Ch1 pen 1, Ch2 pen 2, Ch3 reference; Ch2 wired but enabled when pen 2 is built | `adc_justification.md`; `fSysSetup.m`; D3 decision | LOCKED (D3-A) | Schematic review |
| SC-07 | Clock tree: one TCXO → PLL → clk_dds + MCLK_adc; single sync reset; integer-J frames | AGENTS full-FPGA decision | LOCKED architecture, TBD part | Clock-phase sweep; leakage test |
| SC-08 | Budget gate: \(T_{pose}=T_{acq}+T_{demod}+T_{solv}<10\) ms; pose rate ≥100 Hz; latency ≤20 ms off / ≤100 ms on; lane rate and pin budget | Phase 1 #14–16; `adc_justification.md` §5 | PROPOSED | Budget spreadsheet + timed loop |
| SC-09 | Units/naming: RMS unless stated; dBc; T/A; mm; sample/frame definitions | Team convention | PROPOSED | Document review |
| SC-10 | Change control: one owner per interface; freeze date; written deviation for any reopen | Team process | PROPOSED | Signed table |

**Exit gate.** `contract/system_contract.md` is created; the tone plan, ADC contract,
clock tree, and budget are locked; D1–D4 and SC-01d are chosen and signed. Do not start
FG-1 until SC-01, SC-01d, SC-03, SC-04, SC-05, SC-06 are signed.

---

## 3. Stage FG-1 — Field, ICNIRP, current, volume

**Purpose.** Close geometry + volume + current + ICNIRP as one set, and produce the field
and conditioning map that the pen coil and solver consume.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| FG-01 | Geometry: 8 coils, 25 turns, 70 mm square, trace 0.5 mm / gap 0.25 mm, 1.6 mm PCB, 30×30 cm, centres/orientations per `fSysSetup.m`; placement tolerance to be set | Thesis §4.8; `fSysSetup.m:90-105` | LOCKED heritage, PROPOSED tolerance | Gerber + CMM/optical check |
| FG-02 | Electrical: coil resistance ≤2.5 Ω, inductance 70 µH ±20%, mutual-coupling matrix at 20–30 kHz | Thesis §4.8 (2 Ω, 70 µH) | PROPOSED | LCR + impedance analyser |
| FG-03 | Current: 250 mA nominal heritage, **150 mA prototype first**, 500 mA max; RMS-vs-peak convention frozen at SC-09; programmable 150–500 mA; continuous max = min(FG-06, FG-07); tolerance ±1%; drift ≤0.1% over 18–28 °C; THD ≤−60 dBc | Thesis §4.2–4.3; `driver_power_requirements.md` thermal note | PROPOSED; 150 mA first | Sense-resistor FFT + thermal soak |
| FG-04 | Field map: B per tone at 98 points; worst-case minimum per tone; inter-coil balance; no tone below the noise floor anywhere in the volume | Jaeger Ch.3; `simulations/field_jacobian.py` | PROPOSED | Filament-model map + field probe |
| FG-05 | Conditioning: full 8×5 Jacobian \(J\); rank 5; no simultaneous null over the cube and ±45°; 95th-percentile CRLB ≤0.15 mm / ≤0.1° per SC-01d; 150/B requires \(\sigma_B\le26\) pT, 100/B ≤58 pT, 200/B ≤11 pT; target 150 mm, 100 mm min, 200 mm stretch | Solver requirement; `field_jacobian.py`; SC-01d/e | PROPOSED | Simulated \(J\)/CRLB map + measured finite difference |
| FG-06 | ICNIRP: linear sum \(\sum_j B_j/27\,\mu T \le 1\) at all accessible points; report max continuous current and 27 µT contour; non-metal guard per SC-04b (open-top ring/fence, no metal within 150 mm) | ICNIRP 2010 Eq.5; Phase 1 #20; SC-04b | LOCKED rule, PROPOSED geometry | AC field-probe scan over volume + accessible boundary |
| FG-07 | Thermal: coil power, PCB temperature rise ≤20 °C, max continuous current for 8 coils; enclosure rise | Proposed; no source yet | PROPOSED | Thermal soak + thermocouples/IR |
| FG-08 | Current-sense: \(R_{store}\) per coil, summer scale, V/I transfer, bandwidth ≥? kHz, phase, common-mode, ADC Ch0 interface | `fSysSetup.m` `R_store`, `I_summer_scale` | PROPOSED | Inject known current; measure Ch0 |
| FG-09 | Calibration: κ per coil/tone; 7×7 grid; drift budget; geometry tolerance included | Jaeger §7.2.2; Eq.7.10 | LOCKED method, PROPOSED numbers | 7×7 κ fit + repeat run |
| FG-10 | Test plan: field map, ICNIRP scan, current-loop step, thermal soak, harmonic FFT | Phase 1 test plan | PROPOSED | Test report |

**Known closure to resolve at this gate (filed filament sim, equal 250 mA per coil):**

| z | Max linear ICNIRP sum | Verdict |
|---|---|---|
| 40 mm | 43.0 µT | fail |
| 50 mm | 32.0 µT | fail |
| 66 mm | 21.6 µT | pass, ~20% margin |
| 85.6 mm | 14.8 µT | pass |
| 150 mm | 5.6 µT | pass |

The 27 µT contour is at about \(z \approx 57\) mm at 250 mA. Therefore the volume's
bottom face (100/150/200 mm candidate) and the continuous current must be chosen together. At 500 mA, even
\(z=66\) mm gives 43 µT; 500 mA is not a continuous ICNIRP-compliant current.

**Current convention (not yet frozen, SC-09).** The table assumes 250 mA is the
field-driving RMS amplitude. If the heritage 250 mA is a peak value, scale the field by
\(1/\sqrt{2}\) before comparing with the 27 µT RMS limit.

**Exit gate.** `docs/phase2/fg_requirements.md`; update `simulations/field_jacobian.py` to
report the full 8×5 Jacobian, ICNIRP linear sum, and max continuous current. Sign the
cube bottom face, nominal current, max continuous current, and current-sense contract.

**If the gate fails.** If ICNIRP fails at the chosen \(z_{min}\), either raise the cube
bottom/guard (if ergonomically acceptable) or reduce the continuous current. If current
drops, re-run PEN-3; do not keep 250 mA by silently shrinking the volume.

---

## 4. Stage DRV-2 — Driver, power, PSU

**Purpose.** Turn the FG current/voltage/thermal envelope into a stable constant-current
drive, including the excitation DAC and power delivery. Runs in parallel with PEN-3/FE-4
after FG-1. First-pass requirements: `docs/phase2/driver_power_requirements.md`.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| DRV-01 | Excitation: **FPGA DDS on Artix-7 XC7A35T PL (PS-less, BRD-01) + M16 DAC/filter: 1× DAC80508 (16-bit, 8 ch, 200 kSPS) + 8× LTC1563-2 (4th-order, 60 kHz); XADC 12-bit not used; DAC update 199.805 kSPS (÷164); SPI 49.152 MHz, 8×24-bit + TRIGGER frame = 216 bits, software LDAC (no LDAC pin)**; amplitude/phase control | `tone_plan.md`; AGENTS full-FPGA; `simulations/m16/FINAL_REPORT.md` | LOCKED (M16 selected 2026-10-27) | 8-tone FFT + phase; filter/image/EVM |
| DRV-02 | Output: 250 mA nominal / 500 mA max; **150 mA prototype first**; programmable 150–500 mA; 70 µH + 2 Ω; 34 kHz \(\lvert Z\rvert\approx15.1\ \Omega\); 250 mA → 5.3 V peak, 500 mA peak → 7.55 V peak (rail limit); 20–34 kHz | Thesis §4.2–4.3; `tone_plan.md`; thermal note | PROPOSED; 150 mA first | Load-step test |
| DRV-03 | Constant-current: phase margin ≥45° at 34 kHz; output impedance high; current error ≤0.1%; drift ≤0.1% over 18–28 °C | Thesis §4.3.3; O'Donoghue §II | PROPOSED | Step/load response; current log |
| DRV-04 | Distortion: THD ≤−60 dBc at 250 mA; **all-tone IMD** below the spur budget (3rd-order products fall on tone bins); crosstalk ≤−60 dB; noise | Docs spur budget; `tone_plan.md` IMD note | PROPOSED | Sense-resistor FFT + 8-tone IMD |
| DRV-05 | Power: **C1 + medical-grade locked** — one external 15 V/60 W-class medical-grade adapter (no on-board mains stage) + on-board DC-DC/LDO tree; +15 V, −15 V, +5 V, +3.3 V; FPGA core via board regulator (+1.8 V only if final board needs it) | `driver_power_requirements.md` §3 | LOCKED C1 + medical-grade | Rail noise/load test |
| DRV-06 | Thermal: 8 channels at 250 mA; coil \(I^2R\) ≈0.125 W/coil, sense ≈0.06 W each, LMH6321 dissipation; no 3 kg heatsink; ~180 cm² board; **one-box enclosure with internal shield partition** | Thesis §4.3; measured R/L; D5 decision | LOCKED one-box; thermal test PROPOSED | Thermal soak |
| DRV-07 | Protection: overcurrent, overtemp, disable, fault, stop ≤100 ms; no DC current in coil (100 µF AC coupling); **hardware E-stop: NC mushroom button in driver enable chain, independent of FPGA; opto status; software watchdog; A+ per-coil peak comparators** | Phase 1 #17; thesis §4.3.1; D5 decision | LOCKED E-stop; other protection PROPOSED | Fault injection; E-stop timing |
| DRV-08 | Current-sense **A+ locked**: per-coil \(R_{store}\) + analog summer → ADC Ch0; individual peak/overcurrent comparators; no mux/extra ADC; V/I/phase at 34 kHz; keep \(R_{store}\) 0.957–1.239 Ω / summer 2.0103 baseline | `fSysSetup.m`; `driver_power_requirements.md` | LOCKED A+ | Known-current injection; phase check |
| DRV-09 | Test: constant-current step/load, THD/IMD, thermal, fault/disable | Phase 1 test plan | PROPOSED | Test report |

**Electronics LOCKED as one board (BRD-01, 2026-10-28):** the old PWR-DRV-01 / FE-ADC-01 /
FPGA-IF-01 split is three zones of one 4-layer board; FG-01 stays a separate passive coil PCB.
FPGA integration is **D (PS-less Artix-7 on BRD-01)**, 2026-10-28 — `system_schematic.md` §6.0.

**Driver topology LOCKED (2026-10-27): A — LMH6321-class, new board based on thesis
§4.3, not a clone.** Single +15 V, AC-coupled, 100 µF, 250 mA nominal / 500 mA max,
~180 cm². Exact passives and alternate parts are open where lifecycle/thermal/loop
justify a change; record the deviation. The vendor Rev A discrete class-AB board
(±15 V, ~30 W, 3 kg heatsink) is reference/fallback only.
**Still open:** thermal/test details and the M16 bench (8-tone EVM, loop PM/step,
LMH6321 crossover, EMI/thermal). The DAC/filter is locked: **DAC80508 + 8×
LTC1563-2**, 199.805 kSPS, SPI 49.152 MHz. Current-sense **A+** is locked (summed Ch0 +
individual peak/overcurrent taps). Power is **C1 + medical-grade** (external
15 V/60 W medical adapter + on-board DC-DC/LDO tree; FPGA core via its board
regulator). Enclosure is **one box with internal shield**; hardware **E-stop**
is a NC mushroom button in the driver enable chain, independent of the FPGA.

**Exit gate.** One channel constant-current verified before any accuracy claim; THD/IMD,
thermal, protection, current-sense V/I/phase, DAC part, power rails, schematic/BOM
signed.

**If the gate fails.** If the chosen driver cannot deliver FG-03/DRV-02 current or
compliance, return to FG-1 and re-run the field/ICNIRP/pen closure. Do not silently
reduce current and leave PEN-3 based on the old field.

---

## 5. Stage PEN-3 — Pen coil and amp-floor verification

**Purpose.** Given the field from FG-1, choose \(N\), \(A\), \(\mu_a\) and decide air vs
ferrite with numbers. This is a verification stage: the coil is cheap to change.
First-pass link budget: `docs/phase2/pen_link_budget.md`.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| PEN-01 | Input: B per tone at the worst pose from FG-04 | FG-1 | TBD | Field map |
| PEN-02 | Coil: **B air-core LOCKED** (1.59 mm, 5.3 pT at 20 kHz with INA163); A/E are alternates; C air is out (2.48 mm, 18.6 pT); mass ≤50 g pen; no ferrite for B | Jaeger Ch.7 Table 7.1; `pen_link_budget.md` | LOCKED (B air) | Build + scale |
| PEN-03 | Signal: \(V_s=N A \omega \mu_a B\) per tone at worst pose; source impedance; winding capacitance | Jaeger Eq.7.2–7.9 | PROPOSED | Helmholtz calibration |
| PEN-04 | Amp floor: demonstrate per-tone \(\sigma_B\le26\) pT at 150 mm/B (weakest-tone SNR ≥72 dB), ≤58 pT at 100 mm/B, ≤11 pT at 200 mm/B; **INA163 required for 150/200**; INA128/AD620 only for 100/B; use measured \(A_{sens}(f)\)/noise and re-run the weighted CRLB | `pen_link_budget.md`; SC-01e | PROPOSED | Noise-floor + weighted CRLB |
| PEN-05 | Ferrite: **no ferrite for B (LOCKED)**; C ferrite only if a small-diameter coil is forced (1.90 mm, ~6.2 pT, but nonlinearity/Barkhausen); measured µa; linearity; mass; capacitance | Jaeger Eq.7.5–7.7; `pen_link_budget.md` | LOCKED (no ferrite for B) | A/B FFT + linearity sweep |
| PEN-06 | Resonance: \(C_{total}\le73\) pF at 34 kHz; \(f_{res}>340\) kHz; W2697 0.6 m (59 pF) passes | `tone_plan.md` §6; connector Rev D | LOCKED budget | LCR + resonance sweep |
| PEN-07 | Calibration: \(A_{sens}(f)=V/B\) by Helmholtz; κ per tone | `fSysSetup.m` | PROPOSED | Helmholtz run |
| PEN-08 | Test: Helmholtz, noise, \(\sigma_B\)/weighted CRLB, mass, linearity; tone assignment weakest coil → 34 kHz | Phase 1 test plan; `pen_link_budget.md` | PROPOSED | Test report |

**Exit gate.** Build/measure **B air + INA163** (A/E alternates); \(A_{sens}(f)\) and
input-referred noise over 20–34 kHz; re-run the weighted CRLB. 150 mm/B is the target;
200 mm/B is allowed only if it passes; 100 mm/B is the fallback. Do not exceed FG-06.

---

## 6. Stage FE-4 — Receiver front end

**Purpose.** Amplify the pen signal and produce the differential output that the locked
AD7768-4 expects. The new block is the single-ended-to-differential output stage; the
heritage stops at a single-ended DAQ input. First-pass requirements:
`docs/phase2/frontend_requirements.md`.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| FE-01 | Input: **INA163 (LOCKED)**, differential, \(Z_{in}\ge1\) MΩ, CMRR ≥60 dB (target 100 dB), input protection/ESD, bias/AC-coupling for the 12 µA input bias current; preamp input capacitance ≤20 pF in the 73 pF coil budget | `pen_link_budget.md`; thesis §4.4.2; E301 reference | LOCKED part (INA163); bias network PROPOSED | CMRR sweep 20–34 kHz; bias/offset check |
| FE-02 | Gain: INA163 ~35× + differential stage ~2× (total ~70×); strongest tone at 150/200 mm ≤−6 dBFS; weakest tone above noise; headroom for 30–40 dB tone spread | `pen_link_budget.md`; SC-05 | PROPOSED | Gain/phase sweep; full-scale test |
| FE-03 | Noise: INA163 1.1 nV/√Hz; total input-referred ≤26 nV over 500 Hz; \(\sigma_B\le26\) pT at 150 mm/B (≤11 pT at 200, ≤58 pT at 100) | `pen_link_budget.md`; SC-01e | PROPOSED | Input-referred noise; weighted CRLB |
| FE-04 | Output stage: single-ended-to-differential, \(V_{CM}\) = ADC VCM, ±4.096 V differential, AD7768 reference RC/charge-reservoir network, **ADA4940-2 (LOCKED; ADA4896-2 alternate)**, inter-channel phase match ≤0.1° | AD7768 datasheet; `frontend_requirements.md`; AN-1384 | LOCKED part/architecture | Output settling + phase test |
| FE-05 | Reference/clock: ADR434 4.096 V, ADC VCM, MCLK from the common clock tree | `BOM_ADC-01` | LOCKED part | Rail/reference noise |
| FE-06 | Test: gain, CMRR, noise, THD, phase match, settling into the AD7768 RC/input model | Phase 1 test plan | PROPOSED | Test report |

**Decision LOCKED (2026-10-27).** **INA163** (1.1 nV/√Hz) + **ADA4940-2**
differential stage (ADA4896-2 alternate). The **AD7768-4 is the locked ADC**; the front
end matches its ±4.096 V differential input, VCM, and external RC/charge reservoirs.
The E301 **AD620/AD627 + AD711** and the INA128/TL071 parts list are **not sufficient
for 200 mm/B and only marginal for 150 mm/B** (B/E at 34 kHz); they are 100 mm
fallback/reference only. The INA163 input bias current (12 µA) is handled with AC
coupling. Supplies: INA163 ±12 V, ADA4940-2 +5 V, AD7768 +5 V/+3.3 V.

**Exit gate.** Schematic/BOM; bench verification; \(\sigma_B\)/weighted CRLB; output
drives the AD7768 RC/input model.

---

## 7. Stage ADC-5 — ADC interface verification

**Purpose.** Verify the locked AD7768-4 interface against its actual datasheet, not the
SAR-oriented assumptions in the earlier requirements.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| ADC-01 | Input range: differential ±VREF = ±4.096 V; VCM common mode; correct RQ-A5 (±5/±10 V is stale) | AD7768 datasheet | LOCKED part, PROPOSED correction | DC sweep |
| ADC-02 | Input network: precharge buffer, input current, settling, external RC/charge reservoirs; the 73 pF coil budget covers cable + connector + **preamp input**, not the ADC switched-cap network | Datasheet; `BOM_ADC-01` open item; §4 topology correction | LOCKED contract, TBD measurement | Input-current + settling test; preamp-input capacitance check |
| ADC-03 | Reference: ADR434 4.096 V, noise, decoupling, reference buffer | `BOM_ADC-01` | LOCKED part, PROPOSED network | Reference noise/FFT |
| ADC-04 | Clock: MCLK ≤32.768 MHz, ODR 256 kSPS, DCLK, SYNC/START/DRDY; integer-J; jitter ≤30 ps for 104 dB at 34 kHz (1 ns only gives 73.4 dB) | Datasheet; SC-07; RQ-A4 correction | PROPOSED | Clock-phase sweep + jitter measurement |
| ADC-05 | Lane/pin: **4 active channels**; 4 DOUT lanes; DCLK 8.192 MHz; 32-bit frames; 2×8/custom header. 2×6 Pmod is insufficient for 4 DOUT + control + MCLK | Datasheet; D3-A; Pmod 2×6 = 8 I/O | PROPOSED interface | Pin-budget review + capture |
| ADC-06 | Data path: DCLK-synchronous DOUT lanes, not SPI; SPI is configuration only | Datasheet | LOCKED correction | Logic-analyser capture |
| ADC-07 | Test: code density, FFT/SINAD/THD, CMRR, reference noise, lane capture, zero dropped frames | `adc_justification.md` §8 | PROPOSED | Test report |

**Immediate blocker resolved.** The real datasheet is now at `docs/ad7768-ad7768-4.pdf`
and `reference-cache/datasheets/AD7768-allds.pdf`. Extract the precharge-buffer input current,
external RC/charge-reservoir values, and settling requirements to close ADC-02. The ADC
sits behind the preamp: the 73 pF coil budget covers cable + connector + preamp input,
not the ADC's switched-cap network.

**Exit gate.** Interface verified; BOM update; zero dropped frames over a 1-hour run.

**If the gate fails.** If the AD7768-4 fails \(C_{in}\), lane, or pin-budget checks,
invoke the documented AD7606C-16 + matched anti-alias fallback and return to SC-0. Do
not patch the front end around a failing ADC.

---

## 8. Stage DIG-6 — Digital, demod, timing

**Purpose.** Close the common-clock, integer-J, demod, solver, and latency/rate budget.

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| DIG-01 | DDS: 8 tones, 32-bit accumulator, 4096-entry LUT, **1 SPI at 49.152 MHz (8×24-bit = 192 bits)**, phase coherence | AGENTS; `docs/phase2/anser-baseline-findings.md` §6; `dig6_requirements.md` | PROPOSED requirements | Two-tone FFT + phase |
| DIG-02 | Capture: DCLK/DOUT lanes, DRDY, ping-pong BRAM/DMA, no missed frames | ADC-5; `dig6_requirements.md` | PROPOSED requirements | 1-hour capture |
| DIG-03 | Demod: Goertzel per tone; rectangular + integer-J primary, Hamming fallback; phase sign, \(Y_I/Y_V\), fixed group-delay offset | `fSysGetField.m`; `docs/phase2/tone_plan.md` | PROPOSED requirements | Golden comparison; rectangular vs Hamming |
| DIG-04 | Solver: LM/TRF, bounds, warm start, retry, relaxed tolerance | `fSysDecodeField.m` | PROPOSED requirements | Golden comparison |
| DIG-05 | Budget: \(T_{pose}=8.633\) ms (2.000 acq + 0.133 ADC + 0.5 demod + 5.0 solve + 1.0 overhead) = 115.8 Hz; latency ≤20/100 ms; lane 32.768 Mbit/s | Phase 1 #14–16; `dig6_requirements.md` | PROPOSED requirements | Timed loop + budget sheet |
| DIG-06 | Test: integer-J leakage, moving-sensor run, drop counter | Phase 1 test plan | PROPOSED requirements | Test report |

**Compute justification:** `docs/phase2/fpga_vs_mcu_compute_budget.md` — 800 filament
segments/evaluation, forward-difference Jacobian 6 evaluations/iteration, 100 Hz
worst-case ≈2.5–5.8 GFLOP/s; the FPGA parallel kernel covers it, a high-end MCU does not
guarantee it. Full FPGA Phase 2 justification/requirements:
`docs/phase2/fpga_justification_and_requirements.md`. DIG-06 must replace the estimate with
measured cycles/evaluation.

**Exit gate.** Budget closure; MATLAB golden match; 1-hour moving run with zero dropped
frames. If integer-J fails, return to SC-03 — do not patch it in DIG-6.

---

## 9. Stage INT-7 — Integration, calibration, acceptance

| ID | Requirement | Source / rationale | Status | Verification |
|---|---|---|---|---|
| INT-01 | Constant-current verified first, before any accuracy claim | O'Donoghue §II; thesis §4.3.3 | LOCKED gate | Current log |
| INT-02 | κ calibration on 7×7 grid | Jaeger §7.2.2 | LOCKED method | κ fit residuals |
| INT-03 | 98-point RMS at 85.6/152 mm, Eq.7.10 | Jaeger Eq.7.10 | LOCKED | Accuracy run |
| INT-04 | Hand accuracy ≤2 mm / ≤1°; repeatability ≤10 µm | Phase 1 #5–6, #11 | LOCKED | 7×7 grid + 10 approaches |
| INT-05 | Tremor ≥20 dB @6–12 Hz; ≤3 dB <1 Hz; latency; stop ≤100 ms | Phase 1 #12–17 | LOCKED | Sine sweep + timing |
| INT-06 | ICNIRP scan, thermal, EMC; ≤27 µT at accessible points | Phase 1 #20–25 | LOCKED | Field-probe scan + thermal log |
| INT-07 | BOM ≤1000 CAD/pair | Phase 1 #24 | LOCKED | BOM roll-up |
| INT-08 | Test report + Phase 2 report | Manual pp.13–14 | PROPOSED | Submitted report |

**Exit gate.** Phase 1 specs #1–25 met or deviation documented; test report; Phase 2
report.

---

## 10. What changed from the original order

| Original | Fixed order | Why |
|---|---|---|
| FG spec first | SC-0 contract first | Tone plan, ADC contract, clock tree, and budget are inputs to FG, not outputs of it |
| FG → pen → FE → ADC → digital | FG → {driver/power, pen} → FE → ADC verify → digital | Driver/power was missing; ADC contract must precede FE |
| ADC interface after FE | ADC contract in SC-0; ADC verification after FE | The locked ADC constrains the FE output stage; verification still follows FE |
| “CONVST” | SYNC/START/DRDY | AD7768-4 has no CONVST; data path is DCLK/DOUT, not SPI |
| “Uniformity” | Inter-coil balance + 8×5 Jacobian conditioning | Uniform B has zero gradient and no position information |
| ICNIRP number | ICNIRP number + linear multi-tone sum + accessible boundary | Eq.5 sums per-tone RMS amplitudes; the near-board contour is the real constraint |
| Digital last | Tone plan/integer-J in SC-0; digital closure last | Late integer-J failure invalidates the FG tone plan |
| — | INT-7 calibration/acceptance | κ, 98-point RMS, constant-current, ICNIRP, thermal, EMC were not in the design order |

---

## 11. Working checklist

- [x] **SC-0** — frame, volume (D1-B/D3-A/D4 locked), tone plan, ICNIRP surface, ADC contract, clock tree, budget gate frozen.
- [ ] **FG-1** — field map, ICNIRP linear-sum closure, 8×5 conditioning, thermal, current-sense signed.
- [ ] **DRV-2** — one-channel constant-current verified; THD, thermal, protection; BOM/schematic Rev 0.02 with M16 (bench test open).
- [ ] **PEN-3** — \(N\), \(A\), \(\mu_a\) and ferrite decision with numbers; \(A_{sens}(f)\); SNR map.
- [x] **FE-4** — INA163 + ADA4940-2 locked; gain/noise/CMRR/differential output bench verification open.
- [ ] **ADC-5** — \(C_{in}\)/drive/reference/clock/lane/pin verified; zero dropped frames.
- [ ] **DIG-6** — requirements proposed; integer-J, Goertzel, solver, latency/rate budget at requirements level; bench timing open.
- [ ] **INT-7** — κ, 98-point RMS, tremor, latency, stop, ICNIRP scan; Phase 1 specs #1–25.

## 12. Immediate next actions

1. Review the Rev A draft system flow chart, board-level schematic, and system BOM; the team decides the open items before sign-off.
2. Bench-close ADC-5: 4-channel/4-lane capture, RC settling, FFT/SINAD, zero dropped frames.
3. Run the FG-1 closure at the 150 mm/B baseline: full CRLB/jitter, ICNIRP/current/thermal; final volume by SC-01d.
4. Bench-close DRV-2 one channel at 150 mA: constant-current, THD/IMD, thermal, E-stop/overcurrent, EMI with the one-box shield.
5. Bench-close DIG-6: integer-J leakage, golden demod/solver, 8.633 ms worst-case timing, 1-hour moving run.

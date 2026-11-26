# BRD-01 passive value justification and provenance register

Third document in the BRD-01 reference set. `docs/phase2/brd01_wiring_manifest.md` is
net-centric (net → pins), `docs/phase2/brd01_component_reference.md` is component-centric
(component → pins → wires, including each passive's **function**), and this one
answers **why this value and who says so**. It covers every resistor and
capacitor in the netlist exactly once.

**What `UNDOCUMENTED` means here.** It means **no recorded justification was
found** in the repo or in a datasheet section the repo names. It does **not**
mean the value is wrong. Several of these are certainly correct engineering
that was simply never written down — the register at §5 is a list of missing
paperwork and open questions, not a list of defects. Where a repo file states a
value without deriving it, this document says "stated, not derived" and cites
the file rather than inventing a reason. Where only a datasheet is referenced,
this document cites the reference number or the named datasheet section and
does not claim to have read the datasheet itself.

**Source shorthand** (all paths repo-root-relative; line numbers at first
citation):

| Alias | File |
|---|---|
| PT2 | `docs/phase2/power_tree_v2.md` — **LOCKED power tree, decision #31 (2026-11-25); supersedes the #20 part list**, not a proposal |
| BOM | `hardware/brd-01/kicad/bom-to-cad.md` |
| SS | `docs/phase2/system_schematic.md` |
| FE | `docs/phase2/frontend_requirements.md` |
| DRV | `docs/phase2/driver_power_requirements.md` |
| M16 | `docs/handoff/m16-fpga-handoff.md` |
| IO | `docs/handoff/brd01_io_handoff.md` |
| DL | `contract/decisions_log.md` |
| MAN | `docs/reference/MANIFEST.md` |
| PTR | `hardware/brd-01/kicad/power-tree.md` (legacy v1 tree; stale, see §6.5) |
| CR | `docs/phase2/brd01_component_reference.md` |
| ADCIC | `docs/phase2/adc_interface_closure.md` |

Method: `kicad-cli sch export netlist --format kicadxml -o /tmp/vj/net.xml hardware/brd-01/kicad/brd-01.kicad_sch` (KiCad 10.0.8) gives **640 components, 605 nets, 501 two-pin passives = 276 R + 225 C**. Every R/C ref below comes from that netlist, not from prose.

---

## 1. Headline finding — summary

Evidence classes are mutually exclusive and are defined as: **arithmetic** = a
calculation shown in §2/§4 that reaches a target the repo states; **repo file**
= a specific file/line states the value or the class rule, but not its
derivation ("stated, not derived"); **datasheet section** = a datasheet section
named in the repo (REF number given in `docs/reference/MANIFEST.md:11-24`),
not read here; **UNDOCUMENTED** = none of the above.

| Evidence class | Count | Share of 501 |
|---|---:|---:|
| Arithmetic shown in this document | 159 | 31.7 % |
| Cited to a repo file (stated / class rule, not derived) | 239 | 47.7 % |
| Cited to a datasheet section named in the repo | 50 | 10.0 % |
| `UNDOCUMENTED` | 53 | 10.6 % |
| **Total** | **501** | **100.0 %** |

Structural partition (every passive in exactly one tier):

| Tier | Rule | Count | Share |
|---|---|---:|---:|
| 1 | Value participates in an equation or a datasheet-prescribed function | 283 | 56.5 % |
| 2 | Supply decoupling and bulk, justified by class | 149 | 29.7 % |
| 3 | Pulls, series links, bleeds, simple signal coupling | 69 | 13.8 % |
| **Total** | | **501** | **100.0 %** |

Gate 1: 283 + 149 + 69 = 501; netlist-minus-assigned and assigned-minus-netlist
are both empty. Gate 2: 159 + 239 + 50 + 53 = 501. **89.4 %** of passives have either arithmetic or a
specific citation; **10.6 %** have no recorded justification at all. Of the
89.4 %, **57.7 %** rest on a citation or class statement rather than a
per-part derivation.

---

## 2. Tier 1 — value-setting passives (283)

### 2.1 Regulator feedback dividers

All buck dividers use `Vout = VFB × (1 + Rtop/Rbot)`. PT2:221 gives the
TPS62130A rule `R1 = R2 × (VOUT/0.8 − 1)` with `R2 ≤ 400 kΩ`, and PT2:179 gives
the TPSM63604 rule with `VFB = 1 V`.

| Served part / rail | Refs (value) | Arithmetic | Designed quantity | Source |
|---|---|---|---|---|
| U144 TPS62130A, `+1V0_FPGA` | R190 49.9 kΩ top, R191 200 kΩ bottom | `0.8 × (1 + 49.9/200) = 0.99960 V`; VFB band 785.6–814.4 mV → 0.9816–1.0176 V | 1.000 V; Artix-7 0.95–1.05 V ✓ | PT2:221-223; CR:463 |
| U145 TPS62130A, `+1V8_FPGA` | R193 249 kΩ, R194 200 kΩ | `0.8 × (1 + 249/200) = 1.796 V`; band 1.7637–1.8283 V | 1.796 V (target 1.80, −0.22 %); Artix-7 1.71–1.89 V ✓ | PT2:221-223; CR:497 |
| U7 TPS62130A, `+3.3V` | R806 619 kΩ, R807 200 kΩ | `0.8 × (1 + 619/200) = 3.276 V`; band 3.2170–3.3350 V | 3.276 V (target 3.3, −0.73 %); VCCO 3.135–3.465 V ✓ | PT2:221-223; CR:430 |
| U147 TPSM63604, `+6V` | R800 49.9 kΩ 0.1 %, R801 10.0 kΩ 0.1 % | `1 × (1 + 49.9/10.0) = 5.99 V`; VFB ±1 % → 5.930–6.050 V | 5.99 V (target 6.0, −0.17 %) | PT2:179; CR:573 |

**Dispatch correction:** the brief lists `R195` among the feedback dividers.
The netlist shows `R195` is the 100 kΩ `PG_1V8` pull-up on U145's PG / U7's EN
(CR:421, CR:429); the U7 divider is R806/R807. No capacitor or resistor named
`R195` touches `U7.FB`.

### 2.2 U147 TPSM63604 — frequency, enable, feed-forward

| Refs (value) | Formula and arithmetic | Designed quantity | Source |
|---|---|---|---|
| R802 13.0 kΩ 1 % (RT) | PT2:182 gives `RRT = 13.46/fSW − 0.44 kΩ`; invert: `fSW = 13.46/(13.0 + 0.44) = 1.0015 MHz` | 1.0015 MHz free-running (PT2 calls it 1.000 MHz); sync target 1.024 MHz | PT2:182, PT2:192-200; REF-14 = TI SLVSGJ5 (MAN:166-171) |
| C805 18 pF C0G (FB feed-forward) | No calculation in repo; PT2:180 states it is between the datasheet Table 8-1 values of 22 pF (5 V) and 15 pF (7.5 V). Linear interpolation at 6 V gives 19.2 pF; the captured 18 pF is the value PT2 records. | Feed-forward pole for 6 V out; **stated, not derived** | PT2:180; REF-14 (MAN:166) |
| R803 1.00 MΩ / R804 118 kΩ (EN/UVLO) | Divider factor `118/(1000+118) = 0.10555`; `1.263/0.10555 = 11.97 V` on, `0.91/0.10555 = 8.62 V` off | 11.97 V turn-on, 8.62 V turn-off; parallel 105 kΩ, inside the ~100 kΩ asked for when syncing | PT2:183, PT2:340 |
| C809 1 nF (BUCK_SYNC → EN/SYNC) | Datasheet-recommended AC coupling; 3.3 V edge > 2.4 V threshold. No per-value derivation. | 1.024 MHz sync injection (32.768 MHz ÷ 32) | PT2:184, PT2:402; REF-14 (MAN:166) |
| C810 1 µF X7R (VLDOIN) | Local bypass; PT2:185 says VOUT ≤ 12 V so tie to VOUT for efficiency. Value stated, not derived. | VLDOIN bypass | PT2:185; REF-14 (MAN:166) |

### 2.3 Soft-start, noise and input-filter setting

| Refs (value) | Formula and arithmetic | Designed quantity | Source |
|---|---|---|---|
| C181, C185, C814 — 3.3 nF each on U144/U145/U7 `SS/TR` | PT2:224 gives `tSS = C × 1.25 V / 2.5 µA`: `3.3 nF × 1.25 / 2.5 µA = 1.65 ms` | 1.65 ms ramp; inside Artix-7 0.2–50 ms window (PT2:353) | PT2:224, PT2:344-353; REF-08 / TI SLVSAG7F (MAN:102-111) |
| C189, C815 — 1 µF on U146/U149 `NR` | No arithmetic: PT2:255-256 states CNR = 1 µF in the PSRR/noise specs and ≥10 µF / 47 µF on the output. | Noise-reduction pole for TPS7A4701 | PT2:253-260; REF-08 / TI SBVS204G (MAN:102-111) |
| R808, R809 — 0.68 Ω in FL1/FL2 damper legs | PT2:319 gives `Rd ≈ √(L/C)`: `√(1 µH / 2.2 µF) = 0.6742 Ω` → 0.68 Ω standard (+0.86 %) | 0.674 Ω target; ±1.8 dB worst case in the 20–34 kHz band (PT2:321-332) | PT2:303-332 |
| C818, C820 — 10 µF damper capacitors | PT2:319 states the leg is `0.68 Ω in series with 10 µF X7R ≥16 V`; **stated, not derived** (only Rd has an equation). | Damped LC leg; peak +2.7 dB at 64 kHz | PT2:315-332 |
| C203 — 150 nF on DAC80508 `REF` | Netlist/component reference state the value only. No datasheet section for the REF bypass cap is named in the repo. | DAC internal 2.5 V reference bypass — **UNDOCUMENTED** (§5) | CR:1238; REF-08 DAC80508 (MAN:102-111) |

### 2.4 ±12VA analog LDOs (legacy SET network)

`hardware/brd-01/kicad/power-tree.md:93-94` states "R3 121k on SET → 12.1 V"
and "R1 121k on SET → −12.1 V". This is a **legacy v1** document (it also
carries `+15V_DRV`, `+5V`, K1/K2 — see CR:208), but the SET network itself is
unchanged by PT2 §2. The arithmetic implied by the stated
outcome is `12.1 V / 121 kΩ = 100 µA`; the repo does **not** transcribe the
SET-current equation, so the value is cited, not derived.

| Refs (value) | What is recorded | Designed quantity | Source |
|---|---|---|---|
| R3 121 kΩ (U6 LT3045-1 SET), R1 121 kΩ (U2 LT3093 SET) | Stated, not derived | ±12.1 V analog rails | PTR:93-94 (stale tree, SET network unchanged); PT2:33 |
| C3, C6 — 4.7 µF on the same SET pins | Value stated in the component reference; no rationale or datasheet section named | SET-pin bypass — **UNDOCUMENTED** (§5) | CR:355, CR:401 |
| R4 750 Ω / R2 7.5 kΩ on `ILIM` | Value stated; ILIM equation not in repo | Current-limit programming — **UNDOCUMENTED** (§5) | PTR:93-94; CR:351, CR:397 |

### 2.5 Driver — current sense, loop, filters, trip

| Served part | Refs (value) | Formula and arithmetic | Designed quantity | Source |
|---|---|---|---|---|
| R20–R27 (`R_store`, 8×) | 1.00 Ω 0.1 % 0.5 W | `I·R`: at 150 mA → 0.150 V / 22.5 mW; 250 mA → 0.250 V / 62.5 mW; 500 mA → 0.500 V / **250 mW ≤ 500 mW rating** | 1 Ω per coil, calibrated per channel; thesis 0.957–1.239 Ω is heritage | SS:131-144; BOM:197; DL:19-21 |
| R220–R295 (48 × 42.7 kΩ 0.1 %) | Six resistors per LTC1563-2 | M16:307 gives `R = 10 kΩ × 256/60 = 42.67 kΩ`; invert `fc(kHz) = 2560/R(kΩ) = 2560/42.7 = 59.95 kHz` (−0.08 %, i.e. about −42 Hz as BOM:435 says) | 60 kHz 4th-order Butterworth, one resistor/channel (decision #19) | M16:305-310; BOM:435; DL:32 |
| C212/C220/…/C268 (8× TDK CAA572, 100 µF) | DC-blocking coupling capacitor | Decision #8 locks 100 µF; BOM:371-391 records TDK ESR 2.2 mΩ, ESL 2.163 nH and the unqualified ripple/thermal checks. No arithmetic in repo. | 100 µF series coupling (value from decision, **stated not derived**; part qualification open) | DL:21, DL:24; BOM:347-391; SS:146-168 |
| R380/R381 and R382/R383 (4 × 10 kΩ) | Two equal dividers (BIAS_DIV and VMID) | `15 × 10/(10+10) = 7.5 V` | 7.5 V mid-rail for bipolar coil current | SS:146-168, SS:158-160 |
| R360/R362/…/R374 (8 × 10 kΩ) and R620/R630/…/R690 (8 × 10 kΩ) | Error-amp feedback and command input | "10 kΩ" for both is captured in BOM:437-438 and SS:149; no gain arithmetic is claimed. | Unity-ish error-loop network; **stated, not derived** | BOM:437-438; SS:146-168 |
| R623/R633/…/R693 (8 × 330 kΩ) with C622/C632/…/C692 (8 × 150 pF) | Lead compensation | BOM:439-440: value open at requirements, 330 kΩ / 150 pF captured as prototype starting points; tune at bench for ≥45° PM at 34 kHz. | Prototype lead network; **stated, not derived** | BOM:439-440; DRV:59; SS:163-165 |
| R361/R363/…/R375 (8 × 15 kΩ) | Driver input resistor | No repo statement or derivation for 15 kΩ; SS:149 and BOM:437 show 10 kΩ in this position. | **UNDOCUMENTED** (§5, §6.3) | CR:361-375 netlist context |
| R621/R631/…/R691 (8 × 1.40 kΩ), R622/R632/…/R692 (8 × 10 MΩ) | Vmid bias and wide feedback | No recorded equation or target | **UNDOCUMENTED** (§5) | netlist only |
| R200 20 kΩ + R201–R208 8 × 10 kΩ | Current-sense summer | `−Rf/Rin = −20 kΩ/10 kΩ = −2.000` per input; locked scale is **2.0103** → **−0.51 % low** (§6.1) | Scale 2.0103 from `software/anser-matlab-ref/fSysSetup.m`; captured network gives 2.000 | SS:187-205; BOM:444; DRV:32-36, DRV:64 |
| R400–R473 (32 × 10 kΩ 0.1 %) | Difference-amp networks across R_store | `Rf/Rin = 10 kΩ/10 kΩ = 1.000` per leg; 4 resistors/channel × 8 channels | Unity difference amp; matched 0.1 % for CMRR | BOM:443; SS:146-168 |
| R600–R607 (8 × 10.7 kΩ 1 %) | LMH6321 `CL` programming | No formula transcribed in repo; BOM:447 states "about 280 mA nominal peak at 15 V" and names TI LMH6321 §§6.7, 6.9 | ≈280 mA clamp — **cited to datasheet section**, not reproduced here | BOM:447; REF-08 LMH6321 (MAN:102-111) |
| R710 52.3 kΩ 0.1 % / R711 10 kΩ 0.1 %, C710 100 nF | TRIP_REF divider and bypass | `3.3 × 10/(52.3+10) = 0.5297 V` ≈ 0.53 V | 0.53 V comparator reference — arithmetic closes (§6.2) | SS:199-203; BOM:445; PT2:486-497 |
| R720–R735 (8 × 10 kΩ / 8 × 100 kΩ) | Comparator `IN−` networks | Input node = `(Vsense/10 k + 3.3/100 k)/(1/10 k + 1/100 k) = (10Vsense + 3.3)/11`; setting this to 0.5297 V gives `Vsense = 0.2527 V` → **252.7 mA at 1 Ω**, matching the driver-sheet "~253 mA" note (§6.2) | ≈253 mA positive-peak trip | SS:199-203; BOM:445; PT2:491-493 |
| R712 4.7 kΩ | Open-drain fault bus pull-up | 3.3 V pull-up; value stated, no derivation | Fault-bus idle high | SS:203; CR:643 |

### 2.6 Receiver — gain, coupling and ADC interface

INA163 gain is `G = 1 + 6000/RG` (two-stage instrumentation-amp equation for
this part); the repo states the target and the resistor but not the equation.

| Served part | Refs (value) | Formula and arithmetic | Designed quantity | Source |
|---|---|---|---|---|
| INA163 U104/U106/U107 | R105, R544, R564 — 176 Ω each | `1 + 6000/176 = 35.091` | Gain 35 (decision #17); +0.26 % on the nominal | SS:242, SS:254; FE:19-23, FE:99-100; DL:30; REF-08 INA163 (MAN:102-111) |
| INA163 input coupling | C113/C114, C540/C541, C560/C561 — 10 µF per leg | `Xc(20 kHz) = 1/(2π·20k·10µ) = 0.796 Ω`, vs 8.6 Ω coil — SS:251 states 0.8 Ω | AC coupling, negligible at 20 kHz | SS:249-253; BOM:521; DL:30 |
| INA163 bias return | R103/R104, R542/R543, R562/R563 — 10 kΩ 0.1 % | `12 µA × 10 kΩ = 0.12 V` DC offset (SS:250) | Bias path for the floating coil | SS:249-250; BOM:522; FE:104-109 |
| INA163 input protection | R101/R102, R540/R541, R560/R561 — 100 Ω per leg (Tier 3) | Series limit with the Schottky clamps; no value arithmetic | ≤73 pF coil budget | SS:252-253; BOM:520 |
| ADA4940-2 Ch0 (U105 A) | R110/R111/R112/R113 — 1 kΩ | `1 k/1 k = 1.000` | Ch0 pseudo-differential unity stage (current-sum channel) | BOM:444-445; SS:262-269 |
| ADA4940-2 Ch1–Ch3 | R120/R121, R548/R549, R568/R569 — 499 Ω; R122/R123, R550/R551, R570/R571 — 1 kΩ | `1000/499 = 2.004` | Nominal 2× FDA stage, +0.20 %; total chain ≈35.09 × 2.004 = 70.3 | FE:19-23, FE:87-100; BOM:525; DL:30 |
| AD7768-4 input RC (4 channels) | R114/R115, R124/R125, R552/R553, R572/R573 — 20 Ω; C120/C121, C125/C126, C544/C545, C564/C565 — 470 pF; C122, C127, C546, C566 — 100 pF | No recomputation in repo: decision #18 locks AN-1384/eval start values `RIN = 20 Ω`, `C1 = C2 = 470 pF`, `C3 = 100 pF`, bench-tunable | ADC charge-reservoir network; **stated, not derived** | DL:31; ADCIC:14, ADCIC:24; BOM:527-529; REF-07 AD7768-4 Rev D (MAN:91-100) |
| ADC reference | R186 10 Ω (renamed from R184 in `8d39a99`); C101 10 µF + C102 100 nF | R186 sits between the OPA192 buffer (U103 OUT/IN-) and ADC_REF, with D534 clamp; PT2:293-301 discusses clamp current. 10 Ω is provisional (BOM:530) | 4.096 V reference distribution | SS:258; BOM:530; PT2:274-301 |
| AD7768 internal bypass | C103 10 µF (`Net-(U101-DREGCAP)`), C104/C105 1 µF (`Net-(U101-REGCAPA)`/`Net-(U101-REGCAPB)`), C106 100 nF (VCM), C131 100 nF (`Net-(U102-VOUT)`) | Values only in the netlist/component reference; no datasheet section named. Net names renamed in `8d39a99` (were `/receiver/DREGCAP`, `/receiver/REGCAPA/B`, `/receiver/REF_RAW`) | **UNDOCUMENTED** (§5) | CR:3442; netlist |
| ADC MCLK | R100 33 Ω (Tier 3) | Series source termination from the 32.768 MHz XO; no arithmetic | Clock integrity | SS:259-260; BOM:532 |
| USB VBUS sense | R158 4.7 kΩ / R159 10 kΩ | `5 × 10/(4.7+10) = 3.401 V` at CBUS2; no documented threshold to compare against | VBUS detect divider; **stated, not derived** | IO:175-186; BOM:467 |

---

## 3. Tier 2 — decoupling and bulk (149)

These are justified **by class**, not per-value arithmetic. No individual
"why 100 nF at this particular pin" derivation exists; that is a property of
the class, and is recorded as such.

| Group | Count | Grouping rule and justification | Source |
|---|---:|---|---|
| 100 nF IC supply bypass (0603, X7R implied) | 115 | One 100 nF from each IC supply pin to GND; conventional local decoupling. PT2:177 names it "layout practice" for U147 VIN; BOM:448 says driver bypass values follow datasheet recommendations; BOM:469 and BOM:531 state the FPGA/receiver rail bypass values with bench verification still open. Includes the 100 nF/50 V U147 input parts (C802, C803) and the 100 nF/25 V U7 AVIN cap (C812). | PT2:177; BOM:448, BOM:469, BOM:531 |
| Regulator input/output bulk (10 µF, 22 µF, 47 µF, 4.7 µF, 1 µF and the two electrolytics) | 34 | Datasheet-recommended input/output capacitance per rail: U147 ≥2×10 µF VIN (PT2:176), 3×22 µF COUT with COUT(min) ≈28 µF effective (PT2:181), 68–100 µF electrolytic to damp cable resonance (PT2:178); TPS62130A 10 µF PVIN / 22 µF COUT (PT2:217-220); TPS7A4701 ≥10 µF, 47 µF ceramic "highly recommended" (PT2:256), 2.2 µF input (PT2:251); FPGA rail bulk C170–C172 (BOM:469); VMID reservoir C282/BOM:199 and its 100 nF bypass C283 (SS:158-160). | PT2:176-181, PT2:217-220, PT2:251-256; BOM:199, BOM:469; SS:158-160; REF-08/REF-14 (MAN:102-111, MAN:166-171) |

Note: the 47 µF and 10 µF regulator caps are counted here, not in Tier 1,
because the repo cites a datasheet *minimum/recommendation* rather than a
calculated value. C189/C815 (`NR`) and C818/C820 (damper leg) are in Tier 1
because they participate in a named setting function.

---

## 4. Tier 3 — pulls, links, bleeds and simple signal coupling (69)

| Group | Refs / count | Justification and constraint | Source |
|---|---|---|---|
| PG pull-ups (100 kΩ) | R805, R192, R195 (3) | Open-collector PG needs a pull-up. PT2:186, PT2:226: datasheet asks 10–100 kΩ, ≤16 V; R805/R192/R195 pull to `+6V` so TPS62130 EN stays ≤ VIN+0.3 V. | PT2:186, PT2:226; REF-14 (MAN:166) |
| STOP pull-downs (100 kΩ) | R754 on `PICO_STOP_REQ_N`, R753 on `PICO_STOP_N` (2) | R754 holds the FPGA-side request low while the FPGA is unconfigured (SS:224). R753 was added so the arm stays stopped when +3.3 V is lost (commit `7e60030`, CR:150). Neither value is derived; the *constraint* is fail-safe idle-low. | SS:207-224; CR:150, CR:429; contract ICD `contract/icd/pico_link.md` |
| Digital/ADC config pulls (4.7 kΩ / 10 kΩ) | R140–R144, R148, R149, R162–R166, R180, R181 (14) | QSPI CS/PUDC_B/INIT_B/DONE/PROGRAM_B/D2/D3, DAC/ADC chip-select and control pulls, ADC SPI_STRAP and DAISY_IN. BOM:470 records QSPI pulls and mode straps; values stated, not derived. | BOM:464-471; CR:4538-4559; DL:31 |
| 0 Ω configuration links | R150–R157, R790 (9) | XADC unused inputs to GND, CFGBVS/MODE0/1/2 straps and the QSPI clock link. BOM:470 calls out the 0 Ω QSPI clock link; straps are captured, not derived. | BOM:470; CR:4699-4705; PT2:402 |
| DAC SPI series termination (33 Ω) | R145, R146, R147 (3) | 33 Ω at the FPGA pin on CS/SCLK/SDI; BOM:468, SS:347. Value stated, to be checked after routing (no source-impedance calculation in repo). | BOM:468; SS:347; M16 §4.5 |
| MCLK series (33 Ω) | R100 (1) | SS:259: 32.768 MHz XO → 33 Ω → ADC MCLK. Value stated, not derived. | SS:259-260; BOM:532 |
| USB D+/D− series and load (27 Ω, 47 pF) | R160, R161, C173, C174 (4) | IO:182 and BOM:467 record the 27 Ω series / 47 pF load pair; no FT231X section or signal-integrity calculation is named in the repo. | IO:175-186; BOM:467 |
| USB CC pulls (5.1 kΩ) | R182, R183 (2) | IO:186: present to GND on CC1/CC2; **the repo explicitly says no attach-detection function is stated**. Value stated, not derived. | IO:186; BOM:467 |
| FG input series protection (100 Ω) | R101, R102, R540, R541, R560, R561 (6) | Series resistance with the Schottky clamps; SS:252-253 and BOM:520 require the protection capacitance to fit the 73 pF coil budget. Value stated, not derived. | SS:249-253; BOM:520 |
| DAC command / sense AC coupling (1 µF, 100 nF) | C620/C621 … C690/C691 (16) | SS:161-168 requires the DAC command to be AC-coupled; the sense path is AC-coupled to the difference amp. Values are captured only. **UNDOCUMENTED** (§5). | SS:146-168; netlist |
| Rearm switch pulls and debounce | R750 10 kΩ, R751 10 kΩ, R712 4.7 kΩ (3, cited); R752 1 kΩ + C755 100 nF (2, undocumented) | BOM:242-246: the 10 kΩ rearm pull-up gives ≈330 µA when pressed (`15 V / 10 kΩ ≈ 330 µA` at the switch node). R752/C755 debounce has no time-constant statement. | BOM:240-246; CR:289-295 |
| Reverse-polarity gate bias | R770 10 kΩ (1) with C770 1 µF/50 V (1, undocumented) | BOM:424: `(15 V − 12 V)/10 kΩ ≈ 0.3 mA` into the 12 V zener, specified at 50 µA. C770 has no recorded rationale. | BOM:414-424 |
| Chassis bleed (1 MΩ ∥ 1 nF/50 V X7R) | R185, C191 (2) | Bond `/connectors/CHASSIS` to GND through a 1 MΩ ∥ 1 nF RC; the intent is recorded in commit `d56e973` ("bond CHASSIS to GND through 1M // 1nF RC bleed") and CR:208, but no value derivation or decision document exists. | commit `d56e973`; CR:208; `docs/phase2/brd01_wiring_manifest.md:1242` |

---

## 5. `UNDOCUMENTED` register — the actionable output

All 53 entries, grouped; every undocumented ref appears exactly once. "No
recorded justification was found" means the named datasheet section, bench
measurement or decision below would settle it.

| Refs | Value | What it serves | What would settle it |
|---|---|---|---|
| C103, C104, C105, C106, C131 (5) | 10 µF, 1 µF, 1 µF, 100 nF, 100 nF | AD7768-4 DREGCAP, REGCAPA/B, VCM, REF_RAW pins | AD7768-4 Rev D datasheet (REF-07; MAN:91-100), pin function / recommended bypass-capacitance section; confirm the value against the released schematic before ordering. |
| C203 (1) | 150 nF | DAC80508 internal 2.5 V REF bypass | DAC80508 datasheet (REF-08; MAN:102-111), reference/voltage-output bypass section. |
| R2, R4 (2) | 7.5 kΩ, 750 Ω | LT3093 / LT3045-1 `ILIM` | LT3093 and LT3045-1 datasheets (REF-08), current-limit programming equation; compute the intended limit and compare with the ±12VA load budget (BOM:153-175). |
| C3, C6 (2) | 4.7 µF | LT3093 / LT3045-1 SET-pin bypass | Same datasheets, SET-pin noise-bypass recommendation. |
| R361, R363, R365, R367, R369, R371, R373, R375 (8) | 15 kΩ | OPA192 error-amp output → LMH6321 `VIN` | Reconcile with SS:149 / BOM:437, which show 10 kΩ in this position; then take the driver owner's loop-gain derivation or a bench phase-margin measurement (DRV:59). |
| R621, R631, R641, R651, R661, R671, R681, R691 (8) | 1.40 kΩ | Vmid bias into the OPA192 `IN+` summing node | Driver owner: derive the intended command bias level and input impedance from the 7.5 V mid-rail and the 10 kΩ command resistor; verify with a DC operating-point measurement. |
| R622, R632, R642, R652, R662, R672, R682, R692 (8) | 10 MΩ | Wide feedback around each error amp | Driver owner: state the loop topology (integrator/lead) and the intended pole/zero; the 330 kΩ/150 pF lead pair is documented, the 10 MΩ path is not. |
| C620, C621, C630, C631, C640, C641, C650, C651, C660, C661, C670, C671, C680, C681, C690, C691 (16) | 1 µF (command), 100 nF (sense) | DAC command and current-sense AC coupling per channel | Driver owner: state the intended high-pass corner for the 20–34 kHz tones and the DC-block requirement; derive C from that corner or record the bench measurement. |
| R752, C755 (2) | 1 kΩ, 100 nF | SW750 rearm switch debounce / Schmitt input | Rearm owner: state the required debounce time (`τ = R·C` = 100 µs as captured) and switch bounce limit, or measure bounce on the assembled board. |
| C770 (1) | 1 µF / 50 V | Reverse-polarity zener/MOSFET gate node bypass | Power owner: state the transient-immunity requirement or take a gate-waveform measurement during input reversal and inrush. |

**Counts by category:** AD7768 internal bypass 5; DAC REF bypass 1; LT
current-limit/SET 4; driver loop/compensation 24; driver signal coupling 16;
rearm debounce 2; reverse-polarity bypass 1 → **53 total**.

---

## 6. Suspicious section — arithmetic checks that matter

### 6.1 Current-sense summer gain misses the locked scale

`R200 = 20 kΩ`, `R201–R208 = 10 kΩ` give `−Rf/Rin = −2.000`. The locked
`I_summer_scale` is **2.0103** (DRV:32-36, DRV:64; SS:142-144; BOM:444), so the
captured network is **0.512 % low**. BOM:444 says "nominal scale −2.000 from
each input; verify Ch0 gain and phase on the bench" — the 2.0103 figure comes
from `software/anser-matlab-ref/fSysSetup.m`, which the repo names as its
source but does not embed. This is a real, checkable mismatch: either 2.0103 is
a calibration constant (κ absorbs it) or R200 should be ~20.103 kΩ. **No
resistor change is made here.** Resolution: decide whether the scale is a
hardware ratio or a software coefficient, then reconcile the two documents.

### 6.2 `TRIP_REF` is not actually unreconciled — the missing link is the comparator divider

PT2:486-497 and BOM:445 call three numbers "unreconciled": 0.53 V at
`TRIP_REF`, "~253 mA at 3.3 V" on the driver sheet, and "~280 mA nominal LMH6321
clamp". Taking the captured networks together:

- `TRIP_REF = 3.3 × 10/(52.3 + 10) = 0.5297 V` — matches 0.53 V.
- Each comparator `IN−` node is weighted by **10 kΩ from the sense output** and
  **100 kΩ to +3.3 V**: `V− = (10·Vsense + 3.3)/11`.
- Trip when `V− = V+ = 0.5297 V`: `Vsense = (0.5297×11 − 3.3)/10 = 0.2527 V`.
- With the 1 Ω shunts R20–R27, that is **252.7 mA ≈ the "~253 mA" note**.

So the first two numbers agree to 0.1 %; the 280 mA figure is the LMH6321 `CL`
clamp (R600–R607, BOM:447), a different mechanism that should sit *above* the
comparator trip — and does (253 < 280 mA, 9.7 % headroom). The finding is that
PT2:486-497 records an open question that the captured schematic already
answers; the remaining bench item is clamp tolerance, not divider arithmetic.
PT2:494-497 forbids resistor changes before measurement; this document makes
no changes.

### 6.3 Other checks run

| Check | Result |
|---|---|
| U144 FB: 0.8×(1+49.9/200) | 0.99960 V vs 1.000 V — **pass** (−0.04 %), inside 0.982–1.018 V |
| U145 FB: 0.8×(1+249/200) | 1.796 V vs 1.80 V — **pass** (−0.22 %), inside 1.764–1.829 V |
| U7 FB: 0.8×(1+619/200) | 3.276 V vs 3.3 V — **pass** (−0.73 %), inside 3.217–3.335 V and VCCO ±5 % |
| U147 FB: 1×(1+49.9/10) | 5.99 V vs 6.0 V — **pass** (−0.17 %), inside 5.92–6.06 V |
| U147 RT: 13.46/(13.0+0.44) | 1.0015 MHz vs 1.000 MHz stated — **pass** (+0.15 %); sync 1.024 MHz is +2.25 % above free-run (PT2:192-207 says bench-confirm lock) |
| U147 UVLO: 1.263/0.10555 and 0.91/0.10555 | 11.97 V on / 8.62 V off — **pass**, matches PT2:183, PT2:340 |
| Soft start: 3.3 nF × 1.25 V / 2.5 µA | 1.65 ms — **pass**, all three rails |
| FL dampers: √(1 µH/2.2 µF) | 0.6742 Ω vs 0.68 Ω — **pass** (+0.86 %) |
| LTC1563-2: 2560/42.7 | 59.95 kHz vs 60 kHz — **pass** (−0.08 %) across all 48 resistors |
| INA163: 1+6000/176 | 35.09 vs 35 — **pass** (+0.26 %), R105/R544/R564 |
| FDA: 1000/499 | 2.004 vs 2 — **pass** (+0.20 %), Ch1–Ch3; Ch0 1 kΩ/1 kΩ = 1.000 |
| Sense difference amps: 10 kΩ/10 kΩ | 1.000, 32 resistors — **pass** |
| INA coupling: 1/(2π·20k·10µ) | 0.796 Ω vs 0.8 Ω in SS:251 — **pass** |
| INA bias: 12 µA × 10 kΩ | 0.12 V vs SS:250 — **pass** |
| Vmid: 15 × 10/(10+10) | 7.5 V — **pass** |
| R770: (15−12)/10 kΩ | 0.3 mA vs BOM:424 — **pass** |
| R20–R27 dissipation at 500 mA | 0.25 W vs 0.5 W rating — **pass** |
| USB VBUS divider: 5×10/(4.7+10) | 3.401 V, but **no documented threshold** — inconclusive, not a failure |
| Current summer: 20 kΩ/10 kΩ | 2.000 vs 2.0103 — **FAIL** (§6.1) |
| TRIP_REF / trip-current | 0.5297 V → 252.7 mA — **pass**, contrary to "unreconciled" (§6.2) |

### 6.4 Documentation mismatches (not value errors)

- The 15 kΩ driver input resistors (R361 etc.) conflict with the 10 kΩ shown
  in SS:149 and BOM:437 — see §5.
- The U144 FSW strap and the STOP-gate polarity are already documented defects
  with fixes in CR:141-165; they are not passive values and are out of scope.
- Ch3 front end is DNP by decision (CR:217, BOM:534); its values are captured
  but not ordered. That is a population decision, not a justification gap.

### 6.5 Stale source caveat

PTR:87-94 is the v1 power tree and still lists `+15V_DRV`, `+5V`, K1/K2, U3 and
U1 (CR:208). Its ±12VA SET statements (PTR:93-94) are used here only because
PT2 §2 explicitly leaves the MGJ2/LT3045/LT3093 ±12VA chain unchanged
(PT2:33, PT2:471). All other power values in this register cite PT2.

---

## 7. Gates

| Gate | Result |
|---|---|
| Netlist passive count | 501 (276 R + 225 C), from `/tmp/vj/net.xml` generated at this checkout |
| Gate 1 — exactly one tier per passive | Tier 1 = 283, Tier 2 = 149, Tier 3 = 69; sum 501; netlist-minus-assigned = ∅, assigned-minus-netlist = ∅ |
| Gate 2 — evidence classes sum to total | 159 + 239 + 50 + 53 = 501 |
| Gate 3 — every cited repo path resolves | Checked with a script over all `path:line` citations in this document |
| Gate 4 — checks | `tools/check_references.py`, `tools/contract_ci.py check`, `tools/check_doc_paths.py` results recorded in the handoff report |
| Gate 5 — diff scope | Only this file added; no `.kicad_sch`, `contract/` or existing document modified; generator kept in `/tmp/vj/` and not committed |

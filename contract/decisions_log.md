# Phase 2 — Locked decisions log

**Canonical location:** `contract/` · **Version:** 1.1.0 · **Tag:** `contract-v1.1.0` (pending review)
**Change process:** `contract/README.md`.

**Status:** decisions locked through 2026-11-25. **M16 selected 2026-10-27.**
D1/D3/D4/FE-4 and the M16 DAC/filter are locked; the remaining rows state their
own status. Each row links the decision to its justification and source.
Hardware-dependent items are listed separately as **verification gates** (tests,
not open design choices). Order-time items are under **procurement checks**.
#30 (arm-only STOP) and #31 (power tree v2) are recorded in the 1.1.0 contract PR
on `docs/spine-consistency`; the tag and arm-repo sync are pending. Rows superseded
in part keep their original text as history. Decision number 29 was withdrawn and
no #29 row exists.

| # | Date | Decision | Justification | Status | Source |
|---|---|---|---|---|---|
| 1 | 2026-10-26 | **Tone plan:** 20, 22, 24, 26, 28, 30, 32, 34 kHz (2 kHz spacing); AD7768-4 256 kSPS; N=512; rectangular + integer-J primary, Hamming fallback; N=1024 Hamming fallback | AD7768 max 256 kSPS; 2 ms acquisition restores 7.87 ms demod/solve budget; 2 kHz gives 4-bin spacing; 1 kHz would need N=1024 (4 ms) for Hamming; rectangular integer-J gives zero tone-to-tone leakage | LOCKED | `docs/phase2/tone_plan.md` |
| 2 | 2026-10-27 | **Volume policy:** 100 mm minimum, 150 mm target, 200 mm stretch; final volume = largest cube passing SC-01d | Anser 250 mm is heritage; Phase 1 #3 is 100 mm; first-pass 150/B is feasible, 200/B corners are much weaker; final by measured jitter/CRLB | LOCKED policy; final volume by test | `contract/system_contract.md` |
| 3 | 2026-10-27 | **ICNIRP surface B:** 27 µT at any accessible point, with a non-metal guard at the ~57 mm contour; guard is an access barrier, not an EMF shield | Phase 1 #20; field near the board exceeds 27 µT; non-metal guard blocks access without distorting the field; 150/B leaves 28.6 mm | LOCKED | `system_contract.md` SC-04a/b |
| 4 | 2026-10-27 | **Pen coil B air-core**, no ferrite; A/E alternates; C air out | B: 1.59 mm accuracy, 5.3 pT at 20 kHz, 3.1 pT at 34 kHz with INA163; passes 150/B ~5× and 200/B ~2×; C is 2.48 mm/18.6 pT; ferrite adds nonlinearity | LOCKED | `docs/phase2/pen_link_budget.md` |
| 5 | 2026-10-27 | **ADC/FE:** AD7768-4 locked; FE-4 designed to ±4.096 V differential, VCM, external RC/charge reservoirs; INA163 + ADA4940-2 locked (ADA4896-2 alternate) | AD7768-4 24-bit simultaneous, 256 kSPS, DCLK/DOUT, SYNC/START/DRDY; INA163 noise meets the 150/200 pT gate; ADA4940-2 is ADI's recommended fast-mode driver | LOCKED | `frontend_requirements.md` |
| 6 | 2026-10-27 | **Current-sense A+:** per-coil \(R_{store}\) + analog summer → ADC Ch0, plus individual peak/overcurrent comparators; no mux, no extra ADC | One coil per tone (FDM), so the summed current spectrum contains each coil's current; Helmholtz/7×7/κ/\(I_{out}\) calibration works with one current channel; A+ adds fault detection without phase penalty | LOCKED | `driver_power_requirements.md` §4 |
| 7 | 2026-10-27 | **Power C1 + medical-grade:** one external medical-grade 15 V/60 W adapter + on-board DC-DC/LDO tree; +15 V, −15 V, +5 V, +3.3 V; no on-board mains stage; FPGA core via its board regulator | No from-scratch 110 V design; adapter is the mains safety/EMC boundary; medical-grade for handheld pen/leakage; one wall adapter | LOCKED | `driver_power_requirements.md` §3 |
| 8 | 2026-10-27 | **Driver A:** LMH6321-class, thesis §4.3 architecture, **new board not a clone**; single +15 V AC-coupled, 100 µF, 250 mA nominal / 500 mA max, ~180 cm²; parts open | Thesis optimised design vs vendor Rev A discrete class-AB 30 W/3 kg; lower heat/size; new board allows part changes with deviation | LOCKED architecture | `driver_power_requirements.md` §2 |
| 9 | 2026-10-27 | **DAC architecture:** FPGA DDS + external 16-bit DAC, 8 ch; XADC 12-bit not used; part/update rate fixed by the M16 decision (#19) | 16-bit for the 8-tone/CRLB; the FPGA has no 16-bit DAC; XADC unsuitable; the M16 part/update-rate trade is in #19 | LOCKED architecture; part #19 | `driver_power_requirements.md` §5 |
| 10 | 2026-10-27 | **Enclosure + E-stop:** one box with internal shield partition; hardware **NC mushroom E-stop** in driver enable chain, independent of FPGA; opto status; software watchdog; follower stop ≤100 ms | One-box simplicity; partition isolates on-board switchers/high-current driver; hardware E-stop is fail-safe and not dependent on FPGA | LOCKED one box; **E-stop parts/chain superseded by #30** (no panel stop on BRD-01; ≤100 ms = arm motion) | `driver_power_requirements.md` §6; `docs/phase2/estop_scope_change.md` §D |
| 11 | 2026-10-27 | **Current/thermal:** programmable current setpoint 150–500 mA; prototype at **150 mA first**; 250 mA fallback with +5 V driver rail/series cap/heatsink as needed; 500 mA max needs higher rail | 8×250 mA linear from +15 V ≈12–16 W in LMH6321; series cap alone at +15 V does not reduce it; 150 mA gives 5.3 pT vs 6.6 pT required for 200/B (1.25×) and 15.6 pT for 150/B (3×); no PCB re-spin for current change | LOCKED | `driver_power_requirements.md` §6 |
| 12 | 2026-10-27 | **DRV-2 requirements gate accepted**; BOM/schematic pass deferred | All block-level DRV-2 decisions are locked; exact DAC/adapter/LMH6321 lifecycle/passives are BOM/schematic items; tests at prototype | ACCEPTED | `driver_power_requirements.md` §7 |
| 13 | 2026-10-27 | **Calibration method:** Helmholtz \(A_{sens}(f)\), 7×7 grid κ/zOffset, stored/measured \(I_{out}\); one current-sense channel; no extra ADC | FDM separates the 8 coil currents in the summed channel; Helmholtz/7×7/κ absorbs current/sensor scaling; new FPGA can use live per-tone \(I_{out}\) | LOCKED method | `calibration_tooling.md` |
| 14 | 2026-10-27 | **D1 volume placement = B:** 150 mm cube, bottom face 85.6 mm, top 235.6 mm; 100 mm minimum cube at 85.6–185.6; 200 mm stretch only by SC-01d | 45% ICNIRP margin at 250 mA; bottom aligns with the 85.6 mm calibration plane; 95th/max conditioning 69.5/73.1, only modestly worse than 100/B; the 50–150 mm cube fails ICNIRP at 250 mA | **LOCKED**; SC-01d may demote to 100 mm, not move the bottom without a deviation | `system_contract.md` D1 |
| 15 | 2026-10-27 | **D3 ADC channel map = A:** Ch0 current-sense, Ch1 pen 1, Ch2 pen 2, Ch3 reference sensor; Ch2 wired but enabled when pen 2 is built | Phase 1 #1–2 supports 1–2 pens; keeps the reference channel; no spare but the 4-channel ADC is fully used; first build is 4-channel capable | LOCKED | `system_contract.md` D3 |
| 16 | 2026-10-27 | **D4 precision volume:** 150 mm tracking volume with a **100 mm high-precision core** (x,y ±50 mm, z 110.6–210.6 mm); 200 mm only if SC-01d passes; 100 mm minimum | Phase 1 #3–6; 100 mm core needs ≤58 pT, 150 mm shell ≤26 pT, 200 mm ≤11 pT; the core carries the tremor/jitter target, the shell the ≤2 mm gross tracking | LOCKED | `system_contract.md` D4 |
| 17 | 2026-10-27 | **FE-4 amplifier chain = INA163 + ADA4940-2**, gain 35× + 2×, AC-coupled coil input, ±12 V analog for INA163, +5 V for ADA4940; ADA4896-2 alternate | INA163 1.1 nV/√Hz meets 150/200 pT; ADA4940-2 is the AD7768 fast-mode recommended fully differential driver; E301 AD620/AD627 is 100 mm fallback only | LOCKED | `frontend_requirements.md` |
| 18 | 2026-10-27 | **ADC-5 interface:** 4 channels, 4 DOUT lanes, DCLK 8.192 MHz, 32-bit frames, 2×8/custom header; RC start values \(R_{IN}=20\ \Omega\), \(C_1=C_2=470\ pF\), \(C_3=100\ pF\); ADR434 shared with a buffer | 4 ch × 32 bit × 256 kSPS = 32.768 Mbit/s; 4 lanes → 8.192 MHz; AN-1384/eval values span 10–82 Ω and 470–680 pF, so start mid-range and tune at the bench; 2×6 Pmod is insufficient | **LOCKED (2026-11-02)** — RC values bench-tune within the stated range | `adc_interface_closure.md`; `contract/icd/adc_fpga.md` |
| 19 | 2026-10-27 | **DAC/filter = M16 (SELECTED):** 1× DAC80508 (16-bit, 8 ch, 200 kSPS, SPI, internal 2.5 V ref) + 8× LTC1563-2 (4th-order Butterworth, 60 kHz, one resistor/channel). DAC update **199.805 kSPS** = 32.768 MHz ÷164; SPI **49.152 MHz**, 8×24-bit data + 24-bit TRIGGER = **216 bits = 4.394 µs**; the LDAC is a **software trigger (TRIGGER 0x05 bit 4)** — the part has no LDAC pin. | Filter AC: −35.3 dB at 165.8 kHz, −0.05 dB/34 kHz. Summer 8-tone EVM −67.1 dBc (7.1 dB margin at −110 dB THD); DAC crosstalk/INL ≤−85 dBc; OPA2192/AD7768 not the limit. Cost ~$73 less than the 8× AD5541A board (DAC80508 $42.52 CAD at Digi-Key; earlier $5 estimate was wrong); one SPI, 13 fewer FPGA pins. SPICE report `simulations/m16/FINAL_REPORT.md`. | **LOCKED (selected 2026-10-27)** | `simulations/m16/FINAL_REPORT.md`; BOM_SYSTEM-01 |
| 20 | 2026-10-27 | **Power parts = ME60A1503F01** 15 V/60 W medical adapter; **OKI-78SR-5/1.5** +5 V; **RV-1515D** ±15 V isolated; **TPS7A4701/TPS7A33** LDOs to ±12 V analog; **TPS7A20** +3.3 V | 60 W covers 150 mA (≈18 W driver) + FPGA/analog; isolated analog module keeps driver switching off the FE; LDOs clean the rails; no on-board mains | parts superseded by #31 (adapter and one-board intent stand) | `driver_power_requirements.md` §3; BOM |
| 21 | 2026-10-27 | **FPGA/clock interface (M16):** 32.768 MHz XO (Citizen CSX750FBC32.768M); **PS-less Artix-7 XC7A35T on BRD-01 (#26), all signals are board nets — no 2×20 IDC**; 32.768 MHz → PLL ×3 → ÷2 = **49.152 MHz SPI**; ÷164 = **199.805 kSPS DAC**; ÷128 = 256 kSPS ADC. ADC, DAC, E-stop, watchdog are zone A/B/C nets; 13 pins spare. | Exact integer tones: 2 kHz × k = 32.768 MHz × k/16384, k=10…17; one clock for DDS and ADC removes leakage; M16 DAC at 200 kSPS; pinout in `system_schematic.md` | LOCKED interface (M16); **FPGA = PS-less Artix-7, see #26**; E-stop zone wording superseded by #30 | `system_schematic.md`; `dig6_requirements.md` |
| 22 | 2026-10-27 | **Enclosure/E-stop parts:** one aluminum box with internal shield; Schneider XB4BS8444 or AutomationDirect GCX1131 NC mushroom; fan/filter; no metal within 150 mm of the volume | One-box decision; NC fail-safe; 22 mm panel mount; the guard is non-metal per SC-04b | **LOCKED box/fan/filter; mushroom part no longer on BRD-01 (#30)** | BOM; `docs/phase2/estop_scope_change.md` §D |
| 23 | 2026-10-27 | **DIG-6 requirements accepted:** 32-bit DDS, 4096-entry LUT, 4-channel capture, Goertzel, 8×5 LM/TRF, 8.633 ms pipeline, 115.8 Hz, filter-off latency 8.6 ms | 2.000 ms acquisition + 0.133 ms ADC delay + 0.5 ms demod + 5.0 ms solve + 1.0 ms overhead = 8.633 ms; ≥100 Hz; ≤20 ms off / ≤100 ms on | **LOCKED (2026-11-02)** — bench evidence stays open | `dig6_requirements.md` |
| 24 | 2026-10-27 | **System flow chart, board-level schematic, system BOM Rev A issued** | Phase 2 report §3/§5 and design-review drawing set; procurement gate | DRAFT Rev A | `system_flowchart.md`, `system_schematic.md`, `BOM_SYSTEM-01.xlsx` |
| 25 | 2026-10-28 | **Electronics = one board, BRD-01.** Power entry/E-stop/DC-DC, FPGA + clock, DAC80508 + 8× LTC1563-2 + 8 current loops + current sense, receiver (INA163 + ADA4940-2 + AD7768-4), and the FG/pen connectors are **zones of one 4-layer board**, not separate boards. FG-01 stays a separate passive coil PCB; the pen stays passive. | One board removes the 49.152 MHz SPI cable (0.17 ns hold), the ADC ribbon, and three inter-board connectors; the box partition is replaced by an on-board shield can. | **LOCKED (team, 2026-10-28)**; no E-stop zone (#30) | `system_schematic.md` §1, §6.0 |
| 26 | 2026-10-28 | **FPGA integration = D: PS-less FPGA on BRD-01.** XC7A35T-1FTG256C baseline (33k LC, 1.8 Mb BRAM, 90 DSP, 170 I/O, 1.0 mm FTBGA); XC7A50T-1FTG256C as the same-footprint upgrade. QSPI config flash, USB-UART host link, 3.3 V HR banks. No PS, no DDR3, no Linux; the host PC does UI/log/camera. | DDR3 is a PS requirement, not a pose requirement: the pipeline needs ~10–25 kB of BRAM and 0.6–0.7 GFLOP/s. Dropping the PS removes DDR3, the 6-layer stack, PMIC sequencing and the boot image, and keeps the 49.152 MHz SPI on-board. MCU-only (option E) was evaluated and rejected: an analytic-Jacobian solve fits a 1 GHz M7 at ~1× margin, but the 8.633 ms period is then average-case, not guaranteed. | **LOCKED (2026-10-28)** | `fpga_integration_options.md`; `system_schematic.md` §6.0 |
| 27 | 2026-11-02 | **FG-01 = 8 vendor AnserEMT emitter coils, one per position, no stacking, on two in-house machined plates.** Coil: 25 turns split across two layers, 70 mm outer, 0.5 mm track / 0.25 mm gap, 1.6 mm FR4, L ≈ 79 µH, R ≈ 2.9 Ω (AnserEMT 2017, Table 2). 8 PCBs at the `fSysSetup.m` centres (±93.543/±68.55 mm; coils 2,4,5,7 at 45°). | Matches the locked model (N = 25, 70 mm) — my earlier ~20-turn read counted one layer only. No coil layout work; ~$118 cheaper than one 300 × 300 board; $4 spares. Stacking rejected: L ∝ N² would need >7.5 V swing at 250 mA on the +15 V driver. Gerbers must be re-exported from the DesignSpark `.pcb` (2013 export has no outline layer and 10× drill coordinates). | **LOCKED (2026-11-02)**; contract PR in review — VERSION bumped to 1.1.0 in this PR, tag `contract-v1.1.0` pending | `hardware/fg-01/README.md`; `docs/phase2/design_order.md` FG-01; BOM FG-01 |
| 28 | 2026-11-25 | **Clock tree clarification:** SC-07 corrected to match locked decision #21. One 32.768 MHz XO (CSX750FBC32.768M-UT) drives ADC MCLK through 33 Ω and the FPGA clock input directly; DDS clock = 32.768 MHz; PLL ×3 = 98.304 MHz only feeds ÷2 = 49.152 MHz DAC SPI; DAC update ÷164; ADC ODR ÷128; no discrete buffer. | The previous SC-07 text (“TCXO → FPGA PLL → clk_dds + MCLK_adc”) described a PLL-generated MCLK that does not exist on BRD-01 and a TCXO that is not the selected part. The XO-direct tree preserves the SC-07 invariant: one clock, exact integer divides, integer-J, no DDS/ADC beat. | **LOCKED (clarification, 2026-11-25)** | `system_contract.md` SC-07; `system_schematic.md` §5.1/§6.0; `dig6_requirements.md` §1 |
| 30 | 2026-11-25 | **STOP scope = manipulator only.** No panel mushroom / K1 / K2 / opto status on BRD-01; `+15V_FUSED` feeds the eight LMH6321 unswitched and a STOP never removes the field. `PICO_STOP_N` (`U755.4` → `J123.5`) is the AND of `PICO_STOP_REQ_N` (`U4.P4` + `R754` pull-down) and the arm latch `U753.5 (Q)` on `/power/ARM_Q`; `U753.3 (~Q)` is NC. Power-up/+3.3 V brownout (U751) and `/DRIVER_FAULT_N` (U752) clear the latch and assert STOP; SW750 arms it. STOP is arm motion only, ≤100 ms; field, DDS/DAC and pose continue. A genuine FPGA/ADC/driver fault still stops the DDS (zero-scale + one TRIGGER). | User decision recorded in `estop_scope_change.md` §D; netlist/wiring manifest confirm the Q/~Q pin usage. The last hardware-independent stop path on the board is removed — accepted explicitly: STOP now depends on host link, FPGA, cable and Pico firmware. ICNIRP field sum is unchanged. | **LOCKED (user decision, 2026-11-25); tag/release pending review** — supersedes #10/#21/#22/#25 in part; SC-08 stop scope and three ICDs updated | `docs/phase2/estop_scope_change.md` §§C–D; `docs/phase2/brd01_wiring_manifest.md` §5 items 1–5; `docs/phase2/system_schematic.md` §4.5 |
| 31 | 2026-11-25 | **Power tree = v2 (adopted).** 15 V / 60 W ME60A1503F01 adapter unchanged. U147 TPSM63604 6.0 V buck at 1.024 MHz (= 32.768 MHz / 32), synced to BUCK_SYNC, feeds +6V; U144/U145/U7 TPS62130A give +1V0_FPGA / +1V8_FPGA / +3.3V; U149 TPS7A4701 gives +5V_EXC (DAC80508 + 8x LTC1563-2); U146 TPS7A4701 gives +5VA (AD7768-4 + 2x ADA4940-2); U5 MGJ2D151515SC -> U6 LT3045-1 / U2 LT3093 gives +/-12VA. Removed: OKI-78SR-5 (+5V) and TPS7A2033. Supersedes the part list of #20; #20's adapter and one-board intent stand. | The v1 tree cannot hold 5.0 V from the OKI's 4.8-5.2 V output, puts 50-75 mV switching ripple on the DAC/filter rails, and burns 0.8-1.5 W in U146. The captured BRD-01 schematic already implements v2, so adopting it removes the contract-vs-board conflict. | **LOCKED (user decision, 2026-11-25)** | `power_tree_v2.md`; `contract_change_20_draft.md`; `system_schematic.md` §2; `icd/power.md`; captured BRD-01 schematic |

> Editorial note on #31: the submitted decision text named a BOM revision that
> cannot be verified from tracked files; that revision reference was removed.
> The decision itself (v2 parts adopted, #20's part list superseded) is unchanged.
> BOM reconciliation is tracked separately.

## Verification gates (hardware-dependent; not open design decisions)

These are measured tests. A failure triggers the stated fallback, not a redesign
of the locked interface.

- **SC-01d volume:** measured 95th-percentile CRLB/jitter at 150/B; demote to
  100/B if it fails. 200/B only if it passes.
- **PEN-3/FE-4:** measured \(A_{sens}(f)\), input-referred noise, CMRR; confirm
  \(\sigma_B\le26\) pT at 150/B (≤11 pT at 200/B).
- **ADC-5:** code density, FFT/SINAD/THD, reference noise, 4-lane capture, zero
  dropped frames over 1 hour.
- **DRV-2 / M16:** one-channel constant-current, THD/IMD, 8-tone EVM, loop
  PM/step, LMH6321 crossover, 8-channel thermal soak, arm STOP/overcurrent
  (field and pose continue), EMI with the one-box shield. The SPICE screen is not a
  substitute for the bench.
- **DIG-6:** integer-J leakage, golden demod/solver match, 8.633 ms worst-case
  timing, 1-hour moving run.
- **INT-7:** κ 7×7, 98-point RMS at 85.6/152 mm, tremor 20 dB/3 dB, latency,
  stop ≤100 ms, ICNIRP scan, BOM ≤1000 CAD/pair or documented deviation.

## Procurement checks (order-time, not design)

- Re-quote DAC80508MRTET, LTC1563-2IGN#PBF, LMH6321MR/NOPB, AD7768-4,
  ADR434, INA163, ADA4940-2, ME60A1503F01 and the adopted v2 power parts
  (TPSM63604, TPS62130A, TPS7A4701, MGJ2D151515SC, LT3045-1, LT3093);
  confirm stock and lifecycle. RV-1515D and OKI-78SR-5 are removed by #31.
- LMH6321: TI product page says ACTIVE; distributor stock is thin, so buy
  8 + 2 spares now. Fallback: vendor Rev A discrete stage or a comparable
  high-current buffer with a recorded deviation.
- Confirm XC7A35T-1FTG256C stock, HR (3.3 V) bank coverage and 35T→50T pin compatibility.
  If the HLS solver does not fit the 35T, use the
  XC7A50T in the same FTG256 footprint; the interface is unchanged.
- Exact enclosure, fan, heatsink, and panel connectors are order-time choices.
- No BOM row may ship with a placeholder supplier P/N.

## Closed / follow-up interface items

- **Power tree v1 vs board — CLOSED by #31 (2026-11-25).** The user adopted the
  v2 tree; the earlier contract-vs-board conflict no longer stands. Evidence at
  the time: `hardware/brd-01/kicad/brd-01.kicad_sch` at `ef04f63` contains
  `MGJ2D151515SC` and no `OKI-78SR`, `RV-1515`, `TPS7A20` or `TPS7A4701`
  strings; `hardware/brd-01/kicad/bom-to-cad.md:151` records the user's part
  confirmation (U5 MGJ2D151515SC, U6 LT3045EDD-1#TRPBF, U2 LT3093EMSE#TRPBF);
  `docs/phase2/brd01_component_reference.md:357` lists U5 as MGJ2D151515SC.
  The part list of #20 is superseded by #31; its 15 V/60 W adapter and
  one-board intent stand.
- **Pico `J123.1` — OPEN follow-up.** The ICD still lists pin 1 as `3V3`; the
  committed netlist has `J123.1` as a no-connect
  (`docs/phase2/brd01_wiring_manifest.md` §5 item 6;
  `docs/handoff/brd01_io_handoff.md` §1; `power_tree_v2.md` §7 D4). The pinout
  change is not written into the frozen Rev A ICD by #31's part-list row; align
  it before wiring the follower harness.
- **DAC DDS amplitude — OPEN follow-up.** `icd/dac_fpga.md` §3 item 2 keeps the
  M-variant gain-2 0–5 V default; `power_tree_v2.md` §7 D2 gives a 0.3–4.6 V
  limit on `+5V_EXC`. That limit is not written into the frozen DAC ICD by
  #31's part-list row.

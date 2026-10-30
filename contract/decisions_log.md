# Phase 2 — Locked decisions log

**Canonical location:** `contract/` · **Version:** 1.0.0 · **Tag:** `contract-v1.0.0`
**Change process:** `contract/README.md`.

**Status:** decisions locked through 2026-10-28. **M16 selected 2026-10-27.**
D1/D3/D4/FE-4 and the M16 DAC/filter are locked; the remaining rows state their
own status. Each row links the decision to its justification and source.
Hardware-dependent items are listed separately as **verification gates** (tests,
not open design choices). Order-time items are under **procurement checks**.

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
| 10 | 2026-10-27 | **Enclosure + E-stop:** one box with internal shield partition; hardware **NC mushroom E-stop** in driver enable chain, independent of FPGA; opto status; software watchdog; follower stop ≤100 ms | One-box simplicity; partition isolates on-board switchers/high-current driver; hardware E-stop is fail-safe and not dependent on FPGA | LOCKED | `driver_power_requirements.md` §6 |
| 11 | 2026-10-27 | **Current/thermal:** programmable current setpoint 150–500 mA; prototype at **150 mA first**; 250 mA fallback with +5 V driver rail/series cap/heatsink as needed; 500 mA max needs higher rail | 8×250 mA linear from +15 V ≈12–16 W in LMH6321; series cap alone at +15 V does not reduce it; 150 mA gives 5.3 pT vs 6.6 pT required for 200/B (1.25×) and 15.6 pT for 150/B (3×); no PCB re-spin for current change | LOCKED | `driver_power_requirements.md` §6 |
| 12 | 2026-10-27 | **DRV-2 requirements gate accepted**; BOM/schematic pass deferred | All block-level DRV-2 decisions are locked; exact DAC/adapter/LMH6321 lifecycle/passives are BOM/schematic items; tests at prototype | ACCEPTED | `driver_power_requirements.md` §7 |
| 13 | 2026-10-27 | **Calibration method:** Helmholtz \(A_{sens}(f)\), 7×7 grid κ/zOffset, stored/measured \(I_{out}\); one current-sense channel; no extra ADC | FDM separates the 8 coil currents in the summed channel; Helmholtz/7×7/κ absorbs current/sensor scaling; new FPGA can use live per-tone \(I_{out}\) | LOCKED method | `calibration_tooling.md` |
| 14 | 2026-10-27 | **D1 volume placement = B:** 150 mm cube, bottom face 85.6 mm, top 235.6 mm; 100 mm minimum cube at 85.6–185.6; 200 mm stretch only by SC-01d | 45% ICNIRP margin at 250 mA; bottom aligns with the 85.6 mm calibration plane; 95th/max conditioning 69.5/73.1, only modestly worse than 100/B; the 50–150 mm cube fails ICNIRP at 250 mA | **LOCKED**; SC-01d may demote to 100 mm, not move the bottom without a deviation | `system_contract.md` D1 |
| 15 | 2026-10-27 | **D3 ADC channel map = A:** Ch0 current-sense, Ch1 pen 1, Ch2 pen 2, Ch3 reference sensor; Ch2 wired but enabled when pen 2 is built | Phase 1 #1–2 supports 1–2 pens; keeps the reference channel; no spare but the 4-channel ADC is fully used; first build is 4-channel capable | LOCKED | `system_contract.md` D3 |
| 16 | 2026-10-27 | **D4 precision volume:** 150 mm tracking volume with a **100 mm high-precision core** (x,y ±50 mm, z 110.6–210.6 mm); 200 mm only if SC-01d passes; 100 mm minimum | Phase 1 #3–6; 100 mm core needs ≤58 pT, 150 mm shell ≤26 pT, 200 mm ≤11 pT; the core carries the tremor/jitter target, the shell the ≤2 mm gross tracking | LOCKED | `system_contract.md` D4 |
| 17 | 2026-10-27 | **FE-4 amplifier chain = INA163 + ADA4940-2**, gain 35× + 2×, AC-coupled coil input, ±12 V analog for INA163, +5 V for ADA4940; ADA4896-2 alternate | INA163 1.1 nV/√Hz meets 150/200 pT; ADA4940-2 is the AD7768 fast-mode recommended fully differential driver; E301 AD620/AD627 is 100 mm fallback only | LOCKED | `frontend_requirements.md` |
| 18 | 2026-10-27 | **ADC-5 interface:** 4 channels, 4 DOUT lanes, DCLK 8.192 MHz, 32-bit frames, 2×8/custom header; RC start values \(R_{IN}=20\ \Omega\), \(C_1=C_2=470\ pF\), \(C_3=100\ pF\); ADR434 shared with a buffer | 4 ch × 32 bit × 256 kSPS = 32.768 Mbit/s; 4 lanes → 8.192 MHz; AN-1384/eval values span 10–82 Ω and 470–680 pF, so start mid-range and tune at the bench; 2×6 Pmod is insufficient | PROPOSED — recommended; RC values tune at ADC-5 | `adc_interface_closure.md` |
| 19 | 2026-10-27 | **DAC/filter = M16 (SELECTED):** 1× DAC80508 (16-bit, 8 ch, 200 kSPS, SPI, internal 2.5 V ref) + 8× LTC1563-2 (4th-order Butterworth, 60 kHz, one resistor/channel). DAC update **199.805 kSPS** = 32.768 MHz ÷164; SPI **49.152 MHz**, 8×24-bit data + 24-bit TRIGGER = **216 bits = 4.394 µs**; the LDAC is a **software trigger (TRIGGER 0x05 bit 4)** — the part has no LDAC pin. | Filter AC: −35.3 dB at 165.8 kHz, −0.05 dB/34 kHz. Summer 8-tone EVM −67.1 dBc (7.1 dB margin at −110 dB THD); DAC crosstalk/INL ≤−85 dBc; OPA2192/AD7768 not the limit. Cost ~$73 less than the 8× AD5541A board (DAC80508 $42.52 CAD at Digi-Key; earlier $5 estimate was wrong); one SPI, 13 fewer FPGA pins. SPICE report `simulations/m16/FINAL_REPORT.md`. | **LOCKED (selected 2026-10-27)** | `simulations/m16/FINAL_REPORT.md`; BOM_SYSTEM-01 |
| 20 | 2026-10-27 | **Power parts = ME60A1503F01** 15 V/60 W medical adapter; **OKI-78SR-5/1.5** +5 V; **RV-1515D** ±15 V isolated; **TPS7A4701/TPS7A33** LDOs to ±12 V analog; **TPS7A20** +3.3 V | 60 W covers 150 mA (≈18 W driver) + FPGA/analog; isolated analog module keeps driver switching off the FE; LDOs clean the rails; no on-board mains | PROPOSED — recommended | `driver_power_requirements.md` §3; BOM |
| 21 | 2026-10-27 | **FPGA/clock interface (M16):** 2×20 IDC; 32.768 MHz XO (Citizen CSX750FBC32.768M); FPGA board owned (Zynq-7020 class recommended); 32.768 MHz → PLL ×3 → ÷2 = **49.152 MHz SPI**; ÷164 = **199.805 kSPS DAC**; ÷128 = 256 kSPS ADC. 2×20 carries ADC, DAC, E-stop, watchdog; **13 spare pins** (no LDAC pin). | Exact integer tones: 2 kHz × k = 32.768 MHz × k/16384, k=10…17; one clock for DDS and ADC removes leakage; M16 DAC at 200 kSPS; pinout in `system_schematic.md` | LOCKED interface (M16); **FPGA = PS-less Artix-7, see #26** | `system_schematic.md`; `dig6_requirements.md` |
| 22 | 2026-10-27 | **Enclosure/E-stop parts:** one aluminum box with internal shield; Schneider XB4BS8444 or AutomationDirect GCX1131 NC mushroom; fan/filter; no metal within 150 mm of the volume | One-box decision; NC fail-safe; 22 mm panel mount; the guard is non-metal per SC-04b | PROPOSED — recommended | BOM |
| 23 | 2026-10-27 | **DIG-6 requirements accepted:** 32-bit DDS, 4096-entry LUT, 4-channel capture, Goertzel, 8×5 LM/TRF, 8.633 ms pipeline, 115.8 Hz, filter-off latency 8.6 ms | 2.000 ms acquisition + 0.133 ms ADC delay + 0.5 ms demod + 5.0 ms solve + 1.0 ms overhead = 8.633 ms; ≥100 Hz; ≤20 ms off / ≤100 ms on | PROPOSED — recommended | `dig6_requirements.md` |
| 24 | 2026-10-27 | **System flow chart, board-level schematic, system BOM Rev A issued** | Phase 2 report §3/§5 and design-review drawing set; procurement gate | DRAFT Rev A | `system_flowchart.md`, `system_schematic.md`, `BOM_SYSTEM-01.xlsx` |
| 25 | 2026-10-28 | **Electronics = one board, BRD-01.** Power entry/E-stop/DC-DC, FPGA + clock, DAC80508 + 8× LTC1563-2 + 8 current loops + current sense, receiver (INA163 + ADA4940-2 + AD7768-4), and the FG/pen connectors are **zones of one 4-layer board**, not separate boards. FG-01 stays a separate passive coil PCB; the pen stays passive. | One board removes the 49.152 MHz SPI cable (0.17 ns hold), the ADC ribbon, and three inter-board connectors; the box partition is replaced by an on-board shield can. | **LOCKED (team, 2026-10-28)** | `system_schematic.md` §1, §6.0 |
| 26 | 2026-10-28 | **FPGA integration = D: PS-less FPGA on BRD-01.** XC7A35T-1FTG256C baseline (33k LC, 1.8 Mb BRAM, 90 DSP, 170 I/O, 1.0 mm FTBGA); XC7A50T-1FTG256C as the same-footprint upgrade. QSPI config flash, USB-UART host link, 3.3 V HR banks. No PS, no DDR3, no Linux; the host PC does UI/log/camera. | DDR3 is a PS requirement, not a pose requirement: the pipeline needs ~10–25 kB of BRAM and 0.6–0.7 GFLOP/s. Dropping the PS removes DDR3, the 6-layer stack, PMIC sequencing and the boot image, and keeps the 49.152 MHz SPI on-board. MCU-only (option E) was evaluated and rejected: an analytic-Jacobian solve fits a 1 GHz M7 at ~1× margin, but the 8.633 ms period is then average-case, not guaranteed. | **LOCKED (2026-10-28)** | `fpga_integration_options.md`; `system_schematic.md` §6.0 |

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
  PM/step, LMH6321 crossover, 8-channel thermal soak, E-stop/overcurrent, EMI
  with the one-box shield. The SPICE screen is not a substitute for the bench.
- **DIG-6:** integer-J leakage, golden demod/solver match, 8.633 ms worst-case
  timing, 1-hour moving run.
- **INT-7:** κ 7×7, 98-point RMS at 85.6/152 mm, tremor 20 dB/3 dB, latency,
  stop ≤100 ms, ICNIRP scan, BOM ≤1000 CAD/pair or documented deviation.

## Procurement checks (order-time, not design)

- Re-quote DAC80508MRTET, LTC1563-2IGN#PBF, LMH6321MR/NOPB, AD7768-4,
  ADR434, INA163, ADA4940-2, ME60A1503F01, RV-1515D; confirm stock and lifecycle.
- LMH6321: TI product page says ACTIVE; distributor stock is thin, so buy
  8 + 2 spares now. Fallback: vendor Rev A discrete stage or a comparable
  high-current buffer with a recorded deviation.
- Confirm XC7A35T-1FTG256C stock, HR (3.3 V) bank coverage and 35T→50T pin compatibility.
  If the HLS solver does not fit the 35T, use the
  XC7A50T in the same FTG256 footprint; the interface is unchanged.
- Exact enclosure, fan, heatsink, and panel connectors are order-time choices.
- No BOM row may ship with a placeholder supplier P/N.

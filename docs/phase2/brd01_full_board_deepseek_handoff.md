# BRD-01 Full Board (Driver, Receiver, FPGA, Connectors): Verification, Cost-Optimized BOM & Schematic Wiring Handoff

**Status (2026-11-25): planning handoff, kept as history — not a record of
execution.** Committed BRD-01 facts come from
`docs/phase2/brd01_wiring_manifest.md`, `docs/phase2/brd01_component_reference.md`
and `docs/phase2/power_tree_v2.md` §9: eight driver channels and one DAC80508,
the `+5V_EXC` excitation rail, `D_REF` = `D534`, the 32.768 MHz XO and the
PS-less FPGA netlist are captured, with ERC 0/0. Not evidenced as landed: the
Stage 2 cheapest-qualified BOM substitutions and the open-drain comparator
replacement (the netlist still carries TLV3201 comparators feeding U600–U603
open-drain buffers). The coil value locked by decision #27 is 79 µH / 2.9 Ω;
the "70 µH / 2 Ω" figure quoted below is a driver-budget starting point, not
the locked coil. The BRD-01 power tree is locked as decision #31 (2026-11-25),
superseding the #20 part list; the captured schematic implements it. BOM
reconciliation is not evidenced.
Keep the stages below as the original proposal; do not treat their checklists
as completed gates.
**Designator note (2026-11-26):** `R184` in the historical work order below was
renamed `R186` in commit `8d39a99` (10 Ω ADC-reference filter, U103 OUT/IN- →
`/receiver/ADC_REF`). Read it as `R186`; the original text is kept as history.

**Orchestrator:** `DeepSeek-V4.1-Flash-1017` (calculations gate, BOM/contract decisions, `tools/kicad_sch_helper.py`, `brd-01.kicad_sch` root, `kicad-cli` gates, `git`)  
**Parallel Workers:** `Tencent Hy4 Flash` (read-only doc/math audits, supplier/part-cost screening, disjoint child-sheet edits via helper, SVG→PNG visual checks)  
**Scope:** Everything on `BRD-01` outside the `power` sheet — `driver.kicad_sch`, `receiver.kicad_sch`, `fpga.kicad_sch`, `connectors.kicad_sch`, and `brd-01.kicad_sch` (after/alongside `power_tree_v2.md` PR-A & PR-B)  
**Pipeline Order:** **Stage 1 (Docs & Calculations Verification)** → **Stage 2 (Cheapest Qualified Parts Selection)** → **Stage 3 (Schematic Wiring, Cleanup & ERC=0)**

---

## 1. Orchestrator / Worker Rules (Inherited + Extended)

1. **No raw `.kicad_sch` coordinate guessing.** All schematic edits must go through `tools/kicad_sch_helper.py` on the `1.27 mm` (`50 mil`) grid.
2. **Gate every stage before advancing:**
   * Stage 1 outputs a signed-off **Verification & Margin Ledger** (every calc must pass or log a `contract-change` / design fix before Stage 2).
   * Stage 2 outputs a **Cost-Optimized BOM Delta** (locked core ICs untouched unless flagged; every substitute verified against Stage 1 specs).
   * Stage 3 runs **per-sheet parallel edits** (1 `Hy4 Flash` worker per disjoint `.kicad_sch` file) → `DeepSeek` root wiring → `kicad_netlist_compare.py` expected-diff ledger + full-project `ERC = 0/0` + parallel `Hy4 Flash` SVG→PNG visual inspection.

---

## 2. Stage 1 — Docs Reconciliation & Engineering Calculations (Wave 1)

Dispatch **4 parallel `Hy4 Flash` audit workers** (one per subsystem) to cross-check `system_flowchart.md`, `system_schematic.md` (Rev A, 2026-10-27), `power_tree_v2.md` (2026-11-24), `decisions_log.md`, and the current KiCad files:

### S1-A: Doc Drift & System-Level Reconciliation (`DeepSeek` + `Hy4 Flash`)
* **Supersede stale Rev A power refs:** Flag all `system_schematic.md` §2 references to `OKI-78SR-5`, `TPS7A20`, `RV-1515D`, `+5V_D`, `+3.3V_D`, `+5V_A` as superseded by `power_tree_v2.md` (`+6V`, `+3.3V`, `+5V_EXC`, `+5VA`, `MGJ2D151515SC`).
* **Reconcile coil model:** `system_schematic.md` §3 lists `79 µH / 2.9 Ω` while §9 and `system_flowchart.md` §3 quote `70 µH / 2 Ω`. Compute worst-case impedance using `79 µH / 2.9 Ω` + `1.00 Ω` `R_store` + cable.
* **Verify power budget:** Recompute total `15 V` adapter draw at `150 mA` and `250 mA` RMS using `power_tree_v2.md` §3 (`0.15 A` typ / `0.35 A` max for `+6V` tree) + `8× LMH6321` + `MGJ2`.

### S1-B: `driver` Calculations (`Hy4 Flash` Worker 1)
Verify and output a pass/fail table for:
1. **Coil drive voltage headroom (CRITICAL CHECK):**
   * At `34 kHz` with `79 µH + 2.9 Ω` + `1.00 Ω R_store`: $|Z| = \sqrt{3.9^2 + (2\pi \cdot 34000 \cdot 79\times 10^{-6})^2} \approx 17.32\ \Omega$.
   * At `250 mA RMS` (`354 mA` peak), $V_{peak} \approx 6.13\text{ V}$; at `500 mA` peak, $V_{peak} \approx 8.66\text{ V}$.
   * Check `LMH6321` output swing on `+15 V` single supply (`Vmid = 7.5 V` → `~5.5–6.0 V` linear swing): flag whether `250 mA` clips at `34 kHz` and confirm `500 mA` is impossible without higher rail or lower-inductance coil.
2. **`LMH6321` thermal dissipation:** Compute per-IC dissipation at `150 mA` and `250 mA` RMS, check `SO PowerPAD` $\theta_{JA}$ on 4-layer PCB, and verify copper pour area (`180 cm²` noted in §10).
3. **AC-coupling & `Vmid`:** Verify `C1 = 100 µF` reactance at `20 kHz` (`0.08 Ω`), ripple current rating at `250–500 mA`, and `Vmid = 7.5 V` (`10k/10k` + `1000 µF`) stiffness across 8 channels.
4. **DAC & filter headroom:** Confirm `DAC80508` + `LTC1563-2` on `+5V_EXC` (`4.875–5.125 V` min/max) with `0.3–4.6 V` DDS clamp (`2.45 V` mid), `60 kHz` Butterworth resistor values (`LTC1563-2` datasheet Eq.), and `LP = V+` (`+5V_EXC`).
5. **Current-sense & fault comparator (CRITICAL CHECK):**
   * `R_store = 1.00 Ω 0.1%`: verify power (`0.063 W` @ `250 mA`, `0.25 W` @ `500 mA` peak → `0.5 W` rating ✓), summer gain `×2.0103`, and peak sum `< 2.5 V` within `±4.096 V` ADC FS.
   * **Check `TLV3201` output type:** `system_schematic.md` §4.2/§4.4 specifies `TLV3201` for an *"open-drain wired-OR fault bus"*, **but `TLV3201` is push-pull!** Verify whether the current schematic has `TLV3201` wired-OR (which would cause bus contention) and flag replacement with an open-drain comparator.
6. **49.152 MHz SPI timing:** Verify `DAC80508` `tSDIH = 10 ns` vs `10.17 ns` half-period (`0.17 ns` raw margin), `33 Ω` series damping, and `~2.5 ns` FPGA `SDI` delay (`7.7 / 12.7 ns` balanced).

### S1-C: `receiver` Calculations (`Hy4 Flash` Worker 2)
1. **Front-end gain & noise:** Verify `INA163` $R_G = 6000 / (35 - 1) = 176.47\ \Omega$ (`176 Ω` → `G = 35.09`), `10k 0.1%` bias resistor offset (`12 µA × 10 kΩ = 0.12 V`), `10 µF` input cap reactance (`0.8 Ω` @ `20 kHz` vs `8.6 Ω` coil), and `100 Ω` + Schottky clamp capacitance (`< 10 pF`).
2. **ADC swing & anti-aliasing:** Verify `ADA4940-2` (`G = 2`, `VCM = 2.5 V` → `0.45–4.55 V` per leg), strongest `34 kHz` tone (`3.40 V` diff = `83%` of `±4.096 V` FS ✓), and `20 Ω / 470 pF / 100 pF` RC corner frequency vs `8.192 MHz` modulator & `256 kSPS` ODR.
3. **Reference clamp (`C7`):** Verify `ADR434` (`4.096 V`) + `OPA192` + `R184` (`10 Ω`) + `D_REF` (`BAS70`) fault current during power-down (`≤ 100 mA` `AD7768-4` latch-up limit).

### S1-D: `fpga` & `connectors` Calculations (`Hy4 Flash` Worker 3)
1. **Bank & pinout audit:** Verify all `XC7A35T-1FTG256C` used banks are **HR (`3.3 V`)**, confirm `35T ↔ 50T` `FTG256` pin compatibility, and verify `BUCK_SYNC` on ball `R3` (`IO_L8P_T1_34`, Bank 34 `3.3 V`).
2. **Clock & config:** Verify `32.768 MHz` XO fanout (`MCLK_ADC` via `33 Ω` + FPGA input), `W25Q64` QSPI config pins, `U142` (`FT231X`) on `+3.3V` (`D3`), and `DCLK`/`DOUT0–3` trace-length matching constraint.
3. **Connectors & safety:** Verify `J1–J8` (`3 A` keyed, star return), `J123` Pico header (`D4`: pin 1 `NC`, `3× Pico 2` step/dir + watchdog), and `K1`/`K2` + opto `ESTOP_STATUS` isolation.

---

## 3. Stage 2 — Cheapest Qualified Parts Selection (Wave 2)

After Stage 1 calculations pass, run **3 parallel `Hy4 Flash` BOM-optimization workers** (plus `DeepSeek` final sign-off).

### Hard Selection Rules
1. **Locked Core ICs (Do NOT swap without a `contract-change` issue):** `XC7A35T-1FTG256C`, `AD7768-4`, `DAC80508`, `LTC1563-2`, `LMH6321`, `INA163`, `ADA4940-2`, `ADR434`, `FT231X`.
2. **Optimize cost & reel consolidation everywhere else:** Pick the cheapest in-stock part (Mouser/DigiKey/JLCPCB-LCSC baseline) that meets Stage 1's electrical, thermal, tolerance, and package specs, consolidating duplicate values/packages.

### Target Cost-Audit Categories
| Worker | Subsystem | Specific Cost & Spec Checks |
|---|---|---|
| **W2-A** | `driver` BOM | **Fix push-pull bug:** Replace `TLV3201` (push-pull) with cheapest qualified open-drain comparator (e.g., dual/quad open-drain `LMV339`/`LM393` or fast `TLV7022`/`TLV1702` if `< 1 µs` trip required). Audit `OPA192`/`OPA2192` (keep precision low-offset where needed on summer/diff amp, evaluate cheaper `±15 V` op-amps for non-critical buffers). Select cheapest `100 µF ≥ 16 V` low-ESR cap for `C1`, cheapest `1.00 Ω 0.1% 0.5 W` shunt, and consolidated `0603` `1%` resistors. |
| **W2-B** | `receiver` BOM | Consolidate `BAS70` / `BAT54` dual Schottky arrays (use same part for `±12VA` clamps and `D_REF`). Select cheapest `C0G/NP0` `470 pF` / `100 pF` caps, `10 µF` low-DF film/X7R AC-coupling caps, `176 Ω` / `10 kΩ 0.1%` thin-film resistors, and `OPA192` reference buffer. |
| **W2-C** | `fpga` & `connectors` BOM | Cheapest `64 Mbit` QSPI flash (`W25Q64JV` or compatible), cheapest `32.768 MHz` CMOS XO meeting `AD7768-4` jitter/stability, cheapest `J1–J8` (`Molex Mini-Fit Jr` vs `JST VH` 2-pin `3 A` keyed), cheapest `K2` force-guided relay + panel E-stop (`XB4BS8444` vs `GCX1131`), and cheapest optocoupler. |

**Stage 2 Gate:** `DeepSeek` reviews all substitutions, locks the final BOM table (MPN, footprint, quantity, unit/extended cost, Stage 1 spec margin), and logs any part changes in `bom-to-cad.md`.

---

## 4. Stage 3 — Schematic Wiring, Cleanup & Verification (Wave 3)

Execute **only after Stage 1 & Stage 2 are signed off**:

1. **Pre-Wave Pin & Baseline Setup (`DeepSeek`):**
   * Export pre-Stage-3 netlist & ERC baseline.
   * Update `tools/kicad_sch_helper.py` with any new symbols/footprints from Stage 2 (`D_REF`, open-drain comparators, consolidated connectors).
2. **Parallel Child-Sheet Implementation (4 `Hy4 Flash` workers on strictly disjoint files):**
   * **W3-A (`driver.kicad_sch`):** Wire Stage 1/2 fixes (open-drain fault comparators, `Vmid`, `R_store`, summer, `+5V_EXC` on `U10`/`U80–U87`), apply label/NC/`PWR_FLAG` policy, box into clean blue blocks (`DAC + Filter`, `8× Current Loops`, `Summer + Comparators`, `E-stop`).
   * **W3-B (`receiver.kicad_sch`):** Wire `D_REF` (`C7`), verify `INA163` / `ADA4940-2` / `AD7768-4` / `ADR434` connections, apply label/NC/`PWR_FLAG` policy, box into clean blue blocks (`Input Protection`, `Front-End Gain`, `ADC + Ref + Clock`).
   * **W3-C (`fpga.kicad_sch`):** Wire `U142` (`D3` → `+3.3V`), ball `R3` → `BUCK_SYNC` (`D5`), `32.768 MHz` XO, `W25Q64`, bank HR `3.3 V` decoupling, apply label/NC/`PWR_FLAG` policy, box into clean blue blocks (`FPGA Power/Decoupling`, `ADC/DAC Interfaces`, `Config/USB-UART/Clock`, `Safety/Pico`).
   * **W3-D (`connectors.kicad_sch`):** Wire `J123.1` → `no_connect` (`D4`), `J1–J8` star return, pen `J1`/`J2`/`J4`, `K1`/`K2` E-stop, apply label/NC policy, box cleanly.
3. **Orchestrator Integration & Gates (`DeepSeek` + `Hy4 Flash` Vision):**
   * `DeepSeek` wires matching `hierarchical_label` ↔ `sheet` `pin`s on `brd-01.kicad_sch`, runs **symbol↔footprint pad audit** on all non-power ICs (`AD7768-4 64-LQFP`, `DAC80508 WQFN-16`, `LTC1563-2 SSOP-16`, `LMH6321`, `INA163`, `ADA4940-2`, `XC7A35T-1FTG256C`), and verifies **expected-diff netlist ledger** + **`ERC = 0 errors / 0 warnings`**.
   * Export SVG→PNG for all 5 sheets + `brd-01.kicad_sch` and dispatch **6 parallel `Hy4 Flash` vision workers** to catch overlapping text, wire collisions, and box containment.
   * Regenerate BOM, update `system_schematic.md` / `bom-to-cad.md` / `decisions_log.md`, and open PR.

---

## 5. Copy-Paste Orchestrator Prompt for DeepSeek-V4.1-Flash-1017

```text
You are the orchestrator (DeepSeek-V4.1-Flash-1017) for the rest of BRD-01 (driver, receiver, fpga, connectors, and brd-01 root) following a strict 3-stage pipeline: (1) Docs & Calculations Verification -> (2) Cheapest Qualified Parts Selection -> (3) Schematic Wiring & ERC=0. Dispatch Hy4 Flash ONLY on read-only audits, BOM cost screening, SVG->PNG visual checks, or strictly file-disjoint child sheets.

STAGE 1 — VERIFY DOCS & CALCULATIONS (Wave 1, 4 parallel Hy4 Flash audits + your synthesis):
- Reconcile system_flowchart.md & system_schematic.md (Rev A) against power_tree_v2.md (2026-11-24).
- Driver: check 34 kHz coil impedance (79 uH + 2.9 ohm + 1 ohm R_store) vs LMH6321 swing headroom on +15 V (flag 250 mA/500 mA clipping!), LMH6321 thermal dissipation, 100 uF AC-coupling ripple, DAC80508/LTC1563-2 on +5V_EXC (0.3-4.6 V DDS clamp), 49.152 MHz SPI hold margin (tSDIH 10 ns), and flag that TLV3201 is push-pull (cannot wire-OR an open-drain fault bus!).
- Receiver: check INA163 RG (176 ohm -> G=35), 10k 0.1% bias offset, ADA4940-2 G=2 VCM=2.5 V swing (3.40 V diff @ 34 kHz), anti-alias RC, ADR434 + D_REF clamp current.
- FPGA/Connectors: verify all XC7A35T-1FTG256C banks are HR 3.3 V, 35T<->50T pin compatibility, R3 BUCK_SYNC, U142 on +3.3V, J123.1 NC, K1/K2 E-stop isolation.
Gate: produce signed-off Verification & Margin Ledger before Stage 2.

STAGE 2 — CHEAPEST QUALIFIED PARTS SELECTION (Wave 2, 3 parallel Hy4 Flash BOM workers):
- Keep locked core ICs untouched (XC7A35T, AD7768-4, DAC80508, LTC1563-2, LMH6321, INA163, ADA4940-2, ADR434, FT231X).
- Optimize cost & consolidate reels everywhere else: replace TLV3201 with cheapest qualified open-drain comparator; consolidate BAS70/BAT54 arrays, 0603 1% vs 0.1% resistors, C0G vs X7R caps, 100 uF AC-coupling cap, W25Q64, 32.768 MHz XO, J1-J8 3A connectors, K2 relay/opto.
Gate: lock Cost-Optimized BOM Delta & update bom-to-cad.md.

STAGE 3 — SCHEMATIC WIRING & VERIFICATION (Wave 3):
- Update tools/kicad_sch_helper.py for any Stage 2 symbol/footprint changes. Never guess raw coordinates.
- Dispatch 4 parallel Hy4 Flash workers on disjoint sheets (driver, receiver, fpga, connectors) to apply Stage 1/2 fixes, label/NC/PWR_FLAG cleanup, and blue-box layout.
- You wire brd-01.kicad_sch hierarchical pins, audit symbol<->footprint pad maps (AD7768-4 64-LQFP, DAC80508, LTC1563-2, LMH6321, INA163, ADA4940-2, XC7A35T-1FTG256C), verify expected-diff netlist ledger + ERC = 0/0, and dispatch 6 parallel Hy4 Flash vision workers on exported SVG->PNGs. Regenerate BOM and update docs.
```

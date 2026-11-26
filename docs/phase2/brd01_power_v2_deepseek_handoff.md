# BRD-01 Power v2 & Cross-Sheet Redraw: DeepSeek-V4.1-Flash-1017 Orchestrator & Hy4 Flash Worker Plan

**Status (2026-11-25): executed plan, kept as history.** What landed on `main`
is recorded in `docs/phase2/power_tree_v2.md` §9 and confirmed by the committed
netlist in `docs/phase2/brd01_wiring_manifest.md`: `+6V`/`+3.3V`/`+5V_EXC`/`+5VA`,
`U147`/`U7`/`U149`/`U146`/`U5`, `D_REF` = `D534`, `J123.1` no-connect, `U142`
on `+3.3V`, ball `R3` → `BUCK_SYNC`, full-hierarchy ERC 0 errors / 0 warnings.
**Adopted:** decision #31 (2026-11-25) locks this power tree and supersedes
the decision #20 part list; the captured schematic implements it (BOM
reconciliation not evidenced). The pin-1 item is **DONE under decision #32
(2026-11-26)**: `pico_link.md` Rev B now lists pin 1 as NC, matching J123.1's
no-connect; BRD-01 supplies no 3V3 and the Pico uses its own USB.
**Still open:** the M16 DDS-swing centre wording (2.45 V vs 2.5 V) and the bench
items in `power_tree_v2.md` §7 C1/C5/C7. The instructions below are the original
plan, not current work orders — do not re-open the #20 change or treat v2 as
proposed.

**Orchestrator:** `DeepSeek-V4.1-Flash-1017` (state, `git`, `tools/kicad_sch_helper.py`, `power.kicad_sch`, `brd-01.kicad_sch` root wiring, `kicad-cli` gates)  
**Parallel Workers:** `Tencent Hy4 Flash` (read-only audits, SVG/PNG vision checks, disjoint child-sheet edits via helper, docs/issue drafting)  
**Golden Baseline:** `ec88cd1` (`pwr2`) — **pinned explicitly**, never `HEAD`  
**Execution Split:** Two PRs — **PR-A** (`power` repair, redraw, specs, pad audit) and **PR-B** (§7 cross-sheet fixes + contract/docs)  
**Page Budget:** A1 Portrait (`594 × 841 mm`) if block-budgeted cleanly before Step 0; **A0 Portrait (`841 × 1189 mm`)** fallback if `546 × 607 mm` + boxes/margins/TPs crowds A1  
**Hierarchy:** Hierarchical labels (`hlabel`) + sheet pins on `brd-01.kicad_sch` for crossing signal nets (gated per-sheet by pin-membership diff); power symbols for rails/GND

---

## 1. Hard Engineering Rules (Read Before Touching Any File)

1. **Never hand-guess `.kicad_sch` coordinates.** Build `tools/kicad_sch_helper.py` to parse `(lib_symbols ...)` pin definitions + each symbol's `(at x y rot)` and `(mirror x|y)` (handling KiCad's Y-axis flip) and snap all placements, wires, stubs, power symbols, `hlabel`s, and `no_connect` flags to the `1.27 mm` (`50 mil`) grid.
2. **Never commit an electrically broken state.** Do **not** commit the uncommitted 9k-line working tree before Step 1. Pin `before.xml` and `erc_ec88cd1.json` to `ec88cd1`, repair `U145` first, and commit resize + repair as **one** netlist-neutral commit.
3. **Verify membership, not net names—and check merges, not just opens.** Confirm `tools/kicad_netlist_compare.py` compares **pin-membership sets** (since removing facing labels renames auto-nets) and flags **both splits and merges**, plus `refdes` / `lib_id` / `footprint` set equality.
4. **Two separate checklists:** `ERC = 0` does **not** prove contract compliance (`D_REF` missing and `J123.1` on `+3.3V` are not ERC findings). Track Electrical (`ERC`) and Contract (`D1–D5`, `C7`) independently.

---

## 2. Orchestrator / Worker Dispatching Rules (`DeepSeek` → `Hy4 Flash`)

| Rule | Orchestrator (`DeepSeek-V4.1-Flash-1017`) | Parallel Workers (`Hy4 Flash`) |
|---|---|---|
| **File Locking** | Sole writer of `power.kicad_sch`, `brd-01.kicad_sch`, `tools/`, and `git` commits | Allowed to write **only** when each worker owns a **strictly disjoint file** (e.g., 1 worker per child sheet) |
| **Coordinate Math** | Builds and maintains `tools/kicad_sch_helper.py` | **Forbidden** from raw S-expression edits; must call `kicad_sch_helper.py` only |
| **Self-Contained Prompts** | Supplies exact file paths, net/pin tables, and expected JSON/checklist schema | Returns structured findings/diffs only (no prose dumps) |
| **Gate Authority** | Runs all `kicad_netlist_compare.py` + `kicad-cli` ERC gates before any commit | Runs single-sheet `kicad-cli sch export erc` and SVG→PNG visual check before returning |

### Parallel Dispatch Waves

* **Wave 0 — Pre-Flight Audits (4 parallel `Hy4 Flash` read-only workers):**
  * **W0-A (Provenance):** `git diff ec88cd1~1..ec88cd1` → classify added/moved/removed parts (`D140`, `J750`, `R185`, `U143`, `C750–C754`, `U1`).
  * **W0-B (ERC & `U145` Enumeration):** Parse `erc_ec88cd1.json` vs `erc_current.json`; list all `U145` pins and all 15 former `+1V8_FPGA` members from `before.xml`.
  * **W0-C (Pad & Cap Audit):** Audit symbol↔footprint pad maps for `U147` (`TPSM63604RDLR`), `U7` (`TPS62130ARGTR`), `U149` (`TPS7A4701RGWR`); reconcile `C810` vs `U147` `VLDOIN` `1 µF` (pin 5).
  * **W0-D (NC Whitelist & `PWR_FLAG`):** Build mutually exclusive net table from `power_tree_v2.md` §4 (whitelist ~24 true opens; flag `GND` + inductor-fed rails needing `PWR_FLAG`; exclude `BUCK_SYNC`).
* **Wave 1 — PR-A on `power.kicad_sch` (Sequential writes by `DeepSeek`, Parallel visual critique by `Hy4 Flash`):**
  * `DeepSeek` executes Step 1 (`U145` repair) and Step 2 (block-by-block redraw) sequentially.
  * After each block exports SVG→PNG, dispatch `Hy4 Flash` vision workers on cropped block PNGs to report label overlaps, wire crossings, and box containment while `DeepSeek` prepares the next block.
* **Wave 2 — PR-B Disjoint Cross-Sheet Edits (4 parallel `Hy4 Flash` workers, 1 per child sheet):**
  * **W2-A (`driver.kicad_sch`):** Exact-match `+5V` → `+5V_EXC` (`U10` `VDD` + `8× LTC1563-2` `V+`/`LP`) + crossing `hlabel`s.
  * **W2-B (`fpga.kicad_sch`):** **D3** `U142` (`VCC` 12, `~RESET` 11, `3V3OUT` 10 / `FT_3V3` → `+3.3V`), **D5** ball `R3` → `BUCK_SYNC` + crossing `hlabel`s.
  * **W2-C (`receiver.kicad_sch`):** **C7** add `D_REF` (`BAS70` refdes/footprint/BOM, anode `ADC_REF` after `R184` `10 Ω`, cathode `+5VA`) + crossing `hlabel`s.
  * **W2-D (`connectors.kicad_sch`):** **D4** `J123.1` → `no_connect` + crossing `hlabel`s.
  * `DeepSeek` then wires matching `sheet` `pin`s on `brd-01.kicad_sch`, runs full-hierarchy ERC (`0/0`) + expected-diff ledger, and fans out `Hy4 Flash` vision workers across all 6 sheet PNGs in parallel.
* **Wave 3 — Docs & Tracking (3 parallel `Hy4 Flash` workers on disjoint files):**
  * **W3-A (historical plan; #31 row landed; pin-1 done by #32 2026-11-26):** `contract/decisions_log.md` #20, `contract/icd/pico_link.md` (`J123.1` → `NC`, done — Rev B), M16 handoff (resolve D2 `0.3–4.6 V` / `2.45 V` midpoint, still open), `contract-change` PR body.
  * **W3-B:** `hardware/brd-01/kicad/power-tree.md`, README page table, `bom-to-cad.md`, `power_tree_v2.md` §9 (fix stale ERC status).
  * **W3-C:** FPGA RTL tasks (`BUCK_SYNC` `32.768 MHz ÷ 32` on `R3`, DDS clamp `0.3–4.6 V`, Power Estimator `C6`).

---

## 3. Pre-Flight & Step 0 — Contract Issue, Golden Pin, Provenance

1. **Historical step:** a `contract-change` issue was raised for `ec88cd1` against decision #20; it is now resolved by decision #31. D2's arithmetic discrepancy (`0.3–4.6 V` midpoint `2.45 V`, not `2.5 V`) remains a wording item only.
2. **Close KiCad & record version:** Ensure `/usr/bin/kicad` (PID `764171`) is saved/closed and `.lck` files are removed. Record `kicad-cli --version`.
3. **Pin golden `ec88cd1` exports:**
   ```bash
   mkdir -p /tmp/opencode/head /tmp/opencode/svg
   git archive ec88cd1 | tar -x -C /tmp/opencode/head
   kicad-cli sch export netlist --format kicadxml -o /tmp/opencode/before.xml /tmp/opencode/head/hardware/brd-01/kicad/brd-01.kicad_sch
   kicad-cli sch export erc --format json --severity-all -o /tmp/opencode/erc_ec88cd1.json /tmp/opencode/head/hardware/brd-01/kicad/brd-01.kicad_sch
   kicad-cli sch export erc --format json --severity-all -o /tmp/opencode/erc_current.json hardware/brd-01/kicad/brd-01.kicad_sch
   ```
4. **Dispatch Wave 0 (`W0-A` through `W0-D`)** in parallel and review their structured outputs before modifying any schematic.
5. **Lock page budget:** Measure bounding boxes for all 7 blocks with `2.54 mm` stub clearance and box titles. Lock **A1 Portrait (`594 × 841 mm`)** if comfortable, or **A0 Portrait (`841 × 1189 mm`)** if marginal.

---

## 4. PR-A: `power` Sheet Repair, Redraw, Specs & Pad Audit

### Step 1 — Repair `U145` (+1V8_FPGA)
The uncommitted rewrite caused both **opens and a dangerous merge**:
* `BUCK2_FB → GND`: old FB wire now lands on `GND` (`R194` pad 1 grounded, pad 2 floating, `U145-FB` pad 5 floating). Re-adding labels without deleting the stray wire shorts `FB` to `GND` and drives `VOUT → 6 V` into `VCCAUX`.
* `U145-VOS` (pad 14) disconnected from `+1V8_FPGA`.
* `U145-PG` (pad 4) disconnected from `/power/PG_1V8` (breaks `U7` `EN`, killing `+3.3V`).
* `L141`, `R193.2`, `R194.2` off-grid (`1.27–3.81 mm`).

**Action:** Delete **all** wires in `U145` output block (`x 389–423, y 196–222 mm`), snap every pin/component/label from `W0-B` onto the `1.27 mm` grid via `kicad_sch_helper.py`, and rewire.  
**Gate:** `kicad_netlist_compare.py` reports **membership-SAME (zero splits, zero merges)** vs `ec88cd1` + `refdes`/`lib_id`/`footprint` set equality; ERC matches `erc_ec88cd1.json`.  
**Commit:** Commit resize + `U145` repair together as one netlist-neutral commit. *(Bring-up note: first power-up on a current-limited supply.)*

### Step 2 — Block-by-Block Redraw, Label Policy & `PWR_FLAG` Audit
Execute **per block** (`DeepSeek` edits → `kicad_netlist_compare.py` + ERC + `Hy4 Flash` SVG→PNG check → `git commit`):

1. **7 Blue-Boxed Blocks:** (1) Entry/Protection; (2) E-Stop + Arm Latch (`D140`, `J750`, `R185`, `U143`, `C750–C754`, `U751` consolidated from `300 mm`); (3) `+6V` Pre-Regulator (`U147`, `C800–C810`, `R800–R805`); (4) FPGA Bucks (`U144`, `U145`, `U7`, `L140`/`L141`/`L800`, `R190–R195`, `R806`/`R807`); (5) Analog LDOs & Filters (`U149`+`FL1`, `U146`+`FL2`); (6) `±12VA` (`U5`, `U6`, `U2`, pull `C780–C783` inside box); (7) Test Points beside rails.
2. **Mutually Exclusive Label & NC Policy (from `W0-D`, computed *after* Step 1):**
   * **Power rails & `GND` (`104` pins):** Power symbol at pin tip.
   * **`PWR_FLAG`:** Place on `GND` and inductor-fed rails (`+1V0_FPGA`, `+1V8_FPGA`, `+3.3V`).
   * **NC whitelist (§4 only):** `U147` `RBOOT` (4), `CBOOT` (3), `SW` (2) → `no_connect` (**`NC` 15 → `GND`, not NC**); `U7` `PG` → pick `GND` or `no_connect` consistently; `U149`/`U146` unused ANY-OUT (`4,5,8,9,11,12`) + `NC` (`2,17–19`) → `no_connect`. **Never NC-flag `BUCK_SYNC`.**
   * **Same-block 2-pin nets:** Delete facing labels; draw orthogonal wire (`FB` and `PG` inside a buck block get **no label**).
   * **Block-crossing local nets:** Local label on `2.54 mm` stub at block boundary only.

### Step 3 — Full §4 Spec Pass & Final PR-A Sign-off
Apply all §4 value/voltage/dielectric/tolerance strings (`C800–C808`, `C811–C818`, `C820`, `C180–C190`, `R800–R802`, `+` polarity on `68 µF 35 V` bulk), apply `W0-C` fixes for `C810`/`VLDOIN` and any pad-map mismatches on `U147`/`U7`/`U149`, and verify final PR-A netlist-SAME + baseline ERC.

---

## 5. PR-B: §7 Cross-Sheet Fixes, Hierarchical Pins & Docs

### Step 4 — Expected-Diff Cross-Sheet Updates (Wave 2)
Dispatch `W2-A`–`W2-D` in parallel, then wire `brd-01.kicad_sch`:

| Worker / Sheet | Change | Expected Netlist Diff |
|---|---|---|
| `W2-A` `driver` | Exact-match `+5V` (not substring—keep `+5VA`/`+5V_EXC`): `U10` `VDD` + `U80–U87` (`8× LTC1563-2` `V+`/`LP`) → `+5V_EXC` | Moves 27+ pins off `+5V` to `+5V_EXC` |
| `W2-B` `fpga` | **D3:** `U142` (`FT231X`) `VCC` (12), `~RESET` (11), `3V3OUT` (10 / `FT_3V3`) → `+3.3V`; **D5:** Ball `R3` → `BUCK_SYNC` | Merges `FT_3V3` into `+3.3V`; connects `BUCK_SYNC` |
| `W2-C` `receiver` | **C7:** Add `D_REF` (real refdes, footprint, `BAS70` BOM line): anode `ADC_REF` (after `R184`), cathode `+5VA` | Adds 2 diode pins |
| `W2-D` `connectors` | **D4:** `J123` pin 1 → `no_connect` (remove `+3.3V`) | Removes `J123.1` from `+3.3V` |
| `DeepSeek` All 5 + Root | Convert crossing signal nets to `hierarchical_label` + matching `sheet` `pin`s on `brd-01.kicad_sch` + root wires | Zero netlist splits/drops vs pre-hlabel netlist |

**PR-B Gate:** Full-project `kicad-cli sch export erc` = **`0 errors / 0 warnings`**, expected-diff ledger matches 100%, and parallel `Hy4 Flash` vision workers pass all 6 exported PNGs.

### Step 5 — Docs, BOM & FPGA RTL Handoff (Wave 3)
Commit `tools/` scripts, regenerate BOM, and dispatch `W3-A`–`W3-C` in parallel to update all contract docs, KiCad docs, and FPGA RTL tracking issues.

---

## 6. Copy-Paste Orchestrator Prompt for DeepSeek-V4.1-Flash-1017

```text
You are the orchestrator (DeepSeek-V4.1-Flash-1017) for the BRD-01 power_tree_v2 schematic repair, redraw, and §7 cross-sheet completion in hardware/brd-01/kicad/. Dispatch Hy4 Flash sub-workers ONLY on read-only audits, SVG->PNG visual inspections, or strictly file-disjoint child sheets/docs; you own tools/kicad_sch_helper.py, git, power.kicad_sch, brd-01.kicad_sch, and all kicad-cli gates.

HARD RULES:
1. Build tools/kicad_sch_helper.py to parse (lib_symbols ...) + symbol transforms and snap all placements, wires, 2.54 mm stubs, power symbols, hlabels, and no_connects to the 1.27 mm grid. Neither you nor Hy4 Flash may guess raw coordinates.
2. Pin golden reference to ec88cd1 (NEVER HEAD): export /tmp/opencode/before.xml and /tmp/opencode/erc_ec88cd1.json from git archive ec88cd1. Record kicad-cli --version.
3. Confirm tools/kicad_netlist_compare.py checks pin-membership equality (not net names), flags BOTH splits and merges, and checks refdes/lib_id/footprint set equality.

EXECUTION WAVES:
- Step 0 & Wave 0 (historical; #20 issue is resolved by #31): Verify KiCad closed/.lck gone; do NOT commit broken working tree yet. Resolve D2 2.45 V wording. Dispatch 4 parallel Hy4 Flash workers: (A) ec88cd1~1..ec88cd1 provenance diff; (B) ERC baseline + U145 15-pin +1V8_FPGA enumeration; (C) U147/U7/U149 pad-map audit + C810/VLDOIN 1 uF check; (D) §4 NC whitelist + PWR_FLAG audit. Lock page size (A1 portrait 594x841 mm if block budgets fit cleanly, else A0 portrait 841x1189 mm).
- Wave 1 (PR-A on power.kicad_sch):
  - Step 1: Delete all wires in U145 output block (BUCK2_FB is merged to GND). Rewire all U145 pins (VOS 14, FB 5, PG 4) + L141/R193/R194 on 1.27 mm grid. Gate: membership-SAME vs ec88cd1 + measured baseline ERC. Commit resize+repair as one commit.
  - Step 2: Redraw 7 blue-boxed blocks sequentially; after each block run netlist-SAME + ERC + dispatch Hy4 Flash vision on block PNG, then commit. Apply NC whitelist (never NC BUCK_SYNC; U147 NC(15)->GND), PWR_FLAG on GND + inductor-fed rails, direct wires inside blocks, 2.54 mm stubs only on block exits.
  - Step 3: Full §4 spec pass + C810/VLDOIN & pad-map fixes.
- Wave 2 (PR-B cross-sheet): Dispatch 4 parallel Hy4 Flash workers using kicad_sch_helper.py on disjoint files: driver (exact '+5V' -> '+5V_EXC'), fpga (U142 -> '+3.3V', R3 -> BUCK_SYNC), receiver (D_REF with BAS70 BOM/refdes/footprint), connectors (J123.1 -> NC), plus crossing hlabels. You wire brd-01.kicad_sch sheet pins, verify ERC = 0/0 + expected-diff ledger, and dispatch parallel Hy4 Flash vision checks on all 6 PNGs.
- Wave 3: Commit tools/ + regenerate BOM; dispatch 3 parallel Hy4 Flash workers for contract/ICD/M16 docs, power-tree/README/bom-to-cad/v2 §9 docs, and FPGA RTL tracking tasks.
```
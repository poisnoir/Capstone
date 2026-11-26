# BRD-01 Label-Island Rewiring: Breakthrough & OpenCode + DeepSeek + Subagent Workflow

**Status (2026-11-25): plan, not executed.** This was written against base commits
`4952526` / `d0d2c48`; neither is on current `main` (`HEAD ef04f63`). Old
rebase instructions have been replaced with read-only `git fetch`/log inspection
from HEAD `ef04f63`; do **not** rebase onto those stale bases. An SVG text-on-wire bbox linter
(`kicad_sch_audit.py`, proposed under `tools/`) is **not written**; the deterministic gates that do
exist are `tools/kicad_sch_helper.py audit`, `tools/kicad_span_report.py`
(`--compare --fail-on-regression`) and `tools/kicad_netlist_compare.py`, with a
200 dpi render for visual overlap checks. The current BRD-01 wiring truth is
`docs/phase2/brd01_wiring_manifest.md`.

**Target:** `hardware/brd-01/kicad/receiver.kicad_sch` (and remaining flat blocks on `driver.kicad_sch`, `fpga.kicad_sch`, `connectors.kicad_sch`)  
**Reference Commit Style:** `d0d2c48` (`connectivity gate`, `parts gate`, `ERC 0/0`, `open-pin audit`, `200 dpi visual`)  
**Orchestrator:** `DeepSeek-V4.1-Flash-1017` (in OpenCode)  
**Parallel Workers:** `Tencent Hy4 Flash` (or multimodal vision subagents) for SVG/PNG inspection, read-only audits, and disjoint-block stamping

---

## 1. Why the Previous Attempt Stalled — and the 4 Breakthroughs

The `pen-1` rewiring failed visually for four concrete reasons, not because scripted KiCad editing is unviable:

| Blocker in Previous Attempt | Root Cause | Breakthrough Fix |
|---|---|---|
| **1. `2.54 mm` INA163 pitch collisions** | Routing differential clamps + bias resistors inline at `U104`'s native `2.54 mm` pin pitch leaves zero room for labels/values. | **Dog-leg fan-out (`≥ 10.16 mm` row pitch):** Exit `U104` `+IN`/`-IN` horizontally `5.08 mm`, dog-leg vertically to `≥ 10.16 mm` (or `20.32 mm`) apart, and draw `±12VA` as **one shared horizontal rail** with one label per rail. |
| **2. Text rotation & uniform field placement** | Property `(at x y rot)` interacts with symbol rotation, and one `(x, y - 7.62)` offset collides on vertical parts and diodes. | **Occupancy-grid field solver in `tools/kicad_sch_helper.py`:** Force world-space `prop_angle = 0`, register all wire/pin/body bounding boxes on a `1.27 mm` grid, and apply **role-typed placement + semantic label justification** (text points away from block). |
| **3. Slow, blind `220 dpi` render-inspect loop** | Rendering full sheets and asking a model to eyeball everything wastes turns on obvious text-on-wire overlaps. | **Zero-cost SVG bbox linter (proposed `kicad_sch_audit.py` under `tools/`, not written; use helper `audit` + a 200 dpi render for now) first:** Export `kicad-cli sch export svg`, parse `<text>` vs `<path>` wire bounding boxes in Python (`< 0.2 s`), and fix all geometric overlaps *before* rendering a **block-cropped `200 dpi` PNG** for vision subagents. |
| **4. Konnect MCP `GetOpenDocuments` failure** | Konnect's schematic layout tools require an active KiCad GUI session; headless sessions fail. | **Drop Konnect for schematic drafting.** Use `tools/kicad_sch_helper.py` + `kicad-cli` (`sch export netlist`, `sch export erc`, `sch export svg`) for 100% headless determinism; keep Konnect only for future PCB DRC/Freerouting if a GUI session is open. |

---

## 2. Pre-Flight: Sync, `opencode.json`, and Tooling Graduation

Run these once before touching `receiver.kicad_sch`:

1. **Sync upstream first:**
   ```bash
   git status -sb
   git log --oneline -1                     # base is ef04f63
   git fetch lamdesktop                     # read-only sync; do NOT rebase
   git log --oneline HEAD..lamdesktop/main   # inspect any upstream commits
   ```
2. **Handle `opencode.json`:** Do **not** commit machine-local binary paths (`~/.local/bin/konnect`) into `main`. Either add `opencode.json` to `.gitignore` and keep `opencode.example.json` tracked, or verify `opencode.json` uses relative/env paths only before committing it separately.
3. **Graduate `/tmp/bgen.py` → `tools/kicad_sch_helper.py`:** Move the S-expression parser and pin-coordinate solver out of `/tmp/` into `tools/` alongside `tools/kicad_netlist_compare.py` (as specified in the `power_v2` and `full_board` handoffs) so every subagent uses one shared, versioned geometry library.

---

## 3. Mandatory Style Spec (Encoded into `kicad_sch_helper.py`)

Encode these rules directly as Python functions so no subagent ever guesses coordinates:

1. **Grid & Fan-Out:**
   * All symbol origins, wire vertices, junctions, stubs, and labels snap to `1.27 mm` (`50 mil`).
   * Differential pairs (`PEN1_P/N`, `PEN2_P/N`, `REF_P/N`): **minimum `10.16 mm` (`8` grid units)** vertical separation between `+` and `-` lanes; dog-leg immediately outside the IC (`5.08 mm` horizontal exit from `INA163`).
2. **Clamp Rails:**
   * Draw `+12VA` as a single horizontal wire above the top lane and `-12VA` as a single horizontal wire below the bottom lane, with **one** power symbol per rail (never per-diode rail labels).
3. **Role-Typed Field Placement (World-Space `angle = 0`):**
   * **Horizontal passives (`rot ∈ {0, 180}`):** `Reference` at `(x, y - 5.08)` or `(x, y - 6.35)` and `Value` at `(x, y + 5.08)` (or stacked above at `-7.62 / -5.84` only if the upward quadrant is wire-free).
   * **Vertical passives (`rot ∈ {90, 270}`):** Place `Reference` and `Value` on the **outer** side (away from the sibling lane), `justify left` when placed right of the body, `justify right` when placed left.
   * **Clamp diodes (`D101–D104`):** Set `Value` to `(hide yes)`; place `Reference` `5.08 mm` to the outer side.
4. **Semantic Label Justification & Block Boundaries:**
   * Labels appear **only** at block boundaries (`PEN1_P/N`, `PEN1_AMP`, rails, `GND`). Internal nodes (`R101–C113`, `C113–U104`, etc.) use pure orthogonal wires + junctions.
   * Wire enters label from **left** → `(at x y 0)` + `(justify left)` (text extends right, away from block).
   * Wire enters label from **right** → `(at x y 0)` + `(justify right)` (text extends left, away from block).
   * Unused IC pins → `no_connect` markers on exact pin tips.

---

## 4. Two-Tier Verification Pipeline (Fast Local Gate + Cropped Vision)

### Tier 1 — Deterministic Python & `kicad-cli` Gates (`< 2 s` per iteration)
The SVG-bbox item 4 below is a proposed check whose linter is not yet written.
1. **Topology Signature Gate:** Export `kicad-cli sch export netlist --format kicadxml` and compare sorted `(ref, pin)` net groups against `/tmp/receiver-before-wiring.kicad_sch` (or pinned `HEAD`). Require: **0 missing groups, 0 new groups, identical `(refdes, lib_id, footprint)` set**.
2. **ERC Gate:** `kicad-cli sch export erc --format json --severity-all` → **0 errors / 0 warnings**.
3. **Open-Pin Audit:** Verify every `no_connect` matches the explicit unused-pin whitelist and zero pins were silently left floating.
4. **SVG Bounding-Box Overlap Linter (`kicad_sch_audit.py`, proposed, not written):**
   * Export `kicad-cli sch export svg` to `/tmp/opencode/svg/`.
   * Parse all `<text>` bounding boxes and wire/polyline `<path>` segments inside the target block's `(xmin, ymin, xmax, ymax)`.
   * Fail fast if any `<text>` bbox intersects a wire segment, another `<text>` bbox, or a symbol body—returning exact `(ref/label, overlap_target, suggested_shift_mm)` without needing a vision model.

### Tier 2 — Block-Cropped `200 dpi` Vision Subagent Gate
Only after Tier 1 passes all 4 checks:
* Crop the SVG/PDF render to `block_bbox + 15 mm` margin at `200 dpi` (`rsvg-convert` or `pdftoppm -r 200 -x ... -y ... -W ... -H ...`).
* Dispatch a multimodal `Hy4 Flash` vision subagent with **only** the cropped PNG and a binary pass/fail rubric:
  1. Any text touching a wire, junction, or symbol?
  2. Any label pointing *into* the block instead of *away*?
  3. Are `+12VA` / `-12VA` drawn as clean single horizontal rails?
  4. Is the differential pair symmetric and easy to trace left-to-right?
* Cap visual polish at **2 iterations** per template block.

---

## 5. OpenCode + DeepSeek + Subagent Execution Waves

### Wave 0 — Setup & Sync (`DeepSeek` Orchestrator)
1. Read-only sync from `ef04f63` (`git fetch lamdesktop` + log inspection);
   **no rebase**. Resolve `opencode.json` tracking.
2. Pin golden baseline (`before_receiver.xml`, `erc_before.json`).
3. Build `tools/kicad_sch_helper.py` (with Section 3 style rules + occupancy grid). The SVG bbox linter (`kicad_sch_audit.py`) is not written: use helper `audit`, `tools/kicad_span_report.py` and a rendered PNG for the equivalent gates.

### Wave 1 — `PEN1` Lane Template (`DeepSeek` + 1 Geometry Worker + 1 Vision Worker)
1. **Geometry Worker** runs `kicad_sch_helper.py` on **only** the `PEN1` input cluster (`U104`, `R101–R105`, `C113–C114`, `D101–D104`) and iterates against **Tier 1** (`topology`, `ERC`, `open-pin`, `SVG bbox linter`) until Tier 1 is 100% green.
2. **Vision Worker** inspects the cropped `200 dpi` `PEN1` PNG. Fix any aesthetic nit in `kicad_sch_helper.py` parameters, re-verify Tier 1 + Tier 2, and **commit `PEN1` as the golden lane template** (`d0d2c48` commit message contract).

### Wave 2 — Stamp Sibling Lanes in Parallel (`PEN2`, `REF_COIL` / remaining receiver blocks)
* Because `PEN1` is parameterized by `(dx, dy)` anchor and net/refdes map, **stamp `PEN2` and remaining receiver lanes mechanically** in one pass.
* Dispatch **parallel `Hy4 Flash` vision workers** (1 cropped block PNG per worker) while `DeepSeek` runs the full-project `topology + ERC 0/0 + open-pin` gate.
* Commit each verified block/lane cleanly.

### Wave 3 — Optional Structural Upgrade (Only if Flat Maintenance Hurts)
Once the current flat sheets are clean and committed, consider two structural upgrades as separate PRs:
1. **Symbol-space pitch variant:** Create a schematic-only `INA163_508` / `LTC1563_508` library symbol (`5.08 mm` pin pitch, identical pin numbers/netlist) to eliminate dog-leg fan-outs permanently.
2. **Hierarchical sheet instancing:** Convert the 4 receiver lanes into 4 instances of `receiver_lane.kicad_sch` and the 8 driver channels into 8 instances of `driver_channel.kicad_sch` so future edits happen in **one** place.

---

## 6. Copy-Paste Orchestrator Prompt for OpenCode (`DeepSeek-V4.1-Flash-1017`)

```text
You are the orchestrator (DeepSeek-V4.1-Flash-1017) for removing label islands on BRD-01 (starting with receiver.kicad_sch PEN1 lane) using OpenCode and parallel subagents. Do NOT use Konnect MCP for schematic layout (headless GetOpenDocuments is unhandled).

PRE-FLIGHT:
1. Base is HEAD `ef04f63`. Run `git fetch lamdesktop` and inspect the log
   (read-only); do **not** rebase onto stale commits. Keep opencode.json out of
   hardware commits (gitignore or separate config commit).
2. Pin golden netlist & ERC from HEAD before editing: export /tmp/opencode/before.xml and /tmp/opencode/erc_before.json via `kicad-cli`.
3. Graduate /tmp/bgen.py into `tools/kicad_sch_helper.py` with: (a) 1.27 mm grid snapping, (b) >=10.16 mm differential-pair row separation via 5.08 mm dog-leg fan-out from U104, (c) single horizontal +12VA/-12VA clamp rails (1 label per rail), (d) role-typed world-space angle=0 field placement on a 1.27 mm occupancy grid (diodes hide Value, Ref 5.08 mm outside), and (e) semantic label justification pointing away from the block.
4. The SVG bbox linter (`kicad_sch_audit.py`) is **not written**. Before any PNG render, use the existing `tools/kicad_sch_helper.py audit`, `tools/kicad_span_report.py` and a `kicad-cli sch export svg` render inspected visually.

EXECUTION WAVES:
- Wave 1 (PEN1 Template): Rewire U104 + R101-R105 + C113-C114 + D101-D104 using `tools/kicad_sch_helper.py`. Loop on Tier 1 gates (topology signature == before.xml, ERC == 0/0, open-pin audit, SVG bbox audit == 0 overlaps). Once Tier 1 passes, render a cropped 200 dpi PNG of the PEN1 block and dispatch a multimodal vision subagent with a strict 5-point visual rubric. Fix any flagged collision in helper parameters, re-verify all gates, and commit in d0d2c48 style.
- Wave 2 (Stamp & Parallel Verify): Stamp sibling receiver lanes by (dx, dy) template translation, run full-sheet Tier 1 gates, and dispatch parallel vision subagents (1 cropped block PNG per worker) before committing.
```

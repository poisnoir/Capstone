# BRD-01 OpenCode + DeepSeek + Open-Source Tooling Handoff Plan

**Status (2026-11-25): plan, not executed.** The inherited-state line below
(`HEAD 4952526`, five commits behind `lamdesktop/main`, reference `d0d2c48`) is
historical; neither commit is on current `main` (`HEAD ef04f63`), so the
`git rebase lamdesktop/main` steps are stale — re-check HEAD before running
them. The proposed SVG linter (`kicad_sch_audit.py` under `tools/`) is **not written**: use
`tools/kicad_sch_helper.py audit`, `tools/kicad_span_report.py` and
`tools/kicad_netlist_compare.py` for deterministic gates, plus a 200 dpi render
for visual overlap checks. Netlist truth is
`docs/phase2/brd01_wiring_manifest.md`.

**Target:** `hardware/brd-01/kicad/receiver.kicad_sch` (`PEN1` lane template → `PEN2`/`REF_COIL` stamps) & remaining flat blocks  
**Inherited State (historical; see Status above):** `HEAD 4952526`, reference commit `d0d2c48`, `ERC = 0/0`, clean `/tmp/receiver-before-wiring.kicad_sch`  
**Orchestrator:** `DeepSeek-V4.1-Flash-1017` in OpenCode  
**Subagent Runtime:** [oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim) (or [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)) + project-local [Markdown subagent definitions](https://github.com/ankitmundada/awesome-opencode-subagents/blob/master/OPENCODE.md)

---

## 1. Pre-Flight Setup (Mandatory Before Choosing an Option)

1. **Sync upstream & reconcile `d0d2c48`:**
   ```bash
   git status -sb
   git fetch lamdesktop
   git log --oneline HEAD..lamdesktop/main
   git rebase lamdesktop/main
   ```
2. **Fix `opencode.json` tracking:** Move machine-local paths (`~/.local/bin/konnect`) into `.gitignore` (commit `opencode.example.json` instead) so hardware PRs stay clean.
3. **Pin golden baseline before any edit:**
   ```bash
   mkdir -p /tmp/opencode/svg /tmp/opencode/png
   kicad-cli sch export netlist --format kicadxml -o /tmp/opencode/before.xml hardware/brd-01/kicad/brd-01.kicad_sch
   kicad-cli sch export erc --format json --severity-all -o /tmp/opencode/erc_before.json hardware/brd-01/kicad/brd-01.kicad_sch
   ```
4. **Configure OpenCode multi-model subagents (`~/.config/opencode/oh-my-opencode-slim.json` + `.opencode/agents/`):**
   * **Orchestrator (`DeepSeek-V4.1-Flash-1017`):** Owns `git`, baseline netlist/ERC gates, and final commit sign-off.
   * **Geometry/Script Worker (fast coding model):** Runs Python (`kiutils` / `elkjs`) on one isolated block at a time.
   * **Vision Critic (multimodal model, `.opencode/agents/kicad-vision-critic.md`):** Receives **only** a block-cropped `200 dpi` PNG and returns `PASS / FAIL + (ref, issue, fix)` JSON against a 5-point rubric (text-on-wire, label direction away from block, single `±12VA` rails, symmetry, readability).
   * **Gate Runner (`.opencode/agents/kicad-netlist-gate.md`):** Runs topology signature diff, `ERC = 0/0`, open-pin audit, and SVG bounding-box overlap check (the linter for the last item is not yet written).

---

## 2. Three Options to Try (What to Do for Each)

### Option A — Headless Schematic MCP + `kiutils` + `KiBot` (Fastest Drop-In Upgrade)
*Best when you want to keep the existing flat KiCad structure and replace fragile `/tmp/` S-expression scripts + GUI-bound [Konnect](https://github.com/mixelpixx/Konnect).*

**What to install / configure:**
1. Replace Konnect in `opencode.json` for schematic work with a headless schematic MCP server: [ElectroMCP](https://github.com/mhavelka77/ElectroMCP) or [mcp-kicad-sch-api](https://github.com/circuit-synth/mcp-kicad-sch-api) (both operate directly on `.kicad_sch` files and render PNGs + run ERC without an open KiCad GUI).
2. Replace `/tmp/bgen.py` with [kiutils](https://github.com/mvnmgrx/kiutils) (SCM-friendly Python dataclasses that preserve untouched S-expressions for clean `git diff`) and [kicad-skip](https://github.com/psychogenic/kicad-skip), plus [kicad-tools](https://github.com/rjwalters/kicad-tools) (`kct nets`) for fast JSON net tracing.
3. Add a `kibot.yaml` using [KiBot](https://github.com/INTI-CMNB/kibot) to run `erc`, `netlist`, and `svg`/`pdf` exports in one reproducible command.

**What to do step by step:**
1. Encode the style spec into `tools/kicad_sch_helper.py` on top of `kiutils`:
   * **Dog-leg fan-out:** Exit `U104` (`INA163`) `+IN`/`-IN` horizontally `5.08 mm`, then dog-leg vertically to `≥ 10.16 mm` row separation (never `2.54 mm`).
   * **Shared clamp rails:** Draw `+12VA` as one horizontal wire above the top lane and `-12VA` below the bottom lane with one power symbol per rail.
   * **Role-typed world-space `angle = 0` fields:** Horizontal passives (`Ref` above, `Value` below or `-7.62 / -5.84` if clear); vertical passives on the outer side; diodes (`D101–D104`) hide `Value` and place `Ref` `5.08 mm` outside.
   * **Semantic label justification:** `(justify left)` when wire enters from left, `(justify right)` when wire enters from right (text always points away from block).
2. The proposed SVG bbox linter (`kicad_sch_audit.py`) is **not written**; use `tools/kicad_sch_helper.py audit`, `tools/kicad_span_report.py` and a rendered SVG for the equivalent checks **before** any PNG render.
3. Iterate `PEN1` until Tier 1 (`topology == before.xml`, `ERC == 0/0`, `open-pin audit`, `SVG bbox == 0 overlaps`) passes, then dispatch the **Vision Critic** subagent on the cropped `200 dpi` PNG. Commit `PEN1`, then stamp `PEN2` and `REF_COIL` in parallel.

**Exit criteria:** `PEN1` passes Tier 1 + Tier 2 in ≤ 2 vision rounds and stamps cleanly to sibling lanes.

---

### Option B — Algorithmic Orthogonal Layout via `elkjs` + `kiutils` (Zero Coordinate Guessing)
*Best if hand-tuned `1.27 mm` offsets in Option A still produce wire crossings or label collisions.*

**What to install / configure:**
1. Install [elkjs](https://github.com/kieler/elkjs) (Node CLI or `npx`) alongside `kiutils`.
2. Configure ELK's [layered algorithm](https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-layered.html) with:
   * `elk.edgeRouting: ORTHOGONAL`
   * `elk.portConstraints: FIXED_SIDE` (inputs `WEST`, outputs `EAST`, `+12VA` `NORTH`, `-12VA`/`GND` `SOUTH`)
   * `elk.spacing.nodeNode` and `elk.spacing.edgeEdge` set to exact multiples of `1.27 mm` (`10.16 mm` minimum between differential rows).

**What to do step by step:**
1. Export the `PEN1` cluster (`U104`, `R101–R105`, `C113–C114`, `D101–D104`) from `kiutils` into an ELK JSON graph with exact symbol bounding boxes and pin-offset ports.
2. Run `elkjs` to compute **collision-free node `(x, y)` coordinates, orthogonal wire bend points, and junction coordinates**.
3. Snap `elkjs` output to `1.27 mm` and write symbols + wires + junctions back to `receiver.kicad_sch` via `kiutils`.
4. Run Tier 1 (`KiBot` / `kicad-cli` topology + ERC + SVG bbox audit) and Tier 2 (cropped `200 dpi` Vision Critic).

**Exit criteria:** Zero manual `(x, y)` wire tuning required; `PEN1` routes orthogonally with zero text-on-wire overlaps on the first SVG pass.

---

### Option C — Structural Refactor: Hierarchical Sheet Instances or `atopile` (Fixes 4× / 8× Duplication)
*Best after `PEN1` is proven (or if maintaining 4 flat receiver lanes and 8 flat driver channels remains error-prone).*

**Two paths:**
1. **Path C1 — Native KiCad Hierarchical Sheets (Recommended for existing BRD-01):**
   * Extract one clean `receiver_lane.kicad_sch` and one `driver_channel.kicad_sch` (styled via Option A or B).
   * Instantiate `receiver_lane.kicad_sch` ×4 on `receiver.kicad_sch` and `driver_channel.kicad_sch` ×8 on `driver.kicad_sch` using `hierarchical_label` + `sheet` `pin`s.
   * Re-run the `topology signature` gate (ignoring hierarchical net prefix renames, comparing `(ref, pin)` connectivity sets—note: update refdes mapping if KiCad re-annotates sheet instances) and `ERC = 0/0`.
2. **Path C2 — Code-First Parametric Modules via [atopile](https://github.com/atopile/atopile):**
   * Define `ReceiverLane` and `DriverChannel` as reusable `.ato` modules and compile directly to KiCad, eliminating manual sheet stamping for future board revisions.

**Exit criteria:** Edits to one lane/channel propagate to all 4×/8× instances with `ERC = 0/0` and unchanged netlist connectivity.

---

## 3. Recommended Decision Flow

| Step | Action | Escalate If… |
|---|---|---|
| **1** | Run **Pre-Flight** + **Option A** on `PEN1` (`U104` cluster) | SVG bbox linter still flags wire crossings after 2 helper tweaks → **Switch to Option B (`elkjs`)** |
| **2** | Stamp `PEN2` / `REF_COIL` and verify in parallel with Vision Critic subagents | Cross-lane maintenance or 8× driver channel edits feel brittle → **Schedule Option C1 (Hierarchical Sheets)** as a dedicated PR |

---

## 4. Copy-Paste Handoff Prompt for DeepSeek-V4.1-Flash-1017 in OpenCode

```text
You are the orchestrator (DeepSeek-V4.1-Flash-1017) in OpenCode for removing label islands on BRD-01 (starting with receiver.kicad_sch PEN1 lane). Do NOT use Konnect MCP for schematic drafting (headless GetOpenDocuments is unhandled).

PRE-FLIGHT:
1. Stale rebase instruction (see Status): re-check HEAD against `lamdesktop/main` before any sync; keep machine-local opencode.json paths out of hardware commits.
2. Pin golden baseline before editing: export /tmp/opencode/before.xml and /tmp/opencode/erc_before.json via `kicad-cli`.
3. Set up subagent roles (via oh-my-opencode-slim / .opencode/agents/):
   - Geometry Worker: Python + kiutils (+ elkjs if needed).
   - Gate Runner: kicad-cli netlist topology diff + ERC 0/0 + open-pin audit + SVG bbox overlap linter.
   - Vision Critic: multimodal model inspecting ONLY block-cropped 200 dpi PNGs against a 5-point rubric (no text-on-wire, labels point away from block, single +/-12VA rails, differential symmetry, readability).

EXECUTE OPTION A (escalate to OPTION B elkjs if wire crossings persist):
1. Graduate /tmp/bgen.py to `tools/kicad_sch_helper.py` using `kiutils` (SCM-friendly diffs). Enforce:
   - 1.27 mm grid snapping.
   - 5.08 mm horizontal exit from U104 +IN/-IN -> dog-leg vertical fan-out to >=10.16 mm row pitch.
   - Single horizontal +12VA (top) and -12VA (bottom) clamp rails with 1 power symbol per rail.
   - World-space angle=0 role-typed field placement (diodes hide Value, Ref 5.08 mm outside) + semantic label justification away from block.
2. The proposed SVG overlap linter (`kicad_sch_audit.py`) is **not written**; use `tools/kicad_sch_helper.py audit`, `tools/kicad_span_report.py` and a visual SVG check before rendering PNGs.
3. Wave 1 (PEN1 Template): Rewire U104, R101-R105, C113-C114, D101-D104. Pass all Tier 1 gates (topology == before.xml, ERC 0/0, open-pin audit, SVG bbox 0 overlaps), then pass Tier 2 (cropped 200 dpi Vision Critic). Commit in d0d2c48 format.
4. Wave 2 (Stamp & Parallel Verify): Stamp sibling receiver lanes by (dx, dy) translation, run Tier 1 gates, and dispatch parallel Vision Critic subagents (1 cropped PNG per worker). Commit each verified block.
```

# BRD-01 schematic layout rules — allocate, then place, then wire

**Audience:** any agent editing a BRD-01 `.kicad_sch`. **Authority:** the netlist and the
200 dpi render, not the existing drawing. This document orders the work; it does not
change any circuit decision.

## 1. Why this exists

Minimise-movement wiring keeps accidental historical placement and pushes long spans from
one net into another instead of removing them. On the receiver sheet, closing
`PEN2_AMP` shrank its pin span from 410.21 × 8.89 mm to 24.13 × 2.54 mm but grew the
neighbouring `FDA2_P` from **203.20 × 5.08 mm to 496.57 × 6.35 mm** (`hw/receiver-frontends`
commit `136004f`; the same pattern grew `FDA3_P` from 203.20 × 6.35 mm to 496.57 × 6.35 mm
in `d0d2c48`): the net list improved on paper while the drawing got worse.

## 2. The procedure, in order, with a gate between each step

Constants for every step: grid **G = 1.27 mm**; routing channel **C = 5.08 mm** (4 G);
sheet frame inset **10.16 mm** (8 G); maximum in-block label hop **25.4 mm** (20 G).
Snap every coordinate inward to G. All schematic edits go through
`tools/kicad_sch_helper.py` — "no raw `.kicad_sch` coordinate guessing" is already a
locked team rule (`docs/phase2/brd01_full_board_deepseek_handoff.md` §1.1).

Paper sizes come from the `(paper …)` header of each sheet; page numbers from
`hardware/brd-01/kicad/README.md` (sheet index):

| Sheet file | `(paper …)` | Size W × H (mm) | Page | Block inventory (handoff §4 W3-A…D) |
|---|---|---|---|---|
| `hardware/brd-01/kicad/brd-01.kicad_sch` | A4 | 297 × 210 | 1 | root sheet pins only; no parts to allocate |
| `hardware/brd-01/kicad/power.kicad_sch` | A1 portrait | 594 × 841 | 2 | recorded `hw/power-redraw` blocks; do not renumber them |
| `hardware/brd-01/kicad/driver.kicad_sch` | User 841 1320 | 841 × 1320 | 3 | DAC + Filter; 8× Current Loops; Summer + Comparators; E-stop |
| `hardware/brd-01/kicad/receiver.kicad_sch` | A1 | 841 × 594 | 4 | Input Protection; Front-End Gain; ADC + Ref + Clock |
| `hardware/brd-01/kicad/fpga.kicad_sch` | A2 | 594 × 420 | 5 | FPGA Power/Decoupling; ADC/DAC Interfaces; Config/USB-UART/Clock; Safety/Pico |
| `hardware/brd-01/kicad/connectors.kicad_sch` | A3 | 420 × 297 | 6 | FG headers; pen panels + harnesses; reference/Pico headers; USB-C + ESD |

Sheet names, cross-sheet nets and the direction of each boundary are in
`docs/handoff/brd01_io_handoff.md` §1, §5 and §6; use those, not a guess, for what enters
and leaves a sheet.

### Step 1 — Allocate (before placing anything)

1. Write the sheet's W, H from the table above. Frame = `(10.16, 10.16, W−10.16, H−10.16)`.
2. Flow axis: `W > H` → x (left to right); `H > W` → y (top to bottom).
3. Take the block list from the inventory table above. For N sequential blocks, divide
   the frame into N equal slices **along the flow axis**; subtract 5.08 mm from the
   trailing edge of every slice except the last. Snap each boundary inward to G.
4. For repeated lanes inside a block (8 current loops, Ch1–Ch3 front ends, 8 comparators),
   divide the perpendicular axis into as many equal lanes as there are repeats, again
   with 5.08 mm between lanes.
5. Write one line per block: `ID | (x1,y1,x2,y2) | parts (refs) | nets kept local`.
   Contents are taken from the netlist (`kicad-cli sch export netlist --format kicadxml`)
   and from `python3 tools/kicad_sch_helper.py list SHEET --bbox x1,y1,x2,y2`; nothing is
   assigned to a block that is not on that line.

**Gate 1:** every rectangle is inside the frame; every coordinate is a multiple of 1.27;
for any two blocks either `a.x2 + 5.08 ≤ b.x1` or `a.y2 + 5.08 ≤ b.y1`; every part on the
sheet appears on exactly one contents line. If any test fails, redo the allocation. Do
not place a symbol yet.

### Step 2 — Map the signal flow (the step that was being skipped)

1. Axis x: signals enter at `x1`, leave at `x2`. Axis y: enter at `y1`, leave at `y2`.
2. Write, for the block: `in: <net list>`, `out: <net list>`, then `order: <ref>, <ref>, …`
   along the flow axis, from entry edge to exit edge. Use the sheet flow in
   `docs/handoff/brd01_io_handoff.md` §6 (for example the receiver is
   pen/REF → INA163 → ADA4940-2 → AD7768-4 → FPGA).
3. Construct the order from netlist adjacency: two parts sharing a local net are adjacent
   in the list; protection and series parts come first immediately inside the entry edge;
   a test point on an output comes last. Every ref in the block's Step 1 contents appears
   exactly once.

**Gate 2:** each in/out net is attached to a pin of a part at the corresponding edge of
the order; no two adjacent parts in the order are separated by an unrelated part; the
order contains every allocated ref once. If it fails, fix the order before placing.

### Step 3 — Place

Using only helper verbs that exist — `move`, `textpos`, `setrot`, `label`, `glabel`,
`power`, `box`, `nc`, with `list` and `pins` for inventory — put every symbol and then
every label at its planned coordinate.

1. Symbols: walk the Step 2 order and give each part successive grid positions inside the
   rectangle, spacing = largest whole multiple of G that fits `n+1` slots between the two
   edges. Pin rows of repeated lanes line up on the same y (x-axis flow) or x (y-axis flow).
2. Rails: horizontal, at the top of the block for positive rails and below the served pin
   for GND; place with `power`/`glabel`. A decoupling capacitor goes immediately beside
   (one G in the flow direction from) the pin it serves, moved with `move`.
3. Connectors sit on the block's entry edge; series resistors, ESD and coupling parts sit
   in the first inboard grid column; labels point outward, away from the block.
4. Draw the block outline with `box --from x1,y1 --to x2,y2 --title <ID>`.

**Gate 3:** `python3 tools/kicad_sch_helper.py list SHEET --bbox x1,y1,x2,y2` shows every
allocated ref inside its rectangle; `python3 tools/kicad_sch_helper.py audit SHEET --bbox x1,y1,x2,y2`
reports zero symbols off the 1.27 mm grid and zero wire ends off grid;
`pins SHEET --refs …` shows every pin on grid after de-duplication by `(ref, pin)` (see §3).
If not, move parts now; no wire exists yet.

### Step 4 — Placement review, before any wire exists

For a fresh block the sheet has no wires in it, so render it directly. For a rework,
render a copy with wires stripped:

```bash
COPY=/tmp/opencode/<sheet>-placement.kicad_sch
cp hardware/brd-01/kicad/<sheet>.kicad_sch "$COPY"
WIRES=$(python3 tools/kicad_sch_helper.py list "$COPY" --bbox 0,0,W,H \
        | awk '$1=="WIRE"{print $NF}' | paste -sd, -)
python3 tools/kicad_sch_helper.py del "$COPY" --uuids "$WIRES" --apply
kicad-cli sch export pdf -o /tmp/opencode/<block>-placement.pdf "$COPY"
pdftoppm -png -r 200 -singlefile /tmp/opencode/<block>-placement.pdf /tmp/opencode/<block>-placement
```

Open the PNG and look at the block. The check is four questions: is any part in the path
of the flow? does any reference or value text collide? is there a clear horizontal or
vertical channel between rows? can you read the block's function from the drawing alone?
Answers must be **no, no, yes, yes**.

**Gate 4:** if any answer is wrong, go back to Step 3 and fix placement. Do **not** start
wiring to work around a placement fault. Recording "ERC 0" here is not a pass: there are
no wires yet.

### Step 5 — Wire, only now

Take exact pin ends from `python3 tools/kicad_sch_helper.py pins SHEET --refs …`; place
wire ends there with `wire`, make each run horizontal or vertical (one coordinate equal at
both ends), and use `junction` where a wire end lands on another wire's interior. Use
`label`/`glabel` only where a direct wire would exceed 25.4 mm; a longer hop is a Step 2
or Step 3 failure, not a label problem. `setpt` repairs an existing end onto a pin;
`delwire`, `delat` and `del` remove superseded wiring. A wire crossing a pin mid-span does
not connect in KiCad (helper docstring) — every connection is pin-end to pin-end.

**Gate 5:** `audit SHEET --bbox x1,y1,x2,y2` reports no hanging wire ends, no labels off
wire or pin, and an open-pin count equal to the pre-existing NC/DNC count; export netlists
before and after (`kicad-cli sch export netlist --format kicadxml -o …`) and run
`python3 tools/kicad_netlist_compare.py before.xml after.xml` — connectivity and part set
must be unchanged (intended net-name renames only).

### Step 6 — Wire review

Export the finished sheet at 200 dpi (`kicad-cli sch export pdf --pages <page> -o …`, then
`pdftoppm -png -r 200`) and view it.

**Gate 6:** no wire crosses a symbol body; no wire passes a pin mid-span; no label
overprints a symbol. If any check fails, return to Step 3 — a wire collision is
normally a placement collision — then repeat Steps 4–6. Finish with
`python3 tools/kicad_sch_helper.py audit SHEET` and full-project ERC = 0/0.

## 3. The span metric, and its trap

Measure a net's span from **pin positions**, not from label positions. Use
`tools/kicad_span_report.py`; it is the ledger for this rule, not a script to
hand-roll per block:

```bash
kicad-cli sch export netlist --format kicadxml -o /tmp/opencode/brd01.xml hardware/brd-01/kicad/brd-01.kicad_sch
python3 tools/kicad_span_report.py hardware/brd-01/kicad/receiver.kicad_sch \
    --netlist /tmp/opencode/brd01.xml --sheet /receiver/
```

Net membership comes from the kicadxml netlist and coordinates from
`tools/kicad_sch_helper.py`, but the tool is **unit-aware**: each pin of a
multi-unit part is counted once, at the unit that declares it. Calling the
helper's `instances()` directly emits every pin at every unit and
double-counts U105/U108, so do not use that output as a span ledger. Rails are
excluded by default (`GND`, `+`/`-` supplies and `power:` symbol values); the
excluded count is printed and `--include-rails` shows them — a distributed
rail such as `/driver/BUFFER_VMID` spans the whole board by design and cannot
be closed by one block. Span = `(max x − min x) × (max y − min y)` mm; the sum
rule uses **S = width + height** (the convention of `hw/receiver-frontends`
commit `ff7e52e`). `--sheet /receiver/` filters by the netlist's `<sheetpath>`;
nets with pins on more than one sheet are marked `CROSS` rather than being
attributed to one sheet.

Before and after a block, run the gate on a plain copy of the old sheet (the
tool is read-only; it never writes a schematic):

```bash
python3 tools/kicad_span_report.py --compare /tmp/opencode/before.receiver.kicad_sch \
    hardware/brd-01/kicad/receiver.kicad_sch \
    --netlist-before /tmp/opencode/before.xml --netlist-after /tmp/opencode/brd01.xml \
    --sheet /receiver/ --fail-on-regression
```

`--compare` classifies every net in both revisions as improved / unchanged /
worsened, prints `before -> after`, and **always prints a regressed net even
when the total improves**. `--tolerance MM` allows a small per-net delta;
`--json` emits the same data for scripts.

The trap: **a span can be reduced by moving the problem, not solving it.** In `136004f`,
moving R548 from x = 486.41 to 100.33 beside U106 cut `PEN2_AMP` from 410.21 × 8.89 mm to
24.13 × 2.54 mm, but the far pins of `FDA2_P` (U108.24 and R550.2) stayed at
x = 397.51 / 600.71 while the label hop moved to x = 104.14 — so `FDA2_P` grew from
203.20 × 5.08 mm to 496.57 × 6.35 mm. `d0d2c48` repeated it for `FDA3_P`
(203.20 × 6.35 → 496.57 × 6.35 mm).

**Rule:** a block is done only when **ΣS over all affected nets decreases and no affected
net's S increases** (`S_after ≤ S_before` for each). A small width increase with a larger
height decrease is acceptable (commits `ff7e52e`: `AIN2−` width 144.78 → 148.59 mm but
S 520.70 → 500.38 mm). If any net regresses, the fix belongs in Step 2/3, not in a label
move. `FDA2_P` is the counter-example: the targeted net improved hugely, the block still
failed.

## 4. What "acceptable" looks like, per block type

- **IC with decoupling:** IC horizontal in the flow; cap one grid step beside the exact
  supply pin; rail label above, `power:GND` symbol directly below the cap's ground pin;
  reference/value texts outside the part outline.
- **Comparator row:** input labels on the entry edge, output on the other edge; one row
  per channel, test point at the end of the output run; all rows aligned on the same y.
- **Connector block:** connector on the block edge; ESD and series parts immediately
  inboard in the first grid column; net labels outward, clear of the symbol body.
- **Divider:** stacked vertically, top rail above the upper resistor, GND below the lower;
  the tap label at the midpoint between them, on a short wire stub.

## 5. The checklist (paste one per block into the lead's report)

```
- [ ] Block <ID> on <sheet>, page <N>: rectangle <x1,y1,x2,y2>, contents <refs/nets> written before placement (Step 1, Gate 1)
- [ ] Signal flow mapped: in <nets>, out <nets>, order <refs> (Step 2, Gate 2)
- [ ] All parts/labels/rails/connector placed on the 1.27 mm grid; `list`/`audit` clean (Step 3, Gate 3)
- [ ] 200 dpi placement render viewed with wires excluded: no part in the flow path, no text collision, clear channel, readable function (Step 4, Gate 4)
- [ ] Wires added pin-end to pin-end; junctions where needed; no in-block label hop >25.4 mm (Step 5, Gate 5)
- [ ] 200 dpi wire render viewed: no wire through a symbol, no wire past a pin mid-span, no label overprint (Step 6, Gate 6)
- [ ] Span ledger: ΣS before <…> -> after <…>; worst individual net <name> <before> -> <after>; no net increased
- [ ] Netlist compare: connectivity/parts unchanged; ERC 0 errors / 0 warnings
```

## 6. What is explicitly NOT a layout decision

These need the block owner or integrator, not a layout commit:

- **Grounding policy** — chassis/shield bond, star point, analog/digital separation.
  `docs/handoff/brd01_io_handoff.md` §7 lists the unbonded `/connectors/CHASSIS` net as an
  open item; a `move` or `wire` does not settle it.
- **Reference designator assignment** — refs are identity; renumbering is a separate
  decision, not a way to make text fit.
- **Part value changes** — e.g. Ch2 gain values and Ch3 population, open in
  `hardware/brd-01/kicad/README.md`, or any BOM substitution (`setvalue` is not a layout
  tool).
- **Sheet partitioning across the hierarchy** — which net is local, global or a
  hierarchical sheet pin; that changes the contract boundary and its owner.

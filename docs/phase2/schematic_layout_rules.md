# BRD-01 schematic layout rules — allocate → flow → place → review → wire → review → full review → loop

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

## 2. The procedure, in order, with a gate between each step and a loop back

Constants for every step: grid **G = 1.27 mm**; routing channel **C = 5.08 mm** (4 G);
sheet frame inset **10.16 mm** (8 G); maximum in-block label hop **25.4 mm** (20 G).
Snap every coordinate inward to G. All schematic edits go through
`tools/kicad_sch_helper.py` — "no raw `.kicad_sch` coordinate guessing" is already a
locked team rule (`docs/phase2/brd01_full_board_deepseek_handoff.md` §1 item 1).

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
no wires yet. Then run the §3 measurement gate on this block — keep a before copy of the
sheet plus its netlist and run `kicad_span_report.py --compare --fail-on-regression`
(command in §3). Placement is not accepted until ΣS decreases with **no** affected net's
S increasing; if it fails, return to Step 2/3, not to a label move.

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
`python3 tools/kicad_sch_helper.py audit SHEET`, full-project ERC = 0/0, and a second run
of the §3 `kicad_span_report.py --compare --fail-on-regression` gate: wiring must not
undo the span win accepted at Gate 4. Only then dispatch Step 7.

### Step 7 — Full schematic review (three independent models)

This is the sheet-level gate: it reviews the whole rendered sheet against
`docs/phase2/schematic_review_prompt.md`, including notes, title block, net names and
cross-sheet consistency — things Gates 4 and 6 do not cover.

1. Export the complete sheet at 200 dpi (`kicad-cli sch export pdf --pages <page> -o …`,
   then `pdftoppm -png -r 200`) and attach the PNG(s) plus the `.kicad_sch`.
2. Fill the prompt's **Sheet context** block for this sheet, then send the exact prompt
   verbatim to each of these three reviewer models, with no hint about expected findings:
   - `opencode-go/muse-spark-1.3-contributor`
   - `opencode-go/hy4-flash-free`
   - `opencode-go/deepseek-v4.1-flash`
3. Each reply must contain a findings table, the three named change lists, and exactly
   one verdict line (`VERDICT: APPROVE` / `VERDICT: APPROVE WITH NOTES` / `VERDICT: REJECT`).
   Copy every finding into the lead's report with its block ID, refdes, net and severity;
   mark a challenge to a deliberate decision `[DECISION]` and a drafting defect
   `[DRAFTING]` (§6).

**Gate 7 (pass rule):** the sheet passes only if **2 of the 3** models return `APPROVE` or
`APPROVE WITH NOTES` *and* no blocking finding from any reviewer remains open. A single
blocking finding is still resolved before sign-off; it is not downgraded to a note. A
`REJECT` from any model overrides this majority and invokes the hard reset below.

**Loop-back rule — the review decides which stage to re-enter.** Re-enter the **earliest**
stage implicated by the findings and re-run every gate from there through Gate 7; do not
patch a finding on top of a finished drawing.

| Finding class (prompt section) | Re-enter | Then |
|---|---|---|
| Placement / layout (L1–L9): flow direction, block separation, grouping, alignment, repeated cells, density, text placement | **Step 1 allocate** if a block boundary, flow axis or routing channel is wrong; otherwise **Step 3 place** | Repeat 3 → 4 (placement render + span gate) → 5 → 6 → 7 |
| Wiring (W1–W9): pin ends, wire over symbol/pin, junctions, label hops, NCs, pairs, sense taps | **Step 5 wire** | Repeat 5 → 6 → 7. If the wiring fault is a placement collision, go to Step 3 instead |
| Labelling (N1–N7): naming, perspective, off-sheet names, notes, title block, rails | **Step 3 place** (where the text and label physically sit and what it says is decided) | Repeat 3 → 4 → 5 → 6 → 7; re-wire only if moving the label breaks a run |
| `[DECISION]` — a deliberate decision in the prompt's Sheet context | Owner / integrator per §6, not a layout patch | Record the owner's ruling in the prompt context, then re-run Step 7 |

**Hard reset:** if any reviewer returns `REJECT`, **or** a majority of the three report
blocking findings, the block goes back to **Step 1 allocate**, not to a patch on the
finished drawing. Re-derive the rectangles and signal order, then run Steps 2–7 again.
Labelling-only or wiring-only fixes are never an excuse to skip the placement review.

Every iteration re-runs the §3 span gate at Gates 4 and 6 and records the iteration in the
§5 ledger.

## 3. The span metric: two classes, two totals, one narrow gate

Measure a net's span from **pin positions**, not from label positions. Use
`tools/kicad_span_report.py`; it is the ledger for this rule, not a script to
hand-roll per block:

```bash
kicad-cli sch export netlist --format kicadxml -o /tmp/opencode/brd01.xml hardware/brd-01/kicad/brd-01.kicad_sch
python3 tools/kicad_span_report.py hardware/brd-01/kicad/receiver.kicad_sch \
    --netlist /tmp/opencode/brd01.xml --sheet /receiver/ \
    --blocks /tmp/opencode/receiver.blocks.csv --hubs U101,ADC_VCM
```

Net membership comes from the kicadxml netlist and coordinates from
`tools/kicad_sch_helper.py`, but the tool is **unit-aware**: each pin of a
multi-unit part is counted once, at the unit that declares it. Calling the
helper's `instances()` directly emits every pin at every unit and
double-counts U105/U108, so do not use that output as a span ledger. Rails are
excluded by default (`GND`, `+`/`-` supplies and `power:` symbol values); the
excluded count is printed and `--include-rails` shows them — a distributed
rail such as `/driver/BUFFER_VMID` spans the whole board by design and cannot
be closed by one block. Span = `(max x − min x) × (max y − min y)` mm; each
section totals **S = width + height** (the convention of `hw/receiver-frontends`
commit `ff7e52e`). `--sheet /receiver/` filters by the netlist's `<sheetpath>`;
nets with pins on more than one sheet are marked `CROSS` rather than being
attributed to one sheet.

**Blocks are explicit.** `--blocks FILE` takes either a JSON list of
`{"name", "x0", "y0", "x1", "y1"}` objects (or `name: [x0,y0,x1,y1]`) or the
plain CSV form `name x0,y0,x1,y1` with `#` comments. Use the rectangles written
down in Step 1, e.g. for the receiver (`hw/relayout-receiver`):

```
R1 447.04,25.40,814.07,568.96   # ADC + reference + FDA
R2 25.40,25.40,434.34,200.66    # Ch0/Ch1 front end
R3 25.40,213.36,434.34,393.70   # Ch2 pen 2 front end
R4 25.40,406.40,434.34,568.96   # Ch3 reference-coil front end
```

If `--blocks` is omitted the tool **infers** blocks by clustering symbol
origins on each axis and splitting where the gap is ≥ 12.7 mm (cross-product
of x and y clusters, padded by half the gap so pins on the edge are included),
and the header says `blocks: inferred ...`. Inferred blocks are convenient for
a quick look but are sensitive to whole-sheet moves such as a rotation; use
declared blocks for a before/after gate.

A net is **in-block** when every pin whose part is on the sheet under review
lies in one allocated rectangle; it is **cross-block** when its on-sheet pins
touch two or more. Pins of parts on other sheets never assign a block here.
The two classes print as separate sections with separate S totals:

- **in-block** — `net, w × h, S, pins, block`; a net with `w > 25.4` or
  `h > 25.4` is flagged `W6-HOP`. This is the drafting defect reviewers care
  about: W6 of the review prompt forbids an *in-block* label hop over ~25.4 mm.
- **cross-block** — `net, w × h, S, blocks touched`. Cross-block span is
  reported, never flagged: four channels sharing one AD7768-4 (U101) cannot
  all reach the hub with zero hops. `--hubs U101,ADC_VCM` names hub refs and
  nets; a cross-block net that reaches a hub pin, the hub's block, or a named
  hub net prints `INFO (shared-hub cross-block)` instead of a warning.

Before and after a block, run the gate on a plain copy of the old sheet (the
tool is read-only; it never writes a schematic):

```bash
python3 tools/kicad_span_report.py --compare /tmp/opencode/before.receiver.kicad_sch \
    hardware/brd-01/kicad/receiver.kicad_sch \
    --netlist-before /tmp/opencode/before.xml --netlist-after /tmp/opencode/brd01.xml \
    --sheet /receiver/ --blocks /tmp/opencode/receiver.blocks.csv \
    --hubs U101,ADC_VCM --fail-on-regression
```

`--compare` classifies every net in both revisions as improved / unchanged /
worsened, prints `before -> after`, and **always prints a regressed net even
when the total improves**. `--tolerance MM` allows a small per-net delta;
`--top` never hides a gated or moved net; `--json` emits the same data for
scripts.

**The gate is deliberately narrow.** `--fail-on-regression` exits 1 only when
(a) an **in-block** net's S increases beyond tolerance, or (b) a **new**
in-block hop above 25.4 mm appears that was not there before. Cross-block
growth never fails — that is the expected cost of routing to a shared hub.
The summary line prints `in-block regressions == N` (the number that decides
the gate) alongside the ungated cross-block count, and `--help` states the
same rule. To keep the relaxation honest, **any net whose block membership
changes prints `MOVED BLOCK` before→after, whether the gate fails or not**;
a net migrating from in-block to cross-block is itself a finding.

The trap has not gone away: **a span can be reduced by moving the problem, not
solving it.** In `136004f`, moving R548 from x = 486.41 to 100.33 beside U106
cut `PEN2_AMP` from 410.21 × 8.89 mm to 24.13 × 2.54 mm, but the far pins of
`FDA2_P` (U108.24 and R550.2) stayed at x = 397.51 / 600.71 while the label
hop moved to x = 104.14 — so `FDA2_P` grew from 203.20 × 5.08 mm to
496.57 × 6.35 mm. `d0d2c48` repeated it for `FDA3_P`
(203.20 × 6.35 → 496.57 × 6.35 mm).

**Rule:** a block is done only when the in-block ΣS decreases, no in-block
net's S increases, and no new in-block W6 hop appears. A small width increase
with a larger height decrease is acceptable (commits `ff7e52e`: `AIN2−` width
144.78 → 148.59 mm but S 520.70 → 500.38 mm). Cross-block growth to a declared
hub is acceptable and logged as INFO, with the `MOVED BLOCK` lines kept as the
record of the trade. If an in-block net regresses, the fix belongs in Step 2/3,
not in a label move. `FDA2_P` is the counter-example: the targeted net improved
hugely, the block still failed.

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
- [ ] Span gate at Gate 4: `kicad_span_report.py --compare --fail-on-regression`, ΣS down, no net up
- [ ] Wires added pin-end to pin-end; junctions where needed; no in-block label hop >25.4 mm (Step 5, Gate 5)
- [ ] 200 dpi wire render viewed: no wire through a symbol, no wire past a pin mid-span, no label overprint (Step 6, Gate 6)
- [ ] Span gate repeated at Gate 6: still ΣS down, no net regressed by wiring
- [ ] Span ledger: in-block ΣS before <…> -> after <…>; in-block regressions == 0; no new W6 hop >25.4 mm; cross-block/hub growth and MOVED BLOCK lines reviewed; worst individual net <name> <before> -> <after>; no net increased
- [ ] Netlist compare: connectivity/parts unchanged; ERC 0 errors / 0 warnings
- [ ] Step 7: three reviewer verdicts recorded from `schematic_review_prompt.md`; 2/3 pass and no open blocking finding; findings mapped to a re-entry stage (Gate 7)
```

Loop ledger — one row per iteration of the block:

```
| iteration | re-entered stage | findings (ref/net, severity, [DECISION]/[DRAFTING]) | ΣS before -> after | Gate 7 verdicts | next stage |
| 1 | ... | ... | ... | ... | ... |
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

A Step 7 finding marked `[DECISION]` belongs to one of these owners. Record the ruling in
the prompt's Sheet context and re-run Step 7; do not silently "fix" it as drafting.

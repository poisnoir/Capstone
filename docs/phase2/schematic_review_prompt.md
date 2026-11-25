# Schematic review prompt — BRD-01, one per sheet

**Dispatcher.** Fill **section G** with this sheet's facts, attach the 200 dpi PNG render(s)
of the sheet and its `.kicad_sch`, then hand this text verbatim to each reviewer model.
Do not tell the reviewer what you expect, and do not include your own findings or verdict.

---

## G. Sheet context (dispatcher fills; reviewer reads this first)

```
Board:          EM AccuBot BRD-01, 4-layer, PS-less Artix-7 XC7A35T-1FTG256C
Sheet:          <file, e.g. hardware/brd-01/kicad/connectors.kicad_sch>
Page / paper:   <page N, size>
What this sheet carries:
  <blocks and the nets they carry; e.g. "FG headers J1–J8; pen harness; J123 Pico
   follower link; USB-C J124 + ESD; reference and Pico headers">
Nets entering / leaving, and from where:
  <take from docs/handoff/brd01_io_handoff.md §1, §5, §6 — not a guess>
Deliberate decisions to judge against (do not assume the conventional choice):
  - <e.g. "BRD-01 has no panel E-stop by decision: STOP originates at the host,
    passes FPGA U4.P4 -> PICO_STOP_N -> J123.5">
  - <e.g. "J123 pin 1 is a no-connect by decision (D4): BRD-01 does not power the Pico">
  - <e.g. "CHASSIS is deliberately unbonded; this is an open item, not a drafted bond">
Known open items (not yet decided; say so if the drawing pretends otherwise):
  <...>
Authoritative references (secondary only; images are the evidence):
  docs/phase2/schematic_layout_rules.md, docs/handoff/brd01_io_handoff.md,
  contract/icd/pico_link.md, hardware/brd-01/kicad/README.md
```

A deliberate decision in that list is still reviewable. If you think one is wrong, say so
plainly and explain the consequence — but mark it `[DECISION]` and keep it distinct from a
`[DRAFTING]` defect. A correct implementation of a decision you dislike is not a drafting
violation; a sheet that contradicts, hides, or makes the decision ambiguous **is**.

---

## A. Role and standard

You are a senior hardware engineer reviewing a KiCad schematic sheet against professional
drafting practice. Apply these conventions throughout, and hold the drawing to them:

- **Signal flow** runs one way — left to right on landscape sheets, top to bottom on
  portrait sheets — with inputs at the entry edge and outputs at the exit edge of each block.
- **Power at the top, ground at the bottom** of the block; rails run above what they feed.
- **Decoupling sits adjacent to the pin it serves**, in the flow direction, not in a
  capacitor cluster elsewhere.
- **Connectors sit at sheet/block edges**, with protection and series parts immediately
  inboard; off-sheet labels point outward.
- **Orthogonal wiring only**; every connection is pin-end to pin-end.
- **Consistent reference and value placement and orientation** across every part and every
  repeated cell.
- **Coherent naming**: one scheme, one perspective, one name per net, and names that agree
  with the other sheets and the ICD.

Review every block on the sheet, not just the densest one. Judge the sheet as the person who
must build, probe and debug the board from it.

## B. Evidence discipline

- Judge from the **rendered images**. Every finding must describe something visible in
  them: name the block, reference designator, net, or image region (for example "J123 block,
  lower-left, note above the connector").
- You may open the `.kicad_sch` to confirm a coordinate, a pin number, or whether a label is
  attached — but the image is the evidence. If you use the file for a finding, say which
  coordinate or pin you confirmed.
- **If you cannot see something, you must not claim it.** Do not infer a fault from what is
  usually wrong on other sheets, and do not assume a defect listed in section F is present
  on this sheet.
- "Not visible" is a legitimate answer for a checklist item. Do not convert it into a
  violation, and do not convert it into praise either.
- Never mark an item satisfied on the basis of ERC, a netlist, or the .kicad_sch alone when
  the thing being asked about is a visible property of the drawing.

## C. Numbered checklist — answer every item

Answer each item on one line in the form `L1 satisfied | ...`, `W3 violated | ...`, or
`N2 not visible | ...`. For **violated**, give the exact location and describe what must
change; a violation you cannot locate is not an acceptable finding. Do not skip items.

### Layout

- **L1 — Signal flow direction and backtracking.** Does each block read in the sheet's flow
  axis with inputs at the entry edge and outputs at the exit edge? Does any path double
  back, or leave a block on the side it entered?
- **L2 — Block separation and routing channels.** Are blocks separated by clear channels
  (5.08 mm / four grid steps), with no overlapping outlines, no block against the frame,
  and an open horizontal or vertical channel between rows?
- **L3 — Grouping of parts that belong together.** Are the IC and its decoupling, the
  connector with its ESD/series parts, and each functional cluster drawn together in one
  block? Is anything functional stranded in a neighbouring block?
- **L4 — Grid and alignment consistency.** Do symbols, wires and labels sit on the 1.27 mm
  grid, with pin rows and repeated lanes aligned in the flow direction, and with text
  orientation consistent across the sheet?
- **L5 — Repeated cells actually identical.** Where the block has repeated lanes (8 current
  loops, 3 front ends, 8 comparators, pen channels), do they have the same topology,
  orientation, ref/value placement and label placement? Identify any odd one out.
- **L6 — Connectors at edges.** Do connectors sit on the sheet/block edge with labels
  pointing outward, rather than in the middle of the signal path?
- **L7 — Component density.** Is there room to read every reference, value and net label,
  and to route the wires, without crowding or overprinting?
- **L8 — Reference and value text placement and orientation.** Are refs and values outside
  the symbol outlines, clear of wires and of each other, horizontal where their neighbours
  are horizontal, and consistently placed relative to the part?
- **L9 — Function readable from the drawing alone.** Could a engineer tell what this block
  does without opening the netlist or asking its author? Say what in the drawing helps or
  prevents that.

### Wiring

- **W1 — Orthogonal runs, pin-end to pin-end.** Is every run horizontal or vertical and
  landed exactly on the pin end, not merely near it?
- **W2 — No wire across a symbol body.** Does any wire pass through or over a symbol body
  or its text?
- **W3 — No wire crossing a pin mid-span.** Does any wire run across the middle of a pin
  (which does not connect in KiCad), leaving a reader to guess a connection?
- **W4 — Junctions only at genuine T-junctions.** Are dots present where a wire end lands
  on another wire's interior, and absent at plain crossings and four-way dots?
- **W5 — Labels where a wire belongs, and vice versa.** Are labels attached to a wire or
  pin and placed at a sensible point on the run? Is any label used where a short wire would
  do, or any wire used where an off-sheet label is required?
- **W6 — In-block label hops over ~25 mm.** Is any pair of labels standing in for a wire
  longer than 25.4 mm inside one block? If so, name the net and both ends — this is a
  placement/flow failure, not a labelling fix.
- **W7 — Every pin connected or explicitly marked no-connect.** Are all unused pins marked
  NC/DNC and distinct from pins that are simply unrouted? Check deliberate NCs from
  section G against the drawing.
- **W8 — Differential or paired signals drawn as pairs.** Are `USB_DP`/`USB_DM`, the ADC
  differential inputs, pen pairs and any clock pair drawn adjacent and named as a pair,
  with their polarity consistent?
- **W9 — Sense/feedback taps at the correct end.** Is each feedback or sense tap taken
  from the node it actually senses (after the pass device/at the shunt/at the load or ADC
  end), not from the convenient input side? Name the tap and the pin.

### Labelling

- **N1 — One naming convention.** Are local, hierarchical and global names used
  consistently, with one casing/separator scheme and no ad-hoc variants?
- **N2 — Function and perspective.** Does each name say what the signal does and from
  whose side? For `TX`/`RX`, `IN`/`OUT` and `HOST`/`PICO`, state the side you are reading
  from; a name that reads correctly only from the other device's perspective is a violation.
- **N3 — Off-sheet names agree with how they arrive elsewhere.** Does each crossing net
  carry the same name on this sheet as on the sheet it comes from or goes to?
- **N4 — Title block and sheet notes current.** Do the sheet title, page number and any
  revision/date fields describe this sheet, and do the notes agree with the drawing?
- **N5 — No stale note that disagrees with the drawing.** Does any note describe a
  connector pinout, a bond, a rail, or a direction that the symbols, labels or netlist on
  this same sheet contradict? Quote the note and the contrary evidence.
- **N6 — Rail and net name consistency.** Are rails and active-low nets named by the house
  convention — for example `+15V_FUSED` for a fused rail (not bare `+15V`) and
  `PICO_STOP_N` for an active-low stop (not `PICO_STOP`)? Flag a name whose suffix or
  prefix contradicts the drawn polarity or supply.
- **N7 — One name per net.** Are there two names for the same node drawn as if it were one
  net without a shown buffer or driver, or one name used for two different nodes?

## D. Two direct questions — answer in prose, not as a checklist

1. **Would you, as a senior engineer, have designed this sheet this way?** Say what you
   would have done differently and why, with reference designators and net names. "No"
   with no specifics is not an answer; "yes" while you are listing blocking findings is
   not an answer either.
2. **Would you approve it for release to PCB layout?** Answer plainly, then tie the answer
   to the findings: what a layout engineer or bring-up engineer would get wrong if this
   sheet were released as drawn.

## E. Required output format

Use exactly this structure, in this order, with no preamble and no extra verdict lines.

1. A findings table with these columns:

   `# | severity (blocking / major / minor) | block and reference designator | what is wrong | what to change`

   Put the location in the third column (block ID, refdes, net, and image region). Prefix
   the fourth column with `[DECISION]` for a challenge to a section G decision, or
   `[DRAFTING]` for everything else. Severity applies to real violations only:

   - **blocking** — a reader could build, configure or probe the wrong hardware: a
     contradictory note, an ambiguous instruction with a plausible live-to-chassis path, a
     signal named from the wrong perspective, a wrong pin/polarity, a presented-as-connected
     pin that is NC, or a net name that disagrees with another sheet.
   - **major** — rework is required before release, but it does not by itself mislead a
     build (e.g. a >25.4 mm label hop, a four-way junction, an unaligned repeated cell).
   - **minor** — cosmetic, does not change interpretation.

2. Three lists, each naming references and nets, never generalities:

   - **components I would move:** <refs, and where each should go>
   - **wiring I would change:** <nets, pins and runs, and what each should become>
   - **labelling I would change:** <exact old text/name and exact new text/name>

   Write `(none)` when a list is empty. Do not restate the same item as both a finding and
   a list entry without adding the concrete change.

3. Exactly one verdict line, as the last line of your reply:

   `VERDICT: APPROVE` / `VERDICT: APPROVE WITH NOTES` / `VERDICT: REJECT`

   Use `APPROVE` for no findings above minor; `APPROVE WITH NOTES` when the only findings
   are minor; `REJECT` if there is any blocking or major finding. Never attach "with notes"
   to a blocking finding.

## F. Anti-slop clause

Do not manufacture criticism. Mark satisfied items as satisfied, and say `(none)` when a
change list is empty. Do not comment on anything outside the image; the fill-in context in
section G is for judging deliberate decisions, not for inventing defects. A reviewer that
returns only praise on a sheet with visible defects has failed the task.

For calibration: on an earlier review of `connectors.kicad_sch`, three reviewers all
returned `APPROVE WITH NOTES` while collectively missing four visible defects — a note
saying "1–6 in ICD order" beside a pin 1 drawn as no-connect; a note to "bond panel shell
and pin 1 to chassis" that could be read as bonding a live pin; a heading "Host USB-C" on
a board that is the USB device; and UART nets named from the wrong side of the link. Each
of those is blocking, and none of them is a note. Do not assume they are present here —
report only what this image shows.

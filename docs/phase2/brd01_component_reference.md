# BRD-01 component reference — component → pins → wires

> **⚠ STALE TABLES — DO NOT USE AS WIRING TRUTH (2026-11-26).** Every table
> below was generated from the `ef04f63` netlist. Commit `8d39a99` changed that
> netlist: `/power/BUCK1_FB` → `Net-(U144-FB)`,
> `/receiver/DREGCAP` → `Net-(U101-DREGCAP)`,
> `/receiver/FDA1_N` → `Net-(U105B--IN2)`,
> `/receiver/REF_RAW` → `Net-(U102-VOUT)`,
> `/receiver/REGCAPA` → `Net-(U101-REGCAPA)`,
> `/receiver/REGCAPB` → `Net-(U101-REGCAPB)`, and the 10 Ω ADC-reference
> filter resistor `R184` → `R186` (U103 OUT/IN- → `/receiver/ADC_REF`). Net
> names, part designators and the crossing/sheet classification below may have
> changed. Regenerate before relying on any table here:
> `kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch`.

**Provenance (2026-11-26; tables generated 2026-11-25 from base commit `ef04f63`):** generated with `kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch` (KiCad 10.0.8); the committed netlist changed at `8d39a99` (see banner), so these tables describe `ef04f63` only — regenerate before using them as wiring truth.
This is the **component-centric** reference for BRD-01. Its companion,
`brd01_wiring_manifest.md` (and `brd01_wiring_manifest.csv`), is **net-centric**:
net → pins. This document starts at a component and follows each pin to the other
ends of its wire. It does not duplicate the manifest's net tables; where a net has
more than eight ends it shows the nearest few and points to the manifest section
for that sheet.

Everything in Part 4 and Part 5 below is generated, not transcribed: the source is
`kicad-cli sch export netlist --format kicadxml -o net.xml hardware/brd-01/kicad/brd-01.kicad_sch`
(KiCad 10.0.8 Eeschema). `<comp>` supplies ref/value/footprint/libsource/sheet,
`<node>` supplies pin number, `pinfunction`, `pintype` and net membership, and
`<sheetpath names=...>` supplies the sheet. Pin coordinates for the nearest-end
ordering come from `tools/kicad_span_report.py:pin_map()`. Parts 2 and 3 are
hand-written from git history and repo evidence, as requested.

Baseline counted here: **640 components, 605 nets, 2155 node pins**; ERC was
re-run on this checkout and reports **0 errors / 0 warnings** (`Found 0
violations`). The last commit before this reference is `213ac41`
(`docs(brd-01): generate wiring manifest from netlist`).

---

## 1. Scope and method

- Part 2 is a chronological work log from `ec88cd1` to `213ac41` (97 commits),
  grouped by phase, with commit SHAs.
- Part 3 is the outstanding-work register: exactly the 13 supplied items, each
  verified against the current tree, with corrections where the supplied wording
  did not match the repo.
- Part 4 is one entry per component, grouped by sheet, ICs / modules /
  connectors / test points before passives.
- Part 5 is the per-sheet "component → its passives" check table.
- Part 6 records the count reconciliations and gate results.

---

## 2. Work log (hand-written, from git)

All SHAs below are from `git log --oneline --reverse ec88cd1..213ac41`; side-branch
work is named with its originating SHA and the merge that carried it.

### Phase 0 — power-sheet repair and redraw; D_REF clamp (`13d9b2f` → `3cb6b33`)

The starting point was the `ec88cd1` power sheet. `13d9b2f` (`pwr`) and `f4a7dc5`
(`power3`) opened the repair; `9c4a6f8` repaired the U145 +1.8 V output block with
no netlist change; `8af8d29` moved U147 pin 15 to GND per `power_tree_v2` §4;
`11abd0f` applied the §4 value strings (C800–C808, C811–C820, C180–C190,
R800–R802, bulk-polarity marks). `5ceac36` closed the cross-sheet electrical items
and `1ce6a61` converted the three crossing signals to hierarchical labels plus
root-sheet pins; `a9cbe3d` merged that stream.

The **seven-block power redraw** followed, placement-first with a netlist/ERC gate
after each block: `15055d7` block 1 (15 V input protection — CMC net was
126 × 516 mm, reduced to one wired chain at y=100.33), `2577ce8` block 2
(E-stop / arm interlock — 57 × 457 mm across five label islands joined end to
end), `4b6b8f1` merged blocks 1–2; `a72411d` and `f139b4d` did block 3 (U144/U145
soft-start and PG pull-ups), `c485a74` merged it; `fee267d` kept the verified sheet
while taking the handoff docs; `24521b9` block 4 (buck input/output caps and FB
divider), `906e607` block 5 (±12VA bulk), `d3deb72` block 6 (+3.3 V decoupling
row), `ba98c5a` block 7 (rail test points), with `c9228b1` correcting the
hierarchy/status prose and `3cb6b33` moving U5 clear of the LT3045/LT3093 set
resistors.

**D_REF / D534 clamp:** `387f90e` placed `D534` (BAS70H) across `ADC_REF` to
`+5VA` to close contract item C7; `fcfe46f` recorded the open bench item — the
clamp is compliant only while Vf ≤ 0.3 V at the actual fault current, so
V(ADC_REF) − V(+5VA) must be measured while cycling +15 V (`power_tree_v2.md:414`).
ERC does not find this; `brd01_power_v2_deepseek_handoff.md:17` says so explicitly.

### Phase 1 — signal islands, connector blocks, E-stop scope change (`8d9651b` → `e3cb835`)

Receiver label islands were closed one block at a time: `8d9651b` ADC_VCM
(block R1), `0af8e8e` INA_IN_P/N (block R2), `ff7e52e` Ch2/Ch3 ADC filter caps
(block R5), `136004f` PEN2_AMP (R3), `d0d2c48` REF_COIL_AMP (R4). Connectors got
`3614fae` (C3 USB-C/CC/ESD), `f6edcfe` (C2 Pen 1 harness) and `7aad894` (C4 Pen 2
harness); FPGA got `e7fc014` (F1 config/flash/JTAG/status TPs). `6274e8a` added
the BRD-01 I/O handoff and 256-row FPGA signal CSV.

**E-stop removed from the tracker:** `a4a18e8` inventoried scope without an
electrical change; `159b5e6` executed it. Removed: `K1`, `K2`, `D140`, `R185`,
`U143`, `R186`, `U750`, `Q750`, `R753` (nine removals), added
`U755` (74LVC1G08); `+15V_DRV` was merged unswitched into `+15V_FUSED`;
`PICO_STOP_N` was split into FPGA-side `PICO_STOP_REQ_N` (`U4.P4` + reused R754)
and arm-side `PICO_STOP_N` (`U755.4` → `J123.5`); `U4.R2` (`ESTOP_ASSERTED`)
became a no-connect. Parts went **645 → 637** (`estop_scope_change.md:349`).
`953bf86` aligned the system schematic and KiCad README, and `10a5afc` recorded
the latch retarget in the contract draft. Note that R753 was re-added by
`7e60030` (637 → 638) and R181/C191 by `1a1fc5d` (638 → 640).

`640cc62` redrew driver B4 (eight comparators + fault TPs), `1e38cab` redrew B1's
summer resistor grid (SUM_NODE span 316 → 260 mm); `b43c39e` and `e060a88`
reconciled receiver quantities and the U148→U7 proposal. Merges carrying this
work: `1e519e7` (E-stop scope), `b7ef648` (driver B4), `6adb1b4` (fpga
F1), `578097e` (receiver R1/R2), `13f3a24` (receiver R3/R4/R5), `f1cf02f`
(connectors C3), `776a334` (C2/C4), `d89181a` (I/O handoff), `4952526` (doc
corrections), `e3cb835` (driver B1).

### Phase 2 — full re-layout, placement before wiring (`52f2cfa` → `ddb06e0`)

The 7-stage loop in `schematic_layout_rules.md` became the working method:
allocate a block → map signal flow → place → **placement review with wires
excluded** → wire → **wire review** → three-model review, with a gate after every
step and a loop back to the implicated stage. `4b788f7` wrote the canonical
image-grounded review prompt (`schematic_review_prompt.md`: numbered layout /
wiring / labelling checklist, two prose questions, one `VERDICT:` line, and an
anti-slop clause); `a6d733f` merged it together with the layout rules.

Placement first: `52f2cfa` driver B1, `02b599e` receiver R1
(447.04,25.40)–(814.07,568.96), `51bb355` receiver R2
(25.40,25.40)–(434.34,200.66), `2d3a003` receiver R3
(25.40,213.36)–(434.34,393.70), `2871e8d` R1 corrective pass, `935fd1d` fpga B1
banks 14/15 + QSPI, `8aecdfb` fpga B4 core decoupling, `e72fc16` fpga B5 ADC
pull-ups, `3a16b72`/`fa58264`/`3fbd550`/`709a9a6` connector blocks C/B/D/E, then
`95dcd25` the driver's **180° flow correction**. The driver sheet was reissued
from **841 × 1320 portrait to A0 landscape** in `b44795d` (later carried by
`fdf2ff8`); `b9f0f44` placed bias caps beside U39 pins, `cf9026f` wired B1 rails,
`c5afc26` B4 trip rails/FAULT bus, `81c7e29` channel signal paths, `03f3406`
closed receiver FDA/AMP nets by placing FDA halves in their channel blocks,
`a470261` wired USB ESD at J124 and fixed the PICO_TX/RX direction note,
`88c6010` corrected ICD/UART/shield labels.

`42942fb` added the unit-aware span ledger; `63305cb` made it **block-aware**:
`tools/kicad_span_report.py` reports cross-block nets and hubs separately and
`--fail-on-regression` fails **only** on an in-block span regression or a new
in-block hop above 25.4 mm (`kicad_span_report.py:24-26`). `ddb06e0` merged it
with its self-test. The 180° driver reissue kept a known FG6_OUT +134.62 mm
in-block regression visible by instruction (`d4401b1` merge note).

### Phase 3 — acceptance audit, semantic deltas and review repairs (`4080933` → `fc72e9e`)

Two acceptance branches were audited and **discarded**: `hw/fpga-acceptance`
(`161e0ad`) and `hw/power-acceptance` (`b72cffd`) sat ~30 commits behind; taking
their sheets would have rolled back the four completed relayouts. The audit kept
only the two **semantic** changes and applied them by hand: `4080933` moved
`R163.1` from GND to +3.3 V (ADC_RESET_N pull-up) and `193f280` moved `U144.7`
FSW from `PG_1V0` to GND. The `F1` revalue from `cc28870` was **rejected** — the
symbol block stayed byte-identical and F1 kept value `0031.8201`.

**The U144 FSW regression and repair:** `193f280` was wrong. Tying FSW to GND
selects 2.5 MHz, and 1.0 V from 6 V gives a **67 ns on-time, below the 80 ns
minimum**, so the part would fold down to an uncontrolled ~2.1 MHz. `290e79c`
restored FSW to `PG_1V0`: 2.5 MHz at start-up, then **1.25 MHz (133 ns)** once
+1V0 is good (`power_tree_v2.md:481-483`). `2819f13` cleared the stale E-stop
notes. Gate results at `193f280` were all green (ERC 0/0, audit identical, span
0 regressions) — the defect was caught by a reviewer reading the datasheet, not
by a gate.

`7e60030` renamed `ARM_Q` → `ARM_Q_N` and added R753 as a STOP pull-down so the
arm stays stopped when +3.3 V is lost (637 → 638). `858fc10` fixed four FPGA
review defects and added the UG483 bypass table. `c4122de` settled the watchdog
(FPGA PL timer, no external part), Ch2 gain (= Ch1), Ch3 DNP and TRIP_REF
decisions. `efb8801` closed the legacy **GAIN\*/RG\*/INA_IN\*** label hops on the
receiver (605 nets and 640 parts unchanged, ERC 0/0); `4cd4fe0` closed the
**ARM_Q_N** latch hops and cleaned the latch text.

**The STOP-gate polarity bug:** as executed in `159b5e6`, `U755.2` was fed from
`U753.3` (`~Q`), which is high whenever the latch is cleared — so STOP was
asserted merely by arming and the intended active-low request was masked.
`fc72e9e` corrected it to `U753.5` (`Q`), renamed the net `ARM_Q_N → ARM_Q`,
moved the no-connect to `U753.3`, and wired the PG_1V0 label hop inside the U144
block. The netlist now has `/power/ARM_Q` = `U753.5` + `U755.2` and
`unconnected-(U753-~{Q}-Pad3)` = `U753.3` only. ERC and span compare stayed green
across the bug and the fix.

`03b1b42` flagged the missing FG-1 simulation report (`REPORT.md`, absent)
behind the ICNIRP claim; `213ac41` generated the wiring manifest from the netlist (MD + CSV).

### Who caught what — the pattern that matters

**Caught by a reviewer re-reading the source, not by an automated gate:**

- **STOP polarity (`U755.2` fed from `U753.~Q`)** — fixed in `fc72e9e`. ERC and
  the span compare were green before and after; neither checks gate semantics.
- **GAIN\*/RG\* label hops** — `d4401b1`'s merge note says they were "flagged in
  review" and were pre-existing, "so the new-hop gate does not catch them";
  closed in `efb8801`. `INA_IN_P/N` was closed in the same pass.
- **ARM_Q_N hop (~62 mm as reviewed)** — a label hop closed in `4cd4fe0`; again
  a review finding rather than a gate failure. (The exact 62 mm figure is a
  reviewer measurement and is not recorded in a tracked file; the closure
  itself is recorded in the `4cd4fe0` commit message.)
- **U144 FSW → GND** was caught by the datasheet limit (80 ns) in human review,
  while every gate passed at `193f280`.
- **D_REF / J123.1 contract defects** were explicitly out of ERC's reach
  (`brd01_power_v2_deepseek_handoff.md:17`).

**Caught by gates:** span regressions during placement/wiring (e.g. the
CFGBVS/MODE2 attempt discarded in `fed8a46`, SUM_NODE 316 → 260 mm in `1e38cab`,
FG6_OUT +134.62 mm kept visible in `d4401b1`), netlist membership/part-count
deltas, `kicad_sch_helper.py audit` (hanging ends, off-grid, labels off
wire/pin), and ERC. The lesson is recorded in `schematic_layout_rules.md:119`:
"Recording 'ERC 0' here is not a pass" — ERC and span gates do not prove
electrical or contract correctness.

---

## 3. Outstanding work register

Every row was checked against the tree at `213ac41`; corrections to the supplied
wording are called out in the item text.

| # | Item | Severity | What it blocks | Owner |
|---|---|---|---|---|
| 1 | **Receiver Ch2/Ch3 input lanes — CONFIRMED REAL.** `PEN2_IN_P/N`, `REF_COIL_IN_P/N`, `PEN2_PROT_P/N`, `REF_COIL_PROT_P/N` are still label-hopped: 3, 3, 4 and 4 labels per net, every label on a **5.08 mm stub**. Measured x-spans **76.20–248.92 mm** (pin spans in `kicad_span_report.py`: 76.20, 127.00, 241.30, 248.92 mm), y-spans 30.48–48.26 mm — **8 nets** in all. Correction: the supplied "33–190 mm" figures are not what is on the sheet; and "the same defect was fixed on Ch1" is only true of the GAIN/RG/INA hops (`efb8801`) — Ch1's own `PEN1_PROT_P/N` still have 4 labels on 5.08 mm stubs across 134.62 mm. These are cross-block hops, so the block-aware gate intentionally does not fail on them. | Major (drafting + reviewability; electrical connectivity is intact) | Receiver sheet sign-off at Gate 6/7; reliable review of Ch2/Ch3 input lanes | Receiver sheet owner |
| 2 | **`contract-updates` branch is local-only.** Verified: `b527659`, 8 commits ahead of and 10 behind the stated base `213ac41`, `contract/VERSION` = `2.0.0`, `contract_ci` green on that tree (`contract 2.0.0: 18 SC rows, 28 decisions, ICDs OK`). Not on main, not pushed. The E-stop scope, power tree and SC-08 arm-only STOP changes exist in `contract/` only there. Needs the `contract-change` issue → PR → two approvals → version bump/tag flow, which needs `gh` auth. | Blocking (contract and arm repo cannot pull the changes) | Contract release, arm-repo ICD update, SC-08 closure | Contract owner + interface owner and integrator |
| 3 | **Docs teach the inverted latch.** Verified: `docs/phase2/system_schematic.md:214,219-223` and `hardware/brd-01/kicad/README.md:107-108` say `U755` ANDs with `U753.~Q` (pin 3) and that `U753.Q` (pin 5) is NC. Netlist is the opposite: `/power/ARM_Q` = `U753.5` + `U755.2`; `U753.3` is `+no_connect`. Partially duplicated already in `brd01_wiring_manifest.md:1346`. | Major (safety documentation wrong) | System-schematic and README sign-off; fault-injection procedure | System-schematic / KiCad README owner |
| 4 | **Stale power narrative — CONFIRMED.** `hardware/brd-01/kicad/power-tree.md` §§2–5 carry `+15V_DRV` (lines 33, 57, 85, 129, 151, 174, 246), `+5V` (35, 59, 86–89, 245, 250), K1/K2 (32, 56, 116, 129, 136–142), `ESTOP_ASSERTED` (120, 137, 172); `docs/handoff/brd01_io_handoff.md:232` still has `+15V_DRV` and K2. None of those nets/parts exists in the netlist (`R185` now exists, but as the chassis 1M bleed in connectors). | Major (wrong power tree) | Power handoff, BOM ordering, integration | Power owner / docs owner |
| 5 | **RESOLVED by #32 (2026-11-26).** `contract/icd/pico_link.md` Rev B §2 now lists 6-pin `J123.1` as NC, matching the netlist's `unconnected-(J123-Pin_1-Pad1)` (`pintype=passive+no_connect`). BRD-01 supplies no 3V3; the Pico uses its own USB. Retained as history — no contract change remains. | Was Major (ICD wrong); now closed | Pico harness pinout, arm-repo integration | Contract owner (ICD) |
| 6 | **`TRIP_REF` threshold unresolved — CONFIRMED.** `R710` 52.3 kΩ from `+3.3V`, `R711` 10 kΩ to GND → 3.3 × 10/62.3 ≈ **0.53 V**; driver-sheet notes say **~253 mA** (positive-peak trip, 1 Ω shunt) and **~280 mA** (LMH6321 nominal clamp). `power_tree_v2.md:486-495` lists all three as unreconciled and forbids changing resistors before measurement. | Major (protection threshold unverified) | Overcurrent protection validation; driver acceptance | Power/driver owner + bench |
| 7 | **FG-1 simulation report (`REPORT.md`) absent — CONFIRMED.** `design_order.md:105` cites it for per-coil 0.83×, array 0.97× and ICNIRP 18.7 µT at 250 mA, and itself says it must be regenerated. No such file on disk and no object in any git ref (`git rev-list --all --objects | grep simulations/fg1` empty). | Blocking for the ICNIRP claim | FG-1 field/ICNIRP closure and volume gate | FG owner |
| 8 | **`D751` symbol pin names — CONFIRMED.** Netlist library part `TPD2EUSB30` has pin functions `D+_1`, `D-_2`, `GND_3`, while the pins are wired to `/connectors/USB_CC1`, `/connectors/USB_CC2`, GND. Symbol naming is misleading, connectivity is right. | Minor (review/maintenance) | Connector sheet readability; future symbol library cleanup | Connector owner |
| 9 | **`U753`/`U754` power orientation — CONFIRMED as built; trial detail not in repo.** U753 has VCC = pin 8, GND = pin 4, while U752/U754/U755 have VCC = pin 5, GND = pin 3. Deliberately deferred: a trial rotation split 7 nets (the 7-net figure is not recorded in a tracked file; no commit or doc states it). | Minor (drafting consistency) | Cosmetic cleanup only; would require a fresh netlist delta gate | Power owner (latch chain) |
| 10 | **`PG_1V0` closure crosses the U144 body — CONFIRMED geometrically.** On `power.kicad_sch` U144 sits at (304.8, 205.74); the PG_1V0 run includes the horizontal wire (294.64, 208.28) → (314.96, 208.28), which passes through the symbol. `fc72e9e` wired this hop. Conflicts with `schematic_layout_rules.md:146` (Gate 6). | Minor/moderate (drafting rule violation) | Gate 6 sign-off on power sheet | Power drafting owner |
| 11 | **Watchdog has no RTL — CONFIRMED.** `c4122de` settled it as an internal FPGA PL timer with no external part; `system_schematic.md:225-229` says so. `fpga/rtl/` contains only `.gitkeep` — nothing implements it. | Major (safety function unimplemented) | DIG-6 / FPGA implementation and stop-path validation | FPGA owner |
| 12 | **No hardware-independent stop path — CONFIRMED; reviewer count corrected.** `estop_scope_change.md:17,275-278` and `contract_change_estop_draft.md:23-25` accept the loss explicitly and require the reviewer to accept it. Every stop origin needs the FPGA (or a valid +3.3 V rail for the U755 output). The "two of three reviewers challenged it" detail is not recorded in a tracked file — the three-reviewer rule and its 2/3 pass gate are in `schematic_layout_rules.md:153-188`, but no verdict log for this decision is committed. | Major, accepted by decision | Safety case; needs explicit reviewer acceptance in the contract PR | System safety owner / integrator |
| 13 | **Ch3 reference-coil front end DNP — CONFIRMED.** `hardware/brd-01/kicad/bom-to-cad.md:204,534` and `frontend_requirements.md:47-48` state it stays in the board design but all its parts are DNP in the BOM by decision `c4122de`; do not order or fit. | Informational (decision, not defect) | BOM ordering and Ch3 population | Receiver/BOM owner |

---

## 4. Component reference (generated from the netlist)

Page 1 — root has no components; its only wiring is the two hierarchical sheet pins.

### 4.1 How to read it

- One entry per component, grouped by sheet, with ICs / modules / connectors / test points first, then transistors and diodes, then two-pin passives (R, C, L).
- `Connects to` lists the **other ends of the same net**, nearest-first by pin coordinates on the same sheet (netlist order for off-sheet pins). Nets with more than eight ends show the six nearest and the total, with a pointer to the manifest section for that sheet. A no-connect shows `no-connect (single pin)`.
- Role of a supporting passive: **primary rule** — an R/C/L is listed on a component when its supporting net (the functional net of the two, else the supply rail, else GND) touches that component's supply, set, feedback, bias or enable pin (pin name classified by the patterns in §4.1.1). Rail decoupling is attributed to every same-sheet component with a supply pin on that rail (listing is capped per component), since every rail cap otherwise applies to every IC on the board. **Secondary rule** — a passive with no primary host is attached to the nearest same-sheet component sharing one of its nets, with a filter / termination role, so that every passive has a stated host. A passive may legitimately serve more than one component (rail decoupling); it is then listed on each.
- Footprints are the netlist `<footprint>` strings. Values are netlist `<value>` strings; DNP status is a BOM decision, not a netlist property (see Part B item 13).

#### 4.1.1 Pin-role patterns (the classification rule)

| Class | Pin-name patterns | Typical role assigned |
|---|---|---|
| feedback | `FB`, `VOS`, `COMP`, `SENSE`, `PGFB`, `DEF` | feedback divider / filter |
| set | `SET`, `ILIM`, `RT`, `FSW`, `TRIM`, `GAIN`, `RG1/2`, `FORMAT`, `CLK_SEL`, `M0..M2` | gain / timing set |
| bias | `SS/TR`, `NR`, `BIAS`, `CBOOT`, `RBOOT`, `VOCM`, `VCM`, `REF`, `DREGCAP`, `CT` | soft-start / bias / reference |
| enable | `EN`, `EN/SYNC`, `EN/UV`, `MR`, `RESET`, `CLR`, `PRE`, `SHDN`, `OE`, `START`, `DISABLE`, `HALT` | enable / sequencing pull-up |
| supply | `VIN`, `VCC`, `VDD`, `VLDOIN`, `VOUT`, `VBUS`, `V+`, `V-`, `IN`, `OUT`, `SW`, `GND`, `AGND`, `AVSS`, `VCCO`, `EP`, shield | decoupling / bulk / feed |

Signals not in any class (data, analog inputs, clocks) are not "support" pins; their R/C/L neighbours fall through to the secondary rule.

### 4.2 Page 2 — power

Net-centric counterpart: `brd01_wiring_manifest.md` §3.2. 105 components on this sheet.

#### Components

#### F1 — 0031.8201, Fuse_Schurter_0031.8201

Sheet: power (2) · Footprint: Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | passive | `Net-(F1-Pad1)` | J1.1 |
| 2 | — | passive | `Net-(F1-Pad2)` | L1.1 |

Supporting passives:

- input / output filter capacitor: L1 (7448225007) on `Net-(F1-Pad2)`

#### J1 — PJ-079BH

Sheet: power (2) · Footprint: Connector_BarrelJack:BarrelJack_CUI_PJ-079BH_Horizontal · 4 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | passive | `Net-(F1-Pad1)` | F1.1 |
| 2 | — | passive | `Net-(J1-Pad2)` | L1.2 |
| 3 | — | passive+no_connect | `unconnected-(J1-Pad3)` | — (no other pins on this net) |
| SH | Shield_SH | passive+no_connect | `unconnected-(J1-Shield-PadSH)` | — (no other pins on this net) |

#### J750 — 1715721, Conn_01x02

Sheet: power (2) · Footprint: TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `+15V_FUSED` | D1.1, C30.1, L760.2, C803.1, R803.1, U147.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 2 | Pin_2_2 | passive+no_connect | `unconnected-(J750-Pin_2-Pad2)` | — (no other pins on this net) |

#### SW750 — B3F-1002-G, SW_Push

Sheet: power (2) · Footprint: Button_Switch_THT:SW_PUSH_6mm_H4.3mm · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(R751-Pad2)` | R751.2, R752.1 |
| 2 | 2_2 | passive | `GND` | C755.2, U754.3, U753.4, R754.2, U752.3, U755.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- pull-up resistor: R751 (10k) on `Net-(R751-Pad2)`
- series / termination resistor: R752 (1k) on `Net-(R751-Pad2)`

#### TP760 — TestPoint

Sheet: power (2) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `+15V` | U6.7, U6.4, U6.2, U6.1, U5.7, C780.1 |

#### TP761 — TestPoint

Sheet: power (2) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `-15V` | U2.13, U2.5, U2.3, U2.2, U2.1, U5.5, C781.1 |

#### TP762 — TestPoint

Sheet: power (2) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `+12VA` | U6.10, U6.11, C5.1, U6.12, C782.1, C100.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

#### TP763 — TestPoint

Sheet: power (2) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `-12VA` | U2.10, U2.11, C4.1, U2.12, C783.1, C116.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

#### U2 — LT3093EMSE#TRPBF

Sheet: power (2) · Footprint: Package_SO:MSOP-12-1EP_3x4.039mm_P0.65mm_EP1.651x2.845mm · 13 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | IN_1 | power_in | `-15V` | U2.2, U2.3, U2.5, U2.13, TP761.1, U5.5, C781.1 |
| 2 | IN_2 | power_in | `-15V` | U2.3, U2.1, U2.5, U2.13, TP761.1, U5.5, C781.1 |
| 3 | EN/UV_3 | input | `-15V` | U2.2, U2.5, U2.1, U2.13, TP761.1, U5.5, C781.1 |
| 4 | PG_4 | open_collector+no_connect | `unconnected-(U2-PG-Pad4)` | — (no other pins on this net) |
| 5 | PGFB_5 | input | `-15V` | U2.3, U2.2, U2.1, U2.13, TP761.1, U5.5, C781.1 |
| 6 | ILIM_6 | passive | `Net-(U2-ILIM)` | R2.1 |
| 7 | VIOC_7 | output+no_connect | `unconnected-(U2-VIOC-Pad7)` | — (no other pins on this net) |
| 8 | SET_8 | passive | `Net-(U2-SET)` | C3.1, R1.2 |
| 9 | GND_9 | power_in | `GND` | R2.2, C3.2, C4.2, R1.1, C783.2, U6.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 10 | OUTS_10 | input | `-12VA` | U2.11, U2.12, C4.1, C783.1, TP763.1, C116.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | OUT_11 | passive | `-12VA` | U2.10, U2.12, C4.1, C783.1, TP763.1, C116.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 12 | OUT_12 | power_out | `-12VA` | U2.11, U2.10, C4.1, C783.1, TP763.1, C116.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 13 | IN_(EP)_13 | passive | `-15V` | U2.5, U2.3, U2.2, U2.1, TP761.1, U5.5, C781.1 |

Supporting passives:

- gain / feedback-set resistor: R2 (7.5k) on `Net-(U2-ILIM)`
- gain / feedback-set resistor: R1 (121k) on `Net-(U2-SET)`
- supply decoupling: C4 (4.7u), C783 (10u / 25V) on `-12VA`
- supply decoupling: C781 (10u / 35V) on `-15V`
- timing / set capacitor: C3 (4.7u) on `Net-(U2-SET)`

#### U5 — MGJ2D151515SC

Sheet: power (2) · Footprint: Converter_DCDC:Converter_DCDC_Murata_MGJ2DxxxxxxSC_THT · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | +VIN_1 | power_in | `+15V_FUSED` | J750.1, C30.1, L760.2, D1.1, U147.1, U147.16 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 2 | -VIN_2 | power_in | `GND` | C5.2, U5.6, C782.2, U6.13, U6.9, R4.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 5 | -VOUT_5 | power_out | `-15V` | U2.1, U2.2, U2.3, U2.5, U2.13, TP761.1, C781.1 |
| 6 | COM_6 | power_out | `GND` | U5.2, C782.2, C5.2, U6.13, U6.9, C783.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | +VOUT_7 | power_out | `+15V` | U6.1, U6.2, U6.4, U6.7, TP760.1, C780.1 |

Supporting passives:

- supply decoupling: C780 (10u / 35V) on `+15V`
- supply decoupling: C30 (EEUFR1V102), C800 (10u / 50V X7R), C801 (10u / 50V X7R), C802 (100n / 50V), C803 (100n / 50V), C804 (EEU-FR1V680 68u / 35V) on `+15V_FUSED`
- supply decoupling: C781 (10u / 35V) on `-15V`

#### U6 — LT3045EDD-1#TRPBF

Sheet: power (2) · Footprint: Package_DFN_QFN:DFN-12-1EP_3x3mm_P0.45mm_EP1.65x2.38mm · 13 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | IN_1 | power_in | `+15V` | U6.2, U6.4, U6.7, U5.7, TP760.1, C780.1 |
| 2 | IN_2 | power_in | `+15V` | U6.1, U6.4, U6.7, U5.7, TP760.1, C780.1 |
| 3 | VIOC_3 | output+no_connect | `unconnected-(U6-VIOC-Pad3)` | — (no other pins on this net) |
| 4 | EN/UV_4 | input | `+15V` | U6.2, U6.7, U6.1, U5.7, TP760.1, C780.1 |
| 5 | PG_5 | open_collector+no_connect | `unconnected-(U6-PG-Pad5)` | — (no other pins on this net) |
| 6 | ILIM_6 | passive | `Net-(U6-ILIM)` | R4.1 |
| 7 | PGFB_7 | input | `+15V` | U6.4, U6.2, U6.1, U5.7, TP760.1, C780.1 |
| 8 | SET_8 | passive | `Net-(U6-SET)` | C6.1, R3.1 |
| 9 | GND_9 | power_in | `GND` | U6.13, R4.2, C6.2, C5.2, R3.2, U5.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 10 | OUTS_10 | input | `+12VA` | U6.11, U6.12, C5.1, C782.1, TP762.1, C100.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | OUT_11 | passive | `+12VA` | U6.10, U6.12, C5.1, C782.1, TP762.1, C100.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 12 | OUT_12 | power_out | `+12VA` | U6.11, U6.10, C5.1, C782.1, TP762.1, C100.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 13 | GND_(EP)_13 | passive | `GND` | U6.9, R4.2, C5.2, C6.2, U5.2, R3.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- gain / feedback-set resistor: R4 (750) on `Net-(U6-ILIM)`
- gain / feedback-set resistor: R3 (121k) on `Net-(U6-SET)`
- supply decoupling: C5 (10u), C782 (22u / 25V) on `+12VA`
- supply decoupling: C780 (10u / 35V) on `+15V`
- timing / set capacitor: C6 (4.7u) on `Net-(U6-SET)`

#### U7 — TPS62130ARGTR, TPS62130A

Sheet: power (2) · Footprint: Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm_ThermalVias · 17 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | SW_1 | output | `Net-(L800-Pad1)` | U7.2, U7.3, L800.1 |
| 2 | SW_2 | passive | `Net-(L800-Pad1)` | U7.1, U7.3, L800.1 |
| 3 | SW_3 | passive | `Net-(L800-Pad1)` | U7.1, U7.2, L800.1 |
| 4 | PG_4 | open_collector+no_connect | `unconnected-(U7-PG-Pad4)` | — (no other pins on this net) |
| 5 | FB_5 | input | `Net-(U7-FB)` | R806.2, R807.1 |
| 6 | GND_6 | power_in | `GND` | U7.15, U7.16, U7.17, C753.2, U7.7, C752.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | FSW_7 | input | `GND` | U7.8, C814.2, U7.15, U7.16, U7.17, U7.6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 8 | DEF_8 | input | `GND` | U7.7, C814.2, C812.2, U7.15, U7.16, U7.17 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 9 | SS/TR_9 | input | `Net-(U7-SS/TR)` | C814.1 |
| 10 | VIN_10 | power_in | `+6V` | U7.11, U7.12, C812.1, C811.1, R195.1, U145.10 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | VIN_11 | passive | `+6V` | U7.10, U7.12, C812.1, C811.1, R195.1, U145.10 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 12 | VIN_12 | passive | `+6V` | U7.10, U7.11, C812.1, C811.1, R195.1, U145.10 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 13 | EN_13 | input | `/power/PG_1V8` | U145.4, R195.2 |
| 14 | VOS_14 | input | `+3.3V` | L800.2, C754.1, R806.1, C753.1, C813.1, C752.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 15 | GND_15 | passive | `GND` | U7.16, U7.17, U7.6, C753.2, U7.7, C752.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 16 | GND_16 | passive | `GND` | U7.15, U7.17, U7.6, C753.2, U7.7, C752.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 17 | GND_17 | passive | `GND` | U7.15, U7.16, U7.6, C753.2, U7.7, C752.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- enable pull-up: R195 (100k) on `/power/PG_1V8`
- feedback divider: R806 (619k), R807 (200k) on `Net-(U7-FB)`
- feedback filter: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+27 more; see manifest §3.2) on `+3.3V`
- soft-start / bias capacitor: C814 (3.3n) on `Net-(U7-SS/TR)`
- supply bulk / feed: L800 (XFL4020-222MEC) on `Net-(L800-Pad1)`
- supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on `+6V`

#### U144 — TPS62130ARGTR, TPS62130A

Sheet: power (2) · Footprint: Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm_ThermalVias · 17 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | SW_1 | output | `Net-(L140-Pad1)` | U144.2, U144.3, L140.1 |
| 2 | SW_2 | passive | `Net-(L140-Pad1)` | U144.1, U144.3, L140.1 |
| 3 | SW_3 | passive | `Net-(L140-Pad1)` | U144.1, U144.2, L140.1 |
| 4 | PG_4 | open_collector | `/power/PG_1V0` | U144.7, R192.2, U145.13 |
| 5 | FB_5 | input | `/power/BUCK1_FB` | R190.2, R191.1 |
| 6 | GND_6 | power_in | `GND` | U144.15, U144.16, U144.17, U144.8, R191.2, C183.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | FSW_7 | input | `/power/PG_1V0` | R192.2, U144.4, U145.13 |
| 8 | DEF_8 | input | `GND` | C183.2, C180.2, U144.15, U144.16, U144.17, U144.6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 9 | SS/TR_9 | input | `Net-(U144-SS/TR)` | C181.1 |
| 10 | VIN_10 | power_in | `+6V` | U144.11, U144.12, C183.1, R192.1, C180.1, C184.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | VIN_11 | passive | `+6V` | U144.10, U144.12, C183.1, R192.1, C180.1, C184.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 12 | VIN_12 | passive | `+6V` | U144.10, U144.11, C183.1, R192.1, C180.1, C184.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 13 | EN_13 | input | `/power/PG_6V` | R805.1, U147.13 |
| 14 | VOS_14 | input | `+1V0_FPGA` | R190.1, L140.2, C182.1, C150.1, C151.1, C152.1 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 15 | GND_15 | passive | `GND` | U144.16, U144.17, U144.6, U144.8, R191.2, C183.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 16 | GND_16 | passive | `GND` | U144.15, U144.17, U144.6, U144.8, R191.2, C183.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 17 | GND_17 | passive | `GND` | U144.15, U144.16, U144.6, U144.8, R191.2, C183.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- enable pull-up: R805 (100k) on `/power/PG_6V`
- feedback divider: R190 (49.9k), R191 (200k) on `/power/BUCK1_FB`
- feedback filter: C150 (100n), C151 (100n), C152 (100n), C153 (100n), C154 (100n), C155 (100n), C156 (100n), C170 (10u) (+1 more; see manifest §3.2) on `+1V0_FPGA`
- gain / feedback-set resistor: R192 (100k) on `/power/PG_1V0`
- soft-start / bias capacitor: C181 (3.3n) on `Net-(U144-SS/TR)`
- supply bulk / feed: L140 (XFL4020-222MEC) on `Net-(L140-Pad1)`
- supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on `+6V`

#### U145 — TPS62130ARGTR, TPS62130A

Sheet: power (2) · Footprint: Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm_ThermalVias · 17 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | SW_1 | output | `Net-(L141-Pad1)` | U145.2, U145.3, L141.1 |
| 2 | SW_2 | passive | `Net-(L141-Pad1)` | U145.1, U145.3, L141.1 |
| 3 | SW_3 | passive | `Net-(L141-Pad1)` | U145.1, U145.2, L141.1 |
| 4 | PG_4 | open_collector | `/power/PG_1V8` | R195.2, U7.13 |
| 5 | FB_5 | input | `Net-(U145-FB)` | R194.1, R193.2 |
| 6 | GND_6 | power_in | `GND` | U145.15, U145.16, U145.17, U145.7, U145.8, R194.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | FSW_7 | input | `GND` | U145.8, C187.2, U145.15, U145.16, U145.17, U145.6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 8 | DEF_8 | input | `GND` | U145.7, C187.2, C184.2, U145.15, U145.16, U145.17 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 9 | SS/TR_9 | input | `Net-(U145-SS/TR)` | C185.1 |
| 10 | VIN_10 | power_in | `+6V` | U145.11, U145.12, C187.1, C184.1, R195.1, C811.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | VIN_11 | passive | `+6V` | U145.10, U145.12, C187.1, C184.1, R195.1, C811.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 12 | VIN_12 | passive | `+6V` | U145.10, U145.11, C187.1, C184.1, R195.1, C811.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 13 | EN_13 | input | `/power/PG_1V0` | U144.4, U144.7, R192.2 |
| 14 | VOS_14 | input | `+1V8_FPGA` | R193.1, L141.2, C186.1, C157.1, C158.1, C159.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 15 | GND_15 | passive | `GND` | U145.16, U145.17, U145.6, U145.7, U145.8, R194.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 16 | GND_16 | passive | `GND` | U145.15, U145.17, U145.6, U145.7, U145.8, R194.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 17 | GND_17 | passive | `GND` | U145.15, U145.16, U145.6, U145.7, U145.8, R194.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- enable pull-up: R192 (100k) on `/power/PG_1V0`
- feedback divider: R193 (249k), R194 (200k) on `Net-(U145-FB)`
- feedback filter: C157 (100n), C158 (100n), C159 (100n), C160 (100n), C161 (100n), C171 (10u), C186 (22u / 25V X7R) on `+1V8_FPGA`
- soft-start / bias capacitor: C185 (3.3n) on `Net-(U145-SS/TR)`
- supply bulk / feed: L141 (XFL4020-222MEC) on `Net-(L141-Pad1)`
- supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on `+6V`

#### U146 — TPS7A4701RGWR

Sheet: power (2) · Footprint: Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias · 21 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | power_out | `+5VA` | U146.20, U146.3, C190.1, C107.1, C108.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 2 | NC_2 | passive+no_connect | `unconnected-(U146-NC-Pad2)` | — (no other pins on this net) |
| 3 | SENSE/FB_3 | input | `+5VA` | U146.20, U146.1, C190.1, C107.1, C108.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | 6P4V2_4 | input+no_connect | `unconnected-(U146-6P4V2-Pad4)` | — (no other pins on this net) |
| 5 | 6P4V1_5 | input+no_connect | `unconnected-(U146-6P4V1-Pad5)` | — (no other pins on this net) |
| 6 | 3P2V_6 | input | `GND` | U146.10, C189.2, U146.21, U146.7, C820.2, C190.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | GND_7 | power_in | `GND` | U146.21, C190.2, U146.6, U146.10, U147.20, U147.19 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 8 | 1P6V_8 | input+no_connect | `unconnected-(U146-1P6V-Pad8)` | — (no other pins on this net) |
| 9 | 0P8V_9 | input+no_connect | `unconnected-(U146-0P8V-Pad9)` | — (no other pins on this net) |
| 10 | 0P4V_10 | input | `GND` | U146.6, C189.2, C820.2, U146.21, U146.7, U149.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | 0P2V_11 | input+no_connect | `unconnected-(U146-0P2V-Pad11)` | — (no other pins on this net) |
| 12 | 0P1V_12 | input+no_connect | `unconnected-(U146-0P1V-Pad12)` | — (no other pins on this net) |
| 13 | EN_13 | input | `Net-(U146-EN)` | U146.16, U146.15, R809.1, C188.1, L802.2 |
| 14 | NR_14 | passive | `Net-(U146-NR)` | C189.1 |
| 15 | IN_15 | power_in | `Net-(U146-EN)` | U146.16, U146.13, R809.1, C188.1, L802.2 |
| 16 | IN_16 | power_in | `Net-(U146-EN)` | U146.13, U146.15, R809.1, C188.1, L802.2 |
| 17 | NC_17 | passive+no_connect | `unconnected-(U146-NC-Pad17)` | — (no other pins on this net) |
| 18 | NC_18 | passive+no_connect | `unconnected-(U146-NC-Pad18)` | — (no other pins on this net) |
| 19 | NC_19 | passive+no_connect | `unconnected-(U146-NC-Pad19)` | — (no other pins on this net) |
| 20 | OUT_20 | passive | `+5VA` | U146.1, U146.3, C190.1, C107.1, C108.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 21 | EP/GND_21 | passive | `GND` | U146.7, C190.2, U146.6, U146.10, U147.20, U147.19 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- feedback filter: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.2) on `+5VA`
- filter capacitor to ground: C820 (10u / 16V X7R) on `GND`
- soft-start / bias capacitor: C189 (1u / 16V X7R) on `Net-(U146-NR)`
- supply bulk / feed: L802 (XFL4020-102MEC 1u) on `Net-(U146-EN)`
- supply decoupling: C190 (47u / 16V X7R) on `+5VA`
- supply decoupling: C188 (2.2u / 16V X7R) on `Net-(U146-EN)`
- supply feed / filter: R809 (0.68) on `Net-(U146-EN)`

#### U147 — TPSM63604RDLR

Sheet: power (2) · Footprint: accubot:TI_RDL0020A_B3QFN-20_5x5.5mm · 20 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VIN1_1 | power_in | `+15V_FUSED` | U147.16, R803.1, C803.1, C802.1, C801.1, C800.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 2 | SW_2 | passive+no_connect | `unconnected-(U147-SW-Pad2)` | — (no other pins on this net) |
| 3 | CBOOT_3 | passive+no_connect | `unconnected-(U147-CBOOT-Pad3)` | — (no other pins on this net) |
| 4 | RBOOT_4 | passive+no_connect | `unconnected-(U147-RBOOT-Pad4)` | — (no other pins on this net) |
| 5 | VLDOIN_5 | power_in | `+6V` | U147.9, U147.8, R800.1, R805.2, C805.1, C806.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 6 | AGND_6 | power_in | `GND` | U147.11, U147.17, U147.18, U147.19, R802.2, U147.20 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | VCC_7 | passive+no_connect | `unconnected-(U147-VCC-Pad7)` | — (no other pins on this net) |
| 8 | VOUT1_8 | power_out | `+6V` | U147.9, U147.5, R800.1, C805.1, R805.2, C806.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 9 | VOUT2_9 | passive | `+6V` | U147.5, U147.8, R800.1, C805.1, R805.2, C806.1 — 28 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 10 | FB_10 | input | `Net-(U147-FB)` | R801.1, R800.2, C805.2 |
| 11 | AGND_11 | passive | `GND` | U147.17, U147.6, U147.18, U147.19, U147.20, R802.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 12 | RT_12 | passive | `Net-(U147-RT)` | R802.1 |
| 13 | PG_13 | open_collector | `/power/PG_6V` | R805.1, U144.13 |
| 14 | EN/SYNC_14 | input | `Net-(U147-EN/SYNC)` | R804.1, R803.2, C809.2 |
| 15 | NC_15 | passive | `GND` | U147.20, U147.19, U147.18, U147.17, U147.11, R801.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 16 | VIN2_16 | passive | `+15V_FUSED` | U147.1, R803.1, C803.1, C802.1, C801.1, C800.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 17 | PGND_17 | power_in | `GND` | U147.11, U147.18, U147.6, U147.19, U147.20, U147.15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 18 | PGND_18 | passive | `GND` | U147.17, U147.19, U147.11, U147.20, U147.6, U147.15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 19 | PGND_19 | passive | `GND` | U147.20, U147.18, U147.17, U147.11, U147.6, U147.15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 20 | PGND_20 | passive | `GND` | U147.19, U147.18, U147.17, U147.15, U147.11, U147.6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- enable / sequencing network: C809 (1n) on `Net-(U147-EN/SYNC)`
- enable pull-down: R804 (118k) on `Net-(U147-EN/SYNC)`
- enable pull-up: R803 (1.00M) on `Net-(U147-EN/SYNC)`
- feedback divider: R800 (49.9k 0.1%), R801 (10.0k 0.1%) on `Net-(U147-FB)`
- feedback filter: C805 (18p C0G) on `Net-(U147-FB)`
- gain / feedback-set resistor: R802 (13.0k 1%) on `Net-(U147-RT)`
- supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on `+6V`
- supply decoupling: C30 (EEUFR1V102), C800 (10u / 50V X7R), C801 (10u / 50V X7R), C802 (100n / 50V), C803 (100n / 50V), C804 (EEU-FR1V680 68u / 35V) on `+15V_FUSED`

#### U149 — TPS7A4701RGWR

Sheet: power (2) · Footprint: Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias · 21 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | power_out | `+5V_EXC` | U149.20, U149.3, C816.1, C200.1, C201.1, C210.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 2 | NC_2 | passive+no_connect | `unconnected-(U149-NC-Pad2)` | — (no other pins on this net) |
| 3 | SENSE/FB_3 | input | `+5V_EXC` | U149.20, U149.1, C816.1, C200.1, C201.1, C210.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | 6P4V2_4 | input+no_connect | `unconnected-(U149-6P4V2-Pad4)` | — (no other pins on this net) |
| 5 | 6P4V1_5 | input+no_connect | `unconnected-(U149-6P4V1-Pad5)` | — (no other pins on this net) |
| 6 | 3P2V_6 | input | `GND` | U149.10, C815.2, C818.2, U149.21, U149.7, C817.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 7 | GND_7 | power_in | `GND` | U149.21, C816.2, U149.6, U149.10, C815.2, U146.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 8 | 1P6V_8 | input+no_connect | `unconnected-(U149-1P6V-Pad8)` | — (no other pins on this net) |
| 9 | 0P8V_9 | input+no_connect | `unconnected-(U149-0P8V-Pad9)` | — (no other pins on this net) |
| 10 | 0P4V_10 | input | `GND` | U149.6, C815.2, C818.2, U149.21, U149.7, C817.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 11 | 0P2V_11 | input+no_connect | `unconnected-(U149-0P2V-Pad11)` | — (no other pins on this net) |
| 12 | 0P1V_12 | input+no_connect | `unconnected-(U149-0P1V-Pad12)` | — (no other pins on this net) |
| 13 | EN_13 | input | `Net-(U149-EN)` | U149.16, U149.15, R808.1, C817.1, L801.2 |
| 14 | NR_14 | passive | `Net-(U149-NR)` | C815.1 |
| 15 | IN_15 | power_in | `Net-(U149-EN)` | U149.16, U149.13, R808.1, C817.1, L801.2 |
| 16 | IN_16 | power_in | `Net-(U149-EN)` | U149.15, U149.13, R808.1, C817.1, L801.2 |
| 17 | NC_17 | passive+no_connect | `unconnected-(U149-NC-Pad17)` | — (no other pins on this net) |
| 18 | NC_18 | passive+no_connect | `unconnected-(U149-NC-Pad18)` | — (no other pins on this net) |
| 19 | NC_19 | passive+no_connect | `unconnected-(U149-NC-Pad19)` | — (no other pins on this net) |
| 20 | OUT_20 | passive | `+5V_EXC` | U149.1, U149.3, C816.1, C200.1, C201.1, C210.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 21 | EP/GND_21 | passive | `GND` | U149.7, C816.2, U149.6, U149.10, C815.2, U146.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- feedback filter: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.2) on `+5V_EXC`
- filter capacitor to ground: C818 (10u / 16V X7R) on `GND`
- soft-start / bias capacitor: C815 (1u / 16V X7R) on `Net-(U149-NR)`
- supply bulk / feed: L801 (XFL4020-102MEC 1u) on `Net-(U149-EN)`
- supply decoupling: C816 (47u / 16V X7R) on `+5V_EXC`
- supply decoupling: C817 (2.2u / 16V X7R) on `Net-(U149-EN)`
- supply feed / filter: R808 (0.68) on `Net-(U149-EN)`

#### U751 — TPS3808G33DBVR, TPS3808DBV

Sheet: power (2) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | ~{RESET}_1 | output | `Net-(U751-~{RESET})` | R750.2, U752.1 |
| 2 | GND_2 | power_in | `GND` | U752.3, U755.3, R753.2, R754.2, U753.4, U754.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 3 | ~{MR}_3 | input | `+3.3V` | U751.5, U751.6, R750.1, U752.5, U755.5, U753.8 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | CT_4 | input+no_connect | `unconnected-(U751-CT-Pad4)` | — (no other pins on this net) |
| 5 | SENSE_5 | input | `+3.3V` | U751.3, U751.6, R750.1, U752.5, U755.5, U753.8 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 6 | VDD_6 | power_in | `+3.3V` | U751.5, U751.3, R750.1, U752.5, U755.5, U753.8 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- enable pull-up: R750 (10k) on `Net-(U751-~{RESET})`
- feedback filter: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+21 more; see manifest §3.2) on `+3.3V`
- supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on `+3.3V`

#### U752 — SN74LVC1G08DBVR, 74LVC1G08

Sheet: power (2) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `Net-(U751-~{RESET})` | R750.2, U751.1 |
| 2 | — | input | `/DRIVER_FAULT_N` | R712.2, U4.R1, U600.4, U600.6, U601.4, U601.6 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 3 | GND_3 | power_in | `GND` | U755.3, U753.4, R754.2, U751.2, R753.2, U754.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | — | output | `Net-(U753-~{CLR})` | U753.6 |
| 5 | VCC_5 | power_in | `+3.3V` | R750.1, U751.6, U751.3, U751.5, U755.5, U753.2 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on `+3.3V`

#### U753 — SN74LVC2G74DCUT, 74LVC2G74

Sheet: power (2) · Footprint: Package_SO:VSSOP-8_2.3x2mm_P0.5mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | C_1 | input | `Net-(U753-C)` | U754.4 |
| 2 | D_2 | input | `+3.3V` | U753.7, U753.8, U754.5, R751.1, U755.5, U752.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 3 | ~{Q}_3 | output+no_connect | `unconnected-(U753-~{Q}-Pad3)` | — (no other pins on this net) |
| 4 | GND_4 | power_in | `GND` | U754.3, R754.2, U752.3, C755.2, U755.3, SW750.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 5 | Q_5 | output | `/power/ARM_Q` | U755.2 |
| 6 | ~{CLR}_6 | input | `Net-(U753-~{CLR})` | U752.4 |
| 7 | ~{PRE}_7 | input | `+3.3V` | U753.2, U753.8, U754.5, R751.1, U755.5, U752.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 8 | VCC_8 | power_in | `+3.3V` | U753.7, U753.2, U754.5, U755.5, R751.1, U752.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- enable / sequencing network: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+21 more; see manifest §3.2) on `+3.3V`
- supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on `+3.3V`

#### U754 — SN74LVC1G14DBVR, 74LVC1G14

Sheet: power (2) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | NC_1 | no_connect | `unconnected-(U754-NC-Pad1)` | — (no other pins on this net) |
| 2 | — | input | `Net-(C755-Pad1)` | C755.1, R752.2 |
| 3 | GND_3 | power_in | `GND` | C755.2, U753.4, SW750.2, R754.2, U752.3, U755.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | — | output | `Net-(U753-C)` | U753.1 |
| 5 | VCC_5 | power_in | `+3.3V` | U753.7, U753.2, U753.8, R751.1, U755.5, U752.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- filter capacitor to ground: C755 (100n) on `Net-(C755-Pad1)`
- supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on `+3.3V`

#### U755 — SN74LVC1G08DBVR, 74LVC1G08

Sheet: power (2) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `PICO_STOP_REQ_N` | R754.1, U4.P4 |
| 2 | — | input | `/power/ARM_Q` | U753.5 |
| 3 | GND_3 | power_in | `GND` | R754.2, U752.3, R753.2, U753.4, U751.2, U754.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | — | output | `PICO_STOP_N` | R753.1, J123.5 |
| 5 | VCC_5 | power_in | `+3.3V` | U753.8, U753.7, U753.2, R750.1, U752.5, U754.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

Supporting passives:

- pull-down resistor: R753 (100k) on `PICO_STOP_N`
- pull-down resistor: R754 (100k) on `PICO_STOP_REQ_N`
- supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on `+3.3V`

#### Q760 — DMP6023LE-13, Q_PMOS_GDS

Sheet: power (2) · Footprint: Package_TO_SOT_SMD:SOT-223-3_TabPin2 · 3 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | G_1 | input | `Net-(D760-A)` | R770.1, D760.2 |
| 2 | D_2 | passive | `/power/CMC_POS` | L1.4 |
| 3 | S_3 | passive | `Net-(D760-K)` | C770.1, D760.1, L760.1 |

Supporting passives:

- filter capacitor to ground: C770 (1u / 50V) on `Net-(D760-K)`
- pull-down resistor: R770 (10k) on `Net-(D760-A)`

#### D1 — SMBJ18A

Sheet: power (2) · Footprint: accubot:ST_SMBJ_DO-214AA_DS1283 · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+15V_FUSED` | L760.2, C30.1, J750.1, C803.1, C802.1, R803.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 2 | A_2 | passive | `GND` | C770.2, L1.3, R770.2, C30.2, C803.2, C802.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |

#### D760 — BZX38450-C12X, D_Zener

Sheet: power (2) · Footprint: Diode_SMD:D_SOD-323 · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `Net-(D760-K)` | C770.1, L760.1, Q760.3 |
| 2 | A_2 | passive | `Net-(D760-A)` | R770.1, Q760.1 |

Supporting passives:

- input / output filter capacitor: L760 (7447714047) on `Net-(D760-K)`

#### L1 — 7448225007, Choke_CommonMode_FerriteCore_1423

Sheet: power (2) · Footprint: accubot:Wuerth_WE-CMB-HC_S_7448225007 · 4 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(F1-Pad2)` | F1.2 |
| 2 | 2_2 | passive | `Net-(J1-Pad2)` | J1.2 |
| 3 | 3_3 | passive | `GND` | D1.2, C770.2, R770.2, C30.2, C803.2, C802.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.2 |
| 4 | 4_4 | passive | `/power/CMC_POS` | Q760.2 |

#### C3 — 4.7u, C

C3 — 4.7u, C_0805_2012Metric — `Net-(U2-SET)` ↔ `GND` — timing / set capacitor for U2 (pin 1 → 2).

#### C4 — 4.7u, C

C4 — 4.7u, C_1206_3216Metric — `-12VA` ↔ `GND` — supply decoupling for U2 (pin 1 → 2).

#### C5 — 10u, C

C5 — 10u, C_1206_3216Metric — `+12VA` ↔ `GND` — supply decoupling for U6 (pin 1 → 2).

#### C6 — 4.7u, C

C6 — 4.7u, C_0805_2012Metric — `Net-(U6-SET)` ↔ `GND` — timing / set capacitor for U6 (pin 1 → 2).

#### C30 — EEUFR1V102, C_Polarized

C30 — EEUFR1V102, CP_Radial_D12.5mm_P5.00mm — `+15V_FUSED` ↔ `GND` — supply decoupling for U5, U147 (pin 1 → 2).

#### C180 — 10u / 25V, C

C180 — 10u / 25V, C_1206_3216Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C181 — 3.3n, C

C181 — 3.3n, C_0603_1608Metric — `Net-(U144-SS/TR)` ↔ `GND` — soft-start / bias capacitor for U144 (pin 1 → 2).

#### C182 — 22u / 25V X7R, C

C182 — 22u / 25V X7R, C_1210_3225Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C183 — 100n, C

C183 — 100n, C_0603_1608Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C184 — 10u / 25V, C

C184 — 10u / 25V, C_1206_3216Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C185 — 3.3n, C

C185 — 3.3n, C_0603_1608Metric — `Net-(U145-SS/TR)` ↔ `GND` — soft-start / bias capacitor for U145 (pin 1 → 2).

#### C186 — 22u / 25V X7R, C

C186 — 22u / 25V X7R, C_1210_3225Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C187 — 100n, C

C187 — 100n, C_0603_1608Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C188 — 2.2u / 16V X7R, C

C188 — 2.2u / 16V X7R, C_0805_2012Metric — `Net-(U146-EN)` ↔ `GND` — supply decoupling for U146 (pin 1 → 2).

#### C189 — 1u / 16V X7R, C

C189 — 1u / 16V X7R, C_1206_3216Metric — `Net-(U146-NR)` ↔ `GND` — soft-start / bias capacitor for U146 (pin 1 → 2).

#### C190 — 47u / 16V X7R, C

C190 — 47u / 16V X7R, C_1210_3225Metric — `+5VA` ↔ `GND` — enable / sequencing network, supply decoupling for U105, U108, U146 (pin 1 → 2).

#### C750 — 100n, C

C750 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U142, U751, U752, U753, U754, U755, Y1 (pin 1 → 2).

#### C751 — 100n, C

C751 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U142, U751, U752, U753, U754, U755, Y1 (pin 1 → 2).

#### C752 — 100n, C

C752 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U142, U751, U752, U753, U754, U755, Y1 (pin 1 → 2).

#### C753 — 100n, C

C753 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U142, U751, U752, U753, U754, U755, Y1 (pin 1 → 2).

#### C754 — 100n, C

C754 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U142, U751, U752, U753, U754, U755, Y1 (pin 1 → 2).

#### C755 — 100n, C

C755 — 100n, C_0603_1608Metric — `Net-(C755-Pad1)` ↔ `GND` — filter capacitor to ground for U754 (pin 1 → 2).

#### C770 — 1u / 50V, C

C770 — 1u / 50V, C_1206_3216Metric — `Net-(D760-K)` ↔ `GND` — filter capacitor to ground for Q760 (pin 1 → 2).

#### C780 — 10u / 35V, C

C780 — 10u / 35V, C_1206_3216Metric — `+15V` ↔ `GND` — supply decoupling for U5, U6 (pin 1 → 2).

#### C781 — 10u / 35V, C

C781 — 10u / 35V, C_1206_3216Metric — `-15V` ↔ `GND` — supply decoupling for U2, U5 (pin 1 → 2).

#### C782 — 22u / 25V, C

C782 — 22u / 25V, C_1210_3225Metric — `+12VA` ↔ `GND` — supply decoupling for U6 (pin 1 → 2).

#### C783 — 10u / 25V, C

C783 — 10u / 25V, C_1210_3225Metric — `-12VA` ↔ `GND` — supply decoupling for U2 (pin 1 → 2).

#### C800 — 10u / 50V X7R, C

C800 — 10u / 50V X7R, C_1210_3225Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U5, U147 (pin 1 → 2).

#### C801 — 10u / 50V X7R, C

C801 — 10u / 50V X7R, C_1210_3225Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U5, U147 (pin 1 → 2).

#### C802 — 100n / 50V, C

C802 — 100n / 50V, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U5, U147 (pin 1 → 2).

#### C803 — 100n / 50V, C

C803 — 100n / 50V, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U5, U147 (pin 1 → 2).

#### C804 — EEU-FR1V680 68u / 35V, C_Polarized

C804 — EEU-FR1V680 68u / 35V, CP_Radial_D6.3mm_P2.50mm — `+15V_FUSED` ↔ `GND` — supply decoupling for U5, U147 (pin 1 → 2).

#### C805 — 18p C0G, C

C805 — 18p C0G, C_0603_1608Metric — `+6V` ↔ `Net-(U147-FB)` — feedback filter for U147 (pin 1 → 2).

#### C806 — 22u / 25V X7R, C

C806 — 22u / 25V X7R, C_1210_3225Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C807 — 22u / 25V X7R, C

C807 — 22u / 25V X7R, C_1210_3225Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C808 — 22u / 25V X7R, C

C808 — 22u / 25V X7R, C_1210_3225Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C809 — 1n, C

C809 — 1n, C_0603_1608Metric — `/BUCK_SYNC` ↔ `Net-(U147-EN/SYNC)` — enable / sequencing network for U147 (pin 1 → 2).

#### C810 — 1u / 16V, C

C810 — 1u / 16V, C_0603_1608Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C811 — 10u / 25V X7R, C

C811 — 10u / 25V X7R, C_1206_3216Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C812 — 100n / 25V X7R, C

C812 — 100n / 25V X7R, C_0603_1608Metric — `+6V` ↔ `GND` — supply decoupling for U7, U144, U145, U147 (pin 1 → 2).

#### C813 — 22u / 25V X7R, C

C813 — 22u / 25V X7R, C_1210_3225Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U142, U751, U752, U753, U754, U755, Y1 (pin 1 → 2).

#### C814 — 3.3n, C

C814 — 3.3n, C_0603_1608Metric — `Net-(U7-SS/TR)` ↔ `GND` — soft-start / bias capacitor for U7 (pin 1 → 2).

#### C815 — 1u / 16V X7R, C

C815 — 1u / 16V X7R, C_0603_1608Metric — `Net-(U149-NR)` ↔ `GND` — soft-start / bias capacitor for U149 (pin 1 → 2).

#### C816 — 47u / 16V X7R, C

C816 — 47u / 16V X7R, C_1210_3225Metric — `+5V_EXC` ↔ `GND` — supply decoupling for U149 (pin 1 → 2).

#### C817 — 2.2u / 16V X7R, C

C817 — 2.2u / 16V X7R, C_0805_2012Metric — `Net-(U149-EN)` ↔ `GND` — supply decoupling for U149 (pin 1 → 2).

#### C818 — 10u / 16V X7R, C

C818 — 10u / 16V X7R, C_0805_2012Metric — `Net-(C818-Pad1)` ↔ `GND` — filter capacitor to ground for U149 (pin 1 → 2).

#### C820 — 10u / 16V X7R, C

C820 — 10u / 16V X7R, C_0805_2012Metric — `Net-(C820-Pad1)` ↔ `GND` — filter capacitor to ground for U146 (pin 1 → 2).

#### L140 — XFL4020-222MEC, L

L140 — XFL4020-222MEC, L_Coilcraft_XxL4020 — `Net-(L140-Pad1)` ↔ `+1V0_FPGA` — supply bulk / feed for U144 (pin 1 → 2).

#### L141 — XFL4020-222MEC, L

L141 — XFL4020-222MEC, L_Coilcraft_XxL4020 — `Net-(L141-Pad1)` ↔ `+1V8_FPGA` — supply bulk / feed for U145 (pin 1 → 2).

#### L760 — 7447714047, L

L760 — 7447714047, Wuerth_WE-PD_1050_7447714047 — `Net-(D760-K)` ↔ `+15V_FUSED` — input / output filter capacitor for D760 (pin 1 → 2).

#### L800 — XFL4020-222MEC, L

L800 — XFL4020-222MEC, L_Coilcraft_XxL4020 — `Net-(L800-Pad1)` ↔ `+3.3V` — supply bulk / feed for U7 (pin 1 → 2).

#### L801 — XFL4020-102MEC 1u, L

L801 — XFL4020-102MEC 1u, L_Coilcraft_XxL4020 — `+6V` ↔ `Net-(U149-EN)` — supply bulk / feed for U149 (pin 1 → 2).

#### L802 — XFL4020-102MEC 1u, L

L802 — XFL4020-102MEC 1u, L_Coilcraft_XxL4020 — `+6V` ↔ `Net-(U146-EN)` — supply bulk / feed for U146 (pin 1 → 2).

#### R1 — 121k, R

R1 — 121k, R_0603_1608Metric — `GND` ↔ `Net-(U2-SET)` — gain / feedback-set resistor for U2 (pin 1 → 2).

#### R2 — 7.5k, R

R2 — 7.5k, R_0603_1608Metric — `Net-(U2-ILIM)` ↔ `GND` — gain / feedback-set resistor for U2 (pin 1 → 2).

#### R3 — 121k, R

R3 — 121k, R_0603_1608Metric — `Net-(U6-SET)` ↔ `GND` — gain / feedback-set resistor for U6 (pin 1 → 2).

#### R4 — 750, R

R4 — 750, R_0603_1608Metric — `Net-(U6-ILIM)` ↔ `GND` — gain / feedback-set resistor for U6 (pin 1 → 2).

#### R190 — 49.9k, R

R190 — 49.9k, R_0603_1608Metric — `+1V0_FPGA` ↔ `/power/BUCK1_FB` — feedback divider for U144 (pin 1 → 2).

#### R191 — 200k, R

R191 — 200k, R_0603_1608Metric — `/power/BUCK1_FB` ↔ `GND` — feedback divider for U144 (pin 1 → 2).

#### R192 — 100k, R

R192 — 100k, R_0603_1608Metric — `+6V` ↔ `/power/PG_1V0` — enable pull-up, gain / feedback-set resistor for U144, U145 (pin 1 → 2).

#### R193 — 249k, R

R193 — 249k, R_0603_1608Metric — `+1V8_FPGA` ↔ `Net-(U145-FB)` — feedback divider for U145 (pin 1 → 2).

#### R194 — 200k, R

R194 — 200k, R_0603_1608Metric — `Net-(U145-FB)` ↔ `GND` — feedback divider for U145 (pin 1 → 2).

#### R195 — 100k, R

R195 — 100k, R_0603_1608Metric — `+6V` ↔ `/power/PG_1V8` — enable pull-up for U7 (pin 1 → 2).

#### R750 — 10k, R

R750 — 10k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U751-~{RESET})` — enable pull-up for U751 (pin 1 → 2).

#### R751 — 10k, R

R751 — 10k, R_0603_1608Metric — `+3.3V` ↔ `Net-(R751-Pad2)` — pull-up resistor for SW750 (pin 1 → 2).

#### R752 — 1k, R

R752 — 1k, R_0603_1608Metric — `Net-(R751-Pad2)` ↔ `Net-(C755-Pad1)` — series / termination resistor for SW750 (pin 1 → 2).

#### R753 — 100k, R

R753 — 100k, R_0603_1608Metric — `PICO_STOP_N` ↔ `GND` — pull-down resistor for U755 (pin 1 → 2).

#### R754 — 100k, R

R754 — 100k, R_0603_1608Metric — `PICO_STOP_REQ_N` ↔ `GND` — pull-down resistor for U755 (pin 1 → 2).

#### R770 — 10k, R

R770 — 10k, R_0603_1608Metric — `Net-(D760-A)` ↔ `GND` — pull-down resistor for Q760 (pin 1 → 2).

#### R800 — 49.9k 0.1%, R

R800 — 49.9k 0.1%, R_0603_1608Metric — `+6V` ↔ `Net-(U147-FB)` — feedback divider for U147 (pin 1 → 2).

#### R801 — 10.0k 0.1%, R

R801 — 10.0k 0.1%, R_0603_1608Metric — `Net-(U147-FB)` ↔ `GND` — feedback divider for U147 (pin 1 → 2).

#### R802 — 13.0k 1%, R

R802 — 13.0k 1%, R_0603_1608Metric — `Net-(U147-RT)` ↔ `GND` — gain / feedback-set resistor for U147 (pin 1 → 2).

#### R803 — 1.00M, R

R803 — 1.00M, R_0603_1608Metric — `+15V_FUSED` ↔ `Net-(U147-EN/SYNC)` — enable pull-up for U147 (pin 1 → 2).

#### R804 — 118k, R

R804 — 118k, R_0603_1608Metric — `Net-(U147-EN/SYNC)` ↔ `GND` — enable pull-down for U147 (pin 1 → 2).

#### R805 — 100k, R

R805 — 100k, R_0603_1608Metric — `/power/PG_6V` ↔ `+6V` — enable pull-up for U144 (pin 1 → 2).

#### R806 — 619k, R

R806 — 619k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U7-FB)` — feedback divider for U7 (pin 1 → 2).

#### R807 — 200k, R

R807 — 200k, R_0603_1608Metric — `Net-(U7-FB)` ↔ `GND` — feedback divider for U7 (pin 1 → 2).

#### R808 — 0.68, R

R808 — 0.68, R_0603_1608Metric — `Net-(U149-EN)` ↔ `Net-(C818-Pad1)` — supply feed / filter for U149 (pin 1 → 2).

#### R809 — 0.68, R

R809 — 0.68, R_0603_1608Metric — `Net-(U146-EN)` ↔ `Net-(C820-Pad1)` — supply feed / filter for U146 (pin 1 → 2).

### 4.3 Page 3 — driver

Net-centric counterpart: `brd01_wiring_manifest.md` §3.3. 338 components on this sheet.

#### Components

#### TP200 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_CS` | U10.12, R145.2, R162.2 |

#### TP201 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_SCLK` | U10.13, R146.2 |

#### TP202 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_SDI` | U10.14, R147.2 |

#### TP203 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `DAC_SDO` | U10.15, U4.M4 |

#### TP210 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT0` | U60.1, U600.1 |

#### TP211 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT1` | U61.1, U600.3 |

#### TP212 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT2` | U62.1, U601.1 |

#### TP213 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT3` | U63.1, U601.3 |

#### TP214 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT4` | U64.1, U602.1 |

#### TP215 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT5` | U65.1, U602.3 |

#### TP216 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT6` | U66.1, U603.1 |

#### TP217 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.0mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/FAULT7` | U67.1, U603.3 |

#### TP820 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/BUF0` | C212.1, U20.6 |

#### TP821 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `FG0_OUT` | C212.2, J20.1 |

#### TP822 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `FG0_RETURN` | R400.1, R20.1, J20.2 |

#### TP823 — TestPoint

Sheet: driver (3) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `/driver/VMID_7V5` | R383.1, C283.1, R382.2, C282.1, R21.2, R412.1 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C283 (100n) on `/driver/VMID_7V5`
- pull-down resistor: R383 (10k) on `/driver/VMID_7V5`
- pull-up resistor: R382 (10k) on `/driver/VMID_7V5`
- series / termination resistor: R20 (1.00 0.1% 0.5W), R21 (1.00 0.1% 0.5W), R22 (1.00 0.1% 0.5W), R23 (1.00 0.1% 0.5W), R24 (1.00 0.1% 0.5W), R25 (1.00 0.1% 0.5W), R26 (1.00 0.1% 0.5W), R27 (1.00 0.1% 0.5W) on `/driver/VMID_7V5`

#### U10 — DAC80508MRTET

Sheet: driver (3) · Footprint: Package_DFN_QFN:Texas_RTE0016D_WQFN-16-1EP_3x3mm_P0.5mm_EP0.8x0.8mm · 17 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | REF_1 | bidirectional | `/driver/DAC_REF` | C203.1 |
| 2 | OUT0_2 | output | `/driver/DAC0` | R220.1 |
| 3 | OUT1_3 | output | `/driver/DAC1` | R230.1 |
| 4 | OUT2_4 | output | `/driver/DAC2` | R240.1 |
| 5 | OUT3_5 | output | `/driver/DAC3` | R250.1 |
| 6 | GND_6 | power_in | `GND` | U10.17, C203.2, C200.2, U80.9, U80.3, C201.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 7 | VDD_7 | power_in | `+5V_EXC` | C200.1, C201.1, U80.1, U80.16, C210.1, U82.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | OUT4_8 | output | `/driver/DAC4` | R260.1 |
| 9 | OUT5_9 | output | `/driver/DAC5` | R270.1 |
| 10 | OUT6_10 | output | `/driver/DAC6` | R280.1 |
| 11 | OUT7_11 | output | `/driver/DAC7` | R290.1 |
| 12 | ~{CS}_12 | input | `DAC_CS` | TP200.1, R145.2, R162.2 |
| 13 | SCLK_13 | input | `DAC_SCLK` | TP201.1, R146.2 |
| 14 | SDI_14 | input | `DAC_SDI` | TP202.1, R147.2 |
| 15 | SDO/~{ALARM}_15 | output | `DAC_SDO` | TP203.1, U4.M4 |
| 16 | VIO_16 | power_in | `+3.3V` | C202.1, C290.1, C292.1, C294.1, C296.1, C291.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 17 | EP_17 | passive | `GND` | U10.6, C203.2, C200.2, U80.9, U80.3, U80.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- soft-start / bias capacitor: C203 (150n) on `/driver/DAC_REF`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply feed / filter: R220 (42.7k 0.1%) on `/driver/DAC0`
- supply feed / filter: R230 (42.7k 0.1%) on `/driver/DAC1`
- supply feed / filter: R240 (42.7k 0.1%) on `/driver/DAC2`
- supply feed / filter: R250 (42.7k 0.1%) on `/driver/DAC3`
- supply feed / filter: R260 (42.7k 0.1%) on `/driver/DAC4`
- supply feed / filter: R270 (42.7k 0.1%) on `/driver/DAC5`
- supply feed / filter: R280 (42.7k 0.1%) on `/driver/DAC6`
- supply feed / filter: R290 (42.7k 0.1%) on `/driver/DAC7`

#### U20 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U20-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG0` | R600.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN0` | R361.2 |
| 4 | V-_4 | power_in | `GND` | U20.9, C213.2, C290.2, R381.2, C280.2, C281.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U39.1, U22.5, U39.4, U24.5, U26.5, U21.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF0` | TP820.1, C212.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C213.1, R600.1, R380.1, C280.1, U22.7, R382.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U20-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U20.4, C213.2, C290.2, R381.2, C280.2, C281.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-down resistor: R381 (10k) on `GND`
- pull-up resistor: R380 (10k), R600 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C212 (CAA572X7R1E107M670LJ) on `/driver/BUF0`

#### U21 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U21-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG1` | R601.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN1` | R363.2 |
| 4 | V-_4 | power_in | `GND` | U21.9, C221.2, C291.2, U23.4, C223.2, C222.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U23.5, U25.5, U27.5, U20.5, U22.5, U24.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF1` | C220.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C221.1, R601.1, U23.7, C237.1, R603.1, U25.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U21-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U21.4, C221.2, C291.2, U23.4, U23.9, C223.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R601 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C220 (CAA572X7R1E107M670LJ) on `/driver/BUF1`

#### U22 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U22-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG2` | R602.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN2` | R365.2 |
| 4 | V-_4 | power_in | `GND` | U22.9, C229.2, C290.2, C292.2, C213.2, U20.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U20.5, U24.5, U39.1, U39.4, U26.5, R631.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF2` | C228.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C229.1, R602.1, R600.1, C213.1, U20.7, U24.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U22-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U22.4, C229.2, C290.2, C292.2, C213.2, U24.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R602 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C228 (CAA572X7R1E107M670LJ) on `/driver/BUF2`

#### U23 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U23-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG3` | R603.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN3` | R367.2 |
| 4 | V-_4 | power_in | `GND` | U23.9, C237.2, C291.2, C293.2, C221.2, U21.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U21.5, U25.5, U27.5, U22.5, R631.1, U20.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF3` | C236.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C237.1, R603.1, R601.1, C221.1, U21.7, U25.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U23-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U23.4, C237.2, C291.2, C293.2, C221.2, U25.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R603 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C236 (CAA572X7R1E107M670LJ) on `/driver/BUF3`

#### U24 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U24-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG4` | R604.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN4` | R369.2 |
| 4 | V-_4 | power_in | `GND` | U24.9, C245.2, C292.2, C294.2, C229.2, U22.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U22.5, U26.5, U20.5, U39.1, U39.4, R631.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF4` | C244.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C245.1, R604.1, R602.1, C229.1, U26.7, U22.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U24-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U24.4, C245.2, C292.2, C294.2, C229.2, U26.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R604 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C244 (CAA572X7R1E107M670LJ) on `/driver/BUF4`

#### U25 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U25-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG5` | R605.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN5` | R371.2 |
| 4 | V-_4 | power_in | `GND` | U25.9, C253.2, C293.2, C295.2, C237.2, U23.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U23.5, U27.5, U21.5, R631.1, R651.1, U24.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF5` | C252.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C253.1, R605.1, R603.1, C237.1, U27.7, U23.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U25-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U25.4, C253.2, C293.2, C295.2, C237.2, U27.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R605 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C252 (CAA572X7R1E107M670LJ) on `/driver/BUF5`

#### U26 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U26-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG6` | R606.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN6` | R373.2 |
| 4 | V-_4 | power_in | `GND` | U26.9, C261.2, C294.2, C296.2, C303.2, C245.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U24.5, U22.5, R631.1, R621.1, R651.1, R641.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF6` | C260.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C261.1, R606.1, R604.1, C245.1, U24.7, R602.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U26-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U26.4, C261.2, C294.2, C296.2, C303.2, C302.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R606 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C260 (CAA572X7R1E107M670LJ) on `/driver/BUF6`

#### U27 — LMH6321MR/NOPB, LMH6321MR-NOPB

Sheet: driver (3) · Footprint: Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm · 9 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | EF_1 | open_collector+no_connect | `unconnected-(U27-EF-Pad1)` | — (no other pins on this net) |
| 2 | CL_2 | input | `/driver/LIMIT_PROG7` | R607.2 |
| 3 | VIN_3 | input | `/driver/BUF_IN7` | R375.2 |
| 4 | V-_4 | power_in | `GND` | U27.9, C269.2, C295.2, C297.2, C253.2, U25.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | BIAS_REF_5 | input | `/driver/BUFFER_VMID` | U25.5, U23.5, R631.1, R651.1, U21.5, R671.1 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | VOUT_6 | output | `/driver/BUF7` | C268.1 |
| 7 | V+_7 | power_in | `+15V_FUSED` | C269.1, R607.1, R605.1, C253.1, U25.7, R603.1 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 8 | NC_8 | no_connect | `unconnected-(U27-NC-Pad8)` | — (no other pins on this net) |
| 9 | EP/V-_9 | passive | `GND` | U27.4, C269.2, C295.2, C297.2, C253.2, C307.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`
- pull-up resistor: R607 (10.7k 1%) on `+15V_FUSED`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: C268 (CAA572X7R1E107M670LJ) on `/driver/BUF7`

#### U30 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR0` | R361.1, R623.1, R622.1 |
| 2 | V-_2 | power_in | `-12VA` | C215.1, U38.2, U32.2, C205.1, C231.1, U34.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED0` | R621.2, R620.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK0` | R360.2, R622.2, C622.2 |
| 5 | V+_5 | power_in | `+12VA` | C214.1, C204.1, U38.5, C230.1, U32.5, C246.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C622 (150p) on `/driver/FEEDBACK0`
- series / termination resistor: R620 (10k) on `/driver/CMD_BIASED0`
- series / termination resistor: R360 (10k) on `/driver/FEEDBACK0`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R361 (15k), R622 (10M), R623 (330k) on `/driver/ERR0`

#### U31 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR1` | R363.1, R633.1, R632.1 |
| 2 | V-_2 | power_in | `-12VA` | C223.1, U33.2, C239.1, U35.2, C255.1, U37.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED1` | R631.2, R630.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK1` | R362.2, R632.2, C632.2 |
| 5 | V+_5 | power_in | `+12VA` | C222.1, C238.1, U33.5, C254.1, U35.5, C270.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C632 (150p) on `/driver/FEEDBACK1`
- series / termination resistor: R630 (10k) on `/driver/CMD_BIASED1`
- series / termination resistor: R362 (10k) on `/driver/FEEDBACK1`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R363 (15k), R632 (10M), R633 (330k) on `/driver/ERR1`

#### U32 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR2` | R365.1, R643.1, R642.1 |
| 2 | V-_2 | power_in | `-12VA` | C231.1, C215.1, U34.2, U30.2, C247.1, U38.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED2` | R641.2, R640.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK2` | R364.2, R642.2, C642.2 |
| 5 | V+_5 | power_in | `+12VA` | C230.1, C246.1, U30.5, U34.5, C214.1, C204.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C642 (150p) on `/driver/FEEDBACK2`
- series / termination resistor: R640 (10k) on `/driver/CMD_BIASED2`
- series / termination resistor: R364 (10k) on `/driver/FEEDBACK2`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R365 (15k), R642 (10M), R643 (330k) on `/driver/ERR2`

#### U33 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR3` | R367.1, R653.1, R652.1 |
| 2 | V-_2 | power_in | `-12VA` | C239.1, C223.1, U35.2, U31.2, C255.1, U37.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED3` | R651.2, R650.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK3` | R366.2, R652.2, C652.2 |
| 5 | V+_5 | power_in | `+12VA` | C238.1, C254.1, U31.5, U35.5, C222.1, C270.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C652 (150p) on `/driver/FEEDBACK3`
- series / termination resistor: R650 (10k) on `/driver/CMD_BIASED3`
- series / termination resistor: R366 (10k) on `/driver/FEEDBACK3`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R367 (15k), R652 (10M), R653 (330k) on `/driver/ERR3`

#### U34 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR4` | R369.1, R663.1, R662.1 |
| 2 | V-_2 | power_in | `-12VA` | C247.1, C231.1, U36.2, U32.2, C263.1, U41.4 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED4` | R661.2, R660.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK4` | R368.2, R662.2, C662.2 |
| 5 | V+_5 | power_in | `+12VA` | C246.1, C262.1, U36.5, U32.5, C230.1, U41.8 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C662 (150p) on `/driver/FEEDBACK4`
- series / termination resistor: R660 (10k) on `/driver/CMD_BIASED4`
- series / termination resistor: R368 (10k) on `/driver/FEEDBACK4`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R369 (15k), R662 (10M), R663 (330k) on `/driver/ERR4`

#### U35 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR5` | R371.1, R673.1, R672.1 |
| 2 | V-_2 | power_in | `-12VA` | C255.1, C239.1, U37.2, U33.2, C271.1, C307.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED5` | R671.2, R670.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK5` | R370.2, R672.2, C672.2 |
| 5 | V+_5 | power_in | `+12VA` | C254.1, C270.1, U37.5, U33.5, C238.1, C306.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C672 (150p) on `/driver/FEEDBACK5`
- series / termination resistor: R670 (10k) on `/driver/CMD_BIASED5`
- series / termination resistor: R370 (10k) on `/driver/FEEDBACK5`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R371 (15k), R672 (10M), R673 (330k) on `/driver/ERR5`

#### U36 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR6` | R373.1, R683.1, R682.1 |
| 2 | V-_2 | power_in | `-12VA` | C263.1, U41.4, C247.1, U34.2, C301.1, C303.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED6` | R681.2, R680.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK6` | R372.2, R682.2, C682.2 |
| 5 | V+_5 | power_in | `+12VA` | C262.1, U41.8, C302.1, U34.5, C246.1, C300.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C682 (150p) on `/driver/FEEDBACK6`
- series / termination resistor: R680 (10k) on `/driver/CMD_BIASED6`
- series / termination resistor: R372 (10k) on `/driver/FEEDBACK6`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R373 (15k), R682 (10M), R683 (330k) on `/driver/ERR6`

#### U37 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/ERR7` | R375.1, R693.1, R692.1 |
| 2 | V-_2 | power_in | `-12VA` | C271.1, C307.1, C255.1, U35.2, U43.4, C305.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/CMD_BIASED7` | R691.2, R690.2 |
| 4 | IN-_4 | input | `/driver/FEEDBACK7` | R374.2, R692.2, C692.2 |
| 5 | V+_5 | power_in | `+12VA` | C270.1, C306.1, U35.5, U43.8, C254.1, C304.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C692 (150p) on `/driver/FEEDBACK7`
- series / termination resistor: R690 (10k) on `/driver/CMD_BIASED7`
- series / termination resistor: R374 (10k) on `/driver/FEEDBACK7`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R375 (15k), R692 (10M), R693 (330k) on `/driver/ERR7`

#### U38 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `CURRENT_SUM` | R200.1, R110.1 |
| 2 | V-_2 | power_in | `-12VA` | C205.1, U30.2, C215.1, U32.2, C231.1, U34.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `GND` | C204.2, C205.2, C281.2, U39.2, C280.2, C202.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/SUM_NODE` | R204.2, R200.2, R208.2, R205.2, R201.2, R206.2 — 9 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | V+_5 | power_in | `+12VA` | C204.1, C214.1, U30.5, C230.1, U32.5, C246.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R201 (10k 0.1%), R202 (10k 0.1%), R203 (10k 0.1%), R204 (10k 0.1%), R205 (10k 0.1%), R206 (10k 0.1%), R207 (10k 0.1%), R208 (10k 0.1%) on `/driver/SUM_NODE`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`
- supply feed / filter: R200 (20k 0.1%) on `CURRENT_SUM`

#### U39 — OPA192IDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/BUFFER_VMID` | U39.4, U20.5, U22.5, U24.5, U26.5, U21.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | V-_2 | power_in | `GND` | C280.2, C281.2, C204.2, C214.2, U38.3, C205.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/BIAS_DIV` | C281.1, R380.2, R381.1 |
| 4 | IN-_4 | input | `/driver/BUFFER_VMID` | U39.1, U20.5, U22.5, U24.5, U26.5, U21.5 — 17 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | V+_5 | power_in | `+15V_FUSED` | C280.1, R380.1, R600.1, C213.1, U20.7, U22.7 — 40 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C281 (100n) on `/driver/BIAS_DIV`
- supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on `+15V_FUSED`
- supply feed / filter: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on `/driver/BUFFER_VMID`

#### U40 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE0` | R403.1, R201.1, C621.1, R720.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N0` | R402.2, R403.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P0` | R400.2, R401.1 |
| 4 | V-_4 | power_in | `-12VA` | C301.1, U41.4, C263.1, U36.2, C247.1, U34.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P1` | R410.2, R411.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N1` | R412.2, R413.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE1` | R413.1, R202.1, C631.1, R722.1 |
| 8 | V+_8 | power_in | `+12VA` | C300.1, U41.8, C262.1, U36.5, C302.1, C246.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C621 (100n) on `/driver/I_SENSE0`
- input / output filter capacitor: C631 (100n) on `/driver/I_SENSE1`
- pull-down resistor: R401 (10k 0.1%) on `/driver/SENSE_P0`
- pull-down resistor: R411 (10k 0.1%) on `/driver/SENSE_P1`
- series / termination resistor: R403 (10k 0.1%) on `/driver/I_SENSE0`
- series / termination resistor: R413 (10k 0.1%) on `/driver/I_SENSE1`
- series / termination resistor: R402 (10k 0.1%) on `/driver/SENSE_N0`
- series / termination resistor: R412 (10k 0.1%) on `/driver/SENSE_N1`
- series / termination resistor: R400 (10k 0.1%) on `/driver/SENSE_P0`
- series / termination resistor: R410 (10k 0.1%) on `/driver/SENSE_P1`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U41 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE2` | R423.1, R203.1, C641.1, R724.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N2` | R422.2, R423.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P2` | R420.2, R421.1 |
| 4 | V-_4 | power_in | `-12VA` | C263.1, C301.1, U36.2, C303.1, U40.4, U42.4 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P3` | R430.2, R431.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N3` | R432.2, R433.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE3` | R433.1, R204.1, C651.1, R726.1 |
| 8 | V+_8 | power_in | `+12VA` | C302.1, U36.5, C262.1, C300.1, U40.8, U42.8 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C641 (100n) on `/driver/I_SENSE2`
- input / output filter capacitor: C651 (100n) on `/driver/I_SENSE3`
- pull-down resistor: R421 (10k 0.1%) on `/driver/SENSE_P2`
- pull-down resistor: R431 (10k 0.1%) on `/driver/SENSE_P3`
- series / termination resistor: R423 (10k 0.1%) on `/driver/I_SENSE2`
- series / termination resistor: R433 (10k 0.1%) on `/driver/I_SENSE3`
- series / termination resistor: R422 (10k 0.1%) on `/driver/SENSE_N2`
- series / termination resistor: R432 (10k 0.1%) on `/driver/SENSE_N3`
- series / termination resistor: R420 (10k 0.1%) on `/driver/SENSE_P2`
- series / termination resistor: R430 (10k 0.1%) on `/driver/SENSE_P3`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U42 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE4` | R443.1, C661.1, R205.1, R728.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N4` | R442.2, R443.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P4` | R440.2, R441.1 |
| 4 | V-_4 | power_in | `-12VA` | C303.1, C305.1, U43.4, U41.4, U36.2, C263.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P5` | R450.2, R451.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N5` | R452.2, R453.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE5` | R453.1, C671.1, R206.1, R730.1 |
| 8 | V+_8 | power_in | `+12VA` | C304.1, C302.1, U43.8, U41.8, U36.5, C262.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C661 (100n) on `/driver/I_SENSE4`
- input / output filter capacitor: C671 (100n) on `/driver/I_SENSE5`
- pull-down resistor: R441 (10k 0.1%) on `/driver/SENSE_P4`
- pull-down resistor: R451 (10k 0.1%) on `/driver/SENSE_P5`
- series / termination resistor: R443 (10k 0.1%) on `/driver/I_SENSE4`
- series / termination resistor: R453 (10k 0.1%) on `/driver/I_SENSE5`
- series / termination resistor: R442 (10k 0.1%) on `/driver/SENSE_N4`
- series / termination resistor: R452 (10k 0.1%) on `/driver/SENSE_N5`
- series / termination resistor: R440 (10k 0.1%) on `/driver/SENSE_P4`
- series / termination resistor: R450 (10k 0.1%) on `/driver/SENSE_P5`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U43 — OPA2192IDR

Sheet: driver (3) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUTA_1 | output | `/driver/I_SENSE6` | R463.1, C681.1, R207.1, R732.1 |
| 2 | INA-_2 | input | `/driver/SENSE_N6` | R462.2, R463.2 |
| 3 | INA+_3 | input | `/driver/SENSE_P6` | R460.2, R461.1 |
| 4 | V-_4 | power_in | `-12VA` | C305.1, C271.1, C307.1, U37.2, U42.4, C255.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | INB+_5 | input | `/driver/SENSE_P7` | R470.2, R471.1 |
| 6 | INB-_6 | input | `/driver/SENSE_N7` | R472.2, R473.2 |
| 7 | OUTB_7 | output | `/driver/I_SENSE7` | R473.1, C691.1, R208.1, R734.1 |
| 8 | V+_8 | power_in | `+12VA` | C306.1, U37.5, C270.1, C304.1, U42.8, U35.5 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C681 (100n) on `/driver/I_SENSE6`
- input / output filter capacitor: C691 (100n) on `/driver/I_SENSE7`
- pull-down resistor: R461 (10k 0.1%) on `/driver/SENSE_P6`
- pull-down resistor: R471 (10k 0.1%) on `/driver/SENSE_P7`
- series / termination resistor: R463 (10k 0.1%) on `/driver/I_SENSE6`
- series / termination resistor: R473 (10k 0.1%) on `/driver/I_SENSE7`
- series / termination resistor: R462 (10k 0.1%) on `/driver/SENSE_N6`
- series / termination resistor: R472 (10k 0.1%) on `/driver/SENSE_N7`
- series / termination resistor: R460 (10k 0.1%) on `/driver/SENSE_P6`
- series / termination resistor: R470 (10k 0.1%) on `/driver/SENSE_P7`
- supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on `+12VA`
- supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on `-12VA`

#### U60 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT0` | TP210.1, U600.1 |
| 2 | GND_2 | power_in | `GND` | U61.2, U600.2, U62.2, U63.2, C711.2, U601.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U61.3, U62.3, U63.3, R710.2, R711.1, U64.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE0` | R721.2, R720.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U61.5, R729.1, U600.5, R721.1, C711.1, U62.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-up resistor: R729 (100k 0.1%) on `+3.3V`
- pull-up resistor: R721 (100k 0.1%) on `/driver/TRIP_SENSE0`
- series / termination resistor: R720 (10k 0.1%) on `/driver/TRIP_SENSE0`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U61 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT1` | TP211.1, U600.3 |
| 2 | GND_2 | power_in | `GND` | U60.2, U600.2, C711.2, U63.2, U62.2, U601.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U60.3, U63.3, U62.3, R710.2, R711.1, U65.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE1` | R723.2, R722.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U60.5, U600.5, R729.1, C711.1, U63.5, U62.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R722 (10k 0.1%) on `/driver/TRIP_SENSE1`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U62 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT2` | TP212.1, U601.1 |
| 2 | GND_2 | power_in | `GND` | U63.2, C711.2, U600.2, U601.2, U60.2, U64.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U63.3, U60.3, U64.3, U61.3, U65.3, R711.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE2` | R725.2, R724.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U63.5, C711.1, R731.1, U600.5, U601.5, R729.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-down resistor: R711 (10k 0.1%) on `/driver/TRIP_REF`
- pull-up resistor: R723 (100k 0.1%), R731 (100k 0.1%) on `+3.3V`
- pull-up resistor: R710 (52.3k 0.1%) on `/driver/TRIP_REF`
- series / termination resistor: R724 (10k 0.1%) on `/driver/TRIP_SENSE2`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U63 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT3` | TP213.1, U601.3 |
| 2 | GND_2 | power_in | `GND` | U62.2, C711.2, U600.2, U601.2, C712.2, U61.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U62.3, U61.3, U65.3, U60.3, U64.3, R711.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE3` | R727.2, R726.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U62.5, C711.1, U600.5, U601.5, R731.1, R729.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R726 (10k 0.1%) on `/driver/TRIP_SENSE3`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U64 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT4` | TP214.1, U602.1 |
| 2 | GND_2 | power_in | `GND` | U65.2, C712.2, U601.2, U602.2, U62.2, U66.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U65.3, U62.3, U66.3, U63.3, U67.3, C710.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE4` | R729.2, R728.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U65.5, C712.1, U601.5, R733.1, U602.5, R731.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-up resistor: R725 (100k 0.1%), R733 (100k 0.1%) on `+3.3V`
- series / termination resistor: R728 (10k 0.1%) on `/driver/TRIP_SENSE4`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U65 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT5` | TP215.1, U602.3 |
| 2 | GND_2 | power_in | `GND` | U64.2, C712.2, U601.2, U602.2, C713.2, U63.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U64.3, U63.3, U67.3, U62.3, U66.3, C710.1 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE5` | R731.2, R730.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U64.5, C712.1, U601.5, U602.5, R733.1, R731.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R730 (10k 0.1%) on `/driver/TRIP_SENSE5`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U66 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT6` | TP216.1, U603.1 |
| 2 | GND_2 | power_in | `GND` | U67.2, C713.2, U602.2, U603.2, U64.2, U65.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U67.3, U64.3, U65.3, C710.1, U62.3, U63.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE6` | R733.2, R732.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U67.5, C713.1, U602.5, R735.1, U603.5, R733.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C710 (100n) on `/driver/TRIP_REF`
- pull-up resistor: R727 (100k 0.1%), R735 (100k 0.1%) on `+3.3V`
- series / termination resistor: R732 (10k 0.1%) on `/driver/TRIP_SENSE6`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U67 — TLV3201AIDBVR

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/driver/FAULT7` | TP217.1, U603.3 |
| 2 | GND_2 | power_in | `GND` | U66.2, C713.2, U602.2, U603.2, C714.2, U65.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | IN+_3 | input | `/driver/TRIP_REF` | U66.3, U65.3, U64.3, C710.1, U63.3, U62.3 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | IN-_4 | input | `/driver/TRIP_SENSE7` | R735.2, R734.2 |
| 5 | VCC_5 | power_in | `+3.3V` | U66.5, C713.1, U602.5, U603.5, R735.1, R733.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- series / termination resistor: R734 (10k 0.1%) on `/driver/TRIP_SENSE7`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U80 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U80.16, C210.1, U10.7, U82.1, C200.1, U82.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA0` | R222.2, R220.2, R221.2 |
| 3 | NC_3 | passive | `GND` | U80.5, U80.10, U80.12, U80.14, U80.9, U80.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA0` | R222.1 |
| 5 | NC_5 | passive | `GND` | U80.10, U80.3, U80.12, U80.14, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA0` | R221.1, R223.1 |
| 7 | AGND_7 | passive | `/driver/AGND0` | C211.1 |
| 8 | V-_8 | power_in | `GND` | U80.9, U80.14, U80.12, U80.10, C210.2, U80.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U80.8, U80.3, U80.5, U80.10, U80.12, U80.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U80.12, U80.5, U80.14, U80.3, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB0` | R224.2, R223.2, R225.2 |
| 12 | NC_12 | passive | `GND` | U80.10, U80.14, U80.5, U80.3, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB0` | R225.1 |
| 14 | NC_14 | passive | `GND` | U80.12, U80.10, U80.5, U80.3, U80.8, U80.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER0` | R224.1, C620.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U80.1, C210.1, U82.1, U10.7, U82.16, C226.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C620 (1u) on `/driver/FILTER0`
- series / termination resistor: R224 (42.7k 0.1%) on `/driver/FILTER0`
- series / termination resistor: R222 (42.7k 0.1%) on `/driver/INVA0`
- series / termination resistor: R225 (42.7k 0.1%) on `/driver/INVB0`
- series / termination resistor: R221 (42.7k 0.1%), R223 (42.7k 0.1%) on `/driver/LPA0`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C211 (100n) on `/driver/AGND0`

#### U81 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U81.16, C218.1, U83.1, U83.16, C234.1, U85.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA1` | R232.2, R230.2, R231.2 |
| 3 | NC_3 | passive | `GND` | U81.5, U81.10, U81.12, U81.14, U81.9, U81.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA1` | R232.1 |
| 5 | NC_5 | passive | `GND` | U81.10, U81.3, U81.12, U81.14, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA1` | R231.1, R233.1 |
| 7 | AGND_7 | passive | `/driver/AGND1` | C219.1 |
| 8 | V-_8 | power_in | `GND` | U81.9, U81.14, U81.12, U81.10, C218.2, U81.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U81.8, U81.3, U81.5, U81.10, U81.12, U81.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U81.12, U81.5, U81.14, U81.3, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB1` | R234.2, R233.2, R235.2 |
| 12 | NC_12 | passive | `GND` | U81.10, U81.14, U81.5, U81.3, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB1` | R235.1 |
| 14 | NC_14 | passive | `GND` | U81.12, U81.10, U81.5, U81.3, U81.8, U81.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER1` | R234.1, C630.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U81.1, C218.1, U83.1, U83.16, C234.1, U85.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- filter capacitor to ground: C282 (EEUFR1E102) on `GND`
- input / output filter capacitor: C630 (1u) on `/driver/FILTER1`
- series / termination resistor: R234 (42.7k 0.1%) on `/driver/FILTER1`
- series / termination resistor: R232 (42.7k 0.1%) on `/driver/INVA1`
- series / termination resistor: R235 (42.7k 0.1%) on `/driver/INVB1`
- series / termination resistor: R231 (42.7k 0.1%), R233 (42.7k 0.1%) on `/driver/LPA1`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C219 (100n) on `/driver/AGND1`

#### U82 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U82.16, C226.1, C210.1, U80.16, U84.1, U80.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA2` | R242.2, R240.2, R241.2 |
| 3 | NC_3 | passive | `GND` | U82.5, U82.10, U82.12, U82.14, U82.9, U82.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA2` | R242.1 |
| 5 | NC_5 | passive | `GND` | U82.10, U82.3, U82.12, U82.14, U82.8, U82.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA2` | R241.1, R243.1 |
| 7 | AGND_7 | passive | `/driver/AGND2` | C227.1 |
| 8 | V-_8 | power_in | `GND` | U82.9, U82.14, C226.2, U82.12, U82.10, U82.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U82.8, U82.3, U82.5, U82.10, U82.12, U82.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U82.12, U82.5, U82.14, U82.3, U82.8, U82.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB2` | R244.2, R243.2, R245.2 |
| 12 | NC_12 | passive | `GND` | U82.10, U82.14, U82.5, U82.3, U82.8, U82.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB2` | R245.1 |
| 14 | NC_14 | passive | `GND` | U82.12, U82.10, U82.5, U82.3, U82.8, C226.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER2` | R244.1, C640.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U82.1, C226.1, C210.1, U84.1, U80.16, U84.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C640 (1u) on `/driver/FILTER2`
- series / termination resistor: R244 (42.7k 0.1%) on `/driver/FILTER2`
- series / termination resistor: R242 (42.7k 0.1%) on `/driver/INVA2`
- series / termination resistor: R245 (42.7k 0.1%) on `/driver/INVB2`
- series / termination resistor: R241 (42.7k 0.1%), R243 (42.7k 0.1%) on `/driver/LPA2`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C227 (100n) on `/driver/AGND2`

#### U83 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U83.16, C234.1, C218.1, U81.16, U85.1, U81.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA3` | R252.2, R250.2, R251.2 |
| 3 | NC_3 | passive | `GND` | U83.5, U83.10, U83.12, U83.14, U83.9, U83.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA3` | R252.1 |
| 5 | NC_5 | passive | `GND` | U83.10, U83.3, U83.12, U83.14, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA3` | R251.1, R253.1 |
| 7 | AGND_7 | passive | `/driver/AGND3` | C235.1 |
| 8 | V-_8 | power_in | `GND` | U83.9, U83.14, C234.2, U83.12, U83.10, U83.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U83.8, U83.3, U83.5, U83.10, U83.12, U83.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U83.12, U83.5, U83.14, U83.3, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB3` | R254.2, R253.2, R255.2 |
| 12 | NC_12 | passive | `GND` | U83.10, U83.14, U83.5, U83.3, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB3` | R255.1 |
| 14 | NC_14 | passive | `GND` | U83.12, U83.10, U83.5, U83.3, U83.8, U83.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER3` | R254.1, C650.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U83.1, C234.1, C218.1, U85.1, U81.16, U85.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C650 (1u) on `/driver/FILTER3`
- series / termination resistor: R254 (42.7k 0.1%) on `/driver/FILTER3`
- series / termination resistor: R252 (42.7k 0.1%) on `/driver/INVA3`
- series / termination resistor: R255 (42.7k 0.1%) on `/driver/INVB3`
- series / termination resistor: R251 (42.7k 0.1%), R253 (42.7k 0.1%) on `/driver/LPA3`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C235 (100n) on `/driver/AGND3`

#### U84 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U84.16, C242.1, C226.1, U82.16, U86.1, U82.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA4` | R262.2, R260.2, R261.2 |
| 3 | NC_3 | passive | `GND` | U84.5, U84.10, U84.12, U84.14, U84.9, U84.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA4` | R262.1 |
| 5 | NC_5 | passive | `GND` | U84.3, U84.10, U84.12, U84.14, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA4` | R261.1, R263.1 |
| 7 | AGND_7 | passive | `/driver/AGND4` | C243.1 |
| 8 | V-_8 | power_in | `GND` | U84.9, U84.14, U84.12, C242.2, U84.10, U84.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U84.8, U84.3, U84.5, U84.10, U84.12, U84.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U84.12, U84.5, U84.14, U84.3, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB4` | R264.2, R263.2, R265.2 |
| 12 | NC_12 | passive | `GND` | U84.14, U84.10, U84.5, U84.3, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB4` | R265.1 |
| 14 | NC_14 | passive | `GND` | U84.12, U84.10, U84.5, U84.3, U84.8, U84.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER4` | R264.1, C660.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U84.1, C242.1, C226.1, U86.1, U86.16, U82.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C660 (1u) on `/driver/FILTER4`
- series / termination resistor: R264 (42.7k 0.1%) on `/driver/FILTER4`
- series / termination resistor: R262 (42.7k 0.1%) on `/driver/INVA4`
- series / termination resistor: R265 (42.7k 0.1%) on `/driver/INVB4`
- series / termination resistor: R261 (42.7k 0.1%), R263 (42.7k 0.1%) on `/driver/LPA4`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C243 (100n) on `/driver/AGND4`

#### U85 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U85.16, C250.1, C234.1, U83.16, U87.1, U83.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA5` | R272.2, R270.2, R271.2 |
| 3 | NC_3 | passive | `GND` | U85.5, U85.10, U85.12, U85.14, U85.9, U85.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA5` | R272.1 |
| 5 | NC_5 | passive | `GND` | U85.3, U85.10, U85.12, U85.14, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA5` | R271.1, R273.1 |
| 7 | AGND_7 | passive | `/driver/AGND5` | C251.1 |
| 8 | V-_8 | power_in | `GND` | U85.9, U85.14, C250.2, U85.12, U85.10, U85.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U85.8, U85.3, U85.5, U85.10, U85.12, U85.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U85.12, U85.5, U85.14, U85.3, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB5` | R274.2, R273.2, R275.2 |
| 12 | NC_12 | passive | `GND` | U85.14, U85.10, U85.5, U85.3, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB5` | R275.1 |
| 14 | NC_14 | passive | `GND` | U85.12, U85.10, U85.5, U85.3, U85.8, U85.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER5` | R274.1, C670.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U85.1, C250.1, C234.1, U87.1, U87.16, U83.16 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C670 (1u) on `/driver/FILTER5`
- series / termination resistor: R274 (42.7k 0.1%) on `/driver/FILTER5`
- series / termination resistor: R272 (42.7k 0.1%) on `/driver/INVA5`
- series / termination resistor: R275 (42.7k 0.1%) on `/driver/INVB5`
- series / termination resistor: R271 (42.7k 0.1%), R273 (42.7k 0.1%) on `/driver/LPA5`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C251 (100n) on `/driver/AGND5`

#### U86 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U86.16, C258.1, C242.1, U84.16, U84.1, C226.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA6` | R282.2, R280.2, R281.2 |
| 3 | NC_3 | passive | `GND` | U86.5, U86.10, U86.12, U86.14, U86.9, U86.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA6` | R282.1 |
| 5 | NC_5 | passive | `GND` | U86.10, U86.3, U86.12, U86.14, U86.8, U86.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA6` | R281.1, R283.1 |
| 7 | AGND_7 | passive | `/driver/AGND6` | C259.1 |
| 8 | V-_8 | power_in | `GND` | U86.9, U86.14, C258.2, U86.12, U86.10, U86.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U86.8, U86.3, U86.5, U86.10, U86.12, U86.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U86.12, U86.5, U86.14, U86.3, U86.8, U86.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB6` | R284.2, R283.2, R285.2 |
| 12 | NC_12 | passive | `GND` | U86.10, U86.14, U86.5, U86.3, U86.8, U86.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB6` | R285.1 |
| 14 | NC_14 | passive | `GND` | U86.12, U86.10, U86.5, U86.3, U86.8, C258.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER6` | R284.1, C680.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U86.1, C258.1, C242.1, U84.16, U84.1, C226.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C680 (1u) on `/driver/FILTER6`
- series / termination resistor: R284 (42.7k 0.1%) on `/driver/FILTER6`
- series / termination resistor: R282 (42.7k 0.1%) on `/driver/INVA6`
- series / termination resistor: R285 (42.7k 0.1%) on `/driver/INVB6`
- series / termination resistor: R281 (42.7k 0.1%), R283 (42.7k 0.1%) on `/driver/LPA6`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C259 (100n) on `/driver/AGND6`

#### U87 — LTC1563-2IGN#PBF

Sheet: driver (3) · Footprint: Package_SO:SSOP-16_3.9x4.9mm_P0.635mm · 16 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | LP_1 | input | `+5V_EXC` | U87.16, C266.1, C250.1, U85.16, U85.1, C234.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 2 | SA_2 | passive | `/driver/SA7` | R292.2, R290.2, R291.2 |
| 3 | NC_3 | passive | `GND` | U87.5, U87.10, U87.12, U87.14, U87.9, U87.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 4 | INVA_4 | input | `/driver/INVA7` | R292.1 |
| 5 | NC_5 | passive | `GND` | U87.10, U87.3, U87.12, U87.14, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | LPA_6 | output | `/driver/LPA7` | R291.1, R293.1 |
| 7 | AGND_7 | passive | `/driver/AGND7` | C267.1 |
| 8 | V-_8 | power_in | `GND` | U87.9, U87.14, C266.2, U87.12, U87.10, U87.5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 9 | ~{EN}_9 | input | `GND` | U87.8, U87.3, U87.5, U87.10, U87.12, U87.14 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 10 | NC_10 | passive | `GND` | U87.12, U87.5, U87.14, U87.3, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 11 | SB_11 | passive | `/driver/SB7` | R294.2, R293.2, R295.2 |
| 12 | NC_12 | passive | `GND` | U87.10, U87.14, U87.5, U87.3, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 13 | INVB_13 | input | `/driver/INVB7` | R295.1 |
| 14 | NC_14 | passive | `GND` | U87.12, U87.10, U87.5, U87.3, U87.8, U87.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 15 | LPB_15 | output | `/driver/FILTER7` | R294.1, C690.1 |
| 16 | V+_16 | power_in | `+5V_EXC` | U87.1, C266.1, C250.1, U85.16, U85.1, C234.1 — 30 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- input / output filter capacitor: C690 (1u) on `/driver/FILTER7`
- series / termination resistor: R294 (42.7k 0.1%) on `/driver/FILTER7`
- series / termination resistor: R292 (42.7k 0.1%) on `/driver/INVA7`
- series / termination resistor: R295 (42.7k 0.1%) on `/driver/INVB7`
- series / termination resistor: R291 (42.7k 0.1%), R293 (42.7k 0.1%) on `/driver/LPA7`
- supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on `+5V_EXC`
- supply decoupling: C267 (100n) on `/driver/AGND7`

#### U600 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT0` | TP210.1, U60.1 |
| 2 | GND_2 | power_in | `GND` | C711.2, U63.2, U61.2, U62.2, U60.2, U601.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT1` | TP211.1, U61.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U600.6, U601.4, U601.6, R712.2, U602.4, U602.6 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C711.1, U63.5, U62.5, U61.5, U60.5, R729.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U600.4, U601.6, U601.4, R712.2, U602.6, U602.4 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U601 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT2` | TP212.1, U62.1 |
| 2 | GND_2 | power_in | `GND` | C712.2, U65.2, C711.2, U63.2, U64.2, U62.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT3` | TP213.1, U63.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U601.6, U600.4, U602.4, U600.6, U602.6, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C712.1, U65.5, U64.5, U63.5, U62.5, R731.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U601.4, U600.6, U602.6, U600.4, U602.4, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- pull-up resistor: R712 (4.7k) on `/DRIVER_FAULT_N`
- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U602 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT4` | TP214.1, U64.1 |
| 2 | GND_2 | power_in | `GND` | C713.2, U67.2, C712.2, U65.2, U66.2, U64.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT5` | TP215.1, U65.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U602.6, U603.4, U601.4, U603.6, U601.6, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C713.1, U67.5, U66.5, U65.5, U64.5, R733.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U602.4, U603.6, U601.6, U603.4, U601.4, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### U603 — SN74LVC2G07DBVR, 74LVC2G07

Sheet: driver (3) · Footprint: Package_TO_SOT_SMD:SOT-23-6 · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | — | input | `/driver/FAULT6` | TP216.1, U66.1 |
| 2 | GND_2 | power_in | `GND` | C714.2, C713.2, U67.2, U66.2, U602.2, U65.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 3 | — | input | `/driver/FAULT7` | TP217.1, U67.1 |
| 4 | — | open_collector | `/DRIVER_FAULT_N` | U603.6, U602.4, U602.6, U601.4, U601.6, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 5 | VCC_5 | power_in | `+3.3V` | C714.1, U67.5, U66.5, R735.1, C713.1, U602.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.3 |
| 6 | — | open_collector | `/DRIVER_FAULT_N` | U603.4, U602.6, U602.4, U601.6, U601.4, R712.2 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.3 |

Supporting passives:

- supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on `+3.3V`

#### C200 — 100n, C

C200 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C201 — 1u, C

C201 — 1u, C_0805_2012Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C202 — 100n, C

C202 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C203 — 150n, C

C203 — 150n, C_0603_1608Metric — `/driver/DAC_REF` ↔ `GND` — soft-start / bias capacitor for U10 (pin 1 → 2).

#### C204 — 100n, C

C204 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C205 — 100n, C

C205 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C210 — 100n, C

C210 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C211 — 100n, C

C211 — 100n, C_0603_1608Metric — `/driver/AGND0` ↔ `GND` — supply decoupling for U80 (pin 1 → 2).

#### C212 — CAA572X7R1E107M670LJ, C

C212 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF0` ↔ `FG0_OUT` — supply feed / filter for U20 (pin 1 → 2).

#### C213 — 100n, C

C213 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C214 — 100n, C

C214 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C215 — 100n, C

C215 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C218 — 100n, C

C218 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C219 — 100n, C

C219 — 100n, C_0603_1608Metric — `/driver/AGND1` ↔ `GND` — supply decoupling for U81 (pin 1 → 2).

#### C220 — CAA572X7R1E107M670LJ, C

C220 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF1` ↔ `FG1_OUT` — supply feed / filter for U21 (pin 1 → 2).

#### C221 — 100n, C

C221 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C222 — 100n, C

C222 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C223 — 100n, C

C223 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C226 — 100n, C

C226 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C227 — 100n, C

C227 — 100n, C_0603_1608Metric — `/driver/AGND2` ↔ `GND` — supply decoupling for U82 (pin 1 → 2).

#### C228 — CAA572X7R1E107M670LJ, C

C228 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF2` ↔ `FG2_OUT` — supply feed / filter for U22 (pin 1 → 2).

#### C229 — 100n, C

C229 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C230 — 100n, C

C230 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C231 — 100n, C

C231 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C234 — 100n, C

C234 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C235 — 100n, C

C235 — 100n, C_0603_1608Metric — `/driver/AGND3` ↔ `GND` — supply decoupling for U83 (pin 1 → 2).

#### C236 — CAA572X7R1E107M670LJ, C

C236 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF3` ↔ `FG3_OUT` — supply feed / filter for U23 (pin 1 → 2).

#### C237 — 100n, C

C237 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C238 — 100n, C

C238 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C239 — 100n, C

C239 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C242 — 100n, C

C242 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C243 — 100n, C

C243 — 100n, C_0603_1608Metric — `/driver/AGND4` ↔ `GND` — supply decoupling for U84 (pin 1 → 2).

#### C244 — CAA572X7R1E107M670LJ, C

C244 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF4` ↔ `FG4_OUT` — supply feed / filter for U24 (pin 1 → 2).

#### C245 — 100n, C

C245 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C246 — 100n, C

C246 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C247 — 100n, C

C247 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C250 — 100n, C

C250 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C251 — 100n, C

C251 — 100n, C_0603_1608Metric — `/driver/AGND5` ↔ `GND` — supply decoupling for U85 (pin 1 → 2).

#### C252 — CAA572X7R1E107M670LJ, C

C252 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF5` ↔ `FG5_OUT` — supply feed / filter for U25 (pin 1 → 2).

#### C253 — 100n, C

C253 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C254 — 100n, C

C254 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C255 — 100n, C

C255 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C258 — 100n, C

C258 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C259 — 100n, C

C259 — 100n, C_0603_1608Metric — `/driver/AGND6` ↔ `GND` — supply decoupling for U86 (pin 1 → 2).

#### C260 — CAA572X7R1E107M670LJ, C

C260 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF6` ↔ `FG6_OUT` — supply feed / filter for U26 (pin 1 → 2).

#### C261 — 100n, C

C261 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C262 — 100n, C

C262 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C263 — 100n, C

C263 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C266 — 100n, C

C266 — 100n, C_0603_1608Metric — `+5V_EXC` ↔ `GND` — feedback filter, supply decoupling for U10, U80, U81, U82, U83, U84, U85, U86, U87, U149 (pin 1 → 2).

#### C267 — 100n, C

C267 — 100n, C_0603_1608Metric — `/driver/AGND7` ↔ `GND` — supply decoupling for U87 (pin 1 → 2).

#### C268 — CAA572X7R1E107M670LJ, C

C268 — CAA572X7R1E107M670LJ, TDK_CAA572 — `/driver/BUF7` ↔ `FG7_OUT` — supply feed / filter for U27 (pin 1 → 2).

#### C269 — 100n, C

C269 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C270 — 100n, C

C270 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C271 — 100n, C

C271 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C280 — 100n, C

C280 — 100n, C_0603_1608Metric — `+15V_FUSED` ↔ `GND` — supply decoupling for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### C281 — 100n, C

C281 — 100n, C_0603_1608Metric — `/driver/BIAS_DIV` ↔ `GND` — filter capacitor to ground for U39 (pin 1 → 2).

#### C282 — EEUFR1E102, C_Polarized

C282 — EEUFR1E102, CP_Radial_D10.0mm_P5.00mm — `/driver/VMID_7V5` ↔ `GND` — filter capacitor to ground for U81 (pin 1 → 2).

#### C283 — 100n, C

C283 — 100n, C_0603_1608Metric — `/driver/VMID_7V5` ↔ `GND` — filter capacitor to ground for TP823 (pin 1 → 2).

#### C290 — 100n, C

C290 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C291 — 100n, C

C291 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C292 — 100n, C

C292 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C293 — 100n, C

C293 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C294 — 100n, C

C294 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C295 — 100n, C

C295 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C296 — 100n, C

C296 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C297 — 100n, C

C297 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C300 — 100n, C

C300 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C301 — 100n, C

C301 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C302 — 100n, C

C302 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C303 — 100n, C

C303 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C304 — 100n, C

C304 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C305 — 100n, C

C305 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C306 — 100n, C

C306 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C307 — 100n, C

C307 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U30, U31, U32, U33, U34, U35, U36, U37, U38, U40, U41, U42, U43 (pin 1 → 2).

#### C620 — 1u, C

C620 — 1u, C_0805_2012Metric — `/driver/FILTER0` ↔ `/driver/CMD_AC0` — input / output filter capacitor for U80 (pin 1 → 2).

#### C621 — 100n, C

C621 — 100n, C_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/SENSE_AC0` — input / output filter capacitor for U40 (pin 1 → 2).

#### C622 — 150p, C

C622 — 150p, C_0603_1608Metric — `/driver/COMP0` ↔ `/driver/FEEDBACK0` — input / output filter capacitor for U30 (pin 1 → 2).

#### C630 — 1u, C

C630 — 1u, C_0805_2012Metric — `/driver/FILTER1` ↔ `/driver/CMD_AC1` — input / output filter capacitor for U81 (pin 1 → 2).

#### C631 — 100n, C

C631 — 100n, C_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/SENSE_AC1` — input / output filter capacitor for U40 (pin 1 → 2).

#### C632 — 150p, C

C632 — 150p, C_0603_1608Metric — `/driver/COMP1` ↔ `/driver/FEEDBACK1` — input / output filter capacitor for U31 (pin 1 → 2).

#### C640 — 1u, C

C640 — 1u, C_0805_2012Metric — `/driver/FILTER2` ↔ `/driver/CMD_AC2` — input / output filter capacitor for U82 (pin 1 → 2).

#### C641 — 100n, C

C641 — 100n, C_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/SENSE_AC2` — input / output filter capacitor for U41 (pin 1 → 2).

#### C642 — 150p, C

C642 — 150p, C_0603_1608Metric — `/driver/COMP2` ↔ `/driver/FEEDBACK2` — input / output filter capacitor for U32 (pin 1 → 2).

#### C650 — 1u, C

C650 — 1u, C_0805_2012Metric — `/driver/FILTER3` ↔ `/driver/CMD_AC3` — input / output filter capacitor for U83 (pin 1 → 2).

#### C651 — 100n, C

C651 — 100n, C_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/SENSE_AC3` — input / output filter capacitor for U41 (pin 1 → 2).

#### C652 — 150p, C

C652 — 150p, C_0603_1608Metric — `/driver/COMP3` ↔ `/driver/FEEDBACK3` — input / output filter capacitor for U33 (pin 1 → 2).

#### C660 — 1u, C

C660 — 1u, C_0805_2012Metric — `/driver/FILTER4` ↔ `/driver/CMD_AC4` — input / output filter capacitor for U84 (pin 1 → 2).

#### C661 — 100n, C

C661 — 100n, C_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/SENSE_AC4` — input / output filter capacitor for U42 (pin 1 → 2).

#### C662 — 150p, C

C662 — 150p, C_0603_1608Metric — `/driver/COMP4` ↔ `/driver/FEEDBACK4` — input / output filter capacitor for U34 (pin 1 → 2).

#### C670 — 1u, C

C670 — 1u, C_0805_2012Metric — `/driver/FILTER5` ↔ `/driver/CMD_AC5` — input / output filter capacitor for U85 (pin 1 → 2).

#### C671 — 100n, C

C671 — 100n, C_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/SENSE_AC5` — input / output filter capacitor for U42 (pin 1 → 2).

#### C672 — 150p, C

C672 — 150p, C_0603_1608Metric — `/driver/COMP5` ↔ `/driver/FEEDBACK5` — input / output filter capacitor for U35 (pin 1 → 2).

#### C680 — 1u, C

C680 — 1u, C_0805_2012Metric — `/driver/FILTER6` ↔ `/driver/CMD_AC6` — input / output filter capacitor for U86 (pin 1 → 2).

#### C681 — 100n, C

C681 — 100n, C_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/SENSE_AC6` — input / output filter capacitor for U43 (pin 1 → 2).

#### C682 — 150p, C

C682 — 150p, C_0603_1608Metric — `/driver/COMP6` ↔ `/driver/FEEDBACK6` — input / output filter capacitor for U36 (pin 1 → 2).

#### C690 — 1u, C

C690 — 1u, C_0805_2012Metric — `/driver/FILTER7` ↔ `/driver/CMD_AC7` — input / output filter capacitor for U87 (pin 1 → 2).

#### C691 — 100n, C

C691 — 100n, C_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/SENSE_AC7` — input / output filter capacitor for U43 (pin 1 → 2).

#### C692 — 150p, C

C692 — 150p, C_0603_1608Metric — `/driver/COMP7` ↔ `/driver/FEEDBACK7` — input / output filter capacitor for U37 (pin 1 → 2).

#### C710 — 100n, C

C710 — 100n, C_0603_1608Metric — `/driver/TRIP_REF` ↔ `GND` — filter capacitor to ground for U66 (pin 1 → 2).

#### C711 — 100n, C

C711 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C712 — 100n, C

C712 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C713 — 100n, C

C713 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### C714 — 100n, C

C714 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U60, U61, U62, U63, U64, U65, U66, U67, U142, U600, U601, U602, U603, U751, U753, Y1 (pin 1 → 2).

#### R20 — 1.00 0.1% 0.5W, R

R20 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG0_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R21 — 1.00 0.1% 0.5W, R

R21 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG1_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R22 — 1.00 0.1% 0.5W, R

R22 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG2_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R23 — 1.00 0.1% 0.5W, R

R23 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG3_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R24 — 1.00 0.1% 0.5W, R

R24 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG4_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R25 — 1.00 0.1% 0.5W, R

R25 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG5_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R26 — 1.00 0.1% 0.5W, R

R26 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG6_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R27 — 1.00 0.1% 0.5W, R

R27 — 1.00 0.1% 0.5W, R_2512_6332Metric — `FG7_RETURN` ↔ `/driver/VMID_7V5` — series / termination resistor for TP823 (pin 1 → 2).

#### R200 — 20k 0.1%, R

R200 — 20k 0.1%, R_0603_1608Metric — `CURRENT_SUM` ↔ `/driver/SUM_NODE` — supply feed / filter for U38 (pin 1 → 2).

#### R201 — 10k 0.1%, R

R201 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R202 — 10k 0.1%, R

R202 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R203 — 10k 0.1%, R

R203 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R204 — 10k 0.1%, R

R204 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R205 — 10k 0.1%, R

R205 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R206 — 10k 0.1%, R

R206 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R207 — 10k 0.1%, R

R207 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R208 — 10k 0.1%, R

R208 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/SUM_NODE` — series / termination resistor for U38 (pin 1 → 2).

#### R220 — 42.7k 0.1%, R

R220 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC0` ↔ `/driver/SA0` — supply feed / filter for U10 (pin 1 → 2).

#### R221 — 42.7k 0.1%, R

R221 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA0` ↔ `/driver/SA0` — series / termination resistor for U80 (pin 1 → 2).

#### R222 — 42.7k 0.1%, R

R222 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA0` ↔ `/driver/SA0` — series / termination resistor for U80 (pin 1 → 2).

#### R223 — 42.7k 0.1%, R

R223 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA0` ↔ `/driver/SB0` — series / termination resistor for U80 (pin 1 → 2).

#### R224 — 42.7k 0.1%, R

R224 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER0` ↔ `/driver/SB0` — series / termination resistor for U80 (pin 1 → 2).

#### R225 — 42.7k 0.1%, R

R225 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB0` ↔ `/driver/SB0` — series / termination resistor for U80 (pin 1 → 2).

#### R230 — 42.7k 0.1%, R

R230 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC1` ↔ `/driver/SA1` — supply feed / filter for U10 (pin 1 → 2).

#### R231 — 42.7k 0.1%, R

R231 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA1` ↔ `/driver/SA1` — series / termination resistor for U81 (pin 1 → 2).

#### R232 — 42.7k 0.1%, R

R232 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA1` ↔ `/driver/SA1` — series / termination resistor for U81 (pin 1 → 2).

#### R233 — 42.7k 0.1%, R

R233 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA1` ↔ `/driver/SB1` — series / termination resistor for U81 (pin 1 → 2).

#### R234 — 42.7k 0.1%, R

R234 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER1` ↔ `/driver/SB1` — series / termination resistor for U81 (pin 1 → 2).

#### R235 — 42.7k 0.1%, R

R235 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB1` ↔ `/driver/SB1` — series / termination resistor for U81 (pin 1 → 2).

#### R240 — 42.7k 0.1%, R

R240 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC2` ↔ `/driver/SA2` — supply feed / filter for U10 (pin 1 → 2).

#### R241 — 42.7k 0.1%, R

R241 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA2` ↔ `/driver/SA2` — series / termination resistor for U82 (pin 1 → 2).

#### R242 — 42.7k 0.1%, R

R242 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA2` ↔ `/driver/SA2` — series / termination resistor for U82 (pin 1 → 2).

#### R243 — 42.7k 0.1%, R

R243 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA2` ↔ `/driver/SB2` — series / termination resistor for U82 (pin 1 → 2).

#### R244 — 42.7k 0.1%, R

R244 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER2` ↔ `/driver/SB2` — series / termination resistor for U82 (pin 1 → 2).

#### R245 — 42.7k 0.1%, R

R245 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB2` ↔ `/driver/SB2` — series / termination resistor for U82 (pin 1 → 2).

#### R250 — 42.7k 0.1%, R

R250 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC3` ↔ `/driver/SA3` — supply feed / filter for U10 (pin 1 → 2).

#### R251 — 42.7k 0.1%, R

R251 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA3` ↔ `/driver/SA3` — series / termination resistor for U83 (pin 1 → 2).

#### R252 — 42.7k 0.1%, R

R252 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA3` ↔ `/driver/SA3` — series / termination resistor for U83 (pin 1 → 2).

#### R253 — 42.7k 0.1%, R

R253 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA3` ↔ `/driver/SB3` — series / termination resistor for U83 (pin 1 → 2).

#### R254 — 42.7k 0.1%, R

R254 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER3` ↔ `/driver/SB3` — series / termination resistor for U83 (pin 1 → 2).

#### R255 — 42.7k 0.1%, R

R255 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB3` ↔ `/driver/SB3` — series / termination resistor for U83 (pin 1 → 2).

#### R260 — 42.7k 0.1%, R

R260 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC4` ↔ `/driver/SA4` — supply feed / filter for U10 (pin 1 → 2).

#### R261 — 42.7k 0.1%, R

R261 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA4` ↔ `/driver/SA4` — series / termination resistor for U84 (pin 1 → 2).

#### R262 — 42.7k 0.1%, R

R262 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA4` ↔ `/driver/SA4` — series / termination resistor for U84 (pin 1 → 2).

#### R263 — 42.7k 0.1%, R

R263 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA4` ↔ `/driver/SB4` — series / termination resistor for U84 (pin 1 → 2).

#### R264 — 42.7k 0.1%, R

R264 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER4` ↔ `/driver/SB4` — series / termination resistor for U84 (pin 1 → 2).

#### R265 — 42.7k 0.1%, R

R265 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB4` ↔ `/driver/SB4` — series / termination resistor for U84 (pin 1 → 2).

#### R270 — 42.7k 0.1%, R

R270 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC5` ↔ `/driver/SA5` — supply feed / filter for U10 (pin 1 → 2).

#### R271 — 42.7k 0.1%, R

R271 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA5` ↔ `/driver/SA5` — series / termination resistor for U85 (pin 1 → 2).

#### R272 — 42.7k 0.1%, R

R272 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA5` ↔ `/driver/SA5` — series / termination resistor for U85 (pin 1 → 2).

#### R273 — 42.7k 0.1%, R

R273 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA5` ↔ `/driver/SB5` — series / termination resistor for U85 (pin 1 → 2).

#### R274 — 42.7k 0.1%, R

R274 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER5` ↔ `/driver/SB5` — series / termination resistor for U85 (pin 1 → 2).

#### R275 — 42.7k 0.1%, R

R275 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB5` ↔ `/driver/SB5` — series / termination resistor for U85 (pin 1 → 2).

#### R280 — 42.7k 0.1%, R

R280 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC6` ↔ `/driver/SA6` — supply feed / filter for U10 (pin 1 → 2).

#### R281 — 42.7k 0.1%, R

R281 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA6` ↔ `/driver/SA6` — series / termination resistor for U86 (pin 1 → 2).

#### R282 — 42.7k 0.1%, R

R282 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA6` ↔ `/driver/SA6` — series / termination resistor for U86 (pin 1 → 2).

#### R283 — 42.7k 0.1%, R

R283 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA6` ↔ `/driver/SB6` — series / termination resistor for U86 (pin 1 → 2).

#### R284 — 42.7k 0.1%, R

R284 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER6` ↔ `/driver/SB6` — series / termination resistor for U86 (pin 1 → 2).

#### R285 — 42.7k 0.1%, R

R285 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB6` ↔ `/driver/SB6` — series / termination resistor for U86 (pin 1 → 2).

#### R290 — 42.7k 0.1%, R

R290 — 42.7k 0.1%, R_0603_1608Metric — `/driver/DAC7` ↔ `/driver/SA7` — supply feed / filter for U10 (pin 1 → 2).

#### R291 — 42.7k 0.1%, R

R291 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA7` ↔ `/driver/SA7` — series / termination resistor for U87 (pin 1 → 2).

#### R292 — 42.7k 0.1%, R

R292 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVA7` ↔ `/driver/SA7` — series / termination resistor for U87 (pin 1 → 2).

#### R293 — 42.7k 0.1%, R

R293 — 42.7k 0.1%, R_0603_1608Metric — `/driver/LPA7` ↔ `/driver/SB7` — series / termination resistor for U87 (pin 1 → 2).

#### R294 — 42.7k 0.1%, R

R294 — 42.7k 0.1%, R_0603_1608Metric — `/driver/FILTER7` ↔ `/driver/SB7` — series / termination resistor for U87 (pin 1 → 2).

#### R295 — 42.7k 0.1%, R

R295 — 42.7k 0.1%, R_0603_1608Metric — `/driver/INVB7` ↔ `/driver/SB7` — series / termination resistor for U87 (pin 1 → 2).

#### R360 — 10k, R

R360 — 10k, R_0603_1608Metric — `/driver/SENSE_AC0` ↔ `/driver/FEEDBACK0` — series / termination resistor for U30 (pin 1 → 2).

#### R361 — 15k, R

R361 — 15k, R_0603_1608Metric — `/driver/ERR0` ↔ `/driver/BUF_IN0` — supply feed / filter for U30 (pin 1 → 2).

#### R362 — 10k, R

R362 — 10k, R_0603_1608Metric — `/driver/SENSE_AC1` ↔ `/driver/FEEDBACK1` — series / termination resistor for U31 (pin 1 → 2).

#### R363 — 15k, R

R363 — 15k, R_0603_1608Metric — `/driver/ERR1` ↔ `/driver/BUF_IN1` — supply feed / filter for U31 (pin 1 → 2).

#### R364 — 10k, R

R364 — 10k, R_0603_1608Metric — `/driver/SENSE_AC2` ↔ `/driver/FEEDBACK2` — series / termination resistor for U32 (pin 1 → 2).

#### R365 — 15k, R

R365 — 15k, R_0603_1608Metric — `/driver/ERR2` ↔ `/driver/BUF_IN2` — supply feed / filter for U32 (pin 1 → 2).

#### R366 — 10k, R

R366 — 10k, R_0603_1608Metric — `/driver/SENSE_AC3` ↔ `/driver/FEEDBACK3` — series / termination resistor for U33 (pin 1 → 2).

#### R367 — 15k, R

R367 — 15k, R_0603_1608Metric — `/driver/ERR3` ↔ `/driver/BUF_IN3` — supply feed / filter for U33 (pin 1 → 2).

#### R368 — 10k, R

R368 — 10k, R_0603_1608Metric — `/driver/SENSE_AC4` ↔ `/driver/FEEDBACK4` — series / termination resistor for U34 (pin 1 → 2).

#### R369 — 15k, R

R369 — 15k, R_0603_1608Metric — `/driver/ERR4` ↔ `/driver/BUF_IN4` — supply feed / filter for U34 (pin 1 → 2).

#### R370 — 10k, R

R370 — 10k, R_0603_1608Metric — `/driver/SENSE_AC5` ↔ `/driver/FEEDBACK5` — series / termination resistor for U35 (pin 1 → 2).

#### R371 — 15k, R

R371 — 15k, R_0603_1608Metric — `/driver/ERR5` ↔ `/driver/BUF_IN5` — supply feed / filter for U35 (pin 1 → 2).

#### R372 — 10k, R

R372 — 10k, R_0603_1608Metric — `/driver/SENSE_AC6` ↔ `/driver/FEEDBACK6` — series / termination resistor for U36 (pin 1 → 2).

#### R373 — 15k, R

R373 — 15k, R_0603_1608Metric — `/driver/ERR6` ↔ `/driver/BUF_IN6` — supply feed / filter for U36 (pin 1 → 2).

#### R374 — 10k, R

R374 — 10k, R_0603_1608Metric — `/driver/SENSE_AC7` ↔ `/driver/FEEDBACK7` — series / termination resistor for U37 (pin 1 → 2).

#### R375 — 15k, R

R375 — 15k, R_0603_1608Metric — `/driver/ERR7` ↔ `/driver/BUF_IN7` — supply feed / filter for U37 (pin 1 → 2).

#### R380 — 10k, R

R380 — 10k, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/BIAS_DIV` — pull-up resistor for U20 (pin 1 → 2).

#### R381 — 10k, R

R381 — 10k, R_0603_1608Metric — `/driver/BIAS_DIV` ↔ `GND` — pull-down resistor for U20 (pin 1 → 2).

#### R382 — 10k, R

R382 — 10k, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/VMID_7V5` — pull-up resistor for TP823 (pin 1 → 2).

#### R383 — 10k, R

R383 — 10k, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `GND` — pull-down resistor for TP823 (pin 1 → 2).

#### R400 — 10k 0.1%, R

R400 — 10k 0.1%, R_0603_1608Metric — `FG0_RETURN` ↔ `/driver/SENSE_P0` — series / termination resistor for U40 (pin 1 → 2).

#### R401 — 10k 0.1%, R

R401 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P0` ↔ `GND` — pull-down resistor for U40 (pin 1 → 2).

#### R402 — 10k 0.1%, R

R402 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N0` — series / termination resistor for U40 (pin 1 → 2).

#### R403 — 10k 0.1%, R

R403 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/SENSE_N0` — series / termination resistor for U40 (pin 1 → 2).

#### R410 — 10k 0.1%, R

R410 — 10k 0.1%, R_0603_1608Metric — `FG1_RETURN` ↔ `/driver/SENSE_P1` — series / termination resistor for U40 (pin 1 → 2).

#### R411 — 10k 0.1%, R

R411 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P1` ↔ `GND` — pull-down resistor for U40 (pin 1 → 2).

#### R412 — 10k 0.1%, R

R412 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N1` — series / termination resistor for U40 (pin 1 → 2).

#### R413 — 10k 0.1%, R

R413 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/SENSE_N1` — series / termination resistor for U40 (pin 1 → 2).

#### R420 — 10k 0.1%, R

R420 — 10k 0.1%, R_0603_1608Metric — `FG2_RETURN` ↔ `/driver/SENSE_P2` — series / termination resistor for U41 (pin 1 → 2).

#### R421 — 10k 0.1%, R

R421 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P2` ↔ `GND` — pull-down resistor for U41 (pin 1 → 2).

#### R422 — 10k 0.1%, R

R422 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N2` — series / termination resistor for U41 (pin 1 → 2).

#### R423 — 10k 0.1%, R

R423 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/SENSE_N2` — series / termination resistor for U41 (pin 1 → 2).

#### R430 — 10k 0.1%, R

R430 — 10k 0.1%, R_0603_1608Metric — `FG3_RETURN` ↔ `/driver/SENSE_P3` — series / termination resistor for U41 (pin 1 → 2).

#### R431 — 10k 0.1%, R

R431 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P3` ↔ `GND` — pull-down resistor for U41 (pin 1 → 2).

#### R432 — 10k 0.1%, R

R432 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N3` — series / termination resistor for U41 (pin 1 → 2).

#### R433 — 10k 0.1%, R

R433 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/SENSE_N3` — series / termination resistor for U41 (pin 1 → 2).

#### R440 — 10k 0.1%, R

R440 — 10k 0.1%, R_0603_1608Metric — `FG4_RETURN` ↔ `/driver/SENSE_P4` — series / termination resistor for U42 (pin 1 → 2).

#### R441 — 10k 0.1%, R

R441 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P4` ↔ `GND` — pull-down resistor for U42 (pin 1 → 2).

#### R442 — 10k 0.1%, R

R442 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N4` — series / termination resistor for U42 (pin 1 → 2).

#### R443 — 10k 0.1%, R

R443 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/SENSE_N4` — series / termination resistor for U42 (pin 1 → 2).

#### R450 — 10k 0.1%, R

R450 — 10k 0.1%, R_0603_1608Metric — `FG5_RETURN` ↔ `/driver/SENSE_P5` — series / termination resistor for U42 (pin 1 → 2).

#### R451 — 10k 0.1%, R

R451 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P5` ↔ `GND` — pull-down resistor for U42 (pin 1 → 2).

#### R452 — 10k 0.1%, R

R452 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N5` — series / termination resistor for U42 (pin 1 → 2).

#### R453 — 10k 0.1%, R

R453 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/SENSE_N5` — series / termination resistor for U42 (pin 1 → 2).

#### R460 — 10k 0.1%, R

R460 — 10k 0.1%, R_0603_1608Metric — `FG6_RETURN` ↔ `/driver/SENSE_P6` — series / termination resistor for U43 (pin 1 → 2).

#### R461 — 10k 0.1%, R

R461 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P6` ↔ `GND` — pull-down resistor for U43 (pin 1 → 2).

#### R462 — 10k 0.1%, R

R462 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N6` — series / termination resistor for U43 (pin 1 → 2).

#### R463 — 10k 0.1%, R

R463 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/SENSE_N6` — series / termination resistor for U43 (pin 1 → 2).

#### R470 — 10k 0.1%, R

R470 — 10k 0.1%, R_0603_1608Metric — `FG7_RETURN` ↔ `/driver/SENSE_P7` — series / termination resistor for U43 (pin 1 → 2).

#### R471 — 10k 0.1%, R

R471 — 10k 0.1%, R_0603_1608Metric — `/driver/SENSE_P7` ↔ `GND` — pull-down resistor for U43 (pin 1 → 2).

#### R472 — 10k 0.1%, R

R472 — 10k 0.1%, R_0603_1608Metric — `/driver/VMID_7V5` ↔ `/driver/SENSE_N7` — series / termination resistor for U43 (pin 1 → 2).

#### R473 — 10k 0.1%, R

R473 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/SENSE_N7` — series / termination resistor for U43 (pin 1 → 2).

#### R600 — 10.7k 1%, R

R600 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG0` — pull-up resistor for U20 (pin 1 → 2).

#### R601 — 10.7k 1%, R

R601 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG1` — pull-up resistor for U21 (pin 1 → 2).

#### R602 — 10.7k 1%, R

R602 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG2` — pull-up resistor for U22 (pin 1 → 2).

#### R603 — 10.7k 1%, R

R603 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG3` — pull-up resistor for U23 (pin 1 → 2).

#### R604 — 10.7k 1%, R

R604 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG4` — pull-up resistor for U24 (pin 1 → 2).

#### R605 — 10.7k 1%, R

R605 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG5` — pull-up resistor for U25 (pin 1 → 2).

#### R606 — 10.7k 1%, R

R606 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG6` — pull-up resistor for U26 (pin 1 → 2).

#### R607 — 10.7k 1%, R

R607 — 10.7k 1%, R_0603_1608Metric — `+15V_FUSED` ↔ `/driver/LIMIT_PROG7` — pull-up resistor for U27 (pin 1 → 2).

#### R620 — 10k, R

R620 — 10k, R_0603_1608Metric — `/driver/CMD_AC0` ↔ `/driver/CMD_BIASED0` — series / termination resistor for U30 (pin 1 → 2).

#### R621 — 1.40k, R

R621 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED0` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R622 — 10M, R

R622 — 10M, R_0603_1608Metric — `/driver/ERR0` ↔ `/driver/FEEDBACK0` — supply feed / filter for U30 (pin 1 → 2).

#### R623 — 330k, R

R623 — 330k, R_0603_1608Metric — `/driver/ERR0` ↔ `/driver/COMP0` — supply feed / filter for U30 (pin 1 → 2).

#### R630 — 10k, R

R630 — 10k, R_0603_1608Metric — `/driver/CMD_AC1` ↔ `/driver/CMD_BIASED1` — series / termination resistor for U31 (pin 1 → 2).

#### R631 — 1.40k, R

R631 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED1` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R632 — 10M, R

R632 — 10M, R_0603_1608Metric — `/driver/ERR1` ↔ `/driver/FEEDBACK1` — supply feed / filter for U31 (pin 1 → 2).

#### R633 — 330k, R

R633 — 330k, R_0603_1608Metric — `/driver/ERR1` ↔ `/driver/COMP1` — supply feed / filter for U31 (pin 1 → 2).

#### R640 — 10k, R

R640 — 10k, R_0603_1608Metric — `/driver/CMD_AC2` ↔ `/driver/CMD_BIASED2` — series / termination resistor for U32 (pin 1 → 2).

#### R641 — 1.40k, R

R641 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED2` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R642 — 10M, R

R642 — 10M, R_0603_1608Metric — `/driver/ERR2` ↔ `/driver/FEEDBACK2` — supply feed / filter for U32 (pin 1 → 2).

#### R643 — 330k, R

R643 — 330k, R_0603_1608Metric — `/driver/ERR2` ↔ `/driver/COMP2` — supply feed / filter for U32 (pin 1 → 2).

#### R650 — 10k, R

R650 — 10k, R_0603_1608Metric — `/driver/CMD_AC3` ↔ `/driver/CMD_BIASED3` — series / termination resistor for U33 (pin 1 → 2).

#### R651 — 1.40k, R

R651 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED3` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R652 — 10M, R

R652 — 10M, R_0603_1608Metric — `/driver/ERR3` ↔ `/driver/FEEDBACK3` — supply feed / filter for U33 (pin 1 → 2).

#### R653 — 330k, R

R653 — 330k, R_0603_1608Metric — `/driver/ERR3` ↔ `/driver/COMP3` — supply feed / filter for U33 (pin 1 → 2).

#### R660 — 10k, R

R660 — 10k, R_0603_1608Metric — `/driver/CMD_AC4` ↔ `/driver/CMD_BIASED4` — series / termination resistor for U34 (pin 1 → 2).

#### R661 — 1.40k, R

R661 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED4` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R662 — 10M, R

R662 — 10M, R_0603_1608Metric — `/driver/ERR4` ↔ `/driver/FEEDBACK4` — supply feed / filter for U34 (pin 1 → 2).

#### R663 — 330k, R

R663 — 330k, R_0603_1608Metric — `/driver/ERR4` ↔ `/driver/COMP4` — supply feed / filter for U34 (pin 1 → 2).

#### R670 — 10k, R

R670 — 10k, R_0603_1608Metric — `/driver/CMD_AC5` ↔ `/driver/CMD_BIASED5` — series / termination resistor for U35 (pin 1 → 2).

#### R671 — 1.40k, R

R671 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED5` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R672 — 10M, R

R672 — 10M, R_0603_1608Metric — `/driver/ERR5` ↔ `/driver/FEEDBACK5` — supply feed / filter for U35 (pin 1 → 2).

#### R673 — 330k, R

R673 — 330k, R_0603_1608Metric — `/driver/ERR5` ↔ `/driver/COMP5` — supply feed / filter for U35 (pin 1 → 2).

#### R680 — 10k, R

R680 — 10k, R_0603_1608Metric — `/driver/CMD_AC6` ↔ `/driver/CMD_BIASED6` — series / termination resistor for U36 (pin 1 → 2).

#### R681 — 1.40k, R

R681 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED6` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R682 — 10M, R

R682 — 10M, R_0603_1608Metric — `/driver/ERR6` ↔ `/driver/FEEDBACK6` — supply feed / filter for U36 (pin 1 → 2).

#### R683 — 330k, R

R683 — 330k, R_0603_1608Metric — `/driver/ERR6` ↔ `/driver/COMP6` — supply feed / filter for U36 (pin 1 → 2).

#### R690 — 10k, R

R690 — 10k, R_0603_1608Metric — `/driver/CMD_AC7` ↔ `/driver/CMD_BIASED7` — series / termination resistor for U37 (pin 1 → 2).

#### R691 — 1.40k, R

R691 — 1.40k, R_0603_1608Metric — `/driver/BUFFER_VMID` ↔ `/driver/CMD_BIASED7` — bias / reference network, supply feed / filter for U20, U21, U22, U23, U24, U25, U26, U27, U39 (pin 1 → 2).

#### R692 — 10M, R

R692 — 10M, R_0603_1608Metric — `/driver/ERR7` ↔ `/driver/FEEDBACK7` — supply feed / filter for U37 (pin 1 → 2).

#### R693 — 330k, R

R693 — 330k, R_0603_1608Metric — `/driver/ERR7` ↔ `/driver/COMP7` — supply feed / filter for U37 (pin 1 → 2).

#### R710 — 52.3k 0.1%, R

R710 — 52.3k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_REF` — pull-up resistor for U62 (pin 1 → 2).

#### R711 — 10k 0.1%, R

R711 — 10k 0.1%, R_0603_1608Metric — `/driver/TRIP_REF` ↔ `GND` — pull-down resistor for U62 (pin 1 → 2).

#### R712 — 4.7k, R

R712 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/DRIVER_FAULT_N` — pull-up resistor for U601 (pin 1 → 2).

#### R720 — 10k 0.1%, R

R720 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE0` ↔ `/driver/TRIP_SENSE0` — series / termination resistor for U60 (pin 1 → 2).

#### R721 — 100k 0.1%, R

R721 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE0` — pull-up resistor for U60 (pin 1 → 2).

#### R722 — 10k 0.1%, R

R722 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE1` ↔ `/driver/TRIP_SENSE1` — series / termination resistor for U61 (pin 1 → 2).

#### R723 — 100k 0.1%, R

R723 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE1` — pull-up resistor for U62 (pin 1 → 2).

#### R724 — 10k 0.1%, R

R724 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE2` ↔ `/driver/TRIP_SENSE2` — series / termination resistor for U62 (pin 1 → 2).

#### R725 — 100k 0.1%, R

R725 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE2` — pull-up resistor for U64 (pin 1 → 2).

#### R726 — 10k 0.1%, R

R726 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE3` ↔ `/driver/TRIP_SENSE3` — series / termination resistor for U63 (pin 1 → 2).

#### R727 — 100k 0.1%, R

R727 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE3` — pull-up resistor for U66 (pin 1 → 2).

#### R728 — 10k 0.1%, R

R728 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE4` ↔ `/driver/TRIP_SENSE4` — series / termination resistor for U64 (pin 1 → 2).

#### R729 — 100k 0.1%, R

R729 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE4` — pull-up resistor for U60 (pin 1 → 2).

#### R730 — 10k 0.1%, R

R730 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE5` ↔ `/driver/TRIP_SENSE5` — series / termination resistor for U65 (pin 1 → 2).

#### R731 — 100k 0.1%, R

R731 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE5` — pull-up resistor for U62 (pin 1 → 2).

#### R732 — 10k 0.1%, R

R732 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE6` ↔ `/driver/TRIP_SENSE6` — series / termination resistor for U66 (pin 1 → 2).

#### R733 — 100k 0.1%, R

R733 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE6` — pull-up resistor for U64 (pin 1 → 2).

#### R734 — 10k 0.1%, R

R734 — 10k 0.1%, R_0603_1608Metric — `/driver/I_SENSE7` ↔ `/driver/TRIP_SENSE7` — series / termination resistor for U67 (pin 1 → 2).

#### R735 — 100k 0.1%, R

R735 — 100k 0.1%, R_0603_1608Metric — `+3.3V` ↔ `/driver/TRIP_SENSE7` — pull-up resistor for U66 (pin 1 → 2).

### 4.4 Page 4 — receiver

Net-centric counterpart: `brd01_wiring_manifest.md` §3.4. 107 components on this sheet.

#### Components

#### U101 — AD7768-4BSTZ-RL7, AD7768-4BSTZ

Sheet: receiver (4) · Footprint: Package_QFP:LQFP-64_10x10mm_P0.5mm · 64 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | AIN1-_1 | input | `/receiver/AIN1-` | R125.2, C127.2, C126.1 |
| 2 | AIN1+_2 | input | `/receiver/AIN1+` | R124.2, C127.1, C125.1 |
| 3 | AVSS1A_3 | power_in | `GND` | U101.55, U101.46, U101.33, U101.62, U101.51, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 4 | AVDD1A_4 | power_in | `+5VA` | U101.45, U101.60, U101.53, C107.1, C108.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | REF1-_5 | input | `GND` | U101.44, U101.31, U101.58, U101.56, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 6 | REF1+_6 | input | `/receiver/ADC_REF` | U101.43, C102.1, R184.2, C101.1, D534.2 |
| 7 | AVSS_7 | power_in | `GND` | U101.8, U101.51, U101.62, U101.9, U101.10, U101.46 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 8 | AVSS_8 | power_in | `GND` | U101.7, U101.9, U101.51, U101.10, U101.62, U101.39 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 9 | AVSS_9 | power_in | `GND` | U101.10, U101.8, U101.39, U101.7, U101.40, U101.51 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 10 | AVSS_10 | power_in | `GND` | U101.39, U101.9, U101.40, U101.8, U101.41, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | FILTER/GPIO4_11 | bidirectional | `/receiver/ADC_SPI_STRAP` | R180.2 |
| 12 | MODE0/GPIO0_12 | bidirectional+no_connect | `unconnected-(U101-MODE0/GPIO0-Pad12)` | — (no other pins on this net) |
| 13 | MODE1/GPIO1_13 | bidirectional+no_connect | `unconnected-(U101-MODE1/GPIO1-Pad13)` | — (no other pins on this net) |
| 14 | MODE2/GPIO2_14 | bidirectional+no_connect | `unconnected-(U101-MODE2/GPIO2-Pad14)` | — (no other pins on this net) |
| 15 | MODE3/GPIO3_15 | bidirectional+no_connect | `unconnected-(U101-MODE3/GPIO3-Pad15)` | — (no other pins on this net) |
| 16 | ST0/~{CS}_16 | input | `ADC_CS` | R164.2, U4.B12 |
| 17 | SCLK_17 | input | `ADC_SCLK` | U4.A13 |
| 18 | DEC1/SDI_18 | input | `ADC_SDI` | U4.A12 |
| 19 | DEC0/SDO_19 | bidirectional | `ADC_SDO` | U4.B11 |
| 20 | DNC/DGND_20 | passive+no_connect | `unconnected-(U101-DNC/DGND-Pad20)` | — (no other pins on this net) |
| 21 | DIN_21 | input | `/receiver/ADC_DAISY_IN` | R181.1 |
| 22 | DNC_22 | no_connect | `unconnected-(U101-DNC-Pad22)` | — (no other pins on this net) |
| 23 | DNC_23 | no_connect | `unconnected-(U101-DNC-Pad23)` | — (no other pins on this net) |
| 24 | DOUT3_24 | output | `ADC_DOUT3` | U4.A10 |
| 25 | DOUT2_25 | output | `ADC_DOUT2` | U4.B9 |
| 26 | DOUT1_26 | output | `ADC_DOUT1` | U4.A9 |
| 27 | DOUT0_27 | output | `ADC_DOUT0` | U4.A8 |
| 28 | DCLK_28 | output | `ADC_DCLK` | U4.C11 |
| 29 | ~{DRDY}_29 | output | `ADC_DRDY_N` | U4.B10 |
| 30 | ~{RESET}_30 | input | `ADC_RESET_N` | R163.2, U4.A14 |
| 31 | XTAL1_31 | input | `GND` | U101.44, U101.58, U101.5, U101.56, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 32 | XTAL2/MCLK_32 | input | `/receiver/MCLK` | R100.2 |
| 33 | DGND_33 | power_in | `GND` | U101.55, U101.3, U101.46, U101.62, U101.51, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 34 | DREGCAP_34 | power_out | `/receiver/DREGCAP` | C103.1 |
| 35 | IOVDD_35 | power_in | `+3.3V` | C111.1, U101.57, R180.1, C140.1, C141.1, C142.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 36 | SYNC_IN_36 | input | `ADC_SYNC_IN` | R166.2, U4.C14 |
| 37 | ~{START}_37 | input | `ADC_START_N` | R165.2, U4.B14 |
| 38 | SYNC_OUT_38 | output | `ADC_SYNC_OUT` | U4.A15 |
| 39 | AVSS_39 | power_in | `GND` | U101.10, U101.40, U101.9, U101.41, U101.42, U101.8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 40 | AVSS_40 | power_in | `GND` | U101.39, U101.41, U101.10, U101.42, U101.54, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 41 | AVSS_41 | power_in | `GND` | U101.42, U101.40, U101.54, U101.39, U101.10, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 42 | AVSS_42 | power_in | `GND` | U101.41, U101.54, U101.40, U101.39, U101.10, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 43 | REF2+_43 | input | `/receiver/ADC_REF` | U101.6, C102.1, R184.2, C101.1, D534.2 |
| 44 | REF2-_44 | input | `GND` | U101.31, U101.5, U101.58, U101.56, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 45 | AVDD1B_45 | power_in | `+5VA` | U101.4, U101.60, U101.53, C108.1, C107.1, C109.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 46 | AVSS1B_46 | power_in | `GND` | U101.3, U101.62, U101.51, U101.55, U101.33, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 47 | AIN3+_47 | input | `/receiver/AIN3+` | C564.1, C566.1, R572.2 |
| 48 | AIN3-_48 | input | `/receiver/AIN3-` | C566.2, C565.1, R573.2 |
| 49 | AIN2+_49 | input | `/receiver/AIN2+` | C544.1, C546.1, R552.2 |
| 50 | AIN2-_50 | input | `/receiver/AIN2-` | C546.2, C545.1, R553.2 |
| 51 | AVSS2B_51 | power_in | `GND` | U101.62, U101.7, U101.46, U101.8, U101.3, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 52 | REGCAPB_52 | power_out | `/receiver/REGCAPB` | C105.1 |
| 53 | AVDD2B_53 | power_in | `+5VA` | U101.60, U101.45, U101.4, C110.1, C109.1, C108.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 54 | AVSS_54 | power_in | `GND` | U101.42, U101.41, U101.40, U101.39, U101.10, U101.9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 55 | DGND_55 | power_in | `GND` | U101.3, U101.33, U101.46, U101.62, U101.51, U101.7 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 56 | FORMAT0_56 | input | `GND` | U101.58, U101.31, U101.44, U101.5, U101.3, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 57 | PIN/SPI_57 | input | `+3.3V` | U101.35, C111.1, R180.1, C140.1, C141.1, C142.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 58 | CLK_SEL_58 | input | `GND` | U101.31, U101.44, U101.56, U101.5, U101.33, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 59 | VCM_59 | output | `/receiver/ADC_VCM` | C106.1, U108.17, U105.11, U105.17, U108.11 |
| 60 | AVDD2A_60 | power_in | `+5VA` | U101.45, U101.53, U101.4, C109.1, C108.1, C110.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 61 | REGCAPA_61 | power_out | `/receiver/REGCAPA` | C104.1 |
| 62 | AVSS2A_62 | power_in | `GND` | U101.51, U101.46, U101.7, U101.3, U101.8, U101.55 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 63 | AIN0-_63 | input | `/receiver/AIN0-` | C121.1, R115.2, C122.2 |
| 64 | AIN0+_64 | input | `/receiver/AIN0+` | C120.1, R114.2, C122.1 |

Supporting passives:

- enable pull-up: R163 (10k) on `ADC_RESET_N`
- enable pull-up: R165 (10k) on `ADC_START_N`
- filter capacitor to ground: C544 (470p), C545 (470p), C564 (470p), C565 (470p) on `GND`
- input / output filter capacitor: C122 (100p) on `/receiver/AIN0-`
- input / output filter capacitor: C127 (100p) on `/receiver/AIN1-`
- input / output filter capacitor: C546 (100p) on `/receiver/AIN2-`
- input / output filter capacitor: C566 (100p) on `/receiver/AIN3-`
- pull-down resistor: R181 (10k) on `/receiver/ADC_DAISY_IN`
- pull-up resistor: R180 (10k) on `/receiver/ADC_SPI_STRAP`
- soft-start / bias capacitor: C106 (100n) on `/receiver/ADC_VCM`
- soft-start / bias capacitor: C103 (10u) on `/receiver/DREGCAP`
- soft-start / bias capacitor: C104 (1u) on `/receiver/REGCAPA`
- soft-start / bias capacitor: C105 (1u) on `/receiver/REGCAPB`
- supply decoupling: C111 (100n) on `+3.3V`
- supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on `+5VA`

#### U102 — ADR434BRZ

Sheet: receiver (4) · Footprint: Package_SO:SOIC-8_3.9x4.9mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | DNC_1 | no_connect | `unconnected-(U102-DNC-Pad1)` | — (no other pins on this net) |
| 2 | VIN_2 | power_in | `+12VA` | C130.1, U103.5, C100.1, U104.11, U106.11, C115.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 3 | NIC_3 | no_connect | `unconnected-(U102-NIC-Pad3)` | — (no other pins on this net) |
| 4 | GND_4 | power_in | `GND` | C130.2, C131.2, C120.2, C101.2, C102.2, C121.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | TRIM_5 | passive+no_connect | `unconnected-(U102-TRIM-Pad5)` | — (no other pins on this net) |
| 6 | VOUT_6 | power_out | `/receiver/REF_RAW` | C131.1, U103.3 |
| 7 | COMP_7 | passive+no_connect | `unconnected-(U102-COMP-Pad7)` | — (no other pins on this net) |
| 8 | DNC_8 | no_connect | `unconnected-(U102-DNC-Pad8)` | — (no other pins on this net) |

Supporting passives:

- filter capacitor to ground: C101 (10u), C102 (100n), C120 (470p), C121 (470p) on `GND`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C131 (100n) on `/receiver/REF_RAW`

#### U103 — OPA192IDBVR

Sheet: receiver (4) · Footprint: Package_TO_SOT_SMD:SOT-23-5 · 5 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OUT_1 | output | `/receiver/REF_BUF_OUT` | U103.4, R184.1 |
| 2 | V-_2 | power_in | `GND` | C106.2, C103.2, C104.2, C105.2, C131.2, C107.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 3 | IN+_3 | input | `/receiver/REF_RAW` | U102.6, C131.1 |
| 4 | IN-_4 | input | `/receiver/REF_BUF_OUT` | U103.1, R184.1 |
| 5 | V+_5 | power_in | `+12VA` | U102.2, C130.1, C100.1, U104.11, U106.11, C115.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply feed / filter: R184 (10) on `/receiver/REF_BUF_OUT`

#### U104 — INA163UA

Sheet: receiver (4) · Footprint: Package_SO:SOIC-14_3.9x8.7mm_P1.27mm · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VO1_1 | output+no_connect | `unconnected-(U104-VO1-Pad1)` | — (no other pins on this net) |
| 2 | NC_2 | no_connect | `unconnected-(U104-NC-Pad2)` | — (no other pins on this net) |
| 3 | GS1_3 | passive | `/receiver/GAIN1` | R105.1 |
| 4 | IN-_4 | input | `/receiver/INA_IN_N` | R104.1, C114.2 |
| 5 | IN+_5 | input | `/receiver/INA_IN_P` | R103.1, C113.2 |
| 6 | V-_6 | power_in | `-12VA` | C116.1, D104.2, D102.2, D523.2, U106.6, C543.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 7 | NC_7 | no_connect | `unconnected-(U104-NC-Pad7)` | — (no other pins on this net) |
| 8 | SENSE_8 | input | `Net-(U104-SENSE)` | U104.9, R120.1 |
| 9 | VO_9 | output | `Net-(U104-SENSE)` | U104.8, R120.1 |
| 10 | REF_10 | input | `GND` | C116.2, C115.2, R121.1, R111.1, R104.2, R103.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | V+_11 | power_in | `+12VA` | C115.1, D103.1, D101.1, U106.11, D522.1, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 12 | GS2_12 | passive | `/receiver/GAIN2` | R105.2 |
| 13 | NC_13 | no_connect | `unconnected-(U104-NC-Pad13)` | — (no other pins on this net) |
| 14 | VO2_14 | output+no_connect | `unconnected-(U104-VO2-Pad14)` | — (no other pins on this net) |

Supporting passives:

- pull-down resistor: R103 (10k 0.1%) on `/receiver/INA_IN_P`
- pull-down resistor: R104 (10k 0.1%), R111 (1k), R121 (499) on `GND`
- series / termination resistor: R105 (176) on `/receiver/GAIN2`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C116 (100n), C543 (100n), C563 (100n) on `-12VA`

#### U105 — ADA4940-2ACPZ

Sheet: receiver (4) · Footprint: Package_CSP:LFCSP-24-1EP_4x4mm_P0.5mm_EP2.5x2.5mm · 25 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | -IN1_1 | input | `/receiver/FDA0_N` | R113.2, R111.2 |
| 2 | +FB1_2 | passive | `/receiver/FDA0_OUT_P` | U105.18, R113.1, R114.1 |
| 3 | +VS1_3 | power_in | `+5VA` | U105.20, U105.4, U105.14, U105.9, U105.10, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 4 | +VS1_4 | power_in | `+5VA` | U105.3, U105.20, U105.14, U105.9, U105.10, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | -FB2_5 | passive | `/receiver/FDA1_OUT_N` | U105.13, R122.1, R125.1 |
| 6 | +IN2_6 | input | `Net-(U105B-+IN2)` | R122.2, R120.2 |
| 7 | -IN2_7 | input | `/receiver/FDA1_N` | R123.2, R121.2 |
| 8 | +FB2_8 | passive | `/receiver/FDA1_OUT_P` | U105.12, R123.1, R124.1 |
| 9 | +VS2_9 | power_in | `+5VA` | U105.14, U105.10, U105.4, U105.3, U105.20, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 10 | +VS2_10 | power_in | `+5VA` | U105.9, U105.14, U105.4, U105.3, U105.20, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | VOCM2_11 | input | `/receiver/ADC_VCM` | U105.17, U108.17, U101.59, C106.1, U108.11 |
| 12 | +OUT2_12 | output | `/receiver/FDA1_OUT_P` | U105.8, R123.1, R124.1 |
| 13 | -OUT2_13 | output | `/receiver/FDA1_OUT_N` | U105.5, R122.1, R125.1 |
| 14 | ~{DISABLE2}_14 | input | `+5VA` | U105.9, U105.10, U105.4, U105.3, U105.20, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 15 | -VS2_15 | power_in | `GND` | U105.16, U105.22, U105.21, R121.1, R111.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 16 | -VS2_16 | power_in | `GND` | U105.15, U105.22, U105.21, R121.1, R111.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 17 | VOCM1_17 | input | `/receiver/ADC_VCM` | U105.11, U108.17, U101.59, C106.1, U108.11 |
| 18 | +OUT1_18 | output | `/receiver/FDA0_OUT_P` | U105.2, R113.1, R114.1 |
| 19 | -OUT1_19 | output | `/receiver/FDA0_OUT_N` | U105.23, R112.1, R115.1 |
| 20 | ~{DISABLE1}_20 | input | `+5VA` | U105.3, U105.4, U105.14, U105.9, U105.10, U108.20 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 21 | -VS1_21 | power_in | `GND` | U105.22, U105.15, U105.16, R111.1, R121.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 22 | -VS1_22 | power_in | `GND` | U105.21, U105.15, U105.16, R111.1, R121.1, U104.10 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 23 | -FB1_23 | passive | `/receiver/FDA0_OUT_N` | U105.19, R112.1, R115.1 |
| 24 | +IN1_24 | input | `Net-(U105A-+IN1)` | R112.2, R110.2 |
| 25 | EP_25 | passive | `GND` | U108.25, C130.2, C120.2, C101.2, U102.4, C121.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- enable / sequencing network: C190 (47u / 16V X7R) on `+5VA`
- feedback divider: R115 (20) on `/receiver/FDA0_OUT_N`
- feedback divider: R113 (1k), R114 (20) on `/receiver/FDA0_OUT_P`
- feedback divider: R125 (20) on `/receiver/FDA1_OUT_N`
- feedback divider: R123 (1k), R124 (20) on `/receiver/FDA1_OUT_P`
- soft-start / bias capacitor: C106 (100n) on `/receiver/ADC_VCM`
- supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on `+5VA`
- supply feed / filter: R110 (1k), R112 (1k) on `Net-(U105A-+IN1)`
- supply feed / filter: R120 (499), R122 (1k) on `Net-(U105B-+IN2)`

#### U106 — INA163UA

Sheet: receiver (4) · Footprint: Package_SO:SOIC-14_3.9x8.7mm_P1.27mm · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VO1_1 | output+no_connect | `unconnected-(U106-VO1-Pad1)` | — (no other pins on this net) |
| 2 | NC_2 | no_connect | `unconnected-(U106-NC-Pad2)` | — (no other pins on this net) |
| 3 | GS1_3 | passive | `/receiver/PEN2_RG1` | R544.1 |
| 4 | IN-_4 | input | `/receiver/PEN2_IN_N` | C541.2, R543.1 |
| 5 | IN+_5 | input | `/receiver/PEN2_IN_P` | R542.1, C540.2 |
| 6 | V-_6 | power_in | `-12VA` | D523.2, C543.1, D521.2, D533.2, U107.6, U104.6 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 7 | NC_7 | no_connect | `unconnected-(U106-NC-Pad7)` | — (no other pins on this net) |
| 8 | SENSE_8 | input | `Net-(U106-SENSE)` | U106.9, R548.1 |
| 9 | VO_9 | output | `Net-(U106-SENSE)` | U106.8, R548.1 |
| 10 | REF_10 | input | `GND` | R549.1, U108.21, U108.22, C543.2, C542.2, R542.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | V+_11 | power_in | `+12VA` | D522.1, C542.1, U107.11, U104.11, D532.1, C115.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 12 | GS2_12 | passive | `/receiver/PEN2_RG2` | R544.2 |
| 13 | NC_13 | no_connect | `unconnected-(U106-NC-Pad13)` | — (no other pins on this net) |
| 14 | VO2_14 | output+no_connect | `unconnected-(U106-VO2-Pad14)` | — (no other pins on this net) |

Supporting passives:

- pull-down resistor: R543 (10k 0.1%) on `/receiver/PEN2_IN_N`
- pull-down resistor: R542 (10k 0.1%) on `/receiver/PEN2_IN_P`
- pull-down resistor: R549 (499) on `GND`
- series / termination resistor: R544 (176) on `/receiver/PEN2_RG2`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C116 (100n), C543 (100n), C563 (100n) on `-12VA`

#### U107 — INA163UA

Sheet: receiver (4) · Footprint: Package_SO:SOIC-14_3.9x8.7mm_P1.27mm · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | VO1_1 | output+no_connect | `unconnected-(U107-VO1-Pad1)` | — (no other pins on this net) |
| 2 | NC_2 | no_connect | `unconnected-(U107-NC-Pad2)` | — (no other pins on this net) |
| 3 | GS1_3 | passive | `/receiver/REF_COIL_RG1` | R564.1 |
| 4 | IN-_4 | input | `/receiver/REF_COIL_IN_N` | C561.2, R563.1 |
| 5 | IN+_5 | input | `/receiver/REF_COIL_IN_P` | R562.1, C560.2 |
| 6 | V-_6 | power_in | `-12VA` | D533.2, C563.1, D531.2, U106.6, C543.1, D523.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 7 | NC_7 | no_connect | `unconnected-(U107-NC-Pad7)` | — (no other pins on this net) |
| 8 | SENSE_8 | input | `Net-(U107-SENSE)` | U107.9, R568.1 |
| 9 | VO_9 | output | `Net-(U107-SENSE)` | U107.8, R568.1 |
| 10 | REF_10 | input | `GND` | R569.1, U108.15, U108.16, C563.2, C562.2, R562.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | V+_11 | power_in | `+12VA` | D532.1, C562.1, U106.11, D530.1, D522.1, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 12 | GS2_12 | passive | `/receiver/REF_COIL_RG2` | R564.2 |
| 13 | NC_13 | no_connect | `unconnected-(U107-NC-Pad13)` | — (no other pins on this net) |
| 14 | VO2_14 | output+no_connect | `unconnected-(U107-VO2-Pad14)` | — (no other pins on this net) |

Supporting passives:

- pull-down resistor: R563 (10k 0.1%) on `/receiver/REF_COIL_IN_N`
- pull-down resistor: R562 (10k 0.1%) on `/receiver/REF_COIL_IN_P`
- pull-down resistor: R569 (499) on `GND`
- series / termination resistor: R564 (176) on `/receiver/REF_COIL_RG2`
- supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on `+12VA`
- supply decoupling: C116 (100n), C543 (100n), C563 (100n) on `-12VA`

#### U108 — ADA4940-2ACPZ

Sheet: receiver (4) · Footprint: Package_CSP:LFCSP-24-1EP_4x4mm_P0.5mm_EP2.5x2.5mm · 25 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | -IN1_1 | input | `/receiver/FDA2_N` | R551.2, R549.2 |
| 2 | +FB1_2 | passive | `/receiver/FDA2_OUT_P` | U108.18, R551.1, R552.1 |
| 3 | +VS1_3 | power_in | `+5VA` | U108.4, U108.20, U105.10, U108.14, U108.9, U105.9 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 4 | +VS1_4 | power_in | `+5VA` | U108.3, U108.20, U108.14, U108.9, U105.10, U108.10 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 5 | -FB2_5 | passive | `/receiver/FDA3_OUT_N` | U108.13, R570.1, R573.1 |
| 6 | +IN2_6 | input | `Net-(U108B-+IN2)` | R570.2, R568.2 |
| 7 | -IN2_7 | input | `/receiver/FDA3_N` | R571.2, R569.2 |
| 8 | +FB2_8 | passive | `/receiver/FDA3_OUT_P` | U108.12, R571.1, R572.1 |
| 9 | +VS2_9 | power_in | `+5VA` | U108.14, U108.10, U108.4, U108.3, U108.20, C123.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 10 | +VS2_10 | power_in | `+5VA` | U108.9, U108.14, U108.4, U108.3, U108.20, C123.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 11 | VOCM2_11 | input | `/receiver/ADC_VCM` | U108.17, U105.11, U101.59, C106.1, U105.17 |
| 12 | +OUT2_12 | output | `/receiver/FDA3_OUT_P` | U108.8, R571.1, R572.1 |
| 13 | -OUT2_13 | output | `/receiver/FDA3_OUT_N` | U108.5, R570.1, R573.1 |
| 14 | ~{DISABLE2}_14 | input | `+5VA` | U108.9, U108.10, U108.4, U108.3, U108.20, C123.1 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 15 | -VS2_15 | power_in | `GND` | U108.16, R569.1, U107.10, C563.2, U108.22, U108.21 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 16 | -VS2_16 | power_in | `GND` | U108.15, R569.1, U107.10, C563.2, U108.22, U108.21 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 17 | VOCM1_17 | input | `/receiver/ADC_VCM` | U105.11, U108.11, U105.17, U101.59, C106.1 |
| 18 | +OUT1_18 | output | `/receiver/FDA2_OUT_P` | U108.2, R551.1, R552.1 |
| 19 | -OUT1_19 | output | `/receiver/FDA2_OUT_N` | U108.23, R550.1, R553.1 |
| 20 | ~{DISABLE1}_20 | input | `+5VA` | U108.3, U108.4, U105.10, U105.9, U105.14, U108.14 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 21 | -VS1_21 | power_in | `GND` | U108.22, R549.1, U106.10, C543.2, C125.2, U105.16 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 22 | -VS1_22 | power_in | `GND` | U108.21, R549.1, U106.10, C543.2, C125.2, R569.1 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 23 | -FB1_23 | passive | `/receiver/FDA2_OUT_N` | U108.19, R550.1, R553.1 |
| 24 | +IN1_24 | input | `Net-(U108A-+IN1)` | R550.2, R548.2 |
| 25 | EP_25 | passive | `GND` | U105.25, C130.2, C101.2, C120.2, U102.4, C121.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- enable / sequencing network: C190 (47u / 16V X7R) on `+5VA`
- feedback divider: R553 (20) on `/receiver/FDA2_OUT_N`
- feedback divider: R551 (1k), R552 (20) on `/receiver/FDA2_OUT_P`
- feedback divider: R573 (20) on `/receiver/FDA3_OUT_N`
- feedback divider: R571 (1k), R572 (20) on `/receiver/FDA3_OUT_P`
- filter capacitor to ground: C125 (470p), C126 (470p) on `GND`
- soft-start / bias capacitor: C106 (100n) on `/receiver/ADC_VCM`
- supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on `+5VA`
- supply feed / filter: R548 (499), R550 (1k) on `Net-(U108A-+IN1)`
- supply feed / filter: R568 (499), R570 (1k) on `Net-(U108B-+IN2)`

#### D101 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | D103.1, C115.1, U104.11, D520.1, D522.1, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN1_PROT_P` | D102.1, R101.2, C113.1 |

Supporting passives:

- series / termination resistor: R101 (100) on `/receiver/PEN1_PROT_P`

#### D102 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN1_PROT_P` | D101.2, C113.1, R101.2 |
| 2 | A_2 | passive | `-12VA` | D104.2, C116.1, U104.6, D521.2, D523.2, C543.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- input / output filter capacitor: C113 (10u) on `/receiver/PEN1_PROT_P`

#### D103 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | D101.1, C115.1, D520.1, D522.1, U104.11, C542.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN1_PROT_N` | D104.1, R102.2, C114.1 |

Supporting passives:

- series / termination resistor: R102 (100) on `/receiver/PEN1_PROT_N`

#### D104 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN1_PROT_N` | D103.2, C114.1, R102.2 |
| 2 | A_2 | passive | `-12VA` | D102.2, C116.1, U104.6, D521.2, D523.2, C543.1 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

Supporting passives:

- input / output filter capacitor: C114 (10u) on `/receiver/PEN1_PROT_N`

#### D520 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C542.1, D522.1, D103.1, D530.1, D101.1, D532.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN2_PROT_P` | C540.1, R540.2, D521.1 |

Supporting passives:

- input / output filter capacitor: C540 (10u) on `/receiver/PEN2_PROT_P`
- series / termination resistor: R540 (100) on `/receiver/PEN2_PROT_P`

#### D521 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN2_PROT_P` | D520.2, R540.2, C540.1 |
| 2 | A_2 | passive | `-12VA` | C543.1, D523.2, U106.6, D104.2, D531.2, D102.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D522 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C542.1, D520.1, U106.11, D532.1, D103.1, C562.1 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/PEN2_PROT_N` | D523.1, R541.2, C541.1 |

Supporting passives:

- input / output filter capacitor: C541 (10u) on `/receiver/PEN2_PROT_N`
- series / termination resistor: R541 (100) on `/receiver/PEN2_PROT_N`

#### D523 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/PEN2_PROT_N` | D522.2, R541.2, C541.1 |
| 2 | A_2 | passive | `-12VA` | C543.1, U106.6, D521.2, C116.1, U104.6, D533.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D530 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C562.1, D532.1, C542.1, D520.1, D522.1, U107.11 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/REF_COIL_PROT_P` | C560.1, R560.2, D531.1 |

Supporting passives:

- input / output filter capacitor: C560 (10u) on `/receiver/REF_COIL_PROT_P`
- series / termination resistor: R560 (100) on `/receiver/REF_COIL_PROT_P`

#### D531 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/REF_COIL_PROT_P` | D530.2, R560.2, C560.1 |
| 2 | A_2 | passive | `-12VA` | C563.1, D533.2, U107.6, C543.1, D521.2, D523.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D532 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+12VA` | C562.1, D530.1, U107.11, C542.1, D522.1, U106.11 — 47 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/REF_COIL_PROT_N` | D533.1, R561.2, C561.1 |

Supporting passives:

- input / output filter capacitor: C561 (10u) on `/receiver/REF_COIL_PROT_N`
- series / termination resistor: R561 (100) on `/receiver/REF_COIL_PROT_N`

#### D533 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `/receiver/REF_COIL_PROT_N` | D532.2, R561.2, C561.1 |
| 2 | A_2 | passive | `-12VA` | C563.1, U107.6, D531.2, U106.6, C543.1, D523.2 — 43 ends total; full list in `brd01_wiring_manifest.md` §3.4 |

#### D534 — BAS70H,115, D_Schottky

Sheet: receiver (4) · Footprint: Diode_SMD:D_SOD-123F · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | K_1 | passive | `+5VA` | C128.1, U101.4, C112.1, U101.45, C107.1, U101.60 — 29 ends total; full list in `brd01_wiring_manifest.md` §3.4 |
| 2 | A_2 | passive | `/receiver/ADC_REF` | C102.1, C101.1, R184.2, U101.6, U101.43 |

#### C100 — 100n, C

C100 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C101 — 10u, C

C101 — 10u, C_1206_3216Metric — `/receiver/ADC_REF` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C102 — 100n, C

C102 — 100n, C_0603_1608Metric — `/receiver/ADC_REF` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C103 — 10u, C

C103 — 10u, C_1206_3216Metric — `/receiver/DREGCAP` ↔ `GND` — soft-start / bias capacitor for U101 (pin 1 → 2).

#### C104 — 1u, C

C104 — 1u, C_0805_2012Metric — `/receiver/REGCAPA` ↔ `GND` — soft-start / bias capacitor for U101 (pin 1 → 2).

#### C105 — 1u, C

C105 — 1u, C_0805_2012Metric — `/receiver/REGCAPB` ↔ `GND` — soft-start / bias capacitor for U101 (pin 1 → 2).

#### C106 — 100n, C

C106 — 100n, C_0603_1608Metric — `/receiver/ADC_VCM` ↔ `GND` — soft-start / bias capacitor for U101, U105, U108 (pin 1 → 2).

#### C107 — 100n, C

C107 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C108 — 100n, C

C108 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C109 — 100n, C

C109 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C110 — 100n, C

C110 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C111 — 100n, C

C111 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U7, U101, U142, U751, U753, Y1 (pin 1 → 2).

#### C112 — 10u, C

C112 — 10u, C_1206_3216Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C113 — 10u, C

C113 — 10u, C_1206_3216Metric — `/receiver/PEN1_PROT_P` ↔ `/receiver/INA_IN_P` — input / output filter capacitor for D102 (pin 1 → 2).

#### C114 — 10u, C

C114 — 10u, C_1206_3216Metric — `/receiver/PEN1_PROT_N` ↔ `/receiver/INA_IN_N` — input / output filter capacitor for D104 (pin 1 → 2).

#### C115 — 100n, C

C115 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C116 — 100n, C

C116 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U104, U106, U107 (pin 1 → 2).

#### C120 — 470p, C

C120 — 470p, C_0603_1608Metric — `/receiver/AIN0+` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C121 — 470p, C

C121 — 470p, C_0603_1608Metric — `/receiver/AIN0-` ↔ `GND` — filter capacitor to ground for U102 (pin 1 → 2).

#### C122 — 100p, C

C122 — 100p, C_0603_1608Metric — `/receiver/AIN0+` ↔ `/receiver/AIN0-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C123 — 100n, C

C123 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C125 — 470p, C

C125 — 470p, C_0603_1608Metric — `/receiver/AIN1+` ↔ `GND` — filter capacitor to ground for U108 (pin 1 → 2).

#### C126 — 470p, C

C126 — 470p, C_0603_1608Metric — `/receiver/AIN1-` ↔ `GND` — filter capacitor to ground for U108 (pin 1 → 2).

#### C127 — 100p, C

C127 — 100p, C_0603_1608Metric — `/receiver/AIN1+` ↔ `/receiver/AIN1-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C128 — 100n, C

C128 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C130 — 100n, C

C130 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C131 — 100n, C

C131 — 100n, C_0603_1608Metric — `/receiver/REF_RAW` ↔ `GND` — supply decoupling for U102 (pin 1 → 2).

#### C540 — 10u, C

C540 — 10u, C_1206_3216Metric — `/receiver/PEN2_PROT_P` ↔ `/receiver/PEN2_IN_P` — input / output filter capacitor for D520 (pin 1 → 2).

#### C541 — 10u, C

C541 — 10u, C_1206_3216Metric — `/receiver/PEN2_PROT_N` ↔ `/receiver/PEN2_IN_N` — input / output filter capacitor for D522 (pin 1 → 2).

#### C542 — 100n, C

C542 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C543 — 100n, C

C543 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U104, U106, U107 (pin 1 → 2).

#### C544 — 470p, C

C544 — 470p, C_0603_1608Metric — `/receiver/AIN2+` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C545 — 470p, C

C545 — 470p, C_0603_1608Metric — `/receiver/AIN2-` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C546 — 100p, C

C546 — 100p, C_0603_1608Metric — `/receiver/AIN2+` ↔ `/receiver/AIN2-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C547 — 100n, C

C547 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### C560 — 10u, C

C560 — 10u, C_1206_3216Metric — `/receiver/REF_COIL_PROT_P` ↔ `/receiver/REF_COIL_IN_P` — input / output filter capacitor for D530 (pin 1 → 2).

#### C561 — 10u, C

C561 — 10u, C_1206_3216Metric — `/receiver/REF_COIL_PROT_N` ↔ `/receiver/REF_COIL_IN_N` — input / output filter capacitor for D532 (pin 1 → 2).

#### C562 — 100n, C

C562 — 100n, C_0603_1608Metric — `+12VA` ↔ `GND` — supply decoupling for U102, U103, U104, U106, U107 (pin 1 → 2).

#### C563 — 100n, C

C563 — 100n, C_0603_1608Metric — `-12VA` ↔ `GND` — supply decoupling for U104, U106, U107 (pin 1 → 2).

#### C564 — 470p, C

C564 — 470p, C_0603_1608Metric — `/receiver/AIN3+` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C565 — 470p, C

C565 — 470p, C_0603_1608Metric — `/receiver/AIN3-` ↔ `GND` — filter capacitor to ground for U101 (pin 1 → 2).

#### C566 — 100p, C

C566 — 100p, C_0603_1608Metric — `/receiver/AIN3+` ↔ `/receiver/AIN3-` — input / output filter capacitor for U101 (pin 1 → 2).

#### C567 — 100n, C

C567 — 100n, C_0603_1608Metric — `+5VA` ↔ `GND` — feedback filter, supply decoupling for U101, U105, U108, U146 (pin 1 → 2).

#### R100 — 33, R

R100 — 33, R_0603_1608Metric — `CLOCK_32M768` ↔ `/receiver/MCLK` — enable / sequencing network, supply feed / filter for U4, Y1 (pin 1 → 2).

#### R101 — 100, R

R101 — 100, R_0603_1608Metric — `PEN1_P` ↔ `/receiver/PEN1_PROT_P` — series / termination resistor for D101 (pin 1 → 2).

#### R102 — 100, R

R102 — 100, R_0603_1608Metric — `PEN1_N` ↔ `/receiver/PEN1_PROT_N` — series / termination resistor for D103 (pin 1 → 2).

#### R103 — 10k 0.1%, R

R103 — 10k 0.1%, R_0603_1608Metric — `/receiver/INA_IN_P` ↔ `GND` — pull-down resistor for U104 (pin 1 → 2).

#### R104 — 10k 0.1%, R

R104 — 10k 0.1%, R_0603_1608Metric — `/receiver/INA_IN_N` ↔ `GND` — pull-down resistor for U104 (pin 1 → 2).

#### R105 — 176, R

R105 — 176, R_0603_1608Metric — `/receiver/GAIN1` ↔ `/receiver/GAIN2` — series / termination resistor for U104 (pin 1 → 2).

#### R110 — 1k, R

R110 — 1k, R_0603_1608Metric — `CURRENT_SUM` ↔ `Net-(U105A-+IN1)` — supply feed / filter for U105 (pin 1 → 2).

#### R111 — 1k, R

R111 — 1k, R_0603_1608Metric — `GND` ↔ `/receiver/FDA0_N` — pull-down resistor for U104 (pin 1 → 2).

#### R112 — 1k, R

R112 — 1k, R_0603_1608Metric — `/receiver/FDA0_OUT_N` ↔ `Net-(U105A-+IN1)` — supply feed / filter for U105 (pin 1 → 2).

#### R113 — 1k, R

R113 — 1k, R_0603_1608Metric — `/receiver/FDA0_OUT_P` ↔ `/receiver/FDA0_N` — feedback divider for U105 (pin 1 → 2).

#### R114 — 20, R

R114 — 20, R_0603_1608Metric — `/receiver/FDA0_OUT_P` ↔ `/receiver/AIN0+` — feedback divider for U105 (pin 1 → 2).

#### R115 — 20, R

R115 — 20, R_0603_1608Metric — `/receiver/FDA0_OUT_N` ↔ `/receiver/AIN0-` — feedback divider for U105 (pin 1 → 2).

#### R120 — 499, R

R120 — 499, R_0603_1608Metric — `Net-(U104-SENSE)` ↔ `Net-(U105B-+IN2)` — supply feed / filter for U105 (pin 1 → 2).

#### R121 — 499, R

R121 — 499, R_0603_1608Metric — `GND` ↔ `/receiver/FDA1_N` — pull-down resistor for U104 (pin 1 → 2).

#### R122 — 1k, R

R122 — 1k, R_0603_1608Metric — `/receiver/FDA1_OUT_N` ↔ `Net-(U105B-+IN2)` — supply feed / filter for U105 (pin 1 → 2).

#### R123 — 1k, R

R123 — 1k, R_0603_1608Metric — `/receiver/FDA1_OUT_P` ↔ `/receiver/FDA1_N` — feedback divider for U105 (pin 1 → 2).

#### R124 — 20, R

R124 — 20, R_0603_1608Metric — `/receiver/FDA1_OUT_P` ↔ `/receiver/AIN1+` — feedback divider for U105 (pin 1 → 2).

#### R125 — 20, R

R125 — 20, R_0603_1608Metric — `/receiver/FDA1_OUT_N` ↔ `/receiver/AIN1-` — feedback divider for U105 (pin 1 → 2).

#### R180 — 10k, R

R180 — 10k, R_0603_1608Metric — `+3.3V` ↔ `/receiver/ADC_SPI_STRAP` — pull-up resistor for U101 (pin 1 → 2).

#### R181 — 10k, R

R181 — 10k, R_0603_1608Metric — `/receiver/ADC_DAISY_IN` ↔ `GND` — pull-down resistor for U101 (pin 1 → 2).

#### R184 — 10, R

R184 — 10, R_0603_1608Metric — `/receiver/REF_BUF_OUT` ↔ `/receiver/ADC_REF` — supply feed / filter for U103 (pin 1 → 2).

#### R540 — 100, R

R540 — 100, R_0603_1608Metric — `PEN2_P` ↔ `/receiver/PEN2_PROT_P` — series / termination resistor for D520 (pin 1 → 2).

#### R541 — 100, R

R541 — 100, R_0603_1608Metric — `PEN2_N` ↔ `/receiver/PEN2_PROT_N` — series / termination resistor for D522 (pin 1 → 2).

#### R542 — 10k 0.1%, R

R542 — 10k 0.1%, R_0603_1608Metric — `/receiver/PEN2_IN_P` ↔ `GND` — pull-down resistor for U106 (pin 1 → 2).

#### R543 — 10k 0.1%, R

R543 — 10k 0.1%, R_0603_1608Metric — `/receiver/PEN2_IN_N` ↔ `GND` — pull-down resistor for U106 (pin 1 → 2).

#### R544 — 176, R

R544 — 176, R_0603_1608Metric — `/receiver/PEN2_RG1` ↔ `/receiver/PEN2_RG2` — series / termination resistor for U106 (pin 1 → 2).

#### R548 — 499, R

R548 — 499, R_0603_1608Metric — `Net-(U106-SENSE)` ↔ `Net-(U108A-+IN1)` — supply feed / filter for U108 (pin 1 → 2).

#### R549 — 499, R

R549 — 499, R_0603_1608Metric — `GND` ↔ `/receiver/FDA2_N` — pull-down resistor for U106 (pin 1 → 2).

#### R550 — 1k, R

R550 — 1k, R_0603_1608Metric — `/receiver/FDA2_OUT_N` ↔ `Net-(U108A-+IN1)` — supply feed / filter for U108 (pin 1 → 2).

#### R551 — 1k, R

R551 — 1k, R_0603_1608Metric — `/receiver/FDA2_OUT_P` ↔ `/receiver/FDA2_N` — feedback divider for U108 (pin 1 → 2).

#### R552 — 20, R

R552 — 20, R_0603_1608Metric — `/receiver/FDA2_OUT_P` ↔ `/receiver/AIN2+` — feedback divider for U108 (pin 1 → 2).

#### R553 — 20, R

R553 — 20, R_0603_1608Metric — `/receiver/FDA2_OUT_N` ↔ `/receiver/AIN2-` — feedback divider for U108 (pin 1 → 2).

#### R560 — 100, R

R560 — 100, R_0603_1608Metric — `REF_COIL_P` ↔ `/receiver/REF_COIL_PROT_P` — series / termination resistor for D530 (pin 1 → 2).

#### R561 — 100, R

R561 — 100, R_0603_1608Metric — `REF_COIL_N` ↔ `/receiver/REF_COIL_PROT_N` — series / termination resistor for D532 (pin 1 → 2).

#### R562 — 10k 0.1%, R

R562 — 10k 0.1%, R_0603_1608Metric — `/receiver/REF_COIL_IN_P` ↔ `GND` — pull-down resistor for U107 (pin 1 → 2).

#### R563 — 10k 0.1%, R

R563 — 10k 0.1%, R_0603_1608Metric — `/receiver/REF_COIL_IN_N` ↔ `GND` — pull-down resistor for U107 (pin 1 → 2).

#### R564 — 176, R

R564 — 176, R_0603_1608Metric — `/receiver/REF_COIL_RG1` ↔ `/receiver/REF_COIL_RG2` — series / termination resistor for U107 (pin 1 → 2).

#### R568 — 499, R

R568 — 499, R_0603_1608Metric — `Net-(U107-SENSE)` ↔ `Net-(U108B-+IN2)` — supply feed / filter for U108 (pin 1 → 2).

#### R569 — 499, R

R569 — 499, R_0603_1608Metric — `GND` ↔ `/receiver/FDA3_N` — pull-down resistor for U107 (pin 1 → 2).

#### R570 — 1k, R

R570 — 1k, R_0603_1608Metric — `/receiver/FDA3_OUT_N` ↔ `Net-(U108B-+IN2)` — supply feed / filter for U108 (pin 1 → 2).

#### R571 — 1k, R

R571 — 1k, R_0603_1608Metric — `/receiver/FDA3_OUT_P` ↔ `/receiver/FDA3_N` — feedback divider for U108 (pin 1 → 2).

#### R572 — 20, R

R572 — 20, R_0603_1608Metric — `/receiver/FDA3_OUT_P` ↔ `/receiver/AIN3+` — feedback divider for U108 (pin 1 → 2).

#### R573 — 20, R

R573 — 20, R_0603_1608Metric — `/receiver/FDA3_OUT_N` ↔ `/receiver/AIN3-` — feedback divider for U108 (pin 1 → 2).

### 4.5 Page 5 — fpga

Net-centric counterpart: `brd01_wiring_manifest.md` §3.5. 67 components on this sheet.

#### Components

#### J140 — 87831-1420, AMD_Platform_Cable_USB_II_JTAG

Sheet: fpga (5) · Footprint: accubot:Molex_87831-1420 · 14 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | NC_1 | no_connect | `unconnected-(J140-NC-Pad1)` | — (no other pins on this net) |
| 2 | VREF_2 | passive | `+3.3V` | R148.1, U141.8, Y1.4, Y1.1, R149.1, R143.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 3 | GND_3 | passive | `GND` | J140.5, J140.7, J140.9, J140.11, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 4 | TMS_4 | passive | `/fpga/JTAG_TMS` | U4.M7 |
| 5 | GND_5 | passive | `GND` | J140.3, J140.7, J140.9, J140.11, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 6 | TCK_6 | passive | `/fpga/JTAG_TCK` | U4.L7 |
| 7 | GND_7 | passive | `GND` | J140.5, J140.9, J140.11, J140.3, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 8 | TDO_8 | passive | `/fpga/JTAG_TDO` | U4.N8 |
| 9 | GND_9 | passive | `GND` | J140.11, J140.7, J140.5, J140.3, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 10 | TDI_10 | passive | `/fpga/JTAG_TDI` | U4.N7 |
| 11 | GND_11 | passive | `GND` | J140.9, J140.7, J140.5, J140.3, Y1.2, U141.4 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 12 | NC_12 | no_connect | `unconnected-(J140-NC-Pad12)` | — (no other pins on this net) |
| 13 | PGND_13 | passive+no_connect | `unconnected-(J140-PGND-Pad13)` | — (no other pins on this net) |
| 14 | HALT_14 | passive+no_connect | `unconnected-(J140-HALT-Pad14)` | — (no other pins on this net) |

Supporting passives:

- soft-start / bias capacitor: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+27 more; see manifest §3.5) on `+3.3V`

#### TP790 — TestPoint

Sheet: fpga (5) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(U4C-PROGRAM_B_0)` | R144.2, U4.L9 |

Supporting passives:

- pull-up resistor: R144 (4.7k) on `Net-(U4C-PROGRAM_B_0)`

#### TP791 — TestPoint

Sheet: fpga (5) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(U4C-INIT_B_0)` | R142.2, U4.K10 |

Supporting passives:

- pull-up resistor: R142 (4.7k) on `Net-(U4C-INIT_B_0)`

#### TP792 — TestPoint

Sheet: fpga (5) · Footprint: TestPoint:TestPoint_Pad_D1.5mm · 1 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | 1_1 | passive | `Net-(U4C-DONE_0)` | R143.2, U4.H10 |

#### U4 — XC7A35T-1FTG256C, XC7A35T-FTG256

Sheet: fpga (5) · Footprint: Package_BGA:Xilinx_FTG256 · 256 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| A1 | GND_A1 | power_in | `GND` | U4.A11, U4.B8, U4.C5, U4.C15, U4.D2, U4.F8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| A2 | IO_L8N_T1_AD14N_35_A2 | bidirectional+no_connect | `unconnected-(U4B-IO_L8N_T1_AD14N_35-PadA2)` | — (no other pins on this net) |
| A3 | IO_L4N_T0_35_A3 | bidirectional+no_connect | `unconnected-(U4B-IO_L4N_T0_35-PadA3)` | — (no other pins on this net) |
| A4 | IO_L3N_T0_DQS_AD5N_35_A4 | bidirectional+no_connect | `unconnected-(U4B-IO_L3N_T0_DQS_AD5N_35-PadA4)` | — (no other pins on this net) |
| A5 | IO_L3P_T0_DQS_AD5P_35_A5 | bidirectional+no_connect | `unconnected-(U4B-IO_L3P_T0_DQS_AD5P_35-PadA5)` | — (no other pins on this net) |
| A6 | VCCO_35_A6 | power_in | `+3.3V` | U4.B3, U4.D7, U4.E4, U4.F1, U4.J2, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| A7 | IO_L1N_T0_AD4N_35_A7 | bidirectional+no_connect | `unconnected-(U4B-IO_L1N_T0_AD4N_35-PadA7)` | — (no other pins on this net) |
| A8 | IO_L2P_T0_AD8P_15_A8 | bidirectional | `ADC_DOUT0` | U101.27 |
| A9 | IO_L2N_T0_AD8N_15_A9 | bidirectional | `ADC_DOUT1` | U101.26 |
| A10 | IO_L3N_T0_DQS_AD1N_15_A10 | bidirectional | `ADC_DOUT3` | U101.24 |
| A11 | GND_A11 | power_in | `GND` | U4.A1, U4.B8, U4.C5, U4.C15, U4.D2, U4.D12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| A12 | IO_L5N_T0_AD9N_15_A12 | bidirectional | `ADC_SDI` | U101.18 |
| A13 | IO_L7P_T1_AD2P_15_A13 | bidirectional | `ADC_SCLK` | U101.17 |
| A14 | IO_L7N_T1_AD2N_15_A14 | bidirectional | `ADC_RESET_N` | R163.2, U101.30 |
| A15 | IO_L9N_T1_DQS_AD3N_15_A15 | bidirectional | `ADC_SYNC_OUT` | U101.38 |
| A16 | VCCO_15_A16 | power_in | `+3.3V` | U4.B13, U4.C10, U4.E14, U4.H15, U4.J12, U4.T11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B1 | IO_L9N_T1_DQS_AD7N_35_B1 | bidirectional+no_connect | `unconnected-(U4B-IO_L9N_T1_DQS_AD7N_35-PadB1)` | — (no other pins on this net) |
| B2 | IO_L8P_T1_AD14P_35_B2 | bidirectional+no_connect | `unconnected-(U4B-IO_L8P_T1_AD14P_35-PadB2)` | — (no other pins on this net) |
| B3 | VCCO_35_B3 | power_in | `+3.3V` | U4.D7, U4.A6, U4.E4, U4.F1, U4.J2, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B4 | IO_L4P_T0_35_B4 | bidirectional+no_connect | `unconnected-(U4B-IO_L4P_T0_35-PadB4)` | — (no other pins on this net) |
| B5 | IO_L2N_T0_AD12N_35_B5 | bidirectional+no_connect | `unconnected-(U4B-IO_L2N_T0_AD12N_35-PadB5)` | — (no other pins on this net) |
| B6 | IO_L2P_T0_AD12P_35_B6 | bidirectional+no_connect | `unconnected-(U4B-IO_L2P_T0_AD12P_35-PadB6)` | — (no other pins on this net) |
| B7 | IO_L1P_T0_AD4P_35_B7 | bidirectional+no_connect | `unconnected-(U4B-IO_L1P_T0_AD4P_35-PadB7)` | — (no other pins on this net) |
| B8 | GND_B8 | power_in | `GND` | U4.C5, U4.A11, U4.C15, U4.A1, U4.D2, U4.D12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B9 | IO_L3P_T0_DQS_AD1P_15_B9 | bidirectional | `ADC_DOUT2` | U101.25 |
| B10 | IO_L4P_T0_15_B10 | bidirectional | `ADC_DRDY_N` | U101.29 |
| B11 | IO_L4N_T0_15_B11 | bidirectional | `ADC_SDO` | U101.19 |
| B12 | IO_L5P_T0_AD9P_15_B12 | bidirectional | `ADC_CS` | R164.2, U101.16 |
| B13 | VCCO_15_B13 | power_in | `+3.3V` | U4.C10, U4.A16, U4.E14, U4.H15, U4.J12, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| B14 | IO_L8N_T1_AD10N_15_B14 | bidirectional | `ADC_START_N` | R165.2, U101.37 |
| B15 | IO_L9P_T1_DQS_AD3P_15_B15 | bidirectional+no_connect | `unconnected-(U4A-IO_L9P_T1_DQS_AD3P_15-PadB15)` | — (no other pins on this net) |
| B16 | IO_L10N_T1_AD11N_15_B16 | bidirectional+no_connect | `unconnected-(U4A-IO_L10N_T1_AD11N_15-PadB16)` | — (no other pins on this net) |
| C1 | IO_L9P_T1_DQS_AD7P_35_C1 | bidirectional+no_connect | `unconnected-(U4B-IO_L9P_T1_DQS_AD7P_35-PadC1)` | — (no other pins on this net) |
| C2 | IO_L7N_T1_AD6N_35_C2 | bidirectional+no_connect | `unconnected-(U4B-IO_L7N_T1_AD6N_35-PadC2)` | — (no other pins on this net) |
| C3 | IO_L7P_T1_AD6P_35_C3 | bidirectional+no_connect | `unconnected-(U4B-IO_L7P_T1_AD6P_35-PadC3)` | — (no other pins on this net) |
| C4 | IO_L12N_T1_MRCC_35_C4 | bidirectional+no_connect | `unconnected-(U4B-IO_L12N_T1_MRCC_35-PadC4)` | — (no other pins on this net) |
| C5 | GND_C5 | power_in | `GND` | U4.B8, U4.C15, U4.D2, U4.A11, U4.A1, U4.D12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| C6 | IO_L5N_T0_AD13N_35_C6 | bidirectional+no_connect | `unconnected-(U4B-IO_L5N_T0_AD13N_35-PadC6)` | — (no other pins on this net) |
| C7 | IO_L5P_T0_AD13P_35_C7 | bidirectional+no_connect | `unconnected-(U4B-IO_L5P_T0_AD13P_35-PadC7)` | — (no other pins on this net) |
| C8 | IO_L1P_T0_AD0P_15_C8 | bidirectional+no_connect | `unconnected-(U4A-IO_L1P_T0_AD0P_15-PadC8)` | — (no other pins on this net) |
| C9 | IO_L1N_T0_AD0N_15_C9 | bidirectional+no_connect | `unconnected-(U4A-IO_L1N_T0_AD0N_15-PadC9)` | — (no other pins on this net) |
| C10 | VCCO_15_C10 | power_in | `+3.3V` | U4.B13, U4.E14, U4.A16, U4.H15, U4.J12, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| C11 | IO_L11P_T1_SRCC_15_C11 | bidirectional | `ADC_DCLK` | U101.28 |
| C12 | IO_L11N_T1_SRCC_15_C12 | bidirectional+no_connect | `unconnected-(U4A-IO_L11N_T1_SRCC_15-PadC12)` | — (no other pins on this net) |
| C13 | IO_L12N_T1_MRCC_15_C13 | bidirectional+no_connect | `unconnected-(U4A-IO_L12N_T1_MRCC_15-PadC13)` | — (no other pins on this net) |
| C14 | IO_L8P_T1_AD10P_15_C14 | bidirectional | `ADC_SYNC_IN` | R166.2, U101.36 |
| C15 | GND_C15 | power_in | `GND` | U4.C5, U4.D2, U4.B8, U4.D12, U4.A11, U4.E9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| C16 | IO_L10P_T1_AD11P_15_C16 | bidirectional+no_connect | `unconnected-(U4A-IO_L10P_T1_AD11P_15-PadC16)` | — (no other pins on this net) |
| D1 | IO_L10N_T1_AD15N_35_D1 | bidirectional+no_connect | `unconnected-(U4B-IO_L10N_T1_AD15N_35-PadD1)` | — (no other pins on this net) |
| D2 | GND_D2 | power_in | `GND` | U4.C15, U4.D12, U4.C5, U4.E9, U4.B8, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| D3 | IO_L11N_T1_SRCC_35_D3 | bidirectional+no_connect | `unconnected-(U4B-IO_L11N_T1_SRCC_35-PadD3)` | — (no other pins on this net) |
| D4 | IO_L12P_T1_MRCC_35_D4 | bidirectional+no_connect | `unconnected-(U4B-IO_L12P_T1_MRCC_35-PadD4)` | — (no other pins on this net) |
| D5 | IO_L6N_T0_VREF_35_D5 | bidirectional+no_connect | `unconnected-(U4B-IO_L6N_T0_VREF_35-PadD5)` | — (no other pins on this net) |
| D6 | IO_L6P_T0_35_D6 | bidirectional+no_connect | `unconnected-(U4B-IO_L6P_T0_35-PadD6)` | — (no other pins on this net) |
| D7 | VCCO_35_D7 | power_in | `+3.3V` | U4.B3, U4.E4, U4.F1, U4.A6, U4.J2, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| D8 | IO_L6P_T0_15_D8 | bidirectional+no_connect | `unconnected-(U4A-IO_L6P_T0_15-PadD8)` | — (no other pins on this net) |
| D9 | IO_L6N_T0_VREF_15_D9 | bidirectional+no_connect | `unconnected-(U4A-IO_L6N_T0_VREF_15-PadD9)` | — (no other pins on this net) |
| D10 | IO_0_15_D10 | bidirectional+no_connect | `unconnected-(U4A-IO_0_15-PadD10)` | — (no other pins on this net) |
| D11 | IO_L14N_T2_SRCC_15_D11 | bidirectional+no_connect | `unconnected-(U4A-IO_L14N_T2_SRCC_15-PadD11)` | — (no other pins on this net) |
| D12 | GND_D12 | power_in | `GND` | U4.E9, U4.D2, U4.C15, U4.F6, U4.F10, U4.C5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| D13 | IO_L12P_T1_MRCC_15_D13 | bidirectional | `CLOCK_32M768` | Y1.3, R100.1 |
| D14 | IO_L15P_T2_DQS_15_D14 | bidirectional+no_connect | `unconnected-(U4A-IO_L15P_T2_DQS_15-PadD14)` | — (no other pins on this net) |
| D15 | IO_L15N_T2_DQS_ADV_B_15_D15 | bidirectional+no_connect | `unconnected-(U4A-IO_L15N_T2_DQS_ADV_B_15-PadD15)` | — (no other pins on this net) |
| D16 | IO_L17N_T2_A25_15_D16 | bidirectional+no_connect | `unconnected-(U4A-IO_L17N_T2_A25_15-PadD16)` | — (no other pins on this net) |
| E1 | IO_L15N_T2_DQS_35_E1 | bidirectional+no_connect | `unconnected-(U4B-IO_L15N_T2_DQS_35-PadE1)` | — (no other pins on this net) |
| E2 | IO_L10P_T1_AD15P_35_E2 | bidirectional+no_connect | `unconnected-(U4B-IO_L10P_T1_AD15P_35-PadE2)` | — (no other pins on this net) |
| E3 | IO_L11P_T1_SRCC_35_E3 | bidirectional+no_connect | `unconnected-(U4B-IO_L11P_T1_SRCC_35-PadE3)` | — (no other pins on this net) |
| E4 | VCCO_35_E4 | power_in | `+3.3V` | U4.D7, U4.F1, U4.B3, U4.J2, U4.A6, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E5 | IO_L13N_T2_MRCC_35_E5 | bidirectional+no_connect | `unconnected-(U4B-IO_L13N_T2_MRCC_35-PadE5)` | — (no other pins on this net) |
| E6 | IO_0_35_E6 | bidirectional+no_connect | `unconnected-(U4B-IO_0_35-PadE6)` | — (no other pins on this net) |
| E7 | CFGBVS_0_E7 | bidirectional | `/fpga/CFGBVS` | R154.2 |
| E8 | CCLK_0_E8 | bidirectional | `Net-(U4C-CCLK_0)` | R790.1 |
| E9 | GND_E9 | power_in | `GND` | U4.D12, U4.F6, U4.F10, U4.D2, U4.C15, U4.F16 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E10 | VCCBRAM_E10 | power_in | `+1V0_FPGA` | U4.F11, U4.L8, U4.K9, U4.J6, U4.H9, U4.G6 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E11 | IO_L14P_T2_SRCC_15_E11 | bidirectional+no_connect | `unconnected-(U4A-IO_L14P_T2_SRCC_15-PadE11)` | — (no other pins on this net) |
| E12 | IO_L13P_T2_MRCC_15_E12 | bidirectional+no_connect | `unconnected-(U4A-IO_L13P_T2_MRCC_15-PadE12)` | — (no other pins on this net) |
| E13 | IO_L13N_T2_MRCC_15_E13 | bidirectional+no_connect | `unconnected-(U4A-IO_L13N_T2_MRCC_15-PadE13)` | — (no other pins on this net) |
| E14 | VCCO_15_E14 | power_in | `+3.3V` | U4.C10, U4.H15, U4.B13, U4.J12, U4.A16, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| E15 | IO_L18N_T2_A23_15_E15 | bidirectional+no_connect | `unconnected-(U4A-IO_L18N_T2_A23_15-PadE15)` | — (no other pins on this net) |
| E16 | IO_L17P_T2_A26_15_E16 | bidirectional+no_connect | `unconnected-(U4A-IO_L17P_T2_A26_15-PadE16)` | — (no other pins on this net) |
| F1 | VCCO_35_F1 | power_in | `+3.3V` | U4.E4, U4.J2, U4.D7, U4.B3, U4.A6, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F2 | IO_L15P_T2_DQS_35_F2 | bidirectional+no_connect | `unconnected-(U4B-IO_L15P_T2_DQS_35-PadF2)` | — (no other pins on this net) |
| F3 | IO_L14N_T2_SRCC_35_F3 | bidirectional+no_connect | `unconnected-(U4B-IO_L14N_T2_SRCC_35-PadF3)` | — (no other pins on this net) |
| F4 | IO_L14P_T2_SRCC_35_F4 | bidirectional+no_connect | `unconnected-(U4B-IO_L14P_T2_SRCC_35-PadF4)` | — (no other pins on this net) |
| F5 | IO_L13P_T2_MRCC_35_F5 | bidirectional+no_connect | `unconnected-(U4B-IO_L13P_T2_MRCC_35-PadF5)` | — (no other pins on this net) |
| F6 | GND_F6 | power_in | `GND` | U4.F10, U4.E9, U4.F16, U4.D12, U4.G3, U4.D2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F7 | VCCINT_F7 | power_in | `+1V0_FPGA` | U4.F9, U4.G6, U4.H9, U4.J6, U4.K9, U4.L8 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F8 | VCCBATT_0_F8 | power_in | `GND` | U4.G7, U4.A1, U4.A11, U4.B8, U4.C5, U4.C15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F9 | VCCINT_F9 | power_in | `+1V0_FPGA` | U4.F7, U4.G6, U4.H9, U4.J6, U4.K9, U4.L8 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F10 | GND_F10 | power_in | `GND` | U4.F6, U4.F16, U4.E9, U4.G3, U4.D12, U4.G9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F11 | VCCBRAM_F11 | power_in | `+1V0_FPGA` | U4.E10, U4.L8, U4.K9, U4.J6, U4.H9, U4.G6 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| F12 | IO_L16P_T2_A28_15_F12 | bidirectional+no_connect | `unconnected-(U4A-IO_L16P_T2_A28_15-PadF12)` | — (no other pins on this net) |
| F13 | IO_L16N_T2_A27_15_F13 | bidirectional+no_connect | `unconnected-(U4A-IO_L16N_T2_A27_15-PadF13)` | — (no other pins on this net) |
| F14 | IO_L21N_T3_DQS_A18_15_F14 | bidirectional+no_connect | `unconnected-(U4A-IO_L21N_T3_DQS_A18_15-PadF14)` | — (no other pins on this net) |
| F15 | IO_L18P_T2_A24_15_F15 | bidirectional+no_connect | `unconnected-(U4A-IO_L18P_T2_A24_15-PadF15)` | — (no other pins on this net) |
| F16 | GND_F16 | power_in | `GND` | U4.F10, U4.G3, U4.F6, U4.G9, U4.E9, U4.G13 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G1 | IO_L17N_T2_35_G1 | bidirectional+no_connect | `unconnected-(U4B-IO_L17N_T2_35-PadG1)` | — (no other pins on this net) |
| G2 | IO_L17P_T2_35_G2 | bidirectional+no_connect | `unconnected-(U4B-IO_L17P_T2_35-PadG2)` | — (no other pins on this net) |
| G3 | GND_G3 | power_in | `GND` | U4.G9, U4.F16, U4.G13, U4.F10, U4.H6, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G4 | IO_L16N_T2_35_G4 | bidirectional+no_connect | `unconnected-(U4B-IO_L16N_T2_35-PadG4)` | — (no other pins on this net) |
| G5 | IO_L16P_T2_35_G5 | bidirectional+no_connect | `unconnected-(U4B-IO_L16P_T2_35-PadG5)` | — (no other pins on this net) |
| G6 | VCCINT_G6 | power_in | `+1V0_FPGA` | U4.F9, U4.H9, U4.F7, U4.J6, U4.K9, U4.L8 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G7 | GNDADC_0_G7 | power_in | `GND` | U4.F8, U4.A1, U4.A11, U4.B8, U4.C5, U4.C15 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G8 | VCCADC_0_G8 | power_in | `+1V8_FPGA` | U4.L10, U4.K11, U4.J10, U4.G10, C158.1, C159.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G9 | GND_G9 | power_in | `GND` | U4.G3, U4.G13, U4.F16, U4.H6, U4.F10, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G10 | VCCAUX_G10 | power_in | `+1V8_FPGA` | U4.J10, U4.K11, U4.L10, U4.G8, C157.1, C158.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G11 | IO_25_15_G11 | bidirectional+no_connect | `unconnected-(U4A-IO_25_15-PadG11)` | — (no other pins on this net) |
| G12 | IO_L19N_T3_A21_VREF_15_G12 | bidirectional+no_connect | `unconnected-(U4A-IO_L19N_T3_A21_VREF_15-PadG12)` | — (no other pins on this net) |
| G13 | GND_G13 | power_in | `GND` | U4.H6, U4.G9, U4.G3, U4.F16, U4.F10, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| G14 | IO_L21P_T3_DQS_15_G14 | bidirectional+no_connect | `unconnected-(U4A-IO_L21P_T3_DQS_15-PadG14)` | — (no other pins on this net) |
| G15 | IO_L24N_T3_RS0_15_G15 | bidirectional+no_connect | `unconnected-(U4A-IO_L24N_T3_RS0_15-PadG15)` | — (no other pins on this net) |
| G16 | IO_L22N_T3_A16_15_G16 | bidirectional+no_connect | `unconnected-(U4A-IO_L22N_T3_A16_15-PadG16)` | — (no other pins on this net) |
| H1 | IO_L20N_T3_35_H1 | bidirectional+no_connect | `unconnected-(U4B-IO_L20N_T3_35-PadH1)` | — (no other pins on this net) |
| H2 | IO_L20P_T3_35_H2 | bidirectional+no_connect | `unconnected-(U4B-IO_L20P_T3_35-PadH2)` | — (no other pins on this net) |
| H3 | IO_L21N_T3_DQS_35_H3 | bidirectional+no_connect | `unconnected-(U4B-IO_L21N_T3_DQS_35-PadH3)` | — (no other pins on this net) |
| H4 | IO_L18N_T2_35_H4 | bidirectional+no_connect | `unconnected-(U4B-IO_L18N_T2_35-PadH4)` | — (no other pins on this net) |
| H5 | IO_L18P_T2_35_H5 | bidirectional+no_connect | `unconnected-(U4B-IO_L18P_T2_35-PadH5)` | — (no other pins on this net) |
| H6 | GND_H6 | power_in | `GND` | U4.G13, U4.G9, U4.G3, U4.F16, U4.F10, U4.F6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| H7 | VREFN_0_H7 | bidirectional | `/fpga/XADC_VNREF` | R150.1 |
| H8 | VP_0_H8 | bidirectional | `/fpga/XADC_VP` | R151.1 |
| H9 | VCCINT_H9 | power_in | `+1V0_FPGA` | U4.J6, U4.G6, U4.K9, U4.F9, U4.L8, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| H10 | DONE_0_H10 | bidirectional | `Net-(U4C-DONE_0)` | TP792.1, R143.2 |
| H11 | IO_L19P_T3_A22_15_H11 | bidirectional+no_connect | `unconnected-(U4A-IO_L19P_T3_A22_15-PadH11)` | — (no other pins on this net) |
| H12 | IO_L20P_T3_A20_15_H12 | bidirectional+no_connect | `unconnected-(U4A-IO_L20P_T3_A20_15-PadH12)` | — (no other pins on this net) |
| H13 | IO_L20N_T3_A19_15_H13 | bidirectional+no_connect | `unconnected-(U4A-IO_L20N_T3_A19_15-PadH13)` | — (no other pins on this net) |
| H14 | IO_L24P_T3_RS1_15_H14 | bidirectional+no_connect | `unconnected-(U4A-IO_L24P_T3_RS1_15-PadH14)` | — (no other pins on this net) |
| H15 | VCCO_15_H15 | power_in | `+3.3V` | U4.J12, U4.E14, U4.C10, U4.B13, U4.A16, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| H16 | IO_L22P_T3_A17_15_H16 | bidirectional+no_connect | `unconnected-(U4A-IO_L22P_T3_A17_15-PadH16)` | — (no other pins on this net) |
| J1 | IO_L22N_T3_35_J1 | bidirectional+no_connect | `unconnected-(U4B-IO_L22N_T3_35-PadJ1)` | — (no other pins on this net) |
| J2 | VCCO_35_J2 | power_in | `+3.3V` | U4.F1, U4.E4, U4.D7, U4.B3, U4.A6, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J3 | IO_L21P_T3_DQS_35_J3 | bidirectional+no_connect | `unconnected-(U4B-IO_L21P_T3_DQS_35-PadJ3)` | — (no other pins on this net) |
| J4 | IO_L19N_T3_VREF_35_J4 | bidirectional+no_connect | `unconnected-(U4B-IO_L19N_T3_VREF_35-PadJ4)` | — (no other pins on this net) |
| J5 | IO_L19P_T3_35_J5 | bidirectional+no_connect | `unconnected-(U4B-IO_L19P_T3_35-PadJ5)` | — (no other pins on this net) |
| J6 | VCCINT_J6 | power_in | `+1V0_FPGA` | U4.H9, U4.K9, U4.L8, U4.G6, U4.F9, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J7 | VN_0_J7 | bidirectional | `/fpga/XADC_VN` | R152.1 |
| J8 | VREFP_0_J8 | bidirectional | `/fpga/XADC_VPREF` | R153.1 |
| J9 | GND_J9 | power_in | `GND` | U4.J11, U4.K4, U4.K6, U4.K14, U4.L1, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J10 | VCCAUX_J10 | power_in | `+1V8_FPGA` | U4.G10, U4.K11, U4.L10, U4.G8, C157.1, C158.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J11 | GND_J11 | power_in | `GND` | U4.J9, U4.K4, U4.K6, U4.K14, U4.L1, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J12 | VCCO_15_J12 | power_in | `+3.3V` | U4.H15, U4.E14, U4.C10, U4.B13, U4.A16, U4.L6 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| J13 | IO_L1P_T0_D00_MOSI_14_J13 | bidirectional | `/fpga/QSPI_D0` | U141.5 |
| J14 | IO_L1N_T0_D01_DIN_14_J14 | bidirectional | `/fpga/QSPI_D1` | U141.2 |
| J15 | IO_L23P_T3_FOE_B_15_J15 | bidirectional+no_connect | `unconnected-(U4A-IO_L23P_T3_FOE_B_15-PadJ15)` | — (no other pins on this net) |
| J16 | IO_L23N_T3_FWE_B_15_J16 | bidirectional+no_connect | `unconnected-(U4A-IO_L23N_T3_FWE_B_15-PadJ16)` | — (no other pins on this net) |
| K1 | IO_L22P_T3_35_K1 | bidirectional+no_connect | `unconnected-(U4B-IO_L22P_T3_35-PadK1)` | — (no other pins on this net) |
| K2 | IO_L24N_T3_35_K2 | bidirectional+no_connect | `unconnected-(U4B-IO_L24N_T3_35-PadK2)` | — (no other pins on this net) |
| K3 | IO_L24P_T3_35_K3 | bidirectional+no_connect | `unconnected-(U4B-IO_L24P_T3_35-PadK3)` | — (no other pins on this net) |
| K4 | GND_K4 | power_in | `GND` | U4.K6, U4.J11, U4.K14, U4.J9, U4.L1, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K5 | IO_25_35_K5 | bidirectional+no_connect | `unconnected-(U4B-IO_25_35-PadK5)` | — (no other pins on this net) |
| K6 | GND_K6 | power_in | `GND` | U4.K14, U4.K4, U4.L1, U4.J11, U4.J9, U4.L11 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K7 | DXN_0_K7 | bidirectional+no_connect | `unconnected-(U4C-DXN_0-PadK7)` | — (no other pins on this net) |
| K8 | DXP_0_K8 | bidirectional+no_connect | `unconnected-(U4C-DXP_0-PadK8)` | — (no other pins on this net) |
| K9 | VCCINT_K9 | power_in | `+1V0_FPGA` | U4.J6, U4.L8, U4.H9, U4.G6, U4.F9, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K10 | INIT_B_0_K10 | bidirectional | `Net-(U4C-INIT_B_0)` | TP791.1, R142.2 |
| K11 | VCCAUX_K11 | power_in | `+1V8_FPGA` | U4.J10, U4.L10, U4.G10, U4.G8, C157.1, C158.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K12 | IO_0_14_K12 | bidirectional+no_connect | `unconnected-(U4A-IO_0_14-PadK12)` | — (no other pins on this net) |
| K13 | IO_L5P_T0_D06_14_K13 | bidirectional+no_connect | `unconnected-(U4A-IO_L5P_T0_D06_14-PadK13)` | — (no other pins on this net) |
| K14 | GND_K14 | power_in | `GND` | U4.K6, U4.L1, U4.K4, U4.L11, U4.J11, U4.M8 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| K15 | IO_L2P_T0_D02_14_K15 | bidirectional | `/fpga/QSPI_D2` | U141.3, R148.2 |
| K16 | IO_L2N_T0_D03_14_K16 | bidirectional | `/fpga/QSPI_D3` | U141.7, R149.2 |
| L1 | GND_L1 | power_in | `GND` | U4.K14, U4.L11, U4.K6, U4.M8, U4.K4, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L2 | IO_L23N_T3_35_L2 | bidirectional+no_connect | `unconnected-(U4B-IO_L23N_T3_35-PadL2)` | — (no other pins on this net) |
| L3 | IO_L23P_T3_35_L3 | bidirectional+no_connect | `unconnected-(U4B-IO_L23P_T3_35-PadL3)` | — (no other pins on this net) |
| L4 | IO_L1P_T0_34_L4 | bidirectional | `/fpga/DAC_SDI_SRC` | R147.1 |
| L5 | IO_0_34_L5 | bidirectional+no_connect | `unconnected-(U4B-IO_0_34-PadL5)` | — (no other pins on this net) |
| L6 | VCCO_0_L6 | power_in | `+3.3V` | U4.J12, U4.H15, U4.E14, U4.C10, U4.B13, U4.A16 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L7 | TCK_0_L7 | bidirectional | `/fpga/JTAG_TCK` | J140.6 |
| L8 | VCCINT_L8 | power_in | `+1V0_FPGA` | U4.K9, U4.J6, U4.H9, U4.G6, U4.F9, U4.F7 — 20 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L9 | PROGRAM_B_0_L9 | bidirectional | `Net-(U4C-PROGRAM_B_0)` | TP790.1, R144.2 |
| L10 | VCCAUX_L10 | power_in | `+1V8_FPGA` | U4.K11, U4.J10, U4.G8, U4.G10, C158.1, C157.1 — 14 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L11 | GND_L11 | power_in | `GND` | U4.M8, U4.L1, U4.K14, U4.N5, U4.N15, U4.K6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| L12 | IO_L6P_T0_FCS_B_14_L12 | bidirectional | `/fpga/QSPI_CS` | R140.2, U141.1 |
| L13 | IO_L5N_T0_D07_14_L13 | bidirectional+no_connect | `unconnected-(U4A-IO_L5N_T0_D07_14-PadL13)` | — (no other pins on this net) |
| L14 | IO_L4P_T0_D04_14_L14 | bidirectional+no_connect | `unconnected-(U4A-IO_L4P_T0_D04_14-PadL14)` | — (no other pins on this net) |
| L15 | IO_L3P_T0_DQS_PUDC_B_14_L15 | bidirectional | `/fpga/PUDC_N` | R141.2 |
| L16 | VCCO_14_L16 | power_in | `+3.3V` | U4.M13, U4.N10, U4.P7, U4.R14, U4.T11, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M1 | IO_L2N_T0_34_M1 | bidirectional | `/fpga/DAC_SCLK_SRC` | R146.1 |
| M2 | IO_L2P_T0_34_M2 | bidirectional | `/fpga/DAC_CS_SRC` | R145.1 |
| M3 | VCCO_34_M3 | power_in | `+3.3V` | U4.R4, U4.T1, U4.A6, U4.B3, U4.D7, U4.E4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M4 | IO_L1N_T0_34_M4 | bidirectional | `DAC_SDO` | TP203.1, U10.15 |
| M5 | IO_L6P_T0_34_M5 | bidirectional+no_connect | `unconnected-(U4B-IO_L6P_T0_34-PadM5)` | — (no other pins on this net) |
| M6 | IO_L19P_T3_A10_D26_14_M6 | bidirectional+no_connect | `unconnected-(U4A-IO_L19P_T3_A10_D26_14-PadM6)` | — (no other pins on this net) |
| M7 | TMS_0_M7 | bidirectional | `/fpga/JTAG_TMS` | J140.4 |
| M8 | GND_M8 | power_in | `GND` | U4.L11, U4.N5, U4.N15, U4.L1, U4.K14, U4.P2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M9 | M0_0_M9 | bidirectional | `/fpga/MODE0` | R155.2 |
| M10 | M1_0_M10 | bidirectional | `/fpga/MODE1` | R156.2 |
| M11 | M2_0_M11 | bidirectional | `/fpga/MODE2` | R157.2 |
| M12 | IO_L6N_T0_D08_VREF_14_M12 | bidirectional+no_connect | `unconnected-(U4A-IO_L6N_T0_D08_VREF_14-PadM12)` | — (no other pins on this net) |
| M13 | VCCO_14_M13 | power_in | `+3.3V` | U4.L16, U4.N10, U4.P7, U4.R14, U4.T11, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| M14 | IO_L4N_T0_D05_14_M14 | bidirectional+no_connect | `unconnected-(U4A-IO_L4N_T0_D05_14-PadM14)` | — (no other pins on this net) |
| M15 | IO_L3N_T0_DQS_EMCCLK_14_M15 | bidirectional+no_connect | `unconnected-(U4A-IO_L3N_T0_DQS_EMCCLK_14-PadM15)` | — (no other pins on this net) |
| M16 | IO_L7P_T1_D09_14_M16 | bidirectional+no_connect | `unconnected-(U4A-IO_L7P_T1_D09_14-PadM16)` | — (no other pins on this net) |
| N1 | IO_L4P_T0_34_N1 | bidirectional | `HOST_TX` | U142.1 |
| N2 | IO_L3N_T0_DQS_34_N2 | bidirectional | `PICO_TX` | J123.3 |
| N3 | IO_L3P_T0_DQS_34_N3 | bidirectional | `PICO_RX` | J123.4 |
| N4 | IO_L6N_T0_VREF_34_N4 | bidirectional+no_connect | `unconnected-(U4B-IO_L6N_T0_VREF_34-PadN4)` | — (no other pins on this net) |
| N5 | GND_N5 | power_in | `GND` | U4.N15, U4.M8, U4.P2, U4.L11, U4.P12, U4.L1 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| N6 | IO_L19N_T3_A09_D25_VREF_14_N6 | bidirectional+no_connect | `unconnected-(U4A-IO_L19N_T3_A09_D25_VREF_14-PadN6)` | — (no other pins on this net) |
| N7 | TDI_0_N7 | bidirectional | `/fpga/JTAG_TDI` | J140.10 |
| N8 | TDO_0_N8 | bidirectional | `/fpga/JTAG_TDO` | J140.8 |
| N9 | IO_L18P_T2_A12_D28_14_N9 | bidirectional+no_connect | `unconnected-(U4A-IO_L18P_T2_A12_D28_14-PadN9)` | — (no other pins on this net) |
| N10 | VCCO_14_N10 | power_in | `+3.3V` | U4.M13, U4.P7, U4.L16, U4.R14, U4.T11, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| N11 | IO_L13P_T2_MRCC_14_N11 | bidirectional+no_connect | `unconnected-(U4A-IO_L13P_T2_MRCC_14-PadN11)` | — (no other pins on this net) |
| N12 | IO_L13N_T2_MRCC_14_N12 | bidirectional+no_connect | `unconnected-(U4A-IO_L13N_T2_MRCC_14-PadN12)` | — (no other pins on this net) |
| N13 | IO_L11P_T1_SRCC_14_N13 | bidirectional+no_connect | `unconnected-(U4A-IO_L11P_T1_SRCC_14-PadN13)` | — (no other pins on this net) |
| N14 | IO_L12P_T1_MRCC_14_N14 | bidirectional+no_connect | `unconnected-(U4A-IO_L12P_T1_MRCC_14-PadN14)` | — (no other pins on this net) |
| N15 | GND_N15 | power_in | `GND` | U4.N5, U4.P2, U4.M8, U4.P12, U4.L11, U4.R9 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| N16 | IO_L7N_T1_D10_14_N16 | bidirectional+no_connect | `unconnected-(U4A-IO_L7N_T1_D10_14-PadN16)` | — (no other pins on this net) |
| P1 | IO_L4N_T0_34_P1 | bidirectional | `HOST_RX` | U142.17 |
| P2 | GND_P2 | power_in | `GND` | U4.N15, U4.P12, U4.N5, U4.R9, U4.M8, U4.T6 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| P3 | IO_L5N_T0_34_P3 | bidirectional | `PICO_HEARTBEAT` | J123.6 |
| P4 | IO_L5P_T0_34_P4 | bidirectional | `PICO_STOP_REQ_N` | R754.1, U755.1 |
| P5 | IO_L10P_T1_34_P5 | bidirectional+no_connect | `unconnected-(U4B-IO_L10P_T1_34-PadP5)` | — (no other pins on this net) |
| P6 | IO_25_14_P6 | bidirectional+no_connect | `unconnected-(U4A-IO_25_14-PadP6)` | — (no other pins on this net) |
| P7 | VCCO_14_P7 | power_in | `+3.3V` | U4.R14, U4.N10, U4.T11, U4.M13, U4.L16, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| P8 | IO_L20P_T3_A08_D24_14_P8 | bidirectional+no_connect | `unconnected-(U4A-IO_L20P_T3_A08_D24_14-PadP8)` | — (no other pins on this net) |
| P9 | IO_L18N_T2_A11_D27_14_P9 | bidirectional+no_connect | `unconnected-(U4A-IO_L18N_T2_A11_D27_14-PadP9)` | — (no other pins on this net) |
| P10 | IO_L14P_T2_SRCC_14_P10 | bidirectional+no_connect | `unconnected-(U4A-IO_L14P_T2_SRCC_14-PadP10)` | — (no other pins on this net) |
| P11 | IO_L14N_T2_SRCC_14_P11 | bidirectional+no_connect | `unconnected-(U4A-IO_L14N_T2_SRCC_14-PadP11)` | — (no other pins on this net) |
| P12 | GND_P12 | power_in | `GND` | U4.R9, U4.P2, U4.T6, U4.N15, U4.T16, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| P13 | IO_L11N_T1_SRCC_14_P13 | bidirectional+no_connect | `unconnected-(U4A-IO_L11N_T1_SRCC_14-PadP13)` | — (no other pins on this net) |
| P14 | IO_L12N_T1_MRCC_14_P14 | bidirectional+no_connect | `unconnected-(U4A-IO_L12N_T1_MRCC_14-PadP14)` | — (no other pins on this net) |
| P15 | IO_L8P_T1_D11_14_P15 | bidirectional+no_connect | `unconnected-(U4A-IO_L8P_T1_D11_14-PadP15)` | — (no other pins on this net) |
| P16 | IO_L8N_T1_D12_14_P16 | bidirectional+no_connect | `unconnected-(U4A-IO_L8N_T1_D12_14-PadP16)` | — (no other pins on this net) |
| R1 | IO_L7N_T1_34_R1 | bidirectional | `/DRIVER_FAULT_N` | R712.2, U600.4, U600.6, U601.4, U601.6, U602.4 — 10 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R2 | IO_L7P_T1_34_R2 | bidirectional+no_connect | `unconnected-(U4B-IO_L7P_T1_34-PadR2)` | — (no other pins on this net) |
| R3 | IO_L8P_T1_34_R3 | bidirectional | `/BUCK_SYNC` | C809.1 |
| R4 | VCCO_34_R4 | power_in | `+3.3V` | U4.M3, U4.T1, U4.A6, U4.B3, U4.D7, U4.E4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R5 | IO_L23P_T3_A03_D19_14_R5 | bidirectional+no_connect | `unconnected-(U4A-IO_L23P_T3_A03_D19_14-PadR5)` | — (no other pins on this net) |
| R6 | IO_L24P_T3_A01_D17_14_R6 | bidirectional+no_connect | `unconnected-(U4A-IO_L24P_T3_A01_D17_14-PadR6)` | — (no other pins on this net) |
| R7 | IO_L24N_T3_A00_D16_14_R7 | bidirectional+no_connect | `unconnected-(U4A-IO_L24N_T3_A00_D16_14-PadR7)` | — (no other pins on this net) |
| R8 | IO_L20N_T3_A07_D23_14_R8 | bidirectional+no_connect | `unconnected-(U4A-IO_L20N_T3_A07_D23_14-PadR8)` | — (no other pins on this net) |
| R9 | GND_R9 | power_in | `GND` | U4.P12, U4.T6, U4.P2, U4.T16, U4.N15, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R10 | IO_L17P_T2_A14_D30_14_R10 | bidirectional+no_connect | `unconnected-(U4A-IO_L17P_T2_A14_D30_14-PadR10)` | — (no other pins on this net) |
| R11 | IO_L17N_T2_A13_D29_14_R11 | bidirectional+no_connect | `unconnected-(U4A-IO_L17N_T2_A13_D29_14-PadR11)` | — (no other pins on this net) |
| R12 | IO_L15P_T2_DQS_RDWR_B_14_R12 | bidirectional+no_connect | `unconnected-(U4A-IO_L15P_T2_DQS_RDWR_B_14-PadR12)` | — (no other pins on this net) |
| R13 | IO_L16P_T2_CSI_B_14_R13 | bidirectional+no_connect | `unconnected-(U4A-IO_L16P_T2_CSI_B_14-PadR13)` | — (no other pins on this net) |
| R14 | VCCO_14_R14 | power_in | `+3.3V` | U4.P7, U4.T11, U4.N10, U4.M13, U4.L16, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| R15 | IO_L9P_T1_DQS_14_R15 | bidirectional+no_connect | `unconnected-(U4A-IO_L9P_T1_DQS_14-PadR15)` | — (no other pins on this net) |
| R16 | IO_L9N_T1_DQS_D13_14_R16 | bidirectional+no_connect | `unconnected-(U4A-IO_L9N_T1_DQS_D13_14-PadR16)` | — (no other pins on this net) |
| T1 | VCCO_34_T1 | power_in | `+3.3V` | U4.R4, U4.M3, U4.A6, U4.B3, U4.D7, U4.E4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| T2 | IO_L8N_T1_34_T2 | bidirectional+no_connect | `unconnected-(U4B-IO_L8N_T1_34-PadT2)` | — (no other pins on this net) |
| T3 | IO_L9N_T1_DQS_34_T3 | bidirectional+no_connect | `unconnected-(U4B-IO_L9N_T1_DQS_34-PadT3)` | — (no other pins on this net) |
| T4 | IO_L9P_T1_DQS_34_T4 | bidirectional+no_connect | `unconnected-(U4B-IO_L9P_T1_DQS_34-PadT4)` | — (no other pins on this net) |
| T5 | IO_L23N_T3_A02_D18_14_T5 | bidirectional+no_connect | `unconnected-(U4A-IO_L23N_T3_A02_D18_14-PadT5)` | — (no other pins on this net) |
| T6 | GND_T6 | power_in | `GND` | U4.T16, U4.R9, U4.P12, U4.P2, U4.N15, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| T7 | IO_L21P_T3_DQS_14_T7 | bidirectional+no_connect | `unconnected-(U4A-IO_L21P_T3_DQS_14-PadT7)` | — (no other pins on this net) |
| T8 | IO_L21N_T3_DQS_A06_D22_14_T8 | bidirectional+no_connect | `unconnected-(U4A-IO_L21N_T3_DQS_A06_D22_14-PadT8)` | — (no other pins on this net) |
| T9 | IO_L22P_T3_A05_D21_14_T9 | bidirectional+no_connect | `unconnected-(U4A-IO_L22P_T3_A05_D21_14-PadT9)` | — (no other pins on this net) |
| T10 | IO_L22N_T3_A04_D20_14_T10 | bidirectional+no_connect | `unconnected-(U4A-IO_L22N_T3_A04_D20_14-PadT10)` | — (no other pins on this net) |
| T11 | VCCO_14_T11 | power_in | `+3.3V` | U4.R14, U4.P7, U4.N10, U4.M13, U4.L16, R140.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| T12 | IO_L15N_T2_DQS_DOUT_CSO_B_14_T12 | bidirectional+no_connect | `unconnected-(U4A-IO_L15N_T2_DQS_DOUT_CSO_B_14-PadT12)` | — (no other pins on this net) |
| T13 | IO_L16N_T2_A15_D31_14_T13 | bidirectional+no_connect | `unconnected-(U4A-IO_L16N_T2_A15_D31_14-PadT13)` | — (no other pins on this net) |
| T14 | IO_L10P_T1_D14_14_T14 | bidirectional+no_connect | `unconnected-(U4A-IO_L10P_T1_D14_14-PadT14)` | — (no other pins on this net) |
| T15 | IO_L10N_T1_D15_14_T15 | bidirectional+no_connect | `unconnected-(U4A-IO_L10N_T1_D15_14-PadT15)` | — (no other pins on this net) |
| T16 | GND_T16 | power_in | `GND` | U4.T6, U4.R9, U4.P12, U4.P2, U4.N15, U4.N5 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- enable / sequencing network: R100 (33) on `CLOCK_32M768`
- gain / feedback-set resistor: R155 (0) on `/fpga/MODE0`
- gain / feedback-set resistor: R156 (0) on `/fpga/MODE1`
- gain / feedback-set resistor: R157 (0) on `/fpga/MODE2`
- pull-down resistor: R152 (0) on `/fpga/XADC_VN`
- pull-down resistor: R150 (0) on `/fpga/XADC_VNREF`
- pull-down resistor: R151 (0) on `/fpga/XADC_VP`
- pull-down resistor: R153 (0) on `/fpga/XADC_VPREF`
- pull-up resistor: R140 (4.7k) on `+3.3V`
- pull-up resistor: R141 (4.7k) on `/fpga/PUDC_N`
- series / termination resistor: R145 (33) on `/fpga/DAC_CS_SRC`
- series / termination resistor: R146 (33) on `/fpga/DAC_SCLK_SRC`
- series / termination resistor: R147 (33) on `/fpga/DAC_SDI_SRC`
- supply decoupling: C150 (100n), C151 (100n), C152 (100n), C153 (100n), C154 (100n), C155 (100n), C156 (100n), C170 (10u) (+1 more; see manifest §3.5) on `+1V0_FPGA`
- supply decoupling: C157 (100n), C158 (100n), C159 (100n), C160 (100n), C161 (100n), C171 (10u), C186 (22u / 25V X7R) on `+1V8_FPGA`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`

#### U141 — W25Q64JVSSIQ

Sheet: fpga (5) · Footprint: Package_SO:SOIC-8_5.3x5.3mm_P1.27mm · 8 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | ~{CS}_1 | input | `/fpga/QSPI_CS` | U4.L12, R140.2 |
| 2 | IO1/DO_2 | bidirectional | `/fpga/QSPI_D1` | U4.J14 |
| 3 | IO2/~{WP}_3 | bidirectional | `/fpga/QSPI_D2` | R148.2, U4.K15 |
| 4 | GND_4 | power_in | `GND` | J140.3, J140.5, J140.7, J140.9, J140.11, Y1.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 5 | IO0/DI_5 | bidirectional | `/fpga/QSPI_D0` | U4.J13 |
| 6 | CLK_6 | input | `Net-(U141-CLK)` | R790.2 |
| 7 | IO3_7 | bidirectional | `/fpga/QSPI_D3` | R149.2, U4.K16 |
| 8 | VCC_8 | power_in | `+3.3V` | J140.2, Y1.4, Y1.1, U4.L6, R148.1, R143.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- series / termination resistor: R790 (0) on `Net-(U141-CLK)`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`

#### U142 — FT231XQ

Sheet: fpga (5) · Footprint: Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm · 21 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | RXD_1 | input | `HOST_TX` | U4.N1 |
| 2 | ~{RI}_2 | input | `+3.3V` | U142.5, U142.4, U142.6, U142.20, U142.12, U142.11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 3 | GND_3 | power_in | `GND` | U142.13, U142.21, C173.2, C174.2, C145.2, C144.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 4 | ~{DSR}_4 | input | `+3.3V` | U142.5, U142.2, U142.6, U142.20, U142.12, U142.11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 5 | ~{DCD}_5 | input | `+3.3V` | U142.4, U142.2, U142.6, U142.20, U142.12, U142.11 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 6 | ~{CTS}_6 | input | `+3.3V` | U142.4, U142.5, U142.2, U142.20, U142.12, U142.10 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 7 | CBUS2_7 | bidirectional | `/fpga/VBUS_SENSE` | R158.2, R159.1 |
| 8 | USBDP_8 | bidirectional | `/fpga/FT_DP` | C173.1, R160.2 |
| 9 | USBDM_9 | bidirectional | `/fpga/FT_DM` | C174.1, R161.2 |
| 10 | 3V3OUT_10 | passive | `+3.3V` | U142.11, U142.12, U142.20, U142.6, R166.1, U142.4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 11 | ~{RESET}_11 | input | `+3.3V` | U142.10, U142.12, U142.20, U142.5, U142.4, U142.2 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 12 | VCC_12 | power_in | `+3.3V` | U142.20, U142.10, R166.1, U142.6, U142.11, U142.4 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 13 | GND_13 | power_in | `GND` | U142.21, U142.3, C173.2, C174.2, C145.2, C144.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 14 | CBUS1_14 | bidirectional+no_connect | `unconnected-(U142-CBUS1-Pad14)` | — (no other pins on this net) |
| 15 | CBUS0_15 | bidirectional+no_connect | `unconnected-(U142-CBUS0-Pad15)` | — (no other pins on this net) |
| 16 | CBUS3_16 | bidirectional+no_connect | `unconnected-(U142-CBUS3-Pad16)` | — (no other pins on this net) |
| 17 | TXD_17 | output | `HOST_RX` | U4.P1 |
| 18 | ~{DTR}_18 | output+no_connect | `unconnected-(U142-~{DTR}-Pad18)` | — (no other pins on this net) |
| 19 | ~{RTS}_19 | output+no_connect | `unconnected-(U142-~{RTS}-Pad19)` | — (no other pins on this net) |
| 20 | VCCIO_20 | power_in | `+3.3V` | U142.12, U142.6, U142.10, R166.1, U142.4, U142.5 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 21 | GND_21 | power_in | `GND` | U142.13, U142.3, C173.2, C174.2, C145.2, C144.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on `+3.3V`
- filter capacitor to ground: C174 (47p) on `/fpga/FT_DM`
- filter capacitor to ground: C173 (47p) on `/fpga/FT_DP`
- pull-down resistor: R159 (10k) on `/fpga/VBUS_SENSE`
- pull-up resistor: R154 (0), R162 (10k), R164 (10k), R166 (10k) on `+3.3V`
- series / termination resistor: R161 (27) on `/fpga/FT_DM`
- series / termination resistor: R160 (27) on `/fpga/FT_DP`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`

#### Y1 — CSX750FBC32.768M-UT

Sheet: fpga (5) · Footprint: Oscillator:Oscillator_SMD_SeikoEpson_SG8002CA-4Pin_7.0x5.0mm · 4 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | OE_1 | input | `+3.3V` | Y1.4, R143.1, R142.1, R144.1, R148.1, R149.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 2 | GND_2 | power_in | `GND` | J140.11, J140.9, J140.7, J140.5, J140.3, C140.2 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.5 |
| 3 | OUT_3 | output | `CLOCK_32M768` | U4.D13, R100.1 |
| 4 | VDD_4 | power_in | `+3.3V` | Y1.1, R143.1, R142.1, R144.1, R148.1, R149.1 — 122 ends total; full list in `brd01_wiring_manifest.md` §3.5 |

Supporting passives:

- enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on `+3.3V`
- pull-up resistor: R143 (4.7k), R148 (4.7k), R149 (4.7k) on `+3.3V`
- supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on `+3.3V`
- supply feed / filter: R100 (33) on `CLOCK_32M768`

#### C140 — 100n, C

C140 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C141 — 100n, C

C141 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C142 — 100n, C

C142 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C143 — 100n, C

C143 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C144 — 100n, C

C144 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C145 — 4.7u, C

C145 — 4.7u, C_0805_2012Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C150 — 100n, C

C150 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C151 — 100n, C

C151 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C152 — 100n, C

C152 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C153 — 100n, C

C153 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C154 — 100n, C

C154 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C155 — 100n, C

C155 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C156 — 100n, C

C156 — 100n, C_0603_1608Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C157 — 100n, C

C157 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C158 — 100n, C

C158 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C159 — 100n, C

C159 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C160 — 100n, C

C160 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C161 — 100n, C

C161 — 100n, C_0603_1608Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C162 — 100n, C

C162 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C163 — 100n, C

C163 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C164 — 100n, C

C164 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C165 — 100n, C

C165 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C166 — 100n, C

C166 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C167 — 100n, C

C167 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C168 — 100n, C

C168 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C169 — 100n, C

C169 — 100n, C_0603_1608Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C170 — 10u, C

C170 — 10u, C_0805_2012Metric — `+1V0_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U144 (pin 1 → 2).

#### C171 — 10u, C

C171 — 10u, C_0805_2012Metric — `+1V8_FPGA` ↔ `GND` — feedback filter, supply decoupling for U4, U145 (pin 1 → 2).

#### C172 — 10u, C

C172 — 10u, C_0805_2012Metric — `+3.3V` ↔ `GND` — enable / sequencing network, feedback filter, soft-start / bias capacitor, supply decoupling for J140, U4, U7, U141, U142, U751, U753, Y1 (pin 1 → 2).

#### C173 — 47p, C

C173 — 47p, C_0603_1608Metric — `/fpga/FT_DP` ↔ `GND` — filter capacitor to ground for U142 (pin 1 → 2).

#### C174 — 47p, C

C174 — 47p, C_0603_1608Metric — `/fpga/FT_DM` ↔ `GND` — filter capacitor to ground for U142 (pin 1 → 2).

#### R140 — 4.7k, R

R140 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/QSPI_CS` — pull-up resistor for U4 (pin 1 → 2).

#### R141 — 4.7k, R

R141 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/PUDC_N` — pull-up resistor for U4 (pin 1 → 2).

#### R142 — 4.7k, R

R142 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U4C-INIT_B_0)` — pull-up resistor for TP791 (pin 1 → 2).

#### R143 — 4.7k, R

R143 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U4C-DONE_0)` — pull-up resistor for Y1 (pin 1 → 2).

#### R144 — 4.7k, R

R144 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `Net-(U4C-PROGRAM_B_0)` — pull-up resistor for TP790 (pin 1 → 2).

#### R145 — 33, R

R145 — 33, R_0603_1608Metric — `/fpga/DAC_CS_SRC` ↔ `DAC_CS` — series / termination resistor for U4 (pin 1 → 2).

#### R146 — 33, R

R146 — 33, R_0603_1608Metric — `/fpga/DAC_SCLK_SRC` ↔ `DAC_SCLK` — series / termination resistor for U4 (pin 1 → 2).

#### R147 — 33, R

R147 — 33, R_0603_1608Metric — `/fpga/DAC_SDI_SRC` ↔ `DAC_SDI` — series / termination resistor for U4 (pin 1 → 2).

#### R148 — 4.7k, R

R148 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/QSPI_D2` — pull-up resistor for Y1 (pin 1 → 2).

#### R149 — 4.7k, R

R149 — 4.7k, R_0603_1608Metric — `+3.3V` ↔ `/fpga/QSPI_D3` — pull-up resistor for Y1 (pin 1 → 2).

#### R150 — 0, R

R150 — 0, R_0603_1608Metric — `/fpga/XADC_VNREF` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R151 — 0, R

R151 — 0, R_0603_1608Metric — `/fpga/XADC_VP` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R152 — 0, R

R152 — 0, R_0603_1608Metric — `/fpga/XADC_VN` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R153 — 0, R

R153 — 0, R_0603_1608Metric — `/fpga/XADC_VPREF` ↔ `GND` — pull-down resistor for U4 (pin 1 → 2).

#### R154 — 0, R

R154 — 0, R_0603_1608Metric — `+3.3V` ↔ `/fpga/CFGBVS` — pull-up resistor for U142 (pin 1 → 2).

#### R155 — 0, R

R155 — 0, R_0603_1608Metric — `+3.3V` ↔ `/fpga/MODE0` — gain / feedback-set resistor for U4 (pin 1 → 2).

#### R156 — 0, R

R156 — 0, R_0603_1608Metric — `GND` ↔ `/fpga/MODE1` — gain / feedback-set resistor for U4 (pin 1 → 2).

#### R157 — 0, R

R157 — 0, R_0603_1608Metric — `GND` ↔ `/fpga/MODE2` — gain / feedback-set resistor for U4 (pin 1 → 2).

#### R158 — 4.7k, R

R158 — 4.7k, R_0603_1608Metric — `USB_VBUS` ↔ `/fpga/VBUS_SENSE` — supply feed / filter for J124 (pin 1 → 2).

#### R159 — 10k, R

R159 — 10k, R_0603_1608Metric — `/fpga/VBUS_SENSE` ↔ `GND` — pull-down resistor for U142 (pin 1 → 2).

#### R160 — 27, R

R160 — 27, R_0603_1608Metric — `USB_DP` ↔ `/fpga/FT_DP` — series / termination resistor for U142 (pin 1 → 2).

#### R161 — 27, R

R161 — 27, R_0603_1608Metric — `USB_DM` ↔ `/fpga/FT_DM` — series / termination resistor for U142 (pin 1 → 2).

#### R162 — 10k, R

R162 — 10k, R_0603_1608Metric — `+3.3V` ↔ `DAC_CS` — pull-up resistor for U142 (pin 1 → 2).

#### R163 — 10k, R

R163 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_RESET_N` — enable pull-up for U101 (pin 1 → 2).

#### R164 — 10k, R

R164 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_CS` — pull-up resistor for U142 (pin 1 → 2).

#### R165 — 10k, R

R165 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_START_N` — enable pull-up for U101 (pin 1 → 2).

#### R166 — 10k, R

R166 — 10k, R_0603_1608Metric — `+3.3V` ↔ `ADC_SYNC_IN` — pull-up resistor for U142 (pin 1 → 2).

#### R790 — 0, R

R790 — 0, R_0603_1608Metric — `Net-(U4C-CCLK_0)` ↔ `Net-(U141-CLK)` — series / termination resistor for U141 (pin 1 → 2).

### 4.6 Page 6 — connectors

Net-centric counterpart: `brd01_wiring_manifest.md` §3.6. 23 components on this sheet.

#### Components

#### J20 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG0_OUT` | C212.2, TP821.1 |
| 2 | Pin_2_2 | passive | `FG0_RETURN` | R20.1, R400.1, TP822.1 |

#### J21 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG1_OUT` | C220.2 |
| 2 | Pin_2_2 | passive | `FG1_RETURN` | R21.1, R410.1 |

#### J22 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG2_OUT` | C228.2 |
| 2 | Pin_2_2 | passive | `FG2_RETURN` | R22.1, R420.1 |

#### J23 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG3_OUT` | C236.2 |
| 2 | Pin_2_2 | passive | `FG3_RETURN` | R23.1, R430.1 |

#### J24 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG4_OUT` | C244.2 |
| 2 | Pin_2_2 | passive | `FG4_RETURN` | R24.1, R440.1 |

#### J25 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG5_OUT` | C252.2 |
| 2 | Pin_2_2 | passive | `FG5_RETURN` | R25.1, R450.1 |

#### J26 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG6_OUT` | C260.2 |
| 2 | Pin_2_2 | passive | `FG6_RETURN` | R26.1, R460.1 |

#### J27 — 39-30-1020, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `FG7_OUT` | C268.2 |
| 2 | Pin_2_2 | passive | `FG7_RETURN` | R27.1, R470.1 |

#### J120 — IO-TXLR3-M-PS-1

Sheet: connectors (6) · Footprint: — · 4 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | SHIELD_1 | passive | `/connectors/CHASSIS` | J120.SH, J125.1, J125.SH, R185.1, C191.1, J124.SH |
| 2 | CONTACT_2_2 | passive | `/connectors/PEN1_PANEL_P` | J121.1 |
| 3 | CONTACT_3_3 | passive | `/connectors/PEN1_PANEL_N` | J121.2 |
| SH | SHELL_SH | passive | `/connectors/CHASSIS` | J120.1, J125.1, J125.SH, R185.1, C191.1, J124.SH |

Supporting passives:

- supply decoupling: C191 (1n / 50V X7R) on `/connectors/CHASSIS`
- supply return: R185 (1M) on `/connectors/CHASSIS`

#### J121 — JST PHR-2 harness plug, Conn_01x02

Sheet: connectors (6) · Footprint: — · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `/connectors/PEN1_PANEL_P` | J120.2 |
| 2 | Pin_2_2 | passive | `/connectors/PEN1_PANEL_N` | J120.3 |

#### J122 — B2B-PH-K-S, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `PEN1_P` | R101.1 |
| 2 | Pin_2_2 | passive | `PEN1_N` | R102.1 |

#### J123 — BM06B-GHS-TBT, Conn_01x06

Sheet: connectors (6) · Footprint: Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical · 6 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive+no_connect | `unconnected-(J123-Pin_1-Pad1)` | — (no other pins on this net) |
| 2 | Pin_2_2 | passive | `GND` | R185.2, C191.2, J124.A1, J124.A12, J124.B1, J124.B12 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |
| 3 | Pin_3_3 | passive | `PICO_TX` | U4.N2 |
| 4 | Pin_4_4 | passive | `PICO_RX` | U4.N3 |
| 5 | Pin_5_5 | passive | `PICO_STOP_N` | R753.1, U755.4 |
| 6 | Pin_6_6 | passive | `PICO_HEARTBEAT` | U4.P3 |

#### J124 — USB4110-GF-A, USB_C_Receptacle_USB2.0_16P

Sheet: connectors (6) · Footprint: Connector_USB:USB_C_Receptacle_GCT_USB4110 · 17 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| A1 | GND_A1 | passive | `GND` | J124.A12, J124.B1, J124.B12, R183.2, R182.2, D750.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |
| A4 | VBUS_A4 | passive | `USB_VBUS` | J124.A9, J124.B4, J124.B9, R158.1 |
| A5 | CC1_A5 | bidirectional | `/connectors/USB_CC1` | R182.1, D751.1 |
| A6 | D+_A6 | bidirectional | `USB_DP` | J124.B6, D750.1, R160.1 |
| A7 | D-_A7 | bidirectional | `USB_DM` | J124.B7, D750.2, R161.1 |
| A8 | SBU1_A8 | bidirectional+no_connect | `unconnected-(J124-SBU1-PadA8)` | — (no other pins on this net) |
| A9 | VBUS_A9 | passive | `USB_VBUS` | J124.A4, J124.B4, J124.B9, R158.1 |
| A12 | GND_A12 | passive | `GND` | J124.A1, J124.B1, J124.B12, R183.2, R182.2, D750.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |
| B1 | GND_B1 | passive | `GND` | J124.A1, J124.A12, J124.B12, R183.2, R182.2, D750.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |
| B4 | VBUS_B4 | passive | `USB_VBUS` | J124.A4, J124.A9, J124.B9, R158.1 |
| B5 | CC2_B5 | bidirectional | `/connectors/USB_CC2` | R183.1, D751.2 |
| B6 | D+_B6 | bidirectional | `USB_DP` | J124.A6, D750.1, R160.1 |
| B7 | D-_B7 | bidirectional | `USB_DM` | J124.A7, D750.2, R161.1 |
| B8 | SBU2_B8 | bidirectional+no_connect | `unconnected-(J124-SBU2-PadB8)` | — (no other pins on this net) |
| B9 | VBUS_B9 | passive | `USB_VBUS` | J124.A4, J124.A9, J124.B4, R158.1 |
| B12 | GND_B12 | passive | `GND` | J124.A1, J124.A12, J124.B1, R183.2, R182.2, D750.3 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |
| SH | SHIELD_SH | passive | `/connectors/CHASSIS` | C191.1, R185.1, J125.1, J125.SH, J120.SH, J120.1 |

Supporting passives:

- supply decoupling: C191 (1n / 50V X7R) on `/connectors/CHASSIS`
- supply feed / filter: R158 (4.7k) on `USB_VBUS`
- supply return: R185 (1M) on `/connectors/CHASSIS`

#### J125 — IO-TXLR3-M-PS-1

Sheet: connectors (6) · Footprint: — · 4 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | SHIELD_1 | passive | `/connectors/CHASSIS` | J125.SH, R185.1, C191.1, J120.SH, J120.1, J124.SH |
| 2 | CONTACT_2_2 | passive | `/connectors/PEN2_PANEL_P` | J126.1 |
| 3 | CONTACT_3_3 | passive | `/connectors/PEN2_PANEL_N` | J126.2 |
| SH | SHELL_SH | passive | `/connectors/CHASSIS` | J125.1, R185.1, C191.1, J120.SH, J124.SH, J120.1 |

Supporting passives:

- supply decoupling: C191 (1n / 50V X7R) on `/connectors/CHASSIS`
- supply return: R185 (1M) on `/connectors/CHASSIS`

#### J126 — JST PHR-2 harness plug, Conn_01x02

Sheet: connectors (6) · Footprint: — · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `/connectors/PEN2_PANEL_P` | J125.2 |
| 2 | Pin_2_2 | passive | `/connectors/PEN2_PANEL_N` | J125.3 |

#### J127 — B2B-PH-K-S, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `PEN2_P` | R540.1 |
| 2 | Pin_2_2 | passive | `PEN2_N` | R541.1 |

#### J128 — BM02B-GHS-TBT, Conn_01x02

Sheet: connectors (6) · Footprint: Connector_JST:JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical · 2 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | Pin_1_1 | passive | `REF_COIL_P` | R560.1 |
| 2 | Pin_2_2 | passive | `REF_COIL_N` | R561.1 |

#### D750 — TPD2EUSB30DRTR, TPD2EUSB30

Sheet: connectors (6) · Footprint: Package_TO_SOT_SMD:Texas_DRT-3 · 3 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | D+_1 | passive | `USB_DP` | J124.B6, J124.A6, R160.1 |
| 2 | D-_2 | passive | `USB_DM` | J124.B7, J124.A7, R161.1 |
| 3 | GND_3 | passive | `GND` | R183.2, D751.3, R182.2, J124.A1, J124.A12, J124.B1 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |

#### D751 — TPD2EUSB30DRTR, TPD2EUSB30

Sheet: connectors (6) · Footprint: Package_TO_SOT_SMD:Texas_DRT-3 · 3 pins

| Pin | Name | Type | Net | Connects to |
|---|---|---|---|---|
| 1 | D+_1 | passive | `/connectors/USB_CC1` | R182.1, J124.A5 |
| 2 | D-_2 | passive | `/connectors/USB_CC2` | R183.1, J124.B5 |
| 3 | GND_3 | passive | `GND` | R183.2, R182.2, D750.3, J124.A1, J124.A12, J124.B1 — 442 ends total; full list in `brd01_wiring_manifest.md` §3.6 |

Supporting passives:

- pull-down resistor: R182 (5.1k) on `/connectors/USB_CC1`
- pull-down resistor: R183 (5.1k) on `GND`

#### C191 — 1n / 50V X7R, C

C191 — 1n / 50V X7R, C_0603_1608Metric — `/connectors/CHASSIS` ↔ `GND` — supply decoupling for J120, J124, J125 (pin 1 → 2).

#### R182 — 5.1k, R

R182 — 5.1k, R_0603_1608Metric — `/connectors/USB_CC1` ↔ `GND` — pull-down resistor for D751 (pin 1 → 2).

#### R183 — 5.1k, R

R183 — 5.1k, R_0603_1608Metric — `/connectors/USB_CC2` ↔ `GND` — pull-down resistor for D751 (pin 1 → 2).

#### R185 — 1M, R

R185 — 1M, R_0603_1608Metric — `/connectors/CHASSIS` ↔ `GND` — supply return for J120, J124, J125 (pin 1 → 2).

## 5. Per-sheet support summary

Page 1 — root has no components, so no support rows.

Component → the passives that exist to serve it. `—` means no R/C/L was found by either rule on that sheet. Counts are per component, not per net.

### 5.2 power

| Component | Passives that serve it |
|---|---|
| F1 | input / output filter capacitor: L1 (7448225007) on Net-(F1-Pad2) |
| J1 | — |
| J750 | — |
| SW750 | pull-up resistor: R751 (10k) on Net-(R751-Pad2); series / termination resistor: R752 (1k) on Net-(R751-Pad2) |
| TP760 | — |
| TP761 | — |
| TP762 | — |
| TP763 | — |
| U2 | gain / feedback-set resistor: R2 (7.5k) on Net-(U2-ILIM); gain / feedback-set resistor: R1 (121k) on Net-(U2-SET); supply decoupling: C4 (4.7u), C783 (10u / 25V) on -12VA; supply decoupling: C781 (10u / 35V) on -15V; timing / set capacitor: C3 (4.7u) on Net-(U2-SET) |
| U5 | supply decoupling: C780 (10u / 35V) on +15V; supply decoupling: C30 (EEUFR1V102), C800 (10u / 50V X7R), C801 (10u / 50V X7R), C802 (100n / 50V), C803 (100n / 50V), C804 (EEU-FR1V680 68u / 35V) on +15V_FUSED; supply decoupling: C781 (10u / 35V) on -15V |
| U6 | gain / feedback-set resistor: R4 (750) on Net-(U6-ILIM); gain / feedback-set resistor: R3 (121k) on Net-(U6-SET); supply decoupling: C5 (10u), C782 (22u / 25V) on +12VA; supply decoupling: C780 (10u / 35V) on +15V; timing / set capacitor: C6 (4.7u) on Net-(U6-SET) |
| U7 | enable pull-up: R195 (100k) on /power/PG_1V8; feedback divider: R806 (619k), R807 (200k) on Net-(U7-FB); feedback filter: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+27 more; see manifest §3.2) on +3.3V; soft-start / bias capacitor: C814 (3.3n) on Net-(U7-SS/TR); supply bulk / feed: L800 (XFL4020-222MEC) on Net-(L800-Pad1); supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on +6V |
| U144 | enable pull-up: R805 (100k) on /power/PG_6V; feedback divider: R190 (49.9k), R191 (200k) on /power/BUCK1_FB; feedback filter: C150 (100n), C151 (100n), C152 (100n), C153 (100n), C154 (100n), C155 (100n), C156 (100n), C170 (10u) (+1 more; see manifest §3.2) on +1V0_FPGA; gain / feedback-set resistor: R192 (100k) on /power/PG_1V0; soft-start / bias capacitor: C181 (3.3n) on Net-(U144-SS/TR); supply bulk / feed: L140 (XFL4020-222MEC) on Net-(L140-Pad1); supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on +6V |
| U145 | enable pull-up: R192 (100k) on /power/PG_1V0; feedback divider: R193 (249k), R194 (200k) on Net-(U145-FB); feedback filter: C157 (100n), C158 (100n), C159 (100n), C160 (100n), C161 (100n), C171 (10u), C186 (22u / 25V X7R) on +1V8_FPGA; soft-start / bias capacitor: C185 (3.3n) on Net-(U145-SS/TR); supply bulk / feed: L141 (XFL4020-222MEC) on Net-(L141-Pad1); supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on +6V |
| U146 | feedback filter: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.2) on +5VA; filter capacitor to ground: C820 (10u / 16V X7R) on GND; soft-start / bias capacitor: C189 (1u / 16V X7R) on Net-(U146-NR); supply bulk / feed: L802 (XFL4020-102MEC 1u) on Net-(U146-EN); supply decoupling: C190 (47u / 16V X7R) on +5VA; supply decoupling: C188 (2.2u / 16V X7R) on Net-(U146-EN); supply feed / filter: R809 (0.68) on Net-(U146-EN) |
| U147 | enable / sequencing network: C809 (1n) on Net-(U147-EN/SYNC); enable pull-down: R804 (118k) on Net-(U147-EN/SYNC); enable pull-up: R803 (1.00M) on Net-(U147-EN/SYNC); feedback divider: R800 (49.9k 0.1%), R801 (10.0k 0.1%) on Net-(U147-FB); feedback filter: C805 (18p C0G) on Net-(U147-FB); gain / feedback-set resistor: R802 (13.0k 1%) on Net-(U147-RT); supply decoupling: C180 (10u / 25V), C183 (100n), C184 (10u / 25V), C187 (100n), C806 (22u / 25V X7R), C807 (22u / 25V X7R), C808 (22u / 25V X7R), C810 (1u / 16V) (+2 more; see manifest §3.2) on +6V; supply decoupling: C30 (EEUFR1V102), C800 (10u / 50V X7R), C801 (10u / 50V X7R), C802 (100n / 50V), C803 (100n / 50V), C804 (EEU-FR1V680 68u / 35V) on +15V_FUSED |
| U149 | feedback filter: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.2) on +5V_EXC; filter capacitor to ground: C818 (10u / 16V X7R) on GND; soft-start / bias capacitor: C815 (1u / 16V X7R) on Net-(U149-NR); supply bulk / feed: L801 (XFL4020-102MEC 1u) on Net-(U149-EN); supply decoupling: C816 (47u / 16V X7R) on +5V_EXC; supply decoupling: C817 (2.2u / 16V X7R) on Net-(U149-EN); supply feed / filter: R808 (0.68) on Net-(U149-EN) |
| U751 | enable pull-up: R750 (10k) on Net-(U751-~{RESET}); feedback filter: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+21 more; see manifest §3.2) on +3.3V; supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on +3.3V |
| U752 | supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on +3.3V |
| U753 | enable / sequencing network: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+21 more; see manifest §3.2) on +3.3V; supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on +3.3V |
| U754 | filter capacitor to ground: C755 (100n) on Net-(C755-Pad1); supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on +3.3V |
| U755 | pull-down resistor: R753 (100k) on PICO_STOP_N; pull-down resistor: R754 (100k) on PICO_STOP_REQ_N; supply decoupling: C750 (100n), C751 (100n), C752 (100n), C753 (100n), C754 (100n), C813 (22u / 25V X7R) on +3.3V |
| Q760 | filter capacitor to ground: C770 (1u / 50V) on Net-(D760-K); pull-down resistor: R770 (10k) on Net-(D760-A) |
| D1 | — |
| D760 | input / output filter capacitor: L760 (7447714047) on Net-(D760-K) |
| L1 | — |

### 5.3 driver

| Component | Passives that serve it |
|---|---|
| TP200 | — |
| TP201 | — |
| TP202 | — |
| TP203 | — |
| TP210 | — |
| TP211 | — |
| TP212 | — |
| TP213 | — |
| TP214 | — |
| TP215 | — |
| TP216 | — |
| TP217 | — |
| TP820 | — |
| TP821 | — |
| TP822 | — |
| TP823 | filter capacitor to ground: C283 (100n) on /driver/VMID_7V5; pull-down resistor: R383 (10k) on /driver/VMID_7V5; pull-up resistor: R382 (10k) on /driver/VMID_7V5; series / termination resistor: R20 (1.00 0.1% 0.5W), R21 (1.00 0.1% 0.5W), R22 (1.00 0.1% 0.5W), R23 (1.00 0.1% 0.5W), R24 (1.00 0.1% 0.5W), R25 (1.00 0.1% 0.5W), R26 (1.00 0.1% 0.5W), R27 (1.00 0.1% 0.5W) on /driver/VMID_7V5 |
| U10 | soft-start / bias capacitor: C203 (150n) on /driver/DAC_REF; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply feed / filter: R220 (42.7k 0.1%) on /driver/DAC0; supply feed / filter: R230 (42.7k 0.1%) on /driver/DAC1; supply feed / filter: R240 (42.7k 0.1%) on /driver/DAC2; supply feed / filter: R250 (42.7k 0.1%) on /driver/DAC3; supply feed / filter: R260 (42.7k 0.1%) on /driver/DAC4; supply feed / filter: R270 (42.7k 0.1%) on /driver/DAC5; supply feed / filter: R280 (42.7k 0.1%) on /driver/DAC6; supply feed / filter: R290 (42.7k 0.1%) on /driver/DAC7 |
| U20 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-down resistor: R381 (10k) on GND; pull-up resistor: R380 (10k), R600 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C212 (CAA572X7R1E107M670LJ) on /driver/BUF0 |
| U21 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R601 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C220 (CAA572X7R1E107M670LJ) on /driver/BUF1 |
| U22 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R602 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C228 (CAA572X7R1E107M670LJ) on /driver/BUF2 |
| U23 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R603 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C236 (CAA572X7R1E107M670LJ) on /driver/BUF3 |
| U24 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R604 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C244 (CAA572X7R1E107M670LJ) on /driver/BUF4 |
| U25 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R605 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C252 (CAA572X7R1E107M670LJ) on /driver/BUF5 |
| U26 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R606 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C260 (CAA572X7R1E107M670LJ) on /driver/BUF6 |
| U27 | bias / reference network: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID; pull-up resistor: R607 (10.7k 1%) on +15V_FUSED; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: C268 (CAA572X7R1E107M670LJ) on /driver/BUF7 |
| U30 | input / output filter capacitor: C622 (150p) on /driver/FEEDBACK0; series / termination resistor: R620 (10k) on /driver/CMD_BIASED0; series / termination resistor: R360 (10k) on /driver/FEEDBACK0; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R361 (15k), R622 (10M), R623 (330k) on /driver/ERR0 |
| U31 | input / output filter capacitor: C632 (150p) on /driver/FEEDBACK1; series / termination resistor: R630 (10k) on /driver/CMD_BIASED1; series / termination resistor: R362 (10k) on /driver/FEEDBACK1; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R363 (15k), R632 (10M), R633 (330k) on /driver/ERR1 |
| U32 | input / output filter capacitor: C642 (150p) on /driver/FEEDBACK2; series / termination resistor: R640 (10k) on /driver/CMD_BIASED2; series / termination resistor: R364 (10k) on /driver/FEEDBACK2; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R365 (15k), R642 (10M), R643 (330k) on /driver/ERR2 |
| U33 | input / output filter capacitor: C652 (150p) on /driver/FEEDBACK3; series / termination resistor: R650 (10k) on /driver/CMD_BIASED3; series / termination resistor: R366 (10k) on /driver/FEEDBACK3; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R367 (15k), R652 (10M), R653 (330k) on /driver/ERR3 |
| U34 | input / output filter capacitor: C662 (150p) on /driver/FEEDBACK4; series / termination resistor: R660 (10k) on /driver/CMD_BIASED4; series / termination resistor: R368 (10k) on /driver/FEEDBACK4; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R369 (15k), R662 (10M), R663 (330k) on /driver/ERR4 |
| U35 | input / output filter capacitor: C672 (150p) on /driver/FEEDBACK5; series / termination resistor: R670 (10k) on /driver/CMD_BIASED5; series / termination resistor: R370 (10k) on /driver/FEEDBACK5; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R371 (15k), R672 (10M), R673 (330k) on /driver/ERR5 |
| U36 | input / output filter capacitor: C682 (150p) on /driver/FEEDBACK6; series / termination resistor: R680 (10k) on /driver/CMD_BIASED6; series / termination resistor: R372 (10k) on /driver/FEEDBACK6; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R373 (15k), R682 (10M), R683 (330k) on /driver/ERR6 |
| U37 | input / output filter capacitor: C692 (150p) on /driver/FEEDBACK7; series / termination resistor: R690 (10k) on /driver/CMD_BIASED7; series / termination resistor: R374 (10k) on /driver/FEEDBACK7; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R375 (15k), R692 (10M), R693 (330k) on /driver/ERR7 |
| U38 | series / termination resistor: R201 (10k 0.1%), R202 (10k 0.1%), R203 (10k 0.1%), R204 (10k 0.1%), R205 (10k 0.1%), R206 (10k 0.1%), R207 (10k 0.1%), R208 (10k 0.1%) on /driver/SUM_NODE; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA; supply feed / filter: R200 (20k 0.1%) on CURRENT_SUM |
| U39 | filter capacitor to ground: C281 (100n) on /driver/BIAS_DIV; supply decoupling: C213 (100n), C221 (100n), C229 (100n), C237 (100n), C245 (100n), C253 (100n), C261 (100n), C269 (100n) (+1 more; see manifest §3.3) on +15V_FUSED; supply feed / filter: R621 (1.40k), R631 (1.40k), R641 (1.40k), R651 (1.40k), R661 (1.40k), R671 (1.40k), R681 (1.40k), R691 (1.40k) on /driver/BUFFER_VMID |
| U40 | input / output filter capacitor: C621 (100n) on /driver/I_SENSE0; input / output filter capacitor: C631 (100n) on /driver/I_SENSE1; pull-down resistor: R401 (10k 0.1%) on /driver/SENSE_P0; pull-down resistor: R411 (10k 0.1%) on /driver/SENSE_P1; series / termination resistor: R403 (10k 0.1%) on /driver/I_SENSE0; series / termination resistor: R413 (10k 0.1%) on /driver/I_SENSE1; series / termination resistor: R402 (10k 0.1%) on /driver/SENSE_N0; series / termination resistor: R412 (10k 0.1%) on /driver/SENSE_N1; series / termination resistor: R400 (10k 0.1%) on /driver/SENSE_P0; series / termination resistor: R410 (10k 0.1%) on /driver/SENSE_P1; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U41 | input / output filter capacitor: C641 (100n) on /driver/I_SENSE2; input / output filter capacitor: C651 (100n) on /driver/I_SENSE3; pull-down resistor: R421 (10k 0.1%) on /driver/SENSE_P2; pull-down resistor: R431 (10k 0.1%) on /driver/SENSE_P3; series / termination resistor: R423 (10k 0.1%) on /driver/I_SENSE2; series / termination resistor: R433 (10k 0.1%) on /driver/I_SENSE3; series / termination resistor: R422 (10k 0.1%) on /driver/SENSE_N2; series / termination resistor: R432 (10k 0.1%) on /driver/SENSE_N3; series / termination resistor: R420 (10k 0.1%) on /driver/SENSE_P2; series / termination resistor: R430 (10k 0.1%) on /driver/SENSE_P3; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U42 | input / output filter capacitor: C661 (100n) on /driver/I_SENSE4; input / output filter capacitor: C671 (100n) on /driver/I_SENSE5; pull-down resistor: R441 (10k 0.1%) on /driver/SENSE_P4; pull-down resistor: R451 (10k 0.1%) on /driver/SENSE_P5; series / termination resistor: R443 (10k 0.1%) on /driver/I_SENSE4; series / termination resistor: R453 (10k 0.1%) on /driver/I_SENSE5; series / termination resistor: R442 (10k 0.1%) on /driver/SENSE_N4; series / termination resistor: R452 (10k 0.1%) on /driver/SENSE_N5; series / termination resistor: R440 (10k 0.1%) on /driver/SENSE_P4; series / termination resistor: R450 (10k 0.1%) on /driver/SENSE_P5; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U43 | input / output filter capacitor: C681 (100n) on /driver/I_SENSE6; input / output filter capacitor: C691 (100n) on /driver/I_SENSE7; pull-down resistor: R461 (10k 0.1%) on /driver/SENSE_P6; pull-down resistor: R471 (10k 0.1%) on /driver/SENSE_P7; series / termination resistor: R463 (10k 0.1%) on /driver/I_SENSE6; series / termination resistor: R473 (10k 0.1%) on /driver/I_SENSE7; series / termination resistor: R462 (10k 0.1%) on /driver/SENSE_N6; series / termination resistor: R472 (10k 0.1%) on /driver/SENSE_N7; series / termination resistor: R460 (10k 0.1%) on /driver/SENSE_P6; series / termination resistor: R470 (10k 0.1%) on /driver/SENSE_P7; supply decoupling: C204 (100n), C214 (100n), C222 (100n), C230 (100n), C238 (100n), C246 (100n), C254 (100n), C262 (100n) (+5 more; see manifest §3.3) on +12VA; supply decoupling: C205 (100n), C215 (100n), C223 (100n), C231 (100n), C239 (100n), C247 (100n), C255 (100n), C263 (100n) (+5 more; see manifest §3.3) on -12VA |
| U60 | pull-up resistor: R729 (100k 0.1%) on +3.3V; pull-up resistor: R721 (100k 0.1%) on /driver/TRIP_SENSE0; series / termination resistor: R720 (10k 0.1%) on /driver/TRIP_SENSE0; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U61 | series / termination resistor: R722 (10k 0.1%) on /driver/TRIP_SENSE1; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U62 | pull-down resistor: R711 (10k 0.1%) on /driver/TRIP_REF; pull-up resistor: R723 (100k 0.1%), R731 (100k 0.1%) on +3.3V; pull-up resistor: R710 (52.3k 0.1%) on /driver/TRIP_REF; series / termination resistor: R724 (10k 0.1%) on /driver/TRIP_SENSE2; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U63 | series / termination resistor: R726 (10k 0.1%) on /driver/TRIP_SENSE3; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U64 | pull-up resistor: R725 (100k 0.1%), R733 (100k 0.1%) on +3.3V; series / termination resistor: R728 (10k 0.1%) on /driver/TRIP_SENSE4; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U65 | series / termination resistor: R730 (10k 0.1%) on /driver/TRIP_SENSE5; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U66 | filter capacitor to ground: C710 (100n) on /driver/TRIP_REF; pull-up resistor: R727 (100k 0.1%), R735 (100k 0.1%) on +3.3V; series / termination resistor: R732 (10k 0.1%) on /driver/TRIP_SENSE6; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U67 | series / termination resistor: R734 (10k 0.1%) on /driver/TRIP_SENSE7; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U80 | input / output filter capacitor: C620 (1u) on /driver/FILTER0; series / termination resistor: R224 (42.7k 0.1%) on /driver/FILTER0; series / termination resistor: R222 (42.7k 0.1%) on /driver/INVA0; series / termination resistor: R225 (42.7k 0.1%) on /driver/INVB0; series / termination resistor: R221 (42.7k 0.1%), R223 (42.7k 0.1%) on /driver/LPA0; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C211 (100n) on /driver/AGND0 |
| U81 | filter capacitor to ground: C282 (EEUFR1E102) on GND; input / output filter capacitor: C630 (1u) on /driver/FILTER1; series / termination resistor: R234 (42.7k 0.1%) on /driver/FILTER1; series / termination resistor: R232 (42.7k 0.1%) on /driver/INVA1; series / termination resistor: R235 (42.7k 0.1%) on /driver/INVB1; series / termination resistor: R231 (42.7k 0.1%), R233 (42.7k 0.1%) on /driver/LPA1; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C219 (100n) on /driver/AGND1 |
| U82 | input / output filter capacitor: C640 (1u) on /driver/FILTER2; series / termination resistor: R244 (42.7k 0.1%) on /driver/FILTER2; series / termination resistor: R242 (42.7k 0.1%) on /driver/INVA2; series / termination resistor: R245 (42.7k 0.1%) on /driver/INVB2; series / termination resistor: R241 (42.7k 0.1%), R243 (42.7k 0.1%) on /driver/LPA2; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C227 (100n) on /driver/AGND2 |
| U83 | input / output filter capacitor: C650 (1u) on /driver/FILTER3; series / termination resistor: R254 (42.7k 0.1%) on /driver/FILTER3; series / termination resistor: R252 (42.7k 0.1%) on /driver/INVA3; series / termination resistor: R255 (42.7k 0.1%) on /driver/INVB3; series / termination resistor: R251 (42.7k 0.1%), R253 (42.7k 0.1%) on /driver/LPA3; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C235 (100n) on /driver/AGND3 |
| U84 | input / output filter capacitor: C660 (1u) on /driver/FILTER4; series / termination resistor: R264 (42.7k 0.1%) on /driver/FILTER4; series / termination resistor: R262 (42.7k 0.1%) on /driver/INVA4; series / termination resistor: R265 (42.7k 0.1%) on /driver/INVB4; series / termination resistor: R261 (42.7k 0.1%), R263 (42.7k 0.1%) on /driver/LPA4; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C243 (100n) on /driver/AGND4 |
| U85 | input / output filter capacitor: C670 (1u) on /driver/FILTER5; series / termination resistor: R274 (42.7k 0.1%) on /driver/FILTER5; series / termination resistor: R272 (42.7k 0.1%) on /driver/INVA5; series / termination resistor: R275 (42.7k 0.1%) on /driver/INVB5; series / termination resistor: R271 (42.7k 0.1%), R273 (42.7k 0.1%) on /driver/LPA5; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C251 (100n) on /driver/AGND5 |
| U86 | input / output filter capacitor: C680 (1u) on /driver/FILTER6; series / termination resistor: R284 (42.7k 0.1%) on /driver/FILTER6; series / termination resistor: R282 (42.7k 0.1%) on /driver/INVA6; series / termination resistor: R285 (42.7k 0.1%) on /driver/INVB6; series / termination resistor: R281 (42.7k 0.1%), R283 (42.7k 0.1%) on /driver/LPA6; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C259 (100n) on /driver/AGND6 |
| U87 | input / output filter capacitor: C690 (1u) on /driver/FILTER7; series / termination resistor: R294 (42.7k 0.1%) on /driver/FILTER7; series / termination resistor: R292 (42.7k 0.1%) on /driver/INVA7; series / termination resistor: R295 (42.7k 0.1%) on /driver/INVB7; series / termination resistor: R291 (42.7k 0.1%), R293 (42.7k 0.1%) on /driver/LPA7; supply decoupling: C200 (100n), C201 (1u), C210 (100n), C218 (100n), C226 (100n), C234 (100n), C242 (100n), C250 (100n) (+2 more; see manifest §3.3) on +5V_EXC; supply decoupling: C267 (100n) on /driver/AGND7 |
| U600 | supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U601 | pull-up resistor: R712 (4.7k) on /DRIVER_FAULT_N; supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U602 | supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |
| U603 | supply decoupling: C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n), C296 (100n) (+5 more; see manifest §3.3) on +3.3V |

### 5.4 receiver

| Component | Passives that serve it |
|---|---|
| U101 | enable pull-up: R163 (10k) on ADC_RESET_N; enable pull-up: R165 (10k) on ADC_START_N; filter capacitor to ground: C544 (470p), C545 (470p), C564 (470p), C565 (470p) on GND; input / output filter capacitor: C122 (100p) on /receiver/AIN0-; input / output filter capacitor: C127 (100p) on /receiver/AIN1-; input / output filter capacitor: C546 (100p) on /receiver/AIN2-; input / output filter capacitor: C566 (100p) on /receiver/AIN3-; pull-down resistor: R181 (10k) on /receiver/ADC_DAISY_IN; pull-up resistor: R180 (10k) on /receiver/ADC_SPI_STRAP; soft-start / bias capacitor: C106 (100n) on /receiver/ADC_VCM; soft-start / bias capacitor: C103 (10u) on /receiver/DREGCAP; soft-start / bias capacitor: C104 (1u) on /receiver/REGCAPA; soft-start / bias capacitor: C105 (1u) on /receiver/REGCAPB; supply decoupling: C111 (100n) on +3.3V; supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on +5VA |
| U102 | filter capacitor to ground: C101 (10u), C102 (100n), C120 (470p), C121 (470p) on GND; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C131 (100n) on /receiver/REF_RAW |
| U103 | supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply feed / filter: R184 (10) on /receiver/REF_BUF_OUT |
| U104 | pull-down resistor: R103 (10k 0.1%) on /receiver/INA_IN_P; pull-down resistor: R104 (10k 0.1%), R111 (1k), R121 (499) on GND; series / termination resistor: R105 (176) on /receiver/GAIN2; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C116 (100n), C543 (100n), C563 (100n) on -12VA |
| U105 | enable / sequencing network: C190 (47u / 16V X7R) on +5VA; feedback divider: R115 (20) on /receiver/FDA0_OUT_N; feedback divider: R113 (1k), R114 (20) on /receiver/FDA0_OUT_P; feedback divider: R125 (20) on /receiver/FDA1_OUT_N; feedback divider: R123 (1k), R124 (20) on /receiver/FDA1_OUT_P; soft-start / bias capacitor: C106 (100n) on /receiver/ADC_VCM; supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on +5VA; supply feed / filter: R110 (1k), R112 (1k) on Net-(U105A-+IN1); supply feed / filter: R120 (499), R122 (1k) on Net-(U105B-+IN2) |
| U106 | pull-down resistor: R543 (10k 0.1%) on /receiver/PEN2_IN_N; pull-down resistor: R542 (10k 0.1%) on /receiver/PEN2_IN_P; pull-down resistor: R549 (499) on GND; series / termination resistor: R544 (176) on /receiver/PEN2_RG2; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C116 (100n), C543 (100n), C563 (100n) on -12VA |
| U107 | pull-down resistor: R563 (10k 0.1%) on /receiver/REF_COIL_IN_N; pull-down resistor: R562 (10k 0.1%) on /receiver/REF_COIL_IN_P; pull-down resistor: R569 (499) on GND; series / termination resistor: R564 (176) on /receiver/REF_COIL_RG2; supply decoupling: C100 (100n), C115 (100n), C130 (100n), C542 (100n), C562 (100n) on +12VA; supply decoupling: C116 (100n), C543 (100n), C563 (100n) on -12VA |
| U108 | enable / sequencing network: C190 (47u / 16V X7R) on +5VA; feedback divider: R553 (20) on /receiver/FDA2_OUT_N; feedback divider: R551 (1k), R552 (20) on /receiver/FDA2_OUT_P; feedback divider: R573 (20) on /receiver/FDA3_OUT_N; feedback divider: R571 (1k), R572 (20) on /receiver/FDA3_OUT_P; filter capacitor to ground: C125 (470p), C126 (470p) on GND; soft-start / bias capacitor: C106 (100n) on /receiver/ADC_VCM; supply decoupling: C107 (100n), C108 (100n), C109 (100n), C110 (100n), C112 (10u), C123 (100n), C128 (100n), C547 (100n) (+1 more; see manifest §3.4) on +5VA; supply feed / filter: R548 (499), R550 (1k) on Net-(U108A-+IN1); supply feed / filter: R568 (499), R570 (1k) on Net-(U108B-+IN2) |
| D101 | series / termination resistor: R101 (100) on /receiver/PEN1_PROT_P |
| D102 | input / output filter capacitor: C113 (10u) on /receiver/PEN1_PROT_P |
| D103 | series / termination resistor: R102 (100) on /receiver/PEN1_PROT_N |
| D104 | input / output filter capacitor: C114 (10u) on /receiver/PEN1_PROT_N |
| D520 | input / output filter capacitor: C540 (10u) on /receiver/PEN2_PROT_P; series / termination resistor: R540 (100) on /receiver/PEN2_PROT_P |
| D521 | — |
| D522 | input / output filter capacitor: C541 (10u) on /receiver/PEN2_PROT_N; series / termination resistor: R541 (100) on /receiver/PEN2_PROT_N |
| D523 | — |
| D530 | input / output filter capacitor: C560 (10u) on /receiver/REF_COIL_PROT_P; series / termination resistor: R560 (100) on /receiver/REF_COIL_PROT_P |
| D531 | — |
| D532 | input / output filter capacitor: C561 (10u) on /receiver/REF_COIL_PROT_N; series / termination resistor: R561 (100) on /receiver/REF_COIL_PROT_N |
| D533 | — |
| D534 | — |

### 5.5 fpga

| Component | Passives that serve it |
|---|---|
| J140 | soft-start / bias capacitor: C111 (100n), C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n) (+27 more; see manifest §3.5) on +3.3V |
| TP790 | pull-up resistor: R144 (4.7k) on Net-(U4C-PROGRAM_B_0) |
| TP791 | pull-up resistor: R142 (4.7k) on Net-(U4C-INIT_B_0) |
| TP792 | — |
| U4 | enable / sequencing network: R100 (33) on CLOCK_32M768; gain / feedback-set resistor: R155 (0) on /fpga/MODE0; gain / feedback-set resistor: R156 (0) on /fpga/MODE1; gain / feedback-set resistor: R157 (0) on /fpga/MODE2; pull-down resistor: R152 (0) on /fpga/XADC_VN; pull-down resistor: R150 (0) on /fpga/XADC_VNREF; pull-down resistor: R151 (0) on /fpga/XADC_VP; pull-down resistor: R153 (0) on /fpga/XADC_VPREF; pull-up resistor: R140 (4.7k) on +3.3V; pull-up resistor: R141 (4.7k) on /fpga/PUDC_N; series / termination resistor: R145 (33) on /fpga/DAC_CS_SRC; series / termination resistor: R146 (33) on /fpga/DAC_SCLK_SRC; series / termination resistor: R147 (33) on /fpga/DAC_SDI_SRC; supply decoupling: C150 (100n), C151 (100n), C152 (100n), C153 (100n), C154 (100n), C155 (100n), C156 (100n), C170 (10u) (+1 more; see manifest §3.5) on +1V0_FPGA; supply decoupling: C157 (100n), C158 (100n), C159 (100n), C160 (100n), C161 (100n), C171 (10u), C186 (22u / 25V X7R) on +1V8_FPGA; supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V |
| U141 | series / termination resistor: R790 (0) on Net-(U141-CLK); supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V |
| U142 | enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on +3.3V; filter capacitor to ground: C174 (47p) on /fpga/FT_DM; filter capacitor to ground: C173 (47p) on /fpga/FT_DP; pull-down resistor: R159 (10k) on /fpga/VBUS_SENSE; pull-up resistor: R154 (0), R162 (10k), R164 (10k), R166 (10k) on +3.3V; series / termination resistor: R161 (27) on /fpga/FT_DM; series / termination resistor: R160 (27) on /fpga/FT_DP; supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V |
| Y1 | enable / sequencing network: C111 (100n), C202 (100n), C290 (100n), C291 (100n), C292 (100n), C293 (100n), C294 (100n), C295 (100n) (+12 more; see manifest §3.5) on +3.3V; pull-up resistor: R143 (4.7k), R148 (4.7k), R149 (4.7k) on +3.3V; supply decoupling: C140 (100n), C141 (100n), C142 (100n), C143 (100n), C144 (100n), C145 (4.7u), C162 (100n), C163 (100n) (+7 more; see manifest §3.5) on +3.3V; supply feed / filter: R100 (33) on CLOCK_32M768 |

### 5.6 connectors

| Component | Passives that serve it |
|---|---|
| J20 | — |
| J21 | — |
| J22 | — |
| J23 | — |
| J24 | — |
| J25 | — |
| J26 | — |
| J27 | — |
| J120 | supply decoupling: C191 (1n / 50V X7R) on /connectors/CHASSIS; supply return: R185 (1M) on /connectors/CHASSIS |
| J121 | — |
| J122 | — |
| J123 | — |
| J124 | supply decoupling: C191 (1n / 50V X7R) on /connectors/CHASSIS; supply feed / filter: R158 (4.7k) on USB_VBUS; supply return: R185 (1M) on /connectors/CHASSIS |
| J125 | supply decoupling: C191 (1n / 50V X7R) on /connectors/CHASSIS; supply return: R185 (1M) on /connectors/CHASSIS |
| J126 | — |
| J127 | — |
| J128 | — |
| D750 | — |
| D751 | pull-down resistor: R182 (5.1k) on /connectors/USB_CC1; pull-down resistor: R183 (5.1k) on GND |

---

## 6. Gates and reconciliation

**Count reconciliation 1 — components.** The netlist has 640 `<comp ref=…>`
elements; the document has 640 component headings. Set difference in both
directions is empty and no ref appears twice:

```
GATE1 netlist comps: 640 doc entries: 640
  comps - doc: []
  doc - comps: []
  duplicates: {}
```

**Count reconciliation 2 — pins.** The netlist has 2155 `<node>` elements on
605 nets. The document renders 2155 pin entries: one row per pin in each
multi-pin component table, and two pins per compact two-pin R/C/L line
(4-pin `L1` gets a table). Set difference is empty in both directions and no
pin is repeated:

```
GATE2 netlist nodes: 2155 rendered pin entries: 2155
  nodes - rendered: 0 []
  rendered - nodes: 0 []
  duplicate rendered pins: 0
```

**Connects-to validation.** Every `ref.pin` token in a `Connects to` cell was
matched against the netlist's `(ref, pin)` node set; no ref or pin was invented:

```
GATE3 Connects-to ref.pin tokens validated: 3664
```

**Supporting-passive classification.** Primary rule: an R/C/L is listed on a
component when its supporting net — the functional net of its two, else the
supply rail, else GND — touches that component's supply, set, feedback, bias or
enable pin, classified by the pin-name patterns in §4.1.1. Rail decoupling is
attributed to the nearest same-sheet host(s) with a supply pin on that rail;
per-component listings are capped at eight refs with a pointer to the
manifest. Secondary rule: a passive with no primary host is attached to the
nearest same-sheet component sharing one of its nets, with a filter / pull-up /
pull-down / termination role, so every passive appears on at least one
component's support line. A passive may legitimately serve more than one
component (rail decoupling); it is then listed on each.

- Passives with no host after the secondary rule: **0 of 508** R/C/L parts.
- Passives whose host came from the secondary rule rather than a supply/set/
  feedback/bias/enable pin: 241 (mostly signal filters and series resistors).
- Components with no supporting passive under the strict rule: **60**.
- Components with none after the secondary rule: **44**: power D1, J1, J750,
  L1, TP760–TP763; driver TP200–TP203, TP210–TP217, TP820–TP822; receiver
  D521, D523, D531, D533, D534; fpga TP792; connectors D750, J20–J27, J121–J123,
  J126–J128. These are test points, panel headers, diodes and the 4-pin input
  choke — parts that have no setting/decoupling network to attribute.

**Repo gates** (run at `213ac41`, in this worktree):

```
$ python3 tools/check_references.py
external refs: 18
manifest entries: 14
all external references are covered
(exit 0)

$ python3 tools/contract_ci.py check
contract 1.0.0: 18 SC rows, 27 decisions, ICDs OK
(exit 0)

$ python3 tools/check_doc_paths.py
checked: 520 paths
external/local-only: 17

missing paths:
  - docs/phase2/design_order.md: simulations/fg1/REPORT.md
(exit 1 — the same pre-existing missing FG-1 report cited in Part 3 item 7;
 this document does not add a new missing-path finding)

$ kicad-cli sch erc -o /tmp/cr/erc2.rpt hardware/brd-01/kicad/brd-01.kicad_sch
Found 0 violations
(0 errors / 0 warnings)
```

**Change surface.** Only `docs/phase2/brd01_component_reference.md` is added.
No `.kicad_sch`, `contract/` file or existing document is modified; the
throwaway generator and gate scripts live in `/tmp/cr/`, not in the repo.

# E-stop scope change — stage 1 inventory and plan (2026-11-24)

**Status: inventory and plan only.** No `.kicad_sch`, `.kicad_pro` or `contract/` file is
changed in this stage. Branch `hw/estop-scope`.

**User intent (verbatim):** *"remove the emergency stop from the tracker, it should instead only
be for manipulator. it will track regardless of what happens, a person can press the estop to
stop the arm from moving and that's that."*

**User's answers:** *"it will be from the computer or a dedicated button."* then, final:
*"remove the button, there will be no mushroom button K1 or K2."*

> The complete set of conditions that assert `PICO_STOP_N` low is: a host/software stop request; power-up or a +3.3 V brownout; an overcurrent trip on `/DRIVER_FAULT_N`; and an unconfigured FPGA (R754 pulls the request line low). None of them touches `+15V_DRV`: no condition stops the field.

**Decision applied:** the physical stop is deleted from BRD-01 entirely. K1 and K2 do not exist.
The **only** remaining stop origin is software: host → FPGA → the existing active-low `STOP`
line at the Pico (verified in §A.4). **This removes the last hardware-independent stop path on
the board** — the stop now depends on the host link, the FPGA, the cable and the Pico firmware.
That consequence is not softened anywhere in this analysis or in the contract draft; the
reviewer must accept it explicitly.

Consequence: a stop must halt **arm motion only**. The tracker keeps its field drivers powered,
keeps sampling and keeps solving pose. `+15V_DRV` must **never** be interrupted by a stop. The
≤100 ms stop requirement becomes an arm-motion requirement, not a tracker-shutdown requirement.

---

## 0. Accepted base, rebase and measured baseline

The accepted base is **`fcfe46f`** (`docs: record the D_REF clamp margin ...`). This branch was
rebased onto it with `git rebase --onto fcfe46f 8825dcc hw/estop-scope`; the Stage 1 docs commit
is now `374ecad` on top of `fcfe46f`. **Historical note only:** the originally assigned worktree
sat on rejected local `main` at `8825dcc`, whose latch redraw and `D534` deletion are not in the
accepted base and are not discussed further here.

Reproduction commands (read-only exports under `/tmp/opencode/estop-stage1/`):

```bash
git rebase --onto fcfe46f 8825dcc hw/estop-scope
kicad-cli sch export netlist --format kicadxml -o /tmp/opencode/estop-stage1/rebased.xml \
  hardware/brd-01/kicad/brd-01.kicad_sch
python3 tools/kicad_netlist_compare.py /tmp/opencode/estop-stage1/fcfe46f.xml \
  /tmp/opencode/estop-stage1/rebased.xml
kicad-cli sch erc --format json -o /tmp/opencode/estop-stage1/erc-fcfe46f.json \
  hardware/brd-01/kicad/brd-01.kicad_sch
python3 tools/kicad_sch_helper.py audit hardware/brd-01/kicad/power.kicad_sch
```

Measured on the rebased tree (all evidence below is from `fcfe46f`):

- Netlist comparison vs `fcfe46f`: `CONNECTIVITY SAME: 610 nets, 0 renamed`, `PARTS SAME: 645
  components` — the rebase introduced no electrical change.
- ERC: `Found 0 violations` → **0 errors / 0 warnings**.
- `kicad_sch_helper.py audit`: 0 symbols off grid, 0 wire ends off grid, 0 hanging wire ends,
  0 labels off wire/pin, but **8 pre-existing open pins**: `U753.1 C`, `U754.4`, `U754.1 NC`,
  `U750.1 NC`, `C820.1`, `C818.1`, `R809.2`, `R808.2`. (`U753.1`/`U754.4` share a net in the
  exported netlist; the audit still flags their pin ends.) These exist before any edit and must
  not be attributed to the E-stop removal.

---

## A. What the E-stop does today — traced from the exported netlist

### A.1 Field-generator shutdown chain (accepted base `fcfe46f`)

| Net (netlist name) | Pin memberships used as evidence |
|---|---|
| `+15V_FUSED` | `D1.1`, `U5.1`, `U147.1`, `U147.16`, `J750.1`, **`K1.NC1`**, **`K2.NO2`**, `C30.1`, `C800.1`–`C804.1`, `L760.2`, `R803.1` |
| `/power/ESTOP_NC_15V` | **`K1.NC2`**, **`K2.COIL2`**, `J750.2`, `D140.1`, `R185.1` |
| `/power/K2_COIL_LOW` | **`K2.COIL1`**, `D140.2`, **`Q750.3` (drain)** |
| `+15V_DRV` | **`K2.NO1`**, **`U20.7`…`U27.7` (V+ on all eight LMH6321)**, `U39.5`, `C213.1`, `C221.1`, `C229.1`, `C237.1`, `C245.1`, `C253.1`, `C261.1`, `C269.1`, `C280.1`, `R380.1`, `R382.1`, `R600.1`–`R607.1` |

Chain: `+15V_FUSED` → `K1.NC1/NC2` (panel mushroom, via `J750`) → `ESTOP_NC_15V` → `K2.COIL2`
→ coil → `K2.COIL1` → `K2_COIL_LOW` → `Q750` drain/source → GND. K2's NO contact 2
(`K2.NO2`) feeds its own coil supply (self-latching), and NO contact 1 (`K2.NO1`) bridges
`+15V_FUSED` → `+15V_DRV`.

**Verdict on the dispatch summary: correct.** Pressing K1 opens the NC contact, drops K2, and
removes `+15V_DRV` from all eight coil drivers. The field collapses and the tracker is blinded.
`D140` is the coil flyback diode. `J750` is the two-pin panel harness terminal (pin 1
`+15V_FUSED`, pin 2 `ESTOP_NC_15V`). `K1`/`K2` are `accubot:Draft_EStop_Mushroom_NC` /
`accubot:Draft_EStop_Relay_NO`, excluded from the BOM and PCB — a drawn proof-of-concept, with
relay selection still open (`hardware/brd-01/kicad/README.md`, `bom-to-cad.md` §K1/K2).

### A.2 Q750 and the arm/disarm latch (accepted base `fcfe46f`)

`Q750` is an AO3400A NMOS on the **power sheet**: pin 1 = gate on `/power/ARM_GATE`, pin 2 =
source on GND, pin 3 = drain on `/power/K2_COIL_LOW`. Asserting its gate sinks the K2 coil
current → K2 closes → `+15V_DRV` live and the field generator armed.

| Ref (part) | fcfe46f netlist connectivity | Function |
|---|---|---|
| `R753` 100 Ω | `U753.5` (Q) → `R753.1`; `R753.2` → `/power/ARM_GATE` | latch Q drives `Q750` gate |
| `R754` 100 kΩ | `/power/ARM_GATE` ↔ GND | gate pull-down: board starts disarmed |
| `U753` 74LVC2G74 | pin 2 `D` tied `+3.3V`; pin 1 `C` on `Net-(U753-C)`; pin 5 `Q` on `Net-(U753-Q)`; pin 6 `~CLR` on `Net-(U753-~{CLR})`; pin 7 `~PRE` tied `+3.3V`; pin 8 `+3.3V`; pin 4 GND; pin 3 `~Q` NC | D flip-flop latch; Q=1 arms K2 |
| `U754` 74LVC1G14 | input pin 2 on `Net-(C755-Pad1)` (`C755.1`, `R752.2`); output pin 4 on `Net-(U753-C)`; pin 5 `+3.3V`, pin 3 GND, pin 1 NC | Schmitt trigger turning the button RC into a clock edge |
| `SW750` B3F-1002-G | pin 1 on `Net-(R751-Pad2)`, pin 2 GND | momentary ARM pushbutton |
| `R751` 10 kΩ | `+3.3V` → `Net-(R751-Pad2)` | button pull-up |
| `R752` 1 kΩ | `Net-(R751-Pad2)` → `Net-(C755-Pad1)` | series/debounce resistor; button reaches the latch on `fcfe46f` |
| `C755` 100 nF | `Net-(C755-Pad1)` ↔ GND | debounce capacitor |
| `U752` 74LVC1G08 | pin 1 on `Net-(U751-~{RESET})`, pin 2 on `/DRIVER_FAULT_N`, pin 4 on `Net-(U753-~{CLR})`, pin 5 `+3.3V`, pin 3 GND | AND of supervisor-reset and driver-fault; output clears the latch |
| `U750` 74LVC1G14 | input pin 2 on `/ESTOP_ASSERTED`, output pin 4 on `Net-(U751-~{MR})`, pin 5 `+3.3V`, pin 3 GND, pin 1 NC | inverts E-stop status into supervisor manual-reset |
| `U751` TPS3808G33 | pin 1 `~RESET` on `Net-(U751-~{RESET})` with `R750.2` and `U752.1`; pin 2 GND; pin 3 `~MR` from `U750.4`; pin 4 CT NC; pin 5 SENSE and pin 6 VDD on `+3.3V` | 3.3 V supervisor: power-on/brownout/E-stop holds the clear line low |

`R750` (10 kΩ) pulls `U751.~RESET` / `U752.1` up to `+3.3V`. The four nets quoted in the
accepted-base reading are confirmed exactly:

| Net | fcfe46f pin membership |
|---|---|
| `Net-(U753-C)` | `U753.1` (C) + `U754.4` (inverter output) |
| `Net-(U753-~{CLR})` | `U752.4` (AND output) + `U753.6` (`~CLR`) |
| `Net-(U753-Q)` | `R753.1` + `U753.5` (Q) |
| `unconnected-(U753-~{Q}-Pad3)` | `U753.3` (`~Q`) |
| `/power/ARM_GATE` | `Q750.1` (G) + `R753.2` + `R754.1` |

So the flip-flop's clock (pin 1) comes from the `U754` inverter output and `~CLR` (pin 6) from
the `U752` AND gate, on **separate** nets — as specified. `R752` connects `SW750` to the latch;
`~PRE` is tied high, not floating.

**Classification:** today this whole chain is **tracker-side** hardware — it gates the *field
driver* rail, not the arm. Its UI (`SW750`) is an "arm the field" button. The final decision
removes the button and K1/K2, leaving this chain with no output; whether to delete it or retarget
it is a separate, still-open safety decision (§E). Do not delete it as part of the mechanical
K1/K2 removal.

### A.3 `ESTOP_ASSERTED`, the opto, and `/DRIVER_FAULT_N`

`/power/ESTOP_LED`: `R185.2` + `U143.1` (TLP291 LED anode); `R185.1` on `ESTOP_NC_15V`.
`U143.2`/`U143.3` on GND. `U143.4` (collector) is on `/ESTOP_ASSERTED` with `R186.2` (10 kΩ
pull-up to `+3.3V`), `U750.2`, and **`U4.R2`** on the FPGA sheet. The same net passes through
two root-sheet pins: power-sheet **output** (`brd-01.kicad_sch:331`) and fpga-sheet **input**
(`brd-01.kicad_sch:407`); the fpga sheet carries it on hierarchical label `ESTOP_ASSERTED`
(`fpga.kicad_sch:15014`) to `U4.R2`. There is no RTL in `fpga/` that consumes it, so the netlist
lands at the FPGA pin only.

The documents call this FPGA input `ESTOP_STATUS` (`system_schematic.md:313`,
`m16-fpga-handoff.md:365`). It is the **same signal as `/ESTOP_ASSERTED`**: opto on when the
NC mushroom loop is closed, pulled high when the loop opens. It is status, not a drive path;
the FPGA cannot re-arm K2.

`/DRIVER_FAULT_N`: `U600.4`, `U600.6`, `U601.4`, `U601.6`, `U602.4`, `U602.6`, `U603.4`,
`U603.6` (open-drain comparator outputs), `R712.2` pull-up, **`U752.2`** (latch clear input)
and **`U4.R1`** on the FPGA. The driver sheet also carries it on a hierarchical label
(`driver.kicad_sch:25516`) and the root sheet wires it from driver output to power and fpga
inputs (`brd-01.kicad_sch:151`, `:161`, `:191`, `:341`, `:417`, `:483`).

**Safety consequence today:** an overcurrent fault drops K2 as well as notifying the FPGA, so
the field goes away on electrical faults. Under the new policy that protection must remain even
though the E-stop no longer does it.

**What `/ESTOP_ASSERTED` is actually consumed by:** the netlist shows only four lands —
`U143.4` (opto collector), `R186.2` (pull-up to `+3.3V`), `U750.2` (inverter into the
`U751.~MR` / latch-clear chain) and `U4.R2` (FPGA pin via the root sheet pins and the fpga-sheet
hierarchical label). There is **no consumer in `fpga/` RTL** and it does not reach the DAC or the
coil loops directly. Its only functional effect today is indirect: via `U750` → `U751.~MR` →
`U752` → `U753.~CLR` → `ARM_GATE` → `Q750` → K2 coil → `+15V_DRV`. That is exactly the
tracker-kill mechanism the user wants removed.

**What it becomes under the final decision:** `/ESTOP_ASSERTED` is **deleted** with the button
(no mushroom means no status to report). It must not survive as a dangling label or pin. The
`U750`/`U751`/`U752`/`U753`/`U754` + `Q750` chain must be disconnected from `+15V_DRV`; what
remains of it is decided in §E, not here.

### A.4 Computer-origin stop — already present, no new hardware

`contract/icd/pico_link.md` §3 lists PL → Pico commands including **stop**, and §6 states that
**STOP is a hardware active-low level with a pull-down at the Pico** (unplugged cable = stop),
plus HEARTBEAT absent for 100 ms = local Pico stop. §5 explicitly leaves encoding, framing and
the Pico state machine to the implementers.

Netlist evidence on BRD-01:

| Net | Members |
|---|---|
| `PICO_STOP_N` | **`U4.P4`** (FPGA), **`J123.5`** (Pico connector) |
| `PICO_HEARTBEAT` | `U4.P3`, `J123.6` |
| `PICO_TX` / `PICO_RX` | `U4.N2` / `J123.3`, `U4.N3` / `J123.4` |
| `unconnected-(J123-Pin_1-Pad1)` | `J123.1` only |

So a host stop can travel host → FPGA → `U4.P4` → `PICO_STOP_N` → `J123.5` → Pico → arm halt
using existing hardware. **No BRD-01 schematic or BOM change is required for the computer
origin.** Two caveats, neither a hardware change: (1) this path depends on the host link, the
FPGA and the cable, so this is the **only** stop origin and it is *not* hardware-independent —
that is the explicit safety consequence of deleting the button; (2) `J123.1` is currently NC in
the netlist but `pico_link.md` §2 lists pin 1 as 3V3, and
`brd01_full_board_deepseek_handoff.md` line 85 records D4 as "J123.1 → no_connect". That
pre-existing mismatch is noted but needs no change under the no-button decision.

---

## B. Everywhere the old policy is written down

Key for class: **M** = directly states old "E-stop cuts the field/DDS" policy and must be
rewritten; **C** = wording/checklist only, needs clarification that E-stop is arm-only; **N** =
net name / pin label, no policy text (left alone in stage 1).

| File | Line / section | Current statement | Required under new policy | Class |
|---|---|---|---|---|
| `contract/decisions_log.md` | #10, line 23 | "hardware NC mushroom E-stop in driver enable chain, independent of FPGA; opto status; software watchdog; follower stop ≤100 ms" | supersede: E-stop is manipulator-only; ≤100 ms applies to arm motion; tracker keeps field and pose | M |
| `contract/decisions_log.md` | #21, line 34 | "ADC, DAC, E-stop, watchdog are zone A/B/C board nets" | remove E-stop from the board-net list (no K1/K2, no opto) | M |
| `contract/decisions_log.md` | #22, line 35 | NC mushroom part locked (XB4BS8444 / GCX1131), no metal within 150 mm | part may stay; rationale changes from "fail-safe driver cut" to "fail-safe arm stop" | M |
| `contract/decisions_log.md` | #25, line 38 | "power entry/E-stop/DC-DC ... zones of one 4-layer board" | remove E-stop from the board zone statement | C |
| `contract/icd/power.md` | title, lines 15–19, 27 | "E-stop in driver enable chain ... hardware E-stop is the safety path, not the UART"; "Follower stop ≤100 ms" | remove driver-enable claim; state arm-stop ≤100 ms; define whatever new path carries it | M |
| `contract/icd/pico_link.md` | §3 lines 33–39, §6 line 63 | commands include stop; "The hardware E-stop drops the driver enable independently of both processors"; STOP level + heartbeat already defined | keep the computer-origin STOP path unchanged; delete the driver-enable claim and state that the only stop is software and the last hardware-independent path is gone | M |
| `contract/icd/dac_fpga.md` | §3 item 4, line 42 | "On fault/E-stop: stop the DDS, write zero-scale to all 8 channels, then one TRIGGER" | split: **fault** → DDS off / zero-scale survives; **E-stop** → no effect on DDS | M |
| `contract/icd/README.md` | line 12 | ICD index: `power.md` = "Power entry, E-stop, rails, grounding" | wording only, after `power.md` is updated | C |
| `contract/system_contract.md` | SC-08, line 39 | "filter-on <100 ms, stop <100 ms" (no E-stop text) | clarify that "stop" means arm motion; tracking continues on E-stop | M |
| `docs/phase2/system_schematic.md` | line 16 | board block: "power entry + E-stop + DC-DC/LDO" | remove E-stop from the board block; only software STOP remains | C |
| `docs/phase2/system_schematic.md` | lines 38, 80–81, 92 | block diagram "power entry → E-stop K1/K2 → +15 V_DRV"; `+15 V_DRV` source "E-stop K1"; "NC contact in the +15 V_DRV enable; FPGA stays alive to log the stop" | `+15 V_DRV` from `+15V_FUSED` unswitched; K1/K2 retargeted or removed | M |
| `docs/phase2/system_schematic.md` | §4.5, lines 197–203 | "E-stop / enable chain" ASCII: K1 → K2 coil → `+15V_DRV`, opto → `ESTOP_STATUS`; "pressing it drops K2 and removes +15 V_DRV" | delete the K1/K2 chain and the opto status path; show `+15V_FUSED` → `+15V_DRV` unswitched | M |
| `docs/phase2/system_schematic.md` | line 313 | pin table row 37 `ESTOP_STATUS` | delete the `ESTOP_STATUS` row (opto removed) | M |
| `docs/phase2/system_schematic.md` | lines 369, 377, 386 | "NC contact is in the +15 V_DRV enable"; bring-up "then E-stop K1/K2"; system test "E-stop" | arm-only wording; bring-up checks field stays on through E-stop | M |
| `docs/phase2/driver_power_requirements.md` | lines 9–10, 46–47, 261–262 | "hardware E-stop ... in the driver enable chain ... cuts the +15 V driver/load-switch enable; opto status ... follower stop ≤100 ms" | remove driver-enable cut; arm stop ≤100 ms; field stays up | M |
| `docs/phase2/dig6_requirements.md` | lines 65, 137 | DIG-01e "DDS output disabled/zero on fault or E-stop ... no residual field"; timing "Stop (E-stop) <1 ms hardware; NC button cuts driver enable" | DIG-01e keep **fault only**; add "E-stop does not gate DDS"; timing row becomes arm-stop timing | M |
| `docs/phase2/system_flowchart.md` | lines 15, 74, 217, 222, 287, 300, 307 | "hardware E-stop cuts the driver independently"; `ESTOP --> AMP` and `ESTOP --> PICO`; `STOPPED` on E-stop; "E-stop NC opens → driver enable off <1 ms"; "cut +15 V driver enable, opto status" | E-stop → arm stop only; `AMP` edge removed; tracker stays in TRACKING | M |
| `docs/phase2/design_order.md` | lines 61, 158, 176–177, 344 | DRV-2 "one box + E-stop locked"; "hardware E-stop is a NC mushroom button in the driver enable chain"; bench "E-stop/overcurrent" | scope lock changes; bench test verifies field stays on and arm stops | M |
| `docs/phase2/README.md` | lines 50–51 | functional "emergency stop"; non-functional "fail-safe halt on tracking/field fault" | keep both but scope "emergency stop" to the arm; field-fault halt stays a tracker behaviour | C |
| `docs/phase2/brd01_full_board_deepseek_handoff.md` | lines 51, 68, 82, 85, 102 | review checklist for K1/K2, opto `ESTOP_STATUS`, E-stop box on sheets | update checklists to the K1/K2/opto removal | C |
| `docs/phase2/brd01_power_v2_deepseek_handoff.md` | line 86 | block 2 called "E-Stop + Arm Latch" | delete/retitle block 2 (E-stop and latch removed or blocked in §E) | C |
| `docs/handoff/m16-fpga-handoff.md` | lines 365, 394, 410, 469 | pin 37 `ESTOP_STATUS`; "NC mushroom cuts the +15 V driver enable; FPGA gets opto status; cannot re-enable"; test item "Fault/E-stop" | status pin stays; remove driver cut and DDS-stop-on-E-stop test | M |
| `docs/handoff/system-flowchart-handoff.md` | lines 58–60, 199–200, 228, 241 | F5 emergency stop, N4 fail-safe halt, firmware "emergency stop plus stop watchdog within 100 ms", triggers including E-stop all lead to halt | scope E-stop trigger to arm halt; keep tracking-lost/fault halts | M |
| `hardware/README.md` | lines 11, 27–28 | "power/E-stop ... NC E-stop in the driver enable chain (#7/#10/#20)" | remove the driver-enable E-stop claim; no hardware stop path remains | M |
| `hardware/brd-01/README.md` | lines 8, 12, 25 | zone table "Power entry / E-stop"; "Connectors ... E-stop"; open "E-stop relay selection" | remove the E-stop zone and relay-selection open item | M |
| `hardware/brd-01/kicad/README.md` | lines 65, 75–76, 107 | "power tree documents the E-stop latch"; two draft symbols; "active-low overcurrent bus reaches both FPGA and hardware K2 coil inhibit ... latch clears on fault, E-stop, or supervisor reset" | latch narrative must become arm-side or be deleted; overcurrent path to the tracker must survive | M |
| `hardware/brd-01/kicad/bom-to-cad.md` | lines 197, 216–217, 380, 462 | K2 "NO power contact intended to switch +15 V_DRV"; K1/K2 roles; "record ... shunt current ... through E-stop"; "without changing the independent hardware E-stop" | retarget contact purpose; benchmark E-stop measurement becomes "field unchanged, arm stopped" | M |
| `hardware/brd-01/kicad/power-tree.md` | lines 24, 48, 77, 102–133, 164, 264, 267, 284–290 | full rail/latch description: `+15V_DRV` "only when E-stop closed and arm latch set"; "only safety path that removes coil power"; "E-stop pressed → relay drops"; FPGA-ball table | rewrite §2 rail row, §3 chain/behaviour, §cross-sheet tables; keep overcurrent latch | M |
| `hardware/brd-01/kicad/power.kicad_sch` | text at lines 9053, 9132, 9154, 9165, 9176, 9198 | sheet annotations: "Driver interlock \| Power-up, E-stop and overcurrent clear the arm latch"; "K1 opens the physical coil feed"; "Check E-stop relay drop-out time"; "Draft single-channel inhibit" | electrical retarget in stage 2; annotations must match the new latch output | M |
| `hardware/brd-01/kicad/brd-01.kicad_sch` | lines 131, 171, 331, 407 | root labels and sheet pins `/ESTOP_ASSERTED` (power out → fpga in) | status path stays under (a)/(b)/(c); rename only if docs are unified | N |
| `hardware/brd-01/kicad/fpga.kicad_sch` | line 15014 | hierarchical label `ESTOP_ASSERTED` to `U4.R2` | no change: status input only | N |
| `robot-arm/INTEGRATION.md` | line 44 | "hardware E-stop drops the driver enable independently of both processors" | replace with the selected arm-side path; this file is this repo's mirror of the arm-side contract | M |
| `AGENTS.md` | line 107 | board zone "power entry/E-stop/DC-DC" | remove E-stop from the board-zone line | C |
| `hardware/AGENTS.md` | line 32 | test list "E-stop/overcurrent (DRV-2)" | test now proves field-continues + arm-stops; overcurrent test unchanged | C |

**Counts:** 34 rows over 27 distinct files: **24 rows class M** spanning **19 files** (direct
old-policy statements, including SC-08 and the schematic annotations), **8 rows class C**
(wording/checklist only), **2 rows class N** (net labels only, no text change). A raw `grep` for
`E-stop|estop|emergency` matches 26 files; `contract/system_contract.md` is the additional file
found via the `stop <100 ms` wording. The 19 M files break down as 5 in `contract/`
(`decisions_log.md`, `power.md`, `pico_link.md`, `dac_fpga.md`, `system_contract.md`), 7 in
`docs/`, 6 in `hardware/` (including the power-sheet annotations) and `robot-arm/INTEGRATION.md`.

---

## C. Electrical delta and safety consequences

Final decision: no button, no K1/K2, one software stop origin. Each action is marked
**unambiguous** (mechanical consequence of that decision) or **blocked** (needs the §E decision).

| # | Action | Mark | Hazard still covered / newly uncovered |
|---|---|---|---|
| 1 | Remove K2 from `+15V_DRV`: connect `+15V_DRV` to `+15V_FUSED` unswitched (keep fuse, input protection and decoupling). All eight LMH6321 V+ pins stay live through a stop. | unambiguous | Field/pose availability preserved. The board no longer has a contact that removes coil power on stop. |
| 2 | Delete the physical stop entirely: no mushroom, no K1/K2, no panel harness. The only stop origin is host → FPGA → `U4.P4` → `PICO_STOP_N` → Pico. | unambiguous | **The last hardware-independent stop path on the board is removed.** Stop now depends on host link, FPGA, cable and Pico firmware; no new BRD-01 hardware is needed. |
| 3 | Delete `J750`, `R185`, `U143`, `R186` and the `/ESTOP_ASSERTED` net from power, root and fpga sheets. No opto status survives because no button exists. | unambiguous | FPGA/host lose E-stop status reporting — acceptable only because there is no button to report. |
| 4 | Delete the `ESTOP_STATUS` pin-table row and the handoff text that describes the opto status. | unambiguous | Documentation only; pin 37 becomes free/not populated. |
| 5 | Latch `U750`–`U754` + `Q750` + `SW750` + passives: its only output was `ARM_GATE → Q750 → K2 coil → +15V_DRV`. With K2 gone it has no output, but it is **load-bearing** for board-level overcurrent disconnect and power-on/brownout "starts disarmed" behaviour. | **blocked — see §E** | Deleting it silently removes the hardware overcurrent rail disconnect and the disarmed-at-power-up state; retargeting it to STOP needs arbitration with `U4.P4` and a decision on fault/power-up semantics. |
| 6 | Split `dac_fpga.md` §3 item 4: **genuine FPGA/ADC/driver fault** → stop DDS, zero all 8 channels, one TRIGGER (survives); **software stop from the host** → no DDS/DAC/coil effect. | unambiguous | Fault protection preserved; a software arm stop no longer creates a "no residual field" condition. |
| 7 | `pico_link.md` §6: keep STOP as the active-low level (`U4.P4` → `J123.5`) for host stops, tracking-loss and heartbeat; delete the "hardware E-stop drops the driver enable independently of both processors" claim and state that the hardware-independent path is gone. | unambiguous | The independent path is gone by explicit decision; `PICO_STOP_N` remains the only board-originated STOP level. |
| 8 | Keep ICNIRP analysis unchanged: field amplitude, tone plan, currents, guard and 27 µT sum are untouched; the generator already runs continuously during normal tracking. | unambiguous | **No new field hazard is created** by leaving the field on. The safety claim that changes is the loss of the independent arm stop, not exposure. |

`/DRIVER_FAULT_N` must still reach `U4.R1`. Whether it also still reaches `U752.2` depends on
the §E decision; until that is answered, no latch part is deleted.

---

## D. Decision applied — option (b) with no button at all

The narrowed option question is closed by the user's final decision: *"remove the button, there
will be no mushroom button K1 or K2."* This is **option (b) with no button at all**: the
physical stop is deleted from BRD-01; there is no arm-side mushroom, no K1/K2 on the board, and
no status opto for a button that no longer exists.

**The only remaining stop origin is software:** host → FPGA → `U4.P4` → `PICO_STOP_N` →
`J123.5` → Pico → arm halt (§A.4). No new BRD-01 hardware is needed for this path.

**This removes the last hardware-independent stop path on the board.** The stop now depends on
the host link, the FPGA, the cable and the Pico firmware. The previous "hardware E-stop drops
the driver enable independently of both processors" claim in `pico_link.md` §6 becomes false and
must be replaced, not softened. The reviewer must accept this loss explicitly.

Consequences that follow mechanically from that decision:

- `+15V_DRV` is never switched by a stop; it must be joined unswitched to `+15V_FUSED`.
- K1, K2, the panel harness terminal and the opto status chain for the mushroom are deleted.
- `/ESTOP_ASSERTED` (docs name `ESTOP_STATUS`) disappears from the power sheet, the root sheet
  pins and the fpga-sheet hierarchical label.
- `dac_fpga.md` §3 item 4 loses its E-stop clause; a genuine FPGA/ADC/driver fault remains a
  separate tracker-side safe state.
- The arm/disarm latch question is **not** settled by this decision — see §E. Stop before
  deleting it.

## E. Dependency inventory from the netlist (stage 2b evidence)

Exported netlist on the accepted base (`/tmp/opencode/estop-stage1/rebased.xml`, identical to
`fcfe46f`: `CONNECTIVITY SAME`, `PARTS SAME`). All memberships below are from that netlist.

**Parts that exist only for the mushroom/relay path** (additions to the dispatch's list marked `+`):

| Ref | Part | Evidence (net memberships) |
|---|---|---|
| K1 | `Draft_EStop_Mushroom_NC` | `K1.NC1` on `+15V_FUSED`; `K1.NC2` on `/power/ESTOP_NC_15V` |
| K2 | `Draft_EStop_Relay_NO` | `K2.NO2` on `+15V_FUSED` (coil self-feed); `K2.NO1` on `+15V_DRV`; `K2.COIL2` on `/power/ESTOP_NC_15V`; `K2.COIL1` on `/power/K2_COIL_LOW` |
| D140 | PMEG4010CEH | cathode `/power/ESTOP_NC_15V`, anode `/power/K2_COIL_LOW` (coil flyback) |
| J750 `+` | panel terminal 1715721 | pin 1 `+15V_FUSED`, pin 2 `/power/ESTOP_NC_15V` |
| R185 `+` | 3.3 kΩ | `ESTOP_NC_15V` → `/power/ESTOP_LED` |
| U143 `+` | TLP291 opto | pin 1 `/power/ESTOP_LED`; pins 2/3 GND; pin 4 `/ESTOP_ASSERTED` |
| R186 `+` | 10 kΩ | `+3.3V` → `/ESTOP_ASSERTED` (collector pull-up) |
| Q750 | AO3400A | gate on gate net, source GND, drain `/power/K2_COIL_LOW` |
| R753 | 100 Ω | `U753.Q` → gate net |
| R754 | 100 kΩ | gate net → GND |
| U750 `+` | 74LVC1G14 | pin 2 `/ESTOP_ASSERTED`; pin 4 → `U751.~MR` |
| U751 `+` | TPS3808 supervisor | pin 3 MR from U750; pin 1 RESET → U752.1; watches +3.3 V (not solely the mushroom, but its only output feeds the latch) |
| U752 / U753 / U754 `+` | 1G08 / 2G74 / 1G14 | latch chain, see below |
| SW750 / R750 / R751 / R752 / C755 `+` | arm pushbutton and RC | arm/debounce chain, see below |

**Nets that exist only for this path** (`fcfe46f` names): `/power/ESTOP_NC_15V`,
`/power/K2_COIL_LOW`, `/power/ARM_GATE`, `/power/ESTOP_LED`, `/ESTOP_ASSERTED`,
`Net-(U751-~{MR})`, `Net-(U751-~{RESET})`, `Net-(U753-Q)`, `Net-(C755-Pad1)`,
`Net-(R751-Pad2)`, `Net-(U753-C)` and `Net-(U753-~{CLR})`. `+15V_FUSED` **survives** (loses
`K1.NC1`, `K2.NO2`, `J750.1`); `/DRIVER_FAULT_N` **survives** (loses `U752.2` only if the latch
is deleted).

**Latch verdict — DO NOT DELETE YET.** `U753.Q` has exactly one load: `R753.1`; `R753.2` goes
to the Q750 gate. Q750's only drain load is the K2 coil. So with K2 gone the latch has **no
output** — but it is not dead code. It is load-bearing for two other behaviours:

1. **Hardware overcurrent disconnect.** `/DRIVER_FAULT_N` is the wired-OR bus of `U600.4/6`,
   `U601.4/6`, `U602.4/6`, `U603.4/6` (open-drain comparator outputs). The individual
   comparator outputs (`U60`–`U67` pins 1) go only to test points `TP210`–`TP217`. That bus
   reaches `U752.2` and `U4.R1`. The *only board-level* path that turns a comparator trip into a
   field disconnect is `U752 → U753.~CLR → U753.Q → Q750 → K2 → +15V_DRV`. The LMH6321
   current-limit pins (`R600`–`R607`) remain, but the board-level rail disconnect does not.
2. **Power-on / brownout disarmed state.** `U751.~RESET` holds `U752.1` low until +3.3 V is
   valid; the board "always starts disarmed". Deleting the latch makes the field live as soon as
   `+15V_FUSED` is present.

Two outcomes remain, and they are a design decision, not a mechanical consequence: **(i)** delete
the whole latch and accept that overcurrent becomes FPGA-only plus per-device current limit and
the board starts live; or **(ii)** retarget the latch to assert the Pico STOP level, which needs
arbitration with `U4.P4` on `PICO_STOP_N` (currently FPGA-driven) and an explicit decision on
whether power-up/fault should stop the arm. **I have stopped before deleting any of it** — that
choice is the next question.

**Ruling executed (stage 2):** the latch survives and is retargeted. `U753.~Q` (pin 3) drives
`U755.B`; `U753.Q` (pin 5) is an explicit no-connect. `U755` is a 74LVC1G08 AND gate with
`U755.A = PICO_STOP_REQ_N` (`U4.P4` + reused `R754` pull-down) and `U755.Y = PICO_STOP_N`
(→ `J123.5`). A series resistor was rejected because it cannot assert low against a push-pull
FPGA high. `U751.~MR` is tied high; `/DRIVER_FAULT_N` still reaches `U752.2` and `U4.R1`.
`+15V_DRV` is deleted as a name and every driver-sheet label is now `+15V_FUSED`. Net parts
645 → 637 (nine removals, one addition). `U4.R2` is freed and marked no-connect.

### Stage 2 plan (executed)

0. **Stop condition:** the §E latch decision must be answered before any latch part is deleted.
   The `+15V_DRV` bridge and the button/opto removal are mechanically settled; the latch is not.
1. Apply the schematic edit on the branch actually being used, re-export the netlist, and gate
   on exact part removals, net deltas, ERC 0/0, `kicad_sch_helper.py audit`, and a 200 dpi visual
   check of the power-sheet rail.
2. File the `contract-change` issue from `docs/phase2/contract_change_estop_draft.md`, get the
   PR and two approvals, bump `contract/VERSION` + `CHANGELOG.md`, tag `contract-vX.Y.Z`, and
   have the arm repo pull it. The draft must state explicitly that the last hardware-independent
   stop path is gone.
3. Update the 24 M rows (19 files) in §B after the contract is approved (contract first, then
   docs, then schematic annotations, then the arm-repo mirror).
4. Re-run `python3 tools/check_doc_paths.py`, `python3 tools/check_references.py`,
   `python3 tools/contract_ci.py check`, ERC, and a bench test with the single software origin:
   host stop → arm motion stops within 100 ms while field and pose continue.

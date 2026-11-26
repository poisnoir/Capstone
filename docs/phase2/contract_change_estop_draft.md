# Draft `contract-change` issue — E-stop scope: manipulator-only stop, tracker unaffected

> **Historical draft — the scope decision is closed, the contract release is pending.**
> This was filed as a draft, not merged here. The arm-only STOP decision is recorded as
> #30 in the 1.1.0 contract PR on `docs/spine-consistency` (tag pending review); this
> document keeps its original analysis and approval checklist as history. No further
> electrical change is required for the stage-2 wiring, but the bench check in §5 and
> the arm-repo release sync remain open. §3's latch row used the earlier `~Q` wording;
> the executed netlist uses `U753.5 (Q)` via `/power/ARM_Q`, with `U753.3 (~Q)` NC
> (`docs/phase2/brd01_wiring_manifest.md` §5 item 1; `system_schematic.md` §4.5).

**Title:** `contract-change`: delete the physical E-stop from BRD-01; arm STOP is host request
plus hardware latch (AND gate); tracker keeps field and pose

## 1. What changes and why

> The complete set of conditions that assert `PICO_STOP_N` low is: a host/software stop request; power-up or a +3.3 V brownout; an overcurrent trip on `/DRIVER_FAULT_N`; and an unconfigured FPGA (R754 pulls the request line low). None of them touches `+15V_DRV`: no condition stops the field.

The user has decided that the emergency stop is **for the manipulator only**: *"remove the
emergency stop from the tracker ... it will track regardless of what happens, a person can press
the estop to stop the arm from moving and that's that."* After first saying the stop would come
*from the computer or a dedicated button*, the user gave the final decision: *"remove the button,
there will be no mushroom button K1 or K2."* The physical stop is deleted from BRD-01 entirely;
the **board has no panel E-stop**. Arm STOP is now raised by a host/software request through the
FPGA or by the hardware latch on power-up/brownout, overcurrent and pre-configuration. During a
stop the host link, FPGA, cable and Pico firmware are still involved, and the previous
"hardware E-stop independent of both processors" claim in `pico_link.md` §6 is gone: **the last
hardware-independent stop path on the board has been removed**. The reviewer must accept that
loss explicitly. The
reviewer must accept that loss explicitly; it is the single most important consequence of this
change and is not softened here. `+15V_DRV` stays powered, the DDS/DAC and coil loops keep
running, and pose solutions keep flowing during a stop. The ≤100 ms requirement is re-scoped to
**arm motion**. A genuine FPGA/ADC/driver fault remains a separate tracker-side safe-state
condition and may still stop the DDS — that behaviour is retained. Evidence and the affected-text
inventory are in `docs/phase2/estop_scope_change.md`.

## 2. Superseded decisions

| Decision | Current text | Superseded part |
|---|---|---|
| #10 | hardware NC mushroom E-stop in driver enable chain, independent of FPGA; opto status; software watchdog; follower stop ≤100 ms | E-stop no longer exists; the ≤100 ms number applies to arm motion only. The hardware-independent stop path is removed (§6). |
| #21 | "ADC, DAC, E-stop, watchdog are zone A/B/C board nets" | Remove E-stop from the board-net list entirely; no K1/K2 and no opto status remain on BRD-01. |
| #22 | NC mushroom part locked (Schneider XB4BS8444 / AutomationDirect GCX1131), no metal within 150 mm | Deleting K1/K2 supersedes the mushroom part lock for BRD-01; no replacement stop button is specified. The 150 mm metal rule is unaffected. |
| #25 | "power entry/E-stop/DC-DC ... zones of one 4-layer board" | BRD-01 has no E-stop zone; power entry remains. |
| Related: `contract/system_contract.md` SC-08 | "stop <100 ms" with no scope | Must be read as arm-motion stop; tracking continues through the single software stop. |

## 3. Before / after — signals, rails and behaviour

Netlist evidence: exported with `kicad-cli sch export netlist --format kicadxml` from
`hardware/brd-01/kicad/brd-01.kicad_sch` on the accepted base `fcfe46f`; pin memberships are
quoted in `docs/phase2/estop_scope_change.md` §A. The rejected `8825dcc` divergence is historical
only.

| Item | Before (from netlist / ICD) | After (policy; wiring per §6) |
|---|---|---|
| `+15V_DRV` | `K2.NO1` bridges `+15V_FUSED` → `+15V_DRV`; feeds `U20.7`…`U27.7` (all LMH6321) and `U39.5` | Name deleted; every driver-sheet label is now `+15V_FUSED` (label rename, connectivity unchanged). The node is unswitched and **never** interrupted by a stop |
| K1 / K2 | K1 NC (`K1.NC1` on `+15V_FUSED`, `K1.NC2` on `ESTOP_NC_15V`) drops K2; `K2.NO2` self-latches the coil feed; `K2.NO1` removes the driver rail | Deleted; no panel E-stop on BRD-01. `+15V_FUSED` is bridged straight to the driver rail |
| `/power/ESTOP_NC_15V` | `K1.NC2`, `K2.COIL2`, `J750.2`, `D140.1`, `R185.1` | Removed with K1/K2, J750, D140 and R185 |
| `/ESTOP_ASSERTED` (docs call it `ESTOP_STATUS`, pin 37) | `U143.4` opto collector, `R186.2` pull-up, `U750.2`, `U4.R2`; root pins power-out → fpga-in; no RTL consumer | Deleted with the button/opto; root sheet pins and fpga landing removed. **`U4.R2` is freed and marked no-connect: the FPGA loses this input and the RTL team must be told.** |
| `U750`/`U751`/`U752`/`U753`/`U754`, `Q750`, `SW750`, `R750`–`R754`, `C755`, `D140` | `U750` inverts E-stop → `U751.~MR`; `U752` ANDs supervisor reset with `/DRIVER_FAULT_N`; `U753.Q` → `ARM_GATE` → `Q750` → K2 coil → `+15V_DRV` | Latch survives and is retargeted: `U753.~Q` (pin 3) drives new AND gate `U755.B`; `U753.Q` (pin 5) is an explicit NC. `U751.~MR` tied high; `/DRIVER_FAULT_N` still reaches `U752.2` and `U4.R1` |
| `PICO_STOP_N` / `PICO_STOP_REQ_N` | `U4.P4` → `J123.5` on one net | Split: `PICO_STOP_REQ_N` = `U4.P4` + `R754.1` (pull-down for unconfigured FPGA) + `U755.A`; `PICO_STOP_N` = `U755.Y` → `J123.5`. U755 (74LVC1G08) ANDs request with `U753.~Q`; a resistor-only fix was rejected because it cannot assert low against a push-pull high |
| `PICO_HEARTBEAT` | `U4.P3` → `J123.6`; missing 100 ms → Pico stops | Unchanged |
| `/DRIVER_FAULT_N` | comparator bus `U600`–`U603`, `R712.2`, `U752.2`, `U4.R1` | Unchanged: reaches both `U752.2` (clears latch → `~Q=1` → STOP) and `U4.R1` |
| DAC safe state (`dac_fpga.md` §3 item 4) | "On fault/E-stop: stop the DDS, write zero-scale to all 8 channels, then one TRIGGER" | Split: **genuine fault** → DDS off / zero-scale / one TRIGGER (survives); **software arm stop** → no DDS/DAC/coil effect |
| Stop timing | E-stop <1 ms hardware cut of driver enable; follower stop ≤100 ms | Arm motion ≤100 ms from host request, power-up/brownout, overcurrent or unconfigured FPGA; field and pose unchanged; ICNIRP field sum unchanged |

## 4. Reproduction commands and current gates

Commands (from the worktree root, branch `hw/estop-scope`):

```bash
python3 tools/check_doc_paths.py
python3 tools/check_references.py
python3 tools/contract_ci.py check
kicad-cli sch export netlist --format kicadxml -o /tmp/opencode/estop-stage1/rebased.xml \
  hardware/brd-01/kicad/brd-01.kicad_sch
python3 tools/kicad_netlist_compare.py /tmp/opencode/estop-stage1/fcfe46f.xml \
  /tmp/opencode/estop-stage1/rebased.xml
```

Results at the time of this draft (stage 1, two new docs only):

- `check_doc_paths.py`: exit 1, with the single known unrelated failure
  docs/phase2/design_order.md → the missing simulations/fg1/REPORT.md; no new failures from
  this change.
- `check_references.py`: exit 0 ("all external references are covered").
- `contract_ci.py check`: exit 0 (`contract 1.0.0: 18 SC rows, 27 decisions, ICDs OK`).
- `kicad_netlist_compare.py` (fcfe46f → rebased branch): `CONNECTIVITY SAME: 610 nets, 0
  renamed`, `PARTS SAME: 645 components` — no electrical change from the rebase.
- ERC on `fcfe46f`: `Found 0 violations` (0 errors / 0 warnings).
- `kicad_sch_helper.py audit` on `fcfe46f`: 0 off-grid symbols/wires, 0 hanging wire ends, 0
  labels off wire/pin, but 8 pre-existing open pins (`U753.1`, `U754.4`, `U754.1`, `U750.1`,
  `C820.1`, `C818.1`, `R809.2`, `R808.2`) that predate this change.

No schematic or contract file was edited; the netlist above is evidence only.

## 5. Approval checklist (from `AGENTS.md`)

1. File this body as a `contract-change` issue.
2. Open a PR that amends the text inventory in `docs/phase2/estop_scope_change.md` §B and the
   affected contract files once the option is selected.
3. Obtain **two approvals**: interface owner + integrator.
4. Bump `contract/VERSION` and append to `contract/CHANGELOG.md`; tag `contract-vX.Y.Z`.
5. The separate arm repo pulls the new contract release and updates its ICD copy
   (`robot-arm/INTEGRATION.md` mirrors `pico_link.md` §6 in this repo).
6. Re-run the three gates above plus ERC and a single-origin bench test (host stop → arm stops
   ≤100 ms while field and pose continue) before closing the issue.

## 6. Formal contract change required

File the issue and PR for exactly these items; do not edit `contract/` from this stream:

- `contract/decisions_log.md` **#10** (hardware NC mushroom E-stop in driver enable chain;
  follower stop ≤100 ms) and **#22** (NC mushroom part lock); also **#21** and **#25** for the
  board-net/zone wording.
- `contract/icd/power.md` lines ~15 and ~19 (E-stop in the driver enable chain; hardware
  E-stop is the safety path) — now: no panel E-stop, unswitched `+15V_FUSED`, STOP via AND gate.
- `contract/icd/pico_link.md` §6 (hardware E-stop drops driver enable independently of both
  processors) — now: STOP is active low from U755; board loses the last hardware-independent
  stop path; document `PICO_STOP_N` vs `PICO_STOP_REQ_N`.
- `contract/icd/dac_fpga.md` §3 item 4 (on fault/E-stop stop the DDS) — keep the genuine fault
  safe state, remove the E-stop clause.
- `contract/system_contract.md` SC-08 — "stop <100 ms" means arm motion; tracking continues.

## 7. Still open

1. The **lost `U4.R2` input** is marked NC on the FPGA sheet; the RTL team must be told that
   `ESTOP_ASSERTED` no longer exists.
2. The rail is now named `+15V_FUSED` everywhere (`+15V_DRV` deleted as a name); tools, logs and
   test scripts that key on `+15V_DRV` must be updated.
3. A **series resistor** on `PICO_STOP_N` was rejected: it cannot assert a low against a
   push-pull FPGA high. The AND gate U755 is the adopted arbitration.
4. The board has **no panel E-stop**; the removal of the last hardware-independent stop path
   must be accepted by the interface owner and integrator.
5. `J123.1` is NC in the netlist but `pico_link.md` §2 calls pin 1 3V3 (D4 records no_connect);
   a pre-existing mismatch, untouched by this change. **Still OPEN (2026-11-25):** the
   v2 rails were adopted by decision #31, but the frozen ICD pinout was not changed;
   `pico_link.md` keeps 3V3 with an OPEN note before §3.

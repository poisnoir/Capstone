# Draft `contract-change` issue — E-stop scope: manipulator-only stop, tracker unaffected

> **Draft only.** Do not edit `contract/` from this work stream. File this body as a
> `contract-change` issue; the interface owner + integrator approval flow is owned by the
> Orchestrator. Stage 1: no electrical change is made.

**Title:** `contract-change`: delete the physical E-stop from BRD-01; arm stop is software-only
(host → FPGA → Pico STOP); tracker keeps field and pose

## 1. What changes and why

The user has decided that the emergency stop is **for the manipulator only**: *"remove the
emergency stop from the tracker ... it will track regardless of what happens, a person can press
the estop to stop the arm from moving and that's that."* After first saying the stop would come
*from the computer or a dedicated button*, the user gave the final decision: *"remove the button,
there will be no mushroom button K1 or K2."* The physical stop is deleted from BRD-01 entirely;
the **only remaining stop origin** is software — host → FPGA → the existing active-low `STOP`
line at the Pico (`contract/icd/pico_link.md`). This **removes the last hardware-independent stop
path on the board**: the arm stop now depends on the host link, the FPGA, the cable and the Pico
firmware, and the "independent of both processors" claim in `pico_link.md` §6 becomes false. The
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
| `+15V_DRV` | `K2.NO1` bridges `+15V_FUSED` → `+15V_DRV`; feeds `U20.7`…`U27.7` (all LMH6321) and `U39.5` | Direct from `+15V_FUSED` (fuse/protection/decoupling retained); **never** interrupted by an arm stop |
| K1 / K2 | K1 NC (`K1.NC1` on `+15V_FUSED`, `K1.NC2` on `ESTOP_NC_15V`) drops K2; `K2.NO2` self-latches the coil feed; `K2.NO1` removes the driver rail | Deleted (no button, no relay); `+15V_DRV` bridged directly to `+15V_FUSED`; held pending the latch decision in §6 |
| `/power/ESTOP_NC_15V` | `K1.NC2`, `K2.COIL2`, `J750.2`, `D140.1`, `R185.1` | Removed with K1/K2, J750, D140 and R185 |
| `/ESTOP_ASSERTED` (docs call it `ESTOP_STATUS`, pin 37) | `U143.4` opto collector, `R186.2` pull-up, `U750.2`, `U4.R2`; root pins power-out → fpga-in; no RTL consumer | **Deleted** with the button/opto; no dangling label or root pin may remain |
| `U750`/`U751`/`U752`/`U753`/`U754`, `Q750`, `SW750`, `R750`–`R754`, `C755`, `D140` | `U750` inverts E-stop → `U751.~MR`; `U752` ANDs supervisor reset with `/DRIVER_FAULT_N`; `U753.Q` → `ARM_GATE` → `Q750` drain → `K2_COIL_LOW`; output is a **tracker kill** and the board-level overcurrent / power-on lockout | Must be disconnected from `+15V_DRV`. Whether the whole latch is deleted or retargeted to STOP is a **separate open safety decision** (analysis §E); `/DRIVER_FAULT_N` must still reach `U4.R1` |
| `PICO_STOP_N` | `U4.P4` → `J123.5`; active-low level, pull-down at Pico (ICD §6) | Unchanged as the **computer-origin** path (host → FPGA → STOP). `J123.1` pin-1 mismatch must be resolved before reuse |
| `PICO_HEARTBEAT` | `U4.P3` → `J123.6`; missing 100 ms → Pico stops | Unchanged |
| `/DRIVER_FAULT_N` | comparator bus `U600`–`U603`, `R712.2`, `U752.2`, `U4.R1` | Survives to `U4.R1` as the genuine fault path; whether it also still reaches `U752.2` depends on the latch decision |
| DAC safe state (`dac_fpga.md` §3 item 4) | "On fault/E-stop: stop the DDS, write zero-scale to all 8 channels, then one TRIGGER" | Split: **genuine fault** → DDS off / zero-scale / one TRIGGER (survives); **software arm stop** → no DDS/DAC/coil effect |
| Stop timing | E-stop <1 ms hardware cut of driver enable; follower stop ≤100 ms | Arm motion ≤100 ms from the single software origin; tracker latency/pose unchanged; ICNIRP field sum unchanged (field stays on, same as normal operation) |

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

## 6. Still open

1. **The one remaining blocking question — the arm/disarm latch.** The final decision removes
   K1/K2 and the button, but `U750`–`U754` + `Q750` + `SW750` + passives are not merely dead
   code: they are the only board-level path that turns `/DRIVER_FAULT_N` into a field disconnect
   and the only thing that holds the field disarmed at power-up/brownout. Two outcomes remain:
   **(i)** delete the whole latch and accept those safety changes, or **(ii)** retarget it to
   assert the Pico STOP level (needs arbitration with `U4.P4` and a decision on fault/power-up
   semantics). Netlist evidence is in `docs/phase2/estop_scope_change.md` §E. Nothing is deleted
   until this is answered.
2. The branch is now rebased onto `fcfe46f`; on that base `Net-(U753-C)` = `U753.1`+`U754.4`
   and `Net-(U753-~{CLR})` = `U752.4`+`U753.6` are separate, `~PRE` is tied high and `R752`
   connects `SW750` to the latch. Any latch edit must use these memberships, not the rejected
   `8825dcc` redraw.
3. `J123.1` is NC in the netlist but `pico_link.md` §2 calls pin 1 3V3 (D4 records "no_connect");
   a pre-existing mismatch, relevant only if a new discrete is ever added.
4. K1/K2 are draft symbols excluded from BOM/PCB; deletion removes them and `J750`, `D140`,
   `R185`, `U143`, `R186` from the BRD-01 BOM. No replacement button is specified.
5. Host-stop command encoding/framing stays a free implementation choice under `pico_link.md`
   §5; the arm team must accept a host stop as the sole origin, with no new ICD electrical path.
6. **Safety acceptance of the hardware stop removal must be explicit:** this change removes the
   last hardware-independent stop path on the board, so the "independent of both processors"
   claim in `pico_link.md` §6 cannot survive. The only stop is host → FPGA → Pico; an FPGA hang,
   a broken cable or a lost host link removes the ability to stop the arm.

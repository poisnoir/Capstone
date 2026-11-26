# Phase 2 — System schematic (Rev A, board level)

**Status:** Rev A draft, 2026-10-27; updated 2026-11-25 for arm-only STOP (#30),
power tree v2 (#31) and option-D FPGA (#26). This is the
board-level schematic and interface document for the Phase 2 design review. It
states the rails, connectors, channel map, and signal nets; the contract is the
approval gate. The EDA capture (KiCad) adds symbols, footprints, and pin numbers;
it must not change approved interfaces without a deviation.

**Drawing standard.** IEEE 315 / IEC 60617 for the report; signal flow
left-to-right, power top-to-bottom, faults red dashed, calibration blue dashed.

**Boards in the set:**

| Board | Function | Size | Power |
|---|---|---|---|
| **BRD-01** | **single electronics board** — power entry + DC-DC/LDO; FPGA + clock (§6.0); DAC80508 + 8× LTC1563-2 + 8 current loops + current sense; receiver (INA163 + ADA4940-2 + AD7768-4 + ADR434); FG and pen connectors; arm STOP latch (no panel E-stop) | ~250 × 200 mm, 4-layer | +15 V in |
| FG-01 | 8 vendor emitter coils on machined plates (passive; mechanically separate) | 8 × ~91 mm PCB + 2 plates | passive |
| PEN-01 | Coil B + cable + mini-XLR | pen | passive |
| PMS-01 | Pico 2 + XYZ stage + camera | bench | 5 V |
| FPGA | **XC7A35T-1FTG256C** (PS-less; 50T same-footprint upgrade), QSPI config, USB-UART (§6.0) | FTBGA-256, 15×15 mm | 1.0 / 1.8 / 3.3 V |

**Board count.** Decision #10 locks **one box with an internal shield partition**, not a board
count. Since 2026-10-28 the electronics is **one board, BRD-01**; the old PWR-DRV-01 /
FE-ADC-01 / FPGA-IF-01 split is now three **zones** of that board (§4, §5, §6). FG-01 stays a
separate passive PCB because the 300 × 300 mm coil array sits under the tracking volume. FPGA
integration is **option D: PS-less FPGA on BRD-01** (decision #26, 2026-10-28) — §6.0.

---

## 1. System block schematic

```text
 120 V ──► ME60A1503F01 ──► +15 V_RAW         (external medical 15 V / 60 W)
                              │
 ┌────────────────────────────▼──────────────────────────────────────────┐
 │ BRD-01 — one 4-layer board, ~250 × 200 mm                             │
 │                                                                       │
 │  power entry F1/TVS/L1 ──► +15V_FUSED ──► 8× LMH6321 (unswitched)     │
 │        ├─► U147 TPSM63604 +6V ─► U144/U145/U7 ─► FPGA rails +3.3V     │
 │        │        ├─► U149 +5V_EXC ─► DAC80508 + 8× LTC1563-2           │
 │        │        └─► U146 +5VA ─► AD7768-4 + 2× ADA4940-2              │
 │        └─► U5 MGJ2 ±15V ─► U6/U2 LT3045-1/LT3093 ─► ±12VA             │
 │                                                                       │
 │   ┌────────────┐    SPI 49.152 MHz    ┌───────────────┐               │
 │   │ FPGA       │─────────────────────►│ DAC80508      │               │
 │   │ XC7A35T    │                      │ LTC1563-2 ×8  │               │
 │   │ DDS/demod/ │                      │ LMH6321 ×8    │               │
 │   │ LM solver  │◄─ 4 DOUT ──┐         └──────┬────────┘               │
 │   └────────────┘            │                │ I_coil                 │
 │                             │                ▼                        │
 │                      ┌──────┴───────┐   ┌──────────┐                  │
 │                      │ AD7768-4     │◄──│ FG J1–J8 │                  │
 │                      │ ◄ ADA4940-2  │   └──────────┘                  │
 │                      │ ◄ INA163     │        ▲                        │
 │                      └──────▲───────┘        │ R_store ×8             │
 │                             │                │                        │
 │                 pen J ◄─────┘        current-sense summer ────────────┘
 │                                                                       │
 │  ══ on-board shield fence / can: driver + DC-DC | receiver + FPGA ═══  │
 └───────────────┬───────────────────────────────────────┬───────────────┘
                 │ 8 coil pairs (twisted, star return)    │ pen cable
                 ▼                                        ▼
            FG-01 (300 × 300)                       PEN-01 (passive)
                 │
                 └────────── B field ──────────► pen coil ─► INA163
```

The FPGA is drawn inside the board boundary for the selected option D (§6.0, #26): PS-less
Artix-7 on BRD-01, with the 49.152 MHz SPI as a short on-board trace. Options A/B/C in
`fpga_integration_options.md` are the rejected evaluation trail; no SPI header or ribbon
exists in the selected design.

The two signal chains are short loops on one board: **drive** FPGA → DAC → filter → current loop →
FG coil → \(R_{store}\) → summer → ADC Ch0; **receive** pen coil → INA163 → ADA4940-2 → AD7768-4
Ch1–3 → FPGA.

---

## 2. Power tree

**Contract-governing table: decision #31, power tree v2 adopted by the user on
2026-11-25.** It supersedes the part list of #20; the ME60A1503F01 adapter and
one-board intent of #20 stand. `+15V_FUSED` is the unswitched driver rail after
F1/TVS/L1; the obsolete `+15V_DRV` name is gone and no E-stop contact interrupts
the field path (#30).

| Rail | Source | Load | Current (typ/max) | Notes |
|---|---|---|---|---|
| `+15V_FUSED` | ME60A1503F01 via F1/TVS/L1 | 8× LMH6321, U147, U5 | 1.2 A / 2.0 A (driver) | unswitched; no E-stop contact remains |
| `+6V` | U147 TPSM63604, 6.0 V at 1.024 MHz, synced to `BUCK_SYNC` | U144/U145/U7, U149/U146 via FL1/FL2 | 0.33 A / 0.71 A | `PG_6V` starts the downstream sequence |
| `+1V0_FPGA` | U144 TPS62130A | FPGA VCCINT/VCCBRAM | 0.37 A / 0.8 A | EN ← `PG_6V` |
| `+1V8_FPGA` | U145 TPS62130A | FPGA VCCAUX | 0.10 A / 0.2 A | EN ← `PG_1V0` |
| `+3.3V` | U7 TPS62130A | FPGA VCCO, AD7768 IOVDD, FT231X, logic | 0.13 A / 0.26 A (power-on surge) | EN ← `PG_1V8` |
| `+5V_EXC` | U149 TPS7A4701 | DAC80508, 8× LTC1563-2 | 0.095 A / 0.155 A | excitation rail |
| `+5VA` | U146 TPS7A4701 | AD7768-4, 2× ADA4940-2 | 0.043 A / 0.060 A | receiver rail; `D_REF` clamps ADC_REF |
| `±12VA` | U5 MGJ2D151515SC → U6 LT3045-1 / U2 LT3093 | INA163, OPA192, ADR434 buffer | see `power_tree_v2.md` §3/§9 | isolated analog; bench-check 45 kHz spur |

> **Conflict closed by #31 (2026-11-25).** `docs/phase2/power_tree_v2.md` and
> `docs/phase2/contract_change_20_draft.md` were the basis for the adoption.
> OKI-78SR-5, RV-1515D and TPS7A20 / TPS7A2033 are removed from the contract
> part list. The captured BRD-01 schematic already implements v2 (BOM
> reconciliation is tracked separately):
> `hardware/brd-01/kicad/brd-01.kicad_sch` at `ef04f63` contains
> `MGJ2D151515SC` and no `OKI-78SR`, `RV-1515`, `TPS7A20` or `TPS7A4701`
> strings; `hardware/brd-01/kicad/bom-to-cad.md:151` records the user's part
> confirmation (U5 MGJ2D151515SC, U6 LT3045EDD-1#TRPBF, U2 LT3093EMSE#TRPBF);
> `docs/phase2/brd01_component_reference.md:357` lists U5 as MGJ2D151515SC;
> `docs/phase2/brd01_wiring_manifest.md` §5 item 3 confirms the captured rails.

**Protection at the adapter input:** F1 3 A slow-blow, D1 TVS (SMBJ18A),
L1 common-mode choke, C1 1000 µF/25 V, reverse-polarity MOSFET or ideal diode.
No E-stop contact remains in the power path: +15 V_FUSED feeds the driver
continuously. An overcurrent trip still clears the hardware latch, which now
asserts the arm STOP line instead of removing the field rail.

**Power budget at 150 mA:** driver 8×0.15×15 ≈ 18 W; FPGA/ADC/analog ≈ 6 W;
losses ≈ 3 W; total ≈ 27 W of the 60 W adapter. At 250 mA the driver is ≈ 30 W;
total ≈ 40 W. The LMH6321 thermal soak, not the adapter, is the limit.

---

## 3. FG-01 field generator

| Item | Value |
|---|---|
| Coils | **8 × vendor AnserEMT Rev C PCB coil** (dual-layer, 25 turns total, 70 mm outer, 0.5 mm track / 0.25 mm gap, 1.6 mm FR4, L ≈ 79 µH, R ≈ 2.9 Ω) |
| Assembly | one coil per position, **no stacking**; 2 machined plates + M3 standoffs at the centres below |
| Centres | \(x=[-93.543,0,93.543,-68.55,68.55,-93.543,0,93.543]\) mm; \(y=[93.543,68.55,93.543,0,0,-93.543,-68.55,-93.543]\) mm |
| Orientation | vertical: 1,3,6,8; angled 45°: 2,4,5,7 |
| Tone map | coil \(i\) → tone \(i\): 20,22,24,26,28,30,32,34 kHz (FG-1 may reassign weakest → 34 kHz) |
| Connector | J20–J27, 2-pin keyed FG headers on BRD-01 (Molex 39-30-1020; `J1` is the DC barrel jack), pin 1 = drive, pin 2 = return |
| Guard | non-metal open-top ring at the ~57 mm contour (27 µT at 250 mA); removable |
| Metal rule | no metal within 150 mm of the 150 mm cube; the plates sit below the coil plane and outside the 57 mm guard contour |

The coil return is separate from the driver ground; the 8 returns meet at the
FG star point, then one cable to the driver board. Do not daisy-chain the
returns.

---

## 4. Driver section — BRD-01 zone A (was PWR-DRV-01)

### 4.1 Channel map

One eight-channel `DAC80508` (`U10`) produces all eight commands; `U11`–`U17`
do not exist. Each channel has its own LTC1563-2 reconstruction filter
(`U80`–`U87`), OPA192 loop amp (`U30`–`U37`), LMH6321 driver (`U20`–`U27`),
1 Ω sense resistor (`R20`–`R27`) and keyed FG header (`J20`–`J27` on the
connectors sheet). `J1` is the power-entry barrel jack, not an FG connector.

| Channel | DAC80508 output | LTC1563-2 | LMH6321 | \(R_{store}\) | FG connector | Tone |
|---|---|---|---|---|---|---|
| 0 | U10 ch0 | U80 | U20 | R20 1.00 Ω | J20 | 20 kHz |
| 1 | U10 ch1 | U81 | U21 | R21 1.00 Ω | J21 | 22 kHz |
| 2 | U10 ch2 | U82 | U22 | R22 1.00 Ω | J22 | 24 kHz |
| 3 | U10 ch3 | U83 | U23 | R23 1.00 Ω | J23 | 26 kHz |
| 4 | U10 ch4 | U84 | U24 | R24 1.00 Ω | J24 | 28 kHz |
| 5 | U10 ch5 | U85 | U25 | R25 1.00 Ω | J25 | 30 kHz |
| 6 | U10 ch6 | U86 | U26 | R26 1.00 Ω | J26 | 32 kHz |
| 7 | U10 ch7 | U87 | U27 | R27 1.00 Ω | J27 | 34 kHz |

\(R_{store}\) 1.00 Ω 0.1 % 0.5 W; the thesis values 0.957–1.239 Ω are the
heritage baseline, a single 1.00 Ω is the Rev A value and is calibrated per
channel. Summer scale 2.0103.

### 4.2 One channel (repeated 8×)

```text
DAC80508 ch_i ──► LTC1563-2 60 kHz ──► R1 10k ──► A1 + ──► A1 ──► Q1 LMH6321 ──► C1 100µF ──► L_coil ──► R_store ──► Vmid
                               │                                                          │
                               └── Rf 10k ◄── A2 diff amp ◄──────────────────────────────┘
                                                       ▲
                                                      Vmid = 7.5 V
```

- **A1** OPA192 error amplifier, ±12 V; **A2** OPA192 difference amplifier
  across \(R_{store}\); **Q1** LMH6321 on the unswitched +15V_FUSED driver rail.
- **Vmid** is a 7.5 V low-impedance mid-rail (10k/10k divider + 1000 µF +
  100 nF). The coil is AC-coupled by C1, so the DC operating point is 7.5 V and
  the LMH6321 output stays inside 0–15 V while the coil current is bipolar.
- The loop forces \(I_{coil}=V_{cmd}/R_{store}\). The DAC command is AC-coupled
  and scaled so 4.096 V full scale = 500 mA; 150 mA is 30 % of full scale.
- **Compensation:** lead network across A1 (Rc/Cc) tuned at 34 kHz with the
  real coil + cable; phase margin ≥45°. The exact values are a DRV-2 bench
  item; start with the thesis values and adjust.
- **Fault:** A3 comparator (TLV3201) on the \(R_{store}\) peak; threshold
  1.2 × max current; open-drain wired-OR to the fault bus and the FPGA.
- **No DC current:** C1 blocks DC; the mid-rail sets the operating point.

### 4.3 DAC interface

| Signal | Source | Destination | Rate |
|---|---|---|---|
| DAC_SCLK | FPGA PLL ÷2 | DAC80508 SCLK | **49.152 MHz** |
| DAC_CS | FPGA | DAC80508 SYNC/CS | one per 24-bit frame |
| DAC_SDI | FPGA | DAC80508 SDI | MSB first |
| DAC_SDO | DAC80508 | FPGA | optional readback |
| DAC_REF | DAC80508 internal 2.5 V | — | gain 2 → 0–5 V default; **OPEN follow-up:** `power_tree_v2.md` §7 D2 gives a 0.3–4.6 V DDS limit on `+5V_EXC` (see `icd/dac_fpga.md` §3) |

Each 24-bit frame carries one channel; 8 channels = **192 bits**; at 49.152 MHz
the data burst is **3.906 µs** inside the **5.005 µs** update period (199.805 kSPS =
32.768 MHz ÷164). **The DAC80508 has no LDAC pin:** the simultaneous update is a
9th 24-bit frame writing **TRIGGER (0x05) bit 4 = 1**; 216 bits = **4.394 µs**.
Set SYNC (0x02) = 0x00FF once at init to put all 8 channels in synchronous mode. The reconstruction filter is the **LTC1563-2 4th-order Butterworth,
60 kHz** (one resistor per channel); the image at 165.8 kHz is −35.3 dB.

### 4.4 Current-sense summer

```text
R_store0 ──► A10 buffer ──┐
R_store1 ──► A11 buffer ──┤
   …                      ├──► A20 summing amp (×2.0103) ──► AD7768 Ch0
R_store7 ──► A17 buffer ──┘
```

- Buffers: OPA2192 (4 dual) on ±12 V; summing amp OPA192.
- Summer output: 8 tones, each 0.30 V RMS at 150 mA; peak sum <2.5 V, within
  the ±4.096 V ADC range.
- Per-channel peak comparators: TLV3201 ×8 (`U60`–`U67`). Their `/driver/TRIP_REF`
  input comes from `R710` 52.3 kΩ 0.1 % between +3.3 V and the reference node
  and `R711` 10 kΩ 0.1 % from that node to GND, bypassed by `C710` 100 nF:
  \(V_{REF}\approx 3.3\times 10/(52.3+10)\approx 0.53\) V. There is no shunt
  reference part. Open-drain fault bus to the FPGA and the hardware STOP latch.
- The summer is the \(Y_I\) phase reference; its group delay is fixed and
  absorbed by κ.

### 4.5 Arm STOP / latch chain

```text
+15 V_RAW ──► F1 ──► +15 V_FUSED ──► 8× LMH6321      (no E-stop contact)

U4.P4 ──► PICO_STOP_REQ_N ──┐
            R754 pull-down  ├──► U755 74LVC1G08 ──► PICO_STOP_N ──► J123.5
U753.5 (Q) ─► /power/ARM_Q ─┘        (U753.3 ~Q = no-connect)
```

- There is no panel mushroom or K2 relay on BRD-01. The field rail is never
  interrupted by a stop.
- `PICO_STOP_N` is active low. U755 (74LVC1G08) ANDs the FPGA request on
  `U755.1` with the latch output `U753.5 (Q)` on `/power/ARM_Q` → `U755.2`;
  either input low asserts STOP to the arm. `U753.3 (~Q)` is the **no-connect**,
  not the arming signal — netlist evidence in
  `docs/phase2/brd01_wiring_manifest.md` §5 item 1.
- U753 is cleared at power-up/brownout by U751 and on overcurrent via
  `/DRIVER_FAULT_N` → U752. With CLR asserted, `Q=0`, so STOP is asserted; the
  latch is armed by SW750 (`Q=1`), which passes the FPGA request through.
- R754 pulls the FPGA-side request low while the FPGA is unconfigured.
- The watchdog is an **internal timer in the FPGA PL**. No TPS3823 or other
  external supervisor part exists on BRD-01, and no watchdog part or net is
  assigned in the schematic or BOM. Its only output is the FPGA request into
  U755, so it can assert STOP solely through `PICO_STOP_N`. It therefore does
  **not** restore a hardware-independent stop path: like a host request, it
  depends on the configured FPGA fabric.

---

## 5. Receiver board — BRD-01 zone B (FE-ADC)

### 5.1 One channel (pen; repeat for reference)

```text
J1 SIG+ ──► R1 100Ω ──► C1 10µF ──► INA163 +IN
J1 SIG− ──► R2 100Ω ──► C2 10µF ──► INA163 −IN
J1 SHIELD ──► chassis at FE end only
INA163 RG = 176Ω (G = 35)
INA163 OUT ──► ADA4940-2 +IN; −IN via VCM network
ADA4940-2 OUT+ ──► R3 20Ω ──► C3 470pF ─┐
ADA4940-2 OUT− ──► R4 20Ω ──► C4 470pF ─┼──► C5 100pF ──► AD7768 AIN1±
                                        ┘
```

- **Bias:** 10k 0.1 % from each INA163 input to ground after the 10 µF cap;
  the 12 µA bias current gives ~0.12 V offset, within the ±12 V common mode.
  The 10 µF cap is 0.8 Ω at 20 kHz, negligible against the 8.6 Ω coil.
- **Protection:** 100 Ω series + Schottky clamps to ±12 V; the 10 µF cap
  blocks DC. The protection capacitance is <10 pF at the connector.
- **Gain:** INA163 35×, ADA4940-2 2×; total 70×. The strongest 34 kHz tone is
  3.40 V differential, below ±4.096 V.
- **VCM:** AD7768 VCM (2.5 V) sets the ADA4940-2 output common mode; each
  output stays in 0.45–4.55 V.
- **Reference:** ADR434 4.096 V + OPA192 buffer; 10 µF + 100 nF at the ADC.
- **Clock (SC-07, decision #28):** one 32.768 MHz XO (CSX750FBC32.768M-UT) →
  33 Ω series → ADC MCLK; direct branch to the FPGA clock input (no discrete
  buffer). FPGA DDS clock = 32.768 MHz; PLL ×3 = 98.304 MHz feeds only ÷2 =
  49.152 MHz DAC SCLK; DAC update ÷164 = 199.805 kSPS; ADC ODR ÷128 =
  256 kSPS. There is no TCXO and no PLL-generated MCLK.

### 5.2 ADC channel map

| ADC channel | Input | Connector | Notes |
|---|---|---|---|
| Ch0 | current-sense summer | on-board, driver zone | \(Y_I\) |
| Ch1 | pen 1 | J122 (panel XLR J120 via J121) | moving |
| Ch2 | pen 2 | J127 (panel XLR J125 via J126) | wired, enabled when built |
| Ch3 | reference coil | J128 | fixed at FG edge |

### 5.3 ADC pin/interface summary

| Group | Signals | Notes |
|---|---|---|
| Analog inputs | AIN0±…AIN3± | differential ±4.096 V; RC network per §5.1 |
| Reference | REF1±, REF2± | 4.096 V; Ch0/1 and Ch2/3 pairs |
| Clock | MCLK, CLK_SEL | 32.768 MHz CMOS; CLK_SEL = 0 |
| Control | SYNC_IN/START, SYNC_OUT, RESET, DRDY | one-time sync; count DRDY |
| Data | DCLK, DOUT0…DOUT3 | 8.192 MHz, 4 lanes, 32-bit frames |
| SPI | SCLK, SDI, SDO, CS | configuration only |
| Power | AVDD1, AVDD2, IOVDD, AVSS, DGND | +5VA, +5VA, +3.3V |

Pin numbers are per the AD7768-4 Rev.D datasheet; the EDA symbol must use the
datasheet pinout, not a generic 64-LQFP.

---

## 6. FPGA interface — BRD-01 zone C (was FPGA-IF-01)

### 6.0 FPGA integration — D selected (2026-10-28)

**PS-less FPGA on BRD-01: XC7A35T-1FTG256C** (33k logic cells, 1.8 Mb BRAM, 90 DSP, 170 I/O,
1.0 mm FTBGA), with the **XC7A50T-1FTG256C** as the same-footprint upgrade. QSPI config flash,
USB-UART host link, 3.3 V HR banks. No PS, no DDR3, no Linux — the host PC does UI, logging and
camera/viz.

DDR3 is a **PS requirement, not a pose requirement**: the pipeline needs ~10–25 kB of BRAM and
0.6–0.7 GFLOP/s, not a memory controller. Dropping the PS removes DDR3, the 6-layer stack, PMIC
sequencing and the boot image, and keeps the 49.152 MHz SPI on-board. A/B/C were rejected: all
three keep the PS and therefore DDR3, and C also leaves the 49 MHz SPI on a header. Evaluation
trail: `docs/phase2/fpga_integration_options.md`; decision row #26.

**Checks before layout:** every used bank must be HR (3.3 V); 35T→50T FTG256 pin compatibility;
HLS filament/LM fit on the 35T — the 50T is the escape.

The pin list below is the on-board net assignment (no cable).

| Pin | Signal | Direction (FPGA) | Notes |
|---|---|---|---|
| 1 | +3.3 V | power | 0.5 A |
| 2 | +3.3 V | power | 0.5 A |
| 3 | GND | power | — |
| 4 | GND | power | — |
| 5 | MCLK_ADC | in | 32.768 MHz from XO |
| 6 | DCLK | in | 8.192 MHz from ADC |
| 7 | DOUT0 | in | ADC Ch0 |
| 8 | DOUT1 | in | ADC Ch1 |
| 9 | DOUT2 | in | ADC Ch2 |
| 10 | DOUT3 | in | ADC Ch3 |
| 11 | DRDY | in | 256 kHz |
| 12 | SYNC_START | out | one-time |
| 13 | ADC_RESET | out | active low |
| 14 | ADC_SPI_SCLK | out | config |
| 15 | ADC_SPI_MOSI | out | config |
| 16 | ADC_SPI_MISO | in | config |
| 17 | ADC_SPI_CS | out | config |
| 18 | GND | power | — |
| 19 | DAC_SCLK | out | 49.152 MHz |
| 20 | DAC_CS | out | one per 24-bit frame |
| 21 | DAC_SDI | out | MSB first |
| 22 | DAC_SDO | in | optional readback |
| 23–35 | spare | — | **13** pins freed (no LDAC pin; 8-lane DAC removed) |
| 36 | GND | power | — |
| 37 | — | — | no-connect (was ESTOP_STATUS opto input; removed by #30) |
| 38 | WATCHDOG_KICK | out | internal PL watchdog output; contributes to the FPGA `PICO_STOP_REQ_N` request into `U755` (netlist ball `U4.P4`), not a Pico/relay drive (#30) |
| 39 | FAULT_IRQ | in | wired-OR fault bus |
| 40 | GND | power | — |

**The FPGA clock input is the XO direct (§5.1, SC-07/#28).** The PLL ×3 output is
used only for the 49.152 MHz DAC SCLK; it does not generate ADC MCLK.

**SPI placement (option D, #26).** The 49.152 MHz SPI is a ~30–50 mm on-board
trace from the FPGA to the DAC — no header or ribbon. The hold margin is bought
back with the matched pair, the ~2.5 ns SDI delay and probe pads; a cable is not
signable at this rate.

**SPI timing constraint (49.152 MHz).** The DAC80508 needs `tSDIH` = 10 ns and the half
period at 49.152 MHz is 10.17 ns, so hold margin is **0.17 ns** — about 3 cm of trace.
On-board that is recoverable: route SCLK/SDI as a matched pair over continuous ground,
33 Ω series at the FPGA pin, probe pads at the DAC, and add the **~2.5 ns SDI delay** in
the FPGA (balanced result 7.7 / 12.7 ns → 2.7 ns margin each). See
`docs/handoff/m16-fpga-handoff.md` §4.5.

---

## 7. Channel, tone, and connector map

| Tone | Coil | Driver | \(R_{store}\) | FG J | ADC Ch | Pen |
|---|---|---|---|---|---|---|
| 20 kHz | 1 | 0 | 1.00 Ω | J20 | Ch0 (Y_I) / Ch1 | pen 1 |
| 22 kHz | 2 | 1 | 1.00 Ω | J21 | Ch0 / Ch1 | pen 1 |
| 24 kHz | 3 | 2 | 1.00 Ω | J22 | Ch0 / Ch1 | pen 1 |
| 26 kHz | 4 | 3 | 1.00 Ω | J23 | Ch0 / Ch1 | pen 1 |
| 28 kHz | 5 | 4 | 1.00 Ω | J24 | Ch0 / Ch1 | pen 1 |
| 30 kHz | 6 | 5 | 1.00 Ω | J25 | Ch0 / Ch1 | pen 1 |
| 32 kHz | 7 | 6 | 1.00 Ω | J26 | Ch0 / Ch1 | pen 1 |
| 34 kHz | 8 | 7 | 1.00 Ω | J27 | Ch0 / Ch1 | pen 1 |

Ch2 is pen 2 (same eight tones); Ch3 is the reference coil. The FG-1 field map
may swap coil→tone assignment; the tone set and 2 kHz spacing are fixed.

---

## 8. Grounding, shielding, enclosure

- **Star ground** at the adapter input on BRD-01. Driver-zone power ground and
  receiver-zone analog ground are separate planes; join at one point under the
  power entry, not under the ADC.
- **Receiver zone:** analog ground plane under the INA163/ADA4940/ADC; digital
  ground under the ADC IOVDD/DOUT; join at the ADC AGND/DGND pins.
- **On-board shield fence / can** between the driver + DC-DC zone and the
  receiver + FPGA zone, tied to chassis at the feedthrough. The only cables
  leaving the board are the FG coil pairs, the pen cable, and the panel wiring —
  no ADC or DAC ribbon.
- **Pen cable:** shield terminated 360° at the FE end only; coil-to-shield open
  at the pen; pigtail <10 mm.
- **FG cables:** twisted pair per coil, kept away from the pen cable; returns
  star at the FG board.
- **Enclosure:** aluminum 400×300×150 mm, one box, internal partition plus the
  on-board can, fan with
  filter; no metal within 150 mm of the tracking volume. The ICNIRP guard is
  non-metal and removable.
- **Arm STOP (#30):** no panel E-stop on BRD-01; STOP is the AND of the host
  request and the arm latch, and the field rail is unaffected. Tracker stays up
  through a STOP; the last hardware-independent stop path is gone.

---

## 9. Bring-up order

1. **Power only:** adapter, +15V_FUSED, +6V, +1V0_FPGA / +1V8_FPGA / +3.3V,
   +5V_EXC, +5VA, ±12VA (v2 tree, decision #31, §2); check rails, ripple, no
   load; then verify the unswitched driver rail.
2. **FG continuity:** 8 vendor coils, R ≈ 2.9 Ω, L ≈ 79 µH (AnserEMT Table 2,
   decision #27; thesis heritage 2 Ω / 70 µH), no shorts; measure each board.
3. **Driver one channel:** 150 mA into a 2.9 Ω / 79 µH load; step response, phase
   margin, THD; then all 8.
4. **Current sense:** known current, Ch0 V/I/phase; comparator trip.
5. **FE one channel:** Helmholtz \(A_{sens}(f)\), noise, CMRR; then ADC.
6. **ADC:** 4-channel capture, 32.768 Mbit/s, zero dropped frames; FFT/SINAD.
7. **DDS/DAC:** 8 tones, FTWs, amplitude/phase; DAC80508 216-bit frame (8 data +
   TRIGGER, `icd/dac_fpga.md`); LTC1563-2 filter; current-sense FFT.
8. **Closed loop:** demod → solver → pose on the 7×7 grid; κ.
9. **System:** arm STOP (field and pose continue), watchdog, thermal soak, EMI,
   1-hour run.

---

## 10. EDA capture checklist (next step)

- [ ] KiCad project per board, IEEE 315 symbols, 4-layer stackup.
- [ ] AD7768-4 64-LQFP symbol from the datasheet, not generic.
- [ ] DAC80508 WQFN-16, LTC1563-2 SSOP-16, LMH6321 SO PowerPAD, INA163 SOIC-14, ADA4940-2 LFCSP.
- [ ] Thermal relief/copper pour on the LMH6321 exposed pad and the 180 cm²
      driver board.
- [ ] Length-match the 4 DOUT lanes and DCLK; keep the 32.768 MHz clock away
      from the analog input.
- [ ] Star-ground and partition drawing; no metal within 150 mm of the volume.
- [ ] Connector pin numbers and cable schedule frozen before BOM order.

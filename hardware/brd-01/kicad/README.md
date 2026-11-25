# BRD-01 KiCad project

Open [brd-01.kicad_pro](brd-01.kicad_pro) in KiCad **10.0.8** with the
official 10.0.8 symbol and footprint libraries installed. The root schematic
contains five populated sheets. The three signals that cross sheets
(`ESTOP_ASSERTED`, `DRIVER_FAULT_N`, `BUCK_SYNC`) use hierarchical labels and
sheet pins on the root; power rails use power symbols.
Title block rev **0.1**; KiCad ERC reports **zero violations** on the full
hierarchy. The schematic is complete as an engineering draft and carries the
following release holds.

| Page | Sheet | Captured | Open |
|---|---|---|---|
| 2 | Power | Fused entry and corrected TVS polarity, draft hardwired K1/K2 chain, opto status and hardware overcurrent latch with manual rearm, FPGA rail sequencing, +5VA regulator fed from fused 15 V, and the approved MGJ2D151515SC/LT3045EDD-1#TRPBF/LT3093EMSE#TRPBF ±12VA chain | Verify converter headroom and combined receiver and driver load against the 67 mA per-rail rating. Relay selection is the one open hardware item; K1/K2 stay draft and off the BOM. Verify startup, rail load and dissipation against the 67 mA per-rail rating, clamp/release time, restart behavior and input protection. The 3.15 A fuse cartridge is a recorded deviation from the 3.00 A spec. |
| 3 | Driver | DAC80508, eight 60 kHz reconstruction filters, coil outputs and sense returns, sense summer, individual comparator test nets, nominal 253 mA prototype trip, nominal 280 mA peak LMH6321 clamps and a shared active-low fault output to the FPGA | Measure prototype command scaling and loop compensation with the coil and cable, verify coil-return midpoint impedance, LMH6321 clamp tolerance and thermal validation, trip threshold tolerance, and hardware latch pulse capture and relay drop-out. Confirm the summer scale and phase on the bench. |
| 4 | Receiver | AD7768-4 in four-lane SPI-control configuration, ADR434 reference, Ch0 current sense, Ch1 pen 1, Ch2 pen 2 and Ch3 fixed-reference paths | Ch2 and Ch3 reuse the Ch1 circuit provisionally. Reconcile the resulting INA163 and ADA4940-2 quantities with the BOM, verify reference-coil gain, and check ADC settling, reference buffer stability and phase matching. |
| 5 | FPGA | FTG256 ball assignments, QSPI and JTAG, shared clock, USB-UART and Pico signals | Verify timing, power and bypass allocation on the target device. Program FT231X CBUS2 for VBUS sensing and verify USB ESD and power-off behavior. |
| 6 | Connectors | Eight keyed FG headers, two pen panel connectors and JST harnesses, provisional JST GH headers for reference and Pico, plus USB-C with data and CC ESD clamps | Freeze pen and reference polarity and verify mating harnesses, Pico 3V3 use and shield termination. Approve USB shield bonding, enclosure fit and FG mating hardware. |

The BRD-01 draft uses the LTC1563-2 high-speed unity-gain application and the
LMH6321 single-supply ground-pin bias configuration. The driver and receiver
still need circuit review before layout. See [LTC1563-2 data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/156323fa.pdf)
and [LMH6321 data sheet](https://www.ti.com/lit/ds/symlink/lmh6321.pdf).

The 35T and 50T FTG256 tables agree on all 256 ball entries and the KiCad
symbol matches their pin names. The FPGA user signals and QSPI use 3.3 V
HR Banks 14, 15 and 34. Migration still needs implementation timing and
power verification. See the [XC7A35T table](https://download.amd.com/adaptive-socs-and-fpgas/developer/adaptive-socs-and-fpgas/package-pinout-files/a7packages/xc7a35tftg256pkg.txt)
and [XC7A50T table](https://download.amd.com/adaptive-socs-and-fpgas/developer/adaptive-socs-and-fpgas/package-pinout-files/a7packages/xc7a50tftg256pkg.txt).

The FPGA sheet and USB-C CC resistors use standard 0603 footprints for
the digital resistors and small bypass capacitors. The FPGA sheet uses
0805 for its 4.7 µF and 10 µF capacitors. These package assignments are
for layout. Confirm effective capacitance at the rail voltage when
selecting the exact capacitor part numbers.

The receiver and driver use 0603 for the small signal resistors and
capacitors, 0805 for 1 µF, 1206 for 10 µF, and 1 mm exposed pads for
driver probe points. Check resistor matching, capacitor dielectric and
effective capacitance when selecting orderable parts. Driver shunts
reserve provisional 2512 footprints pending part selection. The
coil-coupling capacitors provisionally use TDK CAA572X7R1E107M670LJ
and its series-specific footprint. C30 and
C282 have provisional 1000 µF Panasonic parts and footprints.

The power sheet assigns 0603 through 1210 footprints to regulator and
interlock passives. Qualify the two ±12VA output capacitor groups at
their actual bias voltage. Each LDO requires at least 10 µF effective
output capacitance. Place C5/C782 by U6 and C4/C783 by U2, with the
OUTS connection taken at the local capacitor pad.
[LT3045-1 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/30451fa.pdf) ·
[LT3093 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3093.pdf)

L140 and L141 use Coilcraft XFL4020-222MEC with the KiCad
`Inductor_SMD:L_Coilcraft_XxL4020` footprint. TI lists the 2.2 µH
XFL4020-222 family for the TPS62130A and recommends the nominal
2.2 µH / 22 µF output filter combination. Check peak current and
transient response against the implemented FPGA rail loads.
[TPS62130A datasheet](https://www.ti.com/lit/ds/symlink/tps62130a.pdf) ·
[Coilcraft XFL4020-222](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xfl/xfl4020/xfl4020-222/)

### Sheet index

Capture is complete: every on-board symbol carries a value and a footprint.
The [BOM-to-CAD ledger](bom-to-cad.md) records the part evidence and the
release verification left on each lot. The [power tree](power-tree.md)
documents every rail, the E-stop latch and every net that crosses sheets.

| Page | Sheet | Contents |
|---|---|---|
| 2 | Power | Adapter entry, protection and EMI filter, hardware interlock, FPGA rail sequencing, +5VA regulator and the approved ±12VA chain |
| 3 | Driver | DAC80508, eight 60 kHz filters, eight current loops, sense summer, comparators and open-drain fault bus |
| 4 | Receiver | AD7768-4, ADR434 reference, Ch0 current sense and Ch1–Ch3 sensor front ends |
| 5 | FPGA | FTG256 ball map, QSPI, JTAG, clock, USB-UART and Pico signals |
| 6 | Connectors | FG headers, pen and reference connectors, Pico header, USB-C and ESD |

Two symbols remain deliberate drafts: `accubot:Draft_EStop_Mushroom_NC` and
`accubot:Draft_EStop_Relay_NO` on the power sheet. They are excluded from
the BOM and PCB and use terminal IDs for schematic wiring only, so the
interlock is a drawn proof-of-concept until relays are selected. Everything
else uses a mapped or prototype part. The pen mini-XLR stays in the BOM as
panel hardware.

### Library setup and checks

The project tables resolve `accubot` relative to `${KIPRJMOD}` at
[the shared hardware library](../../kicad/lib/). No global `accubot` table,
plugin, 3D model, or external CAD download is needed. To add more selected
parts in one batch, first check the official libraries against manufacturer
pin tables and package drawings, then curate only missing or incorrect
definitions directly in the shared library and update the ledger. Do not
commit downloaded libraries, datasheets, or per-part import projects.

From the repository root:

```bash
kicad-cli --version
kicad-cli sch erc --exit-code-violations -o /tmp/opencode/brd01-setup-erc.rpt hardware/brd-01/kicad/brd-01.kicad_sch
kicad-cli pcb drc --exit-code-violations -o /tmp/opencode/brd01-setup-drc.rpt hardware/brd-01/kicad/brd-01.kicad_pcb
mkdir -p /tmp/opencode/brd01-symbol-svg
kicad-cli sym export svg --output /tmp/opencode/brd01-symbol-svg hardware/kicad/lib/accubot.kicad_sym
```

KiCad ERC reports zero violations on rev 0.1. F1 carries the Schurter `0001.2509`
3.15 A time-delay cartridge as its MPN field; the 3.15 A rating is a recorded
deviation from the 3.00 A spec that the power owner accepted. K1 and K2 stay
draft symbols excluded from the BOM and PCB, so relay selection is the single
open hardware item. The active-low overcurrent bus reaches both the FPGA and
the hardware K2 coil inhibit. The latch clears on fault, E-stop, or supervisor
reset. A new momentary arm edge is required to energize K2. The interlock
still needs relay/contact selection and fault-injection validation. The prototype loop uses AC-coupled command scaling, a DC feedback path and provisional PI compensation. The summer uses a nominal gain of −2.000 from each input. Measure phase margin, tracking gain and polarity before operating the full array.
A nominal small-signal check used the captured 10 kΩ/100 nF sense path,
parallel 10 MΩ feedback and 330 kΩ/150 pF compensation, a one-pole 10 MHz
gain-bandwidth OPA192 model, an ideal buffer, and 70 µH + 2 Ω coil with
1 Ω shunt and 100 µF series coupling. The reduced closed-loop polynomial
has no right-half-plane poles. Its upper unity crossover is about 70 kHz
with about 80° nominal phase margin. The calculated shunt-current gain
from the filter output is 0.118 A/V at 20 kHz and 0.114 A/V at 34 kHz, so
150 mA RMS requires about 1.80–1.86 V peak at that node. Set initial DDS
amplitude below the nominal trip and trim against the shunt measurement.
Cable parasitics, real buffer and sense-amplifier dynamics, saturation,
capacitor ESR and rail transients are outside this reduced model.

The blank PCB
reports `invalid_outline` until layout adds a real outline. Put only the
released fabrication package in [fab](../fab/).

Setup verification also used a disposable project at the same relative paths
with only the standard global KiCad tables. All 19 units of the 15 curated
symbols loaded; removing the project symbol table produced 19 library errors.
Numbered symbol pins matched numbered footprint pads for the 8 official and
15 curated table pairings, including the JST pen header, and for the separate
ST TVS mapping. The follow-up ST and JST checks also verified pad geometry.

A later disposable schematic checked the JTAG symbol, panel mini-XLR, and
three draft symbols. All five resolved through the project table and
exported to the netlist. Only the panel mini-XLR and JTAG header appeared
in the fixture BOM.

Two disposable boards with outlines reported zero DRC violations: one with
`accubot:RECOM_RV-1515D_DIP24`, and one with `accubot:ST_SMBJ_DO-214AA_DS1283`
and the official JST pen header. These smoke checks verify library use, not
BRD-01 circuit capture, layout readiness, or pen harness qualification.

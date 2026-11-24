# BRD-01 BOM-to-CAD ledger

**Scope:** [SYSTEM-01](../../bom/BOM_SYSTEM-01.xlsx) Rev 0.05, sheet **BOM**
(Excel row numbers below); [ADC-01](../../bom/BOM_ADC-01.xlsx), sheet
`BOM_ADC-01`, rows 9–11 and note row 13; [PEN-ANA-01](../../bom/BOM_PEN-ANA-01.xlsx),
sheet `BOM_PEN-ANA-01`, rows 9–12 and note row 15; and the
[connector requirements](../../bom/connector_requirements.xlsx). The two
note rows provide context, not orderable parts or CAD approvals.
Compared with [SC-05 and the system contract](../../../contract/system_contract.md),
[decisions #5, #7, #8, #10, #17, #19–21 and #25–26](../../../contract/decisions_log.md)
and the [system schematic design record](../../../docs/phase2/system_schematic.md).
References below are from the BOMs or design record, not new schematic annotation.

**Result:** The tables list 8 official symbol/footprint pairings (including
the JST pen header) and 15 pairings using curated symbols. The partially
mapped PROT lot has two separate mappings: a curated symbol with a stock
footprint for the Schurter holder and a curated symbol and footprint for
the ST TVS. The provisional host USB pairing is tracked separately under
PASS-C, alongside a schematic-only JTAG symbol. The library also has the
off-board panel mini-XLR and three draft interface/control symbols. These
partial mappings leave their BOM rows open. There are 2 curated footprints
(RECOM and ST).

The tables fully map 23 SYSTEM-01 rows for CAD: 7 from the official table and
16 from the curated table, since the same `OPA192IDBVR` pairing serves rows 22
and 54. The JST header is counted once, among the 8 official pairings; its CAD
mapping does not complete row 63 or qualify the pen harness. The unresolved
PCB table lists 8 other rows or lots, including PROT and PASS-C. These
counts are not quantities to place or buy, and verified CAD mappings do
not clear circuit-level holds.

## Official KiCad 10.0.8 pairings

Numbers in the check column refer to symbol pin and same-numbered PCB pad.
The pitch in a footprint ID can refer to mating pitch, not PCB row spacing.

| BOM row / refs | Part | Official symbol | Official footprint | Pin and package evidence |
|---|---|---|---|---|
| 30 / U70 | OKI-78SR-5/1.5-W36-C | `Converter_DCDC:OKI-78SR-5_1.5-W36-C` | `Converter_DCDC:Converter_DCDC_Murata_OKI-78SR_Vertical` | [Murata W36](https://www.murata.com/-/media/webrenewal/products/power/datasheet/oki-78sr.ashx) pp. 15, 17: vertical SIP, 0.100″ pitch; 1 input, 2 common, 3 output. Not the horizontal W36H. |
| 38 / J20–J27 | Molex 39-30-1020 | `Connector_Generic:Conn_01x02` | `Connector_Molex:Molex_Mini-Fit_Jr_5569-02A2_2x01_P4.20mm_Horizontal` | [Molex SDA-5569-NA2](https://www.tme.eu/Document/0017caab327e1c52dfc75ff4d307bcaf/MX-39-30-0020.pdf) lists 39-30-1020 as 5569-02A2; right-angle two circuits with retention peg; pads 1–2 and unnumbered NPTH. §4.1/§7 calls BRD connectors J1–J8; use BOM row linkage, not the old designators. |
| 41 / U1F | XC7A35T-1FTG256C | `FPGA_Xilinx_Artix7:XC7A35T-FTG256` | `Package_BGA:Xilinx_FTG256` | [AMD ball table](https://download.amd.com/adaptive-socs-and-fpgas/developer/adaptive-socs-and-fpgas/package-pinout-files/a7packages/xc7a35tftg256pkg.txt): all 256 ball IDs and functions agree with the symbol; exact ball-ID set equals footprint pads. [UG475](https://docs.amd.com/v/u/en-US/ug475_7Series_Pkg_Pinout), FTG256: 17 mm square, 1 mm pitch. Assign footprint manually; no net-to-ball or upgrade validation here. |
| 43 / U2F | FT231XQ | `Interface_USB:FT231XQ` | `Package_DFN_QFN:QFN-20-1EP_4x4mm_P0.5mm_EP2.5x2.5mm` | [FTDI DS_FT231X](https://ftdichip.com/wp-content/uploads/2021/10/DS_FT231X.pdf) §3.1 and Fig. 9.3: QFN-20, EP 21 = GND; USB 8 D+/9 D−, 17 TXD/1 RXD, 12 VCC/20 VCCIO. Not the FT231XS. |
| 44 / U3–U4 | TLP291(GB) | `Isolator:TLP291` | `Package_SO:SOIC-4_4.55x2.6mm_P1.27mm` | [Toshiba TLP291](https://toshiba.semicon-storage.com/info/docget.jsp?did=12884&prodName=TLP291) pp. 1–2, SO4 drawing 11-3C1; 1 anode, 2 cathode, 3 emitter, 4 collector. GB is CTR rank, not a package change. |
| 47 / U5–U6 | TPS62130ARGTR | `Regulator_Switching:TPS62130A` | `Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm_ThermalVias` | [TI TPS62130A](https://www.ti.com/lit/ds/symlink/tps62130a.pdf) Table 6-1, RGT0016C: SW 1–3, GND 6/15/16/17 (EP), AVIN 10/PVIN 11–12 (symbol `VIN`), VOS 14. Rail voltages depend on external circuitry, not different regulator MPNs. |
| 58 / U13 | TPS7A2033PDBVR | `Regulator_Linear:TPS7A20xxxDBV` | `Package_TO_SOT_SMD:SOT-23-5` | [TI TPS7A20](https://www.ti.com/lit/ds/symlink/tps7a20.pdf), DBV Figure 4-4 and Pin Functions: 1 IN, 2 GND, 3 EN, 4 NC, 5 OUT. Keep selected 3.3 V `PDBVR` order code in the part value. |
| 63 / J1P,J2P are panel refs; PCB header refdes open | JST `B2B-PH-K-S` | `Connector_Generic:Conn_01x02` | `Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` | [JST PH catalog](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) pp. 1–3: keyed/shrouded top-entry THT, 5.9 × 4.5 mm body, circuit-1 mark and 2.00 ± 0.05 mm hole pitch. KiCad's Ø0.75 mm holes are within JST's Ø0.70–0.80 mm range; pins 1 and 2 map to like-numbered pads, not to assigned signals. Mates with JST `PHR-2` housing and `SPH-002T-P0.5S` crimp contacts. |

Use `accubot:IO-TXLR3-M-PS-1` for the rear-panel male solder-cup **IO Audio
`IO-TXLR3-M-PS-1`** ([manufacturer datasheet](https://ioaudiotech.com/datasheet/IO-TXLR3-M-PS-1.pdf)),
as identified by PEN-ANA-01 row 9 and Locked-CONN, despite SYSTEM row 63's
abbreviated MPN and Amphenol entry. It has no PCB footprint. The JST harness
carries only SIG+/SIG−; panel pin 1 and the separate shell node go to chassis
star per Locked-CAB C3. Physical contacts 2 and 3 are shown by number, with
signal polarity left for the cable schedule. The cable-side `IO-TXLR3-F` is
unchanged. JST pin assignment and receiver
channel population remain open. Measure the assembled total pen link, including
the internal harness and connector, against the 73 pF limit at 34 kHz (SC-05c).

## Partial PROT lot mappings

**33 / PROT, F1 (§2): Schurter OGN `0031.8201` holder only.** Place
`accubot:Fuse_Schurter_0031.8201`, which defaults to
`Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open`.
The [Schurter OGN datasheet](https://www.schurter.com/en/datasheet/typ_ogn.pdf)
Variants table identifies the open 5 × 20 mm THT holder with 22.5 mm pin
pitch, not the 25 mm `0031.8211`. The
[Schurter THT drilling drawing](https://cdn-reichelt.de/documents/datenblatt/C400/PL%20OGN-225.pdf)
specifies two Ø1.3 mm (+0.1/−0 mm) terminal holes and a Ø2.7 mm optional
center mounting hole. KiCad pins 1 and 2 match like-numbered plated pads
with Ø1.3 mm drills at 22.5 mm pitch; the footprint includes the center
hole as an unnumbered Ø2.7 mm non-plated hole.

F1 specifies the Schurter `0853.0551` transparent cover as a separate
assembly accessory. Install it after soldering and reserve clearance for
cover removal. Schurter lists IP20 with a cover and provides a separate
power-acceptance curve for the transparent version. Check the selected
cartridge dissipation against that curve at the enclosure temperature.
[Schurter cover drawing](https://nl.schurter.com/en/datasheet/typ_Accessories_for_OGN.pdf) ·
[Schurter OGN ratings](https://www.schurter.com/en/datasheet/OGN)

Keep `0031.8201` as the holder MPN, separate from the unselected 3 A
time-delay cartridge MPN. **Candidates only; neither is approved for
substitution:**

- Schurter `0001.2509` is a 5 × 20 mm time-delay cartridge with a
  published 1.5 kA interrupt rating at 300 VDC. Its 3.15 A rating exceeds
  the specified 3.00 A. Evaluate it only if the power owner accepts that
  rating after checking inrush, conductor protection and adapter fault
  behavior. [Schurter SPT data](https://www.schurter.com/en/datasheet/SPT%205x20)
- Eaton `GMD-3-R`: 3.00 A time-delay, 5 × 20 mm ferrule cartridge. The
  [Eaton catalog](https://www.eaton.com/content/dam/eaton/products/electrical-circuit-protection/fuses/bussmann-series-catalogs/bus-ele-cat-1007-flc-2018-sec-03-elx.pdf)
  GMD entry claims 32 VDC (self-certified); [Technical Data 2019](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-gmd-time-delay-glass-tube-fuses-data-sheet.pdf)
  publishes AC interrupt ratings only. The DC voltage claim is not a DC
  breaking rating.
- OptiFuse `TSC-3A`: 3 A time-lag, 5 × 20 mm cartridge. The
  [TSC datasheet](https://www.optifuse.com/optifuse_ecommerce_tools/datasheets/TSC.pdf)
  lists only AC voltage and interrupt ratings.

Before cartridge selection, the hardware owner must establish the required
DC breaking rating at the circuit voltage and prospective fault current,
verify inrush against the fuse time-current behavior, and verify covered
holder access and thermal derating in the enclosure.

**33 / PROT, D1 (§2): STMicroelectronics `SMBJ18A`, unidirectional.** Place
`accubot:SMBJ18A`; it defaults to `accubot:ST_SMBJ_DO-214AA_DS1283`.
Pin 1 (K) maps to the marked cathode pad and pin 2 (A) to the anode pad.
[ST DS1283 Rev. 14](https://www.st.com/resource/en/datasheet/smbj18a.pdf)
Fig. 14 specifies 1.62 × 2.07 mm rectangular lands, a 2.60 mm gap and a
5.84 mm outer span (4.22 mm center-to-center); Fig. 15 identifies the
cathode bar. Stock `Diode_SMD:D_SMB` has 2.50 × 2.30 mm rounded lands on
4.30 mm centers, so the same package name does not guarantee the same land
pattern. This is a CAD mapping, not surge or clamp-coordination validation.

## Curated from manufacturer sources

Curated symbols are in the shared `accubot` library. Order-only variants retain
their exact MPN in the BOM; the symbol ID can name the common physical part
(`AD7768-4BSTZ`, `ADA4940-2ACPZ`). The RECOM module uses both a custom symbol
and footprint.

| BOM row / refs | `accubot` symbol | Footprint ID | Pin and package evidence |
|---|---|---|---|
| 21 / U10 | `DAC80508MRTET` | `Package_DFN_QFN:Texas_RTE0016D_WQFN-16-1EP_3x3mm_P0.5mm_EP0.8x0.8mm` | [TI DAC80508](https://www.ti.com/lit/ds/symlink/dac80508.pdf) §6, RTE0016D: 1 REF, 6 GND, 7 VDD, 12–16 CS/SCLK/SDI/SDO-ALARM/VIO, 17 EP to GND. MRTET is midscale and has SDO, not CLR or LDAC. |
| 22, 54 / U30–U37; U5B–U8B | `OPA192IDBVR` | `Package_TO_SOT_SMD:SOT-23-5` | [TI OPAx192](https://www.ti.com/lit/ds/symlink/opa192.pdf) §5 DBV: 1 OUT, 2 V−, 3 IN+, 4 IN−, 5 V+. Row 22 lists only eight refs for ten parts. |
| 23 / U40–U45 | `OPA2192IDR` | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | [TI OPAx192](https://www.ti.com/lit/ds/symlink/opa192.pdf) §5 D: 1–3 amplifier A, 5–7 amplifier B, 4/8 V−/V+. Four active duals; two ordered spares. |
| 24 / U20–U27 | `LMH6321MR-NOPB` | `Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm` | Orderable MPN and symbol Value: `LMH6321MR/NOPB`. [TI LMH6321](https://www.ti.com/lit/ds/symlink/lmh6321.pdf) Fig. 3-1 and DDA0008B land pattern: 1 EF, 2 CL, 3 VIN, 4 V−, 5 GND, 6 OUT, 7 V+, 8 NC, 9 exposed V−. Not plain SOIC or DDPAK; thermal via placement and copper are layout work. |
| 26 / U60–U67 | `TLV3201AIDBVR` | `Package_TO_SOT_SMD:SOT-23-5` | [TI TLV3201](https://www.ti.com/lit/ds/symlink/tlv3201.pdf) §5 DBV: 1 OUT, 2 GND, 3 IN+, 4 IN−, 5 VCC. OUT is push-pull, not open drain; capture hold below. |
| 36 / U80–U88 | `LTC1563-2IGN#PBF` | `Package_SO:SSOP-16_3.9x4.9mm_P0.635mm` | [ADI 156323fa](https://www.analog.com/media/en/technical-documentation/data-sheets/156323fa.pdf) pp. 2, 7–8, 19: GN package, 0.635 mm pitch, 16 V+, 8 V−, 9 active-low EN; NC 3/5/10/12/14 should go to system ground (passive pins, not ERC no-connect). Eight active filters, one spare. |
| 42 / U1Q | `W25Q64JVSSIQ` | `Package_SO:SOIC-8_5.3x5.3mm_P1.27mm` | [Winbond W25Q64JV Rev. J](https://www.mouser.com/datasheet/2/949/w25q64jv_revj_03272018_plus-1489671.pdf) §3.1, §3.3, ordering and SS outline: 208 mil SOIC, 1 CS#, 2 IO1, 3 IO2, 4 GND, 5 IO0, 6 CLK, 7 IO3, 8 VCC. `IQ` ships with quad enabled; do not substitute a different density or 150 mil body. |
| 50 / U1; ADC-01 row 9 | `AD7768-4BSTZ` | `Package_QFP:LQFP-64_10x10mm_P0.5mm` | [ADI Rev. D](https://www.analog.com/media/en/technical-documentation/data-sheets/ad7768-ad7768-4.pdf) Fig. 11, Tables 10 and 34, p. 108 and [ST-64-2](https://mds.analog.com/api/public/content/st_64_2.pdf): 64 pins, 10 mm body, 0.5 mm pitch, no EP. Pin 20: leave floating when FORMAT0 is low (four DOUT lanes, as locked in the [ADC ↔ FPGA ICD](../../../contract/icd/adc_fpga.md)); connect to DGND through a pull-down resistor when FORMAT0 is high (DOUT0 only). Pins 22–23 are always DNC. SC-05 locks `-RL7`; tray/RL/RL7 are the same CAD package. Do not use the separate eight-channel AD7768 pinout. |
| 51 / U2; ADC-01 row 11 | `ADR434BRZ` | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | [ADI Rev. N](https://www.analog.com/media/en/technical-documentation/data-sheets/adr430_431_433_434_435.pdf) Figs. 2 and 47: R-8; VIN 2, GND 4, TRIM 5, VOUT 6, COMP 7, DNC 1/8, NIC 3. VIN ≥6.1 V; capture hold below. |
| 52 / U3 | `INA163UA` | `Package_SO:SOIC-14_3.9x8.7mm_P1.27mm` | [TI INA163](https://www.ti.com/lit/ds/symlink/ina163.pdf) p. 2 and package D: gain-set 3/12, inverting 4/noninverting 5, sense 8, output 9, REF 10, V− 6/V+ 11. |
| 53 / U4 | `ADA4940-2ACPZ` | `Package_CSP:LFCSP-24-1EP_4x4mm_P0.5mm_EP2.5x2.5mm` | [ADI Rev. E](https://www.analog.com/media/en/technical-documentation/data-sheets/ADA4940-1_4940-2.pdf) Fig. 6, Table 13, Fig. 79: CP-24-7, EP 25 to −VS or ground. Stock symbol mislabels supply pads 3/4, 9/10, 15/16, 21/22 as feedback; curated symbol follows Table 13. SYSTEM says LFCSP-16; that is not this locked dual part. Confirm the order suffix without changing the part family. |
| 55 / U9 | `RV-1515D` | `accubot:RECOM_RV-1515D_DIP24` | [RECOM RV Rev. 3-2024](https://recom-power.com/pdf/Econoline/RV.pdf) pp. 1, 5: 15 V input, dual ±15 V; 14 leads in sparse DIP24 outline, 2.54 mm grid, 15.24 mm row spacing, Ø1.00 mm nominal drill. −VOUT 8/17, COM 10/15, +VOUT 12/13; six installed NC leads have pads. Do not use the single-output pinout or a full DIP24 footprint. |
| 56 / U10B, U11B | `TPS7A4701RGWR` | `Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias` | [TI TPS7A47](https://www.ti.com/lit/ds/symlink/tps7a47.pdf) Table 4-1, RGW0020A: 5×5 mm, IN 15/16, OUT 1/20, GND 7/21 EP. Stock symbol omits optionally tieable pads 2/17/18/19. This symbol exposes all pads. |
| 57 / U12 | `TPS7A3301RGWR` | `Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias` | [TI TPS7A33](https://www.ti.com/lit/ds/symlink/tps7a33.pdf) §5 Pin Functions, RGW0020A: IN 15/16, OUT 1/20, GND 7/21 EP. Stock symbol omits optionally tieable pads 2/4–6/8–12/17–19. This symbol exposes all pads. |
| 59 / Y1 | `CSX750FBC32.768M-UT` | `Oscillator:Oscillator_SMD_SeikoEpson_SG8002CA-4Pin_7.0x5.0mm` | [Citizen CSX-750F solder pad layout](https://media.digikey.com/pdf/Data%20Sheets/Citizen%20PDFs/CSX-750FC,FB,FJ.pdf): 7×5 mm, 1 OE, 2 GND, 3 OUT, 4 VDD. The Epson footprint has matching 1.8×2.0 mm pad extents, 5.08×4.20 mm centers and pin-1 orientation; KiCad rounds pad corners. No Epson part substitution. |

### Approved BRD-01 power capture

`accubot:MGJ2D151515SC` defaults to the stock KiCad footprint
`Converter_DCDC:Converter_DCDC_Murata_MGJ2DxxxxxxSC_THT`. The
[Murata MGJ2 datasheet](https://www.mouser.com/datasheet/2/281/1/kdc_mgj2-2941063.pdf)
specifies 13.5–16.5 V input, dual ±15 V at up to 67 mA per rail, and
pins 1 +VIN, 2 −VIN, 5 −VOUT, 6 COM and 7 +VOUT. The pads are numbered
the same as the pins and match the stock MGJ2D footprint at 2.54 mm pitch.
The [distributor listing](https://www.digikey.ca/en/products/detail/murata-power-solutions-inc/MGJ2D151515SC/5825461)
marks the part obsolete. The user confirmed the existing budget-approved parts as the BRD-01 selections: U5 MGJ2D151515SC, U6 LT3045EDD-1#TRPBF and U2 LT3093EMSE#TRPBF. The KiCad schematic uses those parts. The legacy BOM and [decision #20](../../../contract/decisions_log.md) still list the earlier converter and LDOs and require separate reconciliation.

#### ±12VA quiescent load check

The netlist places U30–U38 and U40–U43 on both rails (17 amplifier
channels) and U103 on the positive rail only. U104, U106 and U107
add three INA163 loads to both rails. Using the datasheet no-output-load
figures, the amplifiers alone account for 48 mA typical on +12VA and
47 mA typical on −12VA. Using the tabulated maximum figures at their
datasheet test conditions gives 57.6 mA and 56.4 mA, respectively.
[TI OPAx192](https://www.ti.com/lit/ds/symlink/opa2192.pdf) ·
[TI INA163](https://www.ti.com/lit/ds/symlink/ina163.pdf)

Allowing the nominal LDO operating currents (2.3 mA and 2.35 mA) on
top of those maximum amplifier figures leaves about 7.1 mA on the
positive converter output and 8.3 mA on the negative output against
the 67 mA per-rail rating. This is a screening estimate. The residual
must cover the positive-rail ADR434, regulator control currents above
nominal, signal and ADC reference drive, and any other bias loads.
Measure both raw converter output voltages and currents at startup,
idle and simultaneous eight-tone operation with all receiver paths
populated, and check regulation with the resulting asymmetric loads.
[ADI LT3045-1](https://www.analog.com/en/products/LT3045-1.html) ·
[ADI LT3093](https://www.analog.com/en/products/lt3093.html) ·
[ADI ADR434](https://www.analog.com/en/products/ADR434.html)

## Unresolved PCB rows

| BOM row / refs | Rev 0.1 state |
|---|---|
| 27 / R20–R27 | For schematic capture use `Device:R`, 1 Ω, ±0.1%, ≥0.5 W. The searched 1206 options did not verify that combination. [Thin Film Technology TFT-DMS-165-1](https://www.thin-film.com/wp-content/uploads/2023/03/TFT-DMS-165-1.pdf) pp. 1–2 factory-code candidate: `TF2512HQ1R00B-T4`, two-terminal 2512, 1 Ω, ±0.1%, 1 W per the series table. CAD reserves the two-terminal `Resistor_SMD:R_2512_6332Metric` footprint provisionally based on the 6.35 × 3.20 mm body. Confirm the exact combination, MOQ, lead time and land pattern with the factory before release. |
| 28 / C20–C27 | Prototype C212, C220, C228, C236, C244, C252, C260 and C268 use TDK CAA572X7R1E107M670LJ with `accubot:TDK_CAA572`. Electrical qualification remains open. |
| 29 / C30–C31 | The schematic follows §2 and §4.2 with two provisional 1000 µF reservoirs. C30 on +15V_FUSED uses Panasonic EEUFR1V102 (35 V, Ø12.5 mm) and C282 on VMID_7V5 uses EEUFR1E102 (25 V, Ø10 mm). Both have 5 mm lead pitch and pin 1 positive. Confirm enclosure clearance, C30 inrush/filter damping and C282 ripple and polarity during shutdown. Reconcile C282 with the workbook’s C31 reference. [Panasonic FR series](https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1259.pdf) |
| 32 / K2 | Kept as `accubot:Draft_EStop_Relay_NO` for the coil and NO power contact intended to switch +15 V_DRV. The user confirmed the draft capture as the rev 0.1 state; K1/K2 stay excluded from the BOM and PCB. Relay selection is the one open hardware item. See [K1/K2 roles](#k1k2-intended-roles-and-capture-hold). |
| 33 / PROT | [Protection inventory](#prot--input-protection): holder, cover, TVS, input filtering and reverse protection captured; Schurter `0001.2509` cartridge recorded with the 3.15 A deviation. |
| 34 / PASS-A | [Driver inventory](#pass-a--driver-and-excitation): loop, filter, mid-rail, current-sense, fault and access parts captured; values are prototype and need bench verification. |
| 45 / PASS-C | [Digital inventory](#pass-c--fpga-and-host): digital passives, JTAG, host USB support and test access captured; supervisor/watchdog open. |
| 60 / PASS-B | [Receiver inventory](#pass-b--receiver-and-adc): four front ends, ADC support and sensor connectors captured on Ch1–Ch3 templates; population and gain reconciliation open. |

### K1/K2 intended roles and capture hold

**User clarification of intended circuit roles only.** This is not approval
of the safety design, a part selection, or a contract change.

- **K1** is a separate panel-mounted, latching, normally closed mushroom
  pushbutton. Schneider Harmony `XB4BS8444` (2 NC, turn-to-release) is a
  datasheet reference only, not a final selection. K1 has no BRD-01 footprint.
- **K2** is a force-guided electromechanical relay. Its normally open power
  contact is intended to switch +15 V_DRV directly. A linked normally closed
  contact may be used for feedback, but none is assigned. Omron `G7SA` is an
  example family only; no model, coil, or suffix has been chosen.

Use `accubot:Draft_EStop_Mushroom_NC` for the intended K1 contact and
`accubot:Draft_EStop_Relay_NO` for the intended K2 coil and NO contact.
Both use functional terminal IDs and are excluded from the BOM and PCB.
An exact part symbol will carry the selected terminal numbering and any
additional contacts.

J750 is the PCB termination for the panel harness. The provisional
Phoenix Contact `1715721` terminal block uses a horizontal 5.08 mm
footprint. Pin 1 feeds the panel NC contact from the fused 15 V rail,
and pin 2 returns from that contact to the relay coil and status circuit.
Confirm wire size and enclosure access with the panel assembly.
[Phoenix Contact drawing](https://www.phoenixcontact.com/gb/products/1715721/pdf)

D140 uses the provisional Nexperia `PMEG4010CEH,115` 40 V, 1 A
Schottky with a SOD-123F footprint. The cathode connects to the switched
coil feed. A diode across the coil limits the switch voltage and slows
coil current decay. Measure contact opening and the decay of driver
current for both a panel stop and an overcurrent trip. Qualify the clamp
against the selected K2 coil and the Q750 drain voltage limit.
[Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/PMEG4010CEH.pdf)

SW750 is the prototype on-board rearm control. The Omron
`B3F-1002-G` is a gold-contact, normally open tactile switch
that fits the 6.5 × 4.5 mm hole pattern. The 10 kΩ pull-up
provides approximately 330 µA when pressed. Keep the rearm control
accessible in the enclosure and verify behavior with switch bounce
and a held switch during stop release.
[Omron B3F datasheet](https://components.omron.com/us-en/datasheet_pdf/A070-E1.pdf)

Schematic §4.5 says K2 removes +15 V_DRV but also says its NO contact
“feeds the LMH6321 enables.” The latter cannot refer to a chip enable pin:
the LMH6321 has none. This ledger records the clarified intent without
rewriting the design record.

Before exact CAD mapping, the power/driver owner must establish the actual
switched DC load, inrush and interrupt duty; reconcile the control and coil
supply with the BOM's 15 V coil entry; resolve contact allocation and
feedback; and confirm restart behavior and stop validation.

The Omron G7SA 12 V coil has a 13.2 V maximum at the datasheet
reference temperature, below the nominal 15 V feed. Its 18 V coil
has a 13.5 V must-operate limit at 23 °C, leaving no pickup margin at
the converter's 13.5 V minimum input before wiring and switch drops.
[Omron G7SA specifications](https://www.ia.omron.com/products/family/386/specification.html)

TE Schrack `2-1415538-8` is a PCB relay candidate with a native 15 V,
321 Ω coil (about 47 mA at nominal voltage) and two changeover poles.
Its linked contacts could use the NO path of one pole for driver power
and the NC path of the other for feedback if specified. The published
250 VAC rating does not establish the DC interruption capability
for this load. TE lists the part as active but unavailable directly,
and DigiKey lists it as nonstock. Resolve prototype sourcing and
obtain DC contact limits before assigning K2.
[TE part data](https://www.te.com/en/product-2-1415538-8.html) ·
[DigiKey listing](https://www.digikey.com/en/products/detail/te-connectivity-potter-brumfield-relays/2-1415538-8/22850162)

### PASS-C host USB: provisional CAD mapping only

**45 / PASS-C: GCT `USB4110-GF-A`, preferred provisional mapping.** Pair
`Connector:USB_C_Receptacle_USB2.0_16P` with
`Connector_USB:USB_C_Receptacle_GCT_USB4110`. The [GCT USB4110 drawing](https://gct.co/files/drawings/usb4110.pdf),
Rev B4, sheet 1, matches the stock footprint's 17 distinct identifiers
(16 contacts plus `SH`), 12 physical signal lands, four SMT shell lands and
two Ø0.65 mm locating holes. Only contacts with the same function share a
land, including A1/B12, A12/B1, A4/B9 and A9/B4.

The smallest nominal clearance from a locating-hole edge to the rounded
A1 or A12 copper land is 0.1944 mm. [JLCPCB's rigid PCB capabilities](https://jlcpcb.com/capabilities/)
list 0.20 mm for NPTH-to-track clearance. Confirm how JLCPCB applies the
rule to these land corners before using the stock geometry for layout.
Confirm the board-edge datum (inferred from the drawing's front face),
panel fit and shell load support. The stock footprint references a STEP
model that is absent from the local KiCad installation. CC, VBUS
sense/backfeed, ESD, shield termination and routing remain open.

**Fallback only: GCT `USB4105-GF-A`.** Pair
`Connector:USB_C_Receptacle_USB2.0_16P` with
`Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal`.
The [GCT USB4105 drawing](https://gct.co/files/drawings/usb4105.pdf), Rev B4
(18 Dec 2023), sheet 1, is the comparison basis:

- All 17 distinct pin and pad identifiers match, including `SH`. The 16
  contact identifiers use 12 physical lands: eight 0.30 × 1.15 mm and four
  0.60 × 1.15 mm. The shared lands pair only same-function contacts; this
  does not approve circuit wiring.
- The footprint matches two 0.60 × 1.70 mm and two 0.60 × 1.40 mm plated
  shell slots, two Ø0.65 mm non-plated holes, and 7.35 mm from the board
  edge to the signal land centers (to drawing precision).

**Board thickness for this comparison:** BRD-01 is approved at 1.6 mm nominal,
standard JLCPCB fabrication. [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/)
specifies ±10% for thickness ≥1.0 mm and gives 1.44–1.76 mm finished for 1.6 mm
(1.60 ± 0.16 mm).

The GCT side view dimensions `S ± 0.15 mm` from the seating plane at the
underside of the SMT solder tails to the shell stake tip. `S` is not the
signal-tail length; the rear-view 0.60 mm callout is for the locating peg,
not the `060` stake suffix. The ordering grid supplies the three nominal `S`
values. Assuming the seating plane is flush with the component-side surface
at the slot and neglecting local standoff, the depth remaining below the
tip is finished board thickness minus `S`. The extremes pair the thinnest
board with the longest stake, and the thickest board with the shortest stake.

| Stake suffix | Nominal `S` (mm) | Min–max `S` (mm) | Tip recess at 1.60 mm (mm) | Min–max tip recess (mm) |
|---|---:|---:|---:|---:|
| Blank | 0.95 | 0.80–1.10 | 0.65 | 0.34–0.96 |
| `060` | 0.60 | 0.45–0.75 | 1.00 | 0.69–1.31 |
| `120` | 1.20 | 1.05–1.35 | 0.40 | 0.09–0.71 |

All three tips stay inside the plated slots under those assumptions. That
is a geometric result, not a solder-fill prediction or an incompatibility
finding. [GCT's USB4105 pin-in-paste guidance](https://gct.co/news/pin-in-paste)
describes through-hole shell stakes, paste volume and possible overprinting
on thicker boards. Neither it nor the drawing or
[GCT product spec A3](https://gct.co/download?type=PDFSpecification&name=usb4105-spec.pdf)
explicitly permits or forbids partial insertion or requires protrusion for
this build. The [JLCPCB pin-in-paste guide](https://jlcpcb.com/blog/pin-in-paste-through-hole-reflow-stencil-guide)
gives typical lead protrusion and discusses barrel fill, not acceptance for
these slots.

Keep the suffix, assembly fit and enclosure fit provisional. Before choosing
a suffix, obtain GCT's written allowable board-thickness range or minimum
stake engagement/protrusion for that variant, and the assembler's written
acceptance of the actual plated slots across the thickness range, including
soldering process, fill/wetting criteria and first-article inspection. CC,
VBUS power sense and backfeed prevention, ESD, shield termination, and routing
remain on design hold. This mapping does not complete PASS-C.

### C20–C27 characterization shortlist

Decision #8 locks 100 µF series DC blocking. Film and 25 V are unevaluated BOM
screening assumptions, not selections. For comparison only, a 500 mA peak
sine is 354 mA RMS; this is not a settled driver waveform specification.

- **Panasonic SU-A bipolar electrolytic:** The [radial catalog](https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ast-ind-152839.pdf)
  SU-A characteristics list and ripple correction table give `ECEA1VN101U`
  (35 V, Ø10 × 16 mm, 5 mm lead pitch) 230 mA RMS at 120 Hz and 85 °C;
  applying the 1.70 factor for 10 kHz and above gives 391 mA RMS. The same
  calculation gives 306 mA RMS for `ECEA1EN101U` (25 V), below the illustrative
  sine case.
  Catalog ripple ratings do not authorize continuous near-zero-bias AC;
  Panasonic's ripple-current precaution warns that reversal can occur at low
  DC bias even within the ripple rating. The 35 V part is a characterization
  and supplier-inquiry candidate only. Do not operate outside published
  conditions without written manufacturer confirmation for the actual waveform.
- **KEMET `C1210C107M3PACTU`:** Nonpolar 100 µF / 25 V X5R, per the
  [X5R series datasheet](https://yageogroup.com/content/datasheet/asset/file/KEM_C1006_X5R_SMD)
  Benefits and Ordering Information sections. Continuous ripple and thermal
  performance in this application have not been verified; not qualified.
- **KEMET `R60DW6100AA50K`:** An unapproved 100 µF film size reference;
  [KEMET part sheet](https://search.kemet.com/component-documentation/download/specsheet/R60DW6100AA50K),
  Dimensions: 41.5 × 20 × 40 mm (L × T × H).
- **TDK `CAA572X7R1E107M670LJ`:** A nonpolar 100 µF ±20%, 25 V X7R
  candidate with metal terminals. TDK specifies a 6.25 × 5.00 mm nominal
  body and 7.20 mm maximum height. Use the series-specific land pattern
  if selected. TDK's simple equivalent circuit gives 2.2 mΩ ESR and
  2.163 nH ESL. That model estimates approximately 0.080 Ω at 20 kHz and
  0.046 Ω at 34 kHz at nominal capacitance. The model does not bound
  effective capacitance or heating under the actual waveform.
  [TDK part specification](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CAA572X7R1E107M670LJ) ·
  [TDK equivalent circuit](https://product.tdk.com/system/files/dam/technicalsupport/tvcl/pdf/mlcc_automotive_megacap-lowr_caa572_ecm.pdf)

The channel 0 prototype exposes TP820–TP821 across C212 and TP822–TP823
across the 1 Ω shunt R20. Record the differential capacitor voltage and
shunt current through startup, steady drive and E-stop. At 150 mA RMS
and 20 kHz, an ideal 100 µF capacitor contributes about 34 mV peak to peak.
Include measured DC offset, ESR voltage and transients when evaluating the
actual dielectric and ripple rating.

The provisional TDK footprint uses a 4.50 mm gap and 1.75 × 5.45 mm
lands from the midpoint dimensions in the [TDK land drawing](https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/specification/mlccspec_commercial_megacap_ca_x7_en.pdf).
Release requires verification of effective capacitance, ripple heating,
startup and loop stability under the measured waveform.

## Lot inventories

These are individual items or repeated functional groups, not placement or
purchase quantities. **Ready** means an exact symbol/footprint pairing is
verified for CAD only; **Provisional** means a pairing is recorded but the
selection is not final; **Captured** means the symbol, value and footprint
are in the schematic and only the listed release check remains; **Symbol
only** means a generic symbol and any source-stated value, with no footprint
or orderable part; **Blocked** means no CAD mapping. Where no agreed board reference or quantity is stated, it
is **not assigned**. Local sketch labels are not board reference designators.

Sources below use **Schematic** for the linked system schematic design record
above, and **BOM** for the linked SYSTEM-01 BOM sheet. Other sources:
[DRV-2](../../../docs/phase2/driver_power_requirements.md),
[FE-4](../../../docs/phase2/frontend_requirements.md),
[design gates](../../../docs/phase2/design_order.md),
[M16 handoff](../../../docs/handoff/m16-fpga-handoff.md),
[power ICD](../../../contract/icd/power.md),
[DAC ICD](../../../contract/icd/dac_fpga.md) and
[ADC ICD](../../../contract/icd/adc_fpga.md).

### PROT — input protection

| Item / source | CAD state | Verification before release |
|---|---|---|
| J1 adapter jack | **Prototype** `PJ-079BH`, footprint `Connector_BarrelJack:BarrelJack_CUI_PJ-079BH_Horizontal` | 2.5 mm center pin, Ø5.5 mm mating plug, 5 A at 24 VDC. Pin 1 feeds F1 and pin 2 returns to the choke. Pin 3 and shield pads are open pending fit and shield review. [Same Sky drawing](https://www.sameskydevices.com/product/resource/pj-079bh.pdf) |
| F1 open holder, Schurter `0031.8201` ([verified holder mapping](#partial-prot-lot-mappings); Schematic §2 identifies the F1 fuse function, not the holder part) | **Ready** for that exact open holder only | Power owner: verify fit, removal clearance and thermal derating with the assigned 0853.0551 cover. |
| F1 replaceable time-delay cartridge (BOM 33; Schematic §2) | **Prototype** Schurter `0001.2509`, 3.15 A, 1.5 kA at 300 VDC | Recorded in the schematic as F1's MPN field; the PCB footprint stays the `0031.8201` holder. 3.15 A exceeds the 3.00 A spec by 5%; the power owner accepted that deviation. Verify inrush, prospective fault current and coordination with the holder and TVS. [Schurter SPT data](https://www.schurter.com/en/datasheet/SPT%205x20) |
| D1 `SMBJ18A` TVS (BOM 33; Schematic §2; [verified pairings](#partial-prot-lot-mappings)) | **Ready** | Power owner: verify surge and clamp coordination; the CAD mapping does not close this test. |
| Input common-mode choke L1 | **Prototype** Würth `7448225007`, 5 A at 70 °C | Supply winding 1–4 and return winding 2–3. Custom 5.0 × 7.7 mm pin pattern and Ø1.30 mm finished holes. Confirm attenuation and thermal rise with the installed harness. [Würth drawing](https://www.we-online.com/components/products/datasheet/7448225007.pdf) |
| Input CLC filter | **Prototype** C770, L760 and C30 | L760 uses Würth `7447714047` with 3.5 × 2.0 mm pads at 9.0 mm pitch. Keep vias and sensitive routing out from under the part. Confirm damping, inrush and EMI on the assembled circuit. [Würth data sheet](https://www.we-online.com/components/products/datasheet/7447714047.pdf) |
| Reverse-polarity protection (BOM 33; Schematic §2) | **Prototype** Q760 DMP6023LE-13, D760 BZX38450-C12X and R770 10 kΩ | Cathode to MOSFET source, anode to gate. At 15 V input, a nominal 12 V clamp implies about 0.3 mA in R770. The zener is specified at 50 µA. Verify gate voltage during input transients, MOSFET thermal rise and inrush, and behavior if the input is reversed while C30 is charged. [Nexperia low-current zeners](https://www.nexperia.com/products/diodes/zener-diodes/serie/bzx38450-series) · [Diodes Inc. MOSFET](https://www.diodes.com/datasheet/download/DMP6023LE.pdf) |

The Schematic §2 adapter-input reservoir (1000 µF / 25 V) is tracked
under the **row 29 reservoir mapping**, not added here. The power ICD's open
adapter connector and the separate K1 panel pushbutton are not assigned to
PROT by the workbook. K2 remains separately held under row 32.

### PASS-A — driver and excitation

| Item / source | CAD state | Verification before release |
|---|---|---|
| LTC1563-2 cutoff-setting resistors per filter channel: 60 kHz from decision #19; 42.67 kΩ (0.1%) design value from M16 handoff §5 (BOM 34 filter R/C) | **Prototype** 48 × 42.7 kΩ, ±0.1%, 0603 | Vishay `TNPW060342K7BEEA` is an orderable realization. Six equal resistors per channel follow the [ADI unity-gain application](https://www.analog.com/media/en/technical-documentation/data-sheets/156323fa.pdf). The standard value raises the nominal resistance by 0.070% and moves an ideal 60 kHz cutoff down by about 42 Hz. Verify the assembled filter response and channel matching. [TI BOM listing](https://www.ti.com/lit/ug/slvud98/slvud98.pdf) |
| Filter capacitor/support provision (BOM 34 “filter R/C”; Schematic §4.3; M16 handoff §5) | **Captured** | The LTC1563-2 unity-gain application needs no external filter capacitors; the capture provides supply bypass. Reconcile the BOM lot wording with that circuit.
| Error-loop command-input resistor, 10 kΩ per channel (Schematic §4.2) | **Captured** 10 kΩ, 0603 | Driver owner: confirm loop capture and value before part allocation. |
| Error-loop sense-feedback resistor, 10 kΩ per channel (Schematic §4.2) | **Captured** 10 kΩ, 0603 | Driver owner: confirm loop capture and gain before part allocation. |
| Error-amplifier lead-compensation resistor per channel, value open (Schematic §4.2; design gates DRV-03) | **Captured** 330 kΩ, 0603 | Tune and verify phase margin with the real coil and cable; the captured value is the prototype starting point.
| Error-amplifier lead-compensation capacitor per channel, value open (same sources) | **Captured** 150 pF, 0603 | Close the same compensation measurement before part selection.
| Vmid divider: 10 kΩ high-side and 10 kΩ low-side in the shown circuit (Schematic §4.2) | **Captured** 2 × 10 kΩ, 0603 | Driver owner: confirm shared versus replicated Vmid implementation and loading. |
| Vmid bypass, 100 nF in the shown circuit (Schematic §4.2) | **Captured** 100 nF, 0603 | Driver owner: confirm Vmid distribution and bypass population; the 1000 µF reservoir is tracked separately under row 29. |
| Per-channel difference-amp sense resistor network, values open (Schematic §4.2; DRV-2 §4) | **Captured** 10 kΩ ±0.1%, 0603 | Verify channel gain matching and common-mode rejection on the assembled board.
| Current-sense summer resistor network, scale 2.0103, component values open (Schematic §4.4; DRV-2 §4) | **Captured** 20 kΩ + 8 × 10 kΩ, ±0.1%, 0603 | Nominal scale −2.000 from each input; verify Ch0 gain and phase on the bench.
| Comparator threshold/reference network, per-channel trip at 1.2 × maximum current with a 0.6 V shunt-reference source in the design record (Schematic §§4.2, 4.4) | **Captured** 52.3 kΩ/10 kΩ divider, 0603 | Nominal 253 mA positive-peak trip with the 1 Ω shunts; verify tolerance and ordering against the 280 mA buffer clamp.
| Comparator fault combining (Schematic §§4.2, 4.4; design gates DRV-07; TLV3201 row 26) | **Captured** 4 × SN74LVC2G07, SOT-23-6 | Open-drain buffers wire-OR the eight push-pull comparator outputs into `DRIVER_FAULT_N`. Verify pulse capture and the hardware latch.
| Per-channel LMH6321 `CL` current-limit input and `EF` error-flag output (row 24; [TI LMH6321](https://www.ti.com/lit/ds/symlink/lmh6321.pdf) §§6.7, 6.9; DRV-2 §2 discusses 300 mA versus short-term 500 mA with the current limit disabled, not a requirement to disable it) | **Captured** 10.7 kΩ programming resistors, 0603 | CL is programmed for about 280 mA nominal peak at 15 V. EF is left unconnected; the TLV3201 comparators carry fault detection. Verify clamp tolerance and thermal rise.
| Other driver/DAC supply bypass and decoupling, values open (BOM 34; DRV-2 §8) | **Captured** 100 nF, 0603 | Values follow the datasheet recommendations; verify rail impedance on the assembled board.
| Driver auxiliary headers (BOM 34; decision #25) | **Open** | Driver owner: identify remaining connector functions and pin counts on the one-board design; no old inter-board header or second set of FG headers. |
| DAC-side SPI probe pads (DAC ICD §1; M16 handoff §4.5) | **Captured** TP200–TP203 | Driver/FPGA owners: define probe nets and geometry; no pad count assigned. |
| Other driver test points (BOM 34; DRV-2 §8) | **Captured** TP210–TP217 and TP820–TP823 | Driver owner: specify required bring-up nets and access, excluding the DAC pads above. |

Rows 21–24, 26–30, 32, 36 and 38 retain their independent mappings or
holds. In particular, the §4.2 coil coupling capacitor and \(R_{store}\)
remain in rows 28 and 27, respectively. The same section mentions AC
coupling of the DAC command without specifying an additional component;
the driver owner must reconcile that wording with the actual signal path
before any extra capacitor is assigned.

### PASS-C — FPGA and host

| Item / source | CAD state | Verification before release |
|---|---|---|
| 2×7 JTAG header (BOM 45; [programmer and footprint hold](#jtag-programmer-and-footprint-hold)) | **Prototype** J140, `accubot:Molex_87831-1420` | Confirm cable fit, finished hole tolerance and +3.3 V rail headroom. |
| Supervisor/watchdog (BOM 45; Schematic §4.5; M16 handoff §10) | **Open** | FPGA/power/follower owners: reconcile a discrete supervisor (TPS3823 mentioned, not selected) versus PL timer, and settle STOP/heartbeat responsibility without changing the independent hardware E-stop. |
| Host USB receptacle ([provisional GCT mapping](#pass-c-host-usb-provisional-cad-mapping-only)) | **Provisional** | FPGA/host and mechanical owners: close the interface and footprint-variant holds listed in the mapping. |
| Host USB support: CC, VBUS sense/backfeed, ESD and shield termination ([USB mapping hold](#pass-c-host-usb-provisional-cad-mapping-only); Schematic §6.0) | **Captured** 5.1 kΩ CC, 2 × TPD2EUSB30, VBUS-sense divider, 27 Ω/47 pF | Shield bonding and power-off backfeed behavior remain layout and test checks.
| FPGA-side DAC SPI series termination, 33 Ω at the FPGA pin (DAC ICD §1; Schematic §6; M16 handoff §4.5) | **Prototype** R145–R147 with 0603 footprints | 33 Ω on CS, SCLK and SDI at the FPGA end. Verify layout and SPI edge integrity. DAC-side probe pads are tracked in PASS-A. |
| FPGA rail bypass/decoupling (BOM 45 and rails in row 47; Schematic §2; DRV-2 §8) | **Prototype** C150–C172 with 0603/0805 footprints | FPGA/power owners: verify effective capacitance and rail impedance against the implemented device and rail load. |
| Other FPGA/configuration passives (BOM 45; Schematic §6.0 QSPI configuration) | **Captured** QSPI pulls, mode straps, 33 Ω and 0 Ω links | PUDC_B, INIT_B, DONE and PROGRAM_B pull-ups plus the 0 Ω QSPI clock link are captured. Tune the source termination after routing.
| Digital test points (BOM 45) | **Captured** TP790–TP792 | FPGA owner: name the bring-up nets and specify access and count; exclude DAC probe pads. |

J123 carries the six signals in the [Pico ICD](../../../contract/icd/pico_link.md)
§2 on a JST GH `BM06B-GHS-TBT`, pins 1–6 in ICD order. The provisional
`accubot:Draft_Pico_Link` symbol is no longer used. TX and RX are named from
BRD-01's perspective.
The workbook does not allocate the connector to PASS-C. Pico ICD §6
places the STOP pull-down at the Pico.
Do not add internal ADC/DAC cable headers from older interfaces; decisions
#21/#25 and Schematic §§6.0, 8 make these on-board nets.

#### JTAG programmer and footprint hold

The target uses the standard 14-position, 2 mm-pitch ribbon for AMD/Xilinx
Platform Cable USB II. [AMD DS593 v1.5.1](https://docs.amd.com/api/khub/documents/TI9ts12CeuAeBtQpR7HWBw/content),
Figure 14 and Table 5, show the target connector pitch and list the
preferred vertical through-hole Molex `87831-1420` as a mating candidate.
The [Molex part sheet](https://www.molex.com/en-us/products/part-detail/878311420)
lists 1.60 mm as the recommended **PCB thickness**, not a hole diameter.

The curated symbol follows DS593 Table 6 in JTAG mode. Pins 1 and 12 have
no cable connection. Pins 3, 5, 7, 9 and 11 are digital ground. Pin 13
(`PGND`) and pin 14 (`HALT`) are optional cable signals. Pin 2 (`VREF`)
is wired to the same regulated +3.3 V net as Artix-7 bank 0 VCCO.
A temporary netlist export including J140 verified the VREF, ground and
JTAG signal mapping. DS593 specifies a 1.5–5 V operating range for VREF
and lists 15 mA at 3.3 V. Include that load when checking the +3.3 V rail.

The provisional footprint follows the released
[Molex SD-87831-0001](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/878/87831/878311420_sd.pdf)
Rev A25 lists `87831-1420` on sheet 10 without a locator peg. Sheet 9
shows 2 mm pitch and 0.90 ±0.05 mm typical terminal holes. KiCad
uses those nominal holes and marks circuit 1. Check the physical cable
orientation and mating clearance against a sample before release. [JLCPCB's rigid PCB capabilities](https://jlcpcb.com/capabilities/pcb-ca-)
publish +0.13/−0.08 mm for finished PTH size and a 0.20 mm recommended
annular ring (0.15 mm minimum) for multilayer 1 oz boards. The finished-hole
range for an order must fit the Molex callout or have written acceptance
from the manufacturer and fabricator. Cable/enclosure fit, board stackup
and +3.3 V rail headroom remain open.

### PASS-B — receiver and ADC

The input pairs below describe one Schematic §5.1 differential front-end
instance; board-wide population and reference designators are **not
assigned**. Decision #15 and the ADC ICD define the four channel functions,
not the number of populated front-end assemblies.

| Item / source | CAD state | Verification before release |
|---|---|---|
| INA163 series input pair, 100 Ω per leg (Schematic §5.1; FE-4 §5) | **Captured** 100 Ω, 0603 | Receiver owner: verify CMRR and coordinate with the input clamps. |
| INA163 input coupling pair, 10 µF per leg (Schematic §5.1; FE-4 §5; decision #17) | **Captured** 10 µF, 1206 | Verify dielectric, leakage and matching for CMRR.
| INA163 bias-return pair, 10 kΩ, 0.1% per leg (Schematic §5.1; FE-4 §5) | **Captured** 10 kΩ ±0.1%, 0603 | Receiver owner: verify offset and CMRR with the matched input network. |
| INA163 gain resistor, 176 Ω for the shown 35× stage (Schematic §5.1; decision #17) | **Captured** 176 Ω, 0603 | Receiver owner: verify gain and tolerances. |
| Sensor input clamps, two diodes per leg | **Prototype** `BAS70H,115` with `Diode_SMD:D_SOD-123F` | Pin 1 K and pin 2 A. Each diode is rated at 2 pF maximum at zero reverse bias and 1 MHz, for up to 4 pF per leg from the diodes alone under that test condition. Check the assembled link capacitance, pulse current, leakage and CMRR. [Nexperia data sheet](https://assets.nexperia.com/documents/data-sheet/BAS70H.pdf) |
| ADA4940-2 gain-setting resistors for 2× stage, resistor values open (Schematic §5.1; decision #17) | **Captured** 499 Ω / 1 kΩ, 0603 | Ch0 uses unity gain and Ch1–Ch3 a nominal 2× stage; verify headroom, settling and phase.
| ADC VCM-to-FDA common-mode network, 2.5 V function from the AD7768 (Schematic §5.1; FE-4 §6; BOM 54) | **Captured** VOCM tied to `ADC_VCM`, 100 nF | Verify the AD7768 VCM drive and settling with both FDA loads.
| ADC input series pair, 20 Ω per leg starting value (Schematic §5.1; decision #18; ADC ICD) | **Captured** 20 Ω, 0603 | ADC owner: verify precharge/input settling at ADC-5; establish the Ch0 pseudo-differential implementation rather than copying a pen channel. |
| ADC input reservoir pair, 470 pF per leg starting value (same sources; FE-4 §6) | **Captured** 470 pF, 0603 | ADC owner: tune with the differential driver and verify channel phase matching. |
| ADC input differential capacitor, 100 pF starting value (same sources) | **Captured** 100 pF, 0603 | ADC owner: confirm differential settling and released network values. No extra copy from the local capacitor labels. |
| ADC reference decoupling: 10 µF and 100 nF from Schematic §5.1 only; the ADC ICD leaves reference distribution open | **Captured** 10 µF + 100 nF, plus 10 Ω isolation | The 10 Ω isolation value is provisional pending settling and stability measurements.
| Other receiver/ADC supply decoupling (BOM 60; Schematic §5.3 identifies rails; ADC-01 note row 13 defers decoupling to schematic and lists no orderable MCLK part) | **Captured** 100 nF, 0603 | Receiver/ADC owners: assign rail bypass values and locations separately from reference decoupling. |
| ADC MCLK series resistor, 33 Ω in the 32.768 MHz path (Schematic §5.1) | **Captured** 33 Ω, 0603 | ADC/FPGA owners: verify clock integrity with the actual clock tree. |
| Buffered clock branch to the FPGA (Schematic §5.1 only; M16 handoff §2 defines the shared clock, not a discrete buffer) | **Captured** direct branch with 33 Ω series | No discrete buffer is used; the oscillator drives the ADC and FPGA through R100. Verify loading and integrity.
| Remaining sensor-side connections: pen channels and fixed reference (BOM 60; Schematic §5.2; decision #15) | **Captured** J122/J127 pen headers and J128 reference header | Ch2 and Ch3 reuse the Ch1 front end provisionally; reconcile INA163 and ADA4940-2 quantities with the BOM.
| Possible current-sense BNC: PEN-ANA-01 note row 15 and connector requirements `Locked-CONN` row 7 reference it but exclude it from the pen BOM; Schematic §§4.4, 5.2 show on-board Ch0, not a BNC selection | **Open** | Receiver/driver owners: decide whether an external BNC is still needed. No BNC population, location or footprint assigned. |

The 2×8/custom connector in the ADC ICD is not counted or placed here;
owner reconciliation with the single-board decision is required before
any physical ADC interconnect could be considered.

#### ADC input capacitor footprint hold

Only KYOCERA AVX `KGM15ACG1H471GT` (470 pF reservoir) and
`KGM15ACG1H101GT` (100 pF differential) are candidates for one shared,
provisional land pattern. The [KGM C0G datasheet](https://datasheets.kyocera-avx.com/C0GNP0-KGM.pdf)
(TDS-SMDMLCC-0036 Rev 7, “How to Order” and “Capacitance Range”) identifies
the KGM15 0603 case and permits reflow, but gives no PCB land drawing.

The [KYOCERA AVX Surface Mounting Guide](https://datasheets.kyocera-avx.com/SurfaceMountGuide.pdf)
(TDS-SMDMLCC-0055 Rev 0, p. 1, reflow drawing) shows two rectangular pads:
D2 and D4 are the individual pad lengths (0.80 mm each), D5 is pad width
(0.75 mm), D3 is the inner gap (0.70 mm), and D1 is the outer span
(2.30 mm). The guide gives generic MLCC pad dimensions, not a solder mask
or stencil drawing. The separate [KYOCERA MLCC handling guide](https://ele.kyocera.com/en/product/capacitor/ceramic/mlcc-handling/mounting-01/)
lists a 0.80–1.00 mm gap and 0.80–1.10 mm land width for its 1608/0603
row with ±0.15 mm body tolerances; its figure distinguishes land from solder
resist. Neither guide explicitly identifies which pattern applies to these
two exact order codes.

Before assigning a footprint, obtain a released drawing or written
manufacturer confirmation identifying the reflow copper pattern for both
codes, and confirm the mask, stencil and assembly requirements with the PCB
owner. No footprint, circuit, population or BOM approval follows from this
check. The 20 Ω resistor stays symbol-only; Ch0 topology, ADC-5 bench tuning,
settling and channel phase matching remain open.

## Capture holds and excluded items

- **Power:** §2 shows the +5 V analog LDO fed by +5 V digital, with no dropout
  headroom, and includes ADR434 on +5 V despite its 6.1 V minimum VIN. Confirm
  the +5 V analog and reference upstream rails and isolated-module load before
  wiring. Do not change the locked power-tree parts here.
- **Fault and stop:** §4.4/§6 calls for a wired-OR/open-drain fault bus; the
  selected TLV3201 is push-pull. Approve the combining circuit or a reviewed
  part change. The [K1/K2 intended roles](#k1k2-intended-roles-and-capture-hold)
  do not close the hardwired stop design. Resolve the K1 selection, K2
  capture hold, and hardwired stop versus FPGA status roles with the
  power, driver, and follower owners.
- **Reference designators and quantity:** allocate two unlisted OPA192 refs
  (row 22); confirm which of the U40–U45 and U80–U88 labels are spares; U3/U4
  receiver refs collide with the optos. §5.1 says repeat the pen front end for
  the reference channel, while row 52 budgets one installed INA163. Resolve
  receiver channel population before BOM freeze.
- **Interface and layout:** select the Pico connector against the
  [Pico ICD](../../../contract/icd/pico_link.md); pin-to-pad verification does not
  assign FPGA nets, validate HR-bank use, or certify 35T→50T interchange.
  The selected Mini-Fit header is not a selected mating cable housing or
  contact. Confirm mating hardware and keep metal outside the locked volume.
- **Not PCB parts:** SYSTEM rows 17–18 (PCB/shipping), 35 (heatsink/fan), 37
  (external ME60A1503F01 adapter), 46 (fan), 64–69 (pen plug/cables/coil/mechanics);
  PEN-ANA-01 rows 10–12 are off-board. FG-01, PMS-01 and enclosure assemblies
  are outside BRD-01; K1 is a separate panel part, not K2.
- **Inactive:** SYSTEM 25 (obsolete driver ADR434), 31 (TPS54331 alternate)
  and ADC-01 10 (ADS1274 backup). Do not build these or place spare MPN rows.

# BRD-01 BOM-to-CAD ledger

**Scope:** [SYSTEM-01](../../bom/BOM_SYSTEM-01.xlsx) Rev 0.05, sheet **BOM**
(Excel row numbers below); [ADC-01](../../bom/BOM_ADC-01.xlsx) rows 9–11;
[PEN-ANA-01](../../bom/BOM_PEN-ANA-01.xlsx) rows 9–12 and its
[connector requirements](../../bom/connector_requirements.xlsx).
Compared with [SC-05 and the system contract](../../../contract/system_contract.md),
[decisions #5, #7, #8, #10, #17, #19–21 and #25–26](../../../contract/decisions_log.md)
and the [system schematic design record](../../../docs/phase2/system_schematic.md).
References below are from the BOMs or design record, not new schematic annotation.

**Result:** 8 verified official pairings, 15 curated symbols, and one
official symbol with a curated footprint (ST TVS). There are 2 curated
footprints in total. This covers 23 complete BRD-01 BOM rows (OPA192
occurs twice), plus the TVS in the PROT lot and the pen interface's
PCB header. Eight active BRD-01 rows or lots remain incomplete. These
counts are not quantities to place or buy. A verified CAD part can still
be subject to a circuit-level hold.

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

The pen connector remains a rear-panel male solder-cup **IO Audio
`IO-TXLR3-M-PS-1`** ([manufacturer datasheet](https://assets.testequity.com/te1/Documents/pdf/io-audio/IO-Audio-Technologies_IO-TXLR3-M-PS-1_3-Pin-Male-Mini-XLR-Panel-Mount-Connector_Datasheet_1024.pdf)),
as identified by PEN-ANA-01 row 9 and Locked-CONN, despite SYSTEM row 63's
abbreviated MPN and Amphenol entry. It has no PCB footprint. The JST harness
carries only SIG+/SIG−; panel pin 1 and shell go to chassis star per Locked-CAB
C3. The cable-side `IO-TXLR3-F` is unchanged. JST pin assignment and receiver
channel population remain open. Measure the assembled total pen link, including
the internal harness and connector, against the 73 pF limit at 34 kHz (SC-05c).

## Curated from manufacturer sources

Curated symbols are in the shared `accubot` library. Order-only variants retain
their exact MPN in the BOM; the symbol ID can name the common physical part
(`AD7768-4BSTZ`, `ADA4940-2ACPZ`). The ST TVS uses an official symbol and
a custom land pattern; the RECOM module uses both a custom symbol and footprint.

**33 / PROT, D1 (§2): STMicroelectronics `SMBJ18A`, unidirectional.** Use
`Device:D_Zener` with Value `SMBJ18A` and assign
`accubot:ST_SMBJ_DO-214AA_DS1283`. Pin 1 (K) maps to the marked cathode pad;
pin 2 (A) maps to the anode pad. `Device:D_TVS` is bidirectional.
[ST DS1283 Rev. 14](https://www.st.com/resource/en/datasheet/smbj18a.pdf)
Fig. 14 specifies 1.62 × 2.07 mm rectangular lands, a 2.60 mm gap and a
5.84 mm outer span (4.22 mm center-to-center); Fig. 15 identifies the
cathode bar. Stock `Diode_SMD:D_SMB` has 2.50 × 2.30 mm rounded lands on
4.30 mm centers, so the same package name does not guarantee the same land
pattern. This is a CAD mapping, not surge or clamp-coordination validation.

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

## Unresolved PCB rows

| BOM row / refs | Needed before capture |
|---|---|
| 27 / R20–R27 | The searched 1206 options did not verify the BOM's 1 Ω, ±0.1%, 0.5 W combination. [Thin Film Technology TFT-DMS-165-1](https://www.thin-film.com/wp-content/uploads/2023/03/TFT-DMS-165-1.pdf) pp. 1–2 factory-code candidate: `TF2512HQ1R00B-T4`, two-terminal 2512, 1 Ω, ±0.1%, 1 W per the series table. Confirm that exact combination, MOQ, lead time and land pattern with the factory before selection. Footprint open; no availability claim or footprint reservation. |
| 28 / C20–C27 | Choose the 100 µF / 25 V series, physical size and lead pitch that meet AC coupling, ripple and thermal needs; ensure film is intentional. |
| 29 / C30–C31 | Choose 1000 µF / 25 V technology, polarity, size, terminals and ripple rating. |
| 32 / K2 | Select the actual force-guided 15 V relay and approve its contact allocation and E-stop chain. §4.5 mentions both dropping driver power and feeding enables; LMH6321 has no enable pin. Do not infer a relay from coil voltage. |
| 33 / PROT | D1 CAD mapping is above; select the fuse/holder, CM choke and reverse MOSFET with ratings and footprints. Surge validation stays open. |
| 34 / PASS-A | Expand the driver passives, filter R/C, headers and test points. LTC1563 uses a single **resistor value** in its unity-gain topology, not a single physical resistor per channel (ADI application schematic has six). |
| 45 / PASS-C | Expand FPGA passives, 2×7 JTAG header, supervisor/watchdog choice (§4.5 also allows a PL timer), host USB connector and test points. |
| 60 / PASS-B | Expand the ADC/preamp passives, RC network, ESD parts and remaining connectors; confirm whether the current-sense BNC is still needed. |

## Capture holds and excluded items

- **Power:** §2 shows the +5 V analog LDO fed by +5 V digital, with no dropout
  headroom, and includes ADR434 on +5 V despite its 6.1 V minimum VIN. Confirm
  the +5 V analog and reference upstream rails and isolated-module load before
  wiring. Do not change the locked power-tree parts here.
- **Fault and stop:** §4.4/§6 calls for a wired-OR/open-drain fault bus; the
  selected TLV3201 is push-pull. Approve the combining circuit or a reviewed
  part change. Confirm K1 selection, K2 function and hardwired stop vs FPGA
  status roles with the driver and follower owners.
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

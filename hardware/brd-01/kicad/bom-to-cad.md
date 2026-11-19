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
mapped PROT lot has two separate mappings: one additional official pairing
for the Schurter holder, and an official symbol with a curated footprint for
the ST TVS. The provisional host USB pairing is tracked separately under
PASS-C. None of these adds a complete BOM row. There are 2 curated
footprints in total (RECOM and ST).

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

The pen connector remains a rear-panel male solder-cup **IO Audio
`IO-TXLR3-M-PS-1`** ([manufacturer datasheet](https://assets.testequity.com/te1/Documents/pdf/io-audio/IO-Audio-Technologies_IO-TXLR3-M-PS-1_3-Pin-Male-Mini-XLR-Panel-Mount-Connector_Datasheet_1024.pdf)),
as identified by PEN-ANA-01 row 9 and Locked-CONN, despite SYSTEM row 63's
abbreviated MPN and Amphenol entry. It has no PCB footprint. The JST harness
carries only SIG+/SIG−; panel pin 1 and shell go to chassis star per Locked-CAB
C3. The cable-side `IO-TXLR3-F` is unchanged. JST pin assignment and receiver
channel population remain open. Measure the assembled total pen link, including
the internal harness and connector, against the 73 pF limit at 34 kHz (SC-05c).

## Partial PROT lot mappings

**33 / PROT, F1 (§2): Schurter OGN `0031.8201` holder only.** Use
`Device:Fuse` and explicitly assign
`Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open`.
The [Schurter OGN datasheet](https://www.schurter.com/en/datasheet/typ_ogn.pdf)
Variants table identifies the open 5 × 20 mm THT holder with 22.5 mm pin
pitch, not the 25 mm `0031.8211`. The
[Schurter THT drilling drawing](https://cdn-reichelt.de/documents/datenblatt/C400/PL%20OGN-225.pdf)
specifies two Ø1.3 mm (+0.1/−0 mm) terminal holes and a Ø2.7 mm optional
center mounting hole. KiCad pins 1 and 2 match like-numbered plated pads
with Ø1.3 mm drills at 22.5 mm pitch; the footprint includes the center
hole as an unnumbered Ø2.7 mm non-plated hole.

Keep `0031.8201` as the holder MPN, separate from the unselected 3 A
time-delay cartridge MPN. **Candidates only; neither is approved for
substitution:**

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
verify inrush against the fuse time-current behavior, and resolve touch
protection for the open holder.

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

## Unresolved PCB rows

| BOM row / refs | Needed before capture |
|---|---|
| 27 / R20–R27 | The searched 1206 options did not verify the BOM's 1 Ω, ±0.1%, 0.5 W combination. [Thin Film Technology TFT-DMS-165-1](https://www.thin-film.com/wp-content/uploads/2023/03/TFT-DMS-165-1.pdf) pp. 1–2 factory-code candidate: `TF2512HQ1R00B-T4`, two-terminal 2512, 1 Ω, ±0.1%, 1 W per the series table. Confirm that exact combination, MOQ, lead time and land pattern with the factory before selection. Footprint open; no availability claim or footprint reservation. |
| 28 / C20–C27 | Hold selection and footprint; see the characterization shortlist below. |
| 29 / C30–C31 | Hardware-owner hold: SYSTEM-01 describes both as 1000 µF / 25 V mid-rail reservoirs, while the system schematic describes one adapter-input reservoir (§2) and one mid-rail reservoir (§4.2). Reconcile the roles and reference designators before shortlisting or assigning footprints. |
| 32 / K2 | Select the actual force-guided 15 V relay and approve its contact allocation and E-stop chain. §4.5 mentions both dropping driver power and feeding enables; LMH6321 has no enable pin. Do not infer a relay from coil voltage. |
| 33 / PROT | [Protection inventory](#prot--input-protection): holder and TVS mapped; cartridge, input filtering and reverse protection open. |
| 34 / PASS-A | [Driver inventory](#pass-a--driver-and-excitation): loop, filter, mid-rail, current-sense and access parts not fully mapped. |
| 45 / PASS-C | [Digital inventory](#pass-c--fpga-and-host): host USB provisional; digital passives, JTAG, watchdog and test access open. |
| 60 / PASS-B | [Receiver inventory](#pass-b--receiver-and-adc): front-end, ADC support and connector population open. |

### PASS-C host USB: provisional CAD mapping only

**45 / PASS-C: GCT `USB4105-GF-A` candidate.** Pair
`Connector:USB_C_Receptacle_USB2.0_16P` with
`Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal`.
The [GCT USB4105 drawing](https://gct.co/files/drawings/usb4105.pdf), Rev B
(18 Dec 2023), sheet 1, is the comparison basis:

- All 17 distinct pin and pad identifiers match, including `SH`. The 16
  contact identifiers use 12 physical lands: eight 0.30 × 1.15 mm and four
  0.60 × 1.15 mm. The shared lands pair only same-function contacts; this
  does not approve circuit wiring.
- The footprint matches two 0.60 × 1.70 mm and two 0.60 × 1.40 mm plated
  shell slots, two Ø0.65 mm non-plated holes, and 7.35 mm from the board
  edge to the signal land centers (to drawing precision).

The drawing's blank stake-length suffix denotes 0.95 mm. Do not lock the
orderable suffix or assume a board thickness: enclosure fit and
manufacturability remain open. CC, VBUS power sense and backfeed prevention,
ESD, shield termination, and routing are on design hold. This mapping does
not complete PASS-C.

### C20–C27 characterization shortlist (no selection)

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

Leave the footprint unassigned until the actual capacitor voltage and current
waveforms, operating temperature, ESR and ripple heating, manufacturer
conditions, and driver stability and startup behavior are verified.

## Lot inventories

These are individual items or repeated functional groups, not placement or
purchase quantities. **Ready** means an exact symbol/footprint pairing is
verified for CAD only; **Provisional** means a pairing is recorded but the
selection is not final; **Symbol only** means a generic symbol and any
source-stated value, with no footprint or orderable part; **Blocked** means
no CAD mapping. Where no agreed board reference or quantity is stated, it
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

| Item / source | CAD state | Owner decision before capture or release |
|---|---|---|
| F1 open holder, Schurter `0031.8201` ([verified holder mapping](#partial-prot-lot-mappings); Schematic §2 identifies the F1 fuse function, not the holder part) | **Ready** for that exact open holder only | Power owner: resolve touch protection before release. This mapping neither qualifies a cover or alternate holder nor approves a cartridge. |
| F1 replaceable 3 A time-delay cartridge (BOM 33; Schematic §2; [candidate evidence and hold](#partial-prot-lot-mappings)) | **Blocked** | Power owner: establish DC breaking rating at prospective fault current, check inrush, and approve a cartridge; no second PCB footprint for it. |
| D1 `SMBJ18A` TVS (BOM 33; Schematic §2; [verified pairings](#partial-prot-lot-mappings)) | **Ready** | Power owner: verify surge and clamp coordination; the CAD mapping does not close this test. |
| Input common-mode choke, shown as `L1` (BOM 33; Schematic §2; DRV-2 §3) | **Blocked** | Power owner: set filter requirements and verify the choke winding/pin arrangement before mapping a symbol or footprint. |
| Other input CLC filter elements (DRV-2 §3 specifies CLC filtering, not the discrete parts) | **Blocked** | Power owner: define the filter and identify which capacitor roles are already served by the input reservoir; no additional capacitor or inductor count assigned. |
| Reverse-polarity protection (BOM 33 says MOSFET; Schematic §2 allows MOSFET or ideal diode) | **Blocked** | Power owner: settle implementation and requirements before any symbol/part mapping. |

The Schematic §2 adapter-input reservoir (1000 µF / 25 V) is tracked
under the **row 29 C30–C31 role hold**, not added here. The power ICD's open
adapter connector and the external K1 panel stop are not assigned to PROT
by the workbook. K2 remains separately held under row 32.

### PASS-A — driver and excitation

| Item / source | CAD state | Owner decision before capture |
|---|---|---|
| LTC1563-2 cutoff-setting resistors per filter channel: 60 kHz from decision #19; 42.67 kΩ (0.1%) design value from M16 handoff §5 (BOM 34 filter R/C) | **Symbol only** `Device:R` | Driver owner: confirm the circuit, physical count and orderable realization of the design value. “One resistor” in M16 is one **value**, not one physical component; the [ADI unity-gain application](https://www.analog.com/media/en/technical-documentation/data-sheets/156323fa.pdf) shows six. |
| Filter capacitor/support provision (BOM 34 “filter R/C”; Schematic §4.3; M16 handoff §5) | **Blocked** | Driver owner: confirm external capacitor roles, if any, against the filter and supply circuit. The lot wording is not an external pole-capacitor design or a quantity. |
| Error-loop command-input resistor, 10 kΩ per channel (Schematic §4.2) | **Symbol only** `Device:R` | Driver owner: confirm loop capture and value before part allocation. |
| Error-loop sense-feedback resistor, 10 kΩ per channel (Schematic §4.2) | **Symbol only** `Device:R` | Driver owner: confirm loop capture and gain before part allocation. |
| Error-amplifier lead-compensation resistor per channel, value open (Schematic §4.2; design gates DRV-03) | **Symbol only** `Device:R` | Driver owner: tune with the real coil/cable at 34 kHz and verify phase margin. |
| Error-amplifier lead-compensation capacitor per channel, value open (same sources) | **Symbol only** `Device:C` | Driver owner: close the same compensation test before selection. |
| Vmid divider: 10 kΩ high-side and 10 kΩ low-side in the shown circuit (Schematic §4.2) | **Symbol only** `Device:R` | Driver owner: confirm shared versus replicated Vmid implementation and loading. |
| Vmid bypass, 100 nF in the shown circuit (Schematic §4.2) | **Symbol only** `Device:C` | Driver owner: confirm Vmid distribution and bypass population; the 1000 µF reservoir is a separate row 29 hold. |
| Per-channel difference-amp sense resistor network, values open (Schematic §4.2; DRV-2 §4) | **Symbol only** `Device:R` | Driver owner: approve resistor values and matching for differential sensing; the coil-current sense resistor is already row 27. |
| Current-sense summer resistor network, scale 2.0103, component values open (Schematic §4.4; DRV-2 §4) | **Symbol only** `Device:R` | Driver owner: approve the summing network for measured Ch0 gain/phase; do not derive component values from the scale alone. |
| Comparator threshold/reference network, per-channel trip at 1.2 × maximum current with a 0.6 V shunt-reference source in the design record (Schematic §§4.2, 4.4) | **Blocked** | Driver owner: close threshold and reference distribution; no shunt part, bias network or per-channel reference replication selected. |
| Comparator fault combining (Schematic §§4.2, 4.4; design gates DRV-07; TLV3201 row 26) | **Blocked** | Driver/power owners: reconcile push-pull output with the wired-OR requirement and approve the fault path before mapping any combining parts. |
| Per-channel LMH6321 `CL` current-limit input and `EF` error-flag output (row 24; [TI LMH6321](https://www.ti.com/lit/ds/symlink/lmh6321.pdf) §§6.7, 6.9; DRV-2 §2 discusses 300 mA versus short-term 500 mA with the current limit disabled, not a requirement to disable it) | **Blocked** | Driver owner: confirm how current limiting is implemented and whether or how EF is used alongside the TLV3201 comparator path. No support part, footprint, or topology assigned; the buffer itself remains mapped in row 24. |
| Other driver/DAC supply bypass and decoupling, values open (BOM 34; DRV-2 §8) | **Symbol only** `Device:C` | Driver/power owners: allocate values and counts to the actual supply pins; do not duplicate filter or Vmid entries. |
| Driver auxiliary headers (BOM 34; decision #25) | **Blocked** | Driver owner: identify remaining connector functions and pin counts on the one-board design; no old inter-board header or second set of FG headers. |
| DAC-side SPI probe pads (DAC ICD §1; M16 handoff §4.5) | **Symbol only** `Connector:TestPoint` | Driver/FPGA owners: define probe nets and geometry; no pad count assigned. |
| Other driver test points (BOM 34; DRV-2 §8) | **Symbol only** `Connector:TestPoint` | Driver owner: specify required bring-up nets and access, excluding the DAC pads above. |

Rows 21–24, 26–30, 32, 36 and 38 retain their independent mappings or
holds. In particular, the §4.2 coil coupling capacitor and \(R_{store}\)
remain in rows 28 and 27, respectively. The same section mentions AC
coupling of the DAC command without specifying an additional component;
the driver owner must reconcile that wording with the actual signal path
before any extra capacitor is assigned.

### PASS-C — FPGA and host

| Item / source | CAD state | Owner decision before capture |
|---|---|---|
| 2×7 JTAG header (BOM 45) | **Symbol only** `Connector_Generic:Conn_02x07_Odd_Even` | FPGA owner: approve programmer pinout, keying and physical connector. The symbol only represents the contact count. |
| Supervisor/watchdog (BOM 45; Schematic §4.5; M16 handoff §10) | **Blocked** | FPGA/power/follower owners: reconcile a discrete supervisor (TPS3823 mentioned, not selected) versus PL timer, and settle STOP/heartbeat responsibility without changing the independent hardware E-stop. |
| Host USB receptacle ([provisional GCT mapping](#pass-c-host-usb-provisional-cad-mapping-only)) | **Provisional** | FPGA/host and mechanical owners: close the interface and footprint-variant holds listed in the mapping. |
| Host USB support: CC, VBUS sense/backfeed, ESD and shield termination ([USB mapping hold](#pass-c-host-usb-provisional-cad-mapping-only); Schematic §6.0) | **Blocked** | Host-interface owner: approve the circuit and routing before allocating passives or protection parts; FT231XQ stays in row 43. |
| FPGA-side DAC SPI series termination, 33 Ω at the FPGA pin (DAC ICD §1; Schematic §6; M16 handoff §4.5) | **Symbol only** `Device:R` | FPGA/DAC owners: apply the frozen ICD's CS requirement and reconcile the schematic/handoff shorthand beside SCLK/SDI before assigning additional nets or a total count. DAC-side probe pads are tracked in PASS-A only. |
| FPGA rail bypass/decoupling (BOM 45 and rails in row 47; Schematic §2; DRV-2 §8) | **Symbol only** `Device:C` | FPGA/power owners: confirm rail pin groups and allocate values/counts; regulators are already in row 47. |
| Other FPGA/configuration passives (BOM 45; Schematic §6.0 QSPI configuration) | **Blocked** | FPGA owner: define the QSPI/boot support circuit; the source does not specify individual pulls, straps or values. |
| Digital test points (BOM 45) | **Symbol only** `Connector:TestPoint` | FPGA owner: name the bring-up nets and specify access and count; exclude DAC probe pads. |

The [Pico ICD](../../../contract/icd/pico_link.md) §2 defines a six-contact
link; its BRD-01 connector remains a separate hold not allocated to PASS-C
by the workbook. Pico ICD §6 places the STOP pull-down at the Pico, not
BRD-01.
Do not add internal ADC/DAC cable headers from older interfaces; decisions
#21/#25 and Schematic §§6.0, 8 make these on-board nets.

### PASS-B — receiver and ADC

The input pairs below describe one Schematic §5.1 differential front-end
instance; board-wide population and reference designators are **not
assigned**. Decision #15 and the ADC ICD define the four channel functions,
not the number of populated front-end assemblies.

| Item / source | CAD state | Owner decision before capture |
|---|---|---|
| INA163 series input pair, 100 Ω per leg (Schematic §5.1; FE-4 §5) | **Symbol only** `Device:R` | Receiver owner: verify CMRR and coordinate with the input clamps. |
| INA163 input coupling pair, 10 µF per leg (Schematic §5.1; FE-4 §5; decision #17) | **Symbol only** `Device:C` | Receiver owner: confirm capacitor technology, matching and DC bias conditions. |
| INA163 bias-return pair, 10 kΩ, 0.1% per leg (Schematic §5.1; FE-4 §5) | **Symbol only** `Device:R` | Receiver owner: verify offset and CMRR with the matched input network. |
| INA163 gain resistor, 176 Ω for the shown 35× stage (Schematic §5.1; decision #17) | **Symbol only** `Device:R` | Receiver owner: verify gain and tolerances. |
| Connector/input ESD clamp group, Schottky clamps to ±12 V in the sketch with protection capacitance <10 pF at the connector (BOM 60; Schematic §5.1; FE-4 §5) | **Symbol only** `Device:D_Schottky` | Receiver owner: approve clamp implementation and validate capacitance within the total 73 pF link budget. No additional ESD array or clamp count implied. |
| ADA4940-2 gain-setting resistors for 2× stage, resistor values open (Schematic §5.1; decision #17) | **Symbol only** `Device:R` | Receiver owner: close the driver gain network and phase matching with the ADC load. |
| ADC VCM-to-FDA common-mode network, 2.5 V function from the AD7768 (Schematic §5.1; FE-4 §6; BOM 54) | **Blocked** | Receiver owner: settle VCM distribution, bias network and allocation of the already-mapped row 54 buffers. |
| ADC input series pair, 20 Ω per leg starting value (Schematic §5.1; decision #18; ADC ICD) | **Symbol only** `Device:R` | ADC owner: verify precharge/input settling at ADC-5; establish the Ch0 pseudo-differential implementation rather than copying a pen channel. |
| ADC input reservoir pair, 470 pF per leg starting value (same sources; FE-4 §6) | **Symbol only** `Device:C` | ADC owner: tune with the differential driver and verify channel phase matching. |
| ADC input differential capacitor, 100 pF starting value (same sources) | **Symbol only** `Device:C` | ADC owner: confirm differential settling and released network values. No extra copy from the local capacitor labels. |
| ADC reference decoupling: 10 µF and 100 nF from Schematic §5.1 only; the ADC ICD leaves reference distribution open | **Symbol only** `Device:C` | ADC/power owners: close reference rail headroom, buffer/distribution and decoupling count across REF inputs; ADR434 and the OPA192 reference/VCM buffers stay in rows 51 and 54. |
| Other receiver/ADC supply decoupling (BOM 60; Schematic §5.3 identifies rails; ADC-01 note row 13 defers decoupling to schematic and lists no orderable MCLK part) | **Symbol only** `Device:C` | Receiver/ADC owners: assign rail bypass values and locations separately from reference decoupling. |
| ADC MCLK series resistor, 33 Ω in the 32.768 MHz path (Schematic §5.1) | **Symbol only** `Device:R` | ADC/FPGA owners: verify clock integrity with the actual clock tree. |
| Buffered clock branch to the FPGA (Schematic §5.1 only; M16 handoff §2 defines the shared clock, not a discrete buffer) | **Blocked** | ADC/FPGA owners: confirm clock distribution and whether a discrete buffer is required; the XO is row 59. |
| Remaining sensor-side connections: pen channels and fixed reference (BOM 60; Schematic §5.2; decision #15) | **Blocked** | Receiver/mechanical owners: reconcile connector population and signal assignment; sketch `J1/J2/J4` are not board refs. Reuse the existing row 63 JST/panel evidence where applicable; no duplicate header or new reference-coil connector assumed. |
| Possible current-sense BNC: PEN-ANA-01 note row 15 and connector requirements `Locked-CONN` row 7 reference it but exclude it from the pen BOM; Schematic §§4.4, 5.2 show on-board Ch0, not a BNC selection | **Blocked** | Receiver/driver owners: decide whether an external BNC is still needed. No BNC population, location or footprint assigned. |

The 2×8/custom connector in the ADC ICD is not counted or placed here;
owner reconciliation with the single-board decision is required before
any physical ADC interconnect could be considered.

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

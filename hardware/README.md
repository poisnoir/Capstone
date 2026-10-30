# hardware/ — BRD-01, FG-01, pen and mechanics

Owner: Tung (electronics), with Tristan on mechanical interfaces. Read
`../contract/` first; the 150 mm metal rule and the ICNIRP guard are contract
items, not suggestions.

## What lives here

| Path | Contents |
|---|---|
| `brd-01/` | One 4-layer board: power/E-stop, FPGA + clock, DAC/filter/current loops, receiver/ADC, connectors |
| `brd-01/driver/` | Pointer to the vendor AC current-driver reference + new driver work |
| `brd-01/frontend/` | Pointer to the vendor sensor-amplifier reference + new INA163/ADA4940 chain |
| `fg-01/` | 8-coil planar field-generator PCB (separate passive board) |
| `pen/` | Passive 5-DOF pen coil and shell |
| `mechanical/` | Enclosure, non-metal ICNIRP guard, mounts, camera bracket |
| `bom/` | System and board BOMs, connector requirements |

## Fixed decisions

- One board, BRD-01, 4 layers; FG-01 is separate; the pen is passive
  (`contract/decisions_log.md` #25).
- FPGA: XC7A35T-1FTG256C baseline, XC7A50T same footprint (#26).
- DAC80508 + 8× LTC1563-2; SPI 49.152 MHz (#19).
- AD7768-4 + INA163 + ADA4940-2 (#5/#17).
- Power: one medical-grade 15 V/60 W adapter; +15/−15/+5/+3.3 V; NC E-stop in
  the driver enable chain (#7/#10/#20).
- No metal within 150 mm of the tracking volume; the ICNIRP guard is a non-metal
  access barrier, not a shield (`SC-04b`, D2).

## EDA

KiCad is the planned tool (`docs/phase2/system_schematic.md` §8). Commit the
project files, not `*-backups/`, `fp-info-cache` or `*.kicad_prl` (gitignored).
If the team changes to Altium/Fusion, revisit `.gitattributes` and LFS before
adding binary board files.

## Current status

The vendor references are pointers only; the new KiCad project and BOM Rev 0.02
are the next deliverables. Do not edit `vendor/`.

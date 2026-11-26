# hardware/ — BRD-01, FG-01, pen and mechanics

Owner: Tung (electronics), with Tristan on mechanical interfaces. Read
`../contract/` first; the 150 mm metal rule and the ICNIRP guard are contract
items, not suggestions.

## What lives here

| Path | Contents |
|---|---|
| `brd-01/` | One 4-layer board for power entry / arm STOP (no panel E-stop, #30), FPGA + clock, excitation, receiver/ADC, and connectors. Open the [BRD-01 KiCad project](brd-01/kicad/brd-01.kicad_pro). |
| `brd-01/driver/` | Pointer to the vendor AC current-driver reference + new driver work |
| `brd-01/frontend/` | Pointer to the vendor sensor-amplifier reference + new INA163/ADA4940 chain |
| [`kicad/lib/`](kicad/lib/) | Shared KiCad symbols and footprints. Open board projects from their board folders. |
| [`fg-01/`](fg-01/README.md) | Passive eight-coil field-generator assembly. Follow its DesignSpark source and fabrication notes. |
| `pen/` | Passive 5-DOF pen coil and shell |
| `mechanical/` | Enclosure, non-metal ICNIRP guard, mounts, camera bracket |
| `bom/` | System and board BOMs, connector requirements |

## Fixed decisions

- One board, BRD-01, 4 layers; FG-01 is separate; the pen is passive
  (`contract/decisions_log.md` #25).
- FPGA: XC7A35T-1FTG256C baseline, XC7A50T same footprint (#26).
- DAC80508 + 8× LTC1563-2; SPI 49.152 MHz (#19).
- AD7768-4 + INA163 + ADA4940-2 (#5/#17).
- Power: one medical-grade 15 V/60 W adapter; BRD-01 rails `+15V_FUSED`, `+6V`,
  `+3.3V`, `+5V_EXC`, `+5VA`, ±12VA (`docs/phase2/power_tree_v2.md`, decision
  #31, superseding the #20 part list); the arm STOP latch gates the follower,
  the driver rail is unswitched (#7/#10/#31, #25).
- No metal within 150 mm of the tracking volume; the ICNIRP guard is a non-metal
  access barrier, not a shield (`SC-04b`, D2).

## EDA

For BRD-01, open the project from `brd-01/kicad/` in your Git checkout.
Its tables find the shared library through relative paths. Commit KiCad
project files and leave `*-backups/`, `fp-info-cache` and `*.kicad_prl` local.
If the team changes to Altium/Fusion, revisit `.gitattributes` and LFS before
adding binary board files.

## Current status

The vendor references are pointers only. The KiCad scaffold and BOM-to-CAD
mapping are available; circuit capture and unresolved BOM selections remain.
Do not edit `vendor/`.

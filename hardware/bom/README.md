# BOM — system and board bills of materials

| File | Scope |
|---|---|
| `BOM_SYSTEM-01.xlsx` | System BOM Rev A (one controller + follower pair) |
| `BOM_ADC-01.xlsx` | ADC/front-end BOM |
| `BOM_PEN-ANA-01.xlsx` | Pen/analog BOM |
| `connector_requirements.xlsx` | Connector requirements |
| `BOM_template.xls` | Blank template |

Rules:

- No BOM row ships with a placeholder supplier P/N (decisions log, procurement
  checks).
- Re-quote the locked parts before ordering: DAC80508MRTET, LTC1563-2IGN#PBF,
  LMH6321MR/NOPB, AD7768-4, ADR434, INA163, ADA4940-2, ME60A1503F01, RV-1515D,
  XC7A35T-1FTG256C.
- `.xlsx` is binary; git cannot diff it. Keep the file small and export CSV when
  a diff matters.
- Cost target: ≤1000 CAD per controller + follower pair, or a documented
  deviation.

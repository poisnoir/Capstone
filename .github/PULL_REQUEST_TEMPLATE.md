## Summary

<!-- What changed and why. Link the issue. -->

## Contract impact

- [ ] No contract change
- [ ] Contract change — affected ID(s): <!-- SC-xx / decision #N / ICD / RQ-Mx -->
- [ ] PR body contains `Contract-Change: yes` (required for `contract/` PRs)
- [ ] `contract/VERSION`, `contract/CHANGELOG.md` and `contract/decisions_log.md` updated

## Tests / evidence

<!-- Commands run, measurements, screenshots, scope captures. -->

```text
python3 tools/check_doc_paths.py
python3 tools/check_references.py
python3 tools/contract_ci.py check
```

## Gate affected

<!-- SC-0 / FG-1 / DRV-2 / PEN-3 / FE-4 / ADC-5 / DIG-6 / INT-7 / none -->

## Checklist

- [ ] Docs/paths updated; `check_doc_paths.py` passes
- [ ] No third-party PDF, datasheet, vendor file or `.raw` added
- [ ] No file over 20 MB
- [ ] If the pico link changed: arm repo sync planned or done
- [ ] Reviewer(s) from the owning team requested

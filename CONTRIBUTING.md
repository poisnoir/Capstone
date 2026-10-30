# Contributing

## Onboarding (30 minutes)

1. Read `README.md`.
2. Read `contract/README.md`, `contract/system_contract.md` and
   `contract/decisions_log.md`.
3. Read your team's `AGENTS.md` and `README.md`.
4. Read `docs/phase2/design_order.md` for the stage gates.
5. Clone the repo and run the checks below.

## Branches and PRs

- `main` is the integration branch. Do not develop on `main`.
- Branch names: `fpga/…`, `hw/…`, `arm/…`, `contract/…`, `docs/…`, `tools/…`.
- Open a PR into `main`. Keep PRs small and scoped to one team unless the change
  is an interface change.
- Review rules:
  - Team folder: 1 approval from the same team.
  - `contract/`: 2 approvals — the interface owner on each side + the contract
    owner. Use the `contract-change` issue template.
  - A PR touching two team folders: one approval from each team.
- Enable the branch ruleset on `main` (public repos get it on GitHub Free):
  PR required, 1 approval, code owners, status checks, no force push. Until it
  is enabled, the `contract-guard` Action and these rules are the enforcement.

## Contract changes

1. Open a `contract-change` issue (affected SC/decision ID, old text, new text,
   reason, impact, gates to re-run).
2. Open a PR that changes `contract/` **and**:
   - bumps `contract/VERSION` (semver: MAJOR = breaking, MINOR = additive,
     PATCH = clarification),
   - adds a `contract/CHANGELOG.md` entry,
   - adds a row to `contract/decisions_log.md` (or marks the existing row),
   - puts `Contract-Change: yes` in the PR body.
3. Get two approvals. Merge. CI tags `contract-vX.Y.Z` and publishes the release.
4. Open the sync PR in the arm repo (or ask the arm team to run
   `contract-sync`). Update the pinned issue.

## Before pushing

```bash
python3 tools/check_doc_paths.py
python3 tools/check_references.py
python3 tools/contract_ci.py check
```

All three must pass. CI runs them again, plus `large-file-guard`.

## Files that must not be committed

- Third-party PDFs, datasheets, papers, the vendor snapshot, the thesis.
- `.raw` / `.op.raw` simulation output (regenerable from `.cir`).
- Any file over 20 MB. `large-file-guard` blocks it.
- Student IDs or personal data. The Phase 1 report is local-only and gitignored;
  never add it.

If you need a reference file, add a `docs/reference/manifest.yml` entry with the
acquisition method and regenerate `MANIFEST.md`:

```bash
python3 tools/gen_reference_manifest.py
```

## Weekly interface sync (15 min)

Use `docs/meetings/TEMPLATE.md`. Agenda:

1. Contract changes since last week (link the PRs).
2. Gate status (FG-1, DRV-2, PEN-3, FE-4, ADC-5, DIG-6, INT-7).
3. Cross-team blockers.
4. Decisions needed (link `contract-change` issues).
5. Next week's interface tests.

## Commits

- Small, focused commits. Imperative summary line.
- Reference the issue or contract ID when relevant.
- Do not commit generated files, caches or editor state.

## Reporting a bug

Use the `bug` issue template with expected/actual, reproduction steps and
evidence (log, screenshot, commit).

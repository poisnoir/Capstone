# GitHub setup

The repo is **public by choice**. The private files (Phase 1 report with student
IDs, `CLIENT_SETUP.md`, thesis `.txt` extracts) are gitignored. Before the first
push, run the guard; it refuses if a private file or student ID is tracked.

> If the team changes its mind and wants a private repo during the course:
> **Settings → General → Danger Zone → Change visibility → Make private**.

## 0. Pre-push check

```bash
git ls-files | grep -iE 'Phase 1 Report|CLIENT_SETUP|extracts/.*\.txt' && echo "private file tracked" || true
python3 tools/check_publish.py --public
```

`check_publish.py --public` fails on a tracked PDF, a student ID in text, a
tracked private file, or a file over 20 MB.

## 1. Push the first commit

```bash
cd /path/to/Capstone
./tools/push_first.sh
```

The guard runs the public-safety check and refuses any tracked file over 20 MB.
The plain `git push -u origin main` also works once the check is clean.

If the push is rejected for a file over 100 MB, something bypassed
`.gitignore`; run `git ls-files | xargs -I{} du -h {} | sort -h | tail` and
remove it before retrying.

## 2. Verify the contract release

The `contract-release` workflow runs on the first push to `main`. It should
create:

- tag `contract-v1.0.0`
- release assets `contract-v1.0.0.zip` and `contract-v1.0.0.json`
- rolling release `contract-latest` with `contract-latest.zip` / `.json`

Check **Actions** and **Releases**. If Actions is disabled or the workflow token
is read-only, enable it under **Settings → Actions → General** and re-run the
workflow.

## 3. Org teams and permissions

Create four teams in the `poisnoir` org and give each `Write` on the repo:

| Team | Members (fill in) | Repo access |
|---|---|---|
| `fpga` | Kevin, William, Amirmohammad | Write |
| `hardware` | Tung | Write |
| `robot-arm` | Tristan, Joyal | Write on the arm repo; Read/Triage here |
| `integration` | leads + contract owner | Write (owns `contract/`, `docs/`, `tools/`) |

Web UI: **Org → Teams → New team**, then **Repo → Settings → Collaborators and
teams → Add team**.

CLI (replace the placeholders):

```bash
for t in fpga hardware robot-arm integration; do
  gh api orgs/poisnoir/teams -f name="$t" -f privacy=closed || true
  gh api "orgs/poisnoir/teams/$t/repos/poisnoir/Capstone" -f permission=push || true
done
# add a member: gh api orgs/poisnoir/teams/fpga/memberships/USERNAME -f role=member
```

`CODEOWNERS` already references `@poisnoir/fpga`, `@poisnoir/hardware`,
`@poisnoir/robot-arm` and `@poisnoir/integration`. If you use different team
names, update `CODEOWNERS`.

## 4. Project board

Create an org-level Project **EM AccuBot** and link both repos (the arm repo can
be linked once it exists).

Fields:

| Field | Type | Values |
|---|---|---|
| Status | single select | Todo, In progress, Blocked, Done |
| Team | single select | FPGA, Hardware, Robot arm, Integration |
| Gate | single select | SC-0, FG-1, DRV-2, PEN-3, FE-4, ADC-5, DIG-6, INT-7 |
| Contract ID | text | SC-xx / decision #N |
| Priority | single select | P0, P1, P2 |

Views: **All**, **FPGA**, **Hardware**, **Robot arm**, **Contract & gates**,
**Blocked**, **This week**.

CLI can create the project (`gh project create --owner poisnoir --title
"EM AccuBot"`); fields and views are easiest in the web UI.

## 5. Labels and milestones

Labels:

```bash
for l in team/fpga team/hardware team/robot-arm team/integration \
         type/decision type/contract-change status/locked status/proposed \
         needs-review blocked task bug gate contract-change; do
  gh label create "$l" --repo poisnoir/Capstone --force || true
done
```

Milestones (one per gate):

```bash
for m in SC-0 FG-1 DRV-2 PEN-3 FE-4 ADC-5 DIG-6 INT-7; do
  gh api repos/poisnoir/Capstone/milestones -f title="$m" || true
done
```

## 6. Gate issues

Create one issue per gate from `.github/ISSUE_TEMPLATE/gate.yml`, paste the
checklist from `docs/phase2/design_order.md` §1, assign the owner, set the
milestone, and add it to the **Contract & gates** view. Closing the issue is the
sign-off.

## 7. Pinned contract issue

Create an issue titled **"Contract v1.0.0 — read before you build"**, body:

```text
Read contract/README.md, contract/system_contract.md and
contract/decisions_log.md before your first PR. Contract changes need a
contract-change issue, two approvals and a VERSION bump.
```

Pin it (issue → ... → Pin issue). This is the low-tech way to make the contract
visible to everyone.

## 8. Arm repo handshake

When the arm team creates its repo:

1. Add the `CONTRACT_READ_TOKEN` secret (fine-grained PAT, **Contents: Read** on
   `poisnoir/Capstone`).
2. Copy `robot-arm/templates/sync-contract.sh` → `capstone/tools/sync-contract.sh`.
3. Copy `robot-arm/templates/contract-sync.yml` and `contract-check.yml` →
   `.github/workflows/`.
4. Copy `robot-arm/templates/CONTRACT_VERSION.example` →
   `capstone/CONTRACT_VERSION`.
5. Run **Actions → contract-sync → Run workflow** with `latest`.
6. Link the arm repo to the Project and fill in `ARM_REPO_URL` in
   `robot-arm/README.md` with a PR.

## 9. Public-repo hygiene

- The Phase 1 report and thesis `.txt` extracts are local-only; never add them.
- Run `python3 tools/check_publish.py --public` before a release or after a
  dependency refresh.
- Confirm `git ls-files | grep -i '\.pdf$'` is empty.
- Enable a branch ruleset (public repos get it on GitHub Free): require a PR,
  1 approval, code owners, status checks, no force push, no deletion.
- Optional: enable GitHub Pages for a rendered docs site.

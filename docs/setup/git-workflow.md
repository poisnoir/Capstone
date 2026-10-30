# Git workflow

The old SFTP folder sync between `laptop` and `desktop` is replaced by git.
Keep the Tailscale link for remote desktop, not for file sync.

## First clone

```bash
git clone git@github.com:poisnoir/Capstone.git
cd Capstone
```

The remote is public. If SSH is not set up, add your public key to GitHub
(`~/.ssh/id_ed25519.pub` → GitHub → Settings → SSH keys) or use HTTPS with a
personal access token.

## Daily flow

```bash
git switch main
git pull --ff-only
git switch -c fpga/dds-lut      # or hw/..., arm/..., contract/..., docs/...
# edit
python3 tools/check_doc_paths.py
python3 tools/check_references.py
python3 tools/contract_ci.py check
git add -A
git commit -m "fpga: add 4096-entry DDS LUT"
git push -u origin fpga/dds-lut
```

Open a PR into `main`. Review rules are in `CONTRIBUTING.md`.

## Contract changes

The contract is not a normal folder. Follow `contract/README.md`:

1. `contract-change` issue.
2. PR with `VERSION`, `CHANGELOG.md`, `decisions_log.md` updates and
   `Contract-Change: yes` in the body.
3. Two approvals.
4. CI tags `contract-vX.Y.Z` and publishes the release.
5. Sync the arm repo and update the pinned issue.

## Two machines

Use git on both machines:

```bash
# laptop
git push origin main

# desktop
git pull --ff-only
```

Do not copy the folder over SFTP; divergent copies are how the old sync broke.
If you need to work on the desktop, clone there once and pull.

## What not to commit

`vendor/`, `reference-cache/`, root PDFs, `docs/extracts/*.pdf`, `.raw` output,
and any file over 20 MB. See `docs/reference/MANIFEST.md`. `large-file-guard`
blocks new large files in CI.

## If you accidentally commit a large file

```bash
git rm --cached path/to/file
git commit -m "chore: remove accidental large file"
```

If it is already pushed, tell the contract owner before rewriting history; a
force-push on `main` is not allowed.

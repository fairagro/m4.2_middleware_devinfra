## MODIFIED Requirements

### Requirement: Generic postCreate installs hooks, optional public GPG keys, and IDE extensions

`scripts/devcontainer-post-create.sh` MUST remain free of hardcoded product workspace names. On Dev Container create it
MUST: fix documented volume permissions when present; sync `.python-version` via `scripts/load-versions-env.sh`; run
`uv sync --dev --all-packages` when a root `pyproject.toml` exists (dev dependency group and all uv workspace members —
aligned with shared reusable code-quality CI) **with uv malware check enabled** (`UV_MALWARE_CHECK=1` or equivalent);
install the commit-stage hook with `pre-commit install --hook-type pre-commit` (via the synced environment); run
`./scripts/setup-git-hooks.sh`; import public GPG keys by invoking the shared **`scripts/import-public-gpg-keys.sh`**
when that script exists (the script MUST import `public_gpg_keys/*.asc` when present and MUST exit successfully when the
directory is absent or empty); attempt to install recommended IDE extensions via Cursor/VS Code remote CLI when
available (at least `charliermarsh.ruff`; MUST NOT fail the whole postCreate if the CLI or an extension install is
missing); and **after** those shared steps (**T-late**), run every `scripts/devcontainer-post-create.d/*` drop-in in
lexicographic order when that directory has matching entries (`nullglob`: absent or empty directory MUST skip cleanly).
Each present drop-in MUST be a regular file and executable; a missing execute bit or non-zero exit MUST fail the whole
postCreate (**hard-fail**). Shared postCreate MUST NOT hard-code optional product-local script names (e.g.
`scripts/install-dev-hooks.sh`, `scripts/setup-git-lfs.sh`). The Ruff CLI MUST come from the uv project environment
after sync. This repository’s `devcontainer.json` MUST list the shared product IDE extension set (Docker / Helm / Python
/ Ruff / Pylint / Mypy / PlantUML / Prettier / markdownlint / signageos SOPS, Kubernetes Tools, and related helpers used
across the three product repos) and postCreate MUST attempt soft-fail install of that same set via remote CLI when
available. The list MUST include at least: `charliermarsh.ruff`, `jebbs.plantuml`, `signageos.signageos-vscode-sops`
(Open VSX / Cursor-supported SOPS editor; MUST NOT require `shipitsmarter.sops-edit` in the shared recommendation list),
`esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`, and `ms-kubernetes-tools.vscode-kubernetes-tools`.

#### Scenario: Fresh Dev Container create

- **WHEN** postCreate runs in this repo’s Linux Dev Container after create
- **THEN** `.python-version` matches `PYTHON_VERSION` from `versions.env`
- **AND** the commit-stage pre-commit hook is installed
- **AND** project hooks from `scripts/git-hooks/` are installed via `setup-git-hooks.sh` (dispatcher +
  `pre-push.d/50-quality`)
- **AND** `uv run ruff --version` works after sync when ruff is a project dependency
- **AND** postCreate does not abort solely because an IDE extension could not be installed
- **AND** if `public_gpg_keys/*.asc` is absent, postCreate still completes successfully
- **AND** if `scripts/devcontainer-post-create.d/` is absent or empty, postCreate completes successfully
- **AND** postCreate does not call `scripts/install-dev-hooks.sh` or `scripts/setup-git-lfs.sh` by those hard-coded
  names even if those files exist

#### Scenario: Post-create sync enables malware check

- **WHEN** postCreate runs `uv sync` because a root `pyproject.toml` exists
- **THEN** the malware check is enabled for that sync

#### Scenario: Product postCreate drop-ins run at T-late

- **WHEN** postCreate runs and `scripts/devcontainer-post-create.d/` contains one or more executable drop-in scripts
- **THEN** those scripts run in lexicographic order after shared hook install and the other shared postCreate steps
- **AND** if any drop-in exits non-zero, postCreate fails

#### Scenario: Non-executable drop-in fails hard

- **WHEN** postCreate runs and `scripts/devcontainer-post-create.d/` contains a non-executable regular file matching the
  drop-in glob
- **THEN** postCreate fails without treating the file as optional soft-skip

#### Scenario: Public GPG keys present

- **WHEN** postCreate runs and `public_gpg_keys/*.asc` files exist
- **THEN** those public keys are imported with `gpg` (via `scripts/import-public-gpg-keys.sh` when that script exists)
  for SOPS encrypt / recipient checks

#### Scenario: Public GPG keys imported via shared script

- **WHEN** postCreate runs and `scripts/import-public-gpg-keys.sh` exists
- **THEN** postCreate invokes that script (not an inline one-off import loop)
- **AND** when no `.asc` files are present, the script and postCreate still succeed

#### Scenario: Kubernetes Tools is on the shared extension list

- **WHEN** a contributor inspects `.devcontainer/devcontainer.json` extensions and the postCreate extension array
- **THEN** both include `ms-kubernetes-tools.vscode-kubernetes-tools`

## ADDED Requirements

### Requirement: Shared import-public-gpg-keys script

The repository MUST provide `scripts/import-public-gpg-keys.sh` that imports every `public_gpg_keys/*.asc` with
`gpg --batch --import`, exits 0 when no keys are present, and fails closed when `gpg` is missing but keys exist.
Documentation (`docs/devcontainer.md`) MUST describe root `public_gpg_keys/` + `.sops.yaml` as the per-repo recipient
layout (content not synced) and MUST note that adding a recipient requires `sops updatekeys` on existing ciphertext by
someone who can decrypt.

#### Scenario: Import script soft-skips empty key dir

- **WHEN** a contributor runs `scripts/import-public-gpg-keys.sh` with no `public_gpg_keys/*.asc`
- **THEN** the script exits 0 without failing

#### Scenario: Docs describe recipient layout

- **WHEN** a contributor reads Dev Container / secrets docs
- **THEN** they learn public keys live under `public_gpg_keys/` and recipients under `.sops.yaml`
- **AND** they learn `sops updatekeys` is required after adding fingerprints to existing enc files

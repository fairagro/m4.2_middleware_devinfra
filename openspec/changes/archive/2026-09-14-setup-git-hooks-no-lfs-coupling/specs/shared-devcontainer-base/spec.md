## MODIFIED Requirements

### Requirement: Generic postCreate installs hooks, optional public GPG keys, and IDE extensions

`scripts/devcontainer-post-create.sh` MUST remain free of hardcoded product workspace names. On Dev Container create it
MUST: fix documented volume permissions when present; sync `.python-version` via `scripts/load-versions-env.sh`; run
`uv sync --dev --all-packages` when a root `pyproject.toml` exists (dev dependency group and all uv workspace members —
aligned with shared reusable code-quality CI); install the commit-stage hook with
`pre-commit install --hook-type pre-commit` (via the synced environment); run `./scripts/setup-git-hooks.sh`; import
`public_gpg_keys/*.asc` when that directory contains `.asc` files (MUST skip cleanly when absent or empty); and attempt
to install recommended IDE extensions via Cursor/VS Code remote CLI when available (at least `charliermarsh.ruff`; MUST
NOT fail the whole postCreate if the CLI or an extension install is missing). The Ruff CLI MUST come from the uv project
environment after sync. This repository’s `devcontainer.json` MUST list the shared product IDE extension set (Docker /
Helm / Python / Ruff / Pylint / Mypy / PlantUML / Prettier / markdownlint / signageos SOPS, and related helpers used
across the three product repos) and postCreate MUST attempt soft-fail install of that same set via remote CLI when
available. The list MUST include at least: `charliermarsh.ruff`, `jebbs.plantuml`, `signageos.signageos-vscode-sops`
(Open VSX / Cursor-supported SOPS editor; MUST NOT require `shipitsmarter.sops-edit` in the shared recommendation list),
`esbenp.prettier-vscode`, and `davidanson.vscode-markdownlint`. Shared postCreate MUST NOT invoke optional product-local
scripts when present (e.g. `scripts/install-dev-hooks.sh`, `scripts/setup-git-lfs.sh`); product-owned tooling such as
Git LFS overlays is applied only by product processes outside this shared script.

#### Scenario: Fresh Dev Container create

- **WHEN** postCreate runs in this repo’s Linux Dev Container after create
- **THEN** `.python-version` matches `PYTHON_VERSION` from `versions.env`
- **AND** the commit-stage pre-commit hook is installed
- **AND** project hooks from `scripts/git-hooks/` are installed via `setup-git-hooks.sh`
- **AND** `uv run ruff --version` works after sync when ruff is a project dependency
- **AND** postCreate does not abort solely because an IDE extension could not be installed
- **AND** if `public_gpg_keys/*.asc` is absent, postCreate still completes successfully
- **AND** postCreate does not call `scripts/install-dev-hooks.sh` or `scripts/setup-git-lfs.sh` even if those files
  exist

#### Scenario: Public GPG keys present

- **WHEN** postCreate runs and `public_gpg_keys/*.asc` files exist
- **THEN** those public keys are imported with `gpg` for SOPS encrypt / recipient checks

### Requirement: Consumer overlay documentation

Documentation (`docs/devcontainer.md`, `docs/sync.md`, `docs/quality.md`, and/or README) MUST state that
`.devcontainer/devcontainer.json` and `.devcontainer/docker-compose.yml` are **verbatim** sync blobs (on the sync
allowlist): products MUST adopt them without post-sync hand-edits. The shared JSON MUST use `workspaceFolder`
`/workspace`, window `name` from `${localWorkspaceFolderBasename}`, and named volume `source=` values derived from
`${localWorkspaceFolderBasename}` so repos do not need product-specific JSON keys for those concerns. The shared Compose
MUST use the matching `..:/workspace` bind. Repo-specific container environment (e.g. `MYPYPATH`, `CST_BAKE_TARGET`)
MUST NOT be edited into synced JSON or Compose; documentation MUST point to an optional product-owned
`.devcontainer/product.env` (not synced; referenced from shared Compose when present) and/or process env / reusable CI
inputs — not Dev Container `remoteEnv` for those product overlays. Shared fragments MUST NOT hardcode another product’s
host folder name as `workspaceFolder` or as a fixed volume source prefix. Docs MUST state that product **ciphertext**
and recipient config (`.sops.yaml`, encrypted secret files) and `public_gpg_keys` **content** stay in each product repo,
while the shared image provides sops/age/gpg/JRE/graphviz and postCreate performs key import when keys are present. Docs
MUST state that **Git LFS** is not part of the shared image or shared hook installer: products that need LFS MUST own
install and hook overlay entirely in the product repo (independent of Devinfra); shared `setup-git-hooks.sh` MUST NOT
remove LFS hooks; shared postCreate MUST NOT call product LFS scripts; docs MUST NOT recommend editing synced JSON
`postCreate` for LFS. Docs MUST NOT describe a standing “thin `devcontainer.json` overlay” adopt pattern. Docs MUST
state the bashrc-free shell contract: synced `devcontainer.json` MUST set `remoteEnv.PATH` to prepend `.venv/bin` and
`scripts/bin`; fleet shell init MUST NOT patch `~/.bashrc` for PATH, aliases, tokens, completions, or sourcing
`load-env.sh`; kubectl/docker short-name bash completion is provided by the shared image; optional
`.env.integration.enc` decrypt runs in shared postCreate and does not auto-export into every shell; product-local
`load-env.sh` / bashrc wiring is deprecated in favor of this contract (product migration tracked in follow-up issues).

#### Scenario: Contributor reads overlay guidance

- **WHEN** a contributor opens the Dev Container docs for product adoption
- **THEN** they learn `devcontainer.json` and `docker-compose.yml` are adopted verbatim from Devinfra sync
- **AND** they learn the in-container workspace path is `/workspace` for all middleware repos
- **AND** they learn window title and history/gh volume names come from `${localWorkspaceFolderBasename}`
- **AND** they learn product-only env belongs in optional `.devcontainer/product.env` and/or CI/hook env — not in synced
  JSON/Compose `remoteEnv` overlays such as `MYPYPATH`
- **AND** they learn secret file **content** stays product-local while tooling and key-import behavior are shared
- **AND** they learn Prettier + markdownlint-cli2 (and their extensions) are the shared markdown format/lint stack that
  replaces or supplements prior product-local markdown tooling on sync
- **AND** they learn Git LFS is product-owned and independent of shared hooks/postCreate (no synced JSON postCreate
  snippet; no shared callback into product LFS scripts)
- **AND** they learn synced `remoteEnv.PATH` prepends `.venv/bin` and `scripts/bin` without patching `~/.bashrc`
- **AND** they learn `k`/`d` bash completion comes from the shared image completion files
- **AND** they learn product `load-env.sh` / bashrc sourcing is not the shared pattern after sync adopt

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
Helm / Python / Ruff / Pylint / Mypy / PlantUML / Prettier / markdownlint / signageos SOPS, Kubernetes Tools, and
related helpers used across the three product repos) and postCreate MUST attempt soft-fail install of that same set via
remote CLI when available. The list MUST include at least: `charliermarsh.ruff`, `jebbs.plantuml`,
`signageos.signageos-vscode-sops` (Open VSX / Cursor-supported SOPS editor; MUST NOT require `shipitsmarter.sops-edit`
in the shared recommendation list), `esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`, and
`ms-kubernetes-tools.vscode-kubernetes-tools`. Shared postCreate MUST NOT invoke optional product-local scripts when
present (e.g. `scripts/install-dev-hooks.sh`, `scripts/setup-git-lfs.sh`); product-owned tooling such as Git LFS
overlays is applied only by product processes outside this shared script.

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

#### Scenario: Kubernetes Tools is on the shared extension list

- **WHEN** a contributor inspects `.devcontainer/devcontainer.json` extensions and the postCreate extension array
- **THEN** both include `ms-kubernetes-tools.vscode-kubernetes-tools`

## ADDED Requirements

### Requirement: Synced workspace recommendations match Dev Container extensions

The repository MUST provide `.vscode/extensions.json` with a `recommendations` array whose extension IDs are exactly the
same set as `.devcontainer/devcontainer.json` `customizations.vscode.extensions` (and the postCreate install list). That
file MUST be on the product sync allowlist. Products MUST NOT need a forked recommendations file for the shared set.

#### Scenario: Recommendations align with Dev Container

- **WHEN** a contributor compares `.vscode/extensions.json` `recommendations` to the Dev Container extension list
- **THEN** the two sets contain the same extension IDs (including Kubernetes Tools)
- **AND** `.vscode/extensions.json` appears on the sync allowlist

### Requirement: Synced IDE settings for Helm templates and kubeconfig alerts

Synced `.vscode/settings.json` MUST set `files.associations` so paths under `**/helmchart/**/templates/**` and
`**/helm/**/templates/**` with extensions `.yaml`, `.yml`, and `.tpl` use language mode `helm`. It MUST set
`vs-kubernetes.suppress-kubeconfig-not-found-alerts` to `true`. It MUST NOT set
`vs-kubernetes.suppress-kubectl-not-found-alerts` solely for this change. Those Helm/`vs-kubernetes` keys MUST live in
`.vscode/settings.json` and MUST NOT be duplicated under `.devcontainer/devcontainer.json`
`customizations.vscode.settings`. Documentation MUST note that Helm templates use language `helm` via Kubernetes Tools
and that missing-kubeconfig alerts are suppressed for chart editing without a cluster config.

#### Scenario: Helm associations and kubeconfig suppress in workspace settings

- **WHEN** a contributor inspects synced `.vscode/settings.json`
- **THEN** `files.associations` maps helmchart and helm template globs to `helm`
- **AND** `vs-kubernetes.suppress-kubeconfig-not-found-alerts` is `true`
- **AND** those keys are absent from `devcontainer.json` `customizations.vscode.settings`

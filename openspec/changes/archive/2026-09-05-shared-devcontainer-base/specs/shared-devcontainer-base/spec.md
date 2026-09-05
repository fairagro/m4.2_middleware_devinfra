# shared-devcontainer-base Specification

## Purpose

Canonical shared Dev Container image, version pins, generic postCreate, and overlay docs so product repos keep only thin
`devcontainer.json` overlays while the base toolchain lives in this Devinfra repo.

## ADDED Requirements

### Requirement: Shared Dev Container image and versions.env

The repository MUST provide `.devcontainer/Dockerfile` and repo-root `versions.env` (consumed via Compose build-args /
`.devcontainer/.env` symlink) that define the **shared product Dev Container toolchain** used by the three m4.2 product
repos: base image pin, Python/uv, Node/OpenSpec, GitHub CLI prerequisites, Git LFS, **jq**, **yq**, **xq**, hadolint,
Starship, container-structure-test, yamlfmt, kubectl, Helm, Minikube, **SOPS**, **age**, **gnupg** (gpg on `PATH`),
**default-jre-headless** (or equivalent JRE), **graphviz**, **Trivy**, and the **Renovate** CLI, plus **Prettier** and
**markdownlint-cli2** (global CLI pins in `versions.env`). The shared image MUST NOT require difftastic. Exact tool
versions MUST live only in `versions.env` (one pin source), except distro packages (e.g. `jq`, `gnupg`, JRE, graphviz)
installed from the base image’s package manager without a separate `versions.env` pin. **yq** (mikefarah), **xq** (XML
query CLI), and **Trivy** MUST be pinned in `versions.env` and installed as release binaries on `PATH`. **Renovate**
MUST be pinned in `versions.env` and installed as a global npm CLI (same pattern as OpenSpec / Prettier). Prettier /
markdownlint-cli2 and their IDE extensions (`esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`) are part of the
**shared** toolchain: when synced into product repos they MUST **replace or supplement** each product’s prior markdown
format/lint feature so consumers converge on one stack. Shipping Trivy/Renovate CLIs in the image does **not** by itself
require shipping reusable GitHub Actions workflows (those remain later CI issues).

#### Scenario: Rebuild uses pinned shared toolchain

- **WHEN** a contributor rebuilds the Dev Container from this repo’s compose/Dockerfile
- **THEN** the image builds with toolchain versions from `versions.env`
- **AND** the shared product tools listed above are available in the container on the documented happy path
- **AND** `jq`, `yq`, and `xq` are on `PATH`
- **AND** `prettier` and `markdownlint-cli2` are on `PATH` from the shared image pins
- **AND** `trivy` and `renovate` are on `PATH`
- **AND** `sops`, `age`, `gpg`, and a JRE/`java` plus `dot` (graphviz) are available on the documented happy path
- **AND** difftastic is not part of the required shared toolchain

### Requirement: Generic postCreate installs hooks, optional public GPG keys, and IDE extensions

`scripts/devcontainer-post-create.sh` MUST remain free of hardcoded product workspace names. On Dev Container create it
MUST: fix documented volume permissions when present; sync `.python-version` via `scripts/load-versions-env.sh`; run
project `uv sync` when a root `pyproject.toml` exists; install the commit-stage hook with
`pre-commit install --hook-type pre-commit` (via the synced environment); run `./scripts/setup-git-lfs.sh`; import
`public_gpg_keys/*.asc` when that directory contains `.asc` files (MUST skip cleanly when absent or empty); and attempt
to install recommended IDE extensions via Cursor/VS Code remote CLI when available (at least `charliermarsh.ruff`; MUST
NOT fail the whole postCreate if the CLI or an extension install is missing). The Ruff CLI MUST come from the uv project
environment after sync. This repository’s `devcontainer.json` MUST list the shared product IDE extension set (Docker /
Helm / Python / Ruff / Pylint / Mypy / PlantUML / Prettier / markdownlint / signageos SOPS, and related helpers used
across the three product repos) and postCreate MUST attempt soft-fail install of that same set via remote CLI when
available. The list MUST include at least: `charliermarsh.ruff`, `jebbs.plantuml`, `signageos.signageos-vscode-sops`
(Open VSX / Cursor-supported SOPS editor; MUST NOT require `shipitsmarter.sops-edit` in the shared recommendation list),
`esbenp.prettier-vscode`, and `davidanson.vscode-markdownlint`.

#### Scenario: Fresh Dev Container create

- **WHEN** postCreate runs in this repo’s Linux Dev Container after create
- **THEN** `.python-version` matches `PYTHON_VERSION` from `versions.env`
- **AND** the commit-stage pre-commit hook is installed
- **AND** Git LFS local config and project hooks from `scripts/git-hooks/` are installed via `setup-git-lfs.sh`
- **AND** `uv run ruff --version` works after sync when ruff is a project dependency
- **AND** postCreate does not abort solely because an IDE extension could not be installed
- **AND** if `public_gpg_keys/*.asc` is absent, postCreate still completes successfully

#### Scenario: Public GPG keys present

- **WHEN** postCreate runs and `public_gpg_keys/*.asc` files exist
- **THEN** those public keys are imported with `gpg` for SOPS encrypt / recipient checks

### Requirement: Consumer overlay documentation

Documentation (`docs/devcontainer.md` and/or README) MUST state that product repos keep a thin `devcontainer.json`
overlay owning at least `name`, `workspaceFolder`, and distinct Docker volume `source=` names (and MAY trim or add
extensions), while shared Dockerfile, compose build definition, `versions.env`, and scripts are consumed from this
Devinfra repo (via sync). Shared fragments MUST NOT hardcode another product’s `workspaceFolder` or volume source names.
Docs MUST state that product **ciphertext** and recipient config (`.sops.yaml`, encrypted secret files) and
`public_gpg_keys` **content** stay in each product repo, while the shared image provides sops/age/gpg/JRE/graphviz and
postCreate performs key import when keys are present.

#### Scenario: Contributor reads overlay guidance

- **WHEN** a contributor opens the Dev Container docs for product adoption
- **THEN** they learn which fields stay product-local in `devcontainer.json`
- **AND** they learn the shared image/`versions.env`/scripts live in Devinfra and must not encode another product’s
  folder or volume names
- **AND** they learn secret file **content** stays product-local while tooling and key-import behavior are shared
- **AND** they learn Prettier + markdownlint-cli2 (and their extensions) are the shared markdown format/lint stack that
  replaces or supplements prior product-local markdown tooling on sync

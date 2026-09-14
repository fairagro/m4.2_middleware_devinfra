# shared-devcontainer-base Specification

## Purpose

Canonical shared Dev Container image, version pins, generic postCreate, and overlay docs so product repos keep only thin
`devcontainer.json` overlays while the base toolchain lives in this Devinfra repo.

## Requirements

### Requirement: Shared Dev Container image and versions.env

The repository MUST provide `.devcontainer/Dockerfile` and repo-root `versions.env` (consumed via Compose build-args /
`.devcontainer/.env` symlink) that define the **shared product Dev Container toolchain** used by the three m4.2 product
repos: base image pin, Python/uv, Node/OpenSpec, GitHub CLI prerequisites, **jq**, **yq**, **xq**, hadolint, Starship,
container-structure-test, yamlfmt, kubectl, Helm, Minikube, **SOPS**, **age**, **gnupg** (gpg on `PATH`),
**default-jre-headless** (or equivalent JRE), **graphviz**, **Trivy**, and the **Renovate** CLI, plus **Prettier** and
**markdownlint-cli2** (global CLI pins in `versions.env`). The shared image MUST NOT require difftastic and MUST NOT
require **Git LFS** (`git-lfs` MUST NOT be a required shared apt/package install; MUST NOT run
`git lfs install --system` as part of the shared image build). Exact tool versions MUST live only in `versions.env` (one
pin source), except distro packages (e.g. `jq`, `gnupg`, JRE, graphviz) installed from the base image’s package manager
without a separate `versions.env` pin. **yq** (mikefarah), **xq** (XML query CLI), and **Trivy** MUST be pinned in
`versions.env` and installed as release binaries on `PATH`. **Renovate** MUST be pinned in `versions.env` and installed
as a global npm CLI (same pattern as OpenSpec / Prettier). Prettier / markdownlint-cli2 and their IDE extensions
(`esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`) are part of the **shared** toolchain: when synced into
product repos they MUST **replace or supplement** each product’s prior markdown format/lint feature so consumers
converge on one stack. Shipping the Renovate CLI in the image MUST be documented together with the shared Renovate
config and per-repo workflow (`shared-renovate` capability). Shipping Trivy in the image does **not** by itself require
shipping a reusable Trivy GitHub Actions workflow (that remains a separate CI concern).

#### Scenario: Rebuild uses pinned shared toolchain

- **WHEN** a contributor rebuilds the Dev Container from this repo’s compose/Dockerfile
- **THEN** the image builds with toolchain versions from `versions.env`
- **AND** the shared product tools listed above are available in the container on the documented happy path
- **AND** `jq`, `yq`, and `xq` are on `PATH`
- **AND** `prettier` and `markdownlint-cli2` are on `PATH` from the shared image pins
- **AND** `trivy` and `renovate` are on `PATH`
- **AND** `sops`, `age`, `gpg`, and a JRE/`java` plus `dot` (graphviz) are available on the documented happy path
- **AND** difftastic is not part of the required shared toolchain
- **AND** `git-lfs` is not required on the shared image happy path

#### Scenario: Dev Container docs link Renovate CLI to shared automation

- **WHEN** a contributor reads Dev Container docs for Trivy / Renovate local CLIs
- **THEN** they learn `renovate` on `PATH` is for local dry-runs against the shared Renovate config
- **AND** they are pointed at the shared Renovate workflow/docs (not only “workflow deferred to open issues”)

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
`esbenp.prettier-vscode`, and `davidanson.vscode-markdownlint`.

#### Scenario: Fresh Dev Container create

- **WHEN** postCreate runs in this repo’s Linux Dev Container after create
- **THEN** `.python-version` matches `PYTHON_VERSION` from `versions.env`
- **AND** the commit-stage pre-commit hook is installed
- **AND** project hooks from `scripts/git-hooks/` are installed via `setup-git-hooks.sh`
- **AND** `uv run ruff --version` works after sync when ruff is a project dependency
- **AND** postCreate does not abort solely because an IDE extension could not be installed
- **AND** if `public_gpg_keys/*.asc` is absent, postCreate still completes successfully

#### Scenario: Public GPG keys present

- **WHEN** postCreate runs and `public_gpg_keys/*.asc` files exist
- **THEN** those public keys are imported with `gpg` for SOPS encrypt / recipient checks

### Requirement: Bashrc-free PATH for venv and scripts/bin

This repository’s Dev Container `remoteEnv` MUST prepend `${workspaceFolder}/.venv/bin` and
`${workspaceFolder}/scripts/bin` on `PATH` (scripts/bin before or after `.venv/bin` is allowed as long as both appear
before the inherited container `PATH`). Shared postCreate and personal-token helpers MUST NOT patch `~/.bashrc` (or
other user shell profiles) to inject that PATH or to source a load-env script. Documentation MUST state that product
`devcontainer.json` overlays MUST carry the same `remoteEnv.PATH` contract so every integrated terminal and remote
process sees uv tool binaries and `scripts/bin` wrappers without home-profile mutation.

#### Scenario: Devinfra remoteEnv includes venv and scripts/bin

- **WHEN** a contributor inspects this repository’s `.devcontainer/devcontainer.json` `remoteEnv.PATH`
- **THEN** both `${workspaceFolder}/.venv/bin` and `${workspaceFolder}/scripts/bin` appear on that PATH value
- **AND** postCreate does not append a `source …/load-env.sh` (or equivalent) line to `~/.bashrc`

#### Scenario: Docs require the same PATH contract for products

- **WHEN** a contributor reads Dev Container adoption docs for product overlays
- **THEN** they learn product `devcontainer.json` MUST set the same `remoteEnv.PATH` prepend for `.venv/bin` and
  `scripts/bin`
- **AND** they learn the fleet MUST NOT rely on patching `~/.bashrc` for that PATH

### Requirement: kubectl and docker shortcut wrappers on scripts/bin

The repository MUST provide executable wrappers under `scripts/bin/` that invoke the shared Dev Container’s kubectl and
docker installs (`/usr/local/bin/kubectl` from the shared Dockerfile pin; `/usr/bin/docker` from the Docker-in-Docker
feature) under the short names formerly used as product bash aliases (`k`, `d`). Those wrappers MUST be listed on the
product sync allowlist with other `scripts/bin` helpers. The wrappers MUST NOT search `PATH` for alternate binaries,
MUST NOT load personal tokens, and MUST NOT patch shell profiles.

#### Scenario: Short names resolve via scripts/bin

- **WHEN** `scripts/bin` is on `PATH` and a contributor runs `k` or `d` in the shared Linux Dev Container
- **THEN** `k` execs `/usr/local/bin/kubectl` and `d` execs `/usr/bin/docker`
- **AND** the wrappers do not source `dev-tokens.sh` or modify `~/.bashrc`

### Requirement: Image bash-completion for kubectl and docker short names

The shared Dev Container image MUST install bash-completion entries under `/usr/share/bash-completion/completions/` for
the short names `k` and `d` that register the same completion functions as `kubectl` and `docker` (respectively),
without patching `~/.bashrc`. The `k` entry MUST reuse the image’s kubectl completion (already generated at image
build). The `d` entry MUST bind to docker’s completion function when the docker completion file is available in the
running container (e.g. after the Docker-in-Docker feature installs the client). Documentation MUST state that
short-name completion comes from the shared image, not from product `load-env.sh`.

#### Scenario: k completion registered in the image

- **WHEN** a contributor inspects `/usr/share/bash-completion/completions/k` in the shared image
- **THEN** that file registers programmable completion for `k` using `__start_kubectl`
- **AND** it does not instruct products to patch `~/.bashrc` for that binding

#### Scenario: d completion registered for docker short name

- **WHEN** bash-completion loads the `d` completion entry and docker’s completion function is available
- **THEN** `d` is registered with `__start_docker` (or equivalent docker completion entrypoint)
- **AND** no `~/.bashrc` mutation is required for that registration

### Requirement: Optional postCreate decrypt of integration env ciphertext

When postCreate runs in a Linux Dev Container and the repository root contains a SOPS-encrypted `.env.integration.enc`,
postCreate MUST attempt to decrypt it to repo-root `.env` using `sops` when available. If `.env` already exists and is
non-empty, postCreate MUST skip decryption. If the ciphertext file is absent, or `sops` / keys are unavailable,
postCreate MUST skip cleanly without failing the whole create. PostCreate MUST NOT patch `~/.bashrc` to auto-`source`
`.env` into interactive shells; leaving the plaintext `.env` file for `dev_environment` / tests that read it is
sufficient.

#### Scenario: Ciphertext present and decrypt succeeds

- **WHEN** postCreate runs and `.env.integration.enc` exists as SOPS ciphertext and decrypt succeeds
- **THEN** repo-root `.env` is written (or left unchanged if already non-empty)
- **AND** postCreate does not append bashrc lines that `source` `.env`

#### Scenario: Ciphertext absent

- **WHEN** postCreate runs and `.env.integration.enc` is missing
- **THEN** postCreate completes successfully without requiring SOPS decrypt

### Requirement: Consumer overlay documentation

Documentation (`docs/devcontainer.md` and/or README) MUST state that product repos keep a thin `devcontainer.json`
overlay owning at least `name`, `workspaceFolder`, and distinct Docker volume `source=` names (and MAY trim or add
extensions), while shared Dockerfile, compose build definition, `versions.env`, and scripts are consumed from this
Devinfra repo (via sync). Shared fragments MUST NOT hardcode another product’s `workspaceFolder` or volume source names.
Docs MUST state that product **ciphertext** and recipient config (`.sops.yaml`, encrypted secret files) and
`public_gpg_keys` **content** stay in each product repo, while the shared image provides sops/age/gpg/JRE/graphviz and
postCreate performs key import when keys are present. Docs MUST state that **Git LFS** is not part of the shared image;
products that need LFS (e.g. sql-to-arc) MUST install it in a product-owned path that sync of the shared Dockerfile does
not overwrite (e.g. product postCreate or a non-synced local fragment). Docs MUST state the bashrc-free shell contract:
product overlays MUST set `remoteEnv.PATH` to prepend `.venv/bin` and `scripts/bin`; fleet shell init MUST NOT patch
`~/.bashrc` for PATH, aliases, tokens, completions, or sourcing `load-env.sh`; kubectl/docker short-name bash completion
is provided by the shared image; optional `.env.integration.enc` decrypt runs in shared postCreate and does not
auto-export into every shell; product-local `load-env.sh` / bashrc wiring is deprecated in favor of this contract
(product migration tracked in follow-up issues, not required inside the Devinfra MVP PR).

#### Scenario: Contributor reads overlay guidance

- **WHEN** a contributor opens the Dev Container docs for product adoption
- **THEN** they learn which fields stay product-local in `devcontainer.json`
- **AND** they learn the shared image/`versions.env`/scripts live in Devinfra and must not encode another product’s
  folder or volume names
- **AND** they learn secret file **content** stays product-local while tooling and key-import behavior are shared
- **AND** they learn Prettier + markdownlint-cli2 (and their extensions) are the shared markdown format/lint stack that
  replaces or supplements prior product-local markdown tooling on sync
- **AND** they learn Git LFS is product-local when needed, not a shared base requirement
- **AND** they learn `remoteEnv.PATH` must prepend `.venv/bin` and `scripts/bin` without patching `~/.bashrc`
- **AND** they learn `k`/`d` bash completion comes from the shared image completion files
- **AND** they learn product `load-env.sh` / bashrc sourcing is not the shared pattern after sync adopt

# shared-devcontainer-base Specification

## Purpose

Canonical shared Dev Container image, version pins, generic postCreate, and verbatim-shared `devcontainer.json` plus
`docker-compose.yml` (`/workspace`, basename window title and volumes) so product repos adopt those entry files without
post-sync hand-edits; product-only container env uses optional non-synced `product.env` and/or CI inputs.

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
shipping a reusable Trivy GitHub Actions workflow (that remains a separate CI concern). The shared
`.devcontainer/docker-compose.yml` MUST bind the repo at `..:/workspace:cached` (or equivalent consistency flag) so the
Compose workspace path matches the shared `devcontainer.json` `workspaceFolder`.

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
- **AND** the Compose service binds the repository at `/workspace` in the container

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
`public_gpg_keys/*.asc` when that directory contains `.asc` files (MUST skip cleanly when absent or empty); attempt to
install recommended IDE extensions via Cursor/VS Code remote CLI when available (at least `charliermarsh.ruff`; MUST NOT
fail the whole postCreate if the CLI or an extension install is missing); and **after** those shared steps (**T-late**),
run every `scripts/devcontainer-post-create.d/*` drop-in in lexicographic order when that directory has matching entries
(`nullglob`: absent or empty directory MUST skip cleanly). Each present drop-in MUST be a regular file and executable; a
missing execute bit or non-zero exit MUST fail the whole postCreate (**hard-fail**). Shared postCreate MUST NOT
hard-code optional product-local script names (e.g. `scripts/install-dev-hooks.sh`, `scripts/setup-git-lfs.sh`). The
Ruff CLI MUST come from the uv project environment after sync. This repository’s `devcontainer.json` MUST list the
shared product IDE extension set (Docker / Helm / Python / Ruff / Pylint / Mypy / PlantUML / Prettier / markdownlint /
signageos SOPS, Kubernetes Tools, and related helpers used across the three product repos) and postCreate MUST attempt
soft-fail install of that same set via remote CLI when available. The list MUST include at least: `charliermarsh.ruff`,
`jebbs.plantuml`, `signageos.signageos-vscode-sops` (Open VSX / Cursor-supported SOPS editor; MUST NOT require
`shipitsmarter.sops-edit` in the shared recommendation list), `esbenp.prettier-vscode`,
`davidanson.vscode-markdownlint`, and `ms-kubernetes-tools.vscode-kubernetes-tools`.

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
- **THEN** those public keys are imported with `gpg` for SOPS encrypt / recipient checks

#### Scenario: Kubernetes Tools is on the shared extension list

- **WHEN** a contributor inspects `.devcontainer/devcontainer.json` extensions and the postCreate extension array
- **THEN** both include `ms-kubernetes-tools.vscode-kubernetes-tools`

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

### Requirement: Bashrc-free PATH for venv and scripts/bin

This repository’s Dev Container `remoteEnv` MUST prepend `/workspace/.venv/bin` and `/workspace/scripts/bin` on `PATH`
(scripts/bin before or after `.venv/bin` is allowed as long as both appear before the inherited container `PATH`). The
PATH value MUST use the fleet in-container workspace path `/workspace` literally — not `${workspaceFolder}` — so Cursor
agent shells (which do not expand that variable) still resolve `scripts/bin` wrappers. `remoteEnv` MUST also set
`VIRTUAL_ENV` to `/workspace/.venv` so IDE and agent shells treat the project venv as active without sourcing `activate`
or patching `~/.bashrc`. Shared postCreate and personal-token helpers MUST NOT patch `~/.bashrc` (or other user shell
profiles) to inject that PATH/VIRTUAL_ENV or to source a load-env script. Documentation MUST state that the
**verbatim-synced** `devcontainer.json` carries this `remoteEnv` contract so every integrated terminal and remote
process sees uv tool binaries and `scripts/bin` wrappers without home-profile mutation.

#### Scenario: Devinfra remoteEnv includes venv and scripts/bin

- **WHEN** a contributor inspects this repository’s `.devcontainer/devcontainer.json` `remoteEnv`
- **THEN** both `/workspace/.venv/bin` and `/workspace/scripts/bin` appear on `PATH`
- **AND** `VIRTUAL_ENV` is `/workspace/.venv`
- **AND** the PATH value does not rely on `${workspaceFolder}` expansion
- **AND** postCreate does not append a `source …/load-env.sh` (or equivalent) line to `~/.bashrc`

#### Scenario: Docs require the same PATH contract for products

- **WHEN** a contributor reads Dev Container adoption docs for product sync
- **THEN** they learn synced `devcontainer.json` MUST set the same `remoteEnv.PATH` prepend for `.venv/bin` and
  `scripts/bin` under `/workspace` and MUST set `VIRTUAL_ENV` to `/workspace/.venv`
- **AND** they learn the fleet MUST NOT rely on patching `~/.bashrc` for that PATH or venv activation

### Requirement: Prompt shows host folder basename

The shared `devcontainer.json` MUST set `remoteEnv.DEVCONTAINER_REPO_NAME` to `${localWorkspaceFolderBasename}` and MUST
point `STARSHIP_CONFIG` at a synced Starship config under `.devcontainer/` that displays that variable as the leading
prompt identity. Documentation MUST state that the cwd basename under `/workspace` is not used as the repo name in the
prompt.

#### Scenario: remoteEnv carries repo basename for Starship

- **WHEN** a contributor inspects `.devcontainer/devcontainer.json` `remoteEnv`
- **THEN** `DEVCONTAINER_REPO_NAME` is `${localWorkspaceFolderBasename}`
- **AND** `STARSHIP_CONFIG` references the synced `.devcontainer/starship.toml`
- **AND** that Starship config is on the product sync allowlist

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
remove LFS hooks or foreign `pre-push.d` fragments; shared postCreate MUST NOT hard-code product LFS script names;
products MUST use `scripts/devcontainer-post-create.d/` drop-ins for optional postCreate work (including LFS setup);
docs MUST NOT recommend editing synced JSON `postCreate` for LFS. Docs MUST NOT describe a standing “thin
`devcontainer.json` overlay” adopt pattern. Docs MUST state the bashrc-free shell contract: synced `devcontainer.json`
MUST set `remoteEnv.PATH` to prepend `.venv/bin` and `scripts/bin`; fleet shell init MUST NOT patch `~/.bashrc` for
PATH, aliases, tokens, completions, or sourcing `load-env.sh`; kubectl/docker short-name bash completion is provided by
the shared image; optional `.env.integration.enc` decrypt runs in shared postCreate and does not auto-export into every
shell; product-local `load-env.sh` / bashrc wiring is deprecated in favor of this contract (product migration tracked in
follow-up issues).

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
- **AND** they learn Git LFS is product-owned; restore after create uses `scripts/devcontainer-post-create.d/` (not
  synced JSON `postCreate` edits and not hard-coded shared callbacks to LFS script names)
- **AND** they learn synced `remoteEnv.PATH` prepends `.venv/bin` and `scripts/bin` without patching `~/.bashrc`
- **AND** they learn `k`/`d` bash completion comes from the shared image completion files
- **AND** they learn product `load-env.sh` / bashrc sourcing is not the shared pattern after sync adopt

### Requirement: Verbatim shared devcontainer.json and compose

The repository MUST provide a fleet-generic `.devcontainer/devcontainer.json` that products adopt verbatim via sync. It
MUST set `workspaceFolder` to `/workspace`, MUST set `name` to `${localWorkspaceFolderBasename}` (or equivalent
substitution that yields a distinct window title per opened folder), and MUST derive additional named volume `source=`
values from `${localWorkspaceFolderBasename}` (e.g. bashhistory and gh-config volumes). It MUST prepend
`/workspace/.venv/bin` and `/workspace/scripts/bin` on `remoteEnv.PATH` (literal `/workspace`, not
`${workspaceFolder}`), MUST set `VIRTUAL_ENV` to `/workspace/.venv`, MUST set `DEVCONTAINER_REPO_NAME` to
`${localWorkspaceFolderBasename}`, and MUST point `STARSHIP_CONFIG` at a synced `.devcontainer/starship.toml`. It MUST
NOT embed product-only `remoteEnv` keys such as product `MYPYPATH` or `CST_*`, and MUST NOT require product-specific
`postStartCommand` for the shared happy path. The repository MUST provide a matching fleet-generic
`.devcontainer/docker-compose.yml` that binds `..:/workspace` for the devcontainer service and MUST list the shared Dev
Container entry files (including `starship.toml`) on the product sync allowlist (MUST NOT list them under sync `exclude`
as standing product-owned overlays). Shared Compose MAY reference an optional `.devcontainer/product.env` with soft-fail
/ `required: false` semantics so absence does not break Dev Container start.

#### Scenario: Shared JSON is path-generic

- **WHEN** a contributor inspects `.devcontainer/devcontainer.json` in this repository
- **THEN** `workspaceFolder` is `/workspace`
- **AND** `name` uses `${localWorkspaceFolderBasename}` (or equivalent)
- **AND** named volume sources use `${localWorkspaceFolderBasename}`-based names
- **AND** `remoteEnv.PATH` includes `.venv/bin` and `scripts/bin`
- **AND** `remoteEnv.VIRTUAL_ENV` is `/workspace/.venv`
- **AND** `remoteEnv.DEVCONTAINER_REPO_NAME` uses `${localWorkspaceFolderBasename}`
- **AND** the file does not hardcode another product’s workspace path or volume prefix

#### Scenario: Shared Compose matches /workspace

- **WHEN** a contributor inspects `.devcontainer/docker-compose.yml` in this repository
- **THEN** the devcontainer service binds the repo at `/workspace`
- **AND** build-args continue to come from `versions.env` via the documented `.env` symlink pattern

#### Scenario: Sync allowlists both entry files

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.devcontainer/devcontainer.json`, `.devcontainer/docker-compose.yml`, and `.devcontainer/starship.toml` are
  allowlisted for verbatim sync
- **AND** none of those paths are standing sync excludes

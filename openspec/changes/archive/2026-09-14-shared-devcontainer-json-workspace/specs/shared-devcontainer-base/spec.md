## MODIFIED Requirements

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

### Requirement: Consumer overlay documentation

Documentation (`docs/devcontainer.md`, `docs/sync.md`, and/or README) MUST state that `.devcontainer/devcontainer.json`
and `.devcontainer/docker-compose.yml` are **verbatim** sync blobs (on the sync allowlist): products MUST adopt them
without post-sync hand-edits. The shared JSON MUST use `workspaceFolder` `/workspace`, window `name` from
`${localWorkspaceFolderBasename}`, and named volume `source=` values derived from `${localWorkspaceFolderBasename}` so
repos do not need product-specific JSON keys for those concerns. The shared Compose MUST use the matching
`..:/workspace` bind. Repo-specific container environment (e.g. `MYPYPATH`, `CST_BAKE_TARGET`) MUST NOT be edited into
synced JSON or Compose; documentation MUST point to an optional product-owned `.devcontainer/product.env` (not synced;
referenced from shared Compose when present) and/or process env / reusable CI inputs. Shared fragments MUST NOT hardcode
another product’s host folder name as `workspaceFolder` or as a fixed volume source prefix. Docs MUST state that product
**ciphertext** and recipient config (`.sops.yaml`, encrypted secret files) and `public_gpg_keys` **content** stay in
each product repo, while the shared image provides sops/age/gpg/JRE/graphviz and postCreate performs key import when
keys are present. Docs MUST state that **Git LFS** is not part of the shared image; products that need LFS (e.g.
sql-to-arc) MUST install it in a product-owned path that sync of the shared Dockerfile does not overwrite (e.g. product
postCreate snippet or a non-synced local fragment). Docs MUST NOT describe a standing “thin `devcontainer.json` overlay”
adopt pattern.

#### Scenario: Contributor reads overlay guidance

- **WHEN** a contributor opens the Dev Container docs for product adoption
- **THEN** they learn `devcontainer.json` and `docker-compose.yml` are adopted verbatim from Devinfra sync
- **AND** they learn the in-container workspace path is `/workspace` for all middleware repos
- **AND** they learn window title and history/gh volume names come from `${localWorkspaceFolderBasename}`
- **AND** they learn product-only env belongs in optional `.devcontainer/product.env` and/or CI/hook env — not in synced
  JSON/Compose
- **AND** they learn secret file **content** stays product-local while tooling and key-import behavior are shared
- **AND** they learn Prettier + markdownlint-cli2 (and their extensions) are the shared markdown format/lint stack that
  replaces or supplements prior product-local markdown tooling on sync
- **AND** they learn Git LFS is product-local when needed, not a shared base requirement

## ADDED Requirements

### Requirement: Verbatim shared devcontainer.json and compose

The repository MUST provide a fleet-generic `.devcontainer/devcontainer.json` that products adopt verbatim via sync. It
MUST set `workspaceFolder` to `/workspace`, MUST set `name` to `${localWorkspaceFolderBasename}` (or equivalent
substitution that yields a distinct window title per opened folder), and MUST derive additional named volume `source=`
values from `${localWorkspaceFolderBasename}` (e.g. bashhistory and gh-config volumes). It MUST NOT embed product-only
`remoteEnv` keys such as product `MYPYPATH` or `CST_*`, and MUST NOT require product-specific `postStartCommand` for the
shared happy path. The repository MUST provide a matching fleet-generic `.devcontainer/docker-compose.yml` that binds
`..:/workspace` for the devcontainer service and MUST list both files on the product sync allowlist (MUST NOT list them
under sync `exclude` as standing product-owned overlays). Shared Compose MAY reference an optional
`.devcontainer/product.env` with soft-fail / `required: false` semantics so absence does not break Dev Container start.

#### Scenario: Shared JSON is path-generic

- **WHEN** a contributor inspects `.devcontainer/devcontainer.json` in this repository
- **THEN** `workspaceFolder` is `/workspace`
- **AND** `name` uses `${localWorkspaceFolderBasename}` (or equivalent)
- **AND** named volume sources use `${localWorkspaceFolderBasename}`-based names
- **AND** the file does not hardcode another product’s workspace path or volume prefix

#### Scenario: Shared Compose matches /workspace

- **WHEN** a contributor inspects `.devcontainer/docker-compose.yml` in this repository
- **THEN** the devcontainer service binds the repo at `/workspace`
- **AND** build-args continue to come from `versions.env` via the documented `.env` symlink pattern

#### Scenario: Sync allowlists both entry files

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.devcontainer/devcontainer.json` and `.devcontainer/docker-compose.yml` are allowlisted for verbatim sync
- **AND** they are not listed as standing sync excludes for product ownership

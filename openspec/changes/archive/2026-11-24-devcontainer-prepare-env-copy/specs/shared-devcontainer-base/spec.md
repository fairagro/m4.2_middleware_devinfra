## MODIFIED Requirements

### Requirement: Shared Dev Container image and versions.env

The repository MUST provide `.devcontainer/Dockerfile` and repo-root `versions.env` (consumed via Compose build-args /
`.devcontainer/.env` as a **generated copy** of `versions.env`) that define the **shared product Dev Container
toolchain** used by the three m4.2 product repos: base image pin, Python/uv, Node/OpenSpec, GitHub CLI prerequisites,
**jq**, **yq**, **xq**, hadolint, **actionlint**, **kubeconform**, Starship, container-structure-test, yamlfmt, kubectl,
Helm, Minikube, **SOPS**, **age**, **gnupg** (gpg on `PATH`), **default-jre-headless** (or equivalent JRE),
**graphviz**, **Trivy**, and the **Renovate** CLI, plus **Prettier** and **markdownlint-cli2** (global CLI pins in
`versions.env`). The shared image MUST NOT require difftastic and MUST NOT require **Git LFS** (`git-lfs` MUST NOT be a
required shared apt/package install; MUST NOT run `git lfs install --system` as part of the shared image build). Exact
tool versions MUST live only in `versions.env` (one pin source), except distro packages (e.g. `jq`, `gnupg`, JRE,
graphviz) installed from the base image’s package manager without a separate `versions.env` pin. **yq** (mikefarah),
**xq** (XML query CLI), and **Trivy** MUST be pinned in `versions.env` and installed as release binaries on `PATH`.
**Renovate** MUST be pinned in `versions.env` and installed as a global npm CLI (same pattern as OpenSpec / Prettier).
Prettier / markdownlint-cli2 and their IDE extensions (`esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`) are
part of the **shared** toolchain: when synced into product repos they MUST **replace or supplement** each product’s
prior markdown format/lint feature so consumers converge on one stack. Shipping the Renovate CLI in the image MUST be
documented together with the shared Renovate config and per-repo workflow (`shared-renovate` capability). Shipping Trivy
in the image does **not** by itself require shipping a reusable Trivy GitHub Actions workflow (that remains a separate
CI concern). The shared `.devcontainer/docker-compose.yml` MUST bind the repo at `..:/workspace:cached` (or equivalent
consistency flag) so the Compose workspace path matches the shared `devcontainer.json` `workspaceFolder`. The repository
MUST NOT track `.devcontainer/.env` as a git symlink (or other committed pin duplicate); `versions.env` remains the only
committed pin file for those values.

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

### Requirement: Verbatim shared devcontainer.json and compose

The repository MUST provide a fleet-generic `.devcontainer/devcontainer.json` that products adopt verbatim via sync. It
MUST set `workspaceFolder` to `/workspace`, MUST set `name` to `${localWorkspaceFolderBasename}` (or equivalent
substitution that yields a distinct window title per opened folder), and MUST derive additional named volume `source=`
values from `${localWorkspaceFolderBasename}` (e.g. bashhistory and gh-config volumes). It MUST prepend
`/workspace/.venv/bin` and `/workspace/scripts/bin` on `remoteEnv.PATH` (literal `/workspace`, not
`${workspaceFolder}`), MUST set `VIRTUAL_ENV` to `/workspace/.venv`, MUST set `DEVCONTAINER_REPO_NAME` to
`${localWorkspaceFolderBasename}`, and MUST point `STARSHIP_CONFIG` at a synced `.devcontainer/starship.toml`. It MUST
NOT embed product-only `remoteEnv` keys such as product `MYPYPATH` or `CST_*`, and MUST NOT require product-specific
`postStartCommand` for the shared happy path. It MUST set `initializeCommand` to run a shared host script that removes
any existing `.devcontainer/.env` (including a symlink) and copies repo-root `versions.env` to `.devcontainer/.env`
before Compose parses build-args — so checkouts with `core.symlinks=false` still get pin substitution. The repository
MUST provide that script under `scripts/` and list it on the product sync allowlist with the other Dev Container entry
files. The repository MUST provide a matching fleet-generic `.devcontainer/docker-compose.yml` that binds
`..:/workspace` for the devcontainer service and MUST list the shared Dev Container entry files (including
`starship.toml` and the prepare-env script) on the product sync allowlist (MUST NOT list them under sync `exclude` as
standing product-owned overlays). Shared Compose MAY reference an optional `.devcontainer/product.env` with soft-fail /
`required: false` semantics so absence does not break Dev Container start. Root `.gitignore` MUST ignore the generated
`.devcontainer/.env` (no `!.devcontainer/.env` force-add exception).

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
- **AND** build-args come from `versions.env` via a generated `.devcontainer/.env` copy (not a tracked symlink)

#### Scenario: Host prepare copies versions.env before Compose

- **WHEN** a contributor opens the folder in Dev Containers (or runs the shared prepare script on the host)
- **THEN** `.devcontainer/.env` is a regular file whose contents match repo-root `versions.env`
- **AND** an existing symlink or stale `.devcontainer/.env` is removed before the copy
- **AND** `devcontainer.json` `initializeCommand` invokes that shared script

#### Scenario: Sync allowlists both entry files

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.devcontainer/devcontainer.json`, `.devcontainer/docker-compose.yml`, and `.devcontainer/starship.toml` are
  allowlisted for verbatim sync
- **AND** the prepare-env script is allowlisted with other python-product Dev Container scripts
- **AND** none of those paths are standing sync excludes

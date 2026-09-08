# shared-devcontainer-base Delta

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

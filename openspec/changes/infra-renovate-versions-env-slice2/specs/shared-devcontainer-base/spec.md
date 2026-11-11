# Spec Delta

## MODIFIED Requirements

### Requirement: Product Dev Container vs Infra GitOps image ownership

Documentation for the shared Dev Container (`docs/devcontainer.md` and cross-links from `docs/sync.md`) MUST state that
`.devcontainer/Dockerfile`, `devcontainer.json`, `docker-compose.yml`, `starship.toml`, and the composed product pin
files describe the **python-product** toolchain synced to api / sql_to_arc / harvester. They MUST state that
`m4.2_infrastructure` keeps owning its fat GitOps Dev Container (argocd / kind / chart-testing / related tools) until a
dedicated adoption issue explicitly moves Infra onto a shared Devinfra target or overlay. Docs MUST publish
pin-ownership buckets and the **two-file pin split**:

- **Shared / foundation-eligible** (file `versions.foundation.env`): Helm, minikube (current product local-cluster
  tool), git-lfs (shared-eligible; the existing shared-image rule that git-lfs is not a _required_ install on the
  product happy path remains until a separate change installs it), plus other shared CLIs in that file
- **python-product** (file `versions.env`): Python/uv, CST, Trivy, Renovate CLI, git-cliff, product-app image pins, Dev
  Container base image, and other product-only quality toolchain pins
- **Infra-owned until adoption:** argocd, kind, chart-testing (`ct`)

Docs MUST name the deferred product **minikube → kind** swap as a separate follow-up (not implied by this ownership
doc). This requirement MUST NOT by itself change the installed product image tool set. Docs MUST state Infra receives
`versions.foundation.env` via foundation sync without receiving product `.devcontainer/**` or `versions.env`.

#### Scenario: Docs separate product image from Infra GitOps image

- **WHEN** a contributor reads Dev Container or sync docs about Infra adoption
- **THEN** they learn product `.devcontainer/*` is python-product sync only
- **AND** they learn Infra keeps its fat GitOps image until an adoption issue says otherwise
- **AND** they find the shared / python-product / Infra-owned pin buckets and the two pin files
- **AND** they learn minikube→kind for products is a separate follow-up

### Requirement: Shared Dev Container image and versions.env

The repository MUST provide `.devcontainer/Dockerfile` and repo-root pin files that define the **shared product Dev
Container toolchain** used by the three m4.2 product repos: base image pin, Python/uv, Node/OpenSpec, GitHub CLI
prerequisites, **jq**, **yq**, **xq**, hadolint, Starship, container-structure-test, yamlfmt, kubectl, Helm, Minikube,
**SOPS**, **age**, **gnupg** (gpg on `PATH`), **default-jre-headless** (or equivalent JRE), **graphviz**, **Trivy**, and
the **Renovate** CLI, plus **Prettier** and **markdownlint-cli2**. Exact tool versions MUST live only in the composed
pin SoT — `versions.foundation.env` (foundation-eligible) plus `versions.env` (python-product) — with no intentional
duplicate keys across those files, except distro packages (e.g. `jq`, `gnupg`, JRE, graphviz) installed from the base
image’s package manager without a separate pin. Compose build-args / env loading MUST consume **both** pin files (via
dual `env_file` and/or an equivalent documented load path). `scripts/load-versions-env.sh` MUST source the foundation
file then `versions.env` and fail closed if either required file is missing on a product checkout. The shared image MUST
NOT require difftastic and MUST NOT require **Git LFS** (`git-lfs` MUST NOT be a required shared apt/package install;
MUST NOT run `git lfs install --system` as part of the shared image build). **yq** (mikefarah), **xq** (XML query CLI),
and **Trivy** MUST be pinned in the composed SoT and installed as release binaries on `PATH`. **Renovate** MUST be
pinned in `versions.env` and installed as a global npm CLI (same pattern as OpenSpec / Prettier). Prettier /
markdownlint-cli2 and their IDE extensions (`esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`) are part of the
**shared** toolchain: when synced into product repos they MUST **replace or supplement** each product’s prior markdown
format/lint feature so consumers converge on one stack. Shipping the Renovate CLI in the image MUST be documented
together with the shared Renovate config and per-repo workflow (`shared-renovate` capability). Shipping Trivy in the
image does **not** by itself require shipping a reusable Trivy GitHub Actions workflow (that remains a separate CI
concern). The shared `.devcontainer/docker-compose.yml` MUST bind the repo at `..:/workspace:cached` (or equivalent
consistency flag) so the Compose workspace path matches the shared `devcontainer.json` `workspaceFolder`.

#### Scenario: Rebuild uses pinned shared toolchain

- **WHEN** a contributor rebuilds the Dev Container from this repo’s compose/Dockerfile
- **THEN** the image builds with toolchain versions from the composed pin files
- **AND** the shared product tools listed above are available in the container on the documented happy path
- **AND** `jq`, `yq`, and `xq` are on `PATH`
- **AND** `prettier` and `markdownlint-cli2` are on `PATH` from the shared image pins
- **AND** `trivy` and `renovate` are on `PATH`
- **AND** `sops`, `age`, `gpg`, and a JRE/`java` plus `dot` (graphviz) are available on the documented happy path
- **AND** difftastic is not part of the required shared toolchain
- **AND** `git-lfs` is not required on the shared image happy path
- **AND** the Compose service binds the repository at `/workspace` in the container

#### Scenario: Load fails closed without both pin files

- **WHEN** `scripts/load-versions-env.sh` runs on a product checkout missing `versions.foundation.env` or `versions.env`
- **THEN** it fails with an error naming the missing file

#### Scenario: Dev Container docs link Renovate CLI to shared automation

- **WHEN** a contributor reads Dev Container docs for Trivy / Renovate local CLIs
- **THEN** they learn `renovate` on `PATH` is for local dry-runs against the shared Renovate config
- **AND** they are pointed at the shared Renovate workflow/docs (not only “workflow deferred to open issues”)

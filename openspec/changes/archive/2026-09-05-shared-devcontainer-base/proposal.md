# Proposal: shared-devcontainer-base

## Why

Issue #10 (unblocked by #9): product repos still own nearly identical fat Dev Container Dockerfiles while this repo only
has a lean “step 0” bootstrap. Epic #1 needs one shared base image/`versions.env` here, with products keeping only thin
`devcontainer.json` overlays, and postCreate wiring commit-stage pre-commit plus Git LFS/pre-push hooks.

## What Changes

- Expand `.devcontainer/Dockerfile` + `versions.env` (+ compose build-args) to the **shared product toolchain** common
  across API / sql_to_arc / harvester: CST, yamlfmt, kubectl/helm/minikube, **jq + yq + xq**, **sops + age +
  gnupg/gpg**, **default JRE + graphviz** (PlantUML), **Trivy**, **Renovate** CLI, plus related pins. Include
  **Prettier** + **markdownlint-cli2** (global in the image, pins in `versions.env`) and the **esbenp.prettier-vscode**
  / **davidanson.vscode-markdownlint** extensions so that on product sync (#13) this stack **replaces or supplements**
  whatever markdown format/lint setup products use today. **Do not** carry **difftastic** (unused beyond Dockerfile
  install today). SOPS/age/gpg support **encrypted** repo secrets — not plaintext secrets in git. Trivy/Renovate in the
  image are for **local** scans / config dry-runs; reusable GitHub Actions wiring remains #11/#12.
- Include **Ruff**, **PlantUML** (`jebbs.plantuml`), and the Cursor-supported **SOPS** extension
  (`signageos.signageos-vscode-sops` on Open VSX — not `shipitsmarter.sops-edit`) in shared `devcontainer.json`;
  postCreate MAY soft-fail-install Ruff (and MAY install the others the same way) via remote CLI. Ruff CLI via `uv sync`
  / pre-commit.
- Shared postCreate MUST import `public_gpg_keys/*.asc` when that directory has keys (skip cleanly if absent) — same
  pattern as products. Product **ciphertext** (`.sops.yaml` recipients, `*.enc` / `secrets.enc.yaml` / `client.key`)
  remains **per product repo** (cannot be one shared secret blob); shared docs describe the layout.
- Extend `scripts/devcontainer-post-create.sh` (generic): perms → `load-versions-env` → `uv sync` → `pre-commit install`
  → `setup-git-lfs.sh` → optional public GPG import → optional IDE extension installs (no hardcoded product workspace
  names).
- Document consumer overlays: `name`, `workspaceFolder`, volume `source=` names; shared Dockerfile/compose/
  `versions.env`/scripts sync later (#13). Compose workspace bind paths stay product-local.
- Align Node pin with current Devinfra (v22). Pre-commit for hooks from the **uv project**.
- Update README / `docs/devcontainer.md` / quality docs so “until #10” language is removed.

## Capabilities

### New Capabilities

- `shared-devcontainer-base`: Canonical Dev Container image, `versions.env` pins, generic postCreate, and consumer
  overlay documentation so products only keep thin `devcontainer.json` overlays.

### Modified Capabilities

- `shared-quality-tooling`: Install boundary — commit-stage `pre-commit install` is performed by shared postCreate (no
  longer deferred to an unimplemented #10).
- `shared-git-hooks-lfs`: Install boundary — postCreate MUST invoke `setup-git-lfs.sh` on the documented Dev Container
  create path.

## Impact

- `.devcontainer/` (Dockerfile, docker-compose.yml, this repo’s `devcontainer.json` name/docs only as needed)
- `versions.env`, `scripts/load-versions-env.sh` (validate any new required pins)
- `scripts/devcontainer-post-create.sh`
- `docs/devcontainer.md`, root `README.md`, possibly `docs/quality.md`
- Specs: new `shared-devcontainer-base`; deltas on quality + git-hooks install wording
- Consumers adopt via sync (#13); this change does not open product PRs

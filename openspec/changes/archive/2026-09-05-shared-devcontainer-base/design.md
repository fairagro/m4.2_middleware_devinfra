# Design: shared-devcontainer-base

## Context

See proposal.md — Why. Bootstrap already has lean `.devcontainer/`, `versions.env`, `load-versions-env.sh`, and a
generic postCreate without quality/LFS installs. All three product repos share nearly the same fat Dockerfile tool set;
Devinfra docs still say “until #10” for hook wiring. Path conventions forbid hardcoding another product’s
`workspaceFolder` / volume names in shared fragments. Surface quality bar: Linux Dev Container happy path only.

## Goals / Non-Goals

**Goals:**

- One shared image + `versions.env` covering the common product toolchain (option A), minus unused difftastic, including
  **jq, yq, xq**, **sops, age, gnupg/gpg**, **default-jre-headless + graphviz** (for PlantUML), k8s/helm/minikube, CST,
  yamlfmt, **Trivy**, **Renovate** CLI, and **Prettier + markdownlint-cli2** (shared markdown format/lint —
  replaces/supplements product setups on sync).
- Generic postCreate: perms → load-versions → `uv sync` → commit-stage `pre-commit install` → `setup-git-lfs.sh` →
  import `public_gpg_keys/*.asc` when present → Ruff (and related) extension soft-fail installs.
- Shared IDE extensions: Ruff, PlantUML (`jebbs.plantuml`), SOPS (`signageos.signageos-vscode-sops` — Open VSX / Cursor;
  not shipitsmarter), Prettier (`esbenp.prettier-vscode`), markdownlint (`davidanson.vscode-markdownlint`).
- Clear overlay docs for thin product `devcontainer.json` (`name`, `workspaceFolder`, volume sources).
- Align Node to Devinfra’s current v22 pin.

**Non-Goals:**

- Syncing into product repos (#13).
- Shipping **difftastic**.
- Copying product **ciphertext** or recipient lists into this Devinfra repo (each product keeps its own `.sops.yaml` /
  `*.enc` / `secrets.enc.yaml` / `client.key` / `public_gpg_keys` **content**).
- Reusable CI workflow **definitions** (#11/#12) — Trivy/Renovate **CLIs in the image** are in scope; GHA reusable
  workflows are not.
- Host Homebrew/apt auto-install, worktree exotic layouts, dual token stores.
- Shipping a separate image-global `pre-commit` or `ruff` binary as the primary runner (uv project path is enough).

## Decisions

### 1. Lift shared product tools into Devinfra Dockerfile

- **Choice:** Port common install blocks (kubectl, Helm, Minikube, SOPS, age, yamlfmt, container-structure-test, **yq**)
  plus **`jq`** (apt), **`xq`** (pinned release binary), **`gnupg`**, **`default-jre-headless`**, **`graphviz`**,
  **Trivy** (pinned release binary), **Renovate** (pinned global npm CLI alongside OpenSpec/Prettier), matching
  `versions.env` / compose build-args. Keep **Prettier** / **markdownlint-cli2** as **shared** product tooling — on sync
  (#13) they replace or supplement each product’s prior markdown format/lint feature. Starship/history stay. **Omit
  difftastic**.
- **Alternatives:** Lean image (rejected); omit JRE/graphviz/PlantUML stack (rejected — user lock-in); keep difftastic
  (rejected — unused); rely on yq alone for XML (rejected — user requires `xq` on PATH); defer Trivy/Renovate to CI-only
  (#11) without local CLIs (rejected — user wants them in the Dev Container).
- **Why:** Matches epic done-when and product local-dev (diagrams + encrypted secrets + query CLIs + local security /
  dependency tooling).

### 2. Compose bind path stays product-local

- **Choice:** This repo’s compose uses this repo’s workspace path. Overlay docs tell products to replace bind /
  `workspaceFolder` / volume `source=` names. Do not encode other products’ folder names in shared sources.
- **Alternatives:** Parameterized compose — defer to #13 if needed.

### 3. pre-commit via uv project, not image pin as happy path

- **Choice:** After `uv sync`, `pre-commit install --hook-type pre-commit` from the project env. Optional
  `PRECOMMIT_VERSION` pin only for parity docs — not a second primary installer.
- **Alternatives:** Image-global pre-commit from `PRECOMMIT_VERSION` — skip as primary.

### 4. Node 22

- **Choice:** Keep Devinfra `NODE_VERSION=v22.x` as the shared pin.
- **Alternatives:** API’s v20 — rejected.

### 5. load-versions-env validation

- **Choice:** Do not force every image pin through `load-versions-env.sh`; keep current PYTHON/UV/NODE/OpenSpec/
  Prettier/markdownlint checks unless a script reads more. Distro packages (`jq`, gnupg, JRE, graphviz) need no
  `versions.env` pin; **yq** and **xq** use `versions.env` pins like other release binaries.

### 6. IDE extensions: shared product union + Devinfra extras

- **Choice:** `devcontainer.json` and postCreate share one extension list: union of the three product repos’ common
  needs (Docker/Helm/Python/Ruff/Pylint/Mypy/PlantUML/Jinja/git helpers, …) plus Devinfra Prettier/hadolint/Actions.
  SOPS: `signageos.signageos-vscode-sops` only. Omit `shipitsmarter.sops-edit` and `ms-python.autopep8` (Ruff).
- **Why:** postCreate must install what product contributors expect, not only the five “new” extensions.

### 7. SOPS tooling + public key import in shared postCreate; ciphertext stays per repo

- **Choice:** Image has sops/age/gpg. postCreate imports `public_gpg_keys/*.asc` when files exist (no-op / skip message
  if missing — works for Devinfra without keys). Do **not** invent shared enc files or a shared recipient `.sops.yaml`
  for all products; each product keeps its secret **content**. Docs describe the expected layout.
- **Why:** User asked to include import + SOPS editor/PlantUML/JRE stack; secret blobs cannot be unified across three
  products.

### 8. Trivy + Renovate CLIs in the image (local); GHA stays later

- **Choice:** Pin `TRIVY_VERSION` (release binary on `PATH`) and `RENOVATE_VERSION` (global npm install with Node, same
  pattern as OpenSpec/Prettier). Document local use (fs/image scans, `renovate` config validation / dry-run). Do **not**
  implement reusable `renovate.yml` / trivy-action workflows in this change (#11/#12).
- **Why:** User lock-in; products already use both in CI and need the same CLIs in the Dev Container.

## Risks / Trade-offs

- **[Risk] Larger image (JRE/graphviz + k8s tools)** → Mitigation: accepted; still drop unused difftastic.
- **[Risk] Two SOPS extensions** → Mitigation: shared list uses only `signageos.signageos-vscode-sops`; products on
  shipitsmarter migrate at sync (#13).
- **[Risk] Pin drift vs products until #13** → Mitigation: start from current product pin set; document rebuild.
- **[Risk] postCreate `uv sync` / extension install needs network** → Mitigation: fail clearly on sync; soft-fail
  extensions.
- **[Risk] Hadolint on longer Dockerfile** → Mitigation: existing ignore patterns; run hadolint on edit.

## Migration Plan

1. Land Dockerfile/`versions.env`/postCreate/docs on this branch; rebuild Devinfra container to verify.
2. Consumers adopt via sync PRs (#13): replace fat Dockerfile with shared copy; thin `devcontainer.json` overlays; keep
   product enc / `.sops.yaml` / `public_gpg_keys` content local.
3. Rollback: revert this change; products remain on their current fat images until sync.

## Open Questions

None — lock-ins include JRE/graphviz, PlantUML, public GPG import, signageos SOPS, Prettier/markdownlint as shared
product stack, **Trivy + Renovate CLIs**; ciphertext content remains per product; GHA reusable workflows stay #11/#12.

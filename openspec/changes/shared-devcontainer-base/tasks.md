# Shared Dev Container base — Tasks

## 1. Image and pins

- [ ] 1.1 Expand `versions.env` with shared product toolchain pins (CST, yamlfmt, kubectl, Helm, Minikube, SOPS, age,
      **yq**, **xq**, **Trivy**, **Renovate**; keep Node v22 / Prettier / markdownlint pins; do **not** add
      `DIFFTASTIC_VERSION`; **jq** stays apt)
- [ ] 1.2 Update `.devcontainer/docker-compose.yml` build-args to pass the new pins (including `XQ_VERSION`,
      `YQ_VERSION`, `TRIVY_VERSION`, `RENOVATE_VERSION`)
- [ ] 1.3 Expand `.devcontainer/Dockerfile` with shared install blocks including **jq** (apt), **yq**, **xq**, **sops**,
      **age**, **gnupg**, **default-jre-headless**, **graphviz**, **Trivy**, **Renovate** (npm global); keep
      Prettier/markdownlint globals (exclude difftastic)
- [ ] 1.4 Run hadolint on the Dockerfile and fix actionable findings

## 2. postCreate and version loader

- [ ] 2.1 Extend `scripts/devcontainer-post-create.sh`: after load-versions / token load, `uv sync`, commit-stage
      `pre-commit install`, `./scripts/setup-git-lfs.sh`, import `public_gpg_keys/*.asc` when present, then soft-fail
      IDE extension installs via remote CLI (Ruff / PlantUML / signageos SOPS as listed in `devcontainer.json`)
- [ ] 2.2 Adjust `scripts/load-versions-env.sh` only if new pins must be validated for its current contract (do not
      force every image pin through it)
- [ ] 2.3 Ensure project `pyproject.toml` / lock provides `ruff` for `uv run ruff` after sync (add/adjust dep if
      missing)

## 3. Docs and this-repo overlay

- [ ] 3.1 Update `docs/devcontainer.md`: remove “until #10”; document postCreate (hooks, GPG import, extensions);
      document sops/age/gpg/JRE/graphviz/PlantUML; note Prettier/markdownlint as shared stack; note **Trivy** /
      **Renovate** CLIs for local use (GHA still #11/#12); clarify product-local ciphertext; overlay fields
- [ ] 3.2 Update root `README.md` / `docs/quality.md` install wording to match (postCreate wires commit + LFS hooks)
- [ ] 3.3 Tidy `.devcontainer/devcontainer.json`: drop “step 0” naming; ensure `charliermarsh.ruff`, `jebbs.plantuml`,
      `signageos.signageos-vscode-sops`, `esbenp.prettier-vscode`, `davidanson.vscode-markdownlint`; keep Devinfra-local
      `name` / `workspaceFolder` / volume sources

## 4. Verify

- [ ] 4.1 `bash -n` on touched shell scripts; smoke `source scripts/load-versions-env.sh` in-repo
- [ ] 4.2 Format/lint markdown for touched docs (`npm run format:md` / `lint:md` as needed)

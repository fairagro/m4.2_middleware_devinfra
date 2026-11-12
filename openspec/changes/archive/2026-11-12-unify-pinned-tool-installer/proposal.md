## Why

Five near-duplicate `scripts/install-*.sh` drivers (gitleaks, actionlint, kubeconform, cst, git-cliff) each load
`versions.env`, fail closed without a pin, and download a GitHub release asset. That noise under `scripts/` invites
copy-paste for the next CLI. CI still needs **one install step per tool** — not five full script implementations.

## What Changes

- Add `scripts/install-pinned-tool.sh <tool>` with an in-script bash `case` registry (pin env, URL/asset, arch map,
  extract/install, optional checksum, version-check args)
- **BREAKING** for call sites: delete the five per-tool install scripts (**no permanent shims**); update reusable
  workflows, `devcontainer-post-create.sh`, docs, and sync allowlist to the driver
- Keep contracts: `versions.env` pin SoT; fail closed if pin/file missing; safe under `sudo` (do **not** source
  `load-versions-env.sh`)
- Dev Container Dockerfile stays **inline `curl`/`RUN`** for these CLIs; document that dual path; image-via-driver is
  deferred to [#374](https://github.com/fairagro/m4.2_middleware_devinfra/issues/374)

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-quality-tooling`: single pinned-tool installer contract; gitleaks/actionlint/kubeconform install helpers refer
  to the driver + tool id (CST / git-cliff call sites follow the same driver without new capability names)
- `synced-consumer-paths`: allowlist `scripts/install-pinned-tool.sh`; drop per-tool install script paths

## Impact

- Delete: `scripts/install-{gitleaks,actionlint,kubeconform,cst,git-cliff}.sh`
- Add: `scripts/install-pinned-tool.sh`
- Update: `.github/workflows/reusable-*.yml` call sites, `scripts/devcontainer-post-create.sh`,
  `docs/synced-paths.yaml`, `docs/quality.md`, `docs/ci.md`, sync inventory as needed
- Out of scope: Dockerfile calling the driver (#374); changing pin names or Renovate customManagers

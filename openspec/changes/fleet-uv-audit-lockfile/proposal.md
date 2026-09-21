## Why

Python lockfile / environment CVEs are not covered by Trivy image scans. Products need a primary **`uv.lock` gate** that
runs in quality CI and hooks without an image build
([#174](https://github.com/fairagro/m4.2_middleware_devinfra/issues/174)).

## What Changes

- Adopt **`uv audit`** (A1) as the fleet Python-lock vulnerability gate — not pip-audit / osv-scanner
- Wire **commit-stage hook + reusable code-quality** (B2); fail on any finding (C1) with documented ID ignores
- Enable **`UV_MALWARE_CHECK`** on fleet `uv sync` paths (D2); document as install-time MAL advisory block (not a CVE
  audit substitute)
- Document **layer split** vs Trivy (D1): lock/env = `uv audit`; image/SBOM = Trivy in `reusable-check`
- Named IDE exception for `uv audit` (hooks + CI only; network to OSV)
- **Not** in this change: severity-filtered fail bar (uv has none), pip-audit, osv-scanner, Renovate policy rewrite

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: pre-commit `uv audit`; three-env parity + IDE exception; malware-check on documented sync
  entrypoints; docs vs Trivy
- `reusable-ci-workflows`: code-quality runs `uv audit` after sync; `uv sync` with malware check enabled
- `shared-devcontainer-base`: post-create sync enables malware check
- `synced-consumer-paths`: optional uv-audit ignore overlay on `overlays` (never wiped)

## Impact

- `.pre-commit-config.yaml`, `scripts/run-uv-audit.sh` (optional ignore overlay), `reusable-code-quality.yml`
- `scripts/devcontainer-post-create.sh` and/or `.devcontainer` env
- `docs/quality.md`, `docs/ci.md`, `openspec/principles.global.md` (Code Quality example / note)
- `docs/synced-paths.yaml` if an ignore overlay path is introduced
- Issue [#174](https://github.com/fairagro/m4.2_middleware_devinfra/issues/174)

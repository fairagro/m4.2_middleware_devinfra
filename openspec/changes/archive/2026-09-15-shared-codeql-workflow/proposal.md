## Why

Product repos (API, harvester, sql_to_arc) ship a local `.github/workflows/codeql.yml` that hardcodes Python/uv/Action
pins. Shared Renovate correctly disables `versions.env` in products but still bumps those product-only workflows —
Shadow PRs (e.g. sql_to_arc #136/#137) while fleet SoT stays in Devinfra. CodeQL is not on the sync allowlist and does
not exist in this repo ([#124](https://github.com/fairagro/m4.2_middleware_devinfra/issues/124)).

## What Changes

- Add thin synced `.github/workflows/codeql.yml` in Devinfra (Renovate-like; not `reusable-*.yml`)
- Triggers: **T2a + weekly** — `pull_request` → `main` + schedule `33 5 * * 4`; no `push` on feature/issue/main
- Pins (**P1**): Action refs like other workflows; toolchain from `versions.env` via `load-versions-env.sh`
- Install (**I1**): `uv python install` + `uv sync --dev --all-packages` for the Python matrix job
- Runs in Devinfra too (**D1**)
- Allowlist in `docs/synced-paths.yaml`; document in `docs/ci.md` / `docs/renovate.md`
- Extend product Renovate `matchFileNames` disable with `.github/workflows/codeql.yml`
- **Defer:** product sync adopt and closing product Renovate PRs

## Capabilities

### New Capabilities

- `shared-codeql`: Synced CodeQL analysis workflow contract (triggers, matrix, pins, install bootstrap)

### Modified Capabilities

- `synced-consumer-paths`: Allowlist `.github/workflows/codeql.yml`
- `shared-renovate`: Product Renovate must not bump synced `codeql.yml`

## Impact

- `.github/workflows/codeql.yml` (new)
- `docs/synced-paths.yaml`, `docs/ci.md`, `docs/renovate.md`, `renovate.json`
- OpenSpec specs above
- Products pick up on next sync (#13); until then local CodeQL + shadow pins may remain

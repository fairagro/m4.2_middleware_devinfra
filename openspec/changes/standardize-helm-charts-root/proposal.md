## Why

Fleet chart roots are inconsistent (`helmchart/`, `helm/`, `helmcharts/`). Charter #347 Decision 3 locked a single
canonical root — community/`chart-testing` default **`charts/`**. Devinfra discovery, hooks, IDE associations, docs, and
OpenSpec still encode the dual `helm|helmchart` contract, so consumers cannot converge without a Devinfra SoT change.

## What Changes

- Document and encode **`charts/<chart>/`** (one segment; folder name = Chart.yaml `name`) as the fleet chart root
- Update `scripts/run-helm-lint.sh`, pre-commit `files`/`check-yaml` excludes, `.vscode` Helm associations, and
  quality/CI docs to discover and document `charts/`
- **Transition (lock-in A):** keep temporary dual discovery of legacy `helmchart/` and `helm/` (deprecated in docs); do
  **not** add `helmcharts/` as an alias
- Delta OpenSpec so durable requirements name `charts/` as canonical and describe legacy dual discovery as temporary
- **Out of scope here:** consumer `git mv` (api#653, harvester#591, infra#81); stripping legacy roots (linked follow-up
  after consumer renames + sync); Infra template matrix; Sync profile (#350)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: Helm lint discovery, `check-yaml` Helm template excludes, and quality docs MUST treat
  `charts/` as the canonical chart root; MAY continue recognizing deprecated `helm/` / `helmchart/` during migration
- `shared-devcontainer-base`: synced `.vscode/settings.json` Helm `files.associations` MUST include
  `charts/**/templates` (legacy globs MAY remain during migration)
- `reusable-ci-workflows`: Feature-PR / Helm docs examples and chart-path filter guidance MUST prefer `charts/**` as the
  fleet convention (caller `chart_dir` remains explicit)

## Impact

- Synced into product repos on next Devinfra sync: `run-helm-lint.sh`, `.pre-commit-config.yaml`,
  `.vscode/settings.json`, `docs/quality.md`, `docs/ci.md` (and related allowlisted docs)
- Products still on `helm/` or `helmchart/` keep working until they rename; new `charts/` trees work immediately
- After consumer renames land, a follow-up removes legacy discovery (not this change)

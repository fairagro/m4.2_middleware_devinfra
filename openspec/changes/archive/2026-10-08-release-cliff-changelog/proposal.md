## Why

GitHub Release bodies still append generic `generate_release_notes` (“What’s Changed”) that is weakly structured and
does not match the Conventional Commits grouping already used for `version_bump: auto` (git-cliff). Operators need a
readable cliff changelog on Final Docker/Helm releases while keeping registry/install/license sections. Separately,
editor commit-message guidance should prefer an optional Conventional Commits **scope** (component) so changelogs stay
useful without enforcing a fleet `scope-enum`.

## What Changes

- Add a usable git-cliff changelog `body` template in shared `cliff.toml` (Features / Bug Fixes / Breaking / …) for
  GitHub Release markdown
- Add a thin helper (e.g. `scripts/generate-release-changelog.sh`) that emits cliff markdown for a surface’s R1 tag
  range (`*-docker-v*` / `*-chart-v*`), reusing `GIT_CLIFF_VERSION` / `scripts/install-git-cliff.sh`
- Wire Docker Final (`reusable-release.yml`) and Helm Final (`reusable-helm-release.yml`) to insert a `## Changelog`
  section (plus optional compare “Full Changelog” link); set `generate_release_notes: false`
- Soft-fail when changelog is empty/missing (placeholder text); surface real cliff errors in logs; Release remains
  creatable
- Document in `docs/ci.md`; OpenSpec deltas for release-body + editor guidance
- Update Cursor sparkle (`.cursorrules`) and VS Code Copilot commit-message instructions (and agent/docs mirrors) to
  **prefer** `type(scope): subject` with a short component/scope when one is clear from the diff — without adding
  commitlint `scope-enum` (scope stays optional)

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `reusable-ci-workflows`: Final Docker/Helm GitHub Release bodies include a git-cliff changelog section (R1 ranges);
  disable GitHub auto release notes on those paths
- `shared-quality-tooling`: Editor/agent Conventional Commits guidance prefers an optional component scope

## Impact

- `.github/workflows/reusable-release.yml`, `reusable-helm-release.yml`
- `cliff.toml`, new changelog helper under `scripts/`, `docs/synced-paths.yaml` allowlist
- `docs/ci.md`, `docs/quality.md`
- `.cursorrules`, `.vscode/settings.json`, `.github/copilot-instructions.md`
- OpenSpec main specs for the two capabilities above
- Products receive helper + cliff template + editor guidance on next sync; Release callers see different body shape (no
  GitHub “What’s Changed” dump)

## Why

Three-environment quality parity requires Prettier/markdownlint to gate the same way in IDE, hooks, and GitHub CI. Today
those tools run in IDE/hooks only; `reusable-code-quality.yml` skips them, and docs soften the CI column to
“commit-stage only,” which does not satisfy the parity rule (#40).

## What Changes

- Extend `reusable-code-quality.yml` to run `npm run format:md:check` and `npm run lint:md` with the same shared
  Prettier/markdownlint configs as hooks/IDE (Node setup + `npm ci` in the caller checkout).
- **BREAKING (product callers):** Callers must have synced/root `package.json` + lockfile (and existing markdown
  configs). Missing manifest fails closed — no soft-skip for markdown.
- Allowlist `package.json` and `package-lock.json` for product sync; document the adoption path.
- Update `docs/quality.md` parity table (and related CI/sync notes) so CI is a real markdown gate, not a commit-stage
  substitute.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `reusable-ci-workflows`: reusable code-quality MUST run Prettier/markdownlint check scripts.
- `shared-quality-tooling`: three-environment parity docs/behavior MUST treat markdown as gated in GitHub CI (not
  commit-stage-only).
- `synced-consumer-paths`: allowlist MUST include `package.json` and `package-lock.json` for markdown CI/hooks parity.

## Impact

- `.github/workflows/reusable-code-quality.yml`, `docs/synced-paths.yaml`, `docs/quality.md`, `docs/ci.md` /
  `docs/sync.md` as needed, product sync on next run, OpenSpec deltas above.
- Products without `package.json` will fail code-quality until sync/adopt.

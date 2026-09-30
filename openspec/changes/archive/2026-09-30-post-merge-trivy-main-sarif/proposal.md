## Why

Trivy SARIF from Feature PR / Pre Release is attributed to PR or feature refs, so GitHub Code Scanning alerts on the
**default branch** do not auto-close until a clean SARIF lands on `main`. Operators currently wait for Docker Release
(or similar), which can lag weeks after a Dockerfile pin already fixed the finding. Products need a documented thin
post-merge path that refreshes Default-Branch SARIF without publishing or re-running the full Feature PR bar.

## What Changes

- Document a **thin** recommended product caller: `push` to `main` → `reusable-build` + `reusable-check` only, with
  `security-events: write` so Trivy SARIF uploads against the default branch.
- Keep Feature PR and Release caller guidance unchanged in role: Feature PR stays PR-gated quality/build/check; Release
  keeps its own security gate and does **not** consume prior main-push SARIF.
- Explicit non-goals: path-filters required for v1; removing Trivy from Release; adding `code-quality` or registry
  publish to the post-merge path.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `reusable-ci-workflows`: Require `docs/ci.md` (synced) to document the post-merge main Docker check caller pattern and
  its relationship to Feature PR / Release.

## Impact

- Docs: `docs/ci.md` (and any index links if needed).
- Specs: delta on `reusable-ci-workflows`.
- No new Devinfra reusable workflow required; products adopt the caller snippet. No change to `reusable-check.yml` /
  `reusable-release.yml` behavior in this change.

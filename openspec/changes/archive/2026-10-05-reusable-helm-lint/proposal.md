## Why

Product Feature PRs have no shared Helm chart validation. Charts are packaged only on pre-release/release, and stuffing
chart paths into the Docker `code` detect-changes filter would force build/check without linting. A Devinfra reusable
keeps the fleet pattern consistent while products opt in with their own chart roots.

## What Changes

- Add `.github/workflows/reusable-helm-lint.yml` callable via `workflow_call` with `chart_dir`, boolean `skip`, and an
  optional `helm template` smoke input (default on).
- Pin Helm from the caller checkout’s `versions.env` (`HELM_VERSION`) via the existing load-versions pattern used by
  other Helm reusables.
- Document recommended Feature-PR wiring in `docs/ci.md`: a **separate** chart path filter + `skip` into the new
  reusable — not merging chart paths into the Docker `code` filter.
- Extend `reusable-ci-workflows` requirements for the new reusable and caller guidance.

## Capabilities

### New Capabilities

<!-- none — extend the existing reusable CI capability -->

### Modified Capabilities

- `reusable-ci-workflows`: Require a Helm lint reusable for Feature PRs and document path-gated caller wiring separate
  from Docker build/check.

## Impact

- Devinfra: new workflow YAML, `docs/ci.md`, OpenSpec `reusable-ci-workflows`.
- Products (follow-up, out of this change): extend product-local `detect-changes` and call the reusable (API #206 and
  peers). No product workflow edits in this PR.

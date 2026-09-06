# Proposal: reusable-ci-code-quality-check

## Why

The three m4.2 product repos each carry near-duplicate `reusable-code-quality.yml` and `reusable-check.yml` workflows.
Issue #10 shipped the shared Dev Container toolchain; this change makes the matching **code-quality** and **check**
GitHub Actions workflows the canonical source in Devinfra so products can call them by `uses:` instead of copying YAML.

## What Changes

- Add `.github/workflows/reusable-code-quality.yml` and `reusable-check.yml` adapted from the API product’s current
  patterns (versions.env Python pin, `skip` no-op for required checks).
- Parameterize the Python package root (and related lint/test paths) via `workflow_call` inputs; keep Python version
  from the caller’s `versions.env` (no override input in MVP).
- Parameterize check workflow image base name / components / artifact contract so products are not locked to the API
  image naming.
- Document how product PR workflows call these workflows from a branch or tag of this repo.
- **Out of scope:** `reusable-build.yml` / release workflows (issue “Next” / follow-up CI); product sync PRs that flip
  `uses:` (can be a later PR); Devinfra smoke caller workflow.

## Capabilities

### New Capabilities

- `reusable-ci-workflows`: Shared reusable GitHub Actions for code-quality and container/image check stages, including
  call contract, inputs, and consumer documentation.

### Modified Capabilities

- (none)

## Impact

- New files under `.github/workflows/` and docs (e.g. `docs/ci.md` and/or README pointer).
- Product repos continue to own thin callers (`feature-pull-request.yml`, etc.) until they point `uses:` at this repo;
  artifact naming for check remains coupled to whatever build workflow they run (local or future shared build).
- Trivy / CodeQL action pins follow the adapted API workflows unless a documented bump is needed for Actions
  compatibility.

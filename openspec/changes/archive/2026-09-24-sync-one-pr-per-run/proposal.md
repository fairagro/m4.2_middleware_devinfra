# Proposal: sync-one-pr-per-run

## Why

Product sync currently force-pushes a single rolling branch (`chore/devinfra-sync`) and updates one open PR per
consumer. That makes the review target move under reviewers, hides stacked Devinfra merges in one diff, and diverges
from the archived design (per-SHA branches). Because each sync copies the full allowlist snapshot, a later open sync PR
fully supersedes an earlier one — so we should open a fresh PR per run and close older sync PRs as superseded.

## What Changes

- Stop reusing a fixed sync branch / force-updating one open PR.
- Open **one new sync PR per live sync run** per product repo, on a branch named with the Devinfra source short SHA.
- After the new PR exists, **close** other open sync PRs for that consumer (same bot / sync branch prefix) with a
  **Superseded by #N** comment — do not merge them.
- Document the PR shape and supersede behavior in `docs/sync.md`.
- No auto-merge, merge queue, or `gh stack` in this change.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `product-repo-sync`: Sync MUST open a distinct PR per run (SHA-scoped branch) and MUST supersede older open sync PRs
  instead of force-updating a rolling PR.

## Impact

- `scripts/sync-products.py` (branch naming, push without force-reuse, PR create, list/close supersede)
- `docs/sync.md` (and README link only if needed)
- `openspec/specs/product-repo-sync/spec.md` (via this change’s delta)
- Existing open product PRs on `chore/devinfra-sync` remain until the next live sync closes them as superseded
- Workflow YAML unchanged unless docs-only references need a touch

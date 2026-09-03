# Extract AI review policy and global principles — Proposal

## Why

Wave A needs a single finder/fixer policy and shared engineering foundation so Copilot, Bugbot, and `/review-fixer`
behave the same across the three product repos. Today that content lives only in the API repo (and Principles are
API-shaped); Devinfra has neither, so sync and citations would break if we extract the policy without a shared
`principles.global.md`. Issue #4 (expanded: Copilot entry + global principles).

## What Changes

- Add canonical `docs/ai_review_policy.md` (from the API; strip product-only examples)
- Add shared Finder entries: `.cursor/BUGBOT.md` and `.github/copilot-instructions.md` pointing at that policy
- Add canonical `openspec/principles.global.md` (shared base) and a thin Devinfra `openspec/principles.md` that points
  at it
- Policy and Finder docs cite Supported environment / Type Safety **directly** via `openspec/principles.global.md`
- Update root `README.md`: Docs index + reminder that consumers must not diverge on these synced paths
- Clarify ownership: product OpenSpec **specs/changes** stay local; **principles base** is shared and extendable via
  repo-local `principles.md`

## Capabilities

### New Capabilities

- `ai-review-policy`: Canonical Finder/Fixer policy plus Bugbot and Copilot entry files that load it
- `global-principles`: Shared `openspec/principles.global.md` base and repo-local `openspec/principles.md` extension
  pattern with direct citations to `.global`

### Modified Capabilities

- (none — `path-conventions` unchanged; prior `repo-layout` was archived without a main-spec sync)

## Impact

- Unblocks #5 (`/review-fixer`) and Wave A consumer adoption (#366 / sibling issues)
- Product repos later sync these paths; they keep local `openspec/principles.md` and capability specs
- No sync automation in this change (#13); no review-fixer skill yet (#5)

# Pin vendor skills — Proposal

## Why

Issue #6 needs reproducible vendor agent skills under `.agents/skills/`, with lint excludes and README instructions so
clones and product syncs get the same trees without hand-editing. The set is `gh`, Docker, hadolint, and `uv` (not
GitGuardian `scan-secrets` — secret scanning stays CI/tooling without a pinned agent skill).

## What Changes

- Install and **commit** `.agents/skills/{gh,docker,hadolint,uv}` via `gh skill install` (project scope; Cursor /
  Copilot share `.agents/skills`)
- Remove `.agents/skills/scan-secrets` if previously present
- Document install + `gh skill update` and “do not hand-edit” in the root README
- Keep / confirm shared markdownlint + Prettier ignores for those paths; note pre-commit excludes for when a quality
  skeleton lands (no new pre-commit config in this change)

## Capabilities

### New Capabilities

- `vendor-agent-skills`: Committed vendor skills under `.agents/skills/{gh,docker,hadolint,uv}`, ignores, and README
  reproducibility

### Modified Capabilities

- (none)

## Impact

- New committed trees under `.agents/skills/` (vendor; not hand-edited)
- README + ignore files; consumers sync those paths later

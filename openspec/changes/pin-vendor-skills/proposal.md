# Pin vendor skills — Proposal

## Why

Issue #6 needs reproducible vendor agent skills (`gh` + GitGuardian `scan-secrets`) under `.agents/skills/`, with lint
excludes and README instructions so clones and product syncs get the same trees without hand-editing.

## What Changes

- Install and **commit** `.agents/skills/gh` and `.agents/skills/scan-secrets` via `gh skill install` (project scope;
  Cursor / Copilot share `.agents/skills`)
- Document install + `gh skill update` and “do not hand-edit” in the root README
- Keep / confirm shared markdownlint + Prettier ignores for those paths; note pre-commit excludes for when a quality
  skeleton lands (no new pre-commit config in this change)

## Capabilities

### New Capabilities

- `vendor-agent-skills`: Committed vendor skills under `.agents/skills/{gh,scan-secrets}`, ignores, and README
  reproducibility

### Modified Capabilities

- (none)

## Impact

- New committed trees under `.agents/skills/` (vendor; not hand-edited)
- README + ignore files; consumers sync those paths later
- Does not add `ggshield` runtime install (scan-secrets skill may document that separately)

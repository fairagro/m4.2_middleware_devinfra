## Why

`/code-review` findings published as a wide 5-column Markdown table are unreadable on github.com (Severity/Cost crushed
to ~2 characters). Product PR reviews show the pain
([#217](https://github.com/fairagro/m4.2_middleware_devinfra/issues/217)). Fix upstream in the synced skill + plumbing
contract.

## What Changes

- Lock-in **A2**: human-visible findings as **numbered blocks** (`1. **Title**` + bullets), not `###` sections
- Lock-in **B2**: keep a **compact findings table** in the same body for `/review-fixer` extraction (dual layout)
- Lock-in **C2**: parser keeps accepting **legacy table-only** bodies; dual bodies extract from the table section
- Update skill, `docs/code-review.md`, prompts; OpenSpec deltas for `code-review` + `agent-ai-gh`; tests for dual +
  legacy fixtures
- **Not** in this change: HTML `<table>`, images, or dropping the `path` column / triage fields

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `code-review`: published output shape = numbered blocks + compact path table; marker unchanged
- `agent-ai-gh`: extraction still from Markdown findings table with `path` column (legacy + dual bodies)

## Impact

- `.agents/skills/code-review/SKILL.md`, `docs/code-review.md`, agent prompts if they hard-code the table
- `scripts/ai` tests / fixtures (dual body + legacy table)
- Issue [#217](https://github.com/fairagro/m4.2_middleware_devinfra/issues/217)

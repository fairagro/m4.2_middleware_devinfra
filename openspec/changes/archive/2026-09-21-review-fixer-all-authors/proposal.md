## Why

`/review-fixer` only surfaced unresolved threads from Copilot/Bugbot/Cursor logins. AI-assisted or other reviews under
human logins (e.g. harvester PR #239) produced `open_work_empty` despite open threads. First-party `/code-review`
publishes COMMENT reviews under the human login with findings in the body (often no inline threads) — those must be
triageable too. Keep Copilot summary-only / suppressed packing.

## What Changes

- `review-open` includes **all** unresolved review threads (any first-comment author).
- Finder / summary packing: Copilot/Bugbot/Cursor heuristics **plus** `/code-review` reports (stable HTML comment marker
  - findings-table extract) so human-authored first-party reviews are not skipped.
- Update `review-fixer` / `code-review` skill text; tests for human threads + code-review body findings + suppressed
  Copilot.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-ai-gh`: `review-open` open-work thread filter + code-review summary packing
- `review-fixer`: open-work set includes any-author threads and code-review summary findings
- `code-review`: published report MUST include the stable marker / findings shape review-fixer consumes

## Impact

- `scripts/ai` (`review.py`, tests, README)
- `.agents/skills/review-fixer/SKILL.md`, `.agents/skills/code-review/SKILL.md` (+ thin docs/prompts)

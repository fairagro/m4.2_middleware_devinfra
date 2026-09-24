## Why

`/review-fixer` can resolve `github-code-quality[bot]` review threads after “any author” intake, but that does **not**
dismiss GitHub Code Quality findings. Quality gates can stay blocked while Conversations look clean (#219). The findings
REST API is read-only today — no agent dismiss endpoint — so the MVP must make the gap explicit and enrich open work
with finding state (lock-in **B**).

## What Changes

- Document in `docs/review-fixer.md` and the review-fixer skill: thread resolve ≠ Code Quality **Dismiss finding**;
  Phase 1 MUST call out manual dismiss when Code Quality findings remain `open`.
- Extend `m42-ai review-open` to fetch `GET …/code-quality/findings` (when available) and attach correlatable finding
  `number` / `state` (and rule id when present) onto unresolved threads from `github-code-quality` (soft-fail if the API
  is missing or correlation fails).
- **Not** in this change: a `code-quality-dismiss` write CLI (no documented dismiss API yet).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `agent-ai-gh`: `review-open` MUST optionally enrich Code Quality bot threads with linked finding metadata from the
  read-only findings API.
- `review-fixer`: skill/docs MUST treat Code Quality thread resolve as distinct from finding dismiss and MUST NOT claim
  open work / Remaining risk is clear while linked findings stay `open`.

## Impact

- `scripts/ai` (`review-open` shaping + tests/fixtures), `.agents/skills/review-fixer/SKILL.md`, `docs/review-fixer.md`,
  possibly `scripts/ai/README.md`.
- Products pick this up via sync of the skill/docs/CLI package.

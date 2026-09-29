## Why

`/review-fixer` dismisses correct Low findings once the ~15-line nit-budget is spent, even when the fix is a net code
shrink or size-neutral cleanup. Product PR experience showed humans then override those dismissals for small deletions /
dedupes that never should have competed with additive nits for budget.

## What Changes

- Exempt **size-neutral or size-reducing** correct, this-PR Low findings from the nit-budget: always `fix`, do not
  consume `nit-lines this run`.
- Keep the existing ~15-line soft PR lifetime budget for Low findings that **add** production lines or introduce a new
  abstraction.
- Clarify review-cycle abort: size-neutral/size-reducing Low fixes alone still count as **Fixed non-nit this run: 0**
  (no infinite finder loops); the optional one nit-only pass while budget remains is unchanged for **additive** nits.
- Update `docs/ai_review_policy.md` and `.agents/skills/review-fixer/SKILL.md` checklist wording to match.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `ai-review-policy`: Nit-budget and Fixed non-nit definitions must distinguish additive nits from size-neutral /
  size-reducing Low fixes.

## Impact

- Synced docs + review-fixer skill (products pick up via sync #13).
- No code/runtime change in `scripts/ai/`.
- Agents must estimate net LOC for Low findings when applying budget rules.

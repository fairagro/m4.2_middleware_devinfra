# Tasks

## 1. Skill / docs

- [ ] 1.1 Add a first-hard-gate block to `.agents/skills/review-fixer/SKILL.md` (PR known → always `review-open` first;
      stop on failure; no stash/improvise/silent branch restore; dirty-on-head allowed); verify Fetch section matches
- [ ] 1.2 Add a one-line pointer in thin `docs/review-fixer.md` and/or command/prompt if they summarize fetch; verify no
      contradictory “improvise checkout” wording

## 2. Validate

- [ ] 2.1 Run `uv run --project scripts/ai pytest scripts/ai/tests/test_review_checkout.py` and confirm pass
- [ ] 2.2 Run `openspec validate review-fixer-pr-head-hard-gate --strict` and confirm pass

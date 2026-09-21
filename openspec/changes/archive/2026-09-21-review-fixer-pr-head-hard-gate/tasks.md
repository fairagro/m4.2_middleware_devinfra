# Tasks

## 1. Plumbing

- [x] 1.1 Add structured `PrHeadGateError` + success `ok`/`pr_head_ok` on `review-open`; verify CLI JSON for
      dirty-wrong-branch includes `error_code` and `agent_action: stop`
- [x] 1.2 Extend `test_review_checkout.py` for structured gate JSON; verify suite passes

## 2. Skill / docs

- [x] 2.1 Point `/review-fixer` skill at CLI `ok` / `pr_head_ok` / `agent_action` (first hard gate); no stash/improvise
- [x] 2.2 Update thin docs/README for structured gate JSON; verify no contradictory wording

## 3. Validate

- [x] 3.1 Run `uv run --project scripts/ai pytest scripts/ai/tests/test_review_checkout.py` and confirm pass
- [x] 3.2 Run `openspec validate review-fixer-pr-head-hard-gate --strict` and confirm pass

## 1. Docs and skill honesty

- [x] 1.1 Update `docs/review-fixer.md` with the Code Quality gap (thread resolve ≠ Dismiss finding; read-only findings API) and verify the section is linked from the skill or README index as appropriate
- [x] 1.2 Update `.agents/skills/review-fixer/SKILL.md` Phase 1 / open-work rules for CQ threads + linked `state: open` findings (manual dismiss required; do not claim clear) and verify the normative MUST language is present

## 2. review-open enrichment

- [x] 2.1 Implement soft-fail Code Quality findings fetch + correlation onto CQ bot threads in `scripts/ai` and verify unit/fixture tests cover attach + soft-fail paths
- [x] 2.2 Document the enrichment fields in `scripts/ai/README.md` (and CLI help if present) and verify `review-open` help/README mention finding metadata

## 3. Validation

- [x] 3.1 Run `scripts/ai` pytest for review shaping and verify new tests pass
- [x] 3.2 Spot-check (live or recorded) against a product PR with CQ findings when credentials allow; otherwise document fixture-only verification in the PR body

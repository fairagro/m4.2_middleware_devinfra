## 1. CLI: PR head ensure

- [ ] 1.1 Add helper to resolve PR `headRefName` and ensure local checkout (`gh pr checkout` / fetch+checkout), with
      dirty-on-wrong-branch refuse and fail-closed errors
- [ ] 1.2 Wire ensure into `review-open` before shaping; include `head_ref` and `current_branch` in success JSON
- [ ] 1.3 Document the side effect in `scripts/ai/README.md`

## 2. Tests

- [ ] 2.1 Happy path: clean wrong branch → checkout PR head → JSON includes head fields
- [ ] 2.2 Refuse: dirty tree on non-head branch → non-zero + clear error, no branch switch
- [ ] 2.3 Allow: dirty tree already on PR head → proceed with shaping

## 3. Skill and docs

- [ ] 3.1 Update `.agents/skills/review-fixer/SKILL.md`: PR-scoped runs require successful `review-open` (head checkout)
      before any local `fix` edits
- [ ] 3.2 Short note in `docs/review-fixer.md` (+ command/prompt only if they duplicate the first-step wording)

## 4. Validate

- [ ] 4.1 Run targeted `scripts/ai` tests; `openspec validate --strict` for this change; format/lint Markdown

# Tasks: split surface quality bar path map

## 1. Docs split

- [ ] 1.1 Add `docs/surface-quality-bar.global.md` with the current path→surface table (moved from the policy) plus
      short how-to-read and pointer to product `docs/surface-quality-bar.md`
- [ ] 1.2 Update `docs/ai_review_policy.md` Surface quality bar section: keep rules prose, remove the table, link to
      global map + optional product overlay
- [ ] 1.3 Note sync contract (global synced; product `surface-quality-bar.md` not overwritten) in the global map and/or
      README docs index as needed

## 2. Spec and pointers

- [ ] 2.1 Apply/confirm delta already in this change under `specs/ai-review-policy` against main
      `openspec/specs/ai-review-policy` expectations
- [ ] 2.2 Update skill/docs pointers (review-fixer, issue-fixer, `docs/issue-fixer.md`, README) to cite
      `docs/surface-quality-bar.global.md` where they only cite the policy section for the path map

## 3. Validate

- [ ] 3.1 `openspec validate split-surface-quality-bar-path-map --strict` (or project equivalent)
- [ ] 3.2 `npm run format:md` and `npm run lint:md` on touched Markdown

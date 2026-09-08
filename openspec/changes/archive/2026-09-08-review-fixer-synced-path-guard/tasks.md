# Tasks: review-fixer synced-path guard

## 1. Synced-paths allowlist

- [x] 1.1 Add `docs/synced-paths.global.md` with allowlist globs/paths from issue AC + README inventory and documented
      overlay exceptions
- [x] 1.2 Link the allowlist from root `README.md` Docs index (and brief ownership note if missing)

## 2. review-fixer + policy

- [x] 2.1 Update `.agents/skills/review-fixer/SKILL.md`: hard stop before step 5 for allowlisted paths in consumers; B2
      follow-up/dismiss; Devinfra-checkout exception; no dirty synced trees
- [x] 2.2 Update `docs/ai_review_policy.md` with sync-SoT override sentence and link to `docs/synced-paths.global.md`
- [x] 2.3 Cross-link surface bar / thin command or prompt only if needed for discoverability (no new action enum)

## 3. Attached content fixes

- [x] 3.1 Rewrite `scripts/ai/README.md` Run/Tests for Devinfra workspace vs consumer `--project scripts/ai`
- [x] 3.2 Make `_dev_tokens_write` in `scripts/dev-tokens.sh` atomically replace the store via `mv`

## 4. Validate

- [x] 4.1 Format/lint touched Markdown (`npm run format:md` / `npm run lint:md` as needed)
- [x] 4.2 Spot-check: skill decision order mentions allowlist; token write uses rename; README has both layouts

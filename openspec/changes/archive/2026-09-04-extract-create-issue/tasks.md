# Extract create-issue — Tasks

## 1. Skill (#14)

- [x] 1.1 Add `.agents/skills/create-issue/SKILL.md` from API: creator-only; six org issue types including
      `Refactoring`; triage labels; body template; clear Task vs Refactoring; cite `docs/ai_review_policy.md`
- [x] 1.2 Auth section matching review-fixer (`scripts/bin/gh`, chat ask for `source ./scripts/set-dev-tokens.sh`, no
      PAT in chat)
- [x] 1.3 Create-if-missing for allowlisted triage labels only (fixed colors/descriptions); never free-text labels

## 2. Entrypoints (#14)

- [x] 2.1 Add `.cursor/commands/create-issue.md` pointing at the skill + policy vocabulary; list all six types
- [x] 2.2 Add `.github/prompts/create-issue.prompt.md` (include `Refactoring`)

## 3. Docs (#14)

- [x] 3.1 Document org issue types and triage label families (incl. create-if-missing) in README and/or short docs
- [x] 3.2 Index `/create-issue` among synced agent paths in root README

## 4. Verify

- [x] 4.1 Sanity-check: skill/command/prompt coherent; Auth matches review-fixer; allowlist complete; no bootstrap
      script
- [x] 4.2 Run `npm run format:md` and `npm run lint:md`; fix remaining findings by hand

## 5. review-fixer integration

- [x] 5.1 Point review-fixer Medium+ follow-ups at create-issue (skill + policy + review-fixer spec); drop inline-only
      create template

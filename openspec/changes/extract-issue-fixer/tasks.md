# Extract issue-fixer — Tasks

## 1. Skill (#15)

- [ ] 1.1 Add `.agents/skills/issue-fixer/SKILL.md` from API + lock-ins A–G: triage; explore pause
      (Feature/Refactoring); Discussion/Security gates; empty bootstrap commit on clean tree; draft PR with
      `Fixes #<n>`; local implement; no fix commit/push; split rule (~50 guideline); Auth matching review-fixer
- [ ] 1.2 Deferred work only via create-issue (max 3–6): `relation: sub-of` for acceptance-criteria splits, `linked` for
      distinct follow-ups; missing create-issue → print inputs, no parallel template; optional OpenSpec propose offer
- [ ] 1.3 Quality-check wording when consumer has `middleware/` (aligned with review-fixer)

## 2. Entrypoints (#15)

- [ ] 2.1 Add `.cursor/commands/issue-fixer.md` pointing at the skill; summarize explore-before-PR and empty-commit
      exception
- [ ] 2.2 Add `.github/prompts/issue-fixer.prompt.md` (same rules; allow empty bootstrap push; forbid fix auto-push)

## 3. Docs parity (all three skills)

- [ ] 3.1 Add `docs/issue-fixer.md` (workflow, split, create-issue handoff + relation, Auth pointer)
- [ ] 3.2 Add `docs/review-fixer.md` (skill + policy pointers; open-work / no-commit summary; follow-up relation)
- [ ] 3.3 Update `docs/create-issue.md` for `/issue-fixer` handoff, `/review-fixer` handoff, and **sub-of vs linked**
- [ ] 3.4 Index `/issue-fixer` in README Docs, layout, and synced-paths blurb; link `docs/review-fixer.md` and
      `docs/issue-fixer.md` consistently with create-issue

## 4. Sibling skill wiring

- [ ] 4.1 Amend `.agents/skills/create-issue/SKILL.md`: accept `/issue-fixer` invocations; document
      `relation: sub-of     #<n> | linked`; implement via `gh issue create --parent` (or equivalent) with linked
      fallback on failure
- [ ] 4.2 Amend `.agents/skills/review-fixer/SKILL.md` Follow-up section: pass relation to create-issue (`linked`
      default; `sub-of` only for remaining `Fixes #<n>` acceptance criteria)

## 5. Verify

- [ ] 5.1 Sanity-check: skill/command/prompt/docs coherent with A–G; Auth matches siblings; Copilot prompt allows empty
      bootstrap push; relation heuristics consistent across the three skills
- [ ] 5.2 Run `npm run format:md` and `npm run lint:md`; fix remaining findings by hand

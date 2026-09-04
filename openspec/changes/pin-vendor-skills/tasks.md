# Pin vendor skills — Tasks

## 1. Install and commit vendor skills

- [ ] 1.1 Install `gh` skill from `cli/cli` into project `.agents/skills/gh`
- [ ] 1.2 Install `scan-secrets` from `GitGuardian/agent-skills` into project `.agents/skills/scan-secrets`
- [ ] 1.3 Confirm trees are present and suitable to commit (no hand edits)

## 2. Docs and excludes

- [ ] 2.1 Document install + `gh skill update` + do-not-hand-edit in root README
- [ ] 2.2 Confirm markdownlint + Prettier ignores for vendor paths; note pre-commit for later quality skeleton

## 3. Verify

- [ ] 3.1 Sanity: paths exist; `npm run lint:md` / format ignore vendor trees; format/lint any docs we touch

# Pin vendor skills — Tasks

## 1. Install and commit vendor skills

- [x] 1.1 Install `gh` skill from `cli/cli` into project `.agents/skills/gh`
- [x] 1.2 Install `docker` from `Mindrally/skills` into project `.agents/skills/docker`
- [x] 1.3 Install `hadolint` from `rshade/agent-skills` into project `.agents/skills/hadolint`
- [x] 1.4 Install `uv` from `balintdecsi/skills` into project `.agents/skills/uv`
- [x] 1.5 Remove `.agents/skills/scan-secrets` (not pinned)
- [x] 1.6 Confirm trees are present and suitable to commit (no hand edits)

## 2. Docs and excludes

- [x] 2.1 Document install + `gh skill update` + do-not-hand-edit in root README
- [x] 2.2 Confirm markdownlint + Prettier ignores for vendor paths; note pre-commit for later quality skeleton

## 3. Verify

- [x] 3.1 Sanity: paths exist; `npm run lint:md` / format ignore vendor trees; format/lint any docs we touch

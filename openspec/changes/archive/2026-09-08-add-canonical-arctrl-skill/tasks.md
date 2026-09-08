# Tasks: add-canonical-arctrl-skill

## 1. Import canonical skill

- [x] 1.1 Create `.agents/skills/arctrl/` and copy harvester `SKILL.md` (raw via `gh api`) as the starting content
- [x] 1.2 Confirm front matter / sections cover arctrl ≥ 3.2.1 harvester fidelity (casing, fable_library, WriteContracts
      / GetAdditionalPayload, Comment, Columns API); do not thin to API/sql-to-arc size

## 2. Docs and first-party treatment

- [x] 2.1 Update root README: layout row for `.agents/skills/arctrl/`; clarify first-party (not `gh skill` pin)
- [x] 2.2 Verify vendor excludes (prettier / markdownlint / pre-commit) still list only `gh`, `docker`, `hadolint`, `uv`
      — do not add `arctrl`

## 3. Validate

- [x] 3.1 Run `npm run format:md` and `npm run lint:md`; fix remaining lint by hand if needed (including the new skill)
- [x] 3.2 Spot-check skill path exists and README discovery text matches the spec scenarios

## 1. Propose skill / command

- [ ] 1.1 Add a final Prettier-write step to `.cursor/skills/openspec-propose/SKILL.md` after all required artifacts
      exist (scoped to `changeRoot` / `openspec/changes/<name>/`); verify the skill text names `format:md:check`
      alignment
- [ ] 1.2 Mirror the same step in `.cursor/commands/opsx-propose.md` (and `.github/prompts/opsx-propose.prompt.md` if it
      duplicates the procedure); verify command and skill agree

## 2. Docs

- [ ] 2.1 Document the propose→Prettier guarantee and `openspec update` overwrite risk in `docs/quality.md` and/or
      `openspec/principles.global.md`; verify no guidance tells products to ignore `openspec/changes/**`

## 3. Verify

- [ ] 3.1 Run Prettier write on `openspec/changes/opsx-propose-prettier-format/**` then `npm run format:md:check` /
      `openspec validate opsx-propose-prettier-format --strict`; verify both pass

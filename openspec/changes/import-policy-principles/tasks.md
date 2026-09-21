## 1. Principles

- [ ] 1.1 Add Import policy section to `openspec/principles.global.md` (rules 1–7 + A–D lock-ins); verify section is
      present and cites module-level / absolute / no path-hack rules
- [ ] 1.2 Run `npm run format:md` / `npm run lint:md` on the touched principles file until clean

## 2. Agent pointer

- [ ] 2.1 Update `.agents/skills/code-review/SKILL.md` goal 5 to cite Import policy in `principles.global.md`; verify
      the citation exists
- [ ] 2.2 Update `docs/code-review.md` to point at Import policy for import-graph judgment; verify `npm run lint:md` is
      clean

## 3. Validate

- [ ] 3.1 Run `openspec validate import-policy-principles --strict` until green

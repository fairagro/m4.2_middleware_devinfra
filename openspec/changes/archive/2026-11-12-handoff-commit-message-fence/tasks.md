## 1. Skills

- [x] 1.1 Update `.agents/skills/issue-fixer/SKILL.md` Handoff example: label outside fence; fence = subject only —
      verify the example fence body has no `Suggested commit message` string
- [x] 1.2 Update `.agents/skills/review-fixer/SKILL.md` the same way — verify grep of that Handoff section shows label
      only outside the fence

## 2. Docs (if needed)

- [x] 2.1 Check `docs/quality.md` / `docs/issue-fixer.md` for examples that put the label inside a fence; fix or add a
      one-line note that the copyable block is subject-only — verify no docs fence includes the label line

## 3. Validate

- [x] 3.1 Run `openspec validate handoff-commit-message-fence --strict` and Prettier/markdownlint on touched Markdown —
      verify clean

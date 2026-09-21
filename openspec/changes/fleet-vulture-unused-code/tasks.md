## 1. Dependency and hooks

- [ ] 1.1 Add a pinned `vulture` dependency to the shared uv quality dependency set products/hooks use; run `uv lock` /
      sync as required and verify `uv run vulture --version` works
- [ ] 1.2 Add a commit-stage pre-commit hook that runs `uv run vulture middleware/ --min-confidence 100` (no whitelist
      file) and verify `uv run pre-commit run vulture --all-files` invokes it (exit may be non-zero if findings exist)

## 2. CI and docs

- [ ] 2.1 Add a matching vulture step to `.github/workflows/reusable-code-quality.yml` (same confidence 100 / package
      root) that fails the job on findings; verify the workflow YAML references the same policy as the hook
- [ ] 2.2 Update `docs/quality.md` parity table + files/notes (hooks+CI, IDE exception, D2 policy, FP → `# noqa`/fix)
      and `openspec/principles.global.md` Code Quality example; verify markdown lint/format clean for touched docs

## 3. Code-review anti-duplication

- [ ] 3.1 Update `.agents/skills/code-review/SKILL.md` and `docs/code-review.md` so vulture is toolchain-owned (not
      “once landed”); verify import-linter remains “once landed”

## 4. Validate

- [ ] 4.1 Run `openspec validate fleet-vulture-unused-code --strict` and confirm pass

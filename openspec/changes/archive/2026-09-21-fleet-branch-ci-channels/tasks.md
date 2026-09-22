## 1. Version gate + docs

- [x] 1.1 Change `reusable-build.yml` RC gate from `feature/*` to `build/*` (hard cut; update branch-label strip) and
      verify the condition string is `build/*`
- [x] 1.1b Align `reusable-helm-pre-release.yml` (fail unless `build/*`; strip `build/` for label) and verify no
      remaining `feature/` label strip in `.github/workflows/`
- [x] 1.2 Update `docs/ci.md` version scheme text from `feature/*` to `build/*` and mention fleet channels briefly
- [x] 1.3 Update `openspec/principles.global.md` Branch Strategy table to `build`/`ci`/`docs`/`chore` and verify no
      normative `feature/*` work-branch row remains

## 2. Plumbing

- [x] 2.1 Add `--channel {build,ci,docs}` (default `build`) to `issue-branch` / `issue-start` and form
      `{channel}/issue-<n>-<slug>`; verify unit tests cover default + explicit channel
- [x] 2.2 Update `scripts/ai/README.md` command table for the new branch shape; verify markdownlint MD060 if table
      padded

## 3. issue-fixer surface

- [x] 3.1 Update `.agents/skills/issue-fixer/SKILL.md` branch cadence + channel heuristics; verify skill text uses
      `{channel}/issue-…` not bare `issue-…`
- [x] 3.2 Update thin docs/commands/prompts (`docs/issue-fixer.md`, `.cursor/commands/issue-fixer.md`,
      `.github/prompts/issue-fixer.prompt.md`) to match

## 4. Validate

- [x] 4.1 Run `uv run --project scripts/ai pytest scripts/ai/tests/test_plumbing.py` and confirm pass
- [x] 4.2 Run `openspec validate fleet-branch-ci-channels --strict` and confirm pass

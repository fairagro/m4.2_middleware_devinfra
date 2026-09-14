# issue-fixer OpenSpec for Tasks — Tasks

## 1. Skill

- [x] 1.1 Replace the global OpenSpec ban in `.agents/skills/issue-fixer/SKILL.md` with the type table (Task / Feature /
      Refactoring: propose → apply → draft PR → archive as last `go`; Bug / cheap Security: current fast path;
      Discussion unchanged; user override)
- [x] 1.2 Document embed (follow opsx propose/apply/archive skills), in-skill explore, `issue-branch` before propose,
      `skip_specs` vs delta specs, and preserved guardrails (no auto-commit, no empty bootstrap, draft PR only when
      ahead of `main`)
- [x] 1.3 Keep `/review-fixer` and `/create-issue` off OpenSpec in the issue-fixer skill text

## 2. Entrypoints and docs

- [x] 2.1 Update `.cursor/commands/issue-fixer.md` to match the type-routed cadence (not “never OpenSpec”)
- [x] 2.2 Update `.github/prompts/issue-fixer.prompt.md` the same way
- [x] 2.3 Update `docs/issue-fixer.md` (workflow, skip_specs, last-`go` archive) and the README Issue-fixer blurb

## 3. Validate

- [x] 3.1 `openspec validate issue-fixer-opsx-for-tasks --strict` (and `npm run format:md` / `npm run lint:md` on
      touched Markdown)

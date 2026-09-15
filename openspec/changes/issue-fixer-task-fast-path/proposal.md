## Why

`/issue-fixer` currently requires OpenSpec for org type **Task** (same as Feature/Refactoring). That mismatches
`/create-issue`, where Task means a bounded known-how slice. Small config/hook Tasks pay a full propose → apply →
archive cadence that does not earn its keep ([#125](https://github.com/fairagro/m4.2_middleware_devinfra/issues/125)).

## What Changes

- **Task** uses the Bug-style fast path (no OpenSpec unless the user says `use opsx`)
- **Feature** / **Refactoring** keep OpenSpec; docs-only exception remains for those types only
- Skill-file changes still require OpenSpec even if typed Task
- Misfiled Task that clearly changes `openspec/specs/` → pause once (retype Feature or `use opsx`)
- Sharpen Task definition in `/create-issue`
- **Supersede / abandon** open change `issue-fixer-opsx-for-tasks` (Task→opsx) so no conflicting delta remains
- Align skill, Cursor command, Copilot prompt, `docs/issue-fixer.md`, and specs

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `issue-fixer`: Task off OpenSpec by default; Feature/Refactoring stay on OpenSpec (docs-only + skill-file rules as
  locked)
- `create-issue`: Task typing contract sharpened (known-how vs Feature capability vs Refactoring structure)

## Impact

- `.agents/skills/issue-fixer/SKILL.md`, `.agents/skills/create-issue/SKILL.md`
- `.cursor/commands/issue-fixer.md`, `.github/prompts/issue-fixer.prompt.md`, `docs/issue-fixer.md`
- `openspec/specs/issue-fixer/spec.md`, `openspec/specs/create-issue/spec.md`
- Remove `openspec/changes/issue-fixer-opsx-for-tasks/` (abandoned; superseded by this change)
- No `m42-ai` CLI contract change

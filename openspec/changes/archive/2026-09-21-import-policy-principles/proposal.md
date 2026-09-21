## Why

Product agents (and humans) keep papering over bad import graphs with runtime path hacks, deferred imports, and relative
imports. Shared principles lack a durable import policy. Issue
[#156](https://github.com/fairagro/m4.2_middleware_devinfra/issues/156) (retyped Feature; A–D locked in explore).

## What Changes

- Add an **Import policy** section to `openspec/principles.global.md` (rules 1–7 + decided A–D)
- Point agents at that section from `/code-review` guidance (`SKILL.md` and/or `docs/code-review.md`)
- Update OpenSpec `global-principles` (and `code-review` if the skill/doc contract changes)
- **No** product code cleanup here (harvester #155 / #140 remain product follow-ups)
- **No** import-linter landing in this change

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `global-principles`: Require a normative Import policy in `principles.global.md` (module-level absolute imports, no
  path hacks / cycle-breaking deferred imports, exceptions documented; A–D lock-ins)
- `code-review`: Require the code-review skill (and shared code-review doc) to cite that Import policy for import-graph
  judgment

## Impact

- Devinfra: `openspec/principles.global.md`, `.agents/skills/code-review/SKILL.md`, `docs/code-review.md`, OpenSpec
  `global-principles` + `code-review`
- Products after sync: agents/reviewers see the shared import rules; existing product graphs may need separate cleanup
  issues

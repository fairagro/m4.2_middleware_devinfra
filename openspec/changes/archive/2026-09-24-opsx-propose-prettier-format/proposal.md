## Why

OpenSpec propose writes `openspec/changes/<name>/**/*.md` that often fails fleet Prettier (`proseWrap: always`,
`printWidth: 120`). Commit-stage `prettier-md` / CI `format:md:check` then fail on the first commit of a new change.
Opsx skill/command Markdown was correctly ignored in #241; **change artifacts stay product-owned and must stay
Prettier-checked**. Generation must emit (or immediately format to) Prettier-clean Markdown so agents do not need a
second manual format turn.

## What Changes

- Add a mandatory final step to the OpenSpec **propose** skill (and matching `/opsx-propose` command): after all change
  artifacts exist, run Prettier **write** scoped to that change directory (fleet `.prettierrc.json`).
- Document that `openspec update` may regenerate opsx skills/commands and can wipe the patch — re-apply or upstream.
- Short note in synced quality / principles prose so product agents know the guarantee.
- **Non-goal:** ignoring `openspec/changes/**` in `.prettierignore`.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: Require that OpenSpec propose flows format the new change’s Markdown with the fleet Prettier
  config before the propose step is considered complete.

## Impact

- `.cursor/skills/openspec-propose/SKILL.md`, `.cursor/commands/opsx-propose.md` (and GitHub prompt twin if present)
- Synced docs: `docs/quality.md` and/or `openspec/principles.global.md`
- Product repos after they pick up skill/docs (opsx skills are CLI-managed, not sync-allowlisted — products need the
  same skill patch or an `openspec update` that includes it)

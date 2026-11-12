# Proposal

## Why

`/issue-fixer` and `/review-fixer` pause with a Suggested commit message inside a single fenced block that also contains
the label line. Cursor’s copy-to-clipboard copies that whole fence, so pasting into `git commit` includes
`Suggested commit message:` and forces hand-selection of the subject
([#380](https://github.com/fairagro/m4.2_middleware_devinfra/issues/380)).

## What Changes

- Require the handoff **label** (e.g. “Suggested commit message:”) to appear **outside** the copyable fenced block
- Require the fence to contain **only** the Conventional Commits subject (and optional short body)
- Update synced skill files and brief docs examples that teach the old shape

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `issue-fixer`: handoff Suggested commit message fence must exclude the label line
- `review-fixer`: same handoff fence contract for Phase-1 pauses

## Impact

- `.agents/skills/issue-fixer/SKILL.md`, `.agents/skills/review-fixer/SKILL.md` (synced foundation)
- Optional prose in `docs/quality.md` / `docs/issue-fixer.md` if they show the box shape
- Agent pauses after merge use the new shape; no runtime CI change

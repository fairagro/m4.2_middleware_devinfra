## Context

See `proposal.md`. Skills already require a handoff Conventional Commits subject; only the **presentation** of that
subject is wrong for Cursor’s copy-to-clipboard (label inside the fence).

## Goals / Non-Goals

**Goals:**

- Spec + skill examples: label outside fence; fence = subject (+ optional body) only
- Keep the same pause cadence and Conventional Commits rules

**Non-Goals:**

- Changing Cursor UI / inventing a custom copy button
- Adding `m42-ai suggest-commit` (tracked separately if needed)
- Renaming the prose label away from “Suggested commit message”

## Decisions

1. **Label outside, fence inside** — keep the familiar “Suggested commit message:” line as Markdown prose above a fenced
   `text` (or bare) block that holds only the subject. Agents MUST use this shape in live pauses, not only in skill
   examples.
2. **No new capability** — extend the existing handoff requirements on `issue-fixer` and `review-fixer`.
3. **Docs** — one-line clarity in `docs/quality.md` / `docs/issue-fixer.md` only if they imply the label is inside the
   box; otherwise skills alone are enough.

## Risks / Trade-offs

- [Agents still paste old shape from memory] → Skill example is the SoT; archive sync keeps main specs aligned.
- [Multi-line bodies] → Fence still may include subject + blank line + body; never the label.

## Migration Plan

1. Land delta + skill/docs edits on Devinfra; sync carries skills to consumers.
2. No dual-run period; next agent pauses use the new shape.

## Open Questions

None.

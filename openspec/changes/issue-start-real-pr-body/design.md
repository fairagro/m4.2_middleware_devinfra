## Context

See proposal.md — Why. Locked explore choice **C**: useful auto-default body plus skill guidance to pass `--body-file`
when the agent has a better Summary. Channel `ci`.

## Goals / Non-Goals

**Goals:**

- Never open a draft PR whose Summary is only `MVP scope: (fill in)`.
- Agents can override with a full body file; default remains usable when they do not.
- Contract tests cover default and override without live GitHub.

**Non-Goals:**

- Auto-editing PR bodies after create.
- Changing `issue-branch` / `branch-ahead` / `pr-strip-footer` behavior beyond documenting strip still applies.
- Generating long commit messages or AI-written prose in the CLI.

## Decisions

1. **Default body shape** — When no override is given:

   ```markdown
   ## Summary
   - <issue title>
   - <commit subject 1>
   - <commit subject 2>
   …

   Fixes #<n>
   ```

   Commit subjects from `git log --format=%s <base>..HEAD` (oldest→newest or newest-first — pick **newest first**, cap
   ~15 lines to keep bodies short). If the only subject duplicates the issue title, omit the duplicate bullet.

2. **Override** — `--body-file` / `--body` replace the entire body. Callers MUST still include `Fixes #<n>` (CLI MAY
   append `Fixes #<n>` if missing when override is used — prefer **append if absent** so agents cannot forget
   autoclose).

3. **Skill path** — `/issue-fixer` instructs: prefer `--body-file` with 1–3 real Summary bullets after apply/implement;
   if omitted, CLI default is acceptable. Remove “fill in” as the example template.

4. **Reject the old stub** — Do not emit `(fill in)` under any path.

## Risks / Trade-offs

- [Noisy commit subjects] → Mitigation: cap list; agent `--body-file` override.
- [Override without Fixes] → Mitigation: append `Fixes #<n>` when missing.
- [Skill drift] → Mitigation: delta + thin docs update in same change.

## Migration Plan

1. Land CLI + tests + skill/docs + spec sync.
2. Product sync picks up skills/`scripts/ai`.
3. Rollback: revert commit; old stub behavior returns.

## Open Questions

None.

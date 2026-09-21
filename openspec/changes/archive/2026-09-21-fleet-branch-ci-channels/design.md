## Context

See proposal.md — Why. Lock-in from #185 Discussion: philosophy B (prefix = CI channel; path filters for fine jobs);
channels `build` / `ci` / `docs` / `chore`; issue number always in `{channel}/issue-<n>-…`; hard cut off `feature/*` for
RC (no alias).

## Goals / Non-Goals

**Goals:** Align reusable-build RC gate, principles/CI docs, issue-fixer skill, and `m42-ai issue-branch`/`issue-start`
on the same channel contract.

**Non-Goals:** New Fine-grained prefixes per work kind; auto-migrating existing product `feature/*` branches; changing
Final Release (`main` + `release_type: final`); implementing path-filter matrices beyond documenting that they own
fine-grained skips.

## Decisions

1. **Channels:** `build` (image/RC), `ci` (tooling), `docs`, `chore` (sync/bots — not created by issue-fixer).
2. **Hard cut:** `reusable-build` RC only on `build/*`; strip `feature/` from BRANCH_LABEL sed accordingly
   (`s|^build/||`). Same for `reusable-helm-pre-release` (fail closed unless `build/*`).
3. **CLI:** `--channel {build,ci,docs}` on `issue-branch` / `issue-start`, default `build`.
4. **Skill:** Pick channel from scope heuristics; default `build` when unclear.
5. **Principles table:** Replace `feature/*` row with `build/*` / `ci/*` / `chore/*`; keep `docs/*`.

## Risks / Trade-offs

- [Product Pre Release still on `feature/*`] → Hard cut by design; document in CI docs / PR summary.
- [Wrong channel from skill heuristics] → Prefer `build` when unsure; user can recreate branch.

## Migration Plan

1. Land Devinfra change (workflow + docs + skill + CLI).
2. Products rename active Pre Release branches to `build/…` before next RC dispatch.
3. Archive OpenSpec change after merge.

## Open Questions

None — alias rejected; `ci/` naming locked.

## Context

See proposal.md — Why. Issue #16; explore lock-ins: all four CLI commands in one PR; package under `scripts/ai/` with
its own `pyproject.toml`; GitHub via PATH `gh`. `/issue-fixer` previously treated `/opsx-propose` as optional.

## Goals / Non-Goals

**Goals:** Ship `m42-ai` with the four commands; fixture tests; skill/doc wiring; mandatory propose in issue-fixer;
canonical issue-fixer spec on this change.

**Non-Goals:** Encoding AI review policy in Python; second auth model; live GitHub in CI; requiring `/opsx-explore`.

## Decisions

- **Package layout:** `scripts/ai/` + hatchling + console script `m42-ai` — isolates from future product packages.
- **Transport:** subprocess `gh`/`git` on PATH — same wrappers as skills.
- **issue-fixer propose:** `/opsx-propose` **mandatory**, then **spec-review pause** until user `go`; `/opsx-explore`
  **optional**; missing `openspec/` → stop.
- **Backfill:** this change’s propose documents work already started on branch `issue-16-ai-gh-cli` / PR #23.

## Risks / Trade-offs

- **[Risk] Agents still dump GraphQL** → Mitigation: skill text leads with CLI; done-when for #16 is skill says so
- **[Risk] issue-start vs dirty tree during propose** → Mitigation: propose writes files; empty commit only after clean
  tree or user commits propose+code together
- **[Trade-off] Large single PR (all four commands)** → Accepted per user lock-in 1C

## Migration Plan

1. Land CLI + skill wiring + OpenSpec artifacts on PR #23
2. Sync to product repos later
3. Archive change after merge; sync issue-fixer into `openspec/specs/`

## Open Questions

None for MVP.

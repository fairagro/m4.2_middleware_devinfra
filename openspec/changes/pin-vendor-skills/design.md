# Pin vendor skills — Design

## Context

See proposal.md — Why. Issue #6; explore lock-ins: commit installed trees (install+commit = pin); install into
`.agents/skills/`; defer pre-commit config.

## Goals / Non-Goals

**Goals:** Committed `gh` + `scan-secrets` vendor skills; README install/update; ignores confirmed.

**Non-Goals:** Full quality/pre-commit skeleton (#7+); installing `ggshield` in the Dev Container in this change;
hand-maintained forks of vendor skills.

## Decisions

- **Pinning:** Commit the installed skill trees. Document install commands for reproducibility/rebuild; optional future
  pin refs in README if useful, but the git tree is the source of truth.
- **Install target:** Project-scope install so Cursor/Copilot land under `.agents/skills/` (shared destination).
- **Sources:** `cli/cli` → `gh`; `GitGuardian/agent-skills` → `scan-secrets` (per issue + upstream docs).
- **Pre-commit:** Document intent only; no new hook config until quality skeleton.

## Risks / Trade-offs

- **[Risk] Large vendor trees in git** → Acceptable for shared sync; ignores keep lint quiet
- **[Risk] `gh skill` preview API changes** → Pin via commit; update deliberately
- **[Trade-off] No SHA in README** → Tree SHA is enough; README can still show exact install lines used

## Migration Plan

1. Propose → apply on draft PR for #6
2. Consumers sync `.agents/skills/{gh,scan-secrets}` + README/ignores

## Open Questions

None after explore lock-in.

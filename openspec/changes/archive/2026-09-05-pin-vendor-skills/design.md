# Pin vendor skills — Design

## Context

See proposal.md — Why. Issue #6; explore lock-ins: commit installed trees (install+commit = pin); install into
`.agents/skills/`; defer pre-commit config. Skill set refined: keep `gh`; add Docker + hadolint + `uv`; drop
`scan-secrets` (ggshield doctrine skill not required for agent happy path).

## Goals / Non-Goals

**Goals:** Committed `gh`, `docker`, `hadolint`, `uv` vendor skills; README install/update; ignores confirmed.

**Non-Goals:** Full quality/pre-commit skeleton (#7+); pinning GitGuardian `scan-secrets`; hand-maintained forks of
vendor skills; a general `git` skill.

## Decisions

- **Pinning:** Commit the installed skill trees. Document install commands for reproducibility/rebuild; the git tree is
  the source of truth.
- **Install target:** Project-scope install so Cursor/Copilot land under `.agents/skills/` (shared destination).
- **Sources:** `cli/cli` → `gh`; `Mindrally/skills` → `docker`; `rshade/agent-skills` → `hadolint`; `balintdecsi/skills`
  → `uv`.
- **Pre-commit:** Document intent only; no new hook config until quality skeleton.

## Risks / Trade-offs

- **[Risk] Large vendor trees in git** → Acceptable for shared sync; ignores keep lint quiet
- **[Risk] `gh skill` preview API changes** → Pin via commit; update deliberately
- **[Trade-off] No SHA in README** → Tree SHA is enough; README can still show exact install lines used

## Migration Plan

1. Propose → apply on draft PR for #6
2. Consumers sync `.agents/skills/{gh,docker,hadolint,uv}` + README/ignores

## Open Questions

None after explore lock-in.

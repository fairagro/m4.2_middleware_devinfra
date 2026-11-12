## Context

See `proposal.md`. Prerequisites verified: api#653, harvester#591, infra#81 closed; consumer HEADs have `charts/` only.

## Goals / Non-Goals

**Goals:**

- Single chart root `charts/<chart>/` in runner, hooks, IDE, docs, specs
- Legacy-only checkouts become helm-lint no-ops (no discovery)

**Non-Goals:**

- Renaming product chart _names_ under `charts/`
- Changing `reusable-helm-lint.yml` inputs beyond docs examples
- Infra GitOps tools beyond shared pre-commit / docs

## Decisions

1. **Hard drop** — no env flag to re-enable `helm/` / `helmchart/` discovery.
2. **Keep scenario titles** where OpenSpec MODIFIED requires them; rewrite the “Legacy … still work” scenario so legacy
   roots are **not** discovered (no-op).
3. **`helmcharts/`** remains unsupported (already); call it out with the other aliases.

## Risks / Trade-offs

- [Straggler checkout still on legacy root] → Verified none on HEAD; no-op until they sync `charts/`.
- [Caller path filters still list helm/**] → Docs stop recommending; old callers still work until they edit.

## Migration Plan

1. Land Devinfra change; sync to products/Infra.
2. No dual-run period.

## Open Questions

None.

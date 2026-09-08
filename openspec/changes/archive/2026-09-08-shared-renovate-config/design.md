# Design: shared Renovate config + workflow

## Context

See `proposal.md` — Why. Explore lock-ins: **A1** API-seeded config, **B1** per-repo thin workflow (no reusable), **C1**
alerts on / Dependabot version updates off / Renovate for update PRs, **D1** Devinfra-only this PR, **E1**
`RENOVATE_TOKEN` as Actions secret. Config vs job: shared SoT config (products sync or later `extends`); workflows stay
intentionally identical across repos.

## Goals / Non-Goals

**Goals:**

- Land runnable Renovate SoT in Devinfra (config + workflow + docs).
- Document token, local dry-run, product migration, #13 adoption.
- Extend synced-paths allowlist for Renovate artifacts.

**Non-Goals:**

- `reusable-renovate.yml` or multi-repo `RENOVATE_REPOSITORIES` bot.
- Changing product repos in this PR / deleting their `dependabot.yml` here.
- Hosted GitHub Renovate App install (self-hosted Action path only).
- SOPS-backed token storage.

## Decisions

### D1 — One shared config file now; preset/`extends` later if needed

**Choice:** Single root `renovate.json` in Devinfra (A1). Sync copies it; products may later switch to
`extends: ["github>fairagro/m4.2_middleware_devinfra//renovate.json"]` plus overlay without blocking #38.

**Alternatives:** Multi-file preset layout now — extra indirection before first successful run.

### D2 — Per-repo workflow, not reusable

**Choice:** Mirror API `renovate.yml` (B1). Workflow shape is expected to stay the same across repos; prevent drift via
sync, not via `workflow_call`.

**Alternatives:** reusable now — defer until three callers repeatedly need Action-pin bumps in one place.

### D3 — Token

**Choice:** Document `RENOVATE_TOKEN` repository Actions secret (fine-grained PAT scopes as API README). Workflow does
not use SOPS or commit secrets.

### D4 — Docs home

**Choice:** New `docs/renovate.md` linked from README + short pointers from `docs/devcontainer.md` (CLI) and
`docs/ci.md` (automation). Avoid bloating ci.md with full token guide.

### D5 — Config content

**Choice:** Start from API `renovate.json`; add regex managers for remaining Devinfra `versions.env` pins Renovate
should own (e.g. Trivy, Renovate itself, Node/OpenSpec/Prettier, k8s tools as appropriate). Keep Python 3.12 lock and
grouping patterns. Ignore paths that must not be touched if any.

## Risks / Trade-offs

- **[First schedule fails without secret]** → Mitigation: docs + PR checklist; workflow still lands; manual
  `workflow_dispatch` after secret is set.
- **[Config noise / empty PRs in Devinfra]** → Mitigation: dry-run locally; tune `enabledManagers` / ignorePaths.
- **[API diverge until sync]** → Mitigation: #13 adoption note; API converges on shared file.
- **[Dual bots if products keep dependabot.yml]** → Mitigation: docs C1; product PRs out of scope.

## Migration Plan

1. Merge Devinfra PR; set `RENOVATE_TOKEN` on Devinfra; run `workflow_dispatch`.
2. Sync config+workflow to products (#13); set secret per product; remove `dependabot.yml` version updates.
3. Rollback: revert workflow file / disable workflow; Dependabot can be re-enabled in products if needed.

## Open Questions

None — explore lock-ins bind this design.

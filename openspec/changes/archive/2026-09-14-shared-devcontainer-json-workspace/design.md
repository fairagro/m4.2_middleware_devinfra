## Context

See proposal.md — Why. Dev Containers has no `extends` for JSON. Sync already excluded JSON and Compose; products
duplicated almost the whole files for path/`name`/volumes and (in some repos) `remoteEnv` overlays. Option A with a
fixed container path makes **both** files identical across the fleet. Product env remains a real need (#63 pattern:
env/CI, not synced config blobs).

## Goals / Non-Goals

**Goals:**

- Verbatim-shared `.devcontainer/devcontainer.json` and `.devcontainer/docker-compose.yml` on the sync allowlist.
- Common `workspaceFolder` / Compose bind: `/workspace`.
- Distinct Cursor/VS Code window title via `"name": "${localWorkspaceFolderBasename}"`.
- Distinct named volumes via `${localWorkspaceFolderBasename}-…`.
- Documented optional `.devcontainer/product.env` (not synced) for `MYPYPATH` / `CST_*` / similar.

**Non-Goals:**

- Sync-time merge / `.global` split (B1).
- Removing Compose as a file (still used for build-args + DinD service).
- Custom Starship config / prompt polish.
- Implementing product-repo PRs in this change (follow-ups after sync).
- Changing Dockerfile / postCreate beyond path-agnostic checks already required.
- Re-litigating #58 bashrc/`postStart` beyond “not in shared JSON”.

## Decisions

1. **Share both JSON and Compose** — With `/workspace`, the only former Compose delta (bind target) disappears; build
   args are already identical. Prefer this over “JSON shared, Compose product-local” to avoid maintaining a second
   near-copy. **Alternative considered:** Compose product-local for env only — rejected; optional `product.env` is
   enough and keeps Compose verbatim.

2. **Fixed `/workspace` (not basename path)** — One path in JSON and Compose; host clone name irrelevant inside the
   container. Window title uses basename. **Alternative:** `/workspaces/${localWorkspaceFolderBasename}` — requires
   product-specific Compose binds; rejected for full Compose share.

3. **Optional `product.env`** — Shared Compose references `.devcontainer/product.env` with `required: false` so Devinfra
   and products without the file still start; products that need container `MYPYPATH`/`CST_*` add the file locally
   (gitignored or committed product-owned — docs say: never overwrite via sync; not on allowlist). **Alternative:** only
   CI `MYPYPATH` — insufficient for in-container pre-commit/IDE unless hooks inherit another mechanism.

4. **Sync allowlist** — Move both paths from `exclude` to `allow`. Docs stop calling them product-owned interim.

5. **Purpose / overlay requirement** — Rewrite `shared-devcontainer-base` “Consumer overlay” to describe shared JSON +
   Compose and `product.env` / CI env instead of thin JSON overlays.

## Risks / Trade-offs

- **[Risk] Products with `*-cursor` host folders** → Bind uses `..`; only window `name`/volumes use basename — OK.
- **[Risk] Starship shows `workspace`** → Accepted; venv/package/Git + window title remain; prompt polish later.
- **[Risk] Compose `env_file.required: false` support** → Use Compose Specification form supported by current Docker
  Compose V2 in the DinD image; if unavailable, document `touch`-empty file fallback in design/tasks verify step.
- **[Risk] sql-to-arc multi-step `postCreate` / product `postStart`** → Out of shared JSON; product follow-up to fold
  into product scripts invoked from shared postCreate conventions or drop after #58.
- **[Risk] Sync overwrites divergent product JSON/Compose** → Intended; Wave B adopt issues migrate env first if needed.

## Migration Plan

1. Land shared JSON+Compose + allowlist + docs/specs in Devinfra (this PR).
2. Sync to products; open/close adopt follow-ups: add `product.env` where needed, delete overlay comments, rebuild.
3. Rollback: restore exclude + prior blobs from git history; products can temporarily re-fork.

## Open Questions

- None for MVP (product.env vs CI-only already decided: product.env optional + CI inputs remain).

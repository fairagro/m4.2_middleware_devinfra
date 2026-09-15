## Context

See proposal.md — Why. Git has no include/merge for two root `.gitignore` files. Locked Option A: one synced root
baseline; product deltas only via nested `.gitignore`.

## Goals / Non-Goals

**Goals:**

- Fleet-common ignores in Devinfra root `.gitignore`, safe to sync.
- Clear adopt path: nested overlays for product-only paths.
- Allowlist + sync inventory.

**Non-Goals:**

- Forcing helm/demo paths into the shared file.
- Sync deleting old product root boilerplate (product adopt PRs).
- `.gitignore.global` + merge tooling.

## Decisions

1. **Single synced root `.gitignore`** — expand current stub with Python template essentials + Node + env exceptions
   already used in fleet (`!.devcontainer/.env`, `!.env.integration.enc` where applicable). Keep comments brief.

2. **Nested overlays only** — document with examples in `docs/sync.md` (Overlays table row or dedicated subsection).

3. **Allowlist `.gitignore`** — add to `docs/synced-paths.yaml`; inventory row in `docs/sync.md`.

4. **Content scope (MVP)** — prefer GitHub Python gitignore core + project-known paths (uv/ruff/mypy/pytest caches,
   `node_modules/`, `.env`/`.envrc` + exceptions). Avoid dumping entire Django/Flask sections unless useful; keep file
   maintainable.

5. **Product follow-ups** — optional; not required in this Devinfra PR (same pattern as dockerfile-pins adopt issues).

## Risks / Trade-offs

- [Risk] Sync overwrites product root customizations → Mitigation: docs + adopt checklist; nested files for deltas.
- [Risk] Baseline too aggressive ignores tracked product files → Mitigation: review against Devinfra + sample product
  paths; no helm/demo in shared file.

## Migration Plan

Land baseline + allowlist + docs. After merge, sync PRs replace product root `.gitignore`; product PRs move local-only
rules to nested files and drop boilerplate.

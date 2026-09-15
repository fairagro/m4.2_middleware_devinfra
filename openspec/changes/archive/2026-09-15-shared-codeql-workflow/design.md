## Context

Explore lock-ins for [#124](https://github.com/fairagro/m4.2_middleware_devinfra/issues/124): thin synced workflow (not
reusable-only), T2a+weekly, D1, P1, I1; product adopt deferred. All three products already have root `uv.lock` +
`[tool.uv.workspace]` (I1 safe). Branch protection: no direct push to `main` without PR → no `push: main` needed.

## Goals / Non-Goals

**Goals:**

- Single Devinfra SoT for CodeQL workflow + stop product Renovate shadow bumps after sync of `renovate.json` /
  `codeql.yml`
- Align triggers with Feature-PR CI (`pull_request` → `main`) plus weekly drift net
- Toolchain pins from `versions.env`; Action refs consistent with existing workflows

**Non-Goals:**

- Product sync adopt / closing sql_to_arc #136/#137 in this PR
- `reusable-codeql.yml` as the only delivery
- SHA-pinning all Actions; paths-filter on CodeQL
- Changing Feature-PR / reusable-check SARIF upload behavior

## Decisions

1. **Thin synced `codeql.yml`** — same pattern as `renovate.yml`; name must not match `reusable-*.yml` exclude.
2. **T2a + weekly** — `pull_request` (opened/synchronize/reopened) to `main`; cron `33 5 * * 4`; no branch `push`.
3. **D1** — workflow runs in Devinfra as well (verbatim sync).
4. **P1** — e.g. `actions/checkout@v7`, `astral-sh/setup-uv@v10.1.0`, `github/codeql-action/*@v4`; no literal
   `PYTHON_VERSION` / `UV_VERSION` strings in YAML.
5. **I1** — mirror `reusable-code-quality`: source `scripts/load-versions-env.sh`, `uv python install`,
   `uv sync --dev --all-packages` when `matrix.language == python`.
6. **Matrix** — `actions` + `python`, `build-mode: none`, `fail-fast: false` (product template shape).
7. **Renovate disable** — add `.github/workflows/codeql.yml` to product `matchFileNames` alongside `renovate.yml`.

## Risks / Trade-offs

- [Until products sync] Shadow Renovate PRs can continue → Mitigation: defer adopt documented; sync `renovate.json`
  disable helps only after that file is synced (disable path listed before or with codeql sync).
- [Weekly same cron everywhere] All repos fire together → Accepted for verbatim sync.
- [Devinfra Python surface small] Still scanned → Accepted (D1).

## Migration Plan

1. Land Devinfra workflow + allowlist + Renovate disable + docs/specs.
2. Sync to products (#13); products drop divergent local CodeQL.
3. Close obsolete product Renovate PRs that only touched local `codeql.yml`.

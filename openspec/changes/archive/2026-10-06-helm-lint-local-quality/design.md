## Context

See proposal.md — Why. Feature-PR lint is `reusable-helm-lint.yml` (`helm lint` + optional `helm template ci-smoke`).
Local quality is pre-commit commit-stage wrapped by `scripts/quality-check.sh`. Helm is already on the Dev Container
PATH (`HELM_VERSION` in `versions.env`). `check-yaml` excludes Go templates.

## Goals / Non-Goals

**Goals:**

- Same lint + default-values template smoke as CI, on every existing product chart root, from commit-stage quality.
- Verbatim-syncable: no product fork of `.pre-commit-config.yaml`.
- Harmless on Devinfra and other chart-less trees.

**Non-Goals:**

- Installing Helm on unofficial host checkouts.
- Extra `helm template -f` overlays.
- Adding Helm lint to `reusable-code-quality.yml` or a GitHub required check named `Helm Lint`.
- IDE-on-save lint.

## Decisions

1. **Shared runner script + local pre-commit hook** (not a third-party Helm hook repo). Matches `run-uv-audit.sh` /
   `run-import-linter.sh`. Alternative B (external hook rev) rejected for pin and no-op control.

2. **Discovery:** `helmchart/*/Chart.yaml` and `helm/*/Chart.yaml` only (one segment). Nested charts under `charts/`
   inside a root are linted by `helm lint` on the parent, not as extra roots.

3. **No-op vs fail:** zero discovered charts → exit 0 (Helm optional). Any chart → `helm` required. Do not silently skip
   lint when charts exist but Helm is missing.

4. **PATH Helm, not `azure/setup-helm`.** Local/DC already pins Helm in the image. The runner MAY echo `HELM_VERSION`
   from `versions.env` when present for diagnostics; it MUST NOT download Helm.

5. **Hook files filter:** `^(helm|helmchart)/` so normal commits without chart changes skip the hook;
   `quality-check.sh --all-files` still runs it when those paths exist. Devinfra has neither path → skipped/no-op.

6. **Docs:** `docs/quality.md` is the local gate SoT; `docs/ci.md` gets a short “local hook vs Feature-PR reusable”
   pointer, not a second full snippet.

7. **Sync allowlist:** add `scripts/run-helm-lint.sh` to `docs/synced-paths.yaml` `allow` next to the other quality
   runners so products receive the hook entry’s script.

## Risks / Trade-offs

- **[Risk]** Host contributor with charts but no Helm fails commit-stage → Mitigation: message names Dev Container /
  `HELM_VERSION`; supported environment is DC.
- **[Risk]** `helm template` fails on charts that need extra values → Mitigation: same as CI default (`run_template`
  true); product follow-up for values files, not this MVP.
- **[Trade-off]** Commit hook is path-gated; a middleware-only commit will not re-lint charts until `--all-files` / CI.
  Matches ruff/`middleware/` pattern.

## Migration Plan

1. Land runner + hook + docs on Devinfra `main`.
2. Product sync copies the hook; next chart commit or `quality-check.sh` exercises it.
3. Revert is delete hook + script; products resync.

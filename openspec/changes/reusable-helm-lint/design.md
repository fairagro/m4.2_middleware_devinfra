## Context

See proposal.md — Why. Existing Helm reusables (`reusable-helm-release.yml`, `reusable-helm-pre-release.yml`) package
and publish; Feature PRs already use `skip` on code-quality / build / check. Helm is pinned via `HELM_VERSION` in
`versions.env` and `azure/setup-helm` in those publish workflows. Products use different chart roots.

## Goals / Non-Goals

**Goals:**

- A thin Feature-PR reusable that fails closed on chart syntax/schema problems without publishing.
- Same skip/no-op contract as other Feature-PR reusables for required checks.
- Clear docs so products do not misuse the Docker `code` filter.

**Non-Goals:**

- Wiring product callers in this PR (follow-up product issues).
- Multi-chart matrix in v1 (one `chart_dir` per call; products with multiple charts add multiple jobs or call twice).
- kubeconform / schema validation beyond `helm lint` / optional `helm template`.
- Changing Helm publish workflows.

## Decisions

1. **Standalone `reusable-helm-lint.yml`** (not a job inside code-quality or publish workflows)
   - Keeps Python/markdown quality separate from charts; keeps lint off the publish path.
   - Alternative rejected: fold into `reusable-code-quality` (wrong toolchain); lint inside pre-release (wrong
     lifecycle).

2. **Inputs:** `chart_dir` (required), `skip` (default false), `run_template` (default **true**)
   - Template smoke is cheap and catches render errors lint alone can miss; callers can turn it off.
   - No `values` file input in v1 — use chart defaults / `values.yaml` as Helm does by default.

3. **Helm pin:** load `HELM_VERSION` from caller `versions.env` the same way pre-release/release do (`load-versions-env`
   / grep pattern already used there). Fail if pin missing when `skip` is false.

4. **Concurrency:** feature-oriented (`cancel-in-progress: true`), same group shape as `reusable-code-quality`.

5. **Docs:** extend Feature-PR section with a second paths-filter output (e.g. `helm`) and a lint job; keep suggested
   Docker `code` paths free of chart globs. Note product-specific roots (`helmchart/**` vs `helm/**`).

## Risks / Trade-offs

- **[Risk]** `helm template` fails on charts that need CI-only values → Mitigation: `run_template` input; document
  disabling or adding a later `values_file` follow-up.
- **[Risk]** Products forget separate filter and only add chart paths to `code` → Mitigation: docs MUST call this out
  explicitly (spec scenario).
- **[Trade-off]** One chart per job call — simpler than matrix; multi-chart products need multiple jobs.

## Migration Plan

1. Land reusable + docs on Devinfra `main`.
2. Open/refresh product issues to add detect-changes + `uses:` (API #206 and peers).
3. No rollback beyond reverting the workflow; products not yet wired are unaffected.

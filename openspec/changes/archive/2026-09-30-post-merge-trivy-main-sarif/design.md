## Context

See proposal.md — Why. Locked explore choice: **thin dedicated caller (B)**, jobs limited to what is needed to upload
Trivy SARIF on the default branch after push to `main`. `reusable-check` already uploads SARIF when configured and the
caller grants `security-events: write`; it needs image/SBOM artifacts from `reusable-build` in the same run.

## Goals / Non-Goals

**Goals:**

- One documented product caller pattern: `on.push.branches: [main]` → build → check → SARIF on default branch.
- Make clear that this exists for Code Scanning alert hygiene, not as a substitute for Release.

**Non-Goals:**

- Changing Release to skip Trivy or reuse main-push SARIF.
- Extending the Feature PR template with `push: main` (full PR job set would re-run code-quality and is out of scope).
- Required path-filters for v1 (optional later).
- New Devinfra `workflow_call` reusable solely for this orchestration.

## Decisions

1. **Thin caller, not Feature PR extension** — Document a separate recommended workflow (name e.g. “Main Docker Check”
   or equivalent) with only `reusable-build` + `reusable-check`. Rationale: user goal is SARIF on main; code-quality and
   other Feature PR jobs are superfluous runner cost.
2. **No new reusable workflow file in Devinfra** — Orchestration stays product-local YAML calling existing reusables;
   Devinfra owns the synced docs snippet. Rationale: same as Feature PR / Release caller docs today.
3. **Concurrency** — Recommend a caller-level group keyed by workflow + `github.ref` with `cancel-in-progress: true`
   (scan freshness over serialize). Do not require `detect-changes` / `skip` for v1 (every main push that runs the
   workflow builds); products MAY add path filters later.
4. **Permissions** — Document top-level `security-events: write` (and usual `contents: read` / `secrets: inherit` as in
   other Docker callers) so SARIF upload succeeds.

## Risks / Trade-offs

- [Every main push rebuilds images] → Mitigation: document cost; optional path-filters later; keep jobs minimal.
- [Products forget to adopt] → Mitigation: synced `docs/ci.md` + clear AC that alert close requires adopting the
  template.
- [Category / config drift leaves stale alerts] → Mitigation: same `reusable-check` SARIF path as Feature PR/Release so
  tool identity stays consistent.

## Migration Plan

1. Land docs + spec delta in Devinfra.
2. Product sync picks up `docs/ci.md`; each product adds the thin workflow and merges once to refresh `main` SARIF.
3. Rollback: remove the product workflow; Release still gates publish.

## Open Questions

None.

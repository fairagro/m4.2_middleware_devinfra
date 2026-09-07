# Design: reusable CI build, release, and Helm

## Context

See proposal.md — Why. Devinfra already ships `reusable-code-quality.yml` and `reusable-check.yml` with a documented
artifact contract (`docs/ci.md`). The API still owns local `reusable-build.yml`, `reusable-release.yml`,
`helm-release.yml`, and `helm-pre-release.yml`. Explore lock-ins for issue #12: **A1** (inputs), **B1** (Docker release
without PyPI), **C.1** (shared `*-docker-v*` scheme for all three products), **H1** (Helm into this change), **D2**
(concrete docs snippets).

## Goals / Non-Goals

**Goals:**

- Port build + Docker release + Helm publish into `workflow_call` reusables under this repo.
- Keep the #11 check artifact contract stable so existing check callers keep working once build is shared.
- Document Docker (feature-PR / release) and Helm caller patterns in `docs/ci.md`.

**Non-Goals:**

- Product sync PRs that flip `uses:` (#13).
- PyPI / TestPyPI jobs; ns-pages workflows.
- A CI job _in this repo_ that builds/pushes a product image (proof is YAML + docs; push runs when products call the
  reusable).
- Changing code-quality / check behavior beyond doc cross-links.

## Decisions

1. **Inputs over product-identity vars (A1)**
   - **Choice:** `workflow_call` inputs for `image_base_name`, `components`, DockerHub/GHCR-facing names where needed,
     Helm `chart_dir` / `chart_name`, `version_bump`, `tag_prefix`, `release_type`, `skip` (build/check-style no-op
     where branch protection needs it).
   - **Why:** Matches #11; visible in caller YAML; avoids wrong silent defaults across three repos.
   - **Alternative:** Keep `vars.IMAGE_BASE_NAME` — rejected for identity; optional `vars` only for non-product Git
     identity (`GIT_USER_NAME` / email) if the ported Helm/release steps need them.

2. **Docker release MVP = B1**
   - **Choice:** Push loaded build artifacts to DockerHub + GHCR; optional GitHub release + timestamp-prefixed tag using
     `tag_prefix` (default `docker-v`). Strip PyPI publish jobs from the API template.
   - **Why:** Satisfies image + check pipeline; PyPI is API-only per lock-in.
   - **Alternative:** Full API release 1:1 — rejected (drags PyPI into shared surface).

3. **Version scheme binding (C.1)**
   - **Choice:** Shared build version job keeps API logic: latest `*-docker-vX.Y.Z` → bump; `feature/*` →
     `X.Y.Z-rc.<branch>.<run>` + PEP440 `.devN` output for callers that still build Python artifacts locally.
   - **Why:** One scheme for all three products; docs state the convention.
   - **Alternative:** Per-product tag regex inputs — deferred unless a product cannot adopt.

4. **Helm as reusable `workflow_call` (H1), not only copy of dispatch YAML**
   - **Choice:** Extract reusable Helm workflow(s) (final + pre-release paths, or one workflow with `release_type` /
     branch guards via inputs) with inputs for chart path/name and registries; product keeps a thin `workflow_dispatch`
     caller.
   - **Why:** Same consumption model as Docker reusables; chart layout stays in the product repo.
   - **Alternative:** Only document “copy Helm YAML” — rejected (H1 asks for Devinfra ownership).
   - **Tag scheme:** Keep `*-chart-v*` parallel to Docker `*-docker-v*`; chart `appVersion` still resolves from latest
     Docker tag (existing API behavior).

5. **Single capability / docs home**
   - **Choice:** Extend `reusable-ci-workflows` + `docs/ci.md` rather than a new docs file.
   - **Why:** One CI adoption doc for products.

6. **File naming**
   - **Choice:** `reusable-build.yml`, `reusable-release.yml`, and e.g. `reusable-helm-release.yml` (and
     `reusable-helm-pre-release.yml` if splitting mirrors API clarity better than one parameterized file). Prefer two
     Helm files if final vs pre-release diverge enough to keep readability.
   - **Why:** Predictable `uses:` paths for #13.

## Risks / Trade-offs

- **[Risk] Helm extract misses API-only edge cases** → Mitigation: port from current API YAML; validate with docs + dry
  review against API callers; sync later in #13.
- **[Risk] Products without Docker tags cannot Helm-publish** → Mitigation: keep explicit error (“publish Docker
  first”); document order Docker → Helm.
- **[Risk] Issue #12 body still says Helm product-only** → Mitigation: implement H1; update docs; comment or edit issue
  tasks when applying so Done-when matches.
- **[Trade-off] Larger PR than Docker-only** → Accepted (user **H1**).

## Migration Plan

1. Land reusables + docs on this branch / draft PR (`Fixes #12`).
2. Products keep local copies until #13 points `uses:` at Devinfra refs.
3. Archive change; sync delta into `openspec/specs/reusable-ci-workflows/spec.md`.

## Open Questions

None for MVP (lock-ins closed).

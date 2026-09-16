## Context

See `proposal.md`. Existing release workflows implement tag-first publish and write `## Registry status` into the GitHub
Release body. Build artifacts expire in one day, so Docker retry must rebuild from the release tag. Helm final attaches
a `.tgz` to the Release for later push.

## Goals / Non-Goals

**Goals:**

- Operator-driven retry for an existing Docker (`feature` or `final`) or Helm **final** release
- No new semver / git tag / second Release
- Selective DockerHub / GHCR via boolean inputs
- Update Release `## Registry status` in place
- Share Bake / registry-push **as nested reusable workflows** (not composite actions) so callers stay thin

**Non-Goals:**

- Helm pre-release retry
- Custom “Retry push” button on the GitHub Release page
- Dynamic `workflow_dispatch` choice list of tags
- Product thin callers in this change
- Bit-identical image digests
- Composite actions under `.github/actions/` (rejected — checkout boilerplate cancelled length savings)

## Decisions

1. **One orchestrator** `reusable-registry-retry.yml` with `release_kind: docker | helm`.
2. **Primary input:** `git_tag` (full tag string).
3. **Shared nested reusables** (called via `$/.github/workflows/…` so they resolve to the **same Devinfra commit** as
   the outer reusable when products pin a SHA/branch):
   - `reusable-docker-bake.yml` — checkout + Bake + image artifact
   - `reusable-docker-registry-push.yml` — DockerHub and/or GHCR push from image artifacts
   - `reusable-helm-oci-push.yml` — Helm OCI push from a chart `.tgz` artifact; exposes status outputs
4. **Call sites:** `reusable-build`, `reusable-release`, `reusable-helm-release`, `reusable-helm-pre-release`,
   `reusable-registry-retry`.
5. **Body edit (retry):** replace `## Registry status` through the next `##` heading.
6. **Flags / fail-closed:** at least one of `retry_dockerhub` / `retry_ghcr`; missing DockerHub secrets on explicit
   retry → fail closed.
7. **Helm release split:** package/tag job uploads chart artifact → nested OCI push → GitHub Release job (status from
   push outputs).

## Risks / Trade-offs

- [`$/` requires runner ≥ 2.336] → GitHub-hosted runners; document for self-hosted.
- [Nesting depth / secrets inherit] → Outer must `secrets: inherit` into push reusables.
- [Wrong tag / missing Helm asset] → Fail with clear errors.

## Migration Plan

1. Land nested reusables + wire callers + registry-retry + docs in Devinfra.
2. Products add thin retry callers later (API #443, sql_to_arc #168, harvester #251).

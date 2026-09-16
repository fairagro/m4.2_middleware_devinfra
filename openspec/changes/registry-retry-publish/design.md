## Context

See `proposal.md`. Existing `reusable-release.yml` / `reusable-helm-release.yml` implement tag-first publish and write
`## Registry status` into the GitHub Release body. Helm pre-release has no Release. Build artifacts expire in one day,
so Docker retry must rebuild from the release tag. Helm final attaches a `.tgz` to the Release for later push.

## Goals / Non-Goals

**Goals:**

- Operator-driven retry for an existing Docker (`feature` or `final`) or Helm **final** release
- No new semver / git tag / second Release
- Selective DockerHub / GHCR via boolean inputs
- Update Release `## Registry status` in place
- Document string tag input + listing newest tags (GHA has no dynamic dropdown)

**Non-Goals:**

- Helm pre-release retry
- Custom “Retry push” button on the GitHub Release page (not supported by GitHub)
- Dynamic `workflow_dispatch` choice list of tags
- Product thin callers in this change
- Bit-identical image digests (same commit/tag rebuild is enough)
- Extracting shared push composites from release YAML (optional follow-up if duplication hurts)

## Decisions

1. **One reusable** `reusable-registry-retry.yml` with `release_kind: docker | helm` (not two files in MVP).
2. **Primary input:** `git_tag` (full tag string, e.g. `20260916120000-docker-v1.2.3` or `…-chart-v1.2.3`).
3. **Docker path:** `actions/checkout` at `git_tag` → Bake build (same contract as `reusable-build`) for caller
   `components` → login/push DockerHub and/or GHCR using the same naming as release → `gh release edit` body.
4. **Helm path:** resolve Release for `git_tag` → download `.tgz` asset → `helm push` to selected OCI registries → edit
   Release body. Do not re-bump Chart.yaml / do not create tags.
5. **Body edit:** replace from `## Registry status` through the next `##` heading (exclusive); preserve licenses and
   install docs.
6. **Flags:** `retry_dockerhub` / `retry_ghcr` (at least one must be true).
7. **DockerHub missing secrets:** same as release — skip with status reason when DockerHub selected but secrets absent;
   do not invent credentials.
8. **Failure:** workflow fails if a selected registry push fails (stricter than original soft DockerHub skip on create —
   operator explicitly asked to retry). Missing DockerHub secrets while `retry_dockerhub: true` → fail closed with clear
   message (or skip-with-fail? Prefer fail closed on explicit retry request when secrets missing).

## Risks / Trade-offs

- [Duplicated push YAML vs release] → Accept for MVP; factor composites later if painful.
- [Wrong tag typed] → Docs + fail if tag/Release missing.
- [Helm asset missing] → Fail with clear error (Release must have been created with package).

## Migration Plan

1. Land reusable + docs/spec in Devinfra.
2. Products add thin callers (API #443, sql_to_arc #168, harvester #251).
3. No change to happy-path release workflows required for adopt.

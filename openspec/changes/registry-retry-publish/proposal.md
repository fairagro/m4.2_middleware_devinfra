## Why

Tag-first Docker/Helm releases already create a git tag and GitHub Release when registry push fails or DockerHub is
skipped. Operators need a safe way to re-push to DockerHub and/or GHCR for that **existing** release without bumping
semver or creating a second tag. Docs already call this a follow-up; the reusable path is missing (#34).

## What Changes

- Add `reusable-registry-retry.yml` for an existing release git tag (Docker `feature`/`final` and Helm **final** only).
- Extract shared nested reusables: `reusable-docker-bake.yml`, `reusable-docker-registry-push.yml`,
  `reusable-helm-oci-push.yml` (no composite actions); wire build / Docker release / Helm / retry through `$/` nested
  calls.
- Docker retry: Bake rebuild from tag → selective registry push; no new tag/Release.
- Helm final retry: Release `.tgz` → OCI push; no new chart version/tag.
- Replace Release `## Registry status` with the retry outcome.
- Document in `docs/ci.md`. Product thin callers stay out of this PR.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: registry-retry + nested bake/push reusables; consumer docs

## Impact

- New: `reusable-registry-retry.yml`, `reusable-docker-bake.yml`, `reusable-docker-registry-push.yml`,
  `reusable-helm-oci-push.yml`
- Update: `reusable-build.yml`, `reusable-release.yml`, `reusable-helm-release.yml`, `reusable-helm-pre-release.yml`,
  `docs/ci.md`
- Products later: API #443, sql_to_arc #168, harvester #251

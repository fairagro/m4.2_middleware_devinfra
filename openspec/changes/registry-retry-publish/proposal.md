## Why

Tag-first Docker/Helm releases already create a git tag and GitHub Release when registry push fails or DockerHub is
skipped. Operators need a safe way to re-push to DockerHub and/or GHCR for that **existing** release without bumping
semver or creating a second tag. Docs already call this a follow-up; the reusable path is missing (#34).

## What Changes

- Add a reusable GitHub Actions workflow for **registry retry** against an existing release git tag (Docker
  `feature`/`final` and Helm **final** only).
- Docker: rebuild images from that tag (Bake), then push only selected registries; no new tag/Release create.
- Helm final: push the existing Release `.tgz` asset to selected OCI registries; no new chart version/tag.
- Replace the GitHub Release body’s `## Registry status` section with the retry outcome.
- Document caller contract in `docs/ci.md` (string tag input; how to list newest tags; flags; secrets).
- Product thin `workflow_dispatch` callers stay out of this PR (tracked in product issues).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: add registry-retry reusable contract; extend consumer docs for retry callers

## Impact

- New: `.github/workflows/reusable-registry-retry.yml` (name may vary slightly in design)
- Update: `docs/ci.md`, `openspec/specs/reusable-ci-workflows/spec.md` (via archive sync)
- Products later: API #443, sql_to_arc #168, harvester #251

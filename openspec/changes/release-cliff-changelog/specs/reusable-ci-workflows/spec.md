## ADDED Requirements

### Requirement: Final Release bodies include git-cliff Changelog

When Docker Final (`reusable-release.yml`) or Helm Final (`reusable-helm-release.yml`) creates a GitHub Release, the
hand-built release body MUST include a **`## Changelog`** section whose commit list is produced by **git-cliff** (pinned
fleet version) over commits since the previous surface tag (**R1**: Docker `*-docker-v*` / Helm `*-chart-v*`), using the
shared `cliff.toml` changelog template. The body MUST retain existing operational sections (registry status, install /
build-from-source, Trivy licenses where applicable). Those Final release creations MUST set `generate_release_notes` to
**false** so GitHub’s generic “What’s Changed” dump is not appended. When a previous surface tag exists, the Changelog
section SHOULD include a compare (“Full Changelog”) link from that tag to the new release tag. When cliff produces no
usable changelog text (empty range / no grouped commits), the Release MUST still be creatable (**soft-fail**): the body
MUST include a short placeholder under `## Changelog` and MUST NOT treat emptiness as a hard failure. Real git-cliff
process failures MUST be logged clearly (not silently reported as empty). Documentation in `docs/ci.md` MUST describe
the Changelog section, R1 ranges, soft-fail, and the disabled GitHub auto notes. Pre-release paths that do not create
persisted GitHub Releases are out of scope for this requirement.

#### Scenario: Docker Final Release includes cliff Changelog and no GitHub auto-notes

- **WHEN** `reusable-release.yml` creates a GitHub Release with `skip: false` and `create_github_release: true`
- **THEN** the release body contains a `## Changelog` section derived from git-cliff since the previous Docker surface
  tag (when one exists)
- **AND** existing operational sections (at least registry status) remain in the body
- **AND** `generate_release_notes` is false for that release creation

#### Scenario: Helm Final Release includes cliff Changelog

- **WHEN** `reusable-helm-release.yml` creates a GitHub Release
- **THEN** the release body contains a `## Changelog` section derived from git-cliff since the previous Helm chart
  surface tag (when one exists)
- **AND** `generate_release_notes` is false for that release creation

#### Scenario: Empty changelog soft-fails

- **WHEN** git-cliff succeeds but produces no changelog entries for the surface range
- **THEN** the GitHub Release is still created
- **AND** the body includes a short placeholder under `## Changelog`

#### Scenario: Compare link when previous tag exists

- **WHEN** a previous matching surface tag exists for the Final release being created
- **THEN** the Changelog section includes a repository compare link from that tag to the new release tag

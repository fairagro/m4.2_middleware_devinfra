## ADDED Requirements

### Requirement: Reusable registry-retry workflow

The repository MUST provide `.github/workflows/reusable-registry-retry.yml` callable via `workflow_call` that retries
registry publish for an **existing** Docker or Helm **final** GitHub Release identified by a full git tag input
(`git_tag`). It MUST NOT create a new semver, git tag, or GitHub Release. It MUST accept boolean inputs
`retry_dockerhub` and `retry_ghcr` and MUST require at least one to be true. DockerHub credentials MAY be omitted only
when `retry_dockerhub` is false; when `retry_dockerhub` is true and secrets are missing, the workflow MUST fail closed
with a clear error. GHCR MUST use `GITHUB_TOKEN` with `packages: write` when `retry_ghcr` is true.

For `release_kind: docker` (covering both original `feature` and `final` releases that already have a GitHub Release),
the workflow MUST check out the caller repository at `git_tag`, rebuild component images with the same Bake-based
contract as the shared build workflow (caller `components` / `image_base_name` inputs), and push only to the selected
registries using the same image naming as `reusable-release.yml`.

For `release_kind: helm`, the workflow MUST resolve the GitHub Release for `git_tag`, download the existing chart `.tgz`
Release asset, and `helm push` that package only to the selected OCI registries. It MUST NOT bump Chart.yaml or create
chart tags. Helm **pre-release** retry is out of scope for this requirement.

After successful or partially documented registry attempts, when a GitHub Release exists for `git_tag`, the workflow
MUST update that Release body by **replacing** the existing `## Registry status` section (through the next `##` heading)
with the retry outcome and MUST NOT invent a second top-level registry section. Other Release body sections (e.g.
licenses, install docs) MUST be preserved.

#### Scenario: Docker registry retry rebuilds from tag and pushes

- **WHEN** a product caller invokes the registry-retry reusable with `release_kind: docker`, an existing Docker release
  `git_tag`, `retry_ghcr: true`, and valid component inputs
- **THEN** images are rebuilt from that tag via Bake
- **AND** selected registries receive pushes for those components
- **AND** no new git tag or GitHub Release is created

#### Scenario: Helm final registry retry uses Release asset

- **WHEN** a product caller invokes the registry-retry reusable with `release_kind: helm`, an existing Helm final
  `git_tag`, and at least one registry flag true
- **THEN** the chart `.tgz` is taken from the GitHub Release assets for that tag
- **AND** `helm push` runs only to the selected registries
- **AND** no new chart version or tag is created

#### Scenario: Release body Registry status is replaced

- **WHEN** a registry retry completes against a tag that has a GitHub Release containing `## Registry status`
- **THEN** that section is replaced with the retry’s registry status
- **AND** following body sections remain intact

#### Scenario: Explicit DockerHub retry without secrets fails closed

- **WHEN** `retry_dockerhub` is true and `DOCKERHUB_USER` / `DOCKERHUB_TOKEN` are not available
- **THEN** the workflow fails with a clear error
- **AND** it does not silently skip DockerHub

## MODIFIED Requirements

### Requirement: Consumer call documentation

Documentation in this repository MUST explain how a product PR (or release) workflow calls the reusable code-quality,
check, build, and Docker release workflows with
`uses: fairagro/m4.2_middleware_devinfra/.github/workflows/<file>@<ref>`, which inputs to pass, the artifact contract
between build and check, and that `@main` is acceptable for early adoption while pinning to a tag or commit SHA is
recommended for stability. Documentation MUST include concrete caller snippets for feature-PR and release-style Docker
flows, and for thin Helm `workflow_dispatch` callers that invoke the shared Helm publish reusables. Documentation MUST
state that PyPI and ns-pages workflows remain product-local (API) and are not provided as shared reusables here.
Documentation MUST describe tag-first release identity and that registry push failures/skips are reported in the GitHub
Release body (or Helm pre-release job summary). Documentation MUST also describe the **registry-retry** reusable: full
`git_tag` string input (GitHub Actions has no dynamic tag dropdown; operators list newest tags via Releases UI or
`git tag -l --sort=-creatordate`), `release_kind`, `retry_dockerhub` / `retry_ghcr` flags, that retry does not create
tags, Docker rebuilds from the tag, Helm final uses the Release `.tgz`, and that Helm pre-release retry is out of scope.

#### Scenario: Contributor reads CI docs

- **WHEN** a contributor opens the CI documentation for adopting shared workflows
- **THEN** they learn the `uses:` pattern with branch or tag refs for code-quality, check, build, Docker release, and
  Helm publish
- **AND** they learn required inputs and the build→check artifact contract
- **AND** they learn PyPI and ns-pages stay product-local
- **AND** they learn registry pushes may fail or skip (e.g. missing DockerHub secrets) with status recorded on the
  release
- **AND** they learn how to call the registry-retry reusable for an existing release tag without creating a new tag

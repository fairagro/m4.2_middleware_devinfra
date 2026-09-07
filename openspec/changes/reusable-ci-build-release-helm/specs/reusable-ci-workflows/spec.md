# reusable-ci-workflows Delta

## ADDED Requirements

### Requirement: Reusable build workflow

The repository MUST provide `.github/workflows/reusable-build.yml` callable via `workflow_call`. It MUST calculate a
Docker release version using the shared `*-docker-vX.Y.Z` tag scheme (latest matching tag, then major/minor/patch bump
from an input), emit `version` and `pep440_version` job outputs, and build per-component container images tagged
`local/<image_base_name>-<component>:<version>`. It MUST upload artifacts that satisfy the existing reusable-check
artifact contract (`docker-image-<component>-<version>` containing `docker-image-<component>.tar.gz`, and
`sbom-<component>-<version>` containing `sbom-<component>.spdx.json` when SBOM generation is part of the ported build).
Product-distinguishing names (at least `image_base_name` and `components`) MUST be `workflow_call` inputs, not silent
reliance on caller repository Variables for correct identity. A boolean `skip` input MAY be provided; when true,
required jobs MUST complete successfully via a no-op path where callers need stable check names.

#### Scenario: Build produces check-compatible artifacts

- **WHEN** a product workflow calls the reusable build workflow with `skip: false`, components, and `image_base_name`
- **THEN** the workflow outputs a non-empty `version`
- **AND** uploads Docker image artifacts named per the check contract for each component
- **AND** images inside those archives are tagged `local/<image_base_name>-<component>:<version>`

#### Scenario: Feature branch pre-release version

- **WHEN** the caller runs on a `feature/*` ref and `skip` is false
- **THEN** the emitted Docker `version` follows the shared pre-release pattern derived from the bumped base semver
  (including a run discriminator)
- **AND** `pep440_version` is a PEP 440–compatible form suitable for optional local Python packaging

### Requirement: Reusable Docker release workflow

The repository MUST provide `.github/workflows/reusable-release.yml` callable via `workflow_call`. When not skipped it
MUST consume the build artifact contract, push each component image to DockerHub and GHCR using caller-supplied (or
explicitly defaulted) naming inputs, and MAY create a GitHub release and git tag using a configurable `tag_prefix`
(default `docker-v`) with the repository’s timestamp-prefixed tag pattern. It MUST NOT publish to PyPI or TestPyPI.
Product-distinguishing image and registry namespace values MUST be expressible via `workflow_call` inputs.

#### Scenario: Release pushes images without PyPI

- **WHEN** a product workflow calls the reusable Docker release workflow with version, components, image naming inputs,
  and required registry secrets/token permissions
- **THEN** images are pushed to DockerHub and GHCR for each component
- **AND** no PyPI or TestPyPI publish step runs as part of this workflow

#### Scenario: Optional GitHub release tag

- **WHEN** the caller requests GitHub release creation with `tag_prefix` defaulting to `docker-v`
- **THEN** a release tag consistent with the `*-docker-v*` scheme is created for that version

### Requirement: Reusable Helm publish workflows

The repository MUST provide reusable Helm publish workflow file(s) under `.github/workflows/` callable via
`workflow_call` (final and/or pre-release paths as needed to preserve behavior), adapted from the product Helm chart
release flows. Callers MUST pass chart location and chart name via inputs (`chart_dir`, `chart_name`, and related
naming). The workflows MUST version charts using the shared `*-chart-vX.Y.Z` tag scheme, package the chart from the
**caller** checkout, set chart `appVersion` from the latest Docker release tag when that coupling exists in the source
flows, and push chart packages to DockerHub and GHCR OCI registries. ns-pages publishing MUST remain out of these shared
workflows.

#### Scenario: Helm final publish from product caller

- **WHEN** a product thin caller invokes the reusable Helm final publish workflow with chart inputs and registry
  credentials
- **THEN** a chart package is built from the caller’s chart directory
- **AND** the chart is pushed to the configured DockerHub and GHCR OCI locations
- **AND** a `*-chart-v*` release tag is created according to the shared scheme

#### Scenario: Helm requires prior Docker release tag

- **WHEN** Helm publish needs an app version from Docker tags and no matching `*-docker-v*` tag exists
- **THEN** the workflow fails with a clear error that a Docker release must exist first

## MODIFIED Requirements

### Requirement: Consumer call documentation

Documentation in this repository MUST explain how a product PR (or release) workflow calls the reusable code-quality,
check, build, and Docker release workflows with
`uses: fairagro/m4.2_middleware_devinfra/.github/workflows/<file>@<ref>`, which inputs to pass, the artifact contract
between build and check, and that `@main` is acceptable for early adoption while pinning to a tag or commit SHA is
recommended for stability. Documentation MUST include concrete caller snippets for feature-PR and release-style Docker
flows, and for thin Helm `workflow_dispatch` callers that invoke the shared Helm publish reusables. Documentation MUST
state that PyPI and ns-pages workflows remain product-local (API) and are not provided as shared reusables here.

#### Scenario: Contributor reads CI docs

- **WHEN** a contributor opens the CI documentation for adopting shared workflows
- **THEN** they learn the `uses:` pattern with branch or tag refs for code-quality, check, build, Docker release, and
  Helm publish
- **AND** they learn required inputs and the build→check artifact contract
- **AND** they learn PyPI and ns-pages stay product-local

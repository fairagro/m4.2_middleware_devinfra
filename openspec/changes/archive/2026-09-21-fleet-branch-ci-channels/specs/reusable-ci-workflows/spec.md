## MODIFIED Requirements

### Requirement: Reusable build workflow

The repository MUST provide `.github/workflows/reusable-build.yml` callable via `workflow_call`. It MUST calculate a
Docker release version using the shared `*-docker-vX.Y.Z` tag scheme (latest matching tag, then major/minor/patch bump
from an input), emit `version` and `pep440_version` job outputs, and build per-component container images tagged
`local/<image_base_name>-<component>:<version>`. Building MUST use **Docker Buildx Bake** to compose the synced shared
base Dockerfile (`docker/Dockerfile.product-app.base`) with a **product-local last stage** via Bake `contexts` (export
stage → last stage). It MUST NOT offer a monolith fallback that builds only `docker/Dockerfile.<component>` as a single
file without Bake. It MUST upload artifacts that satisfy the existing reusable-check artifact contract
(`docker-image-<component>-<version>` containing `docker-image-<component>.tar.gz`, and `sbom-<component>-<version>`
containing `sbom-<component>.spdx.json` when SBOM generation is part of the ported build). Product-distinguishing names
(at least `image_base_name` and `components`) MUST be `workflow_call` inputs, not silent reliance on caller repository
Variables for correct identity. A boolean `skip` input MAY be provided; when true, required jobs MUST complete
successfully via a no-op path where callers need stable check names.

When `skip` is false and the caller ref name matches `build/*`, the emitted Docker `version` MUST use the shared
pre-release pattern derived from the bumped base semver (including a branch label and run discriminator), and
`pep440_version` MUST be a PEP 440–compatible form suitable for optional local Python packaging. Refs that do **not**
match `build/*` (including historical `feature/*`) MUST NOT receive that pre-release suffix from this workflow.

#### Scenario: Build produces check-compatible artifacts

- **WHEN** a product workflow calls the reusable build workflow with `skip: false`, components, and `image_base_name`
- **THEN** the workflow outputs a non-empty `version`
- **AND** uploads Docker image artifacts named per the check contract for each component
- **AND** images inside those archives are tagged `local/<image_base_name>-<component>:<version>`

#### Scenario: Feature branch pre-release version

- **WHEN** the caller runs on a `build/*` ref and `skip` is false
- **THEN** the emitted Docker `version` follows the shared pre-release pattern derived from the bumped base semver
  (including a run discriminator)
- **AND** `pep440_version` is a PEP 440–compatible form suitable for optional local Python packaging

#### Scenario: Non-build refs are not RC-suffixed

- **WHEN** the caller runs on a ref that is not `build/*` (for example `feature/*`, `ci/*`, or `issue-*`) and `skip` is
  false
- **THEN** the emitted Docker `version` is the bumped base semver without the shared pre-release suffix

#### Scenario: Build uses Bake with base and last stage

- **WHEN** a product workflow calls the reusable build workflow with `skip: false`
- **THEN** each component image is produced via Buildx Bake using the shared base and a product-local last stage
- **AND** the workflow does not fall back to building a single monolith `docker/Dockerfile.<component>` without Bake

### Requirement: Reusable Helm publish workflows

The repository MUST provide reusable Helm publish workflow file(s) under `.github/workflows/` callable via
`workflow_call` (final and/or pre-release paths as needed to preserve behavior), adapted from the product Helm chart
release flows. Callers MUST pass chart location and chart name via inputs (`chart_dir`, `chart_name`, and related
naming). The workflows MUST version charts using the shared `*-chart-vX.Y.Z` tag scheme, package the chart from the
**caller** checkout, set chart `appVersion` from the latest Docker release tag when that coupling exists in the source
flows, and attempt to push chart packages to DockerHub and GHCR OCI registries. DockerHub credentials MAY be omitted.
When a registry push is skipped or fails, final Helm GitHub Releases MUST document registry status and reason in the
release body; pre-release flows MUST surface the same information in the job summary. ns-pages publishing MUST remain
out of these shared workflows.

Helm **pre-release** MUST emit chart versions with the shared `…-rc.<branch>.<run>` pattern and MUST fail closed unless
the caller ref matches `build/*` (hard cut — not `feature/*`).

#### Scenario: Helm final publish from product caller

- **WHEN** a product thin caller invokes the reusable Helm final publish workflow with chart inputs and registry
  credentials
- **THEN** a chart package is built from the caller’s chart directory
- **AND** a `*-chart-v*` release tag is created according to the shared scheme
- **AND** successful registry pushes publish the chart to the corresponding OCI locations

#### Scenario: Helm requires prior Docker release tag

- **WHEN** Helm publish needs an app version from Docker tags and no matching `*-docker-v*` tag exists
- **THEN** the workflow fails with a clear error that a Docker release must exist first

#### Scenario: Helm release documents skipped DockerHub

- **WHEN** DockerHub secrets are not provided to the Helm final publish workflow
- **THEN** the GitHub Release body states that DockerHub publish was skipped and why

#### Scenario: Helm pre-release requires build channel

- **WHEN** a product caller invokes Helm pre-release on a ref that is not `build/*`
- **THEN** the workflow fails with a clear error naming the `build/*` requirement

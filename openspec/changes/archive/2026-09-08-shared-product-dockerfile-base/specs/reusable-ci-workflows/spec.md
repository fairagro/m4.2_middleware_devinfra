# reusable-ci-workflows Specification (delta)

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

#### Scenario: Build uses Bake with base and last stage

- **WHEN** a product workflow calls the reusable build workflow with `skip: false`
- **THEN** each component image is produced via Buildx Bake using the shared base and a product-local last stage
- **AND** the workflow does not fall back to building a single monolith `docker/Dockerfile.<component>` without Bake

### Requirement: Reusable Docker release workflow

The repository MUST provide `.github/workflows/reusable-release.yml` callable via `workflow_call`. When not skipped and
`create_github_release` is true it MUST create the git release tag (and optional GitHub Release) using a configurable
`tag_prefix` (default `docker-v`) with the repository’s timestamp-prefixed tag pattern **before or independently of**
requiring successful registry pushes (tag-first). When `create_github_release` is false it MUST NOT create a git tag or
GitHub Release, but MAY still attempt registry pushes. It MUST attempt to push each component image to DockerHub and
GHCR using caller-supplied (or explicitly defaulted) naming inputs. DockerHub credentials MAY be omitted; when omitted
the DockerHub push MUST be skipped without failing the overall release identity. When a registry push is skipped or
fails, and a GitHub Release is created, the release body MUST include an explicit registry-status section stating the
outcome and reason (including missing secrets). It MUST NOT publish to PyPI or TestPyPI. Product-distinguishing image
and registry namespace values MUST be expressible via `workflow_call` inputs. Documented “build from source”
instructions in release bodies (and any step that rebuilds component images) MUST use the same Buildx Bake base +
last-stage contract as `reusable-build.yml` (no monolith `docker build -f docker/Dockerfile.<component>`-only path).

#### Scenario: Release pushes images without PyPI

- **WHEN** a product workflow calls the reusable Docker release workflow with version, components, image naming inputs,
  and DockerHub secrets provided
- **THEN** images are pushed to DockerHub and GHCR for each component when those pushes succeed
- **AND** no PyPI or TestPyPI publish step runs as part of this workflow

#### Scenario: Optional GitHub release tag

- **WHEN** the caller sets `create_github_release: true` with `tag_prefix` defaulting to `docker-v`
- **THEN** a release tag consistent with the `*-docker-v*` scheme is created for that version even if a registry push
  later fails

#### Scenario: Image push without tag when release disabled

- **WHEN** the caller sets `create_github_release: false` and `skip: false`
- **THEN** the workflow does not create a git tag or GitHub Release
- **AND** it may still attempt DockerHub/GHCR image pushes

#### Scenario: Release body documents failed or skipped registry push

- **WHEN** DockerHub secrets are missing or a registry push fails and a GitHub Release is created
- **THEN** the release body states which registry was skipped or failed and why

#### Scenario: Release docs use Bake for build-from-source

- **WHEN** a GitHub Release body includes build-from-source instructions for a component image
- **THEN** those instructions use Buildx Bake with shared base + product-local last stage
- **AND** they do not prescribe a monolith `docker build -f docker/Dockerfile.<component>`-only command

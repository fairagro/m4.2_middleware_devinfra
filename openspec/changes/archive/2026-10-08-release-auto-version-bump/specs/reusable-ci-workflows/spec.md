## ADDED Requirements

### Requirement: Auto version_bump via Conventional Commits (git-cliff)

Shared release version calculation MUST accept `version_bump` values `auto`, `major`, `minor`, and `patch`, and MUST
default to **`auto`**. When `version_bump` is `auto`, the workflow MUST derive the next **base** semver using
**git-cliff** (pinned fleet version) from Conventional Commits since the last tag matching the surface’s tag scheme
(**R1**): Docker build/release uses the shared `*-docker-v*` (or configured Docker tag) pattern; Helm final / Helm
pre-release base bump uses the Helm chart version tag scheme for that reusable. Explicit `major` / `minor` / `patch`
MUST keep today’s manual bump behaviour. On `build/*`, after the base version is determined (auto or manual), the
workflow MUST still apply the existing pre-release / PEP 440 suffix rules (**S2**). When `auto` cannot determine a bump
(missing cliff, no usable tag/history, or cliff error), the job MUST **fail closed** with a clear error naming the
failure (**F1**) and MUST NOT silently default to `patch`. Documentation in `docs/ci.md` MUST describe `auto`, the
Conventional Commits mapping, R1 tag ranges, and the override path.

#### Scenario: Auto default bumps from Conventional Commits on Docker build

- **WHEN** a caller invokes `reusable-build.yml` with `skip: false` and `version_bump` left at default `auto`
- **AND** git-cliff can compute a next base version from commits since the latest matching Docker version tag
- **THEN** the emitted base semver matches that cliff result before any `build/*` RC suffix is applied

#### Scenario: Explicit bump still overrides auto

- **WHEN** a caller sets `version_bump` to `major`, `minor`, or `patch`
- **THEN** the workflow applies that manual bump against the latest matching tag
- **AND** it does not require git-cliff success for that path

#### Scenario: Auto fails closed

- **WHEN** `version_bump` is `auto` and git-cliff cannot produce a next base version
- **THEN** the version job fails with a clear error
- **AND** it does not emit a silently patched version

#### Scenario: Pre-release keeps RC suffix after auto base

- **WHEN** the caller runs on `build/*` with `version_bump: auto` and cliff returns a base semver
- **THEN** the emitted Docker `version` still uses the shared pre-release pattern derived from that base
- **AND** `pep440_version` remains a PEP 440–compatible form

#### Scenario: Helm auto uses Helm tag range

- **WHEN** a Helm final or Helm pre-release reusable resolves `version_bump: auto`
- **THEN** git-cliff uses the Helm chart tag scheme for that surface (not the Docker `*-docker-v*` range)
- **AND** fail-closed behaviour matches the Docker auto path

## MODIFIED Requirements

### Requirement: Reusable build workflow

The repository MUST provide `.github/workflows/reusable-build.yml` callable via `workflow_call`. It MUST calculate a
Docker release version using the shared `*-docker-vX.Y.Z` tag scheme (latest matching tag, then major/minor/patch bump
from an input, or **`auto`** via the shared Conventional Commits / git-cliff path defined in **Auto version_bump via
Conventional Commits (git-cliff)**), emit `version` and `pep440_version` job outputs, and build per-component container
images tagged `local/<image_base_name>-<component>:<version>`. Building MUST use **Docker Buildx Bake** to compose the
synced shared base Dockerfile (`docker/Dockerfile.product-app.base`) with a **product-local last stage** via Bake
`contexts` (export stage → last stage). It MUST NOT offer a monolith fallback that builds only
`docker/Dockerfile.<component>` as a single file without Bake. It MUST upload artifacts that satisfy the existing
reusable-check artifact contract (`docker-image-<component>-<version>` containing `docker-image-<component>.tar.gz`, and
`sbom-<component>-<version>` containing `sbom-<component>.spdx.json` when SBOM generation is part of the ported build).
Product-distinguishing names (at least `image_base_name` and `components`) MUST be `workflow_call` inputs, not silent
reliance on caller repository Variables for correct identity. A boolean `skip` input MAY be provided; when true,
required jobs MUST complete successfully via a no-op path where callers need stable check names. The `version_bump`
input MUST accept `auto`, `major`, `minor`, and `patch`, and MUST default to **`auto`**.

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

#### Scenario: Default version_bump is auto

- **WHEN** a caller omits `version_bump` on `reusable-build.yml`
- **THEN** the effective value is `auto`

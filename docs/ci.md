# Reusable CI workflows

Canonical GitHub Actions for the three m4.2 product repos live in this repository:

| Workflow            | Path                                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| Code quality        | [`.github/workflows/reusable-code-quality.yml`](../.github/workflows/reusable-code-quality.yml)         |
| Image / SBOM checks | [`.github/workflows/reusable-check.yml`](../.github/workflows/reusable-check.yml)                       |
| Docker build        | [`.github/workflows/reusable-build.yml`](../.github/workflows/reusable-build.yml)                       |
| Docker release      | [`.github/workflows/reusable-release.yml`](../.github/workflows/reusable-release.yml)                   |
| Helm final release  | [`.github/workflows/reusable-helm-release.yml`](../.github/workflows/reusable-helm-release.yml)         |
| Helm pre-release    | [`.github/workflows/reusable-helm-pre-release.yml`](../.github/workflows/reusable-helm-pre-release.yml) |

**Stay product-local (not shared here):** PyPI / TestPyPI publish jobs and ns-pages workflows (API today).

Product-distinguishing names use **`workflow_call` inputs** (e.g. `image_base_name`, `chart_dir`) — do not rely on
silent repository Variables for correct identity.

## Calling from a product repo

Replace `@main` with a **tag** or **commit SHA** once you want a frozen contract. `@main` is fine for early adoption
while this repo’s CI surface is still moving.

The reusable workflows check out the **caller** repository (not Devinfra), so `versions.env`, `.python-version`,
`scripts/load-versions-env.sh`, Dockerfiles under `docker/Dockerfile.<component>`, and Helm charts must exist in the
product repo. Callers that sync `versions.env` MUST also sync `scripts/load-versions-env.sh`.

### Feature PR (Docker build + check)

```yaml
jobs:
  code-quality:
    needs: [detect-changes]
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-code-quality.yml@main
    with:
      python_package_root: middleware
      components: '["api"]'
      skip: ${{ needs.detect-changes.outputs.code != 'true' }}
    secrets: inherit

  build:
    needs: [detect-changes]
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-build.yml@main
    with:
      components: '["api"]'
      image_base_name: fairagro-advanced-middleware
      skip: ${{ needs.detect-changes.outputs.code != 'true' }}
    secrets: inherit

  check:
    needs: [detect-changes, build]
    if: always() && needs.detect-changes.result == 'success'
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-check.yml@main
    with:
      version: ${{ needs.build.outputs.version }}
      components: '["api"]'
      image_base_name: fairagro-advanced-middleware
      skip: ${{ needs.detect-changes.outputs.code != 'true' || needs.build.result != 'success' }}
    secrets: inherit
```

### Release / pre-release (Docker)

```yaml
jobs:
  build:
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-build.yml@main
    with:
      version_bump: ${{ inputs.version_bump }}
      components: '["api"]'
      image_base_name: fairagro-advanced-middleware
    secrets: inherit

  check:
    needs: [build]
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-check.yml@main
    with:
      version: ${{ needs.build.outputs.version }}
      components: '["api"]'
      image_base_name: fairagro-advanced-middleware
    secrets: inherit

  release:
    needs: [build, check]
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-release.yml@main
    with:
      version: ${{ needs.build.outputs.version }}
      pep440_version: ${{ needs.build.outputs.pep440_version }}
      components: '["api"]'
      image_base_name: fairagro-advanced-middleware
      dockerhub_namespace: zalf
      ghcr_namespace: fairagro
      release_type: final # or feature
      tag_prefix: docker-v
      create_github_release: true
    secrets: inherit
```

Keep any **PyPI** publish steps in a product-local job or workflow after build (API only).

### Helm (thin `workflow_dispatch` caller)

```yaml
name: Helm Chart Release
on:
  workflow_dispatch:
    inputs:
      version_bump:
        type: choice
        options: [major, minor, patch]
        default: patch

jobs:
  helm:
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-helm-release.yml@main
    with:
      version_bump: ${{ inputs.version_bump }}
      chart_dir: helmchart/fairagro-advanced-middleware-api-chart
      chart_name: fairagro-advanced-middleware-api-chart
      dockerhub_namespace: zalf
      require_main: true
    secrets: inherit
```

Pre-release:

```yaml
jobs:
  helm:
    uses: fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-helm-pre-release.yml@main
    with:
      chart_dir: helmchart/fairagro-advanced-middleware-api-chart
      chart_name: fairagro-advanced-middleware-api-chart
      dockerhub_namespace: zalf
    secrets: inherit
```

Order: publish a **Docker** release (so a `*-docker-v*` tag exists) before Helm final/pre-release. Helm sets chart
`appVersion` from the latest Docker tag.

## Inputs

### `reusable-code-quality.yml`

| Input                 | Default      | Purpose                                                    |
| --------------------- | ------------ | ---------------------------------------------------------- |
| `python_package_root` | `middleware` | Path for ruff / pylint / mypy / bandit / pytest            |
| `components`          | `["api"]`    | Accepted for caller compatibility; unused by this workflow |
| `skip`                | `false`      | Successful no-op (keeps required check names green)        |

Python version comes from the caller’s `versions.env` (`PYTHON_VERSION`) plus matching `.python-version` — there is no
version override input.

The job display name stays **`Code Quality Check (3.12)`** for existing branch rulesets.

### `reusable-check.yml`

| Input             | Default                        | Purpose                                                            |
| ----------------- | ------------------------------ | ------------------------------------------------------------------ |
| `version`         | `""`                           | Build version string (required when `skip` is false)               |
| `components`      | `["api"]`                      | JSON array; matrix over components                                 |
| `image_base_name` | `fairagro-advanced-middleware` | Prefix for `local/<name>-<component>:<version>`                    |
| `skip`            | `false`                        | Successful no-op on all check jobs (keeps required statuses green) |

### `reusable-build.yml`

| Input             | Default                        | Purpose                                            |
| ----------------- | ------------------------------ | -------------------------------------------------- |
| `version_bump`    | `patch`                        | major / minor / patch against latest `*-docker-v*` |
| `components`      | `["api"]`                      | JSON array; matrix build                           |
| `image_base_name` | `fairagro-advanced-middleware` | Local image tag prefix                             |
| `skip`            | `false`                        | Successful no-op without artifacts                 |

Outputs: `version`, `pep440_version`, `components`. Version scheme is shared across all three products
(`*-docker-vX.Y.Z`; on `feature/*` → `X.Y.Z-rc.<branch>.<run>`).

### `reusable-release.yml`

| Input                   | Default                        | Purpose                                     |
| ----------------------- | ------------------------------ | ------------------------------------------- |
| `version`               | (required)                     | From build                                  |
| `pep440_version`        | `""`                           | Caller compatibility; unused (no PyPI here) |
| `components`            | `["api"]`                      | Matrix push                                 |
| `image_base_name`       | `fairagro-advanced-middleware` | Must match build                            |
| `dockerhub_namespace`   | `zalf`                         | Docker Hub org/user                         |
| `ghcr_namespace`        | `""` → `repository_owner`      | GHCR namespace; empty uses owner            |
| `release_type`          | (required)                     | `feature` or `final` (prerelease flag)      |
| `create_github_release` | `true`                         | Draft→publish GitHub release + tag          |
| `tag_prefix`            | `docker-v`                     | Tag shape `{timestamp}-{prefix}{version}`   |
| `skip`                  | `false`                        | Successful no-op                            |

Secrets: `DOCKERHUB_USER`, `DOCKERHUB_TOKEN` (optional — if missing, DockerHub push is skipped and the GitHub Release
body states why). GHCR uses `GITHUB_TOKEN` (`packages: write` on the reusable job). Git tags / GitHub Releases are
created even when a registry push fails; the release body includes a **Registry status** section. Re-pushing an existing
release is a follow-up (retry workflow).

GHCR image tag shape: `ghcr.io/<ghcr_namespace>/<image_base_name>-<component>:<version>` (aligned with DockerHub
naming).

When `create_github_release` is false, no git tag or GitHub Release is created (image pushes still run).

### `reusable-helm-release.yml` / `reusable-helm-pre-release.yml`

| Input                   | Default               | Purpose                                      |
| ----------------------- | --------------------- | -------------------------------------------- |
| `chart_dir`             | (required)            | Chart path in caller checkout                |
| `chart_name`            | (required)            | Must match `name:` in Chart.yaml (validated) |
| `dockerhub_namespace`   | `zalf`                | Docker Hub OCI namespace                     |
| `version_bump`          | `patch`               | Final release only                           |
| `require_main`          | `true`                | Final release only                           |
| `create_github_release` | `true`                | Final release only                           |
| `helm_install_name`     | `fairagro-middleware` | Example name in release notes (final only)   |

Helm CLI version comes from the caller’s `versions.env` (`HELM_VERSION`). Secrets `DOCKERHUB_USER` / `DOCKERHUB_TOKEN`
are optional; if missing or a push fails, the Helm GitHub Release body (final) or job summary (pre-release) MUST state
the registry status and reason. GHCR uses `GITHUB_TOKEN`. Chart tags are created before registry pushes (same tag-first
policy as Docker release).

## Check artifact contract

A prior **build** job in the same workflow run must upload:

| Artifact name                        | Expected file inside              |
| ------------------------------------ | --------------------------------- |
| `docker-image-<component>-<version>` | `docker-image-<component>.tar.gz` |
| `sbom-<component>-<version>`         | `sbom-<component>.spdx.json`      |

The build must save the image into that archive **already tagged** as:

`local/<image_base_name>-<component>:<version>`

After `docker load`, the reusable checks reference that same tag (they do not retag).

Container structure tests load:

`docker/container-structure-tests/<component>.yaml` from the **caller** checkout.

## Permissions

Callers that upload SARIF need `security-events: write` on the top-level workflow (or inherit permissions that allow the
reusable security job). Prefer `secrets: inherit` when product secrets are required by nested steps. Docker/Helm pushes
need DockerHub secrets on the caller and `packages: write` for GHCR where applicable.

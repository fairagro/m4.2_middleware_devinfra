# Reusable CI workflows

Canonical GitHub Actions for the three m4.2 product repos live in this repository:

| Workflow            | Path                                                                                            |
| ------------------- | ----------------------------------------------------------------------------------------------- |
| Code quality        | [`.github/workflows/reusable-code-quality.yml`](../.github/workflows/reusable-code-quality.yml) |
| Image / SBOM checks | [`.github/workflows/reusable-check.yml`](../.github/workflows/reusable-check.yml)               |

Shared **build** and **release** reusables are **out of scope** for issue #11 (see epic follow-ups / “Next” on that
issue). Until those land, products keep a local (or later shared) build workflow that uploads the artifacts described
below.

## Calling from a product repo

In the product workflow (e.g. `feature-pull-request.yml`):

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

Replace `@main` with a **tag** or **commit SHA** once you want a frozen contract. `@main` is fine for early adoption
while this repo’s CI surface is still moving.

The reusable workflows check out the **caller** repository (not Devinfra), so `versions.env`, `.python-version`,
`scripts/load-versions-env.sh`, `pyproject.toml`, `.bandit`, the package root (default `middleware/`), and Docker CST
configs must exist in the product repo.

## Inputs

### `reusable-code-quality.yml`

| Input                 | Default      | Purpose                                                    |
| --------------------- | ------------ | ---------------------------------------------------------- |
| `python_package_root` | `middleware` | Path for ruff / pylint / mypy / bandit / pytest            |
| `components`          | `["api"]`    | Accepted for caller compatibility; unused by this workflow |
| `skip`                | `false`      | Successful no-op (keeps required check names green)        |

Python version comes from the caller’s `versions.env` (`PYTHON_VERSION`) plus matching `.python-version` — there is no
version override input. Callers MUST ship `scripts/load-versions-env.sh` together with `versions.env` (same sync set).

The job display name stays **`Code Quality Check (3.12)`** for existing branch rulesets.

### `reusable-check.yml`

| Input             | Default                        | Purpose                                                            |
| ----------------- | ------------------------------ | ------------------------------------------------------------------ |
| `version`         | `""`                           | Build version string (required when `skip` is false)               |
| `components`      | `["api"]`                      | JSON array; matrix over components                                 |
| `image_base_name` | `fairagro-advanced-middleware` | Prefix for `local/<name>-<component>:<version>`                    |
| `skip`            | `false`                        | Successful no-op on all check jobs (keeps required statuses green) |

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
reusable security job). Prefer `secrets: inherit` when product secrets are required by nested steps.

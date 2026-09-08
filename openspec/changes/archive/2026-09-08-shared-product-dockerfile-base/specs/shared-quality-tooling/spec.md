# shared-quality-tooling Specification (delta)

## MODIFIED Requirements

### Requirement: Container-structure-test runner script

The repository MUST provide `scripts/run-container-structure-test.sh` that builds a Docker image via **Buildx Bake** and
runs `container-structure-test` against it. It MUST NOT fall back to a monolith `docker build -f` path. Bake target,
Bake file, image tag, and test definition paths MUST be configurable (arguments and/or environment variables) so product
repos can keep local values. When `CST_BAKE_TARGET` is unset and the checkout has **no product CST layout** — either no
`docker/` directory, or `docker/` without a `docker/container-structure-tests/` directory (e.g. shared Devinfra that
only ships `docker/Dockerfile.product-app.base` and examples) — the script MUST exit successfully with a clear skip
warning rather than failing the pre-push quality stage. Product repos that ship `docker/container-structure-tests/` MUST
require a Bake target / file and MUST still fail hard when those paths are wrong.

#### Scenario: Runner uses product parameters

- **WHEN** the script is invoked with product-specific Bake target, tag, and test paths
- **THEN** it builds that image via Bake and runs container-structure-test with those tests
- **AND** it does not hardcode another product’s paths as the only option
- **AND** it does not use monolith `docker build -f` as a fallback

#### Scenario: Devinfra without product CST layout skips

- **WHEN** the script runs without `CST_BAKE_TARGET`
- **AND** the repository has no `docker/` directory, **or** has `docker/` but no `docker/container-structure-tests/`
- **THEN** the script prints a skip warning and exits 0
- **AND** it does not attempt `docker buildx bake`

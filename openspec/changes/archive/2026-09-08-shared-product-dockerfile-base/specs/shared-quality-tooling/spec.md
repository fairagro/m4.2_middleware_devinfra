# shared-quality-tooling Specification (delta)

## MODIFIED Requirements

### Requirement: Container-structure-test runner script

The repository MUST provide `scripts/run-container-structure-test.sh` that builds a Docker image and runs
`container-structure-test` against it. Dockerfile path, image tag, and test definition paths MUST be configurable
(arguments and/or environment variables) so product repos can keep local values. When the configured Dockerfile path is
missing and the checkout has **no product CST layout** — either no `docker/` directory, or `docker/` without both a
default `docker/Dockerfile` and a `docker/container-structure-tests/` directory (e.g. shared Devinfra that only ships
`docker/Dockerfile.product-app.base` and examples) — the script MUST exit successfully with a clear skip warning rather
than failing the pre-push quality stage. Product repos that ship a product `docker/` layout MUST still fail hard when
the configured Dockerfile path is wrong.

#### Scenario: Runner uses product parameters

- **WHEN** the script is invoked with product-specific Dockerfile, tag, and test paths
- **THEN** it builds that image and runs container-structure-test with those tests
- **AND** it does not hardcode another product’s paths as the only option

#### Scenario: Devinfra without product CST layout skips

- **WHEN** the script runs with the default Dockerfile path and that file is missing
- **AND** the repository has no `docker/` directory, **or** has `docker/` but neither `docker/Dockerfile` nor
  `docker/container-structure-tests/`
- **THEN** the script prints a skip warning and exits 0
- **AND** it does not attempt `docker build`

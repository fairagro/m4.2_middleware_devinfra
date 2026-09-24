## ADDED Requirements

### Requirement: Quality CLI loads product path overlays when unset

`scripts/run-quality-cli.sh` (or a helper it sources) MUST, on each invoke, attempt to load `MYPYPATH` and
`PYLINT_SOURCE_ROOTS` from `.devcontainer/product.env` when those variables are unset or empty in the process
environment, using the same allowed-key parse as reusable CI. Non-empty existing env MUST NOT be overwritten. A missing
file MUST soft-skip. This MUST apply so commit-stage mypy/pylint see path-file edits without requiring a Dev Container
rebuild solely to refresh Compose `env_file`.

#### Scenario: Unset MYPYPATH filled from product.env

- **WHEN** `run-quality-cli.sh mypy …` runs with `MYPYPATH` unset and `.devcontainer/product.env` defines `MYPYPATH=a:b`
- **THEN** the mypy process sees `MYPYPATH=a:b`

#### Scenario: Existing MYPYPATH wins

- **WHEN** `MYPYPATH` is already set non-empty in the environment and the file defines a different value
- **THEN** the runner leaves the process value unchanged

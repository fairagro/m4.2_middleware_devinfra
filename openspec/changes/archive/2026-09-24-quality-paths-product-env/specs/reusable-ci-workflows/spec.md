## ADDED Requirements

### Requirement: Code-quality path overlays from product env file

The reusable code-quality workflow MUST accept optional `mypy_path` and `pylint_source_roots` inputs as today. When
`mypy_path` is empty, the workflow MUST attempt to set `MYPYPATH` from `MYPYPATH=` in a product-owned env file (default
`.devcontainer/product.env`, overridable by an optional `quality_env_file` input). When `pylint_source_roots` is empty,
it MUST attempt to set pylint `--source-roots` from `PYLINT_SOURCE_ROOTS=` in the same file. Non-empty workflow inputs
MUST override the file. A missing file or missing key MUST soft-skip (same as empty inputs today). The workflow MUST NOT
require products to duplicate path literals in caller `with:` when the file is populated.

#### Scenario: Empty mypy_path loads MYPYPATH from product.env

- **WHEN** a caller omits `mypy_path` (or passes empty) and `.devcontainer/product.env` contains `MYPYPATH=a:b`
- **THEN** the mypy step runs with `MYPYPATH` equal to `a:b`

#### Scenario: Explicit mypy_path overrides file

- **WHEN** a caller passes a non-empty `mypy_path` and the env file also defines `MYPYPATH`
- **THEN** the workflow uses the input value, not the file

#### Scenario: Missing product.env is soft

- **WHEN** the env file is absent and path inputs are empty
- **THEN** the workflow still succeeds at the path-overlay step (mypy/pylint use defaults)

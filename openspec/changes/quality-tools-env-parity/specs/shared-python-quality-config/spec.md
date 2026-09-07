# shared-python-quality-config Delta

## ADDED Requirements

### Requirement: Fragment config is the only policy surface

Shared Ruff, Mypy, and Pylint fragment files MUST carry the full shared policy for those tools. Shared and product
invocations (IDE, pre-commit / pre-push, GitHub quality workflows, `quality-check.sh`) MUST NOT pass command-line or IDE
settings that restate fragment-expressible policy. Allowed extras are limited to: `--config` / `--config-file` /
`--rcfile` (or IDE equivalent pointing at the fragment), target paths such as `middleware/`, and documented
product-local path overlays (`MYPYPATH`, pylint `--source-roots`, and equivalents) that MUST NOT be edited into synced
fragments.

#### Scenario: Mypy invocation stays minimal

- **WHEN** shared hooks, CI, or docs show a Mypy command for product `middleware/`
- **THEN** the command uses `--config-file mypy.ini` (or auto-discovery of that fragment) plus target paths
- **AND** it does not add CLI flags that duplicate settings already present in `mypy.ini`

## ADDED Requirements

### Requirement: Shared vulture unused-code gate

The repository MUST provide a fleet **vulture** unused-code gate for product `middleware/` trees. Invocations (commit-
stage pre-commit and reusable code-quality CI) MUST use the same fail policy: minimum confidence **100** and **no**
synced vulture whitelist / ignore fragment. Policy MUST live in the shared hook and CI entries (same args), not in a
product-local `pyproject` `[tool.vulture]` table that sync would overwrite inconsistently.

Documentation MUST state that false positives at confidence 100 are handled in product code (`# noqa` / delete / use
the symbol), not by expanding a Devinfra whitelist file in this change. Dynamic attributes, `__all__`, and pytest
fixtures that still fail at 100 MUST be fixed or noqa’d in the product — not by lowering fleet confidence in a
one-off product fork of the synced pre-commit blob.

#### Scenario: Vulture gate uses confidence 100 without whitelist file

- **WHEN** a consumer inspects the shared vulture pre-commit entry and the reusable code-quality vulture step
- **THEN** both invoke vulture against `middleware/` (or the documented package root input) with minimum confidence 100
- **AND** neither depends on a synced vulture whitelist file for the fail policy

#### Scenario: Docs describe FP handling without a fleet whitelist

- **WHEN** a contributor reads quality docs for vulture
- **THEN** they learn confidence 100 and no synced whitelist
- **AND** they learn to fix or `# noqa` in product code rather than patching synced hook YAML after sync

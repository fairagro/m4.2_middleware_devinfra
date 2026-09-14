## ADDED Requirements

### Requirement: Skill documents shared stubs instead of import-untyped for arctrl and fable

The canonical `.agents/skills/arctrl/SKILL.md` MUST document that type checking for `arctrl` and `fable_library` uses
the shared incomplete stubs under `stubs/` (synced from Devinfra) with `MYPYPATH` / `stubPath`, and MUST NOT present
project-level `[[tool.mypy.overrides]]` `ignore_missing_imports` or “always add `# type: ignore[import-untyped]`” as the
fleet default for those packages. Example imports in the skill SHOULD omit import-untyped ignores for arctrl and
fable_library when illustrating the happy path after stubs sync. The skill MAY still note that other one-off untyped
libraries can use per-import ignores when no shared stub exists.

#### Scenario: Skill package section points at stubs

- **WHEN** an agent or contributor reads the Package & Imports section of the arctrl skill
- **THEN** they learn shared `stubs/arctrl` and `stubs/fable_library` are the preferred silence mechanism
- **AND** they are not directed to patch synced `mypy.ini` or keep arctrl/fable import-untyped ignores as the default

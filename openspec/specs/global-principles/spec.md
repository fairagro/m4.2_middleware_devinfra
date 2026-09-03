# global-principles Specification

## Purpose

Defines the shared OpenSpec principles base file and the repo-local extension pattern so product repos can specialize
without forking Supported environment or Type Safety rules.

## Requirements

### Requirement: Shared principles.global.md exists

The repository MUST provide `openspec/principles.global.md` as the canonical shared engineering foundation for m4.2
middleware consumers. That file MUST include at least: shared values, Supported development environment, Type Safety
core rules, shared code-quality expectations (`uv` and the standard lint/type/security gates), and the rule that
application code must not read configuration via direct `os.environ` (configuration goes through the project's config
wrapper pattern). Product-only technology stacks, module graphs, and scaling notes MUST NOT be normative content of
`principles.global.md`.

#### Scenario: Agent looks up supported environment

- **WHEN** an agent or reviewer needs the supported development environment rule
- **THEN** it is defined in `openspec/principles.global.md`
- **AND** the file does not require FastAPI, Celery, or CouchDB as shared stack

### Requirement: Repo-local principles.md extends global

The repository MUST provide `openspec/principles.md` that points at `openspec/principles.global.md` and MAY add
Devinfra- or product-specific constraints. Repo-local `principles.md` MUST NOT redefine or weaken Supported development
environment or Type Safety rules that live in `principles.global.md`. Consumers of the shared stack MUST use the same
two-file pattern: synced `principles.global.md` plus a local `principles.md` that references it.

#### Scenario: Local principles stay additive

- **WHEN** a product repo adds stack- or module-specific rules in `openspec/principles.md`
- **THEN** that file still references `openspec/principles.global.md`
- **AND** Type Safety and Supported development environment remain owned by the global file

### Requirement: Direct citation of the global file

Shared agent and review documents in this repository that need Supported development environment or Type Safety MUST
cite `openspec/principles.global.md` directly.

#### Scenario: Shared docs cite the global path

- **WHEN** a shared review or agent document in this repo needs those constraints
- **THEN** it links or names `openspec/principles.global.md`
- **AND** it does not rely solely on a local `principles.md` indirection for those sections

### Requirement: README documents principles ownership

The root `README.md` MUST mention `openspec/principles.global.md` as shared (consumers must not diverge) and
`openspec/principles.md` as the local extension point.

#### Scenario: Contributor finds the extension pattern

- **WHEN** a contributor reads the root `README.md` layout or Docs section
- **THEN** they learn that `principles.global.md` is canonical shared content
- **AND** they learn that repo-local `principles.md` is the place to extend

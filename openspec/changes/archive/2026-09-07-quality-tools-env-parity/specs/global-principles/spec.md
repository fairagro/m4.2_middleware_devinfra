# global-principles Delta

## MODIFIED Requirements

### Requirement: Shared principles.global.md exists

The repository MUST provide `openspec/principles.global.md` as the canonical shared engineering foundation for m4.2
middleware consumers. That file MUST include at least: shared values (including **Simplicity**: smallest readable
change, abstractions only when needed, delete unused structure; and **Supported environment first** with the surface
quality bar for product vs shared Devinfra scripts vs agent plumbing), Supported development environment detail, Type
Safety core rules, shared code-quality expectations (`uv` and the standard lint/type/security gates), **quality tool
environment parity** (IDE, pre-commit / pre-push, and GitHub pipelines MUST use the same shared config files and MUST
produce matching gate outcomes for the same tree and toolchain pins; invocations MUST NOT restate config-file policy as
extra CLI/IDE flags beyond config path, targets, and documented path overlays), **Python tooling: `uv` exclusively** (no
`pip` / `poetry` / `pipenv` for project or CI dependency management), and the rule that application code must not read
configuration via direct `os.environ` (configuration goes through the project's config wrapper pattern). Product-only
technology stacks, module graphs, and scaling notes MUST NOT be normative content of `principles.global.md`.

#### Scenario: Agent looks up supported environment

- **WHEN** an agent or reviewer needs the supported development environment rule
- **THEN** it is defined in `openspec/principles.global.md`
- **AND** the file does not require FastAPI, Celery, or CouchDB as shared stack

#### Scenario: Agent looks up simplicity / implementation guidance

- **WHEN** an agent implements or refactors code under these principles
- **THEN** Values → Simplicity tells it to prefer the smallest readable change and avoid speculative abstractions
- **AND** Supported environment first / surface quality bar judges shared Devinfra scripts and agent plumbing on their
  Dev Container (or documented CI) happy paths — not exotic host edges

#### Scenario: Agent looks up quality environment parity

- **WHEN** an agent or reviewer configures IDE, hooks, or CI for a shared quality tool
- **THEN** `openspec/principles.global.md` states that IDE, pre-commit / pre-push, and GitHub pipelines must share
  config files and matching outcomes
- **AND** it forbids restating fragment/config policy via extra CLI or IDE flags beyond config path, targets, and
  documented path overlays

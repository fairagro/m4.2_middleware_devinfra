# global-principles Specification

## Purpose

Defines the shared OpenSpec principles base file and the repo-local extension pattern so product repos can specialize
without forking Supported environment or Type Safety rules.

## Requirements

### Requirement: Shared principles.global.md exists

The repository MUST provide `openspec/principles.global.md` as the canonical shared engineering foundation for m4.2
middleware consumers. That file MUST include at least: shared values (including **Simplicity**: smallest readable
change, abstractions only when needed, delete unused structure; and **Supported environment first** with the surface
quality bar for product vs shared Devinfra scripts vs agent plumbing), Supported development environment detail, Type
Safety core rules, shared code-quality expectations (`uv` and the standard lint/type/security gates), **quality tool
environment parity** (IDE, pre-commit / pre-push, and GitHub pipelines MUST use the same shared config files and MUST
produce matching gate outcomes for the same tree and toolchain pins; invocations MUST NOT restate config-file policy as
extra CLI/IDE flags beyond config path, targets, and documented path overlays), **Python tooling: `uv` exclusively** (no
`pip` / `poetry` / `pipenv` for project or CI dependency management), the rule that application code must not read
configuration via direct `os.environ` (configuration goes through the project's config wrapper pattern), and a normative
**Import policy** section (module-level absolute imports, no path hacks / cycle-breaking deferred imports, documented
exceptions; see the Import policy requirement). Product-only technology stacks, module graphs, and scaling notes MUST
NOT be normative content of `principles.global.md`.

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

#### Scenario: Agent looks up import policy via principles inventory

- **WHEN** an agent or reviewer scans `openspec/principles.global.md` for shared engineering rules
- **THEN** an Import policy section is present alongside Values, Type Safety, and Code Quality

### Requirement: Import policy in shared principles

`openspec/principles.global.md` MUST include a normative **Import policy** section for product application code under
`middleware/` (and for tests that import that code). The section MUST require:

1. No runtime mutation of import paths to make a module resolvable (`sys.path` inserts, rewriting `__path__`,
   project-root shims that redirect to `src/`, and equivalents).
2. Imports MUST run at module level — not inside functions, methods, or conditional runtime blocks — except
   `if TYPE_CHECKING:` for type-only imports.
3. `if TYPE_CHECKING:` is allowed for annotations only; it MUST NOT be used to justify cyclic **runtime** edges.
4. No relative imports — use absolute imports (`middleware.<package>…`).
5. No deferred / lazy imports **for the purpose of breaking import cycles** (including lazy `__getattr__` re-exports
   used only to paper over a bad graph).
6. Split modules so the dependency DAG is acyclic and every **runtime** edge is a normal top-level absolute import.
7. Exceptions to (1)/(2)/(4)/(5)/(6) require user agreement plus an inline comment and/or principles note naming the
   exception and why.

The section MUST also record these decisions:

- **Package `__init__.py`:** Curated public `__all__` with **eager absolute** re-exports is allowed when the subgraph is
  already acyclic; thin docstring-only `__init__` remains preferred when there is no public surface. Lazy /
  `__getattr__` re-exports used only to hide cycles are forbidden.
- **Registration-only imports:** Prefer a side-effect module imported absolutely at module level (no function-body
  imports).
- **Monorepo src-layout shadowing:** Prefer rename/move or documented static layout; runtime shims remain forbidden.
- **Tests:** Rules (2)/(4)/(5)/(6) apply equally to unit tests that import application code.

Product-only module graphs and stack tables MUST remain out of `principles.global.md` (local `principles.md` / product
specs).

#### Scenario: Agent looks up import rules

- **WHEN** an agent or reviewer needs the shared import / cycle policy
- **THEN** it is defined in `openspec/principles.global.md` under Import policy
- **AND** the rules forbid path hacks, relative imports, and cycle-breaking deferred imports
- **AND** `TYPE_CHECKING` is documented as the type-only exception to module-level imports

#### Scenario: Contributor reads package init guidance

- **WHEN** a contributor reads Import policy for `__init__.py` re-exports
- **THEN** they learn eager absolute re-exports are OK when the subgraph is acyclic
- **AND** they learn lazy/`__getattr__` cycle papering is forbidden

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

### Requirement: Code Quality wording is consumer-portable

`openspec/principles.global.md` Code Quality MUST describe shared quality gates in wording that remains accurate for
product consumers: use shared config fragments when present (`ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`) or the
project's equivalent config, and cite `docs/quality.md` when that file is synced. It MUST NOT imply that every consumer
checkout already has Devinfra-only paths, and MUST NOT push agents to invent a second quality policy channel.

#### Scenario: Product agent reads Code Quality

- **WHEN** an agent in a product checkout reads `openspec/principles.global.md` Code Quality
- **THEN** the commands remain valid when shared fragments are synced
- **AND** the text does not require inventing product-local quality policy outside shared fragments / project config

### Requirement: Fleet branch CI channels in shared principles

`openspec/principles.global.md` MUST document the fleet **Branch Strategy** using CI **channel** prefixes (not GitHub
issue types):

| Prefix    | Purpose                                            |
| --------- | -------------------------------------------------- |
| `main`    | Trunk — always deployable                          |
| `build/*` | Product image/app work; optional Pre Release / RC  |
| `ci/*`    | Shared CI/tooling (scripts, Dev Container, tests…) |
| `docs/*`  | Documentation-only; may skip unnecessary CI jobs   |
| `chore/*` | Sync/bots; MUST NOT Pre Release                    |

Issue-driven work MUST keep the issue number in the branch name as `{channel}/issue-<n>-<slug>`. Fine-grained job
selection remains path/change detection — prefixes MUST NOT multiply per file kind (`test/`, `scripts/`, …).

#### Scenario: Agent looks up branch naming

- **WHEN** an agent or contributor reads the Branch Strategy in `openspec/principles.global.md`
- **THEN** they see `build/*`, `ci/*`, `docs/*`, and `chore/*` as the documented short-lived channels
- **AND** they do not see `feature/*` as the normative work-branch prefix

### Requirement: Synced `.global` + product overlay naming is documented

`openspec/principles.global.md` MUST document the fleet naming rule for splitting a shared synced file from a
product-specific companion: synced SoT uses a **`.global`** stem (`*.global` / `*.global.*`) on the sync `allow` list;
the product companion uses the **same basename without `.global`** and is listed under sync `overlays` (never
overwritten). The document MUST cite examples including `principles.global.md` / `principles.md`,
`surface-quality-bar.global.md` / `surface-quality-bar.md`, and `.importlinter.global` / `.importlinter`. It MUST forbid
inventing alternate suffixes such as `.product` for this split.

#### Scenario: Contributor reads principles for overlay naming

- **WHEN** a contributor opens `openspec/principles.global.md` looking for how shared vs product files are named
- **THEN** they find the synced-`.global` + product-local pair rule with the import-linter and principles examples
- **AND** they learn not to use a `.product` suffix for that split

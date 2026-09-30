## MODIFIED Requirements

### Requirement: Agent CLI README documents workspace and consumer layouts

`scripts/ai/README.md` MUST document both layouts:

1. **Devinfra (workspace member):** `scripts/ai` is a `tool.uv.workspace` member of the repo-root `pyproject.toml`;
   preferred invoke `uv run m42-ai …` after root `uv sync`; tests via root `uv run pytest` when so configured.
2. **Product consumers:** by design `scripts/ai` is **not** in the product root workspace; the **primary silent** invoke
   is `m42-ai …` when synced `scripts/bin` is on `PATH` (wrapper unsets conflicting `VIRTUAL_ENV` then runs
   `uv run --project scripts/ai m42-ai …`). Portable equivalent without the wrapper:
   `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …`. Document the matching test command (e.g.
   `uv run --project scripts/ai pytest` or with `env -u VIRTUAL_ENV` when silencing warnings). MUST NOT recommend
   `uv run --active` for this CLI. MUST NOT imply removing Dev Container `VIRTUAL_ENV`.

The README MUST NOT imply that product repos use root-workspace membership solely because Devinfra does. Both layouts
MUST remain valid for their respective repos.

#### Scenario: Product adopter reads Run / Tests sections

- **WHEN** a contributor in a product repo opens synced `scripts/ai/README.md`
- **THEN** they find `m42-ai …` (wrapper) or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …` as the primary
  silent consumer invoke (or clearly labeled consumer path)
- **AND** they find Devinfra workspace / root `uv run` documented as the Devinfra layout
- **AND** test instructions match each layout
- **AND** they are not directed to `uv run --active` or to remove DC `VIRTUAL_ENV`

### Requirement: Synced skills prefer portable m42-ai invoke

Synced first-party agent skills (`issue-fixer`, `create-issue`, `review-fixer`, `code-review`) and their thin docs MUST
document a **silent** primary invoke: `m42-ai …` when `scripts/bin` is on `PATH`, or
`env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …` when the wrapper is unavailable. They MAY note that bare
`uv run m42-ai …` works only when `scripts/ai` is a root uv workspace member (Devinfra). They MUST NOT present bare
`uv run m42-ai` as the only or primary form for product consumers. They MUST NOT document `uv run --active` as the
silence path for this CLI.

#### Scenario: Product agent follows issue-fixer skill

- **WHEN** an agent in a product checkout follows a synced fixer skill to run `m42-ai`
- **THEN** the skill shows a silent primary command (`m42-ai …` or
  `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …`)
- **AND** it does not require root-workspace membership of `scripts/ai`
- **AND** it does not recommend `uv run --active` for silencing the warning

#### Scenario: Product agent follows code-review skill

- **WHEN** an agent in a product checkout follows `/code-review` to run helpers
- **THEN** the skill shows a silent primary command (`m42-ai …` or
  `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai …`)
- **AND** it does not require root-workspace membership of `scripts/ai`

# agent-ai-gh Delta

## ADDED Requirements

### Requirement: Agent CLI README documents workspace and consumer layouts

`scripts/ai/README.md` MUST document both layouts:

1. **Devinfra (workspace member):** `scripts/ai` is a `tool.uv.workspace` member of the repo-root `pyproject.toml`;
   preferred invoke `uv run m42-ai …` after root `uv sync`; tests via root `uv run pytest` when so configured.
2. **Product consumers:** by design `scripts/ai` is **not** in the product root workspace; invoke with
   `uv run --project scripts/ai m42-ai …` (and document the matching test command, e.g.
   `uv run --project scripts/ai pytest`).

The README MUST NOT imply that product repos use root-workspace membership solely because Devinfra does. Both layouts
MUST remain valid for their respective repos.

#### Scenario: Product adopter reads Run / Tests sections

- **WHEN** a contributor in a product repo opens synced `scripts/ai/README.md`
- **THEN** they find `--project scripts/ai` as the primary consumer invoke (or clearly labeled consumer path)
- **AND** they find Devinfra workspace / root `uv run` documented as the Devinfra layout
- **AND** test instructions match each layout

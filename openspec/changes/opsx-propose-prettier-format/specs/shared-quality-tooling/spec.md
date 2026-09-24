## ADDED Requirements

### Requirement: OpenSpec propose formats change Markdown with Prettier

The repository’s OpenSpec **propose** skill (and the matching `/opsx-propose` command text) MUST require that, after all
required change artifacts for a new or continued propose run exist under `openspec/changes/<name>/`, the agent runs
Prettier **write** scoped to that change directory using the repo’s shared Prettier config (same policy as
`npm run format:md` / `format:md:check`). Propose MUST NOT be treated as complete while those Markdown files would fail
`npm run format:md:check` solely due to Prettier wrap/format drift. Documentation MUST note that regenerating opsx
skills via `openspec update` MAY overwrite the skill patch and MUST be re-applied or upstreamed. The repository MUST NOT
solve this by ignoring `openspec/changes/**` in `.prettierignore`.

#### Scenario: Propose ends with Prettier on the change tree

- **WHEN** an agent finishes creating OpenSpec change artifacts via the propose skill / `/opsx-propose`
- **THEN** the skill instructs a Prettier write scoped to `openspec/changes/<name>/` (or equivalent paths from
  `changeRoot`) before claiming propose complete
- **AND** those files pass fleet `format:md:check` without a separate manual format turn

#### Scenario: Changes stay Prettier-checked

- **WHEN** a contributor inspects `.prettierignore` for OpenSpec planning trees
- **THEN** `openspec/changes/**` is not blanket-ignored to silence propose format failures

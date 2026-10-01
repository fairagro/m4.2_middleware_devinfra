## ADDED Requirements

### Requirement: openspec-instructions wraps OpenSpec instructions JSON

The `m42-ai` CLI MUST provide a command (e.g. `openspec-instructions`) that invokes
`openspec instructions <artifact> --change <name> --json` (OpenSpec on `PATH`), validates that stdout is JSON, and
prints machine-readable JSON on stdout.

On success the JSON MUST include at least the fields agents need to write artifacts: `resolvedOutputPath`,
`instruction`, and `template` when present in the OpenSpec payload (other OpenSpec fields MAY be passed through).

On failure (non-zero OpenSpec exit, empty stdout, non-JSON stdout, or OpenSpec JSON whose `status` entries indicate a
blocking error such as `change_error`) the CLI MUST exit non-zero and print structured error JSON including at least
`ok: false`, `error`, and `agent_action: "stop"`. It MUST NOT invent `template` or `resolvedOutputPath`.

#### Scenario: Successful instructions load

- **WHEN** an agent runs `m42-ai openspec-instructions --artifact proposal --change <existing-change>`
- **AND** OpenSpec returns valid instructions JSON for that artifact
- **THEN** the CLI exits 0
- **AND** stdout JSON includes `resolvedOutputPath` and `instruction` (and `template` when OpenSpec provided one)

#### Scenario: Missing change fails closed

- **WHEN** an agent runs `m42-ai openspec-instructions --artifact proposal --change <unknown-change>`
- **THEN** the CLI exits non-zero
- **AND** stdout is structured error JSON with `ok: false` and `agent_action: "stop"`
- **AND** the payload does not invent a template or output path for the agent to write

#### Scenario: Empty or non-JSON OpenSpec output fails closed

- **WHEN** OpenSpec produces empty or non-JSON stdout for an instructions request
- **THEN** the CLI exits non-zero with structured error JSON (`ok: false`, `agent_action: "stop"`)
- **AND** agents are not given a fabricated `template` / `resolvedOutputPath`

### Requirement: OpenSpec skills prefer openspec-instructions and fail closed

Devinfra OpenSpec skills that load artifact instructions (at least `openspec-propose`, `openspec-apply-change`,
`openspec-archive-change`, `openspec-update-change`, `openspec-sync-specs`) MUST document a **silent primary** load via
`m42-ai openspec-instructions` (or `env -u VIRTUAL_ENV uv run --project scripts/ai m42-ai openspec-instructions` when
the wrapper is unavailable). They MUST instruct agents to **stop and report** on helper / OpenSpec failure — MUST NOT
invent `template` or `resolvedOutputPath`, and MUST NOT approximate artifact contents when instructions cannot be
loaded.

They MUST discourage brittle pipes of the form `openspec … --json 2>&1 | python -c 'json.load(sys.stdin)'` as the
primary parse path. A temp-file parse of `openspec instructions … --json` MAY be documented as a fallback only when
`m42-ai` is unavailable, with the same fail-closed rules.

`scripts/ai/README.md` MUST list the new command alongside other agent plumbing commands.

#### Scenario: Propose skill loads proposal instructions

- **WHEN** an agent follows `openspec-propose` to create `proposal.md`
- **THEN** the skill shows `m42-ai openspec-instructions --artifact proposal --change <name>` (or the portable
  `env -u VIRTUAL_ENV uv run --project scripts/ai …` form) as the primary instructions load
- **AND** on failure it directs the agent to stop and report rather than invent a template

#### Scenario: Apply skill refuses invented apply instructions

- **WHEN** `openspec-instructions` (or the documented fallback) fails while loading apply instructions
- **THEN** the apply skill directs the agent to stop
- **AND** does not instruct inventing tasks or skipping the instructions contract

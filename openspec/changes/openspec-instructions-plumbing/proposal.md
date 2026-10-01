## Why

Agents load OpenSpec artifact guidance via `openspec instructions … --json`, then often pipe it through brittle
`python -c 'json.load(sys.stdin)'` one-liners. When stdout is empty or non-JSON, parse fails and agents invent templates
— more work and wrong artifacts. Seen in the wild (`JSONDecodeError` on empty stdin). Harden plumbing so the control
plane stays fail-closed.

## What Changes

- Add a thin `m42-ai openspec-instructions` command that wraps
  `openspec instructions <artifact> --change <name> --json`, validates JSON, and prints structured success fields or a
  clear JSON error with non-zero exit
- Update Devinfra OpenSpec skills
  (`.cursor/skills/openspec-{propose,apply-change,archive-change,update-change,sync-specs}`) to prefer that helper (or
  an equivalent fail-closed temp-file parse), forbid inventing `template` / `resolvedOutputPath` on failure, and
  discourage brittle `2>&1 | python json.load` pipes
- Document the command in `scripts/ai/README.md`
- Fixture/unit tests without requiring a live OpenSpec change network call beyond local CLI

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `agent-ai-gh`: require `openspec-instructions` CLI surface + fail-closed agent guidance for OpenSpec skills that load
  instructions JSON

## Impact

- `scripts/ai` (`m42-ai` CLI + tests + README)
- `.cursor/skills/openspec-*` skill Markdown (Devinfra SoT; regenerate-aware if `openspec update` rewrites skills)
- `openspec/specs/agent-ai-gh` after archive
- No product middleware / CI workflow behavior change beyond synced skill/CLI sync

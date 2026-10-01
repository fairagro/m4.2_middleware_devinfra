## Context

See proposal.md — Why. Today agents call `openspec instructions … --json` and often parse via fragile shell pipes.
OpenSpec 1.13+ usually still emits JSON on `change_error`; empty/non-JSON stdout is the brittle wrapper. Skills under
`.cursor/skills/openspec-*` are Devinfra-customized (e.g. Prettier step on propose) even though they carry OpenSpec
generator metadata — treat them as SoT to patch here; if a later `openspec update` rewrites them, re-apply the
fail-closed + helper prefer guidance.

## Goals / Non-Goals

**Goals:**

- One durable `m42-ai` entrypoint that validates instructions JSON and fails closed
- Skills prefer that entrypoint and forbid inventing templates on failure
- Contract tests with mocked/subprocess OpenSpec output shapes (success, change_error, empty)

**Non-Goals:**

- Patching the OpenSpec CLI itself
- Changing OpenSpec schema / artifact templates
- Syncing openspec-* skills to product repos beyond existing paths (helper syncs via `scripts/ai`)
- Auto-creating missing changes from the helper

## Decisions

1. **CLI name `openspec-instructions`** with `--artifact` / `--change` (mirrors OpenSpec args). Alternative: subcommand
   group `openspec instructions` — rejected to avoid colliding with shelling out to the `openspec` binary name in docs.
2. **Pass-through success JSON** (subset or full OpenSpec object) plus ensure `ok: true` optionally — prefer returning
   the OpenSpec object fields agents already expect (`resolvedOutputPath`, `instruction`, `template`, …) and only use
   the `ok: false` envelope on errors (same pattern family as `review-open` gates).
3. **Detect OpenSpec `status` errors** even when exit code is ambiguous: if JSON has `status` list with
   `severity: error` / `code: change_error`, treat as failure.
4. **Skills: primary = m42-ai; fallback = temp file + python parse with exit check** — never `2>&1 | json.load` as
   primary. Update all five skills that call `openspec instructions`.
5. **`openspec-explore`:** out of scope unless it loads instructions the same way (skip if not).

## Risks / Trade-offs

- [`openspec update` rewrites skills] → Mitigation: keep guidance short and re-apply after update; helper remains the
  durable contract in `scripts/ai` + `agent-ai-gh`.
- [Helper depends on `openspec` on PATH] → Mitigation: clear error when binary missing; Dev Container already pins
  OpenSpec via `versions.env`.
- [Agents ignore skill text] → Mitigation: make the happy path shorter than inventing templates (one CLI call).

## Migration Plan

Land CLI + tests + README + skill edits in one PR. Products pick up CLI on next sync; skill edits apply in Devinfra
immediately (and wherever those skill paths sync).

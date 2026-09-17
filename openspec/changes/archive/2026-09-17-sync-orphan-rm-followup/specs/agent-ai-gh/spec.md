## ADDED Requirements

### Requirement: CLI supports sync follow-up plumbing

The `m42-ai` CLI (under `scripts/ai/`) MUST provide commands (or a documented equivalent invoke surface) that sync
orchestration can call to:

1. Resolve a Devinfra pull request for a given commit SHA (when one exists).
2. Parse `SYNC-FOLLOWUP: <stable-id>` trailers from a PR body and from that PR’s issue/review comments (stable-id MUST
   be a non-empty token suitable for dedupe keys).
3. Ensure a follow-up GitHub issue exists in a target product repository for a given stable-id: create with org type
   `Task`, triage labels `severity:low` and a documented `cost:*` default, body from a Devinfra-owned template that
   links the Devinfra commit/PR, or reuse an existing **open** issue already keyed to that id (dedupe). MUST NOT create
   a second open issue for the same repo + id.

These commands MUST use `gh` on `PATH` (same auth model as the rest of the CLI). They MUST emit machine-readable JSON
suitable for Actions logging. Dry-run / no-op modes MAY exist for testing but live ensure MUST create or reuse issues
only when explicitly requested.

#### Scenario: Parse trailers from body and comments

- **WHEN** an agent or sync job asks the CLI to collect follow-up ids for a PR that has `SYNC-FOLLOWUP: remove-stubs` in
  the body and another id only in a comment
- **THEN** the CLI reports both distinct ids
- **AND** malformed lines without a stable id are ignored

#### Scenario: Ensure reuses open issue

- **WHEN** ensure runs for product repo R and id `remove-stubs` and an open issue already carries that dedupe key
- **THEN** the CLI returns that issue’s URL/number without creating another open issue

#### Scenario: Ensure creates Task when missing

- **WHEN** ensure runs for product repo R and id `remove-stubs` and no open dedupe match exists
- **THEN** the CLI creates a `Task` issue with `severity:low` and the documented cost label
- **AND** the body links the Devinfra source PR or commit

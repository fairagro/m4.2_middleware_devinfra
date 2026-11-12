## MODIFIED Requirements

### Requirement: review-fixer suggests a Conventional Commits message at handoff

Whenever `/review-fixer` Phase 1 pauses after applying local `fix` edits (dirty working tree or index), the skill MUST
include a ready-to-use Conventional Commits subject in that pause message (optional short body only when needed). The
subject MUST follow fleet Conventional Commits hard overrides. The skill MUST NOT auto-commit and MUST NOT steer the
user to Cursor Source Control sparkle for that handoff. Dismiss/follow-up-only runs with no local edits MUST omit the
commit-message block.

When the pause includes a Suggested commit message, any human-readable **label** (e.g. `Suggested commit message:`) MUST
appear **outside** the fenced/copyable block. The fence MUST contain **only** the Conventional Commits subject (and
optional short body) so copy-to-clipboard yields a paste-ready commit message.

#### Scenario: Phase 1 fix pause includes a suggested subject

- **WHEN** Phase 1 applies at least one local `fix` and pauses for the user to commit
- **THEN** the user-visible pause includes a Conventional Commits subject for the dirty/staged diff
- **AND** the skill still waits for a user-created SHA before `Fixed in …` replies

#### Scenario: Handoff fence excludes the label line

- **WHEN** `/review-fixer` Phase 1 pauses with a Suggested commit message after local `fix` edits
- **THEN** the copyable fenced block contains only the Conventional Commits subject (and optional short body)
- **AND** any “Suggested commit message” label text is outside that fence

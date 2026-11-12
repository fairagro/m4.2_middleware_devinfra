## MODIFIED Requirements

### Requirement: issue-fixer suggests a Conventional Commits message at handoff

Whenever `/issue-fixer` pauses and returns control to the user after leaving **uncommitted** changes in the working tree
or index (including OpenSpec propose/apply/archive artifacts and Task/Bug implement edits), the skill MUST include a
ready-to-use Conventional Commits subject in that pause message (optional short body only when multiple independent
themes share one commit). The subject MUST follow fleet hard overrides (OpenSpec archive / planning-only → `chore` /
`docs`, never false `feat` for `version_bump: auto`). The skill MUST NOT auto-commit and MUST NOT steer the user to
Cursor Source Control sparkle for that handoff. Explore-only or Discussion pauses with a clean tree MUST omit the
commit-message block.

When the pause includes a Suggested commit message, any human-readable **label** (e.g. `Suggested commit message:`) MUST
appear **outside** the fenced/copyable block. The fence MUST contain **only** the Conventional Commits subject (and
optional short body) so copy-to-clipboard yields a paste-ready commit message.

#### Scenario: Pause after implement includes a suggested subject

- **WHEN** `/issue-fixer` finishes a Bug/Task implement (or OpenSpec apply/archive) with a dirty working tree and pauses
- **THEN** the user-visible pause includes a Conventional Commits subject matching the full dirty/staged diff
- **AND** the skill still does not create the git commit itself

#### Scenario: Explore-only pause omits commit message

- **WHEN** `/issue-fixer` pauses only for explore lock-in and the working tree has no skill-authored uncommitted changes
- **THEN** the pause does not require a Suggested commit message block

#### Scenario: Handoff fence excludes the label line

- **WHEN** `/issue-fixer` pauses with a Suggested commit message after leaving uncommitted changes
- **THEN** the copyable fenced block contains only the Conventional Commits subject (and optional short body)
- **AND** any “Suggested commit message” label text is outside that fence

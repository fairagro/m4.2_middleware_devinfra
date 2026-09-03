# AI Review Policy — Delta

## Purpose

Defines the canonical Finder/Fixer AI review policy and the shared Bugbot and Copilot entry files that load it for all
m4.2 product consumers.

## ADDED Requirements

### Requirement: Canonical AI review policy document

The repository MUST provide `docs/ai_review_policy.md` as the single Finder/Fixer policy for shared consumers. The
document MUST define Finder and Fixer roles, risk versus nit merge criteria, severity and practicality and cost
guidance, nit-budget rules, type-widening bans, and follow-up issue rules. Product-only API examples (specific routes,
datastores, or config types that are not shared) MUST NOT appear as normative requirements; shared vocabulary MUST be
used instead.

#### Scenario: Contributor opens the shared policy

- **WHEN** a contributor opens `docs/ai_review_policy.md`
- **THEN** they find Finder and Fixer role definitions and the risk-versus-nit merge rule
- **AND** the document does not require API-only nouns as the only valid entry points

### Requirement: Bugbot entry points at the policy

The repository MUST provide `.cursor/BUGBOT.md` that instructs Bugbot to act as the Finder and to follow
`docs/ai_review_policy.md`. The file MUST state that `.cursor/rules/` do not apply to Bugbot for this review role.

#### Scenario: Bugbot loads shared instructions

- **WHEN** Bugbot runs in a consumer that synced `.cursor/BUGBOT.md`
- **THEN** it is directed to `docs/ai_review_policy.md` as Finder policy
- **AND** it is told not to apply `.cursor/rules/` for that role

### Requirement: Copilot entry points at the policy

The repository MUST provide `.github/copilot-instructions.md` that instructs GitHub Copilot, when performing a code
review, to act as the Finder and to follow `docs/ai_review_policy.md`. Product-local agent docs (`AGENTS.md`, local
stack notes) MUST NOT be required content of the shared Copilot entry; consumers MAY keep additional local guidance
outside this synced file.

#### Scenario: Copilot review uses shared Finder policy

- **WHEN** Copilot performs a code review using the synced `.github/copilot-instructions.md`
- **THEN** it is directed to `docs/ai_review_policy.md` as Finder policy
- **AND** the shared file does not mandate reading a product-only `AGENTS.md`

### Requirement: Policy cites principles.global.md directly

Where the AI review policy refers to Supported development environment or Type Safety constraints, it MUST cite
`openspec/principles.global.md` by that path (not only via a repo-local `openspec/principles.md` indirection).

#### Scenario: Fixer dismisses unsupported-host finding

- **WHEN** a fixer dismisses a finding about macOS, Windows, Homebrew, or unofficial host PATH layouts
- **THEN** the policy tells them to quote `openspec/principles.global.md` Supported development environment
- **AND** the citation path is `openspec/principles.global.md`

### Requirement: README indexes the AI review stack

The root `README.md` MUST link to `docs/ai_review_policy.md` and MUST state that consumers must not hand-edit the synced
AI review policy or Finder entry paths.

#### Scenario: Consumer checks ownership for AI review files

- **WHEN** a contributor reads the root `README.md`
- **THEN** they find `docs/ai_review_policy.md` in the Docs index (or equivalent documented layout)
- **AND** they are reminded not to diverge locally on synced AI review paths

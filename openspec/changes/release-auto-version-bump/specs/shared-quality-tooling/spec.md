## ADDED Requirements

### Requirement: Conventional Commits are enforced at commit-stage

The shared quality tooling MUST enforce [Conventional Commits](https://www.conventionalcommits.org/) on commit messages
via **commitlint** (or an equivalent Conventional Commits linter) in the shared pre-commit skeleton, using a fleet
config checked into Devinfra and synced to products. The config MUST accept Renovate’s shared commit message prefix
(`deps:`) so dependency bot commits are not rejected solely for that prefix. Documentation (`docs/quality.md` and/or
`docs/ci.md`) MUST state the mapping used for release `version_bump: auto` (breaking → major, `feat` → minor,
`fix`/other → patch) and that enforcement exists so auto-detect stays trustworthy. Reusable code-quality MAY run the
same commitlint config on CI when practical; commit-stage remains the primary gate.

#### Scenario: Non-conventional commit message fails commit-stage

- **WHEN** a contributor attempts a commit whose message does not satisfy the shared Conventional Commits commitlint
  config
- **THEN** the commit-stage hook fails
- **AND** the failure names Conventional Commits / commitlint as the gate

#### Scenario: Renovate-style deps commits are allowed

- **WHEN** a commit message uses the shared Renovate `deps:` prefix in a form allowed by the fleet commitlint config
- **THEN** commitlint does not fail solely because of that prefix

### Requirement: Editor commit-message generation targets Conventional Commits

Synced IDE settings MUST instruct both **Cursor** and **VS Code** (GitHub Copilot) commit-message generation to produce
Conventional Commits–compatible messages (same fleet convention as commitlint). This MUST NOT be Cursor-sparkle-only: VS
Code Copilot generate-commit-message (or equivalent workspace setting) MUST receive the same convention. Agents that
author commits in these repos MUST follow the same convention. Documentation MUST point operators at those settings and
state that the sparkle / auto-generate buttons remain the supported UX.

#### Scenario: Maintainer finds dual-editor Conventional Commit guidance

- **WHEN** a maintainer opens quality or CI docs after this change
- **THEN** they learn commit messages must be Conventional Commits for `version_bump: auto`
- **AND** they learn Cursor sparkle and VS Code Copilot commit generation are both configured toward that convention
- **AND** they learn commitlint enforces the convention at commit-stage

## MODIFIED Requirements

### Requirement: Editor commit-message generation targets Conventional Commits

Synced IDE settings MUST instruct both **Cursor** and **VS Code** (GitHub Copilot) commit-message generation to produce
Conventional Commits–compatible messages (same fleet convention as commitlint). This MUST NOT be Cursor-sparkle-only: VS
Code Copilot generate-commit-message (or equivalent workspace setting) MUST receive the same convention; Cursor SCM
sparkle MUST be steered via synced root `.cursorrules` when that is the supported Cursor surface. Agents that author
commits in these repos MUST follow the same convention. Guidance MUST **prefer** an optional Conventional Commits
**scope** naming the primary component or area when one is clear from the staged diff (e.g. `fix(payload): …`), while
keeping scope optional — commitlint MUST NOT gain a fleet `scope-enum` solely for this preference. Documentation MUST
point operators at those settings, state that the sparkle / auto-generate buttons remain the supported UX, and note that
scopes are encouraged but not allowlist-enforced.

#### Scenario: Maintainer finds dual-editor Conventional Commit guidance

- **WHEN** a maintainer opens quality or CI docs after this change
- **THEN** they learn commit messages must be Conventional Commits for `version_bump: auto`
- **AND** they learn Cursor sparkle and VS Code Copilot commit generation are both configured toward that convention
- **AND** they learn commitlint enforces the convention at commit-stage

#### Scenario: Editor guidance prefers optional component scope

- **WHEN** a contributor uses Cursor sparkle or VS Code Copilot commit-message generation after this change
- **THEN** the synced instructions ask for an optional `type(scope):` component/area scope when clear from the diff
- **AND** the fleet commitlint config does not require a fixed `scope-enum` for that preference

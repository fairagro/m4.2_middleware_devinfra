## ADDED Requirements

### Requirement: Fleet branch CI channels in shared principles

`openspec/principles.global.md` MUST document the fleet **Branch Strategy** using CI **channel** prefixes (not GitHub
issue types):

| Prefix    | Purpose                                            |
| --------- | -------------------------------------------------- |
| `main`    | Trunk — always deployable                          |
| `build/*` | Product image/app work; optional Pre Release / RC  |
| `ci/*`    | Shared CI/tooling (scripts, Dev Container, tests…) |
| `docs/*`  | Documentation-only; may skip unnecessary CI jobs   |
| `chore/*` | Sync/bots; MUST NOT Pre Release                    |

Issue-driven work MUST keep the issue number in the branch name as `{channel}/issue-<n>-<slug>`. Fine-grained job
selection remains path/change detection — prefixes MUST NOT multiply per file kind (`test/`, `scripts/`, …).

#### Scenario: Agent looks up branch naming

- **WHEN** an agent or contributor reads the Branch Strategy in `openspec/principles.global.md`
- **THEN** they see `build/*`, `ci/*`, `docs/*`, and `chore/*` as the documented short-lived channels
- **AND** they do not see `feature/*` as the normative work-branch prefix

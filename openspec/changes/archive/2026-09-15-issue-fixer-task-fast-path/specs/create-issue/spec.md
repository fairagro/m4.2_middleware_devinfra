# create-issue Delta

## MODIFIED Requirements

### Requirement: One org issue type and triage labels

The skill MUST pick exactly one GitHub org issue type from: `Bug`, `Security`, `Feature`, `Task`, `Discussion`,
`Refactoring`. It MUST NOT encode kinds as `kind:*` labels.

**Task** MUST mean bounded known-how work (config/hook/YAML wiring, cleanup, docs, marker registration, or “do X as
already agreed”) — **not** a new capability or durable contract (that is `Feature`) and **not** multi-module restructure
(that is `Refactoring`). When acceptance criteria would change a capability under `openspec/specs/`, the skill SHOULD
prefer `Feature` (or ask once).

It MUST attach exactly one allowlisted `severity:*` and one `cost:*` label. It MUST attach a `practicality:*` label
**only** when there is a concrete path to a bad outcome (typical for `Bug` / `Security` and `/review-fixer` Medium+
deferrals); it MUST NOT attach `practicality:high` merely because the work is implementable. When omitting practicality,
the issue body triage MUST record `practicality: n/a (no defect path)` (or equivalent). Allowed label names are only
from: `severity:blocker|high|medium|low`, `practicality:high|medium|low|none|seen-in-the-wild`, and
`cost:cheap|medium|expensive`. Severity, practicality, and cost definitions MUST cite `docs/ai_review_policy.md`, with
`practicality:seen-in-the-wild` and `cost:medium` documented as issue-oriented extensions. For `Feature`, `Task`,
`Discussion`, and `Refactoring`, when the user does not supply severity, the skill MUST default to `severity:low` unless
a clear operator/CI break or policy-matching high/blocker/medium path applies — it MUST NOT default to `severity:medium`
because the work “matters”.

#### Scenario: Security finding becomes a Security issue

- **WHEN** the user asks to create an issue for credential leakage with severity High
- **THEN** the skill selects issue type `Security`
- **AND** attaches matching allowlisted severity/practicality/cost labels

#### Scenario: Parity Task without defect-path practicality

- **WHEN** the user asks to create a Task for adding an existing quality gate to reusable CI (improvement, no Bug path)
- **THEN** the skill selects issue type `Task`
- **AND** attaches `severity:low` (unless the user set a higher severity) and a `cost:*` label
- **AND** does not attach a `practicality:*` label

#### Scenario: New capability is Feature not Task

- **WHEN** the user asks to create work that adds a new durable behaviour or capability contract
- **THEN** the skill selects issue type `Feature`
- **AND** it does not select `Task` solely because the change looks small

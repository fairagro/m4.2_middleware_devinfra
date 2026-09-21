## MODIFIED Requirements

### Requirement: Review goals and anti-duplication

The skill MUST cover these goals (skip when not applicable to the diff): security (judgment beyond automated scanners),
correctness / missing edge cases, concurrency and races, architecture and simplicity, import graph / cycles
(**judgment-only** for what import-linter does not encode — applying the **Import policy** in
`openspec/principles.global.md`), defensive bloat vs missing edges, resource use, dead / unused code **only as judgment
beyond what vulture already gates**, OpenSpec↔code drift **only where specs exist and the diff touches that surface**,
docs↔code drift (weaker severity than spec drift), and test adequacy for new risks.

The skill MUST NOT restate findings that the quality toolchain already owns: Ruff, mypy, pylint, Bandit, markdownlint,
Prettier, ggshield, CodeQL, Trivy, **vulture**, and **import-linter**. Format, import sort, line-length, and type noise
that CI already fails MUST be out of scope. Mechanical unused-definition hits that vulture reports at the fleet
confidence gate MUST NOT be re-reported as review findings. Mechanical cycle/layer/forbidden violations that
import-linter reports MUST NOT be re-reported as review findings. Judgment MAY still cover Import-policy rules outside
the linter (module-level placement, relative imports, `sys.path` mutation, lazy imports used only to break cycles).

Severity language MUST align with `docs/ai_review_policy.md`. For Medium+ findings the skill MAY offer `/create-issue`
(it MUST NOT auto-create issues unless the user asks). Shared code-review documentation (`docs/code-review.md`) MUST
point reviewers at the Import policy in `openspec/principles.global.md` for import-graph judgment beyond the linter.

#### Scenario: Style-only nit is omitted

- **WHEN** a diff only has import-sort or line-length issues already covered by Ruff/Prettier
- **THEN** the skill does not report those as findings
- **AND** it still reviews applicable judgment goals on the same diff

#### Scenario: Spec drift only when specs touch the surface

- **WHEN** the diff changes code with no related OpenSpec requirement in the checkout
- **THEN** the skill does not invent a spec-drift finding solely for missing specs

#### Scenario: Import-graph judgment cites principles

- **WHEN** an agent applies the import graph / cycles goal
- **THEN** the skill (or linked `docs/code-review.md`) directs it to Import policy in `openspec/principles.global.md`
- **AND** mechanical import-linter findings remain toolchain-owned

#### Scenario: Vulture-class unused code is omitted

- **WHEN** a diff only has unused definitions that the fleet vulture gate would report
- **THEN** the skill does not restate those as review findings
- **AND** it may still discuss judgment-only dead-code / design issues outside vulture’s mechanical scope

#### Scenario: Import-linter violations are omitted

- **WHEN** a diff only has cycle/layer/forbidden issues that the fleet import-linter gate would report
- **THEN** the skill does not restate those as review findings
- **AND** it may still discuss Import-policy judgment outside the linter’s mechanical scope

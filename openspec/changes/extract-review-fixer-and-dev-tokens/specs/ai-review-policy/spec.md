# AI Review Policy — Delta

## MODIFIED Requirements

### Requirement: Canonical AI review policy document

The repository MUST provide `docs/ai_review_policy.md` as the single Finder/Fixer policy for shared consumers. The
document MUST define Finder and Fixer roles, risk versus nit merge criteria, severity and practicality and cost
guidance, nit-budget rules, type-widening bans, and follow-up issue rules. Product-only API examples (specific routes,
datastores, or config types that are not shared) MUST NOT appear as normative requirements; shared vocabulary MUST be
used instead.

Nit-budget MUST be scoped **per fixer run** (approximately 15 new production lines for cheap nits, never a new
abstraction), MUST NOT be gated on Copilot/Bugbot review round number, MUST still allow cheap fixes for regressions on
the previous fixer pass (counting toward that run’s budget), and MUST never budget away risk or step-5 (cheap + High
practicality + Medium+) findings.

#### Scenario: Contributor opens the shared policy

- **WHEN** a contributor opens `docs/ai_review_policy.md`
- **THEN** they find Finder and Fixer role definitions and the risk-versus-nit merge rule
- **AND** the document does not require API-only nouns as the only valid entry points

#### Scenario: Nit budget is per fixer run

- **WHEN** a fixer triages Low nits on a PR that already had an earlier Copilot/Bugbot review round
- **THEN** cheap nits may still be fixed while this run’s nit prod-line growth stays within ~15
- **AND** the policy does not require dismissing them solely because the review round is 2 or higher

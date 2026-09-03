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

The policy MUST require `dismiss` (practicality None) when a finding’s only realistic path is outside the supported
Linux Dev Container environment (including BSD/non-GNU tool differences and host-only compatibility fallbacks), quoting
`openspec/principles.global.md` Supported development environment, and MUST NOT treat “cheap fix” as a reason to fix
those findings. GitHub Actions Linux CI remains in scope.

The policy MUST also require `dismiss` (practicality None) for findings that only harden a **one-shot local migration**
or ephemeral personal on-disk format that is not the current write path and not a shipped consumer contract (e.g.
pre-`b64:` personal token file lines fixable by re-running setup once). Finders MUST NOT comment on those; fixers MUST
NOT add compatibility parsers or deny-lists for them.

#### Scenario: Contributor opens the shared policy

- **WHEN** a contributor opens `docs/ai_review_policy.md`
- **THEN** they find Finder and Fixer role definitions and the risk-versus-nit merge rule
- **AND** the document does not require API-only nouns as the only valid entry points

#### Scenario: Nit budget is per fixer run

- **WHEN** a fixer triages Low nits on a PR that already had an earlier Copilot/Bugbot review round
- **THEN** cheap nits may still be fixed while this run’s nit prod-line growth stays within ~15
- **AND** the policy does not require dismissing them solely because the review round is 2 or higher

#### Scenario: Host-only fallback finding is dismissed

- **WHEN** a finder reports a bug that only occurs on a non-Dev-Container tool (e.g. `base64` without GNU `-w0`) while
  the primary Dev Container path already works
- **THEN** the fixer dismisses with practicality None and quotes Supported development environment
- **AND** does not apply step 5 merely because the suggested patch is cheap

#### Scenario: One-shot local migration finding is dismissed

- **WHEN** a finder asks to harden or parse a superseded personal on-disk format that is not the current write path
  (e.g. legacy token lines before `b64:`) and the author can fix it by re-running a documented setup command once
- **THEN** the fixer dismisses with practicality None
- **AND** does not add a compatibility parser, `eval` deny-list, or migration branch for that format

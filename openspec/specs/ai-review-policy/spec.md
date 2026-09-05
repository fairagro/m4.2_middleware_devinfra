# ai-review-policy Specification

## Purpose

Defines the canonical Finder/Fixer AI review policy and the shared Bugbot and Copilot entry files that load it for all
m4.2 product consumers.

## Requirements

### Requirement: Canonical AI review policy document

The repository MUST provide `docs/ai_review_policy.md` as the single Finder/Fixer policy for shared consumers. The
document MUST define Finder and Fixer roles, risk versus nit merge criteria, severity and practicality and cost
guidance, nit-budget rules, type-widening bans, and follow-up issue rules. Product-only API examples (specific routes,
datastores, or config types that are not shared) MUST NOT appear as normative requirements; shared vocabulary MUST be
used instead.

Nit-budget MUST be a **soft lifetime cap per PR** of approximately 15 new production lines for cheap nits (never a new
abstraction). It MUST NOT reset on each `/review-fixer` run and MUST NOT be gated on Copilot/Bugbot review round number.
Prior spend MUST be estimated by summing `nit-lines this run: N` markers already present in fixer replies on that PR.
Cheap fixes for regressions on the previous fixer pass MAY be fixed but MUST count toward the same PR total. Risk and
step-5 (cheap + High practicality + Medium+) findings MUST never be budgeted away and MUST NOT consume nit-line budget.
Nit `fix` replies MUST include `nit-lines this run: N`.

The policy MUST require `dismiss` (practicality None) when a finding’s only realistic path is outside the supported
Linux Dev Container environment (including BSD/non-GNU tool differences and host-only compatibility fallbacks), quoting
`openspec/principles.global.md` Supported development environment, and MUST NOT treat “cheap fix” as a reason to fix
those findings. GitHub Actions Linux CI remains in scope.

The policy MUST also require `dismiss` (practicality None) for findings that only harden a **one-shot local migration**
or ephemeral personal on-disk format that is not the current write path and not a shipped consumer contract (e.g.
pre-`b64:` personal token file lines fixable by re-running setup once). Finders MUST NOT comment on those; fixers MUST
NOT add compatibility parsers or deny-lists for them.

The policy MUST define a **surface quality bar** for fixer triage: product/domain code keeps the full bar; agent
plumbing (`scripts/ai/`, skill CLI wiring) is judged on the default Linux Dev Container skill/CLI happy path; exotic
argparse / option-injection / wording-only nits on that surface MUST be practicality Low (or None) and MUST NOT take
step 5 merely because the patch is cheap. Real happy-path breakage on agent plumbing MUST still be fixed.

#### Scenario: Contributor opens the shared policy

- **WHEN** a contributor opens `docs/ai_review_policy.md`
- **THEN** they find Finder and Fixer role definitions and the risk-versus-nit merge rule
- **AND** the document does not require API-only nouns as the only valid entry points

#### Scenario: Nit budget is a soft PR lifetime cap

- **WHEN** a fixer triages Low nits on a PR that already had earlier fixer nit fixes and a later Copilot/Bugbot review
  round
- **THEN** cheap nits may still be fixed only while prior `nit-lines this run` sums plus this run stay within ~15
- **AND** a new `/review-fixer` invocation does not reset that budget to a fresh ~15
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

#### Scenario: Agent-plumbing exotic CLI finding is dismissed

- **WHEN** a finder reports an agent-plumbing issue that only occurs with adversarial or non-default CLI args (e.g.
  `--base --all`) or is wording-only error-message polish
- **THEN** the fixer treats practicality as Low (or None) and dismisses or budgets as a nit
- **AND** does not apply step 5 merely because the suggested patch is cheap

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

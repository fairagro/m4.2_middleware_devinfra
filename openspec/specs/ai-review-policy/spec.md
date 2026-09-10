# ai-review-policy Specification

## Purpose

Defines the canonical Finder/Fixer AI review policy and the shared Bugbot and Copilot entry files that load it for all
m4.2 product consumers.

## Requirements

### Requirement: Canonical AI review policy document

The repository MUST provide `docs/ai_review_policy.md` as the single Finder/Fixer policy for shared consumers. The
document MUST define Finder and Fixer roles, risk versus nit merge criteria, severity and practicality and cost
guidance, nit-budget rules, type-widening bans, and follow-up issue rules. The merge criterion MUST be **no open risk**
findings. **Risk** MUST mean fixer triage severity Blocker/High with practicality not Low/None — not finder summary
banners and not a multiplicative severity×practicality score. The policy MUST define **Fixed non-nit this run** as the
per-invocation count of `fix` actions that are not nits (Risk step-4 fixes and step-5 cheap + High practicality +
Medium+ fixes; nit-budget fixes, dismissals, and follow-ups excluded). The policy MUST define a **review-cycle abort
criterion**: when the latest `/review-fixer` run reports **Fixed non-nit this run: 0**, the cycle MUST stop (no further
finder/`/review-fixer` loops solely for remaining comments, already-zero Remaining risk, or nit/dismiss-only outcomes);
when Fixed non-nit this run is ≥ 1, another finder pass MAY follow after fixes land. At most one deliberate nit-only
pass while nit-budget remains MAY run even when Fixed non-nit would be 0; afterward the same abort applies. Product-only
API examples (specific routes, datastores, or config types that are not shared) MUST NOT appear as normative
requirements; shared vocabulary MUST be used instead.

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

The policy MUST define a **surface quality bar** for fixer triage: product/domain code keeps the full bar; **shared
Devinfra scripts** (`scripts/` except `scripts/ai/` — quality helpers, CST runner, token/Dev Container scripts) are
judged on the documented Linux Dev Container and contributor/CI happy path **with contracted shared files as shipped**
(e.g. complete synced `versions.env`); **agent plumbing** (`scripts/ai/`, skill CLI wiring) is judged on the default
skill/CLI happy path. Exotic argparse / host-only / option-injection / wording-only nits on those non-product surfaces
MUST be practicality Low (or None) and MUST NOT take step 5 merely because the patch is cheap. The policy MUST state
**mechanical path ≠ realistic path**: code that can error when a required shared file is incomplete is not High
practicality when supported callers never ship that incomplete state; fixers MUST `dismiss` (practicality Low or None)
and MUST NOT add `REQUIRE_*` opt-in shims or dual modes solely for “caller deleted a contracted pin.” Real happy-path
breakage on shared scripts or agent plumbing MUST still be fixed (including consumer-sync failures such as hook
argv-length under `pre-commit run --all-files`, or check scripts that mutate contrary to contract). Findings that only
ask to **re-harden** an intentional happy-path simplification, add **host-only prerequisite docs**, or change
shared-hook **style** (`entry` vs `args`) without breaking the happy path MUST be dismissed.

Docs, OpenSpec prose, and code-comment clarifications MUST be severity **Low** (nit or dismiss) when the supported Dev
Container / CI commands and pass/fail gates already work — including inaccurate explanations of _how_ a gate is
implemented (e.g. Bandit `-ll` on hooks vs CI logging). Fixers MUST NOT treat “contributor might be confused” as Medium
“misleads operators” and MUST NOT take step 5 / count **Fixed non-nit** for those. Escalation to Medium+ for docs is
allowed only when the written instructions would make the supported path fail.

#### Scenario: Contributor opens the shared policy

- **WHEN** a contributor opens `docs/ai_review_policy.md`
- **THEN** they find Finder and Fixer role definitions and the risk-versus-nit merge rule
- **AND** the document does not require API-only nouns as the only valid entry points

#### Scenario: Fixed non-nit this run 0 aborts the review cycle

- **WHEN** the latest `/review-fixer` run reports Fixed non-nit this run: 0
- **THEN** the review cycle stops
- **AND** Copilot/Bugbot banners, Remaining risk already 0, or remaining dismissed/nit comments alone do not require
  another pass
- **AND** at most one deliberate nit-only pass remains allowed while nit-budget remains before the same abort applies

#### Scenario: Non-nit fixes allow another finder pass

- **WHEN** the latest `/review-fixer` run reports Fixed non-nit this run ≥ 1
- **THEN** the review cycle does not abort solely because Remaining risk is 0
- **AND** another finder pass MAY be requested after those fixes land

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

#### Scenario: Host-only prerequisite docs finding is dismissed

- **WHEN** a finder asks to document unofficial host prerequisites (e.g. `npm install`, `pre-commit` on `PATH`) while
  the Dev Container path already provides those tools or uses `uv run`
- **THEN** the fixer dismisses (practicality None or Low)
- **AND** does not treat the finding as step 5

#### Scenario: One-shot local migration finding is dismissed

- **WHEN** a finder asks to harden or parse a superseded personal on-disk format that is not the current write path
  (e.g. legacy token lines before `b64:`) and the author can fix it by re-running a documented setup command once
- **THEN** the fixer dismisses with practicality None
- **AND** does not add a compatibility parser, `eval` deny-list, or migration branch for that format

#### Scenario: Intentional simplification re-hardening is dismissed

- **WHEN** a finder asks to restore exotic `bashrc` marker repair, dual host token stores, or similar branches after the
  PR intentionally simplified the Dev Container happy path
- **AND** the documented Dev Container path still works
- **THEN** the fixer dismisses and does not re-introduce that hardening

#### Scenario: Shared Devinfra script exotic finding is dismissed

- **WHEN** a finder reports an issue in `scripts/` (outside `scripts/ai/`) that only matters for unofficial host
  installs or speculative edge hardening, while the documented Dev Container / quality-check / hook path works
- **THEN** the fixer treats practicality as Low (or None) and dismisses or budgets as a nit
- **AND** does not apply step 5 merely because the suggested patch is cheap

#### Scenario: Contract-violator-only incomplete shared config is dismissed

- **WHEN** a finder reports that shared plumbing can fail if a contracted shared file is incomplete (e.g. synced
  `versions.env` missing required pin keys) while this repo’s shipped contract already defines those keys for supported
  callers
- **THEN** the fixer treats practicality as Low or None and dismisses
- **AND** does not add an opt-in `REQUIRE_*` flag or dual validation mode solely for that hypothetical incomplete state
- **AND** does not apply step 5 or spend nit-budget on that hardening

#### Scenario: Agent-plumbing exotic CLI finding is dismissed

- **WHEN** a finder reports an agent-plumbing issue that only occurs with adversarial or non-default CLI args (e.g.
  `--base --all`) or is wording-only error-message polish
- **THEN** the fixer treats practicality as Low (or None) and dismisses or budgets as a nit
- **AND** does not apply step 5 merely because the suggested patch is cheap

#### Scenario: Docs clarification stays Low (not step 5)

- **WHEN** a finder reports inaccurate docs or comments about quality tooling (e.g. claiming hooks and CI both use
  Bandit `-ll`) while the supported commands and MEDIUM/HIGH fail bar already match reality
- **THEN** the fixer assigns severity Low and treats the item as a nit or dismisses it
- **AND** does not take step 5 or count Fixed non-nit solely for that clarification
- **AND** does not classify it as Medium via “misleads operators”

### Requirement: Surface quality bar path map files

The repository MUST provide `docs/surface-quality-bar.global.md` as the synced default **path→surface** map for the
surface quality bar (typical paths, bar, exotic-edge default per surface). `docs/ai_review_policy.md` MUST keep the
triage **rules** that describe how the bar affects fixer step 5, nit-budget, and dismiss behaviour, and MUST point
readers to `docs/surface-quality-bar.global.md` plus an optional product-local overlay at `docs/surface-quality-bar.md`.
Sync of the shared policy and of `surface-quality-bar.global.md` MUST NOT overwrite a product’s
`docs/surface-quality-bar.md`. Consumers MUST NOT need to edit `docs/ai_review_policy.md` solely to add or adjust a
path→surface row.

#### Scenario: Contributor opens the default path map

- **WHEN** a contributor opens `docs/surface-quality-bar.global.md` in Devinfra or after sync into a product repo
- **THEN** they find the default path→surface table (or equivalent map) for shared surfaces
- **AND** they learn that product-specific path rows belong in `docs/surface-quality-bar.md`, not in the synced policy
  body

#### Scenario: Product extends the map without editing the policy

- **WHEN** a product repo needs an additional path→surface row (e.g. a local package layout)
- **THEN** it MAY add that row in local `docs/surface-quality-bar.md`
- **AND** it MUST NOT need to hand-edit synced `docs/ai_review_policy.md` or synced `docs/surface-quality-bar.global.md`
  for that extension

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

### Requirement: Sync source of truth overrides cheap fix for synced paths

The AI review policy MUST state that for paths listed in `docs/synced-paths.yaml`, **sync source of truth**
overrides the usual “cheap + High practicality + Medium+ → `fix` in this PR” step. In a product consumer checkout,
fixers MUST NOT treat a correct cheap patch on a synced path as an in-PR `fix`; they MUST `follow-up` to Devinfra or
`dismiss` (synced — edit upstream) per the review-fixer synced-path rule, or `fix` only a documented product-local
overlay. The policy MUST link to `docs/synced-paths.yaml` (and MAY cross-link the surface quality bar path map).

#### Scenario: Cheap synced-path finding is not step-5 in a consumer

- **WHEN** a fixer applies triage to a correct, cheap, High-practicality Medium finding on a synced path in a product
  repo
- **THEN** the policy forbids treating that item as an in-PR `fix` of the synced file
- **AND** directs `follow-up` / `dismiss` / overlay-only `fix` instead
- **AND** cites `docs/synced-paths.yaml` as the allowlist

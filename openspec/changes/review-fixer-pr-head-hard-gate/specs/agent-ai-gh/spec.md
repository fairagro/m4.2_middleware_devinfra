## MODIFIED Requirements

### Requirement: review-open ensures PR head checkout

Before emitting open-work JSON, `review-open` MUST resolve the PR head ref name, ensure the local checkout is that
branch (fetch + checkout when needed), and include `head_ref`, `current_branch`, `ok: true`, and `pr_head_ok: true` in
success JSON. When the working tree/index is dirty and the current branch is **not** the PR head, the CLI MUST refuse
with non-zero exit and structured error JSON including at least `ok: false`, `pr_head_ok: false`,
`error_code: "dirty_wrong_branch"`, `error`, `agent_action: "stop"`, plus `head_ref` / `current_branch` when known.
Dirty state **on** the PR head MUST be allowed. When the head cannot be checked out, the CLI MUST fail closed with
structured error JSON (`error_code` one of `empty_head_ref`, `checkout_failed`, `checkout_branch_mismatch`) — no partial
silent continue on another branch. `agent_action: "stop"` means agents MUST NOT stash, force-checkout, or otherwise
improvise around the failure.

#### Scenario: Wrong-branch dirty refuses

- **WHEN** `review-open` runs and the working tree is dirty on a branch other than the PR head
- **THEN** the process exits non-zero with structured error JSON (`error_code` `dirty_wrong_branch`, `agent_action`
  `stop`)
- **AND** it does not change the current branch

#### Scenario: Checkout succeeds and JSON includes head

- **WHEN** `review-open` runs on a clean tree (or dirty tree already on the PR head) and the PR head is checkoutable
- **THEN** the local checkout is the PR head branch
- **AND** the emitted JSON includes that branch name with `ok` and `pr_head_ok` true
- **AND** open-work shaping still runs as before

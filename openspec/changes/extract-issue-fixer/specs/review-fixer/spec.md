# review-fixer Delta

## ADDED Requirements

### Requirement: Thin docs page matches sibling skills

The repository MUST provide `docs/review-fixer.md` as a thin human index that links
`.agents/skills/review-fixer/SKILL.md` and `docs/ai_review_policy.md`, and summarizes open-work-only triage and that the
agent does not commit or push (user commits; Fixed replies use that SHA). The root `README.md` Docs section MUST link
this page using the same pattern as `docs/create-issue.md` and `docs/issue-fixer.md`.

#### Scenario: Contributor looks up review-fixer docs

- **WHEN** a contributor opens the root README Docs section for review-fixer
- **THEN** they find a link to `docs/review-fixer.md`
- **AND** that page points at the skill and the AI review policy

## MODIFIED Requirements

### Requirement: README indexes review-fixer

The root `README.md` MUST mention the shared `/review-fixer` artifacts among synced agent paths (skill and/or command)
so consumers know not to diverge locally, and MUST index the skill in Docs and layout consistently with `/create-issue`
and `/issue-fixer` (including the thin docs page).

#### Scenario: Consumer finds review-fixer ownership

- **WHEN** a contributor reads the root README layout or Docs section
- **THEN** they learn that review-fixer skill/command/prompt are canonical shared content
- **AND** they find `docs/review-fixer.md` in the Docs index (or equivalent)

### Requirement: Follow-up issues use create-issue

When opening at most one follow-up issue for Medium+ deferred items, the skill MUST instruct agents to read and follow
`.agents/skills/create-issue/SKILL.md` (org issue type, allowlisted triage labels, body template, Auth, relation). Title
MUST be `Follow-up from PR #<pr_number> AI review`. Low nits MUST NOT become issues. The skill MUST NOT use a separate
inline-only `gh issue create` template that bypasses create-issue. Relation MUST be `linked` by default (standalone
issue with Links to the PR). Relation MUST be `sub-of #<issue_number>` only when the PR body includes
`Fixes #<issue_number>` (or equivalent) and the deferred item is clearly remaining acceptance criteria of that issue.
When unclear, prefer `linked`.

#### Scenario: Medium+ deferral opens one create-issue follow-up

- **WHEN** the fixer defers at least one Medium+ item
- **THEN** the skill directs opening one issue via the create-issue procedure
- **AND** Low-only nits still do not become issues

#### Scenario: Default follow-up is linked not sub-issue

- **WHEN** the fixer opens a Medium+ follow-up that is not remaining acceptance criteria of a `Fixes #<issue_number>`
  issue
- **THEN** create-issue is invoked with `relation: linked`
- **AND** the new issue is not attached as a GitHub sub-issue of an unrelated parent

#### Scenario: Remaining Fixes scope uses sub-of

- **WHEN** the PR body includes `Fixes #42` and a Medium+ deferred item is clearly remaining acceptance criteria of #42
- **THEN** create-issue is invoked with `relation: sub-of #42`

#### Scenario: create-issue missing in consumer checkout

- **WHEN** create-issue artifacts are absent
- **THEN** the skill tells the agent to report that and print intended create-issue inputs
- **AND** it still MUST NOT invent off-allowlist labels or a parallel create path

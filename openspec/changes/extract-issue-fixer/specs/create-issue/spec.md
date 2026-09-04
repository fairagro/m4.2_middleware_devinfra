# create-issue Delta

## ADDED Requirements

### Requirement: issue-fixer may invoke create-issue for split sub-issues

The skill MUST accept invocation from `/issue-fixer` with pre-filled split-slice fields (title, type, triage, problem,
why-not-now, acceptance criteria, links, and `relation: sub-of #<issue_number>`) without re-running issue-fixer explore
or implementation. Each invocation creates one issue. Typical types are `Refactoring` or `Task`; other org types remain
allowed when the slice warrants them. For issue-fixer splits that are part of the parent’s acceptance criteria, relation
MUST be `sub-of` that parent.

#### Scenario: issue-fixer hands off a split slice

- **WHEN** issue-fixer requests one sub-issue for a deferred independent block with type, triage, and
  `relation: sub-of #<issue_number>`
- **THEN** create-issue creates that issue using its type/label/body rules and attaches it as a GitHub sub-issue of the
  parent
- **AND** it does not explore or implement the parent issue

### Requirement: Caller relation sub-of versus linked

When a caller supplies a relation, create-issue MUST apply it as follows:

- `sub-of #<issue_number>` (or equivalent): create the issue as a GitHub native sub-issue of that parent (e.g.
  `gh issue create --parent`), and still include the parent under Links in the body.
- `linked` (default when omitted or unclear): create a standalone issue; put the source issue and/or PR under Links only
  — MUST NOT set a GitHub parent.

If native sub-issue attachment fails **before** any issue is created (unsupported `gh`, permissions, or API error with
no issue URL), the skill MUST fall back to **one** linked issue (body Links), report the failure, and MUST NOT invent a
second create path outside create-issue. If create already produced an issue URL/number and a later step fails (labels,
type, parent mutation), the skill MUST NOT create again — it MUST report the partial failure and return the existing
URL.

#### Scenario: sub-of attaches parent

- **WHEN** create-issue is invoked with `relation: sub-of #42`
- **THEN** it creates the issue as a sub-issue of #42
- **AND** the issue body still links #42

#### Scenario: linked does not set parent

- **WHEN** create-issue is invoked with `relation: linked` and a source PR or issue URL
- **THEN** it creates a standalone issue with Links to that source
- **AND** it does not set a GitHub parent

#### Scenario: no duplicate create after partial failure

- **WHEN** `gh issue create` (with or without `--parent`) already returned an issue URL
- **AND** a later step fails
- **THEN** create-issue does not open a second issue
- **AND** it reports the partial failure with the existing URL

## MODIFIED Requirements

### Requirement: Docs index issue types and triage labels

The root README and/or linked docs MUST document the six org issue types and the triage label families (including
create-if-missing allowlist behavior) so consumers know what `/create-issue` expects. Docs MUST note that
`/review-fixer` and `/issue-fixer` open follow-up or split issues via this skill, and MUST document the **sub-of vs
linked** relation rule (split of parent acceptance criteria → sub-issue; distinct follow-up problem → linked).

#### Scenario: Contributor looks up create-issue conventions

- **WHEN** a contributor reads the root README Docs or layout section for issue creation
- **THEN** they find the org issue types and triage label families
- **AND** they learn that allowlisted missing labels are created on demand by the skill
- **AND** they learn that `/review-fixer` and `/issue-fixer` use create-issue for deferred issues
- **AND** they learn when create-issue uses a native sub-issue versus a linked standalone issue

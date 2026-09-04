# create-issue Delta

## ADDED Requirements

### Requirement: issue-fixer may invoke create-issue for split sub-issues

The skill MUST accept invocation from `/issue-fixer` with pre-filled split-slice fields (title, type, triage, problem,
why-not-now, acceptance criteria, links to parent issue and/or PR) without re-running issue-fixer explore or
implementation. Each invocation creates one issue. Typical types are `Refactoring` or `Task`; other org types remain
allowed when the slice warrants them.

#### Scenario: issue-fixer hands off a split slice

- **WHEN** issue-fixer requests one sub-issue for a deferred independent block with type and triage fields
- **THEN** create-issue creates that issue using its type/label/body rules
- **AND** it does not explore or implement the parent issue

## MODIFIED Requirements

### Requirement: Docs index issue types and triage labels

The root README and/or linked docs MUST document the six org issue types and the triage label families (including
create-if-missing allowlist behavior) so consumers know what `/create-issue` expects. Docs MUST note that
`/review-fixer` and `/issue-fixer` open follow-up or split issues via this skill.

#### Scenario: Contributor looks up create-issue conventions

- **WHEN** a contributor reads the root README Docs or layout section for issue creation
- **THEN** they find the org issue types and triage label families
- **AND** they learn that allowlisted missing labels are created on demand by the skill
- **AND** they learn that `/review-fixer` and `/issue-fixer` use create-issue for deferred issues

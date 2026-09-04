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

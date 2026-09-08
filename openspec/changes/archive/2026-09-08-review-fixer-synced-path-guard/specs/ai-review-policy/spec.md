# ai-review-policy Delta

## ADDED Requirements

### Requirement: Sync source of truth overrides cheap fix for synced paths

The AI review policy MUST state that for paths listed in `docs/synced-paths.global.md`, **sync source of truth**
overrides the usual “cheap + High practicality + Medium+ → `fix` in this PR” step. In a product consumer checkout,
fixers MUST NOT treat a correct cheap patch on a synced path as an in-PR `fix`; they MUST `follow-up` to Devinfra or
`dismiss` (synced — edit upstream) per the review-fixer synced-path rule, or `fix` only a documented product-local
overlay. The policy MUST link to `docs/synced-paths.global.md` (and MAY cross-link the surface quality bar path map).

#### Scenario: Cheap synced-path finding is not step-5 in a consumer

- **WHEN** a fixer applies triage to a correct, cheap, High-practicality Medium finding on a synced path in a product
  repo
- **THEN** the policy forbids treating that item as an in-PR `fix` of the synced file
- **AND** directs `follow-up` / `dismiss` / overlay-only `fix` instead
- **AND** cites `docs/synced-paths.global.md` as the allowlist

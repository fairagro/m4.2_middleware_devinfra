## ADDED Requirements

### Requirement: Container Structure Tests follow versions.env CST_VERSION

When `reusable-check.yml` runs Container Structure Tests with `skip` false, the workflow MUST obtain `CST_VERSION` from
the **caller** repository checkout’s repo-root `versions.env` and MUST run the official `container-structure-test`
release binary at that version against the loaded image and caller CST config. The workflow MUST fail closed with a
clear error when `CST_VERSION` is missing or empty. It MUST NOT rely solely on a third-party Action’s opaque bundled CST
binary for the scanned tool version. Documentation (`docs/ci.md`) MUST state that CI CST follows `versions.env` /
Renovate independently of any Action tag/SHA.

#### Scenario: CST uses versions.env pin

- **WHEN** a product calls `reusable-check.yml` with `skip: false` and the caller checkout has a non-empty `CST_VERSION`
  in `versions.env`
- **THEN** Container Structure Tests execute with that release binary against the loaded component image and config

#### Scenario: Missing CST_VERSION fails closed

- **WHEN** `skip` is false and `CST_VERSION` is missing or empty in the caller `versions.env`
- **THEN** the Container Structure Tests job fails before or at CST invocation with an error naming `CST_VERSION` /
  `versions.env`

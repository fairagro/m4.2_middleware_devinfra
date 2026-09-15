## ADDED Requirements

### Requirement: Reusable code-quality runs Prettier and markdownlint

When `skip` is false, `reusable-code-quality.yml` MUST install a Node toolchain suitable for the caller’s `package.json`
engines (or documented pin), run `npm ci` in the caller checkout, and run `npm run format:md:check` and
`npm run lint:md` (or equivalent scripts that invoke the same shared Prettier/markdownlint configs as commit-stage
hooks). Missing `package.json` / lockfile MUST fail the job (fail closed). These steps MUST use the shared
`.prettierrc*` / `.markdownlint*` configs from the caller tree and MUST NOT introduce a divergent markdown policy for
CI.

#### Scenario: Markdown gates run on non-skip code-quality

- **WHEN** a product workflow calls reusable code-quality with `skip: false` and the caller has synced `package.json`,
  lockfile, and markdown configs
- **THEN** the job runs Prettier check and markdownlint with those shared configs
- **AND** a formatting or lint finding fails the job

#### Scenario: Missing Node manifest fails closed

- **WHEN** reusable code-quality runs with `skip: false` and the caller checkout lacks `package.json` or lockfile
- **THEN** the job fails with a clear error
- **AND** it does not silently skip markdown checks

## MODIFIED Requirements

### Requirement: Reusable code-quality workflow

The repository MUST provide `.github/workflows/reusable-code-quality.yml` callable via `workflow_call`. It MUST install
the caller’s Python toolchain from the caller checkout’s `versions.env` via `scripts/load-versions-env.sh` (callers that
sync `versions.env` MUST also sync that script) and run the shared quality bar (format/lint type-check, Bandit with
medium/high fail policy, pytest, and Prettier/markdownlint check scripts) against a configurable package root (Python)
plus repository Markdown via npm scripts. It MUST accept a boolean `skip` input that still runs the workflow job
successfully with a no-op path when true (so required status checks are not left pending). The default Code Quality job
display name MUST remain `Code Quality Check (3.12)` for branch-ruleset compatibility unless a later change explicitly
migrates consumers.

#### Scenario: Product calls code-quality with package root

- **WHEN** a product workflow calls `fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-code-quality.yml` at a
  branch or tag ref with `skip: false` and a package-root input
- **THEN** the reusable job checks out the **caller** repository
- **AND** runs quality checks against that package root using the caller’s `versions.env` Python pin
- **AND** runs Prettier/markdownlint check scripts from the caller’s Node manifest
- **AND** the job reports under the name `Code Quality Check (3.12)`

#### Scenario: Skip no-op for required checks

- **WHEN** the caller passes `skip: true`
- **THEN** the reusable code-quality job completes successfully without running substantive lint/test steps

# Design: quality tools environment parity

## Context

See proposal.md — Why. Fragments (`ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`, markdownlint) and three runners (IDE
via `.vscode/settings.json`, pre-commit, reusable `code-quality` workflow) already exist after the shared quality config
layer. Parity is mostly true for Ruff; Mypy/Pylint/Bandit IDE coverage and any extra CLI flags need an audit against the
new requirement.

## Goals / Non-Goals

**Goals:**

- Normative three-environment + minimal-CLI rules in specs and `principles.global.md`
- Docs that state the rule clearly for adopters
- Close concrete parity gaps found in the audit (config pointer or policy-on-CLI only)

**Non-Goals:**

- New quality tools or changing rule severity content inside fragments
- Guaranteeing bit-identical log text across IDE vs CLI (only gate outcome / findings parity)
- Forcing every IDE language server to run Bandit/Pylint if the extension ecosystem has no supported equivalent — then
  document “CLI/hook/CI only” for that tool while still requiring the three environments that _do_ run it to match; if a
  tool cannot run in the IDE at all, document that exception explicitly rather than silently drifting CLI vs CI

## Decisions

### D1 — Home capability is `shared-quality-tooling`

Cross-cutting parity lives there; `shared-python-quality-config` only tightens Python fragments; `global-principles`
mirrors the rule into `principles.global.md` for human/agent discovery.

**Alternatives:** New capability `quality-env-parity` — rejected (extra surface for one requirement cluster).

### D2 — “Matching results” means gate outcome, not log identity

Pass/fail and the set of policy violations (rule id + location) must match. Formatting of messages may differ (IDE
diagnostics vs CLI).

### D3 — Allowed CLI extras

Whitelist: config-file path flags, target paths, product path overlays (`MYPYPATH`, `--source-roots`). Everything else
that is expressible in the config file belongs in the file. Hook `entry` vs `args` placement of the config path is
style-only if the executed argv is equivalent.

### D4 — IDE gaps

Prefer pointing extensions at the same fragment (as Ruff already does). If no maintained IDE integration exists for a
tool, document “hooks + CI only” for that tool under the parity section rather than inventing a second config channel.

## Risks / Trade-offs

- [Strict minimal-CLI] → Some tools historically need one-off CLI flags with no config key → Mitigation: document a
  named exception in `docs/quality.md` when unavoidable; prefer upstream config support.
- [IDE cannot run Bandit/Pylint] → Apparent “two environments only” → Mitigation: D4 documentation; still require
  hook/CI parity for those tools.

## Migration Plan

1. Land specs + principles + docs.
2. Audit and patch invocations in the same PR/change apply.
3. Product sync (#13) picks up docs/principles; no forced product CLI rewrite beyond what sync already does for
   fragments/hooks.

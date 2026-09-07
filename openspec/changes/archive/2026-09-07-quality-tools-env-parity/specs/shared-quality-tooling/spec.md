# shared-quality-tooling Delta

## ADDED Requirements

### Requirement: Three-environment quality parity

Every shared quality tool that gates commits or CI for this repository or for synced product consumers (at least: Ruff
format/lint, Mypy, Pylint, Bandit, markdownlint/Prettier where applicable, and pytest when configured as a quality gate)
MUST be runnable in all three environments:

1. **IDE** — workspace / extension settings that invoke the same tool binary family and the same shared config file(s)
2. **Git hooks** — pre-commit (commit stage) and, where the tool is a pre-push gate, the pre-push stage
3. **GitHub pipelines** — reusable or caller workflows that run the shared quality bar

For the same repository tree, the same toolchain pins (`versions.env` / `uv sync` / documented Node toolchain), and the
same target paths, the **pass/fail outcome and substantive findings** MUST match across those three environments.
Divergent severity, rule sets, or config files between IDE, hooks, and CI are forbidden unless a documented exception
exists (none by default).

Shared **config files** (e.g. `ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`, markdownlint/Prettier configs) MUST be
the single source of truth for tool policy. Invocations (CLI, hook `entry`/`args`, CI steps, IDE settings) MUST pass at
most: the path to the shared config file when the tool does not auto-discover it, the analysis target path(s), and
product-local path overlays that cannot live in synced fragments (e.g. `MYPYPATH`, pylint `--source-roots`). They MUST
NOT pass additional command-line (or IDE-equivalent) flags that restate or override policy already expressible in the
shared config file (line length, rule selects, ignore lists, severity thresholds, Python version pins, and similar).

Documentation (`docs/quality.md` and/or Code Quality in `openspec/principles.global.md`) MUST state this three-
environment parity rule and the minimal-CLI rule.

#### Scenario: Same tree fails or passes consistently

- **WHEN** a contributor runs the shared quality bar via IDE-integrated checks, via pre-commit (or `quality-check.sh`),
  and via the reusable code-quality GitHub workflow against the same tree and pins
- **THEN** each environment uses the same shared config file(s) for that tool
- **AND** the gate outcome (pass vs fail on policy findings) is the same across the three

#### Scenario: Invocations do not restate config policy on the CLI

- **WHEN** a consumer inspects shared pre-commit entries, reusable CI quality steps, and IDE tool settings for a gated
  quality tool
- **THEN** those invocations reference the shared config file path (when required) and target paths / allowed path
  overlays only
- **AND** they do not add CLI or IDE flags that duplicate policy already defined in that config file

## Context

[#91](https://github.com/fairagro/m4.2_middleware_devinfra/issues/91). Pre-commit, reusable-code-quality, and
`openspec/principles.global.md` already use `ruff.toml`. Only the two Fixer skills still say `pyproject.toml`.

## Goals / Non-Goals

**Goals:** Align skill Ruff commands with `ruff.toml` SoT.

**Non-Goals:** Changing Ruff config contents; product-only edits; new quality fragments.

## Decisions

1. Replace `--config pyproject.toml` with `--config ruff.toml` in both skills (same bar as pre-commit / CI).
2. `skip_specs: true` — no capability requirement text encodes the old flag; contract already lives in quality specs /
   principles.

## Risks / Trade-offs

- [None material] — matches existing fleet practice.

## Migration Plan

Land in Devinfra → sync skills to products.

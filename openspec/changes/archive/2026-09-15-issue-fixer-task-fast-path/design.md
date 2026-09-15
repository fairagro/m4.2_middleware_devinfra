## Context

Main `openspec/specs/issue-fixer/spec.md` still says `/issue-fixer` never runs OpenSpec, while the live skill (and
unarchived change `issue-fixer-opsx-for-tasks`) already route **Task** through OpenSpec.
[#125](https://github.com/fairagro/m4.2_middleware_devinfra/issues/125) locks **Variant 1**: Task = Bug fast path;
Feature/Refactoring keep OpenSpec.

## Goals / Non-Goals

**Goals:**

- Encode Task fast path + Feature/Refactoring OpenSpec in skill, thin docs, and specs
- Align create-issue Task wording with that routing
- Drop the conflicting open change folder

**Non-Goals:**

- Cost-based OpenSpec routing
- Changing Feature/Refactoring cadence or explore rules
- Retyping historical issues

## Decisions

1. **Task / Bug / cheap Security → fast path** — no OpenSpec unless user override `use opsx`.
2. **Feature / Refactoring → OpenSpec** — except clearly docs-only Markdown/MDC/comments with no skill file in scope.
3. **Skill file in scope → OpenSpec** — even if typed Task (agent procedure is a contract).
4. **Misfiled Task** that clearly changes an `openspec/specs/` capability → pause once; do not silently invent a change
   folder.
5. **Abandon `issue-fixer-opsx-for-tasks`** by deleting the open change directory; this change is the SoT for routing.

## Risks / Trade-offs

- [Misfiled Feature as Task skips OpenSpec] → Mitigation: create-issue wording + misfile pause when specs capability
  clearly changes.
- [Conflicting open change left around] → Mitigation: delete `issue-fixer-opsx-for-tasks` in this PR.

## Migration Plan

1. Land this change on `issue-125-task-fast-path`.
2. Consumers pick up skills on next sync.
3. Prefer typing new capability work as `Feature` (optional note in PR).

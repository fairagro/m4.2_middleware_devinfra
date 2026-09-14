# issue-fixer OpenSpec routing — Design

## Context

See proposal.md for motivation. Today `openspec/specs/issue-fixer/spec.md` forbids OpenSpec for `/issue-fixer`. Explore
is already in-skill. Guardrails to keep: `issue-<n>-<slug>`, no auto-commit, draft PR only when `main..HEAD` is
non-empty, no empty bootstrap, sibling skills off OpenSpec. Skill files are Devinfra source of truth and already on the
sync allowlist.

## Goals / Non-Goals

**Goals:**

- Encode the locked type routing and `go` cadence in the skill, thin docs/command/prompt, and the `issue-fixer` spec
- Embed OpenSpec by **following** existing opsx skills (not a second copy of their steps)

**Non-Goals:**

- Rewriting the OpenSpec CLI
- Requiring `/opsx-explore`
- Changing `/review-fixer` or `/create-issue`
- Changing `m42-ai issue-start` / `issue-branch` contracts

## Decisions

- **Embed vs handoff:** Follow `.cursor/skills/openspec-propose/SKILL.md` (and apply/archive) in the same `/issue-fixer`
  run. Alternative: stop and ask the user to invoke `/opsx-propose` — worse UX and easy to skip.
- **Explore stays in-skill:** Propose artifacts capture lock-in. Alternative: `/opsx-explore` — extra hop, not needed.
- **Branch first:** `issue-branch` before propose so the change folder lives on `issue-<n>-<slug>`. OpenSpec change name
  is independent kebab-case under `openspec/changes/`.
- **Draft PR before archive:** Archive is the last `go` so the PR already exists when specs fold into main; the user
  commits archive output as further commits on the same PR. Alternative: archive before `issue-start` — then the last
  `go` would not be archive.
- **`skip_specs`:** Default to a real delta when a capability contract changes; `skip_specs: true` only for docs/tooling
  with no spec delta.
- **User override:** Explicit “use opsx” on a Bug or “skip openspec” on a Task wins over the type default.

## Risks / Trade-offs

- **[Risk] Agents skip propose and implement anyway** → Mitigation: skill + command + prompt + spec all state the type
  table and pauses; Bug path remains the only no-OpenSpec default.
- **[Risk] Archive `go` with no commits ahead of `main`** → Mitigation: draft-PR step already stops and asks for a
  commit; archive still runs on the working tree and pauses for another commit.
- **[Risk] Products fork the skill** → Mitigation: allowlist already syncs `.agents/skills/issue-fixer/**`; docs say
  Devinfra is SoT.
- **[Trade-off] Archive after draft PR** means a second human commit on the PR. Accepted: matches “last `go`” and keeps
  auto-commit forbidden.

## Migration Plan

- Land skill/docs/spec in this repo; consumers get them on next sync. No runtime migration. Rollback is reverting the
  skill files.

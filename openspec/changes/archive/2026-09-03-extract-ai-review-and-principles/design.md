# Extract AI review policy and global principles — Design

## Context

See proposal.md for motivation. Source of truth today: `fairagro/m4.2_advanced_middleware_api` —
`docs/ai_review_policy.md`, `.cursor/BUGBOT.md`, `.github/copilot-instructions.md`, and `openspec/principles.md`.
sql_to_arc and harvester lack the policy files and use `openspec/specs/principles/` instead of a root `principles.md`.
Epic #1 listed OpenSpec trees as local; this change narrows that: **specs/changes stay local**; **principles base is
shared**.

## Goals / Non-Goals

**Goals:**

- Land canonical policy + both Finder entries + `principles.global.md` in one change so citations do not break
- Cite Supported environment / Type Safety **directly** at `openspec/principles.global.md`
- Keep Copilot shared entry thin (Finder → policy), not a dump of product `AGENTS.md`

**Non-Goals:**

- Extracting `/review-fixer` (#5), vendor skills (#6), or sync automation (#13)
- Converting Devinfra into an OpenSpec store / `references:` setup
- Rewriting product repos' `openspec/specs/principles/` in this PR (Wave A adoption)
- Shipping product-local `AGENTS.md` or full Copilot stack notes from the API

## Decisions

### 1. Same change for policy and principles.global

- **Choice:** One change covering issue #4 expanded (policy, Bugbot, Copilot, global principles)
- **Alternatives:** Separate principles issue after #4
- **Why:** Policy already depends on principles citations; splitting would leave broken or API-shaped paths between PRs

### 2. Direct citations to principles.global.md

- **Choice:** Shared policy and Finder docs name `openspec/principles.global.md` for Supported env / Type Safety
- **Alternatives:** Cite only repo-local `principles.md` that includes global
- **Why:** Robust against local drift; dismissals quote the immutable shared section

### 3. Two-file principles pattern

- **Choice:** Synced `openspec/principles.global.md` + repo-local `openspec/principles.md` that points at `.global`
- **Alternatives:** OpenSpec Stores + `references:`; single merged file with shared/product sections;
  `principles.local.md` beside an unchanged `principles.md`
- **Why:** Matches sync ownership (global = do not edit; local = extend). Keeps the familiar `principles.md` name as the
  product entry while making the shared base explicit. Stores remain optional later for true cross-repo specs.

### 4. What belongs in principles.global.md

- **Include:** Values (shared), Supported development environment, Type Safety core, code-quality gates + `uv`, no
  direct `os.environ` in application code, trunk-based branch strategy if it is truly shared, generic spec/code naming
  hints that do not name product modules
- **Exclude:** FastAPI/Celery/Couch/Rabbit stack table, API module dependency graph, API test path layout, scaling /
  pickle notes, `ConfigWrapper`/`UrlStr` API specifics (local `principles.md` or product skills)

### 5. Strip API-only examples from the policy

- **Choice:** Keep Finder/Fixer machinery; generalize entry points (public HTTP route / worker task / default config)
  and production-size path (`middleware/*/src/` already matches path-conventions)
- **Why:** Issue #4 asks to strip API-only examples; other consumers must not inherit Couch/Celery-only language as
  normative

### 6. Shared Copilot entry is Finder-only

- **Choice:** `.github/copilot-instructions.md` ≈ Bugbot stub: review as Finder → `docs/ai_review_policy.md`; optional
  one-liner to read `openspec/principles.global.md` for Type Safety / supported env when writing or reviewing
- **Alternatives:** Copy full API Copilot file (AGENTS, ConfigWrapper, uv essay)
- **Why:** Product `AGENTS.md` stays local per epic; shared file must not require it

### 7. Devinfra local principles.md

- **Choice:** Thin file: points at `.global`, notes this repo has no product `middleware/` packages, may add
  Devinfra-only markdown/toolchain notes if needed
- **Why:** Same pattern consumers will use; agents have a stable entry path

## Risks / Trade-offs

- **[Risk] sql_to_arc/harvester keep `specs/principles/` and also get `principles.md`** → Mitigation: Wave A documents
  that capability specs may specialize; global file owns cross-cutting env/types; adoption issues reconcile duplication
- **[Risk] Over-thin Copilot entry loses useful API habits** → Mitigation: habits stay in product AGENTS / local
  principles; shared review behavior is the extract goal
- **[Trade-off] Epic text still says OpenSpec out of scope** → Mitigation: README clarifies specs/changes local,
  principles base shared; update epic issue text separately if desired
- **[Risk] Content drift while copying from API** → Mitigation: human review once (issue done-when); prefer verbatim
  shared sections over rewrite

## Migration Plan

1. Add files in Devinfra only (this change)
2. Consumers adopt via Wave A sync / PRs later — out of this change
3. Rollback = revert the Devinfra commit; no runtime deploy

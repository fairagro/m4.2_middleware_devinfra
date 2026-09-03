# Extract review-fixer and personal-token helpers — Design

## Context

See proposal.md. Combines issue #8 (full) and issue #5. Explore lock-ins for #8: `PRODUCT_SLUG` only (no basename map);
full wrappers; **Kombi** shell/postCreate load of stored tokens **plus** PATH wrappers; both `GH_TOKEN` and
`GITGUARDIAN_API_KEY`; empty-skip / `scripts/bin` PATH / no worktree tokens. #5: Variante A, inline follow-up, Done =
files + content ok. #4 already landed policy and `principles.global.md`.

## Goals / Non-Goals

**Goals:**

- Complete #8: tokens + `gh`/`git` wrappers + PATH + shell/postCreate load of stored tokens + empty-skip docs
- Complete #5: skill + Cursor command + Copilot prompt, Auth pointing at shared `gh` + conventions
- Keep GraphQL plumbing in the skill for now (Variante A)

**Non-Goals:**

- #16 `review-open` CLI refactor
- #14 create-issue skill
- #6 vendor skills, #7 quality scripts, #9 hooks/LFS
- Product-repo PR smoke test of `/review-fixer` in this Devinfra change
- Inferring product slug from directory/remote names

## Decisions

### 1. One change for #8 then #5

- **Choice:** Single change; implement token helpers before the skill so Auth text is real
- **Why:** User intent; avoids a skill that documents missing scripts

### 2. Product slug = PRODUCT_SLUG only

- **Choice:** Host path `~/.config/<slug>/tokens.env` uses `PRODUCT_SLUG` from the environment. If `/commandhistory` is
  absent and `PRODUCT_SLUG` is unset/empty, helpers MUST fail with a clear error (do not guess). This Dev Container sets
  `PRODUCT_SLUG=middleware-devinfra` (e.g. `containerEnv`). Consumers set their own slug in overlays.
- **Alternatives:** Basename map; default slug in script
- **Why:** User lock-in; explicit ownership per product overlay

### 3. Kombi: shell/postCreate load + wrappers

- **Choice:**
  - **Load path:** postCreate and/or interactive shell profile sources `dev-tokens.sh` so _already stored_ non-empty
    tokens are exported into the environment (no hang when there is no TTY — skip prompting in non-TTY load).
  - **Wrapper path:** Keep `scripts/bin/gh` and `scripts/bin/git` on `PATH` for Agent/non-login shells, TTY re-prompt
    when appropriate, fail guidance to `set-dev-tokens.sh`, and Cursor `core.hooksPath=/dev/null` stripping on git.
- **Alternatives:** Wrappers only (API today); Env-only without wrappers
- **Why:** Human terminals get tokens early; agents and Cursor SCM still need wrappers

### 4. Both personal token variables

- **Choice:** Prompt/persist `GH_TOKEN` and `GITGUARDIAN_API_KEY` (same empty-skip rules)
- **Why:** User lock-in; prepares #6 scan-secrets without a second token extract

### 5. Empty-skip semantics (from API)

- **Choice:** Empty TTY → persist skip; `set-dev-tokens.sh` forces re-prompt; no hang without TTY
- **Why:** Issue #8 done-when; confirmed

### 6. PATH via remoteEnv

- **Choice:** `remoteEnv.PATH` = `${workspaceFolder}/scripts/bin:${containerEnv:PATH}`
- **Why:** Matches API; required for wrappers

### 7. Review-fixer Variante A

- **Choice:** Copy API skill procedure including GraphQL; Auth → shared `gh` + conventions; cite
  `openspec/principles.global.md`; inline follow-up Markdown
- **Why:** Explore lock-in for #5

### 8. Inline follow-up Markdown

- **Choice:** Body template in the skill; no create-issue dependency
- **Why:** Explore lock-in

## Risks / Trade-offs

- **[Risk] Consumer forgets `PRODUCT_SLUG` on host** → Mitigation: clear error; document in README + conventions link;
  Dev Container sets it for this repo
- **[Risk] Double prompt if shell and wrapper both ask** → Mitigation: skip markers + “already set / key present” logic
  from API; non-TTY load never prompts
- **[Risk] Skill GraphQL duplicates future CLI** → Mitigation: accepted until #16
- **[Trade-off] Epic board order #7→#8** → Mitigation: intentional pull-forward

## Migration Plan

1. Implement #8 scripts + PATH + PRODUCT_SLUG + shell/postCreate load + docs
2. Implement #5 artifacts pointing at them
3. Content review; no consumer sync in this change
4. Rollback = revert

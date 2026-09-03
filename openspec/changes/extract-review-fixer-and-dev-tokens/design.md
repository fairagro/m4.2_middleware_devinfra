# Extract review-fixer and personal-token helpers — Design

## Context

See proposal.md. Combines issue #8 (full) and issue #5. Explore lock-ins for #8: full wrappers; **Kombi**
shell/postCreate load of stored tokens **plus** PATH wrappers; both `GH_TOKEN` and `GITGUARDIAN_API_KEY`; empty-skip /
`scripts/bin` PATH / no worktree tokens. Host token path uses the **git repository name** (from `origin`, not
`PRODUCT_SLUG`). #5: Variante A, inline follow-up, Done = files + content ok. #4 already landed policy and
`principles.global.md`.

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
- Mapping git repository names to short product-slugs for host token paths

## Decisions

### 1. One change for #8 then #5

- **Choice:** Single change; implement token helpers before the skill so Auth text is real
- **Why:** User intent; avoids a skill that documents missing scripts

### 2. Host token dir = git repository name (not PRODUCT_SLUG)

- **Choice:** Host path `~/.config/<git-repo-name>/tokens.env` derives `<git-repo-name>` from
  `git remote get-url origin` (fallback: basename of git toplevel). No `PRODUCT_SLUG` required. Product-slugs remain for
  Docker volume names only. This Dev Container does not set `PRODUCT_SLUG`.
- **Alternatives:** `PRODUCT_SLUG` env only; basename→slug map; hard-coded default slug
- **Why:** Env is easy to forget on host clones; repo name is unique per product and needs no overlay config. Auto-map
  to short slugs fails for repos like `m4.2_advanced_middleware_api` → `middleware-api`.

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

- **[Trade-off] Host path uses repo name (`m4.2_…`), volumes use short product-slug** → Mitigation: document clearly in
  conventions; isolation still per product
- **[Risk] Clone without origin / outside git** → Mitigation: clear error; fallback to toplevel basename when possible
- **[Risk] Double prompt if shell and wrapper both ask** → Mitigation: skip markers + “already set / key present” logic
  from API; non-TTY load never prompts
- **[Risk] Skill GraphQL duplicates future CLI** → Mitigation: accepted until #16
- **[Trade-off] Epic board order #7→#8** → Mitigation: intentional pull-forward

## Migration Plan

1. Implement #8 scripts + PATH + repo-name host path + shell/postCreate load + docs (incl. conventions delta)
2. Implement #5 artifacts pointing at them
3. Content review; no consumer sync in this change
4. Rollback = revert

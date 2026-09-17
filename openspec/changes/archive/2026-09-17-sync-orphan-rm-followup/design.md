## Context

See proposal.md — Why. Today `scripts/sync-products.py` copies the resolved allowlist into a shallow product clone and
opens SHA-scoped sync PRs; the workflow gates on allowlist path changes using `before`→`HEAD`. `m42-ai` already owns
cross-repo `gh` issue create and PR helpers. Lock-ins from explore: **delta orphan delete (A)**, trailers from **body +
comments**.

## Goals / Non-Goals

**Goals:**

- Delta `git rm` for allowlist file-set shrinks between comparison base and source SHA.
- `SYNC-FOLLOWUP` collection + per-product ensure implemented primarily in `m42-ai`; sync script/workflow call it.
- Dispatch input for the same ensure path; dry-run creates neither PRs nor issues.

**Non-Goals:**

- Sync manifest file in products (approach B).
- Deleting never-allowlisted product paths.
- Catch-up purge of orphans older than the comparison window (manual / trailer).
- Auto-merge of sync PRs.

## Decisions

1. **Orphan set = `list-files(base) − list-files(HEAD)`** Resolve allowlist at both trees (`git show` / worktree
   checkout of YAML + expand against that tree’s files, or checkout base briefly). Prefer extending `--list-files` with
   `--ref` rather than inventing a second path SoT. _Rejected:_ product-side manifest (B); `retire:` YAML.

2. **Comparison base** Actions push: `github.event.before`. Local/dispatch live sync: optional `--orphan-base <sha>`; if
   omitted, skip deletes (copy-only) and still allow follow-up ensure when ids are known. _Rejected:_ always full-tree
   reconcile without base.

3. **`m42-ai` surface (MVP)**
   - `pr-for-commit --sha` → JSON `{number,url,…}|null`
   - `sync-followup-ids --pr N` (or `--body` + `--comments` fixtures) → JSON list of ids from body + comments
   - `sync-followup-ensure --owner/--repo --id … --source-pr/--source-sha` → create-or-reuse JSON Dedupe key: label
     `sync-followup:<id>` (create label if missing) and/or title prefix; prefer label for search. Template: file under
     Devinfra (e.g. `docs/sync-followup-issue.md`) with placeholders — not synced to products unless we explicitly
     allowlist later (default: Devinfra-only path read by CLI when cwd is Devinfra).

4. **Orchestration** Workflow after/before sync PRs: resolve PR for `GITHUB_SHA`, collect ids (+ dispatch input), loop
   products calling `sync-followup-ensure`. `sync-products.py` owns copy + orphan `git rm` + commit/PR; MAY shell out to
   `m42-ai` for follow-ups or leave that to the workflow for clearer dry-run splits.

5. **Comment sources** Issue comments on the PR + submitted review bodies that contain the trailer line. Ignore PENDING
   review drafts.

## Risks / Trade-offs

- **[Risk] Older orphans remain** after landing → Mitigation: docs + `SYNC-FOLLOWUP` / one-off product issues; no silent
  full-tree wipe.
- **[Risk] Accidental allowlist drop deletes in three repos** → Mitigation: review Devinfra PR + sync PR diff; no
  auto-merge.
- **[Risk] No PR for direct push** → Mitigation: dispatch follow-up input; deletes still work from `before` delta.
- **[Risk] Bot lacks Issues write on a product** → Mitigation: document in renovate/sync docs (Issues already in table);
  fail closed with clear error per repo.
- **[Trade-off] Body+comments** more complete than body-only → more API calls; acceptable at sync frequency.

## Migration Plan

1. Land Feature on Devinfra `main` (OpenSpec archive with PR).
2. Next allowlist-touching push exercises delta delete + optional trailer.
3. Pre-existing orphans: authors open `SYNC-FOLLOWUP` or product issues manually once.
4. Rollback: revert sync script/workflow to copy-only; leave any already-merged product deletes as-is.

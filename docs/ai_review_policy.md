# AI Review Policy

How shared m4.2 middleware repositories treat GitHub Copilot code review and Cursor Bugbot findings. This file is the
single policy. Copilot loads it via `.github/copilot-instructions.md`; Bugbot via `.cursor/BUGBOT.md`; the local fixer
via `/review-fixer`.

Two channels:

| Channel                                                  | Re-review                 | Must fix                                      |
| -------------------------------------------------------- | ------------------------- | --------------------------------------------- |
| **Risk** (Blocker/High, practicality not Low)            | stays open every round    | yes, if the finding is correct and in this PR |
| **Nit** (Low, or Medium with expensive/out-of-scope fix) | finders may still comment | only while nit-budget remains                 |

Merge criterion: no open **risk** findings. Dismissed nit threads are not a merge blocker. Do not loop until “0 Copilot
comments”.

---

## Roles

1. **Finder** (Copilot on GitHub, Bugbot): high recall. Skip the classes below. Label severity, cite a reachable path,
   do not widen types in suggested patches. Finders do **not** apply nit-budget.
2. **Fixer** (`/review-fixer`): precision and policy. Re-evaluates every thread, then `fix`, `dismiss`, or (rarely)
   `follow-up`.
3. **Human**: samples the fixer’s path sentences and owns the merge.

Every thread is **triaged**. Triage is not the same as implementing. Valid outcomes: fix in this PR, dismiss with a
one-line reason, or one bundled follow-up issue for the whole PR.

---

## Finder instructions (Copilot and Bugbot)

High recall for real bugs. Do **not** apply nit-budget. Do not implement fixes.

**Report**

- Wrong results, data loss/overwrite, broken public API or documented contracts, secrets in logs, races that can clobber
  persisted state
- Swallowed errors, bad idempotency / conflict handling, ownership or authz bypass, resource leaks on hot paths
- New behaviour with no test

Each comment **must** include:

1. **Severity:** `Blocker` | `High` | `Medium` | `Low` (table below; first match; do not upgrade on vibe)
2. **Path sentence:** public route / worker or async task / real default config → function → bad state. No path → do not
   comment
3. A patch only if it **narrows** types or is a local correction

**Do not comment on**

- Ruff, MyPy, Pylint, Bandit, Prettier/markdownlint, hadolint, formatting, import order, naming-only
- `None` guards on Pydantic-validated models or values already excluded by the project's config wrapper
- Extra abstractions, wrappers, or DRY for a single call site
- Drive-by issues in files/hunks this PR did not change, unless Blocker
- Theoretical weaknesses with no reachable path in this service / worker
- Suggested `T | None`, `Any`, `object`, or `if x is None` when the type already excludes `None`
- macOS, Homebrew, Windows, or host `PATH` layouts that the Linux Dev Container does not use
  ([`openspec/principles.global.md`](../openspec/principles.global.md) Supported development environment)

If nothing in **Report** applies, leave no comment. Prefer fewer, higher-severity comments.

---

## Decision order (fixer)

Stop at the first matching step.

1. **Correct?** If the diagnosis is wrong, already covered by types / Pydantic / the config wrapper / a spec invariant,
   or Ruff/MyPy/Pylint/Bandit/Prettier/markdownlint/hadolint already gate it → `dismiss`. If the path is only macOS,
   Homebrew, Windows, or an unofficial host install — quote
   [`openspec/principles.global.md`](../openspec/principles.global.md) Supported development environment → `dismiss`
   (practicality **None**).
2. **This PR?** If it is drive-by on unchanged code, another module, or speculative hardening the change does not need →
   `dismiss` or `follow-up` (only if Medium+).
3. **Cheapest correct fix?** Prefer a narrower type, a cited invariant, or an existing helper over the finder’s patch.
   Widening a type is not a fix (see [Types](#types)).
4. **Risk.** Severity Blocker/High **and** practicality not Low → `fix`. Nit-budget does not apply. If the fix itself is
   a separate feature, split or `follow-up` instead of bloating this PR.
5. **Cheap + high practicality + Medium+.** Cost **cheap**, practicality **High**, severity **Medium or higher**, and
   **no** new abstraction → `fix` in any round. Round/nit-budget does not defer these.
6. **Nit.** Otherwise treat as a nit:
   - Round 1 + cheap + running nit prod-line growth still ≤ ~25 and **no** new abstraction → `fix`
   - Round 2+ **and** the nit is on code the previous fixer pass introduced → `fix` if cheap
   - Else → `dismiss` (Low) or `follow-up` (Medium+ only, typically when expensive or practicality is not High)

If the cheaper fix is unclear, default to `dismiss` rather than adding a layer.

---

## Severity (pick the first match; do not upgrade on vibe)

| Level       | When (any one)                                                                                                                                                                                        |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Blocker** | Wrong domain result; data loss or silent overwrite; broken HTTP/API or documented contract; secret/credential in logs or persistence; documented race that can clobber a document or equivalent state |
| **High**    | Error swallowed (empty `except`, success status on failure); idempotency / conflict handling wrong; authz/ownership bypass; resource leak on a hot path                                               |
| **Medium**  | New behaviour with no test; error path that misleads operators; duplication that will diverge                                                                                                         |
| **Low**     | Naming, comments, extra abstraction, defensive check inside already-validated data, micro-DRY                                                                                                         |

If nothing matches Blocker/High/Medium → **Low**.

---

## Practicality (requires a path sentence)

Practicality is not “we have seen this in prod”. It is “a realistic path exists in _this_ system”.

| Level      | Rule                                                                                                                                                                                                                                |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **High**   | Cite entry → function → bad state. Entry is a public HTTP route, a worker / async task, or a config field set by default / the repo's documented default config.                                                                    |
| **Medium** | Only with non-default config, an internal caller, or admin.                                                                                                                                                                         |
| **Low**    | State is excluded by Pydantic, the config wrapper, annotations, or a spec invariant — **quote the invariant**.                                                                                                                      |
| **None**   | False positive; the alleged path does not exist. Unsupported host (macOS, Windows, Homebrew, unofficial workstation) — quote [`openspec/principles.global.md`](../openspec/principles.global.md) Supported development environment. |

If the fixer cannot write a path sentence, practicality is **Low**, not High.

Risk is high only when severity is Blocker/High **and** practicality is not Low/None.

---

## Cost (estimate _before_ coding, on the chosen fix)

Do not use `git diff --stat` of a patch that does not exist yet. Estimate the fix you would actually apply, not the
finder’s suggested patch.

| Signal               | Cheap                  | Expensive                                |
| -------------------- | ---------------------- | ---------------------------------------- |
| New production lines | 0 or <15               | 15–50 (grey) / >50                       |
| New abstraction      | no                     | new class, helper, or module             |
| Types                | same or **narrower**   | wider (`T \| None`, `Any`, untyped dict) |
| Scope                | one function, one file | multiple modules / extra responsibility  |

**Expensive** if any of: new abstraction, wider type, multiple modules, >50 prod lines. A new helper with no second call
site is expensive even at 20 lines.

### What counts as production size

- **Counts:** runtime code under `middleware/*/src/` (see path conventions).
- **Does not count:** tests that lock **real** behaviour (regression for a real bug, endpoint or public contract). Tests
  that encode a hypothetical state the types already forbid **do** count as bloat — do not add them.
- **Specs:** may grow when they record a contract the code now actually has. Do not add spec text for a theoretical
  weakness. Spec growth is not the production size budget; still apply risk vs cost.

---

## Nit-budget

A **nit** is a correct (or plausible) finding that is **not** high risk and does **not** already qualify as step 5
(cheap + High practicality + Medium+).

Budget (fixer only):

1. **Round 1** (first Copilot/Bugbot review on this PR): cheap nits may be fixed until **~25 new production lines** from
   nit-fixes, and **never** a new abstraction.
2. **Round 2+**: remaining nits only on surface **introduced by the previous fixer pass** (regression of those fixes).
   Other Low / lower-practicality nits on already-reviewed surface → `dismiss` or `follow-up` per the decision order.
3. Risk findings and step-5 (cheap + High practicality + Medium+) findings are **never** budgeted away. A Blocker/High
   with a real path in round 3 is still a must-fix.

Round count = number of Copilot and/or Bugbot review submissions on the PR, not “how many comments”.

---

## Types

These rules apply to writing code and to reviewing it
([`openspec/principles.global.md`](../openspec/principles.global.md) Type Safety).

- Do **not** widen a type to silence a finding (`T` → `T | None`, `Any`, `object`, `dict[str, Any]`). That is a new
  defect, not a fix. Do not hide `Any`/`object` behind a type alias.
- Do **not** add `if x is None` / `x or default` when the annotation, Pydantic model, or config wrapper already excludes
  `None`.
- If `None` is genuinely required, make the **source** optional and update every caller. Do not insert a local guard in
  the middle of the pipeline.
- Prefer a narrower type, an existing helper, or a quoted invariant over a new wrapper or retry layer.

---

## Follow-up issues

- At most **one** follow-up issue per PR.
- Include only deferred items that are **Medium or higher**.
- Low nits that miss the budget get a dismissal reply, not an issue.
- Title: `Follow-up from PR # AI review`. Body: bullet list of deferred findings with path, severity, practicality, and
  why they are out of this PR.

---

## Fixer reply format

Reply on the thread, then resolve:

```text
fix | dismiss | follow-up
correct: yes/no
severity: …
practicality: … (path or invariant)
cost: cheap|expensive (chosen fix, not the suggestion)
reason: …
```

If the chosen fix differs from the suggestion, say what you did instead (e.g. “narrowed return type of `Foo.bar` instead
of adding a None-guard”).

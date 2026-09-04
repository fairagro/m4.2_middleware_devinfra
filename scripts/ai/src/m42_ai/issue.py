"""Issue create / issue-start plumbing via `gh` and `git`."""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import Any

from m42_ai.gh import GhError, run_gh, run_git, repo_owner_name

LABEL_SPECS: dict[str, tuple[str, str]] = {
    "severity:blocker": ("B60205", "Blocks merge / data loss / broken contract"),
    "severity:high": ("D93F0B", "Serious defect with a real path"),
    "severity:medium": ("FBCA04", "Important but not high-risk"),
    "severity:low": ("0E8A16", "Nit / low urgency"),
    "practicality:high": ("1D76DB", "Realistic path in this system"),
    "practicality:medium": ("5319E7", "Non-default / internal / admin path"),
    "practicality:low": ("C5DEF5", "Mostly excluded by types/invariants"),
    "practicality:none": ("EDEDED", "No real path / unsupported environment"),
    "practicality:seen-in-the-wild": ("BFDADC", "Observed in real usage"),
    "cost:cheap": ("C2E0C6", "Small local fix"),
    "cost:medium": ("FEF2C0", "Moderate issue-planning cost"),
    "cost:expensive": ("F9D0C4", "Large or cross-cutting work"),
}

ORG_TYPES = frozenset({"Bug", "Security", "Feature", "Task", "Discussion", "Refactoring"})
ISSUE_URL_RE = re.compile(r"https://github\.com/[^/\s]+/[^/\s]+/issues/\d+")


def slugify(text: str, *, max_len: int = 48) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    if not s:
        s = "issue"
    return s[:max_len].rstrip("-")


def ensure_labels(labels: list[str], *, cwd: Path | None = None) -> None:
    unknown = [n for n in labels if n not in LABEL_SPECS]
    if unknown:
        raise ValueError(f"off-allowlist labels: {unknown}")
    # Default gh page size is 30; triage repos can exceed that. Raise the limit so
    # existing allowlisted labels are not mistaken for missing.
    proc = run_gh(
        ["label", "list", "--limit", "1000", "--json", "name", "--jq", ".[].name"],
        cwd=cwd,
    )
    existing = {line.strip() for line in proc.stdout.splitlines() if line.strip()}
    for name in labels:
        if name in existing:
            continue
        color, desc = LABEL_SPECS[name]
        run_gh(["label", "create", name, "--color", color, "--description", desc], cwd=cwd)


def _extract_issue_url(text: str) -> str | None:
    m = ISSUE_URL_RE.search(text)
    return m.group(0) if m else None


def create_issue(
    *,
    title: str,
    body: str,
    issue_type: str,
    labels: list[str],
    parent: int | None = None,
    cwd: Path | None = None,
) -> dict[str, Any]:
    if issue_type not in ORG_TYPES:
        raise ValueError(f"invalid org issue type: {issue_type!r}")
    ensure_labels(labels, cwd=cwd)

    def _args(with_parent: bool) -> list[str]:
        args = [
            "issue",
            "create",
            "--title",
            title,
            "--body-file",
            "-",
            "--type",
            issue_type,
        ]
        for lab in labels:
            args.extend(["--label", lab])
        if with_parent and parent is not None:
            args.extend(["--parent", str(parent)])
        return args

    relation = f"sub-of #{parent}" if parent is not None else "linked"
    parent_failed: str | None = None

    def _result(
        *,
        url: str,
        relation_out: str,
        parent_fallback: bool,
        parent_error: str | None,
        partial_failure: bool,
    ) -> dict[str, Any]:
        return {
            "url": url,
            "type": issue_type,
            "labels": labels,
            "relation": relation_out,
            "parent_fallback": parent_fallback,
            "parent_error": parent_error,
            "partial_failure": partial_failure,
        }

    if parent is not None:
        try:
            proc = run_gh(_args(True), input_text=body, cwd=cwd)
            created_url = _extract_issue_url(proc.stdout) or proc.stdout.strip()
            return _result(
                url=created_url,
                relation_out=relation,
                parent_fallback=False,
                parent_error=None,
                partial_failure=False,
            )
        except GhError as exc:
            # Only fall back when no issue URL was produced. Parent attach can fail
            # after create; URL is often on stdout while stderr explains the error —
            # GhError keeps both streams so we do not open a second issue.
            maybe = (
                _extract_issue_url(exc.stdout)
                or _extract_issue_url(exc.stderr)
                or _extract_issue_url(str(exc))
            )
            if maybe:
                return _result(
                    url=maybe,
                    relation_out=relation,
                    parent_fallback=False,
                    parent_error=exc.stderr.strip() or str(exc),
                    partial_failure=True,
                )
            parent_failed = exc.stderr.strip() or str(exc)

    proc = run_gh(_args(False), input_text=body, cwd=cwd)
    created_url = _extract_issue_url(proc.stdout) or proc.stdout.strip()
    return _result(
        url=created_url,
        relation_out="linked" if parent_failed else relation,
        parent_fallback=bool(parent_failed),
        parent_error=parent_failed,
        partial_failure=bool(parent_failed),
    )


def issue_start(
    *,
    issue: int,
    slug: str | None = None,
    base: str = "main",
    cwd: Path | None = None,
    draft_title: str | None = None,
) -> dict[str, Any]:
    root = cwd or Path.cwd()
    status = run_git(["status", "--porcelain"], cwd=root)
    if status.stdout.strip():
        raise RuntimeError("working tree/index must be clean before issue-start")

    proc = run_gh(["issue", "view", str(issue), "--json", "title,url,number"], cwd=root)
    meta = json.loads(proc.stdout)
    title = str(meta["title"])
    branch_slug = slugify(slug) if slug else slugify(title)
    branch = f"issue-{issue}-{branch_slug}"

    run_git(["fetch", "origin", base], cwd=root)
    run_git(["checkout", base], cwd=root)
    run_git(["pull", "--ff-only", "origin", base], cwd=root)
    run_git(["checkout", "-b", branch], cwd=root)
    run_git(["commit", "--allow-empty", "-m", f"Start issue #{issue}"], cwd=root)
    run_git(["push", "-u", "origin", "HEAD"], cwd=root)

    pr_title = draft_title or title
    # Keep PR bodies free of tool marketing footers (e.g. "Made with Cursor").
    body = f"## Summary\n- MVP scope: (fill in)\n\nFixes #{issue}\n"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(body)
        body_path = tmp.name
    try:
        proc = run_gh(
            [
                "pr",
                "create",
                "--draft",
                "--base",
                base,
                "--title",
                pr_title,
                "--body-file",
                body_path,
            ],
            cwd=root,
        )
    finally:
        Path(body_path).unlink(missing_ok=True)

    pr_url = proc.stdout.strip()
    owner, name = repo_owner_name(cwd=root)
    return {
        "issue": {"number": issue, "url": meta["url"], "title": title},
        "branch": branch,
        "pr_url": pr_url,
        "repo": f"{owner}/{name}",
    }

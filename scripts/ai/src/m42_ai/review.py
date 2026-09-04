"""Review-open shaping and GitHub write helpers for review replies/resolves."""

from __future__ import annotations

import json
import re
from typing import Any

from m42_ai.gh import run_gh, repo_owner_name

AI_AUTHOR_RE = re.compile(r"copilot|bugbot|cursor", re.I)

REVIEW_OPEN_QUERY = """
query($owner:String!,$name:String!,$n:Int!) {
  repository(owner:$owner, name:$name) {
    pullRequest(number:$n) {
      url
      number
      reviews(first: 50) {
        nodes { databaseId author { login } submittedAt state body }
      }
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 20) {
            nodes { databaseId author { login } body path originalPosition }
          }
        }
      }
    }
  }
}
"""

RESOLVE_MUTATION = """
mutation($id:ID!) {
  resolveReviewThread(input:{threadId:$id}) {
    thread { id isResolved }
  }
}
"""


def is_ai_author(login: str | None) -> bool:
    if not login:
        return False
    return bool(AI_AUTHOR_RE.search(login))


def extract_suppressed_comments(body: str) -> list[str]:
    """Heuristic: bullets under a 'Suppressed comments' (or similar) heading."""
    if not body:
        return []
    lines = body.splitlines()
    collecting = False
    items: list[str] = []
    heading_re = re.compile(r"suppressed\s+comments|needs\s+a\s+closer\s+look", re.I)
    bullet_re = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
    for line in lines:
        if heading_re.search(line):
            collecting = True
            continue
        if collecting:
            if re.match(r"^#{1,6}\s+", line) and not heading_re.search(line):
                break
            if bullet_re.match(line):
                items.append(bullet_re.sub("", line).strip())
            elif line.strip() == "":
                continue
            elif items and not line.startswith((" ", "\t")):
                # left the list block
                break
    return items


def shape_review_open(payload: dict[str, Any]) -> dict[str, Any]:
    """Turn raw GraphQL into agent-facing open-work JSON (no policy decisions)."""
    pr = payload["data"]["repository"]["pullRequest"]
    threads_out: list[dict[str, Any]] = []
    for thread in pr["reviewThreads"]["nodes"]:
        if thread.get("isResolved"):
            continue
        comments = thread.get("comments", {}).get("nodes") or []
        if not comments:
            continue
        first = comments[0]
        author = (first.get("author") or {}).get("login")
        if not is_ai_author(author):
            continue
        threads_out.append(
            {
                "thread_id": thread["id"],
                "is_resolved": False,
                "path": first.get("path"),
                "first_comment": {
                    "database_id": first.get("databaseId"),
                    "author": author,
                    "body": first.get("body") or "",
                    "original_position": first.get("originalPosition"),
                },
                "comment_count": len(comments),
            }
        )

    ai_reviews = [
        r
        for r in pr["reviews"]["nodes"]
        if r.get("author") and is_ai_author((r["author"] or {}).get("login"))
    ]
    ai_reviews.sort(key=lambda r: r.get("submittedAt") or "")
    latest = ai_reviews[-1] if ai_reviews else None
    latest_body = (latest.get("body") or "") if latest else ""
    suppressed = extract_suppressed_comments(latest_body) if latest_body else []

    return {
        "pr": {"number": pr.get("number"), "url": pr.get("url")},
        "round_count": len(ai_reviews),
        "unresolved_ai_threads": threads_out,
        "latest_ai_review": None
        if latest is None
        else {
            "database_id": latest.get("databaseId"),
            "author": (latest.get("author") or {}).get("login"),
            "submitted_at": latest.get("submittedAt"),
            "state": latest.get("state"),
            "body": latest_body,
            "suppressed_comments": suppressed,
        },
        "open_work_empty": len(threads_out) == 0 and not latest_body.strip(),
    }


def fetch_review_open(pr: int, *, owner: str | None = None, repo: str | None = None) -> dict[str, Any]:
    if owner is None or repo is None:
        owner, repo = repo_owner_name()
    proc = run_gh(
        [
            "api",
            "graphql",
            "-f",
            f"query={REVIEW_OPEN_QUERY}",
            "-F",
            f"owner={owner}",
            "-F",
            f"name={repo}",
            "-F",
            f"n={pr}",
        ]
    )
    payload = json.loads(proc.stdout)
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    return shape_review_open(payload)


def review_reply(
    *,
    pr: int,
    body: str,
    in_reply_to: int | None = None,
    conversation: bool = False,
    owner: str | None = None,
    repo: str | None = None,
) -> dict[str, Any]:
    if owner is None or repo is None:
        owner, repo = repo_owner_name()
    if conversation:
        if in_reply_to is not None:
            raise ValueError("use either --conversation or --in-reply-to, not both")
        payload = json.dumps({"body": body})
        proc = run_gh(
            [
                "api",
                "-X",
                "POST",
                f"repos/{owner}/{repo}/issues/{pr}/comments",
                "--input",
                "-",
            ],
            input_text=payload,
        )
    else:
        if in_reply_to is None:
            raise ValueError("--in-reply-to is required unless --conversation")
        payload = json.dumps({"body": body, "in_reply_to": in_reply_to})
        proc = run_gh(
            [
                "api",
                "-X",
                "POST",
                f"repos/{owner}/{repo}/pulls/{pr}/comments",
                "--input",
                "-",
            ],
            input_text=payload,
        )
    return json.loads(proc.stdout)


def review_resolve(thread_id: str) -> dict[str, Any]:
    proc = run_gh(
        [
            "api",
            "graphql",
            "-f",
            f"query={RESOLVE_MUTATION}",
            "-F",
            f"id={thread_id}",
        ]
    )
    payload = json.loads(proc.stdout)
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    return payload["data"]["resolveReviewThread"]["thread"]

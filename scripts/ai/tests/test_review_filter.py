from __future__ import annotations

import json
from pathlib import Path

from m42_ai.issue import slugify
from m42_ai.review import extract_suppressed_comments, is_ai_author, shape_review_open

FIXTURE = Path(__file__).parent / "fixtures" / "review_pr.json"


def test_is_ai_author() -> None:
    assert is_ai_author("copilot-pull-request-reviewer")
    assert is_ai_author("cursor[bot]")
    assert is_ai_author("Bugbot")
    assert not is_ai_author("alice")
    assert not is_ai_author(None)


def test_extract_suppressed_comments() -> None:
    body = "## Suppressed comments\n\n- One\n- Two\n\n## Next\n\n- ignore"
    assert extract_suppressed_comments(body) == ["One", "Two"]


def test_shape_review_open_filters_resolved_and_human() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    shaped = shape_review_open(payload)
    assert shaped["pr"]["number"] == 22
    assert shaped["round_count"] == 2
    assert len(shaped["unresolved_ai_threads"]) == 1
    thread = shaped["unresolved_ai_threads"][0]
    assert thread["thread_id"] == "PRRT_open_ai"
    assert thread["first_comment"]["database_id"] == 200
    assert shaped["latest_ai_review"]["author"] == "cursor"
    assert shaped["latest_ai_review"]["suppressed_comments"] == []
    assert shaped["open_work_empty"] is False


def test_shape_includes_suppressed_from_earlier_review_body_when_latest() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    # Drop cursor review so latest is Copilot with suppressed section
    payload["data"]["repository"]["pullRequest"]["reviews"]["nodes"].pop()
    shaped = shape_review_open(payload)
    assert shaped["latest_ai_review"]["author"] == "copilot-pull-request-reviewer"
    assert shaped["latest_ai_review"]["suppressed_comments"] == [
        "Unused import in foo.py",
        "Typo in README",
    ]


def test_slugify() -> None:
    assert slugify("CLI for agent GitHub/git plumbing!") == "cli-for-agent-github-git-plumbing"

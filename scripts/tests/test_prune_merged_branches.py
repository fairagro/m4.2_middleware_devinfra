"""Regression: prune-merged-branches must not delete a reused superseded head name."""

from __future__ import annotations

import json
import os
import stat
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "prune-merged-branches.sh"

_GIT_ENV = {
    "GIT_AUTHOR_NAME": "prune-test",
    "GIT_AUTHOR_EMAIL": "prune-test@example.test",
    "GIT_COMMITTER_NAME": "prune-test",
    "GIT_COMMITTER_EMAIL": "prune-test@example.test",
}


def _git(cwd: Path, *args: str) -> str:
    env = {**os.environ, **_GIT_ENV}
    out = subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return out.stdout.strip()


def _write_fake_gh(bin_dir: Path, *, prs: list[dict[str, object]], views: dict[str, object]) -> None:
    payload = bin_dir / "payload.json"
    payload.write_text(json.dumps({"prs": prs, "views": views}), encoding="utf-8")
    gh = bin_dir / "gh"
    gh.write_text(
        f"""#!/usr/bin/env python3
import json, sys
data = json.load(open({str(payload)!r}))
args = sys.argv[1:]
if args[:2] == ["repo", "view"]:
    if "-q" in args:
        print("o/r")
    else:
        print(json.dumps({{"nameWithOwner": "o/r"}}))
    raise SystemExit(0)
if args[:2] == ["pr", "list"]:
    print(json.dumps(data["prs"]))
    raise SystemExit(0)
if args[:2] == ["pr", "view"]:
    print(json.dumps(data["views"][args[2]]))
    raise SystemExit(0)
raise SystemExit(f"unexpected gh args: {{args!r}}")
""",
        encoding="utf-8",
    )
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)


def _repo_with_reuse_branch(tmp_path: Path, *, extra_commit: bool) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.email", "prune-test@example.test")
    _git(repo, "config", "user.name", "prune-test")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / "f.txt").write_text("main\n", encoding="utf-8")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-m", "main")
    _git(repo, "checkout", "-b", "reuse-me")
    (repo / "f.txt").write_text("old-pr\n", encoding="utf-8")
    _git(repo, "add", "f.txt")
    _git(repo, "commit", "-m", "closed-pr-head")
    old_oid = _git(repo, "rev-parse", "HEAD")
    if extra_commit:
        (repo / "f.txt").write_text("reused-new-work\n", encoding="utf-8")
        _git(repo, "add", "f.txt")
        _git(repo, "commit", "-m", "reused-tip")
    _git(repo, "checkout", "main")
    _git(tmp_path, "init", "--bare", str(remote))
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main", "reuse-me")
    return repo, old_oid


def _run_prune(repo: Path, bin_dir: Path) -> str:
    env = {**os.environ, **_GIT_ENV, "PATH": f"{bin_dir}:{os.environ.get('PATH', '')}"}
    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.stdout + proc.stderr


def _fixture_prs(old_oid: str) -> tuple[list[dict[str, object]], dict[str, object]]:
    prs: list[dict[str, object]] = [
        {
            "number": 10,
            "state": "CLOSED",
            "mergedAt": None,
            "headRefName": "reuse-me",
            "headRefOid": old_oid,
            "url": "https://example.test/10",
        },
        {
            "number": 11,
            "state": "MERGED",
            "mergedAt": "2026-01-01T00:00:00Z",
            "headRefName": "other-merged",
            "headRefOid": "deadbeef",
            "url": "https://example.test/11",
        },
    ]
    views: dict[str, object] = {
        "10": {"body": "Superseded by #11", "comments": []},
        "11": {
            "number": 11,
            "state": "MERGED",
            "mergedAt": "2026-01-01T00:00:00Z",
            "headRefName": "other-merged",
        },
    }
    return prs, views


def test_reused_superseded_head_name_is_kept(tmp_path: Path) -> None:
    """Keep a reused head name whose tip is not the closed PR commit."""
    repo, old_oid = _repo_with_reuse_branch(tmp_path, extra_commit=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    prs, views = _fixture_prs(old_oid)
    _write_fake_gh(bin_dir, prs=prs, views=views)
    out = _run_prune(repo, bin_dir)
    assert "Mode: dry-run" in out
    assert "local reuse-me (keep:not-proven)" in out
    assert "remote reuse-me (keep:not-proven)" in out
    assert "reuse-me (superseded-chain" not in out


def test_superseded_tip_still_at_closed_oid_is_deletable(tmp_path: Path) -> None:
    """Still allow prune when the tip is the closed superseded PR head."""
    repo, old_oid = _repo_with_reuse_branch(tmp_path, extra_commit=False)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    prs, views = _fixture_prs(old_oid)
    _write_fake_gh(bin_dir, prs=prs, views=views)
    out = _run_prune(repo, bin_dir)
    assert "Mode: dry-run" in out
    assert "local reuse-me (superseded-chain→#11)" in out
    assert "remote reuse-me (superseded-chain→#11)" in out
    assert "reuse-me (keep:not-proven)" not in out

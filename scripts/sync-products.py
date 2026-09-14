#!/usr/bin/env python3
"""Copy allowlisted Devinfra paths into product repos and open sync PRs.

Path set comes only from docs/synced-paths.yaml. See docs/sync.md.
Typical callers: .github/workflows/sync-products.yml, or a manual local run.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = REPO_ROOT / "docs" / "synced-paths.yaml"

TARGETS: dict[str, str] = {
    "api": "fairagro/m4.2_advanced_middleware_api",
    "sql_to_arc": "fairagro/m4.2_sql_to_arc",
    "harvester": "fairagro/m4.2_middleware_harvester",
}

# New branches: chore/devinfra-sync-<shortsha>. Legacy rolling name also matches.
SYNC_BRANCH_PREFIX = "chore/devinfra-sync"
SHORT_SHA_LEN = 7
DRY_RUN_PREVIEW_LIMIT = 20


def sync_branch_name(source_sha: str) -> str:
    """Return SHA-scoped sync branch for this Devinfra commit."""
    short = source_sha.strip()[:SHORT_SHA_LEN]
    if len(short) < SHORT_SHA_LEN:
        raise SystemExit(f"source_sha too short for sync branch: {source_sha!r}")
    return f"{SYNC_BRANCH_PREFIX}-{short}"


def is_sync_head(head_ref: str) -> bool:
    """Return whether head is a legacy or SHA-scoped sync branch."""
    return head_ref == SYNC_BRANCH_PREFIX or head_ref.startswith(
        f"{SYNC_BRANCH_PREFIX}-"
    )


def load_allow_exclude(path: Path) -> tuple[list[str], list[str]]:
    """Load `allow` and effective denylist from the YAML SoT.

    Product-local `overlays` are never overwritten: they are merged into the
    denylist even if a maintainer forgets to duplicate them under `exclude`.
    """
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit(f"{path}: expected a YAML mapping at the root")
    allow = loaded.get("allow") or []
    exclude = loaded.get("exclude") or []
    overlays = loaded.get("overlays") or []
    if not isinstance(allow, list) or not isinstance(exclude, list):
        raise SystemExit(f"{path}: `allow` and `exclude` must be YAML lists")
    if not isinstance(overlays, list):
        raise SystemExit(f"{path}: `overlays` must be a YAML list when present")
    allow_s = [str(x).strip() for x in allow if str(x).strip()]
    exclude_s = [str(x).strip() for x in exclude if str(x).strip()]
    seen = set(exclude_s)
    for raw in overlays:
        item = str(raw).strip()
        if item and item not in seen:
            exclude_s.append(item)
            seen.add(item)
    if not allow_s:
        raise SystemExit(f"{path}: `allow` list is empty")
    return allow_s, exclude_s


def normalize_rel(path: str) -> str:
    """Normalize to repo-relative POSIX paths."""
    rel = path.replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def is_ignored_artifact(rel: str) -> bool:
    """Skip bytecode under allowlisted trees."""
    return "__pycache__" in Path(rel).parts or Path(rel).suffix in {".pyc", ".pyo"}


def _match_double_star(path: str, pattern: str) -> bool:
    """Match patterns like `dir/**` against path."""
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(prefix + "/")
    if "/**/" in pattern:
        left, right = pattern.split("/**/", 1)
        if not path.startswith(left + "/") and path != left:
            return False
        rest = path[len(left) + 1 :] if path.startswith(left + "/") else ""
        return fnmatch.fnmatch(rest, right) or any(
            fnmatch.fnmatch("/".join(rest.split("/")[i:]), right)
            for i in range(len(rest.split("/")))
        )
    return fnmatch.fnmatch(path, pattern.replace("**/", "").replace("/**", "/*"))


def is_excluded(rel: str, excludes: tuple[str, ...]) -> bool:
    """Return whether rel matches any YAML `exclude` glob."""
    rel = normalize_rel(rel)
    for glob in excludes:
        if "**" in glob:
            if _match_double_star(rel, glob):
                return True
        elif "/" in glob:
            if fnmatch.fnmatch(rel, glob):
                return True
        elif fnmatch.fnmatch(rel, glob) or fnmatch.fnmatch(Path(rel).name, glob):
            return True
    return False


def _add_files(found: set[Path], root: Path, path: Path) -> None:
    if path.is_file():
        found.add(path.relative_to(root))
    elif path.is_dir():
        for child in path.rglob("*"):
            if child.is_file():
                found.add(child.relative_to(root))


def resolve_files(
    patterns: list[str], root: Path, excludes: tuple[str, ...]
) -> list[Path]:
    """Expand allowlist globs; drop excludes and bytecode."""
    found: set[Path] = set()
    for raw in patterns:
        pattern = normalize_rel(raw)
        if pattern.endswith("/**"):
            _add_files(found, root, root / pattern[:-3])
        elif any(c in pattern for c in "*?["):
            for match in root.glob(pattern):
                _add_files(found, root, match)
        else:
            _add_files(found, root, root / pattern)
    return sorted(
        rel
        for rel in found
        if not is_excluded(rel.as_posix(), excludes)
        and not is_ignored_artifact(rel.as_posix())
    )


def copy_files(files: list[Path], src_root: Path, dest_root: Path) -> None:
    """Copy allowlisted relative files from src_root into dest_root."""
    for rel in files:
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_root / rel, dest)


def run(
    cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None
) -> None:
    """Print and run a subprocess command; raise on non-zero exit."""
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def try_run(
    cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None
) -> bool:
    """Print and run a command; return whether it exited 0."""
    print("+", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=cwd, env=env, check=False)
    return completed.returncode == 0


def git_out(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    """Run a command and return stripped stdout; raise on non-zero exit."""
    return subprocess.check_output(cmd, cwd=cwd, env=env, text=True).strip()


def open_sync_pr_number(
    *, repo: str, head: str, cwd: Path, env: dict[str, str]
) -> int | None:
    """Return the open PR number for ``head``, if any."""
    raw = git_out(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--head",
            head,
            "--state",
            "open",
            "--json",
            "number",
            "--jq",
            ".[0].number // empty",
        ],
        cwd=cwd,
        env=env,
    )
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError as exc:
        raise SystemExit(f"invalid open PR number for head {head!r}: {raw!r}") from exc


def resolve_token() -> str | None:
    """Return DEVINFRA_BOT_TOKEN or GH_TOKEN from the environment, if set."""
    for key in ("DEVINFRA_BOT_TOKEN", "GH_TOKEN"):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return None


@dataclass(frozen=True)
class SyncTarget:
    """One product-repo sync invocation."""

    key: str
    repo: str
    files: list[Path]
    source_sha: str
    dry_run: bool
    token: str | None


def supersede_older_sync_prs(
    *,
    repo: str,
    new_pr: int,
    source_sha: str,
    cwd: Path,
    env: dict[str, str],
) -> None:
    """Comment + close other open sync PRs; never closes ``new_pr``."""
    raw = git_out(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "100",
            "--search",
            f"head:{SYNC_BRANCH_PREFIX}",
            "--json",
            "number,headRefName",
        ],
        cwd=cwd,
        env=env,
    )
    try:
        listed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"gh pr list returned invalid JSON: {exc}") from exc
    if not isinstance(listed, list):
        raise SystemExit("gh pr list JSON: expected a list")

    short = source_sha[:SHORT_SHA_LEN]
    body = (
        f"Superseded by #{new_pr}. Newer full allowlist sync from Devinfra `{short}`."
    )
    for item in listed:
        if not isinstance(item, dict):
            continue
        number = item.get("number")
        head = item.get("headRefName")
        if not isinstance(number, int) or not isinstance(head, str):
            continue
        if number == new_pr or not is_sync_head(head):
            continue
        run(
            [
                "gh",
                "pr",
                "comment",
                str(number),
                "--repo",
                repo,
                "--body",
                body,
            ],
            cwd=cwd,
            env=env,
        )
        run(
            ["gh", "pr", "close", str(number), "--repo", repo],
            cwd=cwd,
            env=env,
        )
        print(f"superseded open sync PR #{number} ({head})", flush=True)


def sync_target(req: SyncTarget) -> None:
    """Clone one product repo, copy files, open a new SHA-scoped sync PR if needed."""
    print(f"\n=== target {req.key}: {req.repo} ===", flush=True)
    branch = sync_branch_name(req.source_sha)
    if req.dry_run:
        print(
            f"dry-run: would copy {len(req.files)} files, open new sync PR on {branch}, "
            "and supersede older open sync PRs",
            flush=True,
        )
        for rel in req.files[:DRY_RUN_PREVIEW_LIMIT]:
            print(f"  {rel.as_posix()}")
        if len(req.files) > DRY_RUN_PREVIEW_LIMIT:
            print(f"  ... and {len(req.files) - DRY_RUN_PREVIEW_LIMIT} more")
        return

    if not req.token:
        raise SystemExit(
            "live sync requires DEVINFRA_BOT_TOKEN (or GH_TOKEN for local testing)"
        )

    env = os.environ.copy()
    env["GH_TOKEN"] = req.token
    env["GIT_TERMINAL_PROMPT"] = "0"
    run(["gh", "auth", "setup-git"], env=env)

    with tempfile.TemporaryDirectory(prefix=f"sync-{req.key}-") as tmp:
        dest = Path(tmp) / "repo"
        run(
            ["gh", "repo", "clone", req.repo, str(dest), "--", "--depth", "1"],
            env=env,
        )
        run(["git", "checkout", "-B", branch], cwd=dest, env=env)
        copy_files(req.files, REPO_ROOT, dest)

        if not git_out(["git", "status", "--porcelain"], cwd=dest, env=env):
            print("no changes vs target tip; skip PR", flush=True)
            return

        run(["git", "add", "-A"], cwd=dest, env=env)
        run(
            [
                "git",
                "-c",
                "user.name=fairagro-devinfra-bot",
                "-c",
                "user.email=devinfra-bot@users.noreply.github.com",
                "commit",
                "-m",
                f"chore: sync shared Devinfra paths from {req.source_sha[:SHORT_SHA_LEN]}",
            ],
            cwd=dest,
            env=env,
        )

        # Same Devinfra SHA already has an open sync PR (workflow retry) — reuse it.
        existing = open_sync_pr_number(repo=req.repo, head=branch, cwd=dest, env=env)
        if existing is not None:
            print(f"reusing open sync PR #{existing} on {branch}", flush=True)
            supersede_older_sync_prs(
                repo=req.repo,
                new_pr=existing,
                source_sha=req.source_sha,
                cwd=dest,
                env=env,
            )
            return

        # New branch per source SHA — never force-update a rolling sync ref.
        push_head = branch
        if not try_run(["git", "push", "-u", "origin", "HEAD"], cwd=dest, env=env):
            # Remote SHA branch may exist from a prior run that failed before PR create.
            retry_branch = f"{branch}-retry"
            print(
                f"push of {branch} failed; retrying once as {retry_branch} (no force)",
                flush=True,
            )
            run(["git", "branch", "-M", retry_branch], cwd=dest, env=env)
            run(["git", "push", "-u", "origin", "HEAD"], cwd=dest, env=env)
            push_head = retry_branch

        body = f"""## Summary

Sync allowlisted shared paths from [`fairagro/m4.2_middleware_devinfra@{req.source_sha}`](https://github.com/fairagro/m4.2_middleware_devinfra/commit/{req.source_sha}).

Source of truth: [`docs/synced-paths.yaml`](https://github.com/fairagro/m4.2_middleware_devinfra/blob/main/docs/synced-paths.yaml).

Do **not** hand-edit these paths in this consumer — land fixes in Devinfra, then re-sync.

## Test plan

- [ ] Spot-check diff against allowlist / hard excludes
- [ ] CI green on this PR
"""
        run(
            [
                "gh",
                "pr",
                "create",
                "--repo",
                req.repo,
                "--title",
                f"chore: sync shared Devinfra paths ({req.source_sha[:SHORT_SHA_LEN]})",
                "--body",
                body,
                "--head",
                push_head,
            ],
            cwd=dest,
            env=env,
        )
        new_pr = open_sync_pr_number(repo=req.repo, head=push_head, cwd=dest, env=env)
        if new_pr is None:
            raise SystemExit(
                f"sync PR create reported success but no open PR for head {push_head!r}"
            )
        print(f"opened sync PR #{new_pr} on {push_head}", flush=True)
        supersede_older_sync_prs(
            repo=req.repo,
            new_pr=new_pr,
            source_sha=req.source_sha,
            cwd=dest,
            env=env,
        )


def main(argv: list[str] | None = None) -> int:
    """Run product-repo sync CLI; return process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List resolved files / targets; do not clone or open PRs",
    )
    parser.add_argument("--skip-api", action="store_true")
    parser.add_argument("--skip-sql-to-arc", action="store_true")
    parser.add_argument("--skip-harvester", action="store_true")
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="Print resolved allowlist files and exit",
    )
    args = parser.parse_args(argv)

    patterns, excludes = load_allow_exclude(ALLOWLIST_PATH)
    excludes_t = tuple(excludes)
    files = resolve_files(patterns, REPO_ROOT, excludes_t)
    if not files:
        raise SystemExit(
            "allowlist resolved to zero files — check docs/synced-paths.yaml"
        )

    if args.list_files:
        # Machine-readable only (workflow gate uses exact-line match).
        for rel in files:
            print(rel.as_posix())
        return 0

    print(
        f"allowlist patterns: {len(patterns)}; exclude: {len(excludes_t)}; files: {len(files)}",
        flush=True,
    )

    source_sha = git_out(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
    token = resolve_token()
    skips = {
        "api": args.skip_api,
        "sql_to_arc": args.skip_sql_to_arc,
        "harvester": args.skip_harvester,
    }

    for key, repo in TARGETS.items():
        if skips[key]:
            print(f"\n=== skip {key} ({repo}) ===", flush=True)
            continue
        sync_target(
            SyncTarget(
                key=key,
                repo=repo,
                files=files,
                source_sha=source_sha,
                dry_run=args.dry_run,
                token=token,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Copy allowlisted Devinfra paths into product repos and open sync PRs.

Path set comes only from docs/synced-paths.yaml. See docs/sync.md.
Typical callers: .github/workflows/sync-products.yml, or a manual local run.
"""

from __future__ import annotations

import argparse
import fnmatch
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

SYNC_BRANCH = "chore/devinfra-sync"
DRY_RUN_PREVIEW_LIMIT = 20


def load_allow_exclude(path: Path) -> tuple[list[str], list[str]]:
    """Load `allow` and `exclude` lists from the YAML SoT."""
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit(f"{path}: expected a YAML mapping at the root")
    allow = loaded.get("allow") or []
    exclude = loaded.get("exclude") or []
    if not isinstance(allow, list) or not isinstance(exclude, list):
        raise SystemExit(f"{path}: `allow` and `exclude` must be YAML lists")
    allow_s = [str(x).strip() for x in allow if str(x).strip()]
    exclude_s = [str(x).strip() for x in exclude if str(x).strip()]
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


def git_out(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    """Run a command and return stripped stdout; raise on non-zero exit."""
    return subprocess.check_output(cmd, cwd=cwd, env=env, text=True).strip()


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


def sync_target(req: SyncTarget) -> None:
    """Clone one product repo, copy files, force-push SYNC_BRANCH, open PR if needed."""
    print(f"\n=== target {req.key}: {req.repo} ===", flush=True)
    if req.dry_run:
        print(
            f"dry-run: would copy {len(req.files)} files and open/update sync PR",
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
        run(["git", "checkout", "-B", SYNC_BRANCH], cwd=dest, env=env)
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
                f"chore: sync shared Devinfra paths from {req.source_sha[:7]}",
            ],
            cwd=dest,
            env=env,
        )
        run(["git", "push", "-u", "origin", "HEAD", "--force"], cwd=dest, env=env)

        existing = git_out(
            [
                "gh",
                "pr",
                "list",
                "--repo",
                req.repo,
                "--head",
                SYNC_BRANCH,
                "--state",
                "open",
                "--json",
                "number",
                "--jq",
                ".[0].number // empty",
            ],
            cwd=dest,
            env=env,
        )
        if existing:
            print(f"updated existing PR #{existing} via force-push", flush=True)
            return

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
                "chore: sync shared Devinfra paths",
                "--body",
                body,
                "--head",
                SYNC_BRANCH,
            ],
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

    print(
        f"allowlist patterns: {len(patterns)}; exclude: {len(excludes_t)}; files: {len(files)}",
        flush=True,
    )

    if args.list_files:
        for rel in files:
            print(rel.as_posix())
        return 0

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

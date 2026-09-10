#!/usr/bin/env python3
"""Copy allowlisted Devinfra paths into product repos and open sync PRs.

Path set is derived only from docs/synced-paths.yaml (sole SoT). Hard excludes
from the same file apply even if a path is mis-listed under allow. See docs/sync.md.
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

DEFAULT_TARGETS: dict[str, str] = {
    "api": "fairagro/m4.2_advanced_middleware_api",
    "sql_to_arc": "fairagro/m4.2_sql_to_arc",
    "harvester": "fairagro/m4.2_middleware_harvester",
}

DRY_RUN_PREVIEW_LIMIT = 20


def load_synced_paths_yaml(path: Path) -> tuple[list[str], list[str]]:
    """Load allow/exclude path lists from docs/synced-paths.yaml via PyYAML.

    Expected shape::

        allow:
          - path/or/glob/**
        exclude:
          - never/copy/**
        overlays:   # optional; ignored by sync (docs / review-fixer)
          - product/local.md
    """
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
    """Normalize to repo-relative POSIX without stripping leading dots from filenames."""
    rel = path.replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def is_ignored_artifact(rel: str) -> bool:
    """Skip bytecode and other non-source artifacts under allowlisted trees."""
    return "__pycache__" in Path(rel).parts or Path(rel).suffix in {".pyc", ".pyo"}


def is_hard_excluded(rel: str, excludes: tuple[str, ...]) -> bool:
    """Return whether rel matches any glob from docs/synced-paths.yaml `exclude`."""
    rel = normalize_rel(rel)
    for glob in excludes:
        if "**" in glob:
            if _match_double_star(rel, glob):
                return True
        elif fnmatch.fnmatch(rel, glob) or fnmatch.fnmatch(Path(rel).name, glob):
            return True
        if fnmatch.fnmatch(rel, glob):
            return True
    return False


def _match_double_star(path: str, pattern: str) -> bool:
    """Match patterns like dir/** or a/b/** against path."""
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(prefix + "/")
    if "/**/" in pattern:
        left, right = pattern.split("/**/", 1)
        if not path.startswith(left + "/") and path != left:
            return False
        rest = path[len(left) + 1 :] if path.startswith(left + "/") else ""
        return fnmatch.fnmatch(rest, right) or any(
            fnmatch.fnmatch("/".join(rest.split("/")[i:]), right) for i in range(len(rest.split("/")))
        )
    return fnmatch.fnmatch(path, pattern.replace("**/", "").replace("/**", "/*"))


def _add_files_under(found: set[Path], root: Path, path: Path) -> None:
    """Add path (file) or all files under path (dir) to found as root-relative Paths."""
    if path.is_file():
        found.add(path.relative_to(root))
        return
    if path.is_dir():
        for child in path.rglob("*"):
            if child.is_file():
                found.add(child.relative_to(root))


def _resolve_one_pattern(found: set[Path], root: Path, pattern: str) -> None:
    """Expand one allowlist pattern into found."""
    pattern = normalize_rel(pattern)
    if pattern.endswith("/**"):
        _add_files_under(found, root, root / pattern[:-3])
        return
    if "*" in pattern or "?" in pattern or "[" in pattern:
        for match in root.glob(pattern):
            _add_files_under(found, root, match)
        return
    _add_files_under(found, root, root / pattern)


def resolve_files(patterns: list[str], root: Path, excludes: tuple[str, ...]) -> list[Path]:
    """Expand allowlist globs against root; return sorted unique relative Paths."""
    found: set[Path] = set()
    for raw in patterns:
        _resolve_one_pattern(found, root, raw)
    return sorted(
        rel
        for rel in found
        if not is_hard_excluded(rel.as_posix(), excludes) and not is_ignored_artifact(rel.as_posix())
    )


def copy_files(
    files: list[Path],
    src_root: Path,
    dest_root: Path,
    excludes: tuple[str, ...],
) -> int:
    """Copy allowlisted relative files from src_root into dest_root; return count copied."""
    copied = 0
    for rel in files:
        src = src_root / rel
        dest = dest_root / rel
        if is_hard_excluded(rel.as_posix(), excludes):
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1
    return copied


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    """Print and run a subprocess command; raise on non-zero exit."""
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def git_output(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    """Run a command and return stripped stdout; raise on non-zero exit."""
    return subprocess.check_output(cmd, cwd=cwd, env=env, text=True).strip()


@dataclass(frozen=True)
class SyncTargetRequest:
    """Parameters for syncing one product repository."""

    key: str
    repo: str
    files: list[Path]
    excludes: tuple[str, ...]
    source_sha: str
    dry_run: bool
    token: str | None


def sync_target(req: SyncTargetRequest) -> None:
    """Clone one product repo, copy allowlisted files, and open or update a sync PR."""
    print(f"\n=== target {req.key}: {req.repo} ===", flush=True)
    if req.dry_run:
        print(f"dry-run: would copy {len(req.files)} files and open/update sync PR", flush=True)
        for rel in req.files[:DRY_RUN_PREVIEW_LIMIT]:
            print(f"  {rel.as_posix()}")
        if len(req.files) > DRY_RUN_PREVIEW_LIMIT:
            print(f"  ... and {len(req.files) - DRY_RUN_PREVIEW_LIMIT} more")
        return

    if not req.token:
        raise SystemExit("live sync requires DEVINFRA_BOT_TOKEN (or GH_TOKEN for local testing)")

    env = os.environ.copy()
    env["GH_TOKEN"] = req.token
    env["GIT_TERMINAL_PROMPT"] = "0"

    branch = f"chore/devinfra-sync-{req.source_sha[:7]}"
    with tempfile.TemporaryDirectory(prefix=f"sync-{req.key}-") as tmp:
        dest = Path(tmp) / "repo"
        run(
            [
                "gh",
                "repo",
                "clone",
                req.repo,
                str(dest),
                "--",
                "--depth",
                "1",
            ],
            env=env,
        )
        # Prefer updating an existing open sync PR branch if present
        existing = ""
        try:
            existing = git_output(
                [
                    "gh",
                    "pr",
                    "list",
                    "--repo",
                    req.repo,
                    "--head",
                    branch,
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
        except subprocess.CalledProcessError:
            existing = ""

        run(["git", "checkout", "-B", branch], cwd=dest, env=env)
        copy_files(req.files, REPO_ROOT, dest, req.excludes)
        status = git_output(["git", "status", "--porcelain"], cwd=dest, env=env)
        if not status:
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

        body = f"""## Summary

Sync allowlisted shared paths from [`fairagro/m4.2_middleware_devinfra@{req.source_sha}`](https://github.com/fairagro/m4.2_middleware_devinfra/commit/{req.source_sha}).

Source of truth: [`docs/synced-paths.yaml`](https://github.com/fairagro/m4.2_middleware_devinfra/blob/main/docs/synced-paths.yaml).

Do **not** hand-edit these paths in this consumer — land fixes in Devinfra, then re-sync.

## Test plan

- [ ] Spot-check diff against allowlist / hard excludes
      (no `middleware/`, no `openspec/specs|changes`, no `reusable-*.yml`)
- [ ] CI green on this PR
"""
        if existing:
            print(f"updated existing PR #{existing} via force-push to {branch}", flush=True)
            return

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
                branch,
            ],
            cwd=dest,
            env=env,
        )


def resolve_token() -> str | None:
    """Return the first non-empty bot/dev token from the environment, or None."""
    for key in ("DEVINFRA_BOT_TOKEN", "GH_TOKEN"):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return None


def allowlisted_changed_since(files: list[Path], *, base: str = "HEAD~1") -> bool | None:
    """Return True/False if git can diff base..HEAD against allowlist; None if unknown."""
    allow = {rel.as_posix() for rel in files}
    try:
        changed = git_output(
            ["git", "diff", "--name-only", f"{base}..HEAD"],
            cwd=REPO_ROOT,
        )
    except subprocess.CalledProcessError:
        return None
    if not changed:
        return False
    return any(normalize_rel(line) in allow for line in changed.splitlines() if line.strip())


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
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
        help="Print resolved allowlist files and exit (implies local-only)",
    )
    parser.add_argument(
        "--skip-if-unchanged",
        action="store_true",
        help=(
            "Exit 0 without opening PRs when no allowlisted path changed vs HEAD~1 "
            "(used on push to main; path set still comes only from the allowlist)"
        ),
    )
    return parser


def _load_resolved_files() -> tuple[list[str], tuple[str, ...], list[Path]]:
    """Load YAML allow/exclude and resolve files against the repo root."""
    patterns, excludes = load_synced_paths_yaml(ALLOWLIST_PATH)
    excludes_t = tuple(excludes)
    files = resolve_files(patterns, REPO_ROOT, excludes_t)
    if not files:
        raise SystemExit("allowlist resolved to zero files — check docs/synced-paths.yaml")
    return patterns, excludes_t, files


def _print_list_files(files: list[Path], excludes: tuple[str, ...]) -> None:
    """Print resolved paths and fail if a hard-excluded tree leaked into the set."""
    for rel in files:
        assert not is_hard_excluded(rel.as_posix(), excludes), rel
        print(rel.as_posix())
    for rel in files:
        posix = rel.as_posix()
        if (
            posix.startswith("middleware/")
            or posix.startswith("openspec/specs/")
            or posix.startswith("openspec/changes/")
        ):
            raise SystemExit(f"hard exclude leaked: {posix}")
        if posix.startswith(".github/workflows/") and Path(posix).name.startswith("reusable-"):
            raise SystemExit(f"hard exclude leaked: {posix}")


def _should_skip_unchanged(files: list[Path]) -> bool:
    """Return True when --skip-if-unchanged should exit early."""
    changed = allowlisted_changed_since(files)
    if changed is False:
        print(
            "no allowlisted paths changed since HEAD~1; skip sync (sole path SoT: docs/synced-paths.yaml)",
            flush=True,
        )
        return True
    if changed is None:
        print("could not diff HEAD~1..HEAD; proceeding with sync", flush=True)
    return False


def main(argv: list[str] | None = None) -> int:
    """Run product-repo sync CLI; return process exit code."""
    args = _build_parser().parse_args(argv)
    patterns, excludes, files = _load_resolved_files()
    print(
        f"allowlist patterns: {len(patterns)}; exclude: {len(excludes)}; files: {len(files)}",
        flush=True,
    )

    if args.list_files:
        _print_list_files(files, excludes)
        return 0

    if args.dry_run:
        for rel in files:
            assert not is_hard_excluded(rel.as_posix(), excludes), rel

    if args.skip_if_unchanged and _should_skip_unchanged(files):
        return 0

    source_sha = git_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
    token = resolve_token()
    skips = {
        "api": args.skip_api,
        "sql_to_arc": args.skip_sql_to_arc,
        "harvester": args.skip_harvester,
    }

    for key, repo in DEFAULT_TARGETS.items():
        if skips[key]:
            print(f"\n=== skip {key} ({repo}) ===", flush=True)
            continue
        sync_target(
            SyncTargetRequest(
                key=key,
                repo=repo,
                files=files,
                excludes=excludes,
                source_sha=source_sha,
                dry_run=args.dry_run,
                token=token,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())

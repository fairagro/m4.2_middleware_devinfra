"""Unit tests for profile-based synced-paths loading in sync-products."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync-products.py"


def _load_sync_module():

    spec = importlib.util.spec_from_file_location("sync_products", SYNC_SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    # dataclasses needs the module registered before class bodies run
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def sync():
    return _load_sync_module()


def test_load_repo_yaml_has_foundation_and_infra(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    assert "foundation" in config.profiles
    assert "python-product" in config.profiles
    assert "infrastructure" in config.targets
    assert config.targets["infrastructure"][0] == "fairagro/m4.2_infrastructure"
    assert config.targets["infrastructure"][1] == ("foundation",)
    assert config.targets["api"][1] == ("foundation", "python-product")


def test_foundation_excludes_renovate_and_devcontainer(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    foundation = set(sync.effective_allow(config, ("foundation",)))
    assert "scripts/ai/**" in foundation
    assert ".agents/skills/uv/**" in foundation
    assert "scripts/bin/m42-ai" in foundation
    assert "renovate.json" not in foundation
    assert "versions.env" not in foundation
    assert ".devcontainer/Dockerfile" not in foundation
    assert ".pre-commit-config.yaml" not in foundation


def test_product_union_includes_wave_a_surfaces(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    union = set(sync.effective_allow(config, sync.product_union_profiles(config)))
    assert "renovate.json" in union
    assert ".devcontainer/Dockerfile" in union
    assert "scripts/ai/**" in union


def test_legacy_flat_allow_still_loads(sync) -> None:
    text = """
allow:
  - scripts/ai/**
exclude:
  - middleware/**
overlays: []
"""
    config = sync.load_sync_config_text(text, source="test-legacy")
    assert sync._LEGACY_PROFILE in config.profiles
    assert set(config.targets) == {"api", "sql_to_arc", "harvester"}
    patterns, excludes = sync.load_allow_exclude_text(text, source="test-legacy")
    assert patterns == ["scripts/ai/**"]
    assert "middleware/**" in excludes


def test_profiles_reject_top_level_allow(sync) -> None:
    text = """
profiles:
  foundation:
    allow: [a]
targets:
  infrastructure:
    repo: fairagro/m4.2_infrastructure
    profiles: [foundation]
allow:
  - b
exclude: []
overlays: []
"""
    with pytest.raises(SystemExit, match="top-level `allow`"):
        sync.load_sync_config_text(text, source="test-dup")


def test_resolve_head_infra_smaller_than_product_union(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    product = sync.resolve_files(
        sync.effective_allow(config, sync.product_union_profiles(config)),
        REPO_ROOT,
        config.excludes,
    )
    infra = sync.resolve_files(
        sync.effective_allow(config, config.targets["infrastructure"][1]),
        REPO_ROOT,
        config.excludes,
    )
    assert infra
    assert len(infra) < len(product)
    infra_set = {p.as_posix() for p in infra}
    product_set = {p.as_posix() for p in product}
    assert infra_set <= product_set
    assert not any(p.startswith(".devcontainer/") for p in infra_set)
    assert any("scripts/ai/" in p or p.startswith("scripts/ai/") for p in infra_set)

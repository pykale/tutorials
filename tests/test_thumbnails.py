"""Tests for the placeholder thumbnail generator.

Covers the two behaviours the task calls out -- output naming and fallback -- plus determinism (the
property the ``--check`` CI guard relies on) and that a draft is never dressed up as a finished
tutorial.
"""

from __future__ import annotations

from pathlib import Path

from generate_thumbnails import (
    SYMBOLS,
    build,
    resolve_thumbnail,
    thumbnail_filename,
    thumbnail_svg,
)
from models import Catalog


def test_filename_naming():
    assert thumbnail_filename("cifar_isonet") == "cifar_isonet.svg"


def test_svg_is_deterministic():
    a = thumbnail_svg("A tutorial", "#2563eb", "nodes", badge="Draft")
    b = thumbnail_svg("A tutorial", "#2563eb", "nodes", badge="Draft")
    assert a == b


def test_svg_contains_title_accent_and_badge():
    svg = thumbnail_svg("Domain adaptation", "#0f766e", "molecule", badge="Draft")
    assert svg.startswith("<svg")
    assert "Domain adaptation" in svg
    assert "#0f766e" in svg
    assert "Draft" in svg  # status carried by text, not colour alone
    assert 'role="img"' in svg and 'aria-label=' in svg


def test_no_badge_when_none():
    svg = thumbnail_svg("Written tutorial", "#2563eb", "nodes", badge=None)
    assert "Draft" not in svg


def test_unknown_symbol_falls_back_to_nodes():
    # Must not raise; unknown ids degrade gracefully rather than crashing the build.
    svg = thumbnail_svg("X", "#dc2626", "not_a_symbol")
    assert svg.startswith("<svg")


def test_every_catalog_icon_has_a_symbol():
    for bucket in Catalog.load().buckets:
        assert bucket.icon in SYMBOLS, f"{bucket.id.value} icon {bucket.icon!r} has no drawing"


def test_resolve_prefers_real_thumbnail(tmp_path):
    real = tmp_path / "thumb.png"
    real.write_text("x")
    assert resolve_thumbnail("cifar_isonet", real) == real.as_posix()


def test_resolve_falls_back_to_placeholder(tmp_path):
    missing = tmp_path / "nope.png"
    assert resolve_thumbnail("cifar_isonet", missing) == "_static/thumbnails/cifar_isonet.svg"
    assert resolve_thumbnail("cifar_isonet", None) == "_static/thumbnails/cifar_isonet.svg"


def test_build_writes_one_per_tutorial_plus_empty_domains():
    from generate_thumbnails import THUMBNAIL_DIR

    build()
    catalog = Catalog.load()
    for path in catalog.iter_relative_paths():
        slug = Path(path).name
        assert (THUMBNAIL_DIR / f"{slug}.svg").exists(), slug
    # Materials is empty -> gets a domain tile so its card is not blank.
    assert (THUMBNAIL_DIR / "domain_materials.svg").exists()


def test_check_mode_passes_after_build():
    build()
    assert build(check=True) == 0

"""Tests for the homepage/list-page generators and the extended catalogue model."""

from __future__ import annotations

import generate_homepage
from generate_homepage import build
from models import Catalog


def test_catalog_has_ecosystem_and_paths():
    catalog = Catalog.load()
    assert catalog.ecosystem, "ecosystem entries expected"
    assert catalog.learning_paths, "learning paths expected"


def test_others_bucket_is_labelled_others_and_listed_last():
    catalog = Catalog.load()
    others = next(b for b in catalog.buckets if b.id.value == "others")
    assert others.label == "Others"  # matches the folder name (others/)
    assert catalog.buckets[-1].id.value == "others"  # listed last, not first


def test_learning_path_slugs_are_all_known():
    catalog = Catalog.load()
    known = set(catalog.slug_to_path())
    for path in catalog.learning_paths:
        for slug in path.tutorials:
            assert slug in known, f"{path.id} references unknown {slug}"


def test_ecosystem_planned_entries_have_no_url():
    catalog = Catalog.load()
    for entry in catalog.ecosystem:
        if entry.planned:
            assert entry.url is None, f"{entry.name} is planned but carries a url"


def test_build_writes_all_partials(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_homepage, "GENERATED_DIR", tmp_path)
    count = build()
    assert count == 6
    for name in ["news.rst", "domains.rst", "paths.rst", "featured_paths.rst", "ecosystem.rst", "status_table.rst"]:
        assert (tmp_path / name).exists(), name


def test_domains_partial_uses_others_and_counts(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_homepage, "GENERATED_DIR", tmp_path)
    build()
    domains = (tmp_path / "domains.rst").read_text(encoding="utf-8")
    assert "grid-item-card:: Others" in domains
    assert "grid-item-card:: General" not in domains
    assert "10 tutorials" in domains  # Others has 10
    assert "Coming soon" in domains  # Materials
    # Others is rendered last.
    assert domains.rindex("Others") > domains.rindex("Protein")


def test_news_partial_reads_the_data_file(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_homepage, "GENERATED_DIR", tmp_path)
    build()
    news = (tmp_path / "news.rst").read_text(encoding="utf-8")
    assert "Domain-based tutorial structure" in news
    assert "grid-item-card" not in news


def test_status_table_uses_catalog_domain_label(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_homepage, "GENERATED_DIR", tmp_path)
    build()
    status = (tmp_path / "status_table.rst").read_text(encoding="utf-8")
    assert "     - Others\n" in status
    assert "     - general\n" not in status

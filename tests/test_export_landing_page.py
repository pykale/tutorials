"""Tests for the landing-page exporter.

The landing page is a separate codebase consuming this JSON, so the shape of the payload is a
contract. These tests pin the parts the site depends on.
"""

from __future__ import annotations

import export_landing_page
from export_landing_page import build_payload
from models import Catalog


def test_payload_has_every_tutorial():
    payload = build_payload()
    assert len(payload["tutorials"]) == len(Catalog.load().iter_relative_paths())


def test_every_bucket_is_present_even_when_empty():
    """materials has no tutorials; the site still needs the bucket to render its placeholder."""
    payload = build_payload()
    ids = [bucket["id"] for bucket in payload["buckets"]]
    # "others" is listed last (matches the catalogue order).
    assert ids == ["protein", "cancer", "cardiac", "materials", "others"]
    materials = next(bucket for bucket in payload["buckets"] if bucket["id"] == "materials")
    assert materials["count"] == 0


def test_bucket_counts_sum_to_tutorial_count():
    payload = build_payload()
    assert sum(bucket["count"] for bucket in payload["buckets"]) == len(payload["tutorials"])


def test_group_is_set_only_for_nested_tutorials():
    payload = build_payload()
    by_slug = {entry["slug"]: entry for entry in payload["tutorials"]}
    assert by_slug["cifar_isonet"]["group"] == "image_classification"
    assert by_slug["action_recognition"]["group"] is None


def test_facets_cover_every_filter_the_site_offers():
    payload = build_payload()
    expected = {"domain", "task", "modality", "method", "fusion", "dataset", "difficulty", "hardware"}
    assert set(payload["facets"]) == expected
    for name, values in payload["facets"].items():
        assert values, f"facet {name} is empty"
        assert all(item["count"] > 0 for item in values)


def test_colab_and_binder_links_are_hidden_until_notebooks_are_published(monkeypatch):
    payload = build_payload()
    assert all(entry["links"]["colab"] is None and entry["links"]["binder"] is None for entry in payload["tutorials"])

    monkeypatch.setattr(export_landing_page, "NOTEBOOKS_PUBLISHED", True)
    by_slug = {entry["slug"]: entry for entry in build_payload()["tutorials"]}

    # action_recognition needs a GPU and hours of compute: neither launcher should be offered.
    assert by_slug["action_recognition"]["links"]["colab"] is None
    assert by_slug["action_recognition"]["links"]["binder"] is None

    # Once notebooks exist, metadata decides which launchers are offered.
    assert by_slug["synthetic_domain_adaptation"]["links"]["colab"].startswith("https://colab.research.google.com/")
    assert by_slug["synthetic_domain_adaptation"]["links"]["binder"].startswith("https://mybinder.org/")


def test_source_links_point_at_the_tutorial_folder():
    payload = build_payload()
    for entry in payload["tutorials"]:
        assert entry["links"]["source"].endswith(entry["path"])

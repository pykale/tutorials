"""Tests for the schema and bucket-page generators.

Both are 'generated, not hand-edited' artefacts; these tests assert the generation is deterministic
and that the committed schema is current, which is what ``make validate`` relies on.
"""

from __future__ import annotations

import json

from generate_bucket_pages import _gallery_doc, build
from generate_schema import build_schema
from models import Catalog


def test_schema_is_valid_json_and_stable():
    first = build_schema()
    second = build_schema()
    assert first == second, "schema generation must be deterministic"
    parsed = json.loads(first)
    assert parsed["$schema"].startswith("https://json-schema.org/")
    # A representative required field survives generation.
    assert "slug" in parsed["properties"]


def test_committed_schema_matches_generator():
    from models import SCHEMA_PATH

    assert SCHEMA_PATH.read_text(encoding="utf-8") == build_schema(), "run: python scripts/generate_schema.py"


def test_runnable_tutorials_have_installable_requirements():
    """Every tutorial the nightly job will execute must have a requirements.txt to install."""
    from pathlib import Path

    from list_runnable import runnable_paths
    from models import REPO_ROOT

    paths = runnable_paths()
    assert paths, "expected at least one runnable tutorial (the reference narrative)"
    for path in paths:
        assert (REPO_ROOT / Path(path) / "requirements.txt").exists(), path


def test_is_runnable_predicate():
    """draft or GPU-required tutorials are never runnable; a written CPU one is."""
    import yaml
    from models import REPO_ROOT, TutorialMetadata

    def load(rel):
        return TutorialMetadata.model_validate(
            yaml.safe_load((REPO_ROOT / rel / "metadata.yml").read_text(encoding="utf-8"))
        )

    assert load("others/image_classification/digit_domain_adaptation").is_runnable
    assert not load("others/image_classification/cifar_isonet").is_runnable  # draft
    assert not load("others/action_recognition").is_runnable  # gpu_required


def test_gallery_doc_points_at_plot_narrative():
    doc = _gallery_doc("others/image_classification/cifar_isonet")
    assert doc == "/_gallery/others/image_classification/cifar_isonet/plot_cifar_isonet"


def test_bucket_pages_generate_for_every_bucket(tmp_path, monkeypatch):
    import generate_bucket_pages as gbp

    monkeypatch.setattr(gbp, "PAGES_DIR", tmp_path)
    written = build()
    assert written == len(Catalog.load().buckets)
    # materials has no tutorials -> its page must carry the placeholder note, not a broken grid.
    materials = (tmp_path / "materials.rst").read_text(encoding="utf-8")
    assert "No tutorial maps to this domain yet" in materials
    # a populated bucket links to plot_ narratives, never to a bare index.
    others = (tmp_path / "others.rst").read_text(encoding="utf-8")
    assert "/plot_" in others
    assert "/index" not in others

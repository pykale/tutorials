"""Tests for the catalog validator.

These assert the validator *catches* things, not merely that the current tree passes. A validator
that returns an empty list unconditionally would satisfy "the repo is valid" while protecting
nothing.
"""

from __future__ import annotations

import pytest
import yaml
from models import Catalog, TutorialMetadata
from pydantic import ValidationError
from validate_catalog import validate


def test_current_tree_is_valid():
    assert validate() == []


def test_every_catalogued_tutorial_has_metadata():
    catalog = Catalog.load()
    paths = catalog.iter_relative_paths()
    assert len(paths) == 16, "expected all 16 migrated examples to be catalogued"


def test_strict_drafts_flags_the_stubs():
    """Most tutorials are still stubs; --strict-drafts must say so rather than pass silently."""
    errors = validate(strict_drafts=True)
    assert any("draft" in error for error in errors)


def test_metadata_rejects_unknown_field():
    """extra="forbid" is what stops a typo'd key from being silently ignored."""
    with pytest.raises(ValidationError):
        TutorialMetadata.model_validate(
            {
                "title": "x",
                "slug": "x",
                "summary": "a" * 30,
                "domain": "others",
                "task": "t",
                "modality": ["image"],
                "method": ["m"],
                "difficulty": "beginner",
                "source_example": "x",
                "run_command": "python main.py",
                "estimated_runtime": "~1 min",
                "typo_field": True,
            }
        )


def test_metadata_rejects_bad_slug():
    with pytest.raises(ValidationError):
        TutorialMetadata.model_validate(
            {
                "title": "x",
                "slug": "Not-A-Slug",
                "summary": "a" * 30,
                "domain": "others",
                "task": "t",
                "modality": ["image"],
                "method": ["m"],
                "difficulty": "beginner",
                "source_example": "x",
                "run_command": "python main.py",
                "estimated_runtime": "~1 min",
            }
        )


def test_metadata_requires_at_least_one_modality():
    with pytest.raises(ValidationError):
        TutorialMetadata.model_validate(
            {
                "title": "x",
                "slug": "x",
                "summary": "a" * 30,
                "domain": "others",
                "task": "t",
                "modality": [],
                "method": ["m"],
                "difficulty": "beginner",
                "source_example": "x",
                "run_command": "python main.py",
                "estimated_runtime": "~1 min",
            }
        )


def test_catalog_rejects_unknown_bucket():
    with pytest.raises(ValidationError):
        Catalog.model_validate(
            yaml.safe_load(
                """
                version: 1
                buckets:
                  - id: astrophysics
                    label: Astrophysics
                    color: "#123456"
                    summary: not a real domain
                """
            )
        )


def test_validator_flags_a_missing_narrative(tmp_path, monkeypatch):
    """Deleting a tutorial's plot_<slug>.py must be caught -- teeth on the narrative check."""
    import validate_catalog as vc
    from models import REPO_ROOT

    narrative = REPO_ROOT / "others" / "image_classification" / "cifar_isonet" / "plot_cifar_isonet.py"
    backup = narrative.read_text(encoding="utf-8")
    narrative.unlink()
    try:
        errors = vc.validate()
        assert any("plot_cifar_isonet.py does not exist" in e for e in errors)
    finally:
        narrative.write_text(backup, encoding="utf-8")


def test_run_command_matches_entry_point():
    """A run_command that does not invoke the declared entry point is a copy-paste error."""
    catalog = Catalog.load()
    from models import REPO_ROOT

    for path in catalog.iter_relative_paths():
        metadata = TutorialMetadata.model_validate(
            yaml.safe_load((REPO_ROOT / path / "metadata.yml").read_text(encoding="utf-8"))
        )
        assert metadata.entry_point in metadata.run_command, path

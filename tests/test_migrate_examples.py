"""Tests for the migration script.

The migration is idempotent and must never clobber authored files or silently drop an example. These
tests assert those guarantees against a temporary tree, and check the source patches still match the
real files.
"""

from __future__ import annotations

from migrate_examples import (
    MIGRATIONS,
    POST_MIGRATION_PATCHES,
    _is_authored,
    _is_excluded,
    apply_patches,
)
from models import REPO_ROOT, Catalog


def test_authored_files_are_recognised():
    for name in ["plot_cifar_isonet.py", "metadata.yml", "README.md", "requirements.txt"]:
        assert _is_authored(name), name


def test_generated_and_example_files_are_not_authored():
    # main.py etc. are copied from upstream and must be overwritable by a re-sync.
    for name in ["main.py", "config.py", "model.py", "README.upstream.md"]:
        assert not _is_authored(name), name


def test_excluded_dirs_and_suffixes(tmp_path):
    root = tmp_path
    (root / "outputs").mkdir()
    (root / "outputs" / "run.log").write_text("x")
    (root / "weights.pth").write_text("x")
    (root / "main.py").write_text("x")
    assert _is_excluded(root / "outputs" / "run.log", root)  # excluded dir
    assert _is_excluded(root / "weights.pth", root)  # excluded suffix
    assert not _is_excluded(root / "main.py", root)  # ordinary source


def test_every_migration_target_exists_on_disk():
    """The mapping is the source of truth; every target must actually be present."""
    for migration in MIGRATIONS:
        assert (REPO_ROOT / migration.target).is_dir(), migration.target


def test_every_catalogued_tutorial_has_a_migration():
    """No tutorial may exist without a recorded provenance in MIGRATIONS (except materials)."""
    targets = {m.target for m in MIGRATIONS}
    for path in Catalog.load().iter_relative_paths():
        assert path in targets, f"{path} has no entry in MIGRATIONS"


def test_migration_sources_are_unique():
    sources = [m.source for m in MIGRATIONS]
    assert len(sources) == len(set(sources))


def test_post_migration_patches_are_satisfied():
    """apply_patches raises if a patch matches neither old nor new text; a clean dry-run proves the
    patched files are in one of the two expected states."""
    # Should not raise, and should report zero changes because the tree is already patched.
    assert apply_patches(dry_run=True) == 0


def test_patch_targets_exist():
    for relative in POST_MIGRATION_PATCHES:
        assert (REPO_ROOT / relative).exists(), relative

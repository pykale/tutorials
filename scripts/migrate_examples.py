"""Copy PyKale examples into the tutorial tree.

One-shot in principle, idempotent in practice: re-running overwrites the copied example files and
leaves authored files (``plot_<slug>.py``, ``metadata.yml``, ``README.md``, ``requirements.txt``) alone
unless ``--force-authored`` is passed. That distinction matters -- the whole point is that hand-written
narrative survives a re-sync from upstream.

    python scripts/migrate_examples.py --pykale-root ../pykale --dry-run
    python scripts/migrate_examples.py --pykale-root ../pykale
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from models import REPO_ROOT, TUTORIALS_ROOT

# Directory names never copied, wherever they appear.
EXCLUDED_DIRS = {"__pycache__", "outputs", "data", "datasets", ".ipynb_checkpoints", "lightning_logs"}

# File patterns never copied. Datasets and checkpoints stay out of git; `__init__.py` goes because
# the tutorial tree is a collection of scripts, not an importable package.
EXCLUDED_FILES = {"__init__.py"}
EXCLUDED_SUFFIXES = {".pyc", ".pth", ".ckpt", ".zip", ".tar", ".gz", ".npz"}

# Files this repo authors itself. Never clobbered by a re-sync. The narrative is plot_<slug>.py,
# matched by prefix rather than exact name.
AUTHORED_FILES = {"metadata.yml", "README.md", "requirements.txt"}
AUTHORED_PREFIXES = ("plot_",)


def _is_authored(name: str) -> bool:
    return name in AUTHORED_FILES or name.startswith(AUTHORED_PREFIXES)


@dataclass(frozen=True)
class Migration:
    source: str  # folder under pykale/examples
    target: str  # path relative to the repo root


MIGRATIONS: List[Migration] = [
    Migration("cifar_cnntransformer", "others/image_classification/cifar_cnn_transformer"),
    Migration("cifar_isonet", "others/image_classification/cifar_isonet"),
    Migration("digits_dann", "others/image_classification/digit_domain_adaptation"),
    Migration("office_multisource_adapt", "others/image_classification/office_multisource_adaptation"),
    Migration("avmnist_multimodal", "others/audio_visual_digit_classification"),
    Migration("action_dann", "others/action_recognition"),
    Migration("fewshot_protonet", "others/fewshot_image_classification"),
    Migration("multisite_neuroimg_adapt", "others/multisite_neuroimaging_classification"),
    Migration("toy_domain_adaptation", "others/synthetic_domain_adaptation"),
    Migration("video_loading", "others/video_data_loading"),
    Migration("bindingdb_deepdta", "protein/drug_target_affinity_prediction"),
    Migration("bindingdb_drugban", "protein/drug_target_interaction_prediction"),
    Migration("polypharmacy_gripnet", "protein/polypharmacy_side_effect_prediction"),
    Migration("multiomics_mogonet", "cancer/multiomics_cancer_classification"),
    Migration("cmri_mpca", "cardiac/cardiac_mri_diagnosis"),
    Migration("landmark_uncertainty", "cardiac/landmark_uncertainty_estimation"),
]


# Edits applied to copied files after every sync. Upstream examples live inside the `examples`
# package and a few import each other through it; here they are standalone folders, so those imports
# must become local. Keeping the patches here rather than editing files by hand means a re-sync
# cannot silently undo them -- and a patch that stops applying is a loud failure, not a stale fix.
POST_MIGRATION_PATCHES: Dict[str, List[tuple]] = {
    "protein/drug_target_interaction_prediction/test.py": [
        (
            "from examples.bindingdb_drugban.model import",
            "from model import",
        ),
    ],
}


def apply_patches(dry_run: bool) -> int:
    """Apply the post-migration source patches to already-copied files.

    Args:
        dry_run: If True, report what would change without writing.

    Returns:
        int: Number of files patched (or that would be patched).

    Raises:
        FileNotFoundError: If a patch target does not exist on disk.
        ValueError: If a patch matches neither its old nor its new text, which means the
            upstream file changed shape and the patch needs revisiting.
    """
    applied = 0
    for relative, edits in POST_MIGRATION_PATCHES.items():
        path = TUTORIALS_ROOT / relative
        if not path.exists():
            raise FileNotFoundError(f"patch target missing: {path}")
        text = original = path.read_text(encoding="utf-8")
        for old, new in edits:
            if old not in text and new not in text:
                raise ValueError(f"patch for {relative} matches neither old nor new text: {old!r}")
            text = text.replace(old, new)
        if text != original:
            if dry_run:
                print(f"  would patch {relative}")
            else:
                path.write_text(text, encoding="utf-8")
            applied += 1
    return applied


def _is_excluded(path: Path, source_root: Path) -> bool:
    relative = path.relative_to(source_root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return True
    if path.name in EXCLUDED_FILES or path.suffix in EXCLUDED_SUFFIXES:
        return True
    return False


def migrate_one(migration: Migration, examples_root: Path, dry_run: bool, force_authored: bool) -> Dict[str, int]:
    """Copy one example folder into its tutorial target.

    Args:
        migration: The source-to-target mapping for one example.
        examples_root: Absolute path to ``pykale/examples``.
        dry_run: If True, print the plan without touching disk.
        force_authored: If True, overwrite authored files (``plot_*.py``, ``metadata.yml``,
            ``README.md``, ``requirements.txt``) instead of preserving them.

    Returns:
        dict[str, int]: Counts keyed ``"copied"``, ``"skipped"`` and ``"preserved"``.

    Raises:
        FileNotFoundError: If the source example folder does not exist.
    """
    source_root = examples_root / migration.source
    target_root = TUTORIALS_ROOT / migration.target

    if not source_root.is_dir():
        raise FileNotFoundError(f"source example not found: {source_root}")

    counts = {"copied": 0, "skipped": 0, "preserved": 0}

    for source_path in sorted(source_root.rglob("*")):
        if source_path.is_dir() or _is_excluded(source_path, source_root):
            counts["skipped"] += source_path.is_file()
            continue

        relative = source_path.relative_to(source_root)
        target_path = target_root / relative
        at_root = len(relative.parts) == 1

        if at_root and _is_authored(target_path.name) and target_path.exists() and not force_authored:
            counts["preserved"] += 1
            continue

        # The example's own README becomes README.upstream.md: the tutorial README is authored from
        # the template, but the original text is the raw material for it and for the metadata.
        # Nested READMEs (e.g. configs/README.md) are documentation of their folder -- leave them be.
        if at_root and target_path.name == "README.md":
            target_path = target_path.with_name("README.upstream.md")

        if dry_run:
            print(f"  would copy {source_path.relative_to(examples_root)} -> {target_path.relative_to(REPO_ROOT)}")
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
        counts["copied"] += 1

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pykale-root", type=Path, default=REPO_ROOT.parent / "pykale")
    parser.add_argument("--dry-run", action="store_true", help="print the plan without touching disk")
    parser.add_argument("--force-authored", action="store_true", help="also overwrite authored files")
    parser.add_argument("--only", help="migrate a single source example by name")
    args = parser.parse_args()

    examples_root = (args.pykale_root / "examples").resolve()
    if not examples_root.is_dir():
        parser.error(f"no examples/ directory under {args.pykale_root}")

    migrations = MIGRATIONS
    if args.only:
        migrations = [m for m in MIGRATIONS if m.source == args.only]
        if not migrations:
            parser.error(f"unknown example {args.only!r}")

    totals = {"copied": 0, "skipped": 0, "preserved": 0}
    for migration in migrations:
        print(f"{migration.source} -> {migration.target}")
        counts = migrate_one(migration, examples_root, args.dry_run, args.force_authored)
        for key, value in counts.items():
            totals[key] += value

    patched = apply_patches(args.dry_run)
    if patched:
        print(f"\napplied {patched} post-migration patch(es)")

    # Anything in examples/ that no migration claims is a gap in MIGRATIONS, not a file to ignore.
    claimed = {m.source for m in MIGRATIONS}
    present = {p.name for p in examples_root.iterdir() if p.is_dir() and p.name not in EXCLUDED_DIRS}
    orphans = sorted(present - claimed)
    if orphans:
        print(f"\nWARNING: unmapped examples: {', '.join(orphans)}")

    verb = "would copy" if args.dry_run else "copied"
    print(f"\n{verb} {totals['copied']} files; skipped {totals['skipped']}; preserved {totals['preserved']} authored")
    return 1 if orphans else 0


if __name__ == "__main__":
    sys.exit(main())

"""Check that the catalog, the metadata files and the directory tree all agree.

Five checks, each of which has a real failure mode behind it:

1. Catalog parses and every listed tutorial folder exists.       -- catches typos in the catalog
2. Every tutorial folder on disk is listed in the catalog.        -- catches folders added silently
3. Every metadata.yml validates against the model.                -- catches malformed metadata
4. metadata slug/domain match the folder path.                    -- catches copy-paste between tutorials
5. Every migrated example is claimed by exactly one tutorial.     -- catches an example dropped in migration

Run via ``make validate``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

import yaml
from migrate_examples import MIGRATIONS
from models import NON_TUTORIAL_DIRS, REPO_ROOT, TUTORIALS_ROOT, Catalog, TutorialMetadata
from pydantic import ValidationError


def _discover_tutorial_dirs() -> List[str]:
    """Every directory holding a metadata.yml, as a repo-relative posix path.

    Domain folders sit at the repo root alongside scripts/, tests/ and _shared/, so the walk starts
    from the domain directories rather than from the root itself -- otherwise a stray metadata.yml
    in a template or build directory would look like a tutorial.
    """
    found: List[str] = []
    for domain_dir in TUTORIALS_ROOT.iterdir():
        if not domain_dir.is_dir() or domain_dir.name in NON_TUTORIAL_DIRS or domain_dir.name.startswith("."):
            continue
        for metadata_path in domain_dir.rglob("metadata.yml"):
            found.append(metadata_path.parent.relative_to(REPO_ROOT).as_posix())
    return sorted(found)


def validate(strict_drafts: bool = False) -> List[str]:
    """Check that the catalog, the metadata files and the directory tree all agree.

    Args:
        strict_drafts: If True, also report any tutorial still marked ``draft: true``.

    Returns:
        list[str]: Human-readable problems, empty when everything is consistent.
    """
    errors: List[str] = []

    try:
        catalog = Catalog.load()
    except (ValidationError, yaml.YAMLError) as exc:
        return [f"tutorial_catalog.yml does not parse: {exc}"]

    catalogued = catalog.iter_relative_paths()
    on_disk = _discover_tutorial_dirs()

    # Learning paths reference tutorials by slug; a typo would silently drop a step from the homepage.
    known_slugs = set(catalog.slug_to_path())
    for path_def in catalog.learning_paths:
        for slug in path_def.tutorials:
            if slug not in known_slugs:
                errors.append(f"learning path {path_def.id!r} references unknown tutorial {slug!r}")

    for path in catalogued:
        if not (REPO_ROOT / path).is_dir():
            errors.append(f"catalog lists {path} but no such directory exists")
        elif not (REPO_ROOT / path / "metadata.yml").exists():
            errors.append(f"{path} has no metadata.yml")

    for path in on_disk:
        if path not in catalogued:
            errors.append(f"{path} exists on disk but is not listed in tutorial_catalog.yml")

    claimed_sources = set()
    for path in on_disk:
        metadata_path = REPO_ROOT / path / "metadata.yml"
        try:
            metadata = TutorialMetadata.model_validate(yaml.safe_load(metadata_path.read_text(encoding="utf-8")))
        except (ValidationError, yaml.YAMLError) as exc:
            errors.append(f"{path}/metadata.yml is invalid: {exc}")
            continue

        parts = Path(path).parts  # (<domain>, [group], <slug>)
        if metadata.slug != parts[-1]:
            errors.append(f"{path}: slug {metadata.slug!r} does not match the folder name {parts[-1]!r}")
        if metadata.domain.value != parts[0]:
            errors.append(f"{path}: domain {metadata.domain.value!r} does not match the folder {parts[0]!r}")
        if not (REPO_ROOT / path / metadata.entry_point).exists():
            errors.append(f"{path}: entry_point {metadata.entry_point!r} does not exist")
        # The gallery narrative is plot_<slug>.py; without it sphinx-gallery has nothing to render.
        if not (REPO_ROOT / path / f"plot_{metadata.slug}.py").exists():
            errors.append(f"{path}: narrative plot_{metadata.slug}.py does not exist")
        if strict_drafts and metadata.draft:
            errors.append(f"{path}: still marked draft")

        claimed_sources.add(metadata.source_example)

    for migration in MIGRATIONS:
        if migration.source not in claimed_sources:
            errors.append(f"example {migration.source!r} was migrated but no metadata.yml claims it")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict-drafts", action="store_true", help="also fail on any draft: true tutorial")
    args = parser.parse_args()

    errors = validate(strict_drafts=args.strict_drafts)
    if errors:
        print(f"{len(errors)} problem(s):\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    catalog = Catalog.load()
    print(f"OK: {len(catalog.iter_relative_paths())} tutorials across {len(catalog.buckets)} buckets")
    return 0


if __name__ == "__main__":
    sys.exit(main())

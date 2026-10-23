"""Build the ``sphinx_gallery_conf`` dict from the tutorial catalog.

Sphinx-gallery normally needs ``examples_dirs`` and ``gallery_dirs`` hand-maintained in ``conf.py``,
which drifts the moment someone adds a folder. Here both are derived from ``tutorial_catalog.yml``,
so adding a tutorial is a folder plus a catalog line and nothing else.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

# This file lives at source/_shared/gallery/, so the repo root is four levels up.
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from models import Catalog, TutorialMetadata  # noqa: E402

from .notebook_first_cell import notebook_header  # noqa: E402

# Narratives are named plot_<slug>.py: unique stems (sphinx-gallery flattens download names, so every
# file called tutorial.py would collide), and the plot_ prefix is the gallery's own idiom for "a
# script to render". This mirrors PyTorch's *_tutorial.py convention.
NARRATIVE_PREFIX = "plot_"


def _executable_slugs(catalog: Catalog) -> List[str]:
    """Slugs whose narrative is safe to *execute* during the build.

    A tutorial executes only when its narrative is written (``draft: false``) and it does not demand
    a GPU -- otherwise CI would try to train it. Everything else is still rendered as source, just not
    run. Driven by metadata so the build never trains something it should not.
    """
    runnable: List[str] = []
    for path in catalog.iter_relative_paths():
        metadata = TutorialMetadata.model_validate(
            yaml.safe_load((REPO_ROOT / path / "metadata.yml").read_text(encoding="utf-8"))
        )
        if metadata.is_runnable:
            runnable.append(metadata.slug)
    return runnable


def _gallery_dirs(catalog: Catalog) -> Tuple[List[str], List[str]]:
    """Source directories and their built counterparts, in catalog order.

    Gallery order follows the catalog rather than the filesystem, so ``others`` comes first and
    ``materials`` last regardless of alphabetical accidents.
    """
    sources: List[str] = []
    targets: List[str] = []
    for path in catalog.iter_relative_paths():
        sources.append(str(REPO_ROOT / path))
        targets.append(f"_gallery/{path}")
    return sources, targets


def build_gallery_conf(catalog: Catalog | None = None) -> Dict[str, Any]:
    """Build the ``sphinx_gallery_conf`` dict from the catalog.

    Args:
        catalog: Parsed catalog. Loaded from ``tutorial_catalog.yml`` when omitted.

    Returns:
        dict[str, Any]: A ``sphinx_gallery_conf`` mapping, with ``examples_dirs``,
        ``gallery_dirs``, execution/ignore patterns and thumbnail settings all derived from
        the catalog and per-tutorial metadata.
    """
    catalog = catalog or Catalog.load()
    sources, targets = _gallery_dirs(catalog)

    # Execute only the runnable narratives; render the rest as source. main.py/config.py/model.py are
    # never gallery scripts -- the ignore_pattern drops any .py that is not a plot_ narrative so they
    # do not each become a page.
    runnable = _executable_slugs(catalog)
    if runnable:
        filename_pattern = r"[\\/]" + f"{NARRATIVE_PREFIX}(" + "|".join(runnable) + r")\.py$"
    else:
        filename_pattern = r"(?!x)x"  # matches nothing: execute none

    return {
        "examples_dirs": sources,
        "gallery_dirs": targets,
        "filename_pattern": filename_pattern,
        # Every .py that is NOT a plot_ narrative is a supporting project file (main.py, config.py,
        # model.py, test.py) and must not become a gallery example. Anchored at start-or-slash so it
        # matches on the basename, which is what sphinx-gallery tests against.
        "ignore_pattern": r"(?:^|[\\/])(?!" + NARRATIVE_PREFIX + r")[^\\/]*\.py$",
        "download_all_examples": False,
        "remove_config_comments": True,
        "plot_gallery": True,
        "thumbnail_size": (400, 280),
        "default_thumb_file": str(REPO_ROOT / "source" / "_shared" / "assets" / "logos" / "pykale_logo.png"),
        "line_numbers": False,
        "show_signature": False,
        "min_reported_time": 10,
        "notebook_images": True,
        "first_notebook_cell": notebook_header(),
        "reference_url": {"kale": None},
        "backreferences_dir": "_gallery/backreferences",
        "doc_module": ("kale",),
    }

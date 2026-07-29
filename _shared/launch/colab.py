"""Google Colab launch URLs.

Colab opens a notebook straight from GitHub. Sphinx-gallery writes a ``.ipynb`` next to each built
page, so the URL points at the *generated* notebook path under ``docs/``, not at ``tutorial.py``.
"""

from __future__ import annotations

GITHUB_ORG = "pykale"
GITHUB_REPO = "tutorials"
DEFAULT_BRANCH = "main"

COLAB_BASE = "https://colab.research.google.com/github"
BADGE_IMAGE = "https://colab.research.google.com/assets/colab-badge.svg"


NOTEBOOK_DIR = "notebooks"


def notebook_path(relative_path: str) -> str:
    """Repo path of the notebook Colab should open for a tutorial.

    ``relative_path`` is the tutorial directory relative to the repo root, e.g.
    ``others/image_classification/cifar_isonet``; the notebook is sphinx-gallery's ``plot_<slug>``
    output for that folder.

    Colab can only open notebooks from GitHub, Drive or a gist -- not from the built docs site.
    Sphinx-gallery's notebooks are build artefacts under ``_gallery/`` (gitignored), so they are not
    reachable by URL as-is. PyTorch solves this by publishing the built site -- notebooks included --
    to a GitHub branch and pointing Colab at that branch. We adopt the same approach: CI copies the
    generated notebooks to ``notebooks/`` on the published branch. Wiring that up is Phase 2, tied to
    the docs-host decision; until then these URLs 404.

    Args:
        relative_path: Tutorial directory relative to the repo root, e.g.
            ``others/image_classification/cifar_isonet``.

    Returns:
        str: Repo-relative path to the tutorial's ``plot_<slug>.ipynb`` notebook.
    """
    slug = relative_path.rstrip("/").split("/")[-1]
    return f"{NOTEBOOK_DIR}/{relative_path}/plot_{slug}.ipynb"


def colab_url(relative_path: str, branch: str = DEFAULT_BRANCH) -> str:
    return f"{COLAB_BASE}/{GITHUB_ORG}/{GITHUB_REPO}/blob/{branch}/{notebook_path(relative_path)}"


def colab_badge_rst(relative_path: str, branch: str = DEFAULT_BRANCH) -> str:
    """reStructuredText badge for embedding in a gallery page."""
    return f".. image:: {BADGE_IMAGE}\n   :target: {colab_url(relative_path, branch)}\n   :alt: Open in Colab\n"

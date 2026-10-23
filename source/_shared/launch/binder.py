"""mybinder.org launch URLs.

Binder builds an environment from the repo root, so unlike Colab it needs no per-tutorial install
cell -- but it is slow to cold-start and cannot offer a GPU. Tutorials therefore opt in via
``binder: true`` in their metadata, and only CPU-only ones should.
"""

from __future__ import annotations

from urllib.parse import quote

GITHUB_ORG = "pykale"
GITHUB_REPO = "tutorials"
DEFAULT_BRANCH = "main"

BINDER_BASE = "https://mybinder.org/v2/gh"
BADGE_IMAGE = "https://mybinder.org/badge_logo.svg"

# Must match colab.NOTEBOOK_DIR: both point at notebooks once they are published on main.
NOTEBOOK_DIR = "notebooks"


def binder_url(relative_path: str, branch: str = DEFAULT_BRANCH) -> str:
    """Open Binder with the tutorial's generated notebook already loaded."""
    slug = relative_path.rstrip("/").split("/")[-1]
    notebook = quote(f"{NOTEBOOK_DIR}/{relative_path}/plot_{slug}.ipynb", safe="")
    return f"{BINDER_BASE}/{GITHUB_ORG}/{GITHUB_REPO}/{branch}?labpath={notebook}"


def binder_badge_rst(relative_path: str, branch: str = DEFAULT_BRANCH) -> str:
    return f".. image:: {BADGE_IMAGE}\n   :target: {binder_url(relative_path, branch)}\n   :alt: Launch Binder\n"

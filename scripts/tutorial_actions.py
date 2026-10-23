"""Derive the per-tutorial action links (GitHub source, Notebook download, Run in Colab).

All URLs are derived from the tutorial's catalogue path and ``site_meta`` -- never hard-coded per
tutorial. Colab and Notebook are only offered as working links when notebooks are actually published
(``site_meta.NOTEBOOKS_PUBLISHED``); otherwise they are returned disabled with an explanatory reason,
so the UI never shows a working-looking dead link.

``conf.py`` calls :func:`tutorial_actions` from an html-page-context hook for each gallery page and
puts the result in ``context["pky_tutorial"]``; ``source/_templates/tutorial-actions.html`` renders it.
"""

from __future__ import annotations

from typing import Dict, Optional, TypedDict

from site_meta import FEEDBACK_REPO, NOTEBOOKS_PUBLISHED, REPO_BRANCH

# Where CI is expected to publish sphinx-gallery notebooks (see source/_shared/launch/colab.py).
NOTEBOOK_DIR = "notebooks"


class TutorialAction(TypedDict):
    url: Optional[str]
    enabled: bool
    reason: Optional[str]


def source_path(rel_path: str, slug: str) -> str:
    """Repo path of a tutorial's narrative script, e.g. ``others/.../plot_cifar_isonet.py``."""
    return f"{rel_path}/plot_{slug}.py"


def github_source_url(rel_path: str, slug: str, repo: str = FEEDBACK_REPO, branch: str = REPO_BRANCH) -> str:
    """GitHub blob URL for the tutorial's source script."""
    return f"https://github.com/{repo}/blob/{branch}/{source_path(rel_path, slug)}"


def notebook_url(rel_path: str, slug: str, repo: str = FEEDBACK_REPO, branch: str = REPO_BRANCH) -> str:
    """Raw GitHub URL of the published notebook (valid only once notebooks are published)."""
    return f"https://github.com/{repo}/blob/{branch}/{NOTEBOOK_DIR}/{rel_path}/plot_{slug}.ipynb"


def colab_url(rel_path: str, slug: str, repo: str = FEEDBACK_REPO, branch: str = REPO_BRANCH) -> str:
    """Colab URL for the published notebook."""
    return f"https://colab.research.google.com/github/{repo}/blob/{branch}/{NOTEBOOK_DIR}/{rel_path}/plot_{slug}.ipynb"


def tutorial_actions(
    rel_path: str,
    slug: str,
    *,
    draft: bool = False,
    notebooks_published: bool = NOTEBOOKS_PUBLISHED,
) -> Dict[str, TutorialAction]:
    """Build the action set for one tutorial.

    Args:
        rel_path: Tutorial directory relative to the repo root (e.g. ``others/.../cifar_isonet``).
        slug: Tutorial slug.
        draft: Whether the narrative is still a draft (affects the Notebook tooltip only).
        notebooks_published: Whether generated notebooks are publicly available.

    Returns:
        dict: ``{action: {"url", "enabled", "reason"}}`` for ``github``, ``notebook`` and ``colab``.
        ``github`` is always enabled; the other two are enabled only when notebooks are published,
        and otherwise carry a human-readable ``reason`` for the disabled state.
    """
    github: TutorialAction = {"url": github_source_url(rel_path, slug), "enabled": True, "reason": None}

    if notebooks_published:
        notebook: TutorialAction = {"url": notebook_url(rel_path, slug), "enabled": True, "reason": None}
        colab: TutorialAction = {"url": colab_url(rel_path, slug), "enabled": True, "reason": None}
    else:
        reason = (
            "Notebook will be available when this draft becomes executable."
            if draft
            else "Notebook will be available once tutorials are published."
        )
        notebook = {"url": None, "enabled": False, "reason": reason}
        colab = {
            "url": None,
            "enabled": False,
            "reason": "Run in Colab will be available once notebooks are published.",
        }

    return {"github": github, "notebook": notebook, "colab": colab}


def gallery_pagename_to_tutorial(pagename: str) -> Optional[tuple[str, str]]:
    """Map a gallery pagename to ``(rel_path, slug)``, or None if it is not a tutorial page.

    ``_gallery/others/image_classification/cifar_isonet/plot_cifar_isonet`` ->
    ``("others/image_classification/cifar_isonet", "cifar_isonet")``.
    """
    prefix = "_gallery/"
    if not pagename.startswith(prefix):
        return None
    rest = pagename[len(prefix) :]
    parts = rest.split("/")
    if len(parts) < 2 or not parts[-1].startswith("plot_"):
        return None
    slug = parts[-1][len("plot_") :]
    rel_path = "/".join(parts[:-1])
    if rel_path.split("/")[-1] != slug:
        return None
    return rel_path, slug

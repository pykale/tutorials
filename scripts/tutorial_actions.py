"""Derive the per-tutorial action links (GitHub source, Notebook download, Run in Colab).

All URLs are derived from the tutorial's catalogue path -- never hard-coded per tutorial. Each tutorial
ships a self-contained, Colab-runnable ``tutorial.ipynb`` *in its own folder*; Colab and Notebook are
offered as working links for the tutorials that have one (``has_notebook``) and returned disabled with
an explanatory reason for those that do not yet, so the UI never shows a working-looking dead link.

``conf.py`` calls :func:`tutorial_actions` from an html-page-context hook for each gallery page and
puts the result in ``context["pky_tutorial"]``; ``source/_templates/tutorial-actions.html`` renders it.
"""

from __future__ import annotations

from typing import Dict, Optional, TypedDict

from site_meta import FEEDBACK_REPO, REPO_BRANCH

# The self-contained notebook each tutorial folder publishes, next to its narrative and example code.
NOTEBOOK_FILENAME = "tutorial.ipynb"


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


def notebook_path(rel_path: str) -> str:
    """Repo path of a tutorial's self-contained notebook, e.g. ``others/.../cifar_isonet/tutorial.ipynb``."""
    return f"{rel_path}/{NOTEBOOK_FILENAME}"


def notebook_url(rel_path: str, repo: str = FEEDBACK_REPO, branch: str = REPO_BRANCH) -> str:
    """GitHub blob URL of the tutorial's self-contained notebook."""
    return f"https://github.com/{repo}/blob/{branch}/{notebook_path(rel_path)}"


def colab_url(rel_path: str, repo: str = FEEDBACK_REPO, branch: str = REPO_BRANCH) -> str:
    """Google Colab URL that opens the tutorial's self-contained notebook straight from GitHub."""
    return f"https://colab.research.google.com/github/{repo}/blob/{branch}/{notebook_path(rel_path)}"


def tutorial_actions(
    rel_path: str,
    slug: str,
    *,
    draft: bool = False,
    has_notebook: bool = False,
) -> Dict[str, TutorialAction]:
    """Build the action set for one tutorial.

    Args:
        rel_path: Tutorial directory relative to the repo root (e.g. ``others/.../cifar_isonet``).
        slug: Tutorial slug.
        draft: Whether the narrative is still a draft (affects the disabled tooltip only).
        has_notebook: Whether this tutorial ships a ``tutorial.ipynb`` in its folder.

    Returns:
        dict: ``{action: {"url", "enabled", "reason"}}`` for ``github``, ``notebook`` and ``colab``.
        ``github`` is always enabled; Notebook and Colab are enabled for tutorials that have a
        ``tutorial.ipynb`` and otherwise carry a human-readable ``reason`` for the disabled state.
    """
    github: TutorialAction = {"url": github_source_url(rel_path, slug), "enabled": True, "reason": None}

    if has_notebook:
        notebook: TutorialAction = {"url": notebook_url(rel_path), "enabled": True, "reason": None}
        colab: TutorialAction = {"url": colab_url(rel_path), "enabled": True, "reason": None}
    else:
        reason = (
            "A runnable notebook is coming once this draft's narrative is written."
            if draft
            else "A runnable notebook is being prepared for this tutorial."
        )
        notebook = {"url": None, "enabled": False, "reason": reason}
        colab = {
            "url": None,
            "enabled": False,
            "reason": "Run in Colab will be available once this tutorial's notebook is published.",
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

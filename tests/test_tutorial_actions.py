"""Tests for tutorial action-link derivation and Colab availability rules."""

from __future__ import annotations

from tutorial_actions import gallery_pagename_to_tutorial, github_source_url, notebook_url, tutorial_actions

REL = "others/image_classification/cifar_isonet"
SLUG = "cifar_isonet"


def test_github_source_url_points_at_the_tutorial_script():
    url = github_source_url(REL, SLUG)
    assert url == "https://github.com/pykale/tutorials/blob/main/" + REL + "/plot_cifar_isonet.py"
    assert not url.rstrip("/").endswith("tutorials")  # never the repo homepage


def test_notebook_url_points_at_the_in_folder_notebook():
    assert notebook_url(REL).endswith("/" + REL + "/tutorial.ipynb")


def test_actions_github_always_enabled():
    actions = tutorial_actions(REL, SLUG, draft=True, has_notebook=False)
    assert actions["github"]["enabled"] is True
    assert actions["github"]["url"].startswith("https://github.com/")


def test_colab_and_notebook_disabled_without_a_notebook():
    actions = tutorial_actions(REL, SLUG, draft=False, has_notebook=False)
    assert actions["colab"]["enabled"] is False
    assert actions["colab"]["url"] is None
    assert actions["colab"]["reason"]  # a human-readable reason is present
    assert actions["notebook"]["enabled"] is False
    assert actions["notebook"]["reason"]


def test_draft_notebook_reason_mentions_draft():
    actions = tutorial_actions(REL, SLUG, draft=True, has_notebook=False)
    assert "draft" in actions["notebook"]["reason"].lower()


def test_actions_enabled_when_notebook_present():
    actions = tutorial_actions(REL, SLUG, draft=False, has_notebook=True)
    assert actions["colab"]["enabled"] is True
    assert "colab.research.google.com" in actions["colab"]["url"]
    assert actions["colab"]["url"].endswith("/" + REL + "/tutorial.ipynb")
    assert actions["notebook"]["enabled"] is True
    assert actions["notebook"]["url"].endswith("/" + REL + "/tutorial.ipynb")


def test_pagename_mapping():
    page = "_gallery/others/image_classification/cifar_isonet/plot_cifar_isonet"
    assert gallery_pagename_to_tutorial(page) == (REL, SLUG)


def test_pagename_mapping_rejects_non_tutorial_pages():
    assert gallery_pagename_to_tutorial("index") is None
    assert gallery_pagename_to_tutorial("_pages/others") is None
    assert gallery_pagename_to_tutorial("_gallery/others/cifar_isonet/index") is None

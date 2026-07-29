"""Tests for the data-driven left-sidebar context label."""

from __future__ import annotations

from models import REPO_ROOT, Catalog
from sidebar_context import sidebar_context

CAT = Catalog.load()


def test_domain_page_label_is_data_driven():
    visible, aria = sidebar_context(CAT, "_pages/others")
    assert visible == "Tutorials in Others · 10"  # label from catalogue, count from catalogue
    assert aria == "Tutorials in Others"


def test_protein_domain_page():
    visible, aria = sidebar_context(CAT, "_pages/protein")
    assert visible.startswith("Tutorials in Protein")
    assert aria == "Tutorials in Protein"


def test_tutorial_page_label():
    page = "_gallery/others/image_classification/cifar_isonet/plot_cifar_isonet"
    visible, aria = sidebar_context(CAT, page)
    assert visible == "More Others tutorials"
    assert aria == "More Others tutorials"


def test_non_domain_pages_have_no_context():
    assert sidebar_context(CAT, "index") is None
    assert sidebar_context(CAT, "about") is None


def test_template_has_no_hardcoded_domain():
    tpl = (REPO_ROOT / "_templates" / "sidebar-nav-bs.html").read_text(encoding="utf-8")
    assert "pky_sidebar_context" in tpl
    for domain in ("Others", "Protein", "Cancer", "Cardiac", "Materials"):
        assert domain not in tpl, f"{domain} is hard-coded in the shared template"

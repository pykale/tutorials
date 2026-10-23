"""Sphinx configuration for the PyKale tutorial gallery.

Everything tutorial-specific comes from ``tutorial_catalog.yml`` via
``source/_shared/gallery/sphinx_gallery_config.py``. Adding a tutorial should never require editing
this file.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
# Infrastructure (templates, static assets, shared build code, data) lives under source/; put it on
# the path so ``import _shared`` resolves. Build scripts stay in scripts/.
sys.path.insert(0, str(REPO_ROOT / "source"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from _shared.gallery.sphinx_gallery_config import build_gallery_conf  # noqa: E402
from models import Catalog  # noqa: E402

CATALOG = Catalog.load()

# -- Project information -----------------------------------------------------

project = "PyKale Tutorials"
copyright = f"2020 - {datetime.now():%Y}, PyKale Contributors"
author = "PyKale Contributors"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinx_sitemap",
    "sphinx_reredirects",
    "sphinxcontrib.mermaid",
    # sphinxext-opengraph: emits Open Graph / Twitter meta tags so tutorial links preview well when
    # shared -- a professional-polish item PyTorch's site has and ours lacked.
    "sphinxext.opengraph",
    # sphinx-favicon: declares multiple favicon sizes from one config block; more robust than the
    # theme's single html_favicon.
    "sphinx_favicon",
    # sphinx-notfound-page: a branded 404 that keeps the navbar/theme instead of a bare server page.
    "notfound.extension",
    # nbsphinx (for the upstream hand-written .ipynb) is intentionally NOT enabled yet: it needs
    # pandoc, and it collides with sphinx-gallery over the generated plot_*.ipynb download files.
    # Surfacing the upstream notebooks is a separate task, with pandoc in CI.
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
templates_path = ["source/_templates"]
exclude_patterns = [
    "_build",
    # NB: _gallery is sphinx-gallery's *generated source*, not build output -- it must stay included
    # or every gallery page is orphaned. It is gitignored, not Sphinx-excluded.
    "Thumbs.db",
    ".DS_Store",
    "README.md",  # the repo README; the gallery front page is index.rst
    "ROADMAP.md",  # contributor/dev doc, not part of the rendered site
    ".github/**",
    ".pytest_cache/**",
    "source/_shared/templates/**",
    "docs/**",  # contributor/dev notes, not part of the rendered gallery
    "_generated/**",  # include fragments for the homepage, not standalone pages
    "source/_data/**",
    # Upstream READMEs are provenance, not documentation -- they would otherwise be picked up as
    # standalone pages that duplicate each tutorial's own README.
    "**/README.upstream.md",
    "**/configs/README.md",
    # All .ipynb are either sphinx-gallery download artefacts (under _gallery) or upstream extras in
    # the excluded domain trees. Neither should be parsed as a page (and doing so would need pandoc).
    "**/*.ipynb",
    # Domain folders sit at the source root, so Sphinx would otherwise pick up every tutorial README
    # as a standalone page *and* sphinx-gallery would render it again inside _gallery. Excluding the
    # source trees leaves exactly one copy: the generated one. sphinx-gallery reads these files from
    # disk directly, so exclusion does not starve it.
    *[f"{bucket.id.value}/**" for bucket in CATALOG.buckets],
]

# nbsphinx would try to execute the four hand-written notebooks, which need datasets the doc builder
# does not have. They are rendered as committed.
nbsphinx_execute = "never"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "kale": ("https://pykale.readthedocs.io/en/latest/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "lightning": ("https://lightning.ai/docs/pytorch/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
}

# -- HTML output -------------------------------------------------------------

# pydata-sphinx-theme: the theme PyTorch's own is derived from -- top navbar, in-page TOC on the
# right, search, light/dark toggle. Org-neutral and pairs natively with sphinx-design cards.
html_theme = "pydata_sphinx_theme"
html_title = "PyKale Tutorials"
html_static_path = ["source/_static"]
html_css_files = ["custom.css"]
html_js_files = ["js/catalog.js", "js/feedback.js", "js/search.js"]
# source/_static/pykale_logo.png is gitignored and sourced from source/_shared/assets/logos. Copy it
# now, at config import, so it exists before Sphinx validates html_logo -- a bare checkout (as CI
# runs) otherwise warns that the logo is missing, which is fatal under -W. Runs before builder-inited,
# where the logo check has already fired.
import shutil as _shutil  # noqa: E402

_shutil.copyfile(
    REPO_ROOT / "source" / "_shared" / "assets" / "logos" / "pykale_logo.png",
    REPO_ROOT / "source" / "_static" / "pykale_logo.png",
)

html_logo = "source/_static/pykale_logo.png"
# favicon handled by sphinx-favicon (see `favicons` below), not html_favicon.

from sidebar_context import sidebar_context  # noqa: E402
from site_meta import (  # noqa: E402
    ECOSYSTEM_LINKS,
    FEEDBACK_REPO,
    GOOGLE_SEARCH_ENGINE_ID,
    SITE_DOMAIN,
    pykale_release,
    pypi_url,
    version_url,
)
from tutorial_actions import gallery_pagename_to_tutorial, tutorial_actions  # noqa: E402

PYKALE_VERSION = pykale_release()

html_theme_options = {
    # Navbar order: logo, version chip, then the dropdown nav (left). Go-to-PyKale + utility icons
    # sit on the right. navbar-nav / navbar-version / navbar-goto are custom templates in
    # source/_templates/.
    "navbar_start": ["navbar-logo", "navbar-version"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-goto", "theme-switcher", "navbar-icon-links"],
    # Desktop: a real, directly-typeable search-field (Ctrl+K focuses it, Enter runs local search).
    # Mobile: the theme's search-button (icon -> dialog). CSS shows exactly one per width.
    "navbar_persistent": ["search-field", "search-button"],
    "search_bar_text": "Search PyKale Tutorials",
    # Tutorial action toolbar renders at the top of the article on tutorial pages only.
    "article_header_end": ["tutorial-actions"],
    "navbar_align": "left",
    "show_nav_level": 1,
    "navigation_depth": 3,
    "collapse_navigation": False,
    "show_toc_level": 2,
    "icon_links": [
        {
            "name": "PyKale on GitHub",
            "url": "https://github.com/pykale/pykale",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyKale on PyPI",
            "url": pypi_url(),
            "icon": "_static/pypi.svg",
            "type": "local",
        },
        {
            "name": "PyKale API documentation",
            "url": "https://pykale.readthedocs.io",
            "icon": "fa-solid fa-book",
        },
    ],
    "use_edit_page_button": False,
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
    "footer_start": ["footer-links"],
    "footer_end": [],
    # Right (secondary) sidebar. pydata uses the LAST matching pattern, so the catch-all "**" comes
    # first and the exact "index" override last (otherwise "**" would win for the homepage too).
    "secondary_sidebar_items": {
        "**": ["page-toc", "pky-feedback"],
        "index": ["pky-onthispage", "pky-ecosystem", "pky-feedback"],
    },
}

html_context = {
    "default_mode": "light",
    "pykale_version": PYKALE_VERSION,
    "pykale_version_url": version_url(PYKALE_VERSION),
    "pypi_url": pypi_url(),
    "feedback_repo": FEEDBACK_REPO,
    "google_site_domain": SITE_DOMAIN,
    "google_search_engine_id": GOOGLE_SEARCH_ENGINE_ID,
}

# The homepage and the standalone catalogue drop the *left* sidebar (they are landing pages, not
# docs). The homepage keeps a curated *right* sidebar (secondary_sidebar_items above).
_LANDING_PAGES = {"index", "pages/all-tutorials"}
html_sidebars = {page: [] for page in _LANDING_PAGES}


def _nav_context(app, pagename, templatename, context, doctree):
    """Inject catalogue-derived navigation data and a landing body class.

    Keeps the navbar/footer/sidebar templates data-driven from ``tutorial_catalog.yml`` and
    ``site_meta`` so adding a domain or ecosystem entry needs no template edit.
    """
    context["pky_nav"] = {
        "domains": [
            {
                "label": bucket.label,
                "color": bucket.color,
                "docname": f"_pages/{bucket.id.value}",
                "coming_soon": bucket.status.value == "coming_soon",
            }
            for bucket in CATALOG.buckets
        ],
        "ecosystem": ECOSYSTEM_LINKS,
        "year": datetime.now().year,
    }
    if pagename in _LANDING_PAGES:
        context["body_class"] = "pky-landing"

    # Tutorial pages: derive the action-toolbar links from the catalogue path.
    mapped = gallery_pagename_to_tutorial(pagename)
    if mapped:
        rel_path, slug = mapped
        draft = _DRAFT_BY_SLUG.get(slug, False)
        context["pky_tutorial"] = tutorial_actions(rel_path, slug, draft=draft)
        context["pky_tutorial_draft"] = draft

    # Left-sidebar context label ("Tutorials in General" / "More General tutorials"), data-driven.
    ctx = sidebar_context(CATALOG, pagename)
    if ctx:
        context["pky_sidebar_context"], context["pky_sidebar_nav_label"] = ctx


def _draft_by_slug():
    import yaml as _yaml
    from models import TutorialMetadata

    out = {}
    for path in CATALOG.iter_relative_paths():
        meta = TutorialMetadata.model_validate(
            _yaml.safe_load((REPO_ROOT / path / "metadata.yml").read_text(encoding="utf-8"))
        )
        out[meta.slug] = meta.draft
    return out


_DRAFT_BY_SLUG = _draft_by_slug()


def _ensure_static_catalog(app):
    """Write _static/tutorials.json before the build so the faceted filter always has data.

    The filter fetches this file; if a build runs without the separate export step it would be
    missing and the catalogue would silently fail to populate. Generating it here makes the filter
    work on any ``sphinx-build`` invocation.
    """
    import json

    from export_landing_page import build_payload

    out = REPO_ROOT / "source" / "_static" / "tutorials.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_payload(), indent=2) + "\n", encoding="utf-8")


def setup(app):
    app.connect("html-page-context", _nav_context)
    app.connect("builder-inited", _ensure_static_catalog)


# -- Plugin configuration ----------------------------------------------------

# Base URL of the published site. Required by sphinx-sitemap and opengraph; the exact host is
# settled in Phase 2 (GitHub Pages vs ReadTheDocs). Update this when that decision is made.
html_baseurl = "https://pykale.github.io/tutorials/"
sitemap_url_scheme = "{link}"

# sphinxext-opengraph
ogp_site_url = html_baseurl
ogp_site_name = "PyKale Tutorials"
ogp_description_length = 200

# sphinx-favicon: reuse the PyKale mark (served from _static).
favicons = [
    {"href": "pykale_logo.png"},
]

# sphinx-notfound-page: absolute URLs on the 404 so links work from any depth.
notfound_urls_prefix = "/tutorials/"

# sphinx-reredirects: old-path -> new-path map for URLs that move, so existing links do not 404.
# Content pages moved from the site root into pages/; keep their old URLs alive.
redirects: dict[str, str] = {
    "all-tutorials": "pages/all-tutorials.html",
    "getting-started": "pages/getting-started.html",
    "learning-paths": "pages/learning-paths.html",
    "tutorial-status": "pages/tutorial-status.html",
    "about": "pages/about.html",
}

# Mermaid diagrams render client-side; no local binary needed for the HTML build.
mermaid_version = "11.4.1"

# -- sphinx-gallery ----------------------------------------------------------

sphinx_gallery_conf = build_gallery_conf()

# `make html-noplot` sets TUTORIALS_NOPLOT=1. Setting the bool here (rather than -D plot_gallery=0 on
# the command line, which Sphinx coerces to the string "0" and warns about under -W) keeps the strict
# build clean.
if os.environ.get("TUTORIALS_NOPLOT") == "1":
    sphinx_gallery_conf["plot_gallery"] = False

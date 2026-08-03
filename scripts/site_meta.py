"""Site-level metadata derived at build time, kept out of templates so it is testable.

Two things live here: the PyKale release to show in the navbar (never hard-coded), and the GitHub
repository the feedback links target. Both are exposed to templates through ``html_context`` in
``conf.py``.
"""

from __future__ import annotations

# The tutorials repository, used to build "Send feedback" GitHub-issue links and tutorial source
# links. No git remote exists for a local-only checkout, so this is the single place to set it.
FEEDBACK_REPO = "pykale/tutorials"
REPO_BRANCH = "main"

# Whether sphinx-gallery's generated notebooks are published to a public branch/site. Until the
# deployment does this (see ROADMAP Phase 2), the Colab and Notebook actions are shown DISABLED with
# a tooltip rather than as working-looking dead links. Flip to True once publishing is wired up.
NOTEBOOKS_PUBLISHED = False

# Published site host, for the optional "Search this site with Google" fallback. Not repeated in JS.
SITE_DOMAIN = "pykale.github.io/tutorials"

# Optional Google Programmable Search Engine id. Absent by default: the site falls back to a Google
# `site:` query and keeps local Sphinx search working. Never hard-code a private id here.
GOOGLE_SEARCH_ENGINE_ID = None

# Curated ecosystem links, shown in the homepage sidebar and the navbar Ecosystem dropdown.
ECOSYSTEM_LINKS = [
    {"name": "OMAIB", "url": "https://omaib.github.io", "external": True},
    {"name": "UKOMAIN", "url": "https://multimodalai.github.io", "external": True},
    {"name": "PyKale", "url": "https://pykale.github.io/", "external": True},
]


def pykale_release() -> str:
    """Return the PyKale version to display, or ``"dev"`` for an uninstalled checkout.

    Resolution order: an explicit ``PYKALE_VERSION`` environment override (set by CI to the current
    PyPI release, so the published site shows e.g. ``v0.2.0`` rather than ``dev``), then the imported
    package's ``__version__``, then installed distribution metadata, then ``"dev"``. No network access
    here -- CI resolves the PyPI version and passes it in via the env var.

    Returns:
        str: e.g. ``"0.2.0"`` or ``"dev"``.
    """
    import os

    override = os.environ.get("PYKALE_VERSION", "").strip()
    if override:
        return override
    try:
        import kale

        if getattr(kale, "__version__", None):
            return str(kale.__version__)
    except Exception:
        pass
    try:
        from importlib.metadata import version

        return version("pykale")
    except Exception:
        return "dev"


def pypi_url() -> str:
    """PyPI project page for PyKale."""
    return "https://pypi.org/project/pykale/"


def version_url(release: str) -> str:
    """Where the navbar version chip links.

    Args:
        release: The resolved version string.

    Returns:
        str: The PyPI project page for a real release; the PyKale repo for a ``dev`` checkout.
    """
    if release == "dev":
        return "https://github.com/pykale/pykale"
    return pypi_url()

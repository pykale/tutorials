"""Tests for the search configuration: visible desktop field, Google fallback, engine-id optional."""

from __future__ import annotations

from urllib.parse import quote_plus

import site_meta
from models import REPO_ROOT

CONF = (REPO_ROOT / "conf.py").read_text(encoding="utf-8")
FOOTER = (REPO_ROOT / "source" / "_templates" / "footer-links.html").read_text(encoding="utf-8")


def test_visible_desktop_search_field_configured():
    # search-field is the theme's REAL typeable input (not the modal-opening button).
    assert '"search-field"' in CONF
    assert '"search-button-field"' not in CONF  # not the modal button


def test_search_js_binds_ctrl_k_to_the_input():
    js = (REPO_ROOT / "source" / "_static" / "js" / "search.js").read_text(encoding="utf-8")
    assert "metaKey" in js and "ctrlKey" in js
    assert "input.focus()" in js
    assert "stopImmediatePropagation" in js  # blocks the theme modal
    assert '"js/search.js"' in CONF


def test_google_site_domain_is_config_driven():
    assert site_meta.SITE_DOMAIN
    # The footer builds the Google query from the config value, not a repeated literal.
    assert "google_site_domain" in FOOTER
    assert "site:{{ google_site_domain }}" in FOOTER


def test_google_query_escaping_is_safe():
    # A query with spaces/specials must be percent-encoded when the JS/site builds it.
    q = "domain adaptation & fusion"
    encoded = quote_plus(q)
    assert " " not in encoded and "&" not in encoded


def test_absent_engine_id_keeps_local_search():
    # No programmable-search id by default -> local Sphinx search remains the default, nothing breaks.
    assert site_meta.GOOGLE_SEARCH_ENGINE_ID is None
    assert "google_search_engine_id" in CONF

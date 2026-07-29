"""Tests for build-time site metadata: version resolution and feedback repo."""

from __future__ import annotations

import re

import site_meta
from site_meta import FEEDBACK_REPO, pykale_release, pypi_url, version_url


def test_release_is_a_string():
    rel = pykale_release()
    assert isinstance(rel, str) and rel
    # Either a dotted version or the dev sentinel.
    assert rel == "dev" or re.match(r"^\d+\.\d+", rel), rel


def test_version_fallback_to_dev(monkeypatch):
    """With neither kale nor the installed distribution available, resolve to 'dev'."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "kale" or name.startswith("importlib.metadata") or name == "importlib":
            raise ImportError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert pykale_release() == "dev"


def test_version_url_branches():
    # A real release links to PyPI; a dev checkout links to the repo.
    assert version_url("0.2.0") == pypi_url()
    assert "pypi.org" in version_url("1.2.3")
    assert version_url("dev") == "https://github.com/pykale/pykale"


def test_feedback_repo_is_owner_slash_name():
    assert re.match(r"^[\w.-]+/[\w.-]+$", FEEDBACK_REPO), FEEDBACK_REPO
    assert FEEDBACK_REPO.startswith("pykale/")


def test_ecosystem_links_present():
    names = {e["name"] for e in site_meta.ECOSYSTEM_LINKS}
    assert {"OMAIB", "UKOMAIN"} <= names
    for e in site_meta.ECOSYSTEM_LINKS:
        assert e["url"].startswith("https://"), e

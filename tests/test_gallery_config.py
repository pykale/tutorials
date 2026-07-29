"""Tests for the sphinx-gallery configuration.

The ``filename_pattern`` (what executes) and ``ignore_pattern`` (what is not an example at all) are
regexes that already broke the build twice: once treating ``main.py``/``config.py`` as gallery
examples, once colliding on duplicate ``tutorial.py`` names. These tests pin the regex behaviour
directly, so a future edit that reintroduces either failure is caught here instead of in a Sphinx
build log.
"""

from __future__ import annotations

import re

import pytest
from gallery.sphinx_gallery_config import _executable_slugs, build_gallery_conf
from models import Catalog


@pytest.fixture(scope="module")
def conf():
    return build_gallery_conf()


def test_supporting_files_are_ignored(conf):
    """main.py / config.py / model.py / test.py must never be treated as gallery examples."""
    ignore = re.compile(conf["ignore_pattern"])
    for name in ["main.py", "config.py", "model.py", "test.py", "configs.py", "interpret.py"]:
        path = f"others/image_classification/cifar_isonet/{name}"
        assert ignore.search(path), f"{name} should be ignored but is not"


def test_narrative_is_not_ignored(conf):
    ignore = re.compile(conf["ignore_pattern"])
    path = "others/image_classification/cifar_isonet/plot_cifar_isonet.py"
    assert not ignore.search(path), "the plot_ narrative must not be ignored"


def test_only_runnable_narratives_execute(conf):
    """filename_pattern must match written, non-GPU tutorials and nothing else."""
    pattern = re.compile(conf["filename_pattern"])
    runnable = set(_executable_slugs(Catalog.load()))

    # The one written CPU/GPU-optional tutorial executes.
    assert "digit_domain_adaptation" in runnable
    assert pattern.search("x/others/image_classification/digit_domain_adaptation/plot_digit_domain_adaptation.py")

    # A GPU-required tutorial (action_recognition) must never be scheduled for execution in CI.
    assert "action_recognition" not in runnable
    assert not pattern.search("x/others/action_recognition/plot_action_recognition.py")


def test_supporting_file_never_executes(conf):
    """Even a runnable tutorial's main.py must not match the execution pattern."""
    pattern = re.compile(conf["filename_pattern"])
    assert not pattern.search("x/others/image_classification/digit_domain_adaptation/main.py")


def test_examples_and_gallery_dirs_align(conf):
    """Each source dir maps to exactly one output dir, in the same order."""
    assert len(conf["examples_dirs"]) == len(conf["gallery_dirs"])
    assert len(conf["examples_dirs"]) == len(Catalog.load().iter_relative_paths())
    for target in conf["gallery_dirs"]:
        assert target.startswith("_gallery/")


def test_executable_slugs_excludes_drafts():
    """A draft tutorial is rendered but must not be executed."""
    catalog = Catalog.load()
    runnable = set(_executable_slugs(catalog))
    # cifar_isonet is a draft stub; it must not run during the build.
    assert "cifar_isonet" not in runnable


def test_gallery_filter_and_list_runnable_agree():
    """The build's execution set and the CI installer's set are one definition, not two.

    A regression where these drift would make CI install deps for tutorials the build never runs, or
    (worse) run a tutorial whose deps were never installed.
    """
    from list_runnable import runnable_paths

    from_gallery = set(_executable_slugs(Catalog.load()))
    from_cli = {p.split("/")[-1] for p in runnable_paths()}
    assert from_gallery == from_cli

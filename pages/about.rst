About the tutorial project
==========================

PyKale Tutorials is the runnable-tutorial companion to `PyKale
<https://github.com/pykale/pykale>`_, a library for multimodal learning and transfer learning on
interdisciplinary data.

What this is
------------

Each tutorial is a self-contained folder: a narrated ``plot_<slug>.py`` that reads top to bottom and
builds into a notebook, plus the full ``main.py`` experiment it is drawn from. Tutorials are
organised by the domain that owns them — Others, Protein, Cancer, Cardiac and Materials — and every
tutorial carries structured metadata (task, modality, difficulty, runtime, status) that drives the
filters, learning paths and status page.

How it is built
---------------

The site is a `Sphinx <https://www.sphinx-doc.org>`_ project using
`Sphinx-Gallery <https://sphinx-gallery.github.io>`_ to turn tutorial scripts into pages, notebooks
and downloads, themed with the `PyData Sphinx Theme <https://pydata-sphinx-theme.readthedocs.io>`_.
The catalogue in ``tutorial_catalog.yml`` is the single source of truth; domain pages, the homepage
sections, thumbnails and the filterable catalogue are all generated from it.

See :doc:`/CONTRIBUTING` to add or improve a tutorial, and the `roadmap
<https://github.com/pykale/tutorials/blob/main/ROADMAP.md>`_ for what is planned.

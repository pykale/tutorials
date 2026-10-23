.PHONY: help install validate schema export pages thumbnails homepage generate lint test html html-noplot linkcheck clean

SPHINXOPTS ?= -W --keep-going
BUILDDIR   ?= _build
PYTHON     ?= python

help:
	@echo "install      install docs + dev dependencies"
	@echo "validate     check catalog, metadata, schema and thumbnails agree (run before pushing)"
	@echo "schema       regenerate source/_shared/metadata/tutorial.schema.json"
	@echo "export       regenerate the landing-page + source/_static tutorials.json"
	@echo "pages        regenerate the per-domain pages"
	@echo "thumbnails   regenerate the placeholder SVG thumbnails"
	@echo "homepage     regenerate the homepage/list-page partials"
	@echo "generate     run every generator (thumbnails, homepage, pages, export)"
	@echo "lint         run pre-commit on all files"
	@echo "test         run the script unit tests"
	@echo "html         full build, executing runnable tutorials"
	@echo "html-noplot  fast build with no tutorial execution (what CI runs on PRs)"
	@echo "linkcheck    verify external links resolve"
	@echo "clean        remove build artefacts"

install:
	$(PYTHON) -m pip install -e ".[docs,dev]"

validate:
	$(PYTHON) scripts/generate_schema.py --check
	$(PYTHON) scripts/validate_catalog.py
	$(PYTHON) scripts/generate_thumbnails.py --check

schema:
	$(PYTHON) scripts/generate_schema.py

export:
	$(PYTHON) scripts/export_landing_page.py

pages:
	$(PYTHON) scripts/generate_bucket_pages.py

thumbnails:
	$(PYTHON) scripts/generate_thumbnails.py

homepage:
	$(PYTHON) scripts/generate_homepage.py

# Everything the Sphinx build reads from disk. Order-independent, but grouped for one command.
generate: thumbnails homepage pages export

lint:
	pre-commit run --all-files

test:
	$(PYTHON) -m pytest

html: generate
	$(PYTHON) -m sphinx -b html $(SPHINXOPTS) . $(BUILDDIR)/html

html-noplot: generate
	TUTORIALS_NOPLOT=1 $(PYTHON) -m sphinx -b html $(SPHINXOPTS) . $(BUILDDIR)/html

linkcheck:
	$(PYTHON) -m sphinx -b linkcheck . $(BUILDDIR)/linkcheck

clean:
	rm -rf $(BUILDDIR) _gallery _pages _generated sg_execution_times.rst
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

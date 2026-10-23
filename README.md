# PyKale Tutorials

[![Docs build](https://github.com/pykale/tutorials/actions/workflows/docs.yml/badge.svg)](https://github.com/pykale/tutorials/actions/workflows/docs.yml)
[![Live site](https://img.shields.io/website?url=https%3A%2F%2Fpykale.github.io%2Ftutorials%2F&label=tutorials%20site&up_message=online)](https://pykale.github.io/tutorials/)
[![PyKale on PyPI](https://img.shields.io/pypi/v/pykale?label=pykale)](https://pypi.org/project/pykale/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Runnable tutorials for [PyKale](https://github.com/pykale/pykale), published at **[pykale.github.io/tutorials](https://pykale.github.io/tutorials/)** as a [sphinx-gallery](https://sphinx-gallery.github.io/) site.

Each tutorial is a self-contained folder holding two things: a narrated `plot_<slug>.py` that runs in minutes and explains the method, and the full `main.py` experiment it was drawn from. Read the first, run the second when you want real numbers.

## Layout

Tutorials are filed under the domain that owns them. The folder path fixes the domain and the task; everything else a reader might filter on — modality, method, fusion, dataset, difficulty — lives in each tutorial's `metadata.yml`.

```
others/      # domain-agnostic method demos; start here
└── image_classification/
protein/     # molecular therapeutics
cancer/      # multiomics cancer classification
cardiac/     # cardiac imaging and uncertainty
materials/   # reserved, no tutorial yet
```

Domain folders sit at the repository root.

Supporting directories:

| Path | What it holds |
|---|---|
| `source/` | Build infrastructure, kept out of the root: Sphinx `_static` assets, `_templates`, shared gallery/launch code and metadata schema (`_shared`), and the news `_data` |
| `pages/` | Standalone content pages: getting started, all tutorials, learning paths, tutorial status, and about. `index.rst` remains at the root as Sphinx's entry page. |
| `scripts/` | Migration, validation, schema generation, landing-page export |
| `tutorial_catalog.yml` | Source of truth: which tutorials exist and in what order |

## Running a tutorial

```bash
cd others/image_classification/digit_domain_adaptation
pip install pykale
pip install -r requirements.txt
python main.py --cfg configs/MN2UP-DANN.yaml --devices 1
```

Every tutorial's README states its datasets, hardware needs and expected runtime. Datasets are never committed here — they download on demand or come from [pykale/data](https://github.com/pykale/data).

## Building the site

Install the site dependencies and validate the catalogue:

```bash
pip install -e ".[docs,dev]"

# validate: catalog, metadata and schema agree
python scripts/generate_schema.py --check
python scripts/validate_catalog.py

```

For a build without tutorial execution, use the platform shortcut. Both run the thumbnail,
homepage, and domain-page generators before Sphinx:

- **Linux/macOS/CI:** `make validate`, `make html-noplot`, `make html` (needs GNU `make`).
- **Windows:** `.\make.bat validate`, `.\make.bat html-noplot`, `.\make.bat html` (PowerShell/cmd).
  From Git Bash, call it as `cmd //c ".\make.bat html-noplot"`.

To run the equivalent commands directly, generate the source files first:

```bash
python scripts/generate_thumbnails.py
python scripts/generate_homepage.py
python scripts/generate_bucket_pages.py
```

Then run `TUTORIALS_NOPLOT=1 python -m sphinx -b html -W --keep-going . _build/html`
in bash, or set `$env:TUTORIALS_NOPLOT='1'` before the Sphinx command in PowerShell.
For a full build that executes eligible `plot_<slug>.py` narratives, unset that variable and run
the same Sphinx command after installing PyKale and each runnable tutorial's requirements.

Open `_build/html/index.html` when the build finishes.

## How tutorials are tested

Three layers, cheapest first — mirroring how PyTorch's tutorials CI works, minus the GPU fleet:

1. **`validate` + unit tests** (every PR) — catalog/metadata/schema agree; the gallery filter, migration and generators are unit-tested. Fast, no runtime deps.
2. **`html-noplot`** (every PR) — renders every tutorial from source but executes none. Catches structural and parse errors without running anything.
3. **Manually triggered executing build** (`nightly-exec` job) — runs the CPU-runnable, non-draft tutorials with their real dependencies, catching runtime breakage (a wrong `kale` call, a shape mismatch) that the parse-only layers miss. Its nightly schedule is currently disabled. GPU-required tutorials are rendered but never executed. The set that runs is defined once (`TutorialMetadata.is_runnable`) and shared by the build filter and `scripts/list_runnable.py`.

## Status

All 16 tutorials are migrated. Most `plot_<slug>.py` narratives are still stubs, marked `draft: true` in their metadata and badged in the gallery — the underlying example is complete either way. Writing those narratives is the current work. Notebook launch actions remain disabled until generated notebooks are published.

## Relationship to the main library

These tutorials were migrated from `examples/` in the [pykale](https://github.com/pykale/pykale) repository; each tutorial's `metadata.yml` records the folder it came from. The library itself is documented at [pykale.readthedocs.io](https://pykale.readthedocs.io).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New tutorials start from the templates in `source/_shared/templates/`.

## License

MIT — see [LICENSE](LICENSE).

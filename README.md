# PyKale Tutorials

Runnable tutorials for [PyKale](https://github.com/pykale/pykale), published as a [sphinx-gallery](https://sphinx-gallery.github.io/) site.

Each tutorial is a self-contained folder holding two things: a narrated `tutorial.py` that runs in minutes and explains the method, and the full `main.py` experiment it was drawn from. Read the first, run the second when you want real numbers.

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
| `_shared/` | Gallery config, metadata schema, contribution templates, launch-badge builders, assets |
| `scripts/` | Migration, validation, schema generation, landing-page export |
| `tutorial_catalog.yml` | Source of truth: which tutorials exist and in what order |

## Running a tutorial

```bash
pip install -r requirements.txt
cd others/image_classification/digit_domain_adaptation
python main.py --cfg configs/MN2UP-DANN.yaml --devices 1
```

Every tutorial's README states its datasets, hardware needs and expected runtime. Datasets are never committed here — they download on demand or come from [pykale/data](https://github.com/pykale/data).

## Building the site

The tasks are available three ways. The **direct Python commands work everywhere** — use these if in doubt (Windows has no `make` by default):

```bash
pip install -e ".[docs,dev]"

# validate: catalog, metadata and schema agree
python scripts/generate_schema.py --check
python scripts/validate_catalog.py

# fast build, no tutorial execution (what CI runs on PRs)
python scripts/generate_bucket_pages.py
python -m sphinx -b html -W --keep-going . _build/html      # (bash: prefix TUTORIALS_NOPLOT=1)

# full build, executes every runnable tutorial.py
python scripts/generate_bucket_pages.py
python -m sphinx -b html -W --keep-going . _build/html
```

Shortcuts wrapping exactly those commands:

- **Linux/macOS/CI:** `make validate`, `make html-noplot`, `make html` (needs GNU `make`).
- **Windows:** `.\make.bat validate`, `.\make.bat html-noplot`, `.\make.bat html` (PowerShell/cmd).
  From Git Bash, call it as `cmd //c ".\make.bat validate"`, or just run the Python commands above.

Open `_build/html/index.html` when the build finishes.

## How tutorials are tested

Three layers, cheapest first — mirroring how PyTorch's tutorials CI works, minus the GPU fleet:

1. **`validate` + unit tests** (every PR) — catalog/metadata/schema agree; the gallery filter, migration and generators are unit-tested. Fast, no runtime deps.
2. **`html-noplot`** (every PR) — renders every tutorial from source but executes none. Catches structural and parse errors without running anything.
3. **Nightly executing build** (`nightly-exec` job) — actually *runs* the CPU-runnable, non-draft tutorials with their real dependencies, catching runtime breakage (a wrong `kale` call, a shape mismatch) that the parse-only layers miss. GPU-required tutorials are rendered but never executed, matching PyTorch's curated do-not-run list. The set that runs is defined once (`TutorialMetadata.is_runnable`) and shared by the build filter and `scripts/list_runnable.py`.

## Status

All 16 tutorials are migrated and runnable. Most `tutorial.py` narratives are still stubs, marked `draft: true` in their metadata and badged in the gallery — the underlying example is complete either way. Writing those narratives is the current work.

## Relationship to the main library

These tutorials were migrated from `examples/` in the [pykale](https://github.com/pykale/pykale) repository; each tutorial's `metadata.yml` records the folder it came from. The library itself is documented at [pykale.readthedocs.io](https://pykale.readthedocs.io).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New tutorials start from the templates in `_shared/templates/`.

## License

MIT — see [LICENSE](LICENSE).

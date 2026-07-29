# What we take from PyTorch Tutorials

The PyTorch tutorials site (docs.pytorch.org/tutorials) is the reference standard for a Python-library
tutorial gallery. This repo follows its architectural and UX choices where they fit, while staying
recognisably PyKale. This note records the alignment so it is a decision on the record.

## 1. What we draw from PyTorch Tutorials

| Area | PyTorch | Here |
|---|---|---|
| Site generator | Sphinx | Sphinx |
| Executable-tutorial model | sphinx-gallery, one script per tutorial | sphinx-gallery, `plot_<slug>.py` |
| Unique file naming | `quickstart_tutorial.py` | `plot_<slug>.py` |
| Execution control by filename | `plot_` prefix + `filename_pattern` | same, filter from `metadata.is_runnable` |
| Theme lineage | `pytorch_sphinx_theme2` (derived from pydata) | `pydata-sphinx-theme` (the parent theme) |
| Curated top-level navigation | Intro / Domains / … dropdowns | Learn / Domains / Ecosystem / More dropdowns |
| Downloadable notebooks + source | `.ipynb` + `.zip` per tutorial | same (sphinx-gallery default) |
| Category-driven discovery | tag-chip filter bar | faceted catalogue over `tutorials.json` |
| Tutorial cards + thumbnails | image cards | metadata-rich cards + generated SVG thumbnails |
| Code/API cross-linking | intersphinx | intersphinx to kale/torch/lightning/sklearn |
| Search + dark mode | yes | yes (pydata) |
| Content/tooling separation | tutorials vs build scripts | catalogue + generators vs curated shells |
| Tutorials executed in CI | sharded across GPU runners | nightly job runs the CPU-runnable set |
| Curated do-not-run list | explicit + `expected_failing_examples` | GPU-required and drafts rendered, never executed |

## 2. What stays deliberately PyKale-specific

- **PyKale green branding** and design tokens (`--pykale-green-*`), not PyTorch's palette.
- **Domain-based information architecture** — General, Protein, Cancer, Cardiac, Materials — each an
  owner with its own page, colour and hero tile. PyTorch organises by topic tag, not domain.
- **"General", never "Others"** as the label for the domain-agnostic bucket.
- **Richer metadata** — modality, task, fusion, difficulty, runtime, status — driving filters,
  learning paths and the status page, where PyTorch exposes flat tags.
- **UKOMAIN / OMAIB ecosystem** links and a domain-package roadmap (kale-protein, …).
- **Smaller, maintainable CI** — no GPU build fleet; a single nightly CPU execution job.
- **No PyTorch branded theme** and **no copy** of PyTorch's colours, wording or layout.

## 3. Where PyKale aims to go beyond PyTorch

- **Faceted filtering** (domain × task × modality × difficulty × runtime × status) with URL sync and
  deep-linking, versus a single tag bar.
- **Explicit runtime and difficulty** on every card and in the filters.
- **Clear draft states** — drafts are rendered but visibly badged, and listed on a status page, so
  the catalogue is honest about what is finished.
- **Metadata-driven learning paths** curated in the catalogue, not hand-maintained HTML.
- **Domain ownership** as a first-class concept, with an ecosystem map relating tutorials to the
  wider PyKale project.

## Remaining design steps

1. **Real thumbnails** supersede the SVG placeholders automatically as narratives are written and
   produce figures (`resolve_thumbnail`); until then every card carries a branded, per-domain tile.
2. **Domain-page task chips** — group tutorials by task within a domain page.
3. **Tutorial-page polish** — prev/next, related tutorials and a "what you will learn" block are
   partially provided by the theme/gallery and can be extended.

# Contributing

## Setup

```bash
pip install -e ".[docs,dev]"
pre-commit install
```

## Adding a tutorial

1. **Pick the folder.** The path fixes the domain and the task, so this decision is the important one. Domain buckets are `others`, `protein`, `cancer`, `cardiac`, `materials`. Use `others` when the tutorial demonstrates a method rather than an application. If the tutorial is one of a related set, nest it in a group folder as `others/image_classification/` does.

2. **Copy the templates.** For example, to add `others/my_tutorial`:

   ```bash
   mkdir -p others/my_tutorial
   cp source/_shared/templates/metadata.template.yml others/my_tutorial/metadata.yml
   cp source/_shared/templates/README.template.md    others/my_tutorial/README.md
   cp source/_shared/templates/plot.py.template      others/my_tutorial/plot_my_tutorial.py
   ```

3. **Register it** in `tutorial_catalog.yml` under the right bucket, and in the group's `tutorials:` list if it belongs to one. Order within a list is the order it appears in the gallery, so put the gentlest introduction first.

4. **Fill in `metadata.yml`.** Every field is validated. Derive `kale_api` from the imports the code actually makes, not from prose — upstream READMEs have drifted from their code more than once.

5. **Write `plot_<slug>.py`** (replace `<slug>` with the folder name). See the conventions below.

6. **Check it.**

   ```bash
   make validate
   make html-noplot
   ```

## Conventions for `plot_<slug>.py`

Sphinx-gallery turns this file into an HTML page, a notebook and a downloadable script. It is the only file in the folder that the doc build executes.

- **Explain the method, not the API.** If a reader could get the same thing from the docstring, the section is not earning its place. Say why the method suits the problem and what would go wrong without it.
- **Keep it under two minutes on CPU.** Reduce epochs, subsample the data, shrink the model — and then *say so in the text*, with the full command alongside. Silently reporting numbers from a reduced run is how a tutorial becomes misinformation.
- **Make the first plot the best one.** It becomes the gallery thumbnail.
- **Show the mechanism, not just the score.** A metric says whether it worked; a plot of what the model learned says why.
- **Set the seed** with `kale.utils.seed.set_seed`, which covers cuDNN as well as Python, NumPy and torch.
- Sections are `# %%` blocks with an rST heading. The authored `plot_<slug>.py` narrative is linted and formatted; migrated example code is deliberately left byte-identical to upstream.

## Migrated examples

Files copied from `pykale/examples` are kept unmodified so that upstream fixes can be re-synced:

```bash
python scripts/migrate_examples.py --pykale-root ../pykale --dry-run
```

The sync never overwrites `plot_<slug>.py`, `metadata.yml`, `README.md` or `requirements.txt`. Where a copied file genuinely must change — an import that assumed the `examples` package, for instance — record it in `POST_MIGRATION_PATCHES` in `scripts/migrate_examples.py` rather than editing the file directly, so a re-sync cannot quietly undo it.

## Data

Never commit datasets. They belong in [pykale/data](https://github.com/pykale/data) or download on demand. `check-added-large-files` rejects anything over 300 KB.

## Pull requests

Follow the [pykale contribution guide](https://github.com/pykale/pykale/blob/main/.github/CONTRIBUTING.md). Open PRs as drafts, keep them to one tutorial where possible, and make sure `make validate` and `make html-noplot` pass before marking one ready.

## Versioning and release

There is no per-version tutorial archive and no version switcher. `main` is the single source of truth and is what the published site serves.

- **`main` is published.** Every merge to `main` is a candidate for the live site; CI builds and deploys from it. Older tutorial states live in git history, not as browsable versions.
- **Tutorials track the PyKale release.** The gallery is expected to run against the current stable PyKale, so tutorials are brought in line with a release around release day rather than versioned independently.
- **Validate against a release with a throwaway RC branch.** To test tutorials against a release candidate, cut a short-lived branch named `<version>-rc` (for example `0.2.0-rc`), fix what the candidate breaks, and merge back. These branches are for validation only — delete them after the release; they are not archived versions.

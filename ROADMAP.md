# Roadmap

**Phase 1 — scaffold and migrate. _Done._**
All 16 examples migrated from `pykale/examples`, `_shared/` infrastructure and build scripts in place, one complete narrative (`others/image_classification/digit_domain_adaptation`). Local repository only.

**Phase 2 — publish.**
Create `pykale/tutorials`, push, enable Actions, set branch protection, and decide the docs host (ReadTheDocs project vs GitHub Pages). That decision fills in the deploy step `.github/workflows/docs.yml` deliberately leaves blank.

Also required here: **Colab and Binder launch URLs do not resolve yet.** Both point at `notebooks/<domain>/<slug>/tutorial.ipynb`, on the assumption that CI commits sphinx-gallery's generated notebooks to `notebooks/` on main. Sphinx-gallery writes them under `_gallery/`, which is gitignored, and Colab cannot open a notebook from the docs site — only from GitHub, Drive or a gist. Until that CI step exists, every Colab and Binder badge is a 404.

**Phase 3 — the remaining 15 narratives.**
The bulk of the work. Small PRs, one bucket at a time, starting with `others/image_classification` since its four tutorials share a theme. Each landing PR clears that tutorial's `draft: true`. `make validate --strict-drafts` passes when the phase is complete.

**Phase 4 — landing page.**
Blocked on a framework decision. The data contract is already fixed and exported; see `../landing-page/README.md`.

**Phase 5 — retire `pykale/examples/`.**
A PR against the pykale repository: delete the migrated folders, redirect `examples/README.md`, `docs/source/tutorial.md` and `docs/source/notebooks.md` here, and fix every in-repo link. Must come last — pointing users at this site before it is complete breaks working links.

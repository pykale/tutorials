# Roadmap

**Phase 1 — scaffold and migrate. _Done._**
All 16 examples migrated from `pykale/examples`, shared infrastructure and build scripts in place, one complete narrative (`others/image_classification/digit_domain_adaptation`).

**Phase 2 — publish the site. _Done._**
The repository is at `pykale/tutorials`. The docs workflow builds the site and deploys pushes to `main` to GitHub Pages at `https://pykale.github.io/tutorials/`.

**Notebook launch actions remain pending.** Colab and Binder URLs expect `notebooks/<domain>/<slug>/plot_<slug>.ipynb` on `main`, but Sphinx-Gallery generates notebooks under the gitignored `_gallery/` directory. The site keeps notebook download and Colab actions disabled until notebooks are published and verified. Do not add launch badges to the README before that.

**Phase 3 — the remaining 15 narratives.**
The bulk of the work. Small PRs, one bucket at a time, starting with `others/image_classification` since its four tutorials share a theme. Each landing PR clears that tutorial's `draft: true`. `python scripts/validate_catalog.py --strict-drafts` passes when the phase is complete. The executing CI job can be run manually; its nightly schedule is currently disabled.

**Phase 4 — landing page.**
Blocked on a framework decision. The data contract is already fixed and exported; see `../landing-page/README.md`.

**Phase 5 — retire `pykale/examples/`.**
A PR against the pykale repository: delete the migrated folders, redirect `examples/README.md`, `docs/source/tutorial.md` and `docs/source/notebooks.md` here, and fix every in-repo link. Must come last — pointing users at this site before it is complete breaks working links.

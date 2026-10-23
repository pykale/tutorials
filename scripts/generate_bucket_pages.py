"""Write one landing page per bucket into ``_pages/``.

Sphinx-gallery generates an ``index.rst`` for each directory it is pointed at, which here means one
per *tutorial* -- there is nothing that collects ``others/*`` into a single page. Rather than nest
the gallery (sphinx-gallery only understands one level of subsection, and ``others`` is two deep),
each bucket gets a thin generated page whose toctree pulls in that bucket's tutorials.

Generated, not committed: ``_pages/`` is gitignored and rebuilt by ``make html``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from models import REPO_ROOT, Catalog, TutorialMetadata

PAGES_DIR = REPO_ROOT / "_pages"


def _load(relative_path: str) -> TutorialMetadata:
    text = (REPO_ROOT / relative_path / "metadata.yml").read_text(encoding="utf-8")
    return TutorialMetadata.model_validate(yaml.safe_load(text))


def _gallery_doc(relative_path: str) -> str:
    """Docname of the sphinx-gallery example page for a tutorial.

    Each folder is a one-example gallery, so linking to its ``index`` would land on a redundant
    single-thumbnail page; link straight to the ``plot_<slug>`` example instead. Absolute (leading
    slash) because these pages live in ``_pages/`` while the gallery is written to ``_gallery/``.
    """
    slug = Path(relative_path).name
    return f"/_gallery/{relative_path}/plot_{slug}"


def build() -> int:
    catalog = Catalog.load()
    PAGES_DIR.mkdir(exist_ok=True)
    written = 0

    for bucket in catalog.buckets:
        paths = bucket.iter_relative_paths()
        count = len(paths)
        count_line = "Tutorials in development." if count == 0 else f"{count} tutorial{'s' if count != 1 else ''}."
        lines = [
            f"{bucket.label}",
            "=" * len(bucket.label),
            "",
            ".. rst-class:: pky-domain-lead",
            "",
            f"   {' '.join(bucket.summary.split())} **{count_line}**",
            "",
        ]

        if not paths:
            lines += [
                ".. note::",
                "   No tutorial maps to this domain yet. See the roadmap for what is planned here,",
                "   and the contributing guide if you would like to add the first one.",
                "",
            ]
        else:
            # The column count is capped at the number of tutorials (max 4) so a domain with one or
            # two tutorials does not stretch a card across the whole container. CSS reads pky-cols-N.
            cols = min(count, 4)
            lines += [
                ".. grid:: 1 2 2 3",
                "   :gutter: 3",
                f"   :class-container: pky-domain-grid pky-cols-{cols}",
                "",
            ]
            for path in paths:
                metadata = _load(path)
                status = ":bdg-warning:`Draft`" if metadata.draft else ":bdg-success:`Written`"
                lines += [
                    f"   .. grid-item-card:: {metadata.title}",
                    f"      :link: {_gallery_doc(path)}",
                    "      :link-type: doc",
                    f"      :img-top: /source/_static/thumbnails/{metadata.slug}.svg",
                    f"      :class-card: pky-tut-card pky-{bucket.id.value}",
                    "",
                    f"      {status}",
                    "",
                    f"      {' '.join(metadata.summary.split())}",
                    "",
                    "      +++",
                    f"      {metadata.difficulty.value} · {metadata.estimated_runtime}",
                    "",
                ]
            lines += [
                ".. toctree::",
                "   :maxdepth: 1",
                "   :hidden:",
                "",
            ]
            lines += [f"   {_gallery_doc(path)}" for path in paths]
            lines.append("")

        target = PAGES_DIR / f"{bucket.id.value}.rst"
        target.write_text("\n".join(lines), encoding="utf-8")
        written += 1

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    count = build()
    print(f"wrote {count} bucket pages to {PAGES_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

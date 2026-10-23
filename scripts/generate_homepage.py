"""Generate the data-driven reStructuredText partials for the homepage and long-form list pages.

The homepage mixes hand-authored curated shells (hero, get-started, contributing -- in ``index.rst``)
with sections that must stay in sync with the catalogue and the news file. Those sections are
generated here into ``_generated/*.rst`` and pulled in with ``.. include::``, so:

* domain cards, counts and learning paths never drift from ``tutorial_catalog.yml``;
* announcements live in ``source/_data/news.yml``, not buried in ``index.rst``.

``_generated/`` is gitignored and excluded from the Sphinx source tree (the files are include
fragments, not standalone pages).

    python scripts/generate_homepage.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

import yaml
from models import REPO_ROOT, Catalog, TutorialMetadata

GENERATED_DIR = REPO_ROOT / "_generated"
NEWS_FILE = REPO_ROOT / "source" / "_data" / "news.yml"
# Each news badge gets a distinct sphinx-design colour role (styled in custom.css): New = green,
# Updated = blue, Planned = amber. Unknown badges fall back to a neutral secondary.
BADGE_ROLE = {"New": "bdg-success", "Updated": "bdg-info", "Planned": "bdg-warning"}


def _meta(path: str) -> TutorialMetadata:
    return TutorialMetadata.model_validate(
        yaml.safe_load((REPO_ROOT / path / "metadata.yml").read_text(encoding="utf-8"))
    )


def _gallery_doc(path: str) -> str:
    slug = Path(path).name
    return f"/_gallery/{path}/plot_{slug}"


def _news_rst() -> str:
    items = yaml.safe_load(NEWS_FILE.read_text(encoding="utf-8")) or []
    out = [".. grid:: 1 2 2 2", "   :gutter: 3", "   :class-container: pky-news", ""]
    for item in items:
        badge = item.get("badge", "")
        role = BADGE_ROLE.get(badge, "bdg-secondary")
        badge_rst = f":{role}:`{badge}`" if badge else ""
        out += [
            "   .. grid-item-card::",
            "      :class-card: pky-news-card",
            "",
            f"      {badge_rst} **{item['title']}**",
            "",
            f"      {' '.join(item['summary'].split())}",
        ]
        if item.get("link"):
            out += ["", f"      :doc:`{item.get('link_text', 'Learn more')} <{item['link']}>`"]
        out.append("")
    return "\n".join(out) + "\n"


def _domains_rst() -> str:
    catalog = Catalog.load()
    out = [".. grid:: 1 2 2 3", "   :gutter: 3", "   :class-container: pky-domains", ""]
    for bucket in catalog.buckets:
        count = len(bucket.iter_relative_paths())
        coming = bucket.status.value == "coming_soon"
        status = ":bdg-warning:`Coming soon`" if coming else f":bdg-success:`{count} tutorials`"
        examples = " · ".join(bucket.examples) if bucket.examples else ""
        action = f"Explore {bucket.label} →" if not coming else "In development"
        out += [
            f"   .. grid-item-card:: {bucket.label}",
            f"      :link: _pages/{bucket.id.value}",
            "      :link-type: doc",
            f"      :img-top: /source/_static/thumbnails/domain_{bucket.id.value}.svg",
            f"      :class-card: pky-domain-card pky-{bucket.id.value}",
            "",
            f"      {status}",
            "",
            f"      {' '.join(bucket.summary.split())}",
        ]
        if examples:
            out += ["", f"      *{examples}*"]
        out += ["", "      +++", f"      {action}", ""]
    return "\n".join(out) + "\n"


def _paths_rst() -> str:
    catalog = Catalog.load()
    slug_to_path = catalog.slug_to_path()
    out = [".. grid:: 1 2 2 2", "   :gutter: 3", "   :class-container: pky-paths", ""]
    for path_def in catalog.learning_paths:
        steps: List[str] = []
        for i, slug in enumerate(path_def.tutorials, 1):
            meta = _meta(slug_to_path[slug])
            steps.append(f"      {i}. :doc:`{meta.title} <{_gallery_doc(slug_to_path[slug])}>`")
        out += [
            f"   .. grid-item-card:: {path_def.title}",
            "      :class-card: pky-path-card",
            "",
            f"      {' '.join(path_def.summary.split())}",
            "",
            *steps,
            "",
        ]
    return "\n".join(out) + "\n"


def _ecosystem_rst() -> str:
    catalog = Catalog.load()
    out = [".. grid:: 1 2 3 3", "   :gutter: 3", "   :class-container: pky-ecosystem", ""]
    for entry in catalog.ecosystem:
        title = f"{entry.name}"
        card = [f"   .. grid-item-card:: {title}", "      :class-card: pky-eco-card"]
        if entry.url:
            card.append(f"      :link: {entry.url}")
        card += ["", f"      {' '.join(entry.description.split())}"]
        if entry.planned:
            card += ["", "      :bdg-secondary:`Planned`"]
        card.append("")
        out += card
    return "\n".join(out) + "\n"


def _status_table_rst() -> str:
    """A list-table of every tutorial's status, for the Tutorial Status page."""
    catalog = Catalog.load()
    rows = [
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 30 16 18 18 18",
        "   :class: pky-status-table",
        "",
        "   * - Tutorial",
        "     - Domain",
        "     - Status",
        "     - Difficulty",
        "     - Runtime",
    ]
    for path in catalog.iter_relative_paths():
        meta = _meta(path)
        status = "Draft" if meta.draft else "Written"
        rows += [
            f"   * - :doc:`{meta.title} <{_gallery_doc(path)}>`",
            f"     - {meta.domain.value if meta.domain.value != 'others' else 'general'}",
            f"     - {status}",
            f"     - {meta.difficulty.value}",
            f"     - {meta.estimated_runtime}",
        ]
    return "\n".join(rows) + "\n"


def build() -> int:
    GENERATED_DIR.mkdir(exist_ok=True)
    files = {
        "news.rst": _news_rst(),
        "domains.rst": _domains_rst(),
        "paths.rst": _paths_rst(),
        "ecosystem.rst": _ecosystem_rst(),
        "status_table.rst": _status_table_rst(),
    }
    for name, content in files.items():
        (GENERATED_DIR / name).write_text(content, encoding="utf-8")
    return len(files)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    count = build()
    print(f"wrote {count} homepage partials to {GENERATED_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

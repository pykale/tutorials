"""Emit the landing page's data file from the catalog and per-tutorial metadata.

This JSON is the *only* coupling between the tutorials tree and the landing page: the site never
reads tutorial folders. Facets are derived from the metadata enums, so a new modality or fusion type
appears as a filter without touching the site.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import yaml
from models import REPO_ROOT, Catalog, TutorialMetadata

sys.path.insert(0, str(REPO_ROOT / "_shared"))
from launch.binder import binder_url  # noqa: E402
from launch.colab import colab_url  # noqa: E402

DEFAULT_OUTPUT = REPO_ROOT.parent / "landing-page" / "src" / "data" / "tutorials.json"
DOCS_BASE = "https://pykale.github.io/tutorials"


def _tutorial_entry(relative_path: str) -> Dict[str, Any]:
    metadata_path = REPO_ROOT / relative_path / "metadata.yml"
    metadata = TutorialMetadata.model_validate(yaml.safe_load(metadata_path.read_text(encoding="utf-8")))
    parts = Path(relative_path).parts

    entry: Dict[str, Any] = {
        "slug": metadata.slug,
        "title": metadata.title,
        "summary": metadata.summary,
        "path": relative_path,
        # Group is the optional middle folder, e.g. "image_classification". Paths are
        # (domain, slug) or (domain, group, slug).
        "group": parts[1] if len(parts) == 3 else None,
        "domain": metadata.domain.value,
        "task": metadata.task,
        "modality": [m.value for m in metadata.modality],
        "method": metadata.method,
        "fusion": metadata.fusion.value,
        "dataset": [d.name for d in metadata.dataset],
        "difficulty": metadata.difficulty.value,
        "hardware": metadata.hardware.value,
        "estimated_runtime": metadata.estimated_runtime,
        "kale_api": metadata.kale_api,
        "draft": metadata.draft,
        "source_example": metadata.source_example,
        "run_command": metadata.run_command,
        "references": metadata.references,
        "links": {
            "docs": f"{DOCS_BASE}/{metadata.domain.value}/{metadata.slug}.html",
            "source": f"https://github.com/pykale/tutorials/tree/main/{relative_path}",
            "colab": colab_url(relative_path) if metadata.colab else None,
            "binder": binder_url(relative_path) if metadata.binder else None,
        },
    }
    return entry


def _facets(entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Filter options with counts, so the site can grey out or hide empty ones."""

    def counted(values: List[str]) -> List[Dict[str, Any]]:
        return [{"value": value, "count": count} for value, count in sorted(Counter(values).items())]

    return {
        "domain": counted([e["domain"] for e in entries]),
        "task": counted([e["task"] for e in entries]),
        "modality": counted([m for e in entries for m in e["modality"]]),
        "method": counted([m for e in entries for m in e["method"]]),
        "fusion": counted([e["fusion"] for e in entries]),
        "dataset": counted([d for e in entries for d in e["dataset"]]),
        "difficulty": counted([e["difficulty"] for e in entries]),
        "hardware": counted([e["hardware"] for e in entries]),
    }


def build_payload() -> Dict[str, Any]:
    catalog = Catalog.load()
    entries = [_tutorial_entry(path) for path in catalog.iter_relative_paths()]

    buckets = [
        {
            "id": bucket.id.value,
            "label": bucket.label,
            "color": bucket.color,
            "summary": " ".join(bucket.summary.split()),
            "groups": [{"id": g.id, "label": g.label} for g in bucket.groups],
            "count": sum(1 for e in entries if e["domain"] == bucket.id.value),
        }
        for bucket in catalog.buckets
    ]

    return {
        "schema_version": catalog.version,
        "docs_base": DOCS_BASE,
        "buckets": buckets,
        "tutorials": entries,
        "facets": _facets(entries),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if the committed file is stale")
    args = parser.parse_args()

    payload = json.dumps(build_payload(), indent=2) + "\n"

    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != payload:
            print(f"{args.output} is stale; run: make export")
            return 1
        print("landing-page data up to date")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    print(f"wrote {args.output} ({len(payload.splitlines())} lines)")

    # The site's own faceted catalogue reads this from _static so the build is self-contained; the
    # landing-page copy is the separate downstream consumer.
    static_copy = REPO_ROOT / "_static" / "tutorials.json"
    static_copy.write_text(payload, encoding="utf-8")
    print(f"wrote {static_copy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

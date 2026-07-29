"""Data-driven left-sidebar context label ("Tutorials in General" / "More General tutorials").

Pure and testable: the domain label always comes from the catalogue, never hard-coded in a template.
``conf.py`` calls :func:`sidebar_context` from its html-page-context hook.
"""

from __future__ import annotations

from typing import Optional, Tuple

from models import Catalog
from tutorial_actions import gallery_pagename_to_tutorial


def _bucket_by_domain(catalog: Catalog, domain_id: str):
    for bucket in catalog.buckets:
        if bucket.id.value == domain_id:
            return bucket
    return None


def sidebar_context(catalog: Catalog, pagename: str) -> Optional[Tuple[str, str]]:
    """Return ``(visible_label, nav_aria_label)`` for the left sidebar, or None.

    Domain pages -> ``"Tutorials in <Label> · <count>"``; tutorial pages -> ``"More <Label>
    tutorials"``. The ``<Label>`` is the catalogue's bucket label.

    Args:
        catalog: The loaded catalogue.
        pagename: The Sphinx pagename.

    Returns:
        tuple[str, str] | None: (visible text, aria-label) or None when the page has no domain.
    """
    if pagename.startswith("_pages/"):
        bucket = _bucket_by_domain(catalog, pagename.split("/", 1)[1])
        if bucket:
            count = len(bucket.iter_relative_paths())
            aria = f"Tutorials in {bucket.label}"
            visible = f"{aria} · {count}" if count else aria
            return visible, aria

    mapped = gallery_pagename_to_tutorial(pagename)
    if mapped:
        rel_path, _slug = mapped
        bucket = _bucket_by_domain(catalog, rel_path.split("/", 1)[0])
        if bucket:
            label = f"More {bucket.label} tutorials"
            return label, label

    return None

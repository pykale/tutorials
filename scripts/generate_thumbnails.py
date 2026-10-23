"""Deterministic SVG placeholder thumbnails for tutorials.

Draft tutorials produce no figure, so their gallery cards would otherwise be blank. This builds one
branded SVG per tutorial -- domain accent colour, a domain-relevant abstract symbol, the title, and a
Draft / Coming soon badge -- so the catalogue never looks unfinished, while a stub still reads
*clearly as a stub*.

Deterministic: the same metadata always yields byte-identical SVG (no timestamps, no randomness), so
the files are reproducible and a ``--check`` mode can verify them in CI. Output goes to
``source/_static/thumbnails/`` (gitignored); the real sphinx-gallery figure supersedes the placeholder
once a tutorial is written and executed (see :func:`resolve_thumbnail`).

    python scripts/generate_thumbnails.py            # write all
    python scripts/generate_thumbnails.py --check     # fail if any is stale/missing
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml
from models import REPO_ROOT, Catalog, TutorialMetadata

THUMBNAIL_DIR = REPO_ROOT / "source" / "_static" / "thumbnails"
WIDTH, HEIGHT = 400, 260

# Abstract domain symbols. Each returns SVG markup drawn in `accent`, centred around (cx, cy). Kept
# geometric and non-literal on purpose -- no medically misleading imagery.


def _sym_nodes(accent: str) -> str:  # General: a small connected network
    pts = [(150, 90), (250, 80), (300, 150), (210, 175), (120, 150)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 3), (1, 3)]
    lines = "".join(
        f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" '
        f'stroke="{accent}" stroke-width="2" opacity="0.5"/>'
        for a, b in edges
    )
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{accent}"/>' for x, y in pts)
    return lines + dots


def _sym_molecule(accent: str) -> str:  # Protein: hexagon ring with bonded nodes
    ring = "205,70 250,95 250,145 205,170 160,145 160,95"
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="8" fill="{accent}"/>'
        for x, y in [(205, 70), (250, 95), (250, 145), (205, 170), (160, 145), (160, 95)]
    )
    tail = (
        f'<line x1="250" y1="95" x2="300" y2="80" stroke="{accent}" stroke-width="2"/>'
        f'<circle cx="300" cy="80" r="8" fill="{accent}"/>'
    )
    return f'<polygon points="{ring}" fill="none" stroke="{accent}" stroke-width="2.5"/>' + dots + tail


def _sym_layers(accent: str) -> str:  # Cancer: stacked multi-omics layers
    out = []
    for i, dy in enumerate((110, 135, 160)):
        op = 0.35 + i * 0.25
        out.append(
            f'<polygon points="150,{dy} 250,{dy - 22} 300,{dy} 200,{dy + 22}" ' f'fill="{accent}" opacity="{op:.2f}"/>'
        )
    return "".join(out)


def _sym_pulse(accent: str) -> str:  # Cardiac: an ECG trace
    return (
        f'<polyline points="120,150 165,150 180,110 200,190 220,130 240,150 300,150" '
        f'fill="none" stroke="{accent}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def _sym_lattice(accent: str) -> str:  # Materials: a crystal lattice
    dots = []
    lines = []
    coords = [(x, y) for y in (95, 145, 195) for x in (160, 210, 260)]
    for x, y in coords:
        dots.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{accent}"/>')
    for i in (0, 1, 3, 4, 6, 7):
        x, y = coords[i]
        lines.append(f'<line x1="{x}" y1="{y}" x2="{x + 50}" y2="{y}" stroke="{accent}" stroke-width="1.5"/>')
    for i in (0, 1, 2, 3, 4, 5):
        x, y = coords[i]
        lines.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 50}" stroke="{accent}" stroke-width="1.5"/>')
    return "".join(lines) + "".join(dots)


SYMBOLS = {
    "nodes": _sym_nodes,
    "molecule": _sym_molecule,
    "layers": _sym_layers,
    "pulse": _sym_pulse,
    "lattice": _sym_lattice,
}


def _wrap(text: str, width: int = 34, max_lines: int = 2) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        if len(current) + len(word) + 1 > width and current:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and (len(" ".join(lines)) < len(text)):
        lines[-1] = lines[-1].rstrip(".") + "…"
    return lines


def thumbnail_filename(slug: str) -> str:
    """Return the stable filename for a tutorial's placeholder.

    Args:
        slug: The tutorial slug.

    Returns:
        str: ``"<slug>.svg"`` -- slugs are unique across the catalogue.
    """
    return f"{slug}.svg"


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def thumbnail_svg(title: str, accent: str, symbol: str, *, badge: Optional[str] = None, bare: bool = False) -> str:
    """Build a deterministic branded placeholder SVG.

    Args:
        title: Tutorial title, drawn (wrapped) at the bottom.
        accent: Domain accent colour, ``#rrggbb``.
        symbol: Domain symbol id; one of :data:`SYMBOLS`. Unknown ids fall back to ``nodes``.
        badge: Optional status word (e.g. ``"Draft"``, ``"Coming soon"``) shown top-right. Status is
            carried by this text, never by colour alone.
        bare: If True, omit the drawn title (used for domain hero tiles, where the card supplies the
            name). The symbol is re-centred and the accessible label still carries the title.

    Returns:
        str: Complete standalone ``<svg>`` markup.
    """
    draw = SYMBOLS.get(symbol, _sym_nodes)
    if bare:
        title_block = ""
    else:
        lines = _wrap(title)
        text_y = HEIGHT - 46 - (len(lines) - 1) * 22
        title_tspans = "".join(
            f'<tspan x="28" dy="{0 if i == 0 else 22}">{_escape(line)}</tspan>' for i, line in enumerate(lines)
        )
        title_block = (
            f'<text x="28" y="{text_y}" font-family="system-ui, sans-serif" font-size="19" '
            f'font-weight="700" fill="#1f2a26">{title_tspans}</text>'
        )
    badge_svg = ""
    if badge:
        w = 22 + len(badge) * 8
        badge_svg = (
            f'<g><rect x="{WIDTH - w - 20}" y="18" width="{w}" height="26" rx="13" '
            f'fill="#ffffff" stroke="{accent}" stroke-width="1.5"/>'
            f'<text x="{WIDTH - w / 2 - 20}" y="35" text-anchor="middle" '
            f'font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="{accent}">'
            f"{_escape(badge)}</text></g>"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" aria-label="{_escape(title)}">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{accent}" stop-opacity="0.10"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0.02"/></linearGradient></defs>'
        # Solid light base so the tile is self-contained: the dark title stays legible whether the
        # surrounding card is light or dark.
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#fbfdfc"/>'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#g)"/>'
        f'<rect width="{WIDTH}" height="6" fill="{accent}"/>'
        f"{draw(accent)}"
        f"{badge_svg}"
        f"{title_block}"
        f'<text x="28" y="{HEIGHT - 18}" font-family="system-ui, sans-serif" font-size="12" '
        f'font-weight="600" fill="{accent}" letter-spacing="0.5">PyKale Tutorials</text>'
        f"</svg>"
    )


def resolve_thumbnail(slug: str, real_thumbnail: Optional[Path]) -> str:
    """Choose the image a card should show for a tutorial.

    The real sphinx-gallery figure wins when a tutorial has been executed and produced one; otherwise
    the branded placeholder is used, so a card is never blank.

    Args:
        slug: Tutorial slug.
        real_thumbnail: Path to a gallery-generated thumbnail, or ``None`` if none exists.

    Returns:
        str: A ``_static``-relative reference the HTML can use.
    """
    if real_thumbnail is not None and real_thumbnail.exists():
        return real_thumbnail.as_posix()
    return f"_static/thumbnails/{thumbnail_filename(slug)}"


def _badge_for(metadata: TutorialMetadata) -> Optional[str]:
    return "Draft" if metadata.draft else None


def build(check: bool = False) -> int:
    """Write (or verify) one placeholder per tutorial, plus one per domain bucket.

    Args:
        check: If True, do not write; return the count of stale/missing files instead.

    Returns:
        int: Number of files written, or (in check mode) the number that were stale/missing.
    """
    catalog = Catalog.load()
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)
    accent_by_domain = {b.id.value: b.color for b in catalog.buckets}
    symbol_by_domain = {b.id.value: b.icon for b in catalog.buckets}

    stale = 0
    written = 0
    for path in catalog.iter_relative_paths():
        metadata = TutorialMetadata.model_validate(
            yaml.safe_load((REPO_ROOT / path / "metadata.yml").read_text(encoding="utf-8"))
        )
        svg = thumbnail_svg(
            metadata.title,
            accent_by_domain[metadata.domain.value],
            symbol_by_domain[metadata.domain.value],
            badge=_badge_for(metadata),
        )
        target = THUMBNAIL_DIR / thumbnail_filename(metadata.slug)
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != svg:
                stale += 1
        else:
            target.write_text(svg, encoding="utf-8")
            written += 1

    # One hero tile per domain, so every domain card has a branded image. Empty domains are badged
    # "Coming soon"; populated ones carry no badge.
    for bucket in catalog.buckets:
        empty = not (bucket.tutorials or bucket.groups)
        svg = thumbnail_svg(bucket.label, bucket.color, bucket.icon, badge="Coming soon" if empty else None, bare=True)
        target = THUMBNAIL_DIR / f"domain_{bucket.id.value}.svg"
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != svg:
                stale += 1
        else:
            target.write_text(svg, encoding="utf-8")
            written += 1

    return stale if check else written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if any placeholder is stale or missing")
    args = parser.parse_args()

    if args.check:
        stale = build(check=True)
        if stale:
            print(f"{stale} thumbnail(s) stale or missing; run: python scripts/generate_thumbnails.py")
            return 1
        print("thumbnails up to date")
        return 0

    written = build()
    print(f"wrote {written} thumbnails to {THUMBNAIL_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

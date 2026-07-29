"""Structural regression guards for the homepage layout.

The hero was previously clipped by a `width: 100vw` + negative-margin breakout hack. These tests fail
if such fragile offsets return, or if the homepage stops declaring its landing container / hero.
"""

from __future__ import annotations

from models import REPO_ROOT

CSS = (REPO_ROOT / "_static" / "custom.css").read_text(encoding="utf-8")
INDEX = (REPO_ROOT / "index.rst").read_text(encoding="utf-8")


def test_no_viewport_width_breakout_on_hero():
    # The clipping bug: full-viewport width pulled the hero off the left edge.
    assert "100vw" not in CSS, "100vw breakout reintroduced (caused the hero clipping)"
    assert "calc(-50vw" not in CSS, "negative half-viewport margin reintroduced"


def test_hero_uses_no_negative_left_margin_or_transform_positioning():
    # Scan the .pky-hero rule block only.
    start = CSS.index(".pky-hero {")
    block = CSS[start:start + 600]
    assert "margin-left: calc" not in block
    assert "translateX" not in block and "position: absolute" not in block


def test_landing_container_and_hero_declared():
    # Landing pages share the same page-width as every other page (no landing-only cap) for
    # consistency -- the shared 1880px container, not a narrower override.
    assert "max-width: 1880px" in CSS, "shared page-width container missing"
    assert "body.pky-landing .bd-page-width { max-width" not in CSS, "landing has a narrower width cap"
    assert ".pky-hero" in CSS
    assert "pky-hero" in INDEX, "homepage no longer renders the hero"


def test_landing_pages_are_declared_in_conf():
    conf = (REPO_ROOT / "conf.py").read_text(encoding="utf-8")
    assert "_LANDING_PAGES" in conf
    assert "pky-onthispage" in conf and "pky-ecosystem" in conf and "pky-feedback" in conf


def test_green_focus_ring_not_removed():
    # Global green focus ring stays; where nav toggles drop the outline they replace it with a
    # visible green inset bottom line (an accessible treatment), never a blanket removal.
    assert "outline: 3px solid var(--pykale-focus)" in CSS
    start = CSS.index(".bd-header .pky-dropdown .nav-link.dropdown-toggle:focus-visible")
    block = CSS[start:start + 220]
    assert "outline: none" in block and "inset 0 -2px 0 var(--pst-color-primary)" in block


def test_sidebars_are_compact():
    # Rails slimmed from pydata's defaults; guards against wide sidebars returning.
    assert "--pst-sidebar-secondary: 13.5rem" in CSS
    assert "flex: 0 0 12.5rem" in CSS


def test_card_grid_has_five_column_max_breakpoint():
    assert "repeat(5, minmax(0, 1fr))" in CSS
    assert "min-width: 1600px" in CSS  # five is a wide-screen maximum


def test_back_to_top_is_bounded_not_a_bar():
    start = CSS.index("#pst-back-to-top {")
    block = CSS[start:start + 400]
    assert "border-radius: 50%" in block
    assert "46px" in block  # compact circle, not a full-width bar


def test_wide_container_widens_content():
    assert "max-width: 1880px" in CSS


def test_article_container_cap_is_released():
    # The 960px article cap (the main whitespace source) is overridden at matching specificity.
    assert ".bd-main .bd-content .bd-article-container { max-width: none" in CSS


def test_sidebars_within_accepted_maximums():
    # left ~200px (12.5rem), right ~216px (13.5rem) -- both under the accepted maxima.
    assert "flex: 0 0 12.5rem" in CSS
    assert "--pst-sidebar-secondary: 13.5rem" in CSS


def test_catalogue_grid_can_reach_five_columns():
    # The homepage/all-tutorials catalogue still scales to five columns on very wide screens.
    assert "repeat(5, minmax(0, 1fr))" in CSS


def test_bucket_grid_columns_are_capped_per_count():
    # Column count is fixed per page (pky-cols-N); a single card is bounded by max-width so it does
    # not stretch across the container, while a full domain fills the row.
    assert ".pky-domain-grid.pky-cols-1 .sd-row { grid-template-columns: minmax(0, 1fr); max-width: 24rem" in CSS
    assert ".pky-domain-grid.pky-cols-4 .sd-row { grid-template-columns: repeat(4, minmax(0, 1fr))" in CSS
    assert "repeat(5" not in CSS[CSS.index(".pky-domain-grid .sd-row {"):CSS.index(".pky-domain-grid .sd-col")]


def test_bucket_grid_column_count_is_generated_from_metadata():
    from generate_bucket_pages import build

    build()
    from models import REPO_ROOT

    # Cancer has 1 tutorial -> pky-cols-1; Protein has 3 -> pky-cols-3.
    cancer = (REPO_ROOT / "_pages" / "cancer.rst").read_text(encoding="utf-8")
    protein = (REPO_ROOT / "_pages" / "protein.rst").read_text(encoding="utf-8")
    assert "pky-cols-1" in cancer
    assert "pky-cols-3" in protein


def test_navbar_uses_bottom_indicator_not_rectangle():
    # No full outline rectangle on the toggles; a green inset bottom line instead.
    assert "inset 0 -2px 0 var(--pst-color-primary)" in CSS
    start = CSS.index(".bd-header .pky-dropdown .nav-link.dropdown-toggle:focus-visible")
    block = CSS[start:start + 200]
    assert "outline: none" in block  # rectangle removed, replaced by the indicator


def test_back_to_top_arrow_is_visible():
    start = CSS.index("#pst-back-to-top svg")
    block = CSS[start:start + 200]
    assert "fill: #fff" in block  # the theme arrow SVG is shown white, not hidden
    assert "display: none" not in block

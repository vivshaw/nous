"""Smoke tests for the generated reference sheet. The sheet's correctness is
*visual*, so it gets checked in a real browser.
"""

from __future__ import annotations

import os
import pathlib
from typing import Any

import pytest
from build_swatches import SHEET, build

VIEWPORT = 1280

INSTALL_HINT = (
    "no browser available - Playwright is installed, but the browser it drives is a "
    "separate download. Run `uv run playwright install chromium` once, "
    "or set GRO_CHROME to a Chromium/Chrome executable"
)


@pytest.fixture(scope="module")
def browser() -> Any:
    """One isolated Chromium for this module.
    `GRO_CHROME` overrides the pinned browser for environments where
    Playwright's own installer can't run (NixOS, air-gapped).
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip(INSTALL_HINT)

    launch: dict[str, Any] = {"headless": True}
    if override := (os.environ.get("GRO_CHROME") or "").strip():
        if not pathlib.Path(override).exists():
            pytest.fail(f"GRO_CHROME points at a missing file: {override}")
        launch["executable_path"] = override

    with sync_playwright() as play:
        try:
            engine = play.chromium.launch(**launch)
        except Exception as exc:
            pytest.skip(f"{INSTALL_HINT}\n  (playwright said: {exc})")
        try:
            yield engine
        finally:
            engine.close()


@pytest.fixture(scope="module")
def sheets(browser):
    """The sheet loaded once per theme, each in its own browser context."""
    loaded = {}
    contexts = []
    try:
        for theme in ("light", "dark"):
            context = browser.new_context(
                viewport={"width": VIEWPORT, "height": 1000},
                color_scheme=theme,
                device_scale_factor=2,
            )
            contexts.append(context)
            tab = context.new_page()
            errors: list[str] = []
            tab.on("console",
                   lambda m, sink=errors: sink.append(m.text) if m.type == "error" else None)
            tab.on("pageerror", lambda e, sink=errors: sink.append(str(e)))
            # `networkidle`, so the webfont has settled before anything is measured
            tab.goto(SHEET.resolve().as_uri(), wait_until="networkidle")
            tab.emulate_media(color_scheme=theme)
            loaded[theme] = (tab, errors)
        yield loaded
    finally:
        for context in contexts:
            context.close()


@pytest.fixture(scope="module")
def light(sheets):
    return sheets["light"]


@pytest.fixture(scope="module")
def dark(sheets):
    return sheets["dark"]


def test_sheet_is_up_to_date_with_its_generator() -> None:
    """Hand-editing the generated HTML is a trap; this is the tripwire."""
    assert SHEET.read_text() == build(), (
        "swatches.html differs from tools/build_swatches.py - "
        "run `uv run python tools/build_swatches.py`"
    )


def test_no_console_errors(light) -> None:
    tab, errors = light
    assert errors == []


def test_page_does_not_scroll_sideways(light) -> None:
    """Horizontal overflow is the most common generated-layout bug."""
    tab, _ = light
    assert tab.evaluate("document.documentElement.scrollWidth") <= VIEWPORT


def test_inter_actually_loaded(light) -> None:
    """A missing webfont degrades silently to a system sans - catch it here."""
    tab, _ = light
    assert tab.evaluate("document.fonts.check('16px Inter')")


def test_no_chart_card_has_a_nested_scrollbar(light) -> None:
    """A card sized to the plot but not the axis band grows its own tiny scroll."""
    tab, _ = light
    overflowing = tab.evaluate("""
        Array.from(document.querySelectorAll('.card')).filter(
            el => el.scrollHeight > el.clientHeight + 1
        ).map(el => (el.querySelector('.chart-title') || el).textContent.trim())
    """)
    assert overflowing == []


def test_every_chart_has_an_accessible_name(light) -> None:
    tab, _ = light
    unlabelled = tab.evaluate("""
        Array.from(document.querySelectorAll('svg[role="img"]'))
             .filter(s => !s.getAttribute('aria-label')).length
    """)
    assert unlabelled == 0


def test_dark_mode_is_actually_dark(dark) -> None:
    """Guards against the theme attribute overriding the OS preference again."""
    tab, _ = dark
    background = tab.evaluate("getComputedStyle(document.body).backgroundColor")
    channels = [int(v) for v in background.strip("rgba() ").split(",")[:3]]
    assert sum(channels) / 3 < 60, f"body background {background} is not a dark surface"


def test_light_and_dark_pick_different_series_colours(light, dark) -> None:
    def slot_one(tab) -> str:
        return tab.evaluate(
            "getComputedStyle(document.documentElement).getPropertyValue('--viz-1').trim()"
        )

    assert slot_one(light[0]) != slot_one(dark[0])

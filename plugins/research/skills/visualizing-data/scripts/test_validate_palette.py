"""Tests for the chart-palette validator.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from validate_palette import (
    CVD_FLOOR,
    check_categorical,
    check_ramp,
    contrast,
    delta_e,
    oklch,
    pair_indices,
)

SCRIPT = Path(__file__).with_name("validate_palette.py")

SURFACE = "#fbfaf9"

PASSING_PALETTE = ["#7b36c1", "#00848f", "#a37300", "#ae1387", "#0462d3", "#008455"]
SEQUENTIAL_RAMP = ["#f2eaff", "#e0cdfe", "#c2a2f3", "#af7fef", "#9654e0", "#7b36c1", "#5a2391"]

# Clears every check except surface contrast, where it lands in the relief band.
CONTRAST_WARN_PAIR = ["#aa6df5", "#2da4b0"]


def states(checks: list[tuple[str, str, str]]) -> dict[str, str]:
    return {name: state for name, state, _ in checks}


# --- colour maths ------------------------------------------------------------
def test_contrast_is_symmetric_and_bounded() -> None:
    assert contrast("#ffffff", "#000000") == pytest.approx(21.0, abs=0.01)
    assert contrast("#000000", "#ffffff") == pytest.approx(21.0, abs=0.01)
    assert contrast("#7b36c1", "#7b36c1") == pytest.approx(1.0, abs=1e-9)


def test_delta_e_of_a_colour_with_itself_is_zero() -> None:
    assert delta_e("#a37300", "#a37300") == pytest.approx(0.0, abs=1e-9)
    assert delta_e("#a37300", "#a37300", "deutan") == pytest.approx(0.0, abs=1e-9)


def test_simulated_vision_collapses_a_pair_that_normal_vision_separates() -> None:
    """Red and green are far apart until deuteranopia is simulated."""
    plain = delta_e("#ce1c20", "#128737")
    simulated = delta_e("#ce1c20", "#128737", "deutan")
    assert plain > simulated
    assert simulated < CVD_FLOOR


def test_oklch_hue_wraps_into_degrees() -> None:
    for colour in PASSING_PALETTE:
        lightness, chroma, hue = oklch(colour)
        assert 0.0 <= lightness <= 1.0
        assert chroma > 0
        assert 0.0 <= hue < 360.0


def test_hex_parsing_tolerates_padding_and_a_missing_hash() -> None:
    assert contrast(" #ffffff ", "000000") == pytest.approx(21.0, abs=0.01)


# --- which pairs get checked -------------------------------------------------
def test_adjacent_pairs_are_only_neighbours() -> None:
    assert pair_indices(4, "adjacent") == [(0, 1), (1, 2), (2, 3)]


def test_all_pairs_is_every_combination() -> None:
    assert pair_indices(4, "all") == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def test_all_pairs_is_a_superset_of_adjacent() -> None:
    assert set(pair_indices(6, "adjacent")) <= set(pair_indices(6, "all"))


# --- catching bad palettes ---------------------------------------------------
def test_a_near_grey_fails_the_chroma_floor() -> None:
    checks = states(check_categorical(["#7b36c1", "#8d8b8f"], "light", SURFACE, "adjacent"))
    assert checks["Chroma floor"] == "fail"


def test_a_colour_outside_the_band_fails() -> None:
    checks = states(check_categorical(["#f2eaff", "#7b36c1"], "light", SURFACE, "adjacent"))
    assert checks["Lightness band"] == "fail"


def test_two_near_identical_hues_fail_the_plain_sight_gap() -> None:
    checks = states(check_categorical(["#7b36c1", "#7d39c4"], "light", SURFACE, "adjacent"))
    assert checks["Plain-sight gap"] == "fail"


def test_low_contrast_warns_rather_than_fails() -> None:
    """Sub-3:1 is legal with visible labels or a table view, so it is a warning.
    """
    checks = states(check_categorical(CONTRAST_WARN_PAIR, "light", SURFACE, "adjacent"))
    assert checks["Surface contrast"] == "warn"
    assert [state for name, state in checks.items() if name != "Surface contrast"] == ["pass"] * 4


def test_a_single_colour_has_nothing_to_separate() -> None:
    checks = states(check_categorical(["#7b36c1"], "light", SURFACE, "adjacent"))
    assert checks["CVD separation"] == "pass"
    assert checks["Plain-sight gap"] == "pass"


# --- ramps -------------------------------------------------------------------
def test_a_pale_ramp_end_warns_for_a_heat_scale_but_fails_for_ordered_marks() -> None:
    assert check_ramp(SEQUENTIAL_RAMP, "light", SURFACE, ordinal=False)[2][1] == "warn"
    assert check_ramp(SEQUENTIAL_RAMP, "light", SURFACE, ordinal=True)[2][1] == "fail"


def test_a_ramp_out_of_order_fails() -> None:
    shuffled = [SEQUENTIAL_RAMP[0], SEQUENTIAL_RAMP[3], SEQUENTIAL_RAMP[1]]
    checks = states(check_ramp(shuffled, "light", SURFACE, False))
    assert checks["Monotone lightness"] == "fail"


def test_a_multi_hue_ramp_fails_hue_stability() -> None:
    rainbow = ["#f2eaff", "#63c9d4", "#a37300"]
    assert states(check_ramp(rainbow, "light", SURFACE, False))["Hue stability"] == "fail"


def test_steps_too_close_together_fail() -> None:
    crowded = ["#7b36c1", "#7d39c4", "#5a2391"]
    assert states(check_ramp(crowded, "light", SURFACE, False))["Step separation"] == "fail"


def test_categorical_checks_reject_a_perfectly_good_ramp() -> None:
    """Documented behaviour: running the wrong checks fails a correct ramp."""
    assert "fail" in states(
        check_categorical(SEQUENTIAL_RAMP, "light", SURFACE, "adjacent")
    ).values()


# --- the command line --------------------------------------------------------
def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False
    )


def test_cli_exits_zero_when_every_check_passes() -> None:
    result = run(",".join(PASSING_PALETTE), "--mode", "light", "--surface", SURFACE)
    assert result.returncode == 0
    assert "PASSED" in result.stdout


def test_cli_exits_one_on_a_hard_failure() -> None:
    result = run("#7b36c1,#7d39c4", "--mode", "light")
    assert result.returncode == 1
    assert "FAILED" in result.stdout


def test_cli_exits_zero_on_a_warning() -> None:
    result = run(",".join(CONTRAST_WARN_PAIR), "--mode", "light")
    assert result.returncode == 0
    assert "PASSED with warnings" in result.stdout


def test_cli_rejects_malformed_hex() -> None:
    result = run("#7b36c1,nonsense", "--mode", "light")
    assert result.returncode == 2
    assert "not #rrggbb hex" in result.stderr


def test_cli_rejects_an_empty_palette() -> None:
    assert run(" , , ").returncode == 2

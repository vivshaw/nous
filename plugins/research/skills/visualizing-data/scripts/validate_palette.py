#!/usr/bin/env python3
"""Check a chart palette against the measurable rules in `research:visualizing-data`.

Colour safety is not just taste, it is arithmetic. This script does the math so nobody
has to squint at swatches and decide whether two hues "look different enough".

Two modes:

  categorical (default)  identity colours (one hue per series)
    - lightness band     OKLCH L inside the band for the render mode
    - chroma floor       OKLCH C at or above the floor, so a hue is not near-grey
    - CVD separation     OKLab dE (x100) under simulated protanopia/deuteranopia
    - plain-sight gap    the same dE under unsimulated vision
    - surface contrast   WCAG ratio of each mark against the chart surface

  ramp (--ramp)          magnitude colours (one hue, light to dark)
    - monotone lightness, visible step gaps, and a hue that does not wander
    - add --ordinal for discrete ordered marks (funnel stages, tiers, buckets),
      which requires the low end to remain distinguishable from the background.

Usage:
  python3 validate_palette.py "#6d3fa8,#0f7d78,..." --mode light
  python3 validate_palette.py "#6d3fa8,..." --mode dark --surface "#141317"
  python3 validate_palette.py "#6d3fa8,..." --pairs all      # scatter/bubble/map
  python3 validate_palette.py "#efe6fa,...,#2a1046" --ramp    # heat scale
  python3 validate_palette.py "#c2a2f3,...,#5a2391" --ordinal # ordered marks

Exits 0 when nothing hard-fails, 1 otherwise.
Two checks can give a warning without failing, because each is legal with a
documented mitigation:
  - CVD dE in the 6-8 band, legal only alongside a second encoding channel
    (direct labels, surface gaps, texture)
  - sub-3:1 surface contrast, legal only alongside visible labels or a table view
"""

from __future__ import annotations

import argparse
import math
import re
import sys

# --- thresholds -------------------------------------------------------------
# OKLCH lightness bands. Dark surfaces need a narrower, brighter band: a mark
# that is legible on white disappears on near-black.
LIGHTNESS_BAND = {"light": (0.42, 0.76), "dark": (0.50, 0.80)}

# Below this OKLCH chroma a hue stops carrying identity and reads as grey.
CHROMA_FLOOR = 0.06

# dE throughout is Euclidean distance in OKLab, x100.
CVD_TARGET = 8.0          # aim for this between colours that can touch
CVD_FLOOR = 6.0           # below target but legal *with* a second encoding channel
PLAIN_SIGHT_FLOOR = 15.0  # distinguishable under ordinary colour vision
CONTRAST_FLOOR = 3.0      # WCAG non-text contrast against the chart surface

# Ramp thresholds.
RAMP_MIN_STEP = 0.05      # min OKLCH dL between neighbouring steps
RAMP_PALE_END_FLOOR = 2.0 # WCAG contrast of the step closest to the surface
RAMP_HUE_DRIFT = 45.0     # max OKLCH hue spread across the ramp, in degrees

DEFAULT_SURFACE = {"light": "#fbfaf9", "dark": "#141317"}

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied in linear RGB.
CVD_MATRIX = {
    "protan": ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}

HEX_RE = re.compile(r"\A#?[0-9a-fA-F]{6}\Z")

# Callers paste hex lists out of rendered tables and markdown, which can drag along
# non-breaking spaces and friends. Strip the whole Unicode space family.
_SPACE = (" \t\n\v\f\r         "
          "        　")


# --- colour maths -----------------------------------------------------------
def parse_hex(value: str) -> tuple[float, float, float]:
    digits = value.strip(_SPACE).lstrip("#")
    return tuple(int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def to_linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def linear_rgb(value: str) -> tuple[float, float, float]:
    r, g, b = parse_hex(value)
    return to_linear(r), to_linear(g), to_linear(b)


def luminance(value: str) -> float:
    r, g, b = linear_rgb(value)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def oklab(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = rgb
    # long / medium / short cone responses, then the cube root the space is built on
    long_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    med = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    short = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * long_ + 0.7936177850 * med - 0.0040720468 * short,
            1.9779984951 * long_ - 2.4285922050 * med + 0.4505937099 * short,
            0.0259040371 * long_ + 0.7827717662 * med - 0.8086757660 * short)


def oklch(value: str) -> tuple[float, float, float]:
    """Return (lightness, chroma, hue-in-degrees) for a hex colour."""
    lightness, a, b = oklab(linear_rgb(value))
    return lightness, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def simulate(value: str, kind: str) -> tuple[float, float, float]:
    rgb = linear_rgb(value)
    return tuple(  # type: ignore[return-value]
        min(1.0, max(0.0, sum(row[i] * rgb[i] for i in range(3))))
        for row in CVD_MATRIX[kind]
    )


def delta_e(a: str, b: str, kind: str | None = None) -> float:
    """OKLab distance x100. `kind=None` means ordinary colour vision."""
    left = oklab(simulate(a, kind) if kind else linear_rgb(a))
    right = oklab(simulate(b, kind) if kind else linear_rgb(b))
    return 100 * math.dist(left, right)


# --- checks -----------------------------------------------------------------
# Each check returns (name, state, detail). State is "pass", "warn", or "fail";
# only "fail" changes the exit code.
Check = tuple[str, str, str]


def pair_indices(count: int, pairs: str) -> list[tuple[int, int]]:
    """Which slot pairs can end up touching, given the chart form.

    Stacks, grouped bars and line charts only ever put *neighbouring* slots side
    by side, because slots are handed out in order and never skipped. Scatter,
    bubble, choropleth and small multiples can land any two marks together, so
    they need every pair checked.
    """
    if pairs == "all":
        return [(i, j) for i in range(count) for j in range(i + 1, count)]
    return [(i, i + 1) for i in range(count - 1)]


def check_categorical(palette: list[str], mode: str, surface: str, pairs: str) -> list[Check]:
    low, high = LIGHTNESS_BAND[mode]
    checks: list[Check] = []

    off_band = [(c, round(oklch(c)[0], 3)) for c in palette if not low <= oklch(c)[0] <= high]
    checks.append((
        "Lightness band", "pass" if not off_band else "fail",
        f"all {len(palette)} within L {low}-{high}" if not off_band
        else f"outside the band: {fmt_pairs(off_band)}",
    ))

    grey = [(c, round(oklch(c)[1], 3)) for c in palette if oklch(c)[1] < CHROMA_FLOOR]
    checks.append((
        "Chroma floor", "pass" if not grey else "fail",
        f"all {len(palette)} at or above C {CHROMA_FLOOR}" if not grey
        else f"reads grey: {fmt_pairs(grey)}",
    ))

    pairlist = pair_indices(len(palette), pairs)
    scope = "all-pairs" if pairs == "all" else "adjacent"

    worst_cvd = min(
        ((delta_e(palette[i], palette[j], kind), kind, palette[i], palette[j])
         for kind in ("protan", "deutan") for i, j in pairlist),
        default=None, key=lambda row: row[0],
    )
    if worst_cvd is None:
        checks.append(("CVD separation", "pass", "single colour, nothing to separate"))
    else:
        distance, kind, left, right = worst_cvd
        tritan = min(delta_e(palette[i], palette[j], "tritan") for i, j in pairlist)
        state = "pass" if distance >= CVD_TARGET else "warn" if distance >= CVD_FLOOR else "fail"
        checks.append((
            "CVD separation", state,
            f"worst {scope} pair {left} / {right} at dE {distance:.1f} ({kind}); "
            f"tritan {tritan:.1f}",
        ))

    worst_plain = min(
        ((delta_e(palette[i], palette[j]), palette[i], palette[j]) for i, j in pairlist),
        default=None, key=lambda row: row[0],
    )
    if worst_plain is None:
        checks.append(("Plain-sight gap", "pass", "single colour, nothing to separate"))
    else:
        distance, left, right = worst_plain
        passed = distance >= PLAIN_SIGHT_FLOOR
        checks.append((
            "Plain-sight gap", "pass" if passed else "fail",
            f"worst {scope} pair {left} / {right} at dE {distance:.1f}"
            + ("" if passed else
               f" - under {PLAIN_SIGHT_FLOOR:.0f}, so full-colour readers struggle too"),
        ))

    dim = [(c, round(contrast(c, surface), 2)) for c in palette
           if contrast(c, surface) < CONTRAST_FLOOR]
    checks.append((
        "Surface contrast", "pass" if not dim else "warn",
        f"all {len(palette)} at or above {CONTRAST_FLOOR:g}:1" if not dim
        else f"under {CONTRAST_FLOOR:g}:1, needs visible labels or a table view: {fmt_pairs(dim)}",
    ))

    return checks


def check_ramp(palette: list[str], mode: str, surface: str, ordinal: bool) -> list[Check]:
    """A magnitude ramp is judged as a ramp, not as a set of identities. A ramp is
    *supposed* to span the lightness band and to place its steps close together.

    The pale end is judged differently by usage. On a continuous heat scale, the
    palest step means "near zero" and is allowed to sink toward the surface.
    Discrete ordered marks have no such excuse, so `--ordinal` promotes the same
    measurement to a mandatory check.
    """
    checks: list[Check] = []
    lightness = [oklch(c)[0] for c in palette]

    order = sorted(range(len(lightness)), key=lightness.__getitem__)
    forward = list(range(len(lightness)))
    monotone = order in (forward, forward[::-1])
    checks.append((
        "Monotone lightness", "pass" if monotone else "fail",
        "steps run light to dark" if monotone
        else "steps are out of order: L " + ", ".join(f"{v:.3f}" for v in lightness),
    ))

    crowded = [(palette[i], palette[i + 1], round(abs(lightness[i + 1] - lightness[i]), 3))
               for i in range(len(palette) - 1)
               if abs(lightness[i + 1] - lightness[i]) < RAMP_MIN_STEP]
    checks.append((
        "Step separation", "pass" if not crowded else "fail",
        f"every gap at or above dL {RAMP_MIN_STEP}" if not crowded
        else "steps too close to tell apart: "
             + ", ".join(f"{a}/{b} dL {d}" for a, b, d in crowded),
    ))

    pale = max(palette, key=lambda c: oklch(c)[0]) if mode == "light" \
        else min(palette, key=lambda c: oklch(c)[0])
    ratio = contrast(pale, surface)
    if ratio >= RAMP_PALE_END_FLOOR:
        pale_state, note = "pass", ""
    elif ordinal:
        pale_state = "fail"
        note = f" - under the {RAMP_PALE_END_FLOOR:g}:1 floor, and an ordered mark must be visible"
    else:
        pale_state = "warn"
        note = (f" - under {RAMP_PALE_END_FLOOR:g}:1, so this step reads as empty surface; "
                "fine when it means near-zero on a heat scale, not for ordered marks")
    checks.append(("Pale end vs surface", pale_state, f"{pale} at {ratio:.2f}:1" + note))

    hues = [oklch(c)[2] for c in palette]
    spread = max(hues) - min(hues)
    if spread > 180:
        spread = 360 - spread
    checks.append((
        "Hue stability", "pass" if spread <= RAMP_HUE_DRIFT else "fail",
        f"hue spread {spread:.0f} degrees"
        + ("" if spread <= RAMP_HUE_DRIFT else " - too wide to read as one hue"),
    ))

    return checks


def fmt_pairs(rows: list[tuple[str, float]]) -> str:
    return ", ".join(f"{value} ({measure})" for value, measure in rows)


# --- entry point ------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a chart palette against measurable colour rules.")
    parser.add_argument("palette", help="comma-separated hex values, in slot order")
    parser.add_argument("--mode", choices=("light", "dark"), default="light",
                        help="which render mode the palette is stepped for")
    parser.add_argument("--surface", default=None,
                        help="chart surface hex; defaults to the mode's surface")
    parser.add_argument("--pairs", choices=("adjacent", "all"), default="adjacent",
                        help="adjacent for stacks/bars/lines (default); all for "
                             "scatter/bubble/map/small-multiples")
    parser.add_argument("--ramp", action="store_true",
                        help="validate as a magnitude ramp instead of identity colours")
    parser.add_argument("--ordinal", action="store_true",
                        help="ramp mode for discrete ordered marks")
    args = parser.parse_args()

    palette = [c for c in (part.strip(_SPACE) for part in args.palette.split(",")) if c]
    surface = (args.surface or "").strip(_SPACE) or DEFAULT_SURFACE[args.mode]
    if not palette:
        parser.error("no colours given")
    malformed = [c for c in (*palette, surface) if not HEX_RE.match(c)]
    if malformed:
        parser.error(f"not #rrggbb hex: {', '.join(malformed)}")

    if args.ramp or args.ordinal:
        checks = check_ramp(palette, args.mode, surface, args.ordinal)
        kind = "ordinal ramp" if args.ordinal else "ramp"
    else:
        checks = check_categorical(palette, args.mode, surface, args.pairs)
        kind = "categorical"
    print(f"\n{kind} palette, {args.mode} mode on {surface}: {len(palette)} colours")
    for name, state, detail in checks:
        print(f"  [{state.upper():4}] {name:20} {detail}")

    failed = [name for name, state, _ in checks if state == "fail"]
    if failed:
        print(f"\n  FAILED: {', '.join(failed)}\n")
        return 1
    warned = [name for name, state, _ in checks if state == "warn"]
    if warned:
        print(f"\n  PASSED with warnings: {', '.join(warned)}.")
        print("  A warning is legal only with its mitigation: a second encoding "
              "channel for CVD,\n  visible labels or a table view for contrast, "
              "or a near-zero meaning for a pale ramp end.\n")
    else:
        print("\n  PASSED.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

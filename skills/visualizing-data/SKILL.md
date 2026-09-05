---
name: visualizing-data
description: Use when producing any chart, graph, plot, dashboard, or data visualization in any medium - HTML/SVG, React, a plotting library (matplotlib, plotly, d3, Vega, Recharts), or a rendered image. Read before writing the first line of chart code, picking chart colours, or laying out a dashboard. Covers choosing a form, the house jewel-tone palette, mark specs, typography, interaction, and accessibility.
---

# Visualizing Data

## Overview

**Core principle:** a chart is read by a person and executed by you — and you cannot
see what you made. So nothing here is left to taste. The form is chosen by a rule, the
colours come from a fixed palette, and colourblind safety is *computed* by a script.

Everything in this skill is a house standard, not a suggestion. Use the palette as
given. Do not invent hues, do not "adapt" the ramps, and do not pick colours because
they look nice together.

**The habit that matters most: the colour part is arithmetic, so do the arithmetic.**
Never decide by eye whether two colours are far enough apart. Run
`scripts/validate_palette.py`.

---

## The procedure

Do these in order. Colour is step 3 for a reason — most bad charts start there.

1. **Pick the form.** Ask what the reader has to *do* with the data: compare
   magnitudes, tell series apart, judge a direction against a baseline, or read one
   headline number. That job picks the chart type — and often the answer is not a
   chart at all. → `references/choosing-a-form.md`

2. **Lay out the type.** Inter, with the house scale. Titles, labels, ticks and values
   each have a size and a weight already decided. → `references/typography.md`

3. **Assign colour by the job it does.** Identity, magnitude, polarity, or state —
   four jobs, one rule each. Categorical slots are handed out in fixed order, starting
   from amethyst, and never cycled. → `references/palette.md` and
   `references/colour.md`

4. **Validate, if you changed anything.** Using the house palette unmodified? It is
   already validated — skip ahead. Building a palette for someone else's brand, or
   adding a colour? Run the script and fix every FAIL before continuing:

   ```
   python3 scripts/validate_palette.py "#hex,#hex,…" --mode light --surface "#fbfaf9"
   ```

   Run it once per mode. → `references/colour.md` § Validating

5. **Draw the marks to spec.** Thin bars capped at 24px, 2px lines, 8px markers, a 2px
   surface gap between touching fills, hairline chrome, labels placed sparingly.
   → `references/marks.md`

6. **Add the hover layer.** An HTML or SVG chart is interactive; a crosshair and
   tooltip are part of the deliverable, not an enhancement. Only a bare stat tile is
   exempt. → `references/interaction.md`

7. **Make it readable without colour.** Two or more series always get a legend, four
   or fewer also get direct labels, every chart has a table view, and dark mode uses
   its own validated steps rather than an inverted filter.

8. **Render it and actually look at it.** The validator checks colour, not layout.
   Open the file or screenshot it, and look for collided labels, clipped text, and
   overflow before you call it done.

Then read `references/anti-patterns.md` and check your chart against it. If it matches
an entry, it is wrong.

---

## Non-negotiables

- **Amethyst is the primary.** One series, one accent, one highlighted line, one
  meter fill — it is `#7b36c1` (light) / `#aa6cf6` (dark) unless there is a stated
  reason otherwise.
- **Categorical slots are assigned in fixed order and never cycled.** A seventh series
  is not a new hue. It folds into "Other", becomes small multiples, or the chart
  changes form.
- **Never two y-axes on one plot.** Two scales aligned arbitrarily invent a
  correlation that is not in the data. Use two charts, small multiples, or index both
  series to a common base.
- **Colour follows the entity, not its rank.** Filtering a series out must not repaint
  the ones that remain.
- **Sequential is one hue, light to dark. Diverging is two opposed hues with a neutral
  grey midpoint.** Never a rainbow, never a hue at the midpoint.
- **Status colours are reserved.** Success, warning and danger mean exactly that. They
  are never "series 4", they are used sparingly, and they always carry an icon or a
  text label so the colour is not the only signal.
- **Text never wears the series colour.** Marks carry colour; labels, values, legends
  and ticks wear ink tokens. Identity comes from a coloured swatch *beside* the text.
- **Every value is reachable without hovering** — through a direct label, an axis, or
  the table view.

---

## Reference files

| File | What it answers |
|---|---|
| `references/choosing-a-form.md` | Which chart type — and is a chart even right? |
| `references/palette.md` | **The house palette.** Every colour, both modes, as tokens. |
| `references/colour.md` | The four jobs, the checks, how to validate and how to adapt |
| `references/typography.md` | Inter, the type scale, numerals, and how to load the font |
| `references/marks.md` | Mark specs, spacing, labels, legends, stat tiles |
| `references/interaction.md` | Tooltips, hover, filters, loading states |
| `references/anti-patterns.md` | **What goes wrong.** Check every chart against it. |

## Assets

| Path | What it is |
|---|---|
| `assets/swatches.html` | The reference sheet — open it to see every colour, the type scale, and worked examples of each chart form. Load it when you need to see the system rather than read it. |
| `assets/fonts/InterVariable.woff2` | Inter for the web. Also `InterVariable-Italic.woff2`. |
| `assets/fonts/InterVariable.ttf` | Inter for plotting libraries that need a font file (matplotlib, PIL, headless renderers). |
| `scripts/validate_palette.py` | The palette validator. Python 3, no dependencies. |

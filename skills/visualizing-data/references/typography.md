# Typography

**The brand typeface is Inter**, everywhere. Inter is a neutral grotesque with unusually good numerals and a large x-height, which
is what a chart needs. Inter stays legible at 11px on an axis and holds up at 48px on a hero figure without looking like two different fonts. It also includes OpenType features that can fix some specific ways numbers go wrong, such as tabular figures, a slashed zero, and a tailed lowercase `l`.

The font ships with this skill:

| File | For |
|---|---|
| `assets/fonts/InterVariable.woff2` | web — one file, every weight |
| `assets/fonts/InterVariable-Italic.woff2` | web italics, if needed |
| `assets/fonts/InterVariable.ttf` | matplotlib, PIL, headless renderers, anything that wants a font file |

## The scale

Sizes are absolute, not relative. A chart is a fixed composition.

| Role | Size / line-height | Weight | Tracking | Ink |
|---|---|---|---|---|
| Hero figure | 48 / 1.0 | 600 | −0.02em | primary |
| Stat-tile value | 30 / 1.1 | 600 | −0.015em | primary |
| Section heading | 20 / 1.3 | 600 | −0.01em | primary |
| Chart title | 16 / 1.4 | 600 | −0.005em | primary |
| Subtitle, caption | 13 / 1.45 | 400 | 0 | secondary |
| Legend, series label | 12 / 1.3 | 500 | 0 | secondary |
| Data label on a mark | 11 / 1.2 | 600 | 0 | primary |
| Axis tick | 11 / 1.2 | 400 | 0 | muted |
| Table cell | 12 / 1.5 | 400 | 0 | secondary |
| Footnote, source | 11 / 1.45 | 400 | 0 | muted |

The system has two core weights: **400** for anything the reader scans past, **600** for anything they are meant to stop on. 500 appears exactly once, on legend labels, where 400 would disappears next to a swatch but 600 would compete with the title.

## Working with Numerals

- **Columns of numbers get `tabular-nums`.** Table cells, axis ticks, tooltip values, and anything that stacks vertically and has to line up.
- **Large standalone numbers do not.** Tabular figures give every digit the width of a zero, which makes `121` look gappy at 48px. Hero figures and stat-tile values should use the default proportional figures.
- **Add `slashed-zero` wherever a zero could be read as an O:** identifiers, codes, and dense tables.
- Compact large values rather than printing every digit: `1,284`, `12.9K`, `$4.2M`. Full precision belongs in the tooltip and the table.

```css
.viz-table td, .viz-axis text { font-variant-numeric: tabular-nums slashed-zero; }
.viz-hero, .viz-stat-value  { font-variant-numeric: proportional-nums; }
```

Optionally add `font-feature-settings: "cv05" 1` to distinguish lowercase `l` from `1` in dense labels. It is a real improvement in tables of identifiers, but unnecessary anywhere else.

## Loading it

Self-host from the bundled file. One `@font-face` covers every weight.

```css
@font-face {
  font-family: "Inter";
  src: url("./fonts/InterVariable.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

.viz {
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-synthesis-weight: none;
}
```

The fallback stack ensures that if the file cannot load, the chart falls back to a system grotesque with similar metrics. `font-synthesis-weight: none` stops the browser faking a bold when the variable axis already has one.

For plotting libraries, point them at the `.ttf`:

```python
from matplotlib import font_manager
font_manager.fontManager.addfont("assets/fonts/InterVariable.ttf")
plt.rcParams["font.family"] = "Inter"
```

## In an artifact or a sandbox

Where the bundled file cannot be reached, load Inter from Google Fonts instead, keep the same fallback stack, and change nothing else. The scale, weights and numeral rules are all independent of how the font arrives.

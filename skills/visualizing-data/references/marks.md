# Marks and anatomy

For a data visualization, the considered look is a handful of fixed specs plus two pieces of negative space. The data is the only thing allowed to be loud.

## Mark specs

| Mark | Spec |
|---|---|
| Bar / column | **At most 24px thick.** Cap it. Never let a bar fill its band; the leftover negative space lets the chart breathe. **4px rounded at the data end, square at the baseline.** Grows from one baseline. |
| Line | **2px**, round joins and caps. |
| Marker, end dot | **At least 8px across** (r ≥ 4), filled with the series colour. |
| Area fill | The series hue at **~10% opacity.** |
| Gridline, axis | **1px solid hairline**, one step off the surface, recessed. Never dashed. |

Rounding only the data end of bars is important. The rounded end says "this is where the value stops". The square end says "this is where zero is". If both ends were rounded, the bar would look like it floats away from its baseline.

Adjacent marks of the same type should all be the same width.

## Spacers

**Surface gap.** A **2px gap in the surface colour** separates touching fills: every segment of a stacked bar, every pair of adjacent bars, etc. Neighbouring slots read as distinct because of the gap, not because of an outline.

**Surface ring.** Dots and end markers have a **2px ring in the surface colour**, so they remain legible even when crossing a line or overlapping each other. The ring is part of the hover target too, not just spacing.

Never draw a border around a mark to separate it from its neighbour. A stroke adds ink but illuminates no data. At small sizes, it eats the mark it was meant to clarify.

## Labels and legends

**Two or more series need a legend or a direct identity label on every series.** Never make a reader match colours from memory. Direct end labels may replace the legend when every series can be labelled clearly without collisions; otherwise use a legend. **One series gets no legend.** A box with a single swatch would uselessly repeat the title.

Direct labels must be sparing:

- **Never a value on every point.** A number beside every dot or segment is noise and goes unread. Label the endpoint, the extreme, or the one series the chart is about. Let the axis, the legend and the tooltip carry the rest.
- **Direct labels before gridlines. Gridlines before a second axis.** And there is never a second axis.
- **Measure before placing a label inside a mark.** A label only goes inside a bar or segment when the rendered text fits with padding on both sides. If it does not fit, move it outside the bar's end. For an interior stacked segment, which has no free end, drop it and let the legend and tooltip carry the value. Never apply `overflow: hidden`. Clipping the first or last character of a. label is messy and confusing.
- Bar labels are at the tip, columns on the cap, lines at the end.
- Keep axis ticks on round numbers, comma-grouped.

**Text never uses a series colour.** Marks use colour; labels, values, legends and ticks use ink tokens. Identity comes from a small coloured swatch *beside* the text: a dot for scatter, a short stroke for lines, a rect for bars and areas. The one exception is a label sitting inside a filled shape. This should use white or ink chosen by the fill's luminance.

**When end labels collide, do not nudge them apart.** Shifting a label off its line detaches it and reads as noise. Use a thin leader line, facet into small multiples, or fall back to the legend and tooltip. Past about four converging lines, small multiples
is almost always the answer.

**Series names are untrusted input.** They arrive from CSV headers, API responses and tool output. Put them into the DOM with `textContent`, never by concatenating into `innerHTML`.

## Figures: when the form is a number

**Stat tile.** Four parts:

- `label` (sentence case, no trailing colon)
- `value` (600 weight, compacted: `1,284` / `12.9K` / `$4.2M`)
- `delta` (optional; signed, against a named period, status coloured by *direction × whether up is good*)
- `trend` (optional; a sparkline in de-emphasis grey with the current period in amethyst).

The delta's colour is one place a status colour should be used in a figure. It still needs its arrow and its period label, both for accessibiliy, and because "+12% vs last week" is the information, not just "it increased".

**Meter.** The fill represents the state. The unfilled track is a **lighter step of the same ramp**, so the whole bar reads as a unified scale rather than a coloured bit and an empty bit.

**Hero figure.** A single number that a page leads with. 48px, Inter, proportional figures, exactly one per view. If there are two, neither is the hero.

## Containers

A chart lives in a `<figure>` or a card that owns its sizing, its title and caption, and its table-view toggle.

**Any fixed height has to include the axis band.** Always use plot height plus the space the x-axis labels need. Sizing the container to the plot alone gives the card a tiny nested scrollbar, which is a common layout bug in generated charts. Better still, let the container grow with its content.

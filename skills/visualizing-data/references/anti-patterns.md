# Anti-patterns

Check every chart against this list before calling it done. If the output matches an entry, it is wrong and must be fixed.

## Colour and encoding

**❌ Two incomparable y-axes on one plot.**
The alignment between the two scales is arbitrary, so the chart invents a correlation that is not in the data. Reviewers often describe these charts as looking made up. They are correct.
✅ Two charts, small multiples, or index both series to a common base (= 100 at t₀) on one axis.

**❌ Recolouring on filter.**
Don't reassign colours by current rank, for example so that filtering one series out repaints the survivors. A reader who learned that Acme is amethyst is now misled.
✅ Colour tracks the entity, not the row number.

**❌ A seventh categorical colour.**
Don't generate new colours, don't borrow from status, and don't cycled back to slot 1. With this palette, under simulated CVD, any further generated hue would be indistinguishable from a slot that already exists.
✅ Fold the tail into "Other", facet, or switch to a table.

**❌ Deciding colourblind safety by eye.** "These look different enough."
✅ `python3 scripts/validate_palette.py <flags>`. Adjacent ΔE ≥ 8, or 6–8 with a second encoding channel.

**❌ Colouring nominal bars by their value.**
Don't make bars darker where bigger, when the categories have no natural order. It re-encodes bar length as hue, which wastes a free channel on information the chart already shows. It also fails the categorical checks.
✅ One series, one colour, slot 1 for every bar. Genuinely ordered categories take the ordinal ramp.

**❌ A rainbow, or any multi-hue sequential ramp.**
✅ One hue, pale to deep.

**❌ A hue at the diverging midpoint, or two cool hues as the two poles.**
The midpoint has to read as *nothing*. The poles have to read as opposites. Amethyst against sapphire fails: both cool. Topaz against sapphire works.
✅ Warm against cool, neutral grey between.

**❌ A status colour used for a series, or a series colour used for status.**
✅ Status when the colour *means* good or bad; categorical when it means identity. Never both in one chart.

**❌ A palette with a green and a red in it, for categories that are just categories.**
Readers see pass/fail before they read the legend.
✅ The house palette has no red for exactly this reason. Do not add one.

## Form

**❌ Six categorical colours when the story is one number.**
✅ Emphasis: one series in amethyst, the rest grey. Or a stat tile.

**❌ A one-bar bar chart, or a two-slice pie.**
✅ A stat tile. The number is the figure.

**❌ A donut or pie for comparing values that are close.**
✅ A bar, or just the numbers. Avoid pie charts.

**❌ More than about seven colour classes carrying meaning.**
✅ A table, or a table beside a chart. Past seven, adjacent classes blur.

## Marks and chrome

**❌ Thick saturated blocks, heavy gridlines, no breathing room.**
✅ Thin marks, hairline recessive chrome, generous padding. Saturated fills belong on small marks and accents, never on large blocks.

**❌ Dashed gridlines or axis rules.**
Dashing reads as "projection" or "threshold".
✅ Solid 1px hairlines, one step off the surface.

**❌ A number on every data point.**
✅ A legend or direct identity label for every series. Direct value labels only on the endpoint, the extreme, or the series the chart is about.

**❌ A border drawn around marks to separate them.**
✅ The 2px surface gap between fills, and the 2px surface ring on overlapping markers.

**❌ A label clipped by its own mark.**
This includes `overflow: hidden` cropping the ends of an in-segment label, which must be avoided.
✅ Only place a label inside a mark when it measurably fits. Otherwise, put it outside the bar end, or drop it to the tooltip. The value should be in the table view either way.

**❌ A container whose fixed height excludes the axis band.**
This causes the card to grow an unwanted nested scrollbar.
✅ Size for plot plus axis labels, or let the container grow with its content.

**❌ A display or serif face on the hero figure.**
✅ Inter, like everything else.

**❌ `tabular-nums` on a large standalone number.**
This can make figures look gappy.
✅ Proportional figures on hero and stat values. Tabular only where numbers stack.

**❌ Dark mode produced by inverting the light palette.**
✅ The dark column, which is a separately chosen and separately validated set of steps.

**❌ Texture on by default, or as decoration.**
Dense, high-contrast stripes read as noise, cause visual stres, and are a documented trigger for pattern-sensitive epilepsy.
✅ Texture is opt-in, for accessibility setting, print, and `forced-colors` only. Draw it tone-on-tone at coarse spacing. Use it at 45° and 135° only. Order it when it sits on a value scale.

## Interaction and accessibility

**❌ A value that can only be read by hovering.**
✅ Tooltips enhance, never gate. Direct labels or the table view display every value. Keyboard focus shows the same thing that hover shows.

**❌ Pinpoint hover targets**
✅ At least a 24px hit area; a nearest-point layer for dense scatter.

**❌ Per-chart filters, or filters inside a chart card.**
✅ One filter row above everything it scopes.

**❌ A skeleton flash on refetch.**
✅ Hold the previous render at reduced opacity.

**❌ No table view, or colour as the only encoding on a continuous scale.**
✅ Every chart has a table-view twin.

**❌ Series names inserted with `innerHTML`.**
They are untrusted data, that comes from CSV headers and API responses.
✅ `textContent`.

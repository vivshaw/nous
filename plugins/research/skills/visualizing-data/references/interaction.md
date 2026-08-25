# Interaction

An HTML or SVG chart should be interactive. The hover layer is part of the deliverable. The only form that ships without one is a bare stat tile with no plot.

## Tooltips and hover

**Tooltips enhance; they never gate.** Every value a tooltip shows is reachable without a pointer, through a direct label, an axis, or the table view. Keyboard focus shows exactly what hover shows.

- **On line and area charts, a crosshair tracks the X.** A vertical hairline tracks the pointer and snaps to the nearest data position. Readers aim at a date, not at a 2px line.
- **On bars and cells, the mark is the target.** No crosshair. Each bar, segment, dot or heat cell has its own tooltip, and the hovered mark visibly responds with a slight lift or lightening.
- **One tooltip lists every series at that X.** The pointer should never have to land on a particular line to get its number.
- **The value leads, the label follows.** In a tooltip the number is the strong, high-contrast element and the series name is secondary. This is the inverse of a legend, because here the reader already knows which series they are asking about.
- **Key series with a short stroke, not a filled box.** At tooltip density, a solid swatch is heavy colour doing a label's job. Legends should still mirror the mark: a rect for bars and areas, a line for lines, a dot for scatter.
- **The hit target is bigger than the mark.** It includes the 2px surface gap and then some: at least 24px. An 8px scatter dot is an inaccessibly small pinpoint. For dense scatter, use a nearest-point layer so the pointer only has to be *closest*.
- **A value that would not fit on its mark lives in the tooltip.** It stays in the table view, so it's never gated behind a hover.

## Filters and time ranges

Filters are ordinary form controls, not chart marks. Build them with plain HTML styled to match the chart chrome. How to position them:

- **One row, above everything they scope.** Never inside a chart card, never per chart. If one chart needs its own range, it belongs on a different page.
- **Date range first.** This is the most common control readers would reach for. Offer context-relevant presets: today, last 7 / 30 / 90 days, month to date. Put them before a custom range. Nobody wants to fight a calendar grid to say "last 30 days".
- **Filters scope everything below them.** Every chart, stat and table should re-render against the same slice and the numbers should always agree.
- **Refetch keeps the frame.** While data reloads, charts hold their previous render at reduced opacity. No skeleton, no layout jump, no flash.

## The table view

Every chart has one. This is the reason the rest of the rules can stay relaxed. It is a plain `<table>` with the same numbers, reachable from a toggle on the figure. This makes each chart usable with a screen reader, with a printer, with `forced-colors`, or by anyone who just wants the actual figures. Build it from the same data array that drew the chart, so the two cannot drift.

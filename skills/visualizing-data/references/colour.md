# Colour

Colour in a chart is not decoration and is not chosen. Every colour does exactly one of five jobs, and each job has rules.

## Five jobs for colour

| Job | Encodes | Structure |
|---|---|---|
| **Categorical** | Identity: which series | Six hues, fixed order, assigned in sequence, never cycled |
| **Ordinal** | Position in an order: stage, tier, band | One hue, stepped, every step visible against the surface |
| **Sequential** | Magnitude: how much | One hue, pale to deep; the pale end may recede |
| **Diverging** | Polarity: which side of a baseline | Two opposed hues, neutral grey midpoint, matched arms |
| **Status** | State: success, warning, danger | A small reserved set, always with an icon or a word |

Choosing accurately between categorical and ordinal is important. **Would reordering the categories change the meaning?** If yes, it is ordinal and takes a ramp. If no, it is nominal and takes identity colours. Or, when there is only one series, takes slot 1 for every bar.

Never colour nominal bars by their own value. Bar length already shows the value. Spending the colour channel on it too buys nothing while costing a free channel the chart could have.

## The checks

> The house palette clears the target in all modes, so none of these checks are needed for a chart that uses it as documented! This only matters when updating the house palette, or adapting the method to another brand's colours.

There are two sets, because identity colours and magnitude colours fail in different ways.

### Categorical checks

A categorical palette is legal only if it passes all of these. Five are computed by the validator. Two are structural and are enforced by following this document.

1. **Fixed order:** *(structural)* Six hues in the documented sequence. The order determines which pairs touch, which is what makes the palette colourblind-safe. Do not change the order.
2. **Lightness band:** *(computed)* OKLCH L within the band for the mode. Outside it, a mark either burns or disappears.
3. **Chroma floor:** *(computed)* OKLCH C at or above 0.06. Below that, a hue reads as grey and loses its identity.
4. **CVD separation:** *(computed)* OKLab ΔE ×100 between colours that can touch, under simulated protanopia and deuteranopia. Target 8, floor 6. The 6–8 band is legal **only** alongside a second encoding channel.
5. **Plain-sight separation:** *(computed)* The same distance under ordinary colour vision, floor 15. **Mandatory.** A second encoding channel does not excuse it. If full-colour readers cannot tell two neighbours apart, the palette is broken.
6. **Surface contrast:** *(computed)* At least 3:1 against the chart surface, so a mark is visually distinguishable. Below that is a WARN, legal only where the values are readable another way, such as visible labels or a table view.
7. **Documented values only:** *(structural)* Every colour is a hex from `palette.md`. No eyeballed values, no near-misses.

#### Which pairs get separation checked

Slots are handed out in order and never skipped. In a stack, a grouped bar, or a set of lines, only **neighbouring** slots can end up side by side. That is the default.

But scatter, bubble, choropleth and small multiples can place **any** two marks together, so they need every pair checked. This is a much harder test, and it applies a cap to the number of series those forms can carry. Right now, only up to 3 series can be used.

### Ramp checks

A ramp carries magnitude, so it is judged as a ramp rather than as a set of individual identities. Four checks are computed, one is structural.

1. **Monotone lightness:** Steps run light to dark without reversing.
2. **Step separation:** Neighbouring steps differ by at least OKLCH ΔL 0.05, so a reader can tell each band from the next.
3. **Pale end vs surface:** The step nearest the surface clears 2:1. For a continuous scale, this is a WARN, since the palest step means "near zero" and may properly recede into the surface. For an ordinal scale, it is a hard FAIL, as every funnel stage or tier is a mark somebody has to see.
4. **Hue stability:** The hue spread across the ramp stays within 45°. Wider than that, it would no longer be one hue anymore.

## Validating

```
python3 scripts/validate_palette.py "#7b36c1,#00848f,#a37300" \
    --mode light --surface "#fbfaf9"
```

Once per mode. Add `--pairs all` for scatter, bubble, maps and small multiples.

- Exit 0 means nothing hard-failed.
- **FAIL** must be fixed before shipping.
- **WARN** is legal only with its stated mitigation: a second encoding channel for a CVD distance in the 6–8 band, visible labels or a table view for sub-3:1 contrast.

For a magnitude ramp, use `--ramp`, which runs the ramp checks above instead of the categorical ones. Add `--ordinal` for discrete ordered marks, which promotes the pale-end check from a warning to a hard gate.

**Running the categorical checks on a ramp will fail it, correctly and uselessly.** A ramp is supposed to span the lightness band and put its steps close together. Do not "fix" a good ramp to satisfy the wrong checks.

The validator judges colour only. It says nothing about whether the chart is the right form, whether labels collide, or whether the layout overflows. Render the thing and look at it.

### Single status or text colours

For one status colour or one text colour, the question is WCAG text contrast. This should be 4.5:1 for normal text, and 3:1 for large. The validator's `contrast()` function may be used to check this this.

## Second encoding channels

When a CVD distance is within in the 6–8 band, colour needs help. Any of these are adequate:

- **Direct labels** on the marks
- **The 2px surface gap** between touching fills, which separates by shape
- **Texture** such as one directional hatch at 45° and its 135° mirror

Texture is only for accessibility, print and `forced-colors`. Never for decoration, and never on by default. Also, never horizontal or vertical, which read as gridlines. On a value scale, the hatch must be *ordered* with the value, or else it would contradict the colour.

**Draw it tone-on-tone and coarse:** a darker step of the fill's own hue, never black on colour, with enough spacing that the stripes read as separate lines rather than a shimmering field. Contrast is what makes a repeating pattern harmful — dense, high-contrast stripes cause visual stress and are a documented trigger for pattern-sensitive epilepsy. Keeping the hatch low-contrast is what makes this channel safe to hand somebody who needs it.

## Dark mode

Dark mode uses the dark column of the palette. It is a **selected** set of steps, not a computed one. Never invert the light theme, never `filter: invert()`, never darken the light values. A jewel tone stepped for white goes muddy on black. That is why there are two distinct themes.

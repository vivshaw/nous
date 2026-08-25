# The house palette

Jewel tones: deep, saturated, rich. Amethyst leads.

Every value here has been through `scripts/validate_palette.py`. **Use them as given.** Do not round them, re-pick them, or generate new ones.

There is a light and dark mode. The dark mode is based on the same six hues, but re-stepped for a dark surface. Never invert or filter the light values.

---

## Categorical colours: identity

Six slots. Hand them out **in this order**, starting at slot 1, never skipping and never cycling back to the start.

| Slot | Name | Light | Dark | Reads as |
|---|---|---|---|---|
| 1 | **amethyst** | `#7b36c1` | `#aa6cf6` | deep violet — **the primary** |
| 2 | **tourmaline** | `#00848f` | `#0bb6c5` | deep teal |
| 3 | **topaz** | `#a37300` | `#d89b07` | amber gold |
| 4 | **rubellite** | `#ae1387` | `#e851b9` | magenta |
| 5 | **sapphire** | `#0462d3` | `#5097ff` | true blue |
| 6 | **emerald** | `#008455` | `#23ba7d` | deep green |

**When only one colour is needed, it is amethyst.** A single-series line, a highlighted bar, a meter fill, a sparkline, an accent: use slot 1, every time.

### There is no red, and that is deliberate

A palette with a green and a red in it encodes pass/fail whether you meant it to or not. Readers see colour before they read the legend, and this quietly misreports any chart where the categories are just *categories*.

### Accessibility stats

Both modes, on the *adjacent* pairlist: the pairs that can actually touch in a stack, grouped bar, or set of lines, since slots are handed out in order:

| | Light | Dark |
|---|---|---|
| Worst adjacent pair, simulated protanopia/deuteranopia | ΔE **14.1** | ΔE **12.5** |
| Worst adjacent pair, ordinary colour vision | ΔE **19.6** | ΔE **24.1** |
| Lowest contrast against the surface | **4.02:1** (topaz) | **5.45:1** (amethyst) |

Every slot clears 3:1 against its surface in both modes, so no chart needs a contrast mitigation. (ΔE is OKLab distance ×100; the target is 8, the floor is 6.)

### The scatter cap: three series

Stacks, bars and lines only ever put *neighbouring* slots side by side. Scatter, bubble, choropleth and small multiples can put **any** two marks together, which is a much harder test. This palette supports three series in those forms:

| First three slots, all pairs | Light | Dark |
|---|---|---|
| Simulated protanopia/deuteranopia | ΔE 14.2 | ΔE 12.5 |
| Ordinary colour vision | ΔE 19.6 | ΔE 24.1 |

No four-slot subset clears the floors in both modes. **A scatter plot with four categories needs fewer categories or facets, not more colours.** Validate these forms with `--pairs all`.

### Past six series

There is no slot 7. Fold the tail into "Other" (in the de-emphasis grey), facet into small multiples, or change form. Generating a seventh hue produces a colour that is indistinguishable from an existing slot under simulated CVD.

---

## Sequential colours: magnitude

One hue, pale to deep. **The default is amethyst.** Step 600 (light) and step 500 (dark) are the categorical slot-1 value, so a heatmap and a bar chart on the same dashboard agree with each other.

**Amethyst, light mode** (on a light surface, more is *darker*):

| 100 | 200 | 300 | 400 | 500 | 600 | 700 |
|---|---|---|---|---|---|---|
| `#f2eaff` | `#e0cdfe` | `#c2a2f3` | `#af7fef` | `#9654e0` | `#7b36c1` | `#5a2391` |

**Amethyst, dark mode** (on a dark surface, more is *brighter*):

| 100 | 200 | 300 | 400 | 500 | 600 | 700 |
|---|---|---|---|---|---|---|
| `#362151` | `#5c3589` | `#713bad` | `#904ed9` | `#aa6cf6` | `#c095fd` | `#d8c1fe` |

When a single view needs two independent magnitude scales, the second takes the next slot's hue, **tourmaline**:

| mode | 100 | 200 | 300 | 400 | 500 | 600 | 700 |
|---|---|---|---|---|---|---|---|
| light | `#e6f1f2` | `#afe2e8` | `#63c9d4` | `#32b1be` | `#079ba8` | `#00848f` | `#1f666d` |
| dark | `#223739` | `#26555a` | `#20737b` | `#0d94a0` | `#0bb6c5` | `#36d1e0` | `#8ee5ef` |

Do not add a third sequential colour. Two heat scales in one view is already a lot to ask.

### Sequential versus ordinal

The full range is for continuous magnitude, such as heat cells or choropleths. In these, the faintest step means "near zero", so it is allowed to sink into the surface.

A limited range is used from ordered discrete marks, such aa funnel stages, size tiers, or age bands. These are all marks a reader has to see, so they start further in:

| ramp | light starts at | dark starts at |
|---|---|---|
| amethyst | step **300** (2.06:1) | step **200** (2.05:1) |
| tourmaline | step **400** (2.47:1) | step **200** (2.23:1) |

Validate an ordered set with `--ordinal`.

---

## Diverging colours: polarity

**Topaz ↔ sapphire.** Warm against cool, which makes the two ends read as opposites, and a neutral grey midpoint that reads as *nothing happening*. Nine classes, four per arm, matched lightness across the two arms.

**Light:* extremes carry the most ink, the midpoint is nearly the surface:

`#6c4c04` · `#936907` · `#b88930` · `#d9b06a` · **`#e8e7eb`** · `#9cb9e4` · `#5191f0` · `#076be3` · `#034da8`

**Dark:** extremes are brightest, the midpoint recedes:

`#d4aa61` · `#b1832a` · `#8c6307` · `#654703` · **`#2e2d31`** · `#03489e` · `#0665d8` · `#438af2` · `#91b3e5`

The two classes either side of the light-mode midpoint sit just under 2:1 (1.94 and 1.92). That is correct, as they mean "barely off the baseline". But it makes a scale legend mandatory, and those classes must never be the only place a value appears.

Never put a hue at the midpoint, and never use two cool hues as the two poles. Amethyst and sapphire would fail this: both cool, so neither end reads as the opposite of the other.

---

## Status colours: state

**Not drawn from the jewel palette, and used sparingly.** A status colour is never used as a chart's main colour. It may only be used for small things like a dot, an arrow, a threshold rule, or a badge.

| Role | Light | Dark | Light contrast | Dark contrast |
|---|---|---|---|---|
| success | `#128737` | `#2dbe56` | 4.43:1 | 7.59:1 |
| warning | `#be7c06` | `#f5a41e` | 3.32:1 | 8.99:1 |
| danger | `#ce1c20` | `#f6584e` | 5.29:1 | 5.66:1 |

**Always use status colours with an icon or a word.** Colour alone never carries the state.

### The collision, stated plainly

Status colours have to _look_ like status colours. A success green that is not green fails at the only job it has. That leaves two measured proximities:

| Pair | Light ΔE | Dark ΔE |
|---|---|---|
| success ↔ emerald (slot 6) | 4.1 | 5.1 |
| warning ↔ topaz (slot 3) | 5.5 | 5.6 |
| danger ↔ rubellite (slot 4) | 16.5 | 15.8 |

Danger is comfortably clear of everything. Success and warning are not, and no repositioning fixes that without wrecking their meaning. For this readson, you must rely on **role separation**: status always appears as a small mark with a label beside text, series appear as large fills in a plot. If a chart genuinely needs both in the same visual role, drop emerald and topaz from its series and use the later slots.

When a series *means* good or bad, such as an error rate or a pass count, it uses status colours and gives up its categorical slot. It never uses both.

---

## Chrome and ink

| Role | Light | Dark | Used for |
|---|---|---|---|
| chart surface | `#fbfaf9` | `#141317` | the plot background |
| page plane | `#f7f6f9` | `#09080b` | the page behind the cards |
| ink, primary | `#1c191f` | `#f4f3f6` | titles, values, hero figures |
| ink, secondary | `#59575d` | `#b2b0b5` | subtitles, legend text, captions |
| ink, muted | `#757378` | `#86838a` | axis ticks, footnotes |
| gridline | `#e3e2e6` | `#262429` | hairline grid, 1px solid |
| axis / baseline | `#bebdc1` | `#434147` | the zero line and axis rules |
| de-emphasis | `#8d8b8f` | `#706d74` | greyed-out series, "Other" |
| hairline border | `rgba(28,25,31,0.10)` | `rgba(244,243,246,0.10)` | card edges |

The greys carry a trace of the amethyst hue rather than being pure neutral. This helps the chrome sit under the jewel tones instead of beside them.

Muted ink clears 4.5:1 in both modes, because axis ticks are small text and small text is text. De-emphasis clears 3:1 in both modes, because a greyed-out series is still a mark somebody has to see.

---

## As CSS tokens

Declare the roles the chart uses, then write the chart against role names. Dark values go in **both** scopes. The media query handles the OS setting, the attribute selector handles an explicit toggle, and the toggle has to win in both directions.

```css
.viz {
  color-scheme: light;
  --viz-surface:    #fbfaf9;
  --viz-ink:        #1c191f;
  --viz-ink-2:      #59575d;
  --viz-ink-muted:  #757378;
  --viz-grid:       #e3e2e6;
  --viz-axis:       #bebdc1;
  --viz-mute:       #8d8b8f;
  --viz-1: #7b36c1;  /* amethyst (primary) */
  --viz-2: #00848f;  /* tourmaline */
  --viz-3: #a37300;  /* topaz */
  --viz-4: #ae1387;  /* rubellite */
  --viz-5: #0462d3;  /* sapphire */
  --viz-6: #008455;  /* emerald */
}

@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .viz { /* …dark values… */ }
}
:root[data-theme="dark"] .viz { /* …the same dark values… */ }
```

`assets/swatches.html` is a working example of exactly this, with every token declared. Copy its `<style>` block rather than retyping the hexes.

---

## Adapting this to somebody else's brand

Even if the palette is not used, the method should be. Given a different set of ramps:

1. For each slot, take the step whose OKLCH lightness sits in the mode's band and whose chroma clears the floor.
2. Run the validator on **candidate orderings**, not just one. Slot order is a colourblind-safety mechanism. It decides which pairs ever touch.
3. Keep only orderings that clear every gate in both modes, then choose among those on looks.
4. For any adjacent pair under the target, hold its hue constant and move one slot a step lighter or darker. Re-run.

This is how the palette above was developed.

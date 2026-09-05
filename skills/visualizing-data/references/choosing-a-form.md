# Choosing a form

Decide this **before** colour. The reader's job picks the form. Often, the right form isn't a chart.

## Is it even a chart?

| The data is... | Use | Not |
|---|---|---|
| One current value, maybe with a trend | **Stat tile:** value, delta, sparkline | A one-bar bar chart |
| A handful of headline numbers | **KPI row** of stat tiles | A grouped bar chart |
| The one number the page leads with | **Hero figure**, 48px | Anything smaller |
| One ratio against a limit | **Meter** on a same-hue track | A two-slice pie |
| More than about seven meaningful classes | **A table**, or a table beside a chart | More colours |

Do not create a chart only because a chart was expected. If the answer is one number, write the number.

## The job picks the type

| What the reader has to do | Form | Colour job |
|---|---|---|
| Compare magnitudes | Bar or column; heatmap for a grid | Sequential |
| Follow a trend over time | Line; area for a single series | Sequential, or one categorical hue |
| Tell distinct series apart | Grouped or stacked bar, multi-line | Categorical |
| Notice that *one* series matters | **Emphasis:** one in amethyst, the rest grey | Slot 1 plus de-emphasis |
| Judge direction against a baseline | Diverging bar, or a line against a reference | Diverging |
| See parts of a whole | Stacked bar; go horizontal when names are long | Categorical |
| Read an ordered scale (Likert, sentiment) | Diverging stacked bar, centred on neutral | Diverging |
| Compare before and after, per item | Dumbbell | One hue, two steps |

## The reasoning

**Sequential is the safe default.** One hue, darker means more. It is hard to misread and it never accidentally implies that two categories are unrelated. Reach for categorical only when identity genuinely is the point.

**Categorical has a cost.** Six equally loud colours say "all of these matter equally". If one series is the story, categorical actively buries it.

**Emphasis is under-used.** One series in amethyst, everything else in the de-emphasis grey, the important one directly labelled. When someone says a chart is cluttered, this is often the fix.

**Ordinal is not categorical.** If reordering the categories would change the meaning, such as funnel stages, size tiers, age bands, or quartiles, then the order is information. It belongs in a one-hue ramp so the reader sees the order in the colour. Product names,
teams and regions are nominal. Reordering them loses nothing, so they get identity colours, or a single colour if there is only one series.

## How many series

| Series | What to do |
|---|---|
| 1 | Slot 1, amethyst. No legend — the title says what it is. |
| 2–3 | comfortable everywhere, including scatter and maps. Directly label. |
| 4–6 | Fine for stacks, bars and lines. Legend always; direct labels help. **Not** for scatter, bubble, choropleth or small multiples, which cap at three. |
| 7+ | There is no seventh colour. Fold the tail into "Other", facet into small multiples, or switch to a table. |

Never answer "too many series" by making another colour.

# PLOT RULES

Use this file whenever creating charts, graphics, or a visual report. Keep the output simple, dark, readable, and consistent.

## 1. The basic rule

Every chart must make one relationship easier to understand.

Do not add a chart for decoration. Do not add cards, icons, gradients, or extra layout elements just to make the page look busy.

Before making a chart, answer:

1. What question does this chart answer?
2. What data supports it?
3. What should the reader notice?
4. What could the chart make someone misunderstand?

If these questions cannot be answered, do not make the chart.

## 2. Page layout

- Use a pure-black page background.
- Center the report in a normal reading column.
- Use a maximum report width of approximately `1120–1200px`.
- Keep paragraphs narrower, around `70–80ch`.
- Make every chart fill the report column.
- Put exactly one chart, image, diagram, or major table per row.
- Never use side-by-side charts.
- Never use thumbnail grids, chart galleries, contact sheets, or dashboard tiles.
- Use generous vertical space between charts.
- Allow a dense chart to open in a near-full-screen inspection view.

The chart should be large inside a centered report. Do not stretch the entire report across an ultrawide monitor.

## 3. Required chart structure

Every important chart must contain these elements in this order:

### Question

State what the chart is trying to answer.

### Neutral title

Say what is plotted. Do not put the conclusion in the title.

Good:

> Net return by month and strategy

Bad:

> This strategy is amazing

### Subtitle

State the population, date range, sample size, units, filters, and important assumptions.

### How to read it

Briefly explain the axes, colors, marks, baseline, and uncertainty.

### Chart

Render the chart at full report-column width with readable labels.

### What it shows

Explain the actual pattern, magnitude, and important exceptions.

### Why it matters

Explain what decision or understanding changes because of the chart.

### Limitation

State what the chart does not establish or where it could mislead.

### Source

Name the exact source file or dataset used to create the chart.

## 4. Colors

Use this fixed meaning everywhere:

| Meaning | Color |
|---|---|
| Positive or favorable magnitude | Blue `#38bdf8` |
| Negative or adverse magnitude | Red `#ef4444` |
| Warning, fragile, or near a threshold | Orange `#f97316` |
| Neutral, missing, unsupported, or reference | Grey |
| Pass status only | Green `#58c978` |

Rules:

- Keep the same series the same color in every chart.
- Never rely on color alone. Also use signs, labels, shapes, line styles, or position.
- Never use rainbow palettes.
- Never use random chart-library colors.
- Use at most two bright colors in an ordinary chart.
- Reserve saturated color for the data, not headings or containers.
- Missing data must look different from zero.

## 5. Black visual system

Use these defaults:

```css
:root {
  color-scheme: dark;
  --canvas: #000000;
  --surface: #080808;
  --surface-2: #101010;
  --text: #f2f2f2;
  --muted: #b8b8b8;
  --faint: #8f8f8f;
  --line: rgba(255, 255, 255, 0.10);
  --gridline: rgba(255, 255, 255, 0.09);
  --blue: #38bdf8;
  --red: #ef4444;
  --orange: #f97316;
  --green: #58c978;
}
```

- The page and chart backgrounds must be black.
- Do not place a white plot, white notebook export, or white image margin inside the report.
- Use near-white primary text and muted grey secondary text.
- Keep borders and gridlines quiet.
- Use flat surfaces with little or no shadow.
- Do not use gradients, glows, glass effects, textures, 3D, or ornamental images.
- Do not put every section inside a card.

## 6. Chart sizing

- Simple chart: usually `420–520px` tall.
- Dense chart: usually `560–700px` tall.
- Heatmap: size height from its row count.
- Axis and legend text: `11–13px`.
- Chart title: `16–18px`.
- Body text: about `15px`.
- Never shrink text to force a chart into a fixed space.
- Increase chart height when labels collide.
- Use responsive SVG when practical.

## 7. Choosing the chart

| Question | Use |
|---|---|
| Change over time | Line or step chart |
| Compare categories | Sorted horizontal bars |
| Show a distribution | Histogram and/or ECDF |
| Show an estimated effect | Dot-and-whisker plot |
| Show two-variable association | Scatter or hexbin plot |
| Show a two-dimensional matrix | Heatmap plus counts |
| Show cumulative change | Line chart or waterfall |
| Show concentration | Contribution bars and cumulative-share curve |
| Show exact values | Table |
| Show a process or timing sequence | Simple diagram or timeline |

Avoid pie charts, donut charts, gauges, radar charts, 3D charts, word clouds, and decorative diagrams.

## 8. Axes and labels

- Always show units.
- Use four to six useful ticks by default.
- Start bar charts at zero.
- Clearly label a nonzero line-chart range.
- Show an important zero, target, or baseline line.
- Directly label series when possible.
- Put legends above or below the plot, never inside a random box.
- Use consistent number precision.
- Use tabular numerals for values.
- Do not rotate labels to rescue a cramped layout. Change the chart or increase its height.
- Avoid dual y-axes. Use aligned vertical panels instead.
- Annotate only important thresholds, failures, breaks, or outliers.

## 9. Heatmaps

- Use meaningful variables on both axes.
- Sort numeric values numerically.
- Use the same scale across comparable heatmaps.
- Center signed values at a meaningful zero or threshold.
- Show counts or support alongside outcomes.
- Mask missing or unreliable cells.
- Never display missing values as zero.
- Do not celebrate one bright cell surrounded by weak results.
- Keep cell labels readable; move extra details into a tooltip or table.

## 10. Tables and exact data

- Pair important charts with an exact data table or local data file.
- Right-align numeric columns.
- Put units in column headers.
- Use subtle row separators instead of borders around every cell.
- Keep long tables inside a horizontal scroller.
- Do not dump thousands of rows into the main page.
- Do not repeat the same values in cards, prose, charts, and tables.

## 11. Writing around charts

- Use short analytical paragraphs, not a bullet-point summary.
- Do not write “the chart speaks for itself.”
- Do not merely describe the shape. Explain what it means.
- Quantify the important difference.
- Mention important exceptions.
- State the limitation.
- Avoid vague language such as “strong,” “interesting,” “promising,” or “significant” without numbers and context.
- Never use a giant KPI card as a substitute for explanation.

## 12. Interaction

- The chart must be understandable without interaction.
- Tooltips may provide exact values but must not contain the only units or caveats.
- Dense charts should be expandable.
- Expansion must work by mouse and keyboard.
- Provide a visible close button and support `Escape`.
- Do not animate charts on page load.
- Avoid filters and controls unless they answer a real question.

## 13. Responsive behavior

- Keep one chart per row on every screen size.
- Test at approximately `1440px`, `768px`, and `390px`.
- Also test the actual embedded viewer width.
- Reduce tick count before rotating labels.
- Increase height instead of shrinking labels.
- Put wide tables and heatmaps in contained scrollers.
- Never create page-level horizontal overflow.
- Preserve the same data and meaning on mobile.

## 14. Never do these things

- No side-by-side charts.
- No chart thumbnails or galleries.
- No raw white notebook exports.
- No generic dashboard card grids.
- No decorative charts.
- No invented data.
- No unlabeled axes.
- No missing units.
- No unreadable legends.
- No inconsistent colors.
- No autoscaled comparable heatmaps.
- No chart without a source.
- No chart without an explanation.
- No chart-library default theme left in place.
- No claim that the work is finished before viewing the rendered result.

## 15. Final checklist

Before delivery, confirm:

- [ ] The page and plot backgrounds are black.
- [ ] The report is centered and no wider than approximately `1200px`.
- [ ] Every chart fills the report column.
- [ ] There is only one chart or major table per row.
- [ ] Every chart answers one clear question.
- [ ] Every chart has a title, subtitle, how-to-read explanation, interpretation, limitation, and source.
- [ ] Labels, units, ticks, and legends are readable.
- [ ] Colors follow the fixed meaning and remain consistent.
- [ ] Missing values are visibly different from zero.
- [ ] Important charts have exact inspectable data.
- [ ] No dashboard tiles, decorative graphics, white plots, or bullet-summary clutter remain.
- [ ] The report was inspected at wide, embedded, tablet, and mobile sizes.
- [ ] Every plotted value matches its source data.

## 16. Short instruction for an LLM

> Read `plot-rules.md` before making or editing any chart. Use a pure-black, centered report no wider than about 1200px. Put one full-width chart per row. Never use side-by-side charts, thumbnail galleries, dashboard cards, white notebook exports, decorative graphics, or default chart-library styling. Give every chart a clear question, neutral title, detailed subtitle, how-to-read note, interpretation, limitation, and source. Use consistent blue/red/orange/grey semantics, keep labels readable, pair important charts with exact data, inspect the rendered result at multiple widths, and do not deliver until the checklist passes.

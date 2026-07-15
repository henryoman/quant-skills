# Mellow Research Report Design

> **Version:** quiet, simple, low-friction reporting profile  
> **Use when:** the reader wants the conclusion and evidence without a dense
> analytical interface  
> **Relationship:** this is an alternative presentation profile. It does not
> weaken the research, uncertainty, provenance, or accessibility requirements
> in the active framework.

## 1. Design idea

Make the report feel like a calm research notebook that has been carefully
edited. It should be easy to enter, easy to scan, and difficult to misread.

The page should have:

- one clear reading column;
- very little visual chrome;
- a soft charcoal background rather than absolute black;
- warm, readable text rather than stark white;
- one muted accent color;
- generous space between ideas;
- only the charts needed to support the decision.

The style is intentionally understated. It should not look like a dashboard,
terminal, marketing page, or trading screen.

## 2. Best uses

Choose the mellow profile for:

- research notes;
- experiment summaries;
- weekly findings;
- short decision briefs;
- negative-result reports;
- method explanations;
- reports with one to four important visuals.

Use the current unified design or the graph-guided version when the evidence is
too dense to explain comfortably in this restrained format.

## 3. Page structure

Use this sequence:

1. Report title.
2. One-line scope: asset, venue, interval, and date range.
3. A short conclusion of no more than three paragraphs.
4. The minimum evidence needed to support or reject the conclusion.
5. Risks and limitations.
6. Method, sources, and reproducibility details.

Avoid a large hero, KPI wall, side navigation, floating controls, and repeated
summary cards. If a number is important, put it in a sentence or a small facts
row.

## 4. Layout

- Main container: `760px` for prose and tables.
- Wide evidence: up to `1040px`, centered in the same reading flow.
- Page padding: `clamp(20px, 5vw, 64px)`.
- Section spacing: `56–80px`.
- Paragraph spacing: `14–20px`.
- Border radius: `4px` or none.
- Shadows: none.
- Columns: one.

Charts, tables, and code may be wider than prose, but they must not create a
second competing page grid.

## 5. Color tokens

```css
:root {
  --page: #171918;
  --surface: #1e211f;
  --surface-soft: #222623;
  --text: #e5e7e3;
  --muted: #a5aba5;
  --faint: #747b75;
  --rule: #343936;
  --accent: #8faea0;
  --positive: #8da9c4;
  --negative: #c28f8f;
  --warning: #c3a77d;
}
```

Keep saturation low. Use the accent for links, focus, and the single most
important series. Do not color whole sections. Status color should appear as a
small label or mark, not a glowing container.

For print, switch to a white background, near-black text, pale rules, and the
same semantic color mapping.

## 6. Typography

Use a familiar system sans-serif stack:

```css
font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", sans-serif;
```

- Report title: `clamp(30px, 5vw, 46px)`, weight `600`.
- Section title: `22–26px`, weight `600`.
- Subsection title: `16–18px`, weight `600`.
- Body: `16–18px`, line-height `1.65–1.75`.
- Metadata and captions: `13–14px`, line-height `1.5`.
- Numbers: tabular numerals.

Do not use all caps for full headings. Uppercase is acceptable only for tiny
status or metadata labels.

## 7. Summary treatment

Begin with a plain statement such as:

> **Decision:** Inconclusive. High relative volume predicts larger one-minute
> ranges, but it did not provide stable directional information after costs.

Follow it with the two or three facts that support the decision. Avoid a row of
decorative metric cards. If a compact facts row is useful, use quiet text and
hairline separators:

```text
Sample  1.8m bars   |   Holdout  90 days   |   Net edge  -0.3 bps
```

## 8. Charts

Use one chart only when it answers a question that prose or a small table
cannot answer as clearly.

Every chart must include:

- a neutral title;
- a subtitle with scope, unit, and sample;
- labeled axes and visible units;
- a clear baseline or reference line when relevant;
- a short caption stating the main reading and limitation;
- source or generation details.

Chart styling:

- background matches the page or quiet surface;
- gridlines use `--rule` at low contrast;
- axis labels use `--muted`;
- the focal series uses `--accent` or the semantic positive/negative colors;
- comparison series use differentiated greys;
- uncertainty bands use transparent fills, not extra bright lines;
- legends should be replaced by direct labels when practical.

Do not use gradients, 3D marks, excessive data labels, animated drawing, or
hover-only explanations.

## 9. Tables

Tables should resemble careful notes, not database administration screens.

- Use a single rule under the header and quiet row separators.
- Right-align numeric columns.
- Keep units in headers.
- Use tabular numerals.
- Highlight no more than one or two rows.
- Use background fills only for actual state or threshold meaning.
- Allow contained horizontal scrolling on narrow screens.

## 10. Notes and warnings

Use a left rule and a short label:

```text
LIMITATION
The final 14 days contain only one high-volatility event, so crisis-regime
stability remains unknown.
```

Do not place every paragraph in a card. Reserve callouts for decisions,
limitations, data issues, and information-boundary warnings.

## 11. Interaction

The static page must contain the full argument. Optional interaction may add:

- exact values on keyboard-accessible focus or hover;
- disclosure of large method tables;
- copy buttons for code or identifiers;
- enlargement for a dense chart.

Avoid sticky toolbars, ambient animation, auto-playing transitions, and
controls that do not change the reader's understanding.

## 12. Responsive and print behavior

At narrow widths:

- keep the single reading flow;
- preserve at least `16px` body text;
- wrap facts rather than shrinking them;
- allow tables to scroll inside their own container;
- simplify chart labels before reducing their size;
- never create page-level horizontal overflow.

Print must preserve the title, conclusion, visuals, captions, limitations,
method, and sources. Interactive-only states must not be required.

## 13. Mellow acceptance checklist

- Can a reader understand the decision in the first screen?
- Is every section necessary?
- Could any chart be replaced by one sentence or a small table?
- Is there only one primary accent?
- Are important caveats visible without interaction?
- Does the report feel quiet without hiding uncertainty?
- Does the evidence remain auditable despite the simpler presentation?

If simplicity removes denominators, uncertainty, execution assumptions, failed
tests, or provenance, the report is incomplete rather than mellow.

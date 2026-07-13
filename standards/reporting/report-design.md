# Unified Research Report Design System

This is the combined report-design standard for this repository. It preserves the complete guidance from the LIQ and ML source systems, while resolving their incompatible defaults through explicit profiles.

Use this document as the entry point. The original source snapshots remain in `report-design-liq.md` and `report-design-ml.md` for provenance.

## 1. Authority and profile selection

Apply guidance in this order:

1. The report's actual communication goal and explicit task requirements.
2. The shared rules in this unified section.
3. One selected layout profile:
   - **General editorial profile:** decision briefs, technical writeups, status reports, teaching reports, catalogs, and domain-neutral analytical reports. Use the LIQ defaults.
   - **Quantitative evidence profile:** alpha research, trading analysis, parameter surfaces, validation reports, market studies, and reports where dense numerical evidence must be audited. Use the ML defaults.
4. A domain companion such as `report-design-dlmm.md`.
5. One-off requirements documented inside the report.
6. Author preference.

State the selected profile in the report source or artifact metadata. Do not silently mix profile-specific defaults.

## 2. Shared rules

The two source systems agree on the following requirements:

- Start from the audience, the report's single job, and the evidence needed to support the conclusion.
- Use a black screen canvas, near-white text, quiet neutral structure, flat surfaces, and restrained color.
- Use a true light print stylesheet rather than embedding screenshots of the dark report.
- Keep prose readable and let important visuals use substantially more width than body copy.
- Organize the report as a reading surface: frame the question, show the evidence, interpret it, disclose caveats, and provide provenance.
- Keep the complete argument understandable without interaction. Tooltips, disclosures, expansion, and copy controls are progressive enhancements.
- Give every figure a meaningful heading, visible units, evidence context, interpretation, and source or provenance.
- Use color for data or state, never decoration. Keep category mappings stable and never rely on color alone.
- Prefer direct labels, restrained gridlines, honest axes, tabular numerals, and explicit uncertainty.
- Prefer a few strong visuals over dashboard chrome or a field of tiny cards.
- Avoid 3D marks, ornamental gradients, glassmorphism, stock decoration, arbitrary colored containers, and remote dependencies in portable reports.
- Make tables semantic and exact; right-align numeric columns, preserve units, and provide contained horizontal scrolling when necessary.
- Make reports responsive, keyboard accessible, printable, and usable when JavaScript fails.
- Preserve sample size, scope, exclusions, time period, method, units, and source close to the evidence they qualify.

## 3. Resolved defaults

### 3.1 Layout and width

For the **general editorial profile**, use the LIQ `1120px` report container, with `1280px` available for genuinely wide evidence. Caption rails, a visual-plus-note rail, paired visuals, small multiples, and a primary-visual-plus-table layout are allowed when the relationship benefits from proximity. Collapse these layouts at narrow widths.

For the **quantitative evidence profile**, use a single-column, full-available-width visual stack. Every chart, heatmap, image, and major table gets its own row. Do not use paired chart grids, thumbnail galleries, or visual `max-width` caps. Prose remains width-limited.

In both profiles, "full width" means the full width made available by the selected profile; it never means creating page-level horizontal overflow.

### 3.2 Figure headings and interpretation

Use four layers when the evidence warrants them:

1. A section heading phrased as the analytical question or finding.
2. A neutral chart title stating what is plotted.
3. An assumptions-rich subtitle stating scope, unit, period, population, and method.
4. A nearby `Read` paragraph explaining the result, decision relevance, and caveat.

For a simple general report, layers 1 and 2 may be combined into one finding-oriented figure heading. Quantitative reports should keep all four layers when practical. This resolves the LIQ preference for finding/question headings and the ML requirement for neutral descriptive chart titles.

### 3.3 Color semantics

Use these mappings consistently:

- Quantitative favorable or positive magnitude: blue.
- Quantitative adverse or negative magnitude: red.
- Marginal, fragile, warning, or near-threshold magnitude: orange.
- Neutral, near-zero, unknown, unavailable, or not-applicable states: differentiated greys or a labeled neutral pattern.
- Pass/success status badges and small state marks: green.
- Fail status badges and adverse state marks: red.
- Primary focus, selection, or link: blue.

Green is therefore a status color, not the default positive quantitative scale. This preserves LIQ's semantic state palette while following ML's more accessible blue-versus-red data encoding.

### 3.4 Chart height and density

For general editorial charts, begin with the LIQ ranges: `320–460px` for primary charts, `240–340px` for secondary charts, and `120–190px` per small-multiple panel.

For quantitative evidence charts, begin with the ML ranges: `420–620px` for simple bar/line charts, `560–760px` for dense multi-series charts, and row-derived heatmap heights of roughly `44–64px` per row.

These are starting ranges, not fixed aspect ratios. Increase height before crushing labels or reducing type below the documented minimums.

### 3.5 Typography

Use `Inter` only when it is locally bundled or reliably installed, followed by the system sans-serif stack. Never fetch a remote font merely to render a durable report. Use a local monospace stack or tabular numerals for data, timestamps, identifiers, prices, rates, and aligned numeric columns.

Use the LIQ title scale for editorial profiles and the more compact ML title scale for dense quantitative profiles. In either case, the report title is the only oversized text and data labels must remain legible.

### 3.6 Interaction and expansion

The static report must communicate the full argument. For dense quantitative charts and heatmaps, click-to-expand, keyboard-focus tooltips, exact-data disclosure, and a chart data table are expected where feasible. For simpler editorial reports, expansion is optional when the inline visual is already fully legible.

Never place essential units, sources, caveats, or conclusions only inside hover or interaction.

### 3.7 Small multiples and galleries

Small multiples and paired visuals are available only in the general editorial profile and only when shared scales and proximity materially improve comparison. Quantitative evidence defaults to one visual per row.

Image galleries are acceptable only for a genuinely large evidence set with readable full-size inspection. Detached chart galleries and thumbnail dashboards are not acceptable in either profile.

### 3.8 Source-specific constraints

The ML source includes an instruction that active Solana Up/Down reporting is 5-minute only and must not mix legacy 15-minute results. Treat that as an originating-repository constraint, not a universal design rule. Apply it only to reports whose data contract inherits that ML repository convention.

The phrases "instrument ledger" and "evidence terminal" describe precision, alignment, and auditability. They do not authorize fake-terminal decoration such as command prompts, scanlines, glowing text, or decorative telemetry.

## 4. Conflict ledger

| Topic | LIQ source | ML source | Unified resolution |
|---|---|---|---|
| Report width | Centered `1120px`, up to `1280px` for wide evidence | `width: 100%`, no visual max-width | Select by profile |
| Columns | Allows rails, paired visuals, and small multiples | Requires one visual per row and forbids chart grids | Select by profile; quant stays single-column |
| Positive data | Green semantic positive token | Blue positive quantitative magnitude | Green for status; blue for positive magnitude |
| Primary chart height | `320–460px` | `420–620px`; dense charts taller | Select by profile and evidence density |
| Figure title | Prefer finding or question | Require neutral descriptive chart title | Finding/question section + neutral chart title + subtitle + read |
| Expansion | Static-first; interaction optional and subordinate | Click-to-expand expected where feasible | Always static-complete; expansion expected for dense quant |
| Galleries | Allows a controlled gallery for genuine evidence sets | Forbids thumbnail/chart galleries | Evidence-image gallery only; never a detached chart gallery |
| Font stack | Inter first, if available | System sans first | Local Inter allowed; otherwise system stack; never remote |
| Title scale | `30–42px`, weight `700` | `24–40px`, weight `600` | Editorial uses LIQ; dense quant uses ML |
| Solana timeframe | No general restriction | Active Up/Down is 5-minute only | Scope to inheriting ML reports, not the general system |

## 5. Complete LIQ source system

The following part is preserved in full from `report-design-liq.md`. Where it conflicts with Sections 1–4 above, the selected profile and resolved defaults control.

# LIQ HTML Report Design System

> **Purpose:** the general house style for clear, minimal, visually rigorous HTML reports.
> **Applies to:** research reports, analytical briefs, technical writeups, experiment summaries, audits, status reports, evidence reviews, and other durable HTML documents.
> **Companion:** use `report-design-dlmm.md` only when a report needs DLMM-, trading-, execution-, or strategy-specific conventions.
> **Core idea:** a report is a reading surface with visual evidence, not a dashboard wearing a document costume.

This is the main design guide. It is intentionally domain-neutral. It defines how reports should look, read, flow, scale, print, and behave. It covers the overall page before individual charts: silhouette, hierarchy, column structure, typography, spacing, color, dividers, figures, tables, images, annotations, responsive behavior, accessibility, and portable HTML implementation.

The default LIQ report is minimal without feeling unfinished. It uses a near-black working surface, crisp typography, quiet rules, compact metadata, generous but controlled spacing, and visuals that are integrated into the argument. It avoids generic dashboard cards, marketing-page hero sections, ornamental gradients, and chart-library chrome.

---

## 1. How to use this guide

### 1.1 Order of authority

Use design guidance in this order:

1. the report’s actual communication goal;
2. this general design system;
3. a domain-specific companion such as `report-design-dlmm.md`;
4. one-off requirements documented inside the report;
5. author preference.

Domain companions may add terminology, evidence requirements, or specialized visual types. They should not casually replace this guide’s page structure, typography, spacing, responsiveness, or accessibility rules.

### 1.2 Normative words

- **MUST / MUST NOT:** required for a conforming report.
- **SHOULD / SHOULD NOT:** expected unless a clear reason is documented.
- **MAY:** optional.

### 1.3 The authoring sequence

Do not start by choosing charts or writing CSS. Work in this order:

1. Name the audience.
2. Write the page’s single job in one sentence.
3. List the three to seven things the reader must understand.
4. Put those things in a causal or decision-making order.
5. Decide which ideas need prose, numbers, tables, charts, diagrams, or images.
6. Sketch the page silhouette.
7. Apply the tokens and component patterns in this guide.
8. Remove anything that does not improve comprehension.
9. Test narrow, wide, print, keyboard, grayscale, and JavaScript-failure states.

---

## 2. Design direction

### 2.1 Subject, audience, and job

The system is designed for evidence-heavy work read by people who need to understand and act, not browse casually.

- **Subject:** structured findings, methods, comparisons, decisions, and sources.
- **Audience:** a technically capable reader who values speed, clarity, and auditability.
- **Single job:** make the document’s main conclusion and supporting evidence easy to understand without overstating either.

### 2.2 Visual character

The visual character is **instrument ledger**:

- dark, flat, and quiet;
- precise rather than luxurious;
- editorial in hierarchy, technical in detail;
- dense where comparison benefits from density;
- spacious where reading and interpretation need room;
- visually distinctive through rhythm and evidence treatment, not effects.

This is not a fake terminal. Do not add command prompts, scanlines, glowing green text, or decorative telemetry. “Instrument” means dependable alignment and useful feedback. “Ledger” means ordered evidence and visible provenance.

### 2.3 Signature device: the caption rail

The house signature is the **caption rail**: each major visual is bound to its interpretation and provenance.

```text
Finding or question
Short interpretive sentence, if needed

VISUAL

Scope · unit · period · method · source
```

The rail is usually typographic, not boxed. It gives every figure a clear top and bottom. It also keeps charts from becoming decorative islands.

### 2.4 Restraint rule

Spend visual emphasis once per page:

- one primary chart;
- one dominant conclusion;
- one focus color;
- one unusual layout moment, if justified.

Everything else should support that emphasis. A page with six “hero” numbers, eight colored callouts, and four equally loud charts has no hierarchy.

---

## 3. Principles

### 3.1 The report is read, not operated

Reports may include disclosures, filters, and copy actions, but their default state MUST communicate the complete argument. Do not make the reader configure the page before understanding it.

### 3.2 Structure is visible meaning

Dividers, alignment, columns, labels, and spacing must encode relationships:

- a rule separates chapters;
- proximity groups related information;
- alignment makes values comparable;
- indentation expresses hierarchy;
- numbering expresses a real sequence;
- width signals reading versus scanning.

Do not use structural decoration without structural meaning.

### 3.3 Text leads; visuals prove

The report should state what a visual is for. A chart does not excuse vague writing. A paragraph should not force the reader to mentally reconstruct a chart that would be clearer.

### 3.4 Minimal means edited

Minimal reports are difficult because spacing, wording, scale, and alignment are exposed. Remove decoration, not context.

### 3.5 Density should be local

A report can be dense without being uniformly cramped:

- dense tables inside calm sections;
- compact metric strips below a spacious summary;
- tightly aligned small multiples with generous outer margins;
- short captions immediately attached to visuals.

### 3.6 Every visual answers a question

Before adding any graph, table, image, or diagram, complete:

> The reader needs this visual to understand ________.

If the blank cannot be filled with one specific relationship, remove or split the visual.

### 3.7 Evidence strength controls visual strength

Exploratory, incomplete, or uncertain findings SHOULD look quieter than stable primary findings. Do not give the most dramatic styling to the least reliable result.

---

## 4. Report types

The system supports several report shapes. Choose one before laying out the page.

### 4.1 Decision brief

**Use when:** the reader must choose, approve, reject, or defer.

```text
Title + scope
Read
Decision
Key evidence
Alternatives / tradeoffs
Risks
Next action
Sources
```

The first screen should contain the question, answer, and decision status.

### 4.2 Analytical report

**Use when:** the reader must understand a pattern, comparison, or change.

```text
Title + scope
Summary finding
Primary visual
Supporting evidence
Segments / distribution
Counterevidence
Method and caveats
Sources
```

The primary chart is the visual thesis.

### 4.3 Technical report

**Use when:** the reader must understand a system, implementation, incident, or method.

```text
Title + system boundary
Current state / result
Architecture or sequence
Detailed findings
Failure modes
Verification
Files / commands / sources
```

Use diagrams only when relationships or sequence are materially clearer than prose.

### 4.4 Status report

**Use when:** the reader must understand progress, health, change, and blockers.

```text
Title + reporting period
Status sentence
Key changes
Progress against target
Risks / blockers
Decisions needed
Next period
```

Avoid turning status reports into grids of unlabeled KPI cards.

### 4.5 Catalog or index report

**Use when:** the page primarily helps readers find artifacts.

```text
Title + catalog scope
Search / filters
Grouped artifact list
Short metadata and status
Empty state
```

An index may behave more like an interface, but item hierarchy and readable metadata still follow this system.

### 4.6 Narrative or teaching report

**Use when:** the reader needs an explanation built in stages.

```text
Question
Concept
Simple example
Visual explanation
Real evidence
Implication
Caveats
Further reading
```

Use progressive complexity. Do not open with the densest table.

---

## 5. Page architecture

### 5.1 Canonical order

Most reports SHOULD use:

1. Header
2. Read
3. Key numbers or facts
4. Main evidence
5. Supporting evidence
6. Exceptions or counterevidence
7. Implications or decision
8. Caveats and method
9. Sources and reproduction

Reorder only when the reader genuinely needs background before the conclusion.

### 5.2 Page silhouette

```text
┌──────────────────────────────────────────────────────────────┐
│ small context label                              metadata    │
│ REPORT TITLE                                                 │
│ one-sentence scope                                           │
├──────────────────────────────────────────────────────────────┤
│ READ                                                         │
│ concise answer with useful confidence                        │
├──────────────────────────────────────────────────────────────┤
│ metric     metric      metric      metric                    │
├──────────────────────────────────────────────────────────────┤
│ Finding-led visual heading                                   │
│                                                              │
│                     PRIMARY VISUAL                           │
│                                                              │
│ caption rail                                                 │
├──────────────────────────────────────────────────────────────┤
│ supporting visual             supporting table               │
├──────────────────────────────────────────────────────────────┤
│ implications / exceptions / caveats                          │
├──────────────────────────────────────────────────────────────┤
│ sources / method / reproduction                              │
└──────────────────────────────────────────────────────────────┘
```

### 5.3 First viewport

At a normal embedded desktop width, the first viewport SHOULD show:

- report subject;
- scope or reporting period;
- main read;
- status or conclusion;
- the beginning of the primary evidence.

Do not occupy the first viewport with:

- a decorative hero;
- a large empty masthead;
- generic navigation;
- more than one row of summary metrics;
- a full-width image with no analytical role.

### 5.4 Chapters and sections

Each top-level section should perform one job. Good names include:

- `Read`
- `Decision`
- `What changed`
- `Evidence`
- `Distribution`
- `Exceptions`
- `Risk`
- `Method`
- `Sources`
- `Next run`

Avoid generic headings such as `Overview`, `Analysis`, `Insights`, or `Details` when a precise label exists.

### 5.5 Long reports

For reports longer than roughly 3,000 words or ten major sections:

- include a compact contents list after the summary;
- link to real headings;
- keep contents to one level by default;
- do not make the contents sticky inside an embedded viewer;
- add `Back to contents` only after genuinely long chapters;
- never repeat a full navigation rail that competes with the surrounding app.

---

## 6. Grid and container system

### 6.1 Core widths

```css
:root {
  --width-copy: 72ch;
  --width-report: 1120px;
  --width-wide: 1280px;
}

.report {
  width: min(calc(100% - 48px), var(--width-report));
  margin-inline: auto;
  padding-block: 28px 64px;
}

.copy { max-width: var(--width-copy); }
.wide { width: min(100%, var(--width-wide)); }
```

- Use `1120px` for most reports.
- Use `1280px` only for a genuinely wide table, dense small multiples, or a diagram.
- Keep body copy at `58–76ch` even when visuals are wider.
- Never stretch paragraphs across the entire visual width.

### 6.2 Internal grid

The preferred internal grid is 12 conceptual columns. Authors do not need a grid framework; CSS Grid is sufficient.

Common spans:

- prose: 7–9 columns;
- primary visual: 12 columns;
- visual plus note rail: 8 + 4 columns;
- paired visuals: 6 + 6 columns;
- primary visual plus table: 7 + 5 columns;
- metric strip: equal auto-fit columns.

### 6.3 Grid implementations

```css
.layout-rail {
  display: grid;
  grid-template-columns: minmax(0, 8fr) minmax(220px, 4fr);
  gap: 32px;
  align-items: start;
}

.layout-pair {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 32px;
}

.layout-main-table {
  display: grid;
  grid-template-columns: minmax(0, 7fr) minmax(280px, 5fr);
  gap: 32px;
}
```

### 6.4 Alignment

- Titles, headings, paragraphs, tables, and figure headings are left-aligned.
- Numeric table columns are right-aligned.
- Metric values align on a shared top or baseline.
- Paired visuals align their plot areas, not merely their outer boxes.
- Captions align to the visual edge.
- Side notes align with the exact paragraph or visual they qualify.
- Do not center ordinary content.

### 6.5 Full-bleed elements

Within the report container, a visual MAY exceed the prose width. It SHOULD NOT exceed the report width unless:

- it is a large matrix or timeline;
- it remains readable in the embedded viewer;
- it does not create page-wide horizontal overflow;
- a contained scroller is provided when necessary.

---

## 7. Spacing and rhythm

### 7.1 Base scale

```css
:root {
  --s1: 4px;
  --s2: 8px;
  --s3: 12px;
  --s4: 16px;
  --s5: 20px;
  --s6: 24px;
  --s8: 32px;
  --s10: 40px;
  --s12: 48px;
  --s16: 64px;
}
```

### 7.2 Vertical rhythm

| Relationship | Space |
|---|---:|
| label → value | `4px` |
| heading → explanatory line | `6–8px` |
| visual title → plot | `12–16px` |
| plot → caption rail | `8–12px` |
| paragraph → paragraph | `10–14px` |
| list item → list item | `4–8px` |
| subsection → subsection | `24–32px` |
| chapter → chapter | `40–56px` |
| header → first section | `28–40px` |

### 7.3 Section pattern

```css
.report-section {
  padding-block: 32px;
  border-top: 1px solid var(--line);
}

.report-section[data-density="compact"] { padding-block: 24px; }
.report-section[data-density="spacious"] { padding-block: 48px; }
```

### 7.4 Rhythm rules

- Use spacing before adding a container.
- Use one major rule plus space to separate chapters.
- Do not put a border around every section.
- Do not alternate arbitrary section backgrounds.
- Keep related heading, visual, and caption together.
- Increase outer whitespace around the primary conclusion, not around every element.
- If a page feels busy, first remove redundant labels and rules; do not simply increase all gaps.

---

## 8. Color system

### 8.1 Core palette

```css
:root {
  color-scheme: dark;

  --canvas: #000000;
  --surface: #080808;
  --surface-2: #101010;
  --surface-3: #171717;

  --ink: #f4f4f4;
  --ink-muted: #b8b8b8;
  --ink-faint: #777777;

  --line: #242424;
  --line-strong: #3a3a3a;
  --gridline: #1e1e1e;

  --focus: #67b7ff;
  --positive: #58c978;
  --negative: #ff6b66;
  --warning: #e5b94f;
  --unknown: #8b8b8b;
}
```

### 8.2 Roles

- `canvas`: page background.
- `surface`: functional bounded areas only.
- `surface-2`: code, selected row, compact controls, or print fallback preview.
- `ink`: main text and primary chart series.
- `ink-muted`: explanatory text and axes.
- `ink-faint`: metadata and secondary annotations.
- `line`: ordinary separation.
- `line-strong`: major boundary, zero line, or active divider.
- `focus`: selected series, link, keyboard focus, or one primary emphasis.
- semantic colors: meaningful outcomes and states only.

### 8.3 Color discipline

1. Use neutral structure first.
2. Use focus blue for one active or primary distinction.
3. Use semantic color only when the semantic meaning is explicit.
4. Never color a heading merely to create variety.
5. Never use a colored background behind every metric.
6. Never use green/red without a label, sign, position, or shape.
7. Never use a rainbow scale.
8. Keep data palettes consistent across the whole report.
9. The same category MUST retain the same color across figures.
10. Missing or unknown values MUST have a distinct neutral state.

### 8.4 Light and print palette

Screen mode is dark by default. Print mode is light. A report MAY support a light screen theme, but must not compromise the dark house treatment.

```css
@media print {
  :root {
    --canvas: #ffffff;
    --surface: #ffffff;
    --surface-2: #f5f5f5;
    --surface-3: #ededed;
    --ink: #111111;
    --ink-muted: #4d4d4d;
    --ink-faint: #6f6f6f;
    --line: #d8d8d8;
    --line-strong: #a8a8a8;
    --gridline: #e7e7e7;
  }
}
```

---

## 9. Typography

### 9.1 Font roles

Use two functional families:

```css
:root {
  --font-text: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-data: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
}
```

- `--font-text`: titles, headings, body, labels, captions.
- `--font-data`: numbers, timestamps, paths, hashes, code, axis values when alignment benefits.

Do not fetch remote fonts for a durable report. If a project-bundled font is guaranteed, it MAY precede these stacks.

### 9.2 Type scale

| Role | Size | Line height | Weight | Max width |
|---|---:|---:|---:|---:|
| Title | `clamp(30px, 4vw, 42px)` | `1.04` | `700` | `22ch` |
| Deck | `16px` | `1.55` | `400` | `72ch` |
| Major heading | `20px` | `1.25` | `650` | — |
| Minor heading | `15–17px` | `1.35` | `650` | — |
| Body | `15px` | `1.62` | `400` | `72ch` |
| Lead | `17–19px` | `1.55` | `450` | `68ch` |
| Metric value | `20–28px` | `1.1` | `650` | — |
| Table | `12–14px` | `1.45` | `400` | — |
| Caption | `11–12px` | `1.45` | `450` | — |
| Kicker | `11–12px` | `1.25` | `650` | — |
| Axis | `10–12px` | `1.2` | `500` | — |

### 9.3 Hierarchy

- The title is the only oversized text.
- Major headings identify chapters.
- Minor headings identify local questions or findings.
- Figure titles are smaller than chapter headings but may be bolder.
- Metadata is small, not low-contrast to the point of illegibility.
- Metric values are prominent but never larger than the report title.

### 9.4 Typographic details

```css
.numeric,
table,
.metric-strip,
.chart-label {
  font-variant-numeric: tabular-nums lining-nums;
}
```

- Use sentence case.
- Use uppercase only for short kickers, states, or column labels.
- Avoid letter spacing on body copy.
- Keep title tracking around `-0.02em` to `-0.03em`.
- Do not use thin weights on black.
- Do not justify paragraphs.
- Use real typographic quotation marks in prose.
- Use an en dash for ranges and an em dash sparingly.
- Keep labels short enough to avoid forced wrapping when possible.

### 9.5 Links

- Links use focus blue or an underline.
- Source paths may use mono.
- External links SHOULD identify their destination in text.
- Avoid making an entire long card a link when a clear title link works.
- Printed links should remain underlined or expose a useful URL in sources.

---

## 10. Header design

### 10.1 Required anatomy

```html
<header class="report-header">
  <div class="header-topline">
    <p class="kicker">Quarterly review · Final</p>
    <p class="header-date">Generated 2026-07-13</p>
  </div>
  <h1>Specific report title</h1>
  <p class="deck">One sentence defining scope, period, and the question answered.</p>
  <dl class="header-meta">
    <div><dt>Period</dt><dd>Apr–Jun 2026</dd></div>
    <div><dt>Coverage</dt><dd>14 teams</dd></div>
    <div><dt>Status</dt><dd>Final</dd></div>
  </dl>
</header>
```

### 10.2 Header rules

- Keep the header unboxed.
- Put context above the title, never a giant label below it.
- The deck defines scope; it does not repeat the title.
- Put compact metadata in one row when space permits.
- Keep status textual.
- Use a strong bottom rule to transition into the report.
- Do not make the header sticky inside a report viewer.
- Do not put a decorative image behind the title.

### 10.3 CSS

```css
.report-header {
  padding-bottom: 28px;
  border-bottom: 1px solid var(--line-strong);
}
.header-topline {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  color: var(--ink-faint);
  font: 650 11px/1.25 var(--font-data);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.report-header h1 {
  max-width: 22ch;
  margin: 10px 0 0;
  font-size: clamp(30px, 4vw, 42px);
  line-height: 1.04;
  letter-spacing: -0.025em;
}
.deck {
  max-width: 72ch;
  margin: 12px 0 0;
  color: var(--ink-muted);
  font-size: 16px;
  line-height: 1.55;
}
```

---

## 11. Summary and key facts

### 11.1 Summary read

The first substantive paragraph should tell the reader:

- what happened or what the report concludes;
- how large or important it is;
- how certain or complete the evidence is;
- what the reader should do with it, if action is in scope.

Use a lead paragraph, not a huge quote block.

```css
.report-lead {
  max-width: 68ch;
  margin: 0;
  font-size: clamp(17px, 2vw, 19px);
  line-height: 1.55;
  font-weight: 450;
}
```

### 11.2 Metric strip

Metrics are inline facts separated by rules, not a collection of floating dashboard cards.

```html
<dl class="metric-strip">
  <div>
    <dt>Coverage</dt>
    <dd>94%</dd>
    <small>1,842 of 1,963 records</small>
  </div>
  <div>
    <dt>Median cycle</dt>
    <dd>3.8 days</dd>
    <small>down 0.6 days</small>
  </div>
</dl>
```

```css
.metric-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  margin: 24px 0 0;
  border-block: 1px solid var(--line);
}
.metric-strip > div {
  min-width: 0;
  padding: 14px 16px;
  border-right: 1px solid var(--line);
}
.metric-strip > div:last-child { border-right: 0; }
.metric-strip dt { color: var(--ink-muted); font-size: 12px; }
.metric-strip dd {
  margin: 4px 0 0;
  font: 650 21px/1.15 var(--font-data);
}
.metric-strip small {
  display: block;
  margin-top: 5px;
  color: var(--ink-faint);
  font-size: 11px;
}
```

### 11.3 Metric rules

- Use three to six metrics.
- Label every value.
- Include units.
- Include comparison context only when meaningful.
- Do not display meaningless decimal precision.
- Do not color every value.
- If a metric is good or bad only relative to a target, show the target.
- If a percentage hides a small denominator, show the count.
- Do not duplicate the same number in the title, lead, metric strip, and chart annotation.

---

## 12. Sections, callouts, notes, and code

### 12.1 Standard section

```html
<section class="report-section" aria-labelledby="section-evidence">
  <header class="section-header">
    <h2 id="section-evidence">Evidence</h2>
    <p>Optional one-sentence section scope.</p>
  </header>
  <!-- content -->
</section>
```

```css
.section-header { margin-bottom: 20px; }
.section-header h2 { margin: 0; font-size: 20px; line-height: 1.25; }
.section-header p {
  max-width: 72ch;
  margin: 6px 0 0;
  color: var(--ink-muted);
}
```

### 12.2 Callouts

Use a callout only for a decision, warning, exception, or unusually important interpretation.

```html
<aside class="callout" data-tone="warning">
  <strong>Coverage gap</strong>
  <p>Records before 2026-04-03 are incomplete; comparisons use the later shared window.</p>
</aside>
```

```css
.callout {
  max-width: 76ch;
  padding: 12px 0 12px 16px;
  border-left: 3px solid var(--line-strong);
}
.callout[data-tone="focus"] { border-left-color: var(--focus); }
.callout[data-tone="positive"] { border-left-color: var(--positive); }
.callout[data-tone="negative"] { border-left-color: var(--negative); }
.callout[data-tone="warning"] { border-left-color: var(--warning); }
.callout strong { display: block; margin-bottom: 4px; }
.callout p { margin: 0; color: var(--ink-muted); }
```

Do not use filled alert boxes for ordinary context.

### 12.3 Side notes

Side notes are appropriate for definitions, scope qualifications, and reading instructions. They should not contain the only copy of a critical caveat.

```css
.side-note {
  color: var(--ink-muted);
  font-size: 12px;
  line-height: 1.5;
  border-top: 1px solid var(--line);
  padding-top: 10px;
}
```

### 12.4 Code and commands

```css
code, pre { font-family: var(--font-data); }
code {
  padding: 0.08em 0.28em;
  background: var(--surface-2);
  border-radius: 3px;
}
pre {
  max-width: 100%;
  overflow: auto;
  padding: 14px 16px;
  border: 1px solid var(--line);
  background: var(--surface);
  font-size: 12px;
  line-height: 1.55;
}
pre code { padding: 0; background: transparent; }
```

- Show commands only when useful.
- Name the working directory.
- Avoid decorative syntax coloring.
- Never include secrets.
- Wrap or horizontally scroll; never force page overflow.

### 12.5 Lists

- Use bullets for nonsequential items.
- Use numbers only when order matters.
- Keep list items grammatically parallel.
- Add `4–8px` between complex items.
- Avoid deeply nested lists; use subheadings after two levels.

---

## 13. Figures and the caption rail

### 13.1 Figure anatomy

```html
<figure class="report-figure">
  <figcaption class="figure-head">
    <strong>Completion improved most in the middle of the process.</strong>
    <span>Stage-level conversion compared with the prior period.</span>
  </figcaption>
  <div class="figure-body">
    <!-- chart, image, diagram, or table -->
  </div>
  <p class="figure-note">
    1,842 records · Apr–Jun 2026 · percentage of eligible records · source: events.csv
  </p>
</figure>
```

### 13.2 Figure CSS

```css
.report-figure { margin: 0; min-width: 0; }
.figure-head {
  display: grid;
  gap: 4px;
  margin-bottom: 14px;
}
.figure-head strong {
  color: var(--ink);
  font-size: 16px;
  line-height: 1.35;
}
.figure-head span {
  max-width: 72ch;
  color: var(--ink-muted);
  font-size: 13px;
  line-height: 1.5;
}
.figure-body { min-width: 0; }
.figure-note {
  margin: 10px 0 0;
  color: var(--ink-faint);
  font: 450 11px/1.5 var(--font-data);
  overflow-wrap: anywhere;
}
```

### 13.3 Figure heading language

Prefer a finding or question:

- `Growth came from existing accounts, not new acquisition.`
- `Which stages explain the longer cycle?`
- `The error rate fell, but only in high-volume regions.`

Avoid chart nouns alone:

- `Revenue chart`
- `Results`
- `Breakdown`
- `Graph 2`

### 13.4 Figure note contents

Include the context needed to interpret the visual:

- sample or coverage;
- unit;
- date range and timezone if relevant;
- aggregation or estimator;
- exclusions or missingness;
- uncertainty method if shown;
- source.

Do not turn the note into a paragraph. Put extended methods in `Method` or a disclosure.

---

## 14. General chart language

### 14.1 Chart palette

```css
:root {
  --chart-primary: #f4f4f4;
  --chart-secondary: #a8a8a8;
  --chart-tertiary: #666666;
  --chart-focus: #67b7ff;
  --chart-positive: #58c978;
  --chart-negative: #ff6b66;
  --chart-grid: #1e1e1e;
}
```

### 14.2 Visual hierarchy inside a chart

From strongest to weakest:

1. selected or primary data mark;
2. direct label or important annotation;
3. comparison data mark;
4. axis labels;
5. zero/reference line;
6. ordinary gridline;
7. plot boundary, usually absent.

If gridlines are as bright as the data, the hierarchy is wrong.

### 14.3 Chart dimensions

- Primary chart: `320–460px` tall.
- Secondary chart: `240–340px` tall.
- Small multiple: `120–190px` tall per panel.
- Minimum readable plot width: about `280px` after margins.
- Use responsive SVG with a `viewBox`.
- Keep enough right margin for direct labels.
- Increase height rather than crushing labels on narrow screens.

### 14.4 Axes

- State units once clearly.
- Use four to six ticks by default.
- Keep tick formatting consistent.
- Use horizontal gridlines sparingly.
- Make zero or a meaningful baseline stronger.
- Bar charts start at zero.
- Nonzero line-chart domains must be visually honest and labeled.
- Time axes identify timezone when ambiguity matters.
- Log scales explicitly say `log`.
- Do not use dual y-axes unless no clearer small-multiple or indexed alternative exists.

### 14.5 Lines and marks

- Primary line: `2px`.
- Comparison line: `1.5px`, gray or dashed.
- Reference line: `1px`, dashed.
- Confidence band: `10–18%` opacity.
- Scatter point: `3–5px`, semi-transparent.
- Selected point: larger, outlined, and labeled.
- Bars have square corners by default.
- Avoid outlines on every bar.
- Avoid point markers on dense lines.
- Never use 3D marks.

### 14.6 Direct labels and legends

Directly label series whenever practical. A legend is allowed when labels would collide or a scale is reused across panels.

Legend rules:

- place above or below the plot;
- keep it unboxed;
- use full names;
- order items like the marks;
- show line style or symbol as well as color;
- cap visible categories around six.

### 14.7 Annotation

Annotate only what changes interpretation:

- threshold;
- target;
- regime change;
- maximum/minimum;
- data gap;
- decision-driving outlier;
- start/end value.

Use short factual labels. Avoid editorial excitement.

### 14.8 Uncertainty

- Show intervals when estimated.
- Define what they are.
- Keep intervals visually subordinate to the estimate.
- Do not crop intervals at plot edges.
- Do not use error bars without a method label.
- Use a reference line for no difference when comparing effects.

---

## 15. Choosing a visual

| Reader question | Best default | Common mistake |
|---|---|---|
| How did something change over time? | line or step chart | unordered columns |
| Which categories are largest? | sorted horizontal bars | donut with many slices |
| What caused a total to change? | waterfall | disconnected KPIs |
| What is the distribution? | histogram, box plot, or ECDF | mean-only bar |
| Are two measures related? | scatter plot | connected points |
| How do groups differ with uncertainty? | dot-and-whisker | bars hiding intervals |
| How do two dimensions interact? | heatmap | rainbow surface |
| How did entities move between two states? | paired dots or slopegraph | two separate rankings |
| What is the share of a whole? | sorted bars or 100% strip | pie with small slices |
| What is the process or sequence? | flow or timeline | decorative boxes |
| What exact values must be audited? | table | chart for every field |
| What is the hierarchy? | tree | improvised flowchart |
| What is the page layout or UI concept? | wireframe | prose alone |

Use the smallest visual that answers the question. Variety is not a goal.

---

## 16. Common chart patterns

### 16.1 Line chart

Use for ordered change.

- Keep time/order on x.
- Use a real zero/reference when meaningful.
- Directly label the final point.
- Mark gaps rather than connecting across missing data.
- Use a step line when the value changes only at events.
- Avoid smoothing unless named and justified.
- If more than three lines matter, use small multiples or interaction.

### 16.2 Horizontal bars

Use for category comparison and ranking.

- Sort by value unless order has intrinsic meaning.
- Put labels on the left and exact values at bar ends.
- Start the value axis at zero.
- Use a central zero for signed values.
- Keep category labels horizontal.
- Limit visible categories; disclose omitted rows.

### 16.3 Histogram

Use for shape, spread, skew, modes, and tails.

- State binning or bin width.
- Mark median and meaningful thresholds.
- Keep bin widths equal.
- Use the same bins for compared panels.
- Show sample size.
- Consider ECDF for heavy tails.

### 16.4 Scatter plot

Use for two continuous measures.

- Show raw points.
- Use transparency for overlap.
- Label only important outliers.
- Name any fitted model.
- Include an interval around the fit when available.
- Do not describe correlation as causation.
- Use log scales for multiplicative ranges only when explained.

### 16.5 Dot-and-whisker

Use for estimates and intervals.

- Dot is the estimate.
- Whisker is the defined interval.
- Reference line shows zero, baseline, or target.
- Sort rows meaningfully.
- Add sample size where reliability differs.
- Prefer this to bars for modeled effects.

### 16.6 Heatmap

Use for a matrix or interaction.

- Sequential scale for magnitude.
- Diverging scale centered at a meaningful midpoint for signed values.
- Missing cells receive a distinct nonzero style.
- Keep scales fixed across comparable heatmaps.
- Show cell values only when legible.
- Include counts if sparse cells can mislead.

### 16.7 Waterfall

Use for additive change.

- Distinguish starting total, changes, and ending total.
- Show signed values.
- Reconcile visible arithmetic.
- Keep connector lines quiet.
- Do not use if components overlap or are not additive.

### 16.8 Small multiples

Use for repeated comparisons across groups.

- Same geometry.
- Same scales.
- Same color meaning.
- Panel label includes group and sample.
- Arrange in a meaningful order.
- Keep per-panel annotation minimal.

### 16.9 100% strip

Use for a simple two- to four-part share.

- Label segments directly when they fit.
- Put exact values beside the strip when they do not.
- Use neutral tones plus one focus segment.
- Do not use for many tiny categories.

### 16.10 Sparklines

Use only inside a row or metric when compact trend context genuinely helps.

- Show start/end or last value.
- Use a shared scale across compared rows.
- Do not hide an important change behind a tiny sparkline.
- Keep the full chart available elsewhere if precise reading matters.

### 16.11 Discouraged visuals

- Pie/donut: usually replace with bars or a 100% strip.
- Radar: do not use.
- Gauge: replace with value + target strip.
- 3D: do not use.
- Word cloud: replace with ranked terms and counts.
- Sankey: only for real conserved flow.
- Chord/network: only when topology itself is the question.
- Decorative maps: use maps only when geography is analytically meaningful.

---

## 17. Tables

### 17.1 Use tables for exactness

Tables are the right visual when readers need to look up, compare, copy, or audit exact values. A good report often pairs one shape-revealing chart with one exact-value table.

### 17.2 Semantic structure

```html
<div class="table-region" role="region" tabindex="0" aria-label="Regional results">
  <table>
    <caption>Regional results</caption>
    <thead>
      <tr>
        <th scope="col">Region</th>
        <th scope="col" class="num">Records</th>
        <th scope="col" class="num">Completion</th>
        <th scope="col" class="num">Change</th>
      </tr>
    </thead>
    <tbody><!-- rows --></tbody>
  </table>
</div>
<p class="table-note">Sorted by completion · 14 regions · percentage-point change.</p>
```

### 17.3 Table CSS

```css
.table-region {
  max-width: 100%;
  overflow: auto;
  border-block: 1px solid var(--line);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  font-variant-numeric: tabular-nums lining-nums;
}
caption {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
th, td {
  padding: 9px 10px;
  border-bottom: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}
th {
  color: var(--ink-muted);
  font-size: 11px;
  font-weight: 650;
}
th.num, td.num {
  text-align: right;
  font-family: var(--font-data);
  white-space: nowrap;
}
tbody tr:last-child td { border-bottom: 0; }
.table-note {
  margin: 10px 0 0;
  color: var(--ink-faint);
  font-size: 11px;
}
```

### 17.4 Table rules

- Use horizontal rules, not full cell boxes.
- Align numbers right and labels left.
- Use consistent visible precision.
- Put units in headers or caption.
- Make sort order clear.
- Keep long text columns readable; do not force every cell to one line.
- Use sticky headers only for long screen tables; disable for print.
- Use subtle row highlighting only when a specific row matters.
- Avoid zebra striping unless row tracking is genuinely difficult.
- Truncate identifiers in the middle and preserve their full value accessibly.
- For long tables, state `Showing 20 of 380` and provide full data or disclosure.
- Do not silently paginate or filter.
- A table scroller must be keyboard reachable and labeled.

---

## 18. Diagrams, flows, and timelines

### 18.1 When to use a diagram

Use a diagram for:

- sequence;
- hierarchy;
- ownership;
- data flow;
- branching decisions;
- state transition;
- spatial relationship;
- component boundaries.

Do not use a diagram merely because a section has multiple bullets.

### 18.2 Diagram language

- Nodes are text and thin rules, not decorative cards.
- Arrows encode actual direction.
- Line style encodes actual state or boundary.
- Group backgrounds remain extremely subtle.
- Every color has a legend or direct label.
- Use left-to-right for process and top-to-bottom on narrow screens.
- Use one short verb on an arrow only when the relationship is ambiguous.
- Keep crossing lines to a minimum.

### 18.3 Flow diagrams

```text
INPUTS → TRANSFORM → REVIEW → OUTPUT
              ↓
           FAILURE
```

- Show missing/error paths.
- Show loops only when real.
- Label conditions at branches.
- End nodes state outcomes.
- Avoid more than five primary steps in one row.

### 18.4 Timelines

- Time flows consistently.
- Use position for time, not equally spaced events unless the sequence is ordinal.
- Event labels contain action and result.
- Use shape/line style for event type.
- Mark gaps and uncertain timestamps.
- Use vertical timelines on narrow screens.

### 18.5 Trees and hierarchies

- Parent-child depth is represented by indentation or branching.
- Sort siblings meaningfully.
- Keep labels concise.
- Do not use radial trees for ordinary documentation.
- If exact ownership matters, accompany with a table.

### 18.6 Wireframes

Wireframes are appropriate for proposed layouts. Keep them structural:

```text
┌───────────────┬──────────────────────────────┐
│ filters       │ main view                    │
│               │                              │
│               ├──────────────────────────────┤
│               │ supporting detail            │
└───────────────┴──────────────────────────────┘
```

Label regions by purpose, not implementation component names unless the report is technical.

---

## 19. Images, screenshots, and media

### 19.1 Images

Use an image when it contributes evidence, context, or explanation. Do not use stock imagery to make a report feel designed.

### 19.2 Screenshots

- Crop to the relevant state.
- Preserve readable resolution.
- Add capture date and context.
- Add a thin border only when the edge disappears into the page.
- Remove device frames, shadows, perspective, and decorative backgrounds.
- Redact secrets and private information.
- Describe the finding outside the screenshot.
- Do not use screenshots for structured data that should be a chart or table.

### 19.3 Image sizing

```css
.report-image {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
}
```

- Never distort aspect ratio.
- Avoid tiny text baked into raster images.
- Prefer SVG for diagrams and charts.
- Use WebP/PNG/JPEG only as appropriate to content.
- Provide useful alternative text.

### 19.4 Galleries

Use a gallery only for a real visual comparison:

- identical crop/aspect when possible;
- consistent captions;
- two columns maximum for detail-heavy screenshots;
- one column on mobile;
- no carousel.

---

## 20. Interaction

### 20.1 Static first

The default rendered state MUST communicate the report without clicks, hover, or scripts.

Useful interactions:

- expand method or source detail;
- reveal chart data;
- inspect exact chart values;
- copy an identifier or path;
- toggle a small number of comparison series;
- filter a catalog or genuinely large evidence set.

Unhelpful interactions:

- entrance animation;
- carousels;
- hidden conclusions;
- hover-only units or labels;
- filters that silently change denominators;
- auto-playing charts;
- drag/zoom with no analytical need;
- sticky visual effects.

### 20.2 Details and summary

Use native disclosure for secondary material:

```html
<details class="disclosure">
  <summary>Method and exclusions</summary>
  <div class="disclosure-body"><!-- content --></div>
</details>
```

- Summary text says what opens.
- Critical conclusions remain outside the disclosure.
- Print mode may force important disclosures open through duplicated print-only content if necessary.

### 20.3 Tooltips

Tooltips must:

- work by focus as well as hover;
- show category, value, and unit;
- remain within the viewport;
- close on Escape;
- not contain the only source or caveat;
- not obscure the selected mark when avoidable.

Direct labels and chart-data tables are preferred for durable reports.

### 20.4 Motion

- Default charts do not animate on load.
- Small state transitions may use `80–140ms`.
- Respect reduced-motion settings.
- Do not animate numbers counting up.
- Do not animate a line being drawn.

---

## 21. Responsive layout

### 21.1 Embedded-viewer reality

Reports may render inside an iframe beside a navigation sidebar. The iframe width, not the outer browser width, controls layout. A “desktop” browser can still provide only `700–900px` to the report.

### 21.2 Breakpoints

```css
@media (max-width: 980px) {
  .layout-rail,
  .layout-main-table { grid-template-columns: minmax(0, 1fr); }
}

@media (max-width: 760px) {
  .report {
    width: min(calc(100% - 32px), var(--width-report));
    padding-block: 20px 48px;
  }
  .layout-pair { grid-template-columns: minmax(0, 1fr); gap: 24px; }
  .header-topline { align-items: flex-start; flex-direction: column; gap: 6px; }
}

@media (max-width: 560px) {
  .metric-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .metric-strip > div:nth-child(2n) { border-right: 0; }
}

@media (max-width: 420px) {
  .metric-strip { grid-template-columns: minmax(0, 1fr); }
  .metric-strip > div { border-right: 0; }
}
```

### 21.3 Mobile rules

- Body text remains at least `14px`.
- Axis text remains at least `10px`.
- Collapse columns; do not uniformly shrink the whole page.
- Reduce tick count before rotating labels.
- Prefer horizontal bars for long category names.
- Increase chart height if labels need space.
- Put tables in contained scrollers.
- Wrap paths and long labels with `overflow-wrap:anywhere` outside tables.
- Keep interactive targets at least `40×40px`.
- Avoid fixed heights for text-bearing elements.
- Do not create page-wide horizontal overflow.

### 21.4 Responsive figures

- SVG uses `viewBox`, `width:100%`, and `height:auto`.
- Raster images use intrinsic aspect ratio.
- Diagrams may switch from horizontal to vertical.
- Legends may wrap but remain ordered.
- Direct labels may move, abbreviate, or become a compact legend.
- Data and interpretation must remain identical across variants.

---

## 22. Accessibility

### 22.1 Semantic document

Every report MUST have:

- one `<main>`;
- one `<h1>`;
- correctly nested headings;
- `<figure>` and `<figcaption>` for visuals;
- semantic tables;
- `<dl>` for label/value facts;
- native interactive controls;
- a meaningful page `<title>`;
- a declared language.

### 22.2 Contrast

- Normal text: at least 4.5:1.
- Large text and essential graphical marks: at least 3:1.
- Primary series should be unmistakable from gridlines.
- Semantic states need redundant text/sign/shape encoding.
- The page’s conclusion should survive grayscale.

### 22.3 Focus

```css
:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}
```

Never remove focus indication without a replacement.

### 22.4 Accessible charts

Every nontrivial chart needs:

1. a visible finding or question;
2. an accessible name;
3. a concise description;
4. a data table or structured textual summary;
5. redundant encoding beyond color.

Inline SVG pattern:

```html
<svg role="img" aria-labelledby="chart-title chart-desc" viewBox="0 0 960 380">
  <title id="chart-title">Monthly completion rate</title>
  <desc id="chart-desc">Completion rose from 68 percent in January to 81 percent in June.</desc>
  <!-- marks -->
</svg>
```

Decorative SVG elements should be hidden from assistive technology.

### 22.5 Reduced motion and forced colors

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

@media (forced-colors: active) {
  .chart-series { stroke: CanvasText; }
  .chart-focus { stroke: Highlight; }
}
```

---

## 23. Print and PDF

Reports SHOULD produce a clean light-background printout.

```css
@media print {
  :root { color-scheme: light; }

  html, body {
    background: #fff !important;
    color: #111 !important;
  }

  .report {
    width: 100%;
    margin: 0;
    padding: 0;
  }

  .report-header { break-after: avoid; }
  figure, table, .callout, .metric-strip { break-inside: avoid; }
  thead { display: table-header-group; }
  .screen-only { display: none !important; }
  .print-only { display: block !important; }
  [style*="position: sticky"] { position: static !important; }
}
```

Print requirements:

- Use light chart colors or a print-specific SVG variant.
- Do not depend on background-color printing.
- Keep figure headings with figures.
- Repeat table headers.
- Avoid orphan headings.
- Remove sticky behavior and interactive controls.
- Expose source references clearly.
- Keep line styles distinguishable in grayscale.
- Test actual PDF output, not only print preview.

---

## 24. Portable HTML

### 24.1 Baseline

Reports SHOULD:

- render without a network connection;
- contain inline CSS;
- use inline SVG for simple charts;
- use embedded or repository-relative assets;
- avoid external fonts and CDNs;
- preserve readable content when JavaScript fails;
- avoid a large framework runtime for static content.

### 24.2 Security

An appropriate strict baseline:

```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none';
           img-src 'self' data: blob:;
           style-src 'unsafe-inline';
           script-src 'unsafe-inline';
           connect-src 'none';
           object-src 'none';
           base-uri 'none';
           form-action 'none'">
<meta name="referrer" content="no-referrer">
```

- Do not embed secrets or credentials.
- Escape inserted text.
- Prefer `textContent` to HTML string interpolation.
- Serialize embedded JSON safely.
- Do not weaken CSP simply to load decorative assets.

### 24.3 Performance

- Aim for under `1 MB` when practical.
- Prefer vector to base64 raster for charts.
- Avoid hundreds of tooltip nodes.
- Avoid rendering thousands of invisible table rows.
- Downsample only when visually necessary; disclose it.
- The title, summary, and primary evidence should render immediately.

### 24.4 Progressive enhancement

Base HTML contains:

- headings;
- conclusions;
- visible values;
- tables or chart summaries;
- sources.

JavaScript may add:

- tooltips;
- disclosures;
- filtering;
- copy actions;
- chart rendering from embedded data.

If enhancement fails, the report remains useful.

---

## 25. Base CSS starter

```css
:root {
  color-scheme: dark;
  --canvas: #000;
  --surface: #080808;
  --surface-2: #101010;
  --ink: #f4f4f4;
  --ink-muted: #b8b8b8;
  --ink-faint: #777;
  --line: #242424;
  --line-strong: #3a3a3a;
  --gridline: #1e1e1e;
  --focus: #67b7ff;
  --positive: #58c978;
  --negative: #ff6b66;
  --warning: #e5b94f;
  --font-text: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-data: "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  --width-copy: 72ch;
  --width-report: 1120px;
}

* { box-sizing: border-box; }

html {
  min-width: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: var(--font-text);
}

body {
  min-width: 0;
  min-height: 100vh;
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font-size: 15px;
  line-height: 1.62;
  text-rendering: optimizeLegibility;
}

img, svg { max-width: 100%; }

a {
  color: var(--focus);
  text-underline-offset: 0.16em;
}

p, ul, ol { max-width: var(--width-copy); }

h1, h2, h3 {
  color: var(--ink);
  text-wrap: balance;
}

.report {
  width: min(calc(100% - 48px), var(--width-report));
  margin-inline: auto;
  padding-block: 28px 64px;
}

.report-section {
  padding-block: 32px;
  border-top: 1px solid var(--line);
}

.muted { color: var(--ink-muted); }
.faint { color: var(--ink-faint); }
.mono { font-family: var(--font-data); }
.num {
  font-family: var(--font-data);
  font-variant-numeric: tabular-nums lining-nums;
}

:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}

@media (max-width: 760px) {
  body { font-size: 14px; }
  .report {
    width: min(calc(100% - 32px), var(--width-report));
    padding-block: 20px 48px;
  }
  .report-section { padding-block: 24px; }
}
```

---

## 26. Full HTML skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <meta name="referrer" content="no-referrer">
  <title>Specific report title</title>
  <style>
    /* Base tokens and components from this guide. */
  </style>
</head>
<body>
  <main class="report">
    <header class="report-header">
      <div class="header-topline">
        <p class="kicker">Report type · Status</p>
        <p class="header-date">Generated YYYY-MM-DD</p>
      </div>
      <h1>Specific report title</h1>
      <p class="deck">Scope, period, subject, and question in one sentence.</p>
      <dl class="header-meta"><!-- compact metadata --></dl>
    </header>

    <section class="report-section" aria-labelledby="read-heading">
      <header class="section-header">
        <h2 id="read-heading">Read</h2>
      </header>
      <p class="report-lead">The shortest complete answer.</p>
      <dl class="metric-strip"><!-- only essential numbers --></dl>
    </section>

    <section class="report-section" aria-labelledby="evidence-heading">
      <header class="section-header">
        <h2 id="evidence-heading">Evidence</h2>
      </header>
      <figure class="report-figure">
        <figcaption class="figure-head">
          <strong>Finding-led figure title.</strong>
          <span>Optional interpretation.</span>
        </figcaption>
        <div class="figure-body"><!-- visual --></div>
        <p class="figure-note">scope · unit · period · method · source</p>
      </figure>
    </section>

    <section class="report-section" aria-labelledby="exceptions-heading">
      <header class="section-header">
        <h2 id="exceptions-heading">Exceptions</h2>
      </header>
      <p>Where the summary does not hold.</p>
    </section>

    <section class="report-section" aria-labelledby="implications-heading">
      <header class="section-header">
        <h2 id="implications-heading">Implications</h2>
      </header>
      <p>What the evidence changes or does not change.</p>
    </section>

    <section class="report-section" aria-labelledby="method-heading">
      <header class="section-header">
        <h2 id="method-heading">Method and caveats</h2>
      </header>
      <ul><!-- method, missingness, limitations --></ul>
    </section>

    <footer class="report-section" aria-labelledby="sources-heading">
      <header class="section-header">
        <h2 id="sources-heading">Sources</h2>
      </header>
      <ol><!-- source paths and reproduction details --></ol>
    </footer>
  </main>
</body>
</html>
```

---

## 27. Writing and labels

### 27.1 Titles

Titles should be specific enough to distinguish the report in a catalog.

Good:

- `Q2 support cycle and resolution quality`
- `Authentication incident review: 2026-07-09`
- `Cross-region model performance under the final holdout`

Weak:

- `Quarterly report`
- `Analysis`
- `Update`

### 27.2 Section headings

Headings should tell readers why the section exists. Prefer `Where delays begin` to `Cycle-time analysis` when the former accurately describes the content.

### 27.3 Figure titles

State a finding when stable; state a question when the evidence is exploratory.

- Stable: `The final stage accounts for most of the slowdown.`
- Exploratory: `Where does the slowdown first appear?`
- Inconclusive: `Regional differences remain unresolved.`

### 27.4 Labels

- Use words readers recognize.
- Keep the same term across text, chart, and table.
- Avoid raw field names in visible labels.
- Preserve raw names in method/source notes when useful.
- Put units next to values or in headers.
- A control label describes its result: `Show full table`, not `More`.

### 27.5 Tone

- Plain, direct, and specific.
- Active voice by default.
- No hype.
- No vague praise or alarm.
- No “interesting” without saying why.
- No “significant” without a statistical or practical definition.
- Empty states explain what is missing and what to do.
- Errors state what failed and how to recover.

---

## 28. Source and method treatment

### 28.1 Local figure provenance

Every important visual has a short source in its caption rail.

```text
1,842 records · Apr–Jun 2026 · weekly median · 94% coverage · source: events.csv
```

### 28.2 Final sources section

For each source, include as applicable:

- human title;
- repository-relative path or canonical URL;
- source type;
- observed period;
- retrieved/generated time;
- transformation or query;
- version, run ID, or checksum;
- known limitations.

### 28.3 Method section

Method should explain:

- population;
- unit of observation;
- inclusion/exclusion;
- missing data;
- aggregation;
- comparison baseline;
- uncertainty;
- transformations;
- reproducibility.

Keep the summary readable without method detail, but do not make the method hard to find.

---

## 29. Anti-patterns

### 29.1 Layout

Do not use:

- a decorative hero;
- nested card grids;
- page-wide body text;
- arbitrary alternating backgrounds;
- large empty gutters with tiny content;
- more than two main content columns;
- sticky internal navigation that competes with the viewer;
- fixed heights around variable text;
- page-wide horizontal scrolling.

### 29.2 Typography

Do not use:

- multiple display fonts;
- ultra-light text on black;
- centered paragraphs;
- uppercase paragraphs or long headings;
- oversized metric values competing with the title;
- tiny captions below `10px`;
- inconsistent numeric precision;
- raw snake_case labels in reader-facing content.

### 29.3 Surface styling

Do not use:

- gradients;
- glows;
- drop shadows;
- glass blur;
- decorative rounded cards;
- fake browser/device frames;
- colored pills for every status;
- arbitrary icons beside every heading;
- background textures.

### 29.4 Charts

Do not use:

- 3D;
- rainbow palettes;
- truncated bar axes;
- unexplained dual axes;
- unlabeled error bars;
- hidden missing data;
- inconsistent scales across compared panels;
- excessive legends;
- smoothed lines hiding raw behavior;
- charts without a question, caption, or source;
- charts when a sentence or table is clearer.

### 29.5 Interaction

Do not use:

- hover-only meaning;
- entrance animation;
- auto-playing content;
- carousels;
- animated counters;
- filters that hide denominator changes;
- essential content behind disclosure;
- custom controls when native HTML works.

---

## 30. Review checklist

### 30.1 Purpose and structure

- [ ] Audience and single job are clear.
- [ ] The title is specific.
- [ ] Scope, period, and status are visible.
- [ ] The first screen contains the main read.
- [ ] Sections follow the reader’s reasoning path.
- [ ] The primary visual is obvious.
- [ ] Exceptions and caveats are easy to find.
- [ ] Sources are attached to evidence.

### 30.2 Layout

- [ ] Body copy remains `58–76ch`.
- [ ] Visuals use the wider container only when useful.
- [ ] Alignment is consistent.
- [ ] Spacing groups related items.
- [ ] Dividers encode real boundaries.
- [ ] No unnecessary cards or panels.
- [ ] No more than one dominant emphasis.
- [ ] The page has no accidental horizontal overflow.

### 30.3 Typography and color

- [ ] Type roles follow the scale.
- [ ] Body is at least `14px`.
- [ ] Numerals are tabular where compared.
- [ ] Visible precision is consistent.
- [ ] Neutral colors carry most structure.
- [ ] Focus color is used sparingly.
- [ ] Semantic color has redundant encoding.
- [ ] Contrast passes.
- [ ] The main conclusion survives grayscale.

### 30.4 Figures

- [ ] Every figure answers one question.
- [ ] Figure title states a finding or honest question.
- [ ] Visual type matches the relationship.
- [ ] Axes and units are clear.
- [ ] Baseline or zero is visible where relevant.
- [ ] Labels are readable without excessive legend lookup.
- [ ] Uncertainty is defined when shown.
- [ ] Missingness/exclusions are stated.
- [ ] Caption rail includes scope, method, and source.
- [ ] Nontrivial charts have a table or textual alternative.

### 30.5 Tables

- [ ] Caption and scoped headers exist.
- [ ] Numbers align right.
- [ ] Labels align left.
- [ ] Units and sort order are clear.
- [ ] Long tables disclose shown/total rows.
- [ ] Overflow is contained and keyboard accessible.
- [ ] Print repeats table headers.

### 30.6 Responsive and accessible

- [ ] Checked at `1280`, `900`, `760`, `560`, and `360px` iframe widths.
- [ ] Columns collapse logically.
- [ ] Chart labels remain readable.
- [ ] Tables scroll locally.
- [ ] Keyboard focus is visible.
- [ ] Heading order is valid.
- [ ] No essential information is hover-only.
- [ ] Reduced motion is respected.
- [ ] Forced colors and grayscale remain understandable.

### 30.7 Portable and print

- [ ] Works without external network access.
- [ ] Main content survives JavaScript failure.
- [ ] No secrets or credentials are embedded.
- [ ] Assets are self-contained or repository-relative.
- [ ] Print uses a legible light palette.
- [ ] Figures do not split badly.
- [ ] Source paths remain visible.
- [ ] PDF output was inspected.

---

## 31. Acceptance standard

A successful report answers these questions almost immediately:

1. What is this report about?
2. What period and scope does it cover?
3. What is the main finding?
4. What visual evidence supports it?
5. What are the exceptions or limitations?
6. What should the reader do with the result?
7. Where did the evidence come from?

The page should feel calm at first glance and dense on inspection. Its design should disappear while reading but become obvious when removed: the alignments make comparison effortless, the spacing explains grouping, the type reveals hierarchy, the caption rails keep evidence grounded, and the charts show relationships that prose alone would obscure.

That is the house standard: minimal, not empty; dense, not cramped; polished, not decorated; visual, not theatrical.


## 6. Complete ML source system

The following part is preserved in full from `report-design-ml.md`. Repository-specific paths and market conventions retain their original context. Where it conflicts with Sections 1–4 above, the selected profile and resolved defaults control.

# Research Report Design Standard

This document is the default visual specification for research HTML reports in this repository. It is intentionally prescriptive and dense so a report can be designed without asking what “looks right” each time.

The goal is not decoration. The goal is to make alpha evidence fast to scan, hard to misread, and easy to audit. Every visual should help answer whether an edge exists, survives costs, and deserves a stricter forward test.

## 1. Non-negotiable defaults

Unless a task explicitly says otherwise:

- Use a pure-black research canvas with near-white text and quiet neutral structure.
- Render every chart, heatmap, image, and major table **one per row at the full available report width**.
- Never use side-by-side chart grids, thumbnail galleries, or `max-width` caps that shrink plots.
- Use a single-column report flow. Text can have a readable line length, but the chart immediately below it must still use the full available width.
- Prefer a small number of strong charts over a dashboard of tiny panels.
- Give every chart a descriptive title, an assumptions-rich subtitle, visible units, and a nearby interpretation.
- Use color to encode data, never merely to decorate a report.
- Use blue for favorable/positive magnitude, red for adverse/negative magnitude, orange for marginal or warning territory, and grey for neutral/near-zero/not-applicable states.
- Do not use red-versus-green as the default performance encoding. It is less accessible and visually harsher than the current blue-versus-red system.
- Keep grid lines, borders, axes, and card chrome quiet. Data marks and labels should dominate.
- Make charts clickable to expand into a near-full-screen black modal when the report is interactive.
- Preserve an exact data table or inspectable tooltip for every chart when practical.
- Never let a dense parameter surface imply more independent evidence than exists. Display unique markets, trades, sample size, and evidence level near the visual.
- Active Solana Up/Down reporting is 5-minute only. Do not mix legacy 15-minute results into a current report.

## 2. Visual character

The intended look is technical, sparse, and high-contrast:

- Pure black page, not blue-black or charcoal.
- Flat surfaces with minimal shadows.
- Fine neutral borders rather than heavy card outlines.
- System sans-serif for prose and labels.
- Monospace/tabular numerals for values, timestamps, bps, prices, PnL, counts, and identifiers.
- Compact headings, generous vertical separation between ideas, and wide visual footprints.
- Saturated color only inside data marks, heatmap cells, status accents, or the active interaction target.
- No gradients in chart marks, glossy effects, glassmorphism, 3D charts, background textures, ornamental illustrations, or arbitrary colored containers.
- Rounded corners are allowed for metric cards and dialogs, but charts themselves should feel flat and rectangular.

The report should feel like an evidence terminal that is comfortable to read for a long session, not like a marketing site.

## 3. Canonical dark tokens

Use these tokens as the default screen theme. They match the strongest current report treatment.

```css
:root {
  color-scheme: dark;

  /* Canvas and surfaces */
  --report-canvas: #000000;
  --report-surface: #070707;
  --report-surface-subtle: #0d0d0d;
  --report-surface-raised: #111111;

  /* Type */
  --report-ink: #f2f2f2;
  --report-muted: #c9c9c9;
  --report-tertiary: #a9a9a9;
  --report-table-text: #d2d2d2;

  /* Structure and interaction */
  --report-border: rgba(255, 255, 255, 0.13);
  --report-border-quiet: rgba(255, 255, 255, 0.07);
  --report-grid: rgba(255, 255, 255, 0.10);
  --report-grid-strong: rgba(255, 255, 255, 0.20);
  --report-accent: #8ac5ff;
  --report-focus: #8ac5ff;

  /* Semantic state; do not automatically use these as chart series colors */
  --report-pass: #79d996;
  --report-pass-bg: rgba(64, 180, 99, 0.16);
  --report-fail: #ff8583;
  --report-fail-bg: rgba(224, 74, 70, 0.16);
  --report-warning: #e7b84b;
  --report-warning-bg: rgba(231, 184, 75, 0.14);

  /* Geometry */
  --report-radius: 12px;
  --report-card-radius: 16px;
  --report-content-pad: clamp(18px, 2.5vw, 40px);
  --report-section-gap: 32px;
}
```

Rules:

- Page background is `#000000`.
- Use `#070707` or `#0d0d0d` only when a surface needs separation from the canvas.
- Primary text is `#f2f2f2`; secondary copy is `#c9c9c9`; metadata and quiet labels are `#a9a9a9`.
- Borders should usually be 1 px at 7–13% white opacity.
- Do not use a shadow when a border or spacing boundary is sufficient.
- Links and keyboard focus use `#8ac5ff`.
- Keep the number of simultaneous non-neutral colors low.

### Print tokens

Print/PDF should switch to a light theme for legibility and ink use. Preserve the same hierarchy and data semantics.

```css
@media print {
  :root {
    color-scheme: light;
    --report-canvas: #ffffff;
    --report-surface: #ffffff;
    --report-surface-subtle: #f7f7f7;
    --report-ink: #0d0d0d;
    --report-muted: #5d5d5d;
    --report-tertiary: #767676;
    --report-table-text: #3f3f3f;
    --report-border: rgba(13, 13, 13, 0.12);
    --report-grid: rgba(13, 13, 13, 0.10);
  }
}
```

Do not make a screen capture of the dark report and drop it into a PDF. Render a true print variant with readable labels and retained cell distinctions.

## 4. Typography and numeric formatting

### Font stack

```css
--font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
```

Use sans-serif for titles, prose, axis labels, legends, and annotations. Use monospace or `font-variant-numeric: tabular-nums` for numeric columns, tooltip values, data labels, prices, timestamps, bps, ROI, PnL, and counts.

### Type scale

- Page title: `clamp(24px, 3vw, 40px)`, weight 600, line height 1.1–1.2.
- Section heading: 20–24 px, weight 600, line height 1.2.
- Chart title: 16–18 px, weight 550–600, line height 1.3.
- Chart subtitle: 12–14 px, weight 400, muted.
- Body: 14–16 px, line height 1.55–1.7.
- Axis and legend: 11–13 px.
- Metadata/source/caveat: 11–12 px.
- KPI value: 24–32 px, weight 600, tabular numerals.

Avoid light font weights on the black background. Avoid all-caps except for short eyebrow labels, statuses, and compact table headers. Never shrink text below 11 px to make a chart fit; give the chart more space instead.

### Number formatting

- Show the unit in the axis title, subtitle, column header, or value suffix.
- Use consistent precision inside a comparison: `18.97%`, not a mixture of `19%`, `18.970%`, and `0.1897`.
- Default precision: price 2–4 decimals as appropriate; probability 1–2 percentage points; ROI/PnL rate 1–2 decimals; bps 1–2 decimals; counts no decimals.
- Use a true minus sign if the renderer supports it; always show a sign on signed return/PnL labels when that makes direction easier to scan.
- Prefer `$10`, `$0.02`, `39.49%`, `18.97 bps`, `15 trades`, and `22 markets` over unlabeled bare numbers.
- Use `—` for unavailable, `N/A` for not applicable, and an explicit `0` only for a real measured zero.
- Do not round away the sign of a small value. If needed, show `<0.01` or add precision.

## 5. Page and chart layout

### Page flow

The default report sequence is:

1. Title and one-sentence scope.
2. Executive summary with the decision, strongest evidence, and main disqualifier.
3. Compact assumptions/evidence strip.
4. Repeating evidence sections: question → chart → read → caveat.
5. Exact results table where useful.
6. Next experiments.
7. Caveats, evidence level, and decision.
8. Sources/provenance.

Charts must be placed immediately after the text that frames their analytical question. Do not collect charts into a detached gallery.

### Width and columns

```css
.report {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0 var(--report-content-pad) 56px;
  background: var(--report-canvas);
}

.report-stack {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: var(--report-section-gap);
  width: 100%;
  max-width: none;
}

.chart-panel,
.heatmap-panel,
.report-table {
  grid-column: 1;
  width: 100%;
  max-width: none;
  min-width: 0;
}

.prose {
  max-width: 86ch;
}
```

Never use this for report charts:

```css
/* Forbidden for report visuals */
.charts { grid-template-columns: repeat(2, 1fr); }
.chart { max-width: 768px; }
.gallery { display: flex; flex-wrap: wrap; }
```

Text may be kept to 78–86 characters for readability. Visuals do not inherit that cap.

### Spacing

- 24–40 px page side padding on desktop.
- 16–24 px page side padding on small screens.
- 32–48 px between major evidence sections.
- 14–18 px between chart title/subtitle and plot.
- 16–24 px between plot and its interpretation/caption.
- 4–6 px between heatmap cells when cells are large; 1–3 px when the matrix is dense.
- Minimum heatmap cell height: 44 px in-report; 64 px in expanded view.

Whitespace separates ideas. Card borders should not be used to compensate for poor spacing.

### Chart height

Do not force all charts into one fixed aspect ratio.

- Simple bar/line chart: usually 420–620 px desktop height.
- Dense multi-series chart: 560–760 px.
- Heatmap: derive height from row count; aim for 44–64 px per row plus headers.
- Expanded modal: at least 70 vh of plot area, up to roughly 94 vh overall.
- On mobile, allow vertical growth and horizontal scrolling for intrinsically wide matrices instead of crushing labels.

## 6. Required chart anatomy

Every chart should have these elements in this order:

1. **Neutral descriptive title** — what is plotted.
2. **Subtitle** — scope, time range, grain, sample size, fixed assumptions, and unit.
3. **Plot** — full width with readable axes.
4. **Legend** only if it adds information not already visible from direct labels or axis categories.
5. **Read** — one to three sentences explaining the supported takeaway.
6. **Caveat/evidence label** — proxy-only, backtest, paper-traded, fillable, live-filled, or settlement-backed.
7. **Source/inspection affordance** — source label, tooltip, and/or expandable exact data table.

Recommended wording:

```text
Title: Spot-trend ROI by budget and entry time
Subtitle: SOL 5m · 22 resolved markets · max 10s quote offset · $0.02/contract fee stress
Read: The 180-second peak persists across displayed budgets, but all cells reuse the same small event set.
Evidence: Executable-depth replay; no queue position, rejects, latency, or official-settlement verification.
```

Do not use a clever headline that overstates the result. Put interpretation in the `Read` paragraph. “This rule makes money” is not a neutral chart title; “Net PnL by entry rule and split” is.

## 7. Choosing the chart

Use the simplest form that matches the comparison.

| Analytical question | Default chart | Notes |
|---|---|---|
| How did a metric move through time? | Line | Aim for at least 8–12 time points. |
| Which rule/category is larger? | Sorted horizontal bar | Start at zero for absolute magnitudes. |
| How do validation and test compare? | Grouped bar or dot plot | Keep one scale and fixed category ordering. |
| How is a sample split across Up/Down or states? | Stacked bar | Show both count and percentage when concentration matters. |
| What is the distribution of trade PnL? | Histogram | Show zero, median, tails, and sample size. |
| How do distributions differ by rule/regime? | Box plot plus points or small-multiple histogram | Do not hide tiny samples behind a box. |
| Is one numeric feature associated with another? | Scatter | Aim for 12–20+ comparable observations; label outliers. |
| Which two-parameter regions work? | Heatmap | Show counts and fixed assumptions; control multiple-testing interpretation. |
| How does PnL accumulate by trade? | Equity/cumulative PnL line | Add drawdown or loss markers only if readable. |
| What explains a start-to-end change? | Waterfall | Use only when components add cleanly. |
| How concentrated is PnL? | Ranked bar/Pareto | Show top trade/day/market share. |
| What is the exact audit record? | Table | Use when exact lookup matters more than shape. |

### Chart-specific rules

#### Lines

- Use a line only for an ordered continuous axis, usually time.
- Keep the raw observation grain clear.
- Use 2 px as the default focal stroke; 1–1.5 px for context lines.
- Add markers only when points are sparse or each observation matters.
- Direct-label line ends when possible.
- Use dashed neutral lines for benchmarks, zero, 50% probability, or calibration ideals.
- Do not smooth financial or trading series unless the smoothed series is explicitly labeled and the raw series remains available.

#### Bars

- Standard magnitude bars start at zero.
- Sort descending unless order is temporal, ordinal, or semantically fixed.
- Use horizontal bars for long rule names.
- One measure across categories normally uses one color. Highlight a single focal category only when the narrative requires it.
- Do not assign a different rainbow color to every bar.
- Put exact values at bar ends when the labels fit.
- Signed bars must show a strong zero line and reserve space on both sides.

#### Scatter plots

- Use observations at one consistent grain; do not mix totals and individual markets.
- X and Y must share population, filters, and time window.
- Show `n`, and retain a volume/sample-size field for tooltip reliability checks.
- Use size only if a third variable materially changes the interpretation.
- Label outliers or a small number of decision-relevant points, not every point in a dense cloud.
- Add a regression line only when the model and uncertainty are relevant; never use it as decoration.

#### Histograms and distributions

- Use stable, interpretable bin boundaries.
- Mark zero, median, and any cost hurdle.
- Do not hide losing tails with a truncated domain.
- If wins are extremely skewed, show a log or symlog companion view and label the transform prominently.
- Report median, mean, max loss, and concentration rather than relying on the picture alone.

#### Stacked composition

- Use no more than five meaningful categories.
- Keep stack order consistent across panels.
- For Up/Down, preserve the same color mapping everywhere.
- If exact cross-category comparison is more important than composition, use grouped bars instead.

## 8. Color system for charts

### Palette policy

Choose one palette policy per chart:

- **Single-root preferred:** one non-neutral color plus shades and neutral references. Default for simple lines, bars, distributions, scatters, and rankings.
- **Two-root cap:** at most two non-neutral roots plus neutrals. Default for signed values, Up/Down, focal-versus-context, validation-versus-test, and benchmark comparisons.
- **Multi-category exception:** up to five roots when category identity is the actual analytical point. Group additional categories into `Other` or change the chart.

### Approved roots

```css
--chart-blue-xlight: #e0f2fe;
--chart-blue-light:  #7dd3fc;
--chart-blue:        #38bdf8;
--chart-blue-mid:    #0284c7;
--chart-blue-dark:   #075985;

--chart-red-xlight:  #fee2e2;
--chart-red-light:   #fca5a5;
--chart-red:         #ef4444;
--chart-red-mid:     #b91c1c;
--chart-red-dark:    #7f1d1d;

--chart-orange-light:#fdba74;
--chart-orange:      #f97316;
--chart-orange-dark: #9a3412;

--chart-gold:        #eab308;
--chart-olive:       #84cc16;
--chart-pink:        #ec4899;

--chart-neutral-light:#a1a1aa;
--chart-neutral:      #52525b;
--chart-neutral-dark: #27272a;
```

The default multi-category order is blue, gold, orange, olive, pink. Do not introduce purple, teal, or arbitrary library defaults unless a task has a concrete semantic need.

### Semantic mapping

- Positive return/edge/ROI: blue.
- Negative return/loss/adverse slippage: red.
- Marginal, fragile, warning, or near-threshold: orange.
- Near zero: neutral grey.
- Benchmark/reference/ideal line: dark or light neutral, usually dashed.
- Passed validation/status: green may be used in a badge or small status mark, not as the default positive data scale.
- Failed validation/status: red may be used in a badge, but do not confuse a status color with a quantitative magnitude scale.
- Missing data: near-black or hatched neutral with `—`; never map missing to zero.
- No eligible trades: separate state from missing data and real zero.

### Stable series mappings

Within one report, the same entity must keep the same color, marker, and order everywhere. If `Up` is blue in one chart it cannot become orange in another. Define the mapping once in code rather than relying on a chart library’s implicit category order.

Example:

```ts
const SERIES = {
  up: { color: "#38bdf8", lineStyle: "solid", marker: "circle" },
  down: { color: "#f97316", lineStyle: "solid", marker: "square" },
  validation: { color: "#7dd3fc", fillOpacity: 0.55 },
  test: { color: "#0284c7", fillOpacity: 1 },
  benchmark: { color: "#a1a1aa", lineStyle: "dashed" },
};
```

Never depend on color alone. Pair color with direct labels, ordering, marker shape, open versus filled marks, or line style.

## 9. Heatmaps

Heatmaps are a first-class report form for parameter surfaces, timing × rule comparisons, regime matrices, feature correlation, confusion/calibration matrices, and dense condition atlases.

### When to use a heatmap

Use a heatmap when:

- Both axes are meaningful dimensions or ordered parameter values.
- The reader needs to see regions, ridges, cliffs, instability, or isolated pockets.
- There are enough cells for spatial pattern to matter.
- A table would be slower to scan and a scatter would obscure the matrix structure.

Do not use a heatmap when:

- One axis has only one meaningful value.
- There are fewer than roughly 8 useful cells and exact comparison is easier with bars or a table.
- Cell sample sizes differ wildly and cannot be shown.
- The surface is mostly missing values.
- The apparent pattern comes from tuning on the same few markets without a clear multiple-testing warning.

### Matrix construction

- X-axis should usually be the dimension read left-to-right: time to close, threshold, horizon, or budget.
- Y-axis should be the dimension read top-to-bottom: rule, regime, side, fee stress, or second threshold.
- Sort ordered parameters numerically, not lexicographically (`30s, 60s, 120s`, not `120s, 30s, 60s`).
- Preserve semantic category order where one exists; otherwise order by a stable rule defined before looking at the result.
- Do not reorder rows independently for each heatmap if panels are meant to be compared.
- Use square-ish cells when dimensions are symmetric; use rectangular cells when labels or the number of columns require it.
- Keep cell geometry identical across directly comparable heatmaps.

### Scale types

Choose the scale from the metric semantics, not from which palette looks best.

#### Diverging scale

Use for signed ROI, signed PnL, signed bps, residuals, forecast error, and differences from a benchmark.

- The semantic center is normally exactly zero.
- Negative is red, near-zero is grey, positive is blue.
- Use symmetric limits around zero when comparing positive and negative magnitude is the point.
- Use asymmetric fixed thresholds only when the thresholds have explicit trading meaning and are documented.
- Do not let a single outlier wash out the entire surface; use robust limits or threshold bins and preserve the exact outlier value in the label/tooltip.

Current preferred nine-step diverging palette:

```css
--heatmap-1: #7f1d1d;
--heatmap-2: #b91c1c;
--heatmap-3: #ef4444;
--heatmap-4: #f97316;
--heatmap-5: #52525b;
--heatmap-6: #38bdf8;
--heatmap-7: #0284c7;
--heatmap-8: #0369a1;
--heatmap-9: #075985;
```

Current default ROI/bps thresholds when a fixed trading interpretation is useful:

| Value | Fill |
|---:|---|
| `<= -50` | `#991b1b` / deep red |
| `(-50, -25]` | `#ef4444` / red |
| `(-25, -5]` | `#f97316` / orange |
| `(-5, 0]` | `#52525b` / neutral grey |
| `(0, 15)` | `#38bdf8` / light blue |
| `[15, 30)` | `#0284c7` / medium blue |
| `>= 30` | `#075985` / deep blue |

These thresholds are defaults, not universal truths. Change them when the metric’s economically meaningful breakpoints differ, and state the new thresholds in the legend or subtitle. Comparable panels must use the same thresholds.

#### Sequential scale

Use for non-negative quantities such as volume, opportunity size, absolute move, trade count, depth, latency, or sample coverage.

- Use light-to-dark blue for “more”.
- Use light-to-dark red only when “more” is uniformly worse, such as reject rate or drawdown magnitude.
- Start from a meaningful zero or minimum.
- Never use a diverging scale for a quantity that cannot be negative.

Preferred blue sequential anchors:

```text
#e0f2fe → #7dd3fc → #38bdf8 → #0284c7 → #075985
```

Preferred adverse red sequential anchors:

```text
#fee2e2 → #fca5a5 → #f87171 → #dc2626 → #991b1b → #7f1d1d
```

#### Categorical matrix

If cells are states rather than magnitudes—`pass`, `fail`, `pending`, `missing`—use a small categorical palette and explicit text/icons. Do not imply continuous distance between categories.

### Domain and normalization

- For a family of comparable heatmaps, calculate one shared domain from the combined comparison set.
- For a standalone exploratory heatmap, robust limits may use the 2nd–98th or 5th–95th percentiles, but the caption must disclose clipping.
- Never normalize each row or column independently unless the question specifically concerns within-row/within-column relative shape. Label that normalization prominently.
- Never compare colors across panels that use different domains without visibly separate legends.
- If a value is capped for color, the cell label and tooltip still show the uncapped value.

### Cell labels

Default to exact labels inside cells when the matrix is small enough:

- ROI/PnL rate: signed percentage.
- Return: signed bps.
- Count: integer, optionally prefixed by `n=` in a secondary line.
- Two-line cell: primary metric large; sample size or trade count small.

Example cell:

```text
+39.49%
n=15 · 14W/1L
```

Cell text must switch between near-white and near-black based on fill luminance. Add a subtle keyline when adjacent cells have similar colors. Do not use tiny text to force all statistics into the cell; move secondary details to the tooltip.

### Missing, empty, and unreliable cells

Treat these states separately:

- Real zero: neutral quantitative color with `0.00`.
- No eligible trades: dark neutral with `n=0`.
- Missing/not collected: near-black or hatched with `—`.
- Insufficient sample: retain the quantitative fill but add a visible low-confidence cue such as an outline, dot, hatch, or reduced saturation; include `n`.
- Invalid combination: black/transparent with `N/A`.

Never color `n=0` as profitable because a computed ROI defaulted to zero.

### Heatmap tooltips

Hover/focus should show enough evidence to audit a cell:

```text
Rule: Spot trend
Entry: 180s to close
Budget: $10
Max quote offset: 10s
Fee stress: $0.02 / contract
Trades: 15
Unique markets: 15
Wins / losses: 14 / 1
PnL: +59.23 USDC
ROI: +39.49%
Max loss: -0.61 USDC
Evidence: executable-depth replay
```

Tooltips must be keyboard-focusable, remain within the viewport, and never be the only place that units or sample size exist.

### Heatmap legends

- Place a compact horizontal legend above or below the plot.
- Show exact endpoints, zero, and economically meaningful thresholds.
- Label the metric and unit directly in the legend.
- If thresholds are discrete, draw discrete swatches rather than a continuous gradient.
- If cells are clipped to robust limits, label the end bins `≤` and `≥`.

### Heatmap interpretation rules

- Favor broad stable regions over isolated best cells.
- Explicitly call out cliffs where a small parameter change flips the sign.
- Compare neighboring cells, not only the maximum.
- Display the number of parameter combinations searched and the number of unique underlying markets.
- Treat repeated cells built from the same events as correlated evidence.
- Mark the selected/frozen rule with a restrained outline or glyph; do not recolor it and destroy the shared scale.
- If a surface is discovery-only, say so above or below the heatmap.
- If a forward/paper cell contradicts the discovery peak, show that contradiction prominently rather than hiding it in prose.

### Reference heatmap color function

```ts
function signedPerformanceColor(value: number | null): string {
  if (value == null || !Number.isFinite(value)) return "#0d0d0d";
  if (value >= 30) return "#075985";
  if (value >= 15) return "#0284c7";
  if (value > 0) return "#38bdf8";
  if (value > -5) return "#52525b";
  if (value > -25) return "#f97316";
  if (value > -50) return "#ef4444";
  return "#991b1b";
}
```

Use a numeric encoding for the metric even if the renderer’s heatmap API calls the visual channel `color`. Do not accidentally declare a numeric ROI field as nominal/categorical.

## 10. Titles, subtitles, annotations, and reads

### Title pattern

`[Metric] by [comparison dimension(s)]`

Examples:

- `ROI by side rule and entry time`
- `Average net SOL return by model lane and split`
- `Trade count and side mix by frozen rule`
- `Quote disagreement by venue and quote asset`
- `Maximum executable size by price and seconds to close`

### Subtitle pattern

`[Market/instrument] · [time range or snapshot] · [sample/grain] · [cost/fill assumptions] · [evidence level]`

Examples:

```text
SOL 5m Up/Down · Jun 15 replay · 22 resolved markets · $10 VWAP · $0.02/contract fee stress
Binance SOLUSDT 5m · 47,375 rows · 4 bps round trip · directional spot proxy only
Polymarket asks · 100 frozen markets · accepted paper orders · exact fees and official settlement
```

### Annotations

- Use annotations only for a decision-relevant peak, failure, break, outlier, threshold, or benchmark.
- Keep annotation text under roughly two short lines.
- Attach it to the evidence with a quiet neutral connector.
- Do not annotate every bar or point.
- Use exact values in the annotation when the claim depends on magnitude.
- A selected-rule outline is preferable to a starburst, glow, or different color scale.

### “Read” paragraph

Every major chart should be followed by a concise interpretation:

```text
Read: [supported pattern]. [important comparison or instability]. [what this permits or rules out].
```

Good:

> Read: The 180-second spot-trend region is positive across displayed budgets, but the result reuses the same 22 events and the promoted paper slice later lost. Keep it as a frozen hypothesis, not a capital rule.

Bad:

> This amazing chart clearly proves the strategy works.

## 11. Evidence and trading context inside visuals

A visually strong chart is still misleading if it omits trading reality. Include the following in the subtitle, caption, annotation, or adjacent evidence strip as relevant:

- Data source and time range.
- Observation grain.
- Trade count and unique market count.
- Entry rule and side rule.
- Entry timing and quote-age tolerance.
- Selected contract price or full VWAP.
- Budget/size.
- Fees.
- Slippage/price impact.
- Depth assumption.
- Wins and losses.
- PnL and ROI.
- Maximum loss/drawdown.
- Concentration by trade, market, day, side, or regime.
- Evidence level: proxy-only, backtest, paper-traded, fillable, live-filled, or settlement-backed.

Do not put all of this into the visual title. Use the subtitle, tooltip, compact metadata strip, and exact data table.

Recommended evidence badge vocabulary:

```text
PROXY ONLY
BACKTEST — NO DEPTH
EXECUTABLE-DEPTH REPLAY
PAPER — QUOTE OBSERVED
PAPER — ACCEPTED FILL
LIVE FILLED
OFFICIAL SETTLEMENT VERIFIED
```

Status badges describe evidence quality, not whether a chart is profitable.

## 12. Tables and KPI strips adjacent to charts

Use a chart for shape and a table for exact lookup. The underlying chart table should retain more than bare `x`, `y`, and `series` columns when audit context exists.

### KPI strip

Keep KPI strips compact and decision-relevant. Typical fields:

- Unique markets.
- Trades.
- W–L.
- Net PnL.
- ROI.
- Max loss/drawdown.
- Largest-trade/day share.
- Evidence level.

Do not make one KPI card per trivial metric. Four to eight cards is usually enough. Use neutral cards; reserve colored backgrounds for a small status badge.

### Tables

- Full available width, one per row.
- Sticky header for long tables.
- Left-align text; right-align numeric cells.
- Use tabular numerals.
- Preserve units in headers.
- Use subtle row separators, not a heavy border around every cell.
- Freeze important identity columns if horizontal scrolling is necessary.
- Default to a decision-relevant sort and state it.
- Use blue/red text sparingly for signed values; retain the `+`/`−` sign.
- Add the exact source path or dataset identifier near the table.
- Do not dump thousands of raw rows into the main report; provide a filtered table or downloadable local artifact when necessary.

## 13. Interaction

Interaction should improve inspection without becoming required to understand the result.

### Required where feasible

- Hover and keyboard-focus tooltips.
- Click-to-expand chart/heatmap modal.
- Close modal by button, `Escape`, or backdrop click.
- Preserve chart state and return it to the original location when the modal closes.
- Exact-data disclosure or table.
- Visible focus ring.

### Expanded modal

```css
.chart-dialog {
  width: min(96vw, 1800px);
  max-width: none;
  height: min(94vh, 1200px);
  padding: 48px 18px 18px;
  border: 1px solid #555;
  background: #000;
  color: #eee;
}

.chart-dialog::backdrop {
  background: rgba(0, 0, 0, 0.88);
}

.chart-dialog-content {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.chart-dialog-content > *,
.chart-dialog-content svg {
  width: 100% !important;
  max-width: none !important;
  height: auto !important;
}
```

The cursor may be `zoom-in` over an expandable chart. Do not trigger expansion when the user clicks a link, button, table disclosure, or source tooltip inside the panel.

### Avoid

- Animation that delays reading.
- Auto-playing transitions.
- Hover-only essential facts.
- Dragging as the only way to see an axis range.
- Cross-filter systems or dashboard infrastructure for a static research question.
- Remote script dependencies in a portable local HTML report.

## 14. Responsive behavior

- Charts remain one per row at every viewport size.
- At 760–820 px and below, reduce page padding and allow titles to wrap.
- Do not reduce axis labels to unreadable sizes.
- For wide heatmaps, prefer a labeled horizontal scroll container or a deliberate stacked/mobile representation.
- Keep Y-axis labels visible while horizontally scrolling if practical.
- Legends wrap into multiple lines above/below the plot.
- Tooltips portal to a fixed bottom sheet or viewport-safe overlay on touch devices.
- Expanded charts should use the entire available viewport.
- Test at approximately 390 px mobile width, 768 px tablet width, 1440 px laptop width, and a wide desktop.

## 15. Portable artifact chart contract

When a report is built from the repository’s artifact/builder workflow, keep visual intent explicit in the artifact rather than patching arbitrary colors after generation.

Example:

```ts
const chart = {
  id: "signal_entry",
  title: "ROI by side rule and entry time",
  subtitle:
    "SOL 5m · $10 budget · max 10s quote offset · $0.02/contract fee stress · 22 resolved markets",
  type: "heatmap",
  intent: "comparison",
  question: "Which entry-time and side-rule regions retain positive ROI after modeled costs?",
  rationale: "A matrix exposes broad regions and unstable isolated cells better than a ranked table.",
  dataset: "signal_entry",
  sourceId: "depth_grid",
  encodings: {
    x: { field: "entry_seconds", type: "ordinal", label: "Seconds to close" },
    y: { field: "signal_rule", type: "nominal", label: "Side rule" },
    color: { field: "roi_pct", type: "quantitative", label: "ROI", unit: "%" },
  },
  valueFormat: "number",
  unit: "%",
  layout: "full",
  comparisonContext: {
    grain: "entry-time and side-rule parameter cell",
    denominator: "eligible executable-depth replay trades",
    unit: "percent return on modeled spend",
  },
  surface: {
    surface: "card",
    showControls: false,
    viewMode: "visualization",
  },
};
```

Artifact rules:

- Use `layout: "full"` for every report chart.
- Use a numeric/quantitative encoding for numeric color metrics.
- Include `question`, `rationale`, and `comparisonContext` when supported.
- Keep chart datasets rich enough for exact inspection and tooltips.
- Use explicit source metadata and local paths.
- Do not bolt on a second remote chart runtime.
- Package the report so it remains useful offline.
- If final CSS overrides are required, keep them small, named, and idempotent.

## 16. Canonical full-width dark override

For generated portable reports that otherwise inherit narrower defaults, this is the intended override shape:

```css
:root {
  color-scheme: dark !important;
  --portable-canvas: #000 !important;
  --portable-surface: #070707 !important;
  --portable-surface-subtle: #0d0d0d !important;
  --portable-ink: #f2f2f2 !important;
  --portable-muted: #c9c9c9 !important;
  --portable-tertiary: #a9a9a9 !important;
  --portable-table-text: #d2d2d2 !important;
  --portable-border: rgba(255, 255, 255, 0.13) !important;
  --portable-accent: #8ac5ff !important;
}

html,
body {
  background: #000 !important;
  color: #f2f2f2 !important;
}

.portable-fallback,
.portable-block-stack,
.portable-content-card,
.portable-static-chart,
.report-content-grid,
.analytics-layout-canvas {
  width: 100% !important;
  max-width: none !important;
}

.portable-block-stack {
  grid-template-columns: minmax(0, 1fr) !important;
}

.portable-layout-half,
.portable-layout-full {
  grid-column: 1 !important;
}

.portable-static-chart-light {
  display: none !important;
}

.portable-static-chart-dark {
  display: block !important;
}
```

Do not blindly paste this into unrelated third-party documents. It is the repository research-report default.

## 17. Accessibility and perceptual QA

- Text and meaningful labels must meet reasonable contrast on their actual background.
- Every color distinction must have a non-color companion: sign, label, line style, marker shape, ordering, hatch, or outline.
- Keyboard users must reach tooltips, disclosures, and dialog controls.
- Dialogs need an accessible name and must return focus on close.
- Charts need a meaningful accessible label or nearby text summary.
- Exact data should be available as a semantic table when practical.
- Avoid red/green-only distinctions.
- Test heatmap label contrast at every palette step.
- Test grayscale: the takeaway should remain recoverable from labels, signs, and structure.
- Do not encode magnitude with line thickness.
- Keep benchmark and zero lines visible but subordinate to marks.
- Check that labels do not clip at 125–200% browser zoom.

## 18. Final visual QA checklist

Before shipping an HTML report, verify all of the following.

### Analytical integrity

- [ ] Each chart answers a stated analytical question.
- [ ] Chart type matches the comparison.
- [ ] Data source, time range, grain, and filters are correct.
- [ ] Units and denominators are visible.
- [ ] Trade count and unique market count are not conflated.
- [ ] Fees, slippage, price, size, and depth assumptions are stated where relevant.
- [ ] Wins, losses, PnL, ROI, max loss/drawdown, and concentration are available where relevant.
- [ ] Evidence level is explicit.
- [ ] Proxy/backtest output is not described as fillable or live.
- [ ] A parameter search discloses the search count and correlated/reused samples.

### Layout

- [ ] Every chart/image/heatmap is one per row.
- [ ] Every visual uses the full available width with no shrinking max-width cap.
- [ ] No thumbnail gallery or side-by-side visual grid exists.
- [ ] Chart height fits its row count and label density.
- [ ] Prose is readable but does not constrain visual width.
- [ ] Mobile layout stays single-column.

### Color and scales

- [ ] Colors come from an explicit declared palette.
- [ ] The chart uses one root, two roots, or a justified five-root maximum.
- [ ] Same entity keeps the same mapping across the report.
- [ ] Signed performance uses red → grey → blue with a true zero center.
- [ ] Sequential metrics use a sequential scale.
- [ ] Missing, `n=0`, invalid, and real zero are visually distinct.
- [ ] Comparable heatmaps share domains and thresholds.
- [ ] No chart uses a library rainbow default.
- [ ] Color is not the only carrier of meaning.

### Labels and interaction

- [ ] Title is descriptive and non-hyped.
- [ ] Subtitle includes scope, sample, assumptions, and unit.
- [ ] Axis labels, ticks, direct labels, and legends do not collide or clip.
- [ ] Long category labels have enough left margin.
- [ ] Signed bars have a visible zero line and enough space on both sides.
- [ ] Heatmap cells show readable values or inspectable tooltips.
- [ ] Tooltips fit in the viewport and work by keyboard.
- [ ] Click-to-expand works, and the chart returns correctly on close.
- [ ] Exact data/source inspection remains available.

### Final-context inspection

- [ ] Open the actual generated HTML, not only the source spec.
- [ ] Inspect the dark screen version.
- [ ] Inspect the print/light version if the report may be printed or converted.
- [ ] Check approximately 390, 768, 1440, and wide-desktop widths.
- [ ] Check browser zoom and long labels.
- [ ] Check that active 5-minute reporting contains no accidental legacy 15-minute data.
- [ ] Confirm the visual supports the written takeaway and does not hide contradictory evidence.

## 19. Minimal report-design instruction for future work

The following sentence is enough to invoke this standard:

> Follow `report-design.md`: black research theme, single-column full-width charts, explicit palette and scales, thresholded audit-friendly heatmaps, assumptions-rich subtitles, exact evidence context, and click-to-expand visual inspection.

If a future request conflicts with this document, the request wins. Otherwise this document is the default.

## 20. Current repository references

Use these as implementation references, not as permission to copy stale data or legacy strategy logic:

- `apps/research/experiments/solana_alpha_registry/finalize_visual_report.ts` — canonical black, full-width, single-column overrides; heatmap colors; click-to-expand behavior.
- `apps/research/experiments/solana_alpha_registry/build_visual_artifact.ts` — full-width heatmap artifact contracts, titles, subtitles, and evidence framing.
- `apps/research/outputs/alpha_lane_rebuilds/build_report_artifact.ts` — bar/stacked-bar chart contracts, comparison context, and reference lines.
- `apps/research/library/styles.css` — research library dark shell, expanded media treatment, readable tables, and responsive behavior.

The visual rules in this document are stable; the trading conclusions and data inside example reports are not. Always use the newest valid local 5-minute evidence for the actual report.

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

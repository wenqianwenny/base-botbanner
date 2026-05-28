# Dashboard Module Rules

Use this file when a banner involves Base dashboard / 仪表盘 UI, especially chart cards, metric cards, pivot tables, or dashboard configuration panels.

Figma references:
- Original metric card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=51-43613`
- Abstract metric card A: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=51-43576`
- Abstract metric card B: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=51-43641`
- Metric sparkline assets: `figma-refs/components/趋势图1.svg`, `figma-refs/components/趋势图2.svg`
- Original column chart card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=52-43667`
- Abstract column chart card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=52-43697`
- Original radar chart card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=52-43730`
- Abstract radar chart card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=52-43858`
- Original donut chart card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=53-44009`
- Abstract donut chart card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=53-44046`
- Original ranking list card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=54-44090`
- Abstract ranking list card: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=54-44227`

---

## Metric Card Abstraction

When a metric card needs abstraction, follow the provided abstract metric-card style. Do not invent a new abstraction style.

This component is low-freedom. Use `assets/templates/dashboard/metric-card-abstract.html` whenever possible instead of reconstructing the card from memory or prose.

Required implementation rule:
- Copy the template file first, then scale/place the copied component in the banner.
- Do not recreate the card manually from the written dimensions below.
- Generated HTML for abstract metric cards must contain `趋势图1.svg` or `趋势图2.svg`.

### Original Structure

The original metric card contains:
- Title label, e.g. `商机价值`
- Large metric number, e.g. `¥7,580,000`
- Comparison label, e.g. `同比去年`
- Comparison value with trend indicator, e.g. `43%`
- Small trend sparkline at the bottom-right

### Card Proportion

Keep the original card proportion as much as possible.

Rules:
- Preferred ratio: about `1.48:1` width to height
- Acceptable ratio range: `1.42:1` to `1.55:1`
- Base size reference: about `316 × 213px`
- If scaled for banner composition, scale width and height together
- Do not stretch the card into a wide banner strip or a square tile

### Abstract Style

Use a white rounded card with sparse gray placeholder pills and a subtle trend line.

Card:
- Background: `#FFFFFF`
- Radius: `16px`
- Padding: `22px 24px`
- Layout: vertical, `justify-content: space-between`
- Keep the card quiet and airy; do not add borders or dense inner dividers

Top block:
- Title placeholder: `74 × 18px`, radius `100px`, color `rgba(15, 15, 16, 0.06)`
- Main metric placeholder: `174 × 34px`, radius `100px`, color `rgba(15, 15, 16, 0.06)`
- Gap between title and metric placeholders: `14px`

Bottom block:
- Comparison placeholder: `52 × 12px`, radius `100px`, color `rgba(15, 15, 16, 0.06)`
- Trend sparkline sits at bottom-right
- Sparkline must use the Figma SVG assets in `figma-refs/components/趋势图1.svg` or `figma-refs/components/趋势图2.svg`
- Sparkline asset size: `66 × 46px`
- Do not redraw the trend line manually

### Canonical HTML/CSS Template

Canonical source file: `assets/templates/dashboard/metric-card-abstract.html`.

Use this structure for abstract metric cards. Scale the whole card with width/height only; keep internal proportions unless there is a clear composition constraint.

```html
<div class="metric-card metric-card-abstract">
  <div class="metric-card-top">
    <div class="metric-title-skeleton"></div>
    <div class="metric-value-skeleton"></div>
  </div>
  <div class="metric-card-bottom">
    <div class="metric-compare-skeleton"></div>
    <img class="metric-sparkline" src="../figma-refs/components/趋势图1.svg" alt="">
  </div>
</div>
```

```css
.metric-card-abstract {
  width: 316px;
  height: 213px;
  padding: 24px 22px;
  border-radius: 16px;
  background: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.metric-card-top {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.metric-title-skeleton {
  width: 74px;
  height: 18px;
  border-radius: 100px;
  background: rgba(15, 15, 16, 0.06);
}

.metric-value-skeleton {
  width: 174px;
  height: 34px;
  border-radius: 100px;
  background: rgba(15, 15, 16, 0.06);
}

.metric-card-bottom {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  width: 100%;
}

.metric-compare-skeleton {
  width: 52px;
  height: 12px;
  border-radius: 100px;
  background: rgba(15, 15, 16, 0.06);
  margin-bottom: 4px;
}

.metric-sparkline {
  width: 66px;
  height: 46px;
  flex: 0 0 auto;
}
```

For the softer/wavy trend variant, keep the same card, skeletons, layout, and sizes. Only replace the image source:

```html
<img class="metric-sparkline" src="../figma-refs/components/趋势图2.svg" alt="">
```

### Trend Variants

There are two approved abstract metric-card variants:

- Variant A: rising / upward sparkline, based on node `51:43576`
- Variant B: wavy / softer sparkline, based on node `51:43641`
- Use `趋势图1.svg` for one approved trend style and `趋势图2.svg` for the other approved trend style. Do not draw custom SVG paths.

Use the variant that best matches the source metric's trend direction when known. If direction is unknown and multiple metric cards appear together, use both variants to avoid repetition while keeping the same structure.

### Information Rules

In abstracted dashboard background UI:
- Replace readable title, number, label, and percentage with placeholder pills
- Keep the metric hierarchy visible through placeholder sizes
- Keep the sparkline because it identifies the component as a metric card
- Do not show real business numbers unless the metric itself is the primary feature content

In primary/focus UI:
- Real metric text may be retained only when the banner's feature is about that exact metric or insight
- If the metric card is only contextual, use the abstract style even in the foreground

### Do Not

- Do not draw a different card layout when this canonical template can be used
- Do not change internal skeleton sizes independently when scaling; scale the whole card proportionally
- Do not hand-draw the sparkline; always use `趋势图1.svg` or `趋势图2.svg`
- Do not replace a metric card with a bar chart or random chart
- Do not add extra axes, legends, labels, grid lines, or multiple sparklines
- Do not use colored placeholders for title/number
- Do not make the sparkline visually stronger than the metric placeholder
- Do not use more than 2 abstract metric cards in a secondary dashboard background unless the user explicitly asks for a dashboard grid
- Do not alter the card ratio just to fill empty banner space

### Dashboard Row Alignment

Dashboard cards in the same row must share the same top and bottom baseline.

Rules:
- Same-row metric cards, chart cards, ranking cards, and pivot/table cards must have height difference `<= 4px`.
- Do not top-align cards while leaving different bottom edges.
- Do not bottom-align cards while leaving different top edges.
- If cards contain different internal content, normalize the outer card height first, then adjust inner whitespace or remove low-priority inner content.
- Add `grid-alignment` for every hand-positioned dashboard card row.

Required check:

```css
/* ui-check grid-alignment selectors=".metric-card-a,.metric-card-b,.metric-card-c" tolerance=4 */
```

### Acceptance Check

Before final output, verify the abstract metric card:
- Card ratio remains close to `1.48:1`
- Top placeholder is `74 × 18` relative to a `316 × 213` card
- Main metric placeholder is `174 × 34`
- Comparison placeholder is `52 × 12`
- Sparkline sits at bottom-right and uses the Figma SVG asset at `66 × 46`
- No readable text remains in the abstracted card
- No blue/green semantic chart colors remain in the abstracted card

---

## Column Chart Card Abstraction

When a dashboard column / bar chart needs abstraction, follow the provided abstract column-chart style. Do not invent a new chart abstraction.

### Original Structure

The original column chart card contains:
- White chart card with 16px radius
- Title text at top-left, e.g. `新增客户数`
- 10 vertical bars across the card
- Month labels along the bottom, e.g. `1月` to `10月`
- Product chart colors: blue bars with one highlighted cyan/teal bar

### Card Proportion

Keep the original chart-card proportion as much as possible.

Rules:
- Preferred ratio: about `1.15:1` width to height
- Acceptable ratio range: `1.08:1` to `1.22:1`
- Base size reference: about `320 × 277px`
- If scaled for banner composition, scale width and height together
- Do not stretch the card into a wide dashboard strip
- Do not crop inside the card; crop the whole dashboard layer if needed

### Abstract Style

Use a white rounded card with one title placeholder and a sparse set of gray pill bars.

Card:
- Background: `#FFFFFF`
- Radius: `16px`
- Layout: relative positioning is acceptable for exact chart rhythm
- Keep the card clean; no axes, grid lines, legends, or labels

Title placeholder:
- Position: top-left, about `20px` from top and left
- Size: `90 × 18px`
- Radius: `100px`
- Color: `rgba(15, 15, 16, 0.06)`

Bar group:
- Position: about `20px` from left and bottom
- Width reference: about `282px`
- Height reference: about `201px`
- Bars: 10 bars, matching the original card rhythm
- Bar width: `16px`
- Bar radius: `100px` pill ends
- Bar color: `rgba(15, 15, 16, 0.06)`
- Bar alignment: bottom-aligned
- Preserve varied heights; do not make equal-height bars

Recommended abstract bar heights for the base size:
- `54`, `144`, `84`, `124`, `185`, `65`, `89`, `135`, `40`, `112`

These heights preserve the visual rhythm of the original chart while removing real data meaning.

### Information Rules

In abstracted dashboard background UI:
- Replace the real chart title with the title placeholder
- Remove month labels
- Remove all real data labels and axis labels
- Replace colored bars with neutral gray bars
- Keep 10 bars when the source chart has 10 monthly bars; do not reduce to 5-7 bars for this approved card style

In primary/focus UI:
- Real title and semantic colors may be retained only when the banner is specifically about the chart's data or chart result
- If the chart is only contextual, use the abstract style even in the foreground

### Do Not

- Do not show bottom month labels in the abstract version
- Do not keep the blue/cyan colors when the chart is contextual
- Do not add grid lines, axes, legends, values, or tooltip labels
- Do not randomize bar count or spacing
- Do not replace the 10-bar rhythm with a generic mini chart
- Do not make the bars rectangular with small corner radius; use full pill radius
- Do not use this style for horizontal bar charts; create a separate rule when that component is provided

---

## Radar Chart Card Abstraction

When a dashboard radar chart needs abstraction, follow the provided abstract radar-card style. Do not invent a new radar chart abstraction.

This component is low-freedom. Use `assets/templates/dashboard/radar-chart-abstract.html` whenever possible instead of reconstructing the chart from memory or prose.

Required implementation rule:
- Copy the template file first, then scale/place the copied component in the banner.
- Do not recreate the card manually from the written dimensions below.
- The center radar graphic should scale with the card.

### Original Structure

The original radar chart card contains:
- White card with 16px radius
- Title text at top-left, e.g. `销售能力模型`
- Legend row under title, with three colored series
- Center radar chart with circular grid, axis labels, value labels, and three colored series shapes

### Card Proportion

Keep the original chart-card proportion as much as possible.

Rules:
- Preferred ratio: about `0.95:1` width to height
- Acceptable ratio range: `0.90:1` to `1.00:1`
- Base size reference: about `431 × 452px`
- If scaled for banner composition, scale width and height together
- Do not stretch the radar card into a wide dashboard strip
- The center radar visual may scale up/down within the card, but the card ratio should stay close to the reference

### Abstract Style

Use a white rounded card with one title placeholder and a neutral radar graphic.

Card:
- Background: `#FFFFFF`
- Radius: `16px`
- Layout: relative positioning is acceptable for exact chart rhythm
- Keep the card clean; no legends, axis labels, value labels, or tooltip labels

Title placeholder:
- Position: top-left, about `20px` from top and left
- Size: `90 × 18px`
- Radius: `100px`
- Color: `rgba(15, 15, 16, 0.06)`

Radar visual:
- Position: centered horizontally
- Top offset reference: about `85px`
- Base visual size: about `330 × 330px`
- The middle graphic can scale to fit card size
- Grid: neutral light gray circles and radial axes
- Series shapes: neutral gray stroke/fill only
- Preserve multiple overlapping shapes so the component still reads as a radar chart

### Information Rules

In abstracted dashboard background UI:
- Replace the real chart title with the title placeholder
- Remove legend text and legend dots
- Remove axis labels such as `学习能力`, `服务意识`, and numeric value labels
- Remove all semantic series colors
- Keep the circular radar grid and multiple overlapping radar shapes

In primary/focus UI:
- Real title, legend, labels, and semantic colors may be retained only when the banner is specifically about the radar chart's data or insight
- If the radar chart is only contextual, use the abstract style even in the foreground

### Do Not

- Do not show legends in the abstract version
- Do not show axis labels or numeric labels in the abstract version
- Do not keep blue/yellow/green/purple semantic colors when the chart is contextual
- Do not replace radar with a donut, line, or column chart
- Do not make the center radar graphic tiny inside the card
- Do not stretch the radar circle into an oval
- Do not use this style for polar area charts; create a separate rule when that component is provided

### Acceptance Check

Before final output, verify the abstract radar chart card:
- Card ratio remains close to `0.95:1`
- Title placeholder is `90 × 18` relative to a `431 × 452` card
- Center radar graphic is circular and centered
- Center radar graphic scales with card size
- No readable title, legend, axis label, or numeric label remains
- No semantic series colors remain in the abstracted chart

---

## Donut Chart Card Abstraction

When a dashboard donut / ring chart needs abstraction, follow the provided abstract donut-card style. Do not invent a new donut chart abstraction.

This component is low-freedom. Use `assets/templates/dashboard/donut-chart-abstract.html` whenever possible instead of reconstructing the chart from memory or prose.

Required implementation rule:
- Copy the template file first, then scale/place the copied component in the banner.
- Do not recreate the card manually from the written dimensions below.
- The center donut graphic should scale with the card.
- The chart graphic and its center placeholders must be adaptive to the card size. When resizing the card, preserve the card ratio and use proportional sizing/positioning for the donut visual instead of leaving a fixed `300px` graphic inside a resized card.

### Original Structure

The original donut chart card contains:
- White card with rounded corners
- Title text at top-left, e.g. `客户行业分布`
- Donut / ring chart on the left
- Center metric value and helper label, e.g. `129` and `Total`
- Legend list on the right with colored dots and category labels

### Card Proportion

Keep the abstract card proportion close to the provided abstraction reference.

Rules:
- Preferred ratio: about `0.95:1` width to height
- Acceptable ratio range: `0.90:1` to `1.00:1`
- Base size reference: about `431 × 452px`
- If scaled for banner composition, scale width and height together
- Do not stretch the donut card into a wide dashboard strip
- The center donut visual may scale up/down within the card, but the card ratio should stay close to the reference

### Abstract Style

Use a white rounded card with one title placeholder, one large neutral donut chart, and two center placeholder pills.

Card:
- Background: `#FFFFFF`
- Radius: `16px`
- Layout: relative positioning is acceptable for exact chart rhythm
- Keep the card clean; no legends, category labels, numeric labels, or tooltip labels

Title placeholder:
- Position: top-left, about `20px` from top and left
- Size: `90 × 18px`
- Radius: `100px`
- Color: `rgba(15, 15, 16, 0.06)`

Donut visual:
- Position reference: visual area starts around `left: 66px`, `top: 99px`
- Visual area base size: about `300 × 300px`
- Adaptive reference: `left: 15.31%`, `top: 21.9%`, `width: 69.61%`, `aspect-ratio: 1`
- The Figma abstraction node may contain an inner `400 × 400px` image at `left: -50px`, `top: -50px`; treat that as the exported image crop only. Do not size the HTML donut visual to `400 × 400px`.
- Donut ring outer diameter: about `294px`
- Donut ring thickness: about `48px`
- Ring color: `rgba(15, 15, 16, 0.06)`
- Segment separators: white gaps
- The middle graphic can scale to fit card size
- Keep the ring circular; never stretch it into an oval

Center placeholders:
- Main value placeholder: `108 × 32px`, radius `100px`, centered in donut, around `left: 162px`, `top: 226px`
- Helper label placeholder: `62 × 14px`, radius `100px`, below main value, around `left: 185px`, `top: 271px`
- Adaptive implementation: place both center placeholders inside the donut visual and center them as a group. Use proportional dimensions from the `300 × 300px` visual reference: main placeholder `36% × 10.67%`, helper placeholder `20.67% × 4.67%`, gap about `4.33%`.
- Color: `rgba(15, 15, 16, 0.06)`

### Information Rules

In abstracted dashboard background UI:
- Replace the real chart title with the title placeholder
- Remove the legend list and legend dots
- Remove all real category labels and values
- Replace center number and helper label with placeholders
- Remove all semantic series colors
- Keep the segmented donut shape because it identifies the component as a donut chart

In primary/focus UI:
- Real title, legend, values, and semantic colors may be retained only when the banner is specifically about the donut chart's data or insight
- If the donut chart is only contextual, use the abstract style even in the foreground

### Do Not

- Do not show legends in the abstract version
- Do not show category labels or numeric labels in the abstract version
- Do not keep blue/yellow/green/purple/orange semantic colors when the chart is contextual
- Do not replace donut with radar, line, or column chart
- Do not make the center donut graphic tiny inside the card
- Do not stretch the donut circle into an oval
- Do not remove the segmented feeling of the ring
- Do not use this style for pie charts without a center hole; create a separate rule when that component is provided

### Acceptance Check

Before final output, verify the abstract donut chart card:
- Card ratio remains close to `0.95:1`
- Title placeholder is `90 × 18` relative to a `431 × 452` card
- Donut graphic is circular and centered in the visual area
- Donut graphic scales with card size
- Resizing the card does not leave a tiny fixed-size donut or misaligned center placeholders
- Center placeholders remain centered in the donut
- No readable title, legend, category label, value, or helper label remains
- No semantic series colors remain in the abstracted chart

---

## Ranking List Card Abstraction

When a dashboard ranking list / leaderboard card needs abstraction, follow the provided abstract ranking-card style. Do not invent a new leaderboard abstraction.

This component is low-freedom. Use `assets/templates/dashboard/ranking-list-abstract.html` whenever possible instead of reconstructing the card from memory or prose.

Required implementation rule:
- Copy the template file first, then scale/place the copied component in the banner.
- Do not recreate the card manually from the written dimensions below.
- Keep the top-three podium structure and the lower list structure. These two regions are what make the card read as a leaderboard.

### Original Structure

The original ranking list card contains:
- White card with rounded corners
- Title text at top-left, e.g. `销售排行榜`
- Top-three podium area with three user avatars, rank badges, names, and values
- Lower ranked list with rank number, avatar, name, and value

### Card Proportion

Keep the abstract card proportion close to the provided abstraction reference.

Rules:
- Preferred ratio: about `0.95:1` width to height
- Acceptable ratio range: `0.90:1` to `1.00:1`
- Base size reference: `322 × 340px`
- If scaled for banner composition, scale width and height together
- Do not stretch the ranking card into a wide dashboard strip
- Do not collapse the podium and list into a generic table; preserve the two-region hierarchy

### Abstract Style

Use a white rounded card with one title placeholder, three podium avatar placeholders, three podium label placeholders, and three lower list rows.

Card:
- Background: `#FFFFFF`
- Radius: `16px`
- Layout: relative positioning is preferred for exact podium rhythm
- Keep the card clean; no real names, scores, rank numbers, badges, avatar photos, or row highlight backgrounds

Title placeholder:
- Position: top-left, `left: 20px`, `top: 20px`
- Size: `90 × 18px`
- Radius: `100px`
- Color: `rgba(15, 15, 16, 0.06)`

Podium area:
- Left avatar: `52 × 53px`, around `left: 45px`, `top: 83px`
- Center avatar: `74 × 74px`, around `left: 124px`, `top: 62px`
- Right avatar: `52 × 53px`, around `left: 225px`, `top: 83px`
- Podium name placeholders: `45 × 18px`, `top: 145px`
- Name placeholder x positions: left `48px`, center `141px`, right `228px`
- Keep the center avatar larger and higher than the side avatars
- Do not add rank badge icons in the abstract version; the avatar size and layout already convey the podium structure

Lower list:
- Position: `left: 20px`, `bottom: 32px`
- Width: `282px`
- Height: `100px`
- Rows: exactly 3 rows in the abstract version
- Row height: `24px`
- Row gap: `14px`
- Each row has a left circular placeholder `24 × 24px`, a name placeholder, and a right value placeholder
- Name placeholder widths: `90px`, `45px`, `134px` to preserve varied content rhythm
- Right value placeholder: `58 × 10px`, aligned to the row bottom-right

### Information Rules

In abstracted dashboard background UI:
- Replace the real title with the title placeholder
- Replace all avatar photos with neutral gray circular placeholders
- Remove rank badge icons and medal visuals
- Replace names and values with placeholders
- Reduce the lower list to three rows unless the ranking card itself is the primary feature content
- Remove row highlight backgrounds and real rank numbers

In primary/focus UI:
- Real names, values, and rank badges may be retained only when the banner is specifically about the ranking result or leaderboard feature.
- If the ranking card is only contextual, use the abstract style even in the foreground.

### Do Not

- Do not replace the leaderboard with a generic table or bar chart
- Do not keep real user avatars in contextual/background dashboard UI
- Do not show real names, numbers, rank labels, or medal icons in the abstract version
- Do not make all three podium avatars the same size; the center item must remain larger and higher
- Do not add more than three lower rows in the abstract version unless the ranking list is the primary content
- Do not use colored placeholders for different ranks

### Acceptance Check

Before final output, verify the abstract ranking list card:
- Card ratio remains close to `0.95:1`
- Title placeholder is `90 × 18` relative to a `322 × 340` card
- Three podium avatar placeholders are present, with center larger and higher
- Three podium name placeholders align below the avatars
- Lower list has exactly 3 rows, each with circle/name/value placeholders
- No readable title, rank number, user name, avatar photo, value, or badge remains in contextual abstraction
- No semantic rank colors remain in the abstracted card

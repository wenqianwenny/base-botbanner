# Layout Constraint System

This file defines hard layout constraints for every `900 × 500` Base bot banner. Read it before drawing or coding any banner.

## 1. Canvas

Banner:

```text
width: 900px
height: 500px
```

The banner is a fixed product-composition canvas, not a free poster. Every UI surface must be deliberately placed, cropped, or protected.

## 2. Outer Safe Area

Default safe area for non-cropped UI edges:

```text
top: 30px to 50px
left: 30px to 50px
right: 30px to 50px
bottom: 30px to 50px
default: 36px
```

Rules:
- Primary UI must be fully inside the safe area.
- Primary UI must not touch or crowd the top edge, right edge, left edge, or bottom edge.
- Primary UI must keep at least `30px` from every banner edge. For large complete-interface primary surfaces, keep visible edges in the `30px` to `50px` range. Compact floating panels may be vertically centered and therefore can have more than `50px` on the opposite side.
- The checker can derive geometry from pixel `left/top/right/width/height`, and from centered formulas such as `left: 50%; top: 50%; transform: translate(-50%, -50%)` or `top: 50%; transform: translateY(-50%)`.
- Secondary/source UI may break the left edge and bottom edge when it is intentionally cropped.
- Secondary/source UI must always keep its non-cropped top edge inside the `30px` to `50px` safe range.
- Secondary/source UI right edge uses `30px` to `50px` only when it is a contained/complete context surface. When the primary floating panel is on the right, do not force the source/context surface to share the same right safe margin.
- Top-edge crowding is never allowed by default. A source/context UI may crop left or bottom, but not top, unless the user explicitly requests a top crop.
- If the source/context UI is too tall, crop bottom or remove low-priority content before reducing the top safe area.

Failure examples:
- A large background table starts at `top: 12px`.
- A source surface has a full safe card look on the left instead of intentional left/bottom crop.
- A primary floating panel touches the right edge or sits at `top: 18px`.
- The source UI is moved up to make the banner feel fuller instead of using bottom crop.

## 3. Required Surface Classes

Use these classes so scripts can enforce layout:

```text
.source-surface       lower/background/source/context UI
.left-context-source  source UI intentionally placed on the left and cropped left/bottom
.contained-context-source  compact source/context UI kept fully inside the canvas
.intermediate-surface real middle-step UI, such as menu or popover
.primary-surface      foreground result, primary panel, or key complete interface
.ui-surface           every major product surface counted by surface-count
```

Layer order:

```text
source/context < intermediate < primary < pointer
```

The primary surface must never be visually covered by the source/context surface.

## 4. Layout Options

Every new banner must use one of these layout options. Ask the user for `A`, `B`, or `C` before implementation unless the prompt already specifies it.

### Layout A — Primary Right, Secondary Left

Use when the primary/result/floating UI should lead on the right.

```text
secondary/source/lower UI: left, usually left + bottom cropped
primary/result/floating UI: right, complete and readable
```

Rules:
- Use one or two surfaces by default.
- Use three surfaces only when the real product path has three necessary states.
- Secondary/source top safe margin should be `50px` by default.
- The left source/context surface should be wide, larger than the visible canvas area, and intentionally cropped on the left and bottom.
- Prefer showing more source UI under the primary panel instead of exposing background.
- The source and primary surfaces should overlap meaningfully; do not merely place them side by side.
- The right primary surface owns the right safe margin. The source/context surface may move left and must not visually share the same right edge with the primary surface.
- Primary floating panel vertical placement follows height-based rules. Do not vertically center small panels by default.

Recommended markers:

```css
/* ui-check edge-safe selector=.source-surface top-min=48 top-max=52 */
/* ui-check cropped-edge selector=.source-surface side=left,bottom min-out=32 */
/* ui-check edge-safe selector=.primary-surface right-min=30 right-max=50 */
/* ui-check primary-placement selector=.primary-surface small-height=360 bottom=60 center-target-y=250 tolerance=4 */
/* ui-check no-shared-edge a=.primary-surface b=.source-surface edge=right min-delta=40 */
/* ui-check overlap a=.primary-surface b=.source-surface min-x=80 min-y=80 */
```

### Layout B — Primary Left, Secondary Right

Use only when requested or when source geometry makes the right-primary composition weaker.

```text
primary/result/floating UI: left, complete and readable
secondary/source/lower UI: right, usually right + bottom cropped
```

Rules:
- Secondary/source top safe margin should be `50px` by default.
- The right source/context surface should be wide and intentionally cropped on the right and bottom.
- Prefer showing more source UI under the primary panel instead of exposing background.
- The source and primary surfaces should overlap meaningfully.
- The left primary surface owns the left safe margin.
- Primary floating panel vertical placement follows height-based rules. Do not vertically center small panels by default.

Recommended markers:

```css
/* ui-check edge-safe selector=.source-surface top-min=48 top-max=52 */
/* ui-check cropped-edge selector=.source-surface side=right,bottom min-out=32 */
/* ui-check edge-safe selector=.primary-surface left-min=30 left-max=50 */
/* ui-check primary-placement selector=.primary-surface small-height=360 bottom=60 center-target-y=250 tolerance=4 */
/* ui-check no-shared-edge a=.primary-surface b=.source-surface edge=left min-delta=40 */
/* ui-check overlap a=.primary-surface b=.source-surface min-x=80 min-y=80 */
```

### Layout C — Complete-Width Secondary, Overlapped Primary

Use when the secondary/source UI becomes narrow or awkward if cropped left/right.

```text
secondary/source UI: left/right complete, bottom may crop
primary/result/floating UI: overlaps secondary/source UI
```

Rules:
- Secondary/source top safe margin should be `50px` by default.
- Secondary/source left and right edges remain visible; only the bottom may be cropped.
- Source/context width should usually be `590px` to `660px` after removing non-core chrome. Do not make it narrow merely to keep it fully inside the canvas.
- The primary surface must sit above and overlap the secondary/source surface. Side-by-side contact is a failure.
- The primary surface keeps the relevant side safe margin, usually right `30px` to `50px`.
- The source and primary surfaces should overlap by at least `80px` on x and y axes.
- Primary floating panel vertical placement follows height-based rules. If panel height is `<= 360px`, place it `60px` above the banner bottom. If panel height is `> 360px`, vertically center it within the banner. Keep the existing horizontal position and overlap relationship when applying this rule.
- Do not force all panels to vertical center. Do not force all panels to bottom align. Do not change horizontal alignment when applying vertical placement.

Recommended markers:

```css
/* ui-check edge-safe selector=.source-surface left-min=30 left-max=50 top-min=48 top-max=52 */
/* ui-check cropped-edge selector=.source-surface side=bottom min-out=32 */
/* ui-check edge-safe selector=.primary-surface right-min=30 right-max=50 */
/* ui-check overlap a=.primary-surface b=.source-surface min-x=80 min-y=80 */
/* ui-check primary-placement selector=.primary-surface small-height=360 bottom=60 center-target-y=250 tolerance=4 */
/* ui-check z-index-above selector=.primary-surface above=.source-surface */
```

## 4.1 Right Primary Edge Separation

When the primary/floating panel is on the right:

- Keep the primary right margin inside `30px` to `50px`.
- Do not apply right safe-area pressure to the source/context surface unless it is `.contained-context-source`.
- The source/context right edge must not align with the primary right edge.
- The right-edge delta between `.primary-surface` and `.source-surface` must be at least `40px`.
- Do not make the source/context surface look complete by lining it up with the foreground panel's right edge.

Required marker:

```css
/* ui-check no-shared-edge a=.primary-surface b=.source-surface edge=right min-delta=40 */
```

## 4.2 Contained Context Layout

Use this variant when the secondary/source UI is narrow enough that cropping would make the product story weaker.

Rules:
- Apply both `.source-surface` and `.contained-context-source`.
- Source/context width should usually be `<= 620px` after removing non-core chrome.
- Keep the contained source inside the safe area: left/top/bottom edges `30px` to `50px`.
- The contained source may sit behind or slightly under the primary floating panel, but the primary surface remains visually above it.
- Do not use this variant to avoid simplifying a large table/dashboard/app page. If the source is wide, crop left/bottom as the default layout.
- Still keep vertical stagger between source and primary surfaces. Do not center-stack two equally prominent panels.

Recommended CSS markers:

```css
/* ui-check edge-safe selector=.contained-context-source left-min=30 left-max=50 top-min=30 top-max=50 bottom-min=30 bottom-max=50 */
/* ui-check z-index-above selector=.primary-surface above=.contained-context-source */
```

## 5. Cropping Contract

Intentional crop:
- Allowed by default: source/context left edge and bottom edge.
- Not allowed by default: primary UI edges, top edge of source/context UI, core trigger/result/selected content.

Recommended CSS markers:

```css
/* ui-check cropped-edge selector=.source-surface side=left,bottom min-out=32 */
/* ui-check edge-safe selector=.source-surface top-min=30 top-max=50 */
/* ui-check edge-safe selector=.primary-surface top-min=30 right-min=30 bottom-min=30 left-min=30 */
/* ui-check vertical-center selector=.primary-surface target-y=250 tolerance=4 */
/* ui-check no-shared-edge a=.primary-surface b=.source-surface edge=right min-delta=40 */
/* ui-check z-index-above selector=.primary-surface above=.source-surface */
/* ui-check surface-count item-class=ui-surface max=2 */
```

When a left source/context surface is detected, the checker also treats `.source-surface` as a left context by default and expects left/bottom crop.

This crop inference is skipped when `.contained-context-source` is present.

## 6. Floating Panel Radius

Upper-layer floating surfaces use a stable default radius:

```text
floating panel / popover / modal / dropdown radius: var(--radius-card)
```

Rules:
- Apply `border-radius: var(--radius-card)` to every banner-level floating panel, popover, modal, dropdown, compact picker, add panel, or foreground result panel.
- Mark these elements with `.floating-panel` when they are banner-level floating UI. The checker treats missing or non-token `.floating-panel` radius as a failure.
- Do not use larger soft-card radii such as `24px`, `28px`, or `32px` for upper floating panels. Map source radii to approved shape tokens.
- Large lower/source interface frames and device/mockup containers may use their own outer radius. They do not inherit the 16px floating-panel rule.
- Internal product modules, such as field blocks, option rows, table cells, dashboard cards, and IM bubbles, follow their source/component rules and do not automatically become 16px panels.

Required marker when a specific selector is used:

```css
/* ui-check radius selector=.floating-panel value=16 */
```

## 7. Size Adjustment Order

When layout does not fit:

1. Remove unrelated chrome, toolbars, repeated rows, and low-priority text.
2. Crop the source/context surface on low-priority sides.
3. Move content within the surface if there is internal empty space.
4. Shorten lower-priority internal rows, lines, or panels.
5. Only then resize the whole surface.

Never solve layout by moving the whole source surface closer than `30px` to the top edge.

## 8. Script Enforcement

Every generated banner must run:

```bash
python3 scripts/check_banner_ui.py output/<name>.html --fix
python3 scripts/check_banner_ui.py output/<name>.html --png output/<name>@2x.png
```

The checker enforces default surface contracts for `.source-surface`, `.left-context-source`, and `.primary-surface` even when the HTML forgot to add explicit `edge-safe` markers.

Geometry requirements:
- Use pixel `width` and `height` on major surfaces.
- Use pixel `left/top/right` when possible.
- If centering a floating panel, use the supported `50%` + `translate` formulas above; do not use `calc()` or unitless coordinates for major surface placement.

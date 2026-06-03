# UI Foundation — Base Bot Banner

These rules apply to every Base bot banner, regardless of feature module.

## 1. Alignment Is Mandatory

Every repeated UI group must use a stable alignment grid.

Before coding from any source design, extract the source alignment grid:
- stable columns: avatar/icon column, content/text start, value column, right action column
- stable rows: header/title row, toolbar row, repeated item row, footer/composer row
- trigger relationships: trigger rectangle, floating surface size, side, gap, and edge alignment
- parent context: which toolbar, input, card, panel, or row owns each visible control

Apply the grid across the whole source UI surface, not only inside one repeated list. If a source design shows the header avatar and message avatars on the same column, the abstracted banner must keep that column. If a trigger belongs to an input toolbar, the trigger must stay inside that toolbar.

Rules:
- Elements on the same horizontal row must share the same vertical center.
- Elements in a repeated vertical list must share the same `x` positions: icon left, icon center, label left, value left, suffix/right action.
- Do not hand-place repeated rows with different `left`, `top`, or text starts.
- Use CSS grid/flex variables for repeated rows instead of independent absolute positions.
- In one component, row height, icon size, icon slot, label start, and right padding must stay consistent.

### Grid Alignment Rules

Same-level components in one row must share a baseline.

Rules:
- Same-row cards, dashboard blocks, metric cards, chart cards, table summary cards, and repeated grid items must share both top and bottom alignment.
- Height difference within one row must be `<= 4px`.
- Do not create random-height cards in the same row to fill visual space.
- If content density differs, normalize card height first; then remove or skeletonize low-priority inner content instead of changing the outer card height.
- Add `grid-alignment` for every hand-positioned card row.

Forbidden:
- Cards whose tops align but bottoms do not.
- Cards whose bottoms align but tops do not.
- Same-row components with arbitrary heights.

Required check for hand-positioned rows:

```css
/* ui-check grid-alignment selectors=".metric-card-a,.metric-card-b,.metric-card-c" tolerance=4 */
```

Common failure:
- Menu icons alternate between circle, pill, line, and square.
- Row labels start at different x positions.
- A menu is visually centered under a trigger that is right-aligned in the source design.
- A composer input, action icon, trigger button, and menu drift as unrelated pieces.
- Two unrelated overlapping surfaces accidentally share the same right/left edge, making them feel stuck together.

## 1.2 Change Impact Review

After changing any component size, position, z-index, or visibility, re-check neighboring UI surfaces before final output.

Review:
- Does the changed element now touch, cover, or align flush with another unrelated surface?
- Did a wider primary surface require secondary UI to shrink, crop, or simplify?
- Did a narrower secondary UI require its internal cards/bubbles/rows to shrink?
- Are protected triggers and source elements still visible?
- Are unrelated edges separated by at least `16px`, preferably `24px` to `40px`, unless product layout intentionally aligns them?
- Did any dependent geometry change? Recompute anchored menus/popovers, protected trigger rectangles, min/max size markers, z-index checks, and crop/safe-margin checks from the new positions. A stale `ui-check` marker that still passes is a failure, because it validates the wrong geometry.
- Does each visible control still keep its parent-component context, such as a toolbar button inside its toolbar or an input action inside its composer?

If one element changes, rerun `check_banner_ui.py --fix`, regenerate the screenshot, and visually inspect the nearby UI and every dependent component, not just the edited element.

## 1.3 Neighbor Module Clearance

Different information modules inside the same source surface must not touch or visually merge after abstraction.

Rules:
- Keep at least `20px` visible clearance between adjacent modules unless the source design intentionally overlaps them.
- Apply this to text blocks next to images, form content next to visual panels, table/card groups next to side panels, and foreground controls next to skeleton groups.
- If a key content column gets too close to a neighboring image or panel, move the content column toward the available empty side first.
- If moving the column is not enough, shorten lower-priority field lines, option rows, skeleton bars, or card widths before allowing the gap to drop below `20px`.
- Do not solve a clearance problem by shrinking the whole source surface when there is unused room inside the surface.
- Add `rect-clearance` markers for known collision-prone pairs, such as a form input line against a right visual image region or a selected chip against nearby skeleton items.

Recommended marker:

```css
/* ui-check rect-clearance selector=.feature-field avoid-left=620 avoid-top=80 avoid-width=240 avoid-height=420 clearance=20 */
```

## 1.1 Internal Padding Consistency

Abstracted content inside one product component must use a consistent inset system.

Rules:
- Before coding a card, bubble, menu, panel, or option row, define its inner padding token.
- Do not use unrelated top, left, and bottom spacing values for skeleton lines inside the same component.
- For any visible container, decide the alignment mode of its primary information before tuning spacing:
  - Centered content: keep the primary information's visible distance to all non-cropped container edges consistent.
  - Left-aligned content: keep the primary information's visible distance to the top, left, and bottom non-cropped edges consistent.
  - Right-aligned content: keep the primary information's visible distance to the top, right, and bottom non-cropped edges consistent.
- Cropped edges are excluded from this spacing balance rule. If a side is intentionally clipped by the banner or by a parent mask, do not force padding against that side.
- The key label, input line, icon, and helper/content group must fit within the chosen visible inset instead of using independent left/right/top/bottom tuning.
- For compact internal modules, use one inset token by default: `12px` or `16px`.
- Skeleton lines inside cards/bubbles should start at the same left inset and keep the same top/bottom visual rhythm.
- The last skeleton line should not keep a trailing margin that makes the bottom inset look larger or smaller than the top inset.
- For menu rows, distinguish row outer padding from icon centering: define panel padding, row height, icon slot, icon size, and label start as a set. Repeated menu items must share these values.
- For compact menus with abstract icons, the first visible icon's top inset and left inset should match within `1px` unless the source specifies a different menu padding. Example: `18px` icon in a `24px` slot with `12px` row horizontal padding needs `8px` panel top padding, producing a visual inset of about `15px` on both top and left.

Failure examples:
- A message bubble has `padding: 14px 16px`, line gaps with trailing margin, and no explicit last-line reset.
- A menu row has visually unrelated first-row top inset, icon left inset, and label start because each value was tuned separately.

## 1.4 Component Containment

Child elements must stay inside their parent component content box.

Rules:
- Child elements must not touch parent borders or rounded edges.
- Use parent padding plus child `max-width` constraints instead of `width: 100%` for skeleton bars.
- Parent containers should use `overflow: hidden` when child content can reach edges or rounded corners.
- Table skeleton bars must stay inside their table cell content area and must not cross grid lines.
- Add `component-containment` markers for hand-coded cells, rows, chips, cards, and modules where child width is manually set.

Required table CSS pattern:

```css
.table-cell {
  padding: 12px 16px;
  overflow: hidden;
}

.skeleton-line {
  width: 72%;
  max-width: 160px;
  border-radius: 999px;
}

/* ui-check component-containment parent=.table-cell child=.skeleton-line inset=12 */
```

Forbidden:
- `width: 100%` on skeleton bars.
- Child elements touching parent edges.
- Skeleton bars crossing table grid lines.
- Elements overflowing rounded containers.

## 1.4.1 Skeleton Text Length Variation

Abstract text lines must simulate realistic copy length.

Rules:
- Repeated skeleton text in the same module should use at least `3` visibly different widths.
- Adjacent rows should not repeat the exact same skeleton width unless the source content is truly fixed-width.
- Use explicit width classes or module-level width tokens instead of one percentage value for every row.
- Keep each skeleton line inside its cell/card content box.

Forbidden:
- All row skeleton lines having the same length.
- A column of abstract copy bars that reads as a mechanical ruler.
- Random lengths that overflow cells or touch grid lines.

Required marker:

```css
/* ui-check skeleton-variation selector=.table-grid item-class=skeleton-line min-widths=3 */
```

## 1.5 Cross-layer Data Consistency

When Primary UI and Secondary UI express the same product data context, their core data must stay semantically consistent.

Applies to labels, status, users, files, time, levels, categories, and colors.

Rules:
- Secondary UI may be abstracted, cropped, or skeletonized, but it still belongs to the real product context.
- If the foreground UI references a data state, the background UI must use the same state set and color semantics.
- If the foreground filter constrains a visible field by equality or selected values, every visible background result row for that field must show matching values. Do not skeletonize the constrained field in some rows while showing real filtered values in others.
- Do not randomly generate secondary statuses, tags, levels, categories, or semantic colors.
- If foreground shows `A / S`, background must show `A / S`, not `A / B`.

Required marker when both layers share data context:

```css
/* ui-check cross-layer-consistency primary=.primary-surface secondary=.source-surface values="A 级|S 级" forbidden="B 级" */
```

## 1.6 Divider Width

All divider lines inside product UI must use `0.5px`.

Applies to:
- table row and column separators
- card or panel section dividers
- content-area boundaries that separate rows, columns, header/body, or sections

Does not apply to:
- foreground panel outer borders
- input, select, button, tag, or chip component borders
- large secondary outer-frame padding/background
- workflow connector lines, which use their own connection-line rules

Required CSS:

```css
border-bottom: 0.5px solid rgba(31, 35, 41, 0.15);
```

Required marker for hand-coded dividers:

```css
/* ui-check divider-width selector=.table-cell props=border-right,border-bottom value=0.5 */
```

## 2. Secondary UI Must Be Compressed

Secondary UI provides context, not a full product demo.

Rules:
- Keep only the feature-relevant function, selected state, trigger, source object, or result context.
- Remove unrelated top-right tools, extra tabs, redundant toolbar buttons, timestamps, decorative arrows, and full histories.
- Skeletonize repeated rows, secondary labels, helper copy, and background data.
- Remove abstract media/thumbnail blocks when they are secondary-only and do not explain the feature.
- Real readable text is a limited budget. Keep only labels that explain the feature path; skeletonize sibling labels, repeated placeholders, and generic menu items.
- When detail competes with the main feature, remove detail before shrinking the primary feature.
- A secondary UI may be cropped if the cropped side is not core to the feature path.

### Non-Core Chrome Removal

Non-core chrome should be removed, not hollowed out.

Rules:
- If a top bar, toolbar, page header, action cluster, or navigation chrome is not part of the feature path, remove the whole region.
- Do not remove text from toolbar buttons while keeping empty blue/outline button shells.
- Do not keep empty top-right button groups just to make the source UI feel complete.
- Keep a chrome control only when it is feature evidence. In that case it must carry real text, a locked semantic icon, `.pointer-target`, or another explicit core/trigger class.
- If removing the chrome leaves awkward space, crop or resize the source surface instead of adding placeholder controls.

Forbidden:
- Topbar with a primary blue button rectangle and adjacent empty outline button.
- Toolbar/header action area made only of blank rounded rectangles.
- Navigation/action chrome that has no readable label, icon, selected state, or trigger role.

## 2.1 Source Order And Evidence Priority

Product order is product logic. Do not change it during abstraction.

Rules:
- Preserve source order and index for visible ordered content: question numbers, table rows, workflow steps, menu order, list ranking, timeline steps, and numbered configuration stages.
- Do not move the feature item from first to second, reorder rows/steps, or renumber visible content to make the layout feel balanced.
- The core feature evidence must not be visually demoted below sibling or background content. If one item is the feature, it should stay more readable, complete, or prominent than non-core siblings.
- Sibling items may be skeletonized, cropped, or removed before the feature item is moved, renumbered, or visually downgraded.
- If a source order must be changed because of an explicit user request, record that change in the brief.

## 2.2 Compact Selection / Configuration Panels

This applies to compact product panels used to choose, add, configure, or select something: add menus, type pickers, field pickers, filter builders, action menus, dropdowns, small configuration popovers, and similar controls.

Role:
- A compact panel is real product evidence when it contains the selected/target action or configuration.
- If it is primary evidence for the feature, keep the target item label and key selected/configured values real.
- Do not skeletonize the entire compact panel. A fully skeletonized picker/config panel loses the feature information.

Information rules:
- Keep the selected or target item real, such as a chosen type, field, action, status, assignee, or generated condition.
- Keep 2-4 neighboring labels real only when they establish the panel type. Skeletonize or remove additional neighbors.
- Preserve source icon style for the selected/target item if available; otherwise use a locked local icon asset. Only non-core neighboring icons may become neutral placeholders.

Layout rules:
- Preserve compact source scale. Do not inflate a picker/popover into a full page.
- If the panel height is small enough to fit with safe margins, center it vertically in the banner or composition group. Do not leave excessive empty space below it.
- Add `no-excess-blank` when the panel was resized or when visual review shows large bottom whitespace.

Recommended checks:

```css
/* ui-check edge-safe selector=.compact-panel top-min=30 top-max=50 right-min=30 right-max=50 bottom-min=30 bottom-max=50 */
/* ui-check content-density selector=.compact-panel content-selector=.compact-panel-content top=24 right=24 bottom=24 left=24 */
/* ui-check no-excess-blank selector=.compact-panel content-selector=.compact-panel-content max-bottom-blank=24 */
/* ui-check allowed-text values="<target label>|<key selected value>|..." */
```

## 2.3 Internal Content Density

Floating panel interiors must stay visually dense and balanced after abstraction.

Default padding:

```text
top: 24px
right: 24px
bottom: 24px
left: 24px
```

Rules:
- Use this padding on primary floating panels, modal-like result panels, compact config panels, popovers, and dropdowns unless the source Figma panel provides an explicit different inset.
- Wrap the meaningful panel content in a measurable content group, such as `.panel-content`, and add `content-density` to every `.floating-panel`.
- If footer buttons or actions are removed, shrink the panel height to the remaining content. Do not keep the old footer/action area as empty bottom space.
- Do not leave large blank regions below the last meaningful row. Bottom blank should usually equal the bottom padding, `24px`, with only tiny rounding tolerance.

Required check for every floating panel:

```css
/* ui-check content-density selector=.floating-panel content-selector=.panel-content top=24 right=24 bottom=24 left=24 */
```

## 2.4 Text Abstraction Budget

Before coding, classify every visible text string:
- **Core text**: necessary to understand the feature path. Keep real.
- **Context text**: helps identify the product scene. Keep only if short and not competing.
- **Repeated placeholder text**: skeletonize.
- **Sibling menu/list labels**: skeletonize unless the item is selected or feature-relevant.
- **Decorative/helper text**: remove or skeletonize.

Same-priority information must use one abstraction treatment within the same page, panel, list, menu, grid, table, or form section.

Rules:
- Do not mix real readable labels and skeleton labels among items with the same priority.
- If one non-core sibling in a group is skeletonized, all non-core siblings in that group should be skeletonized or removed.
- If neighboring real labels are kept to explain a category, keep that whole same-priority group real; otherwise keep only the selected/target item real.
- Selected, active, focused, or feature-relevant items are a higher priority and may stay real while same-priority non-selected siblings are uniformly abstracted.
- Apply this to menus, type pickers, option rows, table columns, dashboard cards, sidebar entries, message lists, and repeated form questions.

Examples:
- In an IM creation menu focused on `收集表`, keep `收集表`; skeletonize other menu item labels.
- In a form preview, keep `收集表`, `问答题`, `单选题`, and the main input placeholder if it explains the field. Skeletonize repeated option placeholder labels such as `请输入选项`.
- If 3 rows repeat the same non-core text, at most one may remain real; usually all repeated labels become skeleton lines.
- Repeated abstract-only rows are capped at `5`. If a group would show more than 5 skeleton-only items, remove the extras instead of making the panel taller.

## 3. Abstract Asset Rules

Use existing assets before drawing generic placeholders.

Rules:
- All visible avatar/member/user/person/assignee visuals must use `<img>` assets from `figma-refs/components/avatar/`.
- Real-person avatars: use `figma-refs/components/avatar/Avatar-image-*`.
- Generic product avatars: use `[D] Avatar_Person_blue.svg` or `[D] Avatar_Person_grey.svg`.
- If a visible avatar should be grey, use `figma-refs/components/avatar/[D] Avatar_Person_grey.svg`; do not draw a grey CSS circle.
- Foreground, midground, and background avatar/person/member/user/assignee UI must be rendered as `<img>` using a locked avatar-folder asset.
- Do not draw visible avatars with CSS circles, gradient circles, initials, plain shapes, cropped screenshots, or custom face shapes.
- Plain/skeleton circles are allowed only for low-priority background rows where identity is irrelevant.
- Image thumbnails or picture materials: use `figma-refs/components/image/image1.svg`, `image2.svg`, `image3.svg`, or `image4.svg`.
- Abstract circles, rounded rectangles, skeleton lines, generic icon blocks, and chart primitives must use:

```css
background: rgba(15, 15, 16, 0.06);
```

This is `#0F0F10` at 6% opacity.

Do not:
- generate new avatars
- draw avatar placeholders outside `figma-refs/components/avatar/`
- draw CSS human faces
- use random online images
- use non-approved gray fills for abstract shapes
- make outlined square icon placeholders unless the source element is an actual checkbox

## 4. Secondary UI Backing Plate

When a secondary UI sits on the banner background, add a backing plate behind it.

Backing plate rules:
- Extends `14px` beyond the secondary UI on all four sides.
- Background: `rgba(255, 255, 255, 0.8)`.
- Blur: `backdrop-filter: blur(14px)`.
- Border radius: secondary UI radius + `8px` to `12px`, depending on scale.
- The backing plate moves and crops with the secondary UI as one group.

Do not add a backing plate to every small component. Use it for secondary product surfaces or grouped UI scenes that need separation from the background.

## 4.1 Secondary UI Outer Frame

Large lower-layer product interfaces need a visible outside frame, not only a thin CSS border.

Rules:
- Build the frame as a wrapper around the product UI.
- Frame thickness: `10px`, implemented as wrapper `padding: 10px`.
- Frame color / opacity: `background: rgba(255, 255, 255, 0.5)`.
- The product UI sits inside the wrapper; do not draw this as an inset border on the product UI itself.
- The frame and inner UI must be concentric. Outer frame radius = inner UI radius + frame padding.
- For a `10px` outer frame around a `--radius-card` inner surface, use `border-radius: calc(var(--radius-card) + 10px)` on the wrapper and `border-radius: var(--radius-card)` on the inner UI.
- Keep the full wrapper visible on non-cropped sides. Cropped sides may cut the wrapper intentionally.
- Use a normal `1px solid rgba(255,255,255,0.72)` outline only for small flat panels or foreground separation, not for a large secondary/background interface.

Recommended check:

```css
/* ui-check outer-frame selector=.secondary-frame padding=10 background="rgba(255, 255, 255, 0.5)" */
```

## 4.2 Elevation Scope

Use shadow only to separate banner-level floating UI from the banner scene.

Shadow is allowed for:
- foreground floating panels, modals, popovers, dropdowns, and menus
- primary result surfaces that overlap another UI surface
- secondary UI backing plates only when they need soft separation from the banner background

Shadow is not allowed for product modules inside a UI surface:
- IM message bubbles, message cards, composer/input bars, and chat content cards
- table cells, rows, field blocks, form option rows, dashboard cards, chart cards, and internal panels
- abstract skeleton blocks, placeholder text lines, generic icons, avatars, and thumbnails

Internal product modules should use flat fills, strokes, dividers, and source spacing instead of box shadow. If a source design uses a tiny internal shadow, remove it unless that internal module is promoted to the banner-level foreground surface.

When removing shadow from an internal module, preserve separation through the source fill or stroke. Do not let a flat internal card become the same color as its parent surface. If the source provides a module fill, use it exactly; for Lark IM bubbles/cards, use `#F1F2F3` unless the source state specifies another fill.

Use only predefined shadow tokens from `references/design.md` Section 11:

```css
--shadow-primary-strong:
  0px 20px 50px rgba(158, 170, 191, 0.18),
  0px 8px 18px rgba(158, 170, 191, 0.08),
  0px 2px 6px rgba(158, 170, 191, 0.04);

--shadow-secondary-soft:
  0px 10px 28px rgba(158, 170, 191, 0.10),
  0px 3px 10px rgba(158, 170, 191, 0.05);
```

Rules:
- Primary floating panels use `box-shadow: var(--shadow-primary-strong)`.
- Smaller menus/popovers/backing plates may use `box-shadow: var(--shadow-secondary-soft)`.
- Do not invent shadow values. Do not use black shadows, single-layer shadows, or opacity above `25%`.
- Primary panel shadow must be stronger than secondary panel shadow; create hierarchy through blur/spread, not through thicker borders.

## 4.3 Floating Surface Radius

Banner-level floating UI has a shared radius baseline:

- Default token for upper floating panels, popovers, dropdowns, compact selection panels, modal fragments, and foreground result panels: `--radius-card`.
- Use `.floating-panel` on these elements and put `border-radius: var(--radius-card)` on that selector or a selector that directly includes `.floating-panel`.
- If Figma explicitly uses another radius, map it to the closest approved shape token and record that mapping in UI Detail Constraints; otherwise do not improvise.
- Do not apply this rule to lower/source interface frames, device mockups, or product-internal modules. Those surfaces follow source geometry or their module rules.

Required check:

```css
/* ui-check radius selector=.floating-panel value=16 */
```

## 5. Banner Edge Safety

Prefer intentional crop over accidental edge crowding.

Rules:
- If a UI surface is meant to be cropped, it may exceed the banner boundary.
- Cropped sides do not need safe margin.
- Non-cropped sides must keep `30px` to `50px` from the banner edge by default.
- Default non-cropped safe margin: `36px`.
- Use `30px` to `36px` for tight compositions and compact secondary fragments.
- Use `40px` to `50px` for large primary panels when space allows.
- Safe margin is a range, not just a minimum. Do not leave more than `50px` of empty edge space unless that side is intentionally cropped, hidden by another surface, or the source design explicitly needs the whitespace.
- Do not stretch a panel to make its edge sit exactly on the safe-margin line. If content is shorter, reduce the panel height/width so the interior does not create excessive empty space while keeping the visible outer margin within `30px` to `50px`.
- When increasing edge safety, first decide whether the surface should move, shrink, or simplify. For complete-interface primary surfaces, preserve minimum useful scale, but avoid adding blank internal area just to reach the canvas edge.

If a panel feels too close to the edge:
1. Crop a lower-priority side intentionally.
2. Remove secondary UI details.
3. Reduce lower-priority content.
4. Shrink the surface if content no longer needs the old size.
5. Only then reduce the non-cropped margin, never below the required minimum.

## 5.0 Left Context Crop Pattern

When a lower-priority source/context interface is placed on the left of a two-surface banner, it should usually feel larger than a contained card.

Rules:
- Mark the lower context interface with `.source-surface`; add `.left-context-source` when you already know it is the left-side context.
- Even if `.left-context-source` is missing, the checker treats `.source-surface` as a left context automatically when it is positioned left of `.primary-surface`.
- Prefer cropping the context surface at the left edge and bottom edge over shrinking it to fit fully inside the canvas.
- Use this especially for PC form, questionnaire, table, dashboard, app, and workflow source pages.
- Crop only low-priority chrome or repeated content. Do not crop the selected item, focused field, key trigger, or main result evidence.
- If the context surface only needs to express the product body, remove unrelated navigation bars, sidebars, top toolbars, tabs, app switchers, and footer controls before scaling down the body.
- A left source/context page showing a full rounded left corner inside the banner is a failure unless the user explicitly chose a no-crop layout.
- Add a `cropped-edge` marker for the cropped surface, usually `side=left,bottom min-out=32`.
- Add `edge-safe` only for non-cropped edges.

```css
/* ui-check cropped-edge selector=.source-surface side=left,bottom min-out=32 */
/* ui-check edge-safe selector=.source-surface top-min=30 top-max=50 right-min=30 right-max=50 */
```

## 5.1 Primary Surface Scale

Classify the primary result surface before sizing it.

Rules:
- Complete product interfaces/pages/views should read as substantial product surfaces, not narrow floating cards.
- On a `900×500` banner, a complete-interface primary surface should usually occupy `45%` to `60%` of banner width, with a practical minimum of `400px` unless the source itself is narrow.
- Real floating panels, popovers, dropdowns, and modal fragments should preserve their compact source scale and should not be inflated into full pages.
- If space is tight, crop or simplify lower-priority secondary UI before shrinking a complete-interface primary result.
- Compact secondary/source interfaces may use `.contained-context-source` and remain fully visible when their width is usually `<= 620px` after non-core chrome removal. Do not force left/bottom crop on narrow context surfaces when full visibility improves the product story.
- Add `/* ui-check min-size selector=.primary-selector min-width=400 */` to complete-interface primary surfaces.

## 5.2 Product Layering And Protected Triggers

Layer by product logic:
- Source/context UI is lowest.
- Intermediate UI such as a menu/dropdown is above the source.
- Result UI created by the action is topmost.
- Required class names: `.source-surface` for the lower context interface, `.intermediate-surface` for menus/intermediate states, `.primary-surface` for the foreground result or main floating panel.
- The checker treats `.primary-surface` below or visually covered by `.source-surface` as a hard failure.

Do not let an intermediate menu appear above the final result unless the source product really keeps that menu open on top of the result. Do not let the primary result cover the key trigger/source element that proves the interaction path. If space is tight, shrink/crop secondary UI before shrinking a complete-interface primary surface.

Protected triggers must keep their parent-component context. A trigger button is not valid if it is merely visible but detached from the input bar, toolbar, menu row, card, or field that explains what it does. For example, an IM `+` action must remain visually inside the composer/input toolbar; do not pull it out as an isolated floating button just to avoid overlap. If the trigger would be covered, move or crop the secondary UI group while preserving the trigger inside its source component.

Use contract markers:

```css
/* ui-check z-index-above selector=.form-panel above=.action-menu */
/* ui-check rect-clearance selector=.form-panel avoid-left=392 avoid-top=445 avoid-width=32 avoid-height=32 clearance=8 */
/* ui-check max-repeat selector=.action-menu item-class=menu-row exclude-class=selected max=5 */
```

## 6. Menu / Popover Basics

These are baseline rules for menus, popovers, and dropdowns across modules.

Rules:
- Preserve source side and trigger relationship.
- Menu gap to icon button trigger: `4px`, tolerance `±1px`, when the source does not specify otherwise.
- For icon-button triggers, default horizontal alignment is right edge to right edge.
- Do not place menus by visual estimation. Define trigger rectangle, menu dimensions, and anchor formula before coding.
- For a menu above an icon button, use: `menuBottom = triggerTop - 4px`.
- For right-aligned icon-button menus, use: `menuRight = triggerRight`.
- If using absolute canvas coordinates, calculate both axes before coding:
  - `triggerRight = triggerLeft + triggerWidth`
  - `menuLeft = triggerRight - menuWidth`
  - `menuTop = triggerTop - 4px - menuHeight`
- Preferred implementation: place the menu inside a positioned trigger wrapper and anchor with `right: 0; bottom: calc(100% + 4px);`. This prevents drift when the composer or trigger moves.
- Row height: use `32px` for compact menu rows unless source says otherwise.
- Icon slot: `24px`; icon visual: `18px`.
- Text starts at a stable x position, usually `40px` from row left for menu rows with icons.
- Selected row keeps source highlight and check/active indicator when it explains the feature.
- If only one menu item is the feature evidence, keep that item real and skeletonize non-selected sibling labels.
- Keep sibling abstraction consistent inside one menu/list/grid group. Do not mix real readable labels and skeleton labels among non-target siblings. Either keep all siblings in the same semantic group real because their labels are needed, or skeletonize/remove all non-target sibling labels.
- When the feature is a single selected type/action/value, default to keeping only the selected/target label real; all other sibling labels become skeleton lines or are removed.
- Selected labels must fit their selected chip/row. Do not use a fixed width that clips or lets text overflow; size the selected item from icon slot + label + horizontal padding, or add a `text-fit` marker.
- Move trigger + menu together if the exact anchor would clip important information.

## 7. Form Preview Basics

For Base form / collection form previews:
- Title: `30px / 46px`, semibold, if it is the main form title.
- Description/helper: lower priority; skeletonize or shorten if it competes with title.
- Question title: `18px / 28px`, medium.
- Question description/body helper: `14px / 22px`.
- Question number column: fixed width around `54px`, right aligned.
- Content column: fixed start around `64px` from question container left.
- Text area / option rows align to the same content column.
- Option row height: `40px`; radius: `8px`; repeated option gap: `8px`.
- Option radio/checkbox is a real control only when visible in source; do not use checkbox-like placeholders for generic icons.

## 8. Verification Gate

Before final output, render the HTML and check:
- repeated rows share the same icon x and text x
- menu gap and alignment match source constraints; for above-trigger menus the measured vertical gap is `4px ±1px`, and right-aligned menus have `abs(menuRight - triggerRight) <= 1px`
- non-cropped edges keep the required safe-margin range, usually `30px` to `50px` when the prompt does not specify otherwise
- secondary backing plate exists when needed and extends `14px` around UI
- avatars and image thumbnails use approved asset files
- all abstract primitives use `rgba(15, 15, 16, 0.06)`

## 9. UI Check Contract Markers

When a component has details that commonly drift, add a `ui-check` contract comment before its CSS rule. The check script can then verify and safely repair the component without needing to understand the feature.

Supported markers:

```css
/* ui-check balanced-padding selector=.component expected=16 */
/* ui-check content-density selector=.floating-panel content-selector=.panel-content top=24 right=24 bottom=24 left=24 */
/* ui-check grid-alignment selectors=".metric-card-a,.metric-card-b,.metric-card-c" tolerance=4 */
/* ui-check no-shadow selector=.component */
/* ui-check shadow-token selector=.floating-panel token=primary */
/* ui-check source-fill selector=.component expected=#F1F2F3 */
/* ui-check skeleton-fill selector=.line expected="rgba(15, 15, 16, 0.06)" */
/* ui-check last-margin-zero selector=.line */
/* ui-check anchored-menu selector=.action-menu trigger-right=474 trigger-top=445 menu-width=180 menu-height=317 */
/* ui-check min-size selector=.form-panel min-width=400 */
/* ui-check max-size selector=.bubble max-width=320 */
/* ui-check radius selector=.floating-panel value=16 */
/* ui-check radius selector=.polish-panel value=16 */
/* ui-check outer-frame selector=.secondary-frame padding=10 background="rgba(255, 255, 255, 0.5)" */
/* ui-check z-index-above selector=.form-panel above=.action-menu */
/* ui-check rect-clearance selector=.form-panel avoid-left=392 avoid-top=445 avoid-width=32 avoid-height=32 clearance=8 */
/* ui-check max-repeat selector=.action-menu item-class=menu-row exclude-class=selected max=5 */
/* ui-check edge-safe selector=.form-panel top-min=30 top-max=50 right-min=30 right-max=50 bottom-min=30 bottom-max=50 */
/* ui-check cropped-edge selector=.secondary-surface side=left,bottom min-out=32 */
/* ui-check parent-context child=.trigger-button parent=.composer offset-parent=.im-panel */
/* ui-check anchored-to menu=.action-menu trigger=.trigger-button parent=.composer offset-parent=.im-panel side=top gap=4 align=right */
/* ui-check no-excess-blank selector=.form-panel content-bottom=440 max-bottom-blank=40 */
/* ui-check group-centered selectors=".phone-frame,.result-panel" axis=x center-x=450 tolerance=24 */
/* ui-check balanced-content-inset container=.result-panel content=.focus-content align=left tolerance=4 */
/* ui-check allowed-text values="客户跟进记录|客户手机号|150|1111|7615|继续" */
/* ui-check text-fit selector=.selected-type text="电话号码" */
/* ui-check abstraction-consistency selector=.type-grid item-class=type-item exclude-class=selected mode=all-skeleton skeleton-class=skeleton-line */
/* ui-check surface-count item-class=ui-surface max=2 */
```

Marker rules:
- Use `balanced-padding` for cards, bubbles, option rows, menu rows, and compact panels.
- Use `content-density` for every `.floating-panel`. It enforces `24px` padding on all four sides and prevents leftover bottom blank.
- Use `grid-alignment` for same-level hand-positioned card/grid rows. Same-row tops, bottoms, and heights must differ by no more than `4px`.
- Use `no-shadow` for product-internal modules.
- Use `shadow-token` for banner-level floating panels. `token=primary` maps to `var(--shadow-primary-strong)`; `token=secondary` maps to `var(--shadow-secondary-soft)`.
- Use `source-fill` when removing shadow would otherwise make a component disappear into its parent surface.
- Use `skeleton-fill` on abstract primitives and placeholder lines.
- Use `last-margin-zero` when repeated skeleton lines use `margin-bottom`.
- Use `anchored-menu` only when wrapper anchoring is impossible; prefer CSS wrapper anchoring with `right: 0; bottom: calc(100% + 4px)`.
- Use `min-size` on complete-interface primary surfaces.
- Use `max-size` on secondary internal modules that must not touch their parent edge after the parent is cropped or narrowed.
- Use `radius` on foreground floating panels, modal-like result panels, and any hand-coded panel whose source radius must not drift. Default to `16px` for `.floating-panel` unless Figma explicitly says otherwise.
- Use `outer-frame` on large secondary/background product UI wrappers so their visible frame stays `10px`, `rgba(255, 255, 255, 0.5)`, and geometrically concentric with the inner UI.
- Use `z-index-above` for product-logic layer order.
- Use `rect-clearance` to protect key triggers/source fields from overlap.
- Use `max-repeat` for repeated abstract-only lists and menus; cap at `5` by default.
- Skeletonize non-core sibling menu/list labels and repeated placeholder text.
- Use `edge-safe` for every non-cropped major surface. Set both min and max values for visible edges. Default range is `30px` to `50px` unless the prompt or case says otherwise. Omit intentionally cropped sides.
- Use `cropped-edge` for secondary/background product surfaces that should intentionally exceed the banner edge. Use it on large table, dashboard, workflow, or app surfaces so they do not regress into short safe cards. Typical value: `side=left,bottom min-out=32`.
- Use `parent-context` for key triggers that must remain inside a toolbar/input/card/row, such as IM `+` inside `.composer`.
- Use `anchored-to` instead of stale hand-written geometry when the trigger can be derived from CSS or a parent context. This checks the real menu-to-trigger gap and alignment from selectors. If the trigger parent is positioned inside another absolute UI surface, include `offset-parent=.surface` so the check uses canvas coordinates.
- Use `no-excess-blank` when a panel was resized for safety and may now contain too much bottom whitespace. If the content is not absolutely positioned, provide an explicit `content-bottom` value after visual/layout calculation.
- Use `group-centered` for single-interface or source-interface-plus-focus-card compositions. It checks the combined bounding box of the listed selectors against the banner center.
- Use `balanced-content-inset` for important containers whose primary content must keep balanced visible spacing. `align=center` compares all four sides; `align=left` compares top/left/bottom; `align=right` compares top/right/bottom. Use `cropped=left,bottom` to exclude intentionally cropped edges.
- Use `allowed-text` when source fidelity matters and the banner must not introduce new readable product states. List only source/user-approved visible text tokens; the script will flag unexpected readable text.
- Use `text-fit` for selected chips, buttons, tabs, menu items, option rows, and compact controls with real text. It checks that the selector has enough width for the declared text plus padding/icon space.
- Use `abstraction-consistency` for menus, lists, grids, table columns, repeated cards, and form sections where same-priority items must not mix real text and skeleton text. Use `exclude-class=selected` or `exclude-class=core` for higher-priority target items.
- Use `surface-count` when a composition must remain one or two UI surfaces. Mark every major product surface with the same class, such as `ui-surface`, and cap the count, for example `item-class=ui-surface max=2`.

## 10. Banner Pointer

Every banner should include the default pointer asset:

```html
<img class="banner-pointer" src="../figma-refs/components/pointer/pointer-arrow-default.png" alt="">
```

Rules:
- topmost layer above all product UI, usually `z-index: 20` or higher
- fixed PNG asset render size `80px × 80px`
- use the complete PNG component directly; do not redraw, recolor, rebuild, add CSS shadow, or extract a sub-shape
- use the cursor to indicate the key interaction target in the foreground panel, never as decoration
- target priority: input field with generated/user-entered command > primary action button > selected condition/tag > key result card
- place near the primary functional target that advances the feature path
- mark the intended target element with `.pointer-target` and `data-pointer-target-role`; if the arrow is not near `.pointer-target`, the output fails
- allowed pointer target roles: `input-command`, `primary-action`, `selected-condition`, `key-result`
- for a selected button/chip such as `电话号码`, the pointer target is that selected chip/button, not an unrelated add/send/background control
- use `scaleX(-1)` for horizontal flip; do not use a different arrow style
- do not scale, resize, stretch, or change pointer proportions
- move the cursor into nearby whitespace; rotate only slightly when needed to point toward the target
- cursor tip should point toward the target element without covering it
- for an input target, prefer pointing to the right edge of the input field or send button area, with the cursor body outside the input
- keep the visible cursor away from the foreground panel edge; use at least `12px` visual clearance when possible
- keep at least `8px` clearance from text, button icons, selected values, and core controls
- do not cover product icons, readable text, selected values, buttons, input values, or core controls
- prefer placing the cursor beside the target, near a card edge, above-right whitespace, or right-side whitespace
- forbidden: cursor floating in unrelated empty background, cursor used only as decoration, cursor pointing away from the key interaction
- keep pointer selectable in HTML previews; do not set `pointer-events: none` for fixed banner output
- include it in the Asset Lock Manifest as `Banner pointer`

Use `z-index-above` when there is any risk of layering drift:

```css
/* ui-check z-index-above selector=.banner-pointer above=.primary-panel */
/* ui-check pointer-target pointer=.banner-pointer target=.pointer-target max-distance=140 role=input-command */
/* ui-check pointer-asset selector=.banner-pointer width=80 height=80 */
```

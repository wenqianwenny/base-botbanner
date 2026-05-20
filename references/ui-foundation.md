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

## 2.1 Text Abstraction Budget

Before coding, classify every visible text string:
- **Core text**: necessary to understand the feature path. Keep real.
- **Context text**: helps identify the product scene. Keep only if short and not competing.
- **Repeated placeholder text**: skeletonize.
- **Sibling menu/list labels**: skeletonize unless the item is selected or feature-relevant.
- **Decorative/helper text**: remove or skeletonize.

Examples:
- In an IM creation menu focused on `收集表`, keep `收集表`; skeletonize other menu item labels.
- In a form preview, keep `收集表`, `问答题`, `单选题`, and the main input placeholder if it explains the field. Skeletonize repeated option placeholder labels such as `请输入选项`.
- If 3 rows repeat the same non-core text, at most one may remain real; usually all repeated labels become skeleton lines.
- Repeated abstract-only rows are capped at `5`. If a group would show more than 5 skeleton-only items, remove the extras instead of making the panel taller.

## 3. Abstract Asset Rules

Use existing assets before drawing generic placeholders.

Rules:
- Real-person avatars: use `figma-refs/components/avatar/Avatar-image-*`.
- Generic product avatars: use `[D] Avatar_Person_blue.svg` or `[D] Avatar_Person_grey.svg`.
- Image thumbnails or picture materials: use `figma-refs/components/image/image1.svg`, `image2.svg`, `image3.svg`, or `image4.svg`.
- Abstract circles, rounded rectangles, skeleton lines, generic icon blocks, and chart primitives must use:

```css
background: rgba(15, 15, 16, 0.06);
```

This is `#0F0F10` at 6% opacity.

Do not:
- generate new avatars
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

## 4.1 Elevation Scope

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

## 5.1 Primary Surface Scale

Classify the primary result surface before sizing it.

Rules:
- Complete product interfaces/pages/views should read as substantial product surfaces, not narrow floating cards.
- On a `900×500` banner, a complete-interface primary surface should usually occupy `45%` to `60%` of banner width, with a practical minimum of `400px` unless the source itself is narrow.
- Real floating panels, popovers, dropdowns, and modal fragments should preserve their compact source scale and should not be inflated into full pages.
- If space is tight, crop or simplify lower-priority secondary UI before shrinking a complete-interface primary result.
- Add `/* ui-check min-size selector=.primary-selector min-width=400 */` to complete-interface primary surfaces.

## 5.2 Product Layering And Protected Triggers

Layer by product logic:
- Source/context UI is lowest.
- Intermediate UI such as a menu/dropdown is above the source.
- Result UI created by the action is topmost.

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
/* ui-check no-shadow selector=.component */
/* ui-check source-fill selector=.component expected=#F1F2F3 */
/* ui-check skeleton-fill selector=.line expected="rgba(15, 15, 16, 0.06)" */
/* ui-check last-margin-zero selector=.line */
/* ui-check anchored-menu selector=.action-menu trigger-right=474 trigger-top=445 menu-width=180 menu-height=317 */
/* ui-check min-size selector=.form-panel min-width=400 */
/* ui-check max-size selector=.bubble max-width=320 */
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
```

Marker rules:
- Use `balanced-padding` for cards, bubbles, option rows, menu rows, and compact panels.
- Use `no-shadow` for product-internal modules.
- Use `source-fill` when removing shadow would otherwise make a component disappear into its parent surface.
- Use `skeleton-fill` on abstract primitives and placeholder lines.
- Use `last-margin-zero` when repeated skeleton lines use `margin-bottom`.
- Use `anchored-menu` only when wrapper anchoring is impossible; prefer CSS wrapper anchoring with `right: 0; bottom: calc(100% + 4px)`.
- Use `min-size` on complete-interface primary surfaces.
- Use `max-size` on secondary internal modules that must not touch their parent edge after the parent is cropped or narrowed.
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

## 10. Banner Pointer

Every banner should include the default pointer asset:

```html
<img class="banner-pointer" src="../figma-refs/components/pointer/pointer-arrow-default.png" alt="">
```

Rules:
- topmost layer above all product UI, usually `z-index: 20` or higher
- default size `90px × 90px`
- use the complete PNG component directly; do not redraw, recolor, rebuild, add CSS shadow, or extract a sub-shape
- place near the key trigger/action/control that advances the feature path
- use `scaleX(-1)` for horizontal flip; do not use a different arrow style
- do not rotate by default; only rotate when explicitly requested or when the supplied Figma case already uses that exact rotation
- do not cover product icons, readable text, selected values, or core controls
- keep pointer selectable in HTML previews; do not set `pointer-events: none` for fixed banner output
- include it in the Asset Lock Manifest as `Banner pointer`

Use `z-index-above` when there is any risk of layering drift:

```css
/* ui-check z-index-above selector=.banner-pointer above=.primary-panel */
```

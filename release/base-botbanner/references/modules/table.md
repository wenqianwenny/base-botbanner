# Table Module — Base Bot Banner

Use this module when the source UI involves Base table/grid views, data tables, records, fields, rows, field types, side navigation plus grid, table toolbar, table footer, or data-state banners.

This module generalizes from the provided original/abstract pair. Do not preserve a fixed example column such as status by default. Choose real fields based on the actual feature story.

Figma references:
- Table original: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=74-26575`
- Table abstract: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=74-26494`

---

## 1. Field Priority Comes From The Feature

Before abstracting a table, identify the feature-relevant field group.

Examples:
- Time-related feature -> keep the date/time field label or values real; skeletonize status/member/category columns.
- Status workflow feature -> keep status tags real; skeletonize time/member/text columns.
- Assignee/member feature -> keep member field and avatars real; skeletonize status/text fields.
- Text generation/import feature -> keep the source text/title field real; skeletonize secondary fields.
- Lookup/formula/rollup feature -> keep the computed/linked field structure real, not necessarily the first column.

Do not blindly copy the approved abstract example's real columns. The example keeps text/status/member because that was its sample content, not a universal rule.

---

## 2. Core Table Structure To Preserve

Preserve the table's recognizability:
- grid container with subtle row and column dividers
- header row with field-type icons
- row number / selection column when visible in source
- 3-5 visible rows
- 2-4 visible fields/columns
- field-specific cell shapes, such as tags, avatars, date chips, text lines, or checkboxes

When the table is background/secondary context:
- crop the table instead of showing the entire 1440px product screen
- prefer an intentional bottom crop when the table would otherwise look short or leave empty vertical canvas space; the cropped bottom side does not need safe margin
- add `/* ui-check cropped-edge selector=.table-surface side=left,bottom min-out=32 */` when the table is used as a large secondary/background product surface
- keep only the grid area and the minimum surrounding chrome needed to identify Base
- remove full side navigation, top page header, toolbar, footer, and add-field area unless they explain the feature path
- keep feature-relevant table states, tags, levels, users, time, and colors semantically consistent with the foreground panel
- do not introduce random table values such as unrelated levels/statuses when the foreground already defines the allowed data state

When the table is the primary result:
- keep enough width for the feature-relevant fields to read
- crop low-priority sidebars before shrinking the table so much that cells are unreadable
- keep the active field/record result unobstructed

---

## 3. Text Budget

Classify text by field relevance:

Keep real:
- feature-relevant field header label
- feature-relevant cell value, tag, date/time, member name, or record title
- selected/active row value if it explains the result

Skeletonize:
- sibling field labels not needed for the feature
- repeated text rows in non-feature columns
- long record content not needed for the story
- member names when the feature is not about people

Remove:
- extra hidden/secondary view tabs
- toolbar labels and calculations when not part of the feature
- side navigation file list when it is only product chrome
- add-field/add-record columns unless the feature is about adding fields/records

If more than 5 repeated abstract-only rows are visible, remove extras instead of making the table taller.

---

## 4. Field Type Abstraction

Use the source field type to choose the abstraction shape.

Text / long text:
- use skeleton pills or one real text value if the text field is the feature
- row text starts must align in one column
- approved skeleton fill: `rgba(15, 15, 16, 0.06)`

Single select / status:
- preserve colored rounded tags when status is the feature
- if status is secondary, tags may remain as colored pills without readable text
- avoid too many competing tag colors; 2-4 colors is enough for a banner

Member:
- preserve small round avatars when member assignment is relevant
- use approved preset avatars where available
- skeletonize member names when not central
- do not replace member avatars with generic squares

Date/time:
- preserve time/date text or date-chip structure when time is the feature
- skeletonize other fields instead of losing the date evidence

Checkbox:
- keep actual checkbox shape only when source cell is a checkbox field or selection column
- do not use outlined square placeholders for non-checkbox icons

Field icons:
- Keep field-type icons in the header if they help distinguish field types.
- Non-core field icons may be simplified, but they must stay consistent per column.
- Do not mix arbitrary icon shapes within the same header row.

---

## 5. Grid Layout Rules

Tables fail quickly when columns drift. Use a stable grid.

Rules:
- Define column widths first, then place header and body cells on the same x positions.
- Header icon/text and body content in the same field must share the same left inset.
- Row heights must be consistent unless a source row is explicitly expanded.
- Row number/selection column must keep a stable center line.
- Table cells must contain their children. Skeleton bars must not touch cell borders or overflow across grid lines.
- Use cell padding and child max-width constraints for skeleton bars; do not use `width: 100%`.
- Default abstract table cell padding: `12px 16px` for roomy tables, or a proportional equivalent for compressed tables.
- Default skeleton line: `width: 72%`, `max-width: 160px`, `border-radius: 999px`.
- Cell containers should use `overflow: hidden` when content is close to grid lines or rounded corners.

Required containment marker:

```css
/* ui-check component-containment parent=.table-cell child=.skeleton-line inset=12 */
```
- Dividers should be subtle and consistent: use source-like neutral dividers, not heavy borders.
- Skeleton rows must align to the same left inset as the real rows.
- Do not let a foreground panel accidentally share a flush edge with table columns unless intended.

Use ui-check markers when possible:

```css
/* ui-check max-repeat selector=.table-body item-class=table-row max=5 */
/* ui-check skeleton-fill selector=.cell-skeleton expected="rgba(15, 15, 16, 0.06)" */
/* ui-check no-shadow selector=.table-grid */
/* ui-check cropped-edge selector=.table-surface side=left,bottom min-out=32 */
```

---

## 6. Approved Abstract Table Pattern

The approved abstract table example uses:
- white table surface
- rounded outer corners around `10px`
- row/column dividers
- header height around `52px` at the reference scale
- body row height around `48px` to `50px` at the reference scale
- row numbers on the left
- field headers with an icon plus a short skeleton label
- text cells with either one real value or skeleton pill
- status cells with colored rounded tags
- member cells with avatar plus either real name or skeleton name

This is a style reference, not a fixed data recipe. The actual banner must decide which field remains real based on the feature.

---

## 7. Verification

Before output:
- The feature-relevant field is the clearest readable field.
- Non-feature columns are skeletonized or removed.
- The table grid remains recognizable after cropping.
- Header and body columns align exactly.
- Row heights and row-number alignment are stable.
- Abstract text uses `rgba(15, 15, 16, 0.06)`.
- Real text budget is limited to feature evidence and necessary context.
- Side navigation, toolbar, footer, add-field, and add-record areas are removed unless they are part of the product path.
- If the feature is about time/status/member/text, the corresponding column is preserved as real and sibling columns are reduced.
- Use `allowed-text`, `max-repeat`, `skeleton-fill`, `no-shadow`, `edge-safe`, and `min-size` markers where applicable.

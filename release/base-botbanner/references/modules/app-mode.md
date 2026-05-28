# App Mode Module — Base Bot Banner

Use this module when the source UI involves Base App Mode, app pages, business app views, app navigation, app cards/lists, app dashboards, app tables, app forms, or an end-user app surface built from Base data.

This module is a container rule. App Mode often contains table, form, dashboard, card-list, or detail components. First preserve the app shell and route logic, then apply the relevant child module rules to the inner content.

Figma references:
- App Mode original: `https://www.figma.com/design/SYKM6v8NzaaJ22C6fUlmwG/Untitled?node-id=21-17942`
- App Mode abstract: `https://www.figma.com/design/SYKM6v8NzaaJ22C6fUlmwG/Untitled?node-id=21-18269`

---

## 1. Module Role

App Mode is usually not the feature by itself. It is the product surface where a Base capability becomes an end-user app experience.

Before drawing, identify whether App Mode is:
- the primary result interface, such as a created app page or final end-user view
- the secondary source/context interface, such as app navigation before opening a feature
- a container around a table, form, dashboard, card list, or record detail module

If the feature is inside the App Mode page, do not let the app shell consume the banner. Keep enough shell to identify App Mode, then allocate visual priority to the feature-relevant inner component.

---

## 2. Product Structure To Preserve

Preserve the structure that explains the feature:
- app side navigation or top navigation when it identifies the selected app/page
- selected navigation item, selected route, or selected page state
- main page canvas and its content columns/cards/lists
- key inner component that carries the feature evidence
- page-level relationship between navigation and content

If the App Mode page contains child modules:
- table/grid -> also read `references/modules/table.md`
- form/questionnaire -> also read `references/modules/form.md`
- dashboard/charts/metrics -> also read `references/modules/dashboard.md`
- workflow/automation entry -> also read `references/modules/workflow.md`

Do not redraw the inner module from generic shapes when a child module rule exists.

---

## 3. Information Priority

### Keep Real

Keep text and states real when they explain the current feature:
- selected app/page/nav label
- page title or app title if it identifies the scenario
- feature-relevant card title, record title, form question, dashboard metric title, table field, or route
- primary action or selected state only when it is part of the feature path

### Skeletonize

Skeletonize information that supports structure but is not the story:
- unselected navigation labels
- repeated list/card row text
- secondary card descriptions
- sibling metric/card labels
- non-core table/form/dashboard labels inside the app

Use the standard skeleton fill:

```css
background: rgba(15, 15, 16, 0.06);
```

### Remove

Remove elements that compete with the app feature:
- top-right utilities, app chrome, overflow menus, watermarks, scrollbars, and pagination when not part of the path
- repeated abstract-only app buttons/cards/list rows beyond 5
- full side navigation if only one selected route is needed for context
- decorative app thumbnails or images when they do not explain the feature

If removing an element does not hurt recognition of App Mode or the feature path, remove it instead of skeletonizing it.

---

## 4. App Shell Abstraction

The approved abstract pattern keeps:
- a simplified left nav rail around `56px` at the reference scale
- compact selected/content area
- small card/button group at the top
- a main list/table/card region with aligned columns
- subtle border/card lines from source UI

Rules:
- Keep the selected route visually clear.
- Unselected nav items may become short skeleton bars.
- Navigation icon shapes should remain semantically consistent, but non-core icons can be simplified.
- Do not show a full 260px side navigation if it forces the primary app content to be tiny.
- Do not keep all source widgets. Keep only enough to show the app surface and the feature-relevant component.

---

## 5. Inner Content Rules

App Mode inner content should be reduced before the whole interface is scaled down.

For lists/cards:
- keep 2-4 visible rows/cards
- keep one feature-relevant card title real if it explains the story
- skeletonize card metadata and descriptions
- remove action buttons unless the feature is about the action

For metric/dashboard areas:
- use dashboard templates for metric cards and charts
- keep 1-3 visible metrics/charts unless the dashboard itself is the feature
- do not invent fake chart shapes; follow dashboard module templates

For tables/forms:
- use table/form module rules
- keep the relevant field/question real
- skeletonize sibling columns/options/questions

Use ui-check markers:

```css
/* ui-check max-repeat selector=.app-list item-class=app-row max=5 */
/* ui-check skeleton-fill selector=.app-skeleton expected="rgba(15, 15, 16, 0.06)" */
/* ui-check no-shadow selector=.app-internal-card */
```

---

## 6. Banner Layout

When App Mode is the primary result:
- give it substantial scale, usually `45%` to `60%` of the banner width or at least `400px`
- crop low-priority shell/chrome before shrinking the feature content
- keep selected page/content readable

When App Mode is secondary context:
- crop it from the left or bottom so it reads as a source surface
- keep selected nav/route or trigger visible if it explains the path
- reduce repeated app rows/cards instead of allowing edge crowding

Do not invent an additional desktop/editor/table surface if only App Mode was provided. If one source interface is provided, use App Mode alone or App Mode plus a focus card extracted from the same page.

---

## 7. Verification

Before output:
- App Mode is recognizable from shell + selected route + page content.
- The feature-relevant inner component has the highest clarity.
- Unrelated app chrome and repeated abstract rows are removed.
- Child module rules were applied for tables/forms/dashboards/workflows inside the app.
- Selected nav/page state comes from the source design or user request.
- No random app images, icons, or extra pages were invented.
- Internal app cards do not get floating-panel shadows unless they are actual floating overlays in the banner.
- Use `allowed-text`, `max-repeat`, `skeleton-fill`, `no-shadow`, `balanced-content-inset`, `edge-safe`, and `min-size` markers where applicable.

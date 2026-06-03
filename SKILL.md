---
name: base-botbanner
description: "Generate and abstract Base Bot Banner HTML for Lark Base (飞书多维表格) feature announcements. Use this skill whenever the user asks to create, revise, evaluate, or export a Base product banner, bot banner, feature announcement visual, 功能横幅, 产品banner, 界面抽象, 抽象UI, UI abstraction, dashboard/chart abstraction, or wants to turn Base/Figma/product UI screenshots into a 900×500 feature banner. Also trigger when the user mentions Lark Base banner, 多维表格 banner, Base banner, Base UI abstraction, or any task involving Base product feature visuals."
---

# Base Bot Banner HTML Skill

Generate 900×500px HTML/CSS banners for Lark Base feature announcements.

**Abstraction is mandatory whenever product UI, screenshots, Figma URLs, or design references are provided.** Do not directly paste, trace, or fully reproduce the source UI. Preserve product logic and key geometry, then abstract non-core information into clean product-native skeletons/placeholders.

**Figma Banner Specification is the concrete Base banner standard.** When a Figma design/spec/reference is provided, treat it as the executable product standard and layout specification, not mood inspiration. Preserve product behavior, component relationships, spacing, alignment, radius, shadow, states, and asset choices unless an abstraction rule explicitly simplifies non-core details. If skill rules and Figma conflict, Figma wins for product logic and UI detail constraints; banner composition rules only decide canvas safety, crop, and visual hierarchy around those constraints.

**Read [`references/visual-direction.md`](references/visual-direction.md) before generating any new banner.** It is the taste layer: anti-AI cliches, composition strategy, variant planning, and the required Visual Strategy gate.

**Read [`references/ui-foundation.md`](references/ui-foundation.md) before generating any banner.** It contains baseline alignment, abstraction assets, secondary UI compression, backing plate, menu/popover, form preview, and banner edge safety rules.

**Read [`references/layouts.md`](references/layouts.md) before generating any banner.** It contains hard layout constraints: 900×500 canvas, 30-50px non-cropped safe area, source/primary surface classes, left/bottom crop contract, and script-enforced layout checks.

**Read [`references/design.md`](references/design.md) before generating any banner.** It contains all visual rules, design tokens, composition grammar, abstraction techniques, and component specs.

**Mandatory module rule:** If the request or source UI involves dashboard / 仪表盘 / 指标卡 / 图表卡 / 透视表 / 排行榜, read [`references/modules/dashboard.md`](references/modules/dashboard.md) before writing HTML. Dashboard component templates are low-freedom: copy and adapt the canonical template file instead of redrawing from description.

**Mandatory module rule:** If the request or source UI involves IM / chat / bot messages / composer input / action menu / popover-triggered creation / 收集表 from IM, read [`references/modules/im.md`](references/modules/im.md) before writing HTML. IM component relationships are low-freedom: composer input, trigger button, and opened menu must move as one anchored group.

**Mandatory module rule:** If the request or source UI involves form / questionnaire / 问卷 / 收集表 / 填写页 / 题型 / form field / option rows / submit state, read [`references/modules/form.md`](references/modules/form.md) before writing HTML. Form abstraction must start from product path and information priority, not from copying every visible field.

**Mandatory module rule:** If the request or source UI involves table / grid view / data table / 数据表 / 表格视图 / 记录 / 字段 / field columns / record rows, read [`references/modules/table.md`](references/modules/table.md) before writing HTML. Table abstraction must choose real fields from the feature story, not from a fixed example column.

**Mandatory module rule:** If the request or source UI involves App Mode / 应用模式 / app page / app view / business app / app navigation / end-user app surface, read [`references/modules/app-mode.md`](references/modules/app-mode.md) before writing HTML. App Mode is a container module: preserve selected route and app/page structure, then apply child module rules for inner tables, forms, dashboards, or workflows.

**Mandatory module rule:** If the request or source UI involves workflow / automation / 自动化流程 / trigger / action / node / branch / config panel / run log, read [`references/modules/workflow.md`](references/modules/workflow.md) before writing HTML. Workflow abstraction is path-first: preserve trigger -> action/result order, connectors, selected node state, and node/config relationships before simplifying text.

---

## Input & Output

### Input

| Parameter | Required | Description |
|---|---|---|
| Feature description | Yes | New feature name and description text |
| Key product UI screenshot / Figma URL / design reference | Yes | Original product interface reference to audit and abstract |

### Output

- Development HTML file with `<style>` tag (no inline styles, no external CSS)
- Planning brief (`output/<banner-name>.brief.md`) recording the required strategy, audit, abstraction, asset locks, and verification
- Share HTML file (`*.share.html`) with local image assets inlined as data URIs, suitable for sending to teammates as a single file
- Fixed dimensions: **900 × 500px**
- Final exported PNG must be **2x high-resolution**: `1800 × 1000px`, named `output/<banner-name>@2x.png`

### Technical Constraints

- Font: **PingFang SC** only, no external fonts
- No AI-generated or random images — only approved assets from `figma-refs/backgrounds/`
- No external CSS frameworks or libraries
- All styles in a single `<style>` tag within the HTML

---

## Generation Workflow

```
1. Receive feature description + product UI screenshot
       ↓
2. User Choice Gate — ask for background and layout A/B/C unless already specified
       ↓
3. Visual Strategy — define the product story, taste constraints, and composition direction
       ↓
4. Source UI Audit — identify Base modules and component inventory
       ↓
5. Source UI Fidelity — record preserved elements and their locked style/layout constraints
       ↓
6. Abstraction Plan — decide what stays real, becomes skeleton, or is removed
       ↓
7. Write `output/<banner-name>.brief.md` with the required planning sections
       ↓
8. Load module rules and templates
       ↓
9. Define key information and primary/secondary UI
       ↓
10. Abstract product interfaces — hide unnecessary information
       ↓
11. Banner layout — position primary and secondary UI
       ↓
12. Apply chosen background and refine UI details
       ↓
13. Quality check and output files
```

### Step Details

**Step 2 — User Choice Gate**

For every new banner request, resolve the background choice and layout choice before implementation unless the user has already specified them in the prompt. This is a hard stop.

If either choice is missing, ask only for the missing choice(s) and stop. Do not output Visual Strategy, Source UI Audit, Temporary Module Rule, Abstraction Plan, UI Detail Constraints, Asset Lock Manifest, brief files, HTML, share HTML, or PNG until the user answers.

```text
Before I generate, please choose:

Layout:
- A: primary on the right, secondary on the left
- B: primary on the left, secondary on the right
- C: secondary shown complete-width, primary overlaps it

Background:
- green-mist
- green-spring
- dreamy-pink
- blue-soft-flow
- elegant-purple
```

Rules:
- If the user already specifies a background, record it and do not ask again.
- If the user already specifies layout A, B, or C, record it and do not ask again.
- Do not ask the user to choose abstraction mode.
- Layout A: secondary/source/lower UI on the left and primary/result/floating UI on the right.
- Layout B: primary/result/floating UI on the left and secondary/source/lower UI on the right.
- Layout C: secondary/source UI is shown without left/right crop, may crop bottom, and primary/result/floating UI overlaps it.
- Default abstraction: abstract all product UI by default. Preserve a module or surface unabstracted only when the user explicitly says that module/surface should not be abstracted.
- If the user explicitly asks to proceed without questions, use layout A and a background by feature mood, then record those defaults.
- If this gate is skipped, the banner workflow fails even if the generated brief later contains a User Choices section.

Write the resolved choices into the brief:

```text
User Choices:
- Background:
- Layout option:
- Layout default:
- Abstraction default:
- Defaults used:
```

**Step 3 — Visual Strategy**

Before drawing or coding, use `references/visual-direction.md` to define the banner direction. The goal is to avoid mechanically assembling UI pieces.

For non-trivial or ambiguous new banners, briefly compare 2-3 composition plans:
- Spec-safe
- Focused
- Editorial

Then choose one plan before implementation. For simple edits to an existing banner, skip variants and state the chosen strategy directly.

Write this before implementation:

```text
Visual Strategy:
- Feature idea:
- Product evidence:
- Core path:
- UI surfaces:
- Background mood:
- Abstraction decisions:
- Negative constraints:
- Chosen plan:
```

Reject plans that rely on decorative filler, fake data, generic AI glow, or extra UI surfaces that do not explain the product path.

**Step 4 — Source UI Audit**

Before deciding layout or drawing HTML, inspect the source UI and produce a brief module inventory. The user should not need to name module files or templates.

Identify:
- Base module type: table, form, workflow, dashboard, kanban, gantt, calendar, gallery, IM, App Mode
- Component types inside the module: metric card, column chart, radar chart, donut/ring chart, ranking list/leaderboard, pivot table, filter/config panel, table grid, form field, workflow node, message card, etc.
- Which components are primary feature evidence, secondary context, or removable decoration

If the detected module has no dedicated rule file, create a temporary module rule from the provided source UI before implementation. Do not ask the user to predefine the module. Use the temporary rule for the current banner, then promote reusable parts to `references/modules/<module>.md` after the user approves the output.

```text
Temporary Module Rule:
- Module type:
- Product structure:
- Reusable component patterns:
- Fixed UI constraints:
- Abstraction rules:
- Preserve / skeletonize / remove:
- Required assets:
- Required ui-check markers:
- Fidelity risks:
```

If the source UI contains dashboard / 仪表盘 or dashboard-like components:
- Automatically read `references/modules/dashboard.md`
- Automatically use dashboard templates when matching components are detected
- Metric card detected -> copy `assets/templates/dashboard/metric-card-abstract.html`
- Column chart detected -> follow `references/modules/dashboard.md` Column Chart Card Abstraction
- Radar chart detected -> copy `assets/templates/dashboard/radar-chart-abstract.html`
- Donut/ring chart detected -> copy `assets/templates/dashboard/donut-chart-abstract.html`
- Ranking list / leaderboard detected -> copy `assets/templates/dashboard/ranking-list-abstract.html`
- Pivot table detected -> follow dashboard pivot/table rules when available; if unavailable, preserve table structure and abstract conservatively

If the source UI contains IM / chat / bot messages / composer input / action menu / 收集表:
- Automatically read `references/modules/im.md`
- Identify the composer group, trigger icon/button, opened menu/popover, selected item, message bubble/card, and result surface
- Keep the feature trigger and selected action visible
- Remove unrelated IM top-right tools and full message history unless they explain the feature path

If the source UI contains form / questionnaire / 问卷 / 收集表 / 填写页 / 题型 / option rows / submit states:
- Automatically read `references/modules/form.md`
- Identify the form page type, current/featured question, field type, option/input structure, submit area, and any source visual/image region
- Keep the form title, current feature field, and field structure readable
- Skeletonize low-priority subtitle, sibling option labels, repeated placeholders, and non-core question content
- Remove top operation bars, invisible editing affordances, extra questions, and unrelated media when they do not explain the feature path
- If a visual/image region remains visible, identify whether it is a real Figma/source image asset. If yes, download and lock that exact asset before coding; do not substitute a CSS gradient, generated image, background asset, or unrelated local image.

If the source UI contains table / grid view / data table / 数据表 / 表格视图 / records / fields / rows:
- Automatically read `references/modules/table.md`
- Identify the feature-relevant field group before choosing real text
- Keep the table grid, header/body alignment, row rhythm, and field-type structure recognizable
- Preserve real values only for fields that explain the feature, such as time for time-related features or status for workflow/status features
- Skeletonize or remove sibling columns, repeated text, side navigation, toolbar, footer, add-field, and add-record chrome when they are not part of the feature path

If the source UI contains App Mode / 应用模式 / app page / app view / app navigation / end-user app surface:
- Automatically read `references/modules/app-mode.md`
- Identify whether App Mode is the primary result, secondary source context, or a container around table/form/dashboard/workflow content
- Keep the selected app/page/nav route and feature-relevant inner component readable
- Apply child module rules for any inner table, form, dashboard, workflow, card list, or record detail
- Skeletonize or remove unselected nav labels, repeated app rows/cards, top-right utilities, watermarks, and unrelated app chrome

If the source UI contains workflow / automation / 自动化流程 / trigger / action / node / branch / config panel:
- Automatically read `references/modules/workflow.md`
- Write the real path order before drawing, such as `trigger -> data step -> AI/action step -> result`
- Keep key trigger/action/result node titles real and preserve connector direction, node order, selected state, and add-node position
- Show config panels only when they are feature evidence; otherwise simplify the canvas path
- Remove unrelated sidebars, top bars, run logs, branches, help controls, and repeated abstract-only nodes

Write the audit before implementation in this format:

```text
Module Inventory:
- Module: Dashboard
- Components: metric card x2, pivot table x1, config panel x1
- Templates to use: assets/templates/dashboard/metric-card-abstract.html
- Real information to keep:
- Information to abstract:
- Information to remove:
```

**Step 5 — Abstraction Plan**

If any source UI is present, write an explicit abstraction plan before loading templates or coding. This is required even when the user does not use the word "abstract".

Use this format:

```text
Abstraction Plan:
- Product structure to preserve:
- Real information to keep:
- Information to skeletonize:
- Information to remove:
- Text abstraction budget:
- Source spacing constraints:
- UI Detail Constraints:
- Required local assets:
- Component templates / module rules needed:
- Fidelity risk:
```

Rules:
- Keep the real feature trigger, source context, and result state readable.
- Skeletonize low-priority labels, helper copy, repeated rows, secondary chart labels, unrelated fields, and background data.
- Explicitly budget real text. Keep only text that explains the feature path, selected state, source object, or primary result. Skeletonize non-core sibling menu/list labels and repeated placeholder text.
- Repeated abstract-only information is capped. If a group has more than 5 repeated abstract items, remove the extras instead of displaying more skeleton rows.
- Remove secondary abstract media thumbnails/images when they do not explain the feature path. Do not show a large abstract image just because it existed in the source card.
- Remove decorative or unrelated product chrome when it does not explain the feature path.
- For non-core top bars, toolbars, page headers, and top-right actions, remove the whole chrome region instead of keeping empty button/control shells with text removed.
- Treat provided Figma rules as the concrete Base banner standard. Do not reinterpret exact spacing, alignment, state, or component relationships as loose visual inspiration.
- Spacing Fidelity is mandatory for preserved source UI. Record exact source spacing relationships before coding, and do not normalize source values to design-token values such as `18px` -> `16px`, `22px` -> `24px`, or `37px` -> `32px`.
- Extract UI Detail Constraints from the source design before coding. Include component anchoring, exact gaps, alignment, radius, shadows, selected state, and interaction-specific placement that must not drift during banner composition.
- Do not keep raw screenshots as the main UI layer. Rebuild/compose the UI as HTML using abstraction rules and templates.
- If the source UI or banner needs any avatar/member/user/person/assignee visual, it must be an `<img>` asset from `figma-refs/components/avatar/`. Do not draw avatar placeholders, CSS circles, initials, generated faces, cropped screenshots, or external images.
- If the user provided, updated, named, or already used a background asset, preserve that background unless the user explicitly asks to change it.
- If the source UI includes dashboard-like components, this step must identify metric cards, charts, pivot tables, ranking lists, and config panels before implementation.

After the abstraction plan, write an Asset Lock Manifest before coding:

```text
Asset Lock Manifest:
- Background: figma-refs/backgrounds/<exact-file>.png
- Avatars: figma-refs/components/avatar/<exact-file>.svg, ...
- Product icons: figma-refs/components/icons/<exact-file>.svg, ...
- Banner pointer: figma-refs/components/pointer/pointer-arrow-default.png
- Source UI image assets: output/assets/<exact-file> or figma-refs/components/image/<exact-file>, ...
- Component SVGs/templates:
- Assets intentionally abstracted:
```

For every visible source/Figma image asset kept inside a product UI, add a role entry under the same Asset Lock Manifest:

```text
- role: form-theme-image
  asset: output/assets/<banner-name>/form-theme-image.png
  source: Figma node / source UI region description
  selector: .form-theme-image
  fallback_allowed: false
```

Render it as an actual image element with the matching role:

```html
<img class="form-theme-image" data-source-image-role="form-theme-image" src="assets/<banner-name>/form-theme-image.png" alt="">
```

If the source image cannot be downloaded, remove or crop that image region. Do not approximate it with CSS gradients, background assets, or generic abstract images.

When a core semantic icon is visible, also write an Icon Lock Manifest:

```text
Icon Lock Manifest:
- role: polish-trigger-icon
  asset: figma-refs/components/icons/icon_effects_outlined.svg
  required_in_selector: .polish-button img
  fallback_allowed: false
- role: polish-panel-header-icon
  asset: figma-refs/components/icons/icon_effects_outlined.svg
  required_in_selector: .polish-panel-header img
  fallback_allowed: false
```

Rules:
- The HTML must reference the exact locked background filename. Do not swap to another background because it feels more suitable.
- Every banner should use the locked banner pointer asset `figma-refs/components/pointer/pointer-arrow-default.png` directly as the topmost narrative pointer unless the user explicitly asks to omit it. Do not redraw it, rebuild it with CSS, add CSS shadow, or change its angle.
- Every real-person avatar visible in the banner must use a locked `Avatar-image-*` SVG. Do not create CSS faces, gradient circles, initials, or random portraits.
- If a visible product icon has a matching library asset, lock and use that exact SVG. Only abstract icons after classifying them as non-core or semantically generic.
- Core feature icons and source-provided semantic icons must be treated as product evidence, not decorative detail. If Figma provides an icon node or the local icon library has a matching SVG, use that SVG path/file and list it in the Asset Lock Manifest. Do not approximate table, filter, AI input, voice, send, selected action, or primary field-type icons with CSS-drawn shapes.
- Core semantic icons must be rendered with `data-icon-role` and the exact locked asset path, for example `<img data-icon-role="polish-panel-header-icon" src="../figma-refs/components/icons/icon_effects_outlined.svg" alt="">`. Do not use CSS-drawn fallback classes such as `.sparkle-icon`, `.star-icon`, `.magic-icon`, or `.css-icon` for locked icon roles.
- If the provided Figma/source UI contains a visible image/cover/banner asset that remains visible in the abstracted product UI, lock and reuse that source image asset instead of approximating it with CSS gradients or another background. Store remote Figma assets locally before generating share HTML.
- Source/Figma image assets that remain visible must be downloaded into `output/assets/<banner-name>/` or reused from `figma-refs/components/image/`, listed in the Asset Lock Manifest with a `role`, and rendered with `data-source-image-role`. CSS gradients are allowed for the overall banner background only, not for source product image regions.

For UI Detail Constraints, use `references/ui-foundation.md` as the baseline and add source-specific constraints from Figma: anchoring/gap, alignment, radius, selected state, padding grid, elevation scope, source fills/strokes, and protected triggers.

**Step 6 — Write the planning brief**

Before coding, save the planning work to `output/<banner-name>.brief.md`. This brief is a required output artifact, not chat-only reasoning. It must contain these headings:

```text
## User Choices
## Visual Strategy
## Source UI Audit
## Source UI Fidelity
## Temporary Module Rule
## Abstraction Plan
## UI Detail Constraints
## Asset Lock Manifest
## Implementation Notes
## Verification
```

If no temporary module rule is needed, keep the heading and write `Not needed: <reason>`. Do not omit the section.

**Step 7 — Load Module Rules and Templates**

Load only the module references needed by the audit.

Rules:
- Do not ask the user which module file to read.
- Infer modules from the source design/screenshot/Figma node.
- If a module template exists, copy and adapt it instead of recreating from prose.
- If no module rule/template exists, use the Temporary Module Rule from Step 4 and keep abstraction conservative.

Current module references:
- Dashboard / 仪表盘: `references/modules/dashboard.md`
- IM / chat / bot messages / composer / action menus: `references/modules/im.md`
- Form / questionnaire / 收集表 / field types: `references/modules/form.md`
- Table / grid view / records / fields: `references/modules/table.md`
- App Mode / 应用模式 / app page / app navigation: `references/modules/app-mode.md`
- Workflow / automation / 自动化流程 / trigger/action nodes: `references/modules/workflow.md`
- Dashboard metric card template: `assets/templates/dashboard/metric-card-abstract.html`
- Dashboard radar chart template: `assets/templates/dashboard/radar-chart-abstract.html`
- Dashboard donut/ring chart template: `assets/templates/dashboard/donut-chart-abstract.html`
- Dashboard ranking list template: `assets/templates/dashboard/ranking-list-abstract.html`

**Step 8 — Define key information and primary/secondary UI**

Based on the feature description, determine:
- What is the core feature to highlight?
- What is the core interaction path? Identify the trigger, source input/context, and result state.
- What source surfaces were actually provided? Keep source provenance. If only one original interface is provided, every product UI surface in the banner must come from that same interface or be a magnified abstraction of a component inside it. Do not add another platform, module, page, table, editor, admin surface, or extra product state unless it was provided or explicitly requested.
- Which UI state best represents the feature result? → **Primary UI**
- Which UI provides context or shows the workflow/source? → **Secondary UI**
- Is there a necessary intermediate UI that represents a real third step? → **Optional Tertiary UI**
- Is the primary result a complete product interface/page, or a floating panel/popover/modal? This decides scale.

Use the fewest truthful surfaces that explain the feature. Two surfaces are common, but not mandatory. If only one source interface is provided, a single-interface composition is valid; center it or place it slightly off-center if that gives the key content the best scale. Do not invent a second interface from another platform or module just to make the banner feel richer. A third UI layer is allowed only when the real product scenario has three necessary steps and each layer explains a distinct part of the path.

For field-level, type-level, or single-component features, prefer a source-interface-plus-focus-card pattern: keep the provided interface as context, then enlarge the key field/control/state into a foreground floating card derived from that same source UI. This is allowed even when the source design does not literally show a separate popover, because it is a magnified abstraction of the same component, not a new product surface.

For a single-interface plus focus-card composition, treat the source interface and focus card as one composition group. Center the group on the banner or balance it intentionally; do not leave one side mostly empty unless that empty space is part of the intended crop. The focus card may overlap the source interface, but it must not feel detached from it.

The focus card can magnify only information and states that exist in the provided source UI, or states explicitly requested by the user. Do not add validation messages, success states, cursor states, helper text, selected states, or callouts that were not present in the source design or user request.

Write the core path as a concrete sequence before layout, such as `source input -> polish trigger -> result panel`. Keep those elements real, readable, and unobstructed.

Primary UI scale rule:
- If the source result is a complete product interface/page/view, do not compress it into a narrow floating-panel size. It should usually occupy `45%` to `60%` of the banner width, or at least `400px` on a 900px banner when used as the primary result.
- If the source result is a real floating panel/popover/modal, preserve its compact source scale and do not inflate it into a full page.
- If a complete-interface primary must overlap secondary UI, overlap or crop lower-priority secondary context before shrinking the primary result.
- Add `/* ui-check min-size selector=.primary-selector min-width=400 */` to complete-interface primary surfaces.

Source/context surface scale rule:
- Do not over-compress a source product page when the banner still has unused space. If the source context is a PC form/questionnaire/table/app/workflow page and remains important to understanding the feature, it should usually occupy at least `58%` of banner width unless another primary surface truly needs the room.
- When the source/context surface is placed on the left and is lower priority than a foreground panel, enlarge it and crop low-priority `left` and/or `bottom` edges before shrinking it into a safe card. Left-side source pages may extend beyond the banner left edge and bottom edge; non-cropped top/right edges still follow the safe-margin range.
- If the source/context surface exists only to communicate a form/table/dashboard/workflow body, remove unrelated outer chrome such as side navigation, top navigation, toolbars, tabs, app switchers, and decorative visual regions before reducing the size of the core content. Keep outer chrome only when it is part of the feature path or needed to identify the module.
- Preserve source order and index for visible ordered content. Do not renumber questions, move the featured item from first to second, or reorder questions/rows/steps/menu items/ranked lists unless the source or user explicitly changes the order.
- Compact floating panels such as add/type-picker/filter/action/config panels should preserve real target labels and be centered vertically when they fit. Do not skeletonize them completely.

Product layer rule:
- Order surfaces by product logic, not by which panel was drawn last. For paths such as `source UI -> menu/intermediate -> result UI`, the result UI is topmost, the menu/intermediate sits below it, and the source UI is lowest.
- Use required surface class names so the checker can enforce the layer order: foreground/result/floating panel uses `.primary-surface`; lower source/context interface uses `.source-surface`; optional intermediate menu uses `.intermediate-surface`.
- If the primary surface overlaps the source surface, it must visually cover the source surface. A source/context UI covering the primary result is a hard failure.
- The primary result must not cover the key trigger that proves the path, such as the IM `+` button. If a larger primary result conflicts with the trigger, shrink/crop the secondary source UI first.
- Add `z-index-above` to primary result surfaces and `rect-clearance` for protected triggers when overlap is likely.

**Step 9 — Abstract product interfaces**

If the user provides a Figma URL, screenshot, or design file, inspect it first and treat it as the source of truth for product logic and geometry. Preserve the real component hierarchy, relative positions, spacing, icon choice, radius, line weight, and copy unless the abstraction rules explicitly say to crop or hide that detail.

Keep only key functional states, critical interaction areas, and feature-relevant information. Use `references/ui-foundation.md` for abstraction budgets, icon abstraction, padding, source fill, menu/popover, and form basics. Use `references/design.md` Section 7 for abstraction levels and product-logic rules. Do not invent comparison panels, extra labels, new information placement, or a second product platform not present in the source.

Keep the core feature trigger and result fully visible. If foreground UI covers a key trigger/source field, resize, crop, or simplify secondary UI first. Do not crop core IM messages, selected menu items, trigger buttons, result panels, or primary fields at the banner edge.

For mobile source UI, remove system chrome such as status bars, dock bars, and OS indicators by default unless the feature depends on them or the user asks to preserve the literal full device frame. Keep product chrome such as nav bars when it helps identify context.

**Step 10 — Banner layout**

Position the UI layers. First apply `references/layouts.md`, then use `references/design.md` → Composition System (Section 3), Layout Rules (Section 5), Cropping Grammar (Section 4).

Default to the fewest truthful surfaces. If there is one source interface and no separate real result/intermediate surface, use one centered or slightly offset product interface, optionally with a foreground focus card extracted from its key component. Use a two-surface composition when there are real source/result states or when a source page plus magnified component best explains a field-level feature. Use a tertiary UI only when it is a real middle step in the feature path, visually weaker than the primary UI, and simpler than both main layers.

The secondary/background UI is cropped by default when it is a large source surface. Place it with negative left offset (`left: -48px` to `-96px`) so part of the UI extends beyond the banner's left edge. If its full left rounded corner is visible, it is not cropped enough. The safe margin applies only to non-cropped edges, not to the intentionally cropped side. When this surface is the left-side context, add class `.left-context-source`; it must overflow the left and bottom canvas edges.

If the secondary/source UI is compact after non-core chrome removal, use the contained context variant instead of forcing a crop. Add `.contained-context-source`, keep it fully inside the `30px` to `50px` safe area, and keep width usually `<= 620px`. This is for narrow contextual interfaces, not for large tables/dashboards/app pages that should be cropped or simplified.

Do not top-align the major UI surfaces. Keep a visible vertical stagger between primary and secondary UI: recommended top-edge difference 48-80px, minimum 32px. If the top edges differ by less than 24px, treat it as failed alignment and move one layer.

All non-cropped edges should keep a `30px` to `50px` safe margin from the banner boundary. Default to `36px`; use `40px` to `50px` for large primary panels when space allows, and `30px` to `36px` for compact secondary fragments or tight compositions. If a panel is too tall, preserve the margin and reduce content height by removing low-priority information first. Action buttons and footer controls are lowest priority and should be removed before violating the safe margin.

Primary floating panels should be visually centered first, especially vertically. Prefer `top: 50%` + `translateY(-50%)` when it preserves the non-cropped safe margin.

**Step 11 — Apply chosen background and refine UI details**

Use the background chosen in Step 2. If the user skipped the choice or explicitly asked you to choose, select background by feature mood. See `references/design.md` → Background Asset System (Section 11-13), Background Mood Mapping.

Available backgrounds in `figma-refs/backgrounds/`: blue-soft-flow, dreamy-pink, elegant-purple, green-mist, green-spring.

Asset priority:
- User-specified or existing banner background first; do not replace it during unrelated revisions.
- Approved `figma-refs/backgrounds/` asset by mood second.
- Never use generated or external backgrounds.
- Background choice must match the Asset Lock Manifest exactly. If the user says a background was updated or provided, that file is locked unless the user explicitly changes it.

Avatar priority:
- Hard rule: every visible avatar, including real people, named users, generic members, grey placeholders, IM avatars, table assignees, mentions, and stacked avatars, must come from `figma-refs/components/avatar/`.
- Before creating or deriving any named avatar asset, inspect `figma-refs/components/avatar/` and bind the named user to the existing matching file when present. Do not crop a screenshot into a new avatar file when the matching avatar already exists in the avatar folder.
- Named user/source avatar assets in `figma-refs/components/avatar/`, such as `Avatar-image.svg` or `Avatar-image-*.svg`, override generic avatars. If a named user appears with a provided avatar, reuse the exact existing asset in every UI layer, add `data-entity-name`, and record it in `Named Entity Asset Manifest`.
- Preset `figma-refs/components/avatar/Avatar-image-*` for real-person avatars.
- `figma-refs/components/avatar/[D] Avatar_Person_blue.svg` / `figma-refs/components/avatar/[D] Avatar_Person_grey.svg` for generic product avatars. If a visible avatar should be grey, use `[D] Avatar_Person_grey.svg`; do not draw a grey CSS circle.
- If the user provides a new avatar, place it under `figma-refs/components/avatar/` first and lock that file path before using it.
- Any visible avatar/person/member/user/assignee UI must be implemented as `<img>` using a locked asset from `figma-refs/components/avatar/`. CSS-drawn circles, gradient circles, initials, custom faces, cropped screenshots, or random portraits fail the quality check.

Apply design tokens from `references/design.md`:
- Border-radius → Section 9
- Shadows → Section 11
- Typography → Section 8
- Lines → Section 10
- Colors → Section 19
- Components → Section 21
- Icons → Section 14. Always check `figma-refs/components/icons/index.md` first and reuse the matching SVG path from the icon library before drawing any fallback icon.
- Icon abstraction → Section 14. Remove unimportant icons; abstract non-core generic menu icons as consistent filled rounded gray squares, never outlined square placeholders unless the source component is a real checkbox. Core feature icons and source-provided semantic icons must use Figma/local SVG assets, not CSS approximations.
- Grid alignment → `references/ui-foundation.md` Section 1. Same-level cards/components in one row must share top and bottom alignment; height difference must be `<= 4px`. Add `ui-check grid-alignment` for hand-positioned card/grid rows.
- Divider width → `references/ui-foundation.md` Section 1.6. All product UI divider lines use `0.5px`; add `ui-check divider-width` for table grid lines, card section dividers, and panel header/body dividers. Component borders are not treated as dividers.
- Skeleton length variation → `references/ui-foundation.md` Section 1.4.1. Repeated abstract text lines must use at least three visible widths and should simulate real copy length; add `ui-check skeleton-variation` for repeated skeleton groups.
- Floating panel radius → `references/layouts.md` Section 6 and `references/ui-foundation.md` Section 4.3. Banner-level floating panels/popovers/modals/dropdowns use `border-radius: var(--radius-card)` by default and must carry `.floating-panel` plus a radius check. All component radii must use the approved Component Shape Token System in `references/design.md`; do not write invented raw `border-radius` values.
- Floating panel shadow → `references/ui-foundation.md` Section 4.2 and `references/design.md` Section 11. Banner-level primary floating panels use `box-shadow: var(--shadow-primary-strong)`; smaller menus/popovers/backing plates use `box-shadow: var(--shadow-secondary-soft)`. Add `ui-check shadow-token` for hand-coded floating panels. Do not invent or copy arbitrary shadow values.
- Floating panel content density → `references/ui-foundation.md` Section 2.3. Every `.floating-panel` uses `24px` internal padding on all four sides by default and must not keep empty footer/action space after buttons are removed. Add `ui-check content-density` to every floating panel.
- Primary floating panel vertical placement → `references/layouts.md`. Use height-based placement: panels `<= 360px` high sit `60px` above the banner bottom; panels `> 360px` are vertically centered. Add `ui-check primary-placement selector=.primary-surface small-height=360 bottom=60 center-target-y=250 tolerance=4`.
- Floating panel anchoring → Section 3.4. Menus/popovers/dropdowns must stay anchored to their trigger, preserving source side and gap such as `4px` above an icon button.

Before final coding, run the anti-cliche filter from `references/visual-direction.md`. Remove decorative AI tropes, fake metrics, fake logos, filler icon clouds, and unnecessary cards.

**Step 12 — Quality check and output files**

See Quality Checklist below.

Generate a development HTML file meeting all Technical Constraints. Background image uses relative path to `figma-refs/backgrounds/`.

Before final output, validate the required planning brief:

```bash
python3 scripts/check_banner_brief.py output/<banner-name>.brief.md
```

Then validate that every HTML image/SVG/background reference matches the Asset Lock Manifest:

```bash
python3 scripts/check_asset_lock.py output/<banner-name>.html
```

Before creating the final share file and PNG, render the HTML locally and visually inspect the screenshot. Fix the HTML before final output if any of these fail:
- A locked asset is missing, substituted, or rendered as a CSS approximation.
- Background differs from the Asset Lock Manifest.
- Visible avatars are not from `figma-refs/components/avatar/`.
- A menu/popover/dropdown is detached from its trigger, has the wrong side/gap/alignment, or overlaps the trigger incorrectly.
- An anchored menu was positioned by eyeballed absolute coordinates instead of a trigger/menu geometry formula.
- Rows, columns, icons, labels, inputs, and buttons inside the same component do not share a clean alignment grid.
- Non-core topbar/toolbar/header chrome remains as empty rounded button/control shells after text is removed.
- Non-core sibling menu/list labels or repeated placeholder text remain readable instead of being skeletonized.
- Any core IM message, selected menu item, trigger button, result panel, or form field is clipped or partially hidden.
- Floating panels or major UI surfaces are accidentally top-aligned, center-stacked, or visually unrelated.
- Abstract placeholders are too dark, too light, inconsistent, or use non-approved colors.

Then generate a shareable self-contained HTML file by running:

```bash
python3 scripts/make_share_html.py output/<banner-name>.html
```

The share file should be named `output/<banner-name>.share.html`. Use it when sending the banner to teammates; they should not receive `file://` links to your local machine.

Before generating the share file or PNG, run the auto-fix pass for marked CSS contracts:

```bash
python3 scripts/check_banner_ui.py output/<banner-name>.html --fix
```

Then generate the share file and export the review PNG at 2x pixel density. Keep the HTML canvas at 900×500, but capture with device scale factor 2 so the PNG is 1800×1000. Name it `output/<banner-name>@2x.png`. Do not deliver only a blurry 900×500 PNG as the final preview image.

After exporting the PNG, run the strict UI regression check:

```bash
python3 scripts/check_banner_ui.py output/<banner-name>.html --png output/<banner-name>@2x.png
```

If it fails, fix the HTML/CSS or add the missing `ui-check` contract marker, run `--fix`, regenerate the share file and PNG, then rerun the strict check before final output. The script catches common regressions around shadow scope, IM bubble/card fills, skeleton color, padding balance, anchored action menus, banner size, and 2x PNG size.

### UI Check Markers

For details that commonly drift, add `ui-check` comments before the relevant CSS rule. Supported markers and usage are defined in `references/ui-foundation.md` Section 9. Add markers for padding balance, shadow scope, source fill, skeleton color, menu anchoring, min/max size, z-index order, protected trigger clearance, and repeated abstract-only lists.

---

## Resource Files

### Design System
- `references/visual-direction.md` — **Taste and strategy layer (MUST read before new banners)**. Contains anti-AI visual cliches, compact visual-system guidance, composition strategy, variant planning, and the required Visual Strategy gate.
- `references/ui-foundation.md` — **Baseline UI foundation (MUST read before generating)**. Contains alignment grids, secondary UI compression, approved abstraction assets, backing plate rules, menu/popover basics, form preview basics, and 30-50px edge safety.
- `references/layouts.md` — **Hard layout constraints (MUST read before generating)**. Contains the 900×500 canvas contract, 30-50px safe area, source/primary surface classes, left/bottom crop rules, and script-enforced layout checks.
- `references/design.md` — **Full design system (MUST read before generating)**. Contains: canvas specs, composition rules, cropping grammar, layout rules, flat UI system, abstraction rules (5 techniques + 3 levels + product logic), typography, radius, lines, shadows, backgrounds, icons, info hierarchy, color system, module abstraction guide (9 modules), common components (18 categories), banner composition pairings, reference examples.
- `references/modules/dashboard.md` — Dashboard-specific abstraction rules. Read when a banner involves dashboard, metric cards, chart cards, pivot tables, or dashboard configuration.
- `references/modules/im.md` — IM-specific rules. Read when a banner involves chat, bot messages, composer input, action menu, popover-triggered creation, or collection-form creation from IM.
- `references/modules/form.md` — Form/questionnaire-specific abstraction rules. Read when a banner involves forms, questionnaires, collection forms, filling pages, question types, option rows, inputs, or submit states.
- `references/modules/table.md` — Table/grid-specific abstraction rules. Read when a banner involves data tables, grid views, records, fields, rows, field-type columns, or table chrome.
- `references/modules/app-mode.md` — App Mode-specific container rules. Read when a banner involves app pages, app navigation, business app views, or Base end-user app surfaces, then combine with child module rules.
- `references/modules/workflow.md` — Workflow/automation-specific path rules. Read when a banner involves automation triggers, action nodes, connector paths, workflow config panels, branches, or run logs.

### Figma References
- `figma-refs/views/` — Product UI screenshots (table, kanban, gantt, gallery, calendar, form, workflow, dashboard, AppMode). Read the relevant view before abstracting.
- `figma-refs/components/` — 18 SVG component categories. Read SVG files to extract precise path data for icons and components.
- `figma-refs/components/icons/index.md` — Icon index (471 SVGs, organized by outlined/filled). Use this to find the right icon, then read the SVG file.
- `figma-refs/components/pointer/pointer-arrow-default.png` — Default top-layer banner arrow/cursor. Use on every banner near the key trigger/action/control; supports horizontal flip with CSS `scaleX(-1)`.
- `figma-refs/backgrounds/` — 5 approved background PNGs.
- `figma-refs/abstraction-examples/` — Reference for abstraction quality.
- `assets/templates/dashboard/metric-card-abstract.html` — Low-freedom metric card abstraction template. Copy this when abstracting dashboard metric cards.
- `assets/templates/dashboard/radar-chart-abstract.html` — Low-freedom radar chart abstraction template. Copy this when abstracting dashboard radar charts.
- `assets/templates/dashboard/donut-chart-abstract.html` — Low-freedom donut/ring chart abstraction template. Copy this when abstracting dashboard donut or ring charts.
- `assets/templates/dashboard/ranking-list-abstract.html` — Low-freedom ranking list / leaderboard abstraction template. Copy this when abstracting dashboard ranking cards.
- `scripts/make_share_html.py` — Converts local image references in a generated HTML file into data URIs for single-file sharing.
- `scripts/check_banner_ui.py` — Static regression check and safe CSS auto-fix for common banner UI failures. Run `--fix` before share/PNG export and strict check after PNG export.
- `scripts/check_banner_brief.py` — Validates the required `output/<banner-name>.brief.md` planning artifact so strategy, source audit, abstraction, UI constraints, asset locks, and verification are not skipped.
- `scripts/check_asset_lock.py` — Validates that HTML image/SVG/background references are local, exist, and match the `Asset Lock Manifest` in `output/<banner-name>.brief.md`.
- `scripts/build_release.py` — Builds a clean publishable skill folder under `release/base-botbanner/`, excluding `output/`, `.DS_Store`, `__pycache__`, `README.md`, and other non-skill artifacts.

### Examples
- `examples/case1.png` — Workflow new trigger banner
- `examples/case2.png` — AI Agent feature banner
- `examples/case3.png` — Workflow date trigger / scheduled birthday message banner
- `examples/case4.png` — Workflow set field value / linked field banner

---

## Quality Checklist

Before outputting, verify these gates:

- [ ] Strategy gates were written: Visual Strategy, Source UI Audit, Abstraction Plan, UI Detail Constraints, Asset Lock Manifest.
- [ ] Planning artifact exists and passes: `python3 scripts/check_banner_brief.py output/<banner-name>.brief.md`.
- [ ] Asset lock passes: `python3 scripts/check_asset_lock.py output/<banner-name>.html`; no external/random image assets, unlocked backgrounds, unlocked source images, or unlocked SVGs are referenced.
- [ ] Module handling is explicit: relevant module references/templates were loaded, or a Temporary Module Rule was created from the provided source UI.
- [ ] Figma/source UI was treated as the product standard for behavior, component relationships, spacing, alignment, radius, states, and assets.
- [ ] Source surface provenance is preserved: when only one original interface was provided, no second platform/module/page/table/editor/admin surface or extra product state was invented.
- [ ] Product story is clear: source/context, trigger, and result are visible; optional tertiary UI exists only for a real middle step.
- [ ] Primary/secondary hierarchy is correct: primary result has enough scale, secondary UI is simplified/cropped, and product layer order follows source -> intermediate -> result. If only one source interface was provided, a single-interface or source-interface-plus-focus-card layout was considered before adding any extra surface.
- [ ] Core information is preserved; non-core labels, repeated placeholders, and abstract-only rows are skeletonized or removed according to `references/ui-foundation.md`.
- [ ] Asset locks are honored: approved background, preset avatars, product icons/SVGs/templates, and no generated/random images.
- [ ] Source image assets that remain visible in product UI were reused from Figma/source assets, not approximated with CSS or substituted with a background asset.
- [ ] No source-absent product state was added, such as validation success, cursor, selected, helper, or callout states not shown in the source or requested by the user.
- [ ] UI contracts are marked and checked for fragile details: padding, shadow scope, source fill, skeleton color, menu anchoring, size, z-index, trigger clearance, and max repeat.
- [ ] Visual review passes: no accidental edge crowding, top-aligned major surfaces, detached menus, clipped core UI, uneven padding, ambiguous checkbox-like placeholders, or decorative filler.
- [ ] Technical output passes: 900×500 HTML, single `<style>`, PingFang SC, brief MD exists, asset lock passes, share HTML exists, 2x PNG is `1800×1000`, and `scripts/check_banner_brief.py`, `scripts/check_asset_lock.py`, `scripts/check_banner_ui.py --fix`, plus strict `--png` checks passed.

## Publishing

When preparing this skill for teammates, do not publish the working folder directly. Build a clean package:

```bash
python3 scripts/build_release.py
```

Publish the generated `release/base-botbanner/` folder. The release package intentionally excludes generated banner outputs, share previews, `.DS_Store`, caches, and README-style auxiliary docs so the skill stays focused and models do not learn from stale local experiments.

# DESIGN.md — Bot Banner HTML Design System

## Overview

This design system defines the visual language, layout grammar, abstraction rules, and implementation constraints for generating Bot Banner HTML compositions.

Use this file after `references/visual-direction.md` and `references/ui-foundation.md`. The visual-direction file decides the product story, anti-cliche constraints, and composition strategy; the UI foundation file defines baseline alignment, assets, and edge-safety rules; this file defines how to implement that strategy precisely in HTML.

## Figma Banner Specification Authority

Use the Figma rules as the concrete Base bot-banner standard.

This means Figma is not only a visual reference. It is the source of truth for:
- product behavior and component hierarchy
- interaction relationships, such as trigger -> menu/popover
- exact spacing and alignment when present, such as a `4px` popover gap and right-edge alignment
- component radius, stroke, shadow, selected/checked/focused state
- product-native icons, avatars, backgrounds, and existing asset choices

Abstraction may remove, simplify, or skeletonize non-core content, but it must not change product logic or constrained UI relationships.

If exact fidelity conflicts with banner composition, preserve product logic and UI detail constraints first, then move, crop, or remove lower-priority surrounding UI.

The output is NOT:
- a marketing poster
- an illustration
- an infographic
- a hero artwork

The output SHOULD feel like:
- a polished SaaS product scene
- a composed interface moment
- a realistic product interaction state
- a modern Apple / Linear / ChatGPT-style UI composition

The banner communicates functionality through:
- interface relationships
- layout hierarchy
- UI abstraction
- interaction states

NOT through:
- slogans
- explanation text
- decorative graphics

---

# 1. System Philosophy

## 1.1 UI is the Hero

The interface itself is the visual language.

The banner should communicate:
- what happened
- what changed
- what the feature does

through:
- product UI
- content transformation
- component relationships

Avoid:
- giant icons
- promotional layouts
- illustrations
- decorative storytelling

## 1.2 Product Scene, Not Marketing Poster

The banner should feel like:
- a product screenshot composition
- a realistic workflow state
- a captured UI interaction

NOT:
- a promotional KV
- an infographic
- a landing page hero section

---

# 2. Canvas System

## Banner Size

```css
width: 900px;
height: 500px;
```

Rules:
- fixed canvas
- non-responsive
- screenshot-oriented
- export-ready

## Root Container

```css
position: relative;
overflow: hidden;
```

Required because:
- secondary UI must extend outside banner bounds

---

# 3. Composition System

## 3.1 Layer Structure

Default composition:

- one Secondary UI (background/source/context layer)
- one Primary UI (foreground/result/focus layer)

Two UI layers are common and often the best balance, but they are not mandatory. The banner must use the fewest truthful UI surfaces needed to explain the product path.

When only one source interface is provided, a single-interface composition is valid. Center it or place it slightly off-center if that best preserves the source product logic and gives the key content enough scale. Do not create another platform, module, page, table, editor, admin surface, or extra product state simply because the banner usually benefits from two layers.

For field-level, type-level, or single-component features, the preferred pattern is often:
- source interface/page as the background context
- enlarged foreground focus card extracted from a real component or state inside that same source interface

This focus card is not a new product surface. It is a magnified abstraction of the provided UI's key component, used to make the feature readable at banner scale.

For a single-interface plus focus-card composition, the source interface and focus card must read as one centered or intentionally balanced composition group. Do not leave large accidental empty space on one side of the banner. If the source UI is centered, the extracted focus card should align to the same visual center unless the crop has a clear reason.

The extracted focus card may magnify component size, simplify surrounding content, and improve visual hierarchy, but it must not invent source-absent states. Do not add validation messages, success tags, cursor states, helper text, callouts, selected states, or generated labels unless the source UI already contains them or the user explicitly asks for them.

For same-interface magnification, the foreground focus surface may be a cropped duplicate of the same source interface or module area. This is not a second product state. It is a readable enlargement of the real source UI. Preserve selected nav/table/form/workflow context, keep the core feature content visible, and allow non-core right or bottom edges to crop if needed for scale.

A third UI layer is allowed only when the real product scenario contains three necessary steps and each layer expresses a distinct part of the feature path. Example: source list / filter configuration / opened member dropdown. The third layer must be product-real, simpler than the main layers, and visually subordinate to the Primary UI.

Allowed non-UI accents:
- small cursor, connector, glow, or icon accents that do not read as an extra interface surface

### Default Banner Pointer

Use `figma-refs/components/pointer/pointer-arrow-default.png` on every banner by default.

Rules:
- render as an `<img>` asset, not CSS-drawn geometry
- use the complete PNG component file directly; do not extract, redraw, recolor, rebuild, or add CSS shadow
- default size: `90px × 90px`
- place on the topmost layer above primary and secondary UI
- position near the key trigger/action/control, not randomly in empty space
- use it to point at the action that advances the feature path, such as a selected option box, a panel control, a send/input action, a workflow node, or a magnified feature component
- support direction by flipping with `scaleX(-1)`
- do not rotate by default; only rotate when explicitly requested or when the source/reference case already uses that exact rotation, and record the reason in the brief
- do not cover product icons, readable text, selected values, or core controls; keep the product evidence visible
- keep the pointer selectable in HTML previews; do not set `pointer-events: none` for fixed banner output
- do not create alternate arrow/cursor styles per banner
- do not change the baked-in shadow; the PNG already contains the approved shadow treatment

Recommended CSS:

```css
.banner-pointer {
  position: absolute;
  width: 90px;
  height: 90px;
  z-index: 20;
  transform-origin: center;
}

.banner-pointer.flip-x {
  transform: scaleX(-1);
}
```

Use two layers when:
- the middle state can be understood from the source/context layer
- the third panel only repeats information already shown
- the third panel exists only to make the banner look richer
- the feature can be expressed as `source/context -> result`

Use three layers only when:
- the product interaction truly has `source/context -> configuration/action -> opened result/detail`
- removing the middle layer would make the feature logic unclear
- the third layer follows the real Figma/product geometry and does not create an invented explanation panel

Forbidden:
- three independent cards/screens arranged as a fake process
- product screenshot plus popup plus extra explanation card
- dashboard/table/workflow surfaces stacked together when one is only decorative
- separate before/after comparison card unless the original product design has that component
- inventing a second platform/module/page/table/editor/admin surface when the user provided only one original interface, unless the user explicitly provides or asks for that surface
- mixing surfaces as if they belong to the same feature path when the source design only shows one original interface

### Secondary UI (Background Layer)

Purpose:
- provide context
- express source/workflow
- support narrative

Characteristics:
- larger
- weaker
- more abstract
- partially cropped
- visually behind
- frosted glass style: `rgba(255,255,255,0.8)` + `backdrop-filter: blur(24px)`

Position:
- primarily left side
- should exceed the left banner boundary by default
- may also exceed bottom boundary
- default CSS position: `left: -48px` to `-96px`; use a larger negative value for wide secondary UI
- if the full left rounded corner of the secondary UI is visible, the layer is not cropped enough
- for large product canvases such as tables, dashboards, workflows, and app pages, prefer bottom crop as well when the layer would otherwise look short or leave empty vertical space
- add a `cropped-edge` ui-check marker for intentional secondary crops, such as `side=left,bottom min-out=32`

### Primary UI (Foreground Layer)

Purpose:
- express core feature
- express final result/state

Characteristics:
- more focused
- visually stronger
- floating
- higher elevation
- more readable

Position:
- primarily right side
- floating above secondary UI

## 3.2 Key Feature Visibility

The feature's primary interaction path must remain fully visible.

Rules:
- Identify the core feature trigger and result before layout. Examples: a "润色" button, generated card, workflow trigger node, sent message, or key status change.
- Treat the feature path as a sequence, not as a collection of nice-looking UI pieces. Example for AI polish: `source input -> polish trigger -> polished result panel`.
- Use the fewest layers that keep the feature understandable. Two layers are useful when there are real source and result states. If there is only one source state, keep one interface and enlarge the key component as a foreground focus card when needed. Use a third layer only for a necessary real intermediate state.
- Never let the foreground panel cover the key trigger, key input, or key result that explains the feature.
- Never crop out key information. If a message, menu item, selected object, trigger button, or result panel is part of the core path, it must remain fully visible inside the 900×500 canvas.
- If the foreground panel overlaps a key element, resize or crop the secondary UI before hiding or obscuring the key feature.
- If a core element is clipped by the banner edge, move the whole UI group inward, reduce non-core surrounding UI, or crop a different non-essential edge.
- It is acceptable to shorten a source input, reduce its width, or crop non-essential surrounding UI to keep the core trigger visible.
- Secondary information may be hidden when it does not affect the main path or product meaning. Example: for a survey polish banner, keep the text question and polish trigger; hide later form questions if space is needed.
- Non-essential micro-elements can be hidden to simplify the scene. Example: disclosure arrows beside form question titles can be removed when the banner is not about expanding/collapsing questions.

For content transformation features, keep the source and result in their real product locations:
- Source content stays in the source component, such as an input, selected cell, message bubble, or document block.
- Result content stays in the real result component, such as a floating panel, generated card, assistant response, or preview area.
- Do not invent side-by-side comparison UI unless the product design actually contains that comparison component.

## 3.3 Figma Source Fidelity

When the user provides a Figma URL, screenshot, or original design file, it becomes the source of truth for product behavior and geometry.

Rules:
- Inspect the provided reference before composing the banner.
- Treat Figma rules as concrete Base banner specification, not moodboard inspiration.
- Preserve source-surface provenance. If only one original interface is provided, all product UI in the banner must come from that same interface or be extracted/magnified from a component inside it. Do not invent a different platform, device, module, page, editor, table, admin surface, or extra product state.
- Preserve real component hierarchy, relative position, spacing, icon choice, corner radius, line weight, copy placement, and interaction logic.
- Extract UI detail constraints before implementation. Treat exact component relationships from the source design as layout constraints, not optional polish.
- If only one module is needed, crop or abstract the module, but do not redesign its internal layout from memory.
- If only one source interface is provided, first try a single-interface or source-interface-plus-magnified-component composition. Add another full UI surface only when it exists in the provided source or is explicitly requested.
- Do not move result text into a new location, add a comparison panel, change list behavior, or invent an extra state unless the source design already contains it.
- For mobile source UI, remove OS/system chrome such as status bars, dock bars, battery/signal areas, and home indicators by default. Preserve product chrome such as nav bars, tabs, field rows, and action buttons when they support product context.
- If the source UI contains a real image or cover asset and that image remains visible, use the actual Figma/source asset. Do not approximate source images with CSS gradients, generated images, or unrelated background assets. Backgrounds for the overall banner still come only from `figma-refs/backgrounds/`.
- Visible source/Figma image assets must be downloaded or reused locally and rendered as `<img data-source-image-role="...">`. Record the role, local asset path, source description, selector, and `fallback_allowed: false` in the Asset Lock Manifest. If the asset cannot be downloaded, crop or remove that source image region instead of inventing a replacement.
- Product surface outlines used only for light separation should be subtle white translucent strokes, not dark gray/green device frames, unless the source design explicitly shows that frame. For small flat panels or foreground result panels, use `1px solid rgba(255,255,255,0.72)` by default; if the surface itself has a white/solid fill, also set `background-clip: padding-box`.
- Secondary/background product UI frames are stronger than a 1px line. When a lower-layer interface is shown as a large product mockup/surface, build its visible outline as an outside wrapper, not as an inset border on the product UI. Use `padding: 6px; background: rgba(255,255,255,0.5); border-radius: outerRadius`, and place the real UI inside with a smaller inner radius. This reads as a 6px white 50% opacity outside frame. The frame must not consume, crop, or shift the real source UI content. If the frame bottom is meant to be visible, keep the full outside wrapper inside the banner; otherwise an intentionally cropped side should not be judged as a missing frame.
- Do not use only `border: 1px ...` for a large secondary/background interface. That is too thin at banner scale and will disappear after 2x PNG export/downsampling.
- After generating, visually compare the banner against the source reference for obvious misalignment before final output.
- If exact fidelity conflicts with banner clarity, keep product logic and key geometry first, then abstract lower-priority details.

UI detail constraints include:
- trigger-to-popover/menu/dropdown gap and direction
- trigger-to-popover/menu/dropdown horizontal alignment, such as right edge alignment
- selected, checked, hover, focused, active, and disabled states
- component radius, border color, divider weight, shadow, internal padding, and alignment
- icon/button/menu anchoring relationships
- text baseline alignment and row rhythm when they define product feel

If a detail constraint conflicts with banner safety or readability, move the related UI group together or remove lower-priority surrounding UI. Do not independently change the constrained spacing or detach related components.

## 3.4 Floating Panel Anchoring

Floating panels, popovers, menus, dropdowns, and tooltips must preserve their trigger relationship from the source design.

Rules:
- Identify the trigger control before placing the floating panel.
- Preserve the source side and gap whenever the design provides it.
- If the source design places a menu above an icon button with a `4px` gap, keep the menu above that icon button with `4px` vertical spacing.
- Default menu/popover alignment for icon-button triggers is right edge alignment: the menu's right edge aligns to the trigger button's right edge unless the source design clearly uses another alignment.
- Center alignment is not allowed for icon-button menus unless the source design explicitly centers it.
- Do not place a menu by visual balance alone; anchor it to the triggering button or selected object.
- The trigger and its floating panel should both be visible when they explain the feature path.
- If keeping the exact anchor would clip key information, move the trigger + panel group together, or crop unrelated background UI instead.
- Do not detach a menu so it looks like an unrelated card.

---

# 4. Cropping Grammar

## Secondary UI Cropping

The secondary UI should NOT be fully visible.

This is a mandatory visual cue for depth. The lower/background UI should usually extend outside the banner's left edge so the canvas cuts it off. Do not leave a safe margin on the cropped side.

Default CSS:

```css
.secondary-ui {
  position: absolute;
  left: -64px;
  bottom: -40px;
}
```

Cropping target:
- at least 32px of the secondary UI should be outside the left banner boundary
- the visible left side should be cut by the banner edge, not shown as a complete rounded corner
- if the secondary UI is a large screenshot/card, its left x-position should be negative, not `40px`, `50px`, or centered
- the safe-margin rule applies only to non-cropped edges, never to an intentionally cropped left/bottom edge

Correct:
- left edge cropped
- bottom edge cropped
- partially outside banner

Incorrect:
- left side has a full 40-50px margin and visible rounded corner
- centered full screenshot
- fully visible interface
- complete card visibility

The goal is:
- cinematic composition
- visual tension
- stronger hierarchy

## Primary UI Visibility

The primary UI should:
- remain mostly visible
- overlap secondary UI
- visually float above the background layer
- match the source surface type: complete interface/page surfaces should be large; true floating panels/popovers can stay compact

Recommended overlap: 15% ~ 35%

If the primary result is a complete product interface/page/view rather than a real floating panel, it should usually take `45%` to `60%` of the 900px banner width, with a practical minimum around `400px`. Do not shrink a complete interface into a narrow popover-like panel just to preserve secondary context.

Source/context product pages must also keep useful scale. If a PC form, questionnaire, table, app page, or workflow canvas is still needed to understand the feature, do not shrink it while leaving large unused background on the other side. It should usually occupy at least `58%` of banner width unless a larger foreground result surface requires the space.

Visible source order must be preserved across modules: questions, table rows, workflow steps, menu order, ranked lists, timeline steps, and configuration stages must not be renumbered or reordered for composition convenience. The feature item keeps its source order and should not be visually demoted below siblings.

## Primary Panel Centering

Floating primary panels should be visually centered first, especially on the vertical axis.

Default:
- Use vertical centering for the primary UI (`top: 50%` + `translateY(-50%)`) when the panel height allows the non-cropped safe margin.
- Compact floating panels such as type pickers, add menus, filter/action/config panels, small popovers, and short result panels should be vertically centered within the banner or composition group when they fit. Do not leave large empty space below a short panel.
- Keep the panel on the right side only as much as needed to show hierarchy and overlap with the secondary UI.
- Avoid placing the primary panel too close to the bottom or top edge for decorative tension.

If vertical centering conflicts with the safe margin, preserve the safe margin first and reduce lower-priority content.

---

# 5. Layout Rules

## Avoid Mechanical Alignment

Forbidden:
- exact top alignment
- exact bottom alignment
- perfect symmetry
- rigid centering
- primary and secondary UI top edges sitting on the same horizontal line

Recommended:
- visible vertical offsets
- layered positioning
- organic spacing rhythm

## Vertical Stagger Rule

Primary and secondary UI should preserve a clear height difference. Do not top-align the major UI surfaces; it makes the banner feel stiff and screenshot-like.

Rules:
- Default top-edge difference between major UI surfaces: 48-80px
- Minimum acceptable top-edge difference: 32px
- If the difference is under 24px, treat it as failed top alignment
- The foreground/primary panel can sit higher or lower than the background UI, but it must feel intentionally staggered
- For three-layer compositions, all three visible top edges should not form one straight horizontal line; stagger at least two of them

Correct:
- background/source UI starts lower and is cropped left/bottom; primary/result UI floats higher on the right
- background/source UI starts higher and primary/result UI is vertically centered lower, as long as the overlap and hierarchy remain clear

Incorrect:
- secondary table top and primary settings panel top align exactly
- chart cards, table, and side panel all begin at the same y-position
- two full panels with matching top and bottom edges

Typical relationship:

```css
.secondary-ui {
  left: -72px;
  bottom: -48px;
}

.primary-ui {
  right: 76px;
  top: 92px;
}
```

## Margin Priority Rule

All non-cropped UI panels should maintain **30px to 50px margin** from every non-cropped banner edge.

Default margin is `36px`. Use `40px` to `50px` for large primary panels when space allows. Use `30px` to `36px` only for compact secondary fragments or tight compositions.

This is a hard rule. If an interface edge is not intentionally cropped by the composition, it must never sit closer than `30px` to the banner boundary or farther than `50px` in a way that wastes canvas space.

When space is insufficient to fit all content while respecting the safe margin:

1. **Priority: preserve margin** — never compress the safe margin or let panels touch the edge to squeeze content
2. **Reduce panel height** by hiding lower-priority information:
   - Action buttons (采纳/重新润色/提交 etc.) — lowest priority, remove first
   - Secondary detail items (sub-bullets, footnotes) — second to remove
   - Body text items — trim from bottom up
   - Section titles — never remove
   - Panel header (icon + title) — never remove
3. **Information priority order** (highest → lowest):
   - Panel header (feature identity)
   - Section title (content category)
   - Primary result items (core output)
   - Sub-items / nested content
   - Action buttons / controls

For floating result panels, bottom action rows such as "重试 / 取消 / 替换" are optional in banners. Remove them before violating the required safe margin.

Example: if a polish result panel has 7 items + 2 buttons but only fits 5 items with the required bottom margin, remove buttons first, then trim the last 2 items.

## Avoid Orphan Lines

Text must not break with a single word/character alone on the last line (widow/orphan).

When a line wraps awkwardly:
1. **Widen the panel** — prefer increasing panel width to give text more room
2. **Shorten the text** — if widening is not possible, trim wording slightly
3. **Never accept** a lone 1-2 character line at the bottom of a text block

---

# 6. Flat UI System

## UI Style

All interfaces must remain fully flat.

Forbidden:
- perspective
- tilted cards
- 3D objects
- isometric layouts
- volumetric lighting

Allowed:
- soft shadows
- subtle blur
- gentle gradients

## Secondary UI Frosted Glass

The secondary UI (larger, background layer) uses a frosted glass style to convey lightness:

```css
background: rgba(255, 255, 255, 0.8);
backdrop-filter: blur(24px);
```

This is NOT decorative glassmorphism — it is the standard mockup treatment for secondary UI, creating visual depth and lightweight feel.

The banner should feel:
- realistic
- modern
- lightweight
- product-native

---

# 7. UI Abstraction Rules

## Principle

Abstraction is NOT deletion. It is **replacing real content with structural placeholders**.

The goal: preserve the module's visual identity and functional meaning, while removing all specific information.

A viewer should instantly recognize "this is a workflow" or "this is a table" — without being able to read any real data.

## Product Logic Rules (MUST follow)

1. **Never change the product's layout direction.** If the real product uses vertical workflow layout, the abstracted version must also be vertical. Do not rotate or rearrange to fit the banner.

2. **Never change component sizes across a view.** All nodes/cards in the same view must maintain consistent dimensions. Branching does NOT mean smaller cards — same width, same padding, same icon size.

3. **Never add features the product doesn't have.** Only abstract what actually exists in the real interface.

4. **Never remove structural elements that define the module identity.** If the product shows connection lines between nodes, keep them. If it shows column headers, keep them.

5. **Treat the provided product design as the interaction source of truth.** A banner may crop, layer, or abstract the interface, but it must not invent new interaction states or move information into a component where the real product would not show it.

6. **Do not create artificial comparison UI inside product panels.** If a feature transforms content, show the "before" state in the original source location and the "after" state in the real result component. Example: for survey AI polish, the original text stays in the form input; the polish floating panel shows only the polished text, because that is the real product behavior.

## Feature-Path Preservation vs Background Abstraction

Preserve real content only where it explains the feature path.

For AI polish and similar transformation features:
- Keep real source text only in the source input.
- Keep the real feature trigger, such as "润色", visible and readable.
- Keep the real transformed result in the primary foreground component.
- Abstract or hide surrounding context that does not change the meaning of the feature.

Background UI can be reduced aggressively, but it must keep enough structure for the module to remain recognizable.

For form/questionnaire banners:
- Keep the active question and input field readable when they are the source of the feature.
- Secondary questions can become skeleton rows.
- Secondary option labels can become short placeholder lines.
- Unrelated submit buttons can become button-shaped blocks.
- Disclosure arrows, helper copy, secondary labels, and other micro-elements can be removed when they do not explain the feature.
- Abstract buttons still need button proportions. A textless button should be wide enough to read as a control, not as a small color chip.

## 5 Abstraction Techniques

### Abstract Element Color

All abstracted UI elements use the same neutral overlay:

```css
background: rgba(15, 15, 16, 0.06);
```

This corresponds to `#0F0F10` at 6% opacity. Use it for skeleton lines, placeholder pills, abstract icons, abstract chart bars/rings/grids/shapes, abstract avatars, and other non-real placeholder UI.

Do not use separate light-gray solids such as `#EFF0F1` for abstracted elements. A shared transparent overlay keeps stacked abstract layers distinguishable without making the UI noisy.

### Technique 1: Content Line Replacement

Replace real text content with gray horizontal lines of varying widths.

```
Real:    "第三季度销售数据汇总报告"
         ━━━━━━━━━━━━━━━━━━━━━━━

Abstract: ████████  ██████████  ██████
```

Rules:
- Use 2-3 different line widths to suggest content variety
- Color: `rgba(15, 15, 16, 0.06)`
- Height: 6px, border-radius: 3px
- Never use real readable text in secondary UI
- Low-priority explanatory copy can become a muted placeholder line when it only provides atmosphere or helper context. Example: a form subtitle such as "您的真实评价是..." should be abstracted if the banner's real story is the input text, polish trigger, and result panel.
- Secondary form labels, option text, and unrelated submit buttons can be abstracted into skeleton lines or button shapes when they are not part of the feature path.
- When abstracting form modules, keep a stable alignment grid. Use a fixed question-index column and a fixed content column; all titles, inputs, option rows, placeholder lines, and buttons must align to that same content-column start.
- Do not mix real text and placeholder lines arbitrarily. Real text belongs to the feature path; placeholder lines belong to background context.
- Abstract placeholder sizes must follow the real information hierarchy around them. A subtitle/helper placeholder should be shorter and visually weaker than its parent title; when the title text changes length, re-evaluate nearby skeleton line lengths instead of keeping old widths.

### Technique 2: Chrome Removal

Strip away all interface chrome that isn't essential to the feature story.

**Always remove:**
- Left sidebar / navigation
- Top navigation bar
- Breadcrumb
- Tab bars (unless the feature IS about tabs)
- Footer / pagination
- Full toolbar (keep only a fragment if needed for context)
- Settings / configuration panels
- Status bar
- Help icons, tooltips, badges

**Keep only if feature-relevant:**
- View name in toolbar fragment
- A single action button that triggers the feature
- Field type indicators (tag shape, avatar circle, checkbox)

### Technique 3: Structural Skeleton

Keep the structural pattern of the module but reduce its content.

| Module | Structural Pattern | Skeleton Version |
|---|---|---|
| Table | Row-column grid | 3-4 columns × 4-5 rows, headers only |
| Kanban | Multi-column cards | 2-3 columns × 2 cards, minimal content |
| Gantt | Left list + right bars | 3-4 rows with colored bars |
| Calendar | Month grid | 2-3 weeks, event color blocks |
| Workflow | Nodes + connections | 2-3 nodes with lines |
| Dashboard | Card grid | 1-2 chart cards if secondary; 1 focused chart/metric card if primary |
| Form | Vertical field stack | 3-4 fields, input shapes |
| Gallery | Card grid with images | 2 cards with image placeholders |
| IM | Message bubbles | 1-2 card messages |

### Technique 4: Shape Identity Preservation

Each module has a distinctive visual shape that must be preserved even in abstraction.

- **Table**: Horizontal bands (header row + data rows)
- **Kanban**: Vertical columns with rounded cards
- **Gantt**: Left-right split (list | bars)
- **Calendar**: Grid cells with small color bars
- **Workflow**: Connected node cards
- **Dashboard**: Rectangular chart cards in grid
- **Form**: Stacked rounded rectangles (inputs)
- **Gallery**: Portrait cards with top image area
- **IM**: Left-aligned bubbles with avatar dot

If the shape identity is lost, the module becomes unrecognizable.

### Technique 5: Color Abstraction

Keep the product's color system but apply it minimally.

- Use 1-2 semantic colors per banner (not all colors)
- Tags/badges: use solid color pills but with placeholder text (short gray line)
- Charts: use product colors for bars/lines but no data labels
- Avatars: use preset avatar assets when a real-person feel or source avatar is needed; use solid color circles only when identity is irrelevant and the avatar is purely structural/background context.
- Status indicators: keep color meaning (blue=active, green=done)

### Dashboard & Chart Abstraction

Dashboard abstraction must look like a designed product card, not random chart decoration.

Layer rules:
- Secondary dashboard UI: keep 1-2 chart cards maximum.
- Primary dashboard UI: use one focused chart card, metric card, or insight card.
- Do not show a full dashboard grid when the banner is not specifically about the dashboard grid.
- Do not add dashboard as a third surface behind another product UI and a foreground panel.

Card rules:
- Use a clean grid with consistent card width, padding, and baseline alignment.
- Card radius: 12px. Inner padding: 16-20px.
- Each card should have one title skeleton or short metric label, one main metric or chart, and at most one small trend/status element.
- Avoid dense legends, axis labels, filter rows, tables inside chart cards, and full toolbars unless the feature is about those controls.

Chart primitives:
- Bar chart: 5-7 rounded bars, one accent series plus neutral bars, optional subtle baseline.
- Line chart: one smooth line only, 6-8 points, optional very soft area fill.
- Donut chart: one ring with 2-3 segments maximum, optional center metric.
- Metric card: one large number/title, one short helper skeleton, one tiny trend indicator.

Color rules:
- Use one primary chart accent per card and at most one secondary accent in the whole banner.
- Do not use rainbow palettes or many unrelated colors.
- Use product colors: blue `#1456F0` / `#336DF4`, green `#258832`, red `#FF615D`, neutral tracks `#DEE0E3`.

Quality bar:
- Charts should feel calm, sparse, and product-native.
- The chart shape should be recognizable at banner scale without readable axis labels.
- If the chart becomes visually noisy, simplify to metric card + small sparkline.

## Abstraction Level Scale

Not all banners abstract to the same degree:

### Level 1: Low Abstraction
- Keep most real content
- Only remove chrome (sidebar, toolbar)
- Use when: the specific content IS the feature (e.g., new field type showing real data format)

### Level 2: Medium Abstraction (DEFAULT)
- Replace text with placeholder lines
- Remove chrome + reduce content
- Keep structural identity + color system
- Use when: most feature announcements

### Level 3: High Abstraction
- Reduce to pure shapes and color blocks
- Minimal recognizable structure
- Almost diagram-like
- Use when: the feature is about workflow/logic/automation (structural, not content-driven)

---

# 8. Typography System

## Principle

Typography is functional, not promotional.

Avoid:
- marketing headlines
- large slogans
- explanatory copy
- poster typography

Allowed:
- realistic UI content
- product labels
- messages
- form content
- workflow information

## Text Feeling

Typography should feel:
- native to the product
- lightweight
- calm
- breathable

## Spacing

Recommended:
- large line-height
- generous padding
- relaxed content density

Avoid:
- crowded layouts
- excessive information

## Font

PingFang SC only. No external fonts.

## AI Markdown Typography (文案排版)

For text-heavy panels (AI results, markdown content, polish results), use these token-based specs.

Reference Figma nodes:
- Secondary / compact text context (12px): `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=35-28956`
- Important text context (14px): `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=39-29330`

Rules:
- Use these references for all pure text / AI markdown output.
- Preserve markdown structure with real text hierarchy: section title, paragraph, bullet list, nested list.
- Prefer unordered list styling for structured text in banner panels because it improves scanability and visual rhythm.
- If the requester explicitly asks for ordered lists, plain text, or strict product text-component fidelity, adjust the text format to match that request.
- Do not wrap markdown output in decorative cards unless the product component itself is a card.
- Do not add labels such as "before", "after", "analysis", or "summary" unless they exist in the product UI or the generated content itself.
- Keep pure text calm and product-native: no poster typography, no colored callouts, no artificial highlight blocks.
- Structure should improve scanning without adding unnecessary height. When a heading and body can read naturally on one line, prefer `Label: body` over forced line breaks.

### Secondary Text Context (次要信息 — 12px)

| Token | 字号 | 行高 | 字重 | 颜色 | 用途 |
|---|---|---|---|---|---|
| caption-0 | 12px | 20px (167%) | 500 | #1F2329 | 小标题/段落标题 |
| body-2 | 12px | 20px (167%) | 400 | #646A73 | 正文辅助 |

- Use when the text supports another main UI or is visually secondary.
- Examples: secondary explanation, supporting AI rationale, embedded card content, background-layer text.
- 段落间 gap: 2px
- 段落标题前 padding-top: 6px
- 列表项 gap: 4px for compact unordered list blocks
- 列表圆点: 4px circle, `rgba(31,35,41,0.4)`
- 列表缩进: 12px dot column + 6px gap → 文本区域 = 容器宽度 - 18px
- 嵌套列表圆点: 0.5px border `rgba(31,35,41,0.4)`, 无 fill
- First-level unordered list uses a gray filled 4px dot.
- Second-level unordered list adds a 12px indent column and uses a 4px hollow dot.

### Important Text Context (重要信息 — 14px)

| Token | 字号 | 行高 | 字重 | 颜色 | 用途 |
|---|---|---|---|---|---|
| headline | 14px | 22px (157%) | 500 | #1F2329 | 辅助标题/段落标题 |
| body-0 | 14px | 22px (157%) | 400 | #1F2329 | 正文 |

- Use when the text itself is the primary result or core feature output.
- Examples: AI polish result, generated answer, bot response, main notification content.
- 段落间 gap: 8px
- 段落标题前 padding-top: 8px
- 列表项 gap: 6px
- 列表圆点: 4px circle, `rgba(31,35,41,0.4)`
- 列表缩进: 12px dot column + 6px gap → 文本区域 = 容器宽度 - 18px
- 嵌套列表圆点: 0.5px border `rgba(31,35,41,0.4)`, 无 fill

Implementation requirements:
- The markdown container is a vertical block list with `gap: 8px`.
- Section titles use `headline`: 14px / 22px, 500, `#1F2329`.
- Body paragraphs use `body-0`: 14px / 22px, 400, `#1F2329`.
- Avoid ordered list rows in banner pure-text panels unless the requester or exact product UI requires visible numbering.
- Level-1 unordered rows use a 12px marker column + 6px gap + text. The marker is a 4px filled circle centered within a 22px line box.
- Level-2 unordered rows add a 12px indent column before the marker. The marker is a 4px hollow circle with `0.5px solid rgba(31,35,41,0.4)`.
- Do not type bullet characters directly in text. Build bullets as layout columns so multi-line text aligns with the first line.
- Preserve the markdown hierarchy from the generated content. Do not flatten nested lists into plain paragraphs.
- For short labeled items, keep label and body inline. Use a forced second line only when the label-body pair is too long, needs nested structure, or matches the product's actual text component.

### 选择规则

- If pure text is the primary result in the foreground panel, use Important Text Context (14px).
- If pure text is supporting/secondary, use Secondary Text Context (12px).
- Default to unordered lists for structured result text. Switch to ordered lists or plain text only when the requester explicitly asks or when strict product fidelity is the stated priority.
- Do not downshift primary-result text to 12px just to reduce height. Preserve the required safe margin by removing lower-priority UI first.

---

# 9. Radius System

Extracted from component SVGs:

| Element | Radius | Source |
|---|---|---|
| Card / Panel | 12px | Card.svg rx=12 |
| Input / Select | 8px | Input.svg rx=7.75≈8 |
| Button | 6px | Button_Basic.svg |
| Tag (bold bg) | 6px | Tag_Status_Bold.svg rx=6 |
| Notice bar | 6px | Notice.svg path |
| Progress bar | full round (pill) | Progress.svg |
| Checkbox | square | Checkbox.svg |

Rules:
- Foreground floating panels, modal-like result panels, popovers, and banner-level cards use `12px` radius by default unless the Figma/source component specifies another value.
- If the source Figma design provides a concrete panel radius, preserve that radius exactly and record it in UI Detail Constraints.
- Do not inflate floating result panels to `16px`, `20px`, or larger rounded corners just to make them feel softer. Oversized radius makes Base UI look unlike the source product.
- Add a ui-check marker for fragile foreground panel radius when the panel is hand-coded, for example `/* ui-check radius selector=.polish-panel value=12 */`.

---

# 10. Line & Stroke System

## Divider Lines

Used for: table row separators, card section dividers, content area boundaries.

```css
border: 0.5px solid rgba(31, 35, 41, 0.15);
```

- Width: 0.5px
- Color: #1F2329 at 15% opacity
- Style: solid, no dash

## Workflow Connection Lines

Used for: node-to-node connections in workflow/automation diagrams.

```css
stroke: rgba(31, 35, 41, 0.15);
stroke-width: 1px;
```

- Width: 1px
- Color: #1F2329 at 15% opacity
- Style: solid, no dash

### Corner Radius

All turns and bends MUST use rounded corners, never sharp right angles.

Use quadratic bezier (Q) for smooth transitions:

```
/* Correct — rounded corner with 8px radius */
M 300 16 L 178 16 Q 170 16 170 24 L 170 40

/* Wrong — sharp right angle */
M 300 16 L 170 16 L 170 40
```

Recommended corner radius: 8px

## General Line Rules

1. Never use sharp 90° corners on any line that changes direction
2. Never use dashed lines for workflow connections
3. Divider lines (0.5px) and connection lines (1px) are different systems — don't mix specs
4. All line colors use #1F2329 with opacity control, not gray hex values

---

# 11. Shadow System

## Philosophy

Shadows are a banner composition tool, not a default component style. Use them to separate banner-level floating UI surfaces from the background scene. Do not add shadow to modules that live inside a product interface.

Shadows should feel:
- soft
- atmospheric
- Apple-like

Avoid:
- black shadows
- hard shadows
- dramatic elevation

Use:
- same-hue shadows
- low saturation
- cool gray-blue tones

Allowed:
- foreground floating panels, modals, popovers, dropdowns, and menus
- primary result panels that overlap a secondary UI

Not allowed:
- internal IM bubbles/cards/composer bars
- table rows/cells, form option rows, dashboard/chart cards, skeleton lines, thumbnails, and generic icon placeholders

Internal modules should stay flat and rely on fills, strokes, and dividers.

## Primary Floating UI Shadow

```css
box-shadow: 0 4px 6px rgba(31,35,41,0.06),
            0 8px 15px rgba(31,35,41,0.04),
            0 10px 14px rgba(31,35,41,0.04);
```

Use only for banner-level foreground floating panels, large popovers, modal-like result surfaces, or primary UI surfaces that visibly overlap another UI.

## Secondary Floating UI Shadow

```css
box-shadow: 0 2px 8px rgba(31,35,41,0.04);
```

Use only for smaller floating menus/popovers or backing plates that need separation from the banner background. Do not use this on internal cards, IM messages, table blocks, form options, dashboard cards, or chart cards inside a product surface.

---

# 11. Background Asset System

## Background Source

Backgrounds are NOT AI-generated.

Backgrounds come from: `figma-refs/backgrounds/`

Designers can:
- manually choose backgrounds
- or allow automatic recommendation when no background is specified

If the user provides, updates, or names a background asset, that asset is locked as the first choice. Do not replace it based on mood mapping unless the user explicitly asks for a different background.

If revising an existing banner, preserve its current background unless the requested change is about background mood, color, or asset selection.

## Background Asset Lock

Before coding, record the exact background file in the Asset Lock Manifest.

Rules:
- The generated HTML must reference the locked file exactly.
- Do not replace a user-provided, updated, named, or existing background with a mood-mapped background.
- If the source banner already uses a background, keep it unless the user explicitly requests a background change.
- A background change is a product/design decision, not an implementation detail.

## Background Purpose

Backgrounds are:
- atmospheric
- emotional
- supportive

Backgrounds are NOT:
- semantic
- narrative
- functional

The UI must remain the visual focus.

## Background Rules

Allowed:
- organic gradients
- soft blur
- large smooth color transitions
- low-frequency texture

Forbidden:
- illustrations
- particles
- geometric graphics
- sharp contrast
- noisy patterns
- decorative visual centers

## Priority Rule

If the background competes with the UI:
- weaken background first

UI readability and hierarchy always take priority.

---

# 12. Background Library Structure

```
figma-refs/backgrounds/
├── blue-soft-flow.png
├── dreamy-pink.png
├── elegant-purple.png
├── green-mist.png
└── green-spring.png
```

---

# 13. Background Mood Mapping

## Blue

Suitable for:
- AI
- automation
- messaging
- productivity
- collaboration

Feeling:
- rational
- efficient
- modern

## Green

Suitable for:
- forms
- surveys
- writing
- lightweight workflows

Feeling:
- calm
- soft
- approachable

## Purple

Suitable for:
- generative AI
- creativity
- inspiration
- content generation

Feeling:
- imaginative
- intelligent
- futuristic

---

# 14. Icon System

## Source Priority

Use product-native icons from `figma-refs/components/icons/` whenever the original product design includes an icon for the feature.

Rules:
- Check `figma-refs/components/icons/index.md` first, then read the matching SVG file and reuse its path data.
- Do not draw a replacement icon when a matching product icon exists.
- Core feature icons and source-provided semantic icons are product evidence. Table, filter, AI input, voice, send, selected action, and primary field-type icons must use Figma/local SVG assets and be listed in the Asset Lock Manifest. Do not redraw them with CSS approximations.
- Core semantic icons must also be listed in `Icon Lock Manifest` with a stable role and exact asset path. Render them with `data-icon-role`, for example `<img data-icon-role="polish-panel-header-icon" src="../figma-refs/components/icons/icon_effects_outlined.svg" alt="">`.
- Do not use CSS-drawn fallback classes for locked icons: `.css-icon`, `.drawn-icon`, `.sparkle-icon`, `.star-icon`, `.magic-icon`, `.polish-star`, `.custom-icon`, or `.fake-icon`.
- Keep the same icon in every instance of the same product action, such as the trigger button and the floating panel header.
- For AI polish / 润色, use the EffectsOutlined / polish icon from the icon library, not a generic sparkle fallback.

## Allowed
- minimal line icons
- monochrome icons
- product-native symbols

## Forbidden
- giant feature icons
- colorful illustrations
- 3D icons
- emoji-style icons
- decorative iconography

Icons are supporting elements only.

The UI itself must remain the primary visual language.

## Icon Abstraction

When abstracting icons, first decide whether the icon has semantic value.

Remove icons that do not explain the feature path:
- decorative toolbar icons
- repeated top-right action icons
- settings, more, close, sort, or view controls when they are not part of the core interaction
- any icon that would become visual noise after abstraction

Keep and abstract icons that identify a product object or menu choice:
- table / view type icons
- field type icons
- workflow node icons
- menu item icons
- feature trigger icons

For kept abstract icons:
- Preserve the original icon position and approximate size.
- Use a filled neutral gray shape, not an outlined square.
- Default fill: `rgba(15, 15, 16, 0.06)`.
- For menu item icons, use a consistent filled rounded square placeholder for every abstracted menu icon. Recommended size: `18×18px`, radius `4px`, fill `rgba(15, 15, 16, 0.06)`.
- Do not vary menu item abstract icons by row with circles, pills, or line groups. In menus, consistency is more important than category hinting.
- Outside menus, simple filled primitives may hint at category: square for object/card/table type, circle for person/avatar, pill/line group for text/list type.
- If the original icon is a checkbox field or actual selection control, use the real checkbox component rules instead.

Forbidden in icon abstraction:
- Do not use an outlined square as a generic icon placeholder; it reads as a checkbox.
- Do not draw checkmarks unless the product control is actually checked.
- Do not keep unimportant toolbar icons as tiny abstract boxes.
- Do not mix abstract filled icon placeholders with real outlined product icons in the same small menu unless there is a clear primary/secondary reason.

## Consistency Rule

Within the same module, all icons MUST use the same style — all outlined or all filled. Never mix styles within a single view.

---

# 15. Information Hierarchy

## Core Principle

The feature should be expressed through:
- interface state
- interaction relationship
- content transformation

NOT through:
- explanation text
- marketing copy
- slogans

## Example — Attachment Sending

Keep:
- automation nodes
- attachment list
- IM message panel

Remove:
- topbars
- unrelated controls
- repeated labels
- decorative icons

## Example — AI Polish

Keep:
- original content
- "润色" trigger
- optimized result

Remove:
- AI disclaimer
- helper labels
- educational copy
- extra buttons

---

# 16. HTML Output Requirements

The generated result should:
- be valid HTML/CSS
- be screenshot-ready
- include a development HTML file for editing
- include a self-contained share HTML file for teammate review
- include a 2x high-resolution PNG for review and sharing
- support designer editing
- support deterministic layout control

The system should prioritize:
- structure
- reusability
- controllability

over:
- artistic randomness
- image-generation aesthetics

## Share HTML

Never send teammates a `file://` link to a local HTML path. Local file links only work on the author's machine.

Each banner should produce:
- `output/<name>.html` — development version, uses relative asset paths for easy editing
- `output/<name>.share.html` — share version, local image assets inlined as data URIs
- `output/<name>@2x.png` — final high-resolution review image, 1800×1000px

Create the share version with:

```bash
python3 scripts/make_share_html.py output/<name>.html
```

The share HTML must not depend on `figma-refs/` existing on the recipient's machine.

## PNG Export

The HTML canvas remains fixed at 900×500px. The final PNG must be captured at 2x pixel density:

- Final PNG size: 1800×1000px
- File name: `output/<name>@2x.png`
- Use browser screenshot/export with device scale factor 2
- Do not stretch a 900×500 PNG after capture; render at 2x during screenshot
- A 900×500 PNG may be generated for quick checks, but it is not the final deliverable

Example Chrome export:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --force-device-scale-factor=2 --window-size=900,500 --screenshot=output/<name>@2x.png file:///$PWD/output/<name>.html
```

---

# 17. Final Quality Checklist

## Composition
- [ ] secondary UI cropped
- [ ] secondary/background UI has a negative left offset and is cut by the banner's left edge
- [ ] secondary/background UI does not show its complete left rounded corner unless the composition has an explicit reason
- [ ] primary UI floating
- [ ] overlapping relationship exists
- [ ] major UI surfaces are vertically staggered; top edges differ by at least 32px
- [ ] composition defaults to two UI layers: one Secondary UI and one Primary UI
- [ ] any third UI layer is product-real, necessary for a distinct middle step, and visually subordinate
- [ ] no decorative third screenshot, device shell, modal, or explanatory panel
- [ ] no rigid alignment
- [ ] if a Figma/design reference was provided, it was treated as the concrete product specification, not visual inspiration
- [ ] if a Figma/design reference was provided, the banner preserves the source layout, spacing, icon choice, radius, and interaction logic before abstraction
- [ ] if exact fidelity conflicts with banner composition, lower-priority UI was moved/cropped/removed instead of changing constrained product relationships
- [ ] component internals are aligned: repeated rows share icon x, text x, row height, and consistent vertical rhythm
- [ ] menus/popovers/dropdowns remain visually attached to their trigger and preserve source side, gap, and horizontal alignment

## UI Style
- [ ] fully flat
- [ ] no perspective
- [ ] no 3D
- [ ] no glassmorphism

## Content
- [ ] abstracted information
- [ ] only key feature remains
- [ ] no repeated information
- [ ] no explanatory copy
- [ ] feature path is compressed into two layers unless a real third interaction state is necessary
- [ ] dashboard/chart abstraction is sparse, aligned, and product-native; no random dense fake charts
- [ ] core IM message, selected menu item, trigger button, result panel, and form field are not clipped or partially hidden

## Background
- [ ] exact background file was locked before coding
- [ ] uses approved background asset
- [ ] if user provided, updated, named, or already used a background, that exact background was preserved
- [ ] background weaker than UI
- [ ] no decorative graphics

## Assets
- [ ] Asset Lock Manifest was written before coding
- [ ] all foreground/midground human avatars use locked `Avatar-image-*` SVG files
- [ ] no CSS-drawn human faces, random portraits, initials, or gradient avatar substitutes
- [ ] matching product icons use library SVGs unless intentionally removed or abstracted

## Shadows
- [ ] same-hue shadows
- [ ] no black shadows
- [ ] primary UI elevation stronger
- [ ] shadow softness preserved

---

# 18. Final Goal

The final output should feel like:
- a premium SaaS product visual
- a modern UI composition
- a realistic product interaction scene

NOT:
- a tutorial
- a screenshot dump
- a marketing poster
- a decorative illustration

---

# 19. Product Color System

Extracted from component SVGs.

## Brand Primary
- `#1456F0` — Primary blue, CTAs, active states, switch, checkbox, progress fill
- `#336DF4` — Secondary blue, tag dots, accent elements

## Semantic Colors
- `#258832` — Success green, green tag dot
- `#FF615D` — Increase/metrics red
- `#F0F4FF` — Info notice background
- `#DEE0E3` — Progress track background

## Tag Colors (from tag SVGs)
- Blue dot: `#336DF4`
- Green dot: `#258832`
- Tag bold bg: `#1F2329` at 10% opacity

## Neutral Palette
- `#1F2329` — Primary text
- `#646A73` — Secondary text, labels, icons
- `#8F959E` — Placeholder, disabled
- `#D0D3D6` — Input/select border (0.5px)
- `#C9CDD4` — Dividers, connection lines
- `#E5E6EB` — Light borders
- `#F2F3F5` — Page background, section bg
- `#F7F8FA` — Card background, hover bg
- `#FFFFFF` — Surface, card, input bg

---

# 20. Module Abstraction Guide

Reference screenshots: `figma-refs/views/`

## Table View
- Keep: 3-5 columns × 4-6 rows, field type cues (tags, avatars, checkboxes, dates), toolbar fragment
- Remove: sidebar, full toolbar, row numbers, pagination
- Colors: header `#F7F8FA`, alternating `#FFFFFF`/`#F7F8FA`, tag colors blue/green/orange/purple

## Kanban View
- Keep: 2-3 columns × 2-3 cards, column header + count, title + 1-2 metadata per card
- Remove: toolbar, sidebar, excessive card metadata
- Colors: column `#F2F3F5`, card `#FFFFFF`

## Gantt View
- Keep: 4-6 task rows with bars, timeline header, 2-3 bar colors, today marker
- Remove: left task list detail, full date range, dependency lines (unless feature-relevant)
- Colors: bars blue/green/orange, today `#F54A45`

## Gallery View
- Keep: 2-3 cards with cover images, title + 1-2 metadata
- Remove: toolbar, cards beyond 3, full metadata
- Colors: card `#FFFFFF`, cover placeholder gradient/solid

## Calendar View
- Keep: 2-3 weeks grid, 3-5 event color bars, today indicator
- Remove: full month, mini calendar, toolbar
- Colors: event colors blue/green/orange/purple, today `#1456F0` subtle bg

## Form
- Keep: title, 3-4 fields (mix types), submit button
- Remove: settings sidebar, full field list, header image
- Colors: input border `#D0D3D6` 0.5px, submit `#1456F0`

## Workflow
- Keep: trigger + 1-2 action nodes, connection lines, node icon + label
- Remove: config panels, sidebar, status indicators, zoom controls
- Colors: trigger accent `#1456F0`, action accent green/orange, canvas `#F7F8FA`
- Layout: **vertical only** (product constraint)

## Dashboard
- Keep: 1-2 chart cards when dashboard is secondary; one focused chart/metric card when dashboard is primary; title fragment and key metric numbers only when feature-relevant
- Remove: filter bar, full grid, sidebar
- Colors: card `#FFFFFF`, bg `#F2F3F5`, chart colors blue/green/orange/purple
- Layout: clean grid alignment, 12px card radius, 16-20px inner padding
- Charts: use one primitive per card only: rounded bar chart, single-line sparkline, donut with 2-3 segments, or metric card
- Avoid: dense axes, legends, mixed chart types in one card, many colors, random fake data, tiny unreadable labels
- For metric card abstraction, use `references/modules/dashboard.md` and follow the approved abstract metric-card variants.

## IM / Bot Messages
- Keep: bot avatar + name, 1-2 message cards, action buttons (if feature-relevant)
- Keep core message text/card content fully visible. Do not crop the important IM message, bot response, selected action, or command result at the banner edge.
- Remove: full history, unrelated message cards, input bar, sidebar, timestamps
- If an IM action menu or dropdown is the feature focus, keep the trigger icon/button and the menu anchored with the source design's gap and direction.
- If the input/composer bar and action menu are part of the feature path, preserve their spatial relationship from the source: input baseline, icon row, trigger button, menu side, menu gap, and horizontal alignment must read as one connected component.
- Do not let the composer input, send button, or action icons drift independently. Move the composer group together if space is tight.
- Colors: chat `#F2F3F5`, card `#FFFFFF`, bubble bot `#FFFFFF` / user `#1456F0`

---

# 21. Common Components

Source: `figma-refs/components/`

## Person Avatars
- Circular, 24-32px
- Single or stacked (overlapping)
- Asset source: `figma-refs/components/avatar/`
- Three types by usage:
  - **Blue default** (`Avatar_Person_blue`): needs emphasis but no specific identity
  - **Grey default** (`Avatar_Person_grey`): abstracted task components, visually recessive
  - **Colorful real** (`Avatar-image-*`): general person avatar, needs real person feel
- If the source UI shows a real avatar or the banner needs a person/avatar with real-person feel, use the preset `Avatar-image-*` assets. Do not generate a new face, use a random web image, or replace it with a plain circle.
- If the user has provided or updated avatar assets, those assets are the first choice and must not be substituted.
- Use solid color circles only for low-priority background avatars where identity is irrelevant.
- Before coding, lock exact avatar filenames in the Asset Lock Manifest.
- Every visible foreground or midground human avatar must be an `<img>` using a locked `Avatar-image-*` SVG. CSS-drawn faces, initials, gradient circles, emoji-style heads, or random web photos are not allowed.
- If several real-person avatars appear, use distinct preset `Avatar-image-*` files where possible. For low-priority background avatars, it is acceptable to reuse a preset avatar with reduced emphasis, but do not mix preset avatars with custom portraits.

## Buttons
- **Primary** (`Button_Basic`): `#1456F0` bg, white text, radius 6px, height 28px — main CTA
- **Secondary** (`Button_Basic-1`): white bg, `#1456F0` text + border — secondary action
- **Tertiary** (`Button_Basic-2`): light gray bg, neutral text — weak action
- **Danger** (`Button_Basic-3`): red-toned — destructive action
- **Float** (`Button_Float`): circular, shadow elevation — FAB / floating action
- **Icon** (`Button_Icon`, `Button_Icon-1`): icon-only circle, subtle bg — compact action
- **Text** (`Button_Text`): `#1456F0` text, no bg, no border — inline action
- **Text Secondary** (`Button_Text-1`): gray text, no bg — weak inline action

## Tags
- Pill-shaped with colored dot (r=3) + text, height 22px
- **Bold variant** (`Tag_Status_Bold`): bg `#1F2329` at 10%, radius 6px, height 24px
- Dot colors: blue `#336DF4`, green `#258832`, also red, orange, purple, indigo, turquoise, lime, yellow, carmine, gray
- **AI gradient tag**: special gradient variant

## Input / Select
- Height 32px, radius 8px
- Border: `#D0D3D6` 0.5px, fill: white
- Placeholder: `#8F959E`, chevron: `#646A73`

## Card Container
- White bg, radius 12px
- Shadow: triple-layer (see Shadow System)

## Checkbox
- 16×16px, square
- Checked: `#1456F0` fill, white checkmark

## Switch
- Track: pill shape, `#1456F0` when checked
- Thumb: white circle with subtle shadow

## Progress Bar
- Line: track `#DEE0E3`, fill `#1456F0`, pill-shaped ends
- Circle: same colors, ring shape
- Percentage text: `#8F959E`

## Notice / Alert
- Height 40px, radius 6px
- Info: bg `#F0F4FF`, icon `#1456F0`
- Close button: `#646A73`

## Metrics
- Increase: `#FF615D` with up arrow
- Success: green, Warning: orange, Danger: red, Neutral: gray

## Tabs
- Line variant: underline indicator
- View variant: card-like segments
- Active: `#1456F0`, Inactive: `#646A73`

## Image Placeholder
- Used in: gallery cards, list rows, App Mode cards — any scene needing an image feel
- Not a gray block — has visual texture to suggest "photo here"
- Source: `figma-refs/components/image/image1-4.svg`
- Pick 1-2 per banner, avoid repeating the same image adjacent

## Toolbar Fragment
- View name + icon on left, 2-3 action icons on right
- 40-48px height

---

# 22. Banner Composition Pairings

## Data Features
| Primary UI | Secondary UI | Background |
|---|---|---|
| Table (cell detail) | Table (overview) | blue-soft-flow |
| AI panel / popup | Table (cell) | purple / green-mist |
| Table (sorted) | Table (unsorted) | blue-soft-flow |

## Automation
| Primary UI | Secondary UI | Background |
|---|---|---|
| Workflow (trigger) | Workflow (flow) | blue-soft-flow |
| AI action card | Workflow (flow) | purple / green-spring |
| IM message card | Workflow (flow) | blue-soft-flow |

## Form & Collection
| Primary UI | Secondary UI | Background |
|---|---|---|
| Form (generated) | Form (editor) | green-mist |
| Form (new field) | Form (overview) | green-spring |
| Dashboard (chart) | Form (overview) | green-mist |

## Visualization
| Primary UI | Secondary UI | Background |
|---|---|---|
| Dashboard (new card) | Dashboard (grid) | blue-soft-flow |
| Gantt (dependency) | Gantt (timeline) | green-mist |
| Calendar (event) | Calendar (grid) | blue-soft-flow |

## Bot & Messaging
| Primary UI | Secondary UI | Background |
|---|---|---|
| IM (card message) | IM (chat) | blue-soft-flow |
| IM (command result) | IM (chat) | purple |
| IM (notification card) | Workflow (trigger) | blue-soft-flow |

---

# 23. Reference Examples

Source: `examples/`

## Case 1 — Workflow New Trigger
- Primary: trigger node card (floating, right)
- Secondary: workflow nodes (cropped, left, weaker)
- Background: blue-soft-flow
- Key: secondary UI partially cropped at left edge, primary UI overlaps with stronger shadow

## Case 2 — AI Agent Feature
- Primary: AI chat panel (floating, right)
- Secondary: table view (cropped, left, abstracted)
- Background: green-mist
- Key: table view is abstracted with placeholder content, AI panel shows real interaction state

## Case 3 — Workflow Date Trigger
- Primary: trigger configuration panel (floating, right)
- Secondary: workflow canvas with date trigger and message action (cropped, left, weaker)
- Background: elegant-purple / purple mood
- Key: selected workflow node points to the configuration panel; keep date field and trigger time visible as the core configuration result

## Case 4 — Workflow Set Field Value
- Primary: action configuration panel (floating, right)
- Secondary: workflow canvas with selected action node (cropped, left, weaker)
- Background: green-spring
- Key: selected workflow action leads to field-setting options; keep the new linked-field capability visually prominent while abstracting unrelated fields

## Case 5 — Dashboard Countdown Focus
- Primary: countdown component card (floating, left, enlarged, real values)
- Secondary: dashboard canvas with chart cards (large, cropped left/bottom, muted)
- Background: green-mist
- Key: the dashboard proves the component context; the countdown card is the only readable feature result, with dashboard charts kept as soft product evidence

## Case 6 — Workflow Date Configuration
- Primary: trigger date configuration panel (floating, right)
- Secondary: workflow canvas with selected trigger and message node (large, cropped left/bottom)
- Background: elegant-purple
- Key: selected workflow node connects to the configuration panel; use the default pointer asset as a path cue, not as decoration

## Case 7 — App/Table Focus Magnification
- Primary: same-interface focus surface showing the relevant app/table area at readable scale
- Secondary: original app/table interface (cropped, left/bottom, weaker)
- Background: blue-soft-flow
- Key: both layers come from the same source interface; foreground is a magnified product area, not a new invented screen

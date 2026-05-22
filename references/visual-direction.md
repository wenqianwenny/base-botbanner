# Visual Direction

Use this file before composing any Base bot banner. It is the taste layer above the implementation rules in `design.md` and the module templates.

Before writing a Visual Strategy for a new banner, resolve the User Choice Gate from `SKILL.md`: background, primary-side layout direction, and primary UI abstraction mode. This is a hard stop. If the user has not provided all three choices, ask only for the missing choices and do not continue to strategy, audit, planning, or generation until the user answers. The chosen options constrain the strategy; do not override them based on mood unless the user explicitly asks you to choose or use defaults.

## Core Goal

Create a memorable, intentional Base product banner, not just a prompt-compliant UI collage.

When a source product UI, screenshot, Figma URL, or design reference is provided, interface abstraction is mandatory. The output should preserve product logic and key geometry while simplifying non-core information into skeletons/placeholders. Do not use the source UI as an unabstracted screenshot layer.

Before writing HTML, define:
- The single feature idea the banner must communicate
- The product evidence that proves the feature
- The visual system: palette, background mood, UI hierarchy, density, lighting, texture, and negative constraints
- The reason the chosen composition is better than a flatter or busier alternative

## Taste Baseline

Use these principles as the top-level design filter:

- Root the banner in supplied context first: product UI, Figma references, feature copy, brand assets, and previous approved examples.
- Prefer a small, coherent visual vocabulary. Empty space should be solved with proportion, rhythm, crop, overlap, and focal hierarchy, not extra cards or icons.
- Make the core UI state visually dominant. Supporting UI exists only to explain context, trigger, source, or result.
- Preserve product structure, icon geometry, UI proportions, and information hierarchy before abstraction.
- Use placeholders for low-priority text and data. Do not fabricate product claims, fake metrics, fake logos, fake testimonials, or fake UI states.
- Verify the final image as a banner: it must still read clearly at small size.

## Anti-AI Visual Cliches

Avoid these unless the user explicitly asks for them or a supplied brand reference depends on them:

- Purple-pink-blue gradient as the whole idea
- Generic glossy robot mascot in a neon tech void
- Random sparkles, magic dust, HUD grids, circuit lines, bokeh orbs, or meaningless decorative glow
- Emoji-style icon filler
- Fake logos, fake metrics, fake testimonials, fake badges, fake screenshots, or invented claims
- Overcrowded compositions that try to look complete by adding many cards, charts, badges, icons, and labels
- Cheap pseudo-3D plastic treatment without a clear brand reason
- Busy texture behind important text or UI

## Composition Strategy

For concrete product features, use Type 1 banner logic:

1. Analyze the feature/value proposition.
2. Identify the source UI elements that map to the feature path.
3. Choose the fewest UI surfaces needed to show the path.
4. Remove unrelated information and abstract low-priority text/data.
5. Add background atmosphere and compose the UI so the core function is dominant.

Use the fewest truthful UI surfaces needed to explain the feature. Two surfaces are common, but not mandatory:
- Secondary/source/context UI
- Primary/result/focus UI

If the user provides only one source interface, do not invent a second product interface from another platform, device, or module. A single source interface can be centered or slightly offset on the banner. For field-level, component-level, or single-control features, use the provided source interface as context and promote the key component into a foreground floating focus card derived from that same source UI.

Use three surfaces only when the real product flow has three necessary states. A third surface used only for visual richness usually makes the banner worse.

## Approved Case Patterns

Use these patterns when the source UI matches them:

- **Context canvas + extracted component:** a large cropped product surface sits behind a foreground feature component. The foreground component is a real extracted/magnified part of the source UI, not a new invented panel. Good for countdown cards, phone fields, field-type details, and compact feature widgets.
- **Path canvas + configuration panel:** a workflow/table/app canvas shows the selected source object, and a foreground configuration/result panel shows the editable outcome. The selected object, connector/arrow, and panel must explain one product path.
- **Same-interface magnification:** when one product interface contains both context and the feature area, duplicate or crop the same source interface into a larger foreground focus surface. This is valid only when the foreground layer is sourced from the same interface and preserves its UI logic.

In all three patterns, the background/source surface should usually be larger than the banner and intentionally cropped on at least one non-core edge. Do not shrink the source surface into a complete, safe little card unless the source itself is the main feature.

Every banner should use the default pointer asset `figma-refs/components/pointer/pointer-arrow-default.png` as a top-layer action cue unless the user explicitly asks to omit it. Place it near the key trigger/action/control, such as an opened panel control, selected option, send/input action, workflow node, generated result trigger, or the component being magnified. It must clarify the product path and must not replace the product UI evidence.

The pointer supports left/right direction changes via CSS `scaleX(-1)`. Do not rotate it by default. Only rotate when the user explicitly asks or when the supplied Figma case already uses that exact rotation, and record the reason in the brief. Never place the pointer on top of product icons, readable text, selected values, or core controls.

## Variant Planning

For non-trivial or ambiguous banners, produce 2-3 atomic composition plans before writing HTML. Keep them short:

- **Spec-safe:** closest to product UI, lowest risk
- **Focused:** stronger foreground/result emphasis, still product-real
- **Editorial:** more atmospheric or cropped, but still UI-led and not decorative

Choose one plan before implementation. Do not implement multiple variants unless the user asks for them.

For straightforward revisions to an existing banner, skip variants and state the chosen strategy briefly.

## Output Reasoning

Before implementation, write a compact strategy block:

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

This strategy is a quality gate. If the plan sounds like a collection of nice-looking UI pieces instead of one product story, revise the plan before coding.

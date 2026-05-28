# Workflow / Automation Module — Base Bot Banner

Use this module when the source UI involves Base workflow, automation, triggers, actions, nodes, connector lines, branches, config panels, run logs, scheduled tasks, AI steps, notifications, or workflow creation from Base.

Workflow is a path module. Its abstraction must preserve the order and relationship of steps before simplifying visual details.

Figma references:
- Workflow original: `https://www.figma.com/design/SYKM6v8NzaaJ22C6fUlmwG/Untitled?node-id=22-28242`
- Workflow abstract: `https://www.figma.com/design/SYKM6v8NzaaJ22C6fUlmwG/Untitled?node-id=22-28338`

---

## 1. Workflow Path First

Before layout, write the actual workflow path in plain terms:

```text
trigger -> condition/data step -> AI/action step -> result/action step
```

Then decide which nodes are real, skeletonized, or removed.

Rules:
- Keep the trigger node real when the feature starts from an event, time, table record, or user action.
- Keep the feature-specific node real, such as AI generation, sending a message, updating a field, creating a record, or finding records.
- Keep the result/action node real when it proves the automation outcome.
- Preserve vertical order, numbering, connector direction, selected state, and add-node position when visible.
- Do not add fake nodes or source-absent states.

---

## 2. Product Structure To Preserve

Preserve:
- workflow canvas surface
- workflow title/header only when it identifies the module
- enabled/disabled switch when the automation state matters
- node cards with icon, title, secondary status/skeleton line
- connector lines between nodes
- selected/focused node border or state when present in source
- config panel only if the feature is about node configuration or result settings

Remove or reduce:
- full Base top bar, side navigation, search, new-item menu, help button, and run log if not part of the feature
- unrelated workflow nodes or branches
- overflow icons if they clutter the path
- repeated abstract-only nodes beyond the path needed to explain the feature

---

## 3. Node Card Rules

Approved abstract workflow pattern:
- canvas fill: source-like light neutral, commonly `#F5F6F7` or source token
- node width around `340px` to `380px` at reference scale
- node radius around `10px` to `12px`
- node padding around `18px` to `20px`
- icon tile around `39px` to `44px`
- icon tile radius around `9px` to `10px`
- title remains real for key nodes
- secondary status/detail becomes a skeleton pill unless it is feature evidence

Node hierarchy:
- selected node may keep source border/fill
- non-selected key nodes keep white fill
- low-priority node text becomes skeleton
- icons remain semantically meaningful for key nodes

Do not use checkbox-like outlined squares as generic node icons. If an icon is abstracted, use a filled rounded square with approved skeleton color, unless the source component is an actual checkbox.

---

## 4. Connector And Layout Rules

Workflow fails if the path is visually detached.

Rules:
- Node center lines must align vertically unless the source uses branches.
- Connector lines must attach to the visual center between nodes.
- Node numbering stays on the same vertical rhythm.
- Add-node controls must sit on the continuation of the connector, not float arbitrarily.
- If showing a selected node plus config panel, preserve the source side relationship between selected node and panel.
- Major workflow nodes should not be top-aligned with unrelated surfaces; maintain banner stagger when layered with other UI.

Use markers:

```css
/* ui-check balanced-content-inset selector=.workflow-node */
/* ui-check skeleton-fill selector=.workflow-skeleton expected="rgba(15, 15, 16, 0.06)" */
/* ui-check max-repeat selector=.workflow-path item-class=workflow-node max=4 */
```

---

## 5. Text Budget

Keep real:
- workflow title when it identifies the module
- trigger node title
- feature-specific action node title
- result node title when it proves the outcome
- selected config field label/value only if the feature is about configuration

Skeletonize:
- "未完成配置" style status text unless status is the story
- node subtitles/details not essential to the path
- side navigation item labels
- toolbar labels and secondary settings

Remove:
- unrelated branch/node titles
- run logs, help widgets, avatar/topbar utilities
- extra side navigation and new-item menu rows

If the feature is about a specific node type, node title is more important than workflow chrome.

---

## 6. Config Panel Rules

Show a config panel only when it is the feature result or necessary to explain the action.

If shown:
- anchor it to the selected node or source side from Figma
- keep key field labels/values real only when feature-relevant
- skeletonize secondary form values
- remove full panel controls if they are not part of the path
- treat it as a floating banner surface only if it is floating outside the source interface; internal workflow panels follow source elevation

If not shown:
- the workflow path itself should be enough to communicate automation.

---

## 7. Banner Layout

Use the fewest truthful surfaces:
- single workflow canvas when the feature is the automation path
- workflow canvas plus focus card/config panel when a specific node setting is the feature
- source Base table/app context plus workflow result only when the product path genuinely crosses surfaces

When Workflow is primary:
- center or slightly offset the path so all key nodes and connectors are readable
- show 2-4 nodes, not a full dense automation editor
- crop/remove sidebars before shrinking node titles

When Workflow is secondary:
- keep the selected/feature node visible
- simplify to trigger + action/result
- use source crop to show context, but do not let workflow nodes touch banner edges

---

## 8. Verification

Before output:
- The workflow sequence reads in correct order.
- Key trigger/action/result node titles are real and readable.
- Connector lines align to node centers.
- No source-absent nodes, states, or validation messages were added.
- Secondary node details are skeletonized or removed.
- Sidebars, top bars, run logs, and help controls are removed unless required by the path.
- Node cards have balanced internal padding and consistent icon/title alignment.
- Workflow canvas or config panels follow source elevation; do not add floating shadows to internal node cards beyond source style.
- Use `allowed-text`, `max-repeat`, `skeleton-fill`, `balanced-content-inset`, `no-shadow`, `edge-safe`, and `min-size` markers where applicable.

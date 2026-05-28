# IM Module — Base Bot Banner

Use this module when the source UI involves IM, chat, bot messages, composer input, action menus, attachments, collection form creation from IM, or menu-triggered creation flows.

## 1. Core Structure

Typical IM banner surfaces:
- Secondary UI: chat context with 1-2 message bubbles/cards and the composer area.
- Primary UI: generated result, created form, action menu, or product preview.

Do not keep the full IM history. Keep only the message, trigger, and result needed to understand the feature.

Column alignment is source-critical. Group/chat avatar, message avatars, and composer/content columns must preserve the source alignment grid when they remain in the same IM surface. Do not independently center or offset header avatars and message avatars. In the source IM layout, the avatar column is stable and the title/content starts shortly after the avatar, usually about `8px` to `12px` from the avatar edge.

## 2. Composer Group

Treat the composer as one connected component.

Composer group includes:
- input container
- placeholder or source text
- action icons
- trigger icon button
- send button if visible and relevant
- any opened menu/popover anchored to the trigger

Rules:
- Do not let input, icons, trigger, and menu drift independently.
- If space is tight, move or crop the whole composer group.
- If the composer is secondary context and not the feature trigger, abstract it or remove it.
- If the composer trigger opens the feature menu, the trigger button and menu must both remain visible.
- The feature trigger must remain inside the composer/input toolbar. Do not detach the `+` button into a standalone floating control; without the input-bar context, the trigger loses product meaning.

## 3. Action Menu

Baseline menu specs:
- Gap to trigger icon button: `4px`, tolerance `±1px`.
- Default alignment for icon-button trigger: right edge aligned to trigger right edge.
- Define anchor geometry before coding. For a menu above the trigger, the menu bottom must be `4px` above the trigger top; do not eyeball absolute `top` values.
- Preferred implementation: wrap the plus/action button in a positioned anchor and render the opened menu as its child with `right: 0; bottom: calc(100% + 4px);`. If the menu must be positioned elsewhere in the DOM, compute `menuLeft = triggerRight - menuWidth` and `menuTop = triggerTop - 4px - menuHeight` explicitly.
- Compact row height: `32px`.
- Footer/selected rows may be `40px` to `44px` when the source uses a stronger selected state.
- Icon slot: `24px`; icon visual: `18px`.
- Text start: stable, usually `40px` from row left.
- Menu width: follow source; if abstracting from the IM collection-form menu, use `180px` unless content requires the source `228px` variant.
- Dividers stay horizontal and subtle: `0.5px rgba(31,35,41,0.15)`.

Selected item rules:
- Keep the selected item label real when it is the feature evidence, such as `收集表`.
- Keep the selected row highlight if it explains the action.
- Keep semantic selected icon/check only if it is source-real and important.
- Skeletonize non-selected sibling labels unless the sibling item is also part of the feature path.
- For a creation menu focused on `收集表`, all other item labels such as image/file/calendar/live/contact/vote should become skeleton lines.
- Do not show the full list if the non-selected items are abstract-only. Keep at most `5` abstract sibling menu rows before/around the selected item; remove extras to keep the menu compact.

Abstract icon rules:
- If menu item icons are not the feature, abstract all menu icons consistently as filled rounded squares.
- Recommended abstract menu icon: `18px × 18px`, radius `4px`, fill `rgba(15, 15, 16, 0.06)`.
- Do not mix icon shapes row by row.

## 4. Message Content

Rules:
- Core IM message or generated result must never be clipped.
- Message bubbles should be left aligned with avatar and content column.
- Preserve avatar size and baseline rhythm from source where possible.
- Remove timestamps, reactions, extra side buttons, and unrelated cards unless they explain the feature.
- Skeletonize low-priority message text with `rgba(15, 15, 16, 0.06)`.
- Message bubbles, message cards, and composer/input bars are internal IM modules. Do not add box shadow to them; use flat fills, borders, and dividers. The opened action menu may have shadow because it is a banner-level floating panel.
- Use the source IM bubble/card fill. Default Lark IM abstract bubble/card fill is `#F1F2F3`; do not leave a shadowless bubble/card as pure white on a white IM surface.
- Use one internal padding token for each bubble/card, usually `16px`. Skeleton lines inside the bubble/card start at that same inset; reset the last line margin so top and bottom spacing feel equal.
- Avoid `min-height` values that create accidental extra bottom space after skeleton abstraction. If a source minimum height is needed, account for it explicitly and keep visual top/bottom inset balanced.
- When IM is secondary and the panel is cropped/narrowed, message bubbles/cards must shrink with the content column. Keep a visible right inset; do not reuse old fixed widths that nearly touch the panel edge. Add `max-size` markers to secondary IM bubbles/cards when their width is fixed.
- If a floating menu overlaps the IM area, IM bubbles/cards should not share the same right edge as the menu. Shorten secondary bubbles/cards so their right edge is visibly earlier, usually by `24px` to `40px`.
- If an image thumbnail inside a secondary IM card is only an abstract placeholder and not feature evidence, remove it instead of showing a large abstract circle/thumbnail.

## 5. Avatar Use

Rules:
- Use preset `figma-refs/components/avatar/Avatar-image-*` for visible people.
- Use `Avatar_Person_blue` or `Avatar_Person_grey` only for generic product/person placeholders.
- Use plain abstract circles only for low-priority background avatars where identity is irrelevant.
- Foreground/midground human avatars must not be CSS-drawn faces.

## 6. IM Secondary UI Compression

When IM is secondary:
- Keep the group title only if it helps identify the scene.
- Keep at most 1 selected/active tab if relevant; otherwise abstract tabs.
- Keep 1-2 message rows/cards.
- Keep the composer only if it contains the feature trigger.
- Remove top-right global tools unless the feature is about that tool.

## 7. Verification

Before output:
- header/group avatar and message avatars share the same avatar column when both are visible
- group/title text starts close to the group avatar per source spacing; do not create a large decorative gap
- menu is attached to trigger with correct side, gap, and alignment
- above-trigger menu gap measures `4px ±1px`
- right-aligned menu edge matches trigger button right edge within `1px`
- menu rows share one icon column and one text column
- only feature-relevant menu labels are real; non-core sibling labels are skeletonized
- composer group has no drift between input, icons, trigger, and menu
- feature trigger remains inside the composer/input toolbar, not isolated from its parent component
- IM message bubbles/cards/composer have no box shadow; only the opened floating menu may use shadow
- IM message bubbles/cards remain visible after shadow removal by using source fill such as `#F1F2F3`
- skeleton lines inside IM bubbles/cards use consistent inner padding and no trailing last-line margin
- skeletonized IM bubbles/cards do not rely on `min-height` that creates visibly uneven top/bottom padding
- secondary IM bubbles/cards keep visible right inset and pass `max-size` when fixed-width
- secondary IM bubbles/cards do not accidentally align flush with floating menu/panel edges
- core message, selected menu item, trigger, and result are fully visible
- avatars use approved assets

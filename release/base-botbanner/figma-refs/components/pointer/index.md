# Pointer Components

Use these assets as banner-level narrative pointers. They are not product icons.

## Assets

- `pointer-arrow-default.png` — approved top-layer cursor/arrow component from Figma node `79:34293`, including the baked-in shadow.
- `pointer-arrow-default.svg` — source/vector fallback only. Do not use it as the default banner asset when the PNG is available.

## Usage

- Default rendered size: `90px × 90px`.
- Use the PNG file directly as an `<img>`. Do not redraw it, recolor it, reconstruct it with CSS, add CSS shadow, or change its baked-in shadow.
- Place above all product UI layers with the highest local `z-index`.
- Use near the key trigger/action/control, such as a selected option, opened panel, input action, generated result trigger, or workflow node connection.
- Do not cover product icons, readable text, selected values, or core controls. The pointer may sit near the action, but the product evidence must remain visible.
- Support left/right direction by flipping the asset with CSS:

```css
.banner-pointer.flip-x {
  transform: scaleX(-1);
}
```

Do not rotate the pointer by default. Only rotate it when the user explicitly asks or when the supplied Figma case already uses that exact rotation, and record the reason in the brief.

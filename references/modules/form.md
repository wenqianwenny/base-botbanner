# Form / Questionnaire Module — Base Bot Banner

Use this module when the source UI involves Base forms, questionnaires, collection forms, form filling pages, question type fields, option rows, submit states, or form preview/result pages.

This module is not a list of one-off cases. Use provided Figma pairs as seed examples, then generalize by judging product path and information priority.

Figma references:
- PC filling default original: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=71-35898`
- PC filling default abstract: `https://www.figma.com/design/MGrpty5zqhtkxOsOarqtM4/Untitled?node-id=73-26246`

---

## 1. Abstraction Decision Model

Before drawing a form banner, classify every visible element by role.

### Keep Real

Keep information real when it explains the feature path or identifies the current form state:
- form title when it names the scenario
- current or feature-relevant question title
- current field type structure, such as text input, phone input, radio option, date input, formula field, lookup field
- feature-relevant selected/filled/validated value only if it exists in the source or user request
- submit/continue/primary action only when it helps explain the path

### Skeletonize

Skeletonize information that supports layout but is not central to the feature:
- subtitle/helper copy
- non-core option labels
- repeated placeholders such as option text
- sibling question labels when they are not the feature
- background data and low-priority form content

Use the standard skeleton fill:

```css
background: rgba(15, 15, 16, 0.06);
```

### Remove

Remove information that creates noise or competes with the feature:
- full top operation bar, share/view-record/avatar controls, unless the feature is about those controls
- invisible editing affordances such as drag handles, image buttons, delete buttons, and hover actions
- extra questions after the form structure is already clear
- repeated abstract-only rows beyond 5
- secondary media blocks when they do not explain the form path

If an element is unimportant but removing it would break recognition of the component, skeletonize it. If it is unimportant and the component still reads correctly without it, remove it.

---

## 2. PC Filling Default Pattern

The PC filling default source has:
- a large left form area
- an optional right visual/image area
- title block
- question list
- submit area

Source geometry from the seed Figma:
- Full source: `1440 × 900`
- Left form area: about `890px` wide, `rgba(255,255,255,0.5)`
- Right visual area: about `550px` wide, source image fill
- Inner form content width: `712px`
- Form title block: `64px` horizontal padding, `16px` vertical padding
- Title: `30px / 46px`, semibold, `#5D6545`
- Subtitle: `16px / 24px`, `rgba(93,101,69,0.6)`
- Question item: left index column + content column, `30px` top padding, `16px` bottom padding

Abstraction from the approved reference:
- Keep the form title real.
- Convert low-priority subtitle to a short skeleton pill.
- Keep the feature-relevant question title real.
- Keep the field structure real enough to identify the type.
- Convert non-core option labels and date placeholders to skeleton pills.
- Keep the right visual/image area if it is part of the source page mood, but it should not compete with the form path.
- Remove the top operation bar unless it is part of the feature.

---

## 3. Question List Rules

Question rows should preserve the source alignment grid:
- stable question index column
- stable arrow/connector position when visible in source
- stable content start
- stable field/input left edge

Rules:
- Keep 2-3 questions at most in a secondary form surface unless the feature needs more.
- If the focused field is the primary feature, show that question larger or more complete and reduce sibling questions.
- Question index and arrow may stay real because they communicate form order.
- Sibling question titles can stay real only if they clarify the form type; otherwise skeletonize or remove them.
- Do not show dense full form content in a banner just because it exists in the source.

Use marker when repeated question rows are abstract-only:

```css
/* ui-check max-repeat selector=.question-list item-class=question-row max=3 */
```

---

## 4. Field Component Rules

### Textarea / Long Text

Source pattern:
- height about `82px`
- border `1px solid rgba(93,101,69,0.6)`
- radius `6px`
- padding around `8px 6px`
- placeholder `14px / 22px`, `rgba(93,101,69,0.6)`

Rules:
- Preserve border, radius, and height ratio when the textarea is feature-relevant.
- Keep placeholder text only when it explains the state; otherwise skeletonize.
- Do not add shadow to internal form fields.

### Radio / Single Choice

Source pattern:
- option row `240 × 40px`
- radius `8px`
- fill `rgba(93,101,69,0.08)`
- border `1px solid rgba(93,101,69,0.5)`
- radio visual `16px`
- row gap `8px`

Rules:
- Preserve real radio circles because they identify the field type.
- Skeletonize option labels unless the option text is the feature evidence.
- Do not replace radio circles with rounded-square skeleton icons.
- Hidden edit controls such as drag, image, and delete buttons are removed unless the feature is editing options.

### Date / Line Input

Rules:
- Preserve the underline field structure when the field type matters.
- Skeletonize date placeholder text when date is not the feature.
- Keep exact source line/stroke style when the field is foreground.

### Submit / Continue Button

Rules:
- Keep the button shape and source color if it helps identify the form state.
- If the submit action is not the feature, remove its label or keep only a simple filled button silhouette.
- Buttons are lower priority than the focused field and may be removed before breaking safe margins.

---

## 5. Layout In Banner

Use the fewest surfaces that truthfully explain the form feature.

Rules:
- If only one source form interface is provided, do not invent a second platform or editor page.
- A complete PC form page can be used as the main surface; crop or scale it so the question structure remains readable.
- For a field-level feature, use source interface plus a magnified focus card derived from the same field.
- If the source has a right visual/image region and it remains visible, lock and reuse the source image asset instead of drawing a new gradient.
- Do not keep a full `1440 × 900` page in miniature if it makes the key field unreadable; crop and simplify lower-priority regions first.
- Right visual areas are mood/context, not the feature. They may be cropped, dimmed, or reduced if they compete with the form content.

---

## 6. Text Budget

Default PC form text budget:
- Form title: keep real.
- Subtitle: skeletonize unless the subtitle itself is the message.
- Current/featured question title: keep real.
- Sibling question titles: keep at most 1-2 real if they clarify structure; otherwise skeletonize.
- Option labels: skeletonize unless option content is feature evidence.
- Placeholder text: keep only when it defines the field state, such as a meaningful empty input; otherwise skeletonize.
- Primary action label: keep only when action is part of the path.

When the feature is a specific field type, the field type evidence is more important than surrounding explanatory copy.

---

## 7. Verification

Before output:
- The feature-relevant field is readable and not covered.
- The form title or source context is visible enough to identify the page.
- Non-core sibling option labels and repeated placeholders are skeletonized.
- Repeated abstract-only questions/options are capped.
- Internal form fields do not use box shadow.
- Textarea, radio, and line-input geometry follow the source component when foreground.
- Right visual/image area does not overpower the form path.
- Only source-provided states are shown; do not add validation, cursor, selected, helper, or success states unless present in the source or requested by the user.
- Any source image that remains visible is listed in the Asset Lock Manifest.
- Use `allowed-text`, `max-repeat`, `balanced-content-inset`, `source-fill`, `no-shadow`, `edge-safe`, and `min-size` markers where applicable.

#!/usr/bin/env python3
"""Static UI checks for Base bot banner HTML outputs."""

from __future__ import annotations

import argparse
import re
import shlex
import struct
import sys
from pathlib import Path


STYLE_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
CSS_BLOCK_RE = re.compile(r"(?P<selector>[^{}]+)\{(?P<body>[^{}]*)\}", re.DOTALL)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
ANCHOR_RE = re.compile(
    r"/\*\s*ui-check\s+anchored-menu\s+"
    r"selector=(?P<selector>\S+)\s+"
    r"trigger-right=(?P<trigger_right>-?\d+(?:\.\d+)?)\s+"
    r"trigger-top=(?P<trigger_top>-?\d+(?:\.\d+)?)\s+"
    r"menu-width=(?P<menu_width>-?\d+(?:\.\d+)?)\s+"
    r"menu-height=(?P<menu_height>-?\d+(?:\.\d+)?)\s*\*/"
)
GENERIC_MARKER_RE = re.compile(
    r"/\*\s*ui-check\s+"
    r"(?P<kind>balanced-padding|no-shadow|source-fill|skeleton-fill|last-margin-zero|min-size|max-size|z-index-above|rect-clearance|max-repeat|edge-safe|cropped-edge|parent-context|anchored-to|no-excess-blank|group-centered|balanced-content-inset|allowed-text)\s+"
    r"(?P<params>.*?)\s*\*/",
    re.DOTALL,
)

APPROVED_SKELETON = "rgba(15, 15, 16, 0.06)"
FLOATING_SHADOW_HINTS = (
    "menu",
    "popover",
    "dropdown",
    "modal",
    "floating",
    "overlay",
    "tooltip",
    "form-panel",
    "result-panel",
    "secondary-backing",
)
INTERNAL_SHADOW_HINTS = (
    "bubble",
    "card-message",
    "composer",
    "message-card",
    "option-row",
    "table-row",
    "chart-card",
    "metric-card",
    "skeleton",
)


def extract_css(html: str) -> str:
    return "\n".join(match.group(1) for match in STYLE_RE.finditer(html))


def normalize_selector(selector: str) -> str:
    return " ".join(selector.strip().split())


def parse_css(css: str) -> dict[str, dict[str, str]]:
    blocks: dict[str, dict[str, str]] = {}
    css_without_comments = CSS_COMMENT_RE.sub("", css)
    for match in CSS_BLOCK_RE.finditer(css_without_comments):
        selector = normalize_selector(match.group("selector"))
        body = match.group("body")
        props: dict[str, str] = {}
        for part in body.split(";"):
            if ":" not in part:
                continue
            key, value = part.split(":", 1)
            props[key.strip().lower()] = value.strip()
        if props:
            blocks[selector] = props
    return blocks


def find_rule(blocks: dict[str, dict[str, str]], selector: str) -> dict[str, str] | None:
    if selector in blocks:
        return blocks[selector]
    for key, value in blocks.items():
        selectors = [normalize_selector(item) for item in key.split(",")]
        if selector in selectors:
            return value
    return None


def px_number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    if not match:
        return None
    return float(match.group(0))


def class_name(selector: str | None) -> str | None:
    if not selector or not selector.startswith("."):
        return None
    match = re.match(r"\.([A-Za-z0-9_-]+)$", selector)
    if not match:
        return None
    return match.group(1)


def css_value_equal(actual: str | None, expected: str) -> bool:
    if actual is None:
        return False
    return " ".join(actual.lower().split()) == " ".join(expected.lower().split())


def parse_marker_params(text: str) -> dict[str, str]:
    params: dict[str, str] = {}
    for token in shlex.split(text):
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        params[key] = value
    return params


def iter_generic_markers(css: str) -> list[tuple[str, dict[str, str]]]:
    markers: list[tuple[str, dict[str, str]]] = []
    for match in GENERIC_MARKER_RE.finditer(css):
        markers.append((match.group("kind"), parse_marker_params(match.group("params"))))
    return markers


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG file: {path}")
    return struct.unpack(">II", data[16:24])


def same_px_padding(value: str) -> bool:
    tokens = value.split()
    if not tokens:
        return False
    numbers = [px_number(token) for token in tokens if "px" in token]
    if not numbers:
        return False
    if len(numbers) == 1:
        return True
    if len(numbers) == 2:
        top_bottom, left_right = numbers
        return abs(top_bottom - left_right) <= 0.1
    if len(numbers) == 3:
        top, left_right, bottom = numbers
        return abs(top - left_right) <= 0.1 and abs(top - bottom) <= 0.1
    top, right, bottom, left = numbers[:4]
    return max(abs(top - right), abs(top - bottom), abs(top - left)) <= 0.1


def padding_numbers(value: str | None) -> tuple[float, float, float, float]:
    if not value:
        return (0, 0, 0, 0)
    numbers = [px_number(token) for token in value.split() if px_number(token) is not None]
    values = [number for number in numbers if number is not None]
    if not values:
        return (0, 0, 0, 0)
    if len(values) == 1:
        top = right = bottom = left = values[0]
    elif len(values) == 2:
        top = bottom = values[0]
        right = left = values[1]
    elif len(values) == 3:
        top = values[0]
        right = left = values[1]
        bottom = values[2]
    else:
        top, right, bottom, left = values[:4]
    return (top, right, bottom, left)


def get_rect(props: dict[str, str], canvas_width: float = 900) -> tuple[float, float, float, float] | None:
    width = px_number(props.get("width"))
    height = px_number(props.get("height"))
    top = px_number(props.get("top"))
    left = px_number(props.get("left"))
    right = px_number(props.get("right"))
    if width is None or height is None or top is None:
        return None
    if left is None:
        if right is None:
            return None
        left = canvas_width - right - width
    return (left, top, width, height)


def get_selector_rect(blocks: dict[str, dict[str, str]], selector: str) -> tuple[float, float, float, float] | None:
    props = find_rule(blocks, selector)
    if not props:
        return None
    return get_rect(props)


def union_rect(rects: list[tuple[float, float, float, float]]) -> tuple[float, float, float, float] | None:
    if not rects:
        return None
    left = min(rect[0] for rect in rects)
    top = min(rect[1] for rect in rects)
    right = max(rect[0] + rect[2] for rect in rects)
    bottom = max(rect[1] + rect[3] for rect in rects)
    return (left, top, right - left, bottom - top)


def selector_rect_with_offset(
    blocks: dict[str, dict[str, str]],
    selector: str,
    offset_selector: str | None = None,
) -> tuple[float, float, float, float] | None:
    rect = get_selector_rect(blocks, selector)
    if not rect:
        return None
    if not offset_selector:
        return rect
    offset_rect = get_selector_rect(blocks, offset_selector)
    if not offset_rect:
        return rect
    return (rect[0] + offset_rect[0], rect[1] + offset_rect[1], rect[2], rect[3])


def visible_texts(html: str) -> list[str]:
    text_html = re.sub(r"<head[^>]*>.*?</head>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text_html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text_html, flags=re.DOTALL | re.IGNORECASE)
    text_html = re.sub(r"<!--.*?-->", "", text_html, flags=re.DOTALL)
    text_html = re.sub(r"<[^>]+>", "\n", text_html)
    chunks = []
    for chunk in re.split(r"\s+", text_html):
        clean = chunk.strip()
        if clean:
            chunks.append(clean)
    return chunks


def infer_child_rect_in_parent(
    blocks: dict[str, dict[str, str]],
    child_selector: str,
    parent_selector: str,
    offset_parent_selector: str | None = None,
) -> tuple[float, float, float, float] | None:
    child_props = find_rule(blocks, child_selector)
    parent_props = find_rule(blocks, parent_selector)
    if not child_props or not parent_props:
        return None
    parent_rect = get_rect(parent_props)
    if not parent_rect:
        return None
    child_width = px_number(child_props.get("width"))
    child_height = px_number(child_props.get("height"))
    if child_width is None or child_height is None:
        return None
    parent_left, parent_top, parent_width, parent_height = parent_rect
    if offset_parent_selector:
        offset_rect = get_selector_rect(blocks, offset_parent_selector)
        if offset_rect:
            parent_left += offset_rect[0]
            parent_top += offset_rect[1]
    padding_top, padding_right, _padding_bottom, _padding_left = padding_numbers(parent_props.get("padding"))
    child_left = parent_left + parent_width - padding_right - child_width
    child_top = parent_top + padding_top + (parent_height - padding_top - child_height) / 2
    return (child_left, child_top, child_width, child_height)


def get_or_infer_rect(
    blocks: dict[str, dict[str, str]],
    selector: str,
    parent_selector: str | None = None,
    offset_parent_selector: str | None = None,
) -> tuple[float, float, float, float] | None:
    rect = get_selector_rect(blocks, selector)
    if rect:
        return rect
    if parent_selector:
        return infer_child_rect_in_parent(blocks, selector, parent_selector, offset_parent_selector)
    return None


def rects_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float], clearance: float = 0) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    bx -= clearance
    by -= clearance
    bw += clearance * 2
    bh += clearance * 2
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def class_block_bounds(html: str, target_class: str) -> tuple[int, int] | None:
    open_re = re.compile(rf"<(?P<tag>\w+)[^>]*class=[\"'][^\"']*\b{re.escape(target_class)}\b[^\"']*[\"'][^>]*>", re.DOTALL)
    match = open_re.search(html)
    if not match:
        return None
    tag = match.group("tag")
    close_re = re.compile(rf"</{tag}>", re.DOTALL)
    close_match = close_re.search(html, match.end())
    if not close_match:
        return None
    return (match.end(), close_match.start())


def class_is_descendant(html: str, child_class: str, parent_class: str) -> bool:
    bounds = class_block_bounds(html, parent_class)
    if not bounds:
        return False
    body = html[bounds[0] : bounds[1]]
    return re.search(rf"class=[\"'][^\"']*\b{re.escape(child_class)}\b", body) is not None


def check_banner_dimensions(blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    banner = find_rule(blocks, ".banner")
    if not banner:
        errors.append("Missing .banner rule.")
        return
    if px_number(banner.get("width")) != 900 or px_number(banner.get("height")) != 500:
        errors.append(".banner must be exactly 900px by 500px.")


def check_png(path: Path | None, errors: list[str]) -> None:
    if path is None:
        return
    if not path.exists():
        errors.append(f"PNG does not exist: {path}")
        return
    try:
        width, height = png_size(path)
    except ValueError as exc:
        errors.append(str(exc))
        return
    if (width, height) != (1800, 1000):
        errors.append(f"PNG must be 1800x1000, got {width}x{height}: {path}")


def check_shadow_scope(blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    for selector, props in blocks.items():
        shadow = props.get("box-shadow", "").lower()
        if not shadow or shadow == "none":
            continue
        selector_l = selector.lower()
        if any(hint in selector_l for hint in INTERNAL_SHADOW_HINTS):
            errors.append(f"Internal product module must not use box-shadow: {selector}")
            continue
        if not any(hint in selector_l for hint in FLOATING_SHADOW_HINTS):
            errors.append(f"Unexpected box-shadow selector; use only banner-level floating UI: {selector}")


def check_im_modules(blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    for selector in (".bubble", ".card-message"):
        props = find_rule(blocks, selector)
        if not props:
            continue
        if "box-shadow" in props and props["box-shadow"].lower() != "none":
            errors.append(f"{selector} is an internal IM module and must not use box-shadow.")
        background = props.get("background", "").lower()
        if "#f1f2f3" not in background:
            errors.append(f"{selector} should use source IM fill #F1F2F3 after shadow removal.")
        if "min-height" in props:
            errors.append(f"{selector} should not rely on min-height that can unbalance skeleton padding.")
        padding = props.get("padding")
        if padding and not same_px_padding(padding):
            errors.append(f"{selector} padding should use one balanced inset token, got: {padding}")

    line = find_rule(blocks, ".line")
    line_last = find_rule(blocks, ".line:last-child")
    if line and "margin-bottom" in line:
        if not line_last or px_number(line_last.get("margin-bottom")) != 0:
            errors.append(".line uses margin-bottom; add .line:last-child { margin-bottom: 0; }")


def check_skeleton_color(blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    for selector, props in blocks.items():
        selector_l = selector.lower()
        if not any(token in selector_l for token in ("skeleton", ".line", "abstract")):
            continue
        background = props.get("background")
        if background and background.lower() != APPROVED_SKELETON:
            errors.append(f"{selector} uses non-approved abstract fill: {background}")


def check_generic_markers(css: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    for kind, params in iter_generic_markers(css):
        if kind in {"edge-safe", "cropped-edge", "parent-context", "anchored-to", "no-excess-blank", "group-centered", "balanced-content-inset", "allowed-text"}:
            continue
        selector = params.get("selector")
        if not selector:
            errors.append(f"ui-check {kind} is missing selector=...")
            continue

        if kind == "last-margin-zero":
            target_selector = selector if selector.endswith(":last-child") else f"{selector}:last-child"
            props = find_rule(blocks, target_selector)
            if not props or px_number(props.get("margin-bottom")) != 0:
                errors.append(f"ui-check last-margin-zero failed: {target_selector} needs margin-bottom: 0;")
            continue

        props = find_rule(blocks, selector)
        if not props:
            errors.append(f"ui-check {kind} selector not found: {selector}")
            continue

        if kind == "balanced-padding":
            expected = params.get("expected")
            padding = props.get("padding")
            if expected:
                expected_padding = f"{expected}px" if re.fullmatch(r"\d+(?:\.\d+)?", expected) else expected
                if not css_value_equal(padding, expected_padding):
                    errors.append(f"ui-check balanced-padding failed: {selector} padding {padding!r}, expected {expected_padding!r}")
            elif not padding or not same_px_padding(padding):
                errors.append(f"ui-check balanced-padding failed: {selector} padding should use one balanced inset token.")
        elif kind == "no-shadow":
            shadow = props.get("box-shadow", "").lower()
            if shadow and shadow != "none":
                errors.append(f"ui-check no-shadow failed: {selector} has box-shadow.")
        elif kind == "source-fill":
            expected = params.get("expected")
            background = props.get("background")
            if not expected:
                errors.append(f"ui-check source-fill missing expected=... for {selector}")
            elif not background or expected.lower() not in background.lower():
                errors.append(f"ui-check source-fill failed: {selector} background {background!r}, expected {expected!r}")
        elif kind == "skeleton-fill":
            expected = params.get("expected", APPROVED_SKELETON)
            background = props.get("background")
            if not css_value_equal(background, expected):
                errors.append(f"ui-check skeleton-fill failed: {selector} background {background!r}, expected {expected!r}")
        elif kind == "min-size":
            min_width = px_number(params.get("min-width"))
            min_height = px_number(params.get("min-height"))
            width = px_number(props.get("width"))
            height = px_number(props.get("height"))
            if min_width is not None and (width is None or width < min_width):
                errors.append(f"ui-check min-size failed: {selector} width {width}, expected >= {min_width}")
            if min_height is not None and (height is None or height < min_height):
                errors.append(f"ui-check min-size failed: {selector} height {height}, expected >= {min_height}")
        elif kind == "max-size":
            max_width = px_number(params.get("max-width"))
            max_height = px_number(params.get("max-height"))
            width = px_number(props.get("width"))
            height = px_number(props.get("height"))
            if max_width is not None and width is not None and width > max_width:
                errors.append(f"ui-check max-size failed: {selector} width {width}, expected <= {max_width}")
            if max_height is not None and height is not None and height > max_height:
                errors.append(f"ui-check max-size failed: {selector} height {height}, expected <= {max_height}")
        elif kind == "z-index-above":
            above_selector = params.get("above")
            if not above_selector:
                errors.append(f"ui-check z-index-above missing above=... for {selector}")
                continue
            above_props = find_rule(blocks, above_selector)
            if not above_props:
                errors.append(f"ui-check z-index-above target not found: {above_selector}")
                continue
            z_index = px_number(props.get("z-index")) or 0
            above_z_index = px_number(above_props.get("z-index")) or 0
            if z_index <= above_z_index:
                errors.append(f"ui-check z-index-above failed: {selector} z-index {z_index}, {above_selector} z-index {above_z_index}")
        elif kind == "rect-clearance":
            rect = get_rect(props)
            if not rect:
                errors.append(f"ui-check rect-clearance failed: cannot derive rect for {selector}")
                continue
            avoid_left = px_number(params.get("avoid-left"))
            avoid_top = px_number(params.get("avoid-top"))
            avoid_width = px_number(params.get("avoid-width"))
            avoid_height = px_number(params.get("avoid-height"))
            clearance = px_number(params.get("clearance")) or 0
            if None in (avoid_left, avoid_top, avoid_width, avoid_height):
                errors.append(f"ui-check rect-clearance missing avoid rect for {selector}")
                continue
            avoid_rect = (avoid_left, avoid_top, avoid_width, avoid_height)  # type: ignore[arg-type]
            if rects_overlap(rect, avoid_rect, clearance):
                errors.append(f"ui-check rect-clearance failed: {selector} overlaps protected rect within {clearance:g}px clearance")
        elif kind == "max-repeat":
            max_count = int(params.get("max", "0") or "0")
            if max_count <= 0:
                errors.append(f"ui-check max-repeat missing valid max=... for {selector}")


def check_edge_safe(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector")
    if not selector:
        errors.append("ui-check edge-safe is missing selector=...")
        return
    rect = get_selector_rect(blocks, selector)
    if not rect:
        errors.append(f"ui-check edge-safe failed: cannot derive rect for {selector}")
        return
    left, top, width, height = rect
    distances = {
        "left": left,
        "top": top,
        "right": 900 - left - width,
        "bottom": 500 - top - height,
    }
    for side, distance in distances.items():
        min_value = px_number(params.get(f"{side}-min"))
        max_value = px_number(params.get(f"{side}-max"))
        if min_value is not None and distance < min_value:
            errors.append(f"ui-check edge-safe failed: {selector} {side} margin {distance:g}px, expected >= {min_value:g}px")
        if max_value is not None and distance > max_value:
            errors.append(f"ui-check edge-safe failed: {selector} {side} margin {distance:g}px, expected <= {max_value:g}px")


def check_cropped_edge(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector")
    if not selector:
        errors.append("ui-check cropped-edge is missing selector=...")
        return
    rect = get_selector_rect(blocks, selector)
    if not rect:
        errors.append(f"ui-check cropped-edge failed: cannot derive rect for {selector}")
        return
    left, top, width, height = rect
    overflow = {
        "left": max(0.0, -left),
        "top": max(0.0, -top),
        "right": max(0.0, left + width - 900),
        "bottom": max(0.0, top + height - 500),
    }
    sides = [side.strip() for side in params.get("side", "").split(",") if side.strip()]
    if not sides:
        errors.append("ui-check cropped-edge needs side=left|right|top|bottom")
        return
    min_out = px_number(params.get("min-out")) or 1
    for side in sides:
        if side not in overflow:
            errors.append(f"ui-check cropped-edge unsupported side={side!r}")
        elif overflow[side] < min_out:
            errors.append(f"ui-check cropped-edge failed: {selector} {side} overflow {overflow[side]:g}px, expected >= {min_out:g}px")


def check_parent_context(params: dict[str, str], html: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    child = params.get("child")
    parent = params.get("parent")
    offset_parent = params.get("offset-parent")
    if not child or not parent:
        errors.append("ui-check parent-context needs child=... and parent=...")
        return
    child_class = class_name(child)
    parent_class = class_name(parent)
    if child_class and parent_class and class_is_descendant(html, child_class, parent_class):
        return
    child_rect = get_or_infer_rect(blocks, child, parent, offset_parent)
    parent_rect = get_selector_rect(blocks, parent)
    if parent_rect and offset_parent:
        offset_rect = get_selector_rect(blocks, offset_parent)
        if offset_rect:
            parent_rect = (parent_rect[0] + offset_rect[0], parent_rect[1] + offset_rect[1], parent_rect[2], parent_rect[3])
    if not child_rect or not parent_rect:
        errors.append(f"ui-check parent-context failed: {child} is not inside {parent} in DOM and rect could not be derived")
        return
    cx, cy, cw, ch = child_rect
    px, py, pw, ph = parent_rect
    if cx < px or cy < py or cx + cw > px + pw or cy + ch > py + ph:
        errors.append(f"ui-check parent-context failed: {child} is visually outside {parent}")


def check_anchored_to(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    menu_selector = params.get("menu")
    trigger_selector = params.get("trigger")
    parent_selector = params.get("parent")
    offset_parent_selector = params.get("offset-parent")
    if not menu_selector or not trigger_selector:
        errors.append("ui-check anchored-to needs menu=... and trigger=...")
        return
    menu_rect = get_selector_rect(blocks, menu_selector)
    trigger_rect = get_or_infer_rect(blocks, trigger_selector, parent_selector, offset_parent_selector)
    if not menu_rect:
        errors.append(f"ui-check anchored-to failed: cannot derive menu rect for {menu_selector}")
        return
    if not trigger_rect:
        errors.append(f"ui-check anchored-to failed: cannot derive trigger rect for {trigger_selector}")
        return
    menu_left, menu_top, menu_width, menu_height = menu_rect
    trigger_left, trigger_top, trigger_width, trigger_height = trigger_rect
    side = params.get("side", "top")
    gap = px_number(params.get("gap")) or 4
    align = params.get("align", "right")
    tolerance = px_number(params.get("tolerance")) or 1

    if side == "top":
        expected = trigger_top - gap
        actual = menu_top + menu_height
        if abs(actual - expected) > tolerance:
            errors.append(f"ui-check anchored-to failed: {menu_selector} bottom {actual:g}px, expected {expected:g}px above {trigger_selector}")
    elif side == "bottom":
        expected = trigger_top + trigger_height + gap
        actual = menu_top
        if abs(actual - expected) > tolerance:
            errors.append(f"ui-check anchored-to failed: {menu_selector} top {actual:g}px, expected {expected:g}px below {trigger_selector}")
    else:
        errors.append(f"ui-check anchored-to unsupported side={side!r}")

    if align == "right":
        expected = trigger_left + trigger_width
        actual = menu_left + menu_width
        if abs(actual - expected) > tolerance:
            errors.append(f"ui-check anchored-to failed: {menu_selector} right {actual:g}px, expected {expected:g}px")
    elif align == "left":
        if abs(menu_left - trigger_left) > tolerance:
            errors.append(f"ui-check anchored-to failed: {menu_selector} left {menu_left:g}px, expected {trigger_left:g}px")
    elif align == "center":
        expected = trigger_left + trigger_width / 2
        actual = menu_left + menu_width / 2
        if abs(actual - expected) > tolerance:
            errors.append(f"ui-check anchored-to failed: {menu_selector} center {actual:g}px, expected {expected:g}px")
    else:
        errors.append(f"ui-check anchored-to unsupported align={align!r}")


def check_no_excess_blank(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector")
    if not selector:
        errors.append("ui-check no-excess-blank is missing selector=...")
        return
    rect = get_selector_rect(blocks, selector)
    if not rect:
        errors.append(f"ui-check no-excess-blank failed: cannot derive rect for {selector}")
        return
    _left, top, _width, height = rect
    panel_bottom = top + height
    content_bottom = px_number(params.get("content-bottom"))
    content_selector = params.get("content-selector")
    if content_bottom is None and content_selector:
        content_rect = get_selector_rect(blocks, content_selector)
        if content_rect:
            content_bottom = content_rect[1] + content_rect[3]
    if content_bottom is None:
        errors.append(f"ui-check no-excess-blank failed: provide content-bottom=... or a positioned content-selector for {selector}")
        return
    max_blank = px_number(params.get("max-bottom-blank")) or 40
    blank = panel_bottom - content_bottom
    if blank > max_blank:
        errors.append(f"ui-check no-excess-blank failed: {selector} bottom blank {blank:g}px, expected <= {max_blank:g}px")


def check_group_centered(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selectors_text = params.get("selectors") or params.get("selector")
    if not selectors_text:
        errors.append("ui-check group-centered needs selectors=...")
        return
    offset_selector = params.get("offset-parent")
    selectors = [selector.strip() for selector in selectors_text.split(",") if selector.strip()]
    rects = [selector_rect_with_offset(blocks, selector, offset_selector) for selector in selectors]
    if any(rect is None for rect in rects):
        missing = [selector for selector, rect in zip(selectors, rects) if rect is None]
        errors.append(f"ui-check group-centered failed: cannot derive rect for {', '.join(missing)}")
        return
    group = union_rect([rect for rect in rects if rect is not None])
    if not group:
        errors.append("ui-check group-centered failed: cannot derive group rect")
        return
    left, top, width, height = group
    tolerance = px_number(params.get("tolerance")) or 24
    axis = params.get("axis", "x")
    if axis in {"x", "both"}:
        center_x = left + width / 2
        expected_x = px_number(params.get("center-x")) or 450
        if abs(center_x - expected_x) > tolerance:
            errors.append(f"ui-check group-centered failed: group center-x {center_x:g}px, expected {expected_x:g}px ±{tolerance:g}px")
    if axis in {"y", "both"}:
        center_y = top + height / 2
        expected_y = px_number(params.get("center-y")) or 250
        if abs(center_y - expected_y) > tolerance:
            errors.append(f"ui-check group-centered failed: group center-y {center_y:g}px, expected {expected_y:g}px ±{tolerance:g}px")


def check_balanced_content_inset(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    container_selector = params.get("container")
    content_selector = params.get("content")
    if not container_selector or not content_selector:
        errors.append("ui-check balanced-content-inset needs container=... and content=...")
        return
    container = get_selector_rect(blocks, container_selector)
    content = selector_rect_with_offset(blocks, content_selector, container_selector)
    if not container:
        errors.append(f"ui-check balanced-content-inset failed: cannot derive container rect for {container_selector}")
        return
    if not content:
        errors.append(f"ui-check balanced-content-inset failed: cannot derive content rect for {content_selector}")
        return
    cx, cy, cw, ch = container
    ix, iy, iw, ih = content
    distances = {
        "top": iy - cy,
        "right": cx + cw - (ix + iw),
        "bottom": cy + ch - (iy + ih),
        "left": ix - cx,
    }
    cropped = {side.strip() for side in params.get("cropped", "").split(",") if side.strip()}
    align = params.get("align", "center")
    if align == "center":
        sides = ["top", "right", "bottom", "left"]
    elif align == "left":
        sides = ["top", "left", "bottom"]
    elif align == "right":
        sides = ["top", "right", "bottom"]
    else:
        errors.append(f"ui-check balanced-content-inset unsupported align={align!r}")
        return
    sides = [side for side in sides if side not in cropped]
    if len(sides) < 2:
        return
    values = [distances[side] for side in sides]
    tolerance = px_number(params.get("tolerance")) or 4
    if max(values) - min(values) > tolerance:
        detail = ", ".join(f"{side}={distances[side]:g}px" for side in sides)
        errors.append(f"ui-check balanced-content-inset failed: {content_selector} in {container_selector} has uneven {align} insets ({detail}), tolerance {tolerance:g}px")


def check_allowed_text(params: dict[str, str], html: str, errors: list[str]) -> None:
    values = params.get("values")
    if not values:
        errors.append("ui-check allowed-text needs values=...")
        return
    allowed = {value.strip() for value in re.split(r"\|", values) if value.strip()}
    ignored = {value.strip() for value in re.split(r"\|", params.get("ignore", "")) if value.strip()}
    texts = visible_texts(html)
    for text in texts:
        if text in ignored:
            continue
        if text not in allowed:
            errors.append(f"ui-check allowed-text failed: unexpected visible text {text!r}")


def check_geometry_markers(css: str, html: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    for kind, params in iter_generic_markers(css):
        if kind == "edge-safe":
            check_edge_safe(params, blocks, errors)
        elif kind == "cropped-edge":
            check_cropped_edge(params, blocks, errors)
        elif kind == "parent-context":
            check_parent_context(params, html, blocks, errors)
        elif kind == "anchored-to":
            check_anchored_to(params, blocks, errors)
        elif kind == "no-excess-blank":
            check_no_excess_blank(params, blocks, errors)
        elif kind == "group-centered":
            check_group_centered(params, blocks, errors)
        elif kind == "balanced-content-inset":
            check_balanced_content_inset(params, blocks, errors)
        elif kind == "allowed-text":
            check_allowed_text(params, html, errors)


def count_repeated_items(html: str, container_class: str, item_class: str, exclude_class: str | None) -> int | None:
    pattern = re.compile(
        rf"<(?P<tag>\w+)[^>]*class=[\"'][^\"']*\b{re.escape(container_class)}\b[^\"']*[\"'][^>]*>"
        rf"(?P<body>.*?)</(?P=tag)>",
        re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        return None
    count = 0
    for item in re.finditer(r"<[^>]*class=[\"'](?P<class>[^\"']*)[\"'][^>]*>", match.group("body")):
        classes = item.group("class").split()
        if item_class not in classes:
            continue
        if exclude_class and exclude_class in classes:
            continue
        count += 1
    return count


def check_html_markers(css: str, html: str, errors: list[str]) -> None:
    for kind, params in iter_generic_markers(css):
        if kind != "max-repeat":
            continue
        selector = params.get("selector", "")
        if not selector.startswith("."):
            errors.append("ui-check max-repeat currently requires a class selector such as selector=.action-menu")
            continue
        item_class = params.get("item-class")
        max_count = int(params.get("max", "0") or "0")
        if not item_class or max_count <= 0:
            errors.append(f"ui-check max-repeat missing item-class=... or max=... for {selector}")
            continue
        count = count_repeated_items(html, selector[1:], item_class, params.get("exclude-class"))
        if count is None:
            errors.append(f"ui-check max-repeat container not found: {selector}")
            continue
        if count > max_count:
            errors.append(f"ui-check max-repeat failed: {selector} has {count} repeated {item_class} items, max {max_count}")


def check_action_menu_anchor(css: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    menu = find_rule(blocks, ".action-menu")
    if not menu:
        return

    uses_wrapper_anchor = (
        menu.get("right", "").replace(" ", "") == "0"
        and "calc(100% + 4px)" in menu.get("bottom", "")
    )
    if uses_wrapper_anchor:
        return

    anchors = [match for match in ANCHOR_RE.finditer(css) if match.group("selector") == ".action-menu"]
    if not anchors:
        errors.append(
            ".action-menu must use right: 0; bottom: calc(100% + 4px) inside a trigger wrapper, "
            "or include a ui-check anchored-menu comment with trigger/menu geometry."
        )
        return

    anchor = anchors[-1]
    trigger_right = float(anchor.group("trigger_right"))
    trigger_top = float(anchor.group("trigger_top"))
    menu_width = float(anchor.group("menu_width"))
    menu_height = float(anchor.group("menu_height"))
    expected_left = trigger_right - menu_width
    expected_top = trigger_top - 4 - menu_height

    actual_left = px_number(menu.get("left"))
    actual_top = px_number(menu.get("top"))
    actual_width = px_number(menu.get("width"))
    if actual_left is None or actual_top is None or actual_width is None:
        errors.append(".action-menu geometry comment requires left/top/width in CSS.")
        return
    if abs(actual_width - menu_width) > 1:
        errors.append(f".action-menu width does not match geometry comment: {actual_width} vs {menu_width}")
    if abs(actual_left - expected_left) > 1:
        errors.append(f".action-menu right edge is not trigger-aligned: left {actual_left}, expected {expected_left}")
    if abs(actual_top - expected_top) > 1:
        errors.append(f".action-menu vertical gap is not 4px: top {actual_top}, expected {expected_top}")


def replace_css(html: str, new_css: str) -> str:
    match = STYLE_RE.search(html)
    if not match:
        return html
    return html[: match.start(1)] + new_css + html[match.end(1) :]


def update_rule_property(css: str, selector: str, prop: str, value: str) -> str:
    selector_re = re.escape(selector)
    pattern = re.compile(
        rf"(?P<head>^\s*{selector_re}\s*\{{)(?P<body>.*?)(?P<tail>^\s*\}})",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(css)
    if not match:
        return css.rstrip() + f"\n\n    {selector} {{\n      {prop}: {value};\n    }}\n"

    body = match.group("body")
    prop_pattern = re.compile(rf"(?m)^(\s*){re.escape(prop)}\s*:\s*[^;]+;")
    if prop_pattern.search(body):
        body = prop_pattern.sub(rf"\1{prop}: {value};", body, count=1)
    else:
        decl_match = re.search(r"(?m)^(\s*)[a-zA-Z-]+\s*:", body)
        indent = decl_match.group(1) if decl_match else "      "
        body = body.rstrip() + f"\n{indent}{prop}: {value};\n"

    return css[: match.start("body")] + body + css[match.end("body") :]


def remove_rule_property(css: str, selector: str, prop: str) -> str:
    selector_re = re.escape(selector)
    pattern = re.compile(
        rf"(?P<head>^\s*{selector_re}\s*\{{)(?P<body>.*?)(?P<tail>^\s*\}})",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(css)
    if not match:
        return css
    body = match.group("body")
    body = re.sub(rf"(?m)^\s*{re.escape(prop)}\s*:\s*[^;]+;\n?", "", body)
    return css[: match.start("body")] + body + css[match.end("body") :]


def apply_generic_marker_fixes(css: str) -> str:
    for kind, params in iter_generic_markers(css):
        selector = params.get("selector")
        if not selector:
            continue
        if kind == "balanced-padding":
            expected = params.get("expected")
            if expected:
                value = f"{expected}px" if re.fullmatch(r"\d+(?:\.\d+)?", expected) else expected
                css = update_rule_property(css, selector, "padding", value)
        elif kind == "no-shadow":
            css = remove_rule_property(css, selector, "box-shadow")
        elif kind == "source-fill":
            expected = params.get("expected")
            if expected:
                css = update_rule_property(css, selector, "background", expected)
        elif kind == "skeleton-fill":
            expected = params.get("expected", APPROVED_SKELETON)
            css = update_rule_property(css, selector, "background", expected)
        elif kind == "last-margin-zero":
            target_selector = selector if selector.endswith(":last-child") else f"{selector}:last-child"
            css = update_rule_property(css, target_selector, "margin-bottom", "0")
        elif kind == "min-size":
            min_width = px_number(params.get("min-width"))
            min_height = px_number(params.get("min-height"))
            blocks = parse_css(css)
            props = find_rule(blocks, selector)
            if not props:
                continue
            width = px_number(props.get("width"))
            height = px_number(props.get("height"))
            if min_width is not None and (width is None or width < min_width):
                css = update_rule_property(css, selector, "width", f"{min_width:g}px")
            if min_height is not None and (height is None or height < min_height):
                css = update_rule_property(css, selector, "height", f"{min_height:g}px")
        elif kind == "max-size":
            max_width = px_number(params.get("max-width"))
            max_height = px_number(params.get("max-height"))
            blocks = parse_css(css)
            props = find_rule(blocks, selector)
            if not props:
                continue
            width = px_number(props.get("width"))
            height = px_number(props.get("height"))
            if max_width is not None and width is not None and width > max_width:
                css = update_rule_property(css, selector, "width", f"{max_width:g}px")
            if max_height is not None and height is not None and height > max_height:
                css = update_rule_property(css, selector, "height", f"{max_height:g}px")
        elif kind == "z-index-above":
            above_selector = params.get("above")
            if not above_selector:
                continue
            blocks = parse_css(css)
            props = find_rule(blocks, selector)
            above_props = find_rule(blocks, above_selector)
            if not props or not above_props:
                continue
            z_index = px_number(props.get("z-index")) or 0
            above_z_index = px_number(above_props.get("z-index")) or 0
            if z_index <= above_z_index:
                css = update_rule_property(css, selector, "z-index", f"{above_z_index + 1:g}")
    return css


def apply_max_repeat_fixes(html: str, css: str) -> str:
    for kind, params in iter_generic_markers(css):
        if kind != "max-repeat":
            continue
        selector = params.get("selector", "")
        if not selector.startswith("."):
            continue
        item_class = params.get("item-class")
        max_count = int(params.get("max", "0") or "0")
        exclude_class = params.get("exclude-class")
        if not item_class or max_count <= 0:
            continue
        container_class = selector[1:]
        pattern = re.compile(
            rf"(?P<open><(?P<tag>\w+)[^>]*class=[\"'][^\"']*\b{re.escape(container_class)}\b[^\"']*[\"'][^>]*>)"
            rf"(?P<body>.*?)(?P<close></(?P=tag)>)",
            re.DOTALL,
        )

        def replace(match: re.Match[str]) -> str:
            kept = 0
            lines: list[str] = []
            for line in match.group("body").splitlines(keepends=True):
                class_match = re.search(r"class=[\"'](?P<class>[^\"']*)[\"']", line)
                if class_match:
                    classes = class_match.group("class").split()
                    if item_class in classes and not (exclude_class and exclude_class in classes):
                        kept += 1
                        if kept > max_count:
                            continue
                lines.append(line)
            return match.group("open") + "".join(lines) + match.group("close")

        html = pattern.sub(replace, html, count=1)
    return html


def apply_anchor_fixes(css: str) -> str:
    blocks = parse_css(css)
    for anchor in ANCHOR_RE.finditer(css):
        selector = anchor.group("selector")
        props = find_rule(blocks, selector)
        if not props:
            continue
        trigger_right = float(anchor.group("trigger_right"))
        trigger_top = float(anchor.group("trigger_top"))
        menu_width = float(anchor.group("menu_width"))
        menu_height = float(anchor.group("menu_height"))
        css = update_rule_property(css, selector, "left", f"{trigger_right - menu_width:g}px")
        css = update_rule_property(css, selector, "top", f"{trigger_top - 4 - menu_height:g}px")
        css = update_rule_property(css, selector, "width", f"{menu_width:g}px")
    return css


def apply_fixes(html_path: Path) -> bool:
    html = html_path.read_text(encoding="utf-8")
    css = extract_css(html)
    fixed_html = apply_max_repeat_fixes(html, css)
    if fixed_html != html:
        html = fixed_html
        css = extract_css(html)
    fixed_css = apply_generic_marker_fixes(css)
    fixed_css = apply_anchor_fixes(fixed_css)
    if fixed_css == css and fixed_html == html_path.read_text(encoding="utf-8"):
        return False
    html_path.write_text(replace_css(html, fixed_css), encoding="utf-8")
    return True


def run_checks(html_path: Path, png_path: Path | None) -> list[str]:
    html = html_path.read_text(encoding="utf-8")
    css = extract_css(html)
    blocks = parse_css(css)
    errors: list[str] = []

    check_banner_dimensions(blocks, errors)
    check_png(png_path, errors)
    check_shadow_scope(blocks, errors)
    check_im_modules(blocks, errors)
    check_skeleton_color(blocks, errors)
    check_generic_markers(css, blocks, errors)
    check_geometry_markers(css, html, blocks, errors)
    check_html_markers(css, html, errors)
    check_action_menu_anchor(css, blocks, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Base bot banner HTML for common UI regressions.")
    parser.add_argument("html", type=Path, help="Generated 900x500 HTML file")
    parser.add_argument("--png", type=Path, help="Optional exported @2x PNG to verify is 1800x1000")
    parser.add_argument("--fix", action="store_true", help="Apply safe CSS fixes declared by ui-check markers before checking")
    args = parser.parse_args()

    if args.fix:
        changed = apply_fixes(args.html)
        if changed:
            print(f"Applied ui-check fixes to {args.html}")

    errors = run_checks(args.html, args.png)
    if errors:
        print("UI check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("UI check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

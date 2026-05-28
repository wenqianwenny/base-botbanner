#!/usr/bin/env python3
"""Static UI checks for Base bot banner HTML outputs."""

from __future__ import annotations

import argparse
import re
import shlex
import struct
import sys
from html.parser import HTMLParser
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
    r"(?P<kind>balanced-padding|content-density|grid-alignment|component-containment|cross-layer-consistency|divider-width|skeleton-variation|no-shadow|shadow-token|source-fill|skeleton-fill|last-margin-zero|min-size|max-size|radius|outer-frame|z-index-above|rect-clearance|max-repeat|edge-safe|cropped-edge|parent-context|anchored-to|no-shared-edge|overlap|vertical-center|no-excess-blank|group-centered|balanced-content-inset|allowed-text|text-fit|abstraction-consistency|pointer-target|pointer-asset|surface-count)\s+"
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
GRID_CARD_HINTS = (
    "dashboard-card",
    "metric-card",
    "chart-card",
    "kpi-card",
    "grid-card",
    "summary-card",
)
CHROME_CONTAINER_RE = re.compile(
    r"(?:top[-_]?bar|tool[-_]?bar|top[-_]?actions|header[-_]?actions|page[-_]?header|app[-_]?header|nav[-_]?bar)",
    re.IGNORECASE,
)
EMPTY_CHROME_CONTROL_RE = re.compile(r"(?:button|btn|action|control|pill)", re.IGNORECASE)
MEANINGFUL_CHROME_RE = re.compile(r"(?:core|feature|selected|active|trigger|pointer-target)", re.IGNORECASE)
SHADOW_PRIMARY_STRONG = (
    "0px 20px 50px rgba(158, 170, 191, 0.18), "
    "0px 8px 18px rgba(158, 170, 191, 0.08), "
    "0px 2px 6px rgba(158, 170, 191, 0.04)"
)
SHADOW_SECONDARY_SOFT = (
    "0px 10px 28px rgba(158, 170, 191, 0.10), "
    "0px 3px 10px rgba(158, 170, 191, 0.05)"
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
        class_match = re.fullmatch(r"\.([A-Za-z0-9_-]+)", selector)
        if class_match and any(selector_contains_class(item, class_match.group(1)) for item in selectors):
            return value
    return None


def selector_contains_class(selector: str, class_value: str) -> bool:
    return class_value in re.findall(r"\.([A-Za-z0-9_-]+)", selector)


def find_rule_by_class(blocks: dict[str, dict[str, str]], class_value: str) -> dict[str, str] | None:
    direct = find_rule(blocks, f".{class_value}")
    if direct:
        return direct
    for selector, props in blocks.items():
        selectors = [normalize_selector(item) for item in selector.split(",")]
        if any(selector_contains_class(item, class_value) for item in selectors):
            return props
    return None


def px_number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    if not match:
        return None
    return float(match.group(0))


def css_px_number(value: str | None) -> float | None:
    if not value:
        return None
    clean = value.strip().lower()
    if clean == "0":
        return 0.0
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)px", clean)
    if not match:
        return None
    return float(match.group(1))


def css_percent_number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)%", value.strip())
    if not match:
        return None
    return float(match.group(1))


def class_name(selector: str | None) -> str | None:
    if not selector or not selector.startswith("."):
        return None
    match = re.match(r"\.([A-Za-z0-9_-]+)$", selector)
    if not match:
        return None
    return match.group(1)


def count_class_occurrences(html: str, class_value: str) -> int:
    pattern = re.compile(r"class=[\"'][^\"']*\b" + re.escape(class_value) + r"\b[^\"']*[\"']", re.IGNORECASE)
    return len(pattern.findall(html))


def has_class(html: str, class_value: str) -> bool:
    return count_class_occurrences(html, class_value) > 0


def class_sets_containing(html: str, class_value: str) -> list[list[str]]:
    matches = re.findall(r"class=[\"']([^\"']*)[\"']", html, re.IGNORECASE)
    result: list[list[str]] = []
    for match in matches:
        classes = match.split()
        if class_value in classes:
            result.append(classes)
    return result


def css_value_equal(actual: str | None, expected: str) -> bool:
    if actual is None:
        return False
    return " ".join(actual.lower().split()) == " ".join(expected.lower().split())


def css_compact(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", "", value.lower())


def shadow_compact(value: str | None) -> str:
    if value is None:
        return ""
    compact = re.sub(r"\s+", "", value.lower())
    compact = compact.replace("0.10)", ".10)")
    return compact


APPROVED_SHADOWS = {
    "var(--shadow-primary-strong)",
    "var(--shadow-secondary-soft)",
    shadow_compact(SHADOW_PRIMARY_STRONG),
    shadow_compact(SHADOW_SECONDARY_SOFT),
}

SHADOW_TOKEN_VALUES = {
    "primary": "var(--shadow-primary-strong)",
    "primary-strong": "var(--shadow-primary-strong)",
    "strong": "var(--shadow-primary-strong)",
    "secondary": "var(--shadow-secondary-soft)",
    "secondary-soft": "var(--shadow-secondary-soft)",
    "soft": "var(--shadow-secondary-soft)",
}


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


def marker_selectors(css: str, kind: str) -> set[str]:
    return {params.get("selector", "") for marker_kind, params in iter_generic_markers(css) if marker_kind == kind and params.get("selector")}


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


def get_rect(props: dict[str, str], canvas_width: float = 900, canvas_height: float = 500) -> tuple[float, float, float, float] | None:
    width = css_px_number(props.get("width"))
    height = css_px_number(props.get("height"))
    if width is None or height is None:
        return None

    top = css_px_number(props.get("top"))
    top_percent = css_percent_number(props.get("top"))
    if top is None and top_percent is not None:
        top = canvas_height * top_percent / 100

    left = css_px_number(props.get("left"))
    left_percent = css_percent_number(props.get("left"))
    if left is None and left_percent is not None:
        left = canvas_width * left_percent / 100

    right = css_px_number(props.get("right"))
    if top is None:
        return None
    if left is None:
        if right is None:
            return None
        left = canvas_width - right - width

    transform = props.get("transform", "")
    compact_transform = css_compact(transform)
    if "translate(-50%,-50%)" in compact_transform or "translatey(-50%)" in compact_transform:
        top -= height / 2
    if "translate(-50%,-50%)" in compact_transform or "translatex(-50%)" in compact_transform:
        left -= width / 2

    return (left, top, width, height)


def get_selector_rect(blocks: dict[str, dict[str, str]], selector: str) -> tuple[float, float, float, float] | None:
    props = find_rule(blocks, selector)
    if not props:
        return None
    return get_rect(props)


def get_containment_child_rect(
    blocks: dict[str, dict[str, str]],
    child_selector: str,
    parent_rect: tuple[float, float, float, float],
    parent_props: dict[str, str],
) -> tuple[float, float, float, float] | None:
    child_props = find_rule(blocks, child_selector)
    if not child_props:
        return None
    parent_left, parent_top, parent_width, parent_height = parent_rect
    child_width = css_px_number(child_props.get("width"))
    percent_width = css_percent_number(child_props.get("width"))
    if child_width is None and percent_width is not None:
        child_width = parent_width * percent_width / 100
    max_width = css_px_number(child_props.get("max-width"))
    if child_width is not None and max_width is not None:
        child_width = min(child_width, max_width)
    child_height = css_px_number(child_props.get("height"))
    if child_width is None or child_height is None:
        return None
    padding_top, _padding_right, padding_bottom, padding_left = padding_numbers(parent_props.get("padding"))
    child_top = parent_top + padding_top + max(0.0, (parent_height - padding_top - padding_bottom - child_height) / 2)
    child_left = parent_left + padding_left
    return (child_left, child_top, child_width, child_height)


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


class SelectorTextParser(HTMLParser):
    def __init__(self, target_class: str):
        super().__init__()
        self.target_class = target_class
        self.active_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = class_attr(attrs).split()
        if self.active_depth > 0:
            self.active_depth += 1
        elif self.target_class in classes:
            self.active_depth = 1

    def handle_endtag(self, tag: str) -> None:
        if self.active_depth > 0:
            self.active_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.active_depth > 0 and data.strip():
            self.parts.append(data.strip())


def selector_visible_text(html: str, selector: str) -> str:
    cls = class_name(selector)
    if not cls:
        return ""
    parser = SelectorTextParser(cls)
    parser.feed(html)
    return " ".join(parser.parts)


def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
    return {key.lower(): value or "" for key, value in attrs}


def class_attr(attrs: list[tuple[str, str | None]]) -> str:
    for key, value in attrs:
        if key.lower() == "class" and value:
            return value
    return ""


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
            continue
        if shadow_compact(shadow) not in APPROVED_SHADOWS:
            errors.append(f"{selector} uses a non-token box-shadow. Use only var(--shadow-primary-strong) or var(--shadow-secondary-soft).")


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
        if kind in {"edge-safe", "cropped-edge", "parent-context", "anchored-to", "no-shared-edge", "overlap", "vertical-center", "no-excess-blank", "content-density", "group-centered", "grid-alignment", "component-containment", "cross-layer-consistency", "skeleton-variation", "balanced-content-inset", "allowed-text", "text-fit", "abstraction-consistency", "pointer-target", "pointer-asset", "surface-count"}:
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
        elif kind == "shadow-token":
            token = params.get("token")
            expected = SHADOW_TOKEN_VALUES.get((token or "").lower())
            if not expected:
                errors.append(f"ui-check shadow-token missing token=primary|secondary for {selector}")
                continue
            shadow = props.get("box-shadow")
            if shadow_compact(shadow) != shadow_compact(expected):
                errors.append(f"ui-check shadow-token failed: {selector} box-shadow {shadow!r}, expected {expected!r}")
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
        elif kind == "radius":
            expected = px_number(params.get("value"))
            if expected is None:
                errors.append(f"ui-check radius missing value=... for {selector}")
                continue
            radius = px_number(props.get("border-radius"))
            if radius is None:
                errors.append(f"ui-check radius failed: {selector} has no border-radius, expected {expected:g}px")
            elif abs(radius - expected) > 0.5:
                errors.append(f"ui-check radius failed: {selector} border-radius {radius:g}px, expected {expected:g}px")
        elif kind == "divider-width":
            expected = px_number(params.get("value")) or 0.5
            tolerance = px_number(params.get("tolerance")) or 0.05
            prop_names = [
                item.strip()
                for item in (params.get("props") or params.get("prop") or "border").split(",")
                if item.strip()
            ]
            for prop_name in prop_names:
                width = px_number(props.get(prop_name))
                if width is None:
                    errors.append(f"ui-check divider-width failed: {selector} has no {prop_name}.")
                elif abs(width - expected) > tolerance:
                    errors.append(
                        f"ui-check divider-width failed: {selector} {prop_name} width {width:g}px, "
                        f"expected {expected:g}px"
                    )
        elif kind == "outer-frame":
            expected_padding = px_number(params.get("padding"))
            if expected_padding is None:
                errors.append(f"ui-check outer-frame missing padding=... for {selector}")
            else:
                padding = px_number(props.get("padding"))
                if padding is None or abs(padding - expected_padding) > 0.5:
                    errors.append(f"ui-check outer-frame failed: {selector} padding {padding}, expected {expected_padding:g}px")
            expected_background = params.get("background")
            if expected_background:
                background = props.get("background")
                if css_compact(expected_background) not in css_compact(background):
                    errors.append(f"ui-check outer-frame failed: {selector} background {background!r}, expected to contain {expected_background!r}")
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


def rect_edge(rect: tuple[float, float, float, float], edge: str) -> float | None:
    left, top, width, height = rect
    if edge == "left":
        return left
    if edge == "right":
        return left + width
    if edge == "top":
        return top
    if edge == "bottom":
        return top + height
    return None


def check_no_shared_edge(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    a_selector = params.get("a")
    b_selector = params.get("b")
    edge = params.get("edge", "right")
    if not a_selector or not b_selector:
        errors.append("ui-check no-shared-edge needs a=... and b=...")
        return
    a_rect = get_selector_rect(blocks, a_selector)
    b_rect = get_selector_rect(blocks, b_selector)
    if not a_rect:
        errors.append(f"ui-check no-shared-edge failed: cannot derive rect for {a_selector}")
        return
    if not b_rect:
        errors.append(f"ui-check no-shared-edge failed: cannot derive rect for {b_selector}")
        return
    a_edge = rect_edge(a_rect, edge)
    b_edge = rect_edge(b_rect, edge)
    if a_edge is None or b_edge is None:
        errors.append(f"ui-check no-shared-edge unsupported edge={edge!r}")
        return
    min_delta = px_number(params.get("min-delta")) or 40
    delta = abs(a_edge - b_edge)
    if delta < min_delta:
        errors.append(
            f"ui-check no-shared-edge failed: {a_selector} and {b_selector} share {edge} edge "
            f"within {delta:g}px, expected >= {min_delta:g}px"
        )


def check_overlap(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    a_selector = params.get("a")
    b_selector = params.get("b")
    if not a_selector or not b_selector:
        errors.append("ui-check overlap needs a=... and b=...")
        return
    a_rect = get_selector_rect(blocks, a_selector)
    b_rect = get_selector_rect(blocks, b_selector)
    if not a_rect:
        errors.append(f"ui-check overlap failed: cannot derive rect for {a_selector}")
        return
    if not b_rect:
        errors.append(f"ui-check overlap failed: cannot derive rect for {b_selector}")
        return

    ax, ay, aw, ah = a_rect
    bx, by, bw, bh = b_rect
    overlap_x = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    overlap_y = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    min_x = px_number(params.get("min-x")) or 1
    min_y = px_number(params.get("min-y")) or 1
    if overlap_x < min_x or overlap_y < min_y:
        errors.append(
            f"ui-check overlap failed: {a_selector} and {b_selector} overlap "
            f"{overlap_x:g}px x {overlap_y:g}px, expected at least {min_x:g}px x {min_y:g}px"
        )


def check_vertical_center(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector")
    if not selector:
        errors.append("ui-check vertical-center needs selector=...")
        return
    rect = get_selector_rect(blocks, selector)
    if not rect:
        errors.append(f"ui-check vertical-center failed: cannot derive rect for {selector}")
        return
    _left, top, _width, height = rect
    center_y = top + height / 2
    target_y = px_number(params.get("target-y")) or 250
    tolerance = px_number(params.get("tolerance")) or 4
    delta = abs(center_y - target_y)
    if delta > tolerance:
        errors.append(
            f"ui-check vertical-center failed: {selector} center y {center_y:g}px, "
            f"expected {target_y:g}px ± {tolerance:g}px"
        )


def check_component_containment(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    parent_selector = params.get("parent")
    child_selector = params.get("child")
    if not parent_selector or not child_selector:
        errors.append("ui-check component-containment needs parent=... and child=...")
        return
    parent_props = find_rule(blocks, parent_selector)
    parent_rect = get_selector_rect(blocks, parent_selector)
    child_props = find_rule(blocks, child_selector)
    if not parent_props or not parent_rect:
        errors.append(f"ui-check component-containment failed: cannot derive parent rect for {parent_selector}")
        return
    if not child_props:
        errors.append(f"ui-check component-containment failed: child selector not found: {child_selector}")
        return

    if child_props.get("width", "").strip().lower() == "100%":
        errors.append(f"ui-check component-containment failed: {child_selector} must not use width: 100%")

    child_rect = get_containment_child_rect(blocks, child_selector, parent_rect, parent_props)
    if not child_rect:
        errors.append(f"ui-check component-containment failed: cannot derive child rect for {child_selector}")
        return

    inset = px_number(params.get("inset")) or 12
    parent_left, parent_top, parent_width, parent_height = parent_rect
    child_left, child_top, child_width, child_height = child_rect
    inner_left = parent_left + inset
    inner_top = parent_top + inset
    inner_right = parent_left + parent_width - inset
    inner_bottom = parent_top + parent_height - inset
    child_right = child_left + child_width
    child_bottom = child_top + child_height
    tolerance = px_number(params.get("tolerance")) or 1
    if child_left < inner_left - tolerance or child_top < inner_top - tolerance or child_right > inner_right + tolerance or child_bottom > inner_bottom + tolerance:
        errors.append(
            f"ui-check component-containment failed: {child_selector} escapes {parent_selector} content box "
            f"with inset {inset:g}px"
        )

    if params.get("require-overflow-hidden", "false").lower() in {"1", "true", "yes"}:
        overflow = parent_props.get("overflow", "").strip().lower()
        if overflow != "hidden":
            errors.append(f"ui-check component-containment failed: {parent_selector} needs overflow: hidden")


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


def check_content_density(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector")
    if not selector:
        errors.append("ui-check content-density is missing selector=...")
        return
    props = find_rule(blocks, selector)
    rect = get_selector_rect(blocks, selector)
    if not props:
        errors.append(f"ui-check content-density selector not found: {selector}")
        return
    if not rect:
        errors.append(f"ui-check content-density failed: cannot derive rect for {selector}")
        return

    expected_top = px_number(params.get("top")) or 24
    expected_right = px_number(params.get("right")) or 24
    expected_bottom = px_number(params.get("bottom")) or 24
    expected_left = px_number(params.get("left")) or 24
    tolerance = px_number(params.get("tolerance")) or 2

    padding = props.get("padding")
    if not padding:
        errors.append(f"ui-check content-density failed: {selector} needs padding: {expected_top:g}px {expected_right:g}px {expected_bottom:g}px {expected_left:g}px")
    else:
        actual_top, actual_right, actual_bottom, actual_left = padding_numbers(padding)
        expected = (expected_top, expected_right, expected_bottom, expected_left)
        actual = (actual_top, actual_right, actual_bottom, actual_left)
        if any(abs(a - e) > tolerance for a, e in zip(actual, expected)):
            errors.append(
                f"ui-check content-density failed: {selector} padding {padding!r}, "
                f"expected {expected_top:g}px {expected_right:g}px {expected_bottom:g}px {expected_left:g}px"
            )

    content_selector = params.get("content-selector")
    content_bottom = px_number(params.get("content-bottom"))
    if content_selector:
        content_rect = selector_rect_with_offset(blocks, content_selector, selector)
        if not content_rect:
            errors.append(f"ui-check content-density failed: cannot derive content rect for {content_selector}")
            return
        _left, panel_top, _width, panel_height = rect
        _content_left, content_top, _content_width, content_height = content_rect
        content_bottom = content_top + content_height
        top_inset = content_top - panel_top
        if abs(top_inset - expected_top) > tolerance:
            errors.append(f"ui-check content-density failed: {content_selector} top inset {top_inset:g}px, expected {expected_top:g}px")

    if content_bottom is None:
        errors.append(f"ui-check content-density failed: provide content-selector=... or content-bottom=... for {selector}")
        return

    _left, panel_top, _width, panel_height = rect
    blank = panel_top + panel_height - content_bottom
    max_bottom_blank = px_number(params.get("max-bottom-blank")) or (expected_bottom + tolerance)
    if blank > max_bottom_blank:
        errors.append(f"ui-check content-density failed: {selector} bottom blank {blank:g}px, expected <= {max_bottom_blank:g}px")
    if blank < 0:
        errors.append(f"ui-check content-density failed: {selector} content exceeds panel bottom by {-blank:g}px")


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


def check_grid_alignment(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selectors_text = params.get("selectors") or params.get("selector")
    if not selectors_text:
        errors.append("ui-check grid-alignment needs selectors=...")
        return
    selectors = [selector.strip() for selector in selectors_text.split(",") if selector.strip()]
    if len(selectors) < 2:
        errors.append("ui-check grid-alignment needs at least two selectors.")
        return

    rects: list[tuple[str, tuple[float, float, float, float]]] = []
    for selector in selectors:
        rect = get_selector_rect(blocks, selector)
        if not rect:
            errors.append(f"ui-check grid-alignment failed: cannot derive rect for {selector}")
            return
        rects.append((selector, rect))

    tolerance = px_number(params.get("tolerance")) or 4
    tops = [rect[1] for _selector, rect in rects]
    bottoms = [rect[1] + rect[3] for _selector, rect in rects]
    heights = [rect[3] for _selector, rect in rects]
    if max(tops) - min(tops) > tolerance:
        detail = ", ".join(f"{selector} top={rect[1]:g}" for selector, rect in rects)
        errors.append(f"ui-check grid-alignment failed: row tops differ by {max(tops) - min(tops):g}px, expected <= {tolerance:g}px ({detail})")
    if max(bottoms) - min(bottoms) > tolerance:
        detail = ", ".join(f"{selector} bottom={rect[1] + rect[3]:g}" for selector, rect in rects)
        errors.append(f"ui-check grid-alignment failed: row bottoms differ by {max(bottoms) - min(bottoms):g}px, expected <= {tolerance:g}px ({detail})")
    if max(heights) - min(heights) > tolerance:
        detail = ", ".join(f"{selector} height={rect[3]:g}" for selector, rect in rects)
        errors.append(f"ui-check grid-alignment failed: row card heights differ by {max(heights) - min(heights):g}px, expected <= {tolerance:g}px ({detail})")


def check_default_grid_alignment(blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    card_rects: list[tuple[str, tuple[float, float, float, float]]] = []
    for selector, props in blocks.items():
        selector_l = selector.lower()
        if not any(hint in selector_l for hint in GRID_CARD_HINTS):
            continue
        rect = get_rect(props)
        if rect:
            card_rects.append((selector, rect))

    tolerance = 4
    used: set[str] = set()
    for index, (selector, rect) in enumerate(sorted(card_rects, key=lambda item: (item[1][1], item[1][0]))):
        if selector in used:
            continue
        row = [(selector, rect)]
        top = rect[1]
        for other_selector, other_rect in sorted(card_rects, key=lambda item: (item[1][1], item[1][0]))[index + 1 :]:
            if abs(other_rect[1] - top) <= tolerance:
                row.append((other_selector, other_rect))
        if len(row) < 2:
            continue
        used.update(item[0] for item in row)
        heights = [item[1][3] for item in row]
        bottoms = [item[1][1] + item[1][3] for item in row]
        if max(heights) - min(heights) > tolerance or max(bottoms) - min(bottoms) > tolerance:
            detail = ", ".join(f"{item[0]} top={item[1][1]:g} bottom={item[1][1] + item[1][3]:g} height={item[1][3]:g}" for item in row)
            errors.append(f"Same-row card grid alignment failed: top-aligned card bottoms/heights differ by more than 4px ({detail})")


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


def split_marker_values(value: str | None) -> list[str]:
    return [item.strip() for item in re.split(r"\|", value or "") if item.strip()]


def check_cross_layer_consistency(params: dict[str, str], html: str, errors: list[str]) -> None:
    primary = params.get("primary")
    secondary = params.get("secondary")
    values = split_marker_values(params.get("values"))
    forbidden = split_marker_values(params.get("forbidden"))
    if not primary or not secondary or not values:
        errors.append("ui-check cross-layer-consistency needs primary=..., secondary=..., and values=...")
        return
    primary_text = selector_visible_text(html, primary)
    secondary_text = selector_visible_text(html, secondary)
    if not primary_text:
        errors.append(f"ui-check cross-layer-consistency failed: no visible text found for {primary}")
    if not secondary_text:
        errors.append(f"ui-check cross-layer-consistency failed: no visible text found for {secondary}")
    for value in values:
        if value not in primary_text:
            errors.append(f"ui-check cross-layer-consistency failed: {primary} missing {value!r}")
        if value not in secondary_text:
            errors.append(f"ui-check cross-layer-consistency failed: {secondary} missing {value!r}")
    for value in forbidden:
        if value in primary_text:
            errors.append(f"ui-check cross-layer-consistency failed: {primary} contains forbidden {value!r}")
        if value in secondary_text:
            errors.append(f"ui-check cross-layer-consistency failed: {secondary} contains forbidden {value!r}")


def check_surface_count(params: dict[str, str], html: str, errors: list[str]) -> None:
    item_class = params.get("item-class") or params.get("class")
    if not item_class:
        errors.append("ui-check surface-count needs item-class=...")
        return
    max_count = int(params.get("max", "0") or "0")
    min_count = int(params.get("min", "0") or "0")
    count = count_class_occurrences(html, item_class)
    if max_count > 0 and count > max_count:
        errors.append(f"ui-check surface-count failed: .{item_class} count {count}, expected <= {max_count}")
    if min_count > 0 and count < min_count:
        errors.append(f"ui-check surface-count failed: .{item_class} count {count}, expected >= {min_count}")


def check_margin_range(label: str, rect: tuple[float, float, float, float], sides: tuple[str, ...], errors: list[str], min_value: float = 30, max_value: float | None = 50) -> None:
    left, top, width, height = rect
    distances = {
        "left": left,
        "top": top,
        "right": 900 - left - width,
        "bottom": 500 - top - height,
    }
    for side in sides:
        distance = distances[side]
        if distance < min_value:
            errors.append(f"{label} {side} safe margin {distance:g}px, expected >= {min_value:g}px")
        if max_value is not None and distance > max_value:
            errors.append(f"{label} {side} safe margin {distance:g}px, expected <= {max_value:g}px")


def check_floating_panel_radius(html: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    floating_class_sets = class_sets_containing(html, "floating-panel")
    if not floating_class_sets:
        return
    for classes in floating_class_sets:
        radius = None
        radius_source = None
        for class_value in classes:
            props = find_rule_by_class(blocks, class_value)
            if not props:
                continue
            class_radius = px_number(props.get("border-radius"))
            if class_radius is not None:
                radius = class_radius
                radius_source = f".{class_value}"
                break
        if radius is None:
            errors.append(".floating-panel needs border-radius: 16px on itself or on its concrete panel class.")
        elif abs(radius - 16) > 0.5:
            errors.append(f".floating-panel radius failed: {radius_source} border-radius {radius:g}px, expected 16px")


def check_floating_panel_density_contract(css: str, html: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    floating_class_sets = class_sets_containing(html, "floating-panel")
    if not floating_class_sets:
        return

    density_selectors = marker_selectors(css, "content-density")
    for classes in floating_class_sets:
        selector_candidates = {f".{class_value}" for class_value in classes}
        if not selector_candidates & density_selectors:
            errors.append(
                f"{' '.join('.' + class_value for class_value in classes)} requires a ui-check content-density marker "
                "so floating panels do not keep empty footer/action space."
            )

        props = None
        props_source = None
        for class_value in classes:
            props = find_rule_by_class(blocks, class_value)
            if props and "padding" in props:
                props_source = f".{class_value}"
                break
        if not props:
            continue
        padding = props.get("padding")
        if not padding:
            continue
        actual = padding_numbers(padding)
        expected = (24, 24, 24, 24)
        if any(abs(a - e) > 2 for a, e in zip(actual, expected)):
            errors.append(f"{props_source} floating-panel padding {padding!r}, expected 24px on all four sides.")


def check_default_surface_contract(html: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    source = find_rule_by_class(blocks, "source-surface")
    primary = find_rule_by_class(blocks, "primary-surface")
    contained_context = find_rule_by_class(blocks, "contained-context-source")
    source_rect = None
    primary_rect = None
    if source and primary:
        source_z = px_number(source.get("z-index")) or 0
        primary_z = px_number(primary.get("z-index")) or 0
        if primary_z <= source_z:
            errors.append(f".primary-surface must be above .source-surface: primary z-index {primary_z:g}, source z-index {source_z:g}")
        source_rect = get_rect(source)
        primary_rect = get_rect(primary)
        if source_rect and primary_rect and rects_overlap(source_rect, primary_rect) and primary_z <= source_z:
            errors.append(".primary-surface overlaps .source-surface but is not visually above it.")

    if primary:
        primary_rect = primary_rect or get_rect(primary)
        if primary_rect:
            check_margin_range(".primary-surface", primary_rect, ("left", "top", "right", "bottom"), errors, max_value=None)
        else:
            errors.append(".primary-surface needs absolute left/top/width/height so default safe-area can be checked.")

    if source:
        source_rect = source_rect or get_rect(source)
        if source_rect:
            if contained_context:
                check_margin_range(".contained-context-source", source_rect, ("left", "top", "bottom"), errors)
                width = source_rect[2]
                if width > 620:
                    errors.append(f".contained-context-source width {width:g}px is too wide for non-cropped context; crop or simplify when width exceeds 620px.")
            else:
                check_margin_range(".source-surface", source_rect, ("top",), errors)
        else:
            errors.append(".source-surface needs absolute left/top/width/height so default top safe-area can be checked.")

    left_context = find_rule_by_class(blocks, "left-context-source")
    inferred_left_context = False
    if contained_context:
        rect = None
        context_label = ".contained-context-source"
    elif left_context:
        rect = get_rect(left_context)
        context_label = ".left-context-source"
    elif source and primary and source_rect and primary_rect:
        source_center_x = source_rect[0] + source_rect[2] / 2
        primary_center_x = primary_rect[0] + primary_rect[2] / 2
        if source_center_x < primary_center_x:
            rect = source_rect
            context_label = ".source-surface inferred as left context"
            inferred_left_context = True
        else:
            rect = None
            context_label = ".source-surface"
    else:
        rect = None
        context_label = ".left-context-source"

    if left_context or inferred_left_context:
        if not rect:
            errors.append(f"{context_label} needs absolute left/top/width/height so crop can be checked.")
        else:
            left, top, width, height = rect
            left_overflow = max(0.0, -left)
            bottom_overflow = max(0.0, top + height - 500)
            if left_overflow < 32:
                errors.append(f"{context_label} must crop beyond left edge by at least 32px, got {left_overflow:g}px")
            if bottom_overflow < 32:
                errors.append(f"{context_label} must crop beyond bottom edge by at least 32px, got {bottom_overflow:g}px")

    if has_class(html, "banner-pointer") and not has_class(html, "pointer-target"):
        errors.append(".banner-pointer requires a .pointer-target on the key trigger/action/control.")

    check_floating_panel_radius(html, blocks, errors)


def check_text_fit(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector")
    text = params.get("text")
    if not selector or not text:
        errors.append("ui-check text-fit needs selector=... and text=...")
        return
    props = find_rule(blocks, selector)
    if not props:
        errors.append(f"ui-check text-fit selector not found: {selector}")
        return
    width = px_number(props.get("width")) or px_number(props.get("min-width"))
    if width is None:
        errors.append(f"ui-check text-fit failed: {selector} needs width or min-width for text {text!r}")
        return
    font_size = px_number(props.get("font-size")) or px_number(params.get("font-size")) or 16
    icon = px_number(params.get("icon")) or 0
    gap = px_number(params.get("gap")) or (8 if icon else 0)
    padding_left = px_number(params.get("padding-left"))
    padding_right = px_number(params.get("padding-right"))
    if padding_left is None or padding_right is None:
        top, right, _bottom, left = padding_numbers(props.get("padding"))
        padding_left = padding_left if padding_left is not None else left
        padding_right = padding_right if padding_right is not None else right
    # Conservative Chinese/product UI estimate: CJK characters are about 1em wide;
    # latin/digits are narrower. Add a small tolerance so chips do not look tight.
    cjk_count = sum(1 for char in text if ord(char) > 127)
    latin_count = len(text) - cjk_count
    estimated_text_width = cjk_count * font_size + latin_count * font_size * 0.58
    required = estimated_text_width + icon + gap + padding_left + padding_right + 4
    if width < required:
        errors.append(f"ui-check text-fit failed: {selector} width {width:g}px, estimated required >= {required:g}px for {text!r}")


def target_has_role(html: str, selector: str, expected_role: str) -> bool:
    cls = class_name(selector)
    if not cls:
        return False
    tag_re = re.compile(r"<[^>]*class=[\"'][^\"']*\b" + re.escape(cls) + r"\b[^\"']*[\"'][^>]*>", re.IGNORECASE)
    role_re = re.compile(r"data-pointer-target-role=[\"']" + re.escape(expected_role) + r"[\"']", re.IGNORECASE)
    return any(role_re.search(tag) for tag in tag_re.findall(html))


def check_pointer_target(params: dict[str, str], blocks: dict[str, dict[str, str]], html: str, errors: list[str]) -> None:
    pointer_selector = params.get("pointer", ".banner-pointer")
    target_selector = params.get("target", ".pointer-target")
    pointer = get_selector_rect(blocks, pointer_selector)
    target = get_selector_rect(blocks, target_selector)
    if not pointer:
        errors.append(f"ui-check pointer-target failed: cannot derive pointer rect for {pointer_selector}")
        return
    if not target:
        errors.append(f"ui-check pointer-target failed: cannot derive target rect for {target_selector}")
        return
    px, py, pw, ph = pointer
    tx, ty, tw, th = target
    pointer_center = (px + pw / 2, py + ph / 2)
    target_center = (tx + tw / 2, ty + th / 2)
    distance = ((pointer_center[0] - target_center[0]) ** 2 + (pointer_center[1] - target_center[1]) ** 2) ** 0.5
    max_distance = px_number(params.get("max-distance")) or 140
    if distance > max_distance:
        errors.append(f"ui-check pointer-target failed: {pointer_selector} is {distance:g}px from {target_selector}, expected <= {max_distance:g}px")
    expected_role = params.get("role")
    if expected_role:
        allowed_roles = {"input-command", "primary-action", "selected-condition", "key-result"}
        if expected_role not in allowed_roles:
            errors.append(f"ui-check pointer-target failed: unknown role {expected_role!r}")
        elif not target_has_role(html, target_selector, expected_role):
            errors.append(
                f"ui-check pointer-target failed: {target_selector} needs "
                f'data-pointer-target-role="{expected_role}"'
            )


def check_pointer_asset(params: dict[str, str], blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector", ".banner-pointer")
    props = find_rule(blocks, selector)
    rect = get_selector_rect(blocks, selector)
    if not props or not rect:
        errors.append(f"ui-check pointer-asset failed: cannot derive rect for {selector}")
        return
    expected_width = px_number(params.get("width")) or 80
    expected_height = px_number(params.get("height")) or 80
    _left, _top, width, height = rect
    tolerance = px_number(params.get("tolerance")) or 1
    if abs(width - expected_width) > tolerance or abs(height - expected_height) > tolerance:
        errors.append(
            f"ui-check pointer-asset failed: {selector} is {width:g}px x {height:g}px, "
            f"expected {expected_width:g}px x {expected_height:g}px"
        )
    transform = props.get("transform", "").lower()
    compact = css_compact(transform)
    if "scale(" in compact or "scale3d(" in compact or "scaley(" in compact:
        errors.append(f"ui-check pointer-asset failed: {selector} must not scale the cursor")
    if "scalex(" in compact and "scalex(-1)" not in compact:
        errors.append(f"ui-check pointer-asset failed: {selector} may only use scaleX(-1) for horizontal flip")


class ClassItemParser(HTMLParser):
    def __init__(self, container_class: str, item_class: str):
        super().__init__()
        self.container_class = container_class
        self.item_class = item_class
        self.container_depth = 0
        self.item_depth = 0
        self.current_item: dict[str, object] | None = None
        self.items: list[dict[str, object]] = []

    @staticmethod
    def classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        for key, value in attrs:
            if key == "class" and value:
                return set(value.split())
        return set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = self.classes(attrs)
        if self.container_depth:
            self.container_depth += 1
        elif self.container_class in classes:
            self.container_depth = 1

        if not self.container_depth:
            return

        if self.item_depth:
            self.item_depth += 1
            if self.current_item is not None:
                self.current_item["descendant_classes"].update(classes)  # type: ignore[union-attr]
        elif self.item_class in classes:
            self.item_depth = 1
            self.current_item = {
                "classes": classes,
                "descendant_classes": set(classes),
                "text": [],
            }

    def handle_endtag(self, tag: str) -> None:
        if self.item_depth:
            self.item_depth -= 1
            if self.item_depth == 0 and self.current_item is not None:
                self.items.append(self.current_item)
                self.current_item = None
        if self.container_depth:
            self.container_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.item_depth and self.current_item is not None and data.strip():
            self.current_item["text"].append(data.strip())  # type: ignore[union-attr]


def class_items_in_container(html: str, container_class: str, item_class: str) -> list[dict[str, object]]:
    parser = ClassItemParser(container_class, item_class)
    parser.feed(html)
    return parser.items


class EmptyChromeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.container_stack: list[dict[str, object]] = []
        self.item_stack: list[dict[str, object]] = []
        self.empty_items: list[dict[str, str]] = []

    @staticmethod
    def class_text(attrs: list[tuple[str, str | None]]) -> str:
        return class_attr(attrs)

    @staticmethod
    def is_container(class_text_value: str, attrs: dict[str, str]) -> bool:
        if attrs.get("data-allow-empty-chrome", "").lower() in {"true", "1", "yes"}:
            return False
        if EMPTY_CHROME_CONTROL_RE.search(class_text_value):
            return False
        return bool(CHROME_CONTAINER_RE.search(class_text_value))

    @staticmethod
    def is_control(class_text_value: str) -> bool:
        return bool(EMPTY_CHROME_CONTROL_RE.search(class_text_value)) and not bool(MEANINGFUL_CHROME_RE.search(class_text_value))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = attrs_dict(attrs)
        class_text_value = self.class_text(attrs)
        starts_container = self.is_container(class_text_value, attrs_map)
        if starts_container:
            self.container_stack.append({
                "class": class_text_value,
                "depth": 1,
            })
        elif self.container_stack:
            self.container_stack[-1]["depth"] = int(self.container_stack[-1]["depth"]) + 1

        if self.item_stack:
            self.item_stack[-1]["depth"] = int(self.item_stack[-1]["depth"]) + 1
            if tag.lower() in {"img", "svg", "use"} or attrs_map.get("data-icon-role") or attrs_map.get("data-source-image-role"):
                self.item_stack[-1]["has_media"] = True

        if self.container_stack and self.is_control(class_text_value):
            self.item_stack.append({
                "class": class_text_value,
                "container": str(self.container_stack[-1]["class"]),
                "depth": 1,
                "text": [],
                "has_media": tag.lower() in {"img", "svg", "use"} or bool(attrs_map.get("data-icon-role") or attrs_map.get("data-source-image-role")),
            })

    def handle_endtag(self, tag: str) -> None:
        if self.item_stack:
            self.item_stack[-1]["depth"] = int(self.item_stack[-1]["depth"]) - 1
            if int(self.item_stack[-1]["depth"]) == 0:
                item = self.item_stack.pop()
                text = "".join(item["text"]).strip()  # type: ignore[arg-type]
                if not text and not item["has_media"]:
                    self.empty_items.append({
                        "class": str(item["class"]),
                        "container": str(item["container"]),
                    })

        if self.container_stack:
            self.container_stack[-1]["depth"] = int(self.container_stack[-1]["depth"]) - 1
            if int(self.container_stack[-1]["depth"]) == 0:
                self.container_stack.pop()

    def handle_data(self, data: str) -> None:
        if self.item_stack and data.strip():
            self.item_stack[-1]["text"].append(data.strip())  # type: ignore[union-attr]


def check_empty_chrome_controls(html: str, errors: list[str]) -> None:
    parser = EmptyChromeParser()
    parser.feed(html)
    if not parser.empty_items:
        return
    grouped: dict[str, list[str]] = {}
    for item in parser.empty_items:
        grouped.setdefault(item["container"], []).append(item["class"])
    for container, classes in grouped.items():
        examples = ", ".join(f".{class_value.split()[0]}" for class_value in classes[:3])
        errors.append(
            f"Non-core chrome in {container!r} contains empty button/control shells ({examples}). "
            "Remove the whole toolbar/topbar area unless the control is feature evidence with real text or a locked icon."
        )


def check_abstraction_consistency(params: dict[str, str], html: str, errors: list[str]) -> None:
    selector = params.get("selector", "")
    item_class = params.get("item-class")
    if not selector.startswith(".") or not item_class:
        errors.append("ui-check abstraction-consistency needs selector=.container and item-class=...")
        return
    container_class = selector[1:]
    exclude_class = params.get("exclude-class")
    skeleton_class = params.get("skeleton-class", "skeleton")
    real_class = params.get("real-class")
    mode = params.get("mode", "uniform")
    items = class_items_in_container(html, container_class, item_class)
    if not items:
        errors.append(f"ui-check abstraction-consistency failed: no .{item_class} items found in {selector}")
        return

    states: list[str] = []
    for item in items:
        class_set = item["classes"]  # type: ignore[assignment]
        descendant_classes = item["descendant_classes"]  # type: ignore[assignment]
        if exclude_class and exclude_class in class_set:
            continue
        has_skeleton = skeleton_class in descendant_classes
        has_real_class = bool(real_class and real_class in descendant_classes)
        text = " ".join(item["text"])  # type: ignore[arg-type]
        has_real_text = bool(text)
        state = "real" if has_real_class or has_real_text else "skeleton" if has_skeleton else "empty"
        states.append(state)

    if not states:
        return
    if mode == "all-skeleton":
        bad = [state for state in states if state != "skeleton"]
        if bad:
            errors.append(f"ui-check abstraction-consistency failed: {selector} non-excluded .{item_class} items must all be skeleton, got {states}")
    elif mode == "all-real":
        bad = [state for state in states if state != "real"]
        if bad:
            errors.append(f"ui-check abstraction-consistency failed: {selector} non-excluded .{item_class} items must all be real, got {states}")
    elif mode == "uniform":
        meaningful = [state for state in states if state != "empty"]
        if "real" in meaningful and "skeleton" in meaningful:
            errors.append(f"ui-check abstraction-consistency failed: {selector} mixes real and skeleton same-priority .{item_class} items: {states}")
    else:
        errors.append(f"ui-check abstraction-consistency unsupported mode={mode!r}")


def check_skeleton_variation(params: dict[str, str], html: str, blocks: dict[str, dict[str, str]], errors: list[str]) -> None:
    selector = params.get("selector", "")
    item_class = params.get("item-class", "skeleton-line")
    if not selector.startswith("."):
        errors.append("ui-check skeleton-variation needs selector=.container")
        return
    items = class_items_in_container(html, selector[1:], item_class)
    if not items:
        errors.append(f"ui-check skeleton-variation failed: no .{item_class} items found in {selector}")
        return

    widths: list[str] = []
    for item in items:
        class_set = item["classes"]  # type: ignore[assignment]
        width_value: float | None = None
        max_width_value: float | None = None
        class_order = [class_value for class_value in class_set if class_value != item_class] + [item_class]
        for class_value in class_order:
            props = find_rule_by_class(blocks, class_value)
            if not props:
                continue
            class_width = css_px_number(props.get("width"))
            class_max_width = css_px_number(props.get("max-width"))
            if class_width is not None:
                width_value = class_width
                if class_value != item_class:
                    break
            if class_max_width is not None:
                max_width_value = class_max_width
        if width_value is not None:
            widths.append(f"{width_value:g}")
        elif max_width_value is not None:
            widths.append(f"max-{max_width_value:g}")

    min_widths = int(px_number(params.get("min-widths")) or 3)
    unique_widths = sorted(set(widths))
    if len(unique_widths) < min_widths:
        errors.append(
            f"ui-check skeleton-variation failed: {selector} has {len(unique_widths)} skeleton widths "
            f"({', '.join(unique_widths) or 'none'}), expected >= {min_widths}"
        )


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
        elif kind == "no-shared-edge":
            check_no_shared_edge(params, blocks, errors)
        elif kind == "overlap":
            check_overlap(params, blocks, errors)
        elif kind == "vertical-center":
            check_vertical_center(params, blocks, errors)
        elif kind == "no-excess-blank":
            check_no_excess_blank(params, blocks, errors)
        elif kind == "content-density":
            check_content_density(params, blocks, errors)
        elif kind == "group-centered":
            check_group_centered(params, blocks, errors)
        elif kind == "grid-alignment":
            check_grid_alignment(params, blocks, errors)
        elif kind == "component-containment":
            check_component_containment(params, blocks, errors)
        elif kind == "cross-layer-consistency":
            check_cross_layer_consistency(params, html, errors)
        elif kind == "balanced-content-inset":
            check_balanced_content_inset(params, blocks, errors)
        elif kind == "allowed-text":
            check_allowed_text(params, html, errors)
        elif kind == "text-fit":
            check_text_fit(params, blocks, errors)
        elif kind == "abstraction-consistency":
            check_abstraction_consistency(params, html, errors)
        elif kind == "skeleton-variation":
            check_skeleton_variation(params, html, blocks, errors)
        elif kind == "pointer-target":
            check_pointer_target(params, blocks, html, errors)
        elif kind == "pointer-asset":
            check_pointer_asset(params, blocks, errors)
        elif kind == "surface-count":
            check_surface_count(params, html, errors)


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
        rf"(?P<head>^\s*{selector_re}\s*\{{)(?P<body>.*?)(?P<tail>\s*\}})",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(css)
    if not match:
        return css.rstrip() + f"\n\n    {selector} {{\n      {prop}: {value};\n    }}\n"

    body = match.group("body")
    prop_pattern = re.compile(rf"(?P<prefix>(?:^|;)\s*){re.escape(prop)}\s*:\s*[^;]+;?", re.DOTALL)
    if prop_pattern.search(body):
        body = prop_pattern.sub(lambda item: f"{item.group('prefix')}{prop}: {value};", body, count=1)
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
        elif kind == "content-density":
            top = px_number(params.get("top")) or 24
            right = px_number(params.get("right")) or 24
            bottom = px_number(params.get("bottom")) or 20
            left = px_number(params.get("left")) or 24
            css = update_rule_property(css, selector, "padding", f"{top:g}px {right:g}px {bottom:g}px {left:g}px")
            content_selector = params.get("content-selector")
            if content_selector:
                blocks = parse_css(css)
                panel_rect = get_selector_rect(blocks, selector)
                content_rect = selector_rect_with_offset(blocks, content_selector, selector)
                if panel_rect and content_rect:
                    desired_height = content_rect[1] + content_rect[3] - panel_rect[1] + bottom
                    current_height = panel_rect[3]
                    if desired_height > 0 and desired_height < current_height:
                        css = update_rule_property(css, selector, "height", f"{desired_height:g}px")
        elif kind == "no-shadow":
            css = remove_rule_property(css, selector, "box-shadow")
        elif kind == "shadow-token":
            token = params.get("token")
            expected = SHADOW_TOKEN_VALUES.get((token or "").lower())
            if expected:
                css = update_rule_property(css, selector, "box-shadow", expected)
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
        elif kind == "radius":
            expected = px_number(params.get("value"))
            if expected is not None:
                css = update_rule_property(css, selector, "border-radius", f"{expected:g}px")
        elif kind == "divider-width":
            expected = px_number(params.get("value")) or 0.5
            prop_names = [
                item.strip()
                for item in (params.get("props") or params.get("prop") or "border").split(",")
                if item.strip()
            ]
            blocks = parse_css(css)
            props = find_rule(blocks, selector)
            if not props:
                continue
            for prop_name in prop_names:
                value = props.get(prop_name)
                if value and "solid" in value:
                    css = update_rule_property(css, selector, prop_name, re.sub(r"-?\d+(?:\.\d+)?px", f"{expected:g}px", value, count=1))
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
    check_default_surface_contract(html, blocks, errors)
    check_floating_panel_density_contract(css, html, blocks, errors)
    check_default_grid_alignment(blocks, errors)
    check_generic_markers(css, blocks, errors)
    check_geometry_markers(css, html, blocks, errors)
    check_html_markers(css, html, errors)
    check_empty_chrome_controls(html, errors)
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

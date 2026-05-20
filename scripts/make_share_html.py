#!/usr/bin/env python3
"""Create a self-contained share HTML by inlining local image assets."""

from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from pathlib import Path


CSS_URL_RE = re.compile(r"url\((['\"]?)(?!data:|https?:|#)([^'\"\)]+)\1\)")
ATTR_RE = re.compile(r"(?P<attr>\b(?:src|href)=)(?P<quote>['\"])(?!data:|https?:|#)(?P<path>[^'\"]+)(?P=quote)")


def to_data_uri(asset_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(asset_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def should_inline(path_text: str) -> bool:
    suffix = Path(path_text.split("?", 1)[0].split("#", 1)[0]).suffix.lower()
    return suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def inline_css_urls(html: str, base_dir: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        quote, path_text = match.groups()
        if not should_inline(path_text):
            return match.group(0)
        asset_path = (base_dir / path_text).resolve()
        if not asset_path.exists():
            raise FileNotFoundError(f"Referenced asset not found: {path_text} -> {asset_path}")
        return f"url({quote}{to_data_uri(asset_path)}{quote})"

    return CSS_URL_RE.sub(replace, html)


def inline_attrs(html: str, base_dir: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        quote = match.group("quote")
        path_text = match.group("path")
        if not should_inline(path_text):
            return match.group(0)
        asset_path = (base_dir / path_text).resolve()
        if not asset_path.exists():
            raise FileNotFoundError(f"Referenced asset not found: {path_text} -> {asset_path}")
        return f"{attr}{quote}{to_data_uri(asset_path)}{quote}"

    return ATTR_RE.sub(replace, html)


def make_share_html(input_path: Path, output_path: Path | None) -> Path:
    input_path = input_path.resolve()
    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}.share.html")
    else:
        output_path = output_path.resolve()

    html = input_path.read_text(encoding="utf-8")
    html = inline_css_urls(html, input_path.parent)
    html = inline_attrs(html, input_path.parent)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Inline local image assets into a shareable HTML file.")
    parser.add_argument("input", type=Path, help="Input HTML file")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML path; defaults to *.share.html")
    args = parser.parse_args()

    output_path = make_share_html(args.input, args.output)
    print(output_path)


if __name__ == "__main__":
    main()

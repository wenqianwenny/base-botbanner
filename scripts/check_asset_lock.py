#!/usr/bin/env python3
"""Validate banner HTML asset references against the brief Asset Lock Manifest."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


CSS_URL_RE = re.compile(r"url\((['\"]?)(?P<path>[^'\"\)]+)\1\)")
ATTR_RE = re.compile(
    r"<(?P<tag>img|image|source|link)\b[^>]*?\b(?P<attr>src|href)=(?P<quote>['\"])(?P<path>[^'\"]+)(?P=quote)[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
MANIFEST_SECTION_RE = re.compile(
    r"^##\s+Asset Lock Manifest\s*$"
    r"(?P<body>.*?)"
    r"(?=^##\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
LOCAL_ASSET_RE = re.compile(
    r"(?P<path>(?:figma-refs|output/assets|assets)/[^\s`'\"),]+?\.(?:png|jpg|jpeg|gif|webp|svg))",
    re.IGNORECASE,
)
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def is_image_ref(path_text: str) -> bool:
    parsed = urlparse(path_text)
    suffix = Path(parsed.path).suffix.lower()
    return suffix in IMAGE_SUFFIXES


def is_external(path_text: str) -> bool:
    parsed = urlparse(path_text)
    return parsed.scheme in {"http", "https"}


def normalize_rel(path_text: str, base_dir: Path, skill_root: Path) -> str:
    parsed = urlparse(path_text)
    raw_path = unquote(parsed.path)
    resolved = (base_dir / raw_path).resolve()
    try:
        return resolved.relative_to(skill_root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def normalize_manifest_path(path_text: str) -> str:
    path_text = path_text.strip().strip("`'\"")
    if path_text.startswith("assets/"):
        return f"output/{path_text}"
    return path_text


def extract_manifest_paths(brief_path: Path) -> tuple[set[str], str]:
    if not brief_path.exists():
        raise FileNotFoundError(f"Brief file not found: {brief_path}")
    markdown = brief_path.read_text(encoding="utf-8")
    match = MANIFEST_SECTION_RE.search(markdown)
    if not match:
        raise ValueError("Missing ## Asset Lock Manifest section in brief.")
    body = match.group("body")
    paths = {
        normalize_manifest_path(item.group("path"))
        for item in LOCAL_ASSET_RE.finditer(body)
    }
    return paths, body


def extract_html_refs(html_path: Path, skill_root: Path) -> list[tuple[str, str, str]]:
    html = html_path.read_text(encoding="utf-8")
    refs: list[tuple[str, str, str]] = []

    for match in CSS_URL_RE.finditer(html):
        path_text = match.group("path").strip()
        if is_image_ref(path_text) or is_external(path_text):
            refs.append(("css-url", path_text, normalize_rel(path_text, html_path.parent, skill_root) if not is_external(path_text) and not path_text.startswith("data:") else path_text))

    for match in ATTR_RE.finditer(html):
        path_text = match.group("path").strip()
        tag = match.group(0)
        if is_image_ref(path_text) or is_external(path_text):
            source = "avatar-src" if re.search(r"class=['\"][^'\"]*avatar", tag, re.IGNORECASE) else f"{match.group('tag').lower()}-{match.group('attr').lower()}"
            refs.append((source, path_text, normalize_rel(path_text, html_path.parent, skill_root) if not is_external(path_text) and not path_text.startswith("data:") else path_text))

    return refs


def validate(html_path: Path, brief_path: Path, skill_root: Path) -> list[str]:
    locked_paths, manifest_body = extract_manifest_paths(brief_path)
    refs = extract_html_refs(html_path, skill_root)
    errors: list[str] = []

    if not locked_paths:
        errors.append("Asset Lock Manifest contains no local asset paths.")

    for source, original, normalized in refs:
        if original.startswith("data:"):
            continue
        if is_external(original):
            errors.append(f"External image asset is not allowed: {original}")
            continue

        asset_path = skill_root / normalized
        if not asset_path.exists():
            errors.append(f"Referenced asset does not exist: {original} -> {normalized}")

        if normalized not in locked_paths:
            errors.append(f"Asset is referenced but not locked in Asset Lock Manifest: {normalized}")

        if "figma-refs/backgrounds/" in normalized and not re.search(r"^-\s*Background\s*:", manifest_body, re.MULTILINE):
            errors.append("Background asset is used but the manifest has no Background entry.")

        if source == "avatar-src" and not normalized.startswith("figma-refs/components/avatar/"):
            errors.append(f"Avatar image must come from figma-refs/components/avatar/: {normalized}")

    background_refs = [normalized for source, _, normalized in refs if source == "css-url" and "figma-refs/backgrounds/" in normalized]
    for background in background_refs:
        if background not in locked_paths:
            errors.append(f"Background differs from Asset Lock Manifest: {background}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Path to output/<banner-name>.html")
    parser.add_argument("--brief", type=Path, help="Path to output/<banner-name>.brief.md; defaults to matching HTML stem")
    parser.add_argument("--skill-root", type=Path, help="Skill root path; defaults to the HTML grandparent when HTML is in output/")
    args = parser.parse_args()

    html_path = args.html.resolve()
    brief_path = args.brief.resolve() if args.brief else html_path.with_suffix(".brief.md")
    if args.skill_root:
        skill_root = args.skill_root.resolve()
    elif html_path.parent.name == "output":
        skill_root = html_path.parent.parent.resolve()
    else:
        skill_root = Path.cwd().resolve()

    try:
        errors = validate(html_path, brief_path, skill_root)
    except (FileNotFoundError, ValueError) as error:
        print(f"Asset lock check failed:\n- {error}")
        return 1

    if errors:
        print("Asset lock check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Asset lock check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

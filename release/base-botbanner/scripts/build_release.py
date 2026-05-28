#!/usr/bin/env python3
"""Build a clean releasable copy of the Base bot banner skill."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "output",
    "release",
}
EXCLUDED_FILES = {
    ".DS_Store",
    "README.md",
}
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/check_banner_brief.py",
    "scripts/check_banner_ui.py",
    "scripts/check_asset_lock.py",
    "scripts/make_share_html.py",
)


def skill_name(source: Path) -> str:
    skill_md = source / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("'\"")
    return source.name


def should_ignore(path: Path) -> bool:
    if path.name in EXCLUDED_FILES:
        return True
    if path.is_dir() and path.name in EXCLUDED_DIRS:
        return True
    return False


def copy_clean_tree(source: Path, dest: Path, expected_name: str) -> None:
    if dest.exists():
        if dest.name != expected_name or dest.parent.name != "release":
            raise ValueError(f"Refusing to overwrite unexpected destination: {dest}")
        shutil.rmtree(dest)

    for src in source.rglob("*"):
        rel = src.relative_to(source)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if src.name in EXCLUDED_FILES:
            continue
        target = dest / rel
        if src.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def validate_release(dest: Path) -> list[str]:
    errors: list[str] = []
    for required in REQUIRED_FILES:
        if not (dest / required).exists():
            errors.append(f"Missing required file: {required}")

    forbidden = []
    for path in dest.rglob("*"):
        rel = path.relative_to(dest)
        if path.name in EXCLUDED_FILES or any(part in EXCLUDED_DIRS for part in rel.parts):
            forbidden.append(rel.as_posix())
    if forbidden:
        errors.append("Forbidden files or directories copied: " + ", ".join(forbidden[:20]))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1], help="Skill source directory")
    parser.add_argument("--dest", type=Path, help="Destination directory; defaults to <source>/release/<skill-name>")
    args = parser.parse_args()

    source = args.source.resolve()
    expected_name = skill_name(source)
    dest = args.dest.resolve() if args.dest else source / "release" / expected_name

    try:
        copy_clean_tree(source, dest, expected_name)
    except ValueError as error:
        print(f"Release build failed:\n- {error}")
        return 1

    errors = validate_release(dest)
    if errors:
        print("Release build failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

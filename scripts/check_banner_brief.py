#!/usr/bin/env python3
"""Validate the required planning brief for Base bot banner outputs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "User Choices",
    "Visual Strategy",
    "Source UI Audit",
    "Temporary Module Rule",
    "Abstraction Plan",
    "UI Detail Constraints",
    "Asset Lock Manifest",
    "Implementation Notes",
    "Verification",
)

HEADING_RE = re.compile(r"^(?P<level>#{2,3})\s+(?P<title>.+?)\s*$", re.MULTILINE)


def normalize_heading(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip().lower())
    return re.sub(r"[:：]\s*$", "", value)


def extract_sections(markdown: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(markdown))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = normalize_heading(match.group("title"))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[title] = markdown[start:end].strip()
    return sections


def validate(path: Path) -> list[str]:
    if not path.exists():
        return [f"Brief file does not exist: {path}"]
    if path.suffix != ".md":
        return [f"Brief file must be Markdown: {path}"]

    markdown = path.read_text(encoding="utf-8")
    sections = extract_sections(markdown)
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        key = normalize_heading(section)
        body = sections.get(key)
        if body is None:
            errors.append(f"Missing required section: ## {section}")
        elif not body:
            errors.append(f"Required section is empty: ## {section}")

    verification = sections.get(normalize_heading("Verification"), "")
    if verification and "check_banner_brief.py" not in verification:
        errors.append("Verification must mention check_banner_brief.py.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Path to output/<banner-name>.brief.md")
    args = parser.parse_args()

    errors = validate(args.brief)
    if errors:
        print("Brief check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Brief check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

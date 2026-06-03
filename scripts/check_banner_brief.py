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
    "Source UI Fidelity",
    "Temporary Module Rule",
    "Abstraction Plan",
    "UI Detail Constraints",
    "Asset Lock Manifest",
    "Implementation Notes",
    "Verification",
)

HEADING_RE = re.compile(r"^(?P<level>#{2,3})\s+(?P<title>.+?)\s*$", re.MULTILINE)
SPACING_TERMS_RE = re.compile(
    r"(spacing|padding|gap|margin|inset|rhythm|whitespace|间距|内边距|外边距|留白|视觉节奏)",
    re.IGNORECASE,
)


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

    source_fidelity = sections.get(normalize_heading("Source UI Fidelity"), "")
    ui_constraints = sections.get(normalize_heading("UI Detail Constraints"), "")
    if source_fidelity or ui_constraints:
        spacing_context = f"{source_fidelity}\n{ui_constraints}"
        if not SPACING_TERMS_RE.search(spacing_context):
            errors.append("Source UI Fidelity / UI Detail Constraints must record source spacing constraints.")

    user_choices = sections.get(normalize_heading("User Choices"), "")
    if user_choices:
        required_choice_fields = (
            "Background",
            "Layout option",
            "Layout default",
            "Abstraction default",
            "Defaults used",
        )
        for field in required_choice_fields:
            if not re.search(rf"^\s*-\s*{re.escape(field)}\s*[:：]\s*\S+", user_choices, re.MULTILINE):
                errors.append(f"User Choices must include a non-empty '- {field}:' entry.")

        layout_match = re.search(r"^\s*-\s*Layout option\s*[:：]\s*([ABC])\b", user_choices, re.MULTILINE | re.IGNORECASE)
        if not layout_match:
            errors.append("User Choices must include '- Layout option: A|B|C'.")

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

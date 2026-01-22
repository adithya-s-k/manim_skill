#!/usr/bin/env python3
"""Test script for scenes.md"""
from pathlib import Path
from test_utils import test_markdown_file

if __name__ == "__main__":
    skills_dir = Path(__file__).parent.parent / "skills" / "manimce-best-practices" / "rules"
    markdown_file = skills_dir / "scenes.md"

    if not markdown_file.exists():
        print(f"Error: {markdown_file} not found")
        exit(1)

    passed, failed, skipped = test_markdown_file(markdown_file)

    if failed > 0:
        exit(1)

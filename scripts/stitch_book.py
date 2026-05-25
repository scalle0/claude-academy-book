#!/usr/bin/env python3
"""
stitch_book.py
==============

Pipeline step 10: assemble all drafted chapters into a single book.

Reads all chapters/*/chapter.md files, orders them according to
book_index.json (or by slug alphabetically as fallback), and composes
a single book/book.md with frontmatter, table of contents, chapters
with consistent heading levels, and a glossary.

Input
-----
- chapters/*/chapter.md           (drafted chapters from step 6)
- chapters/book_index.json        (chapter order and metadata)
- chapters/*/entities.json        (for glossary assembly)

Output
------
- book/book.md                    (the complete book, ready for Claude in Design)

Usage
-----
    # Stitch all drafted chapters
    python scripts/stitch_book.py

    # Custom output path
    python scripts/stitch_book.py --out book/my_book.md

    # Custom chapter order (comma-separated slugs)
    python scripts/stitch_book.py --order slug1,slug2,slug3

    # Exclude specific chapters
    python scripts/stitch_book.py --exclude slug1,slug2

    # Include only chapters that pass validation
    python scripts/stitch_book.py --validated-only

Dependencies
------------
Python 3.11+ standard library only.

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


# ----------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------

def load_book_index(chapters_root: Path) -> dict | None:
    """Load book_index.json if it exists."""
    path = chapters_root / "book_index.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"WARNING: corrupt book_index.json: {exc}", file=sys.stderr)
        return None


def load_metadata(chapter_dir: Path) -> dict:
    """Load metadata.yaml without PyYAML dependency."""
    meta_path = chapter_dir / "metadata.yaml"
    if not meta_path.exists():
        return {}
    metadata: dict[str, str] = {}
    for line in meta_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip('"').strip("'")
        metadata[key.strip()] = value
    return metadata


def load_entities(chapter_dir: Path) -> dict:
    """Load entities.json for glossary building."""
    path = chapter_dir / "entities.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def find_drafted_chapters(chapters_root: Path) -> list[Path]:
    """Find all chapter directories that have a chapter.md."""
    return sorted([
        d for d in chapters_root.iterdir()
        if d.is_dir()
        and not d.name.startswith(".")
        and (d / "chapter.md").exists()
    ])


# ----------------------------------------------------------------------
# Chapter ordering
# ----------------------------------------------------------------------

def order_chapters(
    chapter_dirs: list[Path],
    book_index: dict | None,
    explicit_order: list[str] | None,
    exclude: set[str],
) -> list[Path]:
    """
    Determine chapter order. Priority:
    1. Explicit --order if given
    2. book_index.json chapter list order
    3. Alphabetical by slug
    """
    # Apply exclusions
    chapter_dirs = [d for d in chapter_dirs if d.name not in exclude]

    if explicit_order:
        slug_to_dir = {d.name: d for d in chapter_dirs}
        ordered = []
        for slug in explicit_order:
            if slug in slug_to_dir:
                ordered.append(slug_to_dir[slug])
            else:
                print(f"WARNING: --order slug '{slug}' has no chapter.md, skipping")
        # Append any chapters not in the explicit order
        remaining = [d for d in chapter_dirs if d not in ordered]
        return ordered + remaining

    if book_index and "chapters" in book_index:
        index_slugs = [ch["slug"] for ch in book_index["chapters"]]
        slug_to_dir = {d.name: d for d in chapter_dirs}
        ordered = []
        for slug in index_slugs:
            if slug in slug_to_dir:
                ordered.append(slug_to_dir[slug])
        # Append any drafted chapters not in the index
        remaining = [d for d in chapter_dirs if d not in ordered]
        return ordered + remaining

    return chapter_dirs  # already sorted alphabetically


# ----------------------------------------------------------------------
# Heading level adjustment
# ----------------------------------------------------------------------

def adjust_heading_levels(content: str, chapter_num: int) -> str:
    """
    Adjust heading levels so each chapter fits into the book structure.

    Book structure:
    - H1: book title (only one, in frontmatter)
    - H2: chapter title (## Chapter N: Title)
    - H3+: section headings within the chapter

    The chapter.md files use H1 for the chapter title and H2 for sections.
    This function shifts everything down one level.
    """
    lines = content.split("\n")
    adjusted = []
    for line in lines:
        if line.startswith("#"):
            # Count leading hashes
            match = re.match(r"^(#+)\s*(.*)", line)
            if match:
                hashes = match.group(1)
                text = match.group(2)
                # Shift down one level (H1 -> H2, H2 -> H3, etc.)
                new_level = len(hashes) + 1
                # Cap at H6
                new_level = min(new_level, 6)
                adjusted.append(f"{'#' * new_level} {text}")
                continue
        adjusted.append(line)
    return "\n".join(adjusted)


def strip_frontmatter_comment(content: str) -> tuple[str, str]:
    """
    Strip the HTML comment frontmatter block from chapter.md.
    Returns (frontmatter, body).
    """
    match = re.match(r"^\s*<!--\s*(.*?)-->\s*", content, flags=re.S)
    if match:
        frontmatter = match.group(1).strip()
        body = content[match.end():].strip()
        return frontmatter, body
    return "", content.strip()


def strip_audit_sections(content: str) -> str:
    """
    Remove the appended Editor queries and Fidelity audit sections
    from the chapter content. These are useful during drafting but
    not part of the final book.
    """
    # Remove ## Editor queries and everything after it if ## Fidelity audit follows
    # Or remove each independently
    patterns = [
        r"\n## Editor queries\s*\n.*?(?=\n## |\Z)",
        r"\n## Fidelity audit\s*\n.*?(?=\n## |\Z)",
    ]
    for pattern in patterns:
        content = re.sub(pattern, "", content, flags=re.S)
    return content.strip()


# ----------------------------------------------------------------------
# Glossary
# ----------------------------------------------------------------------

def build_glossary(chapter_dirs: list[Path]) -> str:
    """
    Build a glossary from entities across all chapters.
    Groups entities by category, deduplicates, and sorts.
    """
    all_entities: dict[str, set[str]] = defaultdict(set)

    for d in chapter_dirs:
        entities = load_entities(d)
        for category, items in entities.items():
            if isinstance(items, list):
                for item in items:
                    all_entities[category].add(item)

    if not any(all_entities.values()):
        return ""

    # Category display order and labels
    category_labels = [
        ("products", "Products and tools"),
        ("features", "Features and capabilities"),
        ("concepts", "Technical concepts"),
        ("people", "People"),
        ("papers_or_docs", "Papers and documentation"),
    ]

    lines = [
        "## Glossary",
        "",
        "Entities referenced across all chapters.",
        "",
    ]

    for cat_key, cat_label in category_labels:
        items = all_entities.get(cat_key, set())
        if not items:
            continue
        lines.append(f"### {cat_label}")
        lines.append("")
        for item in sorted(items):
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Book assembly
# ----------------------------------------------------------------------

def stitch_book(
    chapter_dirs: list[Path],
    output_path: Path,
    book_title: str = "Claude Academy: A Technical Reference",
    author: str = "Steven Callens",
) -> None:
    """Assemble the final book from drafted chapters."""

    if not chapter_dirs:
        sys.exit("No drafted chapters found (no chapter.md files).")

    print(f"Stitching {len(chapter_dirs)} chapters into {output_path}")

    parts: list[str] = []

    # 1. YAML frontmatter
    parts.append(f"""---
title: "{book_title}"
author: "{author}"
date: "{date.today().isoformat()}"
chapters: {len(chapter_dirs)}
source: "Anthropic Claude Academy YouTube playlist"
---""")

    # 2. Title
    parts.append(f"\n# {book_title}\n")
    parts.append(f"*{author} | Generated {date.today().isoformat()}*\n")
    parts.append(
        "This book is a personal technical reference built from transcripts "
        "of Anthropic's Claude Academy talks, enriched with current "
        "documentation from docs.anthropic.com.\n"
    )

    # 3. Table of contents
    toc_lines = ["## Table of contents\n"]
    for i, d in enumerate(chapter_dirs, 1):
        metadata = load_metadata(d)
        title = metadata.get("title", d.name)
        # Create an anchor-friendly slug
        anchor = re.sub(r"[^a-z0-9\s-]", "", title.lower())
        anchor = re.sub(r"\s+", "-", anchor.strip())
        toc_lines.append(f"{i}. [{title}](#{anchor})")
    toc_lines.append("")
    toc_lines.append("---\n")
    parts.append("\n".join(toc_lines))

    # 4. Chapters
    for i, d in enumerate(chapter_dirs, 1):
        metadata = load_metadata(d)
        title = metadata.get("title", d.name)
        chapter_path = d / "chapter.md"
        raw_content = chapter_path.read_text(encoding="utf-8")

        # Strip frontmatter comment and audit sections
        _frontmatter, body = strip_frontmatter_comment(raw_content)
        body = strip_audit_sections(body)

        # Adjust heading levels
        body = adjust_heading_levels(body, i)

        # Add chapter header
        parts.append(f"## Chapter {i}: {title}\n")

        source = metadata.get("url", "")
        upload_date = metadata.get("upload_date", "")
        if source or upload_date:
            meta_line = "*"
            if source:
                meta_line += f"Source: {source}"
            if upload_date:
                if source:
                    meta_line += f" | "
                meta_line += f"Date: {upload_date}"
            meta_line += "*\n"
            parts.append(meta_line)

        parts.append(body)
        parts.append("\n---\n")

        word_count = len(body.split())
        print(f"  Chapter {i}: {title} ({word_count:,} words)")

    # 5. Glossary
    glossary = build_glossary(chapter_dirs)
    if glossary:
        parts.append(glossary)

    # 6. Colophon
    parts.append("## Colophon\n")
    parts.append(
        "This book was generated from YouTube transcripts using a pipeline of:\n\n"
        "- **Whisper large-v3** for audio transcription\n"
        "- **Claude** for summary extraction, enrichment, and chapter drafting\n"
        "- **docs.anthropic.com** for current feature documentation\n\n"
        f"Generated on {date.today().isoformat()}.\n"
    )

    # Write the book
    book_content = "\n".join(parts) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(book_content, encoding="utf-8")

    total_words = len(book_content.split())
    print(f"\nBook written to: {output_path}")
    print(f"  Total words: {total_words:,}")
    print(f"  Total chars: {len(book_content):,}")
    print(f"  Chapters: {len(chapter_dirs)}")


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Pipeline step 10: stitch drafted chapters into book/book.md."
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("book/book.md"),
        help="Output path for the stitched book. Default: book/book.md",
    )
    ap.add_argument(
        "--chapters-dir",
        type=Path,
        default=Path("chapters"),
        help="Root chapters directory. Default: ./chapters",
    )
    ap.add_argument(
        "--order",
        default=None,
        help="Comma-separated list of slugs to define chapter order.",
    )
    ap.add_argument(
        "--exclude",
        default="",
        help="Comma-separated list of slugs to exclude from the book.",
    )
    ap.add_argument(
        "--title",
        default="Claude Academy: A Technical Reference",
        help="Book title for the frontmatter.",
    )
    ap.add_argument(
        "--author",
        default="Steven Callens",
        help="Author name for the frontmatter.",
    )
    ap.add_argument(
        "--validated-only",
        action="store_true",
        help="Only include chapters that have a complete corpus.",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    chapters_root = args.chapters_dir
    if not chapters_root.is_dir():
        sys.exit(f"Chapters directory not found: {chapters_root}")

    # Find drafted chapters
    chapter_dirs = find_drafted_chapters(chapters_root)
    if not chapter_dirs:
        sys.exit(
            f"No drafted chapters found in {chapters_root}.\n"
            f"Run the talk-to-chapter skill to draft chapters first."
        )

    # Optional: filter to validated-only
    if args.validated_only:
        validated = []
        required = ["summary.md", "entities.json", "enrichment.md", "chapter.md"]
        for d in chapter_dirs:
            if all((d / f).exists() for f in required):
                validated.append(d)
            else:
                print(f"  Excluding {d.name}: incomplete corpus")
        chapter_dirs = validated

    # Load book index for ordering
    book_index = load_book_index(chapters_root)

    # Parse ordering options
    explicit_order = None
    if args.order:
        explicit_order = [s.strip() for s in args.order.split(",") if s.strip()]

    exclude = set()
    if args.exclude:
        exclude = {s.strip() for s in args.exclude.split(",") if s.strip()}

    # Order chapters
    chapter_dirs = order_chapters(chapter_dirs, book_index, explicit_order, exclude)

    if not chapter_dirs:
        sys.exit("No chapters remaining after filtering.")

    print(f"Found {len(chapter_dirs)} drafted chapters.")

    # Stitch
    stitch_book(
        chapter_dirs=chapter_dirs,
        output_path=args.out,
        book_title=args.title,
        author=args.author,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")

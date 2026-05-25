#!/usr/bin/env python3
"""
overlap_check.py
================

Pipeline step 5: detect entity and concept overlap across chapters.

For each chapter, compares its entities.json against all other chapters
to identify shared concepts, features, and products. Produces an
overlap_report.md per chapter that the talk-to-chapter skill uses to
decide what each chapter should own vs defer to another chapter.

Also initializes or updates book_index.json, the top-level index that
tracks what each chapter covers.

Input
-----
- chapters/<slug>/entities.json   (from step 2, for all chapters)
- chapters/<slug>/summary.md      (for context in the report)
- chapters/<slug>/metadata.yaml   (for title/date)
- book_index.json                 (created if it does not exist)

Output
------
- chapters/<slug>/overlap_report.md   (per chapter)
- chapters/book_index.json            (updated)

Usage
-----
    # Run overlap check for all chapters
    python scripts/overlap_check.py

    # Single chapter against all others
    python scripts/overlap_check.py chapters/beyond-the-basics-with-claude-code

    # Force re-run (overwrite existing reports)
    python scripts/overlap_check.py --force

Dependencies
------------
Python 3.11+ standard library only. No API calls, no external packages.

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


# ----------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------

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
    """Load entities.json for a chapter."""
    path = chapter_dir / "entities.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def load_all_chapters(chapters_root: Path) -> list[dict]:
    """
    Load metadata and entities for all chapters.
    Returns a list of chapter info dicts.
    """
    chapters = []
    for d in sorted(chapters_root.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        entities = load_entities(d)
        if not entities:
            continue
        metadata = load_metadata(d)
        chapters.append({
            "slug": d.name,
            "dir": d,
            "title": metadata.get("title", d.name),
            "upload_date": metadata.get("upload_date", ""),
            "entities": entities,
        })
    return chapters


# ----------------------------------------------------------------------
# Overlap analysis
# ----------------------------------------------------------------------

def build_entity_index(chapters: list[dict]) -> dict[str, dict[str, list[str]]]:
    """
    Build an inverted index: entity -> {category -> [slugs]}.
    This tells us, for each entity, which chapters mention it and in
    which category.
    """
    index: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for ch in chapters:
        for category, entities in ch["entities"].items():
            if not isinstance(entities, list):
                continue
            for entity in entities:
                entity_lower = entity.lower()
                index[entity_lower][category].append(ch["slug"])
                # Store the canonical casing from first encounter
                if "_canonical" not in index[entity_lower]:
                    index[entity_lower]["_canonical"] = entity
    return dict(index)


def compute_overlap(
    target_slug: str,
    target_entities: dict,
    entity_index: dict[str, dict[str, list[str]]],
    all_chapters: list[dict],
) -> dict:
    """
    Compute overlap between one chapter and all others.

    Returns:
    {
        "shared_entities": {
            "entity_name": {
                "categories": ["products", "features"],
                "shared_with": ["slug1", "slug2"],
            }
        },
        "overlap_by_chapter": {
            "slug1": {
                "title": "...",
                "shared": ["entity1", "entity2"],
                "overlap_score": 5,
            }
        },
        "unique_entities": ["entity3", "entity4"],
    }
    """
    # Collect all entities this chapter mentions
    my_entities: set[str] = set()
    for category, entities in target_entities.items():
        if isinstance(entities, list):
            for e in entities:
                my_entities.add(e.lower())

    shared_entities: dict[str, dict] = {}
    unique_entities: list[str] = []
    overlap_by_chapter: dict[str, dict] = {}

    # Title lookup
    title_map = {ch["slug"]: ch["title"] for ch in all_chapters}

    for entity_lower in sorted(my_entities):
        entry = entity_index.get(entity_lower, {})
        canonical = entry.get("_canonical", entity_lower)

        # Collect all other slugs that mention this entity
        other_slugs: set[str] = set()
        categories: set[str] = set()
        for cat, slugs in entry.items():
            if cat == "_canonical":
                continue
            categories.add(cat)
            for s in slugs:
                if s != target_slug:
                    other_slugs.add(s)

        if other_slugs:
            shared_entities[canonical] = {
                "categories": sorted(categories),
                "shared_with": sorted(other_slugs),
            }
            # Update per-chapter overlap
            for s in other_slugs:
                if s not in overlap_by_chapter:
                    overlap_by_chapter[s] = {
                        "title": title_map.get(s, s),
                        "shared": [],
                        "overlap_score": 0,
                    }
                overlap_by_chapter[s]["shared"].append(canonical)
                overlap_by_chapter[s]["overlap_score"] += 1
        else:
            unique_entities.append(canonical)

    # Sort by overlap score descending
    overlap_by_chapter = dict(
        sorted(overlap_by_chapter.items(),
               key=lambda x: x[1]["overlap_score"], reverse=True)
    )

    return {
        "shared_entities": shared_entities,
        "overlap_by_chapter": overlap_by_chapter,
        "unique_entities": sorted(unique_entities),
    }


# ----------------------------------------------------------------------
# Overlap report generation
# ----------------------------------------------------------------------

def generate_overlap_report(
    slug: str,
    title: str,
    overlap: dict,
    all_chapters: list[dict],
) -> str:
    """Generate the overlap_report.md content for one chapter."""
    shared = overlap["shared_entities"]
    by_chapter = overlap["overlap_by_chapter"]
    unique = overlap["unique_entities"]

    lines = [
        f"# Overlap report: {title}",
        "",
        f"Chapter: `{slug}`",
        f"Compared against: {len(all_chapters) - 1} other chapters",
        "",
    ]

    # Summary stats
    n_shared = len(shared)
    n_unique = len(unique)
    n_overlapping_chapters = len(by_chapter)
    lines.extend([
        "## Summary",
        "",
        f"- **{n_shared}** entities shared with other chapters",
        f"- **{n_unique}** entities unique to this chapter",
        f"- **{n_overlapping_chapters}** chapters have overlapping entities",
        "",
    ])

    # Unique entities (this chapter's distinctive content)
    if unique:
        lines.extend([
            "## Unique to this chapter",
            "",
            "These entities are not mentioned in any other chapter. They are",
            "strong candidates for in-depth coverage here.",
            "",
        ])
        for e in unique:
            lines.append(f"- {e}")
        lines.append("")

    # Most overlapping chapters
    if by_chapter:
        lines.extend([
            "## Overlap by chapter",
            "",
            "Chapters with the most shared entities appear first. High overlap",
            "means the drafting skill should decide which chapter owns which",
            "concepts, and insert cross-references for the rest.",
            "",
        ])
        for other_slug, info in by_chapter.items():
            score = info["overlap_score"]
            other_title = info["title"]
            shared_list = info["shared"]
            lines.append(f"### {other_title}")
            lines.append(f"")
            lines.append(f"Slug: `{other_slug}` | Shared entities: **{score}**")
            lines.append("")
            for e in sorted(shared_list):
                lines.append(f"- {e}")
            lines.append("")

    # Shared entity detail
    if shared:
        lines.extend([
            "## Shared entity detail",
            "",
            "For each shared entity, which chapters also mention it.",
            "",
        ])
        for entity, info in sorted(shared.items()):
            others = info["shared_with"]
            cats = ", ".join(info["categories"])
            lines.append(f"- **{entity}** ({cats}): also in {', '.join(f'`{s}`' for s in others)}")
        lines.append("")

    # Guidance for the drafting skill
    lines.extend([
        "## Drafting guidance",
        "",
        "When drafting this chapter:",
        "",
        "1. **Own** the unique entities listed above. Cover them in depth.",
        "2. For shared entities with high-overlap chapters, decide:",
        "   - Does this chapter provide the primary treatment? If yes, own it.",
        "   - Does another chapter cover it better? If yes, summarise briefly",
        "     and add a cross-reference: \"see Chapter: <title>\".",
        "3. The overlap score is a rough guide. Two chapters sharing 2 generic",
        "   entities (e.g. \"Claude\", \"tokens\") is not meaningful overlap.",
        "   Two chapters sharing 5+ specific features or concepts is.",
        "",
    ])

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Book index
# ----------------------------------------------------------------------

def build_book_index(chapters: list[dict], overlap_data: dict) -> dict:
    """
    Build or update the book_index.json from entity data.

    This is a preliminary index based on entities.json. The talk-to-chapter
    skill updates it with richer data (covers_in_depth, mentions_only,
    code_examples) after drafting.
    """
    index = {"chapters": []}

    for ch in chapters:
        slug = ch["slug"]
        entities = ch["entities"]
        overlap = overlap_data.get(slug, {})
        unique = overlap.get("unique_entities", [])

        # All entities as a flat list
        all_entities = set()
        for cat_list in entities.values():
            if isinstance(cat_list, list):
                all_entities.update(cat_list)

        entry = {
            "slug": slug,
            "title": ch["title"],
            "source": f"Claude Academy talk, {ch.get('upload_date', 'date unknown')}",
            "covers_in_depth": unique[:10],  # preliminary; skill refines this
            "mentions_only": [],              # populated by skill after drafting
            "entities": sorted(all_entities),
            "code_examples": [],              # populated by skill after drafting
        }
        index["chapters"].append(entry)

    return index


# ----------------------------------------------------------------------
# Processing
# ----------------------------------------------------------------------

def process_all(
    chapters_root: Path, force: bool, target_slug: str | None
) -> None:
    """Run overlap check across all chapters."""
    chapters = load_all_chapters(chapters_root)

    if not chapters:
        sys.exit(f"No chapters with entities.json found in {chapters_root}")

    print(f"Loaded {len(chapters)} chapters with entities.")

    # Build the entity index across all chapters
    entity_index = build_entity_index(chapters)
    total_entities = len(entity_index)
    print(f"Entity index: {total_entities} unique entities across all chapters.")

    # Compute overlap for each chapter
    overlap_data: dict[str, dict] = {}
    for ch in chapters:
        overlap_data[ch["slug"]] = compute_overlap(
            target_slug=ch["slug"],
            target_entities=ch["entities"],
            entity_index=entity_index,
            all_chapters=chapters,
        )

    # Generate reports
    if target_slug:
        # Single chapter mode
        targets = [ch for ch in chapters if ch["slug"] == target_slug]
        if not targets:
            sys.exit(f"Chapter not found: {target_slug}")
    else:
        targets = chapters

    n_written = 0
    for ch in targets:
        slug = ch["slug"]
        report_path = ch["dir"] / "overlap_report.md"

        if not force and report_path.exists():
            print(f"  SKIP {slug}: already has overlap_report.md (use --force)")
            continue

        overlap = overlap_data[slug]
        report = generate_overlap_report(
            slug=slug,
            title=ch["title"],
            overlap=overlap,
            all_chapters=chapters,
        )
        report_path.write_text(report, encoding="utf-8")

        n_shared = len(overlap["shared_entities"])
        n_unique = len(overlap["unique_entities"])
        n_overlap_ch = len(overlap["overlap_by_chapter"])
        print(
            f"  {slug}: {n_shared} shared, {n_unique} unique, "
            f"overlaps with {n_overlap_ch} chapters"
        )
        n_written += 1

    print(f"\nWrote {n_written} overlap reports.")

    # Build/update book_index.json
    index_path = chapters_root / "book_index.json"
    book_index = build_book_index(chapters, overlap_data)
    index_path.write_text(
        json.dumps(book_index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {index_path} ({len(book_index['chapters'])} chapters).")


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Pipeline step 5: detect entity overlap across chapters "
            "and generate overlap reports."
        )
    )
    ap.add_argument(
        "chapter_dir",
        nargs="?",
        type=Path,
        default=None,
        help=(
            "Path to a single chapter directory. If given, only generates "
            "the report for that chapter (but still compares against all)."
        ),
    )
    ap.add_argument(
        "--chapters-dir",
        type=Path,
        default=Path("chapters"),
        help="Root chapters directory. Default: ./chapters",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing overlap_report.md files.",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    target_slug = None
    if args.chapter_dir:
        if not args.chapter_dir.is_dir():
            sys.exit(f"Not a directory: {args.chapter_dir}")
        target_slug = args.chapter_dir.name

    process_all(
        chapters_root=args.chapters_dir,
        force=args.force,
        target_slug=target_slug,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")

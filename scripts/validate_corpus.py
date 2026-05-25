#!/usr/bin/env python3
"""
validate_corpus.py
==================

Pipeline step 4: validate that each chapter's corpus is complete and
ready for drafting.

Checks every chapter directory for the required outputs of steps 1-3.
Reports what is present, what is missing, and what looks suspicious
(e.g. empty files, tiny summaries). Gives a clear ready/not-ready
verdict per chapter.

Usage
-----
    # Validate all chapters
    python scripts/validate_corpus.py

    # Validate one chapter
    python scripts/validate_corpus.py chapters/beyond-the-basics-with-claude-code

    # Strict mode: treat warnings as failures
    python scripts/validate_corpus.py --strict

    # JSON output for programmatic use
    python scripts/validate_corpus.py --json

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ----------------------------------------------------------------------
# Corpus requirements
# ----------------------------------------------------------------------

# Required files: must exist and be non-empty for the chapter to be
# considered ready for drafting.
REQUIRED_FILES = [
    ("source/transcript.txt", "step 1: transcription"),
    ("metadata.yaml",         "step 1: transcription"),
    ("summary.md",            "step 2: summarise"),
    ("entities.json",         "step 2: summarise"),
    ("quotes.md",             "step 2: summarise"),
    ("enrichment.md",         "step 3: enrich"),
]

# Minimum file sizes (bytes) below which a file is flagged as suspicious.
# These are generous minimums; a real file should be much larger.
MIN_SIZES = {
    "source/transcript.txt": 500,    # even a short talk produces > 500 chars
    "summary.md":            100,
    "entities.json":         20,     # at minimum: {}
    "quotes.md":             50,
    "enrichment.md":         50,
    "metadata.yaml":         50,
}

# Optional files: nice to have, reported but not required.
OPTIONAL_FILES = [
    ("overlap_report.md",    "step 5: overlap check"),
    ("chapter.md",           "step 6: drafted chapter"),
    ("audit.md",             "step 7: fidelity audit"),
]


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

def validate_chapter(chapter_dir: Path, strict: bool = False) -> dict:
    """
    Validate a single chapter's corpus. Returns a result dict:
    {
        "slug": str,
        "ready": bool,
        "present": [str],
        "missing": [str],
        "warnings": [str],
        "optional_present": [str],
        "optional_missing": [str],
    }
    """
    slug = chapter_dir.name
    present: list[str] = []
    missing: list[str] = []
    warnings: list[str] = []
    optional_present: list[str] = []
    optional_missing: list[str] = []

    # Check required files
    for rel_path, step_label in REQUIRED_FILES:
        full_path = chapter_dir / rel_path
        if not full_path.exists():
            missing.append(f"{rel_path} ({step_label})")
            continue

        size = full_path.stat().st_size
        if size == 0:
            missing.append(f"{rel_path} (exists but empty)")
            continue

        present.append(rel_path)

        # Size check
        min_size = MIN_SIZES.get(rel_path, 0)
        if size < min_size:
            warnings.append(
                f"{rel_path}: only {size} bytes (expected >= {min_size})"
            )

    # Validate entities.json is parseable
    entities_path = chapter_dir / "entities.json"
    if entities_path.exists() and entities_path.stat().st_size > 0:
        try:
            data = json.loads(entities_path.read_text(encoding="utf-8"))
            expected_keys = {"products", "features", "concepts", "people", "papers_or_docs"}
            actual_keys = set(data.keys())
            missing_keys = expected_keys - actual_keys
            if missing_keys:
                warnings.append(
                    f"entities.json: missing keys {missing_keys}"
                )
            total_entities = sum(len(v) for v in data.values() if isinstance(v, list))
            if total_entities == 0:
                warnings.append("entities.json: no entities extracted")
        except json.JSONDecodeError as exc:
            missing.append(f"entities.json (corrupt JSON: {exc})")
            if "entities.json" in present:
                present.remove("entities.json")

    # Check optional files
    for rel_path, step_label in OPTIONAL_FILES:
        full_path = chapter_dir / rel_path
        if full_path.exists() and full_path.stat().st_size > 0:
            optional_present.append(rel_path)
        else:
            optional_missing.append(f"{rel_path} ({step_label})")

    ready = len(missing) == 0
    if strict and warnings:
        ready = False

    return {
        "slug": slug,
        "ready": ready,
        "present": present,
        "missing": missing,
        "warnings": warnings,
        "optional_present": optional_present,
        "optional_missing": optional_missing,
    }


def print_report(results: list[dict]) -> None:
    """Print a human-readable validation report."""
    n_ready = sum(1 for r in results if r["ready"])
    n_total = len(results)

    print(f"\n{'=' * 60}")
    print(f"Corpus validation: {n_ready}/{n_total} chapters ready for drafting")
    print(f"{'=' * 60}\n")

    # Ready chapters (brief)
    ready = [r for r in results if r["ready"]]
    if ready:
        print(f"READY ({len(ready)}):")
        for r in ready:
            warn_note = f"  ({len(r['warnings'])} warnings)" if r["warnings"] else ""
            optional_note = ""
            if r["optional_present"]:
                optional_note = f"  [+{', '.join(r['optional_present'])}]"
            print(f"  {r['slug']}{warn_note}{optional_note}")
        print()

    # Not ready chapters (detailed)
    not_ready = [r for r in results if not r["ready"]]
    if not_ready:
        print(f"NOT READY ({len(not_ready)}):")
        for r in not_ready:
            print(f"\n  {r['slug']}:")
            for m in r["missing"]:
                print(f"    MISSING: {m}")
            for w in r["warnings"]:
                print(f"    WARNING: {w}")
        print()

    # Warnings on ready chapters
    warned = [r for r in ready if r["warnings"]]
    if warned:
        print(f"WARNINGS on ready chapters:")
        for r in warned:
            print(f"\n  {r['slug']}:")
            for w in r["warnings"]:
                print(f"    {w}")
        print()

    # Summary of what needs running
    if not_ready:
        steps_needed: dict[str, int] = {}
        for r in not_ready:
            for m in r["missing"]:
                # Extract step label from "file (step N: label)"
                if "(" in m:
                    step = m.split("(")[-1].rstrip(")")
                    steps_needed[step] = steps_needed.get(step, 0) + 1

        if steps_needed:
            print("To fix, run:")
            for step, count in sorted(steps_needed.items()):
                if "step 2" in step:
                    print(f"  python scripts/extract_summary.py --all --use-claude  ({count} chapters)")
                elif "step 3" in step:
                    print(f"  python scripts/enrich.py --all  ({count} chapters)")
                elif "step 1" in step:
                    print(f"  python scripts/transcribe_playlist.py ...  ({count} chapters)")
                else:
                    print(f"  {step}: {count} chapters")
            print()


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Pipeline step 4: validate chapter corpora are complete."
    )
    ap.add_argument(
        "chapter_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Path to a single chapter directory to validate.",
    )
    ap.add_argument(
        "--chapters-dir",
        type=Path,
        default=Path("chapters"),
        help="Root chapters directory. Default: ./chapters",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (chapter not ready if any warnings).",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON instead of human-readable report.",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    if args.chapter_dir:
        if not args.chapter_dir.is_dir():
            sys.exit(f"Not a directory: {args.chapter_dir}")
        dirs = [args.chapter_dir]
    else:
        chapters_root = args.chapters_dir
        if not chapters_root.is_dir():
            sys.exit(f"Chapters directory not found: {chapters_root}")
        dirs = sorted([
            d for d in chapters_root.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ])

    if not dirs:
        sys.exit("No chapter directories found.")

    results = [validate_chapter(d, strict=args.strict) for d in dirs]

    if args.json_output:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)

    # Exit code: 0 if all ready, 1 if any not ready
    if any(not r["ready"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")

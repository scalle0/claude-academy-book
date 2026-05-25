#!/usr/bin/env python3
"""
enrich.py
=========

Pipeline step 3: enrich chapter entities with current information from
docs.claude.com.

Speakers describe features as they existed at recording time, which may
be months out of date. This script fetches the current documentation for
each Anthropic-specific entity and produces enrichment notes that flag
what has changed so the chapter can use current terminology.

Input
-----
- chapters/<slug>/entities.json   (from step 2)
- chapters/<slug>/metadata.yaml   (for talk date context)

Output
------
- chapters/<slug>/enrichment.md

How it works
------------
1. Read entities.json and filter for Anthropic products/features.
2. Map each entity to known docs.claude.com URLs.
3. Fetch those pages (HTML -> text extraction).
4. Send the fetched documentation + entity list to Claude API.
5. Claude compares what the docs say now vs what a talk from that date
   would have described, and writes enrichment.md.

Usage
-----
    # Single chapter
    python scripts/enrich.py chapters/beyond-the-basics-with-claude-code

    # All chapters
    python scripts/enrich.py --all

    # Force re-enrichment
    python scripts/enrich.py --all --force

Dependencies
------------
- requests (pip install requests)
- anthropic (pip install anthropic)

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

# Load .env from project root (for ANTHROPIC_YT_CLAUDE_LONDON_API_KEY)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass  # python-dotenv is optional; env vars can be set manually


# ----------------------------------------------------------------------
# Entity-to-URL mapping
# ----------------------------------------------------------------------

# Maps Anthropic-specific entities to their docs.claude.com pages.
# Multiple URLs per entity when the topic spans several doc pages.
# Only Anthropic products/features are mapped; generic concepts
# (e.g. "RAG", "embeddings") are not enriched from Anthropic docs.

ENTITY_URL_MAP: dict[str, list[str]] = {
    # Products
    "Claude Code": [
        "https://docs.anthropic.com/en/docs/claude-code/overview",
    ],
    "Claude Desktop": [
        "https://docs.anthropic.com/en/docs/claude-desktop",
    ],
    "Claude": [
        "https://docs.anthropic.com/en/docs/about-claude/models",
    ],
    "Anthropic API": [
        "https://docs.anthropic.com/en/api/getting-started",
    ],
    "Anthropic Console": [
        "https://docs.anthropic.com/en/docs/console-overview",
    ],

    # Models
    "Claude Opus": [
        "https://docs.anthropic.com/en/docs/about-claude/models",
    ],
    "Claude Sonnet": [
        "https://docs.anthropic.com/en/docs/about-claude/models",
    ],
    "Claude Haiku": [
        "https://docs.anthropic.com/en/docs/about-claude/models",
    ],

    # Features
    "MCP": [
        "https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol",
    ],
    "Model Context Protocol": [
        "https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol",
    ],
    "skills": [
        "https://docs.anthropic.com/en/docs/claude-code/skills",
    ],
    "hooks": [
        "https://docs.anthropic.com/en/docs/claude-code/hooks",
    ],
    "sub-agents": [
        "https://docs.anthropic.com/en/docs/claude-code/sub-agents",
    ],
    "subagents": [
        "https://docs.anthropic.com/en/docs/claude-code/sub-agents",
    ],
    "tool use": [
        "https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview",
    ],
    "tool search": [
        "https://docs.anthropic.com/en/docs/claude-code/tool-search",
    ],
    "extended thinking": [
        "https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking",
    ],
    "thinking": [
        "https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking",
    ],
    "prompt caching": [
        "https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching",
    ],
    "KV cache": [
        "https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching",
    ],
    "context window": [
        "https://docs.anthropic.com/en/docs/about-claude/models",
    ],
    "CLAUDE.md": [
        "https://docs.anthropic.com/en/docs/claude-code/claude-md",
    ],
    "system prompt": [
        "https://docs.anthropic.com/en/docs/build-with-claude/system-prompts",
    ],
    "agentic coding": [
        "https://docs.anthropic.com/en/docs/claude-code/overview",
    ],
    "computer use": [
        "https://docs.anthropic.com/en/docs/agents-and-tools/computer-use",
    ],
    "memory": [
        "https://docs.anthropic.com/en/docs/claude-code/memory",
    ],
    "streaming": [
        "https://docs.anthropic.com/en/docs/build-with-claude/streaming",
    ],
    "batch API": [
        "https://docs.anthropic.com/en/docs/build-with-claude/message-batches",
    ],
    "batches": [
        "https://docs.anthropic.com/en/docs/build-with-claude/message-batches",
    ],
    "citations": [
        "https://docs.anthropic.com/en/docs/build-with-claude/citations",
    ],
    "artifacts": [
        "https://docs.anthropic.com/en/docs/claude-ai/artifacts",
    ],
    "projects": [
        "https://docs.anthropic.com/en/docs/claude-ai/projects",
    ],
    "multi-turn conversation": [
        "https://docs.anthropic.com/en/docs/build-with-claude/multi-turn-conversations",
    ],
    "LSP": [
        "https://docs.anthropic.com/en/docs/claude-code/overview",
    ],
    "git worktrees": [
        "https://docs.anthropic.com/en/docs/claude-code/sub-agents",
    ],
    "agentic loop": [
        "https://docs.anthropic.com/en/docs/claude-code/overview",
    ],
    "compaction": [
        "https://docs.anthropic.com/en/docs/claude-code/memory",
    ],
    "fine-tuning": [
        "https://docs.anthropic.com/en/docs/build-with-claude/fine-tuning",
    ],
}


# ----------------------------------------------------------------------
# Web fetching
# ----------------------------------------------------------------------

def fetch_doc_page(url: str) -> str | None:
    """
    Fetch a docs.anthropic.com page and extract text content.
    Returns plain text, or None on failure.
    """
    try:
        import requests
    except ImportError:
        sys.exit(
            "requests not installed. Install with:\n"
            "    pip install requests"
        )

    try:
        resp = requests.get(url, timeout=30, headers={
            "User-Agent": "claude-academy-book/1.0 (enrichment pipeline)"
        })
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"    WARN: failed to fetch {url}: {exc}")
        return None

    return _extract_text_from_html(resp.text)


def _extract_text_from_html(raw_html: str) -> str:
    """
    Simple HTML-to-text extraction. Strips tags, decodes entities,
    collapses whitespace. No dependency on BeautifulSoup.
    """
    # Remove script and style blocks
    text = re.sub(r"<script[^>]*>.*?</script>", "", raw_html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", "", raw_html, flags=re.S | re.I)
    # Remove nav, header, footer blocks (common in doc sites)
    text = re.sub(r"<(nav|header|footer)[^>]*>.*?</\1>", "", text, flags=re.S | re.I)
    # Replace block-level tags with newlines
    text = re.sub(r"<(p|div|h[1-6]|li|tr|br)[^>]*>", "\n", text, flags=re.I)
    # Strip remaining tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Decode HTML entities
    text = html.unescape(text)
    # Collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    # Trim
    text = text.strip()

    # Truncate to a reasonable size for API input
    max_chars = 15_000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRUNCATED]"

    return text


# ----------------------------------------------------------------------
# Entity filtering and URL resolution
# ----------------------------------------------------------------------

# Aliases: maps variant names (as Claude API might produce) to canonical
# ENTITY_URL_MAP keys. Case-insensitive matching applied at lookup time.
_ENTITY_ALIASES: dict[str, str] = {
    "agents": "sub-agents",
    "sub agents": "sub-agents",
    "subagent": "subagents",
    "agent teams": "sub-agents",
    "work trees": "git worktrees",
    "worktrees": "git worktrees",
    "slash loop": "agentic loop",
    "permissions mode": "Claude Code",
    "auto mode": "Claude Code",
    "remote control": "Claude Code",
    "send message tool": "sub-agents",
    "caching": "prompt caching",
    "cache": "prompt caching",
    "mcp servers": "MCP",
    "mcp server": "MCP",
    "model context protocol (mcp)": "MCP",
    "claude.md file": "CLAUDE.md",
    "claude md": "CLAUDE.md",
    "extended thinking mode": "extended thinking",
    "tool calling": "tool use",
    "function calling": "tool use",
    "batch processing": "batch API",
    "message batches": "batch API",
}


def get_enrichable_entities(entities: dict) -> list[str]:
    """
    Filter entities.json to only those that have docs.claude.com mappings.
    Uses direct matching first, then alias matching for variant names.
    Returns a deduplicated list of canonical entity names.
    """
    candidates = set()
    for category in ("products", "features"):
        for entity in entities.get(category, []):
            # Direct match
            if entity in ENTITY_URL_MAP:
                candidates.add(entity)
                continue
            # Alias match (case-insensitive)
            alias_target = _ENTITY_ALIASES.get(entity.lower())
            if alias_target and alias_target in ENTITY_URL_MAP:
                candidates.add(alias_target)
    return sorted(candidates)


def resolve_urls(entities: list[str]) -> dict[str, str]:
    """
    For each entity, resolve its doc URLs and fetch the content.
    Returns {url: page_text} with deduplication (multiple entities
    may point to the same URL).
    """
    url_set: dict[str, str] = {}
    for entity in entities:
        urls = ENTITY_URL_MAP.get(entity, [])
        for url in urls:
            if url not in url_set:
                print(f"    Fetching {url} ...", flush=True)
                text = fetch_doc_page(url)
                if text:
                    url_set[url] = text
                else:
                    url_set[url] = "[FETCH FAILED]"
    return url_set


# ----------------------------------------------------------------------
# Claude API enrichment
# ----------------------------------------------------------------------

def enrich_with_claude(
    entities: list[str],
    doc_pages: dict[str, str],
    metadata: dict,
    model: str = "claude-sonnet-4-6-20260525",
) -> str:
    """
    Send entities + fetched documentation to Claude API.
    Returns the enrichment.md content.
    """
    try:
        import anthropic
    except ImportError:
        sys.exit(
            "anthropic SDK not installed. Install with:\n"
            "    pip install anthropic"
        )

    api_key = (
        os.environ.get("ANTHROPIC_YT_CLAUDE_LONDON_API_KEY")
        or os.environ.get("ANTHROPIC_API_KEY")
    )
    if not api_key:
        sys.exit(
            "API key not set. Set one of:\n"
            "    export ANTHROPIC_YT_CLAUDE_LONDON_API_KEY=sk-ant-...\n"
            "    export ANTHROPIC_API_KEY=sk-ant-...\n"
        )

    client = anthropic.Anthropic(api_key=api_key)
    title = metadata.get("title", "Unknown")
    upload_date = metadata.get("upload_date", "unknown")

    # Build the documentation context
    doc_context_parts = []
    for url, text in doc_pages.items():
        if text == "[FETCH FAILED]":
            doc_context_parts.append(f"### {url}\n[Could not fetch this page]\n")
        else:
            # Limit each page to keep total context manageable
            trimmed = text[:10_000] if len(text) > 10_000 else text
            doc_context_parts.append(f"### {url}\n{trimmed}\n")

    doc_context = "\n---\n".join(doc_context_parts)

    entity_to_urls: dict[str, list[str]] = {}
    for entity in entities:
        entity_to_urls[entity] = ENTITY_URL_MAP.get(entity, [])

    prompt = f"""You are writing enrichment notes for a book chapter derived from a conference talk.

Talk title: {title}
Talk date: {upload_date}
Entities to enrich: {json.dumps(entity_to_urls, indent=2)}

The talk was recorded on the date above. Speakers describe features as they existed at recording time. The documentation below is CURRENT (fetched today). Your job is to compare and flag differences.

For each entity, write a section in this format:

## <Entity Name>

**Current status:** one-sentence summary of what docs.claude.com says today.

**Changes since talk:** what has changed since the talk was recorded (new features, renamed concepts, deprecated functionality, updated model names/versions). Write "No significant changes" if the docs match what a speaker would have said at that time.

**Key details for chapter:** 2-3 bullet points of authoritative current info that the chapter should use.

Rules:
- Be specific. "The API has changed" is not useful. "The messages API now supports citations via the `citations` parameter, added in March 2026" is.
- If a page failed to fetch, say so and note what you know from training data with a caveat.
- No em-dashes. Use commas, semicolons, or sentence breaks.
- Direct technical voice. No filler.

Here is the current documentation:

{doc_context}"""

    print("    Calling Claude API for enrichment ...", flush=True)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    enrichment_body = response.content[0].text.strip()

    # Build the full enrichment.md
    header = (
        f"# Enrichment notes: {title}\n\n"
        f"Talk date: {upload_date}\n"
        f"Enriched: today (live docs.claude.com fetch + Claude API)\n"
        f"Entities enriched: {len(entities)}\n"
        f"Pages fetched: {sum(1 for v in doc_pages.values() if v != '[FETCH FAILED]')}/{len(doc_pages)}\n\n"
        f"---\n\n"
    )

    return header + enrichment_body + "\n"


# ----------------------------------------------------------------------
# Metadata loading (shared pattern with extract_summary.py)
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


# ----------------------------------------------------------------------
# Processing
# ----------------------------------------------------------------------

def process_chapter(chapter_dir: Path, model: str) -> bool:
    """
    Run enrichment on a single chapter. Returns True on success.
    """
    chapter_dir = chapter_dir.resolve()
    slug = chapter_dir.name

    entities_path = chapter_dir / "entities.json"
    if not entities_path.exists():
        print(f"  SKIP {slug}: no entities.json (run extract_summary.py first)")
        return False

    entities = json.loads(entities_path.read_text(encoding="utf-8"))
    metadata = load_metadata(chapter_dir)

    enrichable = get_enrichable_entities(entities)
    if not enrichable:
        print(f"  SKIP {slug}: no Anthropic-specific entities to enrich")
        # Write a minimal enrichment.md so downstream steps know we checked
        title = metadata.get("title", slug)
        (chapter_dir / "enrichment.md").write_text(
            f"# Enrichment notes: {title}\n\n"
            f"No Anthropic-specific entities found in this chapter's entity list.\n"
            f"No enrichment needed.\n",
            encoding="utf-8",
        )
        return True

    print(f"  Enriching {slug} ({len(enrichable)} entities) ...", flush=True)

    # Fetch documentation pages
    doc_pages = resolve_urls(enrichable)

    # Generate enrichment with Claude
    enrichment_md = enrich_with_claude(
        entities=enrichable,
        doc_pages=doc_pages,
        metadata=metadata,
        model=model,
    )

    (chapter_dir / "enrichment.md").write_text(enrichment_md, encoding="utf-8")
    print(f"    enrichment.md: {len(enrichment_md):,} chars")

    return True


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Pipeline step 3: enrich chapter entities with current "
            "docs.claude.com information."
        )
    )
    ap.add_argument(
        "chapter_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Path to a chapter directory.",
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Process all chapters that have entities.json.",
    )
    ap.add_argument(
        "--model",
        default="claude-sonnet-4-6-20260525",
        help="Anthropic model for enrichment. Default: claude-sonnet-4-6-20260525.",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing enrichment.md files.",
    )
    ap.add_argument(
        "--chapters-dir",
        type=Path,
        default=Path("chapters"),
        help="Root chapters directory. Default: ./chapters",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    if not args.all and args.chapter_dir is None:
        sys.exit("Provide a chapter directory or use --all. See --help.")

    # Check dependencies upfront
    try:
        import requests  # noqa: F401
    except ImportError:
        sys.exit("requests not installed. Install with: pip install requests")
    try:
        import anthropic  # noqa: F401
    except ImportError:
        sys.exit("anthropic not installed. Install with: pip install anthropic")

    api_key = (
        os.environ.get("ANTHROPIC_YT_CLAUDE_LONDON_API_KEY")
        or os.environ.get("ANTHROPIC_API_KEY")
    )
    if not api_key:
        sys.exit(
            "API key not set. Set one of:\n"
            "    export ANTHROPIC_YT_CLAUDE_LONDON_API_KEY=sk-ant-...\n"
            "    export ANTHROPIC_API_KEY=sk-ant-..."
        )

    if args.all:
        chapters_root = args.chapters_dir
        if not chapters_root.is_dir():
            sys.exit(f"Chapters directory not found: {chapters_root}")

        dirs = sorted([
            d for d in chapters_root.iterdir()
            if d.is_dir() and (d / "entities.json").exists()
        ])

        if not dirs:
            sys.exit(f"No chapters with entities.json found in {chapters_root}")

        print(f"Found {len(dirs)} chapters with entities.")
        n_ok = 0
        n_skip = 0
        for d in dirs:
            if not args.force and (d / "enrichment.md").exists():
                print(f"  SKIP {d.name}: already enriched (use --force to redo)")
                n_skip += 1
                continue
            if process_chapter(d, args.model):
                n_ok += 1
            else:
                n_skip += 1

        print(f"\nDone. {n_ok} enriched, {n_skip} skipped.")

    else:
        chapter_dir = args.chapter_dir
        if not chapter_dir.is_dir():
            sys.exit(f"Not a directory: {chapter_dir}")
        if not args.force and (chapter_dir / "enrichment.md").exists():
            print("Already enriched. Use --force to redo.")
            return
        process_chapter(chapter_dir, args.model)
        print("Done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")

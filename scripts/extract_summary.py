#!/usr/bin/env python3
"""
extract_summary.py
==================

Pipeline step 2: extract a structured summary, named entities, and notable
quotes from a chapter's transcript.

Input
-----
- chapters/<slug>/source/transcript.txt
- chapters/<slug>/metadata.yaml

Output
------
- chapters/<slug>/summary.md       ~250-word abstract + key claims as bullets
- chapters/<slug>/entities.json    named entities by category
- chapters/<slug>/quotes.md        notable verbatim quotes worth preserving

Modes
-----
- **Heuristic** (default): regex + keyword matching. Fast, deterministic,
  no API key needed. Good enough for entity extraction; summaries are
  extractive (top sentences by relevance score).
- **Claude** (--use-claude): Anthropic API for abstractive summary,
  entity extraction, and quote selection. Requires ANTHROPIC_API_KEY.
  Produces better summaries but costs money and is non-deterministic.

The orchestrating skill in Claude Code typically uses heuristic mode
because Claude does the summary work directly in the chat. The Claude
mode is for standalone batch runs.

Usage
-----
    # Heuristic mode on one chapter
    python scripts/extract_summary.py chapters/beyond-the-basics-with-claude-code

    # Claude mode
    python scripts/extract_summary.py chapters/beyond-the-basics --use-claude

    # Process all chapters
    python scripts/extract_summary.py --all

    # Process all chapters with Claude
    python scripts/extract_summary.py --all --use-claude

Dependencies
------------
- Heuristic mode: Python 3.11+ standard library only.
- Claude mode: pip install anthropic

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
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
# Known entities: seed lists for heuristic extraction
# ----------------------------------------------------------------------

# These lists are not exhaustive. They seed the regex matcher so it can
# find known entities reliably. Unknown entities are caught by pattern
# heuristics (e.g. capitalised multi-word phrases).

KNOWN_PRODUCTS = [
    "Claude Code", "Claude Desktop", "Claude",
    "Claude Opus", "Claude Sonnet", "Claude Haiku",
    "Claude Opus 4", "Claude Sonnet 4", "Claude Haiku 4",
    "Claude 3.5 Sonnet", "Claude 3 Opus", "Claude 3 Haiku",
    "Anthropic Console", "Anthropic API",
    "VS Code", "JetBrains", "Vim", "Neovim",
    "GitHub Copilot", "Cursor", "Windsurf",
    "ChatGPT", "GPT-4",
]

KNOWN_FEATURES = [
    "MCP", "Model Context Protocol",
    "skills", "hooks", "sub-agents", "subagents",
    "tool search", "tool use",
    "extended thinking", "thinking",
    "prompt caching", "KV cache",
    "context window", "context budget",
    "system prompt", "CLAUDE.md",
    "agentic coding", "agentic loop",
    "multi-turn conversation",
    "artifacts", "projects",
    "computer use", "bash tool",
    "memory", "compaction",
    "streaming", "batches", "batch API",
    "citations", "grounding",
    "fine-tuning", "RLHF",
    "LSP", "language server protocol",
    "CI/CD", "pre-commit hooks",
    "git worktrees",
]

KNOWN_CONCEPTS = [
    "context window", "token", "tokens",
    "KV cache", "cache invalidation",
    "in-context learning", "ICL",
    "prompt engineering", "prompt design",
    "chain of thought", "CoT",
    "retrieval augmented generation", "RAG",
    "embeddings", "vector search",
    "hallucination", "grounding",
    "latency", "throughput", "cost",
    "safety", "alignment", "RLHF",
    "red teaming", "jailbreak",
    "multi-agent", "orchestration",
    "tool calling", "function calling",
    "few-shot", "zero-shot",
    "temperature", "top-p", "top-k",
    "system prompt", "user prompt",
]

# Pattern for detecting person names: Capitalised First Last, optionally
# with middle initial. This is deliberately conservative to avoid false
# positives on product names and section headers.
_PERSON_PATTERN = re.compile(
    r"\b([A-Z][a-z]{2,15})\s+([A-Z][a-z]{2,15})\b"
)

# Common false positives for person detection
_NOT_PEOPLE = {
    "Claude Code", "Claude Desktop", "Claude Opus", "Claude Sonnet",
    "Claude Haiku", "Google Cloud", "Visual Studio", "Open Source",
    "Machine Learning", "Deep Learning", "Monte Carlo",
    "New York", "San Francisco", "Los Angeles",
    "All Right", "Of Course",
    # Sentence-initial patterns where "Claude" is the subject
    "Also Claude", "And Claude", "Because Claude", "But Claude",
    "So Claude", "Then Claude", "When Claude", "If Claude",
    "Like Claude", "With Claude", "For Claude",
    "About Claude", "After Claude", "Before Claude",
    # Other common false positives from ASR transcripts
    "The Claude", "This Claude", "That Claude",
    "Your Claude", "Our Claude",
}


# ----------------------------------------------------------------------
# Heuristic entity extraction
# ----------------------------------------------------------------------

def extract_entities_heuristic(text: str) -> dict[str, list[str]]:
    """
    Extract named entities from transcript text using keyword matching
    and pattern heuristics. Returns the entities.json structure.
    """
    text_lower = text.lower()

    products = _match_known(text, text_lower, KNOWN_PRODUCTS)
    features = _match_known(text, text_lower, KNOWN_FEATURES)
    concepts = _match_known(text, text_lower, KNOWN_CONCEPTS)
    people = _extract_people(text)
    papers = _extract_papers_or_docs(text)

    return {
        "products": sorted(products),
        "features": sorted(features),
        "concepts": sorted(concepts),
        "people": sorted(people),
        "papers_or_docs": sorted(papers),
    }


def _match_known(text: str, text_lower: str, known: list[str]) -> set[str]:
    """Find which known entities appear in the text."""
    found: set[str] = set()
    for entity in known:
        # Case-insensitive search using word boundaries
        pattern = r"\b" + re.escape(entity.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(entity)
    return found


def _extract_people(text: str) -> set[str]:
    """
    Extract person names using capitalisation patterns.
    Conservative: requires First Last format, filters known non-people.
    """
    found: set[str] = set()
    for match in _PERSON_PATTERN.finditer(text):
        name = match.group(0)
        if name not in _NOT_PEOPLE:
            found.add(name)
    return found


def _extract_papers_or_docs(text: str) -> set[str]:
    """
    Extract references to papers, documentation pages, or URLs.
    Looks for docs.claude.com references and quoted titles.
    """
    found: set[str] = set()

    # docs.claude.com URLs
    for match in re.finditer(r"docs\.claude\.com[/\w\-]*", text):
        found.add(match.group(0))

    # Quoted titles that look like paper/doc names (4+ words in quotes)
    for match in re.finditer(r'"([^"]{20,120})"', text):
        candidate = match.group(1)
        # Filter out dialogue (contains "I", "you", etc.)
        if not re.search(r"\b(I|you|we|my|your|don't|can't|won't)\b", candidate, re.I):
            found.add(candidate)

    return found


# ----------------------------------------------------------------------
# Heuristic summary extraction
# ----------------------------------------------------------------------

def extract_summary_heuristic(
    text: str, metadata: dict, target_words: int = 250
) -> str:
    """
    Produce an extractive summary: score sentences by relevance signals,
    pick the top ones up to the target word count, then format as a
    summary.md with abstract + key claims.
    """
    sentences = _split_sentences(text)
    if not sentences:
        return _format_summary(metadata, "Transcript is empty.", [])

    scored = []
    for i, sent in enumerate(sentences):
        score = _score_sentence(sent, i, len(sentences))
        scored.append((score, i, sent))

    # Sort by score descending, pick top sentences for abstract
    scored.sort(key=lambda x: x[0], reverse=True)

    # Build abstract from top sentences, re-ordered by position
    abstract_sents: list[tuple[int, str]] = []
    word_count = 0
    for score, idx, sent in scored:
        words = len(sent.split())
        if word_count + words > target_words:
            if abstract_sents:
                break
        abstract_sents.append((idx, sent))
        word_count += words

    # Re-order by position in original text
    abstract_sents.sort(key=lambda x: x[0])
    abstract = " ".join(s for _, s in abstract_sents)

    # Key claims: top 5-7 sentences that contain strong claim signals
    claim_sents = [
        sent for score, _, sent in scored[:15]
        if _is_claim(sent)
    ][:7]

    return _format_summary(metadata, abstract, claim_sents)


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    # Split on sentence-ending punctuation followed by space + uppercase
    raw = re.split(r"(?<=[\.\?\!])\s+(?=[A-Z])", text.strip())
    # Filter out very short fragments
    return [s.strip() for s in raw if len(s.strip().split()) >= 4]


def _score_sentence(sent: str, position: int, total: int) -> float:
    """
    Score a sentence for summary-worthiness. Higher is better.

    Signals:
    - Position: early and late sentences score higher (intro/conclusion)
    - Length: medium-length sentences preferred (not too short, not too long)
    - Entity density: sentences mentioning known entities score higher
    - Claim language: sentences with definitive statements score higher
    """
    score = 0.0
    words = sent.split()
    n_words = len(words)
    sent_lower = sent.lower()

    # Position: first 15% and last 10% of sentences get a boost
    rel_pos = position / max(total, 1)
    if rel_pos < 0.15:
        score += 2.0
    elif rel_pos > 0.90:
        score += 1.5

    # Length: prefer 15-40 word sentences
    if 15 <= n_words <= 40:
        score += 1.0
    elif n_words < 8 or n_words > 60:
        score -= 1.0

    # Entity mentions
    entity_hits = 0
    for entity in KNOWN_PRODUCTS + KNOWN_FEATURES[:20]:
        if entity.lower() in sent_lower:
            entity_hits += 1
    score += min(entity_hits * 0.5, 3.0)

    # Claim language
    if _is_claim(sent):
        score += 1.5

    # Penalise oral artefacts
    oral_markers = ["all right", "you know", "i mean", "let's see",
                    "okay so", "um", "uh", "like i said"]
    for marker in oral_markers:
        if marker in sent_lower:
            score -= 2.0

    return score


def _is_claim(sent: str) -> bool:
    """Check if a sentence looks like a substantive claim."""
    sent_lower = sent.lower()
    claim_patterns = [
        r"\bis\b.*\b(the|a|an)\b",          # "X is the/a Y"
        r"\b(allows?|enables?|provides?)\b",  # capability claims
        r"\b(means?|requires?)\b",            # definitional
        r"\b(should|must|need to)\b",         # prescriptive
        r"\b(because|since|therefore)\b",     # causal
        r"\b(instead of|rather than)\b",      # contrastive
        r"\b\d+[x%]\b",                      # quantitative ("10x", "50%")
        r"\b(faster|slower|better|worse)\b",  # comparative
    ]
    return any(re.search(p, sent_lower) for p in claim_patterns)


def _format_summary(
    metadata: dict, abstract: str, claims: list[str]
) -> str:
    """Format the summary.md output."""
    title = metadata.get("title", "Unknown")
    slug = metadata.get("slug", "unknown")

    lines = [
        f"# Summary: {title}",
        "",
        f"Chapter slug: `{slug}`",
        "",
        "## Abstract",
        "",
        abstract,
        "",
    ]

    if claims:
        lines.extend([
            "## Key claims",
            "",
        ])
        for claim in claims:
            # Trim to a reasonable length for a bullet
            trimmed = claim.strip()
            if len(trimmed) > 200:
                trimmed = trimmed[:197] + "..."
            lines.append(f"- {trimmed}")
        lines.append("")

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Heuristic quote extraction
# ----------------------------------------------------------------------

def extract_quotes_heuristic(text: str, metadata: dict) -> str:
    """
    Find notable verbatim quotes worth preserving in the chapter.
    Looks for: strong metaphors, memorable phrasing, definitive claims.
    """
    sentences = _split_sentences(text)
    quotes: list[str] = []

    for sent in sentences:
        if _is_notable_quote(sent):
            quotes.append(sent)

    # Cap at 15 quotes
    quotes = quotes[:15]

    title = metadata.get("title", "Unknown")
    lines = [
        f"# Notable quotes: {title}",
        "",
        "Verbatim quotes from the transcript worth preserving or",
        "referencing in the chapter.",
        "",
    ]

    if quotes:
        for q in quotes:
            lines.append(f"> {q}")
            lines.append("")
    else:
        lines.append("No notable quotes identified by heuristic extraction.")
        lines.append("")

    return "\n".join(lines)


def _is_notable_quote(sent: str) -> bool:
    """
    Score whether a sentence is a notable quote worth preserving.
    Looks for: metaphors, strong opinions, memorable phrasing.
    """
    sent_lower = sent.lower()
    words = sent.split()

    # Too short or too long
    if len(words) < 8 or len(words) > 50:
        return False

    # Penalise oral filler
    oral = ["all right", "you know", "i mean", "let's see", "okay",
            "um", "uh", "like i said", "so yeah"]
    if any(m in sent_lower for m in oral):
        return False

    score = 0

    # Metaphor signals: "like", "think of it as", "imagine"
    metaphor_patterns = [
        r"\blike\s+a\b", r"\bthink of\b", r"\bimagine\b",
        r"\banalog(y|ous)\b", r"\bmetaphor\b",
    ]
    if any(re.search(p, sent_lower) for p in metaphor_patterns):
        score += 2

    # Strong opinion: "the most important", "the key thing", "crucial"
    opinion_patterns = [
        r"\bmost important\b", r"\bkey (thing|insight|point)\b",
        r"\bcrucial\b", r"\bfundamental\b", r"\bcritical\b",
        r"\bbiggest (mistake|problem|issue)\b",
    ]
    if any(re.search(p, sent_lower) for p in opinion_patterns):
        score += 2

    # Quantitative claims
    if re.search(r"\b\d+[x%]\b", sent):
        score += 1

    # Contrastive ("not X, but Y")
    if re.search(r"\bnot\b.*\bbut\b", sent_lower):
        score += 1

    # Prescriptive advice
    if re.search(r"\b(always|never|don't|stop|start)\b", sent_lower):
        score += 1

    return score >= 2


# ----------------------------------------------------------------------
# Claude mode (Anthropic API)
# ----------------------------------------------------------------------

def extract_with_claude(
    text: str, metadata: dict, model: str = "claude-sonnet-4-20250514"
) -> tuple[str, dict, str]:
    """
    Use the Anthropic API for abstractive summary, entity extraction,
    and quote selection. Returns (summary_md, entities_dict, quotes_md).
    """
    try:
        import anthropic
    except ImportError:
        sys.exit(
            "anthropic SDK not installed. Install with:\n"
            "    pip install anthropic\n"
            "Or use heuristic mode (the default) which needs no API key."
        )

    api_key = os.environ.get("ANTHROPIC_YT_CLAUDE_LONDON_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit(
            "API key not set. Set one of:\n"
            "    export ANTHROPIC_YT_CLAUDE_LONDON_API_KEY=sk-ant-...\n"
            "    export ANTHROPIC_API_KEY=sk-ant-...\n"
            "Or use heuristic mode (the default)."
        )

    client = anthropic.Anthropic(api_key=api_key)
    title = metadata.get("title", "Unknown")

    # Truncate very long transcripts to stay within context limits.
    # Sonnet handles ~200k tokens; a 50k-char transcript is safe.
    max_chars = 150_000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRANSCRIPT TRUNCATED]"

    prompt = f"""You are extracting structured information from a conference talk transcript.

Talk title: {title}
Metadata: {json.dumps(metadata, indent=2)}

The transcript is from a Claude Academy / Anthropic talk. Extract the following three outputs as JSON in a single response.

Respond with ONLY a JSON object with three keys: "summary", "entities", "quotes".

1. "summary": an object with:
   - "abstract": a ~250-word abstract of the talk's core argument and content. Write in technical reference style (dry, precise, like docs.claude.com). Do not use em-dashes.
   - "claims": a list of 5-7 strings, each a key technical claim made in the talk.

2. "entities": an object with:
   - "products": list of product names mentioned (e.g. "Claude Code", "VS Code")
   - "features": list of features/capabilities discussed (e.g. "MCP", "hooks", "skills")
   - "concepts": list of technical concepts (e.g. "context window", "KV cache")
   - "people": list of people mentioned by name
   - "papers_or_docs": list of papers, docs, or URLs referenced

3. "quotes": a list of 5-15 objects, each with:
   - "text": the verbatim quote from the transcript
   - "reason": one sentence on why this quote is worth preserving

Here is the transcript:

{text}"""

    print("Calling Anthropic API ...", flush=True)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()

    # Parse JSON from the response (handle markdown code fences)
    if raw.startswith("```"):
        raw = re.sub(r"^```\w*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(
            f"Failed to parse Claude's response as JSON: {exc}\n"
            f"Raw response:\n{raw[:500]}"
        )

    # Format summary.md
    summary_data = data.get("summary", {})
    abstract = summary_data.get("abstract", "No abstract returned.")
    claims = summary_data.get("claims", [])
    summary_md = _format_summary(metadata, abstract, claims)

    # entities.json
    entities = data.get("entities", {})
    # Ensure all expected keys exist
    for key in ("products", "features", "concepts", "people", "papers_or_docs"):
        if key not in entities:
            entities[key] = []

    # Format quotes.md
    raw_quotes = data.get("quotes", [])
    quote_lines = [
        f"# Notable quotes: {title}",
        "",
        "Quotes selected by Claude from the transcript.",
        "",
    ]
    for q in raw_quotes:
        text_q = q.get("text", "")
        reason = q.get("reason", "")
        quote_lines.append(f"> {text_q}")
        if reason:
            quote_lines.append(f"")
            quote_lines.append(f"*{reason}*")
        quote_lines.append("")
    quotes_md = "\n".join(quote_lines)

    return summary_md, entities, quotes_md


# ----------------------------------------------------------------------
# Metadata loading
# ----------------------------------------------------------------------

def load_metadata(chapter_dir: Path) -> dict:
    """
    Load metadata.yaml from a chapter directory.
    Hand-parsed to avoid PyYAML dependency (matching transcribe_playlist.py).
    """
    meta_path = chapter_dir / "metadata.yaml"
    if not meta_path.exists():
        sys.exit(f"metadata.yaml not found in {chapter_dir}")

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

def process_chapter(chapter_dir: Path, use_claude: bool, model: str) -> bool:
    """
    Run extraction on a single chapter directory.
    Returns True on success.
    """
    chapter_dir = chapter_dir.resolve()
    slug = chapter_dir.name
    transcript_path = chapter_dir / "source" / "transcript.txt"

    if not transcript_path.exists():
        print(f"  SKIP {slug}: no transcript.txt")
        return False

    metadata = load_metadata(chapter_dir)
    text = transcript_path.read_text(encoding="utf-8")

    if not text.strip():
        print(f"  SKIP {slug}: transcript is empty")
        return False

    print(f"  Processing {slug} ({len(text):,} chars) ...", flush=True)

    if use_claude:
        summary_md, entities, quotes_md = extract_with_claude(
            text, metadata, model=model
        )
    else:
        entities = extract_entities_heuristic(text)
        summary_md = extract_summary_heuristic(text, metadata)
        quotes_md = extract_quotes_heuristic(text, metadata)

    # Write outputs
    (chapter_dir / "summary.md").write_text(summary_md, encoding="utf-8")
    (chapter_dir / "entities.json").write_text(
        json.dumps(entities, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (chapter_dir / "quotes.md").write_text(quotes_md, encoding="utf-8")

    n_entities = sum(len(v) for v in entities.values())
    print(f"    summary.md:    {len(summary_md):,} chars")
    print(f"    entities.json: {n_entities} entities")
    print(f"    quotes.md:     {len(quotes_md):,} chars")

    return True


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Pipeline step 2: extract summary, entities, and quotes "
            "from a chapter's transcript."
        )
    )
    ap.add_argument(
        "chapter_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Path to a chapter directory (e.g. chapters/beyond-the-basics).",
    )
    ap.add_argument(
        "--all",
        action="store_true",
        help="Process all chapter directories under chapters/.",
    )
    ap.add_argument(
        "--use-claude",
        action="store_true",
        help="Use Anthropic API instead of heuristic extraction.",
    )
    ap.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Anthropic model to use in Claude mode. Default: claude-sonnet-4-20250514.",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing summary/entities/quotes files.",
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

    if args.all:
        chapters_root = args.chapters_dir
        if not chapters_root.is_dir():
            sys.exit(f"Chapters directory not found: {chapters_root}")

        dirs = sorted([
            d for d in chapters_root.iterdir()
            if d.is_dir() and (d / "source" / "transcript.txt").exists()
        ])

        if not dirs:
            sys.exit(f"No chapters with transcripts found in {chapters_root}")

        print(f"Found {len(dirs)} chapters with transcripts.")
        n_ok = 0
        n_skip = 0
        for d in dirs:
            if not args.force and (d / "summary.md").exists():
                print(f"  SKIP {d.name}: already extracted (use --force to redo)")
                n_skip += 1
                continue
            if process_chapter(d, args.use_claude, args.model):
                n_ok += 1
            else:
                n_skip += 1
        print(f"\nDone. {n_ok} processed, {n_skip} skipped.")

    else:
        chapter_dir = args.chapter_dir
        if not chapter_dir.is_dir():
            sys.exit(f"Not a directory: {chapter_dir}")
        if not args.force and (chapter_dir / "summary.md").exists():
            print(f"Already extracted. Use --force to redo.")
            return
        process_chapter(chapter_dir, args.use_claude, args.model)
        print("Done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")

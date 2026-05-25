# Pipeline Specification

Detailed specification of the 10-step pipeline. This is the contract
each script and skill must satisfy.

## Step 1: Transcribe

**Status:** implemented in `scripts/yt_transcribe.py` (single video) and
`scripts/transcribe_playlist.py` (playlist driver).

**Input:** YouTube URL (video or playlist).

**Output per chapter:**
```
chapters/<slug>/
  source/
    transcript.txt
  metadata.yaml
```

`metadata.yaml` schema:
```yaml
slug: beyond-the-basics-with-claude-code
video_id: "abc123"
title: "Beyond the Basics with Claude Code"
url: https://www.youtube.com/watch?v=abc123
upload_date: 2026-03-15
duration_seconds: 2745
duration_human: "45:45"
transcribed_at: 2026-05-25T10:00:00+00:00
```

Top-level `chapters/playlist_index.json` tracks state for resume-on-rerun.

## Step 2: Extract summary

**Status:** not implemented. Next to build.

**Input:** `chapters/<slug>/source/transcript.txt` + `metadata.yaml`.

**Output:**
```
chapters/<slug>/
  summary.md           # ~250-word abstract + key claims as bullet list
  entities.json        # extracted named entities (products, features, papers)
  quotes.md            # notable verbatim quotes worth preserving
```

`entities.json` schema:
```json
{
  "products": ["Claude Code", "Claude Opus 4.7"],
  "features": ["MCP", "skills", "hooks", "sub-agents", "tool search"],
  "concepts": ["context window", "KV cache", "in-context learning"],
  "people": ["Daisy Holman"],
  "papers_or_docs": []
}
```

Two modes:
- **Heuristic mode** (default): regex + NLP extraction, no LLM. Fast,
  deterministic.
- **Claude mode** (`--use-claude`): Anthropic API for actual summary
  writing. Requires `ANTHROPIC_API_KEY`.

The skill running in Claude Code uses heuristic mode because Claude
does the summary work directly in the chat. The script's Claude mode
is for standalone runs.

## Step 3: Enrich

**Status:** not implemented.

**Input:** `entities.json`.

**Output:** `chapters/<slug>/enrichment.md` with current authoritative
info from `docs.claude.com` for each Anthropic product/feature entity.

This step exists because speakers describe features as they existed at
recording time, which may be months out of date. The enrichment notes
flag what has changed so the chapter can use current terminology.

Implementation: most naturally done by Claude in the chat using
web_fetch on `docs.claude.com` URLs. No dedicated script needed.

## Step 4: Assemble corpus

**Status:** implicit. Once steps 1-3 complete, the corpus exists in
`chapters/<slug>/`. No separate script required.

## Step 5: Overlap check

**Status:** not implemented.

**Input:** `chapters/<slug>/entities.json` + top-level `book_index.json`.

**Output:** `chapters/<slug>/overlap_report.md` describing how this
chapter relates to already-drafted chapters.

`book_index.json` schema:
```json
{
  "chapters": [
    {
      "slug": "beyond-the-basics",
      "title": "Beyond the Basics with Claude Code",
      "source": "Daisy Holman talk, Anthropic, March 2026",
      "covers_in_depth": [
        "context window as fixed budget",
        "KV cache invalidation cost",
        "MCP vs skills tradeoff",
        "red-squigglies feedback loops via hooks"
      ],
      "mentions_only": ["fine-tuning", "in-context learning"],
      "entities": ["Claude Code", "MCP", "skills", "hooks", "sub-agents"],
      "code_examples": ["mcp-config", "claude-md", "skill-frontmatter", "post-tool-hook"]
    }
  ]
}
```

Overlap categories the script detects:
- **Concept overlap:** two chapters both list the same item in
  `covers_in_depth`. Flagged as duplicate, decide canonical home.
- **Quote overlap:** detected by separate quote fingerprinting (later).

Example overlap is editorial-only; not auto-detected.

## Step 6: Draft chapter

**Status:** not implemented. Hardest step.

**Input:** entire `chapters/<slug>/` corpus + the overlap report.

**Output:** `chapters/<slug>/chapter.md`.

Done by Claude in the chat following the technical-reference voice
defined in `docs/design_decisions.md`. Concept-organised structure, not
talk-chronological. Code examples inline where prose calls for them.

## Step 7: Source-fidelity audit

**Status:** not implemented.

**Input:** `chapters/<slug>/chapter.md` + corpus.

**Output:** `chapters/<slug>/audit.md` listing each substantive claim
in the chapter and its source: transcript line, enrichment doc, or
"editorial extension" if not directly from the corpus.

The reason: when I (the author) extend beyond what a speaker said, I
want that visible, not buried. The earlier Holman draft had sections
4.3 and 4.4 that extended beyond the transcript; the audit step makes
that systematic, not a footnote afterthought.

## Step 8: Cross-reference

**Status:** not implemented.

**Input:** overlap report + chapter draft.

**Output:** edited chapter with "see chapter X" notes inserted where
appropriate.

## Step 9: Update book index

**Status:** not implemented.

**Input:** finalised `chapters/<slug>/chapter.md`.

**Output:** updated `book_index.json` with this chapter's row added.

Mostly a JSON merge operation, possibly with a final-pass entity check.

## Step 10: Stitch book

**Status:** not implemented.

**Input:** all `chapters/*/chapter.md` files + `book_index.json`.

**Output:** `book/book.md`.

Composes:
- YAML frontmatter (title, author, date)
- Table of contents (from book_index.json, chapter order configurable)
- Each chapter's content with consistent heading levels
- Glossary section assembled from entities across all chapters
- Asset references resolved

Format: clean markdown ready for Claude in Design.

## Per-step timing estimate

| Step | First time | Subsequent |
|------|-----------|-----------|
| 1. Transcribe (45-min video) | 2 min on 5090 | 90 sec |
| 2. Summarise | 30 sec | 30 sec |
| 3. Enrich | 2-5 min (interactive) | 2-5 min |
| 5. Overlap check | < 5 sec | < 5 sec |
| 6. Draft | 10-30 min (interactive) | 10-30 min |
| 7. Audit | 2-5 min (interactive) | 2-5 min |
| 8. Cross-ref | 1-2 min | 1-2 min |
| 9. Update index | < 5 sec | < 5 sec |
| 10. Stitch | < 5 sec | < 5 sec |

End-to-end per chapter: roughly 30-60 min of wall time, most of it
during steps 3 and 6 where Claude in the chat does substantive work.

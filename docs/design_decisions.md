# Design Decisions

This document captures the choices made during pipeline design, with
the reasoning behind each. New contributors (human or AI) should read
this before changing the architecture.

## 1. What is this book?

A personal technical-reference work on practical Claude Code at scale.
Built from Anthropic's Claude Academy YouTube playlist plus supporting
material. Audience: the author. Voice: technical reference (dry, like
`docs.claude.com`), not narrative essay.

## 2. Chapter unit: one talk = one chapter

Each Claude Academy video becomes one chapter. Talks are the spine of
the book. The alternative (topic-anchored chapters with talks as inputs)
produces a better book but requires upfront topic planning and is harder
to grow incrementally. Talk-anchored is what we chose.

**Consequence:** overlap between chapters is inevitable since multiple
talks discuss e.g. context windows. Mitigation: `book_index.json` tracks
what each chapter covers, and step 5 of the pipeline runs an overlap
check before drafting so each chapter sharpens its unique angle.

## 3. Voice: technical reference

Not speaker-faithful (don't preserve Daisy Holman's idiom). Not author
voice (no first-person essay). Reference style: precise, dry,
look-up-friendly.

**Consequence:** chapter structure is concept-organised, not narrative.
A chapter on "Beyond the Basics" is rearranged from the talk's flow
into sections like "Concepts / Customisation primitives / Patterns /
Reference", with the talk's evidence and examples populating that
structure.

## 4. Audience: self

This is a personal reference. No need to translate jargon for
non-engineers. No need for clinical framing. Direct technical content
throughout.

## 5. Sources in scope

In order of priority:

1. **Claude Academy transcripts** (the spine)
2. **Anthropic documentation** at `docs.claude.com` and the Anthropic
   blog: primary source for what features actually do today, vs what
   speakers said about them months ago
3. **The author's own work** where relevant as worked examples:
   - GRADE-ADOLOPMENT multi-agent pipeline (`scalle0/grade-adolopment-multiagent`)
   - Wanda MCP server (ITG Antwerp travel medicine guidelines)
   - PHI de-identification gateway for clinical documents
   - RTX 5090 local LLM workstation with Tailscale networking
   - ImmunoVax clinical decision support (RAG + FastAPI)
   - Arduino UNO Q hardware experiments

## 6. Out of scope (explicitly)

- General LLM theory not directly tied to Claude Code practice
- Anthropic's safety/alignment research (except where it constrains
  what Claude Code can do)
- Comparison with competing AI coding tools

## 7. Build approach: skill + scripts

Skill orchestrates, Python does heavy lifting. The orchestrating skill
lives at `skills/chapter-pipeline/SKILL.md`. It calls scripts in
`scripts/` via bash, asks for human review at decision points, and
maintains the corpus in `chapters/<slug>/`.

**Why this split:** the work that needs determinism and speed (audio
download, Whisper inference, regex substitutions, JSON manipulation)
goes in scripts. The work that needs judgment (drafting prose, deciding
overlap is acceptable, choosing which entities are canonical) stays in
the skill, where Claude does it.

## 8. Not using Managed Agents

Managed Agents is for unattended scheduled work on Anthropic's compute.
This pipeline is driven interactively on local hardware (RTX 5090).
Wrong tool for this job. If we later want weekly auto-ingestion of new
Claude Academy videos, that would be a Managed Agents wrapper around
the existing pipeline. Not now.

## 9. Output target: Claude in Design

Final stitched output is a single `book/book.md` with frontmatter,
clean section structure, fenced code blocks, and asset references that
Claude in Design can render to PDF or `.docx` for personal use.

## 10. Things deliberately deferred

- **Concept index across chapters:** will emerge organically from
  chapter summaries once 3-5 chapters exist. Don't design it upfront.
- **Image/diagram extraction from talks:** out of scope for v1.
  Transcripts only.
- **Multi-language transcripts:** Claude Academy is English-only.
  The transcriber supports NL/FR/etc. for other sources, but the book
  itself is English.
- **Publication outside personal use:** not planned. If it ever
  happens, copyright clearance for the quoted material would need a
  separate review.

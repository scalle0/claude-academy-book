# Claude Academy Book

A personal project: build a technical-reference markdown book from
transcripts of Anthropic's Claude Academy YouTube talks.

The book is a personal reference work, not a publication. Audience: me.
Voice: technical reference (dry, like `docs.claude.com`). Source spine:
Anthropic's Claude Academy playlist on YouTube, with supporting material
from Anthropic documentation and my own work where relevant.

## Pipeline (10 steps)

```
1.  Transcribe         scripts/transcribe_playlist.py -> chapters/<slug>/source/transcript.txt
2.  Summarise          scripts/extract_summary.py     -> chapters/<slug>/summary.md, entities.json, quotes.md
3.  Enrich             pull current docs.claude.com info -> chapters/<slug>/enrichment.md
4.  Assemble corpus    everything in chapters/<slug>/ ready for drafting
5.  Overlap check      scripts/overlap_check.py against book_index.json -> overlap_report.md
6.  Draft chapter      Claude Code writes chapters/<slug>/chapter.md from the corpus
7.  Source-fidelity audit  every claim traceable to corpus or marked editorial -> audit.md
8.  Cross-reference    insert "see chapter X" notes where overlap is partial
9.  Update book index  add this chapter's entities, claims, concepts to book_index.json
10. Stitch book        scripts/stitch_book.py -> book/book.md (ready for Claude in Design)
```

The pipeline is driven by a Claude Code skill (`skills/chapter-pipeline/`)
that orchestrates scripts and asks for human review at appropriate
checkpoints.

## Current status

- **Step 1 (transcription)**: implemented in `scripts/yt_transcribe.py`
  and `scripts/transcribe_playlist.py`. Tested.
- **Steps 2-10**: not yet built. Next: `extract_summary.py`.

## Directory structure

```
scripts/         Python heavy lifting. One script per pipeline step.
skills/          Claude Code skills (orchestration in markdown).
chapters/        Generated per-chapter corpora. Mostly gitignored.
book/            Final stitched book.md and assets.
docs/            Design decisions, pipeline notes, this project's why.
```

## Setup

```bash
# 1. Python 3.11+ recommended.
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate

# 2. Install dependencies.
pip install -U yt-dlp openai-whisper torch

# 3. ffmpeg must be on PATH:
#    macOS:  brew install ffmpeg
#    Ubuntu: sudo apt install ffmpeg
#    Windows: winget install ffmpeg

# 4. (Optional) Set Whisper model cache somewhere with space.
export WHISPER_CACHE_DIR=/path/to/cache
```

## First run

```bash
# Dry run against Claude Academy to see what's in the playlist.
python scripts/transcribe_playlist.py \
    "https://www.youtube.com/playlist?list=PLkhpYBUaBOP_W7gjN95T1k_kjBUEXuPr7" \
    --dry-run

# Smoke test on first two videos.
python scripts/transcribe_playlist.py \
    "https://www.youtube.com/playlist?list=PLkhpYBUaBOP_W7gjN95T1k_kjBUEXuPr7" \
    --limit 2 --model large-v3 --language en \
    --prompt "Claude Code, Anthropic, MCP, hooks, skills, sub-agents"

# Full run (resumes from where smoke test stopped).
python scripts/transcribe_playlist.py \
    "https://www.youtube.com/playlist?list=PLkhpYBUaBOP_W7gjN95T1k_kjBUEXuPr7" \
    --model large-v3 --language en \
    --prompt "Claude Code, Anthropic, MCP, hooks, skills, sub-agents, KV cache"
```

## See also

- `docs/design_decisions.md`: why this book exists, what counts as in-scope
- `docs/pipeline.md`: detailed pipeline specification, `book_index.json` shape
- `scripts/yt_transcribe.py`: single-video transcriber (Whisper + yt-dlp)
- `scripts/transcribe_playlist.py`: playlist driver

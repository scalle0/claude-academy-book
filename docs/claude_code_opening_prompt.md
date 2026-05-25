# Claude Code Opening Prompt

Paste the following into a fresh Claude Code session opened in this
directory. It bootstraps the repo: git init, pyproject, gitignore,
first commit, and a starting plan.

---

I have a personal project to build a markdown-reference book from
YouTube transcripts of Anthropic's Claude Academy talks. The scaffolding
is already laid out in this directory.

Please read these files first, in order, so you have the design context:

1. `README.md`
2. `docs/design_decisions.md`
3. `docs/pipeline.md`

Then read the two working scripts to understand the style I'm working in:

4. `scripts/yt_transcribe.py`
5. `scripts/transcribe_playlist.py`

Once you have the context, please do the following setup tasks:

1. **Initialise git** with `main` as the default branch.
2. **Write a `.gitignore`** appropriate for Python projects. It should
   exclude:
   - Standard Python artefacts (`__pycache__/`, `*.pyc`, `.venv/`,
     `*.egg-info/`, `dist/`, `build/`)
   - Whisper model cache (`.cache/whisper/` if present, and audio files
     `*.m4a`, `*.webm`, `*.mp3`, `*.wav`)
   - Generated chapter content (`chapters/*/source/transcript.txt`,
     `chapters/*/source/*.m4a`, etc.) but KEEP the directory structure
     and `metadata.yaml` files
   - The book_index.json scaffold should be tracked, but generated
     `chapters/playlist_index.json` can be tracked too (it's useful
     for resume)
   - IDE files (`.vscode/`, `.idea/`)
   - OS files (`.DS_Store`, `Thumbs.db`)
3. **Create `pyproject.toml`** with:
   - Python 3.11+ requirement
   - Dependencies: `openai-whisper`, `yt-dlp`, `torch` (with CUDA hint
     in a comment for the GPU workstation)
   - Optional dev dependencies: `pytest`, `ruff`
   - Project name: `claude-academy-book`
   - Brief project description from the README
4. **Add a `chapters/.gitkeep`** so the directory survives a clone even
   when empty.
5. **First commit** with message like "Initial scaffold: transcription
   pipeline + design docs".

After that, stop and confirm everything looks right before we start on
the next pipeline step (`extract_summary.py`). Do not start step 2 work
until I give the go-ahead.

A few preferences worth knowing upfront:

- **No em-dashes anywhere.** Anywhere I see one I'll ask you to fix it.
  Use commas, colons, or full stops instead.
- **Direct technical voice.** Skip empty intensifiers ("really",
  "very", "quite"). Skip filler ("In order to", "It is important to
  note"). Get to the point.
- **Markdown-first.** No `.docx` unless I explicitly ask. Reports,
  outlines, summaries: markdown.
- **Substance over process.** When you're about to suggest a meeting
  about something, don't. Just do the thing or ask the one question
  that's blocking you.

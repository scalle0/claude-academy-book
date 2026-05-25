#!/usr/bin/env python3
"""
yt_transcribe.py
================

Transcribe a YouTube video (up to ~45 minutes) to a plain .txt file using
openai-whisper.

Pipeline
--------
1. Download audio-only stream with yt-dlp (m4a, no re-encoding when possible).
2. Run openai-whisper on the audio file.
3. Write a plain-text transcript next to the audio, or to the path given by --out.

Why audio-only?
---------------
For a 45-minute talk, the audio is typically 30-60 MB while the video is
500 MB or more. Whisper only needs the audio, so we skip the video entirely.

Dependencies
------------
- Python 3.10+
- ffmpeg on PATH (required by both yt-dlp and whisper)
- pip install -U yt-dlp openai-whisper

GPU is used automatically if a CUDA-capable PyTorch is installed; otherwise
falls back to CPU. The 'large-v3' model on a recent GPU transcribes a 45-min
talk in under two minutes. On CPU expect 10-20x real time for 'small' and
slower for 'medium' or 'large'.

Usage
-----
    python yt_transcribe.py <youtube_url>
    python yt_transcribe.py <url> --model medium --language en
    python yt_transcribe.py <url> --out talk.txt --keep-audio
    python yt_transcribe.py <url> --prompt "Claude Code, MCP, KV cache, Anthropic"

The --prompt flag biases Whisper toward domain vocabulary. This is how you
prevent "Claude" being transcribed as "Cloud", for example.

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ----------------------------------------------------------------------
# Audio download
# ----------------------------------------------------------------------

def download_audio(url: str, workdir: Path) -> tuple[Path, str]:
    """
    Download audio-only stream and return (audio_path, video_title).

    Uses yt-dlp's bestaudio format. Output is whatever container the source
    provides (typically .m4a or .webm). Whisper handles both via ffmpeg.
    """
    out_template = str(workdir / "%(id)s.%(ext)s")

    # Use yt-dlp as a library if available; fall back to subprocess otherwise.
    try:
        import yt_dlp  # type: ignore
    except ImportError:
        sys.exit(
            "yt-dlp is not installed. Install with:\n"
            "    pip install -U yt-dlp"
        )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        # Reject anything obviously too long so we do not silently transcribe
        # a 4-hour livestream. 45 min + a small buffer.
        "match_filter": _duration_limit(seconds=60 * 50),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # yt-dlp may wrap a single video in a playlist-shaped dict.
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        audio_path = Path(ydl.prepare_filename(info))
        title = info.get("title") or info.get("id") or "transcript"

    if not audio_path.exists():
        # Some formats are post-processed to a different extension.
        # Grab whatever single audio file landed in workdir.
        candidates = [p for p in workdir.iterdir() if p.is_file()]
        if not candidates:
            sys.exit("yt-dlp reported success but no audio file was produced.")
        audio_path = candidates[0]

    return audio_path, title


def _duration_limit(seconds: int):
    """Return a yt-dlp match_filter that rejects videos longer than `seconds`."""
    def _filter(info_dict, *, incomplete=False):  # noqa: ARG001
        duration = info_dict.get("duration")
        if duration is not None and duration > seconds:
            return (
                f"Video is {duration // 60} min long; this script is scoped "
                f"to <= {seconds // 60} min. Use a longer-form pipeline if you "
                f"really need the whole thing."
            )
        return None
    return _filter


# ----------------------------------------------------------------------
# Transcription
# ----------------------------------------------------------------------

def transcribe(
    audio_path: Path,
    model_name: str,
    language: str | None,
    initial_prompt: str | None,
) -> tuple[str, str]:
    """
    Run openai-whisper on `audio_path` and return (text, detected_language).

    `detected_language` is the ISO-639-1 code Whisper either was told to use
    (when `language` was set) or detected itself. It is used downstream to
    pick the right language-specific replacement rules.

    Notes
    -----
    - We deliberately do not use word_timestamps. Plain text only.
    - condition_on_previous_text is left at default (True), which usually
      gives better continuity at the cost of occasional drift on long files.
    """
    try:
        import whisper  # type: ignore
    except ImportError:
        sys.exit(
            "openai-whisper is not installed. Install with:\n"
            "    pip install -U openai-whisper"
        )

    device = _pick_device()
    model = ensure_model(whisper, model_name, device)

    if language:
        print(f"Transcribing {audio_path.name}  (language: {language}) ...", flush=True)
    else:
        print(f"Transcribing {audio_path.name}  (auto-detecting language) ...", flush=True)
    result = model.transcribe(
        str(audio_path),
        language=language,            # None = auto-detect
        initial_prompt=initial_prompt, # bias toward domain vocabulary
        verbose=False,                 # set True for per-segment progress
        fp16=(device == "cuda"),       # fp16 only on GPU
    )

    text = result.get("text", "").strip()
    if not text:
        sys.exit("Whisper returned an empty transcript. Check the audio.")

    # Whisper sets result["language"] to the code it actually used.
    detected = (result.get("language") or language or "").lower()
    if not language and detected:
        print(f"Detected language: {detected}", flush=True)

    return text, detected


# ----------------------------------------------------------------------
# Model lifecycle: cache lookup, download with progress, load reporting
# ----------------------------------------------------------------------

# Approximate on-disk sizes of Whisper checkpoints (informational only).
# Source: openai-whisper README. Sizes vary slightly by version.
_MODEL_SIZE_HINT_MB: dict[str, int] = {
    "tiny":     75,
    "base":    140,
    "small":   460,
    "medium": 1500,
    "large":  2900,
    "large-v2": 2900,
    "large-v3": 2900,
}


def ensure_model(whisper_mod, model_name: str, device: str):
    """
    Make sure the Whisper checkpoint is present, then load it.

    Steps
    -----
    1. Resolve the cache directory openai-whisper will use.
    2. Check whether the .pt file is already cached. If so, just load it.
    3. If not, announce the download (with expected size), then let
       whisper.load_model do the actual fetch. openai-whisper streams the
       file with a built-in tqdm progress bar over stderr, which will be
       visible to the user.
    4. After loading, report parameter count and which device it landed on.

    The function returns the loaded model object.
    """
    import os

    # openai-whisper honors XDG_CACHE_HOME / ~/.cache/whisper by default,
    # but exposes _MODELS_DIR-style logic via whisper._download. The public
    # entry point load_model() accepts a download_root, so we resolve the
    # same path ourselves for the cache check.
    cache_root = Path(
        os.environ.get("WHISPER_CACHE_DIR")
        or os.path.join(os.path.expanduser("~"), ".cache", "whisper")
    )
    cache_root.mkdir(parents=True, exist_ok=True)

    # openai-whisper names files <model>.pt
    expected_path = cache_root / f"{model_name}.pt"

    if expected_path.exists():
        actual_mb = expected_path.stat().st_size / (1024 * 1024)
        print(
            f"Whisper model '{model_name}' already cached at "
            f"{expected_path} ({actual_mb:.0f} MB).",
            flush=True,
        )
    else:
        hint = _MODEL_SIZE_HINT_MB.get(model_name)
        size_str = f"~{hint} MB" if hint else "size unknown"
        print(
            f"Whisper model '{model_name}' not in cache. Downloading "
            f"({size_str}) to {cache_root} ...",
            flush=True,
        )
        print(
            "  (openai-whisper will show its own progress bar below.)",
            flush=True,
        )

    print(f"Loading '{model_name}' on {device} ...", flush=True)
    try:
        model = whisper_mod.load_model(
            model_name,
            device=device,
            download_root=str(cache_root),
        )
    except Exception as exc:
        # Most common cause here is a partial download leaving a corrupt
        # .pt file. Point the user at the fix instead of dumping a traceback.
        if expected_path.exists():
            sys.exit(
                f"Failed to load '{model_name}' from cache: {exc}\n"
                f"The cached file may be corrupt. Remove it and rerun:\n"
                f"    rm {expected_path}"
            )
        sys.exit(f"Failed to download or load '{model_name}': {exc}")

    # Confirm what we actually got. dims.n_vocab is a cheap sanity check
    # that we are talking to a real Whisper model.
    try:
        n_params = sum(p.numel() for p in model.parameters())
        actual_device = next(model.parameters()).device
        print(
            f"Model ready: {n_params/1e6:.0f}M params on {actual_device}.",
            flush=True,
        )
    except Exception:
        # If introspection fails we still have the model; do not abort.
        print(f"Model ready on {device}.", flush=True)

    return model


def _pick_device() -> str:
    try:
        import torch  # type: ignore
    except ImportError:
        return "cpu"
    if torch.cuda.is_available():
        return "cuda"
    # Apple Silicon: MPS works for inference but is sometimes flaky with
    # Whisper's larger models. Keep it opt-in via env var if needed.
    return "cpu"


# ----------------------------------------------------------------------
# Post-processing: domain-specific substitutions
# ----------------------------------------------------------------------

# Built-in substitutions, organised by language.
# "common" rules apply to every language; this covers domain acronyms and
# names that get mis-heard in any source language (Anthropic / Claude vocab,
# capitalised acronyms, etc.). Per-language buckets hold rules tuned to
# typical Whisper artefacts in that language.
#
# Order matters within each bucket: longer / more specific patterns first.
# Each key is a regex (case-insensitive). Values can be strings or callables.
DEFAULT_REPLACEMENTS: dict[str, dict[str, object]] = {
    # Always applied, regardless of source language.
    "common": {
        r"cloud\s*code":         "Claude Code",
        r"\bcloud\b":            "Claude",        # bare "Cloud" -> "Claude"
        r"\bquad\.md\b":         "claude.md",
        r"\bquad\b":             "Claude",
        r"\banthropic\b":        "Anthropic",
        r"\bmcp\b":              "MCP",
        r"\bllm[s]?\b":          lambda m: m.group(0).upper(),  # llm -> LLM
        r"\bkv\s+cache\b":       "KV cache",
        r"\bicl\b":              "ICL",
        r"\blsp\b":              "LSP",
        r"\bci(\s*\/\s*|\s+and\s+|\s+en\s+|\s+et\s+)cd\b": "CI/CD",
        r"\bvs\s*code\b":        "VS Code",
        r"\bvim\b":              "Vim",
    },

    # English-specific rules.
    "en": {
        # (Nothing extra for now; common rules cover the main Anthropic
        # talk vocabulary. Add English-only fixes here.)
    },

    # Dutch-specific rules. Steven's local context: UGent, UZ Gent, BCFI,
    # RIZIV, HGR/CSS, BSIM, and common Dutch medical terms Whisper mangles.
    "nl": {
        r"\buz\s*gent\b":              "UZ Gent",
        r"\bu\s*gent\b":               "UGent",
        r"\briziv\b":                  "RIZIV",
        r"\bbcfi\b":                   "BCFI",
        r"\bbsim\b":                   "BSIM",
        r"\bhgr\b":                    "HGR",
        r"\bcss\b":                    "CSS",
        r"\bbapcoc\b":                 "BAPCOC",
        r"\bcovid[\s\-]?19\b":         "COVID-19",
        r"\bsars[\s\-]?cov[\s\-]?2\b": "SARS-CoV-2",
        r"\bhiv\b":                    "HIV",
        r"\btbc?\b":                   "TB",            # 'TBC' or 'TB' -> TB
        r"\bdrc\b":                    "DRC",
    },

    # French-specific rules.
    "fr": {
        r"\bcovid[\s\-]?19\b":         "COVID-19",
        r"\bsars[\s\-]?cov[\s\-]?2\b": "SARS-CoV-2",
        r"\bvih\b":                    "VIH",
        r"\boms\b":                    "OMS",
        r"\binserm\b":                 "Inserm",
        r"\bch[ru]\b":                 lambda m: m.group(0).upper(),  # CHU, CHR
    },

    # Stubs so the language is recognised. Extend as you collect mistakes.
    "de": {},
    "es": {},
    "it": {},
    "pt": {},
}


def build_default_rules(language: str | None) -> dict[str, object]:
    """
    Merge 'common' rules with rules for the requested language.

    Returns an ordered dict where common rules come first (they cover
    domain acronyms that apply everywhere), followed by language-specific
    rules (which may override common ones if needed).

    If `language` is None or unknown, only common rules are returned.
    """
    rules: dict[str, object] = dict(DEFAULT_REPLACEMENTS["common"])
    if language:
        lang_rules = DEFAULT_REPLACEMENTS.get(language.lower())
        if lang_rules:
            rules.update(lang_rules)
    return rules


def find_auto_replacements_file(language: str | None, script_dir: Path) -> Path | None:
    """
    Look for a user replacements file matching the current language.

    Convention: rules_<lang>.txt next to the script (e.g. rules_nl.txt,
    rules_fr.txt). Returns the path if it exists, else None.

    This lets users maintain per-language rule files without having to
    pass --replacements every run.
    """
    if not language:
        return None
    candidate = script_dir / f"rules_{language.lower()}.txt"
    return candidate if candidate.exists() else None


def load_replacements_file(path: Path) -> dict[str, object]:
    """
    Parse a replacements file. Format: one rule per line,

        pattern => replacement

    Lines starting with '#' and blank lines are ignored. Patterns are
    regex, applied case-insensitively. Returns just the file's rules,
    without any defaults (the caller decides how to merge them).
    """
    if not path.exists():
        sys.exit(f"Replacements file not found: {path}")
    rules: dict[str, object] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=>" not in line:
            sys.exit(f"{path}:{lineno}: expected 'pattern => replacement'")
        pat, repl = (s.strip() for s in line.split("=>", 1))
        if not pat:
            sys.exit(f"{path}:{lineno}: empty pattern")
        rules[pat] = repl
    return rules


# Kept for backward compatibility with the earlier ensure_model tests.
def load_replacements(custom_path: Path | None) -> dict[str, object]:
    """
    Build a rules dict: common defaults + optional user file.
    Language-aware loading is done in main(); this helper is kept for
    callers (and tests) that just want 'common + a file'.
    """
    rules = dict(DEFAULT_REPLACEMENTS["common"])
    if custom_path is None:
        return rules
    rules.update(load_replacements_file(custom_path))
    return rules


def apply_replacements(text: str, rules: dict[str, object]) -> tuple[str, int]:
    """
    Apply substitution rules to `text`. Returns (new_text, total_changes).
    Patterns are matched case-insensitively. Regex compile errors are
    surfaced with the offending pattern so they are easy to fix.
    """
    total = 0
    out = text
    for pattern, replacement in rules.items():
        try:
            compiled = re.compile(pattern, flags=re.IGNORECASE)
        except re.error as exc:
            sys.exit(f"Bad regex in replacements: {pattern!r}: {exc}")
        out, n = compiled.subn(replacement, out)
        total += n
    return out, total


# ----------------------------------------------------------------------
# Output formatting
# ----------------------------------------------------------------------

def format_paragraphs(raw_text: str) -> str:
    """
    Whisper returns one long line. Insert paragraph breaks at sentence
    boundaries every ~3-5 sentences so the .txt is readable.
    """
    # Split into sentences on .?! followed by whitespace + uppercase or end.
    sentences = re.split(r"(?<=[\.\?\!])\s+(?=[A-Z\"\u201C])", raw_text.strip())
    if len(sentences) <= 3:
        return raw_text.strip() + "\n"

    paragraphs: list[str] = []
    buf: list[str] = []
    for sentence in sentences:
        buf.append(sentence.strip())
        # New paragraph every 4 sentences as a reasonable default.
        if len(buf) >= 4:
            paragraphs.append(" ".join(buf))
            buf = []
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(paragraphs) + "\n"


def safe_filename(title: str) -> str:
    """Make a filesystem-safe filename from a YouTube title."""
    cleaned = re.sub(r"[^\w\s\-\.]", "", title).strip()
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned[:120] or "transcript"


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Transcribe a YouTube video to plain text with openai-whisper."
    )
    ap.add_argument("url", help="YouTube video URL")
    ap.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model size. Default: medium. Use large-v3 for best quality.",
    )
    ap.add_argument(
        "--language",
        default=None,
        help=(
            "Language code (e.g. 'en', 'nl', 'fr', 'de'). Default: auto-detect "
            "from the first 30 seconds of audio. The detected (or specified) "
            "language also selects language-specific built-in fix-ups and "
            "any matching rules_<lang>.txt file next to this script."
        ),
    )
    ap.add_argument(
        "--prompt",
        default=None,
        help=(
            "Optional initial prompt to bias the decoder toward domain "
            "vocabulary (e.g. 'Claude Code, MCP, KV cache'). Should be in "
            "the same language as the audio."
        ),
    )
    ap.add_argument(
        "--out",
        default=None,
        type=Path,
        help="Output .txt path. Default: <video_title>.txt in current directory.",
    )
    ap.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep the downloaded audio file next to the transcript.",
    )
    ap.add_argument(
        "--no-fixups",
        action="store_true",
        help=(
            "Disable the built-in domain substitutions (both common and "
            "language-specific). Auto-discovered rules_<lang>.txt files "
            "and --replacements are still applied."
        ),
    )
    ap.add_argument(
        "--replacements",
        type=Path,
        default=None,
        help=(
            "Path to a plain-text file with extra substitutions, one per line "
            "in the form 'pattern => replacement'. Patterns are regex, "
            "case-insensitive. Applied last, so user rules override built-ins."
        ),
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit(
            "ffmpeg was not found on PATH. Install it first:\n"
            "  macOS:  brew install ffmpeg\n"
            "  Ubuntu: sudo apt install ffmpeg\n"
            "  Windows: winget install ffmpeg"
        )

    with tempfile.TemporaryDirectory(prefix="yt_transcribe_") as tmp:
        workdir = Path(tmp)
        audio_path, title = download_audio(args.url, workdir)
        print(f"Downloaded audio: {audio_path.name}  ({_size_mb(audio_path):.1f} MB)")

        raw_text, detected_lang = transcribe(
            audio_path=audio_path,
            model_name=args.model,
            language=args.language,
            initial_prompt=args.prompt,
        )

        # ---- Assemble language-aware substitution rules ----
        # Priority (low to high; later rules override earlier ones):
        #   1. Common defaults  (always, unless --no-fixups)
        #   2. Language-specific defaults for `detected_lang` (unless --no-fixups)
        #   3. Auto-discovered rules_<lang>.txt next to this script
        #   4. Explicit --replacements file
        # `detected_lang` reflects either --language or Whisper's auto-detection.
        if args.no_fixups:
            rules: dict[str, object] = {}
        else:
            rules = build_default_rules(detected_lang)

        script_dir = Path(__file__).resolve().parent
        auto_file = find_auto_replacements_file(detected_lang, script_dir)
        if auto_file is not None:
            print(f"Auto-loading language rules from {auto_file.name}")
            rules.update(load_replacements_file(auto_file))

        if args.replacements is not None:
            rules.update(load_replacements_file(args.replacements))

        if rules:
            cleaned, n_changes = apply_replacements(raw_text, rules)
            if n_changes:
                print(f"Applied {n_changes} domain fix-up(s).")
        else:
            cleaned = raw_text

        formatted = format_paragraphs(cleaned)

        out_path = args.out or Path.cwd() / f"{safe_filename(title)}.txt"
        out_path.write_text(formatted, encoding="utf-8")
        print(f"\nTranscript written to: {out_path}")
        print(f"  characters: {len(formatted):,}")
        print(f"  words (approx): {len(formatted.split()):,}")

        if args.keep_audio:
            kept = out_path.with_suffix(audio_path.suffix)
            shutil.copy2(audio_path, kept)
            print(f"  audio kept at: {kept}")


def _size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted.")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"\nSubprocess failed: {exc}")

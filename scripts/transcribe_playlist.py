#!/usr/bin/env python3
"""
transcribe_playlist.py
======================

Iterate a YouTube playlist (or channel URL) and transcribe each video
into its own chapter folder under ./chapters/<slug>/.

Per video, the layout is:

    chapters/<slug>/
      source/
        transcript.txt        <- output of yt_transcribe.py
      metadata.yaml           <- video id, title, duration, URL, upload date

A top-level playlist_index.json tracks state across runs so the script
can resume after interruptions and skip already-completed videos.

Pipeline
--------
1. yt-dlp enumerates the playlist with --flat-playlist (one HTTP call,
   no downloads), returning title + id + duration for every entry.
2. Filter out videos longer than --max-duration (default 50 minutes,
   matching yt_transcribe.py's own hard limit).
3. For each remaining video, shell out to yt_transcribe.py with the
   per-chapter output path. Unknown flags on this script are forwarded
   verbatim, so --model, --language, --prompt etc. all work as expected.
4. Write metadata.yaml. Update playlist_index.json. Move on.

Usage
-----
    # Process a playlist with default settings
    python transcribe_playlist.py <playlist_url>

    # Use the big model and bias toward Anthropic vocabulary
    python transcribe_playlist.py <playlist_url> \\
        --model large-v3 \\
        --language en \\
        --prompt "Claude Code, MCP, Anthropic, KV cache"

    # Re-run: skips anything in playlist_index.json with status 'done'
    python transcribe_playlist.py <playlist_url>

    # Re-run and retry failed videos as well
    python transcribe_playlist.py <playlist_url> --retry-failed

Author: built for Steven Callens.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

# Default location of yt_transcribe.py relative to this script.
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TRANSCRIBER = SCRIPT_DIR / "yt_transcribe.py"
DEFAULT_CHAPTERS_DIR = Path("chapters")
DEFAULT_MAX_SECONDS = 50 * 60   # 50 min, same ceiling as yt_transcribe.py
INDEX_FILENAME = "playlist_index.json"


# ----------------------------------------------------------------------
# Playlist enumeration
# ----------------------------------------------------------------------

def enumerate_playlist(url: str) -> list[dict]:
    """
    Return a list of {id, title, duration, url} dicts for every video in
    the playlist or channel at `url`. Uses yt-dlp's --flat-playlist mode,
    which does one network call and downloads nothing.
    """
    try:
        import yt_dlp  # type: ignore
    except ImportError:
        sys.exit("yt-dlp not installed. Install with: pip install -U yt-dlp")

    ydl_opts = {
        "extract_flat": True,    # don't resolve individual videos
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    entries = info.get("entries") or []
    out: list[dict] = []
    for e in entries:
        if not e or not e.get("id"):
            continue
        out.append({
            "id": e["id"],
            "title": e.get("title") or e["id"],
            "duration": e.get("duration"),  # may be None on flat-playlist
            "url": e.get("url") or f"https://www.youtube.com/watch?v={e['id']}",
            "upload_date": e.get("upload_date"),  # YYYYMMDD or None
        })
    return out


# ----------------------------------------------------------------------
# Slug generation
# ----------------------------------------------------------------------

def make_slug(title: str, video_id: str, max_len: int = 60) -> str:
    """
    Produce a filesystem-safe, lowercase, hyphen-separated slug from a
    video title. Falls back to the video id if the title is empty after
    cleaning, so we always get something.
    """
    # Normalise unicode (handle accented characters, emoji)
    s = unicodedata.normalize("NFKD", title)
    s = s.encode("ascii", "ignore").decode("ascii")
    # Lowercase
    s = s.lower()
    # Replace any run of non-alphanumeric with a single hyphen
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # Strip leading/trailing hyphens
    s = s.strip("-")
    # Truncate
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or video_id.lower()


# ----------------------------------------------------------------------
# Index (state across runs)
# ----------------------------------------------------------------------

def load_index(path: Path) -> dict:
    """Load the playlist index, or return an empty skeleton."""
    if not path.exists():
        return {"created": _now_iso(), "videos": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit(f"Corrupt index at {path}: {exc}\nDelete the file to start fresh.")


def save_index(index: dict, path: Path) -> None:
    """Write the index atomically."""
    index["updated"] = _now_iso()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ----------------------------------------------------------------------
# Metadata file
# ----------------------------------------------------------------------

def write_metadata(chapter_dir: Path, entry: dict, slug: str) -> None:
    """
    Write a tiny YAML file with video metadata. We hand-write it instead
    of pulling in PyYAML so the script has no extra dependencies beyond
    what yt_transcribe.py already needs.
    """
    upload = entry.get("upload_date") or ""
    if upload and len(upload) == 8:
        upload = f"{upload[:4]}-{upload[4:6]}-{upload[6:8]}"

    duration = entry.get("duration")
    duration_str = _format_duration(duration) if duration else "unknown"

    lines = [
        f"slug: {slug}",
        f"video_id: {entry['id']}",
        f"title: {_yaml_quote(entry['title'])}",
        f"url: {entry['url']}",
        f"upload_date: {upload}",
        f"duration_seconds: {duration if duration is not None else 'null'}",
        f"duration_human: {duration_str}",
        f"transcribed_at: {_now_iso()}",
        "",
    ]
    (chapter_dir / "metadata.yaml").write_text("\n".join(lines), encoding="utf-8")


def _yaml_quote(s: str) -> str:
    """Minimal YAML string quoting: wrap in double quotes, escape inner quotes."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _format_duration(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


# ----------------------------------------------------------------------
# Transcriber invocation
# ----------------------------------------------------------------------

def run_transcriber(
    transcriber: Path,
    url: str,
    output_path: Path,
    passthrough: list[str],
) -> bool:
    """
    Shell out to yt_transcribe.py for one video. Return True on success.

    We forward unknown flags from this script's own argv as passthrough
    so users can control --model, --language, --prompt, etc. without
    this driver knowing about them individually.
    """
    cmd = [
        sys.executable, str(transcriber),
        url,
        "--out", str(output_path),
        *passthrough,
    ]
    print(f"\n>>> Transcribing -> {output_path}")
    print(f"    cmd: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> tuple[argparse.Namespace, list[str]]:
    """
    Parse our own flags, return (known_args, passthrough_args).

    Anything we don't recognise is treated as a flag for yt_transcribe.py
    and forwarded verbatim. This keeps us decoupled from the transcriber's
    evolving CLI.
    """
    ap = argparse.ArgumentParser(
        description=(
            "Transcribe a YouTube playlist or channel into per-chapter folders. "
            "Unknown flags are forwarded to yt_transcribe.py."
        )
    )
    ap.add_argument("url", help="YouTube playlist or channel URL")
    ap.add_argument(
        "--chapters-dir",
        type=Path,
        default=DEFAULT_CHAPTERS_DIR,
        help=f"Root directory for chapter folders. Default: ./{DEFAULT_CHAPTERS_DIR}",
    )
    ap.add_argument(
        "--transcriber",
        type=Path,
        default=DEFAULT_TRANSCRIBER,
        help=f"Path to yt_transcribe.py. Default: {DEFAULT_TRANSCRIBER}",
    )
    ap.add_argument(
        "--max-duration",
        type=int,
        default=DEFAULT_MAX_SECONDS,
        help=(
            f"Skip videos longer than this many seconds. Default: "
            f"{DEFAULT_MAX_SECONDS} ({DEFAULT_MAX_SECONDS // 60} min)."
        ),
    )
    ap.add_argument(
        "--retry-failed",
        action="store_true",
        help="Re-attempt videos previously marked 'failed' in the index.",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would happen; do not download or transcribe anything.",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most N videos this run (after filtering). Useful for testing.",
    )
    return ap.parse_known_args()


def main() -> None:
    args, passthrough = parse_args()

    if not args.transcriber.exists():
        sys.exit(f"Transcriber not found at {args.transcriber}")

    args.chapters_dir.mkdir(parents=True, exist_ok=True)
    index_path = args.chapters_dir / INDEX_FILENAME
    index = load_index(index_path)

    print(f"Enumerating playlist: {args.url}")
    videos = enumerate_playlist(args.url)
    print(f"Playlist contains {len(videos)} videos.")

    # ---- Classify each video ----
    plan: list[tuple[dict, str, str]] = []   # (entry, slug, status_reason)
    for entry in videos:
        slug = make_slug(entry["title"], entry["id"])
        prior = index["videos"].get(entry["id"], {})
        prior_status = prior.get("status")

        # Already done? Skip.
        if prior_status == "done" and not args.retry_failed:
            continue
        if prior_status == "failed" and not args.retry_failed:
            plan.append((entry, slug, "skipped-prior-failure"))
            continue

        # Too long?
        dur = entry.get("duration")
        if dur is not None and dur > args.max_duration:
            plan.append((entry, slug, f"too-long-{dur}s"))
            continue

        plan.append((entry, slug, "queued"))

    queued = [p for p in plan if p[2] == "queued"]
    skipped = [p for p in plan if p[2] != "queued"]
    already = len(videos) - len(plan)

    print(f"  already done: {already}")
    print(f"  queued:       {len(queued)}")
    print(f"  skipped:      {len(skipped)}")
    for entry, slug, reason in skipped:
        print(f"    - [{reason}] {entry['title'][:60]}")

    if args.limit is not None:
        queued = queued[: args.limit]
        print(f"\nLimiting to first {len(queued)} of queued (--limit).")

    if args.dry_run:
        print("\nDry run; nothing transcribed.")
        for entry, slug, _ in queued:
            print(f"  would transcribe: {slug:60s}  {entry['url']}")
        return

    # ---- Process queued videos ----
    n_ok = 0
    n_fail = 0
    for i, (entry, slug, _) in enumerate(queued, 1):
        print(f"\n[{i}/{len(queued)}] {entry['title']}")
        chapter_dir = args.chapters_dir / slug
        source_dir = chapter_dir / "source"
        source_dir.mkdir(parents=True, exist_ok=True)
        transcript_path = source_dir / "transcript.txt"

        # Record attempt before running, so a crash leaves a trace.
        index["videos"][entry["id"]] = {
            "slug": slug,
            "title": entry["title"],
            "url": entry["url"],
            "status": "in-progress",
            "attempted_at": _now_iso(),
        }
        save_index(index, index_path)

        ok = run_transcriber(
            transcriber=args.transcriber,
            url=entry["url"],
            output_path=transcript_path,
            passthrough=passthrough,
        )

        if ok and transcript_path.exists() and transcript_path.stat().st_size > 0:
            write_metadata(chapter_dir, entry, slug)
            index["videos"][entry["id"]]["status"] = "done"
            index["videos"][entry["id"]]["transcript"] = str(transcript_path)
            n_ok += 1
        else:
            index["videos"][entry["id"]]["status"] = "failed"
            n_fail += 1

        index["videos"][entry["id"]]["finished_at"] = _now_iso()
        save_index(index, index_path)

    print(f"\nDone. {n_ok} transcribed, {n_fail} failed.")
    print(f"Index: {index_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted. Re-run to resume; completed videos will be skipped.")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"\nSubprocess failed: {exc}")

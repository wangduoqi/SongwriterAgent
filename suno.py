"""
Suno API command-line client.

Currently a STUB implementation - generates placeholder files.
Replace the three functions (submit/status/download) when you have real Suno API access.

Usage:
  python suno.py submit --lyrics-file PATH --style-file PATH
  python suno.py submit --lyrics-file PATH --style "city pop, female vocal"
  python suno.py status <job_id>
  python suno.py download <job_id> --out PATH

Job state is persisted to .suno_jobs.json so you can check status across runs.
"""
import argparse
import json
import sys
import time
import uuid
from pathlib import Path

JOBS_FILE = Path(__file__).parent / ".suno_jobs.json"


def _load_jobs() -> dict:
    if JOBS_FILE.exists():
        return json.loads(JOBS_FILE.read_text(encoding="utf-8"))
    return {}


def _save_jobs(jobs: dict) -> None:
    JOBS_FILE.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")


def _read_text(path_or_inline: str, file_arg: str | None) -> str:
    """Resolve a value from either --x or --x-file."""
    if file_arg:
        return Path(file_arg).read_text(encoding="utf-8").strip()
    if path_or_inline:
        return path_or_inline
    return ""


# --- Commands ---

def cmd_submit(args) -> int:
    lyrics = _read_text(args.lyrics, args.lyrics_file)
    style = _read_text(args.style, args.style_file)
    if not lyrics:
        print("ERROR: lyrics required (--lyrics or --lyrics-file)", file=sys.stderr)
        return 1
    if not style:
        print("ERROR: style required (--style or --style-file)", file=sys.stderr)
        return 1

    job_id = f"stub_{uuid.uuid4().hex[:10]}"
    jobs = _load_jobs()
    jobs[job_id] = {
        "submitted_at": time.time(),
        "lyrics": lyrics,
        "style": style,
        "status": "queued",
    }
    _save_jobs(jobs)

    print(json.dumps({
        "job_id": job_id,
        "status": "queued",
        "hint": f"Check status: python suno.py status {job_id}",
    }, indent=2))
    return 0


def cmd_status(args) -> int:
    jobs = _load_jobs()
    job = jobs.get(args.job_id)
    if not job:
        print(json.dumps({"error": "job not found", "job_id": args.job_id}))
        return 1

    elapsed = time.time() - job["submitted_at"]
    if elapsed < 5:
        status = "queued"
    elif elapsed < 12:
        status = "processing"
    else:
        status = "complete"
    job["status"] = status
    _save_jobs(jobs)

    print(json.dumps({
        "job_id": args.job_id,
        "status": status,
        "elapsed_seconds": round(elapsed, 1),
    }, indent=2))
    return 0


def cmd_download(args) -> int:
    jobs = _load_jobs()
    job = jobs.get(args.job_id)
    if not job:
        print(json.dumps({"error": "job not found", "job_id": args.job_id}))
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # STUB: write a text placeholder where the mp3 would go.
    # Real impl would download the audio file from Suno's CDN URL.
    out.write_text(
        f"[STUB AUDIO PLACEHOLDER]\n"
        f"job_id: {args.job_id}\n"
        f"style: {job['style']}\n\n"
        f"=== lyrics ===\n{job['lyrics']}\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "job_id": args.job_id,
        "path": str(out.resolve()),
        "size_bytes": out.stat().st_size,
        "note": "STUB: file is a text placeholder, not real audio",
    }, indent=2))
    return 0


def cmd_list(args) -> int:
    """Bonus: list all known jobs."""
    jobs = _load_jobs()
    if not jobs:
        print("(no jobs)")
        return 0
    for jid, j in sorted(jobs.items(), key=lambda kv: kv[1]["submitted_at"]):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(j["submitted_at"]))
        style = j["style"][:50]
        print(f"  {jid}  [{j['status']:<10}]  {ts}  {style}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Suno API CLI (stub)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_submit = sub.add_parser("submit", help="submit a new generation job")
    p_submit.add_argument("--lyrics", help="lyrics inline")
    p_submit.add_argument("--lyrics-file", help="path to lyrics .txt")
    p_submit.add_argument("--style", help="style prompt inline")
    p_submit.add_argument("--style-file", help="path to style .txt")
    p_submit.set_defaults(func=cmd_submit)

    p_status = sub.add_parser("status", help="check job status")
    p_status.add_argument("job_id")
    p_status.set_defaults(func=cmd_status)

    p_dl = sub.add_parser("download", help="download finished audio")
    p_dl.add_argument("job_id")
    p_dl.add_argument("--out", required=True, help="output path (e.g. songs/foo/v1.mp3)")
    p_dl.set_defaults(func=cmd_download)

    p_list = sub.add_parser("list", help="list all jobs")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
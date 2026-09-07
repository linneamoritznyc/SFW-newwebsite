# sfw-clipper — full source bundle

Paste this whole file into Claude Code. Every section below is one file.
Recreate the tree exactly as the headings specify, then:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in ANTHROPIC_API_KEY at minimum
```

`ffmpeg` must be on PATH.

## Tree

```
sfw-clipper/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── clipper/
│   ├── __init__.py
│   ├── config.py
│   ├── interface.py
│   ├── transcript.py
│   ├── selection.py
│   ├── output.py
│   ├── cli.py
│   └── engines/
│       ├── __init__.py
│       ├── local.py
│       └── opus.py
└── glossary/
    └── en.yaml
```

Note: `clipper/__init__.py` and `clipper/engines/__init__.py` are empty files.

---

## `README.md`

````markdown
# sfw-clipper

Turns long-form Soil Food Web lectures into short vertical clips.

Two engines behind one `clip()` interface: the OpusClip API the Foundation
already pays for, and a self-hosted path costing pennies per hour of video.
Swapping between them is a config change. **The cost comparison is the demo.**

## What it does

```
source (URL or file)
  └─ yt-dlp ──────────── media cache        .scratch/media/
  └─ faster-whisper ──── transcript cache   .scratch/transcripts/
  └─ Claude ──────────── selection cache    .scratch/selections/
  └─ ffmpeg ──────────── rendered clips     .scratch/rendered/
  └─ publish ─────────── OUTPUT_ROOT/pending/clips/{source}/{lang}/
                         + manifest.json
```

Transcription and selection are cached **separately and deliberately**.
Transcription is the slow step; selection is the step you iterate on.
Re-running selection with a new prompt never re-transcribes.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in ANTHROPIC_API_KEY at minimum
```

Also needs `ffmpeg` on PATH.

## Use

```bash
python -m clipper.cli transcribe <url-or-path>
python -m clipper.cli select <url-or-path> --force   # iterate on the prompt
python -m clipper.cli run <url-or-path> --engine local
python -m clipper.cli compare <url-or-path>          # cost side by side
```

## Design decisions worth not re-litigating

**Media is never committed.** Code, config, prompts and glossary only.
See `.gitignore`.

**Clips land in `/pending/`, never published directly.** Nobody running this
pipeline can verify translated output, and the organisation's reputation is
fragile. Everything ships labelled as unreviewed machine output.

**Drive auth is a service account against a shared folder**, not OAuth on a
personal login, so handover doesn't route through anyone's individual account.

**`OUTPUT_ROOT` is the single handover switch.** Point it at
`drive:<FOLDER_ID>` for a folder the org owns and nothing else changes.

**Selection is tuned to this content, not generic virality.** The prompt in
`clipper/selection.py` prioritises self-contained mechanism explanations and
explicitly deprioritises sweeping unquantified climate and yield claims. Those
are a credibility liability for this organisation, not a hook.

**Output structure is deliberate.** The Foundation's Drive filing is a live
internal complaint, so `/clips/{source-video}/{lang}/` plus a manifest is free
credibility.

## Before the first live OpusClip run

Confirm against `developer.opus.pro/document/introduction`:

- exact v2 endpoint paths and response field names — isolated in
  `_ENDPOINTS` in `clipper/engines/opus.py`, a one-line fix
- the org's plan tier (API needs Pro Beta / Max / Business)
- credit pricing, so `OpusEngine.estimate_cost` returns a real number

Operational constraints already handled: 30 req/min, 10h max video, 30 GB max
file, and **projects expire after 30 days** — the engine always downloads
outputs rather than storing remote URLs.

## Phase two (not now)

Translated subtitles, starting with Telugu.

- Whisper's built-in translate only goes to English. Use Claude on the
  transcript instead.
- `glossary/{lang}.yaml` maps fixed technical terms to agreed renderings or
  transliterations. Versioned, correctable by a native speaker, improves every
  future clip. Arguably the real deliverable.
- Cache translations keyed on segment hash so fixing one clip doesn't
  re-translate the rest.
- Nothing goes public without a native speaker's check. RySS has hundreds of
  Telugu speakers — "ready for your team to review" is a better position than
  "done".
````

---

## `requirements.txt`

```text
anthropic>=0.40
faster-whisper>=1.0
yt-dlp>=2024.8.6
requests>=2.32
python-dotenv>=1.0
google-api-python-client>=2.140
google-auth>=2.33
PyYAML>=6.0
```

---

## `.gitignore`

```gitignore
# Media never gets committed. Code, config, prompts and glossary only.
.scratch/
output/
secrets/
*.mp4
*.mkv
*.webm
*.wav
*.m4a
.env
__pycache__/
*.pyc
.venv/
```

---

## `.env.example`

```bash
# --- engine ---------------------------------------------------------
CLIP_ENGINE=local            # local | opus

# --- paths ----------------------------------------------------------
SCRATCH_ROOT=./.scratch
# Local path, or drive:<FOLDER_ID> for a shared Drive folder the org owns.
# This single value is what makes handover clean. Change it, nothing else.
OUTPUT_ROOT=./output

# --- anthropic ------------------------------------------------------
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-6

# --- google drive (service account, not personal OAuth) --------------
GOOGLE_SERVICE_ACCOUNT_JSON=./secrets/service-account.json

# --- opusclip (key must come from the ORG's billed account) ----------
OPUS_API_KEY=
OPUS_ORG_ID=
OPUS_BASE_URL=https://api.opus.pro
OPUS_API_VERSION=v2

# --- whisper --------------------------------------------------------
WHISPER_MODEL=large-v3
WHISPER_DEVICE=auto
WHISPER_COMPUTE_TYPE=int8

# --- clip shape -----------------------------------------------------
MIN_CLIP_SECONDS=45
MAX_CLIP_SECONDS=90
CANDIDATES_REQUESTED=20
MIN_CONFIDENCE=0.6
```

---

## `clipper/__init__.py`

Empty file. Create it.

---

## `clipper/config.py`

```python
"""Central config. Every path and credential resolves here, nowhere else.

Handover rule: changing OUTPUT_ROOT and swapping the service-account JSON
should be sufficient to move this pipeline off Linnea's account entirely.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _env(key: str, default: str | None = None, required: bool = False) -> str | None:
    val = os.getenv(key, default)
    if required and not val:
        raise RuntimeError(f"Missing required env var: {key}")
    return val


@dataclass(frozen=True)
class Config:
    # --- engine selection ---------------------------------------------
    engine: str = _env("CLIP_ENGINE", "local")  # "local" | "opus"

    # --- local scratch (Minerva alumni Drive / local disk) -------------
    scratch_root: Path = Path(_env("SCRATCH_ROOT", "./.scratch"))

    # --- where finished clips land -------------------------------------
    # Single value that controls handover. Either a local path or a
    # Drive folder ID prefixed with "drive:".
    output_root: str = _env("OUTPUT_ROOT", "./output")

    # --- Google Drive (service account, NOT personal OAuth) ------------
    drive_sa_json: str | None = _env("GOOGLE_SERVICE_ACCOUNT_JSON")

    # --- Anthropic ------------------------------------------------------
    anthropic_api_key: str | None = _env("ANTHROPIC_API_KEY")
    anthropic_model: str = _env("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    # --- OpusClip -------------------------------------------------------
    opus_api_key: str | None = _env("OPUS_API_KEY")
    opus_org_id: str | None = _env("OPUS_ORG_ID")
    opus_base_url: str = _env("OPUS_BASE_URL", "https://api.opus.pro")
    opus_api_version: str = _env("OPUS_API_VERSION", "v2")

    # --- transcription --------------------------------------------------
    whisper_model: str = _env("WHISPER_MODEL", "large-v3")
    whisper_device: str = _env("WHISPER_DEVICE", "auto")
    whisper_compute_type: str = _env("WHISPER_COMPUTE_TYPE", "int8")

    # --- clip shape -----------------------------------------------------
    min_clip_seconds: float = float(_env("MIN_CLIP_SECONDS", "45"))
    max_clip_seconds: float = float(_env("MAX_CLIP_SECONDS", "90"))
    candidates_requested: int = int(_env("CANDIDATES_REQUESTED", "20"))
    min_confidence: float = float(_env("MIN_CONFIDENCE", "0.6"))

    @property
    def transcripts_dir(self) -> Path:
        return self.scratch_root / "transcripts"

    @property
    def media_dir(self) -> Path:
        return self.scratch_root / "media"

    @property
    def selections_dir(self) -> Path:
        return self.scratch_root / "selections"

    def ensure_dirs(self) -> None:
        for d in (self.transcripts_dir, self.media_dir, self.selections_dir):
            d.mkdir(parents=True, exist_ok=True)


CONFIG = Config()
```

---

## `clipper/interface.py`

```python
"""The one interface both engines implement.

Everything downstream (Drive upload, manifest, review queue) depends only
on these types, so swapping OpusClip for the self-hosted path is a config
change, not a rewrite. The cost comparison is the demo.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Protocol, Sequence


@dataclass
class Segment:
    """One transcript segment with word-level timing available upstream."""
    start: float
    end: float
    text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Transcript:
    source_id: str
    language: str
    duration: float
    segments: list[Segment] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(s.text.strip() for s in self.segments)

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "language": self.language,
            "duration": self.duration,
            "segments": [s.to_dict() for s in self.segments],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Transcript":
        return cls(
            source_id=d["source_id"],
            language=d["language"],
            duration=d["duration"],
            segments=[Segment(**s) for s in d["segments"]],
        )


@dataclass
class ClipCandidate:
    """Selection output, before any cutting happens."""
    start: float
    end: float
    hook: str
    why: str
    confidence: float

    @property
    def duration(self) -> float:
        return self.end - self.start

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Clip:
    """A cut, rendered clip on disk, not yet uploaded."""
    source_id: str
    index: int
    path: Path
    candidate: ClipCandidate
    language: str = "en"
    reviewed: bool = False
    engine: str = "unknown"

    def to_manifest_entry(self) -> dict:
        return {
            "index": self.index,
            "filename": self.path.name,
            "language": self.language,
            "start": self.candidate.start,
            "end": self.candidate.end,
            "duration": round(self.candidate.duration, 2),
            "hook": self.candidate.hook,
            "why": self.candidate.why,
            "confidence": self.candidate.confidence,
            "engine": self.engine,
            "reviewed": self.reviewed,
        }


@dataclass
class ClipResult:
    source_id: str
    engine: str
    clips: list[Clip]
    cost_usd: float | None = None
    notes: str = ""


class ClipEngine(Protocol):
    """Implemented by LocalEngine and OpusEngine."""

    name: str

    def clip(self, source: str, *, language: str = "en") -> ClipResult:
        """Take a URL or local file path, return rendered clips."""
        ...

    def estimate_cost(self, duration_seconds: float) -> float:
        """Best-effort USD estimate for one video. Drives the comparison."""
        ...


def get_engine(name: str) -> ClipEngine:
    if name == "local":
        from .engines.local import LocalEngine
        return LocalEngine()
    if name == "opus":
        from .engines.opus import OpusEngine
        return OpusEngine()
    raise ValueError(f"Unknown engine: {name!r} (expected 'local' or 'opus')")
```

---

## `clipper/transcript.py`

```python
"""Transcription and its cache.

Transcription is the slow step; selection is the step that gets iterated on.
They are cached separately and deliberately: re-running selection with a new
prompt must never re-transcribe.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from .config import CONFIG
from .interface import Segment, Transcript


def source_id(source: str) -> str:
    """Stable, filesystem-safe ID for a URL or path."""
    h = hashlib.sha256(source.encode()).hexdigest()[:12]
    stem = Path(source).stem if not source.startswith("http") else "remote"
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in stem)[:40]
    return f"{safe}-{h}".strip("-")


def fetch_media(source: str) -> Path:
    """Download with yt-dlp if a URL, otherwise pass the local path through."""
    CONFIG.ensure_dirs()
    if not source.startswith("http"):
        p = Path(source)
        if not p.exists():
            raise FileNotFoundError(source)
        return p

    sid = source_id(source)
    target = CONFIG.media_dir / f"{sid}.mp4"
    if target.exists():
        return target

    subprocess.run(
        [
            "yt-dlp",
            "-f", "bv*[height<=1080]+ba/b[height<=1080]",
            "--merge-output-format", "mp4",
            "-o", str(target),
            source,
        ],
        check=True,
    )
    return target


def _cache_path(sid: str) -> Path:
    return CONFIG.transcripts_dir / f"{sid}.json"


def load_cached(sid: str) -> Transcript | None:
    p = _cache_path(sid)
    if not p.exists():
        return None
    return Transcript.from_dict(json.loads(p.read_text()))


def save_cached(t: Transcript) -> Path:
    CONFIG.ensure_dirs()
    p = _cache_path(t.source_id)
    p.write_text(json.dumps(t.to_dict(), ensure_ascii=False, indent=2))
    return p


def transcribe(source: str, *, language: str | None = None,
               force: bool = False) -> Transcript:
    """faster-whisper large-v3 with word timestamps, cached to disk."""
    sid = source_id(source)
    if not force:
        cached = load_cached(sid)
        if cached:
            return cached

    from faster_whisper import WhisperModel

    media = fetch_media(source)
    model = WhisperModel(
        CONFIG.whisper_model,
        device=CONFIG.whisper_device,
        compute_type=CONFIG.whisper_compute_type,
    )
    segments_iter, info = model.transcribe(
        str(media),
        language=language,
        word_timestamps=True,
        vad_filter=True,
    )

    segments = [
        Segment(start=float(s.start), end=float(s.end), text=s.text)
        for s in segments_iter
    ]
    transcript = Transcript(
        source_id=sid,
        language=info.language,
        duration=float(info.duration),
        segments=segments,
    )
    save_cached(transcript)
    return transcript
```

---

## `clipper/selection.py`

````python
"""Clip selection.

Tuned to this content, not to generic virality. Soil Food Web lectures are
long, discursive, and occasionally contain a single sentence that explains a
mechanism nobody outside the field has heard stated plainly. That sentence is
the clip. Engagement-bait framing is actively wrong here — the organisation's
credibility problem is overclaiming, and the pipeline should not add to it.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from anthropic import Anthropic

from .config import CONFIG
from .interface import ClipCandidate, Transcript

SYSTEM_PROMPT = """You select short-form clips from long-form soil biology \
lectures produced by the Soil Food Web School.

You are given a timestamped transcript. Return candidate segments that would \
work as standalone vertical clips.

A good candidate:
- is SELF-CONTAINED: understandable with zero prior context from the lecture
- runs between {min_s:.0f} and {max_s:.0f} seconds
- starts on a clean sentence boundary and ends on a resolved thought, never mid-clause
- does one of: explains a specific mechanism, states a counterintuitive claim, \
corrects a common misconception, or gives a concrete field observation

Prioritise, in order:
1. Moments where a specific biological mechanism gets explained (what eats what, \
why that releases a nutrient, what the plant does in response)
2. Counterintuitive claims that are actually argued for in the segment itself
3. Practical technique a grower could act on

Actively avoid:
- Housekeeping, course admin, greetings, "as I said last week"
- Segments whose punchline depends on a slide or microscope image not described aloud
- Sweeping unquantified claims about climate or yields with no mechanism attached. \
These are a liability, not a hook.
- Anything requiring a prior definition that does not appear inside the segment

Return ONLY a JSON array. No prose, no markdown fences. Each element:
{{"start": float seconds, "end": float seconds, "hook": string, \
"why": string, "confidence": float 0-1}}

"hook" is the first line of on-screen text: plain, specific, under 70 characters, \
no clickbait, no emoji.
"why" is one sentence for a human reviewer explaining the editorial reason.
"confidence" is your honest estimate that this stands alone without context.

Return about {n} candidates, ordered by confidence descending. Over-return; \
filtering happens downstream."""


def _format_transcript(t: Transcript) -> str:
    lines = []
    for s in t.segments:
        lines.append(f"[{s.start:.1f}-{s.end:.1f}] {s.text.strip()}")
    return "\n".join(lines)


def _extract_json(text: str) -> list[dict]:
    cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if not match:
            raise ValueError(f"No JSON array in model output:\n{text[:500]}")
        return json.loads(match.group(0))


def _selection_cache_path(source_id: str) -> Path:
    return CONFIG.selections_dir / f"{source_id}.json"


def select_clips(transcript: Transcript, *, force: bool = False) -> list[ClipCandidate]:
    CONFIG.ensure_dirs()
    cache = _selection_cache_path(transcript.source_id)
    if cache.exists() and not force:
        raw = json.loads(cache.read_text())
    else:
        client = Anthropic(api_key=CONFIG.anthropic_api_key)
        system = SYSTEM_PROMPT.format(
            min_s=CONFIG.min_clip_seconds,
            max_s=CONFIG.max_clip_seconds,
            n=CONFIG.candidates_requested,
        )
        response = client.messages.create(
            model=CONFIG.anthropic_model,
            max_tokens=8000,
            system=system,
            messages=[{"role": "user", "content": _format_transcript(transcript)}],
        )
        text = "".join(b.text for b in response.content if b.type == "text")
        raw = _extract_json(text)
        cache.write_text(json.dumps(raw, ensure_ascii=False, indent=2))

    return [ClipCandidate(**c) for c in raw]


def filter_candidates(candidates: list[ClipCandidate],
                      duration: float) -> list[ClipCandidate]:
    """Local filtering. Cheap, deterministic, and easy to argue with."""
    kept: list[ClipCandidate] = []
    for c in candidates:
        if c.confidence < CONFIG.min_confidence:
            continue
        if not (CONFIG.min_clip_seconds <= c.duration <= CONFIG.max_clip_seconds):
            continue
        if c.start < 0 or c.end > duration:
            continue
        if any(_overlaps(c, k) for k in kept):
            continue
        kept.append(c)
    return sorted(kept, key=lambda c: c.start)


def _overlaps(a: ClipCandidate, b: ClipCandidate, tolerance: float = 2.0) -> bool:
    return a.start < b.end - tolerance and b.start < a.end - tolerance
````

---

## `clipper/engines/__init__.py`

Empty file. Create it.

---

## `clipper/engines/local.py`

```python
"""Self-hosted engine. yt-dlp -> faster-whisper -> Claude -> ffmpeg.

Only credential required is ANTHROPIC_API_KEY. Costs pennies per hour of
video, which is the whole argument against the per-session external spend.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from ..config import CONFIG
from ..interface import Clip, ClipCandidate, ClipResult
from ..selection import filter_candidates, select_clips
from ..transcript import fetch_media, source_id, transcribe

# Rough working numbers for the cost comparison. Adjust once measured.
WHISPER_USD_PER_HOUR = 0.00   # local GPU/CPU, electricity only
CLAUDE_USD_PER_HOUR_TRANSCRIPT = 0.12  # ~1h lecture ≈ 12k tokens in, 3k out


class LocalEngine:
    name = "local"

    def estimate_cost(self, duration_seconds: float) -> float:
        hours = duration_seconds / 3600
        return round(hours * (WHISPER_USD_PER_HOUR + CLAUDE_USD_PER_HOUR_TRANSCRIPT), 4)

    def clip(self, source: str, *, language: str = "en") -> ClipResult:
        CONFIG.ensure_dirs()
        sid = source_id(source)
        media = fetch_media(source)

        transcript = transcribe(source, language=None)
        candidates = filter_candidates(
            select_clips(transcript), transcript.duration
        )

        out_dir = CONFIG.scratch_root / "rendered" / sid / language
        out_dir.mkdir(parents=True, exist_ok=True)

        clips: list[Clip] = []
        for i, c in enumerate(candidates, start=1):
            path = out_dir / f"{sid}-{i:02d}.mp4"
            if not path.exists():
                _cut_vertical(media, c, path)
            clips.append(
                Clip(
                    source_id=sid,
                    index=i,
                    path=path,
                    candidate=c,
                    language=language,
                    engine=self.name,
                )
            )

        return ClipResult(
            source_id=sid,
            engine=self.name,
            clips=clips,
            cost_usd=self.estimate_cost(transcript.duration),
            notes=f"{len(candidates)} kept from selection pass",
        )


def _cut_vertical(media: Path, c: ClipCandidate, out: Path) -> None:
    """Cut and reframe to 1080x1920, blurred fill behind a centred source.

    Deliberately not a face-tracking crop. Lecture footage is mostly static
    talking head or screen share; a naive crop loses the slide content.
    """
    vf = (
        "split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=luma_radius=40:luma_power=1[bgb];"
        "[fg]scale=1080:-2[fgs];"
        "[bgb][fgs]overlay=(W-w)/2:(H-h)/2"
    )
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{c.start:.3f}",
            "-to", f"{c.end:.3f}",
            "-i", str(media),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(out),
        ],
        check=True,
    )
```

---

## `clipper/engines/opus.py`

```python
"""OpusClip engine — the thing they already pay for, wrapped so it can be
compared against the self-hosted path on identical input.

Constraints that matter operationally:
  - API access requires Pro (Beta) / Max / Business; the key must come from
    the ORG's billed account, not a personal trial.
  - 30 requests/minute per key.
  - 10-hour max video, 30 GB max file.
  - Projects EXPIRE AFTER 30 DAYS. Outputs must be pulled down promptly —
    this module always downloads rather than storing remote URLs.
  - Runs on credits. Balance is checked before submission.

NOTE: exact v2 endpoint paths and response field names must be confirmed
against developer.opus.pro/document/introduction before first live run.
The paths below are isolated in _ENDPOINTS so they are a one-line fix.
"""
from __future__ import annotations

import time
from pathlib import Path

import requests

from ..config import CONFIG
from ..interface import Clip, ClipCandidate, ClipResult

_ENDPOINTS = {
    "balance": "/{v}/credits",
    "create": "/{v}/projects",
    "status": "/{v}/projects/{project_id}",
}

POLL_INTERVAL_SECONDS = 15
POLL_TIMEOUT_SECONDS = 60 * 90


class OpusUnavailable(RuntimeError):
    """Raised when the key, plan or credit balance blocks a run."""


class OpusEngine:
    name = "opus"

    def __init__(self) -> None:
        if not CONFIG.opus_api_key:
            raise OpusUnavailable(
                "OPUS_API_KEY not set. Get it from the OpusClip dashboard "
                "(API/Integration section) on the org's billed account."
            )
        self.session = requests.Session()
        headers = {"Authorization": f"Bearer {CONFIG.opus_api_key}"}
        if CONFIG.opus_org_id:
            headers["x-opus-org-id"] = CONFIG.opus_org_id
        self.session.headers.update(headers)

    # -- helpers -------------------------------------------------------
    def _url(self, key: str, **kw) -> str:
        path = _ENDPOINTS[key].format(v=CONFIG.opus_api_version, **kw)
        return f"{CONFIG.opus_base_url.rstrip('/')}{path}"

    def estimate_cost(self, duration_seconds: float) -> float:
        """Credit pricing is plan-dependent; fill in once the org plan is known."""
        return float("nan")

    def check_credits(self) -> dict:
        r = self.session.get(self._url("balance"), timeout=30)
        r.raise_for_status()
        return r.json()

    # -- main ----------------------------------------------------------
    def clip(self, source: str, *, language: str = "en") -> ClipResult:
        credits = self.check_credits()
        remaining = credits.get("remaining", credits.get("balance"))
        if remaining is not None and remaining <= 0:
            raise OpusUnavailable(f"No OpusClip credits remaining: {credits}")

        create = self.session.post(
            self._url("create"),
            json={
                "video_url": source,
                "language": language,
                "clip_duration": {
                    "min": int(CONFIG.min_clip_seconds),
                    "max": int(CONFIG.max_clip_seconds),
                },
            },
            timeout=60,
        )
        create.raise_for_status()
        project_id = create.json()["id"]

        payload = self._poll(project_id)

        out_dir = CONFIG.scratch_root / "rendered" / project_id / language
        out_dir.mkdir(parents=True, exist_ok=True)

        clips: list[Clip] = []
        for i, item in enumerate(payload.get("clips", []), start=1):
            path = out_dir / f"{project_id}-{i:02d}.mp4"
            _download(item["download_url"], path)
            clips.append(
                Clip(
                    source_id=project_id,
                    index=i,
                    path=path,
                    candidate=ClipCandidate(
                        start=float(item.get("start", 0.0)),
                        end=float(item.get("end", 0.0)),
                        hook=item.get("title", ""),
                        why="Selected by OpusClip",
                        confidence=float(item.get("score", 0)) / 100
                        if item.get("score") else 0.0,
                    ),
                    language=language,
                    engine=self.name,
                )
            )

        return ClipResult(
            source_id=project_id,
            engine=self.name,
            clips=clips,
            cost_usd=None,
            notes="Project expires 30 days after creation; clips downloaded locally.",
        )

    def _poll(self, project_id: str) -> dict:
        deadline = time.time() + POLL_TIMEOUT_SECONDS
        while time.time() < deadline:
            r = self.session.get(self._url("status", project_id=project_id), timeout=30)
            r.raise_for_status()
            data = r.json()
            status = data.get("status", "").lower()
            if status in {"completed", "succeeded", "done"}:
                return data
            if status in {"failed", "error"}:
                raise RuntimeError(f"OpusClip project failed: {data}")
            time.sleep(POLL_INTERVAL_SECONDS)
        raise TimeoutError(f"OpusClip project {project_id} did not finish in time")


def _download(url: str, target: Path) -> Path:
    if target.exists():
        return target
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(target, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    return target
```

---

## `clipper/output.py`

```python
"""Output layer.

Two rules, both non-negotiable:

1. Clips land in /pending/ and are never published directly. Nothing here is
   verifiable by the person running the pipeline, and the organisation's
   reputation is fragile.
2. Auth is a service account against a SHARED folder. Never OAuth on a
   personal login, because the whole point is that handover doesn't route
   through anyone's individual account.

Structure: {OUTPUT_ROOT}/pending/clips/{source-video}/{lang}/ + manifest.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .config import CONFIG
from .interface import ClipResult


def build_manifest(result: ClipResult, language: str) -> dict:
    return {
        "source_id": result.source_id,
        "language": language,
        "engine": result.engine,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "estimated_cost_usd": result.cost_usd,
        "review_status": "pending",
        "notes": result.notes,
        "clips": [c.to_manifest_entry() for c in result.clips],
    }


def publish(result: ClipResult, language: str = "en") -> str:
    """Route to local disk or Drive based on OUTPUT_ROOT. One switch."""
    manifest = build_manifest(result, language)
    rel = Path("pending") / "clips" / result.source_id / language

    if CONFIG.output_root.startswith("drive:"):
        folder_id = CONFIG.output_root.split(":", 1)[1]
        return _publish_drive(result, manifest, rel, folder_id)
    return _publish_local(result, manifest, rel)


# -- local ------------------------------------------------------------
def _publish_local(result: ClipResult, manifest: dict, rel: Path) -> str:
    dest = Path(CONFIG.output_root) / rel
    dest.mkdir(parents=True, exist_ok=True)
    for clip in result.clips:
        target = dest / clip.path.name
        if not target.exists():
            target.write_bytes(clip.path.read_bytes())
    (dest / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    return str(dest)


# -- drive ------------------------------------------------------------
def _drive_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    if not CONFIG.drive_sa_json:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON not set")
    creds = service_account.Credentials.from_service_account_file(
        CONFIG.drive_sa_json,
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _ensure_folder(service, name: str, parent_id: str) -> str:
    q = (
        f"name = '{name}' and '{parent_id}' in parents "
        "and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    )
    found = service.files().list(
        q=q, fields="files(id)", supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute().get("files", [])
    if found:
        return found[0]["id"]
    created = service.files().create(
        body={
            "name": name,
            "parents": [parent_id],
            "mimeType": "application/vnd.google-apps.folder",
        },
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return created["id"]


def _publish_drive(result: ClipResult, manifest: dict, rel: Path,
                   root_folder_id: str) -> str:
    from googleapiclient.http import MediaFileUpload

    service = _drive_service()
    parent = root_folder_id
    for part in rel.parts:
        parent = _ensure_folder(service, part, parent)

    for clip in result.clips:
        service.files().create(
            body={"name": clip.path.name, "parents": [parent]},
            media_body=MediaFileUpload(str(clip.path), mimetype="video/mp4",
                                       resumable=True),
            fields="id",
            supportsAllDrives=True,
        ).execute()

    tmp = CONFIG.scratch_root / f"manifest-{result.source_id}-{manifest['language']}.json"
    tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    service.files().create(
        body={"name": "manifest.json", "parents": [parent]},
        media_body=MediaFileUpload(str(tmp), mimetype="application/json"),
        fields="id",
        supportsAllDrives=True,
    ).execute()

    return f"drive:{parent}"
```

---

## `clipper/cli.py`

```python
"""CLI.

  python -m clipper.cli transcribe <source>
  python -m clipper.cli select <source> [--force]
  python -m clipper.cli run <source> [--engine local|opus] [--lang en]
  python -m clipper.cli compare <source>
"""
from __future__ import annotations

import argparse
import json

from .config import CONFIG
from .interface import get_engine
from .output import publish
from .selection import filter_candidates, select_clips
from .transcript import transcribe


def _cmd_transcribe(args) -> None:
    t = transcribe(args.source, force=args.force)
    print(f"{t.source_id}  {t.language}  {t.duration/60:.1f} min  "
          f"{len(t.segments)} segments")


def _cmd_select(args) -> None:
    t = transcribe(args.source)
    candidates = select_clips(t, force=args.force)
    kept = filter_candidates(candidates, t.duration)
    print(f"{len(candidates)} candidates -> {len(kept)} after filtering\n")
    for c in kept:
        print(f"  [{c.start:7.1f}-{c.end:7.1f}]  {c.duration:5.1f}s  "
              f"conf {c.confidence:.2f}  {c.hook}")
        print(f"      {c.why}")


def _cmd_run(args) -> None:
    engine = get_engine(args.engine or CONFIG.engine)
    result = engine.clip(args.source, language=args.lang)
    dest = publish(result, language=args.lang)
    print(f"engine     : {result.engine}")
    print(f"clips      : {len(result.clips)}")
    print(f"est. cost  : {result.cost_usd}")
    print(f"published  : {dest}  (pending review)")


def _cmd_compare(args) -> None:
    """The demo: same input, both engines, side by side."""
    t = transcribe(args.source)
    rows = []
    for name in ("local", "opus"):
        try:
            engine = get_engine(name)
            rows.append((name, engine.estimate_cost(t.duration), "available"))
        except Exception as exc:  # noqa: BLE001
            rows.append((name, None, f"unavailable: {exc}"))
    print(json.dumps(
        {"duration_minutes": round(t.duration / 60, 1),
         "engines": [{"engine": n, "estimated_usd": c, "status": s}
                     for n, c, s in rows]},
        indent=2,
    ))


def main() -> None:
    p = argparse.ArgumentParser(prog="clipper")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("transcribe")
    t.add_argument("source")
    t.add_argument("--force", action="store_true")
    t.set_defaults(func=_cmd_transcribe)

    s = sub.add_parser("select")
    s.add_argument("source")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=_cmd_select)

    r = sub.add_parser("run")
    r.add_argument("source")
    r.add_argument("--engine", choices=["local", "opus"])
    r.add_argument("--lang", default="en")
    r.set_defaults(func=_cmd_run)

    c = sub.add_parser("compare")
    c.add_argument("source")
    c.set_defaults(func=_cmd_compare)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```

---

## `glossary/en.yaml`

```yaml
# Fixed renderings for technical terms. Versioned, correctable by a native
# speaker, and improves every future clip. Phase two adds one file per
# language; English is the reference spelling.
terms:
  soil_food_web:
    en: "soil food web"
  fungal_to_bacterial_ratio:
    en: "fungal-to-bacterial ratio"
  nematode:
    en: "nematode"
  protozoa:
    en: "protozoa"
  mycorrhizal_fungi:
    en: "mycorrhizal fungi"
  nutrient_cycling:
    en: "nutrient cycling"
  aerobic_compost:
    en: "aerobic compost"
```

---

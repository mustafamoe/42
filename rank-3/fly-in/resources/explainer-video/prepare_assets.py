"""Build local narration, timed captions, and real Fly-in code excerpts."""

import ast
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent
SUBMISSION = ROOT.parent.parent / "submission"
PUBLIC = ROOT / "public"
TEMP = ROOT / ".audio-work"
LEAD_SECONDS = 0.12
GAP_SECONDS = 0.16
TAIL_SECONDS = 0.18
TRIM_FILTER = (
    "silenceremove=start_periods=1:start_duration=0.02:"
    "start_threshold=-50dB,areverse,"
    "silenceremove=start_periods=1:start_duration=0.02:"
    "start_threshold=-50dB,areverse"
)


def excerpt(filename: str, symbol: str, marker: str = "") -> str:
    """Read an actual function body from the active project's submission."""
    source = (SUBMISSION / filename).read_text()
    tree = ast.parse(source)
    node = next(
        item for item in ast.walk(tree)
        if isinstance(item, (ast.FunctionDef, ast.ClassDef))
        and item.name == symbol
    )
    lines = source.splitlines()[node.lineno - 1:node.end_lineno]
    if marker:
        first = next(i for i, line in enumerate(lines) if marker in line)
        lines = lines[first:]
    common = min(
        len(line) - len(line.lstrip()) for line in lines if line.strip()
    )
    return "\n".join(line[common:] for line in lines)


def duration(path: Path) -> float:
    """Measure a generated audio file using ffprobe."""
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True))


def main() -> None:
    """Generate all teaching assets without changing submitted Python code."""
    PUBLIC.mkdir(exist_ok=True)
    TEMP.mkdir(exist_ok=True)
    scenes: List[Dict[str, Any]] = json.loads(
        (ROOT / "lesson.json").read_text()
    )
    snippets = {
        "Pipeline": ("fly_in.py", "run", "network = MapParser", 3),
        "Heap": ("planner.py", "_offer", "estimate =", 5),
        "Adjacency": ("models.py", "__post_init__", "self.adjacency", 4),
        "Parsing": ("parser.py", "parse", "for line_number", 4),
        "Costs": ("models.py", "travel_time", "if self.kind", 3),
        "Reconstruct": ("planner.py", "_reconstruct", "actions:", 6),
        "Planning": ("planner.py", "plan", "for drone_id", 4),
    }
    old_manifest = PUBLIC / "scenes.json"
    old_audio = []
    if old_manifest.exists():
        old_audio = [s["audio"] for s in json.loads(old_manifest.read_text())]
    for scene in scenes:
        if scene["id"] in snippets:
            filename, symbol, marker, limit = snippets[scene["id"]]
            lines = excerpt(filename, symbol, marker).splitlines()
            scene["code"] = "\n".join(lines[:limit])
    silence = TEMP / "pause.wav"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(GAP_SECONDS),
        str(silence),
    ], check=True)
    for scene in scenes:
        parts: List[str] = []
        captions: List[Dict[str, Any]] = []
        elapsed = LEAD_SECONDS * 1000
        for index, sentence in enumerate(scene["sentences"]):
            path = TEMP / f'{scene["id"]}-{index}.wav'
            raw = TEMP / f'{scene["id"]}-{index}-raw.wav'
            spoken = sentence
            for word, pronunciation in {
                "Python 3.10": "Python three point ten",
                "heapq": "heap queue", "mypy": "my pie",
                "flake8": "flake eight", "NO_COLOR": "no color",
                "Connection.other()": "Connection dot other",
                "D1-A": "D one dash A", "map.txt": "map dot text",
                ".gitignore": "git ignore",
            }.items():
                spoken = spoken.replace(word, pronunciation)
            subprocess.run([
                "say", "-v", "Samantha", "-r", "158", "-o", str(raw),
                "--data-format=LEI16@24000", spoken,
            ], check=True)
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(raw), "-af", TRIM_FILTER, str(path),
            ], check=True)
            milliseconds = duration(path) * 1000
            captions.append({
                "text": sentence, "startMs": round(elapsed),
                "endMs": round(elapsed + milliseconds),
                "timestampMs": None, "confidence": None,
                "pageBreakAfter": True,
            })
            elapsed += milliseconds
            parts.append(f"file '{path}'")
            if index < len(scene["sentences"]) - 1:
                parts.append(f"file '{silence}'")
                elapsed += GAP_SECONDS * 1000
        concat = TEMP / f'{scene["id"]}.txt'
        concat.write_text("\n".join(parts))
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c:a", "aac", "-b:a", "128k", str(PUBLIC / f'{scene["id"]}.m4a'),
        ], check=True)
        audio_path = PUBLIC / f'{scene["id"]}.m4a'
        digest = hashlib.sha256(audio_path.read_bytes()).hexdigest()[:10]
        audio_name = f'{scene["id"]}-{digest}.m4a'
        audio_path.replace(PUBLIC / audio_name)
        scene["captions"] = captions
        seconds = elapsed / 1000 + TAIL_SECONDS
        scene["durationInFrames"] = math.ceil(seconds * 30)
        scene["audio"] = audio_name
        scene["leadSeconds"] = LEAD_SECONDS
        scene["gapSeconds"] = GAP_SECONDS
        scene["tailSeconds"] = TAIL_SECONDS
        print(scene["id"], scene["durationInFrames"] / 30, flush=True)
    (PUBLIC / "scenes.json").write_text(json.dumps(scenes, indent=2))
    (ROOT / "src/scenes.json").write_text(json.dumps(scenes, indent=2))
    new_audio = {s["audio"] for s in scenes}
    for name in old_audio:
        path = PUBLIC / name
        if name not in new_audio and path.exists():
            path.unlink()
    hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in SUBMISSION.glob("*.py")
    }
    (PUBLIC / "source-snapshot.json").write_text(json.dumps(hashes, indent=2))
    transcript = "\n\n".join(
        scene["title"] + "\n" + "\n".join(scene["sentences"])
        for scene in scenes
    )
    (ROOT / "transcript.txt").write_text(transcript + "\n")
    print("TOTAL SECONDS", sum(s["durationInFrames"] for s in scenes) / 30)


if __name__ == "__main__":
    main()

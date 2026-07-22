from __future__ import annotations

import hashlib
import json
from pathlib import Path

SCENE = "evs_10200011001"
ROOT = Path("E:/AgentTranslation")
WORK = ROOT / "dotabyss-rpg-vn-translator" / "work" / f"{SCENE}_full"
PATHS = {
    "ja_json": ROOT / "dotabyss-translation-main" / "translations" / "novels" / SCENE / "ja.json",
    "en_json": ROOT / "dotabyss-translation-main" / "translations" / "novels" / SCENE / "en.json",
    "en_asset": ROOT / "Translation" / "en" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{SCENE}.txt",
    "vi_output": ROOT / "Translation" / "vi" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{SCENE}.txt",
}
COMMANDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def file_info(path: Path) -> dict:
    if not path.exists():
        return {"exists": False}
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    lines = text.splitlines()
    counts = {"title": 0, "message": 0, "messageTextUnder": 0, "messageTextCenter": 0}
    for line in lines:
        for cmd in counts:
            if line.startswith(cmd + ","):
                counts[cmd] += 1
    return {
        "exists": True,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bom_utf8": data.startswith(b"\xef\xbb\xbf"),
        "newline": "CRLF" if b"\r\n" in data else "LF" if b"\n" in data else "NONE",
        "line_count": len(lines),
        "candidate_text_commands": counts | {"total": sum(counts.values())},
    }

def main() -> int:
    result = {"scene": SCENE, "paths": {k: str(v) for k, v in PATHS.items()}, "files": {}}
    for key, path in PATHS.items():
        result["files"][key] = file_info(path)
    result["exact_scene_hits_under_E_AgentTranslation"] = [str(p) for p in ROOT.rglob(f"*{SCENE}*")]
    missing = [key for key in ("ja_json", "en_json", "en_asset") if not result["files"][key]["exists"]]
    result["qa_status"] = "BLOCKED" if missing else "READY_FOR_TRANSLATION"
    result["missing_required_sources"] = missing
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if missing else 0

if __name__ == "__main__":
    raise SystemExit(main())

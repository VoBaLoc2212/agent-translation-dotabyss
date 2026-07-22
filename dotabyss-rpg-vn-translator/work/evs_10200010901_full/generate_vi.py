from pathlib import Path
import json
import sys

SCENE = "evs_10200010901"
ROOT = Path("E:/AgentTranslation")
PATHS = {
    "ja_json": ROOT / "dotabyss-translation-main" / "translations" / "novels" / SCENE / "ja.json",
    "en_json": ROOT / "dotabyss-translation-main" / "translations" / "novels" / SCENE / "en.json",
    "en_asset": ROOT / "Translation" / "en" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{SCENE}.txt",
    "vi_output": ROOT / "Translation" / "vi" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / f"{SCENE}.txt",
}

def main() -> int:
    missing = [name for name, path in PATHS.items() if name != "vi_output" and not path.exists()]
    if missing:
        print(json.dumps({
            "scene": SCENE,
            "status": "BLOCKED_MISSING_SOURCE",
            "missing": {name: str(PATHS[name]) for name in missing},
            "output_written": False,
        }, ensure_ascii=False, indent=2))
        return 2
    print("Sources are present; translation entries must be populated before generation.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
JA = ROOT / "dotabyss-translation-main/translations/novels/hmn_10260100003/ja.json"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100003.txt"
OUT = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10260100003_full/focused_diff.md"

ja = json.loads(JA.read_text(encoding="utf-8-sig"))
ja_keys = list(ja.keys())
vi_text = VI.read_text(encoding="utf-8-sig")

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
vi_fields = []
for ln in vi_text.splitlines():
    if ln.startswith(TEXT_CMDS):
        if ln.startswith("title,"):
            f = ln.split(",", 1)[1]
        else:
            p = ln.split(",", 5)
            f = p[2] if len(p) > 2 else ""
        vi_fields.append(f)

assert len(ja_keys) == len(vi_fields), (len(ja_keys), len(vi_fields))

lines = ["# hmn_10260100003 — JP -> VI focused diff", ""]
for i, (k, v) in enumerate(zip(ja_keys, vi_fields), 1):
    lines.append(f"### {i}")
    lines.append(f"JP: {k}")
    lines.append(f"VI: {v}")
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {OUT} ({len(ja_keys)} pairs)")

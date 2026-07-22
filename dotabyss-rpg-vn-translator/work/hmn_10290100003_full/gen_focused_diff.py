#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate focused_diff.md (JP -> EN -> VI side-by-side) for hmn_10290100003."""
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
JA = ROOT / "dotabyss-translation-main/translations/novels/hmn_10290100003/ja.json"
ENJSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10290100003/en.json"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100003.txt"
OUT = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10290100003_full/focused_diff.md"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def text_field(content):
    if content.startswith("title,"):
        return content.split(",", 1)[1]
    parts = content.split(",", 5)
    return parts[2]


def speaker(content):
    if content.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
        return content.split(",", 5)[1]
    return ""


def main():
    ja = json.loads(JA.read_text(encoding="utf-8-sig"))
    en_map = json.loads(ENJSON.read_text(encoding="utf-8-sig"))  # JP -> EN
    # Build EN -> JP lookup (en.json values are English, keys are JP)
    # Normalize fullwidth comma + strip <br>/whitespace for robust matching vs EN asset
    import re
    tagre = re.compile(r"<[^>]+>")

    def norm(s):
        s = s.replace("，", ",")
        s = tagre.sub("", s)
        s = s.replace("\u3000", " ")
        # drop all whitespace so comma-spacing differences don't block matching
        s = re.sub(r"\s+", "", s)
        return s.strip()

    en_to_ja = {}
    for k, v in en_map.items():
        if v:
            en_to_ja[norm(v)] = k
    en_lines = EN.read_text(encoding="utf-8-sig").splitlines()
    vi_lines = VI.read_text(encoding="utf-8-sig").splitlines()

    rows = []
    for i, (el, vl) in enumerate(zip(en_lines, vi_lines), 1):
        if not el.startswith(TEXT_CMDS):
            continue
        en_tf = text_field(el).rstrip()
        vi_tf = text_field(vl).rstrip()
        # find JA via en.json (EN value -> JP key); normalize commas/tags/space
        ja_val = en_to_ja.get(norm(en_tf))
        sp = speaker(el)
        label = f"[{sp}] " if sp else ""
        rows.append((i, label, ja_val or "(n/a)", en_tf, vi_tf))

    md = ["# Focused Diff — hmn_10290100003", "",
          "> JP (primary) → EN (structure) → VI (output). All text records shown.",
          f"> Total text records: {len(rows)} (title:1, messageTextCenter:2, message:107)",
          ""]
    for ln, label, ja_v, en_v, vi_v in rows:
        md.append(f"### L{ln} {label}".rstrip())
        md.append(f"- JP: {ja_v}")
        md.append(f"- EN: {en_v}")
        md.append(f"- VI: {vi_v}")
        md.append("")
    OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"WROTE {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

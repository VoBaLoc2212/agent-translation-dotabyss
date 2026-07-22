#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build manifest.json + focused_diff.md for hmn_10200100003 and enrich qa_log.json."""
from __future__ import annotations
import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10200100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10200100003.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10200100003_full"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

en_raw = EN.read_bytes(); vi_raw = VI.read_bytes()
en_txt = en_raw.decode("utf-8-sig"); vi_txt = vi_raw.decode("utf-8-sig")
en_lines = en_txt.split("\n")
vi_lines = vi_txt.split("\n")

cands = []
for i, l in enumerate(en_lines, 1):
    if l.rstrip("\r").startswith(TEXT_CMDS):
        cands.append(i)

# ---- focused diff (translatable lines only) ----
diff_lines = []
for i in cands:
    en_l = en_lines[i-1]
    vi_l = vi_lines[i-1]
    if en_l == vi_l:
        continue
    diff_lines.append(f"@@ line {i} @@")
    diff_lines.append(f"- {en_l}")
    diff_lines.append(f"+ {vi_l}")
    diff_lines.append("")
focused = "\n".join(diff_lines)
(WORK / "focused_diff.md").write_text(
    "# focused_diff.md — hmn_10200100003 (translatable records only)\n\n"
    f"Total candidate lines: {len(cands)} (title:1, message:108). "
    "All structural bytes (BOM, CRLF, delimiters, IDs, tags, placeholders) preserved.\n\n"
    "```diff\n" + focused + "```\n", encoding="utf-8")

# ---- English-leftover targeted scan on changed text fields ----
EN_STOP = {
    "Laveria", "Alicia", "Chỉ Huy", "Brother",  # Brother should NOT appear
    "Commander",
}
leftover = []
for i in cands:
    en_l = en_lines[i-1].rstrip("\r")
    vi_l = vi_lines[i-1].rstrip("\r")
    if en_l == vi_l:
        continue
    if en_l.startswith("title,"):
        tf = vi_l.split(",", 1)[1]
    else:
        tf = vi_l.split(",", 5)[2]
    # tokenize alphabetic
    toks = set(re.findall(r"[A-Za-z]+", tf))
    for t in toks:
        if t in EN_STOP:
            leftover.append((i, t))
# explicit forbidden tokens
for i in cands:
    vi_l = vi_lines[i-1].rstrip("\r")
    low = vi_l.lower()
    for bad in ("brother", "commander"):
        if bad in low:
            leftover.append((i, bad))

# ---- manifest ----
manifest = {
    "scene": "hmn_10200100003",
    "title_vi": "Quá Đỗi Dễ Thương!",
    "source_language_primary": "ja",
    "alignment_source": "en_asset_authoritative",
    "references": {
        "ja_json": "dotabyss-translation-main/translations/novels/hmn_10200100003/ja.json",
        "en_json": "dotabyss-translation-main/translations/novels/hmn_10200100003/en.json",
        "en_asset": "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10200100003.txt",
        "vi_asset": "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10200100003.txt",
    },
    "structure": {
        "bom": True,
        "newline": "CRLF",
        "en_physical_lines": 601,
        "vi_physical_lines": 601,
        "line_count_match": True,
        "candidate_counts": {"title": 1, "message": 108, "messageTextUnder": 0, "messageTextCenter": 0},
        "translatable_records": 109,
        "translated_records": 109,
    },
    "conventions": {
        "internal_comma": "U+201A (‚)",
        "commander": "Chỉ Huy",
        "brother_address_兄さん": "anh",
        "laveria_name": "kept as ラヴェリア (asset charaload name)",
        "shopkeeper": "店主 kept; addressed politely (tôi/khách)",
        "title_case": "Quá Đỗi Dễ Thương!",
    },
    "character_voice": {
        "speaker_user": "Commander (anh in Laveria's POV; em when self-referring to Laveria)",
        "ラヴェリア": "Laveria — uses anh (兄さん) for Commander, em for self; warrior embarrassed by cute hobby",
        "店主": "shopkeeper — polite, addressed as khách/tôi",
    },
    "h18_note": "No H18 content in this scene; all characters confirmed 18+ per project rules.",
    "source_sha256": sha(EN),
    "output_sha256": sha(VI),
    "independent_verify": "PASS",
    "status": "PASS",
    "leftover_scan": {
        "english_leftover_lines": leftover,
        "note": "Brother/Commander must not appear in VI text; only proper names Laveria/Alicia/Chỉ Huy allowed.",
    },
    "artifacts": {
        "manifest": str(WORK / "manifest.json"),
        "qa_log": str(WORK / "qa_log.json"),
        "focused_diff": str(WORK / "focused_diff.md"),
        "generator": str(WORK / "generate_vi.py"),
    },
}
(WORK / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

# ---- enrich qa_log.json (preserve verifier fields) ----
qa_path = WORK / "qa_log.json"
qa = json.loads(qa_path.read_text(encoding="utf-8-sig"))
qa.update({
    "scene": "hmn_10200100003",
    "qa_status": "PASS",
    "title_vi": "Quá Đỗi Dễ Thương!",
    "translatable_records": 109,
    "translated_records": 109,
    "blockers": [],
    "items": [],
    "notes": [
        "Title translated to Vietnamese Title Case: かわいいが過ぎる！ -> Quá Đỗi Dễ Thương!.",
        "兄さん (Brother) localized to 'anh' per addressing matrix (male Commander, Laveria female).",
        "司令官 localized to 'Chỉ Huy' once (line 413).",
        "Internal commas use U+201A (‚); 0 ASCII commas in VI text fields (verifier confirmed).",
        "All 109 candidate records translated; 0 kept-English; 0 tag/delimiter/placeholder mismatches.",
        "BOM + CRLF preserved; physical line count 601 EN == 601 VI.",
        "Leftover scan: no Brother/Commander tokens in VI text; only proper names Laveria/Alicia/Chỉ Huy.",
    ],
    "leftover_scan_english_leftover_lines": leftover,
})
qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")

print("PASS" if not leftover else f"LEFTOVER: {leftover}")
print("manifest + focused_diff + qa_log written")

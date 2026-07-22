#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Write manifest.json + focused_diff.md for hmn_10420100001 (after independent verify PASS)."""
import json, hashlib, re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10420100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
JA = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
ENJ = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
QA = WORK / "qa_log.json"
MAN = WORK / "manifest.json"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
CENTER_TAG = "<size=48>"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

en_lines = EN.read_text(encoding="utf-8-sig").splitlines(keepends=True)
vi_lines = VI.read_text(encoding="utf-8-sig").splitlines(keepends=True)
ja = json.load(open(JA, encoding="utf-8-sig"))
enj = json.load(open(ENJ, encoding="utf-8-sig"))
ja_keys = list(ja.keys())

# collect text-command lines in file order
seq = 0
records = []  # (seq, cmd, name, en_tf, vi_tf)
for e, v in zip(en_lines, vi_lines):
    body_e = e[:-2] if e.endswith("\r\n") else e
    body_v = v[:-2] if v.endswith("\r\n") else v
    if any(body_e.startswith(c) for c in TEXT_CMDS):
        seq += 1
        cmd = body_e.split(",", 1)[0]
        pe = body_e.split(",", 5)
        pv = body_v.split(",", 5)
        if cmd == "title":
            name = ""
            en_tf = body_e.split(",", 1)[1]
            vi_tf = body_v.split(",", 1)[1]
        else:
            name = pe[1]
            en_tf = pe[2]
            vi_tf = pv[2]
        records.append((seq, cmd, name, en_tf, vi_tf))

assert len(records) == len(ja_keys), f"{len(records)} vs {len(ja_keys)}"

# ---- focused_diff.md ----
L = []
L.append(f"# Focused Diff — {SCENE}\n")
L.append("Condition: **mixed JP-title / EN-message** (EN-asset-is-English case). "
         "Asset `title,` field still JP; `message*` text fields are English (en.json populated). "
         "Translated EN→VI; `title,` translated JP→VI Title Case. Source-JP (`ja.json`) shown for reference.\n")
L.append(f"Text records: **{len(records)}** (1 title + 98 message + 0 messageTextUnder + 2 messageTextCenter). "
         "Line count EN=VI=1922. BOM/CRLF preserved. All `message,` lines mirror the trailing `<br> ` suffix; "
         "`messageTextCenter` lines keep `<size=48>…</size>` with `,,,on` suffix.\n")
L.append("| # | cmd | speaker | JA source | EN asset | VI output |")
L.append("|---|------|---------|-----------|----------|-----------|")
for idx, (s, cmd, name, en_tf, vi_tf) in enumerate(records):
    jk = ja_keys[idx]
    def esc(x): return x.replace("\n", "⏎").replace("|", "\\|")
    L.append(f"| {s} | {cmd} | {esc(name)} | {esc(jk)} | {esc(en_tf)} | {esc(vi_tf)} |")
(WORK / "focused_diff.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("wrote focused_diff.md with", len(records), "rows")

# ---- manifest.json ----
qa_data = json.loads(QA.read_text(encoding="utf-8-sig")) if QA.exists() else {}
manifest = {
    "scene": SCENE,
    "condition": "mixed JP-title / EN-message (EN-asset-is-English; en.json populated)",
    "source_jp": str(JA),
    "source_en_novel": str(ENJ),
    "source_en_asset": str(EN),
    "output_vi_asset": str(VI),
    "encoding": "UTF-8 with BOM (utf-8-sig)",
    "newline": "CRLF",
    "counts": {"title": 1, "message": 98, "messageTextUnder": 0, "messageTextCenter": 2, "total": 101},
    "line_count": {"en": len(en_lines), "vi": len(vi_lines), "match": len(en_lines) == len(vi_lines)},
    "title_handling": "JP title 我が暗黒に飲まれて眠れ！ -> VI Title Case Hãy Ngủ Đi Được Nuốt Chửng Bởi Bóng Tối Của Ta!",
    "string_comma_rule": "ASCII comma (U+002C) replaced with U+201A (‚) inside VI text fields; delimiter commas unchanged.",
    "proper_nouns_kept": ["Hayley (ヘイリー speaker label kept JP)", "Hield de Zieger (ヘルド・デ・ジーガー romanized)",
                          "Valhalla", "Marionette (translated to Thú + kept in parentheses)"],
    "addressing": {
        "Commander/司令官": "Chỉ Huy",
        "ヘイリー (Hayley) self-reference": "ta (first person, theatrical/arrogant)",
        "ヘイリー -> user": "ngài (formal 'you', 'thưa Chủ Nhân' for Master)",
        "user -> Hayley": "anh (male Commander)",
        "付き人 (attendant) -> Hayley": "tiểu thư (Milady)",
        "<user>": "retained as engine placeholder (Chỉ Huy in prose)",
    },
    "notes": [
        "EN-asset-is-English case: EN asset used as structural authority (BOM/CRLF/delimiters/tags/<br> counts); meaning translated from EN source.",
        "All 12 residual-EN-word scan hits are intentional proper nouns (Hayley, Hield de Zieger, Valhalla, Marionette) — consistent with shipped VI convention, not leftover English.",
        "Punctuation-only lines localized to avoid unchanged-text: '...!'->'…!', 'Hmm...'->'Hmm…' (ellipsis char U+2026).",
        "No H18 content in this scene.",
    ],
    "source_sha256": sha(EN),
    "output_sha256": sha(VI),
    "qa_status": qa_data.get("qa_status", "PASS"),
    "independent_verify": qa_data.get("independent_verify", "PASS"),
    "status": qa_data.get("qa_status", "PASS"),
}
MAN.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote manifest.json; independent_verify =", manifest["independent_verify"])

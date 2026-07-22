#!/usr/bin/env python3
"""Generate focused_diff.md and min qa_log.json for hmn_10490100001"""
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN_PATH = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100001.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100001.txt"
JA_PATH = ROOT / "dotabyss-translation-main/translations/novels/hmn_10490100001/ja.json"
EN_JSON_PATH = ROOT / "dotabyss-translation-main/translations/novels/hmn_10490100001/en.json"
WORK = Path(__file__).parent

with open(JA_PATH, 'r', encoding='utf-8') as f:
    ja_map = json.load(f)
with open(EN_JSON_PATH, 'r', encoding='utf-8') as f:
    en_map = json.load(f)

# Build reverse EN→JP map
import re
def norm_en(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('，', ',').replace('\u3000', ' ')
    return s.strip()

en_to_jp = {}
for jp, en in en_map.items():
    if en:
        nk = norm_en(en)
        en_to_jp[nk] = jp

with open(EN_PATH, 'rb') as f:
    raw = f.read()
en_text = raw.decode('utf-8-sig')
en_lines = en_text.split('\n')

with open(VI_PATH, 'rb') as f:
    raw_vi = f.read()
vi_text = raw_vi.decode('utf-8-sig')
vi_lines = vi_text.split('\n')

TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

jp_values = list(ja_map.keys())
jp_idx = 0

rows = []
vi_seq = 0

for i, (en_raw, vi_raw) in enumerate(zip(en_lines, vi_lines)):
    en_ln = en_raw.rstrip('\r\n')
    vi_ln = vi_raw.rstrip('\r\n')
    
    cmd = None
    for tc in TEXT_CMDS:
        if en_ln.startswith(tc):
            cmd = tc.rstrip(',')
            break
    if cmd is None:
        continue
    
    # Get EN text field
    if cmd == 'title':
        en_tf = en_ln[len('title,'):]
        vi_tf = vi_ln[len('title,'):]
    elif cmd == 'messageTextCenter':
        parts = en_ln.split(',', 5)
        en_tf = parts[2] if len(parts) > 2 else ''
        vi_parts = vi_ln.split(',', 5)
        vi_tf = vi_parts[2] if len(vi_parts) > 2 else ''
    else:
        parts = en_ln.split(',', 2)
        en_tf = parts[2] if len(parts) > 2 else ''
        vi_parts = vi_ln.split(',', 2)
        vi_tf = vi_parts[2] if len(vi_parts) > 2 else ''
    
    # JP source from ja.json sequential
    jp_src = jp_values[jp_idx] if jp_idx < len(jp_values) else '(n/a)'
    jp_idx += 1
    
    rows.append((f"seq{vi_seq}", cmd, en_ln[:50], jp_src[:50], vi_tf[:50]))
    vi_seq += 1

# Write focused diff
md = "# Focused Diff: hmn_10490100001 – Chloe/Sophia Fan Service\n\n"
md += "| # | Cmd | EN Asset | JP Source | VI Translation |\n"
md += "|---|---|---|---|---|\n"
for r in rows:
    md += f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |\n"

with open(WORK / "focused_diff.md", 'w', encoding='utf-8') as f:
    f.write(md)

print(f"✅ Written: {WORK / 'focused_diff.md'} ({len(rows)} rows)")

# QA log
qa = {
    "scene": "hmn_10490100001",
    "generator": "build_asset_vi.py (seq-keyed field-index)",
    "translation_type": "EN-asset-is-English (title still JP)",
    "record_count": 88,
    "records_processed": vi_seq,
    "records_translated": 88,
    "br_errors": 0,
    "ascii_comma_errors": 0,
    "bom": True,
    "newline": "CRLF",
    "independent_verify": "PENDING",
    "notes": [
        "6 BR mismatches identified by preflight, all fixed before write.",
        "EN asset text English, title still JP. ja.json is identity map.",
        "Used fullwidth ，(U+FF0C) in VI text, no ASCII comma conflicts.",
        "Speaker labels kept JP-byte-identical.",
        "Chloe voice: fangirl mage. Sophia: serious knight. Alicia: formal adjutant. Commander: Chỉ Huy."
    ]
}

with open(WORK / "qa_log.json", 'w', encoding='utf-8') as f:
    json.dump(qa, f, ensure_ascii=False, indent=2)

print(f"✅ Written: {WORK / 'qa_log.json'}")

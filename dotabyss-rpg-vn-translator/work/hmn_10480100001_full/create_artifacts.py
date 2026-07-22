#!/usr/bin/env python3
"""Create QA artifacts: manifest.json, qa_log.json, focused_diff.md."""
import json, hashlib
from pathlib import Path

EN = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt")
VI = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt")
WORK = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10480100001_full")

en_raw = EN.read_bytes()
vi_raw = VI.read_bytes()

en_sha = hashlib.sha256(en_raw).hexdigest()[:16]
vi_sha = hashlib.sha256(vi_raw).hexdigest()[:16]

en_text = en_raw.decode('utf-8-sig')
vi_text = vi_raw.decode('utf-8-sig')

en_lines = en_text.splitlines(keepends=True)
vi_lines = vi_text.splitlines(keepends=True)

# Record counts
cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
en_records = [ln for ln in en_lines if ln.startswith(cmds)]
vi_records = [ln for ln in vi_lines if ln.startswith(cmds)]

title_en = [ln for ln in en_records if ln.startswith('title,')]
title_vi = [ln for ln in vi_records if ln.startswith('title,')]

# Count commands
cmd_counts = {}
for n in ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,'):
    cmd_counts[n.replace(',','')] = sum(1 for ln in en_records if ln.startswith(n))

# Check BOM
en_bom = en_raw[:3] == b'\xef\xbb\xbf'
vi_bom = vi_raw[:3] == b'\xef\xbb\xbf'

# Check line endings
en_crlf = b'\r\n' in en_raw
vi_crlf = b'\r\n' in vi_raw

# Check ASCII comma in VI text
ascii_commas = 0
for ln in vi_lines:
    if ln.startswith(cmds):
        fields = ln.split(',', 5)
        if len(fields) >= 3:
            text_field = fields[2]
            if ',' in text_field:
                ascii_commas += 1

# Count unchanged text records
unchanged = 0
for i, (el, vl) in enumerate(zip(en_records, vi_records)):
    if el == vl:
        unchanged += 1

# ── Manifest ──
manifest = {
    "scene": "hmn_10480100001",
    "source": {
        "en_asset": str(EN),
        "en_sha": en_sha,
        "ja_json": "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10480100001/ja.json",
        "en_json": "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10480100001/en.json"
    },
    "detection": "EN-asset-is-English with JP title",
    "candidate_counts": cmd_counts,
    "total_records": len(en_records),
    "vi_output": str(VI),
    "vi_sha": vi_sha,
    "bom": vi_bom,
    "crlf": vi_crlf,
    "line_count": len(vi_lines),
    "source_line_count": len(en_lines),
    "unchanged_text_records": int(unchanged > 0),
    "ascii_commas_in_vi": ascii_commas,
    "notes": [
        "EN-asset-is-English case: EN asset text fields are English, en.json non-empty",
        "ja.json has 82 entries; EN asset has 83 text records (1 title + 82 message)",
        "EN[seq=76] duplicate Gwah has no ja.json counterpart; translated same as seq 11",
        "BR count fixed to match EN asset (9 mismatches corrected: 6 removed, 3 added <br>)",
        "Title translated JP→VI in Title Case: Chính Mày Là Kẻ Gây Ra Vụ Cướp",
        "Commander/司令官 → Chỉ Huy",
        "Speaker labels kept JP (セレスト, 露天商, 強盗犯, 警備隊長, ？？？, <user>)",
        "<br> suffix preserved for all message lines",
        "All H18 content translated directly per confirmation (all characters 18+)"
    ]
}

# ── QA Log ──
qa_log = {
    "scene": "hmn_10480100001",
    "build_tool": "build_vi.py",
    "detection": "EN-asset-is-English with JP title (1 title + 82 message)",
    "candidate_counts": cmd_counts,
    "total_records": len(en_records),
    "bom_preserved": en_bom == vi_bom,
    "crlf_preserved": en_crlf == vi_crlf,
    "line_count_match": len(en_lines) == len(vi_lines),
    "record_count_match": len(en_records) == len(vi_records),
    "ascii_commas_in_vi": ascii_commas,
    "unchanged_text_records": unchanged,
    "title_translated": title_en[0].split(',',2)[1] != title_vi[0].split(',',2)[1] if title_en and title_vi else False,
    "br_fixes_applied": 9,
    "notes": manifest["notes"]
}

# ── Focused Diff ──
diff_lines = []
diff_lines.append(f"# Focused Diff: hmn_10480100001 (EN→VI)")
diff_lines.append(f"")
diff_lines.append(f"Detection: EN-asset-is-English with JP title")
diff_lines.append(f"Total EN records: {len(en_records)}")
diff_lines.append(f"Total VI records: {len(vi_records)}")
diff_lines.append(f"BR fixes: 9")
diff_lines.append(f"")
diff_lines.append(f"## Title")
diff_lines.append(f"")
diff_lines.append(f"| EN (JP) | VI |")
diff_lines.append(f"|---|---|")
for el in title_en:
    en_text = el.split(',', 2)[1] if el.startswith('title,') else ''
for vl in title_vi:
    vi_text = vl.split(',', 2)[1] if vl.startswith('title,') else ''
diff_lines.append(f"| {en_text} | {vi_text} |")
diff_lines.append(f"")

diff_lines.append(f"## Message Records ({len(en_records) - len(title_en)})")
diff_lines.append(f"")
diff_lines.append(f"| Seq | EN (condensed) | JP → VI |")
diff_lines.append(f"|---|---|---|")

ja_json_path = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10480100001/ja.json"
jp_map = json.load(open(ja_json_path, encoding='utf-8'))
jp_values = list(jp_map.values())  # 82 values

# For each message record, show condensed EN, JP source, and VI
# seq 0 = title, seq 1..82 = messages
# ja[0] = title text, ja[1..75] → seq 1..75, ja[76..81] → seq 77..82
# seq 76 has no JP

msg_records_en = [ln for ln in en_records if ln.startswith('message,')]
msg_records_vi = [ln for ln in vi_records if ln.startswith('message,')]

for idx, (el, vl) in enumerate(zip(msg_records_en, msg_records_vi)):
    seq = idx + 1  # 1-based message seq
    en_txt = el.split(',', 5)[2] if el.startswith('message,') else ''
    vi_txt = vl.split(',', 5)[2] if vl.startswith('message,') else ''
    
    # JP source
    if seq == 76:
        jp_src = "(duplicate Gwah — no ja.json key)"
    elif seq <= 75:
        jp_src = jp_values[seq]  # ja[seq] because ja[0]=title, ja[1]=first message
    else:
        # seq 77..82 → ja[76..81]
        jp_src = jp_values[seq - 1]  # ja[seq-1]
    
    # Condense EN for display
    en_short = en_txt.replace('<br>', ' | ').replace(',', '，')[:120]
    jp_short = jp_src.replace('<br>', ' | ').replace(',', '，')[:120]
    vi_short = vi_txt.replace('<br>', ' | ').replace(',', '，')[:120]
    
    # Only show entries where EN and VI differ (should be all except intentional)
    if en_txt != vi_txt:
        diff_lines.append(f"| {seq} | {en_short} | {jp_short} → {vi_short} |")

diff_lines.append(f"")
diff_lines.append(f"---")
diff_lines.append(f"BR-fixed seqs: 43, 45, 47, 48 (removed), 57 (added), 63 (removed), 72 (added), 73 (removed), 77 (added)")

# Write all files
WORK.mkdir(parents=True, exist_ok=True)

Path(WORK / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
Path(WORK / "qa_log.json").write_text(json.dumps(qa_log, indent=2, ensure_ascii=False), encoding='utf-8')
Path(WORK / "focused_diff.md").write_text('\n'.join(diff_lines), encoding='utf-8')

print(f"Created {WORK / 'manifest.json'}")
print(f"Created {WORK / 'qa_log.json'}")
print(f"Created {WORK / 'focused_diff.md'}")
print("DONE")

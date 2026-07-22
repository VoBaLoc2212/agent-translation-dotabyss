#!/usr/bin/env python3
"""Generate focused diff for hmn_10440100002"""
import json, re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10440100002/ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10440100002/en.json"
VI_ASSET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100002.txt"

ja_map = json.loads(JA_JSON.read_text(encoding="utf-8"))
jp_keys = list(ja_map.keys())

vi_lines = VI_ASSET.read_text(encoding="utf-8-sig").split("\n")

TEXT_CMDS = ("title,", "message,", "messageTextCenter,", "messageTextUnder,")

COMMA = "\u201A"
records = []
seq = 0
for ln in vi_lines:
    stripped = ln.strip("\r\n ")
    cmd_prefix = None
    for cmd in TEXT_CMDS:
        if stripped.startswith(cmd):
            cmd_prefix = cmd
            break
    if cmd_prefix is None:
        continue
    
    parts = ln.strip("\r\n").split(",")
    tf_idx = 1 if cmd_prefix == "title," else 2
    text_field = parts[tf_idx] if tf_idx < len(parts) else ""
    text_clean = re.sub(r"(?:<[^>]+>\s*)+$", "", text_field)
    records.append((seq, cmd_prefix.rstrip(","), text_clean))
    seq += 1

# Build a reverse lookup from en.json to get JP key for each record
def norm(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("，", ",").replace("　", " ").replace("\u3000", " ")
    s = s.replace("…", "...").replace("—", "--").replace("–", "-")
    s = re.sub(r"\s+", "", s)
    return s

extra_centers = {36, 43}

md = []
md.append("# HMN_10440100002 - Yachiyo Weather Forecast Scene")
md.append("## Focused Diff: JP (ja.json) -> VI (translated)")
md.append("")
md.append(f"Total records: {len(records)}")
md.append("1 title + 89 message + 3 messageTextUnder + 7 messageTextCenter")
md.append("")
md.append("Format: `[seq] command | JP source text | VI translation`")
md.append("---")
md.append("")

ja_idx = 0
for en_seq in range(100):
    _, cmd, vi_text = records[en_seq]
    
    if en_seq in extra_centers:
        jp_text = "(repeat card, no unique JP key)"
    elif ja_idx < len(jp_keys):
        jp_text = jp_keys[ja_idx]
        ja_idx += 1
    else:
        jp_text = "(no JP source)"
    
    md.append(f"### Seq {en_seq} - `{cmd}`")
    md.append(f"- **JP**: {jp_text[:150]}")
    md.append(f"- **VI**: {vi_text[:150]}")
    md.append("")

out = "\n".join(md)
Path("focused_diff.md").write_text(out, encoding="utf-8")
print(f"Done. {len(records)} records, {len(md)} lines.")

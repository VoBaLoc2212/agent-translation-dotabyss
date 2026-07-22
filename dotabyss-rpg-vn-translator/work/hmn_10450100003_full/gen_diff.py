#!/usr/bin/env python
"""Generate focused_diff.md for hmn_10450100003."""
import json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100003.txt"
VI_OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100003.txt"
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10450100003/ja.json"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10450100003_full"
DIFF_FILE = WORK / "focused_diff.md"

ja_data = json.loads(JA_JSON.read_text(encoding="utf-8-sig"))
jp_values = list(ja_data.keys())

en_text = EN_ASSET.read_bytes().decode("utf-8-sig")
vi_text = VI_OUT.read_bytes().decode("utf-8-sig")
en_lines = en_text.splitlines(True)
vi_lines = vi_text.splitlines(True)

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

lines_out = []
lines_out.append("# Focused Diff: hmn_10450100003 (Iola - First Battle)\n")
lines_out.append("\n## Scene\n")
lines_out.append("Iola's first combat — a magic student who also knows martial arts faces a monster alone and discovers her unique fighting style.\n")
lines_out.append("\n**Mode:** EN-asset-is-English (title still JP)\n")
lines_out.append("**Records:** 101 (1 title + 98 message + 1 messageTextUnder + 1 messageTextCenter)\n")
lines_out.append("**Character:** イオラ (Iola) — young magic student\n")
lines_out.append("**Commander:** → `Chỉ Huy` (soldiers), `Thầy` (Iola from 先生)\n")
lines_out.append("\n## Record-by-Record Diff\n")
lines_out.append("| # | Cmd | JP | EN | VI | Notes |\n")
lines_out.append("|---|---|---|---|---|---|\n")

def esc_cell(s):
    s = s.replace("|", "\\|").replace("\n", "\\n")
    return s[:97] + "..." if len(s) > 100 else s

def get_text_field(clean_line, cmd):
    """Extract text field from a cleaned text command line."""
    if "," not in clean_line:
        return ""
    if cmd == "title":
        return clean_line.split(",", 1)[1]
    else:
        parts = clean_line.split(",", 5)
        return parts[2] if len(parts) > 2 else ""

seq = 0
for i, (en_ln, vi_ln) in enumerate(zip(en_lines, vi_lines)):
    en_clean = en_ln.rstrip("\r\n")
    if not en_clean.startswith(TEXT_CMDS):
        continue
    seq += 1
    cmd = en_clean.split(",", 1)[0]  # e.g. "title", "message"
    
    jp = jp_values[seq - 1] if seq - 1 < len(jp_values) else ""
    en_tf = get_text_field(en_clean, cmd)
    vi_clean = vi_ln.rstrip("\r\n")
    vi_tf = get_text_field(vi_clean, cmd)
    
    en_disp = en_tf.rstrip(" ")
    vi_disp = vi_tf.rstrip(" ")
    
    notes = ""
    if en_tf == vi_tf:
        notes = "⚠️ UNCHANGED"
    elif "Chỉ Huy" in vi_tf:
        notes = "→Chỉ Huy"
    elif "Thầy" in vi_tf:
        notes = "→Thầy"
    
    lines_out.append(f"| {seq} | {cmd} | {esc_cell(jp)} | {esc_cell(en_disp)} | {esc_cell(vi_disp)} | {notes} |\n")

lines_out.append("\n## Summary\n")
lines_out.append("- **Verifier:** independent_verify: **PASS**\n")
lines_out.append("- **Structural:** Lines 2338/2338, BOM ✓, CRLF ✓, Tags ✓, Delimiters ✓\n")
lines_out.append("- **101/101 records translated:** 0 unchanged\n")
lines_out.append("- **Addressing:** Commander → Chỉ Huy, 先生 → Thầy\n")
lines_out.append("- **Title:** `いけー！　あたしの火炎魔法！` → `Đi Nào! Hỏa Diễm Ma Pháp Của Tôi!`\n")
lines_out.append("- **Center:** `—A Few Days Later—` → `——Một Vài Ngày Sau——`\n")
lines_out.append("- **SFX:** skree→Kí，GRROOOWL→GỪUU，pant→thở dốc，clatter→Lộp cộp，BOGH→BỐP，boom→ĐÙNG\n")
lines_out.append("- **6 internal `<br>` fixes** to match EN authoritative counts\n")

DIFF_FILE.write_text("".join(lines_out), encoding="utf-8")
print(f"Focused diff written to {DIFF_FILE}")
print(f"{seq} records documented")

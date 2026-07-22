#!/usr/bin/env python3
"""Generate focused diff for hmn_10450100002 (Iola study scene)."""
import json
from pathlib import Path

EN = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt")
VI = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt")
JA = Path("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10450100002/ja.json")
EN_JSON = Path("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10450100002/en.json")
DIFF = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10450100002_full/focused_diff.md")

en_lines = EN.read_text(encoding='utf-8-sig').splitlines(True)
vi_lines = VI.read_text(encoding='utf-8-sig').splitlines(True)
ja_map = json.loads(JA.read_text(encoding='utf-8-sig'))
en_map = json.loads(EN_JSON.read_text(encoding='utf-8-sig'))

# Build JP reverse-lookup: en.json value -> ja.json key
en_to_ja = {}
for k, v in en_map.items():
    if v:  # non-empty
        # Normalize for matching
        vn = v.replace('，', ',').replace('<br> ', '').replace('<br>', '').strip()
        en_to_ja[vn] = k

cmds = ('title,', 'message,', 'messageTextCenter,', 'messageTextUnder,')

md = ["# Focused Diff — hmn_10450100002 (Iola Study Scene)\n",
      "| # | Cmd | Speaker | JP (novel) | EN (asset) | VI (output) |\n",
      "|---|-----|---------|-----------|-----------|-----------|\n"]

seq = 0
for i, (en_ln, vi_ln) in enumerate(zip(en_lines, vi_lines), 1):
    en_s = en_ln.rstrip('\r\n')
    vi_s = vi_ln.rstrip('\r\n')
    
    cmd = None
    for c in cmds:
        if en_s.startswith(c):
            cmd = c
            break
    if not cmd:
        continue
    
    seq += 1
    parts = en_s.split(',')
    
    if cmd == 'title,':
        speaker = ''
        en_tf = parts[1] if len(parts) > 1 else ''
    elif cmd == 'message,':
        speaker = parts[1] if len(parts) > 1 else ''
        en_tf = parts[2] if len(parts) > 2 else ''
    else:
        speaker = parts[1] if len(parts) > 1 else ''
        en_tf = parts[2] if len(parts) > 2 else ''
    
    # Get VI text field
    vi_parts = vi_s.split(',')
    if cmd == 'title,':
        vi_tf = vi_parts[1] if len(vi_parts) > 1 else ''
    else:
        vi_tf = vi_parts[2] if len(vi_parts) > 2 else ''
    
    # Look up JP from en_to_ja
    en_norm = en_tf.replace('，', ',').replace('<br> ', '<br>').strip()
    jp_tf = en_to_ja.get(en_norm, '')
    if not jp_tf:
        # Try without br
        en_norm2 = en_tf.replace('，', ',').replace('<br> ', '').replace('<br>', '').strip()
        jp_tf = en_to_ja.get(en_norm2, '')
    if not jp_tf and cmd == 'title,':
        jp_tf = en_tf  # title is JP
    
    # Truncate for readability
    jp_short = jp_tf[:50].replace('\n', '\\n') if jp_tf else '(n/a)'
    en_short = en_tf[:50].replace('\n', '\\n')
    vi_short = vi_tf[:50].replace('\n', '\\n')
    
    md.append(f"| {seq} | {cmd[:-1]} | {speaker[:15]} | {jp_short} | {en_short} | {vi_short} |\n")

DIFF.parent.mkdir(parents=True, exist_ok=True)
DIFF.write_text(''.join(md), encoding='utf-8')
print(f"Focused diff written: {DIFF} ({len(md)-2} records)")

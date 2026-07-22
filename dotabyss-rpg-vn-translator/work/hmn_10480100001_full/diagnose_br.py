#!/usr/bin/env python3
"""Diagnose all BR mismatches between EN asset and VI translations."""
import sys
from pathlib import Path

EN_ASSET = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt")

# Read VI dict from build script
vi_ns = {}
exec(open("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10480100001_full/build_vi.py").read(), vi_ns)
VI = vi_ns["VI"]

text = EN_ASSET.read_bytes().decode('utf-8-sig')
lines = text.splitlines(keepends=True)

cmds = ('title,', 'message,')
seq = 0
mismatches = []
for ln in lines:
    if not ln.startswith(cmds):
        continue
    stripped = ln.rstrip('\r\n')
    vi_text = VI[seq]
    if ln.startswith('message,'):
        parts = stripped.split(',', 5)
        en_text = parts[2]
        if en_text.rstrip().endswith('<br>'):
            idx = en_text.rfind('<br>')
            internal_en = en_text[:idx]
        else:
            internal_en = en_text
        en_br = internal_en.count('<br>')
        vi_br = vi_text.count('<br>')
        if en_br != vi_br:
            mismatches.append((seq, en_br, vi_br, internal_en[:120], vi_text[:120]))
    seq += 1

print(f"Total BR mismatches: {len(mismatches)}")
for seq, en_br, vi_br, en_txt, vi_txt in mismatches:
    print(f"  Seq {seq}: EN br={en_br} VI br={vi_br}")
    print(f"    EN: {en_txt}")
    print(f"    VI: {vi_txt}")
    print()

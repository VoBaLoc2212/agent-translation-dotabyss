#!/usr/bin/env python3
"""Dump exact text records with BR counts from EN asset."""
import re

EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"

with open(EN_PATH, 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8-sig')
lines = text.split('\n')

seq = 0
cmd_counts = {}
for i, ln in enumerate(lines):
    ln_stripped = ln.strip()
    if not ln_stripped:
        continue
    
    parts = ln_stripped.split(',', 5)
    cmd = parts[0]
    
    if cmd == 'title,':
        # title line: title,text
        # The stripped line starts with 'title,'
        # So parts[0] = 'title' (the comma is the delimiter)
        text_field = ln_stripped[len('title,'):]
        br_cnt = text_field.count('<br>')
        cmd_counts['title'] = cmd_counts.get('title', 0) + 1
        print(f"seq={seq:3d}  line={i+1:3d}  cmd=title       br={br_cnt}  text={repr(text_field[:120])}")
        seq += 1
    elif cmd in ('messageTextUnder', 'messageTextCenter'):
        # these might have format: cmd,text,rest
        text_field = parts[2] if len(parts) > 2 else ''
        br_cnt = text_field.count('<br>')
        cmd_counts[cmd] = cmd_counts.get(cmd, 0) + 1
        print(f"seq={seq:3d}  line={i+1:3d}  cmd={cmd:20s}  br={br_cnt}  text={repr(text_field[:120])}")
        seq += 1
    elif cmd == 'message':
        # message,NAME,TEXT,...
        if len(parts) >= 3:
            text_field = parts[2]
            # Check if there's a raw suffix (for reconstruction)
            br_cnt = text_field.count('<br>')
            trailing = parts[3:] if len(parts) > 3 else []
            cmd_counts['message'] = cmd_counts.get('message', 0) + 1
            print(f"seq={seq:3d}  line={i+1:3d}  cmd=message     br={br_cnt}  trailing={trailing}  text={repr(text_field[:100])}")
        else:
            print(f"seq={seq:3d}  line={i+1:3d}  cmd=message  SHORT! parts={parts}")
        seq += 1

print(f"\n\nTOTAL: title={cmd_counts.get('title',0)} message={cmd_counts.get('message',0)} "
      f"messageTextUnder={cmd_counts.get('messageTextUnder',0)} "
      f"messageTextCenter={cmd_counts.get('messageTextCenter',0)}")
print(f"GRAND TOTAL: {sum(cmd_counts.values())}")

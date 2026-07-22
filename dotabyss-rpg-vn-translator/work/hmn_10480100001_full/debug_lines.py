#!/usr/bin/env python3
"""Quick debug: check which lines are getting corrupted in the VI build."""
import json, re

EN_ASSET = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt"

with open(EN_ASSET, 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8-sig')
en_lines = text.splitlines(True)
print(f"Original: {len(en_lines)} lines")

# Check the ending of every line
for i, line in enumerate(en_lines):
    if i < 5 or i > len(en_lines) - 3:
        print(f"L{i}: end={repr(line[-10:])} len={len(line)}")

# Check text command lines specifically
text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
for i, line in enumerate(en_lines):
    for cmd in text_cmds:
        if line.startswith(cmd):
            parts = line.split(',', 5)
            ending = repr(line[-10:])
            n_parts = len(parts)
            print(f"L{i}: cmd={cmd} parts={n_parts} end={ending} last_part_end={repr(parts[-1][-10:])}")
            break

print("\n--- Checking last line ---")
print(f"Last line: {repr(en_lines[-1][:40])} end={repr(en_lines[-1][-10:])}")

#!/usr/bin/env python3
"""Debug: check why join reduces line count."""
import json, re

EN_ASSET = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt"

with open(EN_ASSET, 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8-sig')
en_lines = text.splitlines(True)

# Simulate the build
out_lines_list = list(en_lines)

# Check for \r\r\n sequences
count_double_crlf = 0
for i, line in enumerate(en_lines):
    if '\r\r\n' in line:
        count_double_crlf += 1
        if count_double_crlf <= 5:
            print(f"L{i}: has double CRLF: {repr(line[:30])} ... {repr(line[-10:])}")

# Just join without any changes
joined = ''.join(out_lines_list)
re_split = joined.splitlines(True)
print(f"\nOriginal lines: {len(en_lines)}")
print(f"Re-joined+split: {len(re_split)}")
print(f"Double CRLF occurrences: {count_double_crlf}")
print(f"Joined size: {len(joined)} vs original {len(raw)}")

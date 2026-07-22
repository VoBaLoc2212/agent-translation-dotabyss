import json
import re
import os

# Load EN asset lines
with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'r', encoding='utf-8-sig') as f:
    en_asset_lines = [line.rstrip('\n\r') for line in f]

TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
en_asset_records = []
for i, line in enumerate(en_asset_lines):
    for cmd in TEXT_CMDS:
        if line.startswith(cmd):
            parts = line.split(',', 5)
            speaker = parts[1] if len(parts) > 1 else ''
            text_field = parts[2] if len(parts) > 2 else ''
            en_asset_records.append((i, cmd, speaker, text_field, line))
            break

print(f"EN asset text records: {len(en_asset_records)}")

# Load ja.json keys
with open('dotabyss-translation-main/translations/novels/hmn_10440100001/ja.json', 'r', encoding='utf-8') as f:
    ja_data = json.load(f)
jp_keys = list(ja_data.keys())
print(f"JA keys: {len(jp_keys)}")

def count_br(text):
    return text.count('<br>')

# Check BR counts for each record
print("\n=== EN Asset BR counts per record ===")
for seq, (line_idx, cmd, speaker, text_field, full_line) in enumerate(en_asset_records):
    br = count_br(text_field)
    if seq < len(jp_keys):
        jp_key = jp_keys[seq]
        print(f"  Seq {seq:3d} (line {line_idx:4d}) {cmd} BR={br} | JP: {jp_key[:60]}")
    else:
        print(f"  Seq {seq:3d} (line {line_idx:4d}) {cmd} BR={br} | EXTRA: {text_field[:60]}")

# Now I need to create VI translations with exact BR counts matching EN asset
# The VI translations should be adjusted to have the same number of <br> as the EN asset text_field
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Count text records in the EN asset and check alignment."""
from pathlib import Path
import json

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10470100001"

en_file = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
ja_file = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
en_json_file = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"

data = en_file.read_bytes()
text = data.decode("utf-8-sig")
lines = text.splitlines(True)

bom = data[:3]
has_crlf = b"\r\n" in data
print(f"EN asset BOM bytes: {bom.hex()}")
print(f"EN asset has CRLF: {has_crlf}")
print(f"EN asset total lines: {len(lines)}")

records = []
for i, ln in enumerate(lines, 1):
    stripped = ln.strip()
    if stripped.startswith(("title,", "message,", "messageTextUnder,", "messageTextCenter,")):
        records.append((i, stripped))

print(f"\nText records: {len(records)}")
for i, stripped in records:
    cmd = stripped.split(",")[0]
    preview = stripped[:90]
    print(f"  L{i:4d}: {cmd:25s} | {preview}")

with open(ja_file, encoding="utf-8") as f:
    ja_data = json.load(f)
print(f"\nja.json entries: {len(ja_data)}")

with open(en_json_file, encoding="utf-8") as f:
    en_data = json.load(f)
print(f"en.json entries: {len(en_data)}")

# Check first few en.json values
for i, (k, v) in enumerate(en_data.items()):
    if i >= 3:
        break
    snippet = v[:60] if v else "(empty)"
    print(f"  en.json[{k[:30]}]: \"{snippet}\"")

# Map each ja.json entry to the corresponding EN asset text field
# ja.json and en.json are ordered dicts, keys in same order
ja_keys = list(ja_data.keys())
if len(ja_keys) == len(records):
    print(f"\nRecords count MATCH: {len(ja_keys)} ja.json entries == {len(records)} EN records")
else:
    print(f"\nRecords count MISMATCH: {len(ja_keys)} ja.json entries != {len(records)} EN records")
    print("This means some EN records may not have a direct JP counterpart")

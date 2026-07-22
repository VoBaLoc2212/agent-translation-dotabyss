#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract EN asset text fields vs JP source alignment for translation."""
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

with open(ja_file, encoding="utf-8") as f:
    ja_map = json.load(f)
with open(en_json_file, encoding="utf-8") as f:
    en_map = json.load(f)

ja_keys = list(ja_map.keys())
ja_vals = list(ja_map.values())
en_vals = list(en_map.values())

# Iterate text records and show alignment
idx = 0
for ln in lines:
    stripped = ln.strip()
    if stripped.startswith(("title,", "message,", "messageTextUnder,", "messageTextCenter,")):
        cmd = stripped.split(",")[0]
        
        # Get the text field
        if cmd == "title,":
            # title,<text> - split at first comma
            text_field = stripped.split(",", 1)[1]
        else:
            # message,<speaker>,<text>,...
            parts = stripped.split(",", 5)
            text_field = parts[2] if len(parts) > 2 else ""
        
        jp_key = ja_keys[idx] if idx < len(ja_keys) else "N/A"
        jp_val = ja_vals[idx] if idx < len(ja_vals) else "N/A"
        en_val = en_vals[idx] if idx < len(en_vals) else "N/A"
        
        br_count = text_field.count("<br>")
        
        print(f"=== RECORD {idx+1} === (cmd={cmd}, br={br_count})")
        print(f"  EN ASSET TEXT: {text_field[:120]}")
        print(f"  JP KEY:        {jp_key[:80]}")
        print(f"  JP VAL:        {jp_val[:80]}")
        if en_val:
            print(f"  EN VAL:        {en_val[:80]}")
        print()
        
        idx += 1

assert idx == 80, f"Expected 80 records, got {idx}"

#!/usr/bin/env python3
"""
Build complete JP->VI map from existing VI asset (more complete than vi.json).
"""

import json
from pathlib import Path

EN_ASSET = Path(r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt")
VI_ASSET = Path(r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt")
JA_JSON = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json")
EN_JSON = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json")

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# Load ja.json (JP identity)
with open(JA_JSON, "r", encoding="utf-8-sig") as f:
    ja_data = json.load(f)

# Load en.json (JP -> EN)
with open(EN_JSON, "r", encoding="utf-8-sig") as f:
    en_data = json.load(f)

# Build EN -> JP reverse map
en_to_jp = {v: k for k, v in en_data.items()}

# Read assets
en_bytes = EN_ASSET.read_bytes()
en_text = en_bytes.decode("utf-8-sig")
en_lines = en_text.splitlines(True)

vi_bytes = VI_ASSET.read_bytes()
vi_text = vi_bytes.decode("utf-8-sig")
vi_lines = vi_text.splitlines(True)

# Align text records and build JP -> VI map
jp_to_vi = {}
text_idx = 0

for en_line, vi_line in zip(en_lines, vi_lines):
    en_clean = en_line.lstrip("\ufeff").rstrip("\r\n")
    vi_clean = vi_line.lstrip("\ufeff").rstrip("\r\n")
    
    if en_clean.startswith(TEXT_CMDS):
        en_parts = en_clean.split(",", 5)
        vi_parts = vi_clean.split(",", 5)
        
        if en_clean.startswith("title,"):
            if len(en_parts) == 2 and len(vi_parts) == 2:
                en_text_field = en_parts[1]
                vi_text_field = vi_parts[1]
                
                # Find JP key for this EN text
                if en_text_field in en_to_jp:
                    jp_key = en_to_jp[en_text_field]
                    if vi_text_field != en_text_field:  # Only if actually translated
                        jp_to_vi[jp_key] = vi_text_field
                        print(f"Mapped: {jp_key[:50]}... -> {vi_text_field[:50]}...")
        else:
            if len(en_parts) == 6 and len(vi_parts) == 6:
                en_text_field = en_parts[2]
                vi_text_field = vi_parts[2]
                
                if en_text_field in en_to_jp:
                    jp_key = en_to_jp[en_text_field]
                    if vi_text_field != en_text_field:  # Only if actually translated
                        jp_to_vi[jp_key] = vi_text_field
                        print(f"Mapped: {jp_key[:50]}... -> {vi_text_field[:50]}...")
        
        text_idx += 1

print(f"\nBuilt JP->VI map with {len(jp_to_vi)} entries")

# Save to vi.json
vi_json_path = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/vi.json")
with open(vi_json_path, "w", encoding="utf-8") as f:
    json.dump(jp_to_vi, f, ensure_ascii=False, indent=2)
print(f"Saved to {vi_json_path}")
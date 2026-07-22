#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete translation script for hmn_10500100002 - with fuzzy matching
"""

import json
import os
import difflib

# File paths
JA_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json"
EN_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json"
EN_ASSET = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
VI_OUTPUT = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
VI_JSON_OUT = "E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100002_full/vi.json"

# Load JSON files
with open(JA_JSON, 'r', encoding='utf-8') as f:
    ja_json = json.load(f)

with open(EN_JSON, 'r', encoding='utf-8') as f:
    en_json = json.load(f)

with open(VI_JSON_OUT, 'r', encoding='utf-8') as f:
    vi_json = json.load(f)

# Build EN -> JP reverse mapping with normalized keys
def normalize_en(text):
    """Normalize EN text for matching - remove <br>, normalize punctuation/whitespace"""
    if not text:
        return ''
    t = text.strip()
    # Remove <br> tags
    t = t.replace('<br> ', '').replace('<br>', '')
    # Replace fullwidth comma with halfwidth
    t = t.replace('，', ',')
    # Replace fullwidth colon with halfwidth
    t = t.replace('：', ':')
    # Replace fullwidth period with halfwidth
    t = t.replace('。', '.')
    # Replace em dash with regular dash
    t = t.replace('—', '-')
    t = t.replace('–', '-')
    # Replace fullwidth question/exclamation
    t = t.replace('？', '?')
    t = t.replace('！', '!')
    # Normalize whitespace
    t = ' '.join(t.split())
    return t

# Build multiple normalized versions for each EN entry
en_to_jp = {}
en_normalized = {}  # map normalized -> original EN text
for jp_key, en_val in en_json.items():
    if en_val and en_val.strip():
        norm = normalize_en(en_val)
        en_to_jp[norm] = jp_key
        en_normalized[norm] = en_val.strip()

print(f"Built EN->JP map with {len(en_to_jp)} entries")

# JP -> VI mapping
jp_to_vi = vi_json

# Read EN asset file
with open(EN_ASSET, 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

# Process each line
vi_lines = []
translated_count = 0
fuzzy_count = 0
skipped_count = 0

for line in en_lines:
    line = line.rstrip('\r\n')
    if not line:
        vi_lines.append('')
        continue
    
    parts = line.split(',', 5)
    if len(parts) < 6:
        vi_lines.append(line)
        continue
    
    # Only translate message lines
    if parts[0] == 'message' and parts[2].strip():
        en_text = parts[2].strip()
        
        # Check if ends with <br>
        has_br = en_text.endswith('<br> ') or en_text.endswith('<br>')
        if has_br:
            en_text_clean = en_text.replace('<br> ', '').replace('<br>', '')
        else:
            en_text_clean = en_text
        
        # Normalize for lookup
        norm_text = normalize_en(en_text_clean)
        
        # Try exact match first
        jp_text = en_to_jp.get(norm_text)
        
        # If no exact match, try fuzzy match
        if not jp_text:
            matches = difflib.get_close_matches(norm_text, en_to_jp.keys(), n=1, cutoff=0.85)
            if matches:
                jp_text = en_to_jp[matches[0]]
                fuzzy_count += 1
                print(f"  FUZZY MATCH: {norm_text[:60]}... -> {matches[0][:60]}...")
        
        vi_text = ''
        if jp_text:
            vi_text = jp_to_vi.get(jp_text, '')
        
        if vi_text:
            # Add back <br> suffix if original had it
            if has_br and not vi_text.endswith('<br> '):
                vi_text = vi_text + '<br> '
            parts[2] = vi_text
            translated_count += 1
            print(f"  TRANSLATED: {en_text_clean[:60]}... -> {vi_text[:60]}...")
        else:
            skipped_count += 1
            if skipped_count <= 10:
                print(f"  MISSING VI: {norm_text[:80]}...")
                if jp_text:
                    print(f"    JP key found: {jp_text}")
                    print(f"    VI translation missing")
    
    vi_lines.append(','.join(parts))

# Write VI output with BOM + CRLF
os.makedirs(os.path.dirname(VI_OUTPUT), exist_ok=True)
with open(VI_OUTPUT, 'w', encoding='utf-8-sig', newline='\r\n') as f:
    for line in vi_lines:
        f.write(line + '\r\n')

print(f"\n=== SUMMARY ===")
print(f"EN lines: {len(en_lines)}")
print(f"VI lines: {len(vi_lines)}")
print(f"Translated (exact): {translated_count - fuzzy_count}")
print(f"Translated (fuzzy): {fuzzy_count}")
print(f"Total translated: {translated_count}")
print(f"Skipped: {skipped_count}")
print(f"Output: {VI_OUTPUT}")
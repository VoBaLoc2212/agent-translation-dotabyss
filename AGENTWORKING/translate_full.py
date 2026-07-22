#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete translation script for hmn_10500100002
"""

import json
import os

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

# Build EN -> JP reverse mapping
# Normalize EN text: replace fullwidth comma with halfwidth, normalize whitespace
def normalize_en(text):
    """Normalize EN text for matching"""
    if not text:
        return ''
    t = text.strip()
    # Remove trailing <br> and space
    t = t.replace('<br> ', '').replace('<br>', '')
    # Replace fullwidth comma with halfwidth
    t = t.replace('，', ',')
    # Replace em dash with regular dash (the EN JSON has regular dash)
    t = t.replace('—', '-')
    # Normalize spaces
    t = ' '.join(t.split())
    return t

en_to_jp = {}
for jp_key, en_val in en_json.items():
    if en_val and en_val.strip():
        norm = normalize_en(en_val)
        en_to_jp[norm] = jp_key

print(f"Built EN->JP map with {len(en_to_jp)} entries")

# JP -> VI mapping
jp_to_vi = vi_json

# Read EN asset file
with open(EN_ASSET, 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

# Process each line
vi_lines = []
translated_count = 0
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
            en_text = en_text.replace('<br> ', '').replace('<br>', '')
        
        # Normalize for lookup
        norm_text = normalize_en(en_text)
        
        jp_text = en_to_jp.get(norm_text)
        vi_text = ''
        if jp_text:
            vi_text = jp_to_vi.get(jp_text, '')
        
        if vi_text:
            # Add back <br> suffix if original had it
            if has_br and not vi_text.endswith('<br> '):
                vi_text = vi_text + '<br> '
            parts[2] = vi_text
            translated_count += 1
            print(f"  TRANSLATED: {en_text[:60]}... -> {vi_text[:60]}...")
        else:
            skipped_count += 1
            if skipped_count <= 10:
                print(f"  MISSING: {norm_text[:80]}...")
                # Show close matches
                for k in en_to_jp:
                    if k.startswith(norm_text[:20]):
                        print(f"    CLOSE: {k[:80]}...")
                        break
    
    vi_lines.append(','.join(parts))

# Write VI output with BOM + CRLF
os.makedirs(os.path.dirname(VI_OUTPUT), exist_ok=True)
with open(VI_OUTPUT, 'w', encoding='utf-8-sig', newline='\r\n') as f:
    for line in vi_lines:
        f.write(line + '\r\n')

print(f"\n=== SUMMARY ===")
print(f"EN lines: {len(en_lines)}")
print(f"VI lines: {len(vi_lines)}")
print(f"Translated: {translated_count}")
print(f"Skipped: {skipped_count}")
print(f"Output: {VI_OUTPUT}")
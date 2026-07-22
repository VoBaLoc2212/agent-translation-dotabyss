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

# Build EN -> JP reverse mapping with multiple normalized versions
def normalize_en(text):
    """Normalize EN text for matching - remove <br>, normalize punctuation/whitespace"""
    if not text:
        return ''
    t = text.strip()
    # Remove <br> tags
    t = t.replace('<br> ', '').replace('<br>', '')
    # Replace fullwidth comma with halfwidth
    t = t.replace('，', ',')
    # Replace em dash with regular dash
    t = t.replace('—', '-')
    # Replace ellipsis with three dots
    t = t.replace('…', '...')
    # Replace curly quotes
    t = t.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
    # Normalize whitespace
    t = ' '.join(t.split())
    return t

def normalize_en_loose(text):
    """Even looser normalization - remove all punctuation and extra spaces"""
    if not text:
        return ''
    t = normalize_en(text)
    # Remove all punctuation except alphanumeric
    import re
    t = re.sub(r'[^\w\s]', '', t)
    t = ' '.join(t.split())
    return t.lower()

en_to_jp = {}
en_to_jp_loose = {}

for jp_key, en_val in en_json.items():
    if en_val and en_val.strip():
        norm = normalize_en(en_val)
        en_to_jp[norm] = jp_key
        loose = normalize_en_loose(en_val)
        en_to_jp_loose[loose] = jp_key

print(f"Built EN->JP map with {len(en_to_jp)} exact + {len(en_to_jp_loose)} loose entries")

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
        
        # Try exact normalized match
        norm_text = normalize_en(en_text)
        jp_text = en_to_jp.get(norm_text)
        
        # Try loose match if exact fails
        if not jp_text:
            loose_text = normalize_en_loose(en_text)
            jp_text = en_to_jp_loose.get(loose_text)
        
        # Try difflib close match if still not found
        if not jp_text and en_to_jp:
            # Find best match using difflib
            matches = difflib.get_close_matches(norm_text, list(en_to_jp.keys()), n=1, cutoff=0.85)
            if matches:
                jp_text = en_to_jp[matches[0]]
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
            print(f"  TRANSLATED: {en_text[:60]}... -> {vi_text[:60]}...")
        else:
            skipped_count += 1
            if skipped_count <= 15:
                print(f"  MISSING: {norm_text[:80]}...")
    
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
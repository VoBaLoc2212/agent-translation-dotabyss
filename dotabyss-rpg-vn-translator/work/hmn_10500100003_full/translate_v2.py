#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate EN asset to VI using vi.json, preserving structure exactly.
Uses normalized matching to handle fullwidth/halfwidth differences.
"""

import json
import re

def normalize_text(text: str) -> str:
    """Normalize text for matching: fullwidth->halfwidth, strip trailing whitespace, normalize <br>"""
    # Fullwidth to halfwidth
    text = text.replace('，', ',').replace('。', '.').replace('！', '!').replace('？', '?')
    text = text.replace('：', ':').replace('；', ';').replace('（', '(').replace('）', ')')
    text = text.replace('「', '"').replace('」', '"').replace('『', '"').replace('』', '"')
    text = text.replace('　', ' ')  # ideographic space
    # Normalize <br> variants
    text = re.sub(r'<br\s*/?>', '<br>', text, flags=re.IGNORECASE)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Load vi.json
with open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100003_full/vi.json', 'r', encoding='utf-8') as f:
    vi_map = json.load(f)

# Load en.json
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100003/en.json', 'r', encoding='utf-8') as f:
    en_map = json.load(f)

# Create EN->VI mapping with normalized keys
en_to_vi = {}
for ja_key, en_val in en_map.items():
    if ja_key in vi_map:
        vi_val = vi_map[ja_key]
        norm_en = normalize_text(en_val)
        en_to_vi[norm_en] = vi_val

print(f"Built {len(en_to_vi)} EN->VI mappings")

# Load EN asset
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Process each line
output_lines = []
title_translated = False

for line in lines:
    stripped = line.rstrip('\n\r')
    
    if stripped.startswith('title,'):
        parts = stripped.split(',', 1)
        if len(parts) >= 2:
            ja_title = parts[1]
            if ja_title in vi_map:
                parts[1] = vi_map[ja_title]
                title_translated = True
            output_lines.append(','.join(parts))
        else:
            output_lines.append(stripped)
    elif stripped.startswith('message,'):
        parts = stripped.split(',', 5)
        if len(parts) >= 6:
            en_text = parts[2]
            norm_en = normalize_text(en_text)
            
            if norm_en in en_to_vi:
                vi_text = en_to_vi[norm_en]
                # Preserve <br> suffix from original
                if en_text.endswith('<br> ') and not vi_text.endswith('<br> '):
                    vi_text = vi_text + '<br> '
                elif en_text.endswith('<br>') and not vi_text.endswith('<br>'):
                    vi_text = vi_text + '<br>'
                parts[2] = vi_text
            output_lines.append(','.join(parts))
        else:
            output_lines.append(stripped)
    else:
        output_lines.append(stripped)

# Write VI output with BOM and CRLF
with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'w', encoding='utf-8-sig', newline='\r\n') as f:
    for i, out_line in enumerate(output_lines):
        f.write(out_line)
        if i < len(output_lines) - 1:
            f.write('\r\n')
        else:
            f.write('\r\n')

print(f"Written {len(output_lines)} lines")

# Verify line count
with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    vi_lines = f.readlines()

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

print(f"EN lines: {len(en_lines)}")
print(f"VI lines: {len(vi_lines)}")
print(f"Title translated: {title_translated}")
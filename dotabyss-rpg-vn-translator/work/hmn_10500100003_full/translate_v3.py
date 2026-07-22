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

# Load EN asset (binary to preserve exact CRLF)
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    raw = f.read()

# Detect BOM
has_bom = raw.startswith(b'\xef\xbb\xbf')
if has_bom:
    raw = raw[3:]

# Detect newline style
has_crlf = b'\r\n' in raw

# Decode
text = raw.decode('utf-8', errors='replace')
lines = text.splitlines(True)  # keep line endings

# Process each line
output_lines = []
title_translated = False

for line in lines:
    # Remove line ending for processing
    line_content = line.rstrip('\r\n')
    
    if line_content.startswith('title,'):
        parts = line_content.split(',', 1)
        if len(parts) >= 2:
            ja_title = parts[1]
            if ja_title in vi_map:
                parts[1] = vi_map[ja_title]
                title_translated = True
            output_lines.append(','.join(parts))
        else:
            output_lines.append(line_content)
    elif line_content.startswith('message,'):
        parts = line_content.split(',', 5)
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
            output_lines.append(line_content)
    else:
        output_lines.append(line_content)

# Write VI output with BOM and correct newlines
output_text = '\n'.join(output_lines) + '\n'
if has_crlf:
    output_text = output_text.replace('\n', '\r\n')

if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_text.encode('utf-8')
else:
    output_bytes = output_text.encode('utf-8')

with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'wb') as f:
    f.write(output_bytes)

print(f"Written {len(output_lines)} lines")

# Verify line count
with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    vi_raw = f.read()
vi_has_bom = vi_raw.startswith(b'\xef\xbb\xbf')
if vi_has_bom:
    vi_raw = vi_raw[3:]
vi_text = vi_raw.decode('utf-8', errors='replace')
vi_lines = vi_text.splitlines()

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    en_raw = f.read()
en_has_bom = en_raw.startswith(b'\xef\xbb\xbf')
if en_has_bom:
    en_raw = en_raw[3:]
en_text = en_raw.decode('utf-8', errors='replace')
en_lines = en_text.splitlines()

print(f"EN lines: {len(en_lines)}")
print(f"VI lines: {len(vi_lines)}")
print(f"Title translated: {title_translated}")
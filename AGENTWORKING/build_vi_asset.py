#!/usr/bin/env python3
"""
Build Vietnamese asset file for hmn_10500100002
Replaces EN text fields with VI translations while preserving all technical structure.
"""

import json
import re

# Load translations
with open('E:/AgentTranslation/translate_hmn10500100002.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# Now translations dict is available

# Read the EN asset file
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt', 'rb') as f:
    raw = f.read()

# Detect BOM
has_bom = raw.startswith(b'\xef\xbb\xbf')
if has_bom:
    raw = raw[3:]

# Detect line ending
has_crlf = b'\r\n' in raw

# Decode
text = raw.decode('utf-8')

# Split lines preserving endings
lines = text.splitlines(keepends=True)

# Extract text commands in order (matching JP order)
text_commands = []
for i, line in enumerate(lines):
    if line.startswith('title,') or line.startswith('message,') or line.startswith('messageTextUnder,') or line.startswith('messageTextCenter,'):
        if line.startswith('title,'):
            parts = line.split(',', 1)
            if len(parts) >= 2:
                text_field = parts[1].rstrip('\r\n')
                text_commands.append(('title', i, text_field, line))
        elif line.startswith('message,'):
            parts = line.split(',', 2)
            if len(parts) >= 3:
                text_field = parts[2].rstrip('\r\n')
                text_commands.append(('message', i, text_field, line))
        elif line.startswith('messageTextUnder,'):
            parts = line.split(',', 2)
            if len(parts) >= 3:
                text_field = parts[2].rstrip('\r\n')
                text_commands.append(('messageTextUnder', i, text_field, line))
        elif line.startswith('messageTextCenter,'):
            parts = line.split(',', 2)
            if len(parts) >= 3:
                text_field = parts[2].rstrip('\r\n')
                text_commands.append(('messageTextCenter', i, text_field, line))

print(f"Found {len(text_commands)} text commands in asset")

# Load JP texts in order
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json', 'r', encoding='utf-8-sig') as f:
    ja_data = json.load(f, object_pairs_hook=list)

jp_texts = [v for k, v in ja_data]
print(f"JP texts count: {len(jp_texts)}")

# Verify alignment
if len(text_commands) != len(jp_texts) + 1:  # +1 for title which is also in ja_data
    print(f"WARNING: Count mismatch! Asset commands: {len(text_commands)}, JP texts: {len(jp_texts)}")
    # The title is the first entry in ja_data
    # text_commands[0] is title, text_commands[1:] are messages
    # ja_data[0] is title, ja_data[1:] are messages
    pass

# Build VI translations for each text command by matching JP text
vi_translations = []
for idx, (cmd_type, line_num, en_text, orig_line) in enumerate(text_commands):
    if idx == 0:
        # Title
        jp_key = jp_texts[0]
    else:
        # Messages
        jp_key = jp_texts[idx]
    
    if jp_key in translations:
        vi_text = translations[jp_key]
        vi_translations.append((cmd_type, line_num, vi_text, orig_line))
        print(f"  [{idx}] {cmd_type}: OK")
    else:
        print(f"  [{idx}] {cmd_type}: MISSING JP key: {jp_key[:60]}")
        # Keep original EN text
        vi_translations.append((cmd_type, line_num, en_text, orig_line))

print(f"VI translations ready: {len(vi_translations)}")

# Now rebuild the file
output_lines = lines[:]
for cmd_type, line_num, vi_text, orig_line in vi_translations:
    line = lines[line_num]
    if line.startswith('title,'):
        # title,<text>
        parts = line.split(',', 1)
        if len(parts) >= 2:
            # Preserve the original line ending
            ending = line[len(line.rstrip('\r\n')):]
            new_line = f"title,{vi_text}{ending}"
            output_lines[line_num] = new_line
    elif line.startswith('message,'):
        # message,<speaker>,<text>,...
        parts = line.split(',', 2)
        if len(parts) >= 3:
            ending = line[len(line.rstrip('\r\n')):]
            # Rebuild with new text field
            new_line = f"{parts[0]},{parts[1]},{vi_text}{ending}"
            output_lines[line_num] = new_line
    elif line.startswith('messageTextUnder,'):
        parts = line.split(',', 2)
        if len(parts) >= 3:
            ending = line[len(line.rstrip('\r\n')):]
            new_line = f"{parts[0]},{parts[1]},{vi_text}{ending}"
            output_lines[line_num] = new_line
    elif line.startswith('messageTextCenter,'):
        parts = line.split(',', 2)
        if len(parts) >= 3:
            ending = line[len(line.rstrip('\r\n')):]
            new_line = f"{parts[0]},{parts[1]},{vi_text}{ending}"
            output_lines[line_num] = new_line

# Verify line count
assert len(output_lines) == len(lines), f"Line count mismatch: {len(output_lines)} vs {len(lines)}"

# Verify text commands count
new_text_commands = 0
for line in output_lines:
    if line.startswith('title,') or line.startswith('message,') or line.startswith('messageTextUnder,') or line.startswith('messageTextCenter,'):
        new_text_commands += 1
assert new_text_commands == len(text_commands), f"Text command count mismatch"

# Write output
output_text = ''.join(output_lines)
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_text.encode('utf-8')
else:
    output_bytes = output_text.encode('utf-8')

output_path = 'E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt'
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'wb') as f:
    f.write(output_bytes)

print(f"Written to: {output_path}")
print(f"Lines: {len(output_lines)}")
print(f"BOM: {has_bom}")
print(f"CRLF: {has_crlf}")
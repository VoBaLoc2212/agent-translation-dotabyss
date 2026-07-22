import json
import re

# Load vi.json
with open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100003_full/vi.json', 'r', encoding='utf-8') as f:
    vi_map = json.load(f)

# Load EN asset
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Build reverse mapping from EN to VI
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100003/en.json', 'r', encoding='utf-8') as f:
    en_map = json.load(f)

# Create EN->VI mapping
en_to_vi = {}
for ja_key, en_val in en_map.items():
    if ja_key in vi_map:
        vi_val = vi_map[ja_key]
        en_clean = en_val.rstrip()
        en_to_vi[en_clean] = vi_val

print(f"Loaded {len(en_to_vi)} EN->VI mappings")

# Process each line
output_lines = []
for line in lines:
    stripped = line.rstrip('\n\r')
    
    # Only process 'message' and 'title' commands
    if stripped.startswith('message,'):
        parts = stripped.split(',', 5)
        if len(parts) >= 6:
            en_text = parts[2]
            has_br = en_text.endswith('<br> ') or en_text.endswith('<br>')
            
            vi_text = None
            if en_text in en_to_vi:
                vi_text = en_to_vi[en_text]
            else:
                en_stripped = en_text.rstrip()
                if en_stripped in en_to_vi:
                    vi_text = en_to_vi[en_stripped]
            
            if vi_text:
                if has_br and not vi_text.endswith('<br> '):
                    vi_text = vi_text + '<br> '
                parts[2] = vi_text
            
            output_lines.append(','.join(parts))
        else:
            output_lines.append(stripped)
    elif stripped.startswith('title,'):
        parts = stripped.split(',', 1)
        if len(parts) >= 2:
            ja_title = parts[1]
            if ja_title in vi_map:
                parts[1] = vi_map[ja_title]
            output_lines.append(','.join(parts))
        else:
            output_lines.append(stripped)
    else:
        # Keep all other lines as-is
        output_lines.append(stripped)

# Write output with BOM and CRLF
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
print(f"VI file has {len(vi_lines)} lines")

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()
print(f"EN file has {len(en_lines)} lines")

# Check a few message lines
for i, line in enumerate(vi_lines[:60]):
    if line.startswith('message,'):
        print(f"Line {i+1}: {line.strip()}")
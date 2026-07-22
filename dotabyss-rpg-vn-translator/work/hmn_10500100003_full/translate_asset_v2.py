import json
import re

# Load vi.json
with open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100003_full/vi.json', 'r', encoding='utf-8') as f:
    vi_map = json.load(f)

# Load EN asset
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

# Load en.json to get EN->JA mapping
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100003/en.json', 'r', encoding='utf-8') as f:
    en_map = json.load(f)

# Create JA->VI mapping from vi.json
ja_to_vi = vi_map

# Create EN->VI mapping using en.json (EN values) and vi.json (JA keys)
en_to_vi = {}
for ja_key, en_val in en_map.items():
    if ja_key in ja_to_vi:
        vi_val = ja_to_vi[ja_key]
        # Normalize EN value for matching
        en_norm = en_val.rstrip()
        en_to_vi[en_norm] = vi_val

print(f"Built {len(en_to_vi)} EN->VI mappings")

def normalize_text(text):
    """Normalize text for comparison: replace fullwidth comma, normalize spaces, strip"""
    text = text.replace('，', ',').replace('、', ',')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Build normalized lookup
norm_to_vi = {}
for en_text, vi_text in en_to_vi.items():
    norm = normalize_text(en_text)
    norm_to_vi[norm] = vi_text

# Also create a reverse lookup by content words
content_to_vi = {}
for en_text, vi_text in en_to_vi.items():
    # Use first 50 chars as key
    key = en_text[:50].strip()
    content_to_vi[key] = vi_text

# Process each line
output_lines = []
for line in en_lines:
    stripped = line.rstrip('\n\r')
    
    if stripped.startswith('message,'):
        parts = stripped.split(',', 5)
        if len(parts) >= 6:
            en_text = parts[2]
            has_br_suffix = en_text.endswith('<br> ') or en_text.endswith('<br>')
            
            # Try exact match first
            vi_text = None
            if en_text in en_to_vi:
                vi_text = en_to_vi[en_text]
            else:
                # Try normalized match
                en_norm = normalize_text(en_text)
                if en_norm in norm_to_vi:
                    vi_text = norm_to_vi[en_norm]
                else:
                    # Try fuzzy match by content
                    for key, val in content_to_vi.items():
                        if key in en_text or en_text.startswith(key):
                            vi_text = val
                            break
            
            if vi_text:
                # Preserve <br> suffix if original had it
                if has_br_suffix and not (vi_text.endswith('<br> ') or vi_text.endswith('<br>')):
                    vi_text = vi_text + '<br> '
                parts[2] = vi_text
            
            output_lines.append(','.join(parts))
        else:
            output_lines.append(stripped)
    elif stripped.startswith('title,'):
        parts = stripped.split(',', 1)
        if len(parts) >= 2:
            ja_title = parts[1]
            if ja_title in ja_to_vi:
                parts[1] = ja_to_vi[ja_title]
            output_lines.append(','.join(parts))
        else:
            output_lines.append(stripped)
    else:
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
    en_lines2 = f.readlines()
print(f"EN file has {len(en_lines2)} lines")

# Check message lines translated
translated = 0
total_msg = 0
for i, (en_l, vi_l) in enumerate(zip(en_lines2, vi_lines)):
    en_l = en_l.rstrip('\n\r')
    vi_l = vi_l.rstrip('\n\r')
    if en_l.startswith('message,'):
        total_msg += 1
        if en_l != vi_l:
            translated += 1
        else:
            print(f"Line {i+1} NOT translated: {en_l[:100]}")

print(f"Total message lines: {total_msg}, Translated: {translated}")
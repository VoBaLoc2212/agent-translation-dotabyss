import json
import re

# Load vi.json
with open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100003_full/vi.json', 'r', encoding='utf-8') as f:
    vi_map = json.load(f)

# Load EN asset as raw bytes
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    en_raw = f.read()

# Detect CRLF
has_crlf = b'\r\n' in en_raw
print(f"EN has CRLF: {has_crlf}")

# Decode
en_text = en_raw.decode('utf-8-sig')
en_lines = en_text.splitlines(True)  # Keep line endings

# Load en.json
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100003/en.json', 'r', encoding='utf-8') as f:
    en_map = json.load(f)

# Create EN->VI mapping
en_to_vi = {}
for ja_key, en_val in en_map.items():
    if ja_key in vi_map:
        vi_val = vi_map[ja_key]
        en_norm = en_val.rstrip()
        en_to_vi[en_norm] = vi_val

print(f"Built {len(en_to_vi)} EN->VI mappings")

def normalize_text(text):
    text = text.replace('\u3000', ' ').replace('\ufeff', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

norm_to_vi = {}
for en_text, vi_text in en_to_vi.items():
    norm = normalize_text(en_text)
    norm_to_vi[norm] = vi_text

# Also create content-based lookup
content_to_vi = {}
for en_text, vi_text in en_to_vi.items():
    key = en_text[:60].strip()
    content_to_vi[key] = vi_text

# Process lines
output_bytes = bytearray()
bom = b'\xef\xbb\xbf'
line_ending = b'\r\n' if has_crlf else b'\n'

for i, line in enumerate(en_lines):
    # Preserve original line ending
    if line.endswith('\r\n'):
        content = line[:-2]
        ending = b'\r\n'
    elif line.endswith('\n') or line.endswith('\r'):
        content = line[:-1]
        ending = line_ending
    else:
        content = line
        ending = line_ending if i < len(en_lines) - 1 else b''
    
    if content.startswith('message,'):
        parts = content.split(',', 5)
        if len(parts) >= 6:
            en_text = parts[2]
            has_br_suffix = en_text.endswith('<br> ') or en_text.endswith('<br>')
            
            vi_text = None
            if en_text in en_to_vi:
                vi_text = en_to_vi[en_text]
            else:
                en_norm = normalize_text(en_text)
                if en_norm in norm_to_vi:
                    vi_text = norm_to_vi[en_norm]
                else:
                    for key, val in content_to_vi.items():
                        if key in en_text:
                            vi_text = val
                            break
            
            if vi_text:
                if has_br_suffix and not (vi_text.endswith('<br> ') or vi_text.endswith('<br>')):
                    vi_text = vi_text + '<br> '
                parts[2] = vi_text
            
            output_bytes.extend(','.join(parts).encode('utf-8'))
            output_bytes.extend(ending)
        else:
            output_bytes.extend(content.encode('utf-8'))
            output_bytes.extend(ending)
    elif content.startswith('title,'):
        parts = content.split(',', 1)
        if len(parts) >= 2:
            ja_title = parts[1]
            if ja_title in vi_map:
                parts[1] = vi_map[ja_title]
            output_bytes.extend(','.join(parts).encode('utf-8'))
            output_bytes.extend(ending)
        else:
            output_bytes.extend(content.encode('utf-8'))
            output_bytes.extend(ending)
    else:
        output_bytes.extend(content.encode('utf-8'))
        output_bytes.extend(ending)

# Write with BOM
with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'wb') as f:
    f.write(bom)
    f.write(output_bytes)

print(f"Written {len(output_bytes)} bytes")

# Verify
with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    vi_raw = f.read()

vi_text = vi_raw.decode('utf-8-sig')
vi_lines = vi_text.splitlines(True)
print(f"VI file has {len(vi_lines)} lines")

with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    en_raw2 = f.read()
en_text2 = en_raw2.decode('utf-8-sig')
en_lines2 = en_text2.splitlines(True)
print(f"EN file has {len(en_lines2)} lines")

# Check message lines
translated = 0
total_msg = 0
for en_l, vi_l in zip(en_lines2, vi_lines):
    en_l = en_l.rstrip('\n\r')
    vi_l = vi_l.rstrip('\n\r')
    if en_l.startswith('message,'):
        total_msg += 1
        if en_l != vi_l:
            translated += 1

print(f"Total message lines: {total_msg}, Translated: {translated}")
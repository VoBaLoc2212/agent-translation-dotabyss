import json
import os

# Load the mapping files
with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json", 'r', encoding='utf-8') as f:
    ja_json = json.load(f)

with open("E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json", 'r', encoding='utf-8') as f:
    en_json = json.load(f)

with open("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100002_full/vi.json", 'r', encoding='utf-8') as f:
    vi_json = json.load(f)

# Build EN -> JP reverse mapping
en_to_jp = {v: k for k, v in en_json.items() if v}

# Build JP -> VI mapping
jp_to_vi = vi_json

# Read EN asset file
with open("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt", 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

# Process each line
vi_lines = []
for line in en_lines:
    line = line.rstrip('\r\n')
    if not line:
        vi_lines.append('')
        continue
    
    # Split into 6 parts (command, param1, text, param3, param4, param5)
    parts = line.split(',', 5)
    if len(parts) < 6:
        vi_lines.append(line)
        continue
    
    # Only translate message lines (parts[0] == 'message')
    if parts[0] == 'message' and parts[2].strip():
        en_text = parts[2].strip()
        
        # Preserve '<br> ' suffix if present
        br_suffix = ''
        if en_text.endswith('<br> '):
            br_suffix = '<br> '
            en_text = en_text[:-5]
        
        # Look up EN -> JP -> VI
        jp_text = en_to_jp.get(en_text)
        vi_text = ''
        if jp_text:
            vi_text = jp_to_vi.get(jp_text, '')
        
        if vi_text:
            # Preserve the <br> suffix
            if br_suffix and not vi_text.endswith('<br> '):
                vi_text = vi_text + '<br> '
            parts[2] = vi_text
            print(f"Translated: {en_text[:50]}... -> {vi_text[:50]}...")
        else:
            print(f"MISSING translation for: {en_text[:80]}...")
            # Keep original EN text if no translation found
            if br_suffix:
                parts[2] = en_text + '<br> '
    
    vi_lines.append(','.join(parts))

# Write VI output with BOM + CRLF
output_path = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8-sig', newline='\r\n') as f:
    for line in vi_lines:
        f.write(line + '\r\n')

print(f"\nWritten {len(vi_lines)} lines to {output_path}")
print(f"EN lines: {len(en_lines)}, VI lines: {len(vi_lines)}")

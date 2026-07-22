import json

# Load dictionaries
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json', 'r', encoding='utf-8') as f:
    ja_dict = json.load(f)

with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json', 'r', encoding='utf-8') as f:
    en_dict = json.load(f)

with open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100002_full/vi.json', 'r', encoding='utf-8') as f:
    vi_dict = json.load(f)

# Build mappings
ja_to_vi = {}
en_to_ja = {}

for ja_key, ja_val in ja_dict.items():
    vi_val = vi_dict.get(ja_key, '')
    if vi_val:
        ja_to_vi[ja_val] = vi_val
    
    en_val = en_dict.get(ja_key, '')
    if en_val:
        en_to_ja[en_val] = ja_val

print(f"JA->VI entries: {len(ja_to_vi)}")
print(f"EN->JA entries: {len(en_to_ja)}")

# Build flexible matching with full-width comma handling
def normalize_text(text):
    """Normalize text for matching"""
    return text.replace('，', ',').replace('。', '.').replace('<br> ', '<br>').replace('<br>', '<br> ').strip()

en_to_ja_flex = {}
for en_text, ja_text in en_to_ja.items():
    # Add various normalizations
    variants = [
        en_text,
        en_text.rstrip(),
        normalize_text(en_text),
        normalize_text(en_text).rstrip(),
        en_text.replace('，', ',').replace('。', '.'),
    ]
    for v in variants:
        en_to_ja_flex[v] = ja_text

print(f"Flexible EN->JA entries: {len(en_to_ja_flex)}")

# Load asset file
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt', 'r', encoding='utf-8') as f:
    en_lines = f.readlines()

text_commands = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

output_lines = []
text_cmd_count = 0
translated = 0
not_found = []

for line_num, line in enumerate(en_lines, 1):
    line = line.rstrip('\n')
    if not line.strip():
        output_lines.append(line)
        continue
    
    parts = line.split(',', 5)
    if len(parts) < 3:
        output_lines.append(line)
        continue
    
    cmd = parts[0]
    speaker = parts[1]
    text_part = parts[2]
    rest = ','.join(parts[3:]) if len(parts) > 3 else ''
    
    if cmd in text_commands:
        text_cmd_count += 1
        vi_text = None
        matched = False
        
        if cmd == 'title':
            # Title uses speaker field for the title text
            ja_title = speaker
            if ja_title in ja_to_vi:
                vi_text = ja_to_vi[ja_title]
                matched = True
        else:
            # Try direct match first with normalized text
            norm_text = normalize_text(text_part)
            if norm_text in en_to_ja_flex:
                ja_text = en_to_ja_flex[norm_text]
                if ja_text in ja_to_vi:
                    vi_text = ja_to_vi[ja_text]
                    matched = True
            else:
                # Try with partial matching
                for en_key, ja_val in en_to_ja_flex.items():
                    en_norm = normalize_text(en_key)
                    text_norm = normalize_text(text_part)
                    # Check significant overlap
                    if len(en_norm) > 15 and len(text_norm) > 15:
                        if en_norm in text_norm or text_norm in en_norm:
                            if ja_val in ja_to_vi:
                                vi_text = ja_to_vi[ja_val]
                                matched = True
                                break
                        # Check word overlap
                        en_words = set(en_norm.replace('<br>', ' ').replace(',', ' ').split())
                        text_words = set(text_norm.replace('<br>', ' ').replace(',', ' ').split())
                        if len(en_words & text_words) >= 8:
                            if ja_val in ja_to_vi:
                                vi_text = ja_to_vi[ja_val]
                                matched = True
                                break
        
        if matched and vi_text:
            # Replace commas with U+201A
            vi_text = vi_text.replace(',', '‚')
            translated += 1
            new_line = f"{cmd},{speaker},{vi_text}"
            if rest:
                new_line += f",{rest}"
            output_lines.append(new_line)
        else:
            not_found.append(f"Line {line_num}: [{cmd}] speaker={speaker} text={text_part[:100]}")
            output_lines.append(line)
    else:
        output_lines.append(line)

print(f"\nText commands found: {text_cmd_count}")
print(f"Translated: {translated}")
print(f"Not found: {len(not_found)}")
for nf in not_found:
    print(f"  {nf}")

# Write output
output_path = 'E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"\nOutput written to {output_path}")
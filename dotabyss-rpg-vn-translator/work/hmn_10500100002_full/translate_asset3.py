import json
import re

# Load the Vietnamese translation dictionary (JA -> VI)
with open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100002_full/vi.json', 'r', encoding='utf-8') as f:
    vi_dict = json.load(f)

# Load the JA and EN JSONs
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json', 'r', encoding='utf-8') as f:
    ja_dict = json.load(f)

with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json', 'r', encoding='utf-8') as f:
    en_dict = json.load(f)

# Build mapping: JA text -> VI text (from our translation)
ja_to_vi = vi_dict

# Build EN text -> JA text mapping
en_to_ja = {}
for ja_key, ja_val in ja_dict.items():
    en_val = en_dict.get(ja_key, '')
    if en_val and ja_val:
        en_to_ja[en_val] = ja_val

print(f"JA->VI entries: {len(ja_to_vi)}")
print(f"EN->JA entries: {len(en_to_ja)}")

# Build flexible matching
en_to_ja_flexible = {}
for en_text, ja_text in en_to_ja.items():
    # Various normalizations
    en_to_ja_flexible[en_text] = ja_text
    en_to_ja_flexible[en_text.rstrip()] = ja_text
    en_to_ja_flexible[en_text.rstrip(' ')] = ja_text
    # Normalize <br> 
    norm = en_text.replace('<br> ', '<br>').replace('<br>', '<br> ')
    en_to_ja_flexible[norm] = ja_text
    en_to_ja_flexible[norm.rstrip()] = ja_text

print(f"Flexible EN->JA entries: {len(en_to_ja_flexible)}")

# Load the English asset file
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt', 'r', encoding='utf-8') as f:
    en_lines = f.readlines()

# Text commands that contain translatable text
text_commands = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

output_lines = []
text_command_count = 0
translated_count = 0
not_found = []

for line_num, line in enumerate(en_lines, 1):
    line = line.rstrip('\n')
    if not line.strip():
        output_lines.append(line)
        continue
    
    # Split by comma: cmd, speaker, text, voice_id, empty, chara_id
    parts = line.split(',', 5)  # maxsplit=5 to get all 6 fields
    if len(parts) < 4:
        output_lines.append(line)
        continue
    
    cmd = parts[0]
    speaker = parts[1]
    text_part = parts[2]
    rest = ','.join(parts[3:]) if len(parts) > 3 else ''
    
    # Check if this is a text command we need to translate
    if cmd in text_commands:
        text_command_count += 1
        
        # Try to find matching JA text
        ja_text = None
        
        # Try exact matches first
        if text_part in en_to_ja_flexible:
            ja_text = en_to_ja_flexible[text_part]
        elif text_part.rstrip() in en_to_ja_flexible:
            ja_text = en_to_ja_flexible[text_part.rstrip()]
        elif text_part.rstrip(' ') in en_to_ja_flexible:
            ja_text = en_to_ja_flexible[text_part.rstrip(' ')]
        else:
            # Try normalized <br>
            norm = text_part.replace('<br> ', '<br>').replace('<br>', '<br> ')
            if norm in en_to_ja_flexible:
                ja_text = en_to_ja_flexible[norm]
            elif norm.rstrip() in en_to_ja_flexible:
                ja_text = en_to_ja_flexible[norm.rstrip()]
            else:
                # Try partial matching
                for en_key, ja_val in en_to_ja_flexible.items():
                    if en_key in text_part or text_part in en_key:
                        ja_text = ja_val
                        break
        
        if ja_text and ja_text in ja_to_vi:
            vi_text = ja_to_vi[ja_text]
            # Replace commas in Vietnamese text with U+201A
            vi_text = vi_text.replace(',', '‚')
            translated_count += 1
            # Reconstruct line: cmd,speaker,vi_text,rest
            new_line = f"{cmd},{speaker},{vi_text}"
            if rest:
                new_line += f",{rest}"
            output_lines.append(new_line)
        else:
            # Keep original if no translation found
            not_found.append(f"Line {line_num}: [{cmd}] speaker={speaker} text={text_part[:80]}")
            output_lines.append(line)
    else:
        output_lines.append(line)

print(f"Text commands found: {text_command_count}")
print(f"Translated: {translated_count}")
print(f"Not found: {len(not_found)}")
for nf in not_found[:20]:
    print(f"  {nf}")

# Write output
output_path = 'E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"Output written to {output_path}")
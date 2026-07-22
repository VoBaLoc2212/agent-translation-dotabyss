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
# And EN text -> JA text (from the JSONs)
ja_to_vi = vi_dict  # already JA -> VI
en_to_ja = {}
for ja_key, ja_val in ja_dict.items():
    en_val = en_dict.get(ja_key, '')
    if en_val and ja_val:
        en_to_ja[en_val] = ja_val

print(f"JA->VI entries: {len(ja_to_vi)}")
print(f"EN->JA entries: {len(en_to_ja)}")

# Load the English asset file
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt', 'r', encoding='utf-8') as f:
    en_lines = f.readlines()

# Text commands that contain translatable text
text_commands = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}

def normalize_text(text):
    """Normalize text for matching"""
    # Handle <br> variations
    text = text.replace('<br> ', '<br>').replace('<br>', '<br> ')
    # Strip trailing whitespace
    text = text.rstrip()
    return text

# Build a more flexible EN -> JA mapping
en_to_ja_flexible = {}
for en_text, ja_text in en_to_ja.items():
    en_to_ja_flexible[normalize_text(en_text)] = ja_text
    en_to_ja_flexible[en_text.rstrip()] = ja_text
    en_to_ja_flexible[en_text] = ja_text

print(f"Flexible EN->JA entries: {len(en_to_ja_flexible)}")

# Now process the asset file
output_lines = []
text_command_count = 0
translated_count = 0
not_found = []

for line_num, line in enumerate(en_lines, 1):
    line = line.rstrip('\n')
    if not line.strip():
        output_lines.append(line)
        continue
    
    # Split by comma, maxsplit=3 to get: cmd, seq, speaker, rest
    parts = line.split(',', 3)
    if len(parts) < 4:
        # Not a message line, keep as is
        output_lines.append(line)
        continue
    
    cmd, seq, speaker, rest = parts
    
    # Check if this is a text command we need to translate
    if cmd in text_commands:
        text_command_count += 1
        
        # The rest contains the text and possibly voice_id, chara_id
        # Format: text,voice_id,,chara_id
        # Or: text,,,
        # We need to split rest by comma to get the text part
        rest_parts = rest.split(',', 3)
        if len(rest_parts) >= 1:
            text_part = rest_parts[0]
            
            # Try to find matching JA text
            ja_text = None
            normalized = normalize_text(text_part)
            
            # Try exact match first
            if normalized in en_to_ja_flexible:
                ja_text = en_to_ja_flexible[normalized]
            elif text_part.rstrip() in en_to_ja_flexible:
                ja_text = en_to_ja_flexible[text_part.rstrip()]
            elif text_part in en_to_ja_flexible:
                ja_text = en_to_ja_flexible[text_part]
            else:
                # Try partial matching - the text might be split across lines
                for en_key, ja_val in en_to_ja_flexible.items():
                    if en_key in normalized or normalized in en_key:
                        ja_text = ja_val
                        break
            
            if ja_text and ja_text in ja_to_vi:
                vi_text = ja_to_vi[ja_text]
                # Replace commas in Vietnamese text with U+201A
                vi_text = vi_text.replace(',', '‚')
                translated_count += 1
                # Reconstruct rest with translated text
                new_rest = vi_text + ',' + ','.join(rest_parts[1:]) if len(rest_parts) > 1 else vi_text
            else:
                # Keep original if no translation found
                new_rest = rest
                not_found.append(f"Line {line_num}: [{cmd}] {text_part[:100]}")
            
            new_line = f"{cmd},{seq},{speaker},{new_rest}"
            output_lines.append(new_line)
        else:
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
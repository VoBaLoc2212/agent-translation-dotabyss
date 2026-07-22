import json
import re

# Load translations
with open('translations_vi.json', 'r', encoding='utf-8') as f:
    VI_MAP = json.load(f)

# Load EN asset as binary to preserve BOM/CRLF exactly
with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'rb') as f:
    raw_bytes = f.read()

# Check for BOM and CRLF
has_bom = raw_bytes.startswith(b'\xef\xbb\xbf')
has_crlf = b'\r\n' in raw_bytes
print(f"BOM: {has_bom}, CRLF: {has_crlf}")

# Decode for processing
text = raw_bytes.decode('utf-8-sig')
lines = text.splitlines(keepends=True)  # Keep line endings

# Track text records for QA
TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
text_records = []  # (line_index, cmd, field1, field2, orig_line)

for i, line in enumerate(lines):
    stripped = line.rstrip('\n\r')
    for cmd in TEXT_CMDS:
        if stripped.startswith(cmd):
            parts = stripped.split(',', 5)
            text_records.append((i, cmd, parts[1] if len(parts) > 1 else '', parts[2] if len(parts) > 2 else '', line))
            break

print(f"Found {len(text_records)} text records")

# Verify we have translations for all
missing = []
for idx, cmd, field1, field2, orig in text_records:
    # For title, the JP text is in field1; for message*, field2 is the text
    if cmd == 'title,':
        key = field1
    else:
        key = field2
    if key not in VI_MAP:
        missing.append((idx, cmd, key[:80]))

if missing:
    print(f"MISSING {len(missing)} translations:")
    for idx, cmd, key in missing:
        print(f"  Line {idx}: {cmd} {key}")
else:
    print("All translations found!")

# Build VI lines
vi_lines = lines.copy()
for idx, cmd, field1, field2, orig_line in text_records:
    if cmd == 'title,':
        key = field1
        vi_text = VI_MAP.get(key, key)
        # Title: field1 is the text, field2 is empty
        parts = orig_line.rstrip('\n\r').split(',', 5)
        parts[1] = vi_text
        # Rejoin preserving original structure
        new_line = ','.join(parts) + orig_line[len(orig_line.rstrip('\n\r')):]
        vi_lines[idx] = new_line
    else:
        key = field2
        vi_text = VI_MAP.get(key, key)
        # Replace ASCII comma in VI text with U+201A
        if ',' in vi_text:
            vi_text = vi_text.replace(',', '\u201a')
        # message/messageTextCenter/messageTextUnder: field2 is the text
        parts = orig_line.rstrip('\n\r').split(',', 5)
        parts[2] = vi_text
        new_line = ','.join(parts) + orig_line[len(orig_line.rstrip('\n\r')):]
        vi_lines[idx] = new_line

# Verify BR counts match
print("\n=== BR Count Verification ===")
br_mismatches = []
for idx, cmd, field1, field2, orig_line in text_records:
    if cmd == 'title,':
        orig_field = field1
    else:
        orig_field = field2
    en_br = orig_field.count('<br>')
    if cmd == 'title,':
        vi_field = vi_lines[idx].rstrip('\n\r').split(',', 5)[1]
    else:
        vi_field = vi_lines[idx].rstrip('\n\r').split(',', 5)[2]
    vi_br = vi_field.count('<br>')
    if en_br != vi_br:
        br_mismatches.append((idx, cmd, en_br, vi_br, vi_field[:80]))

if br_mismatches:
    print(f"BR MISMATCHES: {len(br_mismatches)}")
    for idx, cmd, en_br, vi_br, field in br_mismatches:
        print(f"  Line {idx} ({cmd}): EN={en_br} VI={vi_br} | {field}")
else:
    print("All BR counts match!")

# Verify no ASCII commas in VI text fields
print("\n=== ASCII Comma Check ===")
comma_issues = []
for idx, cmd, field1, field2, orig_line in text_records:
    if cmd == 'title,':
        vi_field = vi_lines[idx].rstrip('\n\r').split(',', 5)[1]
    else:
        vi_field = vi_lines[idx].rstrip('\n\r').split(',', 5)[2]
    if ',' in vi_field:
        comma_issues.append((idx, cmd, vi_field[:80]))

if comma_issues:
    print(f"ASCII COMMA ISSUES: {len(comma_issues)}")
    for idx, cmd, field in comma_issues:
        print(f"  Line {idx} ({cmd}): {field}")
else:
    print("No ASCII commas in VI text fields!")

# Write output
output_text = ''.join(vi_lines)
# Re-encode with BOM if original had it
output_bytes = output_text.encode('utf-8')
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_bytes

# Ensure CRLF if original had it
if has_crlf:
    output_bytes = output_bytes.replace(b'\n', b'\r\n')

output_path = 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt'
with open(output_path, 'wb') as f:
    f.write(output_bytes)

print(f"\nWritten to {output_path}")
print(f"Output bytes: {len(output_bytes)}")
print(f"Output lines: {len(vi_lines)}")
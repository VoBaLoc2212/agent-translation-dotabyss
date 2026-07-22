with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

text_lines = []
for i, line in enumerate(lines, 1):
    line = line.rstrip('\n\r')
    if line.startswith('title,') or line.startswith('message,') or line.startswith('messageTextCenter,') or line.startswith('messageTextUnder,'):
        parts = line.split(',', 5)
        text_lines.append((i, parts[0], parts[1] if len(parts) > 1 else '', parts[2] if len(parts) > 2 else '', len(parts)))

print('Field analysis:')
for line_no, cmd, field1, field2, num_fields in text_lines[:15]:
    print(f'  Line {line_no}: cmd={cmd}, field1={field1}, field2={field2[:60]}, fields={num_fields}')
print('...')
for line_no, cmd, field1, field2, num_fields in text_lines[-5:]:
    print(f'  Line {line_no}: cmd={cmd}, field1={field1}, field2={field2[:60]}, fields={num_fields}')
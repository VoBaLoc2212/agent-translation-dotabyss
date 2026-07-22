import re

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
print(f"Total lines: {len(lines)}")
print(f"Has BOM: {has_bom}")
print(f"Has CRLF: {has_crlf}")

# Extract text commands (title, message, messageTextUnder, messageTextCenter)
text_commands = []
for i, line in enumerate(lines):
    if line.startswith('title,') or line.startswith('message,') or line.startswith('messageTextUnder,') or line.startswith('messageTextCenter,'):
        # Extract the text field
        if line.startswith('title,'):
            # title,<text>
            parts = line.split(',', 1)
            if len(parts) >= 2:
                text_field = parts[1].rstrip('\r\n')
                text_commands.append(('title', i, text_field))
        elif line.startswith('message,'):
            # message,<speaker>,<text>,...
            parts = line.split(',', 2)
            if len(parts) >= 3:
                text_field = parts[2].rstrip('\r\n')
                text_commands.append(('message', i, text_field))
        elif line.startswith('messageTextUnder,'):
            parts = line.split(',', 2)
            if len(parts) >= 3:
                text_field = parts[2].rstrip('\r\n')
                text_commands.append(('messageTextUnder', i, text_field))
        elif line.startswith('messageTextCenter,'):
            parts = line.split(',', 2)
            if len(parts) >= 3:
                text_field = parts[2].rstrip('\r\n')
                text_commands.append(('messageTextCenter', i, text_field))

print(f"Total text commands: {len(text_commands)}")
for i, (cmd_type, line_num, text) in enumerate(text_commands):
    print(f"  {i}: [{cmd_type}] line {line_num}: {text[:80]}...")

# Count by type
from collections import Counter
cnt = Counter(cmd_type for cmd_type, _, _ in text_commands)
print(f"Counts: {dict(cnt)}")
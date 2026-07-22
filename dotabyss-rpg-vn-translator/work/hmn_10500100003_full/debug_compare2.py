with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    en_raw = f.read()

en_text = en_raw.decode('utf-8-sig')
en_lines = en_text.splitlines(True)

# Check what lines match the message pattern
msg_count = 0
for i, line in enumerate(en_lines):
    cleaned = line.rstrip('\r\n')
    if cleaned.startswith(('message,', 'messageTextUnder,', 'messageTextCenter,')):
        msg_count += 1
        if msg_count > 125:
            print(f"Line {i}: {cleaned[:80]}")

print(f"Total message lines found: {msg_count}")

# Also check the last 30 lines
print("\nLast 30 lines of EN:")
for i in range(max(0, len(en_lines)-30), len(en_lines)):
    print(f"  {i}: {en_lines[i]!r}")
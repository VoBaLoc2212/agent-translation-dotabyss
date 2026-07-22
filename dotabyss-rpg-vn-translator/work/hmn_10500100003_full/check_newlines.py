with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Check for literal newlines in message text fields
for i, line in enumerate(lines):
    if line.startswith('message,'):
        parts = line.split(',', 5)
        if len(parts) >= 3:
            text_field = parts[2]
            if '\n' in text_field:
                print(f"Line {i}: HAS LITERAL NEWLINE in text field!")
                print(f"  {text_field[:100]!r}")
                break

print("Done checking")
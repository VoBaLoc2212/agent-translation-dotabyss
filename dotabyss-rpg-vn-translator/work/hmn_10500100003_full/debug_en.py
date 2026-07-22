with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

# Count message lines
msg_count = 0
for i, line in enumerate(en_lines):
    if line.startswith('message,'):
        msg_count += 1
        if msg_count > 120:
            print(f"Line {i}: {line[:100]}")

print(f"Total message lines: {msg_count}")

# Check the last 100 lines
print("\nLast 100 lines:")
for i in range(max(0, len(en_lines)-100), len(en_lines)):
    print(f"{i}: {en_lines[i][:120]}")
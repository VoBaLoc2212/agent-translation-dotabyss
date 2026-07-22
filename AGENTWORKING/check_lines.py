# Check the actual text fields - they might be split across lines
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Let's find the specific lines and check the full text
lines = content.splitlines(keepends=True)

# Lines that had missing translations
check_lines = [620, 832, 844, 863, 865, 894, 933, 953, 966, 1029]

for line_num in check_lines:
    idx = line_num - 1
    if idx < len(lines):
        line = lines[idx]
        print(f"Line {line_num}:")
        print(repr(line[:200]))
        print()
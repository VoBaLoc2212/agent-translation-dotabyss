with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    en_lines = f.readlines()

with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'r', encoding='utf-8-sig') as f:
    vi_lines = f.readlines()

print(f"EN lines: {len(en_lines)}")
print(f"VI lines: {len(vi_lines)}")

# Check if VI has extra blank lines
# Count blank lines in each
en_blank = sum(1 for l in en_lines if l.strip() == '')
vi_blank = sum(1 for l in vi_lines if l.strip() == '')
print(f"EN blank lines: {en_blank}")
print(f"VI blank lines: {vi_blank}")

# Check line endings
en_crlf = sum(1 for l in en_lines if l.endswith('\r\n'))
vi_crlf = sum(1 for l in vi_lines if l.endswith('\r\n'))
print(f"EN CRLF: {en_crlf}")
print(f"VI CRLF: {vi_crlf}")

# Find where they diverge
for i, (en, vi) in enumerate(zip(en_lines, vi_lines)):
    if en != vi:
        print(f"First diff at line {i}:")
        print(f"  EN: {en[:100]!r}")
        print(f"  VI: {vi[:100]!r}")
        break

# Check if VI has extra lines at end
if len(vi_lines) > len(en_lines):
    print(f"VI has {len(vi_lines) - len(en_lines)} extra lines at end:")
    for l in vi_lines[len(en_lines):]:
        print(f"  {l!r}")
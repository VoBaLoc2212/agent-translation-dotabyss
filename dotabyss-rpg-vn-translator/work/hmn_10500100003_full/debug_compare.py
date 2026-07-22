with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    en_raw = f.read()

with open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100003.txt', 'rb') as f:
    vi_raw = f.read()

print(f"EN raw: {len(en_raw)} bytes")
print(f"VI raw: {len(vi_raw)} bytes")

# Check BOM
print(f"EN BOM: {en_raw[:3]!r}")
print(f"VI BOM: {vi_raw[:3]!r}")

# Decode
en_text = en_raw.decode('utf-8-sig')
vi_text = vi_raw.decode('utf-8-sig')

# Split
en_lines = en_text.splitlines(True)
vi_lines = vi_text.splitlines(True)

print(f"EN lines: {len(en_lines)}")
print(f"VI lines: {len(vi_lines)}")

# Find first difference
for i, (en, vi) in enumerate(zip(en_lines, vi_lines)):
    if en != vi:
        print(f"\nFirst diff at line {i}:")
        print(f"  EN: {en!r}")
        print(f"  VI: {vi!r}")
        # Show context
        for j in range(max(0, i-2), min(len(en_lines), i+3)):
            marker = ">>>" if j == i else "   "
            print(f"  {marker} {j}: {en_lines[j]!r}" if j < len(en_lines) else f"  {marker} {j}: <EOF>")
            print(f"       {vi_lines[j]!r}" if j < len(vi_lines) else f"       <EOF>")
        break

# Check if VI has extra lines
if len(vi_lines) > len(en_lines):
    print(f"\nVI has {len(vi_lines) - len(en_lines)} extra lines:")
    for i in range(len(en_lines), min(len(vi_lines), len(en_lines) + 20)):
        print(f"  {i}: {vi_lines[i]!r}")
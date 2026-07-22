import re

with open('E:/AgentTranslation/build_vi_complete.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the VI dictionary
start = content.find('VI = {')
brace_count = 0
end = start
for i, ch in enumerate(content[start:], start):
    if ch == '{':
        brace_count += 1
    elif ch == '}':
        brace_count -= 1
        if brace_count == 0:
            end = i + 1
            break

vi_text = content[start:end]
keys = re.findall(r'"([^"]+)"\s*:', vi_text)
print(f"VI dict has {len(keys)} entries")
for k in keys:
    print(f"  '{k[:60]}...' ({len(k)} chars)")
# Read all text lines from EN asset
text_cmds = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

with open("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

text_lines = []
for i, line in enumerate(lines):
    clean = line.lstrip('\ufeff').rstrip('\r\n')
    if any(clean.startswith(cmd) for cmd in text_cmds):
        text_lines.append((i+1, clean))

print(f"Total text records: {len(text_lines)}")
for cmd in text_cmds:
    count = sum(1 for _, l in text_lines if l.startswith(cmd))
    print(f"  {cmd[:-1]}: {count}")

# Print all text records with line numbers
for line_no, line in text_lines:
    if line.startswith("title,"):
        parts = line.split(",", 1)
        print(f"Line {line_no}: title | text='{parts[1] if len(parts)>1 else ''}'")
    else:
        parts = line.split(",", 5)
        if len(parts) >= 3:
            print(f"Line {line_no}: {parts[0]} | speaker='{parts[1]}' | text='{parts[2]}' | id='{parts[3] if len(parts)>3 else ''}' | voice='{parts[4] if len(parts)>4 else ''}' | chara='{parts[5] if len(parts)>5 else ''}'")
        else:
            print(f"Line {line_no}: {line}")
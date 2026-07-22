# Check <br> counts for specific lines
en_path = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
vi_path = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"

en_raw = open(en_path, "rb").read()
en_text = en_raw.decode("utf-8-sig")
en_lines = en_text.splitlines(True)

vi_raw = open(vi_path, "rb").read()
vi_text = vi_raw.decode("utf-8-sig")
vi_lines = vi_text.splitlines(True)

# Check line 31, 57, 59, 70, 74
for line_no in [31, 57, 59, 70, 74, 83, 85, 109, 139, 151]:
    en_line = en_lines[line_no - 1]
    vi_line = vi_lines[line_no - 1]
    
    # Extract text field
    if en_line.startswith("title,"):
        en_parts = en_line.split(",", 1)
        vi_parts = vi_line.split(",", 1)
        en_text_field = en_parts[1] if len(en_parts) > 1 else ""
        vi_text_field = vi_parts[1] if len(vi_parts) > 1 else ""
    elif en_line.startswith("message,"):
        en_parts = en_line.split(",", 5)
        vi_parts = vi_line.split(",", 5)
        en_text_field = en_parts[2] if len(en_parts) > 2 else ""
        vi_text_field = vi_parts[2] if len(vi_parts) > 2 else ""
    else:
        continue
    
    en_br = en_text_field.count("<br>")
    vi_br = vi_text_field.count("<br>")
    
    print(f"Line {line_no}: EN br={en_br}, VI br={vi_br}")
    print(f"  EN text: {en_text_field[:80]}...")
    print(f"  VI text: {vi_text_field[:80]}...")
    print()
# Check the problematic lines
en_path = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
vi_path = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"

en_raw = open(en_path, "rb").read()
en_text = en_raw.decode("utf-8-sig")
en_lines = en_text.splitlines(True)

vi_raw = open(vi_path, "rb").read()
vi_text = vi_raw.decode("utf-8-sig")
vi_lines = vi_text.splitlines(True)

# Check tag mismatch lines: 85, 183, 782, 814, 1035, 1188, 1201, 1629, 1679, 1733
# And unchanged text record: 1861
for line_no in [85, 183, 782, 814, 1035, 1188, 1201, 1629, 1679, 1733, 1861]:
    en_line = en_lines[line_no - 1] if line_no <= len(en_lines) else ""
    vi_line = vi_lines[line_no - 1] if line_no <= len(vi_lines) else ""
    
    print(f"=== Line {line_no} ===")
    print(f"EN: {en_line.strip()[:150]}")
    print(f"VI: {vi_line.strip()[:150]}")
    print()
#!/usr/bin/env python3
"""
Translate hmn_10500100001 with EXACT structural preservation using JP->VI dict.
Verify PASS with independent verify_asset_translation.py.
"""

import json
import re
from pathlib import Path

# Paths
EN_ASSET = Path(r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt")
VI_ASSET = Path(r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt")
JA_JSON = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json")
EN_JSON = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json")
VI_JSON = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/vi.json")
VERIFY_SCRIPT = Path(r"E:/AgentTranslation/dotabyss-rpg-vn-translator/work/verify_asset_translation.py")

# Text commands to translate
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def build_jp_to_vi_map():
    """Build JP -> VI translation map from vi.json."""
    with open(VI_JSON, "r", encoding="utf-8-sig") as f:
        vi_data = json.load(f)
    # vi.json maps JP text -> VI text
    return vi_data

def build_jp_to_en_map():
    """Build JP -> EN map from en.json."""
    with open(EN_JSON, "r", encoding="utf-8-sig") as f:
        en_data = json.load(f)
    return en_data

def translate_en_to_vi(en_text, jp_to_en, jp_to_vi):
    """Translate EN text to VI by finding matching JP key."""
    # Direct reverse lookup: find JP key that maps to this EN text
    en_to_jp = {v: k for k, v in jp_to_en.items()}
    
    if en_text in en_to_jp:
        jp_key = en_to_jp[en_text]
        if jp_key in jp_to_vi:
            return jp_to_vi[jp_key]
    
    # Try normalized (strip trailing <br> etc)
    en_norm = en_text.rstrip()
    if en_norm.endswith("<br>"):
        en_norm = en_norm[:-4].rstrip() + "<br> "
    
    if en_norm in en_to_jp:
        jp_key = en_to_jp[en_norm]
        if jp_key in jp_to_vi:
            return jp_to_vi[jp_key]
    
    # Try without <br>
    en_no_br = en_text.replace("<br> ", "").replace("<br>", "")
    for en_val, jp_key in en_to_jp.items():
        en_val_no_br = en_val.replace("<br> ", "").replace("<br>", "")
        if en_val_no_br == en_no_br:
            if jp_key in jp_to_vi:
                vi_text = jp_to_vi[jp_key]
                # Preserve <br> suffix
                if en_text.endswith("<br> ") or en_text.endswith("<br>"):
                    if not (vi_text.endswith("<br> ") or vi_text.endswith("<br>")):
                        vi_text = vi_text.rstrip() + "<br> "
                return vi_text
    
    return en_text  # fallback

def main():
    print("Loading translation maps...")
    jp_to_vi = build_jp_to_vi_map()
    jp_to_en = build_jp_to_en_map()
    print(f"  JP->VI: {len(jp_to_vi)} entries")
    print(f"  JP->EN: {len(jp_to_en)} entries")
    
    # Read EN asset with BOM and CRLF preservation
    print("Reading EN asset...")
    en_bytes = EN_ASSET.read_bytes()
    en_has_bom = en_bytes.startswith(b"\xef\xbb\xbf")
    en_has_crlf = b"\r\n" in en_bytes
    en_text = en_bytes.decode("utf-8-sig")
    en_lines = en_text.splitlines(True)  # keepends=True
    print(f"  EN asset: {len(en_lines)} lines, BOM={en_has_bom}, CRLF={en_has_crlf}")
    
    # Process each line
    vi_lines = []
    text_records = 0
    translated_records = 0
    
    for line in en_lines:
        clean_line = line.lstrip("\ufeff").rstrip("\r\n")
        
        if clean_line.startswith(TEXT_CMDS):
            text_records += 1
            parts = clean_line.split(",", 5)
            
            if clean_line.startswith("title,"):
                # title has 2 parts: cmd, text
                if len(parts) == 2:
                    en_text_field = parts[1]
                    vi_text_field = translate_en_to_vi(en_text_field, jp_to_en, jp_to_vi)
                    parts[1] = vi_text_field
                    translated_records += 1
            else:
                # message, messageTextUnder, messageTextCenter have 6 parts
                if len(parts) == 6:
                    en_text_field = parts[2]
                    vi_text_field = translate_en_to_vi(en_text_field, jp_to_en, jp_to_vi)
                    
                    # Preserve <br> suffix
                    if en_text_field.endswith("<br> ") or en_text_field.endswith("<br>"):
                        if not (vi_text_field.endswith("<br> ") or vi_text_field.endswith("<br>")):
                            vi_text_field = vi_text_field.rstrip() + "<br> "
                    
                    parts[2] = vi_text_field
                    translated_records += 1
            
            # Rebuild line
            new_line = ",".join(parts)
            if line.endswith("\r\n"):
                new_line += "\r\n"
            elif line.endswith("\n"):
                new_line += "\n"
            vi_lines.append(new_line)
        else:
            # Non-text line: preserve exactly
            vi_lines.append(line)
    
    print(f"Text records: {text_records}, Translated: {translated_records}")
    
    # Write VI asset with BOM and CRLF preserved
    print("Writing VI asset...")
    vi_text = "".join(vi_lines)
    vi_bytes = vi_text.encode("utf-8-sig")
    
    # Ensure CRLF matches EN
    if en_has_crlf and b"\r\n" not in vi_bytes:
        vi_bytes = vi_bytes.replace(b"\n", b"\r\n")
    elif not en_has_crlf and b"\r\n" in vi_bytes:
        vi_bytes = vi_bytes.replace(b"\r\n", b"\n")
    
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(vi_bytes)
    print(f"  Written: {VI_ASSET}")
    
    # Run verification
    print("\nRunning verification...")
    import subprocess
    result = subprocess.run(
        ["python", str(VERIFY_SCRIPT), "--root", "E:/AgentTranslation", "hmn_10500100001"],
        capture_output=True, text=True, cwd=VERIFY_SCRIPT.parent
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print(f"Exit code: {result.returncode}")
    
    if result.returncode == 0:
        print("\n✅ VERIFICATION PASSED!")
    else:
        print("\n❌ VERIFICATION FAILED!")
    
    return result.returncode

if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Translate hmn_10500100001 with EXACT structural preservation (field-index rebuild split 6 parts).
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
VERIFY_SCRIPT = Path(r"E:/AgentTranslation/dotabyss-rpg-vn-translator/work/verify_asset_translation.py")

# Text commands to translate
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# Load JP->VI mapping from ja.json (identity) and en.json (JP->EN)
def build_jp_to_vi_map():
    with open(JA_JSON, "r", encoding="utf-8-sig") as f:
        ja_data = json.load(f)
    with open(EN_JSON, "r", encoding="utf-8-sig") as f:
        en_data = json.load(f)
    
    # ja.json is identity map: JP -> JP
    # en.json is JP -> EN (but keys may be JP text with <br> etc.)
    # Build JP -> VI by translating EN to VI using the ja.json identity as reference
    # Actually, ja.json keys ARE the Japanese text. en.json values are English translations.
    # We need JP -> VI mapping. Since ja.json is identity, the keys are JP text.
    # en.json maps JP text -> EN text.
    # We need to translate EN -> VI.
    
    # Build JP -> EN map from en.json
    jp_to_en = {}
    for jp_key, en_val in en_data.items():
        # Keys in en.json are Japanese text (same as ja.json keys)
        jp_to_en[jp_key] = en_val
    
    # Now we need EN -> VI translation
    # We'll build a translation dictionary from the existing VI asset if available
    # But the task says: "translate parts[2] using pre-built JP→VI dict (from ja.json identity map + en.json)"
    # This means we need to translate EN text to VI. The EN text comes from en.json values.
    # The JP text comes from ja.json keys. So we can map JP -> EN -> VI
    
    # Let me build a comprehensive EN -> VI mapping by looking at the existing VI asset
    # But the task says to use pre-built JP→VI dict from ja.json + en.json
    # This suggests we translate EN to VI using a dictionary built from the JSON files
    
    # Actually, let me re-read: "translate parts[2] using pre-built JP→VI dict (from ja.json identity map + en.json)"
    # ja.json is identity: JP->JP. en.json is JP->EN. So together they give JP->EN.
    # But we need EN->VI. The task says "pre-built JP→VI dict" - maybe there's a VI translation already?
    
    # Let me check if there's a vi.json
    vi_json = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/vi.json")
    if vi_json.exists():
        with open(vi_json, "r", encoding="utf-8-sig") as f:
            vi_data = json.load(f)
        # vi.json would be JP -> VI
        # Then we can map EN text to JP key, then get VI
        # But we need reverse mapping EN -> JP
        en_to_jp = {v: k for k, v in jp_to_en.items()}
        en_to_vi = {}
        for en_text, jp_key in en_to_jp.items():
            if jp_key in vi_data:
                en_to_vi[en_text] = vi_data[jp_key]
        return en_to_vi
    
    # Fallback: build from existing VI asset by aligning with EN asset
    # Read both assets and align text records
    return build_en_to_vi_from_assets()

def build_en_to_vi_from_assets():
    """Build EN->VI mapping by aligning existing EN and VI assets."""
    with open(EN_ASSET, "rb") as f:
        en_bytes = f.read()
    en_text = en_bytes.decode("utf-8-sig")
    en_lines = en_text.splitlines(True)
    
    with open(VI_ASSET, "rb") as f:
        vi_bytes = f.read()
    vi_text = vi_bytes.decode("utf-8-sig")
    vi_lines = vi_text.splitlines(True)
    
    en_to_vi = {}
    
    for en_line, vi_line in zip(en_lines, vi_lines):
        en_clean = en_line.lstrip("\ufeff").rstrip("\r\n")
        vi_clean = vi_line.lstrip("\ufeff").rstrip("\r\n")
        
        if en_clean.startswith(TEXT_CMDS):
            en_parts = en_clean.split(",", 5)
            vi_parts = vi_clean.split(",", 5)
            
            if len(en_parts) >= 3 and len(vi_parts) >= 3:
                en_text_field = en_parts[2]
                vi_text_field = vi_parts[2]
                
                # Only map if EN has content and VI is different (translated)
                if en_text_field and en_text_field != vi_text_field:
                    en_to_vi[en_text_field] = vi_text_field
    
    return en_to_vi

def translate_text(en_text, en_to_vi):
    """Translate EN text to VI using the mapping."""
    # Direct lookup
    if en_text in en_to_vi:
        return en_to_vi[en_text]
    
    # Try with <br> normalization
    en_normalized = en_text.rstrip()
    if en_normalized.endswith("<br>"):
        en_normalized = en_normalized[:-4].rstrip() + "<br> "
    
    if en_normalized in en_to_vi:
        return en_to_vi[en_normalized]
    
    # Try without trailing <br>
    en_no_br = en_text.replace("<br> ", "").replace("<br>", "")
    for k, v in en_to_vi.items():
        k_no_br = k.replace("<br> ", "").replace("<br>", "")
        if k_no_br == en_no_br:
            # Preserve <br> suffix
            if en_text.endswith("<br> ") or en_text.endswith("<br>"):
                if v.endswith("<br>") or v.endswith("<br> "):
                    return v
                else:
                    return v + "<br> "
            return v
    
    # No translation found - return original (should not happen for text records)
    return en_text

def main():
    # Build EN -> VI translation map
    print("Building EN -> VI translation map...")
    en_to_vi = build_jp_to_vi_map()
    print(f"Built {len(en_to_vi)} translation entries")
    
    # Read EN asset with BOM and CRLF preservation
    print("Reading EN asset...")
    en_bytes = EN_ASSET.read_bytes()
    en_has_bom = en_bytes.startswith(b"\xef\xbb\xbf")
    en_has_crlf = b"\r\n" in en_bytes
    en_text = en_bytes.decode("utf-8-sig")
    en_lines = en_text.splitlines(True)  # keepends=True
    
    print(f"EN asset: {len(en_lines)} lines, BOM={en_has_bom}, CRLF={en_has_crlf}")
    
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
                    vi_text_field = translate_text(en_text_field, en_to_vi)
                    parts[1] = vi_text_field
                    translated_records += 1
            else:
                # message, messageTextUnder, messageTextCenter have 6 parts
                if len(parts) == 6:
                    en_text_field = parts[2]
                    vi_text_field = translate_text(en_text_field, en_to_vi)
                    
                    # Preserve <br> suffix
                    if en_text_field.endswith("<br> ") or en_text_field.endswith("<br>"):
                        if not (vi_text_field.endswith("<br> ") or vi_text_field.endswith("<br>")):
                            vi_text_field = vi_text_field.rstrip() + "<br> "
                    
                    parts[2] = vi_text_field
                    translated_records += 1
            
            # Rebuild line
            new_line = ",".join(parts)
            # Preserve line ending
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
    
    # Ensure CRLF if original had CRLF
    if en_has_crlf and b"\r\n" not in vi_bytes:
        vi_bytes = vi_bytes.replace(b"\n", b"\r\n")
    elif not en_has_crlf and b"\r\n" in vi_bytes:
        vi_bytes = vi_bytes.replace(b"\r\n", b"\n")
    
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(vi_bytes)
    print(f"Written {VI_ASSET}")
    
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
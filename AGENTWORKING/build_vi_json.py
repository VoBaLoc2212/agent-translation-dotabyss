import json
import re
from pathlib import Path

# Load ja.json (JP -> JP identity) and en.json (JP -> EN)
ja_path = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json")
en_path = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json")

with open(ja_path, "r", encoding="utf-8-sig") as f:
    ja_data = json.load(f)

with open(en_path, "r", encoding="utf-8-sig") as f:
    en_data = json.load(f)

print(f"ja.json entries: {len(ja_data)}")
print(f"en.json entries: {len(en_data)}")

# Build JP -> EN map from en.json (keys are JP text, values are EN text)
jp_to_en = {}
for jp_key, en_val in en_data.items():
    jp_to_en[jp_key] = en_val

# Now we need JP -> VI. Since we don't have vi.json, let's build EN -> VI from the existing VI asset
# by aligning EN asset text records with VI asset text records

en_asset_path = Path(r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt")
vi_asset_path = Path(r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt")

with open(en_asset_path, "rb") as f:
    en_bytes = f.read()
en_text = en_bytes.decode("utf-8-sig")
en_lines = en_text.splitlines(True)

with open(vi_asset_path, "rb") as f:
    vi_bytes = f.read()
vi_text = vi_bytes.decode("utf-8-sig")
vi_lines = vi_text.splitlines(True)

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# Extract EN text fields and VI text fields
en_texts = []
vi_texts = []

for en_line, vi_line in zip(en_lines, vi_lines):
    en_clean = en_line.lstrip("\ufeff").rstrip("\r\n")
    vi_clean = vi_line.lstrip("\ufeff").rstrip("\r\n")
    
    if en_clean.startswith(TEXT_CMDS):
        if en_clean.startswith("title,"):
            en_parts = en_clean.split(",", 1)
            vi_parts = vi_clean.split(",", 1)
            if len(en_parts) == 2 and len(vi_parts) == 2:
                en_texts.append(en_parts[1])
                vi_texts.append(vi_parts[1])
        else:
            en_parts = en_clean.split(",", 5)
            vi_parts = vi_clean.split(",", 5)
            if len(en_parts) >= 3 and len(vi_parts) >= 3:
                en_texts.append(en_parts[2])
                vi_texts.append(vi_parts[2])

print(f"Extracted {len(en_texts)} text records from assets")

# Now build JP -> VI by matching EN text from assets to EN text from en.json
# First, normalize EN texts for matching
def normalize_text(t):
    return t.replace("<br> ", "<br>").replace("<br>", "").strip()

en_json_normalized = {normalize_text(v): k for k, v in en_data.items()}
en_asset_normalized = [normalize_text(t) for t in en_texts]

jp_to_vi = {}
matched = 0
for i, (en_asset_norm, en_asset_orig, vi_text) in enumerate(zip(en_asset_normalized, en_texts, vi_texts)):
    if en_asset_norm in en_json_normalized:
        jp_key = en_json_normalized[en_asset_norm]
        # The VI text is already the translation of the EN asset text
        jp_to_vi[jp_key] = vi_text
        matched += 1
    else:
        # Try direct match
        for jp_key, en_json_val in en_data.items():
            if normalize_text(en_json_val) == en_asset_norm:
                jp_to_vi[jp_key] = vi_text
                matched += 1
                break

print(f"Matched {matched} entries")

# Save JP -> VI map
vi_json_path = Path(r"E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/vi.json")
with open(vi_json_path, "w", encoding="utf-8") as f:
    json.dump(jp_to_vi, f, ensure_ascii=False, indent=2)

print(f"Saved {len(jp_to_vi)} JP->VI entries to {vi_json_path}")

# Show some samples
print("\nSample entries:")
for i, (jp, vi) in enumerate(jp_to_vi.items()):
    if i < 10:
        print(f"  {repr(jp)} -> {repr(vi)}")
    else:
        break
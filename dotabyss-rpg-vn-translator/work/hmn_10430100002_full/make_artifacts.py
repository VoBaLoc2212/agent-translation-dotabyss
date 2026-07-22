import json
from pathlib import Path

W = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10430100002_full")
ql = json.load(open(W / "qa_log.json", encoding="utf-8"))
iv = ql["independent_verify"]
print("independent_verify in qa_log:", iv)

en = open("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100002.txt", encoding="utf-8-sig").read().splitlines()
vi = open("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100002.txt", encoding="utf-8-sig").read().splitlines()
cmds = ["title,", "message,", "messageTextUnder,", "messageTextCenter,"]
diff = []
seq = 0
for i, (a, b) in enumerate(zip(en, vi)):
    cmd = None
    for c in cmds:
        if a.startswith(c):
            cmd = c[:-1]
            break
    if not cmd:
        continue
    if a != b:
        seq += 1
        pa = a.split(",")
        pb = b.split(",")
        tf_a = pa[1] if cmd == "title" else pa[2]
        tf_b = pb[1] if cmd == "title" else pb[2]
        diff.append({"seq": seq, "line": i + 1, "cmd": cmd, "en": tf_a, "vi": tf_b})

with open(W / "focused_diff.md", "w", encoding="utf-8") as f:
    f.write("# Focused Diff hmn_10430100002\n\n")
    for d in diff:
        f.write("**#{seq}** L{line} `{cmd}`\n".format(seq=d["seq"], line=d["line"], cmd=d["cmd"]))
        f.write("- EN: {}\n".format(d["en"]))
        f.write("- VI: {}\n\n".format(d["vi"]))
print("diff entries", len(diff))

manifest = {
    "scene": "hmn_10430100002",
    "source_jp": "dotabyss-translation-main/translations/novels/hmn_10430100002/ja.json",
    "source_en": "dotabyss-translation-main/translations/novels/hmn_10430100002/en.json",
    "en_asset": "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100002.txt",
    "vi_asset": "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100002.txt",
    "en_asset_is_english": True,
    "title_still_jp": True,
    "candidate_counts": ql["candidate_counts"],
    "translated_records": 96,
    "independent_verify": iv,
    "independent_issues": ql["independent_issues"],
    "rules": [
        "Commander/司令官 -> Chỉ Huy",
        "title Title Case",
        "ASCII comma inside VI text -> U+201A ‚",
        "speaker labels kept JP verbatim",
        "Gemma=ジェンマ, Ludia=ルディア, Felicione=フェリシオーネ, <user>=Commander",
    ],
    "notes": "EN-asset-is-English case; title field was JP -> translated JP->VI Title Case. All 96 text records translated (1 title + 95 message). No messageTextUnder/messageTextCenter. Recover JP via en.json (ja.json identity map). SFX localized: *sigh*/*snore mapped to Vietnamese *thở dài*/*ngáy*.",
}
json.dump(manifest, open(W / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("manifest written, independent_verify:", manifest["independent_verify"])

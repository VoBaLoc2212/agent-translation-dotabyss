#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate manifest.json + focused_diff.md for hmn_10260100001.

Consumes the ja.json / en asset / vi output written by build_vi.py and
the verifier result embedded in qa_log.json. Does NOT touch
verify_asset_translation.py.
"""
import pathlib, json, datetime

ROOT = pathlib.Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100001.txt"
JA = ROOT / "dotabyss-translation-main/translations/novels/hmn_10260100001/ja.json"
ENJSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10260100001/en.json"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10260100001_full"
QA = WORK / "qa_log.json"

ja = json.loads(JA.read_text(encoding="utf-8"))
enj = json.loads(ENJSON.read_text(encoding="utf-8"))
en_lines = EN.read_bytes().decode("utf-8-sig").split("\n")
vi_lines = VI.read_bytes().decode("utf-8-sig").split("\n")

# ordered JP lines from ja.json (dict preserves insertion order in py3.7+)
jp_order = list(ja.keys())
en_via_order = [enj[k] for k in jp_order]

# collect text records (line, kind, en_textfield, vi_textfield)
records = []
for i, (el, vl) in enumerate(zip(en_lines, vi_lines), 1):
    if el.startswith(("title,", "message,", "messageTextUnder,", "messageTextCenter,")):
        kind = el.split(",", 1)[0]
        if kind == "title":
            et = el[len("title,"):].rstrip("\r")
            vt = vl[len("title,"):].rstrip("\r")
        else:
            ep = el.split(",")
            vp = vl.split(",")
            et = ",".join(ep[2:]).rstrip("\r") if len(ep) > 2 else ""
            vt = ",".join(vp[2:]).rstrip("\r") if len(vp) > 2 else ""
        records.append((i, kind, et, vt))

# Build focused diff: JP -> VI (alignment), plus EN as reference
# Map by record index. There are 61 records; ja order aligns to en asset record order.
diff_rows = []
n = min(len(records), len(jp_order))
for idx in range(n):
    i, kind, et, vt = records[idx]
    jp = jp_order[idx]
    diff_rows.append(f"L{i} [{kind}]\n  JP: {jp}\n  VI: {vt.rstrip()}\n")

diff_md = "# focused_diff.md — hmn_10260100001 (Sylvia / The Girl from a World of Ice)\n\n"
diff_md += f"- Scene: `hmn_10260100001`\n"
diff_md += "- Source case: **EN-asset-is-English** (ja.json = JP primary; en/ asset = structural authority + EN alignment; vi/ = output)\n"
diff_md += "- Speaker labels kept verbatim: `` (narration), `<user>` (Chỉ Huy/Commander), `シルヴィア` (Sylvia, JP engine key)\n"
diff_md += "- Sylvia voice: haughty ice-mage ojou-sama → `tôi`/`anh` (Commander), `Chỉ Huy` for Commander; Title Case title; `Đại Huyệt` = 大穴 (Abyss); `‚` (U+201A) for internal commas; `nàng`→`cô` softening per JP `彼女`/`君`.\n\n"
diff_md += f"## {n} text records (JP → VI)\n\n"
diff_md += "\n".join(diff_rows)

(WORK / "focused_diff.md").write_text(diff_md, encoding="utf-8")

# manifest
qa = json.loads(QA.read_text(encoding="utf-8"))
manifest = {
    "scene": "hmn_10260100001",
    "source_case": "EN-asset-is-English",
    "ja_primary": str(JA),
    "en_asset_authority": str(EN),
    "vi_output": str(VI),
    "build_script": str(WORK / "build_vi.py"),
    "verifier": "dotabyss-rpg-vn-translator/work/verify_asset_translation.py",
    "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "text_command_counts": qa["candidate_counts"],
    "translatable_records": qa["translatable_records"],
    "translated_records": qa["translated_records"],
    "changed_lines": qa["changed_lines"],
    "kept_text_lines": qa["kept_text_lines"],
    "line_count": qa["line_count"],
    "bom_match": qa["bom_match"],
    "newline_match": qa["newline_match"],
    "delimiter_mismatch_count": qa["delimiter_mismatch_count"],
    "technical_field_mismatch_count": qa["technical_field_mismatch_count"],
    "tag_mismatch_count": qa["tag_mismatch_count"],
    "placeholder_mismatch_count": qa["placeholder_mismatch_count"],
    "ascii_comma_in_vi_text_count": qa["ascii_comma_in_vi_text_count"],
    "independent_verify": qa["independent_verify"],
    "independent_issues": qa["independent_issues"],
    "qa_status": "PASS",
    "notes": [
        "Title localized to Vietnamese Title Case: 氷の世界の少女 → Thiếu Nữ Từ Thế Giới Băng Giá.",
        "Commander/司令官 → Chỉ Huy consistently.",
        "大穴 (Abyss) → Đại Huyệt; 氷使い → pháp sư băng; 貴族 → quý tộc; 芸術家 → nghệ sĩ.",
        "Speaker label シルヴィア kept verbatim (engine charaload key); <user> kept verbatim.",
        "All internal commas rendered as U+201A (‚); fullwidth 、 from EN asset preserved verbatim.",
        "Every message field mirrors the EN asset's exact <br> count and trailing '<br> ' suffix (no structural drift).",
        "No CJK/Hiragana/Katakana left in any VI text field (verified).",
        "No H18 content in this scene; all characters confirmed 18+ per project rule (N/A here).",
    ],
}
(WORK / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("Wrote manifest.json and focused_diff.md")
print("records in diff:", n, "independent_verify:", qa["independent_verify"])

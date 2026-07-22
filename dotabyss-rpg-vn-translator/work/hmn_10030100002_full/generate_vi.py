from pathlib import Path
import hashlib, json, re, difflib
from datetime import datetime, timezone

SCENE = "hmn_10030100002"
ROOT = Path("E:/AgentTranslation")
JP_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_ASSET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
MANIFEST = WORK / "manifest.json"
QA_LOG = WORK / "qa_log.json"
DIFF = WORK / "focused_diff.md"

TEXT_RECORDS = {"title": 1, "message": 2, "messageTextUnder": 2, "messageTextCenter": 2}

TRANSLATIONS = [
    "Chỉ Là Đang Đấu Giá Thôi Mà♪",
    "<size=48>――Hội Trường Đấu Giá</size>",
    "C-chín vạn vàng...<br> ",
    "Vậy thì mười vạn vàng nhé♪<br> ",
    "Nào‚ mười vạn rồi! Còn ai trả mười vạn nữa không!<br>『Ma Đạo Bộc Thạch』 quý hiếm đây! Không nơi nào khác có đâu!<br> ",
    "Khụ... Giá trúng thầu cao hơn dự tính rồi. Cứ thế này thì<br>không ổn mất...<br> ",
    "Ôi chao‚ rắc rối rồi nhỉ‚ anh yêu.<br> ",
    "Em nghĩ là tại ai hả!<br>Marina đang đẩy giá lên còn gì!<br> ",
    "Hai ta cũng như nhau thôi mà? Em chỉ đang ra giá thôi đấy chứ♪<br> ",
    "...Nhưng mà‚ anh yêu‚ anh thật sự cần thắng bằng mọi giá đến thế sao?<br> ",
    "Đó là đạo cụ nguy hiểm có thể gây nổ lớn đấy.<br>Nó mà phát nổ trong căn cứ này thì rắc rối lắm‚ nếu được thì anh muốn đơn vị sử dụng nó.<br> ",
    "Vậy người giành được nó không phải anh mà là em cũng được nhỉ?<br>Nếu nằm trong tay em thì sẽ yên tâm hơn‚ khi cần em cũng có thể dùng mà.<br> ",
    "Ừm... có lẽ đúng là vậy‚ nhưng...<br> ",
    "Còn ai không! Không có rồi nhỉ! Vậy với giá mười vạn‚ cô gái bên kia thắng thầu!<br> ",
    "Cảm ơn nhiều ạ～.<br> ",
    "Khự! Trong lúc mình còn đang nghĩ thì...!<br>Thôi kệ vậy‚ đúng là nếu Marina giữ nó thì cũng yên tâm thật.<br> ",
    "Fufufu... Món này xem ra sẽ rất được săn đón ở Tiền Đồn nhỉ.<br>Không biết nên rao bán với giá bao nhiêu đây‚ em háo hức quá～.<br> ",
    "Khoan khoan khoan‚ em định bán nó thật à!?<br>Chẳng phải Marina sẽ giữ nó bên mình sao!?<br> ",
    "Tất nhiên em sẽ giữ bên mình rồi? Cho đến khi bán được thôi ạ.<br> ",
    "Cô nàng này...! Em chơi anh một vố rồi đấy!<br> ",
    "Xin anh cứ yên tâm. Em sẽ bảo đảm an toàn thật cẩn thận rồi bán cho người ở ngoài căn cứ mà♪<br> ",
    "Nào nào‚ anh không có thời gian tức giận đâu‚ anh yêu.<br>Món đấu giá tiếp theo đã được mang ra rồi kìa～.<br> ",
    "Khụ...!<br> ",
    "Nào‚ tiếp theo là món này!<br>Một vật phẩm đến từ vùng đất Hourai xa xôi‚ 『Thạch Đăng Hộ Mệnh』!<br> ",
    "Theo danh mục thì đây là đạo cụ có thể triển khai tường chắn ngay tại chỗ đấy.<br>Món này cũng có vẻ cần cho anh lắm nhỉ‚ anh yêu?<br> ",
    "Ừ‚ nghe nói chỉ dùng một lần‚ nhưng năng lực đó thì anh nhất định muốn có<br>lắm...!<br> ",
    "Nào‚ món này cũng bắt đầu từ một vạn!<br> ",
    "Tôi ra giá!<br> ",
    "Vậy em cũng tham gia. Hai vạn! Nào nào‚ lần này ai sẽ thắng đây♪<br> ",
    "Khụ... Lần này anh tuyệt đối không nhường đâu!<br> ",
    "Ôi chao‚ anh đang hừng hực khí thế nhỉ‚ anh yêu. Em không ghét đàn ông nhiệt huyết đâu～.<br> ",
    "Mười lăm vạn!<br> ",
    "Mười tám vạn!<br> ",
    "Khụ... h-hai mươi vạn!<br> ",
    "Hai mươi vạn! Đã có hai mươi vạn‚ nào còn ai nữa không!<br>Đây là 『Thạch Đăng Hộ Mệnh』 quý hiếm đấy!<br> ",
    "...Chắc đến đây là được rồi nhỉ. Em xin rút lui vậy～.<br> ",
    "Tốt! Lần này là anh thắng rồi!<br> ",
    "Vâng‚ em thua mất rồi ạ. Quả không hổ là anh yêu.<br> ",
    "Marina‚ em trông chẳng tiếc nuối chút nào nhỉ...? ...Hử?<br> ",
    "Khoan đã‚ mức giá này cao hơn dự toán rất nhiều!<br>Vậy nên em mới rút lui nhẹ nhàng như thế à!<br> ",
    "Nếu rẻ thì em thật sự cũng muốn có nó mà?<br>Điều đó không phải nói dối đâu ạ.<br> ",
    "Nhưng 『Thạch Đăng Hộ Mệnh』 là đạo cụ dựng tường chắn tại chỗ mà.<br>Dùng cho việc thám hiểm Đại Huyệt thì hơi không hợp nhỉ.<br> ",
    "Còn bảo liệu nó có bán được giá cao ở căn cứ này không thì...<br>không biết sẽ thế nào đây?<br> ",
    "Em biết rõ nên mới rút lui à... khụ...<br> ",
    "Nào‚ mọi chuyện bắt đầu thú vị rồi đấy♪ Đến món tiếp theo rồi‚ anh yêu!<br> ",
    "...Nào‚ còn vị nào khác không ạ?<br> ",
    "Ư...<br> ",
    "Vậy 『Đại Thương Cây Băng Khổng Lồ』 này sẽ thuộc về<br>cô gái bên kia với giá năm vạn!<br> ",
    "Cảm ơn ạ～.<br> ",
    "Lại là Marina thắng à...<br>Mà giá cũng sát mức thấp nhất của giá trúng thầu dự kiến còn gì.<br> ",
    "Vì mọi người có vẻ không ra giá nhiều lắm nên<br>em xin phép nhận lấy vậy～.<br> ",
    "Anh yêu cũng cứ cạnh tranh với em cũng được mà?<br> ",
    "Món anh nhắm tới vẫn chưa xuất hiện.<br>Anh không thể tiêu thêm tiền được nữa.<br> ",
    "Đúng vậy nhỉ. Nhờ mọi người hào hứng mà<br>những món ở nửa đầu đều đạt giá khá cao rồi.<br> ",
    "Anh lo lắng về ngân sách còn lại cũng là chuyện dễ hiểu.<br>Đúng là phán đoán bình tĩnh đấy‚ anh yêu♪<br> ",
    "...Chẳng lẽ tất cả đều đúng như em tính toán sao?<br> ",
    "Em đẩy giá lên ngay từ đầu<br>để có thể thắng các món sau với giá rẻ hơn à!<br> ",
    "Làm gì có chuyện đó ạ. Mọi người chỉ vui vẻ tham gia đấu giá thôi‚ đúng không nào?<br> ",
    "Giả nai quá đấy...! Em dám lừa anh như vậy sao!<br> ",
    "Giọng điệu cay cú ấy đối với em chẳng khác nào tiếng reo hò cổ vũ.<br>Em muốn được nghe nhiều hơn nữa cơ♪<br> ",
    "Thua thật rồi... Tới giờ mình toàn bị dắt mũi thôi sao.<br>Nhưng cuộc đấu còn chưa kết thúc đâu.<br> ",
    "Ôi‚ em mong lắm đấy.<br>Ufufufufu～.<br> ",
    "（Marina‚ em còn non lắm. Dù sao em cũng nghĩ mục tiêu của anh là<br>món tâm điểm 『Quả Cầu Cổ Đại』 chứ gì）<br> ",
    "（Tiếc là anh chẳng hứng thú gì với thứ đó.<br>Chừng nào món anh thật sự muốn còn chưa bị lộ‚ anh sẽ không thua đâu）<br> ",
    "...Anh sẽ khiến em hối hận vì đã thách thức vị Chỉ Huy Tiền Đồn này đấy‚<br>Marina.<br> ",
    "Nào! Cuối cùng cũng đến món tâm điểm hôm nay!<br>『Quả Cầu Cổ Đại』 xuất hiện rồi!<br> ",
    "Ra rồi nhỉ‚ anh yêu.<br>Quả cầu phong ấn một quái vật hùng mạnh‚ tất nhiên anh sẽ giành lấy nó chứ?<br> ",
    "Alicia có bảo anh phải thắng thầu.<br>Nhưng đã là món tâm điểm thì chắc đắt lắm‚ nếu không đủ tiền thì cũng đành chịu thôi.<br> ",
    "Ôi chao‚ anh không cố chấp như em tưởng nhỉ?<br>Nếu phong ấn quái vật bị giải ở ngay căn cứ này thì sẽ nguy to đấy?<br> ",
    "Tất nhiên là nguy hiểm‚ nhưng đã là món tâm điểm thì hẳn được quản lý chặt chẽ.<br>Người thắng thầu cũng sẽ không đối xử cẩu thả với một vật phẩm đắt giá đâu.<br> ",
    "Nếu đúng vậy thì tốt...<br> ",
    "Cùng lúc Marina khẽ lẩm bẩm‚ 『Quả Cầu Cổ Đại』 bắt đầu chầm chậm tỏa ra một luồng hào quang màu bóng tối――",
]

def detect_newline(data: bytes):
    if b"\r\n" in data:
        return "CRLF", "\r\n"
    return "LF", "\n"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_text_preserve(path):
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    encoding = "utf-8-sig" if bom else "utf-8"
    newline_name, newline = detect_newline(data)
    return data.decode(encoding), bom, encoding, newline_name, newline, hashlib.sha256(data).hexdigest(), len(data)

def split_line(line):
    ending = ""
    body = line
    if body.endswith("\r\n"):
        body = body[:-2]; ending = "\r\n"
    elif body.endswith("\n"):
        body = body[:-1]; ending = "\n"
    return body, ending

def get_text_field(parts):
    if not parts: return None
    idx = TEXT_RECORDS.get(parts[0])
    if idx is None or len(parts) <= idx: return None
    return idx

def tags(s):
    return re.findall(r"<[^>]+>", s)

def placeholders(s):
    return re.findall(r"%(?:\d+\$)?[sd]|\{[^{}]+\}|\$\{[^{}]+\}|\\[nrt]|%%", s)

def ascii_comma_in_field(s):
    return "," in s

WORK.mkdir(parents=True, exist_ok=True)
text, bom, encoding, newline_name, newline, en_hash, en_bytes = read_text_preserve(EN_ASSET)
lines = text.splitlines(keepends=True)
candidates = []
for i, line in enumerate(lines, 1):
    body, ending = split_line(line)
    parts = body.split(',')
    idx = get_text_field(parts)
    if idx is not None:
        candidates.append({"line": i, "record_type": parts[0], "text_index": idx, "source_text": parts[idx], "parts_count": len(parts)})

qa = {"scene": SCENE, "qa_status": "PASS", "blockers": [], "warnings": [], "info": [], "kept_english_records": [], "intentional_identical_records": []}
if len(candidates) != len(TRANSLATIONS):
    qa["blockers"].append({"type": "TRANSLATION_COUNT_MISMATCH", "candidate_count": len(candidates), "translation_count": len(TRANSLATIONS)})

for n, vi in enumerate(TRANSLATIONS):
    if ascii_comma_in_field(vi):
        qa["blockers"].append({"type": "ASCII_COMMA_IN_VI_FIELD", "entry_index": n + 1, "text": vi})

out_lines = list(lines)
entries = []
if not qa["blockers"]:
    for n, cand in enumerate(candidates):
        vi = TRANSLATIONS[n]
        line = out_lines[cand["line"]-1]
        body, ending = split_line(line)
        parts = body.split(',')
        source_parts = parts[:]
        idx = cand["text_index"]
        parts[idx] = vi
        out_lines[cand["line"]-1] = ','.join(parts) + ending
        entries.append({
            "index": n + 1,
            "line": cand["line"],
            "record_type": cand["record_type"],
            "speaker_or_empty": source_parts[1] if len(source_parts) > 1 and cand["record_type"] != "title" else None,
            "source_text": cand["source_text"],
            "vi_text": vi,
            "match_status": "ORDERED_CONTEXT_MATCH",
            "translation_status": "TRANSLATED",
        })
    out_text = ''.join(out_lines)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_text.encode('utf-8-sig' if bom else 'utf-8'))

    vi_text, vi_bom, vi_encoding, vi_newline_name, _, vi_hash, vi_bytes = read_text_preserve(VI_ASSET)
    vi_lines = vi_text.splitlines(keepends=True)
    if len(vi_lines) != len(lines):
        qa["blockers"].append({"type": "LINE_COUNT_MISMATCH", "en": len(lines), "vi": len(vi_lines)})
    if vi_bom != bom:
        qa["blockers"].append({"type": "BOM_MISMATCH", "en": bom, "vi": vi_bom})
    if vi_newline_name != newline_name:
        qa["blockers"].append({"type": "NEWLINE_MISMATCH", "en": newline_name, "vi": vi_newline_name})

    delimiter_mismatches = []
    technical_mismatches = []
    tag_mismatches = []
    placeholder_mismatches = []
    unchanged_text_records = []
    ascii_comma_violations = []
    for i, (el, vl) in enumerate(zip(lines, vi_lines), 1):
        eb, _ = split_line(el); vb, _ = split_line(vl)
        if eb.count(',') != vb.count(','):
            delimiter_mismatches.append(i)
            continue
        ep = eb.split(','); vp = vb.split(',')
        eidx = get_text_field(ep); vidx = get_text_field(vp)
        if eidx is None:
            if ep != vp:
                technical_mismatches.append({"line": i, "type": "NON_TEXT_CHANGED"})
            continue
        if eidx != vidx or ep[0] != vp[0]:
            technical_mismatches.append({"line": i, "type": "TEXT_INDEX_OR_RECORD_TYPE_CHANGED"})
            continue
        if ep[:eidx] + ep[eidx+1:] != vp[:vidx] + vp[vidx+1:]:
            technical_mismatches.append({"line": i, "type": "TECHNICAL_FIELDS_CHANGED"})
        if tags(ep[eidx]) != tags(vp[vidx]):
            tag_mismatches.append({"line": i, "en_tags": tags(ep[eidx]), "vi_tags": tags(vp[vidx])})
        if placeholders(ep[eidx]) != placeholders(vp[vidx]):
            placeholder_mismatches.append({"line": i, "en_placeholders": placeholders(ep[eidx]), "vi_placeholders": placeholders(vp[vidx])})
        if ep[eidx] == vp[vidx]:
            unchanged_text_records.append(i)
        if ',' in vp[vidx]:
            ascii_comma_violations.append(i)
    if delimiter_mismatches: qa["blockers"].append({"type": "DELIMITER_MISMATCH", "lines": delimiter_mismatches})
    if technical_mismatches: qa["blockers"].append({"type": "TECHNICAL_MISMATCH", "items": technical_mismatches})
    if tag_mismatches: qa["blockers"].append({"type": "TAG_MISMATCH", "items": tag_mismatches})
    if placeholder_mismatches: qa["blockers"].append({"type": "PLACEHOLDER_MISMATCH", "items": placeholder_mismatches})
    if unchanged_text_records: qa["blockers"].append({"type": "UNINTENTIONAL_KEPT_EN_TEXT", "lines": unchanged_text_records})
    if ascii_comma_violations: qa["blockers"].append({"type": "ASCII_COMMA_IN_OUTPUT_TEXT_FIELD", "lines": ascii_comma_violations})

    # Targeted English leftovers: avoid naive ASCII-word scans because many Vietnamese syllables are unaccented.
    targeted_patterns = [
        r"\bHoney\b", r"\bhoney\b", r"\bgold\b", r"\bCommander\b", r"\bFrontline\b",
        r"\bAuction\b", r"\bHall\b", r"\bAncient\b", r"\bOrb\b", r"\bGuardian\b",
        r"\bStone\b", r"\bLantern\b", r"\bUgh\b", r"\bTch\b", r"\bYes\b", r"\bNo\b",
        r"\bOh dear\b", r"\bThank you\b", r"\bWait\b", r"\bFired up\b",
        r"\bpricey\b", r"\bbid\b", r"\bauction\b", r"\bmonster\b",
    ]
    leftover_markers = []
    for entry in entries:
        vt = re.sub(r"<[^>]+>", " ", entry["vi_text"])
        for pat in targeted_patterns:
            if re.search(pat, vt):
                leftover_markers.append({"line": entry["line"], "pattern": pat, "text": entry["vi_text"]})
    if leftover_markers:
        qa["blockers"].append({"type": "TARGETED_ENGLISH_LEFTOVER", "items": leftover_markers})
    qa["info"].append({"type": "INTENTIONAL_LATIN_TEXT", "items": ["Marina", "Alicia", "Hourai", "Fufufu", "Ufufufufu"], "reason": "proper names or stylized laugh/onomatopoeia intentionally retained"})

    if qa["blockers"]:
        qa["qa_status"] = "FAIL"
    else:
        qa["qa_status"] = "PASS"

    manifest = {
        "scene": SCENE,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_paths": {"ja_json": str(JP_JSON), "en_json": str(EN_JSON), "en_asset": str(EN_ASSET)},
        "output_path": str(VI_ASSET),
        "artifact_paths": {"manifest": str(MANIFEST), "qa_log": str(QA_LOG), "focused_diff": str(DIFF), "script": str(WORK / "generate_vi.py")},
        "source_properties": {"sha256": en_hash, "bytes": en_bytes, "bom": bom, "encoding": encoding, "newline": newline_name, "line_count": len(lines)},
        "output_properties": {"sha256": vi_hash, "bytes": vi_bytes, "bom": vi_bom, "encoding": vi_encoding, "newline": vi_newline_name, "line_count": len(vi_lines)},
        "candidate_counts": {"total": len(candidates), **{rt: sum(1 for c in candidates if c["record_type"] == rt) for rt in TEXT_RECORDS}},
        "translated_records": len(entries),
        "mapping_basis": "JP ja.json primary; EN en.json and EN asset used for ordered alignment/context; asset candidate order authoritative.",
        "character_notes": {"Marina": "Giữ tên Marina trong lời dịch; giọng thương nhân trêu chọc. 旦那さま rendered as anh yêu as scene-specific teasing address to Commander.", "Commander": "<user>/司令官 rendered as anh/Chỉ Huy depending context."},
        "entries": entries,
        "qa_status": qa["qa_status"],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # Focused diff only text records.
    before = []
    after = []
    for c, e in zip(candidates, entries):
        before.append(f"L{c['line']}: {c['record_type']} | {c['source_text']}\n")
        after.append(f"L{c['line']}: {c['record_type']} | {e['vi_text']}\n")
    diff = ''.join(difflib.unified_diff(before, after, fromfile="EN asset text fields", tofile="VI asset text fields", lineterm="\n"))
    DIFF.write_text("# Focused Diff — hmn_10030100002\n\n```diff\n" + diff + "\n```\n", encoding="utf-8")
else:
    qa["qa_status"] = "FAIL"

qa["summary"] = {
    "candidate_records": len(candidates),
    "translation_entries": len(TRANSLATIONS),
    "blocker_count": len(qa["blockers"]),
    "adult_h18": "No explicit H18 content in this asset; project 18+ confirmation noted.",
    "unchanged_english_policy": "No text record may remain identical to EN unless logged intentional.",
}
QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"qa_status": qa["qa_status"], "blockers": len(qa["blockers"]), "candidates": len(candidates), "output": str(VI_ASSET), "qa_log": str(QA_LOG)}, ensure_ascii=False, indent=2))

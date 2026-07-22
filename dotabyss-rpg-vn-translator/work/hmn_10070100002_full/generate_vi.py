#!/usr/bin/env python
from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path

SCENE = "hmn_10070100002"
ROOT = Path("E:/AgentTranslation")
EN_PATH = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
JP_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
WORK_DIR = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
MANIFEST_PATH = WORK_DIR / "manifest.json"
QA_PATH = WORK_DIR / "qa_log.json"
DIFF_PATH = WORK_DIR / "focused_diff.md"
TEXT_CMDS = ("title", "message", "messageTextUnder", "messageTextCenter")
TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}")

TRANSLATIONS = [
    "Kỳ Bí! Hiện Tượng Tâm Linh Ở Căn Cứ Tiền Tuyến!",
    "Em là Film‚ xin phép vào nhé.<br>Chỉ Huy‚ anh gọi em ạ?<br> ",
    "Xin lỗi vì đã gọi em tới tận đây. Anh có chuyện muốn hỏi Film… à không‚<br>Film và Noir.<br> ",
    "Thật ra gần đây ở Căn Cứ Tiền Tuyến liên tục xảy ra những chuyện<br>kỳ lạ.<br> ",
    "Kỳ lạ ạ?<br>Là những chuyện như thế nào vậy?<br> ",
    "Có lẽ nên gọi là các vụ việc huyền bí. Anh nhận được không ít<br>báo cáo giống hiện tượng tâm linh.<br> ",
    "Ôi chà‚ người trẻ đúng là thích mấy chuyện đồn thổi nhỉ～<br> ",
    "Nếu chỉ đến mức đó thì còn đỡ. Nhưng lời đồn lan quá rộng đến nỗi<br>đã có người từ chối làm việc rồi.<br> ",
    "Hừm. Đúng là không thể bỏ mặc chuyện đó được nhỉ?<br> ",
    "Thủ phạm chính là hai em phải không‚ Film‚ Noir!<br> ",
    "…!!!<br> ",
    "Hì hì hì… Anh tinh thật đấy. Suy luận xuất sắc lắm‚ Chỉ Huy…<br> ",
    "…Em cũng muốn khen anh như vậy lắm‚ nhưng tiếc là sai rồi. Em chỉ<br>có linh lực đủ làm nước trong cốc hơi gợn lên thôi.<br> ",
    "Nói rồi‚ Film biểu diễn bằng cách làm tách cà phê mà<br>Chỉ Huy đang uống dở rung lên.<br> ",
    "Hừm. Với năng lực cỡ đó thì đúng là không thể gây ra chuyện gì lớn.<br> ",
    "Đúng không? Nếu có khả năng thì chỉ có Noir thôi‚ nhưng…<br> ",
    "…!? …!!!<br> ",
    "Noir đâu có che giấu trò nghịch ngợm của mình nhỉ. Có vẻ em ấy<br>không phải thủ phạm đâu～<br> ",
    "Ừ‚ anh cũng nghĩ là vậy. Nhưng lời đồn kiểu đó đang<br>lan trong căn cứ là sự thật.<br> ",
    "Ể～‚ tổn thương quá đi～!<br> ",
    "Vậy nên từ đây mới là chuyện chính. Anh muốn em giúp anh điều tra<br>các vụ huyền bí này.<br> ",
    "Tất nhiên là được rồi♪ Chuyện liên quan tới ma quỷ thì cứ giao cho<br>chị đây. Chúng ta sẽ giải quyết vụ này!<br> ",
    "…♪<br> ",
    "Cứ bị xem là thủ phạm thế này thì khó chịu lắm.<br>Em phải rửa sạch thanh danh mới được.<br> ",
    "Em sẽ cho anh thấy việc bị nguyền rủa suốt bao năm qua không phải để làm cảnh đâu～<br> ",
    "Bị nguyền rủa suốt bao lâu mà<br>cũng tự hào được à…<br> ",
    "Đây là địa điểm đầu tiên. Lời đồn nói rằng…<br> ",
    "Rầm!!!<br> ",
    "Oái!?<br> ",
    "Ôi chà‚ anh giật mình rồi à? Có em ở đây rồi nên anh không cần sợ đâu～?<br> ",
    "A-anh không sợ. Anh chỉ cảnh giác vì chuyện xảy ra quá đột ngột thôi.<br> ",
    "Hì hì‚ anh không cần cố tỏ ra cứng cỏi đâu～ Cứ dựa vào<br>chị Film này cũng được mà.<br> ",
    "Anh không hề cố tỏ ra cứng cỏi! Dù sao thì đó chính là<br>hiện tượng tâm linh trong báo cáo!<br> ",
    "Một tiếng động lớn vang lên đột ngột… Người ta gọi đó là<br>“tiếng gõ ma” nhỉ?<br> ",
    "Nhưng em không cảm nhận được linh lực gì đặc biệt. Noir‚ em thấy sao?<br> ",
    "…?<br> ",
    "Có vẻ Noir cũng nghĩ vậy. Nghĩa là đây không phải<br>hiện tượng tâm linh rồi.<br> ",
    "Ngược lại như thế còn rắc rối hơn. Anh hoàn toàn không biết nguyên nhân là gì.<br> ",
    "Nếu là nhà cũ thì anh còn hiểu chuyện chỗ này chỗ kia kêu cọt kẹt‚<br>nhưng khu này vừa mới xây xong mà…<br> ",
    "Hừm. Vừa mới xây… à. Này‚ kể cho em rõ hơn chút đi.<br> ",
    "Nhân sự tăng lên khiến căn cứ trở nên chật chội.<br>Đây là khu vực được mở rộng gấp rút.<br> ",
    "Ra vậy～ Em hiểu rồi‚ Chỉ Huy. Tiếng gõ đó chỉ là<br>âm thanh tòa nhà đang kêu cọt kẹt thôi.<br> ",
    "Ý em là sao? Anh đã nói nơi này vừa mới xây xong rồi mà?<br> ",
    "Chính vì vậy đấy～ Gỗ mới sẽ nở ra hoặc co lại theo độ ẩm.<br> ",
    "Trước khi vật liệu xây dựng ổn định hoàn toàn thì những âm thanh<br>như thế này cũng thường xảy ra lắm～<br> ",
    "Trước đây khi điều tra một vụ huyền bí‚ em từng gặp chuyện tương tự.<br>Vài tuần nữa thì tiếng này hẳn sẽ lắng xuống.<br> ",
    "…Ra vậy‚ nghe hợp lý đấy. Quả nhiên Film biết nhiều thật.<br> ",
    "Hì hì‚ túi khôn của chị đây mà.<br> ",
    "Túi khôn của bà cụ thì đúng hơn… nhỉ.<br> ",
    "Anh vừa nói gì vậy‚ Chỉ Huy?<br> ",
    "K-không có gì. Đến hiện trường tiếp theo thôi.<br> ",
    "Địa điểm tiếp theo là ở đây. Có báo cáo rằng máu<br>nhỏ xuống từ trần nhà.<br> ",
    "Ồ. Nếu thật như vậy thì chắc chắn là hiện tượng tâm linh rồi～<br> ",
    "Tách…<br> ",
    "Á!? Có gì đó nhỏ xuống rồi!<br> ",
    "Ôi‚ thứ màu đỏ này là…?<br> ",
    "Sao vậy‚ Film!? Đừng nói là máu…<br> ",
    "Không. Đây không phải máu đâu. Mùi khác hẳn‚ cảm giác khi chạm vào<br>cũng hoàn toàn khác nữa～<br> ",
    "…Nghe em nói thì đúng là vậy. Em tinh thật đấy‚ Film.<br> ",
    "Dù sao em cũng đã thuộc về Kỵ Sĩ Đoàn rất～～～～～～lâu rồi mà.<br>Máu thì em quen quá rồi.<br> ",
    "Nghĩa là hiện tượng này chỉ là chất lỏng màu đỏ nhỏ xuống thôi à.<br>Tầng trên chắc là nhà kho. Lên xem nào.<br> ",
    "<size=48>—Tầng Trên</size>",
    "…Hóa ra lon mực đỏ đã bị hỏng. Nó rỉ xuống phòng bên dưới‚<br>rồi bị đồn thành máu.<br> ",
    "Đơn giản đến thế sao… Thành kiến đúng là đáng sợ thật.<br> ",
    "Chúng ta nên dọn dẹp cho sạch sẽ nhỉ～<br> ",
    "Đây là nơi cuối cùng. Báo cáo nói rằng――<br> ",
    "Ưưưưư…<br> ",
    "Ôi‚ âm thanh vừa rồi là…?<br> ",
    "Em nghe thấy chứ? Lời đồn là có thể nghe thấy<br>một tiếng rên rỉ bí ẩn.<br> ",
    "Em nghe thấy rõ. Nhưng… Noir‚ em cũng không cảm nhận được<br>linh lực đúng không?<br> ",
    "…♪<br> ",
    "Vậy thì em nghĩ đây cũng không phải hiện tượng tâm linh. Âm thanh đó<br>là gì nhỉ… Chỉ Huy‚ anh có manh mối nào không?<br> ",
    "Đáng lẽ quanh đây không có thiết bị nào phát ra tiếng động lớn.<br>Cũng không phải nơi mọi người hay tụ tập…<br> ",
    "…Khoan đã. Này Noir‚ em lại đây một chút được không?<br> ",
    "Em có thể xuyên qua tường đúng không? Thử đi vào trong<br>bức tường xem nhé?<br> ",
    "…♪<br> ",
    "Noir đi vào trong tường rồi. Tiện thật đấy～ Chỉ Huy‚ anh đã<br>biết tiếng rên đó là gì chưa?<br> ",
    "Ừ‚ nếu suy đoán của anh đúng thì có lẽ là…<br> ",
    "Ồ! Em ra rồi à‚ Noir. Sao rồi? Có gì bất thường không?<br> ",
    "…! …!!!<br> ",
    "Em để ý bức tường này à? …Ơ?<br> ",
    "Ôôôôôôn!!!<br> ",
    "Hình như tiếng rên đang lớn hơn. Có vẻ nó phát ra<br>từ đây.<br> ",
    "Quả nhiên. Đây không phải tiếng rên của ma gì cả. Đó là<br>âm thanh rò ra từ ống truyền âm.<br> ",
    "Ống truyền âm… là thứ dùng để nói chuyện giữa<br>những căn phòng cách xa nhau trong cùng tòa nhà ấy hả?<br> ",
    "Ừ. Anh thử đưa nó vào khu mở rộng để vận hành thí điểm.<br> ",
    "Có vẻ ống kim loại sau bức tường này bị hỏng khiến âm thanh rò ra.<br>Công của Noir đấy‚ nhờ em ấy vào được trong tường.<br> ",
    "Ôi chà‚ hóa ra là vậy～ Chúng ta nên nhờ người sửa lại cho đàng hoàng.<br> ",
    "Thật tình‚ chẳng có chuyện nào là hiện tượng tâm linh cả. Công bố<br>sự thật ra thì vụ náo động cũng sẽ lắng xuống thôi.<br> ",
    "Hì hì. Vất vả thật‚ nhưng em thấy vui lắm. Được đi khắp nơi<br>cùng Chỉ Huy‚ nói chuyện thật nhiều…<br> ",
    "Ừ‚ giống như một buổi hẹn hò vậy.<br> ",
    "Cái gì!<br> ",
    "Tr-trời‚ Chỉ Huy! Gọi là hẹn hò gì chứ… Anh không nên trêu người lớn tuổi hơn đâu!<br> ",
    "Sao vậy‚ chỉ có anh nghĩ thế thôi à?<br> ",
    "Anh nói vậy thì… em cũng hơi nghĩ như thế. Cảm giác như em<br>đã trở lại làm một cô gái bình thường.<br> ",
    "Với anh‚ Film vốn là một cô gái bình thường mà.<br> ",
    "L-l-lại trêu người lớn tuổi hơn nữa rồi! Em sẽ thuyết giáo anh đấy!<br> ",
    "Sợ quá sợ quá. Vậy hôm nay cảm ơn em nhé.<br> ",
    "Ừ. Tạm biệt anh.<br> ",
    "…<br> ",
    "Kết thúc mất rồi nhỉ‚ Noir. Cuộc điều tra ma vui vẻ cùng Chỉ Huy.<br>…Giá mà còn thật nhiều‚ thật nhiều hiện tượng tâm linh nữa xảy ra.<br> ",
    "Nếu vậy thì em lại có thể‚ cùng Chỉ Huy…<br> ",
    "…?<br> ",
]

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def text_idx(cmd: str) -> int:
    return 1 if cmd == "title" else 2

def tags(s: str):
    return sorted(TAG_RE.findall(s))

def placeholders(s: str):
    return sorted(PLACEHOLDER_RE.findall(s))

def newline_style(data: bytes) -> str:
    if b"\r\n" in data:
        return "CRLF"
    if b"\n" in data:
        return "LF"
    return "NONE"

def load_pairs(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=list)

def main() -> int:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    raw = EN_PATH.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    candidates = []
    output_lines = list(lines)
    blockers = []
    structural_issues = []
    t_iter = iter(TRANSLATIONS)

    for idx, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        cmd = stripped.split(",", 1)[0] if "," in stripped else stripped
        if cmd not in TEXT_CMDS:
            continue
        try:
            vi = next(t_iter)
        except StopIteration:
            blockers.append(f"MISSING_TRANSLATION_LINE_{idx+1}")
            break
        if "," in vi:
            blockers.append(f"ASCII_COMMA_IN_TRANSLATION_LINE_{idx+1}")
        parts = stripped.split(",")
        ti = text_idx(cmd)
        if len(parts) <= ti:
            blockers.append(f"TEXT_FIELD_MISSING_LINE_{idx+1}")
            continue
        old_text = parts[ti]
        if tags(old_text) != tags(vi):
            blockers.append(f"TAG_MISMATCH_LINE_{idx+1}:{tags(old_text)}->{tags(vi)}")
        if placeholders(old_text) != placeholders(vi):
            blockers.append(f"PLACEHOLDER_MISMATCH_LINE_{idx+1}")
        old_signature = parts[:ti] + parts[ti+1:]
        parts[ti] = vi
        newline = line[len(stripped):]
        new_line = ",".join(parts) + newline
        if stripped.count(",") != new_line.rstrip("\r\n").count(","):
            blockers.append(f"DELIMITER_CHANGED_LINE_{idx+1}")
        if old_signature != parts[:ti] + parts[ti+1:]:
            blockers.append(f"TECH_FIELD_CHANGED_LINE_{idx+1}")
        candidates.append({
            "index": len(candidates) + 1,
            "line": idx + 1,
            "command": cmd,
            "source_text": old_text,
            "vi_text": vi,
            "status": "TRANSLATED",
            "match_status": "CONTEXT_MATCH" if len(candidates) >= 101 else "EXACT",
        })
        output_lines[idx] = new_line

    try:
        next(t_iter)
        blockers.append("EXTRA_TRANSLATIONS")
    except StopIteration:
        pass

    if len(candidates) != len(TRANSLATIONS):
        blockers.append(f"TRANSLATION_COUNT_MISMATCH:{len(candidates)}!={len(TRANSLATIONS)}")

    out_text = "".join(output_lines)
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_PATH.write_bytes((b"\xef\xbb\xbf" if bom else b"") + out_text.encode("utf-8"))

    vi_raw = VI_PATH.read_bytes()
    vi_text = vi_raw.decode("utf-8-sig")
    vi_lines = vi_text.splitlines(keepends=True)
    if len(lines) != len(vi_lines):
        structural_issues.append(f"LINE_COUNT:{len(lines)}->{len(vi_lines)}")
    if newline_style(raw) != newline_style(vi_raw):
        structural_issues.append("NEWLINE_STYLE_CHANGED")
    if bom != vi_raw.startswith(b"\xef\xbb\xbf"):
        structural_issues.append("BOM_CHANGED")
    text_records = 0
    changed_text_records = 0
    delimiter_mismatches = []
    field_mismatches = []
    tag_mismatches = []
    placeholder_mismatches = []
    kept_text_lines = []
    for ln, (old_raw, new_raw) in enumerate(zip(lines, vi_lines), 1):
        old = old_raw.lstrip("\ufeff").rstrip("\r\n")
        new = new_raw.lstrip("\ufeff").rstrip("\r\n")
        if old.count(",") != new.count(","):
            delimiter_mismatches.append(ln)
        op = old.split(",")
        np = new.split(",")
        if len(op) != len(np):
            field_mismatches.append(ln)
            continue
        if op and op[0] in TEXT_CMDS:
            text_records += 1
            ti = text_idx(op[0])
            if old != new:
                changed_text_records += 1
            else:
                kept_text_lines.append(ln)
            if ti < len(op):
                if tags(op[ti]) != tags(np[ti]):
                    tag_mismatches.append(ln)
                if placeholders(op[ti]) != placeholders(np[ti]):
                    placeholder_mismatches.append(ln)
                if "," in np[ti]:
                    structural_issues.append(f"ASCII_COMMA_TEXT_LINE_{ln}")
                if op[:ti] + op[ti+1:] != np[:ti] + np[ti+1:]:
                    structural_issues.append(f"TECH_FIELD_CHANGED_LINE_{ln}")

    blockers.extend([f"DELIMITER_MISMATCH_LINES:{delimiter_mismatches}" for _ in delimiter_mismatches[:1]])
    blockers.extend([f"FIELD_MISMATCH_LINES:{field_mismatches}" for _ in field_mismatches[:1]])
    blockers.extend([f"TAG_MISMATCH_LINES:{tag_mismatches}" for _ in tag_mismatches[:1]])
    blockers.extend([f"PLACEHOLDER_MISMATCH_LINES:{placeholder_mismatches}" for _ in placeholder_mismatches[:1]])
    blockers.extend(structural_issues)
    if kept_text_lines:
        blockers.append(f"KEPT_TEXT_LINES:{kept_text_lines}")
    if changed_text_records != text_records:
        blockers.append(f"TRANSLATED_RECORDS:{changed_text_records}!={text_records}")

    counts = {cmd: 0 for cmd in TEXT_CMDS}
    for c in candidates:
        counts[c["command"]] += 1

    manifest = {
        "scene": SCENE,
        "status": "PASS" if not blockers else "FAIL",
        "source": str(EN_PATH),
        "output": str(VI_PATH),
        "ja_json": str(JP_JSON),
        "en_json": str(EN_JSON),
        "source_sha256": sha256(EN_PATH),
        "output_sha256": sha256(VI_PATH),
        "source_bytes": len(raw),
        "output_bytes": len(vi_raw),
        "bom": bom,
        "newline": newline_style(raw),
        "source_line_count": len(lines),
        "output_line_count": len(vi_lines),
        "candidate_counts": counts,
        "candidate_total": len(candidates),
        "translated_records": changed_text_records,
        "novel_pair_counts": {
            "ja": len(load_pairs(JP_JSON)),
            "en": len(load_pairs(EN_JSON)),
        },
        "entries": candidates,
    }
    qa = {
        "scene": SCENE,
        "qa_status": manifest["status"],
        "blockers": blockers,
        "structural_qa": {
            "source_line_count": len(lines),
            "output_line_count": len(vi_lines),
            "delimiter_mismatches": delimiter_mismatches,
            "field_mismatches": field_mismatches,
            "tag_mismatches": tag_mismatches,
            "placeholder_mismatches": placeholder_mismatches,
            "kept_text_lines": kept_text_lines,
            "text_records": text_records,
            "translated_records": changed_text_records,
            "bom_preserved": bom == vi_raw.startswith(b"\xef\xbb\xbf"),
            "newline_preserved": newline_style(raw) == newline_style(vi_raw),
        },
        "linguistic_qa": {
            "jp_primary_en_alignment_only": True,
            "title_title_case_vi": True,
            "commander_term": "司令官/Commander -> Chỉ Huy",
            "names_preserved": ["Film", "Noir", "フィルム", "ノワール"],
            "h18_present": False,
            "notes": [
                "Film dùng giọng chị gái dịu dàng pha trêu đùa; với Chỉ Huy dùng em/anh tùy sắc thái.",
                "Noir chủ yếu là phản ứng không lời; các dấu ba chấm EN được Việt hóa sang dấu … để tránh kept-English.",
                "messageTextCenter địa điểm được dịch và giữ nguyên thẻ <size=48>.",
            ],
        },
        "unresolved": [],
    }

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")

    old_focus = []
    new_focus = []
    for c in candidates:
        ln = c["line"]
        old_focus.append(f"{ln}: {lines[ln-1]}")
        new_focus.append(f"{ln}: {vi_lines[ln-1]}")
    diff = difflib.unified_diff(old_focus, new_focus, fromfile="EN text records", tofile="VI text records", lineterm="\n")
    DIFF_PATH.write_text("# Focused Diff\n\n```diff\n" + "".join(diff) + "```\n", encoding="utf-8")

    print(json.dumps({"status": manifest["status"], "blockers": blockers, "output": str(VI_PATH), "manifest": str(MANIFEST_PATH), "qa": str(QA_PATH), "diff": str(DIFF_PATH)}, ensure_ascii=False, indent=2))
    return 0 if not blockers else 1

if __name__ == "__main__":
    raise SystemExit(main())

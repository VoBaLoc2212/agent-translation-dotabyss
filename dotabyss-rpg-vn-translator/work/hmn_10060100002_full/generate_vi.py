from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path

SCENE = "hmn_10060100002"
ROOT = Path("E:/AgentTranslation")
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_ASSET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
MANIFEST = WORK / "manifest.json"
QA_LOG = WORK / "qa_log.json"
FOCUSED_DIFF = WORK / "focused_diff.md"
TEXT_CMDS = {"title", "message", "messageTextUnder", "messageTextCenter"}
TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}")

VI_TRANSLATIONS = [
    "Có Thật Sự Cần Điều Trị Không?",
    "<size=48>—Căn Cứ Tiền Tuyến‚ Phòng Điều Trị</size>",
    "Noemi đã chuẩn bị phòng điều trị từ sáng sớm.<br> ",
    "…Hôm nay không có chuyến thăm dò nào‚ nên mình hãy chuyên tâm<br>vào công việc của một giáo sĩ nào.<br> ",
    "Để có thể giúp ích cho mọi người‚ và cho Chỉ Huy hơn nữa‚<br>mình phải tích lũy thật nhiều kinh nghiệm qua việc chữa trị hằng ngày!<br> ",
    "…Nói vậy thôi chứ cũng không có nhiều người bị thương ghé đến lắm.<br>Nếu có thời gian‚ mình phải dọn dẹp để nơi này luôn sạch sẽ mới được.<br> ",
    "A‚ Noemi! Cô có thể chữa trị giúp tôi được không?<br> ",
    "Vâng vâng‚ tất nhiên rồi! Xin mời qua bên này nào～<br> ",
    "…Xin hãy chữa lành. Rồi‚ tôi nghĩ thế này là ổn rồi đấy.<br> ",
    "Ôi‚ cảm ơn cô nhiều lắm‚ Noemi!<br>Đau vai thế này thì vung vũ khí khó chịu thật sự…<br> ",
    "Không có gì đâu‚ đó là kết quả của việc anh đã cố gắng bảo vệ căn cứ mà.<br>Nhưng xin anh đừng gắng sức quá nhé?<br> ",
    "Vâng! Cảm ơn cô rất nhiều!<br> ",
    "Người tiếp theo‚ xin mời～<br> ",
    "Noemi ơi‚ nhờ cô đấy! Tôi hình như hơi bị đau chân rồi.<br> ",
    "Ôi‚ vậy thì phiền thật nhỉ～ …Ủa? Anh vẫn đi bộ bình thường tới đây sao?<br> ",
    "À‚ ờ‚ cũng không đến mức không đi được!<br>Nhưng nếu đang chiến đấu mà nó đau lên thì sẽ rắc rối lắm…<br> ",
    "Thì ra là vậy! Vậy tôi sẽ chữa cho thật cẩn thận nhé～<br> ",
    "Ơ‚ hì hì… Tôi lỡ bị thương nhẹ ở tay.<br>Tôi chỉ mong cô nắm chặt lấy tay tôi rồi chữa lành cho thôi…<br> ",
    "Sao anh lại bị thương ở chỗ đó chứ!?<br>Tôi sẽ chữa‚ sẽ chữa mà‚ nhưng xin hãy cẩn thận hơn nhé!<br> ",
    "Đầu tôi có một cục u này! Tôi muốn cô xoa xoa rồi đặt tay lên chữa cho tôi ấy mà!<br> ",
    "Chỉ là cục u thì cứ để yên cũng tự khỏi thôi mà～!<br>Anh có thật sự cần điều trị không vậy!?<br> ",
    "K‚ không‚ đau thật mà! Thật đấy! Xin cô chữa cho tôi với!<br> ",
    "Thôi nào‚ tôi sẽ tin anh đấy nhé～?<br> ",
    "X‚ xin lỗi… A‚ được chữa trị trong lúc bị mắng cũng hay thật…<br> ",
    "Có・Nghe・Tôi・Nói・Không～!?<br> ",
    "Phù… Cũng không còn ai vào nữa‚<br>chắc sắp hết bệnh nhân rồi nhỉ?<br> ",
    "Vậy mình ra ngoài nghỉ một chút…<br> ",
    "Khi Noemi rời khỏi phòng điều trị‚<br>cô bắt gặp một cảnh tượng ngoài sức tưởng tượng.<br> ",
    "Tôi đã chờ mãi rồi đấy! Tiếp theo phải đến lượt tôi chứ!<br> ",
    "Toàn ưu tiên binh lính là vô lý quá còn gì!<br>Bọn tôi cũng muốn được Noemi chữa trị chứ!<br> ",
    "Đừng làm ồn‚ Noemi sẽ nghe thấy đấy!<br>Mọi người đều bình đẳng! Xếp hàng‚ xếp hàng nào!<br> ",
    "Anh vừa được chữa rồi còn gì!<br>Cái vai sao rồi‚ cái vai ấy!<br> ",
    "Tiếp theo là eo của tôi! Có ý kiến gì không!?<br> ",
    "Rất nhiều đàn ông lớn tiếng quát tháo‚<br>tranh cãi xem ai được vào phòng điều trị trước.<br> ",
    "S‚ sao chuyện lại thành ra thế này～!?<br> ",
    "A! Noemi! Xin hãy chữa trị cho tôi!<br> ",
    "Đừng có chen hàng! Anh xuống cuối‚ cuối hàng ấy!<br> ",
    "Nhưng trong nhiệm vụ lần trước‚ Noemi đã lo cho tôi nhất mà!<br>Cho tôi được chữa trước một chút cũng được chứ!<br> ",
    "Hả!? Cô ấy cũng lo cho tôi nữa đấy!<br>Lúc chữa trị vừa rồi‚ mắt chúng tôi cứ chạm nhau suốt cơ mà!?<br> ",
    "Noemi làm gì nhớ đến mấy người!<br>Tôi bị thương nặng hơn bất kỳ ai‚ nên chắc chắn cô ấy chưa quên tôi đâu!<br> ",
    "T‚ tôi lo cho tất cả mọi người mà! Tôi nhớ hết! Không sao đâu～!<br> ",
    "Tôi sẽ chữa theo thứ tự‚ nên xin mọi người bình tĩnh lại～!<br> ",
    "Mày nói gì hả! Bị thương nặng nghĩa là<br>mày đã khiến Noemi vất vả nhất còn gì!<br> ",
    "Hả!? Kẻ chẳng bị thương gì nghiêm trọng<br>mà vẫn bắt Noemi tốn công thì ngậm miệng lại đi!<br> ",
    "Aaa! Đừng đánh nhau‚ xin đừng đánh nhau mà～! Cần chữa bao nhiêu tôi cũng chữa hết～!<br> ",
    "Làm sao đây‚ làm sao đây…! Hỡi Chúa‚ xin hãy cứu rỗi đứa con lạc lối này…<br> ",
    "Mà sao mình lại cầu Chúa vì chuyện thế này chứ!<br>Huhuhu‚ ai đó giúp với～!<br> ",
    "Giọng nói của Noemi không với tới ai khiến cô hoảng hốt.<br>Từ sau lưng cô‚ một giọng nói vang lên.<br> ",
    "――Các cậu đang ầm ĩ chuyện gì thế?<br> ",
    "A… Chỉ Huy!<br> ",
    "Thưa Chỉ Huy! Không‚ cũng không có gì nghiêm trọng đâu ạ…<br> ",
    "Ờ thì‚ chỉ là đang chờ tới lượt ở phòng điều trị nên hơi…<br> ",
    "…Đúng vậy sao‚ Noemi?<br> ",
    "V‚ vâng. Mọi người đều nói là cần điều trị…<br>Dù em có xin họ bình tĩnh lại‚ họ cũng chẳng chịu nghe～!<br> ",
    "Hừm. Trong căn cứ có nhiều người bị thương thế này<br>thì với tư cách Chỉ Huy‚ anh không thể bỏ mặc được nhỉ?<br> ",
    "K‚ không‚ cũng không hẳn là bị thương.<br>Chỉ vì trị liệu của Noemi tuyệt quá nên bọn tôi nhất định muốn được nhận…<br> ",
    "M‚ mà trước hết Chỉ Huy đến đây làm gì vậy!<br>Chẳng lẽ ngài cũng nhắm đến Noemi…!?<br> ",
    "Không không‚ anh chỉ là một bệnh nhân thôi.<br> ",
    "Ơ…!? Chỉ Huy cũng bị thương sao ạ!?<br> ",
    "Không có gì to tát đâu‚ lúc làm giấy tờ anh hơi trượt tay.<br>Chỉ bị giấy cứa vào đầu ngón tay thôi.<br> ",
    "Trời ơi! Em sẽ chữa ngay cho anh!<br> ",
    "Ểể!? Chỉ Huy định chen lượt sao!?<br> ",
    "Không‚ anh không nhất thiết phải nhờ Noemi đâu.<br>Nếu Noemi bận thì anh sẽ tìm người chữa trị khác.<br> ",
    "A… đúng‚ là vậy nhỉ…<br> ",
    "Nhưng nếu được chọn thì anh vẫn muốn nhờ Noemi.<br>Em ấy rất đáng tin cậy‚ và anh tin tưởng em ấy.<br> ",
    "Ơ…!? Chỉ Huy‚ thật… vậy sao ạ?<br> ",
    "Ừ‚ anh vẫn luôn trông cậy vào em đấy‚ Noemi.<br> ",
    "Hì hì… vâng‚ từ nay em cũng sẽ cố gắng～!<br> ",
    "Này này này này! Quả nhiên cả Chỉ Huy cũng nhắm đến Noemi mà!<br> ",
    "Dù ngài là Chỉ Huy thì tôi cũng không thể bỏ qua chuyện này…!<br>Xin hãy tuân thủ quy tắc và xếp ở cuối hàng!<br> ",
    "Ối‚ hình như anh lỡ nói thừa rồi.<br>Chuyện này chắc còn lâu mới lắng xuống.<br> ",
    "Còn ầm ĩ hơn lúc nãy nữa～! Ph‚ phải làm sao đây～!!!<br> ",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_asset(path: Path):
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    bom = data.startswith(b"\xef\xbb\xbf")
    newline = "CRLF" if b"\r\n" in data else "LF"
    lines = text.splitlines(True)
    return data, text, lines, bom, newline


def clean(line: str) -> str:
    return line.lstrip("\ufeff").rstrip("\r\n")


def text_index(cmd: str) -> int:
    return 1 if cmd == "title" else 2


def tags(s: str):
    return TAG_RE.findall(s)


def placeholders(s: str):
    return PLACEHOLDER_RE.findall(s)


def load_pairs(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=list)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    en_data, en_text, en_lines, en_bom, newline = read_asset(EN_ASSET)
    ja_pairs = load_pairs(JA_JSON)
    en_pairs = load_pairs(EN_JSON)

    candidates = []
    new_lines = []
    tr_i = 0
    blockers = []
    qa_items = []
    for line_no, raw in enumerate(en_lines, 1):
        body = clean(raw)
        parts = body.split(",")
        cmd = parts[0] if parts else ""
        ending = "\r\n" if raw.endswith("\r\n") else "\n" if raw.endswith("\n") else ""
        if cmd in TEXT_CMDS:
            idx = text_index(cmd)
            if len(parts) <= idx:
                blockers.append(f"TEXT_FIELD_MISSING_LINE_{line_no}")
                new_lines.append(raw)
                continue
            if tr_i >= len(VI_TRANSLATIONS):
                blockers.append(f"MISSING_TRANSLATION_LINE_{line_no}")
                new_lines.append(raw)
                continue
            old_text = parts[idx]
            vi_text = VI_TRANSLATIONS[tr_i]
            if "," in vi_text:
                blockers.append(f"ASCII_COMMA_IN_TRANSLATION_{tr_i+1}_LINE_{line_no}")
            if tags(old_text) != tags(vi_text):
                blockers.append(f"TAG_MISMATCH_LINE_{line_no}")
            if placeholders(old_text) != placeholders(vi_text):
                blockers.append(f"PLACEHOLDER_MISMATCH_LINE_{line_no}")
            jp = ja_pairs[tr_i][0] if tr_i < len(ja_pairs) else None
            en_ref = en_pairs[tr_i][1] if tr_i < len(en_pairs) else None
            candidates.append({
                "index": tr_i + 1,
                "line": line_no,
                "command": cmd,
                "speaker_or_field1": parts[1] if len(parts) > 1 else "",
                "jp": jp,
                "en_asset": old_text,
                "en_novel": en_ref,
                "vi": vi_text,
                "match_status": "EXACT_OR_ORDERED_CONTEXT",
                "translation_status": "TRANSLATED",
            })
            parts[idx] = vi_text
            new_body = ",".join(parts)
            new_lines.append(new_body + ending)
            tr_i += 1
        else:
            new_lines.append(raw)

    if tr_i != len(VI_TRANSLATIONS):
        blockers.append(f"TRANSLATION_COUNT_MISMATCH_USED_{tr_i}_DEFINED_{len(VI_TRANSLATIONS)}")

    vi_text_full = "".join(new_lines)
    encoding = "utf-8-sig" if en_bom else "utf-8"
    VI_ASSET.write_text(vi_text_full, encoding=encoding, newline="")

    _, _, vi_lines, vi_bom, vi_newline = read_asset(VI_ASSET)
    delimiter_mismatches = []
    field_mismatches = []
    tech_mismatches = []
    kept_text_lines = []
    for line_no, (old_raw, new_raw) in enumerate(zip(en_lines, vi_lines), 1):
        old = clean(old_raw)
        new = clean(new_raw)
        if old.count(",") != new.count(","):
            delimiter_mismatches.append(line_no)
        old_parts = old.split(",")
        new_parts = new.split(",")
        if len(old_parts) != len(new_parts):
            field_mismatches.append(line_no)
            continue
        cmd = old_parts[0] if old_parts else ""
        if cmd in TEXT_CMDS:
            idx = text_index(cmd)
            if old == new:
                kept_text_lines.append(line_no)
            if old_parts[:idx] + old_parts[idx+1:] != new_parts[:idx] + new_parts[idx+1:]:
                tech_mismatches.append(line_no)

    if len(en_lines) != len(vi_lines):
        blockers.append(f"LINE_COUNT_MISMATCH_{len(en_lines)}_{len(vi_lines)}")
    if en_bom != vi_bom:
        blockers.append("BOM_CHANGED")
    if newline != vi_newline:
        blockers.append("NEWLINE_CHANGED")
    if delimiter_mismatches:
        blockers.append(f"DELIMITER_MISMATCH_LINES_{delimiter_mismatches[:10]}")
    if field_mismatches:
        blockers.append(f"FIELD_MISMATCH_LINES_{field_mismatches[:10]}")
    if tech_mismatches:
        blockers.append(f"TECH_MISMATCH_LINES_{tech_mismatches[:10]}")
    if kept_text_lines:
        blockers.append(f"KEPT_TEXT_LINES_{kept_text_lines[:10]}")

    qa_status = "PASS" if not blockers else "FAIL"
    old_focus = [f"{i}:{clean(l)}\n" for i, l in enumerate(en_lines, 1) if clean(l).split(",", 1)[0] in TEXT_CMDS]
    new_focus = [f"{i}:{clean(l)}\n" for i, l in enumerate(vi_lines, 1) if clean(l).split(",", 1)[0] in TEXT_CMDS]
    diff = difflib.unified_diff(old_focus, new_focus, fromfile=str(EN_ASSET), tofile=str(VI_ASSET), lineterm="")
    FOCUSED_DIFF.write_text("\n".join(diff) + "\n", encoding="utf-8")

    manifest = {
        "scene": SCENE,
        "status": qa_status,
        "source_paths": {"ja_json": str(JA_JSON), "en_json": str(EN_JSON), "en_asset": str(EN_ASSET)},
        "output_path": str(VI_ASSET),
        "artifact_paths": {"manifest": str(MANIFEST), "qa_log": str(QA_LOG), "focused_diff": str(FOCUSED_DIFF), "script": str(WORK / "generate_vi.py")},
        "source_sha256": sha256(EN_ASSET),
        "output_sha256": sha256(VI_ASSET),
        "encoding": {"bom": en_bom, "newline": newline},
        "counts": {
            "source_lines": len(en_lines),
            "output_lines": len(vi_lines),
            "novel_ja_pairs": len(ja_pairs),
            "novel_en_pairs": len(en_pairs),
            "candidate_text_records": len(candidates),
            "translations_defined": len(VI_TRANSLATIONS),
            "title": sum(1 for c in candidates if c["command"] == "title"),
            "message": sum(1 for c in candidates if c["command"] == "message"),
            "messageTextUnder": sum(1 for c in candidates if c["command"] == "messageTextUnder"),
            "messageTextCenter": sum(1 for c in candidates if c["command"] == "messageTextCenter"),
        },
        "entries": candidates,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    qa = {
        "scene": SCENE,
        "qa_status": qa_status,
        "blockers": blockers,
        "items": qa_items,
        "structural_qa": {
            "line_count_match": len(en_lines) == len(vi_lines),
            "bom_preserved": en_bom == vi_bom,
            "newline_preserved": newline == vi_newline,
            "delimiter_mismatches": delimiter_mismatches,
            "field_mismatches": field_mismatches,
            "technical_field_mismatches": tech_mismatches,
            "kept_text_lines": kept_text_lines,
        },
        "linguistic_qa": {
            "jp_primary_en_alignment_only": True,
            "commander_rendering": "司令官/Commander -> Chỉ Huy; first-person male Commander uses anh with Noemi in direct dialogue",
            "no_ascii_comma_inside_vi_text_fields": True,
            "title_case_vietnamese_title": True,
            "h18_note": "No H18/adult content in this scene; project adult confirmation acknowledged.",
            "unresolved": [],
        },
    }
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"scene": SCENE, "qa_status": qa_status, "blockers": blockers, "output": str(VI_ASSET), "records": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if qa_status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())

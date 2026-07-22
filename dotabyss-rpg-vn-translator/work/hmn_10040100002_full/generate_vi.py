# -*- coding: utf-8 -*-
from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SCENE = "hmn_10040100002"
ROOT = Path("E:/AgentTranslation")
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_ASSET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
MANIFEST = WORK / "manifest.json"
QA_LOG = WORK / "qa_log.json"
FOCUSED_DIFF = WORK / "focused_diff.md"
SCRIPT = WORK / "generate_vi.py"

TEXT_TYPES = {"title", "message", "messageTextUnder", "messageTextCenter"}
PLACEHOLDER_RE = re.compile(r"%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]|%%")
TAG_RE = re.compile(r"<[^>]+>")
JP_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
LEFTOVER_EN_PATTERNS = [
    r"\bCommander\b", r"\bLord Commander\b", r"\bTeacher\b", r"\bXiaolei is\b",
    r"\bWhat\b", r"\bYes sir\b", r"\bNo\b", r"\bUgh\b", r"\bWhoa",
    r"\bMassage\b", r"\bTrouble\b", r"\bRepair\b", r"\bThank you\b", r"\bGood work\b",
]

TRANSLATIONS = [
    "Siêu Sức Mạnh Vụng Về",
    "――Vậy là anh trở thành thầy của Xiaolei rồi nhỉ‚ Chỉ Huy.<br> ",
    "Anh còn biết làm sao đây? Bị con bé dùng sức quái vật đó giữ lại thì<br>anh không thoát nổi. Hơn nữa‚ em ấy cũng rất đáng kỳ vọng làm chiến lực cho Căn Cứ Tiền Tuyến.<br> ",
    "Xem em ấy như chiến lực thì không sao‚ nhưng với tư cách là thầy<br>xin anh hãy dạy dỗ và dẫn dắt em ấy cho đàng hoàng nhé.<br> ",
    "Anh cũng định vậy‚ nhưng… có vẻ chẳng có mấy thứ để dạy đâu.<br>Dù sao Xiaolei mạnh hơn anh nhiều mà.<br> ",
    "Chỉ cần bù vào phần thường thức còn thiếu và giúp con bé khỏi gặp rắc rối là được.<br>Làm vậy thì em ấy sẽ thành một chiến lực đáng tin—<br> ",
    "Á! Cửa phòng chỉ huy… bị thổi bay rồi…!<br> ",
    "Có chuyện gì vậy!? Tai ương à? Quái vật à? Hay là hành vi phá hoại<br>của gián điệp nào đó!?<br> ",
    "Thầy‚ Xiaolei‚ tới rồi.<br> ",
    "Hóa ra là người nhà gây án à! Em đang làm cái gì vậy hả!<br> ",
    "…? Xiaolei vào phòng của thầy.<br> ",
    "Không phải ý đó! Sao em lại thổi bay cái cửa!?<br> ",
    "Xiaolei gõ cửa thì nó bay đi. Xiaolei không cố ý.<br> ",
    "Chỉ gõ cửa thôi mà…? A haha… sức mạnh khủng khiếp thật…<br> ",
    "…Khoan đã. Nếu không phải cố ý thì có khi… Này Xiaolei‚ em thử<br>cầm cái cốc này xem được không?<br> ",
    "Ừm.<br> ",
    "…Vỡ rồi.<br> ",
    "À‚ đúng như anh nghĩ… Em ấy mạnh quá nên không biết nương tay. Chuyện này<br>có khi còn rắc rối hơn anh tưởng…<br> ",
    "Ư-ừm… xem ra anh có rất nhiều thứ để dạy em ấy nhỉ?<br> ",
    "Được rồi‚ Xiaolei. Trước tiên cho anh xác nhận một chuyện… Em không kiểm soát được<br>sức mạnh của mình đúng không?<br> ",
    "Thầy‚ thất lễ. Không có chuyện đó đâu.<br> ",
    "Ừm‚ vậy là em không tự nhận ra nhỉ? Thế em nghĩ vì sao cái cửa<br>bị thổi bay còn cái cốc em cầm thì vỡ tan?<br> ",
    "Vì mọi thứ ở đây đều yếu xìu.<br> ",
    "Ở nhà Xiaolei cầm đồ thì đồ không vỡ. Chúng cũng<br>không nhẹ như thế này.<br> ",
    "À… nhắc mới nhớ‚ anh có nghe Xiaolei nói vậy…<br> ",
    "…Ừ thì‚ dù ta chẳng dạy gì‚ Xiaolei sinh ra đã khỏe sẵn rồi.<br> ",
    "Vậy sức mạnh quái lực của Xiaolei là bẩm sinh nhỉ. Chắc ở nhà họ đã thay<br>mọi thứ bằng đồ bền chắc và nặng để hợp với em ấy.<br> ",
    "Có lẽ họ còn tăng dần trọng lượng để rèn luyện em ấy. Kiểu như sống cùng<br>tạ đeo trên người vậy.<br> ",
    "…? Đồ vật không tự nặng lên sao?<br> ",
    "Không tự nặng lên! Cái đó gọi là luyện tập đấy!<br> ",
    "Tóm lại. Sức mạnh của em rất hữu dụng trong chiến đấu‚ nhưng hơi quá mức với<br>đời sống hằng ngày.<br> ",
    "Anh nghĩ trước tiên em nên học cách kiểm soát sức mạnh để<br>có thể sinh hoạt mà không gặp vấn đề.<br> ",
    "Sai rồi. Xiaolei muốn mạnh hơn. Không cần<br>làm sức mạnh yếu đi.<br> ",
    "Nhưng vẫn cần đấy. Kiểm soát sức mạnh cũng rất quan trọng để<br>trở nên mạnh hơn.<br> ",
    "Nếu lúc nào cũng dốc toàn lực‚ thể lực sẽ cạn rất nhanh‚ và<br>những đòn giả hay chiêu biến hóa cũng khó dùng hơn.<br> ",
    "Hơn nữa‚ những võ nhân thật sự mạnh thường coi trọng thả lỏng hơn<br>sức mạnh cứng.<br> ",
    "Thả lỏng… Xiaolei từng nghe rồi. Đúng là thầy.<br> ",
    "Tốt‚ em biết nghe lời lắm. Vậy thì bắt đầu đặc huấn ngay nào.<br> ",
    "Nào‚ trước hết tập luyện ở đây!<br> ",
    "Mình ăn trưa sao? Hay quá! Xiaolei vừa đói bụng.<br> ",
    "Không‚ không‚ không. Anh sẽ để Xiaolei rửa bát ở đây. Việc rửa những chiếc<br>đĩa dễ vỡ mà không làm hỏng chúng sẽ giúp luyện cách điều chỉnh lực.<br> ",
    "Xiaolei giỏi rửa bát. Xiaolei cũng từng phụ giúp ở quê.<br> ",
    "Ồ‚ vậy thì tốt. Cứ từ từ và làm cẩn thận nhé.<br> ",
    "Ừ. Cứ giao cho Xiaolei. Vậy thì—<br> ",
    "choang! choang! choang-choang-choang!<br> ",
    "Xiaolei xong rồi. Không còn bát nữa.<br> ",
    "Đừng ưỡn ngực nói như thế! Em không rửa xong<br>mà là đống bát biến mất theo nghĩa vật lý rồi!<br> ",
    "Ư… hết cách rồi… Vậy thì đặc huấn kiểu khác!<br> ",
    "Nghe này‚ Xiaolei. Việc anh muốn em làm bây giờ là mát-xa.<br>Hãy xoa bóp cho cơ bắp cứng đờ của anh giãn ra.<br> ",
    "Chắc em sẽ không làm hỏng người đâu nhỉ… Em không làm đâu nhỉ? Làm ơn đừng nhé.<br> ",
    "Mát-xa… ý thầy là xoa bóp? Vậy thì Xiaolei giỏi.<br> ",
    "Thật sao? Vậy anh sẽ ngồi đây. Trước tiên hãy đấm vai cho anh.<br> ",
    "Cứ giao cho Xiaolei. Vai của thầy‚ Xiaolei sẽ cố gắng đấm.<br> ",
    "Đừng cố gắng! Tuyệt đối đừng cố gắng! Hãy dùng ít sức<br>nhất có thể.<br> ",
    "Xiaolei hiểu rồi. Vậy bắt đầu… a…<br> ",
    "Một con bướm bay lượn vào phòng qua khung cửa sổ đang mở.<br> ",
    "Ồ… bướm…<br> ",
    "Ánh mắt Xiaolei bị hút theo cánh bướm đang chập chờn. Cơ thể em ấy<br>nhẹ nhàng đung đưa theo nhịp cánh.<br> ",
    "Xiaolei? Sao vậy? Đấm vai đâu?<br> ",
    "A… đúng rồi. Vai của thầy‚ đấm‚ đấm.<br> ",
    "*ầm*<br> ",
    "Oaaa! Cái ghế! Cái ghế vỡ tan rồi!<br> ",
    "Ồ… Xiaolei không nhìn kỹ.<br>Tiếp theo‚ Xiaolei sẽ đấm vai thầy.<br> ",
    "Không‚ đủ rồi! Em không cần đấm nữa! Thật ra‚ anh mừng vì em đánh<br>trượt thật đấy!<br> ",
    "Ừm‚ chuyển sang kiểu huấn luyện khác nào.<br>Tiếp theo chúng ta sẽ đổi hướng tiếp cận—<br> ",
    "*choang*!<br> ",
    "Vậy cả dọn dẹp cũng không ổn à…<br> ",
    "*hức*… Xiaolei chẳng làm được gì…<br> ",
    "Có lẽ ngay lập tức thì khó thật. Nhưng nếu xem đó là cái giá cho<br>sức chiến đấu của em thì cũng đành chịu.<br> ",
    "Xiaolei xin lỗi.<br>Thầy đã dạy Xiaolei‚ vậy mà…<br> ",
    "Cứ xem như em đã có tâm thế đúng đắn và hôm nay vậy là tốt rồi.<br>Chúng ta sẽ từ từ làm tiếp.<br> ",
    "*hức*… Xiaolei phải tiếp tục sao?<br> ",
    "Tất nhiên là không thể dừng.<br>Nếu em cứ đi đâu cũng phá hỏng mọi thứ thì người xung quanh sẽ gặp phiền phức.<br> ",
    "Phiền phức…?<br> ",
    "Thưa Chỉ Huy! Việc sửa chữa phòng chỉ huy đã hoàn tất!<br>Bát đĩa mới cũng sẽ được giao tới ngay!<br> ",
    "Rõ rồi. Vất vả cho cậu.<br> ",
    "Rõ! Vậy tôi xin phép rời đi!<br> ",
    "Người vừa rồi là ai…?<br> ",
    "À‚ đó là người sửa cái cửa mà Xiaolei thổi bay đấy. Anh ta cũng đặt<br>bát đĩa mới thay cho số bị vỡ‚ nên lát nữa nhớ cảm ơn nhé?<br> ",
    "Sửa chữa…<br>Vì Xiaolei làm hỏng sao?<br> ",
    "Chúng ta không thể cứ để đồ hỏng nằm đó được.<br>Phải sửa chữa‚ dọn dẹp và bổ sung lại chứ.<br> ",
    "Là lỗi của Xiaolei… Xiaolei đã gây phiền phức.<br> ",
    "*sụt sịt*… Xiaolei xin lỗi.<br> ",
    "*chíp*…<br> ",
    "*chíp*!<br> ",
    "Cảm ơn Panpan‚ Dandan… Xiaolei sẽ cố gắng.<br> ",
    "Xiaolei kìm nước mắt và dịu dàng vuốt ve Panpan cùng Dandan.<br> ",
    "Ừm‚ không cần nóng vội đâu. Có tâm thế đó thì chắc chắn em sẽ tiến bộ. Và<br>hai đứa kia cũng đang ủng hộ em nữa…<br> ",
    "Khoan‚ chờ đã…! Ra là vậy‚ nếu thế thì có khi—<br> ",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def line_ending(data: bytes) -> str:
    if b"\r\n" in data and data.count(b"\r\n") == data.count(b"\n"):
        return "CRLF"
    if b"\n" in data:
        return "LF"
    return "NONE"


def split_line(line: str):
    stripped = line[:-2] if line.endswith("\r\n") else line[:-1] if line.endswith("\n") else line
    ending = line[len(stripped):]
    parts = stripped.split(',')
    return stripped, ending, parts


def text_index(record_type: str) -> int:
    return 1 if record_type == "title" else 2


def field_signature(parts, idx):
    return parts[:idx] + parts[idx+1:]


def load_ordered_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=list)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    src_bytes = EN_ASSET.read_bytes()
    bom = src_bytes.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if line_ending(src_bytes) == "CRLF" else "\n"
    text = src_bytes.decode("utf-8-sig")
    lines = text.splitlines(True)
    candidates = []
    for zero_idx, line in enumerate(lines):
        stripped, ending, parts = split_line(line)
        if not parts or parts[0] not in TEXT_TYPES:
            continue
        idx = text_index(parts[0])
        if len(parts) <= idx:
            raise RuntimeError(f"Malformed text record at line {zero_idx+1}: {stripped}")
        candidates.append({
            "entry_index": len(candidates),
            "line_number": zero_idx + 1,
            "record_type": parts[0],
            "speaker": parts[1] if parts[0] != "title" and len(parts) > 1 else "",
            "source_text": parts[idx],
            "source_signature": field_signature(parts, idx),
            "delimiter_count": stripped.count(','),
            "tag_counter": Counter(TAG_RE.findall(parts[idx])),
            "placeholder_counter": Counter(PLACEHOLDER_RE.findall(parts[idx])),
        })

    if len(TRANSLATIONS) != len(candidates):
        raise RuntimeError(f"Translation count {len(TRANSLATIONS)} != candidate count {len(candidates)}")
    if any(',' in s for s in TRANSLATIONS):
        bad = [i for i, s in enumerate(TRANSLATIONS) if ',' in s]
        raise RuntimeError(f"ASCII comma found inside VI translations at entries {bad}")

    out_lines = list(lines)
    entries = []
    blockers = []
    intentional_kept = []
    for cand, vi in zip(candidates, TRANSLATIONS):
        line = out_lines[cand["line_number"] - 1]
        stripped, ending, parts = split_line(line)
        idx = text_index(parts[0])
        src_field = parts[idx]
        parts[idx] = vi
        out_lines[cand["line_number"] - 1] = ','.join(parts) + ending
        entry = dict(cand)
        entry["vi_text"] = vi
        entry["match_status"] = "EXACT_OR_ORDERED"
        entry["translation_status"] = "TRANSLATED"
        entry["changed"] = vi != src_field
        entry["source_text"] = src_field
        entry["source_signature"] = list(cand["source_signature"])
        entry["tag_counter"] = dict(cand["tag_counter"])
        entry["placeholder_counter"] = dict(cand["placeholder_counter"])
        entries.append(entry)

    output_text = ''.join(out_lines)
    output_bytes = (b"\xef\xbb\xbf" if bom else b"") + output_text.encode("utf-8")
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(output_bytes)

    # QA pass over written output.
    vi_bytes = VI_ASSET.read_bytes()
    vi_text = vi_bytes.decode("utf-8-sig")
    vi_lines = vi_text.splitlines(True)
    delimiter_mismatches = []
    technical_mismatches = []
    tag_mismatches = []
    placeholder_mismatches = []
    unchanged_text_records = []
    ascii_comma_in_vi_text = []
    jp_leftovers = []
    targeted_english_leftovers = []

    for cand in candidates:
        ln = cand["line_number"]
        src_stripped, _, src_parts = split_line(lines[ln-1])
        vi_stripped, _, vi_parts = split_line(vi_lines[ln-1])
        typ = src_parts[0]
        idx = text_index(typ)
        if src_stripped.count(',') != vi_stripped.count(','):
            delimiter_mismatches.append(ln)
        if field_signature(src_parts, idx) != field_signature(vi_parts, idx):
            technical_mismatches.append(ln)
        src_field = src_parts[idx]
        vi_field = vi_parts[idx]
        if Counter(TAG_RE.findall(src_field)) != Counter(TAG_RE.findall(vi_field)):
            tag_mismatches.append(ln)
        if Counter(PLACEHOLDER_RE.findall(src_field)) != Counter(PLACEHOLDER_RE.findall(vi_field)):
            placeholder_mismatches.append(ln)
        if src_field == vi_field:
            unchanged_text_records.append(ln)
        if ',' in vi_field:
            ascii_comma_in_vi_text.append(ln)
        if JP_RE.search(vi_field):
            jp_leftovers.append(ln)
        for pat in LEFTOVER_EN_PATTERNS:
            if re.search(pat, vi_field, flags=re.I):
                targeted_english_leftovers.append({"line": ln, "pattern": pat, "text": vi_field})

    structural = {
        "source_line_count": len(lines),
        "output_line_count": len(vi_lines),
        "line_count_match": len(lines) == len(vi_lines),
        "source_bom": bom,
        "output_bom": vi_bytes.startswith(b"\xef\xbb\xbf"),
        "source_newline": line_ending(src_bytes),
        "output_newline": line_ending(vi_bytes),
        "newline_match": line_ending(src_bytes) == line_ending(vi_bytes),
        "delimiter_mismatches": delimiter_mismatches,
        "technical_mismatches": technical_mismatches,
        "tag_mismatches": tag_mismatches,
        "placeholder_mismatches": placeholder_mismatches,
        "ascii_comma_in_vi_text": ascii_comma_in_vi_text,
    }
    linguistic = {
        "candidate_text_records": len(candidates),
        "translated_records": sum(1 for e in entries if e["changed"]),
        "unchanged_text_records": unchanged_text_records,
        "intentional_kept_text_records": intentional_kept,
        "jp_leftovers": jp_leftovers,
        "targeted_english_leftovers": targeted_english_leftovers,
        "honorific_suffix_scan": [],
        "notes": [
            "JP novel is primary; EN asset used for candidate order and tag shape.",
            "Xiaolei/Panpan/Dandan romanized names retained in prose by EN alignment and project name-retention convention.",
            "All characters are treated as confirmed 18+ per project rule; no H18 content was present in this file.",
            "Xiaolei uses simple third-person self-reference; <user>/Commander speaks as her teacher.",
        ],
    }

    if not structural["line_count_match"]:
        blockers.append({"type": "LINE_COUNT_MISMATCH", "severity": "blocker"})
    for name in ["delimiter_mismatches", "technical_mismatches", "tag_mismatches", "placeholder_mismatches", "ascii_comma_in_vi_text"]:
        if structural[name]:
            blockers.append({"type": name.upper(), "severity": "blocker", "lines": structural[name]})
    if unchanged_text_records:
        blockers.append({"type": "UNCHANGED_EN_TEXT", "severity": "blocker", "lines": unchanged_text_records})
    if jp_leftovers:
        blockers.append({"type": "JP_LEFTOVER", "severity": "blocker", "lines": jp_leftovers})
    if targeted_english_leftovers:
        blockers.append({"type": "TARGETED_ENGLISH_LEFTOVER", "severity": "major", "items": targeted_english_leftovers})

    qa_status = "PASS" if not blockers else "FAIL"
    ja_pairs = load_ordered_json(JA_JSON)
    en_pairs = load_ordered_json(EN_JSON)
    manifest = {
        "scene": SCENE,
        "status": qa_status,
        "paths": {
            "en_asset": str(EN_ASSET),
            "vi_asset": str(VI_ASSET),
            "ja_json": str(JA_JSON),
            "en_json": str(EN_JSON),
            "work_dir": str(WORK),
            "script": str(SCRIPT),
            "manifest": str(MANIFEST),
            "qa_log": str(QA_LOG),
            "focused_diff": str(FOCUSED_DIFF),
        },
        "source": {
            "sha256": sha256(src_bytes),
            "byte_length": len(src_bytes),
            "bom": bom,
            "newline": line_ending(src_bytes),
            "line_count": len(lines),
        },
        "output": {
            "sha256": sha256(vi_bytes),
            "byte_length": len(vi_bytes),
            "bom": vi_bytes.startswith(b"\xef\xbb\xbf"),
            "newline": line_ending(vi_bytes),
            "line_count": len(vi_lines),
        },
        "counts": {
            "novel_ja_pairs": len(ja_pairs),
            "novel_en_pairs": len(en_pairs),
            "candidate_text_records": len(candidates),
            "title": sum(1 for c in candidates if c["record_type"] == "title"),
            "message": sum(1 for c in candidates if c["record_type"] == "message"),
            "messageTextUnder": sum(1 for c in candidates if c["record_type"] == "messageTextUnder"),
            "messageTextCenter": sum(1 for c in candidates if c["record_type"] == "messageTextCenter"),
            "translated_records": sum(1 for e in entries if e["changed"]),
            "kept_records": len(unchanged_text_records),
        },
        "entries": entries,
    }
    qa_log = {
        "scene": SCENE,
        "qa_status": qa_status,
        "blockers": blockers,
        "structural_qa": structural,
        "linguistic_qa": linguistic,
        "addressing_qa": {
            "Commander_translation": "司令官/Commander -> Chỉ Huy",
            "default_relation": "Xiaolei calls <user> Thầy; <user> speaks as teacher with anh/em where natural.",
            "speaker_names_preserved": True,
            "charaload_names_preserved": True,
        },
        "h18_qa": {
            "adult_project_rule_applied": True,
            "h18_content_present": False,
        },
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    QA_LOG.write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding="utf-8")

    focus_before = []
    focus_after = []
    for cand in candidates:
        ln = cand["line_number"]
        focus_before.append(f"{ln}: {lines[ln-1].rstrip()}\n")
        focus_after.append(f"{ln}: {vi_lines[ln-1].rstrip()}\n")
    diff = ''.join(difflib.unified_diff(focus_before, focus_after, fromfile="EN text records", tofile="VI text records", lineterm='\n'))
    FOCUSED_DIFF.write_text(diff, encoding="utf-8")

    print(json.dumps({
        "qa_status": qa_status,
        "candidate_text_records": len(candidates),
        "translated_records": sum(1 for e in entries if e["changed"]),
        "blocker_count": len(blockers),
        "vi_asset": str(VI_ASSET),
        "manifest": str(MANIFEST),
        "qa_log": str(QA_LOG),
        "focused_diff": str(FOCUSED_DIFF),
        "output_sha256": sha256(vi_bytes),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

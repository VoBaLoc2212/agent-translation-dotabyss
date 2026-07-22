from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SCENE = "hmn_10140100003"
ROOT = Path("E:/AgentTranslation")
SRC = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work" / f"{SCENE}_full"
JA = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "ja.json"
ENJ = ROOT / "dotabyss-translation-main/translations/novels" / SCENE / "en.json"

TRANSLATIONS = [
    "Ở Dị Giới Không Có Smartphone",
    "Này‚ tiếp theo mình đi đâu vậy?<br> ",
    "Ra chợ anh sẽ mua cho em thứ em thích. Thấy món nào có vẻ làm em<br>vui lên thì cứ chọn.<br> ",
    "Thật hả? Không biết có game không nhỉ?<br> ",
    "Được‚ để anh hỏi thử. Chủ tiệm‚ game được để ở khu nào?<br> ",
    "Đều gom lại ở đằng kia đấy ạ.<br> ",
    "Aaa‚ quả nhiên không có video game rồi. Chán ghê.<br> ",
    "Không có thứ em muốn à…? Có game nào em biết không?<br> ",
    "À‚ bài Tây kìa.<br> ",
    "Bài Tây… kiểu trò chơi bài nhỉ.<br> ",
    "Tuy là game analog nhưng dù sao game vẫn là game mà.<br> ",
    "Cứ mua thử đã. Chủ tiệm‚ cho tôi lấy bộ này.<br> ",
    "Cảm ơn ạ.<br> ",
    "Pico‚ ngoài game ra em còn tìm thứ gì nữa không?<br> ",
    "Có PC gaming không? Với cả tai nghe Bluetooth cao cấp kết nối được với điện thoại!<br> ",
    "…Đó là bùa chú gì vậy ạ?<br> ",
    "Không biết nữa…<br> ",
    "Uaaaah! Mình muốn về thế giới cũ quá đi!<br> ",
    "Ừm… Tạm thời chuyển chỗ đã nhỉ…<br> ",
    "Đây là đâu vậy?<br> ",
    "Phòng chỉ huy.<br> ",
    "Cái đó mình biết rồi. Đột nhiên kéo mình vào đây<br>là định làm gì?<br> ",
    "Đừng nói kỳ quặc thế. Anh chỉ định cùng em chơi bộ bài vừa mua thôi.<br>Em thích game mà‚ đúng không?<br> ",
    "Chơi được nhiều trò lắm nhưng chỉ có hai người thôi… Muốn thử<br>Speed không? Hoặc Memory‚ Sevens gì đó?<br> ",
    "Trò nào anh cũng chơi cùng được.<br> ",
    "Ủa? Trông anh có vẻ tự tin ghê?<br> ",
    "Không nhanh trí thì không làm Chỉ Huy được đâu.<br> ",
    "…Tự nhiên mình hơi sợ rồi đó. Đây không phải bài cởi đồ đúng không?<br> ",
    "Không phải!<br> ",
    "Lỡ thật ra thua cược lớn là bị đưa xuống cơ sở lao động ngầm thì<br>mình chịu không nổi đâu nha!?<br> ",
    "Cũng không có chuyện đó. Đây là trò chơi lành mạnh nên yên tâm đi.<br> ",
    "Vậy thì ổn! Nào‚ bắt đầu game thôi!<br> ",
    "L-lại thua nữa… sáu trận liên tiếp?<br> ",
    "Ưư‚ mình bị gamer analog dị giới săn gà rồi…<br>Chắc chắn là lừa người mới mà… tụt mood quá…<br> ",
    "Em nói mình thích game nên anh nghĩ nương tay thì thất lễ… Xin lỗi vì<br>đã bắt em chơi thứ em không giỏi. Tha cho anh nhé.<br> ",
    "Cái này là game rác‚ rác thật luôn. Mình không bao giờ chơi bài với Chỉ Huy nữa.<br> ",
    "…Trước lần sau phải xem lại mẫu hình và thứ tự ưu tiên mới được.<br> ",
    "Vừa nói không bao giờ chơi nữa mà em hăng hái ghê nhỉ…<br> ",
    "Mình là gamer cày cuốc mà! Quen tay rồi mới là lúc vào trận thật!<br> ",
    "Ưư‚ nhưng không có cách tra chiến thuật bài Tây… Mình muốn lên mạng quá…<br> ",
    "(Anh tưởng nó sẽ giúp em đổi gió‚ nhưng chơi game từ thế giới cũ<br>lại chỉ khiến em nhớ bên đó hơn sao…)<br> ",
    "Vậy Chỉ Huy ơi‚ mình qua chỗ Adelheid chưa? Chắc điện thoại<br>sạc xong rồi đó.<br> ",
    "…Không‚ anh vẫn còn một nơi muốn đi. Dọn xong rồi<br>ra ngoài nào.<br> ",
    "Cửa mở đánh cạch!<br> ",
    "Chỉ Huy! Quán Rượu và Chợ gửi hóa đơn khổng lồ tới rồi đây!<br>Xin hãy giải thích chuyện này là sao!<br> ",
    "Chết rồi! Pico‚ trốn qua cửa sổ thôi!<br> ",
    "Phù… bằng cách nào đó cũng cắt đuôi được Alicia rồi. Thế nào?<br>Chỗ này ấy.<br> ",
    "Có gì đâu?<br> ",
    "Đó chính là điểm hay của nơi này. Khi không muốn nghĩ gì hoặc chán ngấy<br>công việc‚ anh đến đây nằm dài ngắm trời.<br> ",
    "Hừm… chỗ nghỉ của Chỉ Huy à.<br> ",
    "Cảnh đẹp đúng không? Thỉnh thoảng thong thả ở nơi như thế này cũng đâu tệ nhỉ?<br> ",
    "Muốn thong thả thì ở trong phòng vẫn hơn. Mình ghét gần cỏ<br>vì sẽ có côn trùng bay tới.<br> ",
    "Vậy không thong thả nữa‚ thử vận động chút nhé?<br> ",
    "Trông mình giống kiểu giải tỏa stress bằng vận động à?<br> ",
    "…Không giống.<br> ",
    "Mà nói vậy chứ Chỉ Huy cũng đâu có vẻ giỏi<br>vận động.<br> ",
    "…Đúng vậy thật. Anh lúc nào cũng chỉ nằm ườn ở đây thôi.<br> ",
    "Tự hủy luôn kìa!<br> ",
    "Ừm… nơi này cũng không thành chỗ giúp em vui được à.<br> ",
    "Sau khi Pico bình tĩnh lại‚ cả hai trở về trong Căn Cứ Tiền Tuyến.<br>Bước chân họ nặng nề‚ lê đi một cách uể oải.<br> ",
    "…Pico‚ em ổn không?<br> ",
    "…Không hẳn. Mệt rồi.<br> ",
    "Vậy à…<br> ",
    "(Anh đã thử đủ cách‚ nhưng rốt cuộc vẫn chẳng giúp được em ấy…)<br> ",
    "A…!<br>Aaaaa!<br> ",
    "Sao vậy?<br> ",
    "Mèo con kìa!<br>Nhìn đi‚ đằng kia! Đằng kia đó!<br> ",
    "Mèo…?<br> ",
    "Meo?<br> ",
    "Nó có lại đây không? Có lại không?<br>Chíp chíp chíp…<br> ",
    "Con mèo chậm rãi tiến lại gần Pico.<br> ",
    "Hoaaa! Nó thân người quá!<br>Dễ thương ghê!<br> ",
    "Hình như có ai đó trong căn cứ vẫn cho con mèo này ăn.<br> ",
    "Thật á!? Mình cũng muốn làm! Muốn chơi với mèo méo meo!<br> ",
    "…Mai anh giới thiệu cho.<br> ",
    "Hoan hô!<br>Vui quá đi.<br> ",
    "Em thích mèo à?<br> ",
    "Ừ! Đến cả trang phục và kiểu tóc của mình cũng lấy chủ đề mèo mà.<br>Nếu được chơi với mèo thì ở thế giới này mình cũng sống nổi đó. Meo?<br> ",
    "Meo.<br> ",
    "Meo! Hì hì hì.<br> ",
    "(Pico đang cười! May quá…)<br> ",
    "(…Nhưng mà)<br> ",
    "(Mới vừa nãy em ấy còn than thở nhiều như thế‚ vậy mà chỉ gặp mèo thôi sao…?<br>R-rốt cuộc những việc anh làm hôm nay là gì đây…!?)<br> ",
    "…Này‚ Chỉ Huy. Nhờ mèo con mà mình khỏe lên rồi nên mình sẽ nói<br>vào lúc này nhé—<br> ",
    "Cảm ơn anh vì cả ngày hôm nay.<br> ",
    "Không có gì. Dù anh cũng chẳng giúp được bao nhiêu.<br> ",
    "Hả? Không phải vậy đâu. Anh dẫn mình đi khắp nơi‚ mình thật sự vui lắm.<br>Với cả chạy trốn Alicia-tan cũng vui nữa.<br> ",
    "Ở một mình thì hình như mình lại nghĩ đủ thứ rồi tụt mood. Mình nhận ra điều đó<br>cũng là nhờ Chỉ Huy kéo mình đi vòng vòng đó.<br> ",
    "Khi còn ở thế giới cũ‚ dù một mình trong phòng thì vẫn có mọi người kết nối<br>qua mạng nên mình không thấy cô đơn. Nhưng ở đây thì khác.<br> ",
    "Vậy nên trong lúc ở thế giới này‚ mình sẽ thử tận hưởng thời gian bên<br>người khác.<br> ",
    "Vậy à. Nếu em có thể nghĩ tích cực như thế thì anh cũng yên tâm.<br>Công dẫn em ra ngoài không uổng rồi.<br> ",
    "Dù sự thay đổi kịch tính của Pico vẫn khiến anh phải ngạc nhiên.<br> ",
    "Ê hê hê. Mình bắt đầu nghĩ thế giới này cũng không tệ lắm rồi.<br> ",
    "Có lẽ mình đã tìm thấy điểm hay của thế giới này.<br> ",
    "Chịu em thật. Tất cả là nhờ mèo nhỉ.<br> ",
    "Không không. Không phải mèo đâu. Ở thế giới cũ bên kia cũng có mèo mà.<br>Dù không gặp con mèo đó‚ mình chắc chắn vẫn sẽ cảm ơn Chỉ Huy.<br> ",
    "Cách em nói thì đó là thứ chỉ có ở thế giới này à?<br> ",
    "Ừm!<br> ",
    "…Hôm nay anh có giới thiệu thứ như vậy sao?<br> ",
    "(Hừm… là Chỉ Huy mà không ngờ lại chậm hiểu ghê.)<br> ",
    "(Có vẻ anh ấy lo cho mình‚ từ giờ mình sẽ dựa dẫm thật nhiều<br>luôn♪)<br> ",
    "Em cười tủm tỉm gì thế?<br> ",
    "Hổng có gì! Đi lấy smartphone từ Adelheid về thôi! Sau đó<br>lại giúp mình quay phim nhé!<br> ",
    "Rồi rồi. Đừng kéo anh.<br> ",
]

TEXT_CMDS = {"title", "message", "messageTextUnder", "messageTextCenter"}
TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"%(?:%|[sd])|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def newline_style(raw: bytes) -> str:
    if b"\r\n" in raw:
        return "CRLF"
    if b"\n" in raw:
        return "LF"
    return "none"


def split_line(line: str):
    end = ""
    if line.endswith("\r\n"):
        line, end = line[:-2], "\r\n"
    elif line.endswith("\n"):
        line, end = line[:-1], "\n"
    return line, end


def text_index(fields):
    return 1 if fields[0] in {"title", "messageTextUnder", "messageTextCenter"} else 2


def tag_counts(s: str):
    return Counter(TAG_RE.findall(s))


def placeholder_counts(s: str):
    return Counter(PLACEHOLDER_RE.findall(s))


def ascii_commas_in_text(s: str) -> bool:
    return "," in s


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = SRC.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    text_records = []
    for idx, line in enumerate(lines):
        core, end = split_line(line)
        fields = core.split(",")
        if fields and fields[0] in TEXT_CMDS:
            text_records.append((idx, fields[0], fields, end))
    if len(text_records) != len(TRANSLATIONS):
        raise SystemExit(f"translation count mismatch: {len(TRANSLATIONS)} vs records {len(text_records)}")

    errors = []
    out_lines = list(lines)
    mapping = []
    for n, (idx, cmd, fields, end) in enumerate(text_records):
        ti = text_index(fields)
        old_text = fields[ti]
        new_text = TRANSLATIONS[n]
        if ascii_commas_in_text(new_text):
            errors.append({"record": n + 1, "line": idx + 1, "error": "ASCII comma in VI text"})
        if tag_counts(old_text) != tag_counts(new_text):
            errors.append({"record": n + 1, "line": idx + 1, "error": "tag mismatch", "src": dict(tag_counts(old_text)), "vi": dict(tag_counts(new_text))})
        if placeholder_counts(old_text) != placeholder_counts(new_text):
            errors.append({"record": n + 1, "line": idx + 1, "error": "placeholder mismatch"})
        old_delims = out_lines[idx].count(",")
        fields[ti] = new_text
        new_core = ",".join(fields)
        out_lines[idx] = new_core + end
        if out_lines[idx].count(",") != old_delims:
            errors.append({"record": n + 1, "line": idx + 1, "error": "delimiter count changed", "old": old_delims, "new": out_lines[idx].count(",")})
        mapping.append({"record_index": n + 1, "line": idx + 1, "command": cmd, "status": "TRANSLATED", "source_text": old_text, "vi_text": new_text})

    output_text = "".join(out_lines)
    OUT.write_bytes((b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b"") + output_text.encode("utf-8"))

    out_raw = OUT.read_bytes()
    out_dec = out_raw.decode("utf-8-sig")
    out_lines_verify = out_dec.splitlines(keepends=True)
    src_cores = [split_line(l)[0] for l in lines]
    out_cores = [split_line(l)[0] for l in out_lines_verify]
    structural = {
        "line_count_match": len(lines) == len(out_lines_verify),
        "bom_preserved": raw.startswith(b"\xef\xbb\xbf") == out_raw.startswith(b"\xef\xbb\xbf"),
        "newline_preserved": newline_style(raw) == newline_style(out_raw),
        "delimiter_counts_match": [s.count(",") for s in src_cores] == [o.count(",") for o in out_cores],
        "text_record_count": len(text_records),
        "command_counts": dict(Counter(cmd for _, cmd, _, _ in text_records)),
    }
    qa_status = "PASS" if not errors and all(v for k, v in structural.items() if isinstance(v, bool)) else "FAIL"

    manifest = {
        "scene": SCENE,
        "status": qa_status,
        "source_paths": {"asset_en": str(SRC), "novel_ja": str(JA), "novel_en": str(ENJ)},
        "output_path": str(OUT),
        "work_dir": str(WORK),
        "encoding": "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8",
        "newline": newline_style(raw),
        "source_sha256": sha256(SRC),
        "output_sha256": sha256(OUT),
        "line_count": len(lines),
        "text_record_count": len(text_records),
        "text_command_counts": structural["command_counts"],
        "mapping_summary": {"TRANSLATED": len(mapping), "UNMATCHED": 0, "AMBIGUOUS": 0, "REVIEW": 0},
        "qa_status": qa_status,
        "structural_qa": structural,
        "errors": errors,
        "notes": [
            "JP novel used as primary source; EN asset used for alignment and authoritative technical structure.",
            "Speaker names and charaload asset names preserved as source.",
            "Pico localized with casual gamer tone; Commander/司令官 rendered as Chỉ Huy in Vietnamese text.",
        ],
    }
    qa_log = {
        "scene": SCENE,
        "qa_status": qa_status,
        "structural_qa": structural,
        "linguistic_qa": {
            "jp_primary_en_alignment_only": True,
            "commander_term": "Chỉ Huy",
            "title_case_vi": True,
            "ascii_comma_policy": "No ASCII comma added inside Vietnamese text fields; U+201A used where a comma pause was needed.",
            "h18": "No explicit H18 content in this scene; project adult confirmation noted.",
            "unresolved_items": [],
        },
        "text_records": len(text_records),
        "mapping": mapping,
        "errors": errors,
    }
    (WORK / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK / "qa_log.json").write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding="utf-8")

    diff = difflib.unified_diff(
        text.splitlines(),
        out_dec.splitlines(),
        fromfile=str(SRC),
        tofile=str(OUT),
        lineterm="",
    )
    (WORK / "focused_diff.md").write_text("```diff\n" + "\n".join(diff) + "\n```\n", encoding="utf-8")
    print(json.dumps({"status": qa_status, "records": len(text_records), "errors": errors, "output": str(OUT), "work": str(WORK)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

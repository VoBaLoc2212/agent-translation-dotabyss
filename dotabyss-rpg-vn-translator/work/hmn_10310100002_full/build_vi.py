#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Field-index VI builder for hmn_10310100002 (EN-asset-is-English case).

Reads the EN asset (structural authority), swaps ONLY the text field
(parts[2] for message*, parts[1] for title) with the ordered VI translations,
mirrors the source trailing tag suffix ("<br> "), and preserves BOM/CRLF/
delimiter/field/tag/placeholder structure. Internal commas use U+201A '‚'.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10310100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# Trailing run of tag+optional-space, e.g. "<br> " or "</size>" or "<br> <br> ".
# NOTE: must include the closing '>' inside the char class so the whole tag is
# consumed. The skill's documented r"(?:<[^>]+\s*)+$" stops BEFORE '>' and
# matches nothing, dropping every trailing "<br> " suffix.
TAGSUF_RE = re.compile(r"(?:<[^>]*>\s*)+$")

# Ordered VI text fields, 1:1 with source text records in file order.
# (title first, then each message in order). INTERNAL <br> placed where source had
# them. Do NOT end with <br>; the suffix is mirrored automatically.
TRANSLATIONS = [
    # 0 - title
    "Theo Dấu Vết",
    # 1 - message <user> (internal <br>)
    "Theo lời Kotono‚ đám sói tấn công có vẻ ở quanh đây……<br>Như anh nghĩ‚ khắp nơi đều có dấu hiệu của quái vật và thú hoang.",
    # 2
    "Hatsune‚ em có tìm ra vị trí lũ quái vật được không?",
    # 3 - ハツネ
    "Tất nhiên. Chẳng mấy kẻ có thể qua mắt được đôi mắt và mũi của em đâu.",
    # 4 - <user>
    "Tốt. Dẫn đường đi em.",
    # 5 - ハツネ
    "Ừ! Cứ giao cho em!",
    # 6 - ハツネ  (EN internal <br> after "Coi chừng bước chân")
    "—Lối này. Coi chừng bước chân—dưới chân có rễ cây đấy.<br>Đi sát lại và theo em nhé.",
    # 7 - <user>
    "Rõ rồi.",
    # 8 - <user>  (EN internal <br> after "không cần ánh sáng")
    "Nhưng anh mừng vì em ở đây. Một mình thì anh chẳng thể đi qua khu rừng ban đêm mà không cần ánh sáng.<br>Nhờ vậy mà kỹ năng của lính đã tiến bộ.",
    # 11 - ハツネ
    "Em hy vọng vậy.—Ừm. Mùi này...",
    # 12 - ハツネ
    "Hít hít... Hít hít...",
    # 13 - ハツネ
    "...Chắc chắn luôn! Đây là mùi của Thiếu Chủ!",
    # 14 - <user>
    "Đúng là khứu giác của Thú Nhân có khác. Em có đuổi theo mùi đó được không?",
    # 15 - ハツネ
    "Tất nhiên! Mùi kéo dài về phía này...",
    # 16 - <user>
    "Này‚ đợi một chút đã!",
    # 17 - ハツネ
    "Hả! Đừng có cản đường em!",
    # 18 - <user>
    "Em đang bị tầm nhìn hẹp rồi đấy. Nhìn cái cây bên phải kìa.",
    # 19 - ハツネ
    "Hả? Cái cây thì sao? Anh đang nói cái gì vậy?",
    # 20 - ハツネ
    "...! Những vết móng này...",
    # 21 - <user>
    "Đây là vết móng của một loài thú ăn thịt lớn. Nó hẳn đã chiếm giữ khu vực này làm lãnh thổ.",
    # 22 - <user> (internal <br>)
    "Anh hiểu em muốn nhanh lên‚ nhưng hãy đi vòng cẩn thận đã.<br>Nếu chọc giận con thú‚ tìm người mất tích sẽ chẳng là gì so với chuyện khác.",
    # 23 - ハツネ
    "...Ừ‚ anh nói đúng. Chúng ta sẽ vòng qua bên trái.",
    # 24 - <user>
    "Tốt. Lúc cần em cũng biết nghe lời nhỉ.",
    # 25 - ハツネ
    "(Anh chàng này... không chỉ nói suông. Anh ấy bình tĩnh và có kiến thức đấy.)",
    # 26 - ハツネ
    "(Nghĩ lại thì‚ Kotono gọi anh ta là 'Chủ nhân'... Lẽ nào Kotono thật sự chọn anh chàng này làm Chủ nhân mới của mình?)",
    # 27 - ハツネ
    "(Anh chàng này... rốt cuộc là ai vậy?)",
    # 28 - ハツネ
    "Đây là...!",
    # 29 - <user>
    "Em tìm thấy gì à? ...Hử? Có thứ gì cắm dưới đất kìa. Đó là đoản đao phải không?",
    # 30 - ハツネ
    "Đoản đao này... Lãnh Chúa đã trao cho Thiếu Chủ như vật chứng kế vị! Ngài ấy luôn mang theo bên mình.",
    # 31 - <user> (internal <br>)
    "Xét theo độ dài‚ nó chỉ hợp để tự vệ thôi.<br>Trong chiến đấu thực sự‚ anh chỉ dùng khi mất đi katana.",
    # 32 - <user>
    "Vậy là... Thiếu Chủ tuyệt vọng đến mức phải dùng đến phương sách cuối cùng.",
    # 33 - ハツネ
    "*thở dốc*... Máu trên mặt đất! Quá nhiều...",
    # 34 - <user>
    "Cỏ xung quanh đây cũng bị giẫm đạp nát. Có vẻ họ đã giao chiến với quái vật ở chỗ này.",
    # 35 - <user>
    "Không ở gần đây nữa... hình như Thiếu Chủ đã đi rồi.",
    # 36 - <user> (internal <br>)
    "(Thiếu Chủ trốn thoát trong lúc chiến đấu‚ hay bị đánh bại rồi bị lôi về hang ổ?<br>...Không‚ khoan đã. Xét theo thói quen của lũ sói ở đây...)",
    # 37 - ハツネ
    "Không... Thiếu Chủ... đáng lẽ em phải bảo vệ ngài mà!",
    # 38 - ハツネ
    "Thiếu Chủ... Thiếu Chủ...",
    # 39 - <user>
    "Bình tĩnh. Vẫn chưa chắc ngài ấy đã chết.",
    # 40 - ハツネ (internal <br>)
    "Đừng nói mấy lời an ủi vô ích đó. Với lượng máu thế này thì không thể nào ngài ấy còn sống‚ và cũng chẳng có thi thể...<br>Thiếu Chủ đã bị quái vật ăn thịt mất rồi!",
    # 41 - <user>
    "Như anh bảo‚ bình tĩnh đi. Nhìn này—trong vũng máu có lông thú.",
    # 42 - ハツネ
    "Hử...?",
    # 43 - <user> (internal <br>)
    "Nghĩa là Thiếu Chủ của em đã giao chiến với quái vật và làm nó bị thương.<br>Nếu vậy‚ không phải toàn bộ máu này đều là của ngài ấy.",
    # 44 - <user> (internal <br>)
    "Hơn nữa‚ lũ quái vật dạng sói không mang con mồi về hang ổ.<br>Và ở đây cũng chẳng có thi thể của Thiếu Chủ.",
    # 45 - <user>
    "Nói tóm lại‚ khả năng ngài ấy vẫn còn sống là rất cao.",
    # 46 - ハツネ
    "T...thật sao...? Thiếu Chủ... có an toàn không...?",
    # 47 - <user> (internal <br>)
    "Có lẽ vậy. Nhưng ngài ấy vẫn đang gặp nguy hiểm. Nếu em bỏ cuộc‚ thì ngay cả những gì còn kịp làm cũng sẽ trở nên quá muộn.<br>Em hiểu chứ?",
    # 48 - ハツネ
    "...Ừ.",
    # 49 - <user> (internal <br>)
    "Vậy thì không có thời gian để khóc đâu. Chúng ta sẽ tiến lên.<br>Chỉ có mình em mới có thể cứu được Thiếu Chủ.",
    # 50 - ハツネ
    "...Được rồi! Mùi của Thiếu Chủ... lối này! Nó kéo về hướng này!",
    # 51 - <user>
    "Được! Lên nào‚ Hatsune!",
    # 52 - ハツネ
    "...Kìa! Trên cái cây đó! Chính là Thiếu Chủ! Ngài ấy ở trên đó!",
    # 53 - <user> (internal <br>)
    "Chắc ngài ấy nhận ra không thể chạy trốn nên đã trèo lên cây. Quyết định sáng suốt.<br>Nhưng...",
    # 54 - 狼
    "*gừ gừ...*",
    # 55 - <user>
    "Con sói đang lảng vảng dưới gốc cây... chờ con mồi kiệt sức.",
    # 56 - ホウライの青年
    "*thở dốc*‚ *thở dốc*‚ *thở dốc*",
    # 57 - ハツネ
    "Thiếu Chủ‚ mặt ngài tái nhợt như ma...!",
    # 58 - <user> (internal <br>)
    "Ngài ấy đã mất rất nhiều máu. Hẳn đang chật vật giữ lấy ý thức.<br>...Không ổn rồi. Nếu ngài ấy rơi từ đó xuống‚ coi như xong đời.",
    # 59 - ハツネ
    "Thiếu Chủ! Em đến cứu ngài đây!",
    # 60 - <user> (internal <br>)
    "Khoan đã! Con quái đó từng làm Kotono chật vật! Không phải là loại kẻ thù mà<br>em có thể xông tới đánh bừa được đâu!",
    # 61 - ハツネ (internal <br>)
    "Vậy thì em làm mồi nhử! Anh đưa Thiếu Chủ về căn cứ trong lúc<br>em đánh lạc hướng con đó!",
    # 62 - <user>
    "Đừng có ngốc. Em nghĩ Thiếu Chủ của em sẽ vui sao nếu biết em hy sinh bản thân?",
    # 63 - ハツネ
    "Nhưng...!",
    # 64 - ハツネ
    "Ư...! Thế em phải làm sao đây?!",
    # 65 - <user>
    "Anh có một kế hoạch. Nếu thuận lợi‚ tất cả sẽ trở về an toàn được.",
    # 66 - ハツネ
    "Thật sao? Nói anh nghe! Em phải làm gì?!",
    # 67 - <user>
    "Anh cần em đảm nhận một vai trò hơi nguy hiểm. Em sẽ giúp anh chứ?",
    # 68 - ハツネ
    "Tất nhiên! Nếu có thể giúp Thiếu Chủ‚ em sẽ làm bất cứ điều gì!",
    # 69 - <user>
    "Đúng tinh thần đó! Thế thì‚ Hatsune‚ trước tiên em—",
]


def main() -> None:
    data = EN.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    vi_lines: list[str] = []
    idx = 0
    record_count = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            record_count += 1
            assert idx < len(TRANSLATIONS), f"Ran out of translations at record {record_count}"
            vi_text = TRANSLATIONS[idx]
            idx += 1
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text  # title has no trailing tag suffix in this project
            else:
                parts = ln.split(",", 5)
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                parts[2] = vi_text + suffix
            assert "," not in vi_text, f"ASCII comma in VI text (record {record_count}); use U+201A '‚'"
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    assert idx == len(TRANSLATIONS), f"translations not fully used: {idx}/{len(TRANSLATIONS)}"
    assert record_count == len(TRANSLATIONS), f"record count {record_count} != {len(TRANSLATIONS)}"

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()

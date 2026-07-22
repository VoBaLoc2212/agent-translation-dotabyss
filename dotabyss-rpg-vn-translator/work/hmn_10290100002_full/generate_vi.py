#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate VI asset for hmn_10290100002 (EN-asset-is-English case).

Strategy: the EN asset text fields are already English; the JP `ja.json` is
the meaning source. We translate JP->VI, replacing the English text field of
each text-command line (title/message/messageTextCenter) while preserving every
structural byte: BOM, CRLF, field delimiters, tags, placeholders, speaker
labels, voice keys, chara keys, and the exact `<br>` count per field.

Comma rule: inside Vietnamese text fields use U+201A (‚) instead of ASCII ','.
Commander / 司令官 -> Chị Huy. Characters kept as in shipped VI convention.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100002.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100002.txt"

# line_no (1-indexed in the asset file) -> VI text field (with trailing <br> where present)
VI_TEXT = {
    17: "Với Tư Cách Là Thợ Làm Bánh Của Vương Quốc Đồ Ngọt",
    27: "<size=48>—Vài Ngày Sau.</size>",
    47: "Đã muộn thế này rồi sao... Anh làm hơi quá sức một chút hôm nay.<br> ",
    58: "...Hm? Cái mùi thơm ngọt ngào‚ thoảng qua gì thế?<br> ",
    60: "...Để anh đi xem thử sao.<br> ",
    94: "Ưaaa‚ em phải làm sao đây...?<br> ",
    109: "(Myrtille‚ hả? Nướng bánh muộn thế này...)<br> ",
    139: "Cái bánh tart này thì quá đơn giản‚ nhưng cái kia thì rối tung cả lên... Ư‚ biết đâu<br>em cứ xếp chồng cả hai lại thành một cái cho rồi!<br> ",
    172: "Này‚ Myrtille?<br> ",
    189: "Ôi trời!<br> ",
    198: "Chỉ Huy! Anh làm gì ở đây muộn thế này?<br> ",
    200: "Đó mới là điều anh phải hỏi em. Em đang làm đồ bán cho<br>ngày mai à?<br> ",
    208: "Không đâu! Bây giờ em đang làm bánh tart cho Hội Thi Đồ Ngọt đấy.<br> ",
    210: "Hội Thi Đồ Ngọt à? ...À‚ cuộc thi nướng bánh mà họ tổ chức ở<br>căn cứ đúng không?<br> ",
    221: "Đây là cuộc thi cực kỳ quan trọng để chọn ra người thợ làm bánh giỏi nhất<br>căn cứ đấy!<br> ",
    232: "Với tư cách là thợ làm bánh từ Vương Quốc Đồ Ngọt‚ Mil nhất định phải thắng.<br> ",
    234: "Anh không biết Vương Quốc Đồ Ngọt ra sao‚ nhưng anh hiểu là em không<br>thể thua được.<br> ",
    238: "Nhưng em đừng lo. Bánh tart được làm bằng cả tấm chân tình của Myrtille<br>thì đâu dễ thua đâu.<br> ",
    249: "Nhưng‚ nhưng! Dù em có làm bao nhiêu đi nữa‚ em cũng không thể thấy ""đây là cái<br>đó!""<br> ",
    258: "Em chẳng thể chọn được bánh tart nào để dự thi!<br> ",
    269: "Mỗi cái bánh tart đều có điểm đặc biệt riêng của nó‚ em biết không? Em không thể chọn<br>ra cái ngon nhất!<br> ",
    271: "Vậy rắc rối của em bắt nguồn từ việc yêu bánh tart đến thế à... Thế thì‚ sao<br>không nhờ ai khác nếm thử?<br> ",
    282: "Em hiểu rồi! Mil cần một ý kiến khách quan! Vậy thì‚ Chỉ Huy‚ hãy chọn giúp<br>Mil một cái nhé?<br> ",
    284: "Anh á? Anh nếm thử thì được‚ nhưng anh đâu phải chuyên gia bánh ngọt gì...<br> ",
    313: "Gâu‚ gâu‚ gâu?<br> ",
    315: "Ừ‚ nhờ ai đó quen thuộc với đồ ngọt của em hơn‚ một người<br>thực sự yêu bánh tart‚ chọn thì tốt hơn...<br> ",
    327: "Khoan‚ anh... là một con gấu à!<br> ",
    333: "Gâuu.<br> ",
    335: "Gấu con‚ kẻ đã lẻn vào bếp mà không ai hay biết‚ vươn một<br>cái chân lên như thể nói 'Chào buổi tối!'<br> ",
    366: "Ồ‚ Anh Gấu! Hôm nay anh lại đến nữa rồi!<br> ",
    368: "Gâuu!<br> ",
    370: "Gã này hay đến đây lắm à?<br> ",
    378: "Ừ! Anh ấy lẻn vào lúc không có ai để ăn bánh tart của Mil.<br> ",
    380: "Gâu‚ gâu‚ gâu‚ Gâââuuu!<br> ",
    382: "Trông anh ấy to hơn lần trước rồi. Anh ấy được cưng chiều khá nhiều đây.<br> ",
    390: "Thôi‚ hãy cẩn thận đừng để bị bắt. Ở căn cứ này có rất nhiều người<br>có thể biến anh thành nguyên liệu nồi canh chỉ bằng một đòn.<br> ",
    394: "Gâuu...<br> ",
    396: "Gấu con cau mày như thể nói 'Đáng sợ thật...' Đó là một cử chỉ<br>kỳ lạ giống con người đến lạ.<br> ",
    406: "Nhưng có lẽ anh ấy xuất hiện cũng tốt. Anh ấy đã ăn bánh tart của em<br>vô số lần‚ nên anh ấy biết mùi vị chứ‚ đúng không?<br> ",
    408: "Gâu?<br> ",
    410: "Để anh ấy nếm thử đi.<br> ",
    452: "Em hiểu rồi! Anh Gấu‚ anh có thể chọn giúp em cái bánh tart nào ngon nhất không?<br> ",
    454: "Gâu!<br> ",
    456: "Gấu con vỗ ngực như thể nói‚ 'Cứ giao cho tôi!'<br> ",
    499: "Đây là những bánh tart Mil đang phân vân—cái nào đưa đi dự thi<br>trong cuộc thi.<br> ",
    501: "Gâu‚ gâu gâu!<br> ",
    512: "Anh chắc chưa? Thế thì cứ thử đi!<br> ",
    551: "Gâu!<br> ",
    555: "Gấu con vung dao và nĩa rồi cắt một chiếc bánh tart<br>một cách điêu luyện.<br> ",
    557: "Khoan‚ khoan‚ khoan! Sao một con gấu lại dùng dao nĩa thanh lịch thế để ăn<br>bánh tart vậy?<br> ",
    597: "Mil nghĩ chân anh ấy sẽ dính bẩn‚ nên Mil đưa cho anh ấy‚ và<br>anh ấy dùng ngay lập tức.<br> ",
    599: "Gấu tài năng thật...<br> ",
    635: "Gấu con thanh lịch đưa bánh tart lên miệng‚ gật đầu<br>trầm ngâm‚ rồi bắt đầu gừ gừ.<br> ",
    637: "Gâu‚ gâu gâu‚ gâu gâu.<br> ",
    639: "... Có vẻ anh ấy đang nói gì đó‚ nhưng anh chẳng hiểu tí nào<br>anh ấy đang nói gì.<br> ",
    650: "Hmm... nhưng có vẻ không phải đánh giá tốt lắm... Có lẽ sự cân bằng<br>nguyên liệu hơi bị lệch.<br> ",
    652: "Gâu... gâu‚ gâu gâu?<br> ",
    654: "Gấu con cầm chiếc bánh tart tiếp theo‚ đưa mũi lại gần vết cháy mờ<br>ở cạnh‚ rồi lắc đầu như thể nói 'chà chà'.<br> ",
    665: "Ồ! Bị cháy rồi! Chắc tại Mil nướng thử quá nhiều lần‚ nên Mil hơi<br>lơ đễnh với nhiệt độ...<br> ",
    667: "Gâu gâu. Gâu gâu.<br> ",
    678: "Mm‚ Mil sẽ cẩn thận.<br> ",
    680: "Gã này là sao vậy? Anh ấy là một loại chuyên gia ẩm thực à?<br> ",
    684: "Gâu.<br> ",
    686: "Đừng có gật đầu. Không phải vậy chứ‚ đúng không? Trời ạ‚ anh ấy có gu<br>ẩm thực tinh tế ghê.<br> ",
    728: "Fufufu. Nhưng anh ấy đáng tin cậy thật‚ nhỉ?<br> ",
    766: "Gấu con ăn hết đống bánh tart và cuối cùng để lại một cái trên<br>bàn. Đó là một chiếc bánh tart đơn giản được trang trí bằng trái cây.<br> ",
    810: "Ehh... c-cái này á? Bánh Tart Trái Cây Mùa Sao?<br> ",
    812: "Gâu‚ gâu‚ gâu.<br> ",
    814: "Bánh tart trái cây ngon mà‚ đúng không? Có gì sai với nó đâu?<br> ",
    825: "Nó là món kinh điển và ai cũng thích‚ nhưng chẳng có gì độc đáo! Trong<br>cuộc thi‚ nó có thể bị lẫn mất giữa đám đông!<br> ",
    862: "Gâu‚ gâu‚ gâu‚ gâu? Gâuu‚ gâu‚ gâu‚ gâu‚ gâu!<br> ",
    864: "Anh chẳng hiểu anh ấy đang hăng say về chuyện gì‚ nhưng... anh nghĩ anh ấy đang nói<br>em nên tự tin vào bản thân.<br> ",
    868: "Gâu!<br> ",
    870: "Bánh tart đơn giản lại để tài nghệ của Myrtille tỏa sáng‚ đúng không? Anh cũng nghĩ<br>đó là lựa chọn tốt.<br> ",
    879: "Thắng bằng một chiếc bánh tart tiêu chuẩn... Khó quá‚ sẽ vất vả lắm!<br> ",
    890: "Nhưng... Mil là thợ làm bánh từ Vương Quốc Đồ Ngọt! Mil nhất định phải<br>thắng được bằng cái này‚ đúng không!<br> ",
    892: "Gâu‚ gâu! Gâuu‚ gâu‚ gâu!<br> ",
    934: "Ừ! Mil sẽ tiếp tục nâng cao chất lượng chiếc bánh tart này‚ và rồi Mil sẽ<br>thắng cuộc thi!<br> ",
    945: "Chỉ Huy! Anh Gấu! Mil nhất định sẽ thắng‚ nghe chưa!<br> ",
    947: "Ừ‚ anh rất mong chờ đấy.<br> ",
    951: "Gâuuu!<br> ",
}


def replace_field(line: str, vi_text: str) -> str:
    if line.startswith("title,"):
        parts = line.split(",", 1)
        parts[1] = vi_text
        return ",".join(parts)
    if line.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
        parts = line.split(",", 5)
        # keep parts[:2] (cmd + speaker) and parts[3:] (voice/chara keys) identical
        parts[2] = vi_text
        return ",".join(parts)
    return line


def main() -> int:
    data = EN.read_bytes()
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = [ln.rstrip("\r") for ln in text.split("\n")]

    out_lines = []
    for idx, line in enumerate(lines, 1):
        if idx in VI_TEXT:
            old = line
            # capture original text field for preflight assertions
            if old.startswith("title,"):
                old_field = old.split(",", 1)[1]
            else:
                old_field = old.split(",", 5)[2]
            new_field = VI_TEXT[idx]
            assert "," not in new_field, f"ASCII comma in VI text line {idx}: {new_field!r}"
            assert old_field.count("<br>") == new_field.count("<br>"), (
                f"<br> count mismatch line {idx}: EN={old_field.count('<br>')} VI={new_field.count('<br>')}"
            )
            new_line = replace_field(old, new_field)
            # structural safety: delimiter (ASCII comma) count unchanged
            assert old.count(",") == new_line.count(","), (
                f"delimiter count changed line {idx}: EN={old.count(',')} VI={new_line.count(',')}"
            )
            out_lines.append(new_line)
        else:
            out_lines.append(line)

    out = "\n".join(out_lines)
    if has_crlf:
        out = out.replace("\r\n", "\n").replace("\n", "\r\n")
    VI.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"Wrote {VI} with {len(out_lines)} lines; translated {len(VI_TEXT)} text fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

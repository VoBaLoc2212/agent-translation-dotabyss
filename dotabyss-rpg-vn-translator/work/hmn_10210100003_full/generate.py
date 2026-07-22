#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate VI translation for hmn_10210100003 from the EN asset.

Strategy: read EN asset, for each text command line (title/message/
messageTextUnder/messageTextCenter) replace ONLY the text field (parts[2])
with the ordered VI translation. Speaker/voice/chara/scene IDs, tags,
placeholders, delimiters, BOM, CRLF and line count are preserved byte-for-byte.

Rules applied:
- Commander / Lord Commander -> Chỉ Huy
- 前線基地の兵士A/B, ヒュメナ, ウパ, <user> speaker labels kept verbatim
- in-dialogue Humena/Upa romanized; Upachan -> Upa
- sentence commas use U+201A (‚); ASCII comma never appears in text field
- %user% placeholder preserved
- title in Vietnamese Title Case
"""
from __future__ import annotations
import io
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10210100003.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10210100003.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# Ordered VI text fields, aligned to the 101 text records in EN (title, then 99 messages, then 1 messageTextCenter).
# NO trailing space here; added by the script except for title (idx 0) and messageTextCenter (idx 64).
VI = [
    "Vở Kịch Cả Đời",  # 0 title
    "Này này‚ anh em nghe chưa? Người ta bảo Chỉ Huy sắp đấu với<br>Humena đấy!",  # 1
    "Chúng tôi đang nói về kẻ đập nát trăm viên ngói‚ Humena‚ người được<br>tinh linh nước ban phước mà‚ đúng không? Không có ý gì với Chỉ Huy đâu‚ nhưng ông ấy không tài nào thắng nổi đâu.",  # 2
    "Họ còn hủy cả cá cược vì tỉ lệ cá cược quá<br>chênh lệch. Cái này giống một màn trình diễn hơn là một trận đấu thật sự.",  # 3
    "Thế nhưng‚ đây là Chỉ Huy‚ người từng đối đầu với tai ương<br>trước đây. Dù phải đối mặt với sức mạnh của tinh linh nước‚ tôi không nghĩ ông ấy sẽ bại trận nếu có kế hoạch.",  # 4
    "Mọi người trở nên hưng phấn quá rồi‚ nhưng thế có ổn không anh? Họ<br>vẫn có vẻ hiểu lầm về Upa...",  # 5
    "Không phải rất thuận tiện sao? Anh sẽ giải quyết mọi chuyện ngay tại đây.",  # 6
    "Được rồi‚ Humena. Đúng như chúng ta đã bàn‚ anh trông cậy vào em đấy.",  # 7
    "Ư-ưm‚ anh có chắc là ổn không? Có lẽ vẫn còn cách khác mà...",  # 8
    "Không sao. Nào‚ bắt đầu chiến dịch thôi... khẹc!",  # 9
    "Khúc khúc khúc! Bọn mấy người nói khoác ghê đấy‚ lũ cổ động viên chế giễu kia! Các người tưởng anh không tài nào<br>đánh bại nổi Humena đúng không?",  # 10
    "Đúng thế chứ! Thế kế hoạch của ngài là gì‚ Chỉ Huy?",  # 11
    "Các người cứ đợi mà xem! Nhưng anh nói trước thế này: anh đã chiếm<br>thế thượng phong về mặt tinh thần! Nhìn Humena đi! Em ấy đang nao núng mà‚ đúng không!",  # 12
    "Ư! Á‚ ờ... ưm...",  # 13
    "Em có đến đây thật đấy‚ nhưng mà‚ em cũng chẳng mấy hào hứng với chuyện này.",  # 14
    "Ồ hô‚ ra em không muốn đấu với anh sao?",  # 15
    "Đúng vậy‚ Chỉ Huy. Anh không phải là người em muốn giao chiến. Em<br>không muốn làm anh bị thương.",  # 16
    "Khúc khúc‚ ha ha ha! Phư ha ha ha! Em đã sa vào bẫy của anh rồi‚ Humena!",  # 17
    "Chỉ Huy tiến lại gần Humena và kéo cô ấy vào một cái<br>ôm thật chặt‚ tay quàng qua vai cô ấy.",  # 18
    "Ư! Này‚ Chỉ Huy!",  # 19
    "C-cái gì!? Chỉ Huy! Ngài đang làm gì với Humena thế?",  # 20
    "Này‚ này‚ này! Mối quan hệ giữa hai người là sao thế?",  # 21
    "Như các người thấy đấy! Humena‚ người mà các người truy đuổi‚ đã hoàn toàn<br>mở lòng với anh!",  # 22
    "'Mở lòng‚' anh ta bảo! Ư-chứ ra là‚ em đâu có được báo trước là nó lại<br>đi xa đến thế—",  # 23
    "Gì cơ? Em chưa mở lòng với anh sao?",  # 24
    "Ư-ưm‚ ý em là... ừ... có‚ nhưng mà...",  # 25
    "Các người thừa nhận rồi! Vậy là hai người thân mật lắm hả?",  # 26
    "Y-yêu đương chi chứ! Không đời nào! Không phải như thế đâu!",  # 27
    "Dù sao đi nữa‚ anh đã giành được lòng tin của Humena! Anh đã thu phục được em ấy!",  # 28
    "Ý là... chẳng lẽ...?",  # 29
    "Đúng vậy! Lũ tinh linh nước cũng chẳng khác gì! Anh đã thuần phục chúng hoàn toàn!",  # 30
    "Chỉ Huy ném những mảnh bánh dumpling xuống nước‚ và lũ Upa<br>bắt đầu mổ chúng một cách vui vẻ.",  # 31
    "Upa!♪",  # 32
    "Lũ tinh linh nước đang ăn đồ ăn của Chỉ Huy kìa!",  # 33
    "Và chúng trông vui vẻ hẳn lên! Chúng thực sự đã gắn bó với ngài ấy‚<br>đúng không!",  # 34
    "Upa!",  # 35
    "Như mọi người đã biết‚ Humena đã nhận được sự ban phước từ các<br>tinh linh nước!",  # 36
    "Nhờ giành được lòng tin của các tinh linh nước‚ anh cũng đã nhận được sự<br>ban phước giống hệt Humena!",  # 37
    "Ra thế! Với chuyện đó‚ có lẽ ngài có thể thắng!",  # 38
    "Sức Mạnh Tinh Linh Nước giờ là của anh! Phư ha ha ha!",  # 39
    "Ư-nhưng em bảo anh này‚ làm gì có cái gọi là Sức Mạnh Tinh Linh Nước...",  # 40
    "Đủ lời nói nhảm rồi‚ Humena! Nào‚ xông vào đi!",  # 41
    "... Ư-anh có chắc về chuyện này không?",  # 42
    "Tất nhiên! Không cần nương tay! Xông vào anh đi! Ga ha ha ha ha!",  # 43
    "(Chỉ Huy‚ dù anh đang diễn‚ nhưng giọng của anh đang run lên<br>mất rồi... Anh đang cố gắng quá sức vì em và Upa. Em cũng phải cố gắng hơn nữa.)",  # 44
    "(Em phải đảm bảo anh không bị thương... nhẹ thôi‚ nhẹ thôi...)",  # 45
    "Ha yá!",  # 46
    "Ự! Gưaaaaaaaa!",  # 47
    "Bị đòn của Humena đánh trúng‚ %user% bay vút đi‚ lăn lông lốc trên<br>sàn võ đường.",  # 48  (keep %user%)
    "Không... thể nào... Với sự Ban Phước của Tinh Linh Nước... Lẽ ra anh phải mạnh hơn chứ?",  # 49
    "Không phải thế đâu. Upa chẳng có năng lực đặc biệt nào cả.",  # 50
    "Vậy những lời đồn là dối trá...? Thế rốt cuộc cái Sức Mạnh Tinh Linh Nước<br>là cái gì...?",  # 51
    "Những đứa bé này là những người bạn thân quý của em. Được ở bên chúng cho em<br>sức mạnh để cố gắng hết sức và trở nên mạnh mẽ hơn. Chỉ có vậy thôi.",  # 52
    "Vậy sức mạnh thật sự chính là sự gắn kết giữa những người bạn... Ah... anh thật ngu ngốc...<br>Giỏi lắm‚ Humena... *ự*!",  # 53
    "U-Upa! Upa!",  # 54
    "Này‚ vậy cái chuyện mạnh lên nhờ tinh linh nước chỉ là<br>một đống xàm bớt thôi hả?",  # 55
    "Thế mà lũ tinh linh nước lo lắng hết sức‚ còn Chỉ Huy thì<br>tơi tả hẳn rồi.",  # 56
    "Chà‚ hết diễn rồi‚ về thôi!",  # 57
    "Đám người xem tụ tập‚ nhận ra các tinh linh nước chẳng có ban phước gì để<br>ban phát‚ bèn bỏ đi với vẻ thất vọng.",  # 58
    "Ư-thế là... kế hoạch... thành công...",  # 59
    "Ư-anh có ổn không? Chỉ Huy? Em xin lỗi‚ em đã nương tay hết mức có thể...!<br> ",  # 60 (internal br present)
    "Em nương tay... mà đây là sức mạnh... *ụa*",  # 61
    "C-Chỉ Huy!",  # 62
    "Upa!",  # 63
    "<size=48>Vài Ngày Sau.</size>",  # 64 messageTextCenter (no trailing space)
    "Nào nào‚ những Upa‚ các em muốn bơi bao nhiêu cũng được!♪",  # 65
    "Upa!",  # 66
    "Các tinh linh nước‚ được thả từ bể ra‚ bắt đầu bơi lội vòng quanh<br>đại dương xinh đẹp.",  # 67
    "Chúng trông vui đấy‚ những Upa.",  # 68
    "Ừ! Đã lâu lắm rồi bọn nhỏ mới được thấy biển. Em vui lắm vì chúng<br>đều đang tận hưởng!",  # 69
    "Anh bắt em phải đợi đến khi anh hồi phục. Và em cũng đã chăm sóc cho anh.<br>Xin lỗi nhé‚ Humena.",  # 70
    "Đừng nói vậy. Nhờ có anh‚ những Upa mới được vui chơi như<br>thế này. Chuyện đó là lẽ đương nhiên mà!",  # 71
    "Hơn nữa‚ em luôn muốn anh được thấy bọn nhỏ bơi giữa biển như<br>thế này.",  # 72
    "Ah... cảnh đẹp thật. Anh có thể thấy rõ chúng là tinh linh nước.",  # 73
    "Đáng công mạo hiểm cả thân mình để cho lũ ngốc kia thấy là làm thân với<br>các tinh linh nước chẳng khiến người ta mạnh lên.",  # 74
    "Và anh cũng cho họ thấy chuyện gì sẽ xảy ra nếu kẻ nào tiếp cận em<br>vì dục vọng cá nhân. Vậy là chúng ta sẽ ổn thôi.",  # 75
    "Ừm. Cảm ơn anh rất nhiều vì đã làm sáng tỏ sự hiểu lầm.",  # 76
    "Có người còn xin lỗi vì đã hiểu lầm‚ và có người nhờ em huấn luyện<br>bọn họ.",  # 77
    "Nhưng... kể từ khi bọn họ phát hiện Upa chẳng có năng lực gì‚ họ nhìn Upa như thể là món ăn.<br>Hơi phiền đấy. A ha ha.",  # 78
    "Ừ thì‚ bọn đó trông cũng ngon đấy‚ mấy con đó...",  # 79
    "Này‚ Chỉ Huy!",  # 80
    "Upa!",  # 81
    "Ha ha ha‚ anh chỉ đùa thôi‚ đùa thôi.",  # 82
    "Chà...<br>Này‚ Chỉ Huy.",  # 83
    "Anh không cần phải đi xa đến thế vì bọn em đâu‚ anh biết mà?",  # 84
    "Anh không cần phải nhận đòn trực tiếp đâu.<br>Anh có thể nhờ một người lính được huấn luyện kỹ hơn làm việc đó...",  # 85
    "Anh có cân nhắc chuyện đó‚ nhưng việc để một gã đàn ông khác giả vờ thân thiết với<br>em khiến anh không vui.",  # 86
    "...Ừ‚ nghĩ lại thì‚ em cũng chẳng thích điều đó.",  # 87
    "Em không muốn ai nghĩ em thân thiết với một gã đàn ông khác.<br>Nếu họ định vòng tay qua vai em‚ em sẽ lập tức bỏ chạy mất.",  # 88
    "Ồ‚ ra em cũng nghĩ vậy.<br>Thế thì anh mừng vì mình đã làm tới cùng.",  # 89
    "Ừ... đúng vậy.♪",  # 90
    "Dù vậy‚ anh cũng có chút thất vọng.<br>Nếu sự ban phước của những Upa là thật‚ anh đã có thể học đánh một chút.",  # 91
    "...Anh không cần thứ đó đâu‚ Chỉ Huy.<br>Bất cứ khi nào anh cần‚ em sẽ là sức mạnh của anh.",  # 92
    "Em cơ à.<br>Nghe có vẻ đáng tin cậy hơn là tăng sức nhờ ban phước.",  # 93
    "Ừ‚ hãy tin tưởng ở em.<br>Cứ nói với em bất cứ khi nào anh gặp rắc rối.",  # 94
    "Dù là lúc nào hay là ai đi nữa‚<br>em sẽ lập tức chạy đến cùng Upa.",  # 95
    "Vì anh‚ Chỉ Huy‚ em sẽ làm bất cứ điều gì!♪",  # 96
    "Đúng như mong đợi từ Humena‚ người có thể đập vỡ 100 viên ngói—mấy câu<br>tán tỉnh của em cũng mạnh chẳng kém.",  # 97
    "Fu fu‚ điều duy nhất em có thể làm là<br>tung đòn thẳng diện với Sức Mạnh Tinh Linh Nước.",  # 98
    "Đúng không‚ Upa?",  # 99
    "Upa!",  # 100
]
# Localize the water-spirit character name to a Vietnamese-readable spelling.
# EN asset uses "Upaa!" (long) / "Upa!" (bark) / "Upa(s)" (in dialogue). Normalize to "Ưpa".
VI = [s.replace("Upaa", "Ưpa").replace("Upas", "Ưpas").replace("Upa", "Ưpa") for s in VI]
# EN message text fields end with "<br> " (a <br> tag then a trailing space).
# Title (0) and messageTextCenter (64) keep their exact text. All other (message) fields
# get "<br> " appended; the base still must contain the correct number of INTERNAL <br>
# tags to match the EN source's tag multiset.
assert VI[64] == "<size=48>Vài Ngày Sau.</size>", "messageTextCenter base changed"
for i, s in enumerate(VI):
    if i in (0, 64):
        continue
    VI[i] = s + "<br> "


def main() -> None:
    data = EN.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    vi_lines: list[str] = []
    idx = 0
    text_record_count = 0
    for ln in lines:
        if ln.startswith(TEXT_CMDS):
            text_record_count += 1
            assert idx < len(VI), f"Ran out of VI at record {text_record_count}"
            vi_text = VI[idx]
            idx += 1
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text
            else:
                # split into at most 6 fields; text field never contains ASCII comma in EN
                parts = ln.split(",", 5)
                parts[2] = vi_text
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    assert idx == len(VI), f"VI list not fully consumed: used {idx}/{len(VI)}; text_records={text_record_count}"
    assert text_record_count == len(VI), f"text record count {text_record_count} != VI {len(VI)}"

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT}")
    print(f"text_records={text_record_count} vi_used={idx} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()

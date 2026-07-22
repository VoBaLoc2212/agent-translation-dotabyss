#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic VI builder for hmn_10200100002.

Approach: substring/field-index replacement. The EN asset text fields are
English (already localized) with authoritative structure (fullwidth `，` commas,
`<br>` breaks, trailing field signatures). We translate each translatable
field to Vietnamese and rebuild the line preserving every structural byte
(BOM, CRLF, delimiters, tags, IDs, trailing empty fields, trailing commas).

Rules applied:
- title -> Vietnamese Title Case.
- Commander (<user>) = male -> 'anh'; 司令官 -> 'Chỉ Huy'.
- Laveria (ラヴェリア) addresses Commander as 兄さん -> 'anh' (em->anh).
- Alicia (アリシア) addresses Commander as 司令官 -> 'Chỉ Huy'.
- Laveria's アタシ self-ref -> 'em'; Alicia's わたし self-ref -> 'em'.
- No ASCII commas inside VI fields (use U+201A , only if needed; avoided here).
- Preserve `，` fullwidth commas and `<br>` counts from EN asset exactly.
- Keep speaker/charaload JP names unchanged.
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10200100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# line_no -> VI translation for the text field only (EN asset field).
# The EN asset text field is the source-of-truth for structure.
TRANSLATIONS = {
    23:  "Đến Chiến Trường Quyết Định……!",
    44:  "Được rồi‚ báo cáo của chuyến thám hiểm trước đã tổng hợp xong. Anh‚<br>anh có thể xác nhận giúp em được không?<br> ",
    46:  "Ừm… ừ‚ không có vấn đề gì. Vậy là chốt rồi‚ Alicia‚ gửi cho các<br>nước đi!<br> ",
    54:  "Này‚ này‚ anh ơi‚ anh có thể qua loa thế không?<br> ",
    56:  "Anh đã xem nội dung rồi. Anh cũng biết em giỏi thế nào‚<br>Laveria. Đây gọi là tiết kiệm thời gian.<br> ",
    58:  "Nếu phải nói thì‚ Laveria… anh nghĩ em hơi tự khiêm tốn<br>về thành tích của mình đấy.<br> ",
    66:  "Ồ? Anh đọc kỹ thế cơ à. Đúng là Chỉ Huy<br>có khác.<br> ",
    71:  "Vậy nhé‚ Alicia‚ việc này giao cho em. Chỉ Huy đã<br>duyệt rồi.<br> ",
    86:  "Vâng‚ em sẽ nộp! Mọi người đã vất vả rồi!<br> ",
    100: "Phần hôm nay cuối cùng cũng xong… Cảm ơn em‚ Laveria‚ em giúp đỡ nhiều lắm.<br> ",
    103: "Em quen mấy việc giấy tờ kiểu này rồi. Dễ ợt thôi.<br> ",
    105: "Ra thế. Nhưng em vốn làm công việc giấy tờ cơ mà‚<br>tại sao giờ lại muốn chiến đấu như một chiến binh?<br> ",
    109: "Đó là điều cần thiết để bảo vệ đồng đội. Anh cũng nghĩ vậy mà‚<br>đúng không anh?<br> ",
    111: "Ừm… Còn anh‚ giống như bị giao nhiệm vụ ấy. Còn cái cảm giác<br>trách nhiệm như em… anh không chắc.<br> ",
    113: "Thôi nào. Này Laveria‚ đây là thưởng hôm nay của em.<br>Cũng không nhiều vàng‚ nhưng hãy nhận lấy.<br> ",
    122: "Hả!? Em không cần thưởng đâu! Em chỉ giúp một tay thôi mà!<br> ",
    124: "Anh đã nhờ em làm việc ngoài phận sự. Không trả thưởng thì anh<br>thấy áy náy lắm.<br> ",
    127: "Nhưng… cảm giác nhận tiền dù chẳng làm được gì nhiều thì…<br> ",
    129: "Hãy coi như là tấm lòng của anh. Em cứ tiêu vào sở thích hay<br>thứ gì em thích cũng được.<br> ",
    145: "Đồ em thích‚ hử… Được rồi‚ em sẽ nhận với lòng biết ơn.<br> ",
    147: "Tốt. Vẫn còn nhiều báo cáo chưa xử lý… Em có thể giúp anh<br>ngày mai và cả ngày mốt được không?<br> ",
    159: "Ngày mai lẫn ngày mốt cơ à… Thôi‚ được. Em sẽ ở lại<br>Căn Cứ Tiền Tuyến một thời gian.<br> ",
    161: "Đúng ý anh! Em đúng là cứu tinh!<br> ",
    164: "Thật tình‚ anh đúng là Chỉ Huy hay sai khiến người khác. Hôm nay<br>em xin phép về đây. Mọi người vất vả rồi!<br> ",
    176: "Được‚ thế là có thêm một người lo được việc giấy tờ. Anh nghĩ<br>chúng ta sẽ vượt qua được tình hình này thôi.<br> ",
    193: "Ôi‚ Chỉ Huy. Laveria cũng bận mà‚ anh đừng ép<br>cô ấy quá đấy.<br> ",
    195: "Anh có trả thù lao đàng hoàng cơ mà‚ nên không tính là ép buộc đúng không?<br> ",
    197: "Hơn nữa‚ Laveria dù không trả tiền cũng sẽ giúp anh. Cô ấy thật đáng tin cậy.<br> ",
    202: "Vâng‚ chúng em thực sự biết ơn Laveria. Mạnh mẽ và đáng tin trên<br>chiến trường‚ lại còn giỏi giấy tờ nữa……<br> ",
    204: "Anh ước gì có thêm năm Laveria nữa. Sẽ cho họ luân phiên trực ở<br>phòng chỉ huy.<br> ",
    209: "Ư… thế thì em thành thừa thãi mất rồi……<br> ",
    268: "Laveria‚ cảm ơn em đã giúp đỡ hôm nay nữa.<br> ",
    271: "Em đã hứa với anh. Với lại em rảnh‚ nên giúp một tay không<br>thành vấn đề.<br> ",
    273: "Nhờ em mà‚ Laveria‚ chúng ta có thể tránh được làm đêm. Hôm nay<br>cũng nhờ em! Tiểu thư Laveria mạnh mẽ‚ giỏi giấy tờ lại xinh đẹp!<br> ",
    284: "Đừng có nịnh hót kỳ cục. Nào‚ đưa file tiếp theo cho anh đi.<br> ",
    286: "Được rồi‚ anh nhờ em đấy‚ Laveria.<br> ",
    293: "May quá……<br> ",
    298: "Hử? Có chuyện gì sao‚ Alicia?<br> ",
    305: "Em mạnh mẽ‚ ngầu lại còn được Chỉ Huy dựa dẫm……<br>Laveria‚ em luôn nghĩ chị thật tuyệt vời!<br> ",
    312: "Haha‚ em có gì đâu. Chỉ là làm được hơi nhiều việc một chút thôi.<br> ",
    325: "Điểm yếu của em cũng nhiều lắm. Hôm nọ lúc chiến đấu em nóng quá<br>nên đã lao lên quá đà đúng không?<br> ",
    328: "Đó đâu tính là khuyết điểm! Em cũng muốn trở thành như chị‚ tiểu thư Laveria……<br> ",
    334: "Alicia cứ là chính em là được. Bên cạnh anh cần có một người như em.<br> ",
    343: "Hể…… thật vậy sao?<br> ",
    348: "Ừ‚ em làm không khí vui hơn mà. Chỉ có mình anh cau có thì chẳng<br>thể chỉ huy dễ dàng được.<br> ",
    356: "Thật ư? Chỉ Huy‚ hóa ra em có ích thật!<br> ",
    358: "Ừ‚ em có ích đấy. Nói sao nhỉ…… em kiểu như linh vật của<br>căn cứ ấy.<br> ",
    363: "Ư… linh vật……<br> ",
    374: "Fufu… ý là em là một sự hiện diện dễ thương đấy‚ Alicia.<br> ",
    378: "Này‚ anh có chuyện muốn hỏi. Anh ơi‚ anh hình dung em là<br>kiểu người như thế nào?<br> ",
    380: "Hử? Cách anh nhìn em á? Thì…<br> ",
    382: "Chiến đấu xuất sắc‚ tâm lý vững vàng ngay cả trong khủng hoảng‚<br>và là một chiến binh được mọi người tin tưởng.<br> ",
    384: "Em có thói quen tập trung vào chiến đấu nên với tư cách chỉ huy anh<br>kỳ vọng em phát triển thêm. Nói chung thì‚ em là một mỹ nhân đáng tin.<br> ",
    391: "Đáng tin‚ hử. Đánh giá cao thật đấy……<br> ",
    393: "Anh định khen cao thế mà trông em không vui lắm nhỉ.<br> ",
    397: "Không‚ em đang có động lực đây. Em phải luôn là chỗ dựa đáng tin cho anh‚ anh ơi.<br> ",
    407: "Em cũng muốn trở thành một Phó Chỉ Huy đáng tin…… Nếu có dịp‚<br>hãy kể em nghe thêm nhé!<br> ",
    415: "À‚ lần tới sao không cùng mọi người<br>từ Lux Nova đi chơi phố?<br> ",
    420: "Ừ‚ nghe vui đấy. Nhất định hãy mời em nhé.<br> ",
    425: "Vâng‚ chắc chắn! Nghe nói có cửa hàng mới khai trương nên em sẽ dẫn anh đi!<br> ",
    435: "Cửa hàng mới…… là kiểu cửa hàng gì vậy?<br> ",
    443: "Là một cửa hàng đầy những món đồ dễ thương ạ. Em cũng đang mong được đi cùng!<br> ",
    451: "…Một cửa hàng đầy đồ dễ thương……! Vậy là cuối cùng cửa hàng đó……!<br> ",
    456: "Được rồi! Không phải lúc tán gẫu! Quay lại làm việc thôi!<br> ",
    460: "Sao thế Laveria‚ tự dưng lại có động lực thế?<br> ",
    484: "Ít nói đi‚ làm nhiều lên! Ta sẽ xong nhanh thôi!<br> ",
    488: "Đ-được rồi…… Sao anh lại thế? Động lực kinh khủng thật……<br> ",
    520: "A‚ cuối cùng cũng được tự do. Không có sự giúp đỡ của Laveria thì<br>anh không biết mọi chuyện sẽ ra sao……<br> ",
    522: "Hử……? Người ở kia là……<br> ",
    544: "……<br> ",
    546: "Laveria‚ hử. Trông cô ấy nghiêm túc lạ thường…… đang làm gì thế nhỉ?<br> ",
    565: "Đ-được rồi‚ không ai nhìn thấy chứ? Không ai phát hiện ra em chứ……?<br> ",
    567: "Cô ấy có vẻ đang nhìn quanh đầy bồn chồn…… Nhưng hơn là cảnh giác‚<br>trông cô ấy như đang nôn nao……<br> ",
    574: "Có thật là ổn không……? Nhưng…… chỉ một lần‚ chỉ một chút thôi……!<br> ",
    592: "Cô ấy đang len lỏi đi trong khi liếc quanh…… Đáng ngờ‚ quá đỗi<br>lộ liễu đáng ngờ!<br> ",
    594: "Laveria định làm gì giữa phố phường thế này……?<br> ",
    596: "…Anh có nên đi theo không? Nếu cô ấy gặp rắc rối thì anh không thể bỏ mặc được.<br> ",
    603: "Đ-được rồi‚ ta đi đến chiến trường quyết định……! Fufu‚ fufufufufu!<br> ",
}


def main():
    assert TRANSLATIONS, "fill TRANSLATIONS"
    for ln, vi in TRANSLATIONS.items():
        assert "," not in vi, f"ASCII comma in VI for line {ln}: use U+201A ,"

    raw = EN.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf", "EN source must have BOM"
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(True)
    out = []
    translated = 0
    for idx, line in enumerate(lines, 1):
        if idx in TRANSLATIONS:
            vi = TRANSLATIONS[idx]
            cleaned = line.rstrip("\r\n")
            if cleaned.startswith("title,"):
                parts = cleaned.split(",", 1)
                assert len(parts) == 2, f"title field split issue line {idx}: {line!r}"
                new = "title," + vi
            elif cleaned.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
                parts = cleaned.split(",", 5)
                assert len(parts) >= 3, f"message field split issue line {idx}: {line!r}"
                parts[2] = vi
                new = ",".join(parts)
            else:
                raise AssertionError(f"unexpected text cmd line {idx}: {line!r}")
            trailer = line[len(line.rstrip("\r\n")):]
            assert trailer in ("\r\n", "\n", ""), f"unexpected trailer line {idx}: {trailer!r}"
            out.append(new + trailer)
            translated += 1
        else:
            out.append(line)
    out_bytes = b"\xef\xbb\xbf" + "".join(out).encode("utf-8")
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out_bytes)
    print(f"translated {translated}/{len(lines)} lines -> {VI}")


if __name__ == "__main__":
    main()

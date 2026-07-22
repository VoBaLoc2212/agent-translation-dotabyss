#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Custom VI builder for hmn_10400100001.

Case: EN-asset-is-English with a JP title (title, field is JP; message,/
messageTextCenter, fields are English). The EN text also carries the
"Commaander" typo (-> Chih Huy / Chỉ Huy) which we repair, fullwidth
'，' commas (-> U+201A '‚'), and residual English SFX (localized).

Rules applied:
- title,  -> full VI (Title Case), no suffix
- messageTextCenter, -> full VI (incl. <size=48>..</size>), no suffix
- message, -> VI body + mirrored trailing "<br> " suffix (authoritative)
- BOM + CRLF preserved; delimiter/field/tag/placeholder counts unchanged.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10400100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAGSUF_RE = re.compile(r"(?:<[^>]+>\s*)+$")

# line_no -> VI text (full for title/center, body-only for message)
VI = {
    31: "Sẽ Trở Thành Đấu Sĩ Giỏi Nhất Thế Giới",
    41: "<size=48>—Bên Trong Đại Huyệt‚ Khu Vực Đã Thám Hiểm</size>",
    48: "Đội dự bị đang tiến hành nhiệm vụ thám sát.",
    75: "Gừư!",
    89: "...! Chuyện gì vậy!",
    91: "Phục kích!<br>Đội hậu quân đang bị tấn công!",
    157: "Chết tiệt! Đã thành hỗn chiến rồi!",
    206: "Gàaaaa!",
    261: "Ai xử lý con này giùm!<br>Kyaaa!",
    285: "Cứ giao cho em!",
    365: "Gừ!",
    379: "Một cô gái lao vào thế thủ của quái vật. Khoảnh khắc sau‚ một nắm đấm nhỏ bé<br>thổi bay nó đi.",
    422: "Tiếp theo!",
    535: "Gừư...",
    610: "Con này nữa!",
    691: "Gư!",
    835: "Cô ấy hạ gục một kẻ thù và lao ngay vào kẻ tiếp theo trong cùng một nhịp thở.<br>Quái vật ngã gục trước khi kịp phản ứng.",
    837: "Tuyệt vời! Cô bé đó là ai vậy?",
    839: "Luca! Đúng như mong đợi‚ em ấy thật phi thường.",
    884: "Gùuuu!",
    938: "Con quái vật khổng lồ cuối cùng lao vào Luca. Không hề nao núng‚ em ấy bước<br>vào thế thủ và siết chặt nắm đấm.",
    969: "Và thế là xong!",
    1038: "Nắm đấm mang điện của Luca nổ lách tách‚ tung sét đánh tứ tung. Em ấy vọt lên và<br>đâm xuyên quái vật bằng một đòn chí mạng.",
    1053: "*Gừư...*",
    1112: "*phù*... Có lẽ thế là xong. Mọi người ổn chứ?",
    1173: "Vâ-vâng. Cảm ơn em‚ Luca. Em có bị thương không?",
    1184: "Không có gì! Vừa là một bài tập tốt!",
    1223: "Em làm cả đống thứ đó rồi gọi là bài tập thôi à? Đáng nể đấy‚ Luca.",
    1234: "Á‚ Chỉ Huy! Hê hê‚ dễ ợt ấy mà!",
    1245: "Em sẽ trở thành đấu sĩ giỏi nhất thế giới‚ nên không quái nào<br>đánh bại được em đâu!",
    1247: "Đấu sĩ giỏi nhất thế giới à? Sau khi thấy em chiến đấu‚ anh thấy không<br>phải chuyện viển vông nữa.",
    1259: "Ở Đại Huyệt còn nhiều kẻ thù mạnh hơn nữa đúng không? Ừm‚ nghe<br>như một bài huấn luyện tuyệt vời!",
    1261: "Ồ‚ em coi chiến đấu là một phần huấn luyện à? Không lạ khi em tiến bộ<br>nhanh thế.",
    1263: "Ở Căn Cứ Tiền Tuyến cũng có nhiều người mạnh‚ không chỉ<br>riêng Đại Huyệt. Có lẽ nên giao lưu với họ.",
    1274: "Đúng rồi‚ đúng thế! Em sẽ tìm người mạnh khi chúng ta về<br>căn cứ!",
    1298: "Chúng ta chưa thám hiểm xong đâu‚ đừng lơ là cảnh giác!",
    1325: "<size=48>—Vài Ngày Sau—</size>",
    1342: "Được rồi‚ giấy tờ hôm nay xong rồi. Giá mỗi ngày đều thế này<br>thì tốt...",
    1352: "Cửa bật mở với một tiếng ầm!",
    1387: "Cái gì—ôi!",
    1389: "Khi tôi nhìn về phía cửa‚ Luca đã đứng ngay trước<br>mặt tôi.",
    1400: "Chỉ Huy‚ em thách đấu với anh!",
    1402: "Gần quá! Đừng làm anh giật mình‚ Luca!",
    1414: "Hả? Gần á? Em không nghĩ vậy.",
    1416: "Đừng nói sát mặt anh như thế! Anh ngửi thấy mùi em và cảm nhận hơi thở em!",
    1434: "Hít hít... Á‚ em nói đúng. Đây là mùi của Chỉ Huy!",
    1436: "Thôi đừng ngửi anh! Nào‚ lùi lại đi!",
    1494: "Cái gì thế‚ Chỉ Huy? Anh đang đỏ mặt à? Em làm tim anh<br>đập thình thịch phải không?",
    1496: "Em ồn ào quá. Thế‚ em muốn gì?",
    1507: "Em đã nói 'em thách đấu‚' mà nhỉ? Em đến đây để đánh với Chỉ Huy!",
    1509: "Hả? Anh á? ...Sao lại thành chuyện đó?",
    1521: "Em nghe nói Chỉ Huy là người mạnh nhất ở căn cứ này. Nên em muốn đấu<br>với anh!",
    1523: "Anh là mạnh nhất! Ai nói thế?",
    1534: "Em đã hỏi khắp nơi xem ai biết người mạnh nhất ở đây. Rồi bà<br>thương nhân mờ ám và cô bé dùng ma thuật đã chỉ em!",
    1546: "Họ bảo nếu anh đánh thật sự‚ Chỉ Huy sẽ là người<br>mạnh nhất ở Căn Cứ Tiền Tuyến!",
    1548: "Bọn họ...! Thôi‚ anh hiểu sao họ nói vậy‚ nhưng...",
    1559: "Hóa ra anh thật sự mạnh! Này‚ đánh với em đi‚ Chỉ Huy!",
    1570: "Em sẽ trở thành Đấu Sĩ Vĩ Đại Nhất Thế Giới bằng cách chiến đấu<br>với thật nhiều người mạnh!",
    1572: "Em thật đơn giản...",
    1574: "...Được rồi‚ để anh xem xét.",
    1608: "Thật á? Hay quá‚ đánh ngay đi!",
    1610: "Bình tĩnh. Em mới là người thách đấu anh‚ nên để anh ít nhất<br>chọn thời gian và địa điểm. Được không?",
    1622: "Tất nhiên. Em sẽ đánh bất cứ lúc nào‚ bất cứ đâu!",
    1624: "...Em thật sự đơn giản‚ Luca. Thôi‚ anh sẽ chơi với em một chút.",
    1649: "<size=48>—Vài Giờ Sau</size>",
    1656: "Khu vực núi non gần Căn Cứ Tiền Tuyến",
    1658: "Được rồi‚ mọi chuẩn bị đã xong. Cũng đến lúc rồi...",
    1694: "Chỉ Huy! Em đến rồi. Anh đã đợi em à?",
    1705: "Anh mong đợi được đấu với em đến thế á? Em cũng vậy!",
    1707: "Thôi‚ phải thừa nhận phần vui mới bắt đầu. Nào‚ bất cứ khi nào em<br>sẵn sàng. Tới đi!",
    1719: "OK! Em bắt đầu đây‚ Chỉ Huy!",
    1723: "Ừ‚ trận đấu bắt đầu!",
    1750: "Ta a a!",
    1766: "Luca‚ với tư thế chồm tới sẵn sàng‚ bỗng biến mất khỏi<br>tầm mắt.",
    1800: "Sẵn sàng...",
    1802: "Khoảnh khắc tiếp theo‚ Luca xuất hiện ngay trước %user%‚ nắm đấm<br>bao bọc trong sấm sét.",
    1831: "*thở dốc*—Hả!",
    1853: "Ngay khi em dừng lại để tung một cú đấm toàn lực‚ chân Luca trượt<br>khỏi dưới em.",
    1884: "Cái gì thế‚ cái gì thế!",
    1886: "Ồ kìa! Có cả vũng nước ở chỗ này à? Thôi‚ anh cũng bất ngờ đấy.",
    1897: "Đâu phải vũng nước. Nó trơn tuột và em không cử động được!",
    1899: "Ồ‚ đây là chất nhờn của Slime à? Em sẽ chẳng dễ dàng đứng dậy<br>đâu‚ nhỉ?",
    1910: "Nó trơn quá! Chỉ Huy‚ cứu em với!",
    1912: "Ha ha ha! Giữa trận đấu mà kêu cứu à? Buồn cười thật! Nào‚<br>để anh đỡ em dậy!",
    1923: "Hwa! Khoan‚ đừng cù nách em! Đừng cù chỗ đó!",
    1925: "Thế còn chỗ này thì sao?",
    1944: "Không‚ cổ và lưng em cũng cấm! Hyah! Hư hư hư! A ha ha ha! Bụng<br>em đau quá!",
    1946: "Thấy chưa? Người em trơn tuột nên chẳng thể phản kháng‚ đúng không?<br>Thế nào‚ Luca? Đầu hàng không?",
    1957: "Kyah! Fah! A ha ha ha ha! Chưa‚ em chưa thua!",
    1959: "Em có gan đấy! Thế... còn chỗ này thì sao!",
    1976: "K-khoan! Đừng cù lòng bàn chân em‚ nghiêm túc đấy! *rên rĩ*! ừm ừm!<br>A ha ha ha ha ha!",
    1987: "Xin lỗi‚ em chịu hết nổi! Em thua‚ đầu hàng‚ đầu hàng!",
    2030: "Được rồi‚ anh thắng. Này‚ Luca‚ cái khăn đây.",
    2047: "Cảm ơn‚ Chỉ Huy. Hừm‚ hừm...",
    2058: "Ứ‚ em thua mà chẳng làm được gì... Anh thật sự tuyệt vời‚<br>Chỉ Huy!",
    2060: "...Anh không ngờ lại được khen như vậy. Không phàn nàn gì về việc anh<br>bất công hay gian lận sao?",
    2071: "Ừ‚ anh bất công đấy‚ Chỉ Huy! Đồ gian lận!",
    2082: "Nhưng Đấu Sĩ Vĩ Đại Nhất Thế Giới không thua chỉ vì một<br>mánh khóe rẻ tiền. Chỉ Huy đã đánh bại em thật tuyệt vời!",
    2084: "Ồ-ồ. Em thật thà thật sự‚ Luca...",
    2096: "Nhưng lần sau em sẽ không thua! Hãy chuẩn bị đi!",
    2098: "Hóa ra còn lần sau nữa à...",
    2109: "Tất nhiên! Em sẽ đánh bại anh‚ Chỉ Huy‚ và trở thành người mạnh nhất ở<br>Căn Cứ Tiền Tuyến!",
}


def main() -> None:
    data = EN.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "EN asset missing BOM"
    has_crlf = b"\r\n" in data
    text = data.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    vi_lines: list[str] = []
    used = set()
    record_count = 0
    for i, ln in enumerate(lines, 1):
        if ln.startswith(TEXT_CMDS):
            record_count += 1
            assert i in VI, f"missing VI for line {i}"
            vi_text = VI[i]
            used.add(i)
            if ln.startswith("title,"):
                parts = ln.split(",", 1)
                parts[1] = vi_text
            elif ln.startswith("messageTextCenter,") or ln.startswith("messageTextUnder,"):
                parts = ln.split(",", 5)
                parts[2] = vi_text  # full incl. tags, no suffix append
            else:  # message,
                parts = ln.split(",", 5)
                assert "," not in vi_text, f"ASCII comma in VI body line {i}; use U+201A '‚'"
                m = TAGSUF_RE.search(parts[2])
                suffix = m.group(0) if m else ""
                assert vi_text.count("<br>") == parts[2].count("<br>") - (1 if suffix == "<br> " else 0), \
                    f"<br> count mismatch line {i}"
                parts[2] = vi_text + suffix
            vi_lines.append(",".join(parts))
        else:
            vi_lines.append(ln)

    assert used == set(VI.keys()), f"unused VI keys: {set(VI.keys()) - used}"
    assert record_count == len(VI), f"record count {record_count} != {len(VI)}"

    out = ("\r\n" if has_crlf else "\n").join(vi_lines)
    OUT.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
    print(f"WROTE {OUT} | records={record_count} lines={len(vi_lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()

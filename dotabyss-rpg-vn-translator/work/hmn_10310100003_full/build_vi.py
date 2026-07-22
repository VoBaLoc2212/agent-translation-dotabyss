#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI asset for hmn_10310100003 by replacing EN text fields (EN-asset-is-English case).

Strategy: read EN asset, for each text-command line replace the text field (index 2 for
message*/messageTextUnder, index 1 for title) with the Vietnamese translation. Speaker label
(field 1) and all technical trailing fields are preserved byte-for-byte. BOM + CRLF preserved.
`<br>` counts are mirrored from the EN asset (authoritative). ASCII commas inside VI -> U+201A.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10310100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10310100003.txt"

# line_number -> VI text field (already includes the authoritative `<br>` suffix where the
# EN asset had one). Duplicate EN fields (71/296, 403/670, 1913/2003) get the same VI.
VI_TEXT = {
    21: "Nơi Ân Nghĩa Và Trung Nghĩa",
    71: "Grr...!<br> ",
    296: "Grr...!<br> ",
    109: "(Thân thể ta không cử động được…! Chẳng lẽ máu chảy quá nhiều rồi sao…?<br>Đến mức này‚ ta sẽ ngã khỏi cây và thành mồi cho sói…)<br> ",
    111: "(Chẳng lẽ ta chết ở chốn này sao…? Thật uổng phí…)<br> ",
    126: "Xin lỗi… Phụ vương‚ mẫu thân…<br> ",
    178: "Thiếu Chủ!<br> ",
    209: "Cái gì…!?<br> ",
    211: "Chẳng lẽ… Hatsune‚ là cậu sao…? Sao cậu lại ở đây…!?<br> ",
    255: "Tôi sẽ giải thích sau! Xin hãy đợi một chút!<br> ",
    347: "Giờ thì‚ này ác thú! Đến đi! Tôi sẽ là đối thủ của ngươi!<br> ",
    349: "Hatsune…! Cẩn thận‚ con quái thú đó nguy hiểm lắm!<br> ",
    354: "Đã rõ!<br> ",
    403: "Grr!<br> ",
    670: "Grr!<br> ",
    448: "(Nhanh thật…! Nhưng mà—)<br> ",
    521: "Grr!?<br> ",
    577: "Đừng tưởng bắt được ta dễ dàng như vậy!<br> ",
    586: "Grrrrr…!<br> ",
    630: "Đến đi…! Ta sẽ khiến ngươi hối hận vì đã làm Thiếu Chủ bị thương!<br> ",
    728: "Ối!<br> ",
    834: "Hatsune liên tục lách né móng vuốt và hàm răng của sói<br>trong gang tấc.<br> ",
    880: "Hả! Chỉ có thế thôi sao!<br> ",
    921: "Grrrrr…!<br> ",
    978: "(Ta cứ né đòn mãi‚ nên nó ngày càng bực mình rồi…<br>Đến lúc rồi đây.)<br> ",
    1023: "Grr… Grr!<br> ",
    1067: "Ối! Nhìn gì thế! Tôi ở đây này…<br> ",
    1099: "Hatsune định lách người tránh cú lao của sói‚<br>nhưng đột ngột mất thăng bằng.<br> ",
    1110: "Chết tiệt! Khỉ thật‚ tôi vấp phải rễ cây rồi!<br> ",
    1171: "Grr!<br> ",
    1173: "Con sói lao vào Hatsune đang mất thăng bằng!<br> ",
    1175: "H-Hatsune! Coi chừng!<br> ",
    1239: "…Chỉ đùa thôi!<br> ",
    1268: "Nghe này‚ trước tiên hãy thu hút sự chú ý của con sói đó. Trong lúc đó‚ tôi sẽ giăng bẫy.<br> ",
    1279: "Bẫy…?<br> ",
    1281: "Ừ. Mấy cái cây quanh đây cành mềm lại dẻo dai dễ uốn.<br>Thêm nữa‚ dây leo cũng rất nhiều.<br> ",
    1283: "Dùng cành cây‚ dây leo‚ và bất cứ dụng cụ nào có sẵn kết hợp lại‚<br>chúng ta sẽ giăng được một cái bẫy đơn giản để bắt con sói đó.<br> ",
    1294: "Cậu thật sự làm được sao…?<br> ",
    1296: "Nhưng con sói đó khá thông minh. Kotono bị nó đánh úp cũng vì<br>nó tấn công từ hướng xuôi gió.<br> ",
    1298: "Có lẽ nếu ta dẫn thẳng nó vào bẫy‚ nó sẽ nghi ngờ<br>và không có tác dụng đâu.<br> ",
    1300: "Đấy‚ lúc đó chính là lượt của em.<br> ",
    1311: "Tôi…?<br> ",
    1313: "Ừ. Với những động tác của em ở sân tập‚ em hoàn toàn có thể<br>tiếp tục lách né đòn của con sói. Thế nào?<br> ",
    1340: "Chuyện đó… Ừ! Tôi nghĩ mình làm được.<br> ",
    1342: "Tốt. Vậy thì cứ thẳng tay chọc giận và dắt mũi nó đi. Rồi lúc nó<br>nổi điên lên…<br> ",
    1353: "Đấy mới là lúc giăng bẫy!<br> ",
    1355: "Đúng vậy. Thành bại của kế hoạch này là do em đấy.<br> ",
    1357: "—Chính em mới là người cứu Thiếu Chủ.<br> ",
    1369: "…<br> ",
    1380: "Ừ… tất nhiên rồi! Tôi sẽ làm!<br> ",
    1423: "(Nó đã nổi điên lên và sập bẫy quá dễ dàng!)<br> ",
    1449: "Ngay bây giờ!<br> ",
    1497: "Con sói lao về phía Hatsune bị dây leo thực vật quấn lấy chân‚<br>và bị treo lơ lửng trên không—!<br> ",
    1532: "Gyaow! Grr! Grr‚ grr…!<br> ",
    1543: "—Dù ngươi có gào thế nào‚ cũng đã muộn rồi.<br> ",
    1581: "Hãy chuẩn bị đi!<br> ",
    1619: "Xẹt—!<br> ",
    1621: "Gyaow…!<br> ",
    1670: "Được rồi‚ kế hoạch thành công! Đúng như dự đoán‚ Hatsune. Giỏi lắm—<br> ",
    1716: "Ồ…!<br> ",
    1750: "Ối! Này‚ sao tự dưng ôm lấy tôi thế…?<br> ",
    1763: "Tuyệt quá‚ cậu! Cậu đã hạ gục kẻ mà ngay cả Kotono cũng từng thất bại<br>trước đó!<br> ",
    1765: "Hiểu rồi‚ hiểu rồi. Bình tĩnh lại đã‚ được không?<br> ",
    1776: "Ahaha! Tôi cảm thấy như cùng với cậu thì có thể đánh bại bất kỳ kẻ thù nào!<br> ",
    1795: "…Hức! Đúng rồi‚ Thiếu Chủ!<br> ",
    1830: "Hatsune…<br> ",
    1841: "Thiếu Chủ! Ngài không sao chứ? Phải mau chữa trị vết thương thôi…<br> ",
    1843: "Ah‚ tôi đã cầm máu rồi. Tôi mang ơn cậu‚ Hatsune. Và<br>người kia…<br> ",
    1845: "Tôi là %user%.<br> ",
    1847: "Chỉ Huy…?<br> ",
    1849: "…Không biết chừng‚ ngài có phải Chỉ Huy của Căn Cứ Tiền Tuyến không?<br> ",
    1851: "Đại loại vậy.<br> ",
    1862: "Nói mới nhớ‚ họ đúng là gọi ngài như vậy. 'Chỉ Huy' là chức vụ gì vậy?<br> ",
    1864: "Hatsune‚ cậu không biết sao…? Ngài ấy là người nắm toàn quyền<br>của Căn Cứ Tiền Tuyến đấy.<br> ",
    1883: "Ê!? T-thật ư! Hình như mình đã vô lễ mà không hay biết…<br> ",
    1885: "Không sao cả. Giờ đổi thái độ thì cũng thấy kỳ kỳ đấy.<br> ",
    1896: "Ồ‚ thật sao? Hehe‚ dù ngài là đại nhân vật thế kia mà vẫn giúp đỡ chúng tôi.<br>Cậu đúng là người tốt‚ Chỉ Huy!<br> ",
    1898: "Nhờ ngài‚ mạng sống của tôi đã được cứu. Tôi biết lấy gì để đền đáp…<br> ",
    1900: "Đừng bận tâm. Kết quả là ta đã tiêu diệt được một quái vật nguy hiểm‚<br>và giảm thiểu được thương vong. Kết thúc tốt đẹp là được rồi.<br> ",
    1902: "Ngài thật là người rộng lượng… So với ngài thì tôi còn<br>phải học nhiều lắm.<br> ",
    1913: "Thiếu Chủ…<br> ",
    2003: "Thiếu Chủ…<br> ",
    1925: "…Tôi nhặt được trên đường. Trả lại cho ngài này.<br> ",
    1953: "Con đoản đao phụ thân ban cho…<br> ",
    1964: "Hãy trở về Hourai đi‚ Thiếu Chủ.<br>Chúa tể cũng đang đợi ngài trở về.<br> ",
    1966: "Hatsune… Một kẻ như ta có xứng đáng cầm đoản đao này không?<br> ",
    1977: "Tất nhiên rồi.<br>Ngài chính là người sẽ trở thành người đứng đầu gia tộc…<br> ",
    1979: "Tôi gặp Kotono ở Căn Cứ Tiền Tuyến và được cô ấy chỉ dạy‚ tưởng mình đã mạnh lên.<br>Nhưng thực tế lại yếu kém thế này… Ta không còn mặt mũi nào gặp phụ thân.<br> ",
    1990: "Thiếu Chủ… ngài nói gì thế…<br> ",
    1992: "Xin lỗi‚ Hatsune. Có lẽ ta vẫn chưa thể về Hourai.<br>Ta muốn ở lại Căn Cứ Tiền Tuyến thêm một thời gian để tiếp tục tu luyện.<br> ",
    2026: "Tôi hiểu rồi.<br>Vậy thì‚ tôi‚ Hatsune‚ sẽ đi theo hầu hạ ngài đến Căn Cứ Tiền Tuyến luôn!<br> ",
    2028: "Ta hiểu… Xin lỗi nhé‚ Hatsune.<br>Có em ở bên‚ ta thấy yên tâm hơn nhiều.<br> ",
    2039: "Tôi sẽ bảo vệ ngài khỏi mọi nguy hiểm!<br>Trước tiên‚ hãy trở về Căn Cứ Tiền Tuyến để chữa trị vết thương đã.<br> ",
    2075: "Sau đó‚ %user% và những người khác đã trở về an toàn Căn Cứ Tiền Tuyến.",
    2107: "Nghe tốt đấy. Chàng trai đó mất nhiều máu nhưng nghe nói mạng sống không nguy hiểm.<br>Có vẻ khoảng một tuần là cậu ấy có thể cử động được.<br> ",
    2115: "Thật là nhẹ nhõm…<br> ",
    2149: "Chỉ Huy. Cảm ơn ngài rất nhiều.<br> ",
    2161: "Tôi không thể cứu được Thiếu Chủ chỉ một mình…<br>Tôi mang ơn cậu một món nợ lớn‚ Chỉ Huy.<br> ",
    2163: "Đừng bận tâm. Nếu không có em‚ ta đã mất đi một nhân tài quý giá.<br> ",
    2165: "Nên đừng coi đó là món nợ gì cả.<br> ",
    2176: "Không đời nào!<br>Một samurai trả ơn là chuyện đương nhiên!<br> ",
    2185: "Dù ngài có bảo không cần đi nữa‚<br>tôi cũng nhất định sẽ đền đáp!<br> ",
    2187: "Rồi rồi. Em đúng là đứa ngoan cố nhỉ?<br> ",
    2198: "Này‚ Chỉ Huy‚ tôi tính ở lại Căn Cứ Tiền Tuyến cùng Thiếu Chủ‚<br>nhưng mà…<br> ",
    2209: "Ơ… nếu không phiền‚ có thể cho tôi giúp ngài công việc lần nữa được không?<br> ",
    2216: "Tôi muốn trả món nợ‚ nhưng cũng bởi‚ chỉ cần ở đây thôi tôi cũng cảm thấy<br>mình có thể mạnh lên gấp bội!<br> ",
    2225: "Tôi nhất định sẽ trở nên có ích cho ngài‚ Chỉ Huy! Thế nào?<br> ",
    2227: "Gì cơ‚ ngài nghiêm túc hỏi thế khiến tôi tưởng có chuyện gì‚ hóa ra chỉ thế thôi à.<br> ",
    2229: "Tất nhiên‚ chẳng có lý do gì để từ chối. Có em ở đây là chỗ dựa tinh thần cho<br>Căn Cứ Tiền Tuyến rồi.<br> ",
    2240: "T-thật sao!? Ehehe‚ ngài đã nói vậy thì tôi đành chịu thôi.<br> ",
    2251: "Lúc ngài gặp khó‚ tôi sẽ ra tay trợ giúp! Nên là…<br> ",
    2262: "Từ nay về sau hãy tiếp tục sát cánh bên nhau nhé‚ Chỉ Huy!<br> ",
}

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def clean(line: str) -> str:
    return line.rstrip("\r\n")


def main() -> int:
    raw = EN.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)

    # Preflight: every text line must have a VI entry whose <br> count matches the EN text field.
    mismatches = []
    for i, rawline in enumerate(lines, 1):
        line = clean(rawline)
        if not line.startswith(TEXT_CMDS):
            continue
        if i not in VI_TEXT:
            mismatches.append(f"L{i}: MISSING_VI_ENTRY")
            continue
        if line.startswith("title,"):
            old_tf = line.split(",", 1)[1]
        else:
            old_tf = line.split(",", 5)[2]
        new_tf = VI_TEXT[i]
        if old_tf.count("<br>") != new_tf.count("<br>"):
            mismatches.append(
                f"L{i}: BR_MISMATCH en={old_tf.count('<br>')} vi={new_tf.count('<br>')} | EN={old_tf!r}"
            )
        if "," in new_tf:
            mismatches.append(f"L{i}: ASCII_COMMA_IN_VI")
        # placeholder sanity
        import re
        ph = re.compile(r"%\\w+%")
        if ph.findall(old_tf) != ph.findall(new_tf):
            mismatches.append(f"L{i}: PLACEHOLDER_MISMATCH en={ph.findall(old_tf)} vi={ph.findall(new_tf)}")

    if mismatches:
        print("PREFLIGHT FAILURES:")
        for m in mismatches:
            print("  " + m)
        return 1
    print(f"Preflight OK: {len(VI_TEXT)} text fields, all <br>/comma/placeholder checks passed.")

    out_lines = []
    for i, rawline in enumerate(lines, 1):
        line = clean(rawline)
        if line.startswith("title,"):
            parts = line.split(",", 1)
            parts[1] = VI_TEXT[i]
            out_lines.append(parts[0] + "," + parts[1])
        elif line.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
            parts = line.split(",", 5)
            parts[2] = VI_TEXT[i]
            out_lines.append(",".join(parts))
        else:
            out_lines.append(line)
    # restore line endings
    out = ("\r\n" if has_crlf else "\n").join(out_lines)
    if has_crlf:
        out += "\r\n"
    else:
        out += "\n"
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(("\xef\xbb\xbf" + out.encode("utf-8")) if has_bom else out.encode("utf-8"))
    print(f"Wrote {VI} (bom={has_bom}, crlf={has_crlf})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

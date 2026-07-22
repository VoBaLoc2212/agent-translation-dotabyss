#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI output for hmn_10280100003 by replacing EN text fields (EN-asset-is-English case).
JP primary meaning via ja.json; EN asset is structural authority (BOM/CRLF/delimiters/<br> count).
Commander/司令官 -> Chiet Huy. 女店長 -> kept as speaker label; in dialogue addressed as "co" (Commander) / "ngai" (herself to Commander).
Commas inside VI text use U+201A (‚). Title in Vietnamese Title Case.
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10280100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10280100003.txt"

# line_no (1-indexed in file) -> VI text field (including trailing "<br> " suffix where EN has it)
VI_TEXT = {
    20: "Lời Thề Hội Ngộ Giữa Tiếng Sóng",
    28: "Sạp hàng rách nát chúng ta bắt gặp ở Chợ chính là của chủ cửa hàng<br>nơi Emily từng làm việc.<br> ",
    30: "Chỉ Huy và Emily đã đưa chủ cửa hàng đến quán rượu và<br>bắt đầu nghe câu chuyện tỏ tường.<br> ",
    70: "Giờ thì‚ cựu chủ tiệm… tôi nghe Emily kể rằng vì đuổi theo kho báu mà một ngày nọ anh đã rời bỏ<br>cửa hàng ở Eldorana đi mất…<br> ",
    117: "Sếp ơi… em lo lắng lắm đấy‚ trời ạ!<br>Sao lúc ra đi anh chẳng nói năng gì với em vậy!<br> ",
    119: "Chuyện đó… em thật sự xin lỗi ngài.<br> ",
    121: "Một ngày… em nghe khách tại tiệm Eldorana nhắc đến Đại Huyệt‚<br>rồi nghe đủ thứ tin đồn xôm tận mũi về nó.<br> ",
    123: "Vậy là cô nôn nóng không chịu nổi nên bỏ tiệm đi luôn… đúng không?<br> ",
    125: "Ừm… kiểu vậy đó.<br>Em cứ bồn chồn nghĩ mình phải đến Đại Huyệt thật nhanh!<br> ",
    136: "Em dễ dàng hình dung cảnh sếp hối hả chạy đi trong lúc hoảng loạn‚ sếp ơi.<br> ",
    147: "Thế là anh đã đến tận Đại Huyệt… rốt cuộc thế nào rồi?<br> ",
    151: "Thất bại rồi. Không… thất bại ê chề luôn.<br> ",
    153: "Em chẳng có sức mạnh để đánh bại quái vật‚ nên định ít nhất cũng sẽ nhắm tới kho báu ở vùng nông của Đại Huyệt…<br>nhưng hình như cũng lắm kẻ nghĩ giống em.<br> ",
    155: "Đúng vậy. Hình như ngay sau khi Đại Huyệt vừa xuất hiện‚<br>rất nhiều kẻ đã xông vào tranh đoạt kho báu.<br> ",
    157: "Kho báu em nhắm tới đã bị lấy sạch‚ và em chẳng còn gì trên tay…<br>Giờ em chỉ mót nhặt đồ phế liệu quanh Đại Huyệt‚ sống lay lắt qua ngày thế này đây.<br> ",
    168: "Tình cảnh tệ thế kia… sao anh không quay về Eldorana? Tiệm vẫn còn nguyên đó mà‚<br>biết không?<br> ",
    170: "…Em bị mờ mắt trước cám dỗ của kho báu nên đột ngột đóng cửa tiệm để đi Đại Huyệt.<br>Em nghĩ chừng nào chưa giàu to thì chưa về được Eldorana.<br> ",
    172: "Ra cô cố chấp không chịu quay về‚ quá kiêu hãnh để lùi bước.<br>Không phải tôi không hiểu cảm giác đó‚ nhưng…<br> ",
    183: "Ôi thôi‚ anh đúng là bó tay.<br> ",
    194: "Này‚ sếp ơi. Nghỉ xíu đi‚ nhé? Đây là bữa cơm nhân viên em<br>vẫn ăn hằng ngày.<br> ",
    196: "Hả? K‚ không‚ em không thể nhận thế được…<br> ",
    201: "Gùùù… gruuu rùm rùm…<br> ",
    203: "Bụng của cựu chủ tiệm réo ầm ĩ.<br> ",
    214: "Fufu‚ anh đói bụng rồi phải không?<br>Đừng có nhịn‚ biết không?<br> ",
    216: "…Nghe tiếng đó rồi em chẳng giấu được nữa. Cảm ơn ngài‚ để em ăn chút.<br>Không biết bao lâu rồi em mới có bữa ăn ra hồn thế này…<br> ",
    218: "Mời ngài… nhai nhai.<br>Ngon quá… ngon thật sự… hàà~…<br> ",
    229: "Fufu‚ đây là bữa cơm nhân viên đặc biệt của quán này.<br>Rất vui vì anh thích nó!♪<br> ",
    231: "Ở Eldorana chúng em chỉ chuyên hải sản‚ nhưng căn cứ này tập hợp nguyên liệu và gia vị từ khắp thế giới.<br>Em nếm được vị sâu đậm chưa từng biết tới.<br> ",
    242: "Đúng vậy! Vị cay thoang thoảng làm rất tốt vai trò của nó—<br> ",
    251: "(Mặt cựu chủ tiệm đã hồng hào trở lại‚ và Emily trông vui vẻ.<br>Chắc hồi ở Eldorana hai người cũng nói chuyện thế này thôi.)<br> ",
    308: "Trời ơi… Emily‚ em quá tốt bụng rồi.<br>Làm chị hơi lo quá đó.<br> ",
    320: "Ehehe… xin lỗi nhé‚ Ludia.<br>Em thật sự rất thích được thấy mọi người mỉm cười.<br> ",
    331: "Hơn nữa‚ sếp đã cực kỳ chăm sóc em.<br> ",
    343: "Đúng đó‚ sếp thường làm những chuyện liều lĩnh bốc đồng như lúc nãy…<br>nhưng em chẳng tài nào ghét được chị ấy.<br> ",
    383: "Emily‚ rốt cuộc em vẫn dịu dàng nhỉ… dù nụ cười vô tư mà lắt léu mật độc<br>thì vẫn y như xưa.<br> ",
    388: "Tôi nghĩ Emily đã rất hiền lành‚ xem xét việc nơi cô ấy làm việc bỗng một ngày<br>bốc hơi mất.<br> ",
    390: "…Đúng là vậy thật.<br>Xin lỗi em… chị đã gây phiền toái quá nhiều cho em‚ Emily.<br> ",
    401: "Không sao đâu‚ thật mà. Gặp lại nhau thế này‚ em mừng lắm.<br> ",
    413: "Thế… sếp định tính sao từ giờ trở đi‚ sếp ơi?<br> ",
    415: "Về chuyện tương lai‚ tôi có một đề xuất.<br> ",
    426: "Hả? Chỉ Huy?<br> ",
    459: "*bùm‚ bùm‚ bùm!*<br> ",
    484: "Êyyy!<br> ",
    486: "C‚ đây là… cái gì vậy?<br> ",
    488: "Emily và cựu chủ tiệm tròn mắt nhìn đống đồ quý giá<br>được bày trên bàn.<br> ",
    490: "Đây là những thứ tôi mua gom ở Chợ hôm nay. Hãy bán chúng khéo léo để đổi<br>thành tiền.<br> ",
    499: "K‚ lúc nào anh…<br> ",
    501: "Tôi mua phòng khi tình cảnh như thế này xảy ra. Nếu không cần dùng thì<br>tôi dùng cho mình cũng được mà.<br> ",
    503: "Ý ngài là… em được nhận những thứ này sao…?<br> ",
    505: "Đừng có hiểu lầm. Không phải cho cô đâu. Là cho Emily đấy. Hãy về<br>Eldorana và dùng thứ này để tái thiết tiệm.<br> ",
    507: "Thà hèn mang nhuốc nhơ còn hơn đem đời mình ra bỏ vì cái ngạnh ngạnh kỳ quặc.<br>Hãy cố gắng sống đúng đắn vì cô ấy‚ dù phải hứng sỉ nhục. Đừng bao giờ làm Emily buồn nữa‚ rõ chưa?<br> ",
    509: "…Em hiểu rồi‚ em thề sẽ không bao giờ làm cô bé này khóc nữa.<br> ",
    530: "Chỉ Huy… cảm ơn ngài nhiều lắm…<br> ",
    532: "Cho em… nói chuyện riêng với Emily một lát được không?<br> ",
    534: "Được thôi‚ chắc hai đứa cũng có nhiều chuyện để nói. Emily‚ em ổn chứ?<br> ",
    545: "Vâng. Cảm ơn ngài‚ Chỉ Huy. Em đi đây.<br> ",
    576: "Emily… thật sự xin lỗi vì đã bắt em vất vả nhiều.<br> ",
    587: "Không sao đâu‚ sếp ơi. Đừng bận tâm nữa nhé.<br> ",
    594: "Hãy dùng những món quý giá đó thật tốt nhé? Tiệm này tuyệt vời mà‚<br>nên chị nhất định phải tái thiết nó đấy!<br> ",
    596: "Nói đến chuyện đó… Emily. Nếu em thích‚ thì quay lại<br>giúp chị tái thiết nhé?<br> ",
    607: "Hả…?<br> ",
    609: "Thật tình‚ chị chẳng dám mặt mũi nào nhìn em. Chị đã phản bội em‚ người đã cống hiến<br>cho tiệm nhiều hơn bất kỳ ai.<br> ",
    611: "Nhưng dù vậy‚ em vẫn không bỏ rơi chị. Em vẫn đối xử với chị y như<br>xưa. Điều đó làm chị vui hơn bất cứ gì.<br> ",
    622: "Sếp ơi…<br> ",
    624: "Emily. Có em‚ chị tin chúng ta sẽ làm 'Hãy Lắng Nghe Tiếng Sóng'<br>trở lại như xưa… không‚ còn sung túc gấp bội.<br> ",
    626: "Thế… em thấy sao?<br> ",
    651: "Sếp ơi… cảm ơn anh. Em thật vui khi được nghe anh nói vậy‚ thật sự.<br> ",
    662: "Nhưng… em xin lỗi anh.<br> ",
    673: "Em có người bên cạnh ngay lúc này… người em muốn làm cho vui<br>hơn bất cứ ai khác.<br> ",
    675: "Người đó‚ chẳng lẽ là…? Không‚ chị không bới móc đâu.<br> ",
    680: "Thế thì chị sẽ về Eldorana‚ dốc sức tái thiết tiệm. Lúc về quê ghé qua nhé.<br>Chị sẽ nấu cho em một bữa cực ngon.<br> ",
    691: "Wa♪ ehehe… em hiểu rồi. Em rất mong được nếm món sếp nấu đấy♪<br> ",
    760: "Xin lỗi phải đợi lâu!<br> ",
    762: "Em đến muộn quá. Mọi chuyện ổn chứ?<br> ",
    773: "Vâng! Lâu lắm rồi mới gặp lại‚ nên em cứ luyên thuyên<br>nói chuyện mãi.<br> ",
    784: "Thế còn chủ tiệm thì sao?<br> ",
    796: "Chị ấy bảo 'ngày mai sẽ về Eldorana'‚ rồi hăng hái<br>rẽ đi mất rồi.<br> ",
    807: "Chị ấy nhiều tật xấu… nhưng lúc cần thì chị ấy làm nghiêm túc‚<br>nên em tin chị ấy sẽ làm tiệm lại sung túc như xưa.<br> ",
    809: "Tôi cứ tưởng chị ấy mời em quay lại Eldorana… em<br>từ chối rồi à?<br> ",
    857: "Hả… t‚ tuyệt quá‚ Chỉ Huy! Sao ngài lại biết được vậy!?<br> ",
    859: "Một người từng làm dưới chị ấy mà lúc túng quẫn lại dịu dàng với chị đến thế…<br>nếu tôi ở vị trí chủ tiệm‚ tôi nhất định sẽ mời em ấy quay lại.<br> ",
    868: "Ha~‚ ra là thế… Chỉ Huy thông minh thật đấy~…<br> ",
    880: "Đúng như ngài đoán‚ Chỉ Huy‚ sếp có mời em làm lại…<br>nhưng em đã từ chối.<br> ",
    882: "Thế tại sao lại thế?<br> ",
    893: "Đúng vậy‚ Eldorana và Tiền Tuyến Căn Cứ đều có những điểm hay riêng‚<br>nhưng…<br> ",
    904: "Nhưng với em… người em muốn làm vui nhất… chính là ngài‚<br>Chỉ Huy!♪<br> ",
    906: "Hả? Tôi à?<br> ",
    918: "Đúng vậy!♪<br> ",
    930: "Từ nay về sau‚ em sẽ nỗ lực hết mình để làm ngài thật nhiều nụ cười‚<br>Chỉ Huy!♪<br> ",
}

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def clean(s):
    return s.lstrip("\ufeff").rstrip("\r\n")

raw = EN.read_bytes()
assert raw[:3] == b"\xef\xbb\xbf", "EN missing BOM"
has_crlf = b"\r\n" in raw
text = raw.decode("utf-8-sig")
lines = [ln.rstrip("\r") for ln in text.split("\n")]
# drop trailing empty final element if present (file ends with \n)
if lines and lines[-1] == "":
    lines = lines[:-1]

out_lines = []
changed = 0
for i, line in enumerate(lines, 1):
    if i in VI_TEXT:
        vi = VI_TEXT[i]
        assert "," not in vi, f"ASCII comma in VI line {i}: {vi!r}"
        if line.startswith("title,"):
            parts = line.split(",", 1)
            old_tf = parts[1] if len(parts) > 1 else ""
            parts[1] = vi
            new_line = ",".join(parts)
        else:
            parts = line.split(",", 5)
            assert len(parts) >= 3, f"line {i} too few fields: {line!r}"
            old_tf = parts[2]
            parts[2] = vi
            new_line = ",".join(parts)
        # guard: <br> count must match EN text field
        old_br = old_tf.count("<br>")
        new_br = vi.count("<br>")
        assert old_br == new_br, f"LINE {i}: <br> count mismatch EN={old_br} VI={new_br}\nEN: {old_tf!r}\nVI: {vi!r}"
        out_lines.append(new_line)
        changed += 1
    else:
        out_lines.append(line)

assert changed == len(VI_TEXT), f"expected {len(VI_TEXT)} changes, got {changed}"

out = ("\r\n" if has_crlf else "\n").join(out_lines) + ("\r\n" if has_crlf else "\n")
VI.parent.mkdir(parents=True, exist_ok=True)
VI.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))
print(f"WROTE {VI}  lines={len(out_lines)} changed={changed} crlf={has_crlf}")

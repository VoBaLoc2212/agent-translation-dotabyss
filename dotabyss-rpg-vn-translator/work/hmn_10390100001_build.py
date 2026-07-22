#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build VI output for hmn_10390100001 from the EN asset (EN-asset-is-English case).

title field is still JP; message/messageTextCenter fields are English.
We translate ONLY the text field, preserving every technical field (voice id,
chara keys, tags, placeholders), the <br> count, BOM and CRLF exactly.
Vietnamese commas use U+201A (‚) instead of ASCII comma.
"""
import importlib.util

EN = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10390100001.txt"
VI = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10390100001.txt"

# Full authored translated line per line number (1-based). Only text-command lines.
VI_LINES = {
    19: "title,Mong Cứu Rỗi Bằng Giáo Lý Của Chúa",
    33: "message,<user>,Chà... Thật bực mình!<br> ",
    44: "message,アリシア,C-chẳng lẽ ngài vẫn còn bực tức sao ạ?<br> ",
    46: "message,<user>,Đương nhiên! Anh nghe nói có chỗ bán nước ép ngon lắm‚ nên anh đã đi‚<br>nhưng—<br> ",
    48: "message,<user>,Người ta chen hàng‚ đưa sai tiền thừa‚ còn nước ép thì<br>ra bị pha loãng bằng đá!<br> ",
    59: "message,アリシア,Hay là do nổi tiếng nên cách quản lý của họ đổi rồi nhỉ...?<br> ",
    61: "message,<user>,Đúng là vậy‚ nhưng... ngày tệ thế này—*lầm bầm‚ lầm bầm‚ lầm bầm‚<br>lầm bầm‚ lầm bầm‚ lầm bầm‚ lầm bầm*<br> ",
    114: "message,アリシア,(Ái... chuyện này kéo dài mãi mất... cứu tôi với...)<br> ",
    180: "message,？？？,Xin lỗi. Ngài có một chút thời gian không ạ?<br> ",
    182: "message,<user>,Cái gì?<br> ",
    224: "message,？？？,Tôi nghe lóm một chút cuộc trò chuyện của ngài... Có chuyện chẳng lành<br>gì sao?<br> ",
    226: "message,<user>,...Ừ‚ đúng vậy. Đây là ngày tệ nhất từ trước đến nay.<br> ",
    237: "message,？？？,Thật đáng tiếc. Nếu ngài không phiền‚ có thể kể cho tôi nghe chuyện gì<br>đã xảy ra không ạ?<br> ",
    248: "message,マーガレット,Tôi tên là Margaret. Chỉ là một nữ tu khiêm tốn... nhưng tôi nghĩ mình<br>có thể giúp ngài trấn tĩnh tâm trạng.<br> ",
    250: "message,<user>,Người của nhà thờ à... Thật tình‚ lúc này anh chỉ muốn than trách với<br>Chúa hay ai đó thôi.<br> ",
    306: "message,アリシア,C-Chỉ Huy. Em hiểu cảm giác của ngài‚ nhưng nói vậy có hơi quá<br>không ạ?<br> ",
    313: "message,マーガレット,Hư hư. Tôi chẳng hề phiền chút nào. Tôi cũng muốn ngài hướng những cảm xúc ấy về<br>phía tôi nữa.<br> ",
    324: "message,マーガレット,Trên đời này chẳng có gì là vô nghĩa. Đón nhận những cảm xúc nảy sinh tự<br>nhiên‚ đúng như bản chất của chúng‚ chính là tín điều của tôi.<br> ",
    335: "message,アリシア,Ra là vậy... Chỉ Huy! Vì chúng ta ở đây rồi‚ sao ngài không kể cho cô ấy<br>nghe nhỉ? Đúng không ạ?<br> ",
    337: "message,<user>,Hừm...<br> ",
    385: "message,アリシア,Chỉ Huy!<br> ",
    387: "message,<user>,Được rồi. Anh cũng chẳng mấy hào hứng‚ nhưng nếu Alicia đã nài nỉ‚ anh sẽ nghe cô ấy nói.<br> ",
    442: "message,マーガレット,Cảm ơn ngài. Tôi sẽ dẫn ngài đến nhà thờ ngay kia‚ nên xin ngài cứ tự<br>nhiên nói chuyện.<br> ",
    470: "messageTextCenter,,<size=48>——Vài Phút Sau——</size>,,,on",
    516: "message,マーガレット,Ồ. Thế ra ngài là Chỉ Huy của căn cứ này sao.<br> ",
    527: "message,マーガレット,Ngài vừa hoàn thành một nhiệm vụ vất vả và đang định nghỉ ngơi thì xui<br>xẻo ập tới‚ tôi hiểu rồi.<br> ",
    529: "message,<user>,Ừ. ...Chết tiệt. Nói ra lại làm anh bực lên lần nữa rồi.<br> ",
    541: "message,マーガレット,Tôi thấu hiểu ngài. Nhưng thưa Chỉ Huy‚ ngài có thể nhìn nhận theo<br>hướng này không ạ?<br> ",
    568: "messageTextCenter,,<size=48>——Vài Phút Sau——</size>,,,on",
    605: "message,<user>,Haha‚ ha ha ha! Cô nói hoàn toàn đúng‚ Margaret! Chuyện nãy chẳng có gì<br>to tát cả!<br> ",
    659: "message,アリシア,Ê ê! Chỉ Huy!<br> ",
    661: "message,<user>,Có chuyện gì thế‚ Alicia?<br> ",
    672: "message,アリシア,Chỉ Huy! C-ngài bị làm sao vậy?! Trông ngài khác hẳn với Chỉ Huy<br>bình thường!<br> ",
    674: "message,<user>,...Ừ‚ có thể nói anh đã là một người khác so với lúc nãy.<br>Lời của Margaret đã lay động anh nhiều đến thế đấy.<br> ",
    686: "message,マーガレット,Hư hư hư. Nhưng tôi có nói gì đặc biệt đâu.<br> ",
    697: "message,アリシア,C-ừm‚ đúng vậy... Em cũng thấy đó là một bài thuyết giáo tuyệt vời‚ nhưng<br>em không ngờ nó lại lay động ngài đến thế...<br> ",
    708: "message,マーガレット,Điều đó cho thấy Chỉ Huy đã dồn nén bao nhiêu uất ức bấy lâu<br>nay.<br> ",
    710: "message,<user>,Ha ha ha. Trời ơi‚ xấu hổ quá.<br> ",
    712: "message,<user>,Càng nghĩ anh càng nhận ra mình đã nổi giận vì một chuyện vụn vặt<br>như thế.<br> ",
    714: "message,<user>,Nước ép vừa lạnh vừa ngon‚ nhân viên đã xin lỗi‚ còn tặng thêm cả vé số<br>miễn phí.<br> ",
    716: "message,<user>,Vé số không trúng‚ nhưng anh đã cảm nhận được tấm lòng tốt của họ rồi—còn<br>đòi hỏi gì hơn nữa?<br> ",
    773: "message,アリシア,(Ôi thôi‚ những gì cậu ấy nói nghe có vẻ hay ho đấy‚ nhưng em hoàn<br>toàn không yên tâm... đây chẳng phải Chỉ Huy bình thường...)<br> ",
    824: "message,<user>,Nhìn chung‚ chuyến mua sắm cũng tốt—<br> ",
    826: "message,<user>,…<br> ",
    852: "message,<user>,Khoan—không‚ nói vậy sao rồi!<br> ",
    900: "message,アリシア,Á á! S-sao cậu đột nhiên bùng nổ thế!?<br> ",
    902: "message,<user>,Anh đã bị thao túng một cách tinh vi‚ nhưng anh đâu dễ dàng đổi ý như<br>vậy!<br> ",
    913: "message,アリシア,À‚ cậu đã trở lại bình thường rồi.<br> ",
    964: "message,アリシア,Nhưng em muốn nói lời của Margaret mạnh mẽ đến mức tạm thời thay đổi<br>cách nhìn của ngài sao?<br> ",
    968: "message,<user>,...Đúng vậy. Margaret‚ cô thực ra là một nữ tu nổi tiếng hay<br>sao?<br> ",
    979: "message,マーガレット,Không‚ không phải vậy. Tôi chẳng có thành tựu gì đặc biệt.<br> ",
    984: "message,マーガレット,Nhưng trong gia tộc tôi có vài vị tu sĩ nổi tiếng. Biết đâu gia tộc chúng<br>tôi được Chúa ban phước.<br> ",
    995: "message,アリシア,Ra là vậy... nhưng cách cô lắng nghe và nói chuyện‚ Margaret ơi‚ thật<br>dịu dàng.<br> ",
    1006: "message,アリシア,Không phải do gia tộc hay dòng máu đâu; em cảm thấy chính cô có tài dẫn<br>dắt người khác!<br> ",
    1017: "message,マーガレット,Hư hư‚ cảm ơn ngài. Lời ngài nói làm tôi phấn chấn.<br> ",
    1019: "message,<user>,Anh không thể phủ nhận tài năng ấy. Nếu không‚ anh đã chẳng dễ dàng bị<br>lay động đến thế.<br> ",
    1021: "message,<user>,Thật tình‚ điều đó gần như đáng sợ. Nó khiến anh phải dè chừng khi lại<br>gần.<br> ",
    1065: "message,アリシア,Hả? Chỉ Huy‚ lẽ ra ngài mới là người nên nghe Margaret nói thường xuyên<br>hơn chứ?<br> ",
    1067: "message,<user>,Ồ? Em thích làm việc với 'tôi ngoan' suốt sao? Thế thì mới đáng lo đấy‚<br>đúng không?<br> ",
    1078: "message,アリシア,C-thỉnh thoảng thôi! Ý em là‚ thỉnh thoảng vẫn cần mà!<br> ",
    1124: "message,マーガレット,Hư hư‚ đúng vậy.<br> ",
    1168: "message,マーガレット,Thưa Chỉ Huy. Xét đến công việc của ngài‚ tôi hiểu ngài phải cân nhắc<br>những ý tưởng phi chính đạo. Nhưng chỉ riêng điều đó thôi cũng có thể dẫn đến lúc tâm trí căng thẳng‚ như vừa rồi.<br> ",
    1179: "message,マーガレット,Khi chuyện đó xảy ra‚ hãy tìm đến tôi. Ngài không cần thay đổi<br>suy nghĩ—chỉ cần gột sạch tâm trí một chút thôi. Thế là đủ.<br> ",
    1181: "message,<user>,...Ra là vậy. Và thật tình‚ sự bực dọc của anh đã nguôi đi‚ nên có lẽ sẽ<br>có lúc anh nên trông cậy vào cô.<br> ",
    1235: "message,アリシア,Margaret ơi‚ cô sẽ ở lại Căn Cứ Tiền Tuyến một thời gian sao?<br> ",
    1242: "message,マーガレット,Đúng là kế hoạch vậy. Hôm nay tôi tình nguyện từ Milesgard đến đây để<br>tìm một người quen‚ nên tôi vừa mới tới.<br> ",
    1253: "message,マーガレット,Trong lúc tìm người quen‚ tôi cũng mong mang sự cứu rỗi đến cho những<br>người sinh sống tại Căn Cứ Tiền Tuyến qua giáo lý của Chúa.<br> ",
    1264: "message,マーガレット,Lắng nghe nỗi lòng của Chỉ Huy cũng là một phần công việc của tôi.<br>Ngài cứ tự nhiên ghé qua bất cứ lúc nào.<br> ",
    1266: "message,<user>,...Tâm hồn đó thật đáng khâm phục‚ nhưng cô có ổn không đấy?<br> ",
    1277: "message,アリシア,...Em cũng hơi lo.<br> ",
    1288: "message,アリシア,Căn Cứ Tiền Tuyến có nhiều người từ các quốc gia khác‚ bắt đầu từ<br>Perdion. Em từng thấy có người nóng tính hơn cả ngài...<br> ",
    1299: "message,アリシア,Em e rằng sẽ có lúc mọi chuyện không suôn sẻ...<br> ",
    1310: "message,マーガレット,Cảm ơn sự lo lắng của em.<br> ",
    1317: "message,マーガレット,Nhưng không sao đâu. Tôi thấu rõ tình hình. Con đường gian nan không<br>phải lý do để bỏ cuộc.<br> ",
    1363: "message,マーガレット,Hơn nữa‚ tôi không tin ai cũng chối bỏ giáo lý của Chúa.<br> ",
    1375: "message,マーガレット,Có những người hiền hòa như Alicia‚ và sẽ có người lắng nghe tôi‚ như<br>Chỉ Huy.<br> ",
    1386: "message,マーガレット,Tôi sẽ không cố tiếp cận tất cả mọi người cùng lúc. Tôi sẽ lan tỏa giáo lý<br>của Chúa từng bước‚ từng bước một.<br> ",
    1440: "message,アリシア,...Em hiểu rồi. Em ủng hộ cô! Đúng không‚ Chỉ Huy?<br> ",
    1442: "message,<user>,Ừ‚ đúng vậy. Có vẻ cô ấy giỏi cả việc lắng nghe lẫn nói chuyện‚ nên anh<br>nghĩ thử thách của cô ấy có ý nghĩa.<br> ",
    1453: "message,アリシア,Margaret ơi‚ nếu cô gặp khó khăn gì‚ cứ việc tìm đến bọn em<br>nhé!<br> ",
    1499: "message,マーガレット,Cảm ơn ngài. Tôi sẽ cố hết sức.<br> ",
    1514: "message,<user>,(...Cô ấy đúng là một nữ tu hoàn hảo. Mong mọi chuyện suôn<br>sẻ—anh sẽ để mắt đến cô ấy.)<br> ",
}


def text_field_of(authored):
    """Extract the translatable text field from an authored full line."""
    if authored.startswith("title,"):
        return authored.split(",", 1)[1]
    return authored.split(",", 5)[2]


def rebuild(en_line, vi_text, is_title):
    """Replace the text field of an EN line, keeping all technical fields."""
    if is_title:
        p = en_line.split(",", 1)
        p[1] = vi_text
        return ",".join(p)
    p = en_line.split(",", 5)
    p[2] = vi_text
    return ",".join(p)


TEXT = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
raw = open(EN, "rb").read()
en_text = raw.decode("utf-8-sig")
en_lines = en_text.splitlines(keepends=True)  # keep line endings -> matches verifier
en_text_records = sum(1 for l in en_lines if l.startswith(TEXT))
assert en_text_records == len(VI_LINES), f"record count {en_text_records} != {len(VI_LINES)}"

# Preflight: <br> counts and ascii comma in text field
for i, ln in enumerate(en_lines, 1):
    if i in VI_LINES:
        vt = text_field_of(VI_LINES[i])
        en_br = ln.count("<br>")
        vi_br = vt.count("<br>")
        assert en_br == vi_br, f"BR MISMATCH L{i} en={en_br} vi={vi_br}"
        assert "," not in vt, f"ASCII COMMA IN TEXT L{i}: {vt[:60]!r}"

out = []
for i, ln in enumerate(en_lines, 1):
    if i in VI_LINES:
        is_title = ln.startswith("title,")
        vt = text_field_of(VI_LINES[i])
        new_core = rebuild(ln.rstrip("\r\n"), vt, is_title)
        # preserve the original line ending (CRLF) of this line
        ending = ln[len(ln.rstrip("\r\n")):]
        out.append(new_core + ending)
    else:
        out.append(ln)

result = "".join(out)
open(VI, "wb").write(b"\xef\xbb\xbf" + result.encode("utf-8"))
print("WROTE", VI, "lines:", len(out), "text_records:", len(VI_LINES))

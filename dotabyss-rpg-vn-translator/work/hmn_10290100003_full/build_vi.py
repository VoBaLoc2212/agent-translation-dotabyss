#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build VI output for hmn_10290100003 from EN asset, translating JP->VI.

EN-asset-is-English case: en.json holds English, EN asset text is English.
We translate each text field (title/messageTextCenter/message) into Vietnamese,
preserving BOM, CRLF, <br> counts, tags, %user%, delimiters, and speaker labels.
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100003.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100003.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10290100003_full"
WORK.mkdir(parents=True, exist_ok=True)

# VI text field per EN asset 1-based line number.
# Bear SFX localised to Vietnamese onomatopoeia (Gâu/Gừ) so records change.
VI_TEXT = {
    32: "Vỗ Về Bằng Bánh Ngọt Ngào",
    42: "<size=48>Một Vài Tháng Sau</size>",
    88: "Nghĩ lại thì‚ tôi nghe nói Myrtille đã thắng Cuộc Thi Bánh Ngọt được<br>tổ chức hồi nãy rồi đó.<br> ",
    99: "Một chiếc bánh tart việt quất giản đơn‚ nhưng chính vì thế mà tài nghệ của người làm mới<br>thể hiện rõ. Chất lượng ấy đã mê hoặc các giám khảo‚ tôi nghe nói thế!<br> ",
    101: "Bánh tart đó ư? Đương nhiên. Nó ngon tuyệt mà.<br> ",
    112: "...? Chỉ Huy‚ nghe như anh đã nếm thử rồi vậy?<br> ",
    114: "Tôi từng là cố vấn của cô ấy mà.<br>Tôi đã nếm thử từ bản thử nghiệm cho đến thành phẩm hoàn chỉnh.<br> ",
    150: "Cái gì?! Anh làm vậy mà không có em? Thật không công bằng!<br> ",
    161: "Dù anh là Chỉ Huy thì em cũng chẳng tha đâu! Cách xin lỗi thì‚<br>phải đưa em đi tiệm của Myrtille!<br> ",
    163: "...Tiệm của cô ấy ư? Cô ấy mở tiệm mới sao?<br> ",
    174: "Vâng. Có quá nhiều lời yêu cầu được nếm thử chiếc bánh tart chiến thắng nên cô ấy<br>đã quyết định mở một tiệm bánh ngọt.<br> ",
    185: "Giờ nó đã thành hit lớn! Có một hàng dài người xếp hàng!<br> ",
    187: "...Vậy anh muốn em xếp hàng chờ à?<br> ",
    199: "Một mình chán lắm. Chỉ Huy‚ anh đi cùng em nhé!<br> ",
    201: "...Thôi được. Anh chưa chúc mừng cô ấy khai trương‚ nên ghé qua một chút vậy.<br> ",
    258: "Kia là tiệm của Myrtille này. Mọi người vẫn đang xếp hàng như mọi khi!<br> ",
    260: "Cuối hàng ở đằng kia. Chúng ta cứ xếp hàng lặng lẽ thôi.<br> ",
    314: "...Hử? Nếu không phải Chỉ Huy với Alicia thì là ai. Chắc hai người không cần xếp hàng<br>chờ đâu nhỉ?<br> ",
    316: "Phần thú vị của tiệm đông khách chính là được nếm trải cảm giác xếp hàng chờ đợi.<br>Đúng không‚ Alicia?<br> ",
    364: "Vâng‚ bọn em cũng xếp hàng luôn! Đây là cuối hàng nè!<br> ",
    407: "...Gâu.<br> ",
    424: "Ồ‚ anh cũng sẽ xếp hàng à? Thế thì mời anh xếp sau em nhé.<br> ",
    469: "...Hử? Vừa rồi là cái gì...?<br> ",
    491: "Với những bước chân nặng nề‚ ục ịch‚ một con gấu to lớn ngồi phịch xuống tận<br>cuối hàng.<br> ",
    537: "Gìa! Gấu ơi!<br> ",
    547: "Và nó to thật...! Nó thực sự lẻn vào tận đây sao?<br> ",
    593: "Aaaa! Gấu kìa! Chạy đi! Chúng ta sẽ bị ăn mất!<br> ",
    644: "Ôi‚ mọi người làm ầm lên thế này‚ chuyện gì vậy?<br> ",
    655: "Iiii! Có một anh gấu to bự ngay trước tiệm kìa!<br> ",
    702: "Gừ!<br> ",
    704: "Chú gấu tỏ ra bối rối khi mọi người tháo chạy và Myrtille đứng sững sờ.<br>%user% nhận ra cử chỉ đáng yêu ấy.<br> ",
    706: "Hử...? Không lẽ‚ là cậu...<br> ",
    748: "Chỉ Huy‚ Alicia‚ nguy hiểm đấy! Chạy đi!<br> ",
    786: "Mọi người‚ tránh xa con gấu đó ra! Tôi sẽ tiêu diệt nó!<br> ",
    790: "Gừ! Gừ!<br> ",
    792: "Khoan khoan khoan! Đừng giết con gấu này!<br> ",
    803: "Hử...? Nhưng nếu để mặc nó‚ nó có thể tấn công người dân thị trấn...<br> ",
    805: "Con gấu này là bạn của chúng ta mà. Đúng không‚ Myrtille?<br> ",
    847: "Hử...?<br> ",
    849: "Này‚ nhìn cái tai đó xem.<br> ",
    870: "Một vết cắn lớn ở tai phải! Không đời nào‚ là Gấu ơi!<br> ",
    874: "Gâu!<br> ",
    881: "Sao anh lại to thế này noóo!?<br> ",
    913: "Chà‚ thật là ồn ào.<br>Tại anh mà tôi lỡ mất cái bánh tart của Myrtille.<br> ",
    915: "Gâu u...<br> ",
    917: "Không cần xin lỗi đâu. Nhưng tôi đã bảo anh tránh mặt đi vì nguy hiểm<br>mà‚ đúng không?<br> ",
    919: "Gâu gâu u.<br> ",
    961: "Này‚ Gấu ơi... Anh lớn hẳn lên trong lúc Mil chuẩn bị mở tiệm‚<br>phải không?<br> ",
    965: "Gâu!<br> ",
    972: "Giờ anh to thế này‚ chắc chắn mạnh ngang ngửa mọi con gấu khác<br>rồi đúng không?<br> ",
    974: "Gâu gâu.<br> ",
    985: "Thế thì anh không cần tới chỗ Mil nữa cũng được mà‚ đúng không? Anh có thể sống<br>tự do trong rừng rồi!<br> ",
    1022: "Gâu! Gâu u‚ gâu gâu! Gâu u!<br> ",
    1024: "Bối rối‚ Gấu Lớn dùng móng vuốt chỉ qua chỉ lại giữa mình<br>và Myrtille. Có vẻ như nó đang van nài tuyệt vọng rằng‚ 'Chúng ta không phải bạn sao?'<br> ",
    1035: "Gấu ơi...! Ừ‚ Mil cũng muốn anh ăn bánh tart của cô ấy nữa mà!<br> ",
    1077: "Chỉ Huy... Không lẽ chúng ta không thể cho Gấu ơi vào căn cứ được sao‚ nhỉ?<br> ",
    1079: "Không.<br> ",
    1090: "Iiii!<br> ",
    1094: "Gâu u!<br> ",
    1096: "Anh trông chờ gì chứ! Nó đã lớn đến mức chỉ cần muốn là dễ dàng tấn công con người<br>rồi mà!<br> ",
    1098: "Hơn nữa‚ dù tôi có gật đầu thì người dân thị trấn chẳng bao giờ<br>chấp nhận đâu.<br> ",
    1140: "Nhưng... Gấu ơi không phải là gấu xấu mà...<br> ",
    1142: "Gừ r...<br> ",
    1144: "Nhưng nếu người dân thị trấn chấp nhận nó‚ tôi sẽ vui vẻ cho phép thôi.<br> ",
    1155: "Hử... Chỉ Huy...?<br> ",
    1157: "Chúng ta đã cùng ăn bánh tart với nhau mà! Để chiến thuật cho tôi!<br> ",
    1199: "Cảm ơn anh nhiều lắm!<br> ",
    1232: "<size=48>Một Vài Ngày Sau<br>Trước Tiệm Bánh Ngọt Của Myrtille</size>",
    1239: "Con gấu lớn tự ép mình ngồi lên chiếc ghế đặt trước tiệm<br>và khéo léo cắt bánh tart bằng dao và nĩa.<br> ",
    1283: "Cái gì thế‚ con gấu kia! Nó đang ăn bánh tart rất lịch sự!<br> ",
    1294: "Thân hình to lớn thế kia mà ăn lại nhỏ nhắn... Dễ thương quá!<br> ",
    1305: "Với lại‚ nó ăn trông ngon lành thế. Đến cả<br>tôi cũng bắt đầu thèm bánh tart rồi.<br> ",
    1316: "Con gấu này tài ghê! Nó được huấn luyện còn hơn cả con chó nhà tôi.<br> ",
    1360: "Hê‚ đúng như kế hoạch. Mọi người đều mê mệt vì sự đáng yêu của nó!<br> ",
    1362: "Mọi người‚ nghe này. Như các bạn thấy‚ nó là một con gấu ngoan và thông minh<br>đấy.<br> ",
    1364: "Tôi biết nó từ hồi nó còn là gấu con‚ và thực ra nó là một gã<br>khá thú vị.<br> ",
    1375: "Nó thật dịu dàng và tốt bụng! Tôi định biến nó thành gấu linh vật của tiệm<br>chúng ta đấy!<br> ",
    1386: "Mọi người‚ làm ơn chấp nhận nó nhé?<br> ",
    1390: "Gừ!<br> ",
    1445: "Khi con gấu giơ chân lên như muốn nói 'Hãy chăm sóc tôi nhé!'‚ người dân<br>không nhịn được cười dù vẫn bối rối.<br> ",
    1454: "Cái cử động quái chiêu gì thế? Dù là gấu to thế kia mà‚ nó vẫn làm người ta<br>cười được‚ đúng không?<br> ",
    1463: "Tôi chẳng hiểu cái vụ \"gấu linh vật\" này lắm‚ nhưng nếu<br>Chỉ Huy đã nói thế thì tôi sẽ thử xem sao.<br> ",
    1513: "Tốt quá...! Cảm ơn tất cả mọi người nhiều lắm!<br> ",
    1515: "Gâu‚ gâu!<br> ",
    1526: "Hôm nay‚ để kỷ niệm Gấu ơi gia nhập tiệm‚ Mil đang giảm giá lớn<br>các loại bánh tart! Mời mọi người ghé thưởng thức nhé!<br> ",
    1582: "Phù‚ Mil bận rộn quá đi!<br> ",
    1584: "Con gấu đó ăn bánh tart ngon lành thế kia nên ai cũng muốn nếm thử‚<br>tôi đoán vậy.<br> ",
    1588: "Gâu‚ gâu!<br> ",
    1590: "Ừ‚ anh cũng vất vả đấy. Anh làm tốt lắm—gọi mời‚ quảng cáo‚<br>và dỗ dành bọn trẻ.<br> ",
    1594: "Gâu u!♪<br> ",
    1596: "Con gấu gật đầu đầy tự hào‚ giơ chân lên‚ rồi lững thững bỏ đi. Nó sẽ ở trong<br>rừng nhưng thi thoảng lại ghé căn cứ chơi.<br> ",
    1598: "Có vẻ nó sắp thành linh vật của căn cứ rồi nhỉ.<br> ",
    1633: "Tất cả là nhờ anh‚ Chỉ Huy. Mil hơi ngạc nhiên một chút khi thấy<br>Gấu ơi‚ thế thôi.<br> ",
    1635: "Thôi‚ ai thấy gấu to thế cũng giật mình. Và cô‚<br>Myrtille‚ cô nhận ra ngay mà‚ đúng không?<br> ",
    1646: "Bởi vì anh bảo nó vẫn là Gấu ơi ngày nào‚ Chỉ Huy‚ nên<br>Mil mới biết đó chính là anh ấy!<br> ",
    1648: "Nhưng vì lúc đầu nó đáng sợ thế kia‚ giờ quen rồi nên nó trông càng đáng yêu<br>hơn. Tôi chắc chắn từ nay nó sẽ được mọi người yêu quý.<br> ",
    1659: "Nói thật với anh... lúc đầu‚ Mil cũng từng nghĩ anh hơi đáng sợ<br>đấy‚ Chỉ Huy.<br> ",
    1667: "Nhưng anh đã tha thứ cho Gấu ơi vì đã ăn trộm bánh‚ và còn lo lắng<br>về chuyện bánh tart nữa...<br> ",
    1678: "Và anh nhận ra Gấu ơi ngay lập tức dù nó đã lớn thế kia‚ rồi còn giúp<br>chúng tôi để hai đứa được ở bên nhau thêm lần nữa.<br> ",
    1685: "Dù anh trông có vẻ đáng sợ‚ Mil nhận ra ngay rằng anh thực ra là<br>một người tử tế và tuyệt vời!<br> ",
    1687: "A ha ha‚ vậy thì anh cũng giống hệt con gấu đó‚ nhỉ? Càng<br>đáng sợ lúc đầu thì càng trở nên cuốn hút bây giờ‚ đúng không?<br> ",
    1698: "...Không phải một trời một vực đâu‚ anh biết mà?<br> ",
    1706: "Gấu ơi là người bạn dễ thương và tốt bụng. Nhưng Chỉ Huy thì...<br> ",
    1717: "Mạnh mẽ và dịu dàng‚ là người Mil muốn đứng bên cạnh nâng đỡ... người Mil<br>yêu nhất.<br> ",
    1719: "Hả—!<br> ",
    1730: "A! Chỉ Huy‚ anh đang đỏ mặt kìa!<br> ",
    1732: "Khỉ thật‚ tại anh nói những điều xấu hổ trực diện như thế!<br> ",
    1734: "Khỉ thật‚ ngay cả lời nói của anh cũng ngọt ngào‚ Myrtille.<br> ",
    1746: "E hé hé!♪ Khi Chỉ Huy mệt‚ em sẽ luôn dỗ dành anh bằng những<br>món bánh ngọt ngào của em!<br> ",
    1757: "Vậy từ giờ‚ hãy cứ dựa vào Mil nhé‚ anh?<br> ",
}

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")


def count_br(s):
    return s.count("<br>")


def build():
    data = EN.read_bytes()
    has_bom = data.startswith(b"\xef\xbb\xbf")
    text = data.decode("utf-8-sig")
    has_crlf = "\r\n" in text
    segments = text.splitlines(keepends=True)

    out_segments = []
    issues = []
    for idx, seg in enumerate(segments, 1):
        if seg.endswith("\r\n"):
            nl = "\r\n"; content = seg[:-2]
        elif seg.endswith("\n"):
            nl = "\n"; content = seg[:-1]
        else:
            nl = ""; content = seg

        if content.startswith(TEXT_CMDS):
            if idx not in VI_TEXT:
                raise SystemExit(f"MISSING VI for text line {idx}: {content!r}")
            new_text = VI_TEXT[idx]
            # preflight: no ASCII comma in VI text field
            if "," in new_text:
                raise SystemExit(f"ASCII_COMMA in VI line {idx}: {new_text!r}")
            if content.startswith("title,"):
                parts = content.split(",", 1)
                old_tf = parts[1]
                new_content = "title," + new_text
            else:
                parts = content.split(",", 5)
                old_tf = parts[2]
                parts[2] = new_text
                new_content = ",".join(parts)
            # preflight: <br> count must match
            if count_br(old_tf) != count_br(new_text):
                issues.append((idx, count_br(old_tf), count_br(new_text)))
            if old_tf == new_text:
                issues.append(("UNCHANGED", idx))
            out_segments.append(new_content + nl)
        else:
            out_segments.append(seg)

    if issues:
        print("PREFLIGHT ISSUES:")
        for it in issues:
            print(" ", it)
        raise SystemExit("PREFLIGHT FAILED")

    result = "".join(out_segments)
    out_bytes = (b"\xef\xbb\xbf" if has_bom else b"") + result.encode("utf-8")
    VI.write_bytes(out_bytes)
    print(f"WROTE {VI} ({len(out_segments)} segments, bom={has_bom}, crlf={has_crlf})")


if __name__ == "__main__":
    build()

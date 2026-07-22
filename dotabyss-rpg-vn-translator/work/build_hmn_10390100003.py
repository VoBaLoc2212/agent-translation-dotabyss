#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI output for hmn_10390100003.

EN-asset-is-English case (en.json holds English; ja.json == identity map).
The `title,` field of the EN asset is still Japanese -> translate JP->VI Title Case.
All `message,` text fields already hold English -> translate EN->VI.

Structural authority = EN asset (delimiters, BOM, CRLF, <br> count, <size> cards).
Per field:
  - title,            : VI at field index 1 (no <br> suffix mirror)
  - message,          : VI at field index 2, then mirror the source trailing "<br> " suffix
  - messageTextUnder, : VI at field index 2, preserve parts[3:] (e.g. ,,,on)
  - messageTextCenter,: VI at field index 2, preserve parts[3:] (e.g. ,,,on)
Field 1 (speaker label) preserved byte-identical (JP keys / <user>).
ALL trailing parts[3:] are preserved so delimiter/field/tag counts match EN.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10390100003.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10390100003.txt"
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
SUF_RE = re.compile(r"(?:<br>\s*)+$")

# line_no -> VI text field (inner text; EN <br> counts already match source)
VI: dict[int, str] = {
    34: "Ngài Là Sứ Giả Của Chúa Trời",
    65: "...Giữa lúc đang nói chuyện với Margaret，%user% nhíu mày.",
    70: "Margaret. Có vẻ còn quá sớm để ăn mừng an toàn rồi. Chúng ta cần<br>rời khỏi đây nhanh lên.",
    81: "Ý ngài là sao，Chỉ Huy?",
    83: "Đây chỉ là tầng nông thôi，nhưng chẳng có chỗ nào trong Đại Huyệt mà được phép lơ là. Tôi cảm thấy<br>có gì đó gợn gợn. Phải mau rời đi thôi——",
    150: "Kííi!",
    210: "Hảả!? Có quái vật kìa! Sao lại ở chỗ này chứ!?",
    212: "Lại còn đông nghịt nữa kia! Chúng ta tiêu đời rồi，tôi bảo!",
    214: "C-chết tiệt~! Ựa ooo~n!",
    255: "...Chết thật. Đúng như tôi lo sợ.",
    267: "Nhưng，Chỉ Huy. Ngài dường như chẳng mấy bối rối.",
    269: "Lúc này，tôi nghĩ một mình tôi cũng thoát được. Có chở thêm chị<br>cũng ổn thôi.",
    280: "Còn bọn đạo tặc thì sao，Chỉ Huy? Ngài định xử lý họ ra sao?<br>",
    315: "Bỏ mặc chúng. Tôi chẳng có nghĩa vụ gì phải cứu. Nào，đi thôi.",
    338: "Xin ngài chờ đã，Chỉ Huy.",
    340: "...%user% đưa tay định nắm lấy tay Margaret. Nhưng nàng không nhúc nhích，<br>đối mặt với ánh mắt của anh.",
    342: "...Ánh mắt đó là sao? Đừng bảo là chị cũng muốn tôi cứu bọn đạo tặc đó?<br>",
    358: "Đúng vậy，Chỉ Huy. Họ bắt đầu hối lỗi rồi.",
    360: "Bình tĩnh đi? Bọn chúng từng bắt cóc chị đòi tiền chuộc，thậm chí định cướp<br>mạng sống của chị cơ mà?",
    371: "Nhưng em vẫn còn sống. Tội lỗi của chúng hoàn toàn có thể xá tội được.",
    382: "Phải chăng，chính nhờ giúp đỡ bọn họ lúc này—khi họ đã có dấu hiệu thay đổi—<br>mà lời dạy và sự cứu rỗi của Chúa mới trọn vẹn được?",
    384: "...Nực cười. Cụ thể thì chị giúp sao? Cứ tin đi，Chúa sẽ giáng<br>trần từ trên trời xuống cứu tôi，chị và toàn bộ đạo tặc à?",
    396: "Chuyện đó——khó thôi. Trừ phi có phép lạ xảy ra.",
    415: "Nhưng，ở đây có Chỉ Huy... tức là có ngài.",
    426: "Em tin ngài có thể cứu tất cả mọi người ở đây，kể cả em.",
    438: "Từ khi đến Căn Cứ Tiền Tuyến，em có nghe kể qua thành tích của ngài<br>— tài năng ngài chẳng khác gì một vị anh hùng do Chúa ban tặng.",
    449: "Ngài có thể không ưa Chúa，nhưng em tin ngài chính là Sứ Giả của Người.",
    457: "Vật gì em có thể dâng ngài，em thấy đều sẽ hiến cả——<br>xin ngài，hãy cân nhắc giúp em được không?",
    459: "...*thở dài*. Trời ạ. Một nữ tu sĩ kỳ lạ thật. Lời nói và thái độ thì<br>lễ phép，nhưng bản chất chẳng khác gì một lời đe dọa vòng vo.",
    470: "Em xin lỗi. Em không có ý đó——",
    472: "Tôi hiểu. ...Để tôi đổi cách nói. Chị nói vậy，khiến tôi chẳng<br>thể nào từ chối được.",
    483: "...! Vậy thì——",
    485: "Tôi là kẻ tồi tệ hơn chị tưởng. Lời hứa 'sẽ dâng ngài bất cứ thứ gì' đó——<br>tuyệt đối đừng quên đấy.",
    496: "Vâng!",
    519: "Nghe đây，lũ đạo tặc! Quái vật tấn công thì đông thật，nhưng bọn bay<br>chẳng hề thua thiệt về số lượng! Nghe lệnh tôi，tất cả đều sống sót!",
    521: "Nhưng，nếu bay không tin tôi mà xử động，tôi không thể bảo đảm mạng sống. <br>Quyết định đi？ Quyết ngay!",
    523: "V-vừa nghe ông nói bất thình lình thế này...",
    564: "Em cũng xin ngài nữa. Xin hãy nghe theo lệnh Chỉ Huy lúc này!",
    566: "Ơ，ông bảo thế thì em chẳng thể từ chối được! Mọi người！ Hãy nghe<br>theo lệnh Chỉ Huy!",
    578: "Một giọng trầm thấp vang lên 'Ồ!'，và Chỉ Huy gật đầu.",
    638: "Đầu tiên，cho lão luyện kinh nghiệm đối phó đợt sóng quái vật thứ nhất! Bọn<br>chúng là đội tiên phong! Hù dọa rồi đẩy lùi chúng!",
    640: "Trong lúc đó，chia quân thành tiên phong，cung thủ và mồi nhử chạy nhanh! Thoát<br>khỏi vòng vây，rồi vừa rút vừa chiến đấu!",
    670: "—Nhờ mệnh lệnh chuẩn xác của %user%，thế cục lập tức nghiêng<br>về phía bọn đạo tặc.",
    672: "Bọn đạo tặc bảo vệ Margaret và %user%，dần dần di chuyển về<br>phía vùng an toàn—",
    674: "Chúng ta sắp đến nơi rồi! Cố lên!",
    713: "Gào!",
    738: "T-tiêu rồi Chỉ Huy！ Có con khổng lồ ở phía trước kìa!",
    740: "Bọn như thế đó，làm sao đánh bại nổi chứ...?",
    755: "(...Tệ rồi. Chúng bị thương，lại mệt mỏi... Và giờ con này<br>xuất hiện! Đúng lúc tệ nhất! —Giờ làm sao!?)",
    799: "Mọi người，đừng bỏ cuộc! Hãy tin vào Chỉ Huy—",
    848: "—Sau khi hét lên đó，Margaret bắt đầu hát. Một thánh ca.",
    850: "—Bằng giọng mạnh mẽ，nàng hát về một vị anh hùng，với tư cách là Sứ Giả<br>của Chúa，dẫn dắt những kẻ bị mang ấn tội nhân để chinh phạt một đại ác—",
    852: "G-gì cơ? Tự nhiên em thấy dũng cảm thế không biết!",
    854: "Đó không phải tất cả đâu! Vết thương...!",
    856: "Ánh sáng chiếu xuống những tên đạo tặc bị thương. Ánh sáng ấy，thấm<br>đẫm ma lực，dần chữa lành vết thương cho chúng.",
    875: "Người dẫn dắt các bạn chính là Anh Hùng. Ngài ấy nhất định sẽ dẫn chúng ta đến chiến thắng!",
    877: "...Nếu Margaret nói vậy，thế thì đúng là thật! Cứ làm thôi!",
    879: "Bọn em không thua đâu! Chỉ Huy! Hãy ra lệnh đi!",
    881: "Ha ha. Margaret... chị đúng là một người phi thường.",
    969: "—Lũ đạo tặc，sau khi lấy lại ý chí chiến đấu，đã đẩy lùi con quái vật khổng lồ. Sự an toàn của %user% và Margaret đã được bảo đảm.",
    1020: "Chỉ Huy. Cảm ơn ngài... Hình như bọn đạo tặc có điều muốn nhờ ạ.",
    1039: "Sau khi chuộc tội xong，họ nói muốn được làm việc dưới trướng ngài，<br>Chỉ Huy.",
    1041: "Bọn em sống sót được là nhờ ngài và Margaret cả đấy.",
    1043: "Em sẽ chuộc tội bằng mạng sống này，thề đấy! Xin ngài，hãy cho em giúp sức!",
    1045: "...Tôi hiểu. Tôi sẽ cân nhắc. Trước mắt các ngươi sẽ bị giam，nhưng tôi<br>sẽ không đối xử tệ với các ngươi đâu.",
    1081: "Cảm ơn ngài，Chỉ Huy. Em không biết phải bày tỏ lòng biết ơn<br>thế nào cho phải...",
    1083: "Tôi chẳng cần lời nói suông. Chị từng nói sẽ dâng bất cứ thứ gì chị có—<br>chị nhớ chứ?",
    1094: "Dạ vâng. ...Em phải trả ơn cho ngài thế nào，Chỉ Huy?",
    1121: "(...Dù không phải tiền bạc hay vật phẩm，mà chính bản thân em，em—)",
    1141: "Chị đang đánh giá rẻ tôi rồi. Tiền công lính đánh thuê của tôi đâu có rẻ đến thế.",
    1152: "Em thừa hiểu điều đó. Em đã quyết tâm dâng ngài bất cứ thứ gì—thật<br>sự là bất cứ thứ gì.",
    1154: "Hừm. Vậy thì，từ nay hãy cứ ở lại Căn Cứ Tiền Tuyến mà lắng nghe<br>nỗi lòng của mọi người giúp tôi.",
    1165: "—Hả?",
    1167: "Giá trị của tôi và chị có khác，nhưng tôi thừa nhận năng lực của chị<br>và có kẻ được cứu nhờ lời khuyên của chị.",
    1169: "Chị cứ là chính mình là điều tốt nhất với tôi nữa.",
    1180: "Nhưng ngài vừa nói lời cảm ơn suông chẳng đủ，Chỉ<br>Huy...",
    1182: "...Đừng bắt tôi phải nhắc lại. Nghĩa là lời chị nói có giá trị đến thế đấy.<br>",
    1193: "…",
    1195: "Ha ha. Sao thế? Mặt chị đỏ kìa. Chị có thể tự nhiên khen người khác<br>như chẳng hề ngượng，thế mà bị khen thì lại luống cuống à?",
    1206: "...Fu fu. Không，không phải đâu. Em không hề luống cuống—tuyệt đối không.",
    1208: "...Tôi hiểu rồi. Tôi vẫn chẳng tài nào hiểu nổi chị.",
    1241: "%user% dời đi cùng bọn đạo tặc. Ánh mắt ấm áp của Margaret dõi<br>theo bóng lưng anh.",
    1300: "...Một vị quý ông tuyệt vời làm sao.",
    1311: "Sau vụ tập kích nãy giờ，em lại được ngài cứu một lần nữa... Fu fu fu.",
    1345: "<size=48>—Vài Ngày Sau</size>",
    1384: "Chỉ Huy... ngài có nghe chuyện về Sophia và mấy người kia không?",
    1386: "Hả? Tôi chỉ nghe nói sau khi nói chuyện với Margaret và tự nhìn lại<br>bản thân thì thái độ họ thay đổi. Có chuyện gì xảy ra à?",
    1393: "Sophia，Verisa，Marina，Kururu，Himari... Ai nấy đều trở lại bình<br>thường hết rồi，em nghe nói thế!",
    1395: "Tôi thừa nhận Margaret có tài，nhưng... người ta đâu dễ dàng thay<br>đổi thế đâu.",
    1404: "Em đoán là vậy...",
    1449: "Xin lỗi đã làm phiền. Đây là món ngài gọi.",
    1451: "Khi nữ phục vụ mang món đến bàn bên cạnh，%user% nhíu<br>mày khó hiểu.",
    1453: "...Hả? Khoan đã. Sao bàn bên lại được phục vụ trước? Chúng ta gọi trước<br>họ mà，đúng không?",
    1495: "Á!? Em xin lỗi vô cùng! Em sẽ đi kiểm tra ngay.",
    1531: "<size=48>—Vài Phút Sau</size>",
    1560: "Lầm bầm，lầm bầm，lầm bầm...",
    1569: "C-Chỉ Huy! Xin ngài vui lên đi!",
    1571: "Họ xếp đơn chúng ta xuống cuối，đồ uống đưa vội thì dở tệ，thế mà giờ<br>tôi mới là kẻ bị coi như người sai!",
    1580: "N-nhưng cuối cùng họ có xin lỗi，thậm chí còn biếu thêm món ăn<br>đền bù mà，đúng không?",
    1582: "Không thể tha thứ，tuyệt đối không thể tha thứ... Có nên gọi họ qua<br>xin lỗi lần nữa không...?",
    1632: "Ồ chao! Chỉ Huy，thật bất ngờ khi gặp ngài ở đây...",
    1634: "Á! M-Margaret...",
    1645: "Hôm nay là một ngày tốt. Em tạ ơn Chúa vì lòng nhân từ của Người.",
    1699: "Margaret! Đúng lúc quá! Chỉ Huy lại đang cáu kỉnh nữa...",
    1710: "Ồ chao! Chỉ Huy，nếu ngài bất an，xin hãy tâm sự với em.",
    1712: "Ah，không... Tôi chắc chắn sẽ vui lên，nhưng tôi không muốn tính<br>cách mình thay đổi，dù chỉ tạm thời...",
    1758: "Nhưng，Chỉ Huy，em buồn lắm vì ngài chẳng thể thảnh thơi. Em<br>không khỏi lo lắng cho ngài.",
    1760: "Ah，thôi，đừng bận tâm. Tự dưng tôi chẳng còn thiết tha gì nữa. Nên<br>chẳng cần lo. Cứ để tôi yên. ...Được không?",
    1794: "Nhưng—",
    1796: "Thật sự chẳng có gì đâu! Tôi không còn giận nữa mà!",
}

assert len(VI) == 110, f"expected 110 VI entries, got {len(VI)}"

lines = EN.read_text(encoding="utf-8-sig").splitlines()
raw = EN.read_bytes()
has_crlf = b"\r\n" in raw

# ---- preflight: compare inner <br> counts for ALL message lines before writing ----
mismatches = []
for i, line in enumerate(lines, 1):
    if line.startswith("message,"):
        parts = line.split(",", 5)
        tf = parts[2]
        m = SUF_RE.search(tf)
        inner_en = tf[: m.start()] if m else tf
        new_text = VI[i]
        if "," in new_text:
            mismatches.append(f"L{i}: ASCII comma in VI: {new_text!r}")
        if inner_en.count("<br>") != new_text.count("<br>"):
            mismatches.append(
                f"L{i}: <br> mismatch en_inner={inner_en.count('<br>')} vi={new_text.count('<br>')}\n"
                f"     EN : {inner_en!r}\n     VI : {new_text!r}"
            )
if mismatches:
    print("PREFLIGHT FAILED - fix these before writing:")
    print("\n".join(mismatches))
    raise SystemExit(1)

out = []
for i, line in enumerate(lines, 1):
    if line.startswith(TEXT_CMDS):
        if line.startswith("title,"):
            parts = line.split(",", 1)
            cmd = parts[0]
            new_text = VI[i]
            assert "," not in new_text, f"ASCII comma in VI title line {i}: {new_text!r}"
            out.append(f"{cmd},{new_text}")
        elif line.startswith("message,"):
            parts = line.split(",", 5)
            cmd = parts[0]
            tf = parts[2]
            m = SUF_RE.search(tf)
            suf = m.group(0) if m else ""
            inner_en = tf[: m.start()] if m else tf
            new_text = VI[i]
            assert "," not in new_text, f"ASCII comma in VI message line {i}: {new_text!r}"
            assert inner_en.count("<br>") == new_text.count("<br>"), (
                f"<br> mismatch line {i}: en_inner={inner_en.count('<br>')} vi={new_text.count('<br>')}"
            )
            parts[2] = new_text + suf
            out.append(",".join(parts))
        else:  # messageTextUnder / messageTextCenter
            parts = line.split(",", 5)
            cmd = parts[0]
            new_text = VI[i]
            assert "," not in new_text, f"ASCII comma in VI {cmd} line {i}: {new_text!r}"
            parts[2] = new_text
            out.append(",".join(parts))
    else:
        out.append(line)

text = "\n".join(out)
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
VI_PATH.write_text("\ufeff" + text + "\n", encoding="utf-8")
print(f"WROTE {VI_PATH} :: {len(out)} lines, crlf_mirror={has_crlf}")
print("VI entries:", len(VI))

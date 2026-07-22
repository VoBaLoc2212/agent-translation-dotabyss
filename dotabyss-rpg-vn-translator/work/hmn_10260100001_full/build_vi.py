#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build VI asset for hmn_10260100001 (Sylvia / The Girl from a World of Ice).

EN-asset-is-English case:
  - ja.json = JP primary (not used by verifier, only for meaning)
  - en/ asset = structural authority + English alignment
  - vi/ output = must be byte-structurally identical to en/ asset

Approach: field-index replace of the text field (parts[1] for title,
parts[2] for message*) preserving every trailing technical field, BOM and
CRLF. VI strings mirror the EN text field's exact <br> count and trailing
"<br> " suffix. Internal commas use U+201A (‚). Speaker labels (シルヴィア,
<user>, empty) are engine keys -> kept verbatim.
"""
import pathlib

ROOT = pathlib.Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100001.txt"
OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100001.txt"

# line_no -> VI text field (exact <br>/suffix mirror of EN field)
VI = {
    17: "Thiếu Nữ Từ Thế Giới Băng Giá",
    24: "Sylvia là một thiếu nữ được cho là đến từ một dị giới bị phong ấn trong băng giá.<br> ",
    26: "Lo lắng cho cô gái chẳng thể hòa hợp với ai và luôn cô độc<br>‚ Chỉ Huy đã đến tận ký túc xá thăm ngó nàng—<br> ",
    37: "—Hắt xì! C‚ cái lạnh gì thế này? Đang giữa hè mà‚ sao lại lạnh như chính giữa mùa đông thế!<br> ",
    39: "Cái hàn khí khổng lồ này từ đâu tới...? Hể? Đó là... phòng của Sylvia<br> à.<br> ",
    41: "Không biết cô ấy đang làm gì‚ nhưng cứ đà này mọi người sẽ chết cóng<br>mất. Anh phải ép cô ấy dừng lại ngay lập tức...!<br> ",
    62: "Sylvia! Cô rốt cuộc đang làm cái gì thế!<br> ",
    94: "Ồ‚ xông thẳng vào phòng một quý cô mà chẳng thèm gõ cửa—mấy người đàn ông ở thế giới này<br>không biết lễ nghĩa sao?<br> ",
    96: "Nếu muốn tôi chiếu cố‚ trước tiên hãy chấm dứt mấy hành vi phiền phức đi.<br>Ký túc xá đã thành băng giá‚ mọi người đều đang khổ sở vì cô đấy.<br> ",
    109: "Tôi chẳng hề lạnh chút nào. Hay là mọi người đều quá<br>nhạy cảm với cái lạnh?<br> ",
    128: "Như anh thấy‚ tôi chỉ đang tạo ra những tượng băng thôi. Nếu phòng ấm<br>‚ tượng băng sẽ tan mất.<br> ",
    130: "Hóa ra đó là nguồn gốc của cái lạnh... Anh không bảo cô đừng sáng tác<br>‚ nhưng sao cô không dùng một chất liệu khác được? Cứ thế này thì chúng ta sẽ chết cóng mất...<br> ",
    141: "Tôi là một pháp sư băng. Một pháp sư băng mà lại động vào thứ gì<br>ngoài băng là chuyện vô lý.<br> ",
    155: "Hơn nữa... tôi không tài nào phá hủy những tượng băng xinh đẹp đến thế được.<br> ",
    157: "Đúng là những tượng băng đẹp thật... nhưng sao anh lại làm ra thứ này?<br> ",
    169: "Bởi vì tôi từng là một quý tộc‚ đồng thời cũng là một nghệ sĩ.<br> ",
    180: "Đẹp phải không? Ngay cả anh‚ người sinh ra ở một thế giới thiếu thốn mỹ thuật đến mức chẳng hề bồi đắp con mắt thẩm mỹ<br>—anh cũng cảm nhận được vẻ đẹp này‚ đúng không?<br> ",
    182: "Đúng là cô cứ thích thêm mấy lời thừa thãi nhỉ? ...Ngay cả anh<br>cũng thấy được vẻ đẹp này.<br> ",
    184: "Này‚ mấy pho tượng băng này có người mẫu thật không?<br> ",
    196: "Sao anh lại hỏi vậy?<br> ",
    198: "Bởi vì pho tượng băng cô gái kia trông hơi giống cô. Người đàn ông và người đàn bà ở hai bên<br>—chẳng phải là người có liên quan đến cô sao?<br> ",
    209: "Vâng. Đây là gia đình tôi—<br> ",
    238: "K‚ không có ai cả. Tôi chỉ thấy hình dáng ấy dễ nặn thôi.<br> ",
    240: "Ra là vậy.<br> ",
    242: "Dù sao thì‚ đừng tạo tượng băng trong phòng nữa. Ít nhất hãy ra ngoài mà làm. Anh<br>chịu không nổi cái lạnh này.<br> ",
    254: "Đành vậy. Tôi sẽ nghe lời anh. Dẫu sao tôi cũng đang muốn đổi<br>gió.<br> ",
    265: "Thế giới này nóng quá sức. Dùng băng của tôi để làm mát nó cũng chẳng tệ<br>‚ đúng không?<br> ",
    267: "Cô định mang cả kỷ băng hà tới sao!?<br> ",
    269: "Thật tình‚ cô vẫn ngông cuồng như xưa... và phòng cô thì bừa bộn<br>tột độ.<br> ",
    280: "Tuyệt đối không có chuyện đó. Thế này là bình thường mà.<br> ",
    282: "Bình thường á? Khó mà gọi là bình thường. Quần áo của cô vứt đầy ra sàn.<br> ",
    293: "Ư‚ không được...<br> ",
    295: "Ít nhất hãy giặt đồ và cất gọn vào tủ đi.<br> ",
    306: "T‚ tôi không thể... tôi chưa từng làm việc đó bao giờ...<br> ",
    308: "Hầy... không những gây phiền phức‚ cô lại chẳng có chút kỹ năng sinh hoạt.<br> ",
    319: "T‚ tôi đâu có giúp được! Ở thế giới cũ<br>‚ các người hầu đã lo tất cả cho tôi mà!<br> ",
    330: "Tôi nào ngờ mình lại phải tự tay làm mấy việc lặt vặt trong sinh hoạt cho đến khi tới thế giới này<br>‚ biết không...<br> ",
    365: "Khụ khụ! D‚ dù sao đi nữa‚ anh! Anh tới đúng lúc quá! Thực ra tôi có một<br>yêu cầu.<br> ",
    367: "Nếu là để dọn phòng thì thôi. Anh chẳng có ý định trở thành<br>quản gia riêng cho cô đâu.<br> ",
    378: "K‚ không đời nào! Cứ gác chuyện dọn dẹp sang một bên đã.<br> ",
    380: "Thế là thế nào?<br> ",
    396: "—Tôi muốn anh đưa tôi tới Đại Huyệt.<br> ",
    398: "Tới Đại Huyệt á? Rồi anh định làm gì...?<br> ",
    411: "Tôi muốn trở về thế giới cũ càng sớm càng tốt. Tôi không<br>có ý nói nơi này tệ‚ nhưng nó chẳng phải chỗ thuộc về tôi.<br> ",
    431: "Thế nên‚ tôi cũng đã tra cứu các ghi chép của thế giới này. Thế nhưng<br>tôi chẳng tìm được cách nào để về thế giới cũ.<br> ",
    442: "Nếu vậy‚ nơi duy nhất tôi có thể tìm được đường về là<br>Đại Huyệt—<br> ",
    444: "Phải nói trước‚ bọn anh có điều tra mấy chuyện đó khi thám hiểm<br>Đại Huyệt đấy. Dù sao thì hiện tại vẫn chưa có manh mối nào.<br> ",
    449: "Càng có lý do để đi. Có những manh mối anh không thấy được‚ nhưng tôi<br>có thể nhận ra chúng.<br> ",
    466: "Từ góc nhìn của anh‚ một kẻ như tôi từ thế giới khác hẳn là một<br>phiền phức anh muốn tống khứ càng sớm càng tốt—đúng không?<br> ",
    481: "(Tôi biết người ta trở nên khó tính khi bị ép vào đường cùng‚ nhưng tôi không ngờ<br>cô ấy lại khó chiều đến thế. Cô ấy hẳn rất nhớ nhà...)<br> ",
    496: "Được rồi. Anh sẽ đưa cô đi. Nhưng nếu không tìm được cách về thế giới<br>của cô thì sao?<br> ",
    510: "Khi đó... không‚ tôi sẽ nghĩ về nó khi thời điểm<br>tới.<br> ",
    521: "Hiện tại‚ tôi muốn tối đa hóa cơ hội nhiều nhất có thể.<br>Bởi vậy‚ tôi chẳng có ý định để tâm đến mấy chuyện thừa thãi.<br> ",
    532: "Vậy chúng ta lên đường ngay thôi. Thế giới này nóng hơn hẳn so với thế giới tôi từng ở<br>—nếu cứ ở đây lâu hơn‚ tôi sẽ tan chảy mà chết mất.<br> ",
    544: "Hơn nữa... có người ở thế giới tôi đang chờ tôi trở về...<br> ",
    546: "Được rồi được rồi. Anh sẽ đưa cô đi ngay.<br> ",
    548: "Nhưng tuyệt đối đừng đi một mình. Đó là điều kiện để anh đưa cô tới<br>Đại Huyệt—anh nhất quyết thế.<br> ",
    559: "Ồ? Vậy là anh không thể rời mắt khỏi cái phiền phức sao?<br> ",
    561: "—Không. Là để giữ cho cô không gặp nguy hiểm.<br> ",
    588: "...Hừm. Lắm mệnh lệnh thế. Thôi‚ được rồi. Tôi sẽ ở trong tầm mắt của anh<br>nhiều nhất có thể.<br> ",
    632: "(Xin hãy đợi em‚ thưa Cha‚ thưa Mẹ. Lần này‚ em nhất định sẽ tìm được đường<br>về nhà.)<br> ",
}

# Capture original EN field <br> counts for assertion
raw = EN.read_bytes()
assert raw[:3] == b"\xef\xbb\xbf", "EN asset missing BOM"
has_crlf = b"\r\n" in raw
text = raw.decode("utf-8-sig")
lines = text.split("\n")

en_br = {}
for i, l in enumerate(lines, 1):
    if i in VI:
        kind = l.split(",", 1)[0]
        if kind == "title":
            en_br[i] = l[len("title,"):].rstrip("\r").count("<br>")
        else:
            parts = l.split(",")
            en_br[i] = (",".join(parts[2:]) if len(parts) > 2 else "").rstrip("\r").count("<br>")

out_lines = []
for i, l in enumerate(lines, 1):
    if i in VI:
        vi = VI[i]
        assert "," not in vi, f"ASCII comma in VI field at line {i}: {vi!r}"
        assert vi.count("<br>") == en_br[i], (
            f"<br> count mismatch line {i}: EN={en_br[i]} VI={vi.count('<br>')}"
        )
        kind = l.split(",", 1)[0]
        if kind == "title":
            parts = l.split(",")
            parts[1] = vi
            out_lines.append(",".join(parts))
        else:
            parts = l.split(",")
            parts[2] = vi
            out_lines.append(",".join(parts))
    else:
        out_lines.append(l)

out_text = "\n".join(out_lines)
if has_crlf:
    out_text = out_text.replace("\r\n", "\n").replace("\n", "\r\n")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(b"\xef\xbb\xbf" + out_text.encode("utf-8"))
print("Wrote", OUT, "lines:", len(out_lines), "crlf:", has_crlf)
print("VI records translated:", len(VI))

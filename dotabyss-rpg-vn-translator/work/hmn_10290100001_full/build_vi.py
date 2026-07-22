#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build VI asset for hmn_10290100001 from EN asset English text fields.
EN-asset-is-English case: title is JP, message text fields are English.
Translate JP->VI via ja.json; substitute the English text field.
Mirror each source <br> count exactly; use U+201A (‚) for commas inside VI text.
Preserve BOM + CRLF + delimiters + %user% + trailing <br> suffix.
"""
EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100001.txt"
OUT_PATH = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10290100001.txt"

# line_no (1-indexed in EN asset) -> VI text field (including trailing <br> where source has it)
VI = {
    19: "Trông Cậu Ăn Ngon Lắm",  # title
    27: "Ưm‚ kế tiếp làm sao đây... Dù có nghĩ mãi<br>mà não vẫn không chịu vận hành!<br> ",
    66: "Chỉ Huy! Em đã chuẩn bị trà và bánh ngọt rồi. Nghỉ giải lao một chút<br>nhé?<br> ",
    68: "Ừ‚ cứ thế đi...<br>Chắc não không vận hành được là tại thiếu đường thôi.<br> ",
    108: "Của em đây! Đây là bánh tart trái cây đặc biệt do Myrtille mang tới làm quà đấy!<br> ",
    110: "Ồ‚ trông ngon đấy. Ăn thôi.<br> ",
    139: "%user% và Alicia vừa cắn vào bánh tart‚<br>mắt hai người mở to vì bất ngờ.<br> ",
    141: "Ngon tuyệt.<br>Khác hẳn trình so với mọi loại tart từng ăn.<br> ",
    152: "Vừa mềm ẩm‚ lại vừa giòn rụm‚ trái cây và phần đế quyện vào nhau hoàn hảo—<br>thật sự kinh ngạc!<br> ",
    154: "Myrtille là đầu bếp bánh ngọt của Lux Nova phải không?<br>Anh biết bọn họ kỹ thuật cao‚ nhưng không ngờ đồ ngọt lại ngon thế này...<br> ",
    166: "Em nghe nói Myrtille xuất thân từ Vương Quốc Đồ Ngọt!<br>Chắc vì thế mà có kỹ năng độc đáo thế!<br> ",
    176: "Tiếng gõ cửa vang lên trong phòng chỉ huy.<br> ",
    185: "Ồ‚ có khách à? Mời vào!<br> ",
    242: "Làm phiền! Chào Alicia‚ Chỉ Huy!<br> ",
    298: "Myrtille! Chúng em vừa ăn bánh tart cậu mang tới xong!<br> ",
    300: "Ngon bất ngờ thật. Cảm ơn.<br> ",
    311: "Không‚ không! Mil vui lắm vì cậu thích nó!<br> ",
    322: "Vậy‚ cậu đến đây có việc gì? Có chuyện cần giúp không?<br> ",
    341: "Thật ra‚ Mil có chút rắc rối nên muốn nhờ cậu chỉ bảo...<br> ",
    343: "Ồ‚ nhờ tư vấn à? Để đáp lại chiếc tart ngon đó‚ anh nghe bao nhiêu cũng được.<br> ",
    354: "Mil cảm ơn cậu‚ Chỉ Huy!<br> ",
    398: "Lúc Mil không để ý‚<br>mấy cái tart đem bán bỗng biến mất khỏi bếp của ký túc xá.<br> ",
    409: "Hình như có ai đó lấy mất rồi.<br> ",
    411: "Vậy là mấy cái tart bán đã bị mất‚ à...<br> ",
    422: "Với lại khi định làm thêm‚<br>trái cây trong kho cũng hao đi! Họ bảo chắc Mil đã dùng mất!<br> ",
    424: "Oan uổng quá đáng.<br>Ngay cả Myrtille cũng chẳng làm nổi nhiều đồ ngọt đến thế.<br> ",
    435: "Ưm‚ cứ có nguyên liệu trước mắt là<br>Mil lại làm thôi...<br> ",
    437: "Hóa ra cậu có làm! Chẳng trách họ nghi cậu!<br> ",
    448: "Ưm! Nhưng nguyên liệu đều bảo Mil làm cho ngon mà!<br> ",
    459: "Nhưng lần này thật sự không phải Mil! Hãy tin em!<br> ",
    506: "Thôi‚ Myrtille đâu có lý do để nói dối.<br>Tart và trái cây thật sự đã biến mất.<br> ",
    517: "Ý cậu là có kẻ trộm trong ký túc xá?<br>Không thể để nạn trộm cắp xảy ra ở căn cứ được!<br> ",
    519: "Ừ‚ với tư cách Chỉ Huy anh không thể làm ngơ.<br>Lên hiện trường thôi!<br> ",
    571: "Chỗ này! Mấy cái tart để trên bàn đã biến mất rồi.<br> ",
    573: "Chỗ nào người ở ký túc cũng có thể lấy‚ à.<br>Xác định thủ phạm sẽ khó đây...<br> ",
    584: "Ưm‚ muốn ăn tart thì cứ hỏi!<br>Sao phải lén lút mang đi?<br> ",
    608: "Hể? Cái này là...? Myrtille‚ lại đây.<br> ",
    658: "Có chuyện gì‚ Chỉ Huy?<br> ",
    660: "Chỗ %user% chỉ tới‚<br>những dấu chân nhỏ xíu còn sót lại ở cửa sau góc bếp.<br> ",
    669: "Những... dấu chân này?<br> ",
    671: "Ừ‚ nhỏ thật‚ nhưng không nghi ngờ gì nữa.<br>Tóc ngắn cứng cũng rải rác ở đây‚ nên chắc chắn có kẻ đột nhập.<br> ",
    688: "Vậy kẻ lấy tart của em là...<br> ",
    690: "Có khả năng là kẻ để lại dấu chân đó.<br>Đuổi theo thôi.<br> ",
    702: "Ừ! Đi hỏi xem sao họ lấy tart của em!<br> ",
    740: "Chúng ta đã rời căn cứ đi vào rừng rồi.<br> ",
    742: "Đã lần theo dấu chân tới đây‚<br>nhưng đi xa căn cứ quá thì nguy hiểm...<br> ",
    751: "Hể? Không phải nó ở đằng kia sao...?<br> ",
    753: "Tít trong rừng‚<br>một con vật nhỏ xù lông nằm thu mình‚ như đang trốn giữa các cây.<br> ",
    765: "Anh Gấu ơi‚ là gì nhỉ?<br> ",
    767: "Trông như một gấu con. Nó làm gì ở đây thế...?<br> ",
    795: "...*gừ*?<br> ",
    797: "Bé gấu con cảm thấy sự hiện diện‚ quay về phía họ.<br>Miệng nhét đầy tart của Myrtille‚ trái cây rơi rác dưới chân.<br> ",
    827: "C-có con gấu đang ăn tart!<br> ",
    836: "Ể! Vậy thủ phạm là Anh Gấu à?<br> ",
    838: "*G-gừ... gừ‚ gừ...*<br> ",
    840: "Bé gấu liếc qua lại giữa vụn tart còn lại và Myrtille‚<br>rồi gừ lên như đang xin lỗi.<br> ",
    849: "Anh Gấu trông như đang nói xin lỗi?<br> ",
    851: "Ừ... con gấu này biểu cảm bất ngờ thật...<br> ",
    859: "Anh Gấu biết mình làm sai‚ phải không?<br> ",
    871: "*Gừừ...*<br> ",
    873: "Như muốn nói 'Em xin lỗi... cậu giận rồi à...?'‚<br>bé gấu ngước nhìn Myrtille đầy lo sợ.<br> ",
    884: "Ôi chao! Nó dễ thương quá đi!<br> ",
    886: "Biểu cảm khá đấy với một con gấu...<br>Dù sao‚ anh thấy cậu biết hối lỗi rồi.<br> ",
    897: "Sao một đứa ngoan như cậu lại làm thế? Mil thắc mắc.<br> ",
    899: "Mùa trái cây năm nay hình như mất mùa‚<br>nên có lẽ cậu ấy không tìm được thức ăn.<br> ",
    901: "Nhìn cái tai này.<br>Cậu ấy chắc thua trận tranh lãnh thổ—có một vết cắn to đùng.<br> ",
    912: "Mil hiểu rồi... Cậu ấy đang đói...<br> ",
    914: "Gâu...<br> ",
    919: "Lẽ ra không nên lấy khi chưa hỏi‚ nhưng...<br> ",
    948: "Myrtille bước tới bé gấu con và<br>nhẹ nhàng đặt vài cái tart dưới chân nó.<br> ",
    975: "Của cậu đây. Ăn đi.<br> ",
    977: "Gâu!? Gâu gâu!?<br> ",
    988: "Ừm‚ cậu không cần ngại đâu.<br> ",
    992: "Gâuuu!<br> ",
    994: "Bé gấu con dòm biểu cảm Myrtille nhiều lần‚<br>rồi vui vẻ ngấu nghiến tart.<br> ",
    1030: "Cậu chắc chứ? Đáng lý mấy cái đó mang bán mà‚ đúng không?<br> ",
    1041: "Ưm‚ dù là hàng bán đi nữa‚ Mil đâu có mở cửa hàng.<br>Mil chỉ để người ta mua nếu họ muốn thôi.<br> ",
    1053: "Hơn nữa‚ mấy cái này chỉ là thử nghiệm hay loại thôi‚ nên không sao!<br> ",
    1064: "Nhìn này! Cậu ấy thích mẫu mật ong lắm!<br> ",
    1066: "Gâu!♪<br> ",
    1068: "Dù vậy‚ anh thấy phí khi cho gấu ăn.<br>Có biết bao người muốn chúng‚ dù chỉ là mẫu thử‚ đúng không?<br> ",
    1075: "Ừm‚ Mil nghĩ có người sẽ ăn chúng...<br>nhưng Mil muốn cho kẻ thật lòng thèm muốn‚ cậu biết mà~<br> ",
    1090: "Dù sao đi nữa‚<br>điều khiến Mil hạnh phúc nhất là thấy ai đó vui vẻ ăn đồ Mil làm~<br> ",
    1092: "...Anh hiểu rồi.<br> ",
    1107: "(Myrtille đưa đồ ăn đó như thể cảm nhận được anh đang rối.<br>Cô ấy đang cố cứu người bằng đồ ngọt của mình‚ phải không?)<br> ",
    1109: "(Dù là người hay gấu‚ cảm giác đó không đổi‚ à.)<br> ",
    1151: "Gừ... gừ gừ!<br> ",
    1153: "Bé gấu con ăn xong cái tart‚<br>giơ một chân lên như muốn nói 'Cảm ơn!'<br> ",
    1164: "Ừ‚ cậu nói cảm ơn rồi‚ ngoan lắm~<br> ",
    1175: "Lần sau đói thì đừng tự ý lấy.<br>Hãy nói với Mil trước‚ nhé?<br> ",
    1177: "Gừ gừ!<br> ",
    1217: "Thế là‚ thế là xong chuyện rồi nhỉ.<br> ",
    1228: "Cảm ơn cậu~ Chỉ Huy!<br>Giờ em có thể bảo mọi người ở ký túc đừng lo!<br> ",
    1239: "Em kết bạn với Anh Gấu rồi‚ và cậu ấy ăn nhiều đồ ngọt~<br> ",
    1250: "Mọi thứ đều nhờ có cậu‚ Chỉ Huy~<br> ",
    1252: "Anh chỉ giúp chút xíu.<br>Cậu mới là người làm hết‚ Myrtille. Nếu thế là đủ giúp thì anh sẽ ra tay bất cứ lúc nào.<br> ",
    1271: "...Cậu tốt bụng quá‚ Chỉ Huy.<br> ",
    1283: "Vậy thì‚ cậu cũng cứ đến Mil bất cứ lúc nào đói nhé~<br> ",
    1285: "...Thế thì‚ xin lỗi vì hỏi ngay‚<br>nhưng anh đi bộ tới tận rừng nên đói rồi...<br> ",
    1319: "Fufu~ Thế thì cùng nhau ra bếp nhé!<br> ",
}


def replace_text_field(line, vi):
    if line.startswith("title,"):
        return "title," + vi
    parts = line.split(",", 5)
    parts[2] = vi
    return ",".join(parts)


def main():
    raw = open(EN_PATH, "rb").read()
    has_bom = raw[:3] == b"\xef\xbb\xbf"
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.split("\r\n") if has_crlf else text.split("\n")

    errors = []
    for i, line in enumerate(lines, 1):
        if i not in VI:
            continue
        vi = VI[i]
        if line.startswith("title,"):
            old_field = line.split(",", 1)[1]
        else:
            old_field = line.split(",", 5)[2]
        old_br = old_field.count("<br>")
        new_br = vi.count("<br>")
        if old_br != new_br:
            errors.append(f"L{i}: BR mismatch old={old_br} new={new_br} | OLD={old_field!r}")
        if "," in vi:  # ASCII comma — must use ‚ (U+201A)
            errors.append(f"L{i}: ASCII_COMMA in VI | {vi!r}")

    if errors:
        print("PREFLIGHT FAILED:")
        for e in errors:
            print("  " + e)
        raise SystemExit(1)
    print("PREFLIGHT OK: all <br> counts and comma checks passed.")

    out_lines = []
    for i, line in enumerate(lines, 1):
        if i in VI:
            out_lines.append(replace_text_field(line, VI[i]))
        else:
            out_lines.append(line)
    out_text = ("\r\n" if has_crlf else "\n").join(out_lines)
    out_bytes = (b"\xef\xbb\xbf" if has_bom else b"") + out_text.encode("utf-8")
    open(OUT_PATH, "wb").write(out_bytes)
    print(f"WROTE {OUT_PATH} ({len(out_bytes)} bytes, {len(lines)} lines)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic VI builder for hmn_10240100003 (EN-asset-is-English case).
JP primary (ja.json), EN asset = structural authority. Field-index build."""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10240100003"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# line_no -> VI text field only. Commas -> U+201A. <br> counts must match EN asset.
TRANSLATIONS = {
    31: "Công Chúa Của Khu Rừng",
    61: "Chết tiệt! Khu rừng này cỏ rậm rạp‚ đi lại khó chịu quá……!<br>Dám cản đường tao hả‚ tao chặt trụi hết chúng mày!<br> ",
    87: "Cứ tới được chợ đen Eldorana thì chẳng ai lần ra được tao.<br>Chỉ cần thoát khỏi khu rừng này……!<br> ",
    123: "Cái bình gã đeo trên lưng‚ là nước phép của Makkun đúng không……!?<br>Tìm ra ngươi rồi‚ tên trộm!<br> ",
    134: "Được rồi……!<br>Anh ơi‚ mau bắt hắn lại đi……!<br> ",
    136: "Khoan đã‚ Magnolia.<br>Anh hiểu cảm giác của em‚ nhưng giờ đừng vội.<br> ",
    147: "Tại sao……!?<br>Phải mau đưa nước cho Makkun mới được……!<br> ",
    149: "Lao vào không tính toán thì chỉ khiến hắn chạy thoát thôi.<br>Rượt đuổi trong rừng đêm cũng nguy hiểm cho chúng ta.<br> ",
    151: "Cho dù có dồn được hắn vào đường cùng‚ nếu hắn chống cự thì cũng phiền phức.<br> ",
    162: "A…… anh nói đúng.<br>Makkun bây giờ không chiến đấu được……<br> ",
    174: "Nhưng‚ nhưng‚ Manyo phải làm sao đây……<br> ",
    176: "Anh có một kế.<br>Kế bắt gã đó và lấy lại nước phép.<br> ",
    188: "Chuyện đó‚ làm được thật sao……?<br> ",
    190: "Ừ‚ nếu có sức mạnh của em‚ Magnolia à.<br> ",
    201: "Sức mạnh của Manyo……!?<br>Nhưng không có Makkun thì Manyo chỉ là……<br> ",
    203: "Em làm được mà‚ Magnolia.<br>Tin anh‚ được không?<br> ",
    235: "……Vâng‚ em tin anh.<br> ",
    237: "Tốt lắm‚ vẻ mặt tốt đấy.<br>――Nào‚ để anh truyền đạt kế hoạch.<br> ",
    301: "Chết tiệt‚ hướng này có đúng không vậy?<br>Còn phải lang thang thế này đến bao giờ nữa……<br> ",
    312: "Aa thôi nào! Sao khu rừng này đi lại khó khăn thế hả!<br>Đám cỏ này! Cả mấy cái cây to đùng! Chúng cố tình cản đường tao đấy à!?<br> ",
    345: "Ngươi đang làm gì thế!<br>Cái bình sau lưng ngươi là gì! Ngươi lấy trộm từ đâu ra!<br> ",
    354: "Cái quái gì thế này! Là kẻ của căn cứ à!?<br> ",
    365: "Không…… là cái thằng đi cùng con nhỏ cầm bông hoa đó! Nhưng nếu đối thủ chỉ một tên‚<br>tao vẫn thoát được……!<br> ",
    388: "Tốt‚ hắn chạy sâu vào rừng rồi. Đúng như kế hoạch. Dẫn hắn<br>đến điểm đã định‚ trông cậy vào em‚ Magnolia.<br> ",
    425: "Vâng…… mọi người‚ nhờ cả rồi……!<br> ",
    473: "Cắt đuôi được thằng đó chưa nhỉ? Cứ thế mau chóng<br>thoát khỏi rừng……<br> ",
    522: "Ken két ken két ken két!!!<br> ",
    541: "Oáaa! Cái quái gì thế này!?<br> ",
    553: "Bông hoa cắn tao!? Chết tiệt‚ phải chạy thôi!<br> ",
    606: "……Bác Hoa Ken Két đã tìm thấy hắn. Có vẻ chúng ta đang dẫn dụ tốt.<br> ",
    608: "Tốt‚ tiếp theo. Anh sẽ chỉ định điểm khác‚ ra lệnh cho<br>lũ thực vật phép đi!<br> ",
    617: "Vâng……!<br> ",
    671: "Nhoẹt nhoẹt! Nhoẹt nhoẹt nhoẹt!<br> ",
    682: "Oáaa!? Cái cây này phun cái gì vào tao rồi! Lối này không được‚ qua<br>bên kia!<br> ",
    728: "Xoẹt xoẹt! Xoẹt!!!<br> ",
    757: "Oáaaa!? Đám cỏ phóng lá sắc như lưỡi cưa vào tao! Cái khu rừng này<br>rốt cuộc bị làm sao vậy!<br> ",
    809: "Ông chú đang đi về hướng này. Có vẻ mọi người đều làm rất tốt.<br> ",
    811: "Tốt‚ xuất sắc. Giờ là đòn kết thúc. Em làm được mà‚ Magnolia.<br> ",
    822: "Vâng. Em sẽ cố hết sức‚ đúng như anh đã nói.<br> ",
    833: "Manyo sẽ cứu Makkun……!<br> ",
    888: "Hộc hộc…… Chỗ này…… an toàn chưa……?<br> ",
    899: "Chết tiệt‚ giỡn mặt tao. Cớ sao tao phải bỏ chạy khỏi<br>mấy cái cây cỏ tầm thường chứ……<br> ",
    950: "……Ông là người đã làm mọi người bị thương phải không?<br> ",
    961: "Hử!? Mày là con nhỏ cầm bông hoa đó……! Đến một mình sao?<br>Xem ra tao sắp có thêm hàng để bán ở chợ đen rồi.<br> ",
    973: "……Ông chẳng hiểu gì cả‚ ông chú à.<br> ",
    1041: "Ngoạm ngoạm ngoạm!<br> ",
    1050: "Nhoẹt nhoẹt! Nhoẹt nhoẹt nhoẹt!<br> ",
    1059: "Xoẹt xoẹt! Xoẹt!<br> ",
    1105: "Cái gì! Lũ thực vật phép đã tấn công tao…… Chết tiệt‚ ở đây cũng có à!<br> ",
    1155: "Nhưng chúng chỉ là cây cỏ với hoa‚ đâu cử động được! Tao chỉ cần chạy là xong!<br> ",
    1167: "Ông đã hành hạ Makkun‚ vô cớ làm mọi người bị thương. Cả khu rừng<br>sẽ không tha thứ cho ông đâu‚ ông chú.<br> ",
    1176: "Đừng có nói mấy lời vớ vẩn! Chẳng làm được gì mà bày đặt lên mặt!<br> ",
    1188: "Ông không thoát được nữa đâu‚ ông chú. Mọi thứ đều diễn ra đúng như<br>kế hoạch của anh ấy.<br> ",
    1199: "Phải không nào‚ các bạn Hell Rafflesia?<br> ",
    1286: "Ùng ục ùng ục ùng ục ùng ục!<br> ",
    1334: "Hộc hộc! Đám này là cái gì? Hoa khổng lồ khắp mọi nơi!<br> ",
    1347: "Dây leo trườn tới…… Aaa!? Dừng lại‚ đừng siết nữa! Tao không cử động được rồi!<br> ",
    1349: "Được rồi‚ kế dẫn hắn vào bãi Hell Rafflesia thành công rồi!<br>Nào‚ trả lại nước phép đây!<br> ",
    1360: "Kh-khoan! Trả lại đây! Tao định bán nó để thành tỷ phú……!?<br> ",
    1402: "Oáaaaa!? Bị kéo đi rồi!? T-tao bị hoa nuốt chửng……!<br> ",
    1464: "Tốt‚ lấy lại được rồi! Mau đưa nước phép cho Makkun!<br> ",
    1475: "Vâng! Nè Makkun‚ nước đây.<br>Cố uống rồi khỏe lại nhé……!<br> ",
    1495: "Ọ…… A…… Ọọ……<br> ",
    1513: "S-sao rồi? Có kịp không?<br> ",
    1524: "Em không biết…… Cậu cố lên Makkun……<br> ",
    1546: "Ọ…… ọ…… Ọọọọọ!<br>Ngon quááá!<br> ",
    1575: "Ơ-ưa!? Makkun!?<br>Uống nhiều quá‚ đừng uống hết!<br> ",
    1577: "Chà‚ nó tu thẳng từ bình luôn kìa.<br>Đây là nước phép đắt tiền đấy nhỉ……<br> ",
    1595: "Phùaa!<br>Manyo‚ cho tớ thêm nước phép nữa!<br> ",
    1625: "Không được! Makkun‚ cậu khỏe quá đà rồi!<br>Uống nữa là hết phần cho lát sau đấy!<br> ",
    1643: "Haa‚ đành chịu vậy.<br>Không sao! Tớ hồi phục hoàn toàn rồi!<br> ",
    1645: "Xin lỗi vì đã gây phiền hà nhé‚ Manyo‚ anh.<br>Cảm ơn cả hai người!<br> ",
    1647: "Giúp bạn bè là chuyện đương nhiên‚ đừng bận tâm.<br>Với lại Magnolia cũng đã nhờ anh mà.<br> ",
    1674: "Vâng‚ may mà cứu được Makkun.<br> ",
    1715: "……Thật sự cảm ơn anh‚ anh ơi.<br> ",
    1726: "Nhờ có anh mà Makkun đã khỏe lại rồi.<br>Nước phép cũng đã lấy về an toàn.<br> ",
    1728: "Người làm hết mọi việc là em mà‚ Magnolia.<br>Không cần cảm ơn anh đâu.<br> ",
    1730: "Ngược lại‚ anh mới là người phải khen em.<br>Em đã làm hoàn hảo lắm‚ Magnolia.<br> ",
    1739: "Hì hì……<br>Nhờ có anh ở bên‚ em mới cố gắng được.<br> ",
    1741: "Vậy là công của cả hai ta.<br>Thôi nào‚ về căn cứ thôi.<br> ",
    1783: "……Vâng.<br>Đi thôi‚ Makkun.<br> ",
    1803: "Ê! Nhưng Manyo này‚ vẻ mặt cậu tươi tắn ghê ta! Trong lúc tớ nằm liệt<br>cậu trưởng thành rồi hả!?<br> ",
    1830: "……Manyo có trưởng thành gì đâu. Anh ấy đã dạy Manyo rằng Manyo làm được mà.<br> ",
    1850: "Vậy hả? Nhưng với tớ trông cậu khác hẳn đấy!<br> ",
    1879: "Cậu tưởng tượng thôi‚ Makkun. Manyo chẳng thay đổi gì cả.<br> ",
    1892: "……Chỉ là Manyo đã có người mình thích thôi.<br> ",
    1912: "Ố ồ!? Mùa xuân đích thực đã đến với Manyo rồi! Cuối cùng cũng<br>đến lúc đóa hoa của cậu bung nở rồi hả!<br> ",
    1914: "Là ai thế!? Ê ê ê! Kể tớ nghe với!<br> ",
    1944: "Hì hì…… bí mật với cả Makkun nữa.<br> ",
    1964: "Chà! Đúng là thiếu nữ rồi! Phải báo cho ông già của cậu biết mới được!<br> ",
    1993: "B-bí mật với cả bố nữa! Không được nói với ai hết!<br> ",
    2004: "Nào Makkun‚ mình đuổi theo anh ấy thôi.<br> ",
    2029: "Sao thế‚ mau về nào.<br> ",
    2060: "Vâng…… anh ơi‚ về nhà cùng nhau nào♪<br> ",
    2078: "……Ừ thì‚ ai là người đặc biệt thì đã rõ như ban ngày rồi. Hòa thuận<br>nhé‚ hai vị!<br> ",
}


def main():
    assert TRANSLATIONS
    for ln, vi in TRANSLATIONS.items():
        assert "," not in vi, f"ASCII comma in VI L{ln}"

    raw = EN.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf", "EN must have BOM"
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(True)
    out = []
    translated = 0
    for idx, line in enumerate(lines, 1):
        if idx in TRANSLATIONS:
            vi = TRANSLATIONS[idx]
            cleaned = line.rstrip("\r\n")
            trailer = line[len(cleaned):]
            if cleaned.startswith("title,"):
                new = "title," + vi
                old_tf = cleaned.split(",", 1)[1]
            elif cleaned.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
                parts = cleaned.split(",", 5)
                old_tf = parts[2]
                parts[2] = vi
                new = ",".join(parts)
            else:
                raise AssertionError(f"unexpected L{idx}")
            assert old_tf.count("<br>") == vi.count("<br>"), \
                f"<br> mismatch L{idx}: EN={old_tf.count('<br>')} VI={vi.count('<br>')}"
            out.append(new + trailer)
            translated += 1
        else:
            out.append(line)
    out_bytes = b"\xef\xbb\xbf" + "".join(out).encode("utf-8")
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out_bytes)
    print(f"translated {translated}/{len(TRANSLATIONS)} records, {len(lines)} lines -> {VI}")


if __name__ == "__main__":
    main()

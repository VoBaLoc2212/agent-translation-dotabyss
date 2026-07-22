#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic VI builder for hmn_10240100001 (EN-asset-is-English case).

Stores line_no -> VI text field, rebuilds physical line by splitting on ASCII
commas and replacing only the text field index, preserving every trailing
technical field, BOM, CRLF, tags and <br> counts.

Conventions (per dotabyss-rpg-vn-translator rules + neighboring shipped VI):
- Commander protagonist = male -> self "anh", addresses Magnolia/Makkun as "em"/"anh".
- Commander/司令官 -> "Chỉ Huy" ONLY when EN literally says "Commander" (line 1198).
- マニョリア (Magnolia) self "em", calls Commander おにいさん -> "anh".
- マックン (Makkun) self "tớ", calls Commander 兄ちゃん/兄さん -> "anh", "anh trai".
- 怪しげな男 (suspicious man) internal monologue -> "ta".
- Names kept: Magnolia, Makkun, Alicia, Eldorana, Magic Water.
- "Big Brother"/"big bro" -> "anh"/"anh trai"; "buddy" -> "đồng bọn".
- ASCII comma forbidden inside VI prose -> use U+201A '‚'.
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10240100001"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# line_no -> VI translation for the text field only (preserve <br> counts + trailing space).
TRANSLATIONS = {
    21: "Hoa Nở Rộ Ồn Ào",  # title
    40: "Xin lỗi vì bắt em đi cùng anh mua sắm‚ Magnolia. Em<br>đã giúp anh rất nhiều hôm nay.<br> ",
    51: "...Không... em mừng vì đã giúp được anh.<br> ",
    53: "Cái cô Alicia đó lại dám nói là muốn mua hạt giống hoa có thể<br>trồng trong phòng.<br> ",
    62: "Anh chẳng hứng thú gì với hoa cả. Nếu không có em ở đó‚<br>Magnolia‚ anh đã mua bừa một ít rồi.<br> ",
    110: "Em nghĩ... Alicia muốn trồng hoa để trang trí phòng của anh‚<br>anh ạ.<br> ",
    121: "Em chắc chắn những bông hoa hôm nay sẽ nở thật nhiều và lấp đầy phòng anh<br>bằng mùi hương thơm ngát... em hy vọng vậy.<br> ",
    123: "Anh đã có thể mua luôn mấy bông đang nở... nhưng thế thì thô quá.<br>Em đã chọn những hạt này‚ nên anh tin chắc chúng sẽ nở thật đẹp.<br> ",
    134: "...Bởi vì em đã chọn những hạt giống khỏe mạnh.<br> ",
    173: "Cảm ơn‚ anh rất mong chờ đấy. Ah... nói chuyện với em khiến anh cảm thấy<br>như tâm hồn mình đang được gột sạch.<br> ",
    185: "...Em cũng vui khi ở bên anh‚ anh ạ.<br> ",
    187: "Không khí ấm áp này... Heh... làm ta nhớ đến đồng bọn của mình.<br> ",
    189: "Hôm nay anh cũng vui—hử? A-a là ai thế?! Giọng nói vừa rồi là của ai!?<br> ",
    201: "...Hử? Có chuyện gì lạ xảy ra sao?<br> ",
    203: "Không‚ anh cứ cảm thấy như có giọng nói lạ xen vào... Biết đâu chỉ là anh<br>nghe nhầm thôi.<br> ",
    205: "Đúng là làm ta nhớ đến đồng bọn... Chuyện đó cũng đã mấy năm rồi<br>nhỉ...<br> ",
    207: "Biết ngay mà! Có kẻ đang tự dưng bắt đầu kể chuyện đồng bọn của hắn!<br>Này‚ ai đấy‚ cái thằng nào vậy!?<br> ",
    219: "Ah... Makkun thức rồi.<br> ",
    221: "M-Makkun?! Cái quái gì thế!?<br> ",
    233: "Em chưa giới thiệu anh ấy với anh‚ anh ạ. Đó là bạn em‚ một bông hoa<br>tên là Makkun. Cậu ấy rất hay nói chuyện.<br> ",
    254: "Yo! Tớ là Makkun! Hân hạnh được gặp anh‚ anh trai!<br> ",
    257: "Không đời nào‚ một bông hoa lại biết nói! Hoa có thật sự nói được sao?<br> ",
    286: "Makkun là một loài thực vật ma thuật đã phát triển theo cách rất hiếm thấy.<br> ",
    288: "Không‚ không‚ kiểu phát triển gì mà hoa lại biết nói thế?<br> ",
    312: "...Thật ra‚ ông già của Magnolia từng là một thương nhân khá nổi tiếng ở<br>Eldorana.<br> ",
    342: "Vốn dĩ tớ chỉ là một bông hoa bình thường‚ nhưng ông ấy đã nuôi tớ bằng thứ<br>Nước Ma Thuật cực kỳ quý hiếm...<br> ",
    386: "Nước Ma Thuật ban cho tớ sức mạnh phép thuật mạnh mẽ‚ một ý chí rõ ràng‚ và khả<br>năng nói năng.<br> ",
    388: "Này‚ hắn tự dưng lên tiếng kể lể rồi. Mà cũng khá là<br>thú vị đấy...<br> ",
    390: "Chúng tớ đã nói chuyện bao lần‚ cùng cười‚ cùng khóc‚ chia sẻ<br>nỗi lo... và rồi tớ với ông già của Magnolia đã thành đồng bọn.<br> ",
    392: "Câu chuyện bắt đầu trở nên quá nhiệt huyết rồi...<br> ",
    394: "Khi Magnolia đến căn cứ này‚ tớ được giao nhiệm vụ trông<br>coi em ấy.<br> ",
    396: "Heh... ngay cả giờ‚ mỗi khi nhắm mắt tớ vẫn thấy gương mặt của lão‚<br>khóc nức nở vì không nỡ rời xa đứa con.<br> ",
    398: "Bộ phận nào là mắt mà hắn nhắm thế...? Nhưng mà‚<br>đúng là một bông hoa hay nói chuyện thật.<br> ",
    427: "...Bởi vì có Makkun ở đây‚ em không thấy cô đơn dù xa<br>ba.<br> ",
    438: "Và khi em không nói tốt được‚ Makkun sẽ nói thay em.<br> ",
    458: "Đổi lại‚ tớ nhờ Magnolia chăm sóc mình. Đó là mối quan hệ<br>có qua có lại.<br> ",
    460: "Hừ‚ hai đứa đúng là một cặp bài trùng. À này‚ Makkun‚ ngoài nói chuyện ra cậu còn<br>làm được gì nữa?<br> ",
    490: "Cậu ấy có thể cắn quái vật và chiến đấu bên em.<br> ",
    492: "Makkun‚ cậu dữ tợn hơn anh tưởng đấy!<br> ",
    512: "Heh‚ tớ là vệ sĩ của Magnolia! Tớ không để lũ sâu hại nào bén mảng tới em ấy đâu!<br> ",
    514: "Tớ có mối quan hệ cộng sinh với Magnolia! Đúng không‚ Magnolia?<br> ",
    544: "Ừ‚ thiếu Makkun là em sẽ rắc rối. Nên em chăm sóc cậu ấy chu đáo.<br> ",
    553: "Em còn chọn hẳn phòng trong ký túc xá cho Makkun. Một phòng góc có<br>nhiều cửa sổ và ánh nắng tốt.<br> ",
    564: "Hơn nữa‚ nếu để cậu ấy một mình‚ cậu ấy sẽ uống hết Nước Ma Thuật mất. Em phải<br>chăm sóc cậu ấy cẩn thận.<br> ",
    584: "Tớ là thực vật mà‚ anh biết chứ! Hễ có nước ngon ở quanh‚ tớ không thể không<br>uống được!<br> ",
    613: "Uống quá nhiều là không tốt. Cậu sẽ bị thối rễ đấy.<br> ",
    622: "Hơn nữa... Nước Ma Thuật rất đắt.<br> ",
    624: "Nước Ma Thuật quý giá‚ hử. Ở thị trấn này mua được không?<br> ",
    636: "Không‚ nó khó kiếm lắm‚ nên ba em gửi cho em.<br> ",
    638: "Ra thế. Hắn uống nhiều quá thì phiền thật.<br> ",
    673: "Nước Ma Thuật quý giá...? Ta chắc chắn nó đã bán được giá cao ở Eldorana‚<br>đúng không...?<br> ",
    684: "Nãy cô ta bảo đó là phòng góc trong ký túc xá... Nếu ta lấy được<br>Nước Ma Thuật đó...!<br> ",
    686: "...Hử?<br> ",
    705: "Hả!?<br> ",
    750: "Anh? Sao thế anh?<br> ",
    752: "Không‚ anh cứ thấy có ánh mắt kỳ lạ... nhưng...<br> ",
    764: "...Hừm.<br> ",
    784: "Ồ‚ Manyo? Chẳng lẽ đó là ghen tuông? Kiểu như‚ 'Cậu ở với tớ nên đừng<br>bận tâm đến kẻ khác!'?<br> ",
    822: "Ơ... không phải đâu... Không phải vậy đâu...<br> ",
    842: "Tớ thấy lạ là hai người đi chơi trong lúc tớ ngủ! Chẳng lẽ Manyo cuối cùng cũng<br>có mối tình đầu? Tớ ủng hộ em đấy!<br> ",
    877: "...Nếu cậu nói nữa‚ em sẽ cho cậu ngủ tiếp đấy.<br> ",
    897: "Ối‚ xin lỗi‚ xin lỗi! Tớ hơi nói quá đà rồi!<br> ",
    899: "Cho hắn ngủ... ý em là sao?<br> ",
    926: "Makkun... nếu bóp nhẹ ngay trên rễ của cậu ấy... cậu ấy sẽ ngủ. Khi<br>cậu ấy ồn quá... em dùng cách đó để làm cậu ấy yên lặng.<br> ",
    928: "Ừ‚ nếu Makkun không phiền thì cũng được... nhưng đó là cách làm khá<br>thô bạo. Sáng nay em giữ hắn ngủ bằng cách đó sao?<br> ",
    941: "...Ừ. Bởi vì anh luôn thực sự lắng nghe em nói...<br>dù không có Makkun‚ em cũng nghĩ... mình sẽ ổn.<br> ",
    943: "Anh vui vì em nghĩ vậy. Anh cũng thích nói chuyện với em‚ Manyo.<br> ",
    954: "Ôi‚ anh...<br> ",
    974: "Không khí tuyệt vời đấy‚ hai người! Thế nào‚ chúng ta đi ăn một bữa ngon<br>cùng nhau nhé?<br> ",
    1003: "Makkun! Đừng làm phiền anh...!<br> ",
    1005: "Không‚ chẳng phiền gì. Coi như lời cảm ơn vì đã giúp đỡ anh. Ít nhất để<br>anh mời em bữa tối.<br> ",
    1024: "Anh... cảm ơn anh.<br> ",
    1044: "Ồ‚ anh đúng là người biết điều!<br>Từ hôm nay‚ anh là đồng bọn của tớ‚ anh trai!<br> ",
    1064: "Anh trai? Đồng bọn? Ừ‚ anh cũng chẳng phiền... nhưng cậu đúng là một bông hoa<br>nói mượt mà đấy!<br> ",
    1115: "...Heh heh‚ ta nghe được chuyện hay rồi. Khi cô nhóc đó không ở đó‚ ta<br>chẳng còn lựa chọn nào khác ngoài ra tay...!<br> ",
    1143: "<size=48>—Đêm Đó</size>",  # messageTextCenter
    1165: "Được rồi‚ hôm nay làm thế là đủ rồi. Alicia‚ em cũng về đi.<br> ",
    1198: "Hử...! Chỉ Huy‚ vẫn còn quá nhiều việc chưa xong mà!<br> ",
    1200: "Tại chuyến đi mua sắm của em mất thời gian quá. Phần còn lại ta<br>làm ngày mai cũng được.<br> ",
    1211: "Ưm‚ chắc tại chúng ta ăn uống thong thả ngoài phố phường...<br> ",
    1273: "Anh! Ôi‚ may quá‚ anh ở đây...!<br> ",
    1282: "Ôi chao... Magnolia? Có chuyện gì mà chạy xộc vào như thế?<br> ",
    1293: "Ưm‚ ưm... Makkun...!<br> ",
    1300: "Bình tĩnh‚ từ từ nói‚ được không?<br> ",
    1311: "Không‚ không được! Chúng ta phải nhanh lên‚ việc này nghiêm trọng...!<br> ",
    1313: "Ra thế‚ đây là tình trạng khẩn cấp. Em không cần sắp xếp suy nghĩ.<br>Cứ kể cho anh nghe chuyện gì đã xảy ra.<br> ",
    1324: "Ừ... ừ... ưm‚ em thấy là...<br> ",
    1370: "Makkun... cậu ấy không nói được nữa!<br> ",
}


def main():
    assert TRANSLATIONS, "Fill TRANSLATIONS."
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
                assert len(parts) == 2, f"title split issue L{idx}: {line!r}"
                old_tf = parts[1]
                new = "title," + vi
            elif cleaned.startswith(("message,", "messageTextUnder,", "messageTextCenter,")):
                parts = cleaned.split(",", 5)
                assert len(parts) >= 3, f"message split issue L{idx}: {line!r}"
                old_tf = parts[2]
                # guard: <br> count must match
                assert old_tf.count("<br>") == vi.count("<br>"), (
                    f"LINE {idx}: <br> count mismatch EN={old_tf.count('<br>')} VI={vi.count('<br>')}"
                )
                parts[2] = vi
                new = ",".join(parts)
            else:
                raise AssertionError(f"unexpected text cmd L{idx}: {line!r}")
            trailer = line[len(line.rstrip("\r\n")):]
            assert trailer in ("\r\n", "\n", ""), f"bad trailer L{idx}: {trailer!r}"
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

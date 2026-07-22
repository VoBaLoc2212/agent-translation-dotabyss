# -*- coding: utf-8 -*-
"""Deterministic VI builder for hmn_10240100002 (EN-asset-is-English case).

Source hierarchy:
  ja.json        = JP primary (what we translate FROM)
  en/ asset      = structural authority (line order, BOM, CRLF, <br> counts, delimiters)
  vi/ asset      = output

We replace each text field (title index 1, message* index 2) with the VI string
preserving every technical trailing field. Guards: exact <br> count per line,
no ASCII comma inside VI text fields (U+201A '‚' used instead).
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10240100002"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# line_no -> VI text field (the part after title, or the 2nd comma of message*)
TRANSLATIONS = {
    24:  "Những Người Bạn Đặc Biệt",  # title (JP: 特別なお友達)
    # --- Act 1: Makkun weakened ---
    65:  "Xin lỗi… anh…<br> ",
    67:  "Đúng vậy. Ban ngày nó hét ầm ĩ thế kia mà giờ giọng chỉ còn<br>bé tí và khàn đặc.<br> ",
    87:  "Mới chỉ cách lúc gặp nó có vài tiếng thôi mà‚ chuyện gì xảy ra vậy?<br> ",
    96:  "Sau khi em chia tay anh trai ở thị trấn… em về phòng định đem<br>nước cho Makkun uống.<br> ",
    107: "Nhưng lúc đó thì toàn bộ nước vốn phải còn đó đã<br>biến mất hết…!<br> ",
    109: "Nước của Makkun là thứ Ma Thủy quý giá đúng không? Và uống<br>nó vào thì nó mới nói được lời.<br> ",
    129: "Ừm… nó là… nguồn sức mạnh của tớ…<br> ",
    156: "Makkun…! Đừng cố quá sức…!<br> ",
    158: "Nó vẫn gắng nói được chút ít, nhưng yếu đi trông thấy. Có phải do<br>Ma Thủy đã cạn không?<br> ",
    169: "Ừm… vì nhờ có Ma Thủy mà Makkun mới nói được. Thiếu<br>nó, nó sẽ dần mất khả năng nói chuyện…<br> ",
    171: "Vậy là nó đang trở lại thành cây bình thường… sao ta có thể để mặc thế này được.<br> ",
    212: "Được rồi, đi tìm Ma Thủy thôi! Đầu tiên, chúng ta sẽ lục soát<br>phòng của Magnolia!<br> ",
    223: "V‑vâng! Chúng ta đến doanh trại ngay lập tức!<br> ",
    243: "Làm phiền… xin lỗi anh…<br> ",
    268: "Cậu cố thêm chút nữa nhé, Makkun…!<br> ",
    334: "Đây là phòng của Magnolia!<br> ",
    367: "Anh mở cửa đây, Magnolia. Ổn chứ?<br> ",
    377: "Ừm…<br> ",
    406: "Căn phòng tối tăm của Magnolia đã bị lục tung một cách khủng khiếp.<br> ",
    408: "…! Phòng bị xới tung lên…!<br> ",
    437: "Magnolia, Ma Thủy đã biến khỏi phòng này rồi đúng không?<br> ",
    448: "Ừm… lúc về phòng em thấy thành ra thế này, và Ma Thủy<br>thì không còn ở đâu nữa…<br> ",
    493: "Vậy là một vụ trộm tại doanh trại Căn Cứ Tiền Tuyến…! Alicia, đây là<br>tình trạng khẩn cấp. Siết chặt an ninh ngay lập tức.<br> ",
    495: "Gọi bất cứ ai đang rảnh và không trực. Bảo họ lập tức bắt giữ<br>bất cứ thứ gì đáng ngờ.<br> ",
    508: "Vâng, ngay lập tức!<br> ",
    563: "Phải làm sao đây, phải làm sao đây anh trai ơi. Cứ thế này thì Makkun<br>sẽ…<br> ",
    565: "Không sao đâu. Nó cũng là bạn của anh mà, anh nhất định sẽ cứu nó.<br> ",
    574: "Ừm… ừm…!<br> ",
    592: "Cậu thật sự là một người bạn tuyệt vời… anh trai ơi…<br> ",
    610: "Chỉ xác nhận lại lần nữa thôi: Ma Thủy của Makkun không thể<br>mua được ở thị trấn đúng không?<br> ",
    622: "Ừm, vì nó là Ma Thủy quý hiếm. Bố em gửi cho em đấy.<br> ",
    624: "Để cứu Makkun, chúng ta chẳng còn cách nào khác ngoài tìm thủ phạm…<br>Magnolia, ngoài Ma Thủy ra còn gì bị mất nữa không?<br> ",
    643: "Ơ… em nghĩ là… không có gì cả.<br> ",
    645: "Vậy là một vụ trộm nhắm đích danh vào Ma Thủy. Chúng hẳn<br>đã biết nó quý giá.<br> ",
    657: "Nhắm vào Ma Thủy…!?<br> ",
    659: "Không còn lý do nào khác. Chúng xới tung phòng chỉ để ngụy tạo<br>thành một vụ trộm vặt thôi.<br> ",
    670: "Nhưng… gần như chẳng ai biết Manio có Ma Thủy…<br> ",
    688: "Không… tại lúc ở thị trấn tớ đã hét lớn chuyện đó…<br> ",
    715: "Ra thế. Lúc đó có khi ai đó đã nghe thấy chúng ta…<br> ",
    717: "Khả năng đó rất cao. Không có bằng chứng, nhưng tớ cũng cảm thấy<br>vài ánh mắt kỳ lạ…<br> ",
    719: "Nhưng nếu vậy thì vẫn còn cơ hội. Đây không phải vụ do chuyên nghiệp<br>lên kế hoạch mà là hành vi bộc phát.<br> ",
    776: "Rất có khả năng còn sót lại vài manh mối. Nếu ta điều tra<br>cẩn thận…<br> ",
    804: "Đúng như anh nghĩ! Magnolia, nhìn kỹ chỗ này này.<br> ",
    807: "Á, cái này… là dấu chân…!?<br> ",
    809: "Ừ, soi đèn lên thì thấy có dấu chân mờ nhạt. Hắn trộm lúc<br>tối nên mới không nhận ra.<br> ",
    837: "Được rồi, đuổi theo dấu chân nào, Magnolia. Chúng ta sẽ cứu<br>Makkun!<br> ",
    849: "Ừm…!<br> ",
    879: "Chết tiệt, dấu chân kéo ra tận ngoài căn cứ. Hắn định trốn ra ngoài à?<br> ",
    919: "Phía trước là khu rừng nơi cả lũ Hell Rafflesia sinh sống. Dù đó là<br>nơi nguy hiểm…<br> ",
    921: "Ừ, nơi đó cấm người thường vào. Dù có nguy cơ bị quái vật tấn công,<br>hắn vẫn liều làm cái trò điên rồ này.<br> ",
    923: "Magnolia, Ma Thủy quý giá đến mức có kẻ dám rời căn cứ lúc nửa đêm<br>nguy hiểm thế này sao?<br> ",
    934: "Ừm… vì Ma Thủy thấm đẫm sức mạnh mạnh mẽ và có rất<br>nhiều công dụng…<br> ",
    936: "Vậy là gã trộm đang bỏ chạy dù biết rủi ro. Nếu hắn liều mạng vì<br>tiền thì phiền phức đấy.<br> ",
    947: "Nghĩ mà xem, hắn làm khổ Makkun chỉ vì tiền…<br> ",
    968: "Này anh trai ơi.<br>Từ nhỏ Manio đã có thể trò chuyện với tất cả các loài cây.<br> ",
    970: "…Hờ? Vậy cậu có năng lực đặc biệt để nói chuyện với cây cỏ.<br> ",
    1019: "Bố em đã vui mừng khi nghe vậy. Nhưng chẳng người bạn Eldorana nào<br>tin em cả…<br> ",
    1021: "Ờ, khó chứng minh khi đối tượng là cây cỏ. Và người ta<br>chẳng dễ tin những gì một đứa trẻ nói.<br> ",
    1030: "Ừm… mọi người luôn nghĩ em là một đứa trẻ kỳ quặc. Nên bố em<br>đã đưa Ma Thủy cho Makkun.<br> ",
    1032: "Nếu Makkun có thể nói, điều đó sẽ chứng minh năng lực của em… ra thế.<br> ",
    1048: "Ừm. Makkun lúc nào cũng nói rằng một khi nói được, nó sẽ cho mọi<br>người thấy Manio tuyệt vời thế nào.<br> ",
    1050: "Ra thế.<br>Vậy em là người duy nhất có thể nói chuyện với Makkun từ đầu.<br> ",
    1061: "Dù chỉ có Ma Thủy thôi thì cũng chẳng thể tự nhiên nói được. Makkun<br>đã nỗ lực vì em đấy.<br> ",
    1096: "…Nó cũng có điểm tốt đấy, Makkun. Hẳn nó rất yêu em<br>đấy, Magnolia.<br> ",
    1108: "Makkun trông đáng sợ, nhưng là một người bạn đặc biệt hiền lành và hay nói chuyện.<br> ",
    1120: "Nhưng mà, em vẫn không thể nào quên được việc chẳng ai tin em.<br> ",
    1129: "Bởi vậy Manio mới ngại nói chuyện với người… Makkun thay em<br>nói với mọi người.<br> ",
    1141: "Makkun luôn luôn giúp đỡ em…!<br> ",
    1152: "Nhờ Makkun mà mọi người tin em. Dù em bảo muốn trở thành nhà<br>thực vật học, chẳng ai cười nhạo cả.<br> ",
    1172: "M… Manio…<br> ",
    1201: "Makkun…!<br>Sức lực của nó đang cạn dần… mau đưa Ma Thủy cho nó không được!<br> ",
    1203: "Không sao đâu, giờ Magnolia đã mạnh hơn rồi. Dù Makkun không nói được,<br>em vẫn có thể kể tình hình cho chúng ta.<br> ",
    1215: "Anh trai ơi…<br> ",
    1217: "Em là một cô bé can đảm, đang nỗ lực cứu bạn như thế này. Có<br>em và anh, nhất định chúng ta sẽ cứu được Makkun.<br> ",
    1236: "…Ừm, cảm ơn anh, anh trai.<br> ",
    1280: "Anh trai ơi, chúng ta đi sâu vào rừng dần rồi…<br> ",
    1282: "Ừm, cỏ dưới chân ngày càng dày hơn. Khốn nạn, thế này thì chẳng tìm<br>được dấu chân…!<br> ",
    1284: "Vừa nói huênh hoang xong, giờ lại bí ở đây. Có thời gian quay về căn cứ<br>gọi viện binh không…?<br> ",
    1296: "…! Mấy cái cây bên kia đang gọi Manio. Có một gã kỳ lạ, nó bảo thế.<br> ",
    1298: "Ra thế, sức nói chuyện với cây…! Manio, dẫn đường cho anh!<br> ",
    1350: "Hướng này…!<br> ",
    1396: "Đúng rồi! Có vết cỏ dưới bị chặt. Hờ, hắn đang định cố<br>lách qua rừng.<br> ",
    1431: "Á…! Anh trai, có ai đó ở kia kìa…!<br> ",
    1484: "Chết tiệt! Rừng này đi lại khó quá!<br>Không chặt cỏ thì chẳng nhúc nhích nổi!<br> ",
    1493: "Tưởng chạy dọc đường là bị bắt ngay… tch, nếu tệ quá anh sẽ đốt sạch cả<br>khu rừng này luôn!<br> ",
    1526: "Đó là gã kỳ lạ em thấy ở thị trấn!<br>Chính hắn đã trộm Ma Thủy!<br> ",
    1544: "………<br> ",
    1573: "Makkun…!<br>Anh sẽ lấy lại Ma Thủy ngay, nên đợi anh nhé…!<br> ",
}


def main():
    assert TRANSLATIONS, "fill TRANSLATIONS"
    # normalize internal ASCII commas to U+201A '‚' inside VI text fields
    norm = {ln: vi.replace(",", "‚") for ln, vi in TRANSLATIONS.items()}
    for ln, vi in norm.items():
        assert "\uff0c" not in vi, f"fullwidth comma in VI for line {ln}"
    TRANSLATIONS.clear()
    TRANSLATIONS.update(norm)

    raw = EN.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf", "EN source must have BOM"
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(True)
    has_crlf = b"\r\n" in raw

    # verify <br> counts match
    cmds = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
    problems = []
    for idx, line in enumerate(lines, 1):
        if idx not in TRANSLATIONS:
            continue
        cleaned = line.rstrip("\r\n")
        if cleaned.startswith("title,"):
            src_field = cleaned.split(",", 1)[1]
        elif cleaned.startswith(cmds[1:]):
            parts = cleaned.split(",", 5)
            src_field = parts[2] if len(parts) > 2 else ""
        else:
            continue
        vi = TRANSLATIONS[idx]
        if src_field.count("<br>") != vi.count("<br>"):
            problems.append((idx, src_field.count("<br>"), vi.count("<br>"), src_field, vi))
    if problems:
        print("BR MISMATCH:")
        for p in problems:
            print(f"  L{p[0]}: src_br={p[1]} vi_br={p[2]} | src={p[3]!r} | vi={p[4]!r}")
        raise SystemExit("Fix <br> counts before writing.")

    out = []
    translated = 0
    for idx, line in enumerate(lines, 1):
        if idx in TRANSLATIONS:
            vi = TRANSLATIONS[idx]
            cleaned = line.rstrip("\r\n")
            trail = line[len(line.rstrip("\r\n")):]
            assert trail in ("\r\n", "\n", ""), f"bad trailer L{idx}: {trail!r}"
            if cleaned.startswith("title,"):
                new = "title," + vi
            elif cleaned.startswith(cmds[1:]):
                parts = cleaned.split(",", 5)
                assert len(parts) >= 3, f"message split issue L{idx}: {line!r}"
                parts[2] = vi
                new = ",".join(parts)
            else:
                raise AssertionError(f"unexpected text cmd L{idx}: {line!r}")
            out.append(new + trail)
            translated += 1
        else:
            out.append(line)
    if has_crlf:
        body = "".join(out)
    else:
        body = "".join(l.rstrip("\r\n") + "\n" for l in out)
    out_bytes = b"\xef\xbb\xbf" + body.encode("utf-8")
    VI.parent.mkdir(parents=True, exist_ok=True)
    VI.write_bytes(out_bytes)
    print(f"translated {translated}/{len(lines)} lines -> {VI}")


if __name__ == "__main__":
    main()

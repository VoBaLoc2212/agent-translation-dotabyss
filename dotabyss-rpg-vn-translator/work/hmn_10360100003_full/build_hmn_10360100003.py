# -*- coding: utf-8 -*-
"""Build VI output for hmn_10360100003 (EN-asset-is-English, title still JP).
Field-index build: replace parts[2] (message*/messageTextCenter) or parts[1] (title)
with the VI text. Message text fields already carry the authoritative trailing
'<br> ' suffix in the EN asset, so VI values include it verbatim (no mirror needed).
Commas inside VI text use U+201A (‚). BOM + CRLF preserved byte-for-byte.
"""
import io, sys

EN = r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100003.txt"
VI_PATH = r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10360100003.txt"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# line_no -> VI text field (message*/center include trailing '<br> '; title has none)
VI = {
27: "Tuyệt Đối Không Giao Ghế Phó Chỉ Huy!",
54: "Mắt em đã bị mù...! Anh không phải là người xứng đứng bên cạnh Lady Reyzeria<br>đâu!<br> ",
56: "Lime ơi...!<br> ",
66: "Lime chĩa súng vào Chỉ Huy và bóp cò<br>không một chút do dự.<br> ",
90: "*hấp!*<br> ",
130: "*gừuu...*<br> ",
155: "Một viên đạn xẹt qua bên cạnh Chỉ Huy. Phía trước là một<br>quái vật sắp tấn công một binh sĩ Milesgard đang nghỉ ngơi.<br> ",
157: "Cái gì...! Khi nào con quái vật đó xuất hiện?<br>Lime đã nhắm bắn nó sao?<br> ",
197: "Suýt quá!<br>Cảm ơn Phó Chỉ Huy Lime!<br> ",
209: "Chắc chắn là một loại quái vật ẩn mình.<br>Không có gì lạ khi chúng ta không nhận ra.<br> ",
255: "Ôi‚ trời ạ‚ nếu có thứ gì em ghét hơn cả anh‚ thì đó chính là bọn<br>quái vật phiền phức này!<br> ",
266: "Thế mà em vẫn chưa nói xong‚ nhưng bọn chúng chẳng chịu hiểu ý!<br> ",
277: "Toàn thể Kỵ Sĩ Milesgard!<br>Đứng yên! Sẵn sàng! Cảnh giác toàn khu vực!<br> ",
329: "Dạ‚ thưa ngài!<br> ",
331: "Ngay khi giọng Lime vang lên‚ các binh sĩ lập tức đứng dậy.<br>Chúng ngay lập tức lập đội hình‚ che chắn lưng cho nhau.<br> ",
372: "Kẻ địch là một con quái vật xảo quyệt giỏi ẩn nấp!<br>Đừng lơi là cảnh giác và tiêu diệt bọn chúng!<br> ",
433: "Xem ra vẫn có mấy con quái vật phiền phức.<br>Em muốn tập trung cảm nhận sự hiện diện của kẻ địch.<br> ",
444: "Lime‚ từ giờ chị giao quyền chỉ huy cho em nhé?<br> ",
455: "*hấp!* Vâng‚ cứ giao cho em‚ Lady Reyzeria!<br> ",
466: "Ta trông cậy vào em.<br>Giờ thì‚ trò chơi trốn tìm kết thúc rồi‚ hỡi quái vật!<br> ",
514: "Từ giờ em sẽ nắm quyền chỉ huy!<br>Chúng ta sẽ đẩy lùi quái vật và tiến lên‚ lấy Lady Reyzeria làm trung tâm!<br> ",
574: "Tuân lệnh!<br> ",
589: "(Bọn họ chẳng hề nao núng trước sự thay đổi chỉ huy đột ngột. Các<br>binh sĩ hoàn toàn không hoang mang... Ta có thể thấy họ tin tưởng cô ấy.)<br> ",
591: "(Đúng như ta nghĩ‚ Lime thật đáng gờm.)<br> ",
625: "Dưới quyền chỉ huy của Lime‚ các Kỵ Sĩ Milesgard tiếp tục<br>cuộc điều tra. Và rồi‚ tại nơi sâu nhất của khu vực chưa thám hiểm.<br> ",
645: "Đây là... một mạch ma thạch? Ở một nơi chưa thám hiểm<br>lại có thứ như thế này...<br> ",
665: "Tại đó‚ những ma thạch quý giá tạo thành mạch‚ rọi ánh sáng<br>lấp lánh lên Lime và những người vừa đến.<br> ",
712: "Đội điều tra‚ hãy thu thập càng nhiều thông tin càng tốt. Chúng ta cần<br>báo cáo phát hiện lớn lao này về căn cứ.<br> ",
721: "Tuân lệnh!<br> ",
769: "Một kết quả tuyệt vời. Chuyện này sẽ khiến bọn người ở quê nhà xem xét lại<br>đánh giá của họ về Lady Reyzeria.<br> ",
771: "Tốt. Với việc này‚ chiến dịch đã hoàn toàn thành công.<br> ",
784: "Sao anh lại có bộ mặt 'mọi chuyện đã êm đẹp' thế?<br> ",
786: "Hả?<br> ",
799: "Chúng ta đang giữa cuộc nói chuyện mà! Em vẫn còn rất nhiều điều muốn<br>nói!<br> ",
801: "Anh đùa à... Bài thuyết giáo vẫn chưa kết thúc sao...?<br> ",
812: "Tất nhiên! Em cần khiến anh nhìn nhận mọi chuyện một cách đúng đắn!<br> ",
821: "Rất ít người em coi là xứng đứng bên cạnh<br>Lady Reyzeria!<br> ",
832: "Anh là Chỉ Huy duy nhất của Căn Cứ Tiền Tuyến‚ nên anh phải<br>đáng tin cậy!<br> ",
834: "O-oh. Vậy ra anh được đánh giá như thế à...?<br> ",
836: "Được Lime công nhận cảm thấy thật kỳ lạ. Cô không định nói<br>cái gì đó như 'Đừng bịa chuyện‚ thằng ngốc vô dụng' sao?<br> ",
847: "Thật bất lịch sự. Em không thích anh chút nào‚ một chút cũng không‚ nhưng dù vậy‚ em vẫn luôn<br>công nhận năng lực chỉ huy của anh.<br> ",
856: "Em có khi nào gọi anh là kẻ bất tài đâu?<br> ",
858: "Không... chưa từng.<br> ",
869: "Tất nhiên. Làm sao Lady Reyzeria mà em ngưỡng mộ lại có thể<br>chấp nhận một Chỉ Huy bất tài được.<br> ",
880: "Chính vì thế em sẽ bắt anh rút lại lời ngớ ngẩn rằng em<br>ngang hàng với Lady Reyzeria!<br> ",
882: "Dù em có nói vậy‚ thì việc em tài giỏi<br>như Reyzeria đã được chứng minh rồi.<br> ",
893: "Hah! Hãy nhìn kết quả này! Các Kỵ Sĩ Milesgard đã tự mình tiến hành<br>cuộc thám hiểm và còn tìm thấy cả mạch ma thạch!<br> ",
904: "Đây là năng lực của Lady Reyzeria! Làm sao có thể giống của em được?<br> ",
906: "Từ nửa chừng trở đi‚ toàn bộ là do em chỉ huy‚ phải không? Không phải<br>ai thường mà là nhờ kỹ năng của em.<br> ",
917: "Ừm... với tư cách là phó quan của Lady Reyzeria‚ em quả có niềm tự hào<br>không thua kém ai.<br> ",
924: "Nhưng kết quả này chỉ có thể nhờ Lady Reyzeria! Em<br>chỉ làm những gì cần thiết.<br> ",
926: "Ý ta là đó là một công việc tốt. Em đã giữ bình tĩnh‚ không bao giờ thiếu sót<br>quan sát xung quanh‚ và chỉ huy mọi người bằng những mệnh lệnh chính xác.<br> ",
928: "Em có can đảm nói lên ý kiến trước cả cấp trên‚ và có<br>năng lực nắm quyền chỉ huy khi cần với tư cách phó quan—tất cả đều xuất sắc.<br> ",
930: "Nếu em không phải là phó quan của Reyzeria‚ chắc chắn ta đã tuyển mộ em rồi.<br> ",
941: "U-um... c-chuyện đó...! Lady Reyzeria sẽ xử lý tất cả còn tốt hơn thế‚<br>phải không ạ!<br> ",
952: "Điều đó không thay đổi việc em kém cỏi hơn Lady Reyzeria!<br> ",
954: "Không‚ em chẳng kém cỏi chút nào. Ngay cả Reyzeria cũng hẳn thấy<br>như ta.<br> ",
956: "Dù sao thì‚ một Chỉ Huy sẽ chọn người giỏi hơn mình làm<br>phó quan.<br> ",
960: "...em không đồng ý sao‚ Reyzeria?<br> ",
1004: "Không nghi ngờ gì. Lime tài giỏi hơn em rất nhiều.<br> ",
1058: "Lady Reyzeria ơi...!<br> ",
1069: "Chính vì thế em sẽ không giao Lime cho anh đâu. Tiếc quá là anh đã<br>tốn công nịnh nọt em ấy‚ phải không?<br> ",
1071: "Hmph. Sẽ còn nhiều cơ hội. Anh đừng làm em thất vọng.<br> ",
1117: "Lady Reyzeria và Chỉ Huy... đang tranh giành em...! Chuyện này quá<br>đẹp để thành sự thật... Có phải đây là giấc mơ...?<br> ",
1170: "Xin lỗi‚ Lime. Có vẻ em bắt đầu hợp ý với<br>Chỉ Huy rồi‚ nhưng chị không thể để em đi được.<br> ",
1181: "Hah! K-không‚ hoàn toàn không đúng! Em đâu có hợp ý với<br>Chỉ Huy hay gì đâu!<br> ",
1192: "Một gã đàn ông chỉ hơi có chút lý trí và biết điều... em chẳng có<br>chút hứng thú với gã như thế!<br> ",
1194: "...Đánh giá thật sáng lạn.<br> ",
1205: "*hư hư hư*. Thấy chưa? Phó quan của em là một cô gái ngoan‚ phải không?<br> ",
1207: "Em thực sự ghen tị‚ chết tiệt.<br> ",
1238: "<size=48>Một Vài Ngày Sau.</size>",
1289: "Chúng ta đã nhận được lời khen ngợi từ Milesgard về chiến dịch<br>hôm trước.<br> ",
1298: "Hiệp Sĩ Đoàn đã tự mình hoàn thành xuất sắc nhiệm vụ thám sát và<br>đạt được những kết quả lớn lao.<br> ",
1307: "Cả hai đều góp phần nâng cao vị thế của Lady Reyzeria.<br> ",
1318: "Với những kết quả như thế này‚ ngay cả bọn người ở quê nhà cũng sẽ phải<br>công nhận năng lực của Lady Reyzeria!<br> ",
1329: "*hư hư hư*. Anh cũng nhận được lời khen từ cấp trên‚ phải<br>không?<br> ",
1340: "Đừng bận tâm đến em. Nhưng em thật lòng vui vì Lime đã được<br>công nhận đúng mức.<br> ",
1351: "Sự công nhận của em chẳng quan trọng chút nào! Điều quan trọng là Lady<br>Reyzeria nhận được phần xứng đáng!<br> ",
1360: "Ôi chao‚ em đoán thuộc cấp đúng là giống người chỉ huy của mình.<br> ",
1371: "Nhân tiện‚ Lime. Em nên cảm ơn anh vì chuyện này‚ hay là gã đó?<br> ",
1382: "Hả? A-anh đang nói gì vậy? Em đâu có làm gì...<br> ",
1393: "Ôi‚ nếu không phải là...<br> ",
1395: "Hửm‚ Reyzeria và Lime. Hai người có vẻ vui vẻ. Có chuyện<br>gì xảy ra vậy?<br> ",
1406: "Chỉ Huy...<br> ",
1417: "*hư hư*‚ không có gì quan trọng.<br> ",
1465: "Xem ra kế hoạch xảo quyệt của anh đã phát huy tác dụng. Đánh giá của chúng ta ở quê nhà<br>đã khá hơn một chút.<br> ",
1467: "...Ơ‚ anh nhận ra rồi? Giả vờ không biết‚ thật là tệ quá.<br> ",
1478: "Anh và Lime trông có vẻ vui vẻ. Em chỉ nghĩ sẽ<br>tệ nếu chen ngang.<br> ",
1489: "Tuy nhiên... lần sau đừng loại em ra. Nếu là kế hoạch của anh‚ em sẽ<br>theo đó mà làm.<br> ",
1491: "Thế thì yên tâm. Chỉ là hãy chuẩn bị tinh thần bị vắt kiệt sức.<br> ",
1502: "Ôi‚ nếu anh thất bại thảm hại‚ em sẽ để các Kỵ Sĩ Milesgard thu nhận anh.<br>Em sẽ bắt anh làm việc cật lực từ thấp lên cao‚ nên cứ yên tâm.<br> ",
1504: "Nghe ai nói kìa... *khư khư khư*...<br> ",
1515: "Anh nữa‚ *hư hư hư*...<br> ",
1577: "Ách! Đủ rồi! Em sẽ không cho phép thêm nữa!<br> ",
1579: "C-cô làm sao thế‚ Lime! Đâu phải anh đang sỉ nhục Reyzeria‚ đúng<br>không?<br> ",
1588: "Ah‚ phải rồi. Chúng ta đâu có cãi nhau.<br> ",
1599: "Trông với ta thì hai người đang tán tỉnh nhau đấy!<br> ",
1601: "K-không đúng đâu!<br> ",
1612: "Câm miệng! Đồ vô liêm sỉ‚ biến thái dơ bẩn! Em tuyệt đối không<br>cho phép anh lại gần Lady Reyzeria hơn em!<br> ",
1631: "Dù là anh‚ em cũng sẽ không từ bỏ vị trí phó quan của<br>Lady Reyzeria!<br> ",
1633: "Ôi‚ thôi tuỳ em... cứ làm gì thì làm...<br> ",
}

def main():
    raw = open(EN, "rb").read()
    text = raw.decode("utf-8-sig")
    has_crlf = b"\r\n" in raw
    lines = text.split("\n")

    # Enumerate EN text records (their line numbers, 1-based in `lines`)
    en_recs = []
    for i, ln in enumerate(lines, 1):
        if ln.startswith(TEXT_CMDS):
            en_recs.append(i)
    print("EN text record count:", len(en_recs))

    # Guard 1: record-count
    assert len(VI) == len(en_recs), f"VI={len(VI)} != EN={len(en_recs)}"
    missing = [n for n in en_recs if n not in VI]
    extra = [n for n in VI if n not in en_recs]
    assert not missing, f"missing VI for EN lines {missing}"
    assert not extra, f"VI for non-text lines {extra}"

    # Guard 2 & 3: per-line BR count + ASCII comma, print ALL mismatches
    br_bad = []
    comma_bad = []
    out_lines = []
    for i, ln in enumerate(lines, 1):
        if i in VI:
            vi = VI[i]
            if "," in vi:
                comma_bad.append(i)
            if ln.startswith("title,"):
                parts = ln.split(",")
                parts[1] = vi
                new = ",".join(parts)
            else:
                parts = ln.split(",")
                parts[2] = vi
                new = ",".join(parts)
            old_tf = (ln.split(",", 2)[2] if not ln.startswith("title,") else ln[len("title,"):])
            if old_tf.count("<br>") != vi.count("<br>"):
                br_bad.append((i, old_tf.count("<br>"), vi.count("<br>")))
            out_lines.append(new)
        else:
            out_lines.append(ln)

    if br_bad:
        print("BR MISMATCHES:")
        for i, o, n in br_bad:
            print(f"  L{i}: en={o} vi={n}")
    if comma_bad:
        print("ASCII COMMA in VI at lines:", comma_bad)
    assert not br_bad, "BR mismatches present"
    assert not comma_bad, "ASCII comma present in VI"

    out = "\n".join(out_lines)
    if has_crlf:
        out = out.replace("\r\n", "\n").replace("\n", "\r\n")
    data = b"\xef\xbb\xbf" + out.encode("utf-8")
    import os
    os.makedirs(os.path.dirname(VI_PATH), exist_ok=True)
    open(VI_PATH, "wb").write(data)
    print("WROTE", VI_PATH, "lines:", len(out_lines), "bytes:", len(data))

if __name__ == "__main__":
    main()

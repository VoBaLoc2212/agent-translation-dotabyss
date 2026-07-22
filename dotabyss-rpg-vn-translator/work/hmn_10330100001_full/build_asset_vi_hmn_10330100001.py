# -*- coding: utf-8 -*-
"""Field-index generator for hmn_10330100001 (EN-asset-is-English case).

Rebuilds the VI asset by replacing the text field (parts[1] for title,
parts[2] for message*/messageTextUnder/messageTextCenter) with the VI
string, keeping every other field (speaker labels, voice ids, flags) byte
identical to the EN asset. BOM + CRLF preserved exactly.
"""
import pathlib

EN = pathlib.Path(
    "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100001.txt"
)
VI_PATH = pathlib.Path(
    "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100001.txt"
)

# line_no -> VI text field. Fullwidth ，replaced by U+201A ‚; <br> counts preserved.
VI = {
    47: "Tôi Là Phóng Viên Emeralda",
    63: "Cái gì cơ?! Anh từ nước nào thế!?<br> ",
    73: "Em đến từ Eldorana! Chính anh mới là kẻ từ xó xỉnh nào đó phải không!<br> ",
    98: "Á‚ bắt đầu rồi‚ bắt đầu rồi...♪<br> ",
    108: "—Tách‚ tách!<br> ",
    131: "Đồ ngốc. Phí phim quá. Đánh nhau kiểu này thì chẳng thành tin tức gì nữa đâu.<br> ",
    134: "Đúng vậy. Muốn trang báo nóng bỏng thì cần một nhân vật tệ hại rõ ràng nhưng<br>mà có sức ảnh hưởng mạnh — 'Đặc Tin' — xuất hiện.<br> ",
    139: "Chuẩn luôn. Giờ đi tác nghiệp và đưa tin Đặc Tin đi!<br> ",
    147: "Dạ vâng! Em đi bám đuôi Đặc Tin đây!<br> ",
    193: "Chỉ Huy! Anh làm giấy tờ vất vả rồi ạ. Anh làm tốt lắm!<br> ",
    195: "À‚ em mệt quá... Thôi‚ việc xong rồi‚ đọc báo cho phải phép.<br> ",
    201: "Ồ‚ xong rồi thì cho em mượn nhé! Báo từ các nước<br>là nguồn tin tình báo quý giá mà!<br> ",
    203: "Chúng cũng khá giải trí đúng không‚ hửm?<br> ",
    205: "'Đặc Tin! Bắt được tin lớn ở Căn Cứ Tiền Tuyến!'? Họ làm một<br>bài đặc biệt về chúng ta kìa!<br> ",
    214: "Á‚ b‚ bài báo đó là—<br> ",
    221: "Hửm? 'Sự Thật Gây Sốc Được Phơi Bày!' ...?<br> ",
    251: "Dù mang cái tên hào nhoáng Căn Cứ Tiền Tuyến‚ thực chất nó chẳng hơn gì một trạm phòng thủ tạm bợ toàn lính chắp vá.",
    253: "Lũ lính đánh thuê thô bạo say sưa ở quán rượu‚ chửi bới‚ và lính của Tam Quốc cứ đánh nhau suốt. Nói thật‚ chúng thích đánh nhau hơn cầm đũa.",
    255: "Tất nhiên‚ bọn đó chẳng có gu thẩm mỹ hay thời giờ mà quan tâm quần áo tóc tai. Nên thay bằng một lực lượng phòng vệ bài bản‚ có tổ chức.",
    282: "...Lời nhận xét thật cay nghiệt. Alicia‚ em đã biết chuyện này rồi à?<br> ",
    290: "V‚ phải rồi... Thật ra bài báo đó đã lan truyền khắp căn cứ rồi...<br> ",
    292: "Em không thể coi nó hoàn toàn là tin đồn thất thiệt‚ nhưng bài báo này<br>rõ ràng viết với ác ý. Của báo nào vậy?<br> ",
    303: "Của Eldorana...<br>Chúng ta nên khiếu nại không?<br> ",
    305: "Hmph‚ cứ kệ đi. Mọi người sớm quên thôi.<br>...Hửm?<br> ",
    312: "Sao thế‚ Chỉ Huy?<br> ",
    327: "(...Em tưởng mình thấy ai ngoài cửa sổ‚ nhưng có lẽ chỉ là<br>tưởng tượng thôi.)<br> ",
    361: "Suýt quá! Anh mà nhận ra sự hiện diện của em... Đúng là<br>Chỉ Huy có trí giác sắc bén. Anh còn chẳng hề nao núng trước chuyện này.<br> ",
    365: "Nhưng vẻ bình tĩnh đó — anh nghĩ nó kéo dài được bao lâu?<br>Fufufu!♪<br> ",
    410: "<size=48>—Ngày Hôm Sau—</size>",
    422: "...Thì thầm‚ thì thầm.<br> ",
    425: "...Tán gẫu‚ tán gẫu.<br> ",
    444: "Em cứ thấy ánh mắt đổ dồn về mình... Cái quái gì đang xảy ra thế?<br> ",
    463: "C‚ Chỉ Huy! Nguy rồi! Xin anh xem này!<br>Là tờ báo Eldorana đó...<br> ",
    465: "...'Tin Nóng: Chỉ Huy Căn Cứ Tiền Tuyến Là Kẻ Rác Rưởi!'<br>'Phỏng vấn những người phụ nữ bên cạnh anh ↓'<br> ",
    501: "'Chỉ Huy là người thế nào?<br>...À‚ anh ấy là anh hùng theo nghĩa tồi tệ nhất.'<br> ",
    527: "'Hửm? Anh muốn biết anh ấy có bắt nạt em không?'<br> ",
    530: "'Không bình luận!♪'<br> ",
    557: "'C‚ có lẽ anh ấy không phải tuýp người nghiêm túc đâu‚ đúng không?'<br> ",
    586: "'Nói vậy‚ nhưng rõ ràng các cô gái khiếp sợ. Bằng chứng của<br>bạo hành quyền lực. Và việc anh ta thay người phụ nữ này qua người khác—'<br> ",
    617: "'Ừm đúng rồi‚ đúng thế. Phu quân giống như chủ nhân căn cứ này vậy‚ anh biết mà.<br>Còn em thì... đúng không? Fufufu!♡'<br> ",
    642: "'T‚ lời chủ nhân là tuyệt đối!'<br> ",
    667: "Đê tiện...<br> ",
    697: "'...Và thế là‚ xác minh hậu trường đã khẳng định. Bám đuôi Chỉ Huy<br>thì thấy anh ta tối nào cũng đến quán rượu‚ xa hoa tột độ.'<br> ",
    699: "'Cái lạm dụng quyền lực hèn hạ này tuyệt đối không thể tha thứ. Phóng viên chúng tôi<br>sẽ tiếp tục điều tra gã Chỉ Huy rác rưởi này. Hãy đợi số tiếp theo!'<br> ",
    701: "...Cái quái gì thế này!<br> ",
    709: "E‚ thật tệ phải không?<br> ",
    711: "Với lại‚ Alicia‚ chẳng phải em cũng nói xấu gì đó trong<br>cuộc phỏng vấn đó sao?<br> ",
    718: "K‚ không‚ hiểu lầm thôi! Sophia‚ mọi người và em đã nói<br>nhiều về ưu điểm của anh mà‚ Chỉ Huy!<br> ",
    720: "Vậy là họ đã cắt ghép ác ý ra khỏi bối cảnh?<br> ",
    728: "Đúng thế! Em phẫn nộ vì họ dám viết thứ như thế! Chuyện này<br>tuyệt đối không thể tha thứ!<br> ",
    730: "Hửm? Khoan đã‚ nếu em được phỏng vấn — em có biết ai là người viết<br>bài báo này không?<br> ",
    733: "Vâng! Một nữ phóng viên — cô ấy tự xưng là Emeralda!<br> ",
    735: "Ra vậy... Được rồi! Đi tìm Emeralda thôi!<br> ",
    764: "Ở kìa? Có ai gọi em không?<br> ",
    799: "Á! Chỉ Huy‚ đây rồi! Đây là Emeralda!<br> ",
    831: "Xin chào! Em là Emeralda‚ phóng viên báo Eldorana. Cảm ơn<br>em đã hợp tác trong cuộc phỏng vấn hôm nọ nhé‚ Alicia!<br> ",
    837: "Bài báo đó được độc giả đón nhận cực lớn! Sếp em thì tươi cười. Em còn<br>nhận thưởng nữa. Biết đâu em được thăng chức!<br> ",
    847: "Bài báo đó rốt cuộc là cái gì! Hãy đính chính đi!<br> ",
    854: "Đính chính cái gì? Em chỉ viết những gì được kể. Em đâu có in lời nói dối‚ đúng<br>không em?<br> ",
    859: "Nhưng chúng ta nói biết bao chuyện khác! Thật bất công khi chỉ<br>kịch tính hóa mấy phút đầu như vậy!<br> ",
    867: "Nhưng sự thật là sự thật. Đấy gọi là tự do báo chí.<br> ",
    872: "N‚ nhưng mà... dù vậy... *nấc*...!<br> ",
    874: "Emeralda‚ đúng không? Chỉ xác nhận thôi. Tất cả bài báo của em đều dựa trên<br>tác nghiệp thật nên em không có ý định rút lại. Đúng chứ?<br> ",
    881: "Đúng vậy! Em bắt gặp anh‚ Đặc Tin‚ đến quán rượu mỗi<br>ngày luôn đấy!<br> ",
    888: "5 ngày trước: từ 22:04 đến 3:05. 4 ngày trước: từ 22:14<br>đến 2:46. 3 ngày trước: từ 21:08 đến 4:29.<br> ",
    894: "Ngày nào‚ một người phụ nữ khác‚ tiệc tùng đến tận sáng — đúng là<br>kẻ làm tan vỡ trái tim‚ anh nhỉ?<br> ",
    902: "Biết đâu một ngày anh bị đâm trong cuộc cãi vã tình địch‚ nên<br>em chẳng rời mắt khỏi anh được. Fufufu!♪<br> ",
    904: "Anh thua rồi. Em không nhớ chính xác giờ giấc‚ nhưng có lẽ<br>chuẩn lắm.<br> ",
    911: "Thấy chưa? Anh bảo rồi‚ em chẳng bao giờ viết lời nói dối.<br> ",
    913: "Vậy là em đã bám đuôi anh suốt từ nãy‚ mà anh chẳng hề hay<br>biết gì cả.<br> ",
    915: "Thật là khó tin!<br> ",
    923: "...Hửm?<br> ",
    925: "Em hay bị ám sát nên luôn cảnh giác‚ và em có<br>bảo vệ đi theo.<br> ",
    927: "Thế mà em vẫn bám đuôi anh mà không bị lộ. Em đúng là<br>một phóng viên cừ khôi.<br> ",
    933: "…!<br> ",
    938: "Đúng rồi! Anh hiểu mà! Kỹ năng tác nghiệp của em thật tuyệt vời!<br> ",
    944: "Đúng như Đặc Tin nói! Em cũng ghê gớm phết!<br> ",
    949: "O‚ ồ...?<br> ",
    954: "Em chẳng hề nao núng khi đối tượng phàn nàn‚ và chưa một lần<br>viết lời nói dối!<br> ",
    961: "Hơn nữa‚ em khéo chọn đề tài kích thích sự tò mò độc giả và<br>viết bằng văn phong nhẹ nhàng‚ lôi cuốn khiến người ta muốn đọc tiếp.<br> ",
    971: "Chúng đâu chỉ là tin đồn! Bài báo của em là giải trí được làm từ<br>thông tin! Món ăn tinh tế! Nói cách khác‚ chúng là giải trí thuần túy!<br> ",
    981: "Thế mà! Tổng hành dinh lại đẩy em đến xó xỉnh này... Sao mà<br>công bằng được!<br> ",
    985: "Hừm...? Em đâu đến Căn Cứ Tiền Tuyến vì tự nguyện‚<br>đúng không?<br> ",
    993: "Tất nhiên là không! Vùng biên giới này chẳng hợp gu em. Em muốn về<br>thành phố ngay thôi!<br> ",
    1000: "Cầm ly latte từ quán cà phê sành điệu‚ lượn các cửa hàng hiệu‚<br>đi ăn thử bánh ngọt tay cầm sinh tố‚ rồi yoga và spa thư giãn...<br> ",
    1005: "Và tất nhiên‚ đi gặp gỡ ở quán bar sành điệu! Em thật sự nhớ cuộc sống đó!<br> ",
    1009: "Trông em có vẻ tích tụ nhiều stress...<br> ",
    1012: "Em muốn uống tequila và cụng ly!<br> ",
    1014: "Thế thì chẳng sành điệu gì‚ đúng không?<br> ",
    1017: "Nhưng mà người uống không phải em.<br> ",
    1020: "...Càng tệ hơn!<br> ",
    1027: "Nhưng tổng hành dinh và sếp bảo em chẳng được về Eldorana cho đến khi em<br>kiếm được một tin bom cực khủng... *thở dài*<br> ",
    1031: "Hừm... Thế thì sao em không bám sát anh một thời gian và làm<br>vài bài tác nghiệp thực tế nhỉ?<br> ",
    1041: "Ơ‚ anh chắc chứ?<br> ",
    1043: "Ừ. Không khoe đâu‚ nhưng em là người nổi bật nhất ở đây‚ nên em<br>làm tư liệu báo chí tuyệt vời. Đỡ cho em công bám đuôi em đúng không?<br> ",
    1046: "Ừ thì‚ đúng vậy em đoán. Ý em là‚ nếu viết được bài tốt‚ em sẽ được<br>về thành phố. Như mơ thành hiện thực vậy.<br> ",
    1078: "Chỉ Huy‚ anh chắc về chuyện này chứ...?<br> ",
    1080: "Không sao. Thà công khai còn hơn cứ che đậy.<br> ",
    1101: "Thế thì‚ đầu tiên... sao anh không đi cùng em thám hiểm<br>Đại Huyệt nhỉ?<br> ",
}


def main():
    raw = EN.read_bytes()
    has_crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig")
    lines = text.split("\n")
    for i, l in enumerate(lines, 1):
        if i in VI and l.startswith(("title,", "message,", "messageTextUnder,", "messageTextCenter,")):
            parts = l.split(",")  # no maxsplit: preserve trailing empty fields
            idx = 1 if l.startswith("title,") else 2
            vi = VI[i]
            assert "," not in vi, f"ASCII comma in VI line {i}: {vi!r}"
            parts[idx] = vi
            lines[i - 1] = ",".join(parts)
    out = "\n".join(lines)
    data = b"\xef\xbb\xbf" + out.encode("utf-8")
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_PATH.write_bytes(data)
    print(f"WROTE {VI_PATH} lines={len(lines)} crlf={has_crlf}")


if __name__ == "__main__":
    main()

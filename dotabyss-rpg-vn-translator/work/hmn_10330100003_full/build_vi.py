#!/usr/bin/env python
# Build VI output for hmn_10330100003 from EN asset (EN-asset-is-English case).
# Translate JP->VI via ja.json semantics; EN asset is structural authority.
# Preserve delimiters, <br> counts, <user>, BOM, CRLF, trailing "<br> " suffix.
import io, sys

ROOT = "E:/AgentTranslation"
EN = f"{ROOT}/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100003.txt"
VI = f"{ROOT}/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100003.txt"

TITLE = "Viết Cho Xem Bài Báo Tuyệt Vời Nhất!"

# line_no -> VI text field (parts[2] for message; comma-free inside, use U+201A '‚')
MSG = {
 51: "—Emeralda‚ đang truy tìm một tin độc quyền‚ tiếp tục bám đuôi Chỉ Huy.<br> ",
 68: "(Giờ thì‚ Scoop ơi. Có vẻ ngài đang chuẩn bị đi chơi đêm<br>nhưng ngài định đi đâu thế?)<br> ",
 72: "(Cá độ ngầm với tỷ lệ cược điên rồ? Hay là chăm sóc<br>đứa con hoang ngoài giá thú?)<br> ",
 76: "(Không‚ thực ra em biết mà. Scoop thì hay thất thường‚ nhưng tận sâu trong lòng thì…)<br> ",
 94: "Hử?<br> ",
 109: "Khư khư! Thành công mỹ mãn rồi…!<br> ",
 120: "—Ánh mắt Emeralda bắt gặp một người đàn ông đang chạy trốn khỏi Khu Chợ.<br> ",
 129: "…Hử? Người vừa rồi‚ có gì đó khiến em bận tâm.<br> ",
 153: "H-hử? N-nó biến mất rồi! Không còn ở đây nữa! Doanh thu hôm nay chẳng thấy<br>đâu cả!<br> ",
 176: "(…Không thể nào‚ là ông vừa nãy!<br> ",
 179: "(Á‚ nhưng Scoop ơi đã ở quá xa rồi… cứ đà này anh ấy sẽ biến đi<br>đâu mất—mà nếu em đuổi theo thì sẽ lạc mất gã đàn ông khả nghi kia…)<br> ",
 196: "Aa… *sụt sịt*…<br> ",
 203: "Aaaah‚ chết tiệt! Sao em không thể tách thân mình ra làm hai được chứ!<br> ",
 227: "(…*sụt sịt* Kết cục thì‚ linh hồn nhà báo trong em trỗi dậy và em đuổi theo<br>gã đàn ông đó…)<br> ",
 230: "(Tin độc quyền của em… tin độc quyền của em ơi là bay biến mất rồi~~~~!<br> ",
 233: "(Nhưng em phải chịu đựng‚ Emeralda ơi! Em phải chuyển hướng và đeo bám câu chuyện<br>này cho đàng hoàng…)<br> ",
 237: "(Á‚ kia rồi‚ ông vừa nãy kia kìa!<br> ",
 252: "Một số lượng lớn đạo tặc đã tập hợp trong tầm mắt của Emeralda.<br>Một… năm… hai mươi… gần ba mươi tên? Emeralda kinh ngạc.<br> ",
 276: "Khư khư‚ nhìn xem! Núi tiền này đây! Hóa ra gã tiểu thương đó đã<br>tích trữ hết đấy!<br> ",
 278: "Tao cũng moi được mớ này! Căn Cứ Tiền Tuyến là món ngon dễ hớp lắm!<br> ",
 302: "(…bọn này trông như một băng đảng trộm cướp khá lớn nhỉ?<br> ",
 305: "(Một mình em thì nguy hiểm quá… em cần nhanh chóng báo cho Scoop ơi và<br>để anh ấy xử lý chuyện này—)<br> ",
 324: "*rắc*<br> ",
 338: "Ai đó!?<br> ",
 347: "Chết! Em dẫm phải cành cây rồi!<br> ",
 353: "Là một cô gái! Đừng để nó trốn thoát!<br> ",
 364: "Chết!<br> ",
 380: "Emeralda móc tên và buông lỏng dây cung bắn về phía bọn trộm. Một‚ hai‚<br>ba… những gã phía trước ngã xuống trong tích tắc.<br> ",
 404: "Nhưng trong khoảng thời gian đó‚ nhiều đạo tặc khác đã kéo tới. Khi nàng quay người<br>bỏ chạy‚ Emeralda khựng lại vì kinh ngạc.<br> ",
 416: "E-em bị bao vây rồi…? Lúc nào chuyện này xảy ra vậy!?<br> ",
 448: "Ngươi nghĩ ngươi có thể chạy thoát sau khi lếch vào lãnh địa của bọn này sao? Hãy<br>chuẩn bị tinh thần đi… Khư khư.<br> ",
 481: "(Giá như em đã bám đuôi Scoop ơi‚ em đã tóm được một câu chuyện tuyệt vời<br>và về thành thị‚ với một cuộc sống thành thị vui vẻ đang chờ đợi em…)<br> ",
 512: "Thế thì‚ trước tiên hãy lột trần nó ra—<br> ",
 515: "Ồ? Rồi sau đó thì sao?<br> ",
 522: "Hả—!<br> ",
 529: "Hể… Scoop ơi!?<br> ",
 531: "Không chỉ mình ta đâu. Hãy nhìn kỹ vào bóng tối đi.<br> ",
 548: "Emeralda và bọn trộm làm theo lời dặn. Phía sau<br>Chỉ Huy‚ đội bảo vệ của Căn Cứ Tiền Tuyến đã xếp hàng.<br> ",
 574: "Bẫy rồi! Tất cả‚ tấn công!<br> ",
 576: "Tuân lệnh!<br> ",
 578: "Bọn bay! Hãy chuẩn bị đi!<br> ",
 600: "Emeralda. Em không sao chứ?<br> ",
 605: "Á‚ vâng—nhưng sao ngài lại ở đây?<br> ",
 607: "Trước đây anh đã không nhận ra em đang bám đuôi anh‚ phải không? Nên anh rút kinh<br>nghiệm từ đó và cho lính canh bám đuôi em‚ phòng hờ.<br> ",
 615: "Ê ê! Em hoàn toàn không hề hay biết!<br> ",
 617: "Thuộc hạ của anh cũng lão luyện không kém‚ em biết mà.<br> ",
 619: "Dạo này chúng ta thân thiết hơn‚ nên anh định hủy việc bám đuôi em. Nhưng<br>Alicia đã lo cho em—cũng nhờ vậy mà em gặp may đấy.<br> ",
 623: "R-ra là vậy sao…<br> ",
 642: "—Emeralda hướng mắt về cuộc vây bắt hoành tráng của đội bảo vệ. Bọn trộm<br>không tài nào chống cự nổi và bị tóm gọn toàn bộ.<br> ",
 646: "Ngừng kháng cự! Đầu hàng đi!<br> ",
 653: "Híc…<br> ",
 670: "Ủa‚ bọn họ bị đánh tơi bời… Đáng sợ thật…<br> ",
 674: "Nhưng khi họ đứng về phía chúng ta‚ họ thật đáng tin cậy‚ phải không?<br> ",
 682: "(Ừ‚ đúng vậy. Vì bọn họ là kẻ xấu định hại em‚ nên thực ra<br>cảm giác khá sảng khoái.<br> ",
 684: "Phải‚ phải! Với chuyện này‚ em có thể viết thêm một bài báo hay nữa‚ đúng không?<br> ",
 698: "C-chuyện đó thì…<br> ",
 715: "Chẳng ai thèm muốn điểm tốt của Chỉ Huy đâu! Căn Cứ Tiền Tuyến<br>chẳng cần gì ngoài vụ bê bối!<br> ",
 734: "Thôi‚ anh để cách viết thế nào cho em‚ Emeralda. Anh không có ý định<br>phàn nàn về 'tự do báo chí' đâu.<br> ",
 742: "…Rõ rồi!<br> ",
 749: "Phóng viên lão luyện này sẽ viết bài báo tuyệt hay nhất! Cứ đợi đó mà xem!<br> ",
 766: "Khư khư…<br> ",
 777: "Chỉ Huy‚ ngài đang vui đấy.<br> ",
 779: "À‚ tất nhiên rồi. Cứ đọc bài báo Emeralda viết xem.<br> ",
 787: "Dĩ nhiên em đã đọc rồi! Nó đầy những điều tốt đẹp về mọi người ở<br>Căn Cứ Tiền Tuyến và ngài‚ Chỉ Huy—một bài viết tuyệt vời!<br> ",
 791: "Đó là một sự kiện ly kỳ có liên quan đến việc bắt giữ băng trộm. Đây là<br>một bài báo hấp dẫn độc giả sẽ thích.<br> ",
 793: "Đánh giá và doanh số hẳn sẽ tốt. Chắc chắn điều này sẽ giúp Emeralda<br>trở về trụ sở chính.<br> ",
 796: "Đúng vậy! Tuy nhiên‚ sẽ buồn khi phải nói lời tạm biệt với Emeralda…<br> ",
 798: "Ừ‚ đúng thế. Dạo này chúng ta đã cùng hành động với nhau khá nhiều…<br> ",
 822: "Chỉ Huy‚ đừng sướt mướt nữa. Bọn em đã chuẩn bị một bữa tiễn biệt<br>rồi mà.<br> ",
 824: "Emeralda sẽ sớm quay lại với quyết định của mình thôi‚ nên chúng ta ăn mừng đi!<br> ",
 861: "*thở dài*… Chào buổi tối…<br> ",
 892: "Á‚ nói sao trời nghe vậy!<br> ",
 895: "Này‚ Emeralda‚ sao em buồn rầu thế?<br> ",
 902: "Đâu phải em muốn thế… em nhận được lệnh từ trụ sở chính là em sẽ<br>ở lại Căn Cứ Tiền Tuyến.<br> ",
 908: "Cái gì?! Em không thể về sao!?<br> ",
 910: "Này‚ này‚ chuyện gì đang xảy ra vậy? Bài báo đã gây tiếng vang‚<br>phải không? Tờ báo đã bán chạy mà‚ đúng không?<br> ",
 917: "Tờ báo có bán chạy‚ nhưng em đã phớt lờ hoàn toàn ý định của sếp‚ nên vì<br>ganh ghét mà ông ấy đã từ chối yêu cầu của em.<br> ",
 925: "Và sếp của em đã một mình quay về trụ sở chính…<br> ",
 927: "Hả? Cái quái gì vậy!?<br> ",
 935: "Đúng là em muốn nói đấy! Aaaah‚ cuộc sống thành thị của em đã tiêu tan rồi!<br> ",
 938: "À‚ em biết chuyện này sẽ xảy ra ngay cả trước khi viết bài báo.<br> ",
 940: "Thế thì đáng ra em cứ đừng viết nó—ách.<br> ",
 955: "(…Ra là vậy. Emeralda có lẽ đã viết nó để đền ơn anh—)<br> ",
 968: "…Cảm ơn em‚ Emeralda.<br> ",
 972: "Ngài cảm ơn em vì chuyện gì?<br> ",
 974: "Tất nhiên là vì em đã viết một bài báo hay. Nhờ em‚ tinh thần của mọi người<br>đã lên cao.<br> ",
 983: "Thế thì nhẹ nhõm rồi. Và vì ngài đã cứu em‚ giờ chúng ta hết nợ nhau rồi.<br> ",
 993: "Ưm‚ Chỉ Huy… chúng ta phải làm sao với bữa tiễn biệt? Nó đã<br>được chuẩn bị xong rồi‚ nhưng…<br> ",
 995: "Không sao. Thay vì bữa tiễn biệt‚ chúng ta sẽ tổ chức một bữa chào mừng<br>dành cho Emeralda!<br> ",
 1005: "Hử? Dành cho em sao?<br> ",
 1007: "Suy cho cùng‚ em sẽ làm việc ở đây một thời gian‚ phải không? Em là một<br>phóng viên tài năng đưa tin về những chiến tích của chúng ta. Hãy để chúng ta chào đón em!<br> ",
 1035: "Ha ha ha! Nghe tuyệt đấy! Emeralda‚ hôm nay chúng ta uống thả ga<br>luôn nhé!<br> ",
 1042: "Ê ê… em đang dưỡng trái tim tan vỡ ở đây nè‚ biết không?<br> ",
 1049: "Em thà về thành thị còn hơn uống rượu ở một nơi như thế này!<br> ",
 1067: "Mọi người vây quanh Chỉ Huy và Emeralda bật cười. Một<br>làn sóng cạn ly nổi lên từ đâu đó‚ và bữa chào mừng bắt đầu.<br> ",
 1084: "(…À‚ em sẽ chẳng bao giờ nói điều này thành tiếng‚ nhưng… thành thật mà nói‚ em cũng<br>chẳng ghét bầu không khí này đến thế.)<br> ",
 1092: "(Scoop ơi có vẻ chu đáo hơn em tưởng… có lẽ em sẽ thử sống ở<br>Căn Cứ Tiền Tuyến thêm một thời gian nữa.)<br> ",
}

raw = open(EN, 'rb').read()
text = raw.decode('utf-8-sig')
has_crlf = b'\r\n' in raw
lines = text.split('\n')

# ---- PREFLIGHT: assert <br> count match and no ASCII comma in VI text ----
errors = []
for i, line in enumerate(lines, 1):
    body = line[:-1] if line.endswith('\r') else line
    if body.startswith('title,'):
        continue
    if body.startswith('message,'):
        parts = body.split(',', 5)
        if i in MSG:
            old_tf = parts[2]
            new_tf = MSG[i]
            if old_tf.count('<br>') != new_tf.count('<br>'):
                errors.append(f"LINE {i}: <br> count {old_tf.count('<br>')}->{new_tf.count('<br>')}")
            if ',' in new_tf:
                errors.append(f"LINE {i}: ASCII comma in VI text")
        else:
            errors.append(f"LINE {i}: message line missing from MSG dict")

if len(MSG) != sum(1 for ln in lines if ln.startswith('message,')):
    errors.append(f"MSG dict size {len(MSG)} != message line count")

if errors:
    print("PREFLIGHT FAILED:")
    for e in errors:
        print("  ", e)
    sys.exit(1)
print("PREFLIGHT OK: all <br> counts match, no ASCII commas, dict complete.")

# ---- BUILD ----
out_lines = []
for i, line in enumerate(lines, 1):
    cr = line.endswith('\r')
    body = line[:-1] if cr else line
    if body.startswith('title,'):
        out_lines.append('title,' + TITLE + ('\r' if cr else ''))
    elif body.startswith('message,') and i in MSG:
        parts = body.split(',', 5)
        parts[2] = MSG[i]
        out_lines.append(','.join(parts) + ('\r' if cr else ''))
    else:
        out_lines.append(line)

out = '\n'.join(out_lines)
open(VI, 'wb').write(b'\xef\xbb\xbf' + out.encode('utf-8'))
print(f"WROTE {VI} ({len(out_lines)} lines)")

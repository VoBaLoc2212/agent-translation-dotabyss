#!/usr/bin/env python
# Build VI output for hmn_10340100003 from EN asset (EN-asset-is-English, JP title).
# Replace only the text field (parts[2] for message*, parts[1] for title).
# Keep speaker (parts[1]) and all trailing fields byte-identical.
import io, sys

ASSET = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10340100003.txt"
OUT   = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10340100003.txt"

# VI text fields keyed by 1-based line number. Suffix <br>  mirrored from source.
VI = {
 39:  "Thành Lập! Đội Liệt Sĩ Tiêu Diệt Quấy Rối Tình Dục!",
 66:  "Phù~… Thế là ổn cho việc pha trà cho Chỉ Huy rồi.<br>Giờ em chỉ cần đi mua chút bánh ngọt cho khách ghé thăm thôi…<br> ",
 122: "Làm ơn‚ dừng lại đi! Em van ông đấy!<br> ",
 131: "Cái bản mặt đó là gì vậy!<br>Mày trách tao đấy à? Hả?<br> ",
 140: "K‐không‚ không phải vậy đâu!<br>Làm ơn‚ buông em ra…!<br> ",
 189: "Cái đó… em không thể đứng nhìn được!<br>Này‚ ông kia! Thả cô ấy ra đi!<br> ",
 253: "Hả? Việc này chẳng liên quan gì tới mày!<br>Hay là mày sẽ thay chỗ cô ta hả!<br> ",
 265: "Ự!<br> ",
 309: "Đã xác nhận quấy rối tình dục!<br>Tiến hành bắt giữ!<br> ",
 311: "Ôôôôô!<br> ",
 365: "C‐cái quái gì vậy!? Chúng mày là ai?<br> ",
 402: "Quấy rối tình dục sẽ không được dung thứ!<br> ",
 411: "Bọn này sẽ đánh cho cái thái độ thối nát đó bốc hơi khỏi ông!<br>Hãy chuẩn bị đi!<br> ",
 458: "C‐cái gì vậy!<br>Ý nghĩa của chuyện này là…?<br> ",
 521: "Alicia‚ cô có ổn không?<br> ",
 530: "Carla…?<br>Đây là sao? Những người kia là ai vậy…?<br> ",
 541: "Chúng tôi là một hội những chiến binh được thành lập dưới quyền Chỉ Huy‚<br>không khoan nhượng với sự quấy rối vô lý.<br> ",
 585: "Đội Liệt Sĩ Tiêu Diệt Quấy Rối Tình Dục Tiền Tuyến Căn Cứ!<br> ",
 644: "Tiêu diệt quấy rối tình dục…?<br> ",
 655: "Để em giới thiệu. Joe kẻ lật váy bằng ô‚<br>và Kaiman gã cá sấu chịu đựng tắm chung!<br> ",
 720: "Nhắc tới kỹ thuật cây gậy thì cứ giao cho tôi!<br> ",
 729: "Tôi tự tin vào sức bền của mình!<br> ",
 767: "Gordon sommelier ba số đo! Ghee gã ngửi mùi bám sát!<br> ",
 815: "Dù chúng có cải trang thế nào‚ tôi cũng tìm ra!<br> ",
 824: "Tôi sẽ lần theo mùi chính xác hơn cả chó quân dụng!<br> ",
 882: "Họ chính là những thành viên kiêu hãnh của<br>Đội Liệt Sĩ Tiêu Diệt Quấy Rối Tình Dục Tiền Tuyến Căn Cứ!<br> ",
 893: "Toàn là bọn biến thái! Chỉ Huy đã ra lệnh gì vậy?!<br>Chỉ Huy ơi!<br> ",
 948: "Thế ra là chuyện như vậy…<br> ",
 950: "Ra vậy. Có vẻ Carla đang làm tốt đấy.<br> ",
 961: "Kết quả của việc làm tốt là ra thế này sao?! Chỉ Huy đã ra mệnh lệnh gì vậy?!<br> ",
 963: "Ta chỉ đưa ra một đề xuất thôi. Kiểu như‚<br>sao không lập một đội chuyên tiêu diệt quấy rối tình dục nhỉ?<br> ",
 1000:"Vậy‚ nếu em tin tưởng ta‚ muốn thử sức không?<br> ",
 1034:"Vâng‚ em tin tưởng Chỉ Huy! Xin hãy giao việc này cho em!<br> ",
 1045:"Nhưng‚ cụ thể em phải làm gì?<br> ",
 1047:"Tiền Tuyến Căn Cứ‚ nơi sát Đại Huyệt‚ luôn bên bờ vực của cái chết.<br>Có lẽ là bản năng sinh tồn‚ nhưng một số gã không kìm nén nổi dục vọng.<br> ",
 1049:"Có lẽ vì thế mà quấy rối tình dục đã trở thành vấn đề lớn.<br> ",
 1060:"Vậy đây là vấn đề riêng của căn cứ này sao.<br> ",
 1062:"Bởi vậy ta muốn em‚ Carla‚ chỉ huy một đơn vị chuyên biệt để phòng chống quấy rối—<br>không‚ để tiêu diệt quấy rối tình dục.<br> ",
 1073:"Tiêu diệt quấy rối tình dục…?!<br> ",
 1085:"Vâng‚ em sẵn sàng! Nhưng lập đội nghĩa là cần binh sĩ‚ đúng không?<br> ",
 1087:"Đúng vậy. Và không phải binh sĩ bình thường.<br>Ta cần những gã thấu rõ loại người hay quấy rối.<br> ",
 1091:"Và ai hiểu bọn quấy rối nhất? Chính bọn quấy rối.<br>Nói cách khác…<br> ",
 1093:"Carla‚ em sẽ tạo ra một đội ngũ bất khả chiến bại<br>từ những gã quấy rối mạnh nhất!<br> ",
 1104:"Do chính tay em… tạo ra ư?!<br> ",
 1160:"Chết tiệt‚ chẳng tìm được thân hình nào đáng xem.<br>Cái thị trấn này chán thật…<br> ",
 1216:"………<br> ",
 1228:"Hả? Ơ‚ ơ! 95‚ không‚ hơn 100! Sức chiến đấu gì đấy!<br> ",
 1239:"Hàng tuyệt vời quá! Này‚ chị ơi! Cho tôi nhìn kỹ hơn chút đi!<br> ",
 1250:"Á‚ tha cho em đi mà—<br> ",
 1276:"Hê hê hê‚ cô càng chống cự‚ bọn quấy rối càng hưng phấn lên.<br> ",
 1314:"Cho tôi nhìn rõ bộ ngực đó!<br> ",
 1352:"Được rồi‚ bắt quả tang quấy rối! Tôi bắt giữ ông!<br> ",
 1417:"*Bốp!*<br> ",
 1428:"Ự…<br> ",
 1463:"*Thở phào*. Đây đúng là gã quấy rối em cần tìm.<br>Mới bắt được một tên…<br> ",
 1472:"Nhưng vẫn chưa đủ. Em cần thu thập thêm nhiều nữa…<br> ",
 1540:"Chỗ quái quỷ gì thế này! Cho tôi về bồn tắm chung đi!<br> ",
 1551:"Chết tiệt‚ tôi muốn ngửi tí tóc.<br> ",
 1609:"Chào mừng mọi người đến với Trường Huấn Luyện<br>Tiêu Diệt Quấy Rối Tình Dục.<br> ",
 1661:"Cái quái gì vậy! Tôi chỉ ngửi thôi‚ đâu có làm gì sai!<br> ",
 1707:"Mọi người nghe đây. Theo mệnh lệnh của Chỉ Huy‚ các người—<br> ",
 1759:"Tôi chỉ nhìn phụ nữ thôi mà! Đây là chuyên chế!<br> ",
 1805:"N‐nhưng‚ đó là mệnh lệnh!<br> ",
 1857:"Ít nhất cũng mặc cái váy đi chứ! Trả lại ô cho tôi!<br> ",
 1913:"(Ự… bọn họ chẳng chịu nghe gì em nói cả.<br>Đúng như dự đoán‚ lý lẽ chẳng tác dụng với bọn biến thái.)<br> ",
 1924:"(Đây là nhiệm vụ đầu tiên Chỉ Huy giao cho em…<br>Dù thế nào em cũng phải hoàn thành nó.)<br> ",
 1935:"(Nhưng em chỉ làm được những gì đã được dạy.<br>Chỉ những gì em từng học thôi…)<br> ",
 1944:"(Em chưa bao giờ chỉ dạy bọn biến thái. Em phải làm sao đây…?)<br> ",
 1972:"(…Không‚ đúng rồi. Cố làm một việc em chưa biết cách làm<br>đột ngột cũng vô ích.)<br> ",
 1984:"(Những gì em đã học được! Cách sống của một người lính! Em sẽ cho họ thấy!)<br> ",
 2015:"—Im cái mồm đi! Ai cho phép các người mở miệng?<br> ",
 2024:"Các người tưởng mình là con người sao?! Lũ rác rưởi!<br> ",
 2078:"C‐cái gì… rác rưởi…?!<br> ",
 2124:"Đuổi theo mông phụ nữ và bốc mùi thối rữa!<br>Các người là cặn bã‚ rác rưởi‚ thứ rác còn hơn cả rác! Đó chính là các người!<br> ",
 2133:"Các người nghĩ tôi sai sao?! Nói đi‚ Joe!<br> ",
 2185:"C‐chúng tôi không phải rác—<br> ",
 2227:"Đừng để rác rưởi phát tán mùi hôi!<br>Chỉ có hai từ các người được phép ép nói!<br> ",
 2230:"Vâng! Và! Thưa bà! Nói đi‚ lũ rác rưởi!<br> ",
 2284:"V‐vâng‚ thưa bà…<br> ",
 2331:"Đúng vậy! Nghe đây! Dưới quyền của Ngài Chỉ Huy‚<br>tôi sẽ huấn luyện lại các người!<br> ",
 2338:"Mọi người trong căn cứ này đều đang dõi theo các người! Đừng tưởng có thể trốn thoát!<br> ",
 2392:"K‐không đời nào…<br> ",
 2439:"Cho đến khi các người tốt nghiệp khỏi rác rưởi‚ các người chẳng phải con người!<br>Hãy khắc điều đó vào lồng ngực vô dụng của các người!<br> ",
 2491:"Sao lại thành ra thế này…?<br> ",
 2539:"Ghee‚ anh vừa nói gì? Nói lại trước mặt tôi đi!<br> ",
 2593:"V‐vâng‚ thưa bà!<br> ",
 2640:"Tốt hơn rồi! Vì cái tội cãi lời đó‚ mười vòng sân huấn luyện!<br>Joe‚ Gordon‚ Kaiman‚ các anh cùng liên đới trách nhiệm! Chạy đi!<br> ",
 2664:"Áiiii!<br> ",
 2703:"(Họ nghe lời em… em thực sự đang chỉ dạy đàng hoàng!)<br> ",
 2714:"(Gửi những thành viên Đội Cảnh Vệ Cộng Hòa Eldorana đã dẫn dắt em…<br>Carla… Carla sẽ dốc hết sức…!)<br> ",
 2742:"Cái kiểu chạy hời hợt gì vậy? Chạy như thể đang đuổi theo cái mông phụ nữ đi!<br>Chạy đii!<br> ",
 2771:"Đừng ngừng tay chèo! Tiếp tục bơi!<br>Các người định bỏ cuộc nếu bọn quấy rối trốn ra biển sao?<br> ",
 2773:"K‐không đời nào! Làm sao tôi bơi được khi mặc giáp thế này chứ!<br> ",
 2785:"Sao vậy‚ Kaiman! Thời gian ngâm mình trong bồn tắm chung đó thành công cốc sao?<br>Ở dưới nước anh cũng vô dụng luôn à?<br> ",
 2787:"C‐chuyện đó không đúng! Việc… việc tắm chung của tôi không phải vô ích!<br> ",
 2798:"Chứng minh bằng cách bơi đi! Giờ trả lời tôi‚ lũ khốn!<br>Chúng ta xử lý bọn quấy rối ra sao?<br> ",
 2800:"Nghiền nát chúng!<br> ",
 2838:"Lũ rác rưởi‚ các người đã chịu đựng khá tốt cho đến giờ. Huấn luyện kết thúc tại đây.<br> ",
 2845:"Từ giây phút này‚ các người tốt nghiệp khỏi rác rưởi!<br>Các người là những thành viên kiêu hãnh của Đội Liệt Sĩ Tiêu Diệt Quấy Rối Tình Dục Tiền Tuyến Căn Cứ!<br> ",
 2847:"Vâng‚ thưa bà!<br> ",
 2859:"…Mọi người‚ các người đã theo kịp em rất tốt.<br>Từ giờ‚ chúng ta là đồng đội cùng chiến đấu bên nhau.<br> ",
 2919:"Đ‐Đội trưởng…!<br> ",
 2928:"Bọn tôi là đồng đội của ngài‚ Đội trưởng…!<br> ",
 2943:"Đội trưởng Carla!<br> ",
 2952:"Ô ô ô! Đội trưởng Carla! Đội trưởng Carla!<br> ",
 3000:"Cùng nhau tiêu diệt bọn quấy rối đó nào!<br> ",
 3049:"R‐ra là chuyện như vậy…<br> ",
 3051:"Tiền Tuyến Căn Cứ này có lẽ là nơi bố trí tốt nhất cho cô ấy.<br>Còn hơn cả Đội Cảnh Vệ Eldorana nữa.<br> ",
 3062:"Chỉ Huy nghĩ vậy sao…?<br> ",
 3064:"Quan trọng nhất là cô ấy trông có vẻ hạnh phúc.<br> ",
 3114:"(Cảm ơn Chỉ Huy.<br>Em sẽ chiến đấu vì căn cứ này và vì ngài!)<br> ",
 3140:"Giờ thì‚ mọi người!<br>Quấy rối tình dục!<br> ",
 3142:"Tiêu diệt!<br> ",
 3153:"Đúng vậy! Cùng nhau nỗ lực nhé!<br> ",
}

def build():
    raw = open(ASSET,'rb').read()
    has_crlf = b'\r\n' in raw
    text = raw.decode('utf-8-sig')
    lines = text.split('\r\n')
    out = []
    for idx, ln in enumerate(lines, 1):
        if idx in VI:
            assert ln.startswith('title,') or ln.startswith('message,') or ln.startswith('messageTextUnder,') or ln.startswith('messageTextCenter,')
            if ln.startswith('title,'):
                new = 'title,' + VI[idx]
            else:
                parts = ln.split(',')  # no comma inside text field -> safe
                parts[2] = VI[idx]
                new = ','.join(parts)
            out.append(new)
        else:
            out.append(ln)
    body = '\r\n'.join(out) if has_crlf else '\n'.join(out)
    data = b'\xef\xbb\xbf' + body.encode('utf-8')
    open(OUT,'wb').write(data)
    print("WROTE", OUT, "lines:", len(out))

if __name__ == '__main__':
    build()

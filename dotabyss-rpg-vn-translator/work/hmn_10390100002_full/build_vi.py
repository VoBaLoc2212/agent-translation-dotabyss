import re, pathlib

EN = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10390100002.txt"
VI_PATH = pathlib.Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10390100002.txt")

# line_no -> VI text field (internal <br> only; suffix "<br> " mirrored automatically for message,)
VI = {
    34: "Ta Chỉ Truyền Giảng Lời Dạy Của Thần Thôi",
    42: "<size=48>—Vài Ngày Sau.</size>",
    82: "Chỉ Huy‚ ngài có việc ở nhà thờ sao?",
    84: "Ta chỉ hơi bận tâm không biết Margaret thế nào thôi.",
    95: "À‚ ra vậy. Cô ấy nói muốn truyền bá lời dạy của Thần‚ nhưng<br>không biết có suôn sẻ không nhỉ...?",
    97: "Mà này‚ đám đông kia là sao vậy?",
    133: "Một đám đông lớn đang tụ tập bên dưới bàn thờ nhà thờ. Ở<br>chính giữa là Margaret đang đứng.",
    180: "Ha ha ha! Cô Margaret! Trước giờ tôi luôn tự ti về cái khe hở<br>giữa hai răng cửa‚ nhưng giờ chẳng còn bận tâm chút nào nữa!",
    191: "Fufu‚ vậy thì tốt quá rồi. Mong ngài luôn giữ được tâm hồn an yên.",
    233: "Cả nhà tôi cũng vậy! Thằng con tôi lúc nào cũng để cửa mở toang‚<br>giờ tôi chẳng còn thèm để ý nữa luôn!",
    242: "Vợ tôi không còn để ý mấy chuyện vặt vãnh nữa‚ nên tôi hạnh phúc lắm!<br>Cô Margaret tuyệt vời nhất!",
    288: "Tôi nào có làm gì đâu.<br>Tôi chỉ trò chuyện để giúp họ nhẹ lòng đi một chút thôi.",
    299: "Tôi chỉ khơi gợi một chút thôi——<br>Người thắp sáng tâm hồn của mọi người chính là bản thân họ. Fufu.",
    366: "Thưa Đức Margaret. Chúng tôi sắp xuất kích‚<br>ngài có thể cầu nguyện cho chúng tôi được bình an không?",
    383: "Tôi cũng xin ngài cầu nguyện! Chúng tôi dự định khi trở về sẽ tổ chức lễ cưới——",
    452: "Tôi hiểu rồi. Tôi sẽ hết lòng cầu nguyện.<br>Mong hồng ân của Thần sẽ luôn ở bên các vị——",
    521: "Haizz——Thưa ngài Chỉ Huy‚ cô Alicia.<br>Thật lòng xin lỗi vì đã để hai vị phải chờ.",
    523: "Không sao. Bên chỗ cô có vẻ tiến triển rất tốt nhỉ.",
    542: "Nhờ ơn ngài.<br>Tôi rất vui khi thấy nét mặt mọi người thay đổi từng ngày.",
    553: "Cả những người thân thiết với ngài Chỉ Huy và cô Alicia<br>cũng đã ghé thăm nhà thờ.",
    564: "Mọi người dường như đều tự chiêm nghiệm về hành vi của mình‚<br>và đã có dấu hiệu cải thiện‚ điều đó khiến tôi thật sự vui mừng.",
    566: "Ồ? ...Mà tiện thể‚ là những ai vậy?",
    612: "Có mấy người cơ——Cô Sophia nói muốn sửa cái tính quá nghiêm túc<br>của mình‚ nên tôi khuyên cô ấy thả lỏng một chút.",
    627: "(...Nghĩ lại thì‚ hôm nọ lúc chạm mặt nhau‚<br>ta ngáp một cái thật to mà cô ấy chẳng nói gì. Ta còn thấy lạ.)",
    651: "Cô Verisa vì tò mò mà ghé đến‚ tôi có gợi ý ‚Hay là cô thử tôn trọng<br>mọi người hơn xem?‚ và cô ấy vui vẻ thực hành theo.",
    659: "Trước giờ cô ấy vốn đối đáp với mọi người lịch sự trên bề mặt‚<br>nhưng giờ cô ấy vui vì điều đó tự nhiên bộc lộ trong lúc trò chuyện.",
    661: "...Người đó‚ thật sự là Verisa sao?",
    716: "N-ngài Chỉ Huy. Ngài nói quá lời rồi.",
    762: "Cô Marina thì sự chấp niệm với tiền bạc có vẻ đã vơi đi đôi chút.",
    764: "Đó chẳng phải là tẩy não sao!? Cô làm bằng cách nào vậy!?",
    775: "Tôi chỉ đơn thuần truyền giảng lời dạy của Thần thôi mà.",
    786: "Cô Himari vui vì đã trở nên chủ động hơn‚ còn cô Kururu<br>vui vì đã có thể hành động điềm tĩnh hơn. Ufufu.",
    833: "...Alicia. Ngay lúc này‚ trong tất cả mọi người‚ ta sợ Margaret nhất.",
    844: "Ơ-ơ thì... nhưng nếu ai cũng vui thì có sao đâu?<br>Với lại cô ấy đâu có ép buộc gì...",
    856: "Mọi người tự nguyện đến tâm sự nỗi phiền muộn của mình. Họ tự suy<br>ngẫm rồi mới đem lời khuyên của cô ấy ra thực hành‚ đúng không ạ?",
    868: "Vâng. Tôi không hề áp đặt lên họ. Vì điều đó đi ngược lại lời dạy của Thần.",
    915: "Tôi cũng không phủ nhận ‚điểm khiến mỗi người bận tâm‚ về bản thân.<br>Đó cũng là tài sản mà Thần đã ban cho người ấy.",
    926: "Việc có thay đổi hay không không quan trọng. Điều quan trọng là nhìn lại<br>chính mình và không ngừng cố gắng——đó mới là sự cao quý mà Thần mong mỏi ở con người.",
    980: "Ra vậy...! Quả nhiên lời của cô Margaret thật tuyệt vời!<br>Nghe cô nói‚ tôi học được nhiều điều lắm!",
    982: "À~... xin lỗi vì phá hỏng bầu không khí‚ nhưng ta phải đi rồi.<br>Ta vẫn còn công việc chưa xong.",
    993: "Mai này‚ xin ngài cũng hãy kể câu chuyện của mình cho tôi nghe nhé‚ ngài Chỉ Huy.<br>Tôi luôn ở đây chờ ngài.",
    1040: "Haizz... Câu chuyện của cô Margaret thật sự tuyệt vời.<br>Cứ như tâm hồn được gột rửa vậy! Tôi cũng muốn trở thành người như thế.",
    1042: "...Vậy à. Đó là cảm giác mà ta không tài nào hiểu nổi.",
    1053: "Ngài không hợp với kiểu người đó sao‚ Chỉ Huy?",
    1064: "Cũng không phải là tôi không hiểu đâu.<br>Vì cô Margaret là kiểu người trái ngược hoàn toàn với ngài mà~.",
    1066: "Ta không có ý phủ nhận con người của Margaret‚<br>và cũng công nhận giá trị của cô ấy‚ nhưng chỉ vậy thôi thì không sống nổi trên đời.",
    1068: "Chính vì cô ấy là người tốt như thế nên chẳng mấy chốc rắc rối sẽ tìm đến.<br>Chỉ mong đừng có chuyện gì lớn xảy ra...",
    1104: "<size=48>—Ngày Hôm Sau—</size>",
    1157: "Chỉ Huy! Nguy rồi!<br>Cô Margaret đã bị một băng đạo tặc bắt cóc!",
    1170: "Nghe nói lúc cô ấy đang ở nhà thờ sinh hoạt như thường lệ với mọi người‚<br>thì có một gã đàn ông khả nghi ập đến cầu xin được cứu rỗi——",
    1181: "Cô Margaret theo lời hắn đến sào huyệt để giảng đạo‚ nhưng sau đó‚<br>một lá thư đòi tiền chuộc đã được gửi đến cho ngài‚ Chỉ Huy.",
    1183: "...Một khoản kha khá đấy. Hơn nữa‚ địa điểm giao dịch lại ở bên trong Đại Huyệt.<br>Mà lại còn bắt ta phải đến một mình——sao?",
    1185: "Đành vậy. Ta đi ngay đây.",
    1204: "Sao cơ!?<br>Tôi lo cho cô Margaret lắm‚ nhưng như vậy thì quá nguy hiểm!?",
    1206: "Không sao đâu. Với trường hợp của Margaret thì‚ có lẽ——",
    1217: "...?",
    1241: "Nào‚ ta đã đến chỗ hẹn rồi.<br>Margaret và bọn đạo tặc thì——ở đằng kia à.",
    1260: "Hức‚ hức hức... hu hu hu hu u u u u~nnnn!",
    1277: "(...N-nó đang khóc à?)",
    1294: "Ơ-ơ-ơ-ơi! Sao thế này! Tại sao khi nghe câu chuyện của cô‚<br>nước mắt ta cứ tuôn không ngừng thế nàyyy aaa a a~!!!",
    1335: "Không phải tôi khiến các vị như vậy đâu. Người đang rơi lệ chính là trái tim của các vị đấy.",
    1347: "Trộm cắp là tội lỗi. Điều đó không sai‚<br>nhưng cũng không phải hành vi không thể cứu vãn——",
    1358: "Chỉ cần ăn năn tội lỗi và tích thiện từ nay về sau——nếu làm được vậy‚<br>thì việc ác cũng biến thành quá khứ ‚cần thiết để dẫn tới điều thiện‚.",
    1369: "Chính trái tim khao khát con đường ấy của các vị đang tuôn rơi những giọt lệ.<br>Từ bây giờ‚ các vị có thể thay đổi không?",
    1394: "Đúng vậy nhỉ... đúng thật... Hức<br>Cứ thế này thì ta chẳng còn mặt mũi nào nhìn mẹ ở quê nữaaa!",
    1396: "Xin lỗi vì đã cắt ngang. Ta mang tiền đến rồi‚ các ngươi nhận chứ?",
    1398: "A! Là Chỉ Huy của Căn Cứ Tiền Tuyến kìa!?",
    1400: "...Ngài mất công đến tận đây‚<br>nhưng bọn ta không thèm loại tiền kiếm được bằng việc xấu xa nữa đâu!",
    1402: "Đúng vậy! Vốn dĩ nhận tiền xong‚ bọn ta định giết cả Margaret để bôi<br>nhọ danh tiếng Chỉ Huy‚ nhưng giờ bọn ta không làm thế nữa đâu!",
    1404: "Đúng đúng! Từ nay bọn ta sẽ sống một cuộc đời<br>lương thiện!",
    1406: "...Không biết có làm được không nhỉ?",
    1408: "Không‚ làm được! Chỉ cần kiên trì tới khi làm được là xong! Làm thôiii ooo o o—!",
    1423: "(Chỉ trò chuyện thôi mà‚ chẳng những tự cứu mình mà còn cảm hóa được cả bọn đạo tặc——?<br>Chuyện đó có thể xảy ra thật sao!?)",
    1465: "Thưa ngài Chỉ Huy. Xin lỗi vì đã khiến ngài lo lắng.<br>Tôi vô cùng biết ơn vì ngài đã đến cứu tôi.",
    1467: "À‚ ừ——thật lòng mà nói‚ ta không lo lắng lắm đâu.<br>Ta còn linh cảm chuyện thế này sẽ xảy ra‚ nên mới đến một mình đấy.",
    1469: "Nhưng vượt xa tưởng tượng của ta...<br>...Có khi ta chẳng cần đến cũng được nhỉ?",
    1480: "Không hề đâu ạ. Bản thân tôi cũng có nỗi sợ.<br>Chính vì tin ngài Chỉ Huy sẽ đến nên tôi mới bình tĩnh truyền giảng lời dạy của Thần được.",
    1491: "Thoạt nhìn‚ điều đó có vẻ đi ngược lời dạy của Thần‚<br>nhưng ngài Chỉ Huy đúng là bậc nam nhi mà tôi đã tin tưởng.",
    1502: "Cảm ơn ngài. Thưa ngài Chỉ Huy.",
}

raw = open(EN, "rb").read()
has_crlf = b"\r\n" in raw
text = raw.decode("utf-8-sig")
lines = text.split("\r\n") if has_crlf else text.split("\n")

CMD = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def mirror_suffix(src, vi):
    # message, fields end with "<br> " suffix; mirror trailing tag(s)+space
    m = re.search(r"((?:<[^>]+>\s*)+)$", src)
    suf = m.group(1) if m else ""
    return vi + suf

out = []
errors = []
for i, ln in enumerate(lines):
    no = i + 1
    if no in VI:
        cmd = ln.split(",", 1)[0]
        if cmd == "message":
            parts = ln.split(",", 5)
            src = parts[2]
            vi = mirror_suffix(src, VI[no])
            # br count check
            if src.count("<br>") != vi.count("<br>"):
                errors.append(f"BR L{no}: EN={src.count('<br>')} VI={vi.count('<br>')}")
            if "," in VI[no]:
                errors.append(f"COMMA L{no}")
            parts[2] = vi
            out.append(",".join(parts))
        elif cmd in ("title", "messageTextCenter", "messageTextUnder"):
            if cmd == "title":
                parts = ln.split(",", 1)
                parts[1] = VI[no]
                out.append(",".join(parts))
            else:
                parts = ln.split(",", 5)
                if VI[no].count("<br>") != parts[2].count("<br>"):
                    errors.append(f"BR L{no}: EN={parts[2].count('<br>')} VI={VI[no].count('<br>')}")
                parts[2] = VI[no]
                out.append(",".join(parts))
    else:
        out.append(ln)

if errors:
    print("ERRORS:")
    for e in errors: print(" ", e)
    raise SystemExit(1)

new = ("\r\n" if has_crlf else "\n").join(out)
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
VI_PATH.write_bytes(b"\xef\xbb\xbf" + new.encode("utf-8"))
print("WROTE", VI_PATH, "lines", len(out), "records", len(VI))

# -*- coding: utf-8 -*-
import json, re, io, os, sys

W = os.path.dirname(os.path.abspath(__file__))
EN = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100003.txt"
VI = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100003.txt"

recs = json.load(open(W+"/recs.json", encoding="utf-8"))
# VI_DICT keyed by seq -> vietnamese text field (with tags/commas as needed)
VI_DICT = {}
# === CHUNK1 ===
VI_DICT[0]  = "Tiến Lên Đây‚ Hơi Kẻ Hùng Của Ta — Nữ Vương Bóng Tối!"
VI_DICT[1]  = "Khi đoàn quân của Chỉ Huy quay lại‚ đơn vị đã giao chiến với bầy quái vật đủ mọi kích cơ.<br> "
VI_DICT[2]  = "Xin lỗi vì đến muộn! Tình hình thế nào rồi?<br> "
VI_DICT[3]  = "Đơn vị tiền tuyến đã lập tường chắn ngăn đòn đánh úp‚ nhưng đang bị áp đảo về số lượng! Chúng ta cần chỉnh đốn đội hình và yểm trợ tiền tuyến ngay...<br> "
VI_DICT[4]  = "Đ-đơn vị vừa chặn đòn đánh úp‚ là đơn vị em được biên chế đúng không!? Em sẽ hợp quân ngay!<br> "
VI_DICT[5]  = "Hayley‚ cậu càng câu giờ được bao nhiêu thì tình hình càng dễ thở! Tôi trông cậy vào cậu!<br> "
VI_DICT[6]  = "V-vâng!<br> "
VI_DICT[7]  = "Gào o o o!<br> "
VI_DICT[8]  = "Úi chà‚ chết tiệt‚ chết tiệt!<br> "
VI_DICT[9]  = "T-ta ya a a!<br> "
VI_DICT[10] = "Giắt!<br> "
VI_DICT[11] = "Nhát chém của Hayley khiến con quái vật to gấp bội cô ta phải lùi bước. Từ những binh sĩ bị đẩy lùi vang lên tiếng reo hò \"Ô ô!\"<br> "
VI_DICT[12] = "Hayley‚ cứu tinh quá! Đánh bay lũ này đi! Bọn tôi sẽ theo sau!<br> "
VI_DICT[13] = "V-vâng... Mọi người‚ nhờ các bạn giúp đơ!<br> "
VI_DICT[14] = "Ô-ô...? Giữa chiến trường cậu vẫn ăn nói kiểu đó à...? Thôi‚ thắng là được! Xông lên đi!<br> "
VI_DICT[15] = "Dù không cam lòng nhưng bọn này trông cậy vào cô đấy!<br> "
VI_DICT[16] = "(Mọi người kỳ vọng vào em nhiều thế... Phải để em dẫn dắt thôi! Là nữ vương tương lai — là anh hùng!)<br> "
VI_DICT[17] = "Ê-êi ya a a!<br> "
VI_DICT[18] = "Hét lên một tiếng‚ Hayley xông tới. Như hôm qua‚ nàng vung thanh kiếm cao bằng cả người mình và nhảy vượt qua đầu lũ quái vật.<br> "
VI_DICT[19] = "Nhưng độ cao chưa đủ. Nàng không thể cắm kiếm vào con quái khổng lồ‚ chỉ kịp cản đà tiến của chúng.<br> "
VI_DICT[20] = "S-sao lại...!<br> "
VI_DICT[21] = "Go a a a!<br> "
VI_DICT[22] = "Gừ...<br> "
VI_DICT[23] = "Cuối cùng đà xông tới của Hayley cũng bị chặn đứng. Nàng bị buộc vào thế giao chiến tại chỗ với lũ quái vật.<br> "
VI_DICT[24] = "Hayley bị chặn lại rồi!?<br> "
VI_DICT[25] = "Thế có nghĩa là lũ này mạnh hơn bọn hôm qua!?<br> "
VI_DICT[26] = "(Không đúng... Hayley không còn sức bùng nổ như hôm qua. Cả đơn vị bị dây dưa bởi phong độ tệ của ả khiến tinh thần chẳng lên nổi)<br> "
VI_DICT[27] = "(Nếu khơi được sức mạnh thật sự của nàng‚ kết quả sẽ giống hôm qua — đưa Hayley trở lại phong độ là nhiệm vụ của ta!)<br> "
VI_DICT[28] = "Ta đi tới chỗ Hayley ở tiền tuyến! Mọi người hãy bảo vệ ta! Theo ta!<br> "
VI_DICT[29] = "Tuân lệnh!<br> "
VI_DICT[30] = "Gư...<br> "
VI_DICT[31] = "Bịch.<br> "
VI_DICT[32] = "*thở dốc‚ thở dốc*... Cuối cùng cũng hạ được một con... Nhưng với đà này thì em vô dụng quá...<br> "
VI_DICT[33] = "(Người bảo em hãy trông cậy vào Chỉ Huy‚ sao lại...?)<br> "
VI_DICT[34] = "Hayley! Lùi lại đi! Sang chỗ ta!<br> "
VI_DICT[35] = "Hể...? Chỉ Huy?<br> "
VI_DICT[36] = "Đó là mệnh lệnh của Chỉ Huy! Xông lên đi‚ Hayley!<br> "
VI_DICT[37] = "E-em xin lỗi...! Xin đừng‚ đừng cố quá sức...!<br> "
VI_DICT[38] = "Chỉ Huy! S-sao ngài lại ở đây!? Nguy hiểm lắm!<br> "
# === ENDCHUNK ===

# === CHUNK2 ===
VI_DICT[39] = "Chuyện đó ta biết rồi! Cứ nghe ta nói! Ta liều mạng tới tận đây rồi! Phải nghe lời ta!<br> "
VI_DICT[40] = "D-dĩ nhiên... Có mệnh lệnh gì cho em không!?<br> "
VI_DICT[41] = "À... Trở lại cách cậu hành xử hôm qua đi!<br> "
VI_DICT[42] = "Hể...?<br> "
VI_DICT[43] = "Bảo cậu trở lại Hayley — người khoác lên mình sức mạnh của... Bóng Tối cơ mà!<br> "
VI_DICT[44] = "...Ơ‚ Chỉ Huy... đó chỉ là ảo tưởng của em thôi... nó‚ nó chẳng có tác dụng gì đâu...<br> "
VI_DICT[45] = "Không đời nào. Dù là ảo tưởng‚ nó vẫn có ý nghĩa.<br> "
VI_DICT[46] = "Cậu biết tự ám thị không? Bằng cách hóa thân thành người anh hùng mình từng ngương mộ‚ cậu đã tự nhủ \"ta là kẻ mạnh\" để khích lệ bản thân.<br> "
VI_DICT[47] = "Anh hùng mang sức mạnh bóng tối nhưng trái tim là ánh sáng. Bằng cách nhập vai trọn vẹn hình tượng lý tưởng trong tiểu thuyết và anh hùng ca‚ cậu đã đạt được sức mạnh!<br> "
VI_DICT[48] = "...C-có chuyện đó thật sao?<br> "
VI_DICT[49] = "Nghi ngờ thì thử xem. Cảnh cậu hô \"Hãy bị bóng tối nuốt chửng đi!\" chắc chắn sẽ hồi sinh đơn vị — tất cả chúng ta.<br> "
VI_DICT[50] = "N-nhưng‚ nếu em cứ tiếp tục thế này thì sẽ bị đày về nước...<br> "
VI_DICT[51] = "Cứ phớt lờ đi. Kẻ quyền thế nhất ở Căn Cứ Tiền Tuyến chính là ta đây. Dù là song thân‚ thị tùy cũ hay tể tướng‚ ta chẳng để ai kêu ca.<br> "
VI_DICT[52] = "...Mà xưa nay cậu bảo sẽ nghe lời ta cơ mà? Dù ta có thể là người từ kiếp trước — bạn hay kẻ thù của cậu?<br> "
VI_DICT[53] = "...! Chỉ Huy‚ ngài nói thật đấy...?<br> "
VI_DICT[54] = "Xin lỗi ngài‚ Chỉ Huy. Em tin ngài.<br> "
VI_DICT[55] = "Sau một hơi thở sâu‚ khí chất Hayley thay đổi hẳn. Đôi mắt từng ngập ngừng trở nên sắc bén khi ghim nhìn bầy quái vật.<br> "
VI_DICT[56] = "Rồi‚ nàng nở nụ cười tà ác trên môi.<br> "
VI_DICT[57] = "Cu fu fu fu... Fu ha ha!<br> "
VI_DICT[58] = "Bất Tử Điểu Bóng Tối‚ trỗi dậy tại đây! Đập tan ấn niêm do kẻ thao túng phía sau giăng ra‚ ta — hiển linh!<br> "
VI_DICT[59] = "Mật danh là Hayley! Dù là người chiến thắng vinh quang‚ nàng còn cầm quyền lực bóng tối!<br> "
VI_DICT[60] = "Thần hay ác ma đang ngự trong thân này? — Bất kể‚ ta đốt cháy mạng sống này cho một sứ mệnh duy nhất!<br> "
VI_DICT[61] = "Nghĩa là‚ để mang chiến thắng đã hứa đến cho các ngươi! Hãy chiêm ngương thú vật — Marionette — bị bóng tối nuốt chửng!<br> "
VI_DICT[62] = "Hayley giậm mạnh đất‚ vọt nhảy suýt chạm trần. Trong lúc rơi‚ nàng chĩa mũi kiếm khổng lồ vào quái vật.<br> "
VI_DICT[63] = "(Sức mạnh đang trào dâng — với này thì được!)<br> "
VI_DICT[64] = "Ha a a a a!<br> "
VI_DICT[65] = "Giá a a!<br> "
VI_DICT[66] = "Lươi kiếm nàng đâm xuyên đầu quái vật. Hayley lập tức nhảy tiếp. Không chỉ một lần mà nhiều lần. Tiếng reo hò như gầm lên \"Uô ô!\" vang dậy.<br> "
VI_DICT[67] = "Nhìn đi! Thằng Hayley làm được thật rồi!<br> "
VI_DICT[68] = "Tiến lên‚ hơi những chiến binh được Valhalla chọn! Hãy theo ta — nữ vương bóng tối!<br> "
VI_DICT[69] = "Uô ra a!<br> "
VI_DICT[70] = "Chà... Cả sự điên cuồng lẫn sức mạnh đều vô đối.<br> "
VI_DICT[71] = "Nhờ nỗ lực của Hayley‚ tiền tuyến được giữ vững và đội hình được chỉnh đốn. Chỉ Huy cùng đơn vị đã đẩy lùi bầy quái vật.<br> "
VI_DICT[72] = "<size=48>——Sau Khi Quay Về.</size>"
VI_DICT[73] = "Lúc bị đánh úp ta tưởng toang rồi‚ nhưng chẳng ai trọng thương. Nối tiếp hôm qua‚ cuộc thám hiểm thành công.<br> "
VI_DICT[74] = "Hayley‚ anh hùng đấy! Cậu là ân nhân mạng sống của bọn này!<br> "
VI_DICT[75] = "Ta hiểu lòng ngương mộ của cậu‚ nhưng đừng lại gần quá. Bóng tối rò rỉ sẽ lây nhiễm đấy.<br> "
VI_DICT[76] = "Ha ha ha. Thế nhưng sức mạnh đó khủng khiếp thật... Liệu có liên quan tới sức mạnh bóng tối không?<br> "
VI_DICT[77] = "Đúng vậy. Theo phân tích của Chỉ Huy ta thì nguồn sức mạnh dường như vẫn bắt rễ từ bóng tối — hay nói cách khác‚ hỗn mang.<br> "
VI_DICT[78] = "Nhưng nếu đào sâu quá — kh... mắt ta lại nhói lên. Đi xa hơn nữa thì nguy hiểm...!<br> "
VI_DICT[79] = "Nhưng tin rằng kẻ kháng cự sự điên cuồng này là một tồn tại hùng mạnh — đó là lựa chọn duy nhất để dẫn dắt chiến binh tới Valhalla!<br> "
VI_DICT[80] = "Nói chung là cô bảo phải ra chiến trường với niềm tin \"ta mạnh‚ ta đặc biệt!\"<br> "
# === ENDCHUNK ===

# === CHUNK3 ===
VI_DICT[81] = "...Đúng là Chỉ Huy của ta. Ma thuật dịch thuật quá vạn năng‚ dù kẻ thao túng phía sau đã đóng băng bằng công nghệ tương lai — quả là sự dẫn dắt.<br> "
VI_DICT[82] = "Thế ra bài diễn thuyết nghe vô nghĩa của Hayley cũng có ý nghĩa — lúc đó cậu tràn đầy sức sống thật.<br> "
VI_DICT[83] = "Cả lính thường cũng thấu được chân ý của cấm thuật ta sao? Ấn niêm của thế giới đang yếu đi? Cánh cửa đang mở ra...?<br> "
VI_DICT[84] = "Nếu bắt chước cách nói là mạnh lên thì tôi cũng... không‚ hay ta thử xem?<br> "
VI_DICT[85] = "Chúng ta là Chiến Binh Bóng Tối (Chiến Binh Hỗn Mang)... kiểu vậy? Khư khư khư... Dù còn ban ngày mà máu đã sôi lên rồi.<br> "
VI_DICT[86] = "Chiến binh bóng tối với bóng tối à — mấy thứ đó chẳng có trong tiểu thuyết xưa sao? Thật hoài niệm.<br> "
VI_DICT[87] = "(...Ra là thế. Hóa ra chúng ta vẫn ổn được mà nhỉ)<br> "
VI_DICT[88] = "Ô kìa. Thưa tiểu thư‚ ngài đã trở về.<br> "
VI_DICT[89] = "Wa hya...!?<br> "
VI_DICT[90] = "Hayley chốc lát bối rối‚ nhưng liếc nhìn về phía %user%. Khi %user% gật đầu‚ Hayley cũng gật đáp lại như đã quyết tâm.<br> "
VI_DICT[91] = "—Đúng thế. Cuộc thám hiểm thật sựu nghĩa. Mọi chiến binh từng sát cánh chiến trường với ta đều bình an.<br> "
VI_DICT[92] = "Bởi có ta — vị anh hùng — bên cạnh‚ kết quả này là lẽ đương nhiên.<br> "
VI_DICT[93] = "...Tiểu thư. Ý ngài là sao? Sao ngài không sửa lại lời nói và cử chỉ?<br> "
VI_DICT[94] = "Đây là khế ước ta giao kết với Chỉ Huy. Nếu phản bội‚ tim ta sẽ bị hắc nhận xuyên thủng và tử vong.<br> "
VI_DICT[95] = "Thật đáng tiếc... Nếu ngài chẳng màng vận mệnh quốc gia thì hay là hãy trở về bản quốc —<br> "
VI_DICT[96] = "Khoan đã‚ ông lão. Việc Hayley nói năng kỳ quặc là tại ông phải không?<br> "
VI_DICT[97] = "À‚ ra thế? Vậy thì chúng tôi chẳng thể làm ngơ được rồi.<br> "
VI_DICT[98] = "Con bé này phải thế mới tốt! Không thì chẳng xuất được sức! Mà Hayley mà bình thường thì bọn tôi cũng chán lắm.<br> "
VI_DICT[99] = "N-nàng...?<br> "
VI_DICT[100] = "Hơi các người...<br> "
VI_DICT[101] = "Ông lão. Nghe nói ông đã bảo Hayley \"hãy cư xử cho xứng người dẫn đầu\". Rằng \"bằng không chẳng ai theo\".<br> "
VI_DICT[102] = "Nhưng nhờ Hayley bám lấy cái gọi là \"cử chỉ không xứng\" của ông mà mọi người đã chấp nhận nàng. ...Ông vẫn nghĩ nàng phải thay đổi sao?<br> "
VI_DICT[103] = "...Không. Đường tới thành công không chỉ có chính đạo. Hóa ra người nông nổi chính là ta.<br> "
VI_DICT[104] = "Thưa tiểu thư. Tôi chẳng nói thêm lời nào nữa. Xin ngài hãy bước trên chính đạo ngài tin tưởng!<br> "
VI_DICT[105] = "...Được thôi! Gánh cả tâm tình của ngươi‚ ta sẽ tiến bước trên Con Đường Đẫm Máu!<br> "
VI_DICT[106] = "Ho ho ho. ...Thật đáng tin cậy. Tôi mong chờ ngày được hội ngộ lần nữa.<br> "
VI_DICT[107] = "Vậy là ổn thỏa rồi? Tốt quá‚ Hayley.<br> "
VI_DICT[108] = "...Ah. Chỉ Huy của ta. Khoảnh khắc này hôm nay là mở màn chương mới trong anh hùng ca của ta.<br> "
VI_DICT[109] = "Hãy cùng ta trở thành Đấng Cứu Thế! Khư khư khư!<br> "
VI_DICT[110] = "...*thở hắt*... V-với lại‚ làm vợ chồng cũng chẳng sao đâu.<br> "
VI_DICT[111] = "Hử?<br> "
VI_DICT[112] = "...Không có gì.<br> "

assert len(VI_DICT) == len(recs), (len(VI_DICT), len(recs))

raw = open(EN, 'rb').read()
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.split('\r\n')
out = []
# rebuild text fields by seq
seq_iter = 0
for ln in lines:
    c = ln.split(',',1)[0]
    if c in ('title','message','messageTextUnder','messageTextCenter'):
        r = recs[seq_iter]; seq_iter += 1
        vi = VI_DICT[r['seq']]
        if c == 'title':
            parts = ln.split(',',1)
            out.append(parts[0] + ',' + vi)
        else:
            parts = ln.split(',')
            # parts[2] is text field; rejoin all parts preserving trailing fields
            suffix = ''
            if c == 'message':
                # mirror trailing '<br> ' suffix from source text field
                m = re.search(r'(?:<br>\s*)+$', parts[2])
                if m: suffix = m.group(0)
                vi = re.sub(r'(?:<br>\s*)+$', '', vi)
                # EN asset is authoritative for <br> count.
                en_br = r['en'].count('<br>')
                need_internal = en_br - 1  # because trailing suffix adds 1 <br>
                while vi.count('<br>') < need_internal:
                    body = vi
                    ins = None
                    ci = body.find('\u201a')
                    if ci != -1:
                        ins = ci + 1
                    else:
                        sp = body.rfind(' ', len(body)//2, len(body))
                        if sp == -1:
                            sp = body.find(' ')
                        ins = sp if sp != -1 else len(body)
                    vi = body[:ins].rstrip() + '<br> ' + body[ins:].lstrip()
                parts[2] = vi + suffix
            else:
                parts[2] = vi
            out.append(','.join(parts))
    else:
        out.append(ln)

# preflight: <br> count and ascii comma checks
seq_iter = 0
problems = []
for ln in out:
    c = ln.split(',',1)[0]
    if c in ('title','message','messageTextUnder','messageTextCenter'):
        r = recs[seq_iter]; seq_iter += 1
        if c == 'title':
            tf = ln.split(',',1)[1]
        else:
            tf = ln.split(',')[2]
        en_br = r['en'].count('<br>')
        vi_br = tf.count('<br>')
        if vi_br != en_br:
            problems.append(("BR", r['seq'], en_br, vi_br, tf))
        if ',' in tf:
            problems.append(("COMMA", r['seq'], tf))
if problems:
    for p in problems: print("PROBLEM", p)
    sys.exit(1)

result = '\r\n'.join(out) if has_crlf else '\n'.join(out)
os.makedirs(os.path.dirname(VI), exist_ok=True)
with open(VI, 'wb') as f:
    f.write(b'\xef\xbb\xbf' + result.encode('utf-8'))
print("WROTE", VI, "lines=", len(out))

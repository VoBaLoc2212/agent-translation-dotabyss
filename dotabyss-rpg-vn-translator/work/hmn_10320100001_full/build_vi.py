# -*- coding: utf-8 -*-
# EN-asset-is-English (message fields) + JP title. Field-index build.
import io, sys

EN_ASSET = r'E:\AgentTranslation\Translation\en\RedirectedResources\assets\unnamed_assetbundle\hmn_10320100001.txt'
OUT      = r'E:\AgentTranslation\Translation\vi\RedirectedResources\assets\unnamed_assetbundle\hmn_10320100001.txt'

# line_no (0-based, split by \r\n) -> VI text field (must match EN asset <br> count)
VI = {
22:  "Bí Mật Đáng Ngờ Của Thợ Mỏ",
30:  "Phù... Chuyến thám hiểm lần này cũng suôn sẻ ghê.<br> ",
53:  "Hửm?<br> ",
114: "Hì hục... hì hục...<br> ",
136: "Coong! Coong! Coong!<br> ",
151: "Sắp được rồi... hự...!<br> ",
160: "Coong!<br> ",
171: "Ối! Được rồi‚ đá quý...<br> ",
182: "Lấp lánh quá... Tìm được một viên đẹp ơi là đẹp... ê hê hê...<br> ",
184: "Này‚ Daria!<br> ",
196: "...! A‚ sếp... Anh vất vả rồi ạ.<br> ",
232: "Ừ. Em cũng vất vả rồi.<br> ",
234: "Việc khai thác thế nào rồi? Nhìn có vẻ em đã cố gắng rất nhiều đấy.<br> ",
245: "Vâng ạ‚ em đào được nhiều lắm...<br> ",
259: "Loảng xoảng!<br> ",
261: "Chà... Nhiều thật đấy. Túi của em đã đầy ắp cả rồi còn gì.<br> ",
272: "Cảm ơn sếp ạ. Em đã cố gắng hết sức.<br> ",
283: "Hình như quanh đây có mạch quặng đó sếp... Em còn đào được nhiều<br>hơn nữa cơ.<br> ",
285: "Ra vậy. Lặn xuống sâu thế này quả là đáng công.<br> ",
287: "Nói vậy chứ‚ nhiều quặng với ma thạch thật... còn có cả đá quý nữa. Trông chúng<br>ở trạng thái rất tốt.<br> ",
298: "Vâng ạ. Em đã cẩn thận đào hết chúng ra.<br> ",
310: "Đá đẹp thế này mà... Em không muốn thô bạo làm xước<br>chúng đâu ạ.<br> ",
312: "Ra vậy. Đúng như tôi nghĩ‚ tay nghề khai thác của em thật xuất sắc.<br> ",
314: "Làm tốt lắm‚ Daria! Cứ khai thác như vậy nhé.<br> ",
325: "...Vâng ạ. Em sẽ đi lấy về thật nhiều nữa.<br> ",
327: "Hmm. Nhưng có đào thêm nữa thì túi cũng chẳng chứa hết. Phải làm<br>sao đây nhỉ?<br> ",
339: "A... Nếu vậy thì không sao đâu ạ.<br> ",
341: "Sao lại thế?<br> ",
352: "Không cần cho vào túi‚ em vẫn mang được. Ví dụ như...<br> ",
372: "Như là nhét vào trong áo thế này.<br> ",
387: "Hoặc có thể kẹp vào những chỗ như thế này ạ.<br> ",
389: "Này‚ Daria! Đừng có tự nhiên thọc tay vào giữa ngực như thế. Làm<br>tôi giật cả mình.<br> ",
400: "...? Vâng‚ em xin lỗi...?<br> ",
402: "Aa... thôi‚ không sao. Em làm việc đủ nhiều rồi‚ nên thời gian còn lại<br>cứ nghỉ ngơi đi.<br> ",
413: "……!<br> ",
415: "Đến khi cuộc thám hiểm kết thúc‚ em cứ thoải mái làm gì tùy thích.<br> ",
426: "Cảm ơn sếp ạ... Vậy thì em sẽ đi đào thật nhiều.<br> ",
428: "...? Này‚ em biết là được nghỉ mà‚ đúng không?<br> ",
439: "Không đâu‚ em sẽ tiếp tục đào. Em... em thích đá quý mà.<br> ",
441: "Ờ-ờ được. Thôi‚ tùy em vậy.<br> ",
482: "Được rồi... Cũng đến lúc rồi. Đội thám hiểm‚ chúng ta rút quân!<br> ",
484: "Hửm? Daria không có ở đây...? Ê! Daria‚ em ở đâu vậy?<br> ",
486: "Không trả lời... Daria! Em ở đâu rồi!?<br> ",
495: "(Thế này... gay rồi. Chẳng lẽ Daria gặp chuyện gì đó...!)<br> ",
537: "Em đây‚ sếp.<br> ",
539: "Ối!? Gì vậy‚ em đứng sau lưng tôi à!<br> ",
550: "...Em xin lỗi... em vừa đi hái hoa về ạ.<br> ",
552: "Ờ-ờ ra vậy. Vậy thì được. Nhưng nếu có thể‚ đi đâu thì báo tôi một tiếng nhé.<br> ",
580: "...Vâng ạ. Em sẽ chú ý.<br> ",
595: "(Ừm... không biết nữa. Cô ấy chăm chỉ thật‚ nhưng lại chẳng đoán được đang nghĩ gì.)<br> ",
597: "(Lúc nào cũng ít nói‚ chẳng biết trong đầu đang nghĩ gì nữa...)<br> ",
621: "...Ừm‚ sếp ơi.<br> ",
623: "Hửm? Có chuyện gì thế?<br> ",
634: "Em rất thích công việc này... Nên xin hãy cho em tiếp tục khai thác ạ.<br> ",
636: "À‚ tất nhiên rồi. Chính tôi cũng muốn nhờ em tiếp tục. Trông cậy vào<br>em đấy.<br> ",
647: "Vâng ạ. Vì cả đội và vì sếp nữa... em sẽ cố gắng hết mình.<br> ",
662: "(...Thôi thì‚ chắc cô ấy không phải người xấu. Cứ để mắt trông chừng<br>một thời gian vậy.)<br> ",
690: "<size=48>—Vài ngày sau—</size>",
714: "Cốc‚ cốc.<br> ",
716: "Vào đi.<br> ",
757: "Tôi xin phép ạ!<br> ",
768: "Xin lỗi Chỉ Huy. Có chuyện về Daria tôi muốn báo cáo...<br> ",
770: "Hô? Có chuyện gì sao?<br> ",
783: "Thật ra gần đây trong đám binh sĩ đang lan truyền tin đồn rằng<br>Daria rất đáng ngờ.<br> ",
797: "Trong các trận chiến‚ Daria luôn đi cùng chúng tôi với vai trò thợ mỏ...<br> ",
806: "Nhưng đến khi trận chiến kết thúc‚ cô ta lại biến đi đâu mất.<br> ",
817: "Với lại‚ lúc nào cô ta cũng nói y một câu: 'Tôi đi hái hoa.' Lần nào cũng<br>như vậy‚ nên đương nhiên là rất khả nghi.<br> ",
832: "('Đi hái hoa'... Nghĩ lại thì‚ lần thám hiểm trước cô ấy cũng<br>nói vậy.)<br> ",
856: "Nên tôi đã thử điều tra một chút về Daria...<br> ",
865: "Hơn nữa‚ hình như Daria vốn từng là thành viên của một băng<br>trộm khét tiếng!<br> ",
867: "Cái gì...?<br> ",
876: "Chỉ là tin đồn thôi‚ nhưng... Biết đâu có liên quan đến hành tung sau<br>mỗi trận của cô ta!<br> ",
878: "...Ra vậy. Nói tóm lại‚ các cậu nghi Daria ăn trộm. Nhưng...<br> ",
880: "Cô ấy khai thác rất chăm chỉ‚ thành quả cũng đáng nể. Tôi cũng chưa<br>nghe nói có gì bị mất quanh chỗ Daria cả.<br> ",
891: "Hiện giờ thì đúng là vậy‚ nhưng tôi vẫn thấy Daria rất đáng ngờ.<br> ",
902: "Kỹ năng của cô ta đúng là siêu thật. Định mức làm cái là xong ngay. Nhưng<br>chẳng bao giờ chịu nói câu nào‚ cứ thấy rờn rợn thế nào ấy...<br> ",
913: "Nghĩ đến trường hợp xấu nhất‚ liệu cứ để cô ta ở lại căn<br>cứ thế này có ổn không...!<br> ",
928: "(Hừm... Xem ra họ lo lắng ra phết.)<br> ",
930: "(Tin đồn Daria từng là trộm... Bản thân tôi cũng tò mò không biết<br>thực hư ra sao.)<br> ",
932: "(Cứ để mặc thế này‚ sĩ khí của binh lính có thể sa sút mất... Vậy<br>thì...)<br> ",
947: "Được rồi. Giờ tôi sẽ đi hỏi Daria về tin đồn này.<br> ",
958: "Hả? Đích thân Chỉ Huy đi ạ...!<br> ",
960: "Ừ. Hai cậu chờ ở đây. Nghi ngờ về Daria‚ để tôi làm sáng tỏ.<br> ",
969: "V-vâng ạ!<br> ",
978: "Nhờ cả vào Chỉ Huy đấy ạ...!<br> ",
1008:"—*Cốc‚ cốc*<br> ",
1010:"Daria. Em có trong đó không?<br> ",
1012:"...Lại không trả lời. Đúng chất cô ấy.<br> ",
1015:"...Khò...<br> ",
1017:"Hửm? Giữa ban ngày ban mặt mà ngủ à...? Daria‚ dậy đi! Tôi<br>có chuyện muốn hỏi đấy!<br> ",
1019:"...Khò... khò...♪<br> ",
1021:"Nói mơ mà nghe hạnh phúc dữ ha! Thôi được‚ xin lỗi nhé‚ nhưng tôi vào<br>đây!<br> ",
1031:"—*Cạch*<br> ",
1048:"...Khò...<br> ",
1052:"Hửm?<br> ",
1079:"C-cái gì đây...! Đống quặng khổng lồ này là sao!?<br> ",
1094:"(Cả núi quặng chất đống trên giường... Mà Daria thì đang vùi mình<br>trong đó ngủ khì!?)<br> ",
1155:"Hoááp... Hửm? Ai... vậy ạ...?<br> ",
1166:"...A.<br> ",
}

raw = open(EN_ASSET,'rb').read()
assert raw[:3]==b'\xef\xbb\xbf', 'no BOM'
txt = raw.decode('utf-8-sig')
lines = txt.split('\r\n')

# preflight: <br> count check
problems=[]
for idx,vi in VI.items():
    ln=lines[idx]
    cmd=ln.split(',',1)[0]
    if cmd=='title':
        src=ln.split(',',1)[1]
    else:
        src=ln.split(',',5)[2]
    if src.count('<br>')!=vi.count('<br>'):
        problems.append((idx,src.count('<br>'),vi.count('<br>')))
    assert ',' not in vi, f'ASCII comma in VI line {idx}: {vi}'
if problems:
    for p in problems: print('BR MISMATCH',p)
    sys.exit('Fix <br> counts')

# rebuild
out=[]
for idx,ln in enumerate(lines):
    if idx in VI:
        cmd=ln.split(',',1)[0]
        if cmd=='title':
            parts=ln.split(',',1); parts[1]=VI[idx]; ln=','.join(parts)
        else:
            parts=ln.split(',',5); parts[2]=VI[idx]; ln=','.join(parts)
    out.append(ln)
body='\r\n'.join(out)
open(OUT,'wb').write(b'\xef\xbb\xbf'+body.encode('utf-8'))
print('WROTE',OUT,'lines',len(out),'translated',len(VI))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build VI asset for hmn_10410100001 (EN-asset-is-English, mixed JP-title case).
Keyed by sequential text-record index (1-based, in file order).

Conventions:
- Commander (<user>) -> Chit Huy; inner/mono "ta", address Alicia "anh"/"co",
  Ayame "nguoi"/"ta", guard "nguoi".
- Alicia (アリシア) -> Commander "anh"; Commander -> "co"/"anh".
- Ayame (アヤメ) -> Commander "Than"/"Chi Huy"/"anh Chi Huy"; Commander -> "anh"/"co".
- Warehouse guard (倉庫警備の兵士) -> Commander "ngai"/"Chi Huy".
- Fallen enemy (倒れた男) uses 貴様 -> "nguoi".
- 厄災 -> Tai Uong ; 前線基地 -> Can Cu Tien Tuyen ; 書道 -> thu phap ;
  千国連合 -> Lien Minh Ngan Quoc ; ホウライ -> Hourai ; 横領 -> bien thu ;
  暗殺 -> am sat ; 事務員 -> nhan vien van phong.
- ASCII commas inside VI text -> U+201A (‚).
- Tag/placeholder/BOM/CRLF preserved via parts[1]/parts[2] rejoin.
"""
from pathlib import Path
import sys

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10410100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10410100001.txt"

VI_DICT = {
1: "Tôi Muốn Làm Nhân Viên Văn Phòng",
2: "Ngươi đã lách qua mọi cạm bẫy và sắp sửa giết được ta rồi sao……<br>Phải thừa nhận‚ với tư cách sát thủ thì ngươi giỏi hơn ta……<br> ",
3: "Nhưng mọi nỗ lực đó cũng vô ích thôi. Ngươi không còn nơi nào để gọi là nhà nữa!<br> ",
4: "Ara‚ ra là vậy nhỉ. Cảm ơn vì lời khuyên.<br> ",
5: "Bộ dạng ung dung của ngươi cũng chỉ đến lúc này thôi. Chúng ngươi tàn đời rồi――<br> ",
6: "Một tiếng nổ lớn vang lên.<br> ",
7: "Xin lỗi vì đã ngắt lời ngươi.<br>Nếu có dịp gặp lại‚ hãy kể nốt phần sau cho ta nghe.<br> ",
8: "Giờ công việc xong rồi nhỉ. Chúng ta về văn phòng thôi anh Chỉ Huy?<br> ",
9: "Một vụ nổ kinh hoàng làm rung chuyển tòa nhà.<br> ",
10: "Fufu‚ có vẻ náo nhiệt nhỉ. ……Ồ?<br> ",
11: "Đang cháy là văn phòng phải không anh. Vậy…… chúng ta phải làm sao đây?<br> ",
12: "<size=48>Vài Ngày Sau…</size>",
13: "Ta biết mà……<br>Số lượng không lớn‚ nhưng chứng từ xuất kho và tồn kho không khớp nhau.<br> ",
14: "Ý ngài là hàng trong kho đã thất lạc‚<br>đúng như vậy ạ?<br> ",
15: "Nếu cô muốn nói giảm nói tránh thì đúng vậy.<br>Nhưng ta nghĩ có một từ khác thích hợp hơn.<br> ",
16: "Từ khác…… ngài muốn nói sao ạ?<br> ",
17: "Biển thủ‚ đó.<br> ",
18: "C-cái đó hơi quá lời rồi ạ!<br>Ngay cả Chỉ Huy mà nói thế này thì……!<br> ",
19: "Ngươi có tư cách gì để nói câu đó?<br> ",
20: "……Thưa ngài‚ xin lỗi.<br> ",
21: "……*thít*<br>Ngươi chỉ là một gã mồm mép được đàn bà che chở thôi.<br> ",
22: "Ở Căn Cứ Tiền Tuyến này‚ mọi thứ đều quý giá――<br>dù chỉ là vật tư nhỏ nhất.<br> ",
23: "V-vâng‚ thưa ngài!<br> ",
24: "Thế thì ngươi biết mình phải làm gì rồi chứ?<br> ",
25: "Dạ! Tôi sẽ lập tức sửa chữa!<br> ",
26: "Chuyện nhỏ nhặt này ngươi phải tự lo được chứ. ……Haa‚ thật chán.<br> ",
27: "Bọn như thế mà chết đi cũng thành trách nhiệm của ta sao?<br>Ta cứ nghĩ bị Tai Ương giết là tai nạn bất khả kháng cơ.<br> ",
28: "Mà thôi‚ ở Căn Cứ Tiền Tuyến thiếu nhân lực này‚<br>chẳng có nhiều kẻ chúng ta có thể để mất đâu.<br> ",
29: "Chỉ Huy~……Ừm‚ ra là anh ở đây. Em có chút việc muốn nhờ anh~……<br> ",
30: "Gì thế? Nếu là phiền phức thì ta từ chối đấy.<br> ",
31: "Không phải đâu…… có lẽ hơi phiền‚<br>nhưng em muốn anh phỏng vấn một người xin gia nhập căn cứ.<br> ",
32: "Ta đích thân làm việc đó sao? Nếu cô ấy có triển vọng thì tự mình tuyển đi.<br> ",
33: "Vì là người mà ngay cả em cũng khó đánh giá.<br>Anh có thể giao quyết định cho Chỉ Huy được không……?<br> ",
34: "……Người mà ngay cả Alicia cũng không thể phán đoán sao.<br>Nghe có vẻ thú vị đấy. Gặp cô ta một lần xem sao.<br> ",
35: "Vâng‚ nhờ anh. Ơn…… anh hãy cẩn thận nhé……<br> ",
36: "……Cẩn thận á? Cô ta là người thế nào?<br> ",
37: "Ngươi là người xin gia nhập à. Ta là Chỉ Huy của căn cứ này.<br> ",
38: "Thần là Ayame.<br>Được Chỉ Huy phỏng vấn‚ thần thật vinh dự.<br> ",
39: "Bọn ta đang thiếu người.<br>Ta sẽ xem qua hồ sơ ứng tuyển trong lúc nói chuyện‚ cô không phiền chứ?<br> ",
40: "Dạ vâng. Rất mong được chăm sóc ạ.<br> ",
41: "Cuộc phỏng vấn này khác với kiểu thông thường.<br>Trừ khi có lý do bất khả kháng‚ cô sẽ phải ở lại làm việc ở đây.<br> ",
42: "Ara‚ em vui quá.<br>Vì em đến với tâm thế một chiều‚ nên điều này giúp em lắm ạ.<br> ",
43: "Nào‚ hồ sơ ghi…… cô muốn làm nhân viên văn phòng à.<br>Cô là người có kinh nghiệm‚ đúng không?<br> ",
44: "Dạ‚ công việc trước em cũng là nhân viên văn phòng.<br>Em mong có thể phát huy năng lực ở đây ạ.<br> ",
45: "Ở nơi làm cũ‚ công việc chủ yếu của cô là gì?<br> ",
46: "Chủ yếu là dọn dẹp như đổ rác‚<br>và sắp xếp tài liệu.<br> ",
47: "Ừm‚ đúng điều bọn ta cần. Cô có thể bắt tay vào việc ngay được rồi.<br> ",
48: "(Chẳng có chỗ nào kỳ lạ cả nhỉ.<br>Alicia‚ sao cô lại giao người này cho ta?)<br> ",
49: "Tại sao cô bỏ việc cũ? Và tại sao lại đến tận<br>Căn Cứ Tiền Tuyến?<br> ",
50: "Thực ra nơi làm trước của em……<br>đã phát nổ và bốc cháy ạ.<br> ",
51: "Hờ‚ phát nổ…… bốc cháy?<br> ",
52: "Vâng‚ các thành viên cũng mất tích luôn.<br>Và em vẫn chưa được trả lương nữa ạ.<br> ",
53: "Phát nổ thì không có gì lạ…… nhưng‚ thành viên?<br> ",
54: "Xin thú thật‚ mục đích đi làm của em là tiền.<br> ",
55: "Ở đây em sẽ được trả lương đàng hoàng‚<br>và có lẽ cũng chẳng dễ mà nổ tung đâu ạ.<br> ",
56: "Ta không thể nói là sẽ chẳng bao giờ nổ hay cháy. Nhưng điểm đó thì tạm ổn.<br> ",
57: "Tiếp theo là xác nhận tư cách và kỹ năng.<br>Hồ sơ ghi ám sát và thư pháp……<br> ",
58: "...Khoan đã‚ ý câu này là sao?<br> ",
59: "Dạ‚ thần là người từ Liên Minh Ngàn Quốc‚ vùng Hourai.<br>Từ thuở nhỏ thần đã quen với thư pháp bút lông.<br> ",
60: "Thần ghi vào hồ sơ như một sở trường có ích cho nghề văn phòng.<br> ",
61: "Không phải‚ ta muốn hỏi không phải chỗ đó.<br> ",
62: "Ám sát‚ là cái gì? Nhân viên văn phòng đi đâu mất rồi?<br> ",
63: "Vâng‚ vì thần từng là nhân viên văn phòng.<br>Nên thần có thể ám sát bất cứ ai mà không vấn đề gì.<br> ",
64: "Ta chẳng hiểu cô nói gì‚ nhưng cứ sửa lại cho đúng trước đã:<br>Ám sát không nằm trong công việc của nhân viên văn phòng.<br> ",
65: "Ê…… nhân viên văn phòng ở căn cứ này không có việc ám sát sao?<br> ",
66: "Không. Làm sao có được. Mà đúng hơn‚ căn cứ nào cũng chẳng có.<br> ",
67: "Ơn…… vậy công việc 'dọn dẹp' của nhân viên văn phòng là thế nào ạ?<br> ",
68: "Là dọn dẹp nơi làm việc cho sạch sẽ‚ đơn giản vậy thôi.<br> ",
69: "Ý cô là không phải giết những kẻ vướng víu‚ phiền phức hay làm mình bực mình<br>để 'dọn dẹp' chúng sao……?<br> ",
70: "Chẳng có nghiệp vụ văn phòng nào bạo lực đến thế!<br> ",
71: "Ê……? Vậy còn việc sắp xếp tài liệu thì……<br> ",
72: "Là sắp xếp giấy tờ theo loại hoặc ngày tháng<br>để dễ xem.<br> ",
73: "Ý cô là không phải đến nhà những người thần 'dọn dẹp'‚ tìm tài liệu cần thiết<br>rồi đưa cho khách hàng sao……?<br> ",
74: "Ngươi đã từng cướp thông tin từ kẻ mình giết……<br>Đó là việc của ám sát thủ.<br> ",
75: "Khoan đã‚ chẳng lẽ em đã từng làm nghề ám sát sao?<br> ",
76: "Đúng là như vậy.<br>Hơn nữa‚ vì lý do gì mà một nhân viên văn phòng lại đi giết người?<br> ",
77: "Thần được bảo đó là dịch vụ vệ sinh xã hội‚<br>chuyên dọn dẹp rác thải không cần thiết……<br> ",
78: "Một nghề vệ sinh quá ư hung hãn……<br>Cô làm cho bọn khủng bố phản chánh phủ à?<br> ",
79: "Vì em chỉ nhìn vào lương mà nộp đơn mà không xem kỹ ngành nghề‚<br>nên em cũng chẳng rõ công việc đó là gì.<br> ",
80: "Nhưng mọi người ở đó đều rất tốt bụng.<br>Dù nghe xì xào rằng đó là công ty chuyên ám sát.<br> ",
81: "Đâu phải xì xào đâu‚ đó chỉ là sự thật!<br>Đừng tin lời kẻ ám sát!<br> ",
82: "C-cái đó là thật sao……!?<br> ",
83: "Bọn sai khiến ngươi cũng điên rồ thật‚<br>rốt cuộc là băng ám sát gì vậy?<br> ",
84: "(Hay là chúng đã đẩy Ayame vào làm quân cờ hy sinh?<br>Rồi cô ta tình cờ lại bộc lộ tài năng à?)<br> ",
85: "T-thế‚ vậy là em trượt phỏng vấn sao?<br> ",
86: "Nghe qua thì‚ cô không phù hợp làm nhân viên văn phòng……<br> ",
87: "(Nhưng mà‚ phí phạm nếu buông tay cô ta.)<br> ",
88: "(Kẻ ám sát đã đạt kết quả và sống sót.<br>Vì Alicia không ngăn cản‚ cô ta cũng chẳng phải người nguy hiểm…… có lẽ vậy.)<br> ",
89: "Ơn…… nếu được‚ anh có thể cho em thử việc một thời gian được không ạ?<br> ",
90: "Ơn……? Thử việc là thử cái gì?<br> ",
91: "Thưa Chỉ Huy‚ anh có ai muốn em 'dọn dẹp' không ạ?<br> ",
92: "Khi anh nói 'dọn dẹp'‚ ý anh là――<br> ",
93: "……Vâng. Hễ anh ra lệnh‚ em sẽ giết bất cứ ai.<br> ",
94: "Thế nào? Không có kẻ nào anh muốn cho chết sao?<br> ",
}

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

def preflight():
    raw = EN.read_bytes()
    txt = raw.decode("utf-8-sig")
    lines = txt.splitlines(keepends=True)
    seq = 0
    problems = []
    total_br = 0
    for ln in lines:
        s = ln.rstrip("\r\n")
        if not s.startswith(TEXT_CMDS):
            continue
        seq += 1
        parts = s.split(",", 5)
        cmd = parts[0]
        tf = parts[1] if cmd == "title" else parts[2]
        en_br = tf.count("<br>")
        total_br += en_br
        if seq not in VI_DICT:
            problems.append(f"seq {seq} MISSING from VI_DICT")
            continue
        vi = VI_DICT[seq]
        vi_br = vi.count("<br>")
        if vi_br != en_br:
            problems.append(f"seq {seq} BR MISMATCH en={en_br} vi={vi_br} :: {vi[:60]!r}")
        if "," in vi:
            problems.append(f"seq {seq} ASCII COMMA in VI :: {vi[:60]!r}")
    if seq != len(VI_DICT):
        problems.append(f"SEQ COUNT MISMATCH file_text_records={seq} vi_dict={len(VI_DICT)}")
    print(f"EN text records: {seq}  | total <br> in EN: {total_br}")
    print(f"VI dict entries: {len(VI_DICT)}")
    if problems:
        print("PREFLIGHT PROBLEMS:")
        for p in problems:
            print("  -", p)
        return False
    print("PREFLIGHT OK")
    return True

def build():
    raw = EN.read_bytes()
    txt = raw.decode("utf-8-sig")
    has_crlf = b"\r\n" in raw
    lines = txt.splitlines(keepends=True)
    out = []
    seq = 0
    for ln in lines:
        ending = ln[len(ln.rstrip("\r\n")):]
        s = ln.rstrip("\r\n")
        if not s.startswith(TEXT_CMDS):
            out.append(ln)
            continue
        seq += 1
        parts = s.split(",", 5)
        cmd = parts[0]
        if cmd == "title":
            parts[1] = VI_DICT[seq]
        else:
            parts[2] = VI_DICT[seq]
        new = ",".join(parts) + ending
        out.append(new)
    data = "".join(out)
    if has_crlf:
        data = data.replace("\r\n", "\n").replace("\n", "\r\n")
    blob = b"\xef\xbb\xbf" + data.encode("utf-8")
    VI.write_bytes(blob)
    print(f"WROTE {VI}  (lines kept, text records rewritten={seq})")

if __name__ == "__main__":
    ok = preflight()
    if not ok:
        sys.exit(1)
    build()

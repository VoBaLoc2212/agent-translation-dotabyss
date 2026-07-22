#!/usr/bin/env python3
"""Print ALL BR mismatches between EN asset and VI translations."""
from pathlib import Path

en_path = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt")

# Copy VI dict from build_vi.py inline
VI = {
0:"Chính Mày Là Kẻ Gây Ra Vụ Cướp",
1:"Nào nào，hôm nay có cả đống hàng tốt đây！<br>Khách ơi，nhất định hãy ghé xem nhá！",
2:"……Ừm。Chợ hôm nay cũng đông vui nhỉ。<br>Nếu sau việc này không có gì thì cũng muốn thong thả xem rồi về……",
3:"Gyaa！？",4:"Hử……？",5:"Này！ Đưa tiền đây！",
6:"Hiii，dừng lại！ Tôi đưa đây，đừng đá tôi……",
7:"Gi，giữa ban ngày ban mặt mà đi cướp à！？",8:"Hê hê，chào tạm biệt！",
9:"Khắc，đứng lại！",10:"<size=48>Nàyyyyy！</size>",11:"Guwaa！？",
12:"<user> bất ngờ bị một cô gái lạ mặt lao vào đỡ。<br>Cứ thế bị khóa tay lại。",
13:"Chính mày là kẻ trắng trợn gây ra vụ cướp giữa ban ngày ban mặt hả？<br>Dám ra tay trước mặt Celeste đây à，gan nhỉ！",
14:"……Mày là cảnh vệ hả？ Đúng lúc quá！<br>Thằng cướp vừa chạy về hướng kia——",
15:"Tưởng không bị bắt sao，đồ ngốc này。<br>Hừ，nhờ mày mà chị đây kiếm được công lao đây！",
16:"Ngon lành quá……Chắc được thưởng luôn quá？ Hí hí hí。",
17:"Này，nghe tôi nói！",
18:"À ừ ừ hiểu rồi hiểu rồi。Đến mức giữa ban ngày cũng đi cướp，<br>chắc đói bụng lắm hả？ Vô đồn rồi khai đi，ngoan ngoãn nào。",
19:"Không phải！",
20:"Im đi nào thằng cướp à không，cục tiền thưởng。<br>Để xem，1-4-0-0，bắt giữ，chốt……",
21:"Th，thôi mà nghe tôi nói đã——！！！",
22:"（Cuối cùng cũng bị lôi vô đồn cảnh vệ mất rồi……）",
23:"Nào，lấy lời khai nhé。<br>Tên và ngày sinh，viết vô đây。",
24:"Nghe cho rõ đây，tôi không phải kẻ cướp。<br>Thủ phạm là người khác. Tôi thấy hắn chạy trốn。",
25:"Lại bào chữa nhàm chán nữa rồi……chịu thua đi mà？",
26:"Vì đó là sự thật nên biết sao được。<br>Cấp trên của cô đâu？",
27:"Bảo có việc nên đi ra ngoài rồi。",
28:"Mà này，gì đây？ Nhìn chị là con gái nên coi thường hả？<br>Đồ cướp mà lại bảo đàn bà không đáng nói chuyện chắc？",
29:"Không phải vậy。Tôi chỉ muốn cô gọi ai đó biết tôi thôi。<br>Ở đây ngoài cô ra không còn ai à？",
30:"Tiếc nhỉ。Tất cả đều đi hết rồi。",
31:"……Vậy thì đành nhờ cô vậy。Gọi chủ tiệm bị hại đến đi。<br>Họ sẽ chứng minh tôi vô tội。",
32:"Đã bảo rồi，bây giờ chỉ có mình chị nên không được。<br>Không thể để mày một mình được。",
33:"Cứ trói tôi vô ghế cũng được，đi đi。<br>Còn hơn ngồi đây tra hỏi mãi，tiến triển nhanh hơn nhiều đấy？",
34:"Nói thế chứ，chị đi là mày định trốn đúng không？<br>Trốn dây trói các kiểu đấy chứ gì。",
35:"Nếu lo thì nhốt tôi vô xà lim đi！<br>Nãy giờ chẳng tiến triển gì cả！？",
36:"Đương nhiên rồi！ Chị đây không có thời gian hầu trò hề của mày đâu！<br>Cũng không định để mày chạy thoát đâu！",
37:"Vì mày là cục tiền thưởng đem tiền đến cho chị mà。<br>Nên ngoan ngoãn nhận tội đi，trước khi công lao được xác nhận thì đừng hòng thoát。",
38:"Chị rất thích tiền。Nhưng ghét phiền phức và công việc。",
39:"Còn mày là cơ hội ngàn năm có một rơi xuống chỗ chị đây……！<br>Hí hí hí hí ♪",
40:"Mau nhận tội đi。Có hận thì，<br>hận cái sự ngu ngốc của mày để bị bắt bởi một cảnh vệ hư hỏng như chị đây đi。",
41:"（Nó tự nhận mình là đồ hư đấy à……<br>Làm ơn có ai đó ra dáng đến nhanh giúp tôi với……）",
42:"——Cạch。",
43:"Nàyyy，Celeste ơi。<br>Nghe nói bắt được cướp ở chợ，thật không đấy？",
44:"A，Đội trưởng！ Đúng là tai thính quá đi ♪",
45:"Đúng vậy！ Chị đây！ Chị đây bắt được！<br>Phạm tội quả tang！ Màn bắt giữ chớp nhoáng！",
46:"Ồ？ Không ngờ là mày，đồ trốn việc……",
47:"E hè hè hè hè。Có tiền thưởng không ạ？<br>Có mà phải không ạ？",
48:"Ừm，để ta xem nào。<br>Mà，thằng cướp đâu rồi？",
49:"Thằng này đây！ Nó khăng khăng bảo không làm，<br>nhưng chị sẽ moi ra ngay！",
50:"…………Chào。",51:"…………",
52:"Gặp vài lần rồi nhỉ。Ông là Đội trưởng<br>Cảnh vệ phái từ Milesgard đến đúng không？",
53:"A，à，ờ，ờ……t，tại sao ngài lại ở đây ạ？",
54:"Vì chị bắt được nó đó！ Lao vào đỡ lúc nó đang chạy trốn！<br>Thế này——guwaaaa——！ Khóa chặt tay lại！",
55:"<size=48>ĐỒ，ĐỒ NGUUUUUUUUU XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ！！！</size>",
56:"NGHEEE！？",
57:"Đ，Đội trưởng？ La to như thế huyết áp sẽ tăng đấy ạ……？",
58:"Khỏi lo chuyện bao đồng！ Đồ ngu xuẩn này！<br>Mày có biết mày vừa làm gì không hả！？",
59:"Eeeee～……？ Gì ạ，kẻ cướp ấy mà——",
60:"Im mồm！ Bắt nhầm đấy！ Biết mày lười nhưng<br>không ngờ ngu thế này……Danh nghĩa Đội trưởng Cảnh vệ，phạt giảm lương！",
61:"Khôngggg！？ Sao lại thế——！？",
62:"À，không，Đội trưởng——không cần đến mức đó đâu。Phiền thật đấy nhưng<br>nếu chứng minh được tôi vô tội，thế là đủ rồi。",
63:"Hả……？<br>Trời，anh——bộ anh là người tốt hả？ Anh là ai？",
64:"（……Thằng này nịnh thật đấy）",
65:"Tấm lòng của ngài rất đáng quý，nhưng thế thì không làm gương cho kẻ khác được！<br>Xin hãy để tôi toàn quyền xử lý việc kỷ luật！",
66:"Đ，đâu ra thế——！？ Độc tài quá——！！",
67:"Im mồm！ Mau đi bắt thủ phạm thật đi！",
68:"Hii～！？ E，em đi đây——！",
69:"Chỉ Huy，thật có lỗi quá！！",
70:"Không sao。Mà này，con bé lúc nãy——tên là Celeste hả？<br>Nó là người thế nào？",
71:"Nó cũng tự xưng thế，đúng là một cảnh vệ hư hỏng hết chỗ nói……<br>Sống chỉ vì tiền với rượu，hạnh kiểm cũng tệ。Đúng là đồ không thể chịu nổi。",
72:"Vậy mà anh không đuổi nó，chắc vì nó có tài đúng không？",
73:"……！？<br>Sao ngài biết……？",
74:"（……Quả nhiên là thế）",
75:"Nàyyyy！",
76:"Guwaa！？",
77:"（Lúc bị nó bắt，tôi không hề cảm nhận được gì cho đến khi nó lao vào người）",
78:"（Tuy tôi không tự tin về võ lực，nhưng với tư cách Chỉ Huy tôi có khả năng nhận biết nguy hiểm。<br>Vậy mà tôi đã không nhận ra cú lao tới của nó）",
79:"（Nếu dùng được，có vẻ sẽ thành một nhân tài thú vị đây）",
80:"Ơ，Chỉ Huy？",
81:"Xin lỗi，không có gì。Tôi đi tìm Celeste đây。",
82:"（Nó bảo đi đuổi theo tên cướp nên chắc là ở chợ。<br>Đi xem sao。）",
}

text = en_path.read_bytes().decode('utf-8-sig')
lines = text.splitlines(keepends=True)

cmds = ('title,', 'message,')
seq = 0
for ln in lines:
    if not ln.startswith(cmds):
        continue
    stripped = ln.rstrip('\r\n')
    vi_text = VI[seq]
    if ln.startswith('message,'):
        parts = stripped.split(',', 5)
        en_text = parts[2]
        if en_text.rstrip().endswith('<br>'):
            idx = en_text.rfind('<br>')
            internal_en = en_text[:idx]
        else:
            internal_en = en_text
        en_br = internal_en.count('<br>')
        vi_br = vi_text.count('<br>')
        if en_br != vi_br:
            print(f"Seq {seq}: EN br={en_br} VI br={vi_br}")
            print(f"  EN: {internal_en}")
            print(f"  VI: {vi_text}")
            print()
    elif ln.startswith('title,'):
        parts = stripped.split(',', 2)
        en_text = parts[1]
        en_br = en_text.count('<br>')
        vi_br = vi_text.count('<br>')
        if en_br != vi_br:
            print(f"Seq {seq} (title): EN br={en_br} VI br={vi_br}")
            print(f"  EN: {en_text}")
            print(f"  VI: {vi_text}")
            print()
    seq += 1

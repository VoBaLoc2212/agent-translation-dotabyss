#!/usr/bin/env python3
"""build_vi_part1.py — VI_DICT records 1-40 for hmn_10480100003."""
# EN-asset-is-English case: mixed JP-title / EN-message.
# Translate title JP→VI Title Case; translate message EN→VI.

VI_PART1 = {
    # seq=1: title,JP -> VI Title Case
    1: "Tiền Thưởng Bị Chia Bớt Mất!",
    # seq=2: 情報屋A - So，this is where the bandits' hideout is.
    2: "Vậy‚ đây là ổ của bọn cướp đấy.",  
    # seq=3: <user> - To think it was inside the Frontline Base all along... Guess it was hiding in plain sight.
    3: "Không ngờ lại ở ngay trong Căn Cứ Tiền Tuyến… Đúng là núi vàng‚<br>biển bạc giữa phố.",
    # seq=4: セレスト - Good work. Here's your payment.
    4: "Vất vả rồi. Đây‚ tiền công nè.",
    # seq=5: 情報屋A - Hehe，thanks. Oh yeah，this one's on the house. It's a layout map of the hideout and the guard deployment map. Put 'em to good use. Later.
    5: "Hê hê‚ cảm ơn. À‚ phải rồi‚ cái này là quà đấy. Bản đồ sơ đồ ổ và<br>bản đồ bố trí canh gác. Xài tốt nhé. Bye.",
    # seq=6: <user> - Hmph，he charges a lot，but he does good work. Now if we call the Guard Unit for backup，we can catch them all at once...
    6: "Hừm… lấy nhiều thật đấy‚ nhưng đúng là làm ăn tốt. Giờ gọi Đội Cảnh Vệ đến hỗ trợ là<br>tóm gọn hết…",
    # seq=7: セレスト - Hold on a sec! I'm not calling any backup!
    7: "Chờ chút đã! Em không gọi tiếp viện đâu!",
    # seq=8: <user> - Huh? Why not?
    8: "Hả? Sao lại không?",
    # seq=9: セレスト - Because my cut of the bounty would go down!
    9: "Vì phần tiền thưởng của em sẽ bị giảm mất!",
    # seq=10: <user> - You're just in it for the money! Even you must know that's too crazy，right?
    10: "Chỉ vì tiền thôi hả!?<br>Cơ mà em cũng biết thế là điên rồ mà‚ đúng không?",
    # seq=11: セレスト - I said it'll be fiiine! Anyway，I'm going in alone. Bye-bye.
    11: "Đã bảo là yên tâm mà! Dù sao thì em tự đi một mình. Bye bye.",
    # seq=12: <user> - Ah，hold on!
    12: "A‚ khoan đã!",
    # seq=13: セレスト - Not gonna wait!
    13: "Không chờ đâu!",
    # seq=14: <user> - (...Can't be helped. I'll decide on backup after seeing the scene... If it seems too tough，even Celeste will back down.)
    14: "(…Không còn cách nào. Gọi tiếp viện hay không‚ xem tình hình thực tế rồi tính… Nếu khó quá thì<br>Celeste cũng sẽ bỏ cuộc thôi.)",
    # seq=15: 盗賊団下っ端Ａ - Shift change.
    15: "Đổi ca đây.",
    # seq=16: 盗賊団下っ端Ｂ - Yeah，thanks.
    16: "Ờ‚ cảm ơn.",
    # seq=17: セレスト - Huh...? Those guys are built like bricks... they look pretty tough...
    17: "Ủa…? Mấy tên đó lực lưỡng quá‚ nhìn có vẻ mạnh phết…?",
    # seq=18: <user> - They definitely don't look weak... And judging by the map，there are about ten of them，right?
    18: "Nhìn không có vẻ yếu đâu… Và theo bản đồ bố trí thì có tầm<br>mười tên đúng không?",
    # seq=19: セレスト - Umm...
    19: "Ừm…",
    # seq=20: <user> - (She's wavering，but she'll give up now...)
    20: "(Đang phân vân‚ nhưng chắc sẽ bỏ cuộc thôi…)",
    # seq=21: セレスト - Hey—the bounty is only for the daytime robber? There's nothing on those big guys either?
    21: "Nè—tiền thưởng chỉ dành cho tên cướp ban ngày thôi hả?<br>Mấy tên to xác đó không có à?",
    # seq=22: <user> - That's what you were worried about?!
    22: "Hóa ra em lo cái đó đấy hả!!",
    # seq=23: セレスト - I mean，sure，that guy from earlier was good，but ten guys at his level? That's kind of a hassle，y'know? Doesn't really pay off.
    23: "Thì tại… thằng ban nãy cũng ngon đấy‚ nhưng mười thằng cùng trình độ đó thì<br>cũng hơi phiền. Không đáng công lắm.",
    # seq=24: <user> - (If I tell her no，she'll probably lose her motivation. But if I'm too generous，Alicia will get mad at me...)
    24: "(Nếu bảo không thì nó sẽ mất động lực mất. Nhưng mà phóng tay quá thì<br>Alicia sẽ nổi giận với mình…)",
    # seq=25: <user> - Hmm，hmm...
    25: "Ừm ừm…",
    # seq=26: セレスト - Can you pay it or not? Which is it?!
    26: "Có hay không? Là cái nào đây??",
    # seq=27: <user> - Agh，fine! I'll make them eligible for the bounty too!
    27: "…Eo ôi‚ không còn cách nào! Bọn chúng cũng được thêm vào danh sách truy nã!",
    # seq=28: セレスト - For real! Yay!
    28: "Thật hả!? Tuyệt!",
    # seq=29: <user> - But let me get this straight. What's your plan?
    29: "Nhưng để anh xác nhận. Kế hoạch thế nào?",
    # seq=30: セレスト - First，I'll grab the guy watching the back exit and block it from the outside so they can't escape. I don't want anyone getting away.
    30: "Đầu tiên‚ tóm thằng canh lối thoát hiểm‚ rồi chặn bên ngoài không cho chúng trốn. Vì em không muốn<br>để ai chạy thoát.",
    # seq=31: セレスト - Then it's a frontal assault. They'll underestimate me since I'm just a woman，so I'll arrest them all!
    31: "Xong rồi đâm thẳng từ mặt tiền. Tưởng chỉ có một con nhỏ nên sẽ coi thường‚<br>thế là tóm hết!",
    # seq=32: <user> - Aside from your worry about the strength difference，it's a passing grade... Good grief. What happened to that lazy attitude from earlier?
    32: "Ngoài chỗ lo về chênh lệch sức mạnh ra thì tạm ổn đấy… Trời ơi.<br>Cái vẻ lười biếng ban sáng biến đi đâu hết rồi.",
    # seq=33: <user> - Can't be helped. I'll trust your confidence this once. But I'm calling in some soldiers I can command，just in case.
    33: "Không còn cách nào. Lần này anh sẽ tin vào lòng tự tin của em. Nhưng anh sẽ gọi một ít lính<br>anh điều động được đến hỗ trợ.",
    # seq=34: セレスト - Ehh?
    34: "Ơ~?",
    # seq=35: <user> - I'll have them wait till you're losing，so cut me some slack. Civilian safety and capturing the criminals are top priority.
    35: "Để họ chờ tới khi em sắp thua thôi nên thông cảm đi. An toàn dân thường và<br>bắt tội phạm là ưu tiên hàng đầu.",
    # seq=36: セレスト - Fine. If I win，I get the whole cut，right?
    36: "Hiểu rồi. Nếu em thắng thì em hốt trọn hết chứ hả?",
    # seq=37: <user> - Yeah. Alright，go get 'em!
    37: "Ừ. Được rồi‚ xông lên!",
    # seq=38: (narration) - Celeste kicked open the front door，and all the bandits inside turned to look at her.
    38: "Celeste đạp tung cửa trước‚ lũ cướp trong nhà đồng loạt<br>quay lại nhìn.",
    # seq=39: セレスト - Freeze，everyone! I'm arresting you all on suspicion of robbery and theft!
    39: "Tất cả‚ đứng yên! Bắt các người với tội danh cướp giật và<br>trộm cắp!",
    # seq=40: 強盗犯 - What，the guard?
    40: "Gì‚ đội cảnh vệ à?",
}

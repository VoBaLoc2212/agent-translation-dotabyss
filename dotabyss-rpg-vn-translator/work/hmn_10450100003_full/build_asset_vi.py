#!/usr/bin/env python
"""Build VI output for hmn_10450100003 (Iola first battle scene)."""
import json, re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100003.txt"
VI_OUT = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100003.txt"
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10450100003/ja.json"
EN_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10450100003/en.json"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10450100003_full"

TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# ==================== VI TRANSLATIONS (seq 1..101) ====================
# seq = 1-based index of text command records in the EN asset file order
VI = {}

# Record 1 - title (L31): いけー！　あたしの火炎魔法！
VI[1] = "Đi Nào! Hỏa Diễm Ma Pháp Của Tôi!"

# Record 2 - message (L68): イオラ - Huh? ...Umm，my body feels kinda heavy，I guess?
# JP: あれ？<br>うーーーん……？　なんか体が重たい、かも？
VI[2] = "Hử? ...Ừmmmm……? Sao cơ thể cứ nặng nề thế nhỉ?<br> "

# Record 3 - message (L70): <user> - Probably just tired from your first battlefield，huh?
# JP: 初めての戦場で疲れたんじゃないか？
VI[3] = "Chắc chỉ là mệt vì lần đầu ra chiến trường thôi，hả?<br> "

# Record 4 - message (L81): イオラ - Ah，yeah，that could be it... *sigh*...
# JP: あ、そうね。それはありそう――はぁっ。
VI[4] = "À，ừ nhỉ. Cũng có thể lắm——*thở dài*...<br> "

# Record 5 - message (L83): <user> - If so，go rest in the back...
# JP: だったら、後ろのほうで休んでこい。<br>戦闘が終わったら呼びに行くから。
# EN has 1 <br> (collapsed internal break)
VI[5] = "Vậy thì ra phía sau nghỉ đi. Chiến đấu xong sẽ đến gọi em.<br> "

# Record 6 - message (L94): イオラ - Okaaay...
# JP: はーい……
VI[6] = "Vâng ạ……<br> "

# Record 7 - message (L142): イオラ - (*sigh*... Now that I'm alone...)
# JP: （ふぅっ……１人になると、どっと疲れが出るわね。<br>休ませてもらえて正解かも）
VI[7] = "(*Phù*…… khi một mình rồi mệt mới ùa ra.<br>Chắc nghỉ ngơi là lựa chọn đúng đắn.)<br> "

# Record 8 - message (L165): 兵士Ａ - Raaah!
# JP: おらー！
VI[8] = "Háàaa!<br> "

# Record 9 - message (L184): イオラ - ...Hmm，real soldiers sure are loud...
# JP: ……うーん、本物の兵士って、やっぱり戦っているときはうるさいのね。<br>彼氏には、ちょっと向かないかなー。
VI[9] = "...Ừm，lính thật đúng là ồn ào nhỉ khi chiến đấu.<br>Làm bạn trai thì hơi khó đấy nhỉ.<br> "

# Record 10 - message (L195): イオラ - Ahh，I wonder if there's someone perfect...
# JP: あーあ、あたしの好みバッチリの人いないかな～。<br>例えば先生みたいな……
VI[10] = "Haa，không biết có ai hợp gu mình không nhỉ～.<br>Ví dụ như Thầy ấy……<br> "

# Record 11 - message (L199): (none) - —clatter!
# JP: ――ガタタッ。
VI[11] = "——Lộp cộp!<br> "

# Record 12 - message (L225): イオラ - (Huh? Did someone come to rest?)
# JP: （んっ？　誰か休みに来たのかしら？）
VI[12] = "(Hử? Có ai tới nghỉ ngơi à?)<br> "

# Record 13 - message (L299): 小型モンスター - skree...!
# JP: ギッ……！？
VI[13] = "Kí……!?<br> "

# Record 14 - message (L308): イオラ - Wha-! M-Monster!
# JP: なっ！？　モ、モンスター！？
VI[14] = "Hả!? Q-Quái thú!?<br> "

# Record 15 - message (L331): イオラ - I have to call for help...
# JP: 助けを呼ばないと……誰、か……
VI[15] = "Phải gọi cứu viện…… Ai，đâu đó……<br> "

# Record 16 - message (L346): 小型モンスター - ...!
# JP: ……！
VI[16] = "……!<br> "

# Record 17 - message (L401): イオラ - (! N-No!)
# JP: （っ！　だ、だめっ！）
VI[17] = "(Chết! Kh-không được!)<br> "

# Record 18 - message (L420): (none) - Iola hastily shut her mouth...
# JP: イオラは叫び声を上げかけていた口を慌てて閉じた。
VI[18] = "Iola vội vàng ngậm miệng lại，suýt nữa thì hét lên.<br> "

# Record 19 - message (L490): イオラ - (If I upset it carelessly...)
# JP: （下手に刺激したら飛び掛かってくる……やられる！）
VI[19] = "(Nếu kích động nó sẽ lao tới…… mình tiêu!)<br> "

# Record 20 - message (L507): (none) - Though Iola lacked front-line combat experience...
# JP: 前線での実践経験はないイオラだが、格闘家である父との組手経験は豊富。<br>時折本気を見せてくれた父との鍛練の経験が、イオラに危機を直感させた。
VI[20] = "Dù chưa có kinh nghiệm chiến đấu thực tế ở tiền tuyến，Iola lại giàu kinh nghiệm đối luyện với người cha võ sĩ của mình.<br>Những buổi tập mà thỉnh thoảng cha ra tay thật đã giúp Iola cảm nhận trực giác được nguy hiểm.<br> "

# Record 21 - message (L543): イオラ - (I can't run away after all...)
# JP: （やっぱ逃げらんないっぽいな……<br>あたし１人でこいつをどうにかするしかない、ってこと？）
VI[21] = "(Chắc không chạy được rồi……<br>Vậy là mình phải xoay xở với cái thứ này một mình à?)<br> "

# Record 22 - message (L560): (none) - Suddenly，the Commander's words crossed her mind.
# JP: ふと、<user>の言葉がよぎる。
VI[22] = "Chợt，lời của Chỉ Huy thoáng qua trong đầu cô.<br> "

# Record 23 - message (L588): <user> - You're a mage...
# JP: 魔法使いなんだから魔法で、なんてこだわるな。得意の格闘術でも<br>なんでも使って、絶対に生き延びろ。いいな？
VI[23] = "Là pháp sư thì đừng có cố chấp chuyện phải dùng ma pháp. Dùng võ thuật sở trường hay<br>bất cứ thứ gì，nhất định phải sống sót đấy. Nghe chưa?<br> "

# Record 24 - message (L638): (none) - The stance Iola chose...
# JP: イオラが選んだ構えは魔法使いが呪文を唱える姿勢ではなく、<br>慣れ親しんだ格闘家の構えだった。
VI[24] = "Tư thế Iola chọn không phải của một pháp sư tụng thần chú，<br>mà là thế võ quen thuộc của một võ sĩ.<br> "

# Record 25 - message (L693): 小型モンスター - *GRROOOWL!*
# JP: グォオッ！！
VI[25] = "*GỪUU!*<br> "

# Record 26 - message (L745): イオラ - *Tch!*
# JP: くっ！？
VI[26] = "*Chậc!*<br> "

# Record 27 - message (L799): (none) - She dodged the monster's leaping attacks...
# JP: 飛び掛かってきたモンスターの攻撃を格闘術の動きで避ける。<br>モンスターは１度、２度と攻撃を重ねてくるが、どうにかやり過ごす。
VI[27] = "Cô né đòn tấn công của quái thú bằng động tác võ thuật.<br>Quái thú liên tiếp tấn công nhưng cô vẫn xoay sở trụ được.<br> "

# Record 28 - message (L865): イオラ - (I'm okay... I can fight!)
# JP: （大丈夫……ちゃんと戦えてる！）
VI[28] = "(Ổn…… mình chiến được mà!)<br> "

# Record 29 - message (L882): (none) - She recalled training with her martial artist father...
# JP: 格闘家の父と鍛練しているときの感覚が思い出された。<br>リングの上に相手と自分だけ――そんな錯覚がイオラの集中力を高めていく。
VI[29] = "Cảm giác khi tập luyện cùng người cha võ sĩ ùa về.<br>Ảo giác chỉ còn đối thủ và mình trên võ đài——càng làm tăng sự tập trung của Iola.<br> "

# Record 30 - message (L930): イオラ - *Hah!*
# JP: ハッ！
VI[30] = "*Há!*<br> "

# Record 31 - message (L985): (none) - —BOGH!
# JP: ――ボグゥッ！！！
VI[31] = "——BỐP!<br> "

# Record 32 - message (L994): 小型モンスター - *Gii! ... Gii!*
# JP: ギッ！？<br>……ギィィ！！！
VI[32] = "*Kí!? ... Kiiii!*<br> "

# Record 33 - message (L1048): (none) - She landed a counterpunch...
# JP: カウンターで拳を叩き込むが、モンスターを倒すまでには至らない。
# EN has 2 <br> (1 internal + 1 suffix) — need internal split
VI[33] = "Cô tung cú đấm phản đòn，<br>nhưng chưa đủ hạ gục quái thú.<br> "

# Record 34 - message (L1103): イオラ - (If only I could use Magic here...)
# JP: （……ここで、魔法が使えたら――）
VI[34] = "(……Giá mà ở đây dùng được ma pháp――)<br> "

# Record 35 - message (L1120): (none) - The incantation she had unconsciously begun flowed smoothly...
# JP: 無意識に唱え始めていた詠唱はスムーズに進んでいく。<br>集中していたおかげで、魔法への苦手意識が自然と消えていた。
VI[35] = "Câu thần chú cô vô thức bắt đầu niệm trôi chảy dần.<br>Nhờ tập trung cao độ，nỗi sợ ma pháp đã tự nhiên biến mất.<br> "

# Record 36 - message (L1122): (none) - And then—
# JP: そして――
VI[36] = "Và rồi——<br> "

# Record 37 - message (L1160): イオラ - (I did it!)
# JP: （……できた！）
VI[37] = "(……Được rồi!)<br> "

# Record 38 - message (L1226): (none) - Fire ignited on her fist...
# JP: イメージ通りに火が拳に灯る。<br>モンスターが炎に驚き、後ずさった。
VI[38] = "Lửa bùng lên trên nắm đấm đúng như tưởng tượng.<br>Quái thú giật mình vì ngọn lửa，lùi lại.<br> "

# Record 39 - message (L1268): イオラ - An opening! *Haaaaah!*
# JP: 隙ありっ！　ハァァァアッ！
VI[39] = "Sơ hở! *Háaaaa!*<br> "

# Record 40 - message (L1343): 小型モンスター - *GYAAAAH!*
# JP: ギャアアアッ！？
VI[40] = "*Gyaaaa!*?<br> "

# Record 41 - message (L1404): 兵士Ｂ - Commander! The monster has been defeated!
# JP: 司令官！　モンスターの討伐、完了しました！
VI[41] = "Chỉ Huy! Đã tiêu diệt quái thú xong!<br> "

# Record 42 - message (L1406): <user> - Alright... I'll go check on Iola.
# JP: よし。……俺は、イオラの様子でも見てくるか。
VI[42] = "Được rồi……Anh qua xem tình hình Iola thế nào.<br> "

# Record 43 - message (L1408): イオラ - *pant*!
# JP: ハァアアアッ！
VI[43] = "*Háaaaa!*<br> "

# Record 44 - message (L1418): (none) - —boom!
# JP: ――ドーン！！
VI[44] = "——ĐÙNG!!<br> "

# Record 45 - message (L1439): 兵士Ａ - Wh-what was that?! An explosion?!
# JP: な、なんだ！？　爆発音！？
VI[45] = "C-cái gì thế!? Tiếng nổ!?<br> "

# Record 46 - message (L1441): <user> - That's the direction Iola went?!
# JP: イオラが向かった方角だとっ！？
VI[46] = "Hướng Iola đi ư!?<br> "

# Record 47 - message (L1456): <user> - (She's fighting...? No way，she was attacked!...)
# JP: （戦ってる……？　まさか、襲われてたのか！？<br>くそっ！　間に合ってくれ！）
VI[47] = "(Đang chiến đấu……? Không lẽ，bị tấn công rồi!?<br>Chết tiệt! Kịp đấy!)<br> "

# Record 48 - message (L1486): <user> - Iola! Are you okay?!
# JP: イオラ！　無事か！？
VI[48] = "Iola! Em ổn chứ!?<br> "

# Record 49 - message (L1522): イオラ - Hyah，hyah，hyah，hyahh!
# JP: でやでやでやでやーっ！
VI[49] = "Hự，hự，hự，hự—!<br> "

# Record 50 - message (L1532): <user> - ...Huh?
# JP: ……えっ？
VI[50] = "……Hả?<br> "

# Record 51 - message (L1534): (none) - When Commander rushed over，<br>Iola was tearing into the monster...
# JP: <user>が駆け付けると、<br>拳に火を宿したイオラがモンスター相手に暴れ回っていた。
VI[51] = "Khi Chỉ Huy chạy tới，<br>Iola đang quần nhau với quái thú，nắm đấm rực lửa.<br> "

# Record 52 - message (L1545): イオラ - Go! My fire magic! Flame Fist!
# JP: いけー！　あたしの火炎魔法！<br>フレイムフィストーーー！！！
# EN has 1 <br> (collapsed internal break)
VI[52] = "Lên nào! Hỏa diễm ma pháp của tôi! Flame Fist——!!!<br> "

# Record 53 - message (L1644): 小型モンスター - Gigigiiiii!
# JP: ギギギィイイ！？
VI[53] = "Gigigiiiii!?<br> "

# Record 54 - message (L1694): (none) - Every punch sent a fireball into the monster...
# JP: 拳を振るうたびに火の玉が飛んでいき、モンスターに命中し続ける。<br>猛攻を受けたモンスターは力を失い、絶命した。
VI[54] = "Mỗi cú đấm lại phóng ra một quả cầu lửa，trúng liên tiếp vào quái thú.<br>Dính đòn mãnh liệt，quái thú mất sức và tắt thở.<br> "

# Record 55 - message (L1734): イオラ - *pant，pant*... I-I beat it...? On my own...?
# JP: はっ、はぁっ……あ、あたし、倒した……？<br>ひとりで……？
# EN has 1 <br> (collapsed internal break)
VI[55] = "*Hổn hển*…… A，mình hạ được nó……? Một mình……?<br> "

# Record 56 - message (L1798): 兵士Ａ - ...
# JP: ……
VI[56] = "………<br> "

# Record 57 - message (L1800): <user> - ...
# JP: …………
VI[57] = "…………<br> "

# Record 58 - message (L1811): イオラ - Ah，everyone... why's everyone so quiet?
# JP: あ、みんな……なんで黙ってるの？
VI[58] = "À，mọi người…… sao im lặng thế?<br> "

# Record 59 - message (L1823): 兵士Ｂ - Whoa，incredible! What kind of fighting style was that?!
# JP: うおーっ、すげぇー！<br>なんだ今の戦い方！？
# EN has 1 <br> (collapsed internal break)
VI[59] = "Ồ—! Tuyệt vời! Lối đánh vừa rồi là gì thế!?<br> "

# Record 60 - message (L1832): 兵士Ａ - I've never seen a style that mixes martial arts and magic!<br>Commander，what part of her is supposed to be weak?
# JP: 格闘と魔法をミックスさせた戦い方なんて初めて見たぞ！？<br>司令官、この子のどこが弱いんですか！？
VI[60] = "Lần đầu thấy lối đánh kết hợp võ thuật và ma pháp đấy!?<br>Chỉ Huy，con bé này yếu chỗ nào vậy!?<br> "

# Record 61 - message (L1834): <user> - ...That's my line. Good grief. I never thought she'd turn out to be<br>such a monster.
# JP: ……俺の台詞だ。<br>やれやれ。まさか、こんな化け方をするとはな。
VI[61] = "……Đó là lời của anh mới đúng.<br>Trời ạ. Không ngờ nó lại biến hóa thế này.<br> "

# Record 62 - message (L1884): イオラ - Um... are you praising me?
# JP: えっと……あたし、褒められてるの？
VI[62] = "Ừm…… mình đang được khen à?<br> "

# Record 63 - message (L1886): <user> - What else would it look like? You did great，Iola. That was a good<br>fight.
# JP: それ以外にどう見える。<br>よくやったぞ、イオラ。良い戦いだった。
VI[63] = "Chẳng lẽ trông như thế nào khác được.<br>Làm tốt lắm，Iola. Trận đấu hay đấy.<br> "

# Record 64 - message (L1888): <user> - Like your father said，you're overflowing with talent.
# JP: お前の父親が言うように、お前は才能に溢れている。
VI[64] = "Như cha em đã nói，em tràn đầy tài năng.<br> "

# Record 65 - message (L1899): イオラ - ...
# JP: ……
VI[65] = "………<br> "

# Record 66 - message (L1901): <user> - I'm glad you've finally bloomed.
# JP: 花開いて、よかったな。
VI[66] = "Nở hoa rồi，tốt quá nhỉ.<br> "

# Record 67 - message (L1912): イオラ - ...Yeah!♪
# JP: ……うんっ♪
VI[67] = "……Ừm!♪<br> "

# Record 68 - messageTextUnder (L1951): —Later，exploring the Abyss，Iola fought monsters confidently...
# JP: ――その後の大穴探索でも、イオラはモンスター相手に堂々と戦ってみせた。<br>彼女は実戦で、確かに自分の戦い方を会得したのである。
# EN has 0 <br> in text field (mesageTextUnder has no <br> suffix). VI text only (no ,,,on)
VI[68] = "——Sau đó，trong chuyến thám hiểm Đại Huyệt，Iola đã chiến đấu đầy tự tin với lũ quái thú. Qua thực chiến，cô ấy đã thực sự làm chủ lối chiến đấu của riêng mình."

# Record 69 - message (L1993): イオラ - Phew，it's over. My first time exploring the Abyss.
# JP: はーっ、終わっちゃったなぁ。初めての大穴探索。
VI[69] = "Phù，kết thúc rồi. Lần đầu khám phá Đại Huyệt.<br> "

# Record 70 - message (L1995): <user> - You took plenty of notes and improved your magic. Think you can<br>write a decent report?
# JP: メモもたくさん取ったし、魔法も上達した。<br>立派なレポートが書けそうか？
VI[70] = "Ghi chép nhiều rồi，ma pháp cũng tiến bộ.<br>Viết được báo cáo tử tế chứ?<br> "

# Record 71 - message (L2006): イオラ - Yeah! I'm going to write to the school...
# JP: うん！　レポート以外に、格闘と魔法をミックスさせた戦い方についても<br>研究していきたい、って学校に手紙を書くつもりよ。
VI[71] = "Ừm! Ngoài báo cáo ra，em sẽ viết thư cho trường<br>muốn nghiên cứu thêm về cách chiến đấu kết hợp võ thuật và ma pháp.<br> "

# Record 72 - message (L2017): イオラ - Hey，that went pretty well for just winging it!...
# JP: ぶっつけ本番であれだけうまくいったんだもの。<br>ちゃんと研究すれば魔法学校も卒業できると思う！
VI[72] = "Ứng biến mà đã tốt thế kia mà.<br>Nghiên cứu tử tế thì chắc chắn tốt nghiệp được trường ma pháp!<br> "

# Record 73 - message (L2019): <user> - Yeah，I think so too.
# JP: あぁ、俺もそう思うぞ。
VI[73] = "Ừ，anh cũng nghĩ thế.<br> "

# Record 74 - message (L2021): <user> - ...Iola. After you graduate，come work for me.
# JP: ……イオラ。もし卒業したら、俺のところへ働きに来い。
VI[74] = "……Iola. Nếu tốt nghiệp，về chỗ anh làm việc đi.<br> "

# Record 75 - message (L2032): イオラ - Eeeh!
# JP: えっ！？
VI[75] = "Hả!?<br> "

# Record 76 - message (L2043): イオラ - W-well，you can't just spring that on me...
# JP: そ、そんな、急に言われても困るわよ……
VI[76] = "Ch-chuyện đó，bỗng dưng bảo thế cũng khó xử quá……<br> "

# Record 77 - message (L2054): イオラ - Ah，actually，forget it!...
# JP: あ、っていうか、やっぱりやだ！<br>何されるか分かんないし！　不当にこき使われそう！
VI[77] = "À，mà thôi，chẳng thèm!<br>Không biết sẽ bị làm gì nữa! Chắc chắn bị sai vặt vô tội vạ!<br> "

# Record 78 - message (L2056): <user> - I wouldn't do that...
# JP: そんなことはしないが、もし心配ならお前が安心して働けるように、<br>満足いくレベルまで細かい契約書を作ってもいい。
VI[78] = "Anh không làm thế đâu. Nhưng nếu em lo，anh có thể soạn hợp đồng chi tiết<br>đến mức em hài lòng，để em yên tâm làm việc.<br> "

# Record 79 - message (L2058): <user> - Once you graduate，you're an adult...
# JP: 卒業したら、もう大人だからな。やりたいこと、やりたくないことは<br>自分で決めて、相手と交渉するんだ。
VI[79] = "Tốt nghiệp rồi thì là người lớn rồi. Chuyện muốn hay không muốn làm<br>thì tự mình quyết định và thương lượng với đối phương.<br> "

# Record 80 - message (L2069): イオラ - ...So you really see me as an adult，Teacher?
# JP: ……先生は、あたしを大人として扱ってくれるわけ？
VI[80] = "……Thầy thực sự coi em như người lớn sao?<br> "

# Record 81 - message (L2071): <user> - Well，after you graduate，you're an adult.
# JP: そりゃあ、卒業したら大人だろ。
VI[81] = "Tất nhiên，tốt nghiệp thì là người lớn chứ sao.<br> "

# Record 82 - message (L2073): <user> - You've still got time till graduation...
# JP: 卒業までまだ時間はあるだろうし、考えておいてくれ。<br>お前は本番に強くて実戦向けだ。そういう奴は手元にいくらでもほしい。
VI[82] = "Còn thời gian tới tốt nghiệp，cứ suy nghĩ đi.<br>Em là người mạnh trong thực chiến. Loại đấy anh muốn có bao nhiêu cũng được.<br> "

# Record 83 - message (L2084): イオラ - Well，well... You want me，Teacher?
# JP: ふ、ふぅ～ん……あたしがほしいんだ？
VI[83] = "Hử，hử～n…… Thầy muốn em à?<br> "

# Record 84 - message (L2086): <user> - Well，anyway，get a good night's sleep...
# JP: ま、とりあえず今日はしっかり寝て、<br>明日からレポートをがんばって仕上げろ。俺も帰って寝る。じゃあな。
VI[84] = "Thôi，hôm nay cứ ngủ thật ngon đi，<br>từ mai cố gắng hoàn thành báo cáo. Anh cũng về ngủ đây. Bye.<br> "

# Record 85 - message (L2113): イオラ - (After graduation... after graduation，huh?)
# JP: （卒業後……卒業後かぁ）
VI[85] = "(Sau tốt nghiệp…… sau tốt nghiệp à)<br> "

# Record 86 - messageTextCenter (L2149): <size=48>—A Few Days Later—</size>
# JP: <size=48>――数日後</size>
VI[86] = "<size=48>——Một Vài Ngày Sau——</size>"

# Record 87 - message (L2192): イオラ - So anyway! I passed the report and avoided flunking!
# JP: ってなわけで、無事にレポートが合格して落第は回避できたの！
VI[87] = "Và thế là! Báo cáo qua suôn sẻ，thoát khỏi cảnh trượt tốt nghiệp!<br> "

# Record 88 - message (L2203): イオラ - It's all thanks to you，Teacher. Thanks!♪
# JP: あんたのおかげよ。ありがとね♪
VI[88] = "Nhờ có Thầy cả đấy. Cảm ơn nha♪<br> "

# Record 89 - message (L2205): <user> - You're welcome... but you should be able to go back to school by<br>now，so why are you still here?
# JP: どういたしまして。<br>……で、学校にもう戻れるはずなのに、なんでまだここにいるんだ？
VI[89] = "Không có gì.<br>……Mà，đáng lẽ em phải về trường được rồi chứ，sao vẫn còn ở đây?<br> "

# Record 90 - message (L2216): イオラ - Well，you see... nobody's ever tried a fighting style that mixes martial<br>arts and magic，right，Teacher?
# JP: それがね～……格闘と魔法をミックスした戦い方なんて<br>誰もやったことないでしょ？
VI[90] = "Thì tại…… lối đánh kết hợp võ thuật và ma pháp<br>chưa ai từng làm mà đúng không?<br> "

# Record 91 - message (L2236): イオラ - Honestly，even if I go back to school...
# JP: 正直な話、学校に戻ってもどうやって研究すればいいのか分からないのよね。<br>だったら、実戦で磨いていったほうが早いんじゃないかなって思ったの。
VI[91] = "Nói thật thì，về trường cũng chẳng biết nghiên cứu thế nào.<br>Thà mài giũa qua thực chiến còn nhanh hơn không?<br> "

# Record 92 - message (L2238): <user> - Hmm，that's a fair point...
# JP: ふむ。一理あるな。<br>元々、実戦で見出した戦法なわけだし。
VI[92] = "Hừm，cũng có lý.<br>Dù sao cũng là chiến thuật đã tìm ra trong thực chiến mà.<br> "

# Record 93 - message (L2249): イオラ - Right! You've fought all kinds of people...
# JP: でしょ！　色々な人と戦ってきたあんたなら<br>あたしのこともよく分かってくれそうじゃない？
VI[93] = "Đúng không! Thầy từng đánh với đủ loại người，<br>chắc sẽ hiểu em nhỉ?<br> "

# Record 94 - message (L2260): イオラ - I still don't know anything...
# JP: あたし、まだ何も分かってないから――<br>これからも色々教えてほしいの。だめ？
VI[94] = "Em vẫn chưa biết gì cả nên——<br>Em muốn Thầy dạy em đủ thứ từ giờ. Được không?<br> "

# Record 95 - message (L2262): <user> - Good grief. You're always making up your own mind...
# JP: やれやれ。相変わらず、勝手に決めてしまう娘だなぁ。
VI[95] = "Trời ạ. Vẫn là đứa hay tự tiện quyết định nhỉ.<br> "

# Record 96 - message (L2273): イオラ - W-well，I can't help it! That's just who I am!
# JP: しょ、しょうがないじゃん～。<br>それがあたしなんだもん！
# EN has 1 <br> (collapsed internal break)
VI[96] = "C-chẳng phải hết cách sao～. Đó là em mà!<br> "

# Record 97 - message (L2275): <user> - Ha ha ha. True enough. Well，as long as it doesn't interfere with<br>work，I'll teach you.
# JP: ハッハッハ。確かにな。<br>まぁ、仕事に差し支えない範囲でなら教えてやる。
VI[97] = "Ha ha ha. Đúng thật.<br>Thôi，trong phạm vi không ảnh hưởng công việc thì dạy cho.<br> "

# Record 98 - message (L2314): イオラ - Alright，Teacher!♪
# JP: やったねーっ♪
VI[98] = "Được rồi Thầy ơi!♪<br> "

# Record 99 - message (L2316): <user> - Whoa!
# JP: どわっ！？
VI[99] = "Woah!?<br> "

# Record 100 - message (L2318): (none) - Iola suddenly hugged the Commander.
# JP: イオラは<user>にいきなり抱き付いた。
VI[100] = "Iola đột nhiên ôm chặt Chỉ Huy.<br> "

# Record 101 - message (L2329): イオラ - I'm counting on you from now on，Teacher!♪
# JP: これからよろしくね、先生♪
VI[101] = "Từ giờ mong Thầy giúp đỡ nha，Thầy ơi!♪<br> "

# ==================== BUILD ====================
en_raw = EN_ASSET.read_bytes()
has_bom = en_raw.startswith(b"\xef\xbb\xbf")
en_text = en_raw.decode("utf-8-sig")
has_crlf = b"\r\n" in en_raw
lines = en_text.split("\n")
# Restore proper split: splitlines keeps CRLF intact per line
import sys
data = en_raw.decode("utf-8-sig")
lines_raw = data.splitlines(True)

TEXT_CMDS_SET = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

# First enumerate all text lines to get record count
seq = 0
text_line_nos = []
for i, ln in enumerate(lines_raw):
    clean_ln = ln.rstrip("\r\n")
    if clean_ln.startswith(TEXT_CMDS_SET):
        seq += 1
        text_line_nos.append(i)

print(f"Total text records: {seq}")
assert seq == 101, f"Expected 101 text records, got {seq}"
assert len(VI) == 101, f"VI dict has {len(VI)} entries, expected 101"

# PREFLIGHT: check <br> counts and ASCII commas
errors = []
for i, ln in enumerate(lines_raw):
    clean_ln = ln.rstrip("\r\n")
    if not clean_ln.startswith(TEXT_CMDS_SET):
        continue
    seq_idx = text_line_nos.index(i) + 1
    vi_text = VI[seq_idx]
    
    if clean_ln.startswith("title,"):
        # title field
        en_text_field = clean_ln.split(",", 1)[1]
        vi_text_field = vi_text
        # title has no <br> suffix
        en_br = en_text_field.count("<br>")
        vi_br = vi_text_field.count("<br>")
        if en_br != vi_br:
            errors.append(f"LINE {i+1} (seq {seq_idx}) BR MISMATCH: EN has {en_br}, VI has {vi_br}")
        if "," in vi_text_field:
            errors.append(f"LINE {i+1} (seq {seq_idx}) ASCII COMMA in VI")
    elif clean_ln.startswith("messageTextUnder,"):
        parts = clean_ln.split(",", 5)
        en_text_field = parts[2]
        vi_text_field = vi_text
        en_br = en_text_field.count("<br>")
        vi_br = vi_text_field.count("<br>")
        if en_br != vi_br:
            errors.append(f"LINE {i+1} (seq {seq_idx}) BR MISMATCH: EN has {en_br}, VI has {vi_br}")
        if "," in vi_text_field:
            errors.append(f"LINE {i+1} (seq {seq_idx}) ASCII COMMA in VI")
    elif clean_ln.startswith("messageTextCenter,"):
        parts = clean_ln.split(",", 5)
        en_text_field = parts[2]
        vi_text_field = vi_text
        en_br = en_text_field.count("<br>")
        vi_br = vi_text_field.count("<br>")
        if en_br != vi_br:
            errors.append(f"LINE {i+1} (seq {seq_idx}) BR MISMATCH: EN has {en_br}, VI has {vi_br}")
        if "," in vi_text_field:
            errors.append(f"LINE {i+1} (seq {seq_idx}) ASCII COMMA in VI")
    elif clean_ln.startswith("message,"):
        parts = clean_ln.split(",", 5)
        en_text_field = parts[2]
        vi_text_field = vi_text
        en_br = en_text_field.count("<br>")
        vi_br = vi_text_field.count("<br>")
        if en_br != vi_br:
            errors.append(f"LINE {i+1} (seq {seq_idx}) BR MISMATCH: EN has {en_br}, VI has {vi_br}")
        if "," in vi_text_field:
            errors.append(f"LINE {i+1} (seq {seq_idx}) ASCII COMMA in VI")

if errors:
    print("PREFLIGHT ERRORS:")
    for e in errors:
        print(f"  {e}")
    print(f"Total: {len(errors)} errors")
    sys.exit(1)
else:
    print("PREFLIGHT PASSED: all <br> counts match, no ASCII commas in VI fields")

# BUILD output
out_lines = []
seq_idx = 0
for i, ln in enumerate(lines_raw):
    clean_ln = ln.rstrip("\r\n")
    ending = ln[len(clean_ln):]  # preserve original line ending
    
    if not clean_ln.startswith(TEXT_CMDS_SET):
        out_lines.append(ln)
        continue
    
    seq_idx += 1
    vi_text = VI[seq_idx]
    
    if clean_ln.startswith("title,"):
        parts = clean_ln.split(",", 1)
        # parts[0] = "title", parts[1] = text (JP text)
        new_line = f"title,{vi_text}"
    elif clean_ln.startswith("messageTextUnder,"):
        parts = clean_ln.split(",", 5)
        # parts[0..5]: messageTextUnder,,[text],,,on
        parts[2] = vi_text
        new_line = ",".join(parts)
    elif clean_ln.startswith("messageTextCenter,"):
        parts = clean_ln.split(",", 5)
        parts[2] = vi_text
        new_line = ",".join(parts)
    elif clean_ln.startswith("message,"):
        parts = clean_ln.split(",", 5)
        parts[2] = vi_text
        new_line = ",".join(parts)
    
    out_lines.append(new_line + ending)

# Write output
out_raw = ("\ufeff" if has_bom else "") + "".join(out_lines)
VI_OUT.parent.mkdir(parents=True, exist_ok=True)
VI_OUT.write_bytes(out_raw.encode("utf-8-sig") if has_bom else out_raw.encode("utf-8"))

# Verify
out_data = VI_OUT.read_bytes()
out_text = out_data.decode("utf-8-sig")
out_lines2 = out_text.splitlines(True)

en_lines_count = len(lines_raw)
vi_lines_count = len(out_lines2)

print(f"EN lines: {en_lines_count}, VI lines: {vi_lines_count}")
print(f"Line count match: {en_lines_count == vi_lines_count}")
bom_check = out_data.startswith(b'\xef\xbb\xbf')
print(f"BOM preserved: {bom_check == has_bom}")
crlf_check = b'\r\n' in out_data
print(f"CRLF preserved: {crlf_check == has_crlf}")
print("BUILD COMPLETE")

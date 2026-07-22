import os
import json

# ============================================================
# COMPLETE VIETNAMESE TRANSLATION DICTIONARY FOR hmn_10500100001
# Key = EN asset text field (exact match including <br> suffix)
# Value = Vietnamese translation
# ============================================================

VI = {
    # 1. TITLE (JP -> VI Title Case)
    "くすんだ石ころ": "Viên Đá Nhòe",
    
    # 2. MESSAGE TEXTS (EN asset text -> VI)
    "There was a knock at the door.<br> ": "Có tiếng gõ cửa.<br> ",
    "Come in.<br> ": "Vào đi.<br> ",
    "Yes! Pardon the intrusion!<br> ": "Vâng! Phiền rắc chút ạ!<br> ",
    "So you're the volunteer who arrived today.<br> ": "Ngươi là tân binh vừa đến hôm nay à.<br> ",
    "Yes! I am Betty of Milesgard!<br> ": "Vâng! Em là Betty từ Milesgard ạ!<br> ",
    "Haha, you're a lively one. I heard you requested assignment to the<br>Frontline Base—why's that?<br> ": "Haha, nhỏ này nhiệt tình đấy. Nghe nói ngươi xin về Căn Cứ Tiền Tuyến, tại sao vậy?<br> ",
    "Yes! My family has been knights for generations. Since childhood, I've<br>witnessed my father and brother's heroic deeds on the battlefield!<br> ": "Vâng! Gia gia em đời đời quân nhân, từ nhỏ em đã chứng kiến cha anh em anh oai phong trên chiến trường!<br> ",
    "That's why my goal is to become a great soldier like my father and<br>brother, and to make a name for myself!<br> ": "Vì thế mục tiêu của em là trở thành binh sĩ xuất sắc như cha anh, để tên tuổi em được biết đến!<br> ",
    "I see. Your family must be expecting great things from you.<br> ": "Thôi hiểu. Gia đình chắc mong to lớn ở em lắm.<br> ",
    "Huh? Th-that is... um...<br> ": "Ủa? Thì th-thì là ừm...<br> ",
    "What's wrong?<br> ": "Sự việc thế nào?<br> ",
    "Actually, my family has opposed my becoming a soldier...<br> ": "Thực ra... gia đình em phản đối em làm binh sĩ...<br> ",
    "Oh? Why is that?<br> ": "Ồ? Tại sao vậy?<br> ",
    "They said that a small woman like me could never handle dangerous<br>battlefield duties...<br> ": "Bọn họ nói con gái nhỏ nhạy như em không thể gánh nổi nhiệm vụ chiến trường nguy hiểm...<br> ",
    "...I see. Then you came to the right place.<br> ": "...Hiểu rồi. Đến đây là đúng chỗ.<br> ",
    "Huh?<br> ": "Ủa?<br> ",
    "This is the front line. Chances to prove yourself are everywhere. Earn<br>merits here and show your family you've got what it takes.<br> ": "Đây là tiền tuyến. Cơ hội dựng công khắp nơi. Làm công đến đây để gia đình thấy em xứng đáng làm binh sĩ.<br> ",
    "Yes, sir! I will surely meet your expectations, Commander! Now, I shall<br>take my leave!<br> ": "Vâng, ạ! Em chắc chắn sẽ đáp ứng kỳ vọng của Chỉ Huy! Em xin phép lui!<br> ",
    "She is quite spirited, and seems like a fine girl.<br> ": "Cô ấy rất hăng hái, lại còn là cô gái tốt.<br> ",
    "Yeah. Having someone like that around really lifts the mood.<br> ": "Ừ. Có người như thế không khí nơi đây dễ chịu hơn.<br> ",
    "I hope she does well!<br> ": "Hy vọng cô ấy làm tốt!<br> ",
    "Yeah.<br> ": "Ừ.<br> ",
    "<size=48>—A few months later.</size>": "<size=48>—Vài Tháng Sau</size>",
    "So, excavation inside the Abyss is proving difficult. We had high<br>hopes for the Engineer Corps with their specialized skills, but...<br> ": "Vậy thì... khai quật trong Đại Huyệt đang gặp khó khăn. Đội Kỹ Sư chuyên môn ta kỳ vọng cao nhưng...<br> ",
    "When we actually looked into it, they've been fighting endlessly over<br>who should take charge as captain, and work has hardly progressed.<br> ": "Mở ra xem thì toàn tranh giành ai làm đội trưởng dẫn việc, công việc không tiến được chút nào.<br> ",
    "So they'll only listen to someone they acknowledge. These<br>craftsman-types can be a real handful at times like this.<br> ": "Chỉ nghe người mình công nhận thôi. Nhóm thủ công kiểu này lúc khó xử lắm.<br> ",
    "The captain, huh... Should I just appoint one myself? No, if I take a<br>high-handed approach, they'll only resist more...<br> ": "Đội trưởng à... có nên ta chỉ định luôn không? Không, đập đầu cho bọn nó chỉ khiến bọn nó phản kháng mạnh hơn thôi...<br> ",
    "Thinking about it isn't getting me anywhere. I'm going out to get some<br>fresh air.<br> ": "Tưởng cũng chẳng ra gì. Ta ra ngoài hít chút không khí cho thoáng.<br> ",
    "A leader for that rowdy bunch of engineers, huh... What to do... Hmm?<br> ": "Cầm đầu đám kỹ sư man rợ ấy à... Làm sao cho ổn... Ủa?<br> ",
    "*sigh*... What should I do...<br> ": "*Thở dài*... Làm sao bây giờ...<br> ",
    "Betty, long time no see.<br> ": "Betty, lâu không gặp.<br> ",
    "Ah, Lord Commander...!?<br> ": "A, Chỉ Huy...!?<br> ",
    "To think you remembered my name, Lord Commander... I'm deeply<br>honored!<br> ": "Không ngờ Chỉ Huy nhớ tên em... Em xúc động lắm ạ!<br> ",
    "You're exaggerating. But anyway... Did something happen?<br> ": "Nói lớn thật. Thôi không nói nữa... Có chuyện gì à?<br> ",
    "You were sighing with a gloomy face, weren't you?<br> ": "Người ta đang thở dài mặt mũi chán nản mà.<br> ",
    "...Haha, you caught me. That's the Lord Commander for you.<br> ": "...Haha, bị bắt quả tang. Thiệt là Chỉ Huy ạ.<br> ",
    "Actually... I was assigned to a monster-hunting squad, but I froze up<br>in a cave and caused trouble for my comrades.<br> ": "Thực ra... em được phân vào đội săn quái, nhưng trong hang động sợ tới mức đóng băng, làm phiền đồng đội...<br> ",
    "You froze? Were you injured?<br> ": "Đóng băng? Có bị thương không?<br> ",
    "Well, um... I'm not good with dark places. I got scared and couldn't<br>move.<br> ": "Đó, ừm... em sợ chỗ tối. Sợ nên không nhúc nhích được.<br> ",
    "That's tough... If so, why not request a transfer?<br> ": "Khó xử nhỉ... Thế thì xin điều động đi.<br> ",
    "That's why I had myself reassigned as a quartermaster. I thought that<br>as a quartermaster handling supplies and cooking, I could be of use.<br> ": "Đó là em xin điều động làm Binh Quân Nhu. Em nghĩ Binh Quân Nhu lo vật tư nấu ăn thì có ích.<br> ",
    "But even there, I failed...<br> ": "Nhưng ngay đó cũng thất bại...<br> ",
    "What, you're bad at cooking?<br> ": "Cái gì, nấu ăn dở à?<br> ",
    "No, cooking is actually my strong suit. But...<br> ": "Không, nấu ăn là điểm mạnh của em. Nhưng...<br> ",
    "I served a full-course meal, and they got angry, saying, 'Who's got<br>the leisure to eat something like this on the battlefield!'<br> ": "Em trình bày món ăn đầy đủ, bọn nó giận: 'Ai có rảnh ăn mấy thứ này trên chiến trường!'<br> ",
    "A f-full-course meal?<br> ": "M-món ăn đầy đủ?<br> ",
    "I thought a tasty meal would cheer them up, but it backfired.<br> ": "Em nghĩ ăn ngon cho vui, thế mà lỡ làm hại.<br> ",
    "After a string of such failures, I was eventually told I was a failure as<br>a soldier, and they stopped giving me any tasks...<br> ": "Lỗi lầm liên tục, cuối cùng bị nói là binh sĩ thất bại, không giao việc gì nữa...<br> ",
    "A useless soldier like me earning merits? A pipe dream. How can I<br>write home? *sigh*...<br> ": "Binh sĩ vô dụng như em dựng công? Mộng tưởng. Viết thư về nhà sao? *Thở dài*...<br> ",
    "(She's really down... Huh?)<br> ": "(Cô ấy chán nản lắm... Ủa?)<br> ",
    "She scrubbed at the stone.<br> ": "Cô ấy chà xát viên đá.<br> ",
    "Betty, what have you been doing?<br> ": "Betty, ngươi đang làm gì vậy?<br> ",
    "Ah, sorry, it's a habit... I was polishing this.<br> ": "A, lỡ, thói quen thôi... Em đang mài cái này.<br> ",
    "This... is a stone? Why would you do that?<br> ": "Cái này... là đá? Tại sao làm vậy?<br> ",
    "It's my hobby!<br> ": "Sở thích của em!<br> ",
    "Polishing stones?<br> ": "Mài đá?<br> ",
    "Yes!<br> ": "Vâng!<br> ",
    "The stone sparkled.<br> ": "Viên đá lấp lánh.<br> ",
    "Huh? That stone, it's shining awfully bright, isn't it?<br> ": "Ủa? Viên đá đó, chẳng lẽ sáng lắm à?<br> ",
    "Eheh! That's right.<br> ": "Ê hê! Đúng rồi.<br> ",
    "Even a dull pebble buried in the earth for years can shine like a<br>beautiful gem if you polish it carefully and patiently!<br> ": "Viên sỏi nhòe chôn dưới đất nhiều năm, mài kỹ kiên nhẫn cũng sáng đẹp như ngọc báu!<br> ",
    "Speaking of stones, I'm sure there are all sorts of stones in the<br>Abyss that you can't find on the surface!<br> ": "Nói đến đá, chắc trong Đại Huyệt có đủ loại đá mặt đất không thấy!<br> ",
    "Yeah. I wonder what kind of stones are in the Abyss...<br> ": "Ừ. Đại Huyệt có đá gì nhỉ...<br> ",
    "............<br> ": "............<br> ",
    "W-wah!? I-I'm sorry, I got carried away all by myself! In front of the<br>Lord Commander...<br> ": "Ủa wa!? L-lỗi, em tựSay một mình! Trước mặt Chỉ Huy...<br> ",
    "No, it's fine. Having something you can get so into is a good thing.<br> ": "Không, ổn thôi. Có thứ gì đó để say mê là tốt.<br> ",
    "So you know all about stones, then?<br> ": "Vậy ngươi am hiểu đá hết à?<br> ",
    "Of course! But a hobby like this is completely useless on the<br>battlefield...<br> ": "Tất nhiên! Nhưng sở thích này trên chiến trường hoàn toàn vô dụng...<br> ",
    "...Betty.<br> ": "...Betty.<br> ",
    "R-right, I can't be moping around! I have to work hard again<br>starting tomorrow!<br> ": "Đ-đúng, không thể chán nản! Ngày mai phải nỗ lực lại!<br> ",
    "Are you sure you're okay?<br> ": "Ngươi chắc chắn ổn à?<br> ",
    "Of course! Enthusiasm is the only thing I have going for me! So you<br>too must keep smiling and fight on!<br> ": "Tất nhiên! Chỉ có nhiệt huyết là của em! Vậy Chỉ Huy cũng phải nở nụ cười mà chiến đấu!<br> ",
    "Heh. Yeah, I guess so.<br> ": "Hê. Ừ, thôi được.<br> ",
    "Well then, I shall take my leave!<br> ": "Vậy em xin phép lui!<br> ",
    "...Hold on a second.<br> ": "...Chờ đã.<br> ",
    "Betty, would you come with me for a bit?<br> ": "Betty, ngươi theo ta một chút được không?<br> ",
    "...?<br> ": "...?<br> ",
}

# Also need reverse lookup by ja key for title
JA_TO_VI = {
    "くすんだ石ころ": "Viên Đá Nhòe",
    "コンコン――": "Có tiếng gõ cửa.",
    "入っていいぞ。": "Vào đi.",
    "はい！　失礼するであります！": "Vâng! Phiền rắc chút ạ!",
    "お前が今日着任した志願兵か。": "Ngươi là tân binh vừa đến hôm nay à.",
    "はいっ！　<br>ミレスガルド出身のベティであります！": "Vâng! Em là Betty từ Milesgard ạ!",
    "はは、元気なやつだな。<br>前線基地への配属を希望しているみたいだが、どうしてだ？": "Haha, nhỏ này nhiệt tình đấy. Nghe nói ngươi xin về Căn Cứ Tiền Tuyến, tại sao vậy?",
    "はい！　わたしの実家は代々騎士の家柄で<br>幼いころより父や兄の戦場での活躍を目の当たりにしてきたであります！": "Vâng! Gia gia em đời đời quân nhân, từ nhỏ em đã chứng kiến cha anh em anh oai phong trên chiến trường!",
    "だからわたしも父や兄のような<br>立派な兵士になって活躍するのが目標なのであります！": "Vì thế mục tiêu của em là trở thành binh sĩ xuất sắc như cha anh, để tên tuổi em được biết đến!",
    "なるほど。家族にもさぞかし期待されているんだろうな。": "Thôi hiểu. Gia đình chắc mong to lớn ở em lắm.",
    "え？　そ、それはそのぅ……": "Ủa? Thì th-thì là ừm...",
    "なんだ？": "Sự việc thế nào?",
    "実は家族からは、兵士になることを反対されておりまして……": "Thực ra... gia đình em phản đối em làm binh sĩ...",
    "ほう。なぜだ？": "Ồ? Tại sao vậy?",
    "わたしのような小柄な女性に<br>危険な戦場の任務など務まるはずはないと……": "Bọn họ nói con gái nhỏ nhạy như em không thể gánh nổi nhiệm vụ chiến trường nguy hiểm...",
    "……なるほどな。だったらここに来たのは正解だな。": "...Hiểu rồi. Đến đây là đúng chỗ.",
    "え？": "Ủa?",
    "ここは戦場の最前線。手柄を取るチャンスはそこかしこに転がっている。<br>ここで手柄をあげて家族に自分が兵士に相応しいと認めさせてやるといい。": "Đây là tiền tuyến. Cơ hội dựng công khắp nơi. Làm công đến đây để gia đình thấy em xứng đáng làm binh sĩ.",
    "はっ、はいっ！　きっと司令官殿のご期待に応えてみせるであります！<br>それでは、失礼するであります！": "Vâng, ạ! Em chắc chắn sẽ đáp ứng kỳ vọng của Chỉ Huy! Em xin phép lui!",
    "とても元気で、いい子ですね。": "Cô ấy rất hăng hái, lại còn là cô gái tốt.",
    "ああ。ああいうやつがいると、場の空気がよくなる。": "Ừ. Có người như thế không khí nơi đây dễ chịu hơn.",
    "活躍できるといいですね。": "Hy vọng cô ấy làm tốt!",
    "そうだな。": "Ừ.",
    "<size=48>――数か月後</size>": "<size=48>—Vài Tháng Sau</size>",
    "……というわけで、大穴内の掘削作業は現在、難航しております。<br>専門技術を持った工兵隊には期待していたのですが……": "Vậy thì... khai quật trong Đại Huyệt đang gặp khó khăn. Đội Kỹ Sư chuyên môn ta kỳ vọng cao nhưng...",
    "蓋を開けてみれば、誰が隊長として現場を取り仕切るかで揉めてばかりで<br>仕事がろくに進まない状態です。": "Mở ra xem thì toàn tranh giành ai làm đội trưởng dẫn việc, công việc không tiến được chút nào.",
    "……認めた相手の言うことしか聞かないってところか。<br>職人気質な連中ってのは、こういう時厄介だな。": "Chỉ nghe người mình công nhận thôi. Nhóm thủ công kiểu này lúc khó xử lắm.",
    "隊長か……いっそ、俺が指名してしまうか？<br>いや、頭ごなしの行動をとればやつらはより反発するだけだな……": "Đội trưởng à... có nên ta chỉ định luôn không? Không, đập đầu cho bọn nó chỉ khiến bọn nó phản kháng mạnh hơn thôi...",
    "……考えてもらちが明かないな。<br>ちょっと外の空気を吸ってくる。": "Tưởng cũng chẳng ra gì. Ta ra ngoài hít chút không khí cho thoáng.",
    "荒くれ者揃いの工兵隊のまとめ役、か……<br>どうしたものか……　ん？": "Cầm đầu đám kỹ sư man rợ ấy à... Làm sao cho ổn... Ủa?",
    "はぁ……<br>どうしたらいいんだろう……": "*Thở dài*... Làm sao bây giờ...",
    "ベティ、久しぶりだな。": "Betty, lâu không gặp.",
    "あ、司令官殿……！？": "A, Chỉ Huy...!?",
    "まさか司令官殿に名前を憶えていてもらえたなんて……！<br>感激であります！": "Không ngờ Chỉ Huy nhớ tên em... Em xúc động lắm ạ!",
    "大げさだな。<br>それはそうと……なにかあったのか？": "Nói lớn thật. Thôi không nói nữa... Có chuyện gì à?",
    "浮かない顔でため息ついてたろ？": "Người ta đang thở dài mặt mũi chán nản mà.",
    "……はは。バレちゃいましたか。<br>さすがは司令官殿であります。": "...Haha, bị bắt quả tang. Thiệt là Chỉ Huy ạ.",
    "実は……モンスターを討伐する部隊に配属されたでありますが<br>洞窟の中で動けなくなって、仲間に迷惑をかけてしまいまして……": "Thực ra... em được phân vào đội săn quái, nhưng trong hang động sợ tới mức đóng băng, làm phiền đồng đội...",
    "動けなくなった？　ケガでもしたのか？": "Đóng băng? Có bị thương không?",
    "それが、そのぅ……わたし、暗い場所が苦手でして。<br>怖くて動けなくなってしまったのであります。": "Đó, ừm... em sợ chỗ tối. Sợ nên không nhúc nhích được.",
    "それは難儀だな……<br>だったら配置転換を願い出ればどうだ？": "Khó xử nhỉ... Thế thì xin điều động đi.",
    "そう思って、主計兵に配置換えしてもらったであります。<br>消耗品の管理や調理を担当する主計兵なら、お役に立てると思いまして。": "Đó là em xin điều động làm Binh Quân Nhu. Em nghĩ Binh Quân Nhu lo vật tư nấu ăn thì có ích.",
    "ですが、そこでも失敗を……": "Nhưng ngay đó cũng thất bại...",
    "なんだ、料理が苦手なのか？": "Cái gì, nấu ăn dở à?",
    "いえ、料理はむしろ得意であります。<br>ですが……": "Không, nấu ăn là điểm mạnh của em. Nhưng...",
    "コース料理を振る舞ってしまい<br>戦場でこんなもの呑気に食べてられるか！　と怒られまして……": "Em trình bày món ăn đầy đủ, bọn nó giận: 'Ai có rảnh ăn mấy thứ này trên chiến trường!'",
    "コ、コース料理？": "M-món ăn đầy đủ?",
    "おいしい食事で元気になってもらおうと思ったのが<br>仇となったであります。": "Em nghĩ ăn ngon cho vui, thế mà lỡ làm hại.",
    "そんなことが度々あった末に、ついには兵士失格だと言われ、<br>仕事を任せてもらえなくなったであります……": "Lỗi lầm liên tục, cuối cùng bị nói là binh sĩ thất bại, không giao việc gì nữa...",
    "こんなダメダメ兵士、手柄を立てるなんて夢のまた夢であります。<br>故郷の両親に手紙でどう報告すれば……。はぁ……": "Binh sĩ vô dụng như em dựng công? Mộng tưởng. Viết thư về nhà sao? *Thở dài*...",
    "（これはかなり参ってるな。……ん？）": "(Cô ấy chán nản lắm... Ủa?)",
    "ゴシゴシ……": "Cô ấy chà xát viên đá.",
    "ベティ。さっきから何をしているんだ？": "Betty, ngươi đang làm gì vậy?",
    "ああ、すみません、つい癖で……。<br>これを磨いていたであります。": "A, lỡ, thói quen thôi... Em đang mài cái này.",
    "これは……石か？<br>なんでそんなことを。": "Cái này... là đá? Tại sao làm vậy?",
    "わたしの趣味であります！": "Sở thích của em!",
    "石を磨くことがか？": "Mài đá?",
    "はい！": "Vâng!",
    "――キラッ": "Viên đá lấp lánh.",
    "ん？　その石、随分と光ってないか？": "Ủa? Viên đá đó, chẳng lẽ sáng lắm à?",
    "えへっ、そーなんです。": "Ê hê! Đúng rồi.",
    "長年、土に埋もれて一見、くすんだ石ころも<br>丁寧に根気よく磨いてあげると宝石みたいに綺麗に輝くのであります！": "Viên sỏi nhòe chôn dưới đất nhiều năm, mài kỹ kiên nhẫn cũng sáng đẹp như ngọc báu!",
    "石と言えば、大穴にはきっと、<br>地上では見られない色々な石があると思うのです！": "Nói đến đá, chắc trong Đại Huyệt có đủ loại đá mặt đất không thấy!",
    "ああ。大穴には一体どんな石があるんだろう……": "Ừ. Đại Huyệt có đá gì nhỉ...",
    "…………": "............",
    "……わわっ！？　す、すみません、１人ではしゃいでしまって！<br>司令官殿を前にして、つい自分だけの世界に！": "Ủa wa!? L-lỗi, em tự Say một mình! Trước mặt Chỉ Huy...",
    "いや、構わないさ。<br>夢中になれるものがあるってのはいいことだ。": "Không, ổn thôi. Có thứ gì đó để say mê là tốt.",
    "石のことなら何でも詳しいのか？": "Vậy ngươi am hiểu đá hết à?",
    "もちろんであります！<br>ただこんな趣味、戦場では何の役にも立ちませんが……": "Tất nhiên! Nhưng sở thích này trên chiến trường hoàn toàn vô dụng...",
    "……ベティ。": "...Betty.",
    "って、くよくよなんかしていられませんよね！<br>明日から、また頑張らないと！": "Đ-đúng, không thể chán nản! Ngày mai phải nỗ lực lại!",
    "大丈夫なのか？": "Ngươi chắc chắn ổn à?",
    "もちろんであります！　元気だけがわたしの取柄でありますから！<br>司令官殿も笑顔でファイトでありますよ！": "Tất nhiên! Chỉ có nhiệt huyết là của em! Vậy Chỉ Huy cũng phải nở nụ cười mà chiến đấu!",
    "ふっ。そうだな。": "Hê. Ừ, thôi được.",
    "では、これで失礼します！": "Vậy em xin phép lui!",
    "……ちょっと待ってくれ。": "...Chờ đã.",
    "ベティ、ちょっと俺に付き合ってくれないか？": "Betty, ngươi theo ta một chút được không?",
    "？": "...?",
}


def build_vi():
    # Read EN asset
    en_path = 'E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt'
    with open(en_path, 'rb') as f:
        en_bytes = f.read()
    
    has_bom = en_bytes.startswith(b'\xef\xbb\xbf')
    text = en_bytes.decode('utf-8-sig')
    has_crlf = '\r\n' in text
    lines = text.splitlines(keepends=True)
    
    text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
    
    asset_texts = []
    for i, line in enumerate(lines):
        for cmd in text_cmds:
            if line.startswith(cmd):
                raw = line
                ending = ''
                if raw.endswith('\r\n'):
                    ending = '\r\n'
                    raw = raw[:-2]
                elif raw.endswith('\n'):
                    ending = '\n'
                    raw = raw[:-1]
                
                if cmd == 'title,':
                    parts = raw.split(',', 2)
                    en_text = parts[1] if len(parts) > 1 else ''
                    speaker = ''
                else:
                    parts = raw.split(',', 3)
                    en_text = parts[2] if len(parts) > 2 else ''
                    speaker = parts[1] if len(parts) > 1 else ''
                
                asset_texts.append({
                    'line_idx': i,
                    'cmd': cmd.rstrip(','),
                    'speaker': speaker,
                    'en_text': en_text,
                    'raw_line': line,
                    'ending': ending,
                    'parts': parts,
                })
                break
    
    print(f"Total text records: {len(asset_texts)}")
    for at in asset_texts:
        print(f"  Line {at['line_idx']+1}: {at['cmd']} | speaker={at['speaker']!r} | text={at['en_text'][:60]}...")
    
    # Build VI output
    vi_lines = lines[:]
    translated = 0
    
    for at in asset_texts:
        en_text = at['en_text']
        cmd = at['cmd']
        
        # Look up translation
        vi_text = None
        if en_text in VI:
            vi_text = VI[en_text]
        elif en_text.endswith('<br> ') and en_text[:-5] in VI:
            vi_text = VI[en_text[:-5]]
            if not vi_text.endswith('<br> '):
                vi_text = vi_text.rstrip() + '<br> '
        
        # For title, also check JA_TO_VI via en.json -> ja.json reverse mapping
        if vi_text is None and cmd == 'title':
            # en.json has empty value for title, need to translate from JA
            # The EN asset title field contains the JP text
            if en_text in JA_TO_VI:
                vi_text = JA_TO_VI[en_text]
        
        if vi_text is None:
            print(f"WARNING: No translation for line {at['line_idx']+1}: {en_text[:80]}")
            vi_text = en_text  # fallback
        else:
            translated += 1
        
        # Replace ASCII commas in VI text with U+201A
        vi_text_fixed = vi_text.replace(',', '\u201a')
        
        # Rebuild line
        raw = at['raw_line'].rstrip('\r\n')
        if cmd == 'title':
            parts = raw.split(',', 2)
            parts[1] = vi_text_fixed
            new_raw = ','.join(parts)
        else:
            parts = raw.split(',', 3)
            parts[2] = vi_text_fixed
            new_raw = ','.join(parts)
        
        vi_lines[at['line_idx']] = new_raw + at['ending']
    
    print(f"\nTranslated {translated}/{len(asset_texts)} records")
    assert translated == len(asset_texts), f"Only {translated}/{len(asset_texts)} translated"
    
    # Write VI output
    vi_path = 'E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt'
    output_text = ''.join(vi_lines)
    output_bytes = output_text.encode('utf-8')
    if has_bom:
        output_bytes = b'\xef\xbb\xbf' + output_bytes
    
    os.makedirs(os.path.dirname(vi_path), exist_ok=True)
    with open(vi_path, 'wb') as f:
        f.write(output_bytes)
    
    print(f"Written VI: {vi_path}")
    print(f"BOM: {has_bom}, CRLF: {has_crlf}, Lines: {len(vi_lines)}")
    assert len(vi_lines) == len(lines), "Line count mismatch!"
    
    # Write work copy
    work_dir = 'E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100001_full'
    os.makedirs(work_dir, exist_ok=True)
    work_vi = os.path.join(work_dir, 'hmn_10500100001_vi.txt')
    with open(work_vi, 'wb') as f:
        f.write(output_bytes)
    
    # Generate focused diff
    diff_path = os.path.join(work_dir, 'focused_diff.md')
    with open(diff_path, 'w', encoding='utf-8') as f:
        f.write("# Focused Diff: hmn_10500100001\n\n")
        f.write("| Line | Command | Speaker | EN Text | VI Text |\n")
        f.write("|------|---------|---------|---------|--------|\n")
        for at in asset_texts:
            line_no = at['line_idx'] + 1
            en = at['en_text'].replace('\n', '\\n').replace('|', '\\|')
            vi = VI.get(at['en_text'], JA_TO_VI.get(at['en_text'], '')).replace('\n', '\\n').replace('|', '\\|')
            f.write(f"| {line_no} | {at['cmd']} | {at['speaker']} | {en[:60]} | {vi[:60]} |\n")
    print(f"Focused diff: {diff_path}")
    
    # Generate manifest
    manifest = {
        "scene": "hmn_10500100001",
        "total_lines": len(lines),
        "text_records": len(asset_texts),
        "translated_records": translated,
        "title_cmd": sum(1 for a in asset_texts if a['cmd'] == 'title'),
        "message_cmd": sum(1 for a in asset_texts if a['cmd'] == 'message'),
        "messageTextCenter_cmd": sum(1 for a in asset_texts if a['cmd'] == 'messageTextCenter'),
        "messageTextUnder_cmd": sum(1 for a in asset_texts if a['cmd'] == 'messageTextUnder'),
        "bom_preserved": has_bom,
        "crlf_preserved": has_crlf,
        "encoding": "utf-8-sig",
        "delimiter": ",",
        "comma_replacement": "U+201A",
        "source_type": "EN-asset-is-English",
        "notes": "Title field JP->VI Title Case. messageTextCenter Title Case. EN->VI for messages. Speaker labels (field 1) kept JP verbatim. All 6 fields preserved. <br> suffix mirrored on message fields.",
    }
    manifest_path = os.path.join(work_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Manifest: {manifest_path}")
    
    # Generate QA log (pre-verification)
    qa_log = {
        "scene": "hmn_10500100001",
        "total_text_records": len(asset_texts),
        "translated_records": translated,
        "preflight_checks": {
            "line_count_match": len(vi_lines) == len(lines),
            "bom_preserved": has_bom,
            "crlf_preserved": has_crlf,
            "all_records_translated": translated == len(asset_texts),
        },
        "independent_verify": "PENDING",
    }
    qa_path = os.path.join(work_dir, 'qa_log.json')
    with open(qa_path, 'w', encoding='utf-8') as f:
        json.dump(qa_log, f, ensure_ascii=False, indent=2)
    print(f"QA log: {qa_path}")


if __name__ == "__main__":
    build_vi()
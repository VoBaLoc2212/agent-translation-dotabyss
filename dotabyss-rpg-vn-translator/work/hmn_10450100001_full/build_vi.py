#!/usr/bin/env python
"""Build VI output for hmn_10450100001 (Iola first meeting) — v2 fixed <br> and commas."""
import json, re
from pathlib import Path

EN_PATH = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100001.txt")
VI_PATH = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100001.txt")
WORK = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10450100001_full")

# ── Translation dict keyed by text-record sequence (1‑based) ──
# Use <br> for internal line breaks. Use U+201A ‚ for commas inside VI text.

VI = {}

# Record 1 (L17): title
VI[1] = ("title", "Pháp Sư Dễ Thương Nên Được Yêu Thích")

# Record 2 (L25): EN: Phew... I've finished reading that book. I really should get to work<br>now.
# JP: ふぅ……本を読み終えてしまったか。<br>いい加減、そろそろ仕事をしないとなぁ。
VI[2] = ("message", "Phù… cuối cùng cũng đọc xong cuốn sách đó rồi.<br>Cũng đến lúc phải làm việc thôi.")
# br count: EN=2, VI=2 ✓

# Record 3 (L27): EN: If I don't do it properly，Alicia will complain again. Time to turn<br>things around—focus!
# JP: ちゃんとやっておかないと、またアリシアに文句を言われてしまう。<br>ここから挽回するぞ、集中だ！
VI[3] = ("message", "Nếu không làm xong việc tử tế thì lại bị Alicia cằn nhằn mất.<br>Phải lấy lại tinh thần—tập trung nào!")
# br count: EN=2, VI=2 ✓

# Record 4 (L31): EN: *knock，knock*.
# JP: ――コンコン。
VI[4] = ("message", "*cốc‚ cốc*.")
# ASCII comma fix: use ‚

# Record 5 (L39): EN: A knock? Tch... just when I finally got focused... Come in.
# JP: ノック？　ぐっ……せっかく集中したところだったのに……。<br>入っていいぞ。
VI[5] = ("message", "Có tiếng gõ cửa? Chậc… đang lúc tập trung nhất thì…. Vào đi.")
# br: EN=2, VI=2 ✓

# Record 6 (L78): EN: Excuse me! Ah! You're the Commander，right?
# JP: お邪魔しまーす。<br>あ！　あんたが司令官よね？
VI[6] = ("message", "Xin lỗi nha! A! Cậu là Chỉ Huy phải không?")
# br: EN=2, VI=2 ✓

# Record 7 (L80): EN: ...!
# JP: ！？
VI[7] = ("message", "…!")
# br: EN=1 ✓

# Record 8 (L122): EN: Nice to meet you! I'm Iola，from the Perdion Magic Academy!
# JP: はっじめまして～！<br>あたし、ペルディオンの魔法学校から来たイオラよ！　
VI[8] = ("message", "Rất vui được gặp anh! Em là Iola‚ đến từ Học Viện Pháp Thuật Perdion!")
# br: EN=2 ✓

# Record 9 (L124): EN: Huh? Magic Academy? You don't look like a teacher—are you a<br>student?
# JP: んんっ？　魔法学校？<br>教員には見えないな――学生か？
VI[9] = ("message", "Hử? Học Viện Pháp Thuật?<br>Trông không giống giáo viên nhỉ—em là học sinh à?")
# br: EN=2 ✓

# Record 10 (L136): EN: Yep，that's right! As you can see，I'm a beautiful magical girl!
# JP: うん、そうそう。見ての通り、美少女魔法使いなのっ！
VI[10] = ("message", "Ừm‚ đúng vậy! Như anh thấy đấy‚ em là một mỹ nữ pháp sư!")
# br: EN=1 ✓

# Record 11 (L151): EN: (Did she just say that about herself?)
# JP: （……自分で言うか？）
VI[11] = ("message", "(Tự nói về mình luôn hả cô nàng?)")
# br: EN=1 ✓

# Record 12 (L175): EN: Oh my，have I already stunned you?
# JP: あらあら、見惚れちゃった？
VI[12] = ("message", "Ôi chà‚ anh đã bị em làm cho mê mẩn rồi à?")
# br: EN=1 ✓

# Record 13 (L177): EN: Well... something like that. So，what does a lovely magical girl want<br>with me?
# JP: ん……まぁ……そんなところだ……。<br>それで、可憐な美少女魔法使いが俺に何の用事だ？
VI[13] = ("message", "Ừm… cũng gần như vậy đó…<br>Vậy‚ một mỹ nữ pháp sư khả ái tìm tôi có việc gì?")
# br: EN=2 ✓

# Record 14 (L188): EN: Huh? Didn't they tell you? I asked them to make you my temporary<br>instructor.
# JP: えっ？　連絡、行ってないです？<br>臨時であんたに教官をやってもらうよう、お願いしたはずなんだけど？
VI[14] = ("message", "Hả? Họ chưa báo cho anh à?<br>Em đã nhờ họ sắp xếp để anh làm gia sư tạm thời cho em mà?")
# br: EN=2 ✓

# Record 15 (L190): EN: What? Instructor? The Commander，me? I don't recall any such<br>message—
# JP: は？　教員？　司令官の俺が？<br>そんな連絡は来た覚えが――
VI[15] = ("message", "Hả? Gia sư? Tôi—Chỉ Huy á?<br>Tôi chẳng nhận được tin báo nào cả—")
# br: EN=2 ✓

# Record 16 (L205): EN: (Oh，wait. Now that I think about it，I did get some mail from the<br>school the other day. I just left it unread... Could that be...?)
# JP: （あ、いや待てよ？　そういえばこの間、学校から郵便がきていたな。<br>見ないで放置していたが、あれがもしかして……！？）
VI[16] = ("message", "(À‚ khoan đã nào? Nghĩ lại thì hôm trước có thư từ trường gửi đến.<br>Chưa đọc vứt đấy‚ chẳng lẽ…!?)")
# br: EN=2 ✓

# Record 17 (L230): EN: Looks like you have an idea，Teacher!
# JP: その様子だと、心当たりがありそうだね先生！
VI[17] = ("message", "Nhìn mặt là biết anh có linh cảm rồi đúng không‚ Thầy!")
# br: EN=1 ✓

# Record 18 (L232): EN: Well，that's true... but you're already treating me like your teacher! I<br>haven't even agreed to it yet—
# JP: たしかにそうなんだが……もう生徒気分か！？<br>まだやると返事をしたわけじゃ――
VI[18] = ("message", "Đúng là vậy thật… nhưng em đã xem tôi như thầy rồi à!?<br>Tôi có nói là nhận lời đâu—")
# br: EN=2 ✓

# Record 19 (L243): EN: Ehh! I'll be in trouble if you don't!
# JP: えーっ！？　やってもらわないと困るよぉ！
VI[19] = ("message", "Ớ—!? Không nhận thì em khổ lắm!")
# br: EN=1 ✓

# Record 20 (L254): EN: If I don't pass here and get my credits，I'm gonna flunk out!
# JP: ここで合格して単位もらわないと、あたし落第になっちゃう！
VI[20] = ("message", "Nếu không qua được đây để lấy tín chỉ‚ em sẽ bị đúp mất!")
# br: EN=1 ✓

# Record 21 (L256): EN: Huh? Wait，are your grades really that bad?
# JP: んっ？　なんだお前、ひょっとして成績が悪いのか？
VI[21] = ("message", "Hử? Khoan đã‚ thành tích của em tệ tới vậy sao?")
# br: EN=1 ✓

# Record 22 (L267): EN: I-It was just a fluke! I do have talent，you know.
# JP: た、たまたまだよ！　素質はあるんだから！
VI[22] = ("message", "Đ—đó chỉ là tình cờ thôi! Em có tài năng mà‚ anh biết không!")
# br: EN=1 ✓

# Record 23 (L274): EN: The school promised to give me credit as independent research if I<br>turn in a report on the Abyss exploration at the Frontline Base.
# JP: 前線基地で行われている大穴探索の様子をレポートにして出せば、<br>自由研究として単位をくれるって学校が約束してくれてるの。
VI[23] = ("message", "Nhà trường hứa sẽ cho em tín chỉ nghiên cứu độc lập<br>nếu em nộp báo cáo về cuộc thám hiểm Đại Huyệt tại Căn Cứ Tiền Tuyến.")
# br: EN=2 ✓

# Record 24 (L291): EN: Please，think of it as helping a cute student with a future，Teacher!
# JP: 未来ある可愛い学生を助けると思って、お願い！<br>先生っ！！
VI[24] = ("message", "Hãy coi như giúp một học sinh dễ thương có tương lai đi‚ em xin anh! Thầy ơi!!")
# br: EN=2 ✓

# Record 25 (L293): EN: Seriously? I'm busy with work，you know...
# JP: マジか……仕事で忙しいんだがなぁ。
VI[25] = ("message", "Thật à… tôi bận công việc lắm đây này…")
# br: EN=1 ✓

# Record 26 (L304): EN: And yet，there's a porno mag lying on your desk，isn't there?
# JP: その割には、机の上にエロ本が転がってますけど？
VI[26] = ("message", "Vậy mà trên bàn anh lại có tạp chí khiêu dâm đấy nhỉ?")
# br: EN=1 ✓

# Record 27 (L306): EN: ...This，too，is a valuable social education.
# JP: ……これも立派な社会勉強だ。
VI[27] = ("message", "…Cái này cũng là một phần giáo dục xã hội quý báu đấy.")
# br: EN=1 ✓

# Record 28 (L324): EN: Anyway，the magic school people are wrong to think the Frontline<br>Base is for education. Come with that attitude and you'll get hurt.
# JP: それはさておき、魔法学校の連中は前線基地を教育の場だと<br>勘違いしているようだが、そんな心構えでいられると大怪我をする。
VI[28] = ("message", "Dù sao thì‚ mấy người trường pháp thuật dường như lầm tưởng<br>Căn Cứ Tiền Tuyến là chỗ để giáo dục rồi. Có thái độ đó sẽ bị thương đấy.")
# br: EN=2 ✓

# Record 29 (L326): EN: First，let me see what you've got! Show me what kind of magic you<br>can do.
# JP: まずはお前の実力を見せてもらおう！<br>どんな魔法を使えるのか、やってみてくれっ！
VI[29] = ("message", "Trước hết‚ cho tôi xem thực lực của em nào!<br>Cho xem em dùng được loại pháp thuật gì đi!")
# br: EN=2 ✓

# Record 30 (L351): EN: O-okay... Alright，first the basics—I'll do a light spell for the Abyss...<br>mutter，mutter，mutter...
# JP: お、おっけ～……じゃあ、まずは基礎を――大穴探索で役立ちそうな、<br>小さな明かりを出す魔法をやるわね……ぶつぶつぶつぶつ――
VI[30] = ("message", "Ổ—ổn thôi… vậy trước hết là cơ bản—<br>Em sẽ làm phép tạo ánh sáng hỗ trợ thám hiểm Đại Huyệt… lẩm bẩm lẩm bẩm—")
# br: EN=2 ✓

# Record 31 (L355): EN: Iola chanted the spell，concentrating，but her hands trembled and she<br>seemed unsettled.
# JP: イオラは呪文を唱えながら意識を高めていく。<br>だが、手先は震えて、どこか落ち着きがない。
VI[31] = ("message", "Iola vừa đọc thần chú vừa tập trung tinh thần.<br>Nhưng tay cô ấy run rẩy‚ trông có vẻ bất an.")
# br: EN=2 ✓

# Record 32 (L368): EN: Come forth，orb of light，Hyaaah!
# JP: いでよ！　光の玉！　でやぁぁぁっ！
VI[32] = ("message", "Hiện ra đi! Cầu ánh sáng! Dụy—yaaaaa!")
# br: EN=1 ✓

# Record 33 (L386): EN: A blinding flash of light and a loud whoosh erupted.
# JP: ――バシュウウウッ！
VI[33] = ("message", "——VÚÙÙÙ UỒ!")
# br: EN=1 ✓

# Record 34 (L397): EN: Gwaaaah，my eyes，my eyes!
# JP: ぐわあああっ！？<br>目がっ！？　目がぁぁあっ！？
VI[34] = ("message", "GỤ—AA—A!? Mắt!? Mắt tao!?")
# br: EN=2 ✓

# Record 35 (L399): EN: A light burst in front of %user% and he covered his face and rolled<br>on the floor after looking directly at it.
# JP: 目前で光が弾けた。光を直視した<user>が<br>顔を押さえて床を転がり回る。
VI[35] = ("message", "Ánh sáng bùng nổ ngay trước mặt %user%.<br>Nhìn thẳng vào nó‚ anh che mặt và lăn lộn dưới sàn.")
# br: EN=2 ✓

# Record 36 (L410): EN: ...W-well，something like that?
# JP: ……ま、まぁ、こんな感じ？
VI[36] = ("message", "…Ch—chắc là cỡ đó?")
# br: EN=1 ✓

# Record 37 (L412): EN: That's completely different from what I asked for—that's a flash<br>bang!
# JP: 用途が全然違うだろう！<br>これじゃあ目くらましだ！
VI[37] = ("message", "Công dụng hoàn toàn khác rồi!<br>Đây là làm chói mắt mà!")
# br: EN=2 ✓

# Record 38 (L423): EN: S-sorry...
# JP: ご、ごめ～ん……
VI[38] = ("message", "X—xin lỗi nha…")
# br: EN=1 ✓

# Record 39 (L425): EN: Iola. You're about to flunk out，and for a magic school student，<br>you're not exactly great at magic，are you?
# JP: イオラ。お前、落第寸前だけあって、魔法学校の生徒のくせに<br>魔法の扱いが得意じゃなかったりする？
VI[39] = ("message", "Iola. Em sắp bị đúp‚ nhưng là học sinh trường pháp thuật<br>mà lại không giỏi pháp thuật cho lắm hả?")
# br: EN=2 ✓

# Record 40 (L436): EN: Gah!
# JP: ギクッ！
VI[40] = ("message", "Quắ—\"c!")
# br: EN=1 ✓

# Record 41 (L438): EN: Hmm，as I thought.
# JP: うーむ、やっぱりか。
VI[41] = ("message", "Hừm‚ đúng như tôi nghĩ.")
# br: EN=1 ✓

# Record 42 (L440): EN: Maybe unsolicited，but try focusing more. Compared to magic users，<br>your form feels off.
# JP: 余計な助言かもしれないが、もう少し集中してみたらどうだ？<br>魔法を得意としている奴と比べて、詠唱中の動作に違和感があるぞ。
VI[42] = ("message", "Lời khuyên có thể thừa‚ nhưng thử tập trung hơn đi.<br>So với người dùng pháp thuật giỏi‚ động tác của em có gì đó sai sai.")
# br: EN=2 ✓

# Record 43 (L451): EN: If it was that easy，I wouldn't be struggling!
# JP: それが簡単にできたら苦労しないわよーっ！
VI[43] = ("message", "Nếu dễ vậy thì em đã không khổ sở thế này rồi!")
# br: EN=1 ✓

# Record 44 (L453): EN: Well，I guess that's true... If you could do it，you wouldn't be on the<br>verge of failing.
# JP: まぁ、それもそうか……<br>できてたら、落第寸前までいかないもんなぁ。
VI[44] = ("message", "Ừm… cũng đúng…<br>Nếu làm được thì em đã không suýt bị đúp rồi nhỉ.")
# br: EN=2 ✓

# Record 45 (L489): EN: Shut up，shut up，shut UP! Even if it's true，you don't have to make<br>fun of me that much! Stupid!
# JP: う、うるさいうるさいうるさーい！　いくら本当のことだからって<br>そこまでバカにしなくていいじゃないのよ！　バカーっ！
VI[45] = ("message", "Im đi im đi im đ—i! Dù đúng thật thì<br>anh cũng không cần chọc quê em tới mức đó chứ! Đồ ngốc!")
# br: EN=2 ✓

# Record 46 (L510): EN: Wham!
# JP: ――ボグゥッ！！！
VI[46] = ("message", "——BỤP!!!")
# br: EN=1 ✓

# Record 47 (L550): EN: Guhh!
# JP: ぐほおっ！？
VI[47] = ("message", "Gi—hự!?")
# br: EN=1 ✓

# Record 48 (L552): EN: Iola's punch cleanly hit the Commander in the temple.
# JP: イオラが放ったパンチが<br><user>のこめかみにクリーンヒットした。
VI[48] = ("message", "Cú đấm của Iola đáp gọn vào thái dương của Chỉ Huy.")
# br: EN=1 ✓  -- Note: EN has 1 <br> in "hit the Commander in the temple.<br> " but the JP has <br> inside. EN text is: "Iola's punch cleanly hit the Commander in the temple.<br> " so EN=1. 
# Wait let me recheck: L552: "message,,Iola's punch cleanly hit the Commander in the temple.<br> ". Only 1 <br>. Good.

# Record 49 (L554): EN: Gwaaaaah! My head，my heeead!
# JP: ぐあああっ！　頭が、頭がぁぁ～～～っ！？
VI[49] = ("message", "GỤ—AAAA! Đầu! Đầu tao…!")
# br: EN=1 ✓

# Record 50 (L588): EN: Kyaaah! I'm so sorry!
# JP: きゃああ～！？　ごめーんっ！！！
VI[50] = ("message", "Kyaaah! Em xin lỗi! Xin lỗi nha!!!")
# br: EN=1 ✓

# Record 51 (L612): EN: Ow，ow，ow... My vision is still swimming...?
# JP: いててて……まだ視界がグラついてるような――？
VI[51] = ("message", "Đau quá đau quá… Hình như thị giác vẫn còn lắc lư…?")
# br: EN=1 ✓

# Record 52 (L621): EN: I-I'm sorry... I didn't mean to hit you...
# JP: ご、ごめんっ……当てるつもりじゃなかったんだけど……
VI[52] = ("message", "X—xin lỗi… em không cố ý đánh trúng anh đâu…")
# br: EN=1 ✓

# Record 53 (L623): EN: For a mage，you sure have a powerful punch.
# JP: 魔法使いのくせに、ずいぶんパワフルなパンチを持っているな。
VI[53] = ("message", "Là pháp sư mà em có cú đấm mạnh thật đấy.")
# br: EN=1 ✓

# Record 54 (L634): EN: Ah! You finally praised me!
# JP: あっ。やっと褒めてくれたわね！
VI[54] = ("message", "A! Cuối cùng anh cũng khen em!")
# br: EN=1 ✓

# Record 55 (L652): EN: (Glare!)
# JP: （ギロッ！）
VI[55] = ("message", "(Lườm!)")
# br: EN=1 ✓

# Record 56 (L676): EN: Ah，sorry，sorry... I got carried away because I was so happy... Ehehe.
# JP: あ、ごめんごめん……嬉しかったから、ついつい……えへへ。
VI[56] = ("message", "A‚ xin lỗi xin lỗi… vui quá nên lỡ… ehehe.")
# br: EN=1 ✓

# Record 57 (L688): EN: Well，I deserve the praise. This punch is the result of my daily<br>training.
# JP: まぁ、称賛されて当然よ。<br>このパンチは日々の努力の成果なんだから。
VI[57] = ("message", "Ừm‚ em xứng đáng được khen mà.<br>Cú đấm này là thành quả luyện tập hằng ngày đấy.")
# br: EN=2 ✓

# Record 58 (L699): EN: My dad's a fighter，y'know. I started learning from him to lose<br>weight，but I got pretty good at it.
# JP: あたしのパパ、格闘家でね～。<br>ダイエット目的で教わっているうちに上達したってわけ♪
VI[58] = ("message", "Ba em là võ sĩ đó.<br>Học để giảm cân mà không ngờ lại trở nên cừ khôi luôn♪")
# br: EN=2 ✓

# Record 59 (L711): EN: Thanks to that，I can throw a punch that even pro fighters<br>acknowledge! They say it's on par with a champion! Pretty amazing，right?
# JP: おかげでプロの格闘家も認めるパンチを打てるようになったわ！<br>チャンピオン並みだって！　すごいでしょ～？
VI[59] = ("message", "Nhờ vậy em đấm ra cú mà võ sĩ chuyên nghiệp cũng phải công nhận!<br>Bảo em ngang ngửa nhà vô địch đấy! Tuyệt không?")
# br: EN=2 ✓

# Record 60 (L713): EN: From dieting to champion-level... W-well，it truly is impressive.
# JP: ダイエット目的が、チャンピオン並みに……。<br>た、確かにすごいな。
VI[60] = ("message", "Từ giảm cân lên tới trình nhà vô địch…. Đ—đúng là ấn tượng thật.")
# br: EN=2 ✓

# Record 61 (L724): EN: See，see!
# JP: でしょでしょー！
VI[61] = ("message", "Thấy chưa‚ thấy chưa!")
# br: EN=1 ✓

# Record 62 (L726): EN: If only you had as much talent for magic...
# JP: 魔法も同じくらい才能があれば……
VI[62] = ("message", "Giá mà em có tài cho pháp thuật ngang thế…")
# br: EN=1 ✓

# Record 63 (L737): EN: Ugh，that's the worst. Can you really say that?
# JP: うーわ、最悪。<br>そういうこと言っちゃう？
VI[63] = ("message", "Ờ—dô‚ tệ nhất luôn. Anh nói vậy được hả?")
# br: EN=2 ✓

# Record 64 (L739): EN: Didn't you ever think of giving up being a mage and becoming a<br>fighter? You'd probably go further that way.
# JP: 魔法使いをやめて、格闘家になろうとは思わなかったのか？　<br>そっちのほうが大成しそうだが。
VI[64] = ("message", "Em chưa từng nghĩ từ bỏ pháp sư để thành võ sĩ à?<br>Chắc bên đó phát triển hơn đấy.")
# br: EN=2 ✓

# Record 65 (L750): EN: No way!
# JP: 嫌よ！
VI[65] = ("message", "Không đời nào!")
# br: EN=1 ✓

# Record 66 (L752): EN: Huh? Why not?
# JP: んっ？　なんでだ？
VI[66] = ("message", "Hử? Sao lại không?")
# br: EN=1 ✓

# Record 67 (L763): EN: Because being a mage is cuter and more popular.
# JP: 魔法使いのほうが可愛くてモテるから。
VI[67] = ("message", "Vì làm pháp sư thì vừa dễ thương vừa được yêu thích hơn.")
# br: EN=1 ✓

# Record 68 (L765): EN: Uh，right...
# JP: お、おう……
VI[68] = ("message", "Ờ—ờ… phải ha…")
# br: EN=1 ✓

# Record 69 (L776): EN: I hold back from martial arts because it builds muscle and makes me<br>look bulky.
# JP: 格闘技は筋肉がついて体が太くなりそうで<br>控えてるのよねぇ。
VI[69] = ("message", "Em không theo võ thuật vì tập vào sẽ nở cơ và người trông thô kệch mất.")
# br: EN=1 ✓  -- Wait, EN has: "I hold back from martial arts because it builds muscle and makes me<br>look bulky.<br> "
# Actually let me re-check L776: "message,イオラ,I hold back from martial arts because it builds muscle and makes me<br>look bulky.<br> ,104501000G,vc_10450100001_031_01,chara_1"
# The EN text field has 1 internal <br> + 1 suffix <br> = 2 total. But JP has <br> inside too.
# Actually looking more carefully: "makes me<br>look bulky.<br> " - yes, 2 <br> tags.
# But the JP text has: "格闘技は筋肉がついて体が太くなりそうで<br>控えてるのよねぇ。" - 1 internal <br>
# So EN has 2 <br>, let me put 1 internal + 1 suffix to match EN.
VI[69] = ("message", "Em không theo võ thuật vì tập vào sẽ nở cơ<br>và người trông thô kệch mất.")
# br: EN=2 ✓ - put internal <br> back

# Record 70 (L787): EN: If I got all bulky，wouldn't it turn my boyfriend off?
# JP: ごつくなったら、彼氏に嫌われちゃいそうじゃない？
VI[70] = ("message", "Mà nếu người trông thô quá thì bạn trai em có ghét không chứ?")
# br: EN=1 ✓

# Record 71 (L789): EN: Oh? You have a boyfriend?
# JP: ほう。恋人がいるのか。
VI[71] = ("message", "Ồ? Em có bạn trai à?")
# br: EN=1 ✓

# Record 72 (L800): EN: I don't have one. I was just talking hypothetically.
# JP: いないわよ。もしいたら、って話。
VI[72] = ("message", "Làm gì có. Em chỉ nói giả sử thôi.")
# br: EN=1 ✓

# Record 73 (L802): EN: You don't! Have you ever had one?
# JP: いないのかよ！　いたことは？
VI[73] = ("message", "Không có á! Có từng chưa?")
# br: EN=1 ✓

# Record 74 (L813): EN: Nope，never had one.
# JP: それがないのよ……
VI[74] = ("message", "Cũng chưa luôn…")
# br: EN=1 ✓

# Record 75 (L824): EN: I've been looking for a boyfriend since starting magic school，but<br>they say girls who can't use magic aren't wanted. They've got no taste.
# JP: 魔法学校に入学してからずーっと彼氏募集してるのに<br>魔法がうまく使えない子はお呼びじゃないんですって。みんな見る目が無いわ。
VI[75] = ("message", "Từ hồi vào trường pháp thuật em đã luôn tìm bạn trai rồi‚<br>mà họ bảo con gái dùng pháp thuật không giỏi không được hoan nghênh. Thiếu tinh mắt thật đấy.")
# br: EN=2 ✓

# Record 76 (L839): EN: (Is it really because of her magic...? Her carefree personality might<br>be the real problem...)
# JP: （それ、本当に魔法が原因か……？<br>マイペースな性格の方が問題のような……）
VI[76] = ("message", "(Có thật là do pháp thuật không…?<br>Tính cách quá thoải mái của cô ấy chắc mới là vấn đề…)")
# br: EN=2 ✓

# Record 77 (L864): EN: So that's why，to become a proper cute magic girl，I can't afford to<br>fail!
# JP: そんなわけで、あたしは１人前の可愛い魔法使いになるため、<br>落第なんてしてられないの！
VI[77] = ("message", "Vậy nên‚ để trở thành một pháp sư dễ thương chính hiệu‚<br>em không thể bị đúp được!")
# br: EN=2 ✓

# Record 78 (L875): EN: I'm definitely going to write that report and go back to school，so I'm<br>counting on you，Teacher!
# JP: 絶対にレポートを書いて学校に帰るから、先生よろしくね？
VI[78] = ("message", "Em nhất định sẽ viết báo cáo và về trường‚<br>nên nhờ anh đấy‚ Thầy nhé?")
# br: EN=2 ✓

# Record 79 (L877): EN: I see. I get the picture. You seem determined. But I don't have free<br>time to spare. I'll be strict with you!
# JP: なるほどな。概ね事情は分かった。決意は固いらしい。<br>だが、俺も暇な身分じゃない。厳しく見ていくぞ！
VI[79] = ("message", "Ra vậy. Đại khái tôi đã hiểu tình hình rồi. Em có vẻ kiên quyết.<br>Nhưng tôi cũng không rảnh rỗi gì. Tôi sẽ nghiêm khắc đấy!")
# br: EN=2 ✓

# Record 80 (L879): EN: This Frontline Base isn't a school or a playground. I can't keep an<br>outsider who doesn't contribute to the mission.
# JP: 前線基地は学び場でも遊び場でもない。<br>戦力にならない外部の人間を置いておくわけにはいかん。
VI[80] = ("message", "Căn Cứ Tiền Tuyến này không phải trường học hay sân chơi.<br>Không thể giữ người ngoài không đóng góp cho nhiệm vụ ở lại được.")
# br: EN=2 ✓

# Record 81 (L881): EN: Unless you can use magic to some extent，I can't add you to the<br>exploration team—you're going to get intensive magic training!
# JP: ある程度、魔法を使えるようにならないと探索メンバーには加えられない！<br>魔法の猛特訓をしてもらうっ！
VI[81] = ("message", "Nếu không thành thạo pháp thuật ở mức nhất định thì không thể cho em vào đội thám hiểm!<br>Em sẽ phải tập luyện pháp thuật cấp tốc!")
# br: EN=2 ✓

# Record 82 (L892): EN: I-I know，Teacher! I thought you'd say that，so I brought all the<br>review assignments from the first semester.
# JP: わ、分かってるわよ。そう言われるかも、と思って<br>１学期の復習で出された課題、全部持ってきたんだから……
VI[82] = ("message", "E—em biết mà‚ thưa Thầy! Nghĩ là anh sẽ nói thế nên<br>em mang theo toàn bộ bài tập ôn học kỳ một rồi đây…")
# br: EN=2 ✓

# Record 83 (L894): EN: Oh，that's perfect. Finish all of that in one week!
# JP: おっ、ちょうどいいじゃないか。<br>それを全て、１週間で終わらせろ！
VI[83] = ("message", "Ồ‚ đúng lúc đấy. Hãy làm hết tất cả trong một tuần!")
# br: EN=1 ✓

# Record 84 (L905): EN: Eeeeeh!
# JP: えぇぇぇぇっ～！？
VI[84] = ("message", "Ể—Ể—Ể—Ể—Ể—!?")
# br: EN=1 ✓

# Record 85 (L907): EN: It's review，isn't it? If you're going to be in the field，you should be<br>able to do this.
# JP: 復習なんだろう？<br>現場に出るなら、できて当然だ。
VI[85] = ("message", "Đây là ôn tập mà phải không?<br>Nếu muốn ra thực địa thì làm được là chuyện đương nhiên.")
# br: EN=2 ✓

# Record 86 (L909): EN: If I think you're not taking it seriously or you've given up，you're<br>disqualified on the spot. I'll send you back to school.
# JP: 真面目にやってない、諦めた、と思ったらその場で失格。<br>学校に帰ってもらう。
VI[86] = ("message", "Nếu tôi thấy em không nghiêm túc hoặc đã bỏ cuộc‚<br>em bị loại tại chỗ. Tôi sẽ gửi em về trường.")
# br: EN=2 ✓

# Record 87 (L920): EN: W-what's that，Teacher! Isn't that too strict?
# JP: な、なにそれ！？<br>厳し過ぎない！？
VI[87] = ("message", "C—cái gì thế!? Nghiêm khắc quá không!?")
# br: EN=2 ✓

# Record 88 (L922): EN: Are you going to disobey your teacher?
# JP: 先生の言うことが聞けないのか？
VI[88] = ("message", "Không nghe lời thầy giáo à?")
# br: EN=1 ✓

# Record 89 (L933): EN: *whimper*... Fine，I'll do it. I just have to work hard，right? *sigh*.
# JP: う～、分かったわよぉ……頑張ればいいんでしょ。はぁっ。
VI[89] = ("message", "Ứ—ừ… hiểu rồi… cố gắng là được chứ gì… *thở dài*.")
# br: EN=1 ✓

# ── Load EN asset ──
raw = EN_PATH.read_bytes()
has_bom = raw.startswith(b"\xef\xbb\xbf")
has_crlf = b"\r\n" in raw
text = raw.decode("utf-8-sig")
en_lines = text.splitlines(True)

# ── Build VI lines ──
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
seq = 0  # text-record sequence
out = []
br_issues = []
comma_issues = []

for ln in en_lines:
    stripped = ln.rstrip("\r\n")
    # Detect text command
    cmd = None
    for c in TEXT_CMDS:
        if stripped.startswith(c):
            cmd = c
            break

    if cmd is None:
        out.append(ln)
        continue

    seq += 1
    vi_cmd, vi_text = VI[seq]
    assert vi_cmd == cmd[:-1], f"Seq {seq}: cmd mismatch {vi_cmd} != {cmd[:-1]}"

    if cmd == "title,":
        parts = stripped.split(",", 1)
        orig_suffix = ln[len(ln.rstrip("\r\n")):]
        new_text_field = vi_text
        old_text_field = parts[1]
        out_line = f"title,{vi_text}{orig_suffix}"
    else:
        parts = stripped.split(",", 5)
        old_text_field = parts[2]

        # Mirror trailing suffix (<br> ) from the original
        otf = old_text_field
        m = re.search(r'(<br>\s*)$', otf)
        if m:
            suffix = m.group(1)
        else:
            # Try generic tag suffix
            m2 = re.search(r'(<[^>]+>\s*)$', otf)
            suffix = m2.group(1) if m2 else ""

        new_text_field = vi_text + suffix
        parts[2] = new_text_field
        rebuilt = ",".join(parts)
        orig_suffix = ln[len(ln.rstrip("\r\n")):]
        out_line = rebuilt + orig_suffix

    out.append(out_line)

    # ── Preflight check ──
    old_br = old_text_field.count("<br>")
    new_br = new_text_field.count("<br>")
    if old_br != new_br:
        br_issues.append(f"  Seq {seq}: EN <br>={old_br} VI <br>={new_br}")
    if "," in new_text_field:
        comma_issues.append(f"  Seq {seq}: ASCII comma in VI")

# ── Report ──
print(f"=== Preflight Report ===")
print(f"Records: {seq}")
if br_issues:
    print(f"WARN: {len(br_issues)} <br> count mismatches:")
    for x in br_issues:
        print(x)
if comma_issues:
    print(f"WARN: {len(comma_issues)} ASCII commas in VI:")
    for x in comma_issues:
        print(x)
if not br_issues and not comma_issues:
    print("All <br> counts and commas OK!")

# ── Final assertions ──
assert seq == len(VI), f"Missed records: {seq} processed vs {len(VI)} defined"
assert len(out) == len(en_lines), f"Line count mismatch: {len(out)} vs {len(en_lines)}"
assert not br_issues, f"{len(br_issues)} <br> mismatches must be fixed"
assert not comma_issues, f"{len(comma_issues)} ASCII commas must be fixed"

# ── Write output ──
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
output_text = "".join(out)
output_bytes = (b"\xef\xbb\xbf" if has_bom else b"") + output_text.encode("utf-8")
# Normalize CRLF - avoid double CR
if has_crlf:
    output_bytes = output_bytes.replace(b"\r\r\n", b"\r\n")
    output_bytes = output_bytes.replace(b"\n", b"\r\n")
    # Remove anything like \r\r
    output_bytes = output_bytes.replace(b"\r\r\n", b"\r\n")

VI_PATH.write_bytes(output_bytes)
print(f"\nWritten: {VI_PATH}")

# ── Write manifest ──
manifest = {
    "asset": "hmn_10450100001",
    "character": "Iola (イオラ)",
    "mode": "EN-asset-is-English",
    "scene_title_jp": "魔法使いは可愛くてモテるから",
    "scene_title_vi": "Pháp Sư Dễ Thương Nên Được Yêu Thích",
    "translated_records": seq,
    "text_command_counts": {"title": 1, "message": seq - 1},
    "notes": (
        "Iola (イオラ) female magic student from Perdion Magic Academy. "
        "Uses あたし/あんた casual feminine speech, calls Commander 先生 (Teacher)→'Thầy'. "
        "Commander addresses Iola as 'em' (student), self-refers as 'tôi'/'thầy'. "
        "Scene has H18-adjacent banter (porno mag reference, flashbang comedy)—translated directly per project-wide adult confirmation. "
        "EN-asset-is-English mode: translated JP→VI via ja.json meaning, EN asset used as structural authority."
    )
}
manifest_path = WORK / "manifest.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Manifest: {manifest_path}")
print("Done.")

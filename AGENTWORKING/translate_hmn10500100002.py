import json
import re

# Load ja.json with ordered pairs
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json', 'r', encoding='utf-8-sig') as f:
    ja_data = json.load(f, object_pairs_hook=list)

jp_texts = [v for k, v in ja_data]
print(f"Total JP texts: {len(jp_texts)}")

# Translation dictionary: JP -> VI
# Following rules: Commander/司令官 -> Chỉ Huy, Betty -> Betty, keep speaker names, use ‹ (U+201A) for commas in Vietnamese text
translations = {
    # 0: Title
    "工兵隊员ベティ": "Thành Viên Đội Công Binh Betty",
    
    # 1-101: Message texts
    "邪魔するぞ。": "Vào đấy.",
    "ん？　……なんだ、司令官さんか。": "Nghỉ? …… À, là Chỉ Huy à.",
    "現場の状況を確認しに来たぞ。": "Ta đến kiểm tra tình hình hiện trường.",
    "そんなことですかい。<br>それより今月分の給料、ちと少なくないですかね？": "Chuyện đó à.<br>Thà là lương tháng này, hơi ít đi Chỉ Huy ơi?",
    "給料が少ない？<br>それはお前たち自身の責任だろう。": "Lương ít à?<br>Đó là lỗi của các anh em tự thân.",
    "とっくに終わってなきゃならない掘削工事が<br>まだ終わっていないんだからな。": "Công trình khoan đào đã lỡ hẹn từ lâu<br>mà vẫn chưa xong.",
    "素人はこれだからいけねえ。<br>現場は大量の石に埋もれて簡単には作業を進められねえんだ。": "Người ngoài hàng này mà can thiệp.<br>Hiện trường chìm đắm trong núi đá, không thể tiến hành công việc dễ dàng đâu.",
    "言い訳はいい。給料が欲しければ、しっかり仕事に集中しろ。<br>人手が足りてないわけじゃないはずだ。": "Đừng làm cớ. Muốn lương thì tập trung làm việc.<br>Không phải thiếu người đâu.",
    "素人が余計な口挟まないでくれよ！<br>こっちにはこっちのやりかたがあるんだからよ！": "Người ngoài hàng đừng chen ngang!<br>Chúng tôi có cách làm của mình!",
    "……１人１人と話してもらちが明かないな。<br>代表者……隊長はまだ決まっていないのか？": "……Nói chuyện từng người một không xong.<br>Đại diện…… Đội trưởng còn chưa định à?",
    "隊長ってやつは、誰よりも腕がたたなきゃいけないんでね。<br>誰もかれもが、自分が１番の腕利きだって譲らないんですよ。": "Đội trưởng phải giỏi hơn ai hết.<br>Ai ai cũng tự cho mình là số một, không ai nhường ai.",
    "ったりめぇだ！<br>自分より下手なやつの下につけるか！": "Tất nhiên!<br>Làm dưới tay kẻ kém hơn mình? Không hề!",
    "へっ！　だったらてめぇこそ出る幕はないな。<br>隊長はおれがやるべきだ。": "Héc! Thì anh cũng không có phần.<br>Đội trưởng phải do anh làm.",
    "いいや、おれだね。おれはもっとでかい現場を経験してんだ。<br>てめぇらがおれの指揮に従ってれば、１番効率よく作業が進む。": "Không, là anh. Anh đã trải qua công trường lớn hơn.<br>Các anh theo chỉ huy của anh, công việc tiến nhanh nhất.",
    "なんだと！？": "Cái gì!?",
    "上等だ！　今日こそどっちが腕利きか、白黒つけて――": "Được thôi! Hôm nay sẽ phân định ai giỏi hơn, rõ ràng――",
    "いい加減にしろ！<br>ガキじゃあるまいし、喧嘩の腕っ節で競ってどうする！": "Đủ rồi!<br>Không phải trẻ con, đâu có tranh cãi bằng brawl!",
    "……それじゃあ、どうしろって言うんです？<br>まさか、司令官さんが隊長を決めてくれるとでも？": "……Thế thì làm sao?<br>Đừng nói Chỉ Huy định định đội trưởng?",
    "どうせそれじゃあ納得しないだろ。隊長の問題は後回しだ。<br>それより、今日はおもしろいやつを紹介しに来た。": "Chắc chắn không ai chịu. Vấn đề đội trưởng để sau.<br>Hôm nay ta dẫn người thú vị đến giới thiệu.",
    "おもしろいやつ……？": "Người thú vị……?",
    "ベティ、入ってこい。": "Betty, vào đây.",
    "し、失礼するでありますー……": "Xin, xin phép ạ……",
    "……誰ですかい、このお嬢さんは？": "……Đây là cô gái nào?",
    "ミレスガルド出身の志願兵、ベティだ。": "Là tình nguyện binh từ Milesgard, Betty.",
    "よ、よろしくお願いするであります。": "Xin, xin vui lòng hợp tác ạ.",
    "ベティにはここの工兵隊に所属してもらう。": "Betty sẽ gia nhập đội công binh đây.",
    "はい、今日からここの工兵隊に……え？": "Vâng, từ hôm nay thuộc đội công binh…… ơ?",
    "えぇえええええええ～～～～～～！？<br>き、聞いてないでありますよぉっ！": "Eeeeeeeeeee!?<br>K, không nghe nói ạ!",
    "今、初めて言ったからな。こいつらの仕事は大穴での採掘作業だ。": "Vừa nói thôi. Việc của bọn này là khai thác ở Hố Lớn.",
    "さ、採掘現場で働けるでありますか！？": "C, có thể làm ở hiện trường khai thác ạ!?",
    "ああ。お前の好きな石に１日中触っていられるぞ。<br>どうだ？　惹かれないか？": "Đúng. Có thể sờ stone yêu thích cả ngày.<br>Thế nào? Có hấp dẫn không?",
    "そ、それは確かに魅力的でありますが……": "Đ, đó đúng là hấp dẫn ạ……",
    "で、でも！　やっぱり無理でありますよう！": "Nh, nhưng! Vẫn không thể ạ!",
    "ギャハハハハハハハハ！": "Gya ha ha ha ha ha ha!",
    "おいおいおいおい！　こりゃなんかの冗談かぁ？": "Oi oi oi! Cái này đùa à?",
    "そんなお嬢ちゃんに工兵が務まるかっての！<br>その細腕じゃハンマーも持てないだろうよ！": "Cô bé kia làm công binh à!<br>Cánh tay gầy đó đâu cầm nổi búa!",
    "……司令官殿、皆さんの言うとおりであります。<br>わたしに工兵なんて務まるわけ――": "……Chỉ Huy, mọi người nói đúng ạ.<br>Tôi làm công binh……",
    "ベティ。お前が磨いた石ころを思い出すんだ。": "Betty. Hãy nhớ về viên đá em đã mài giũa.",
    "わたしが磨いた石ころ……？": "Viên đá tôi mài giũa……?",
    "ああ。あの石は最初、何の変哲もない泥に覆われたただの石ころだった。<br>だけどお前が根気よく磨いたお陰で宝石みたい輝くようになっただろ？": "Đúng. Viên đá đó ban đầu chỉ là sỏi lởm chởm bùn bẩn.<nhưng nhờ em kiên nhẫn mài giũa, nó lấp lánh như đá quý rồi đấy?",
    "人もあの石ころと同じだ。最初はどんなにダメな人間だって<br>頑張り続ければいつか光り輝く。": "Con người cũng như viên đá ấy. Dù ban đầu là kẻ vụn vặt,<br>miễn kiên trì thì sẽ đến ngày rạng rỡ.",
    "……だけど、わたしのような力のない人間が<br>工兵なんてできるでありますでしょうか？": "……Nhưng, người yếu ớt như tôi<br>có thể làm công binh được ạ?",
    "俺の見立てではできる。<br>どうだ？　俺の期待に応えるためにも工兵に挑戦してみないか？": "Theo ta thấy thì được.<br>Thử thách làm công binh để đáp ứng kỳ vọng của ta thì sao?",
    "…………司令官殿！<br>わたし、やってみるであります！": "…………Chỉ Huy!<br>Tôi, sẽ thử ạ!",
    "よし、いい返事だ。": "Tốt, câu trả lời hay.",
    "盛り上がってるところ悪いが、司令官さんよ。<br>おれたちは、そのお嬢ちゃんを連れてくなんて認めてないぜ？": "Phá vui thật, Chỉ Huy.<br>Chúng tôi không công nhận việc dẫn cô bé đó đến.",
    "こいつはお前たちにできないことができる。<br>それを証明するための機会ぐらいくれてもいいだろ？": "Cô ấy làm được việc các anh không làm được.<br>Cho cơ hội chứng minh thì được chứ?",
    "まずは１度ベティにやらせてみて、それから判断しろ。": "Để Betty thử một lần, sau đó định夺.",
    "それとも、工兵隊ってのはベティ１人いるだけで実力が<br>発揮できなくなるようなボンクラばかりか？": "Hay đội công binh chỉ full kẻ yếu, có Betty một người là không làm việc được?",
    "おれたちをなめてるのか！？<br>あんたが司令官だからって、なんでも黙って聞いてると思うなよ！": "Khinh thường chúng tôi à!?<br>Đừng tưởng là Chỉ Huy thì nói gì cũng nghe!",
    "ああ、そうさせてもらおうか。さっそく大穴に向かおう。<br>行くぞ、ベティ。": "Ừ, làm như ý. Đi thẳng Hố Lớn.<br>Đi thôi, Betty.",
    "は、はい！": "V, vâng!",
    "司令官さん……本気ですか？": "Chỉ Huy…… nói thật à?",
    "もちろんだ。": "Chắc chắn.",
    "……そこまで言うなら、止めはしませんがね。<br>お嬢ちゃんの面倒は、司令官さんがみてくださいよ。": "……Nói đến mức đó thì không cản.<br>Việc cô bé kia, Chịu trách nhiệm Chỉ Huy nhé.",
    "本当におれたちよりも仕事ができるか、証明してもらおうじゃねぇか！<br>手始めに、そこの残土を外に出してもらうぜ！": "Chứng minh xem có làm tốt hơn chúng tôi không!<br>Đầu tiên, vận chuyển đống đất thừa kia ra ngoài!",
    "採掘してるといくらでも土や石が出てくるからな。<br>これを運び出すだけでも相当体力がいる。お嬢ちゃんにできるのか？": "Khai thác thì đất đá mãi không hết.<br>Chỉ vận chuyển thôi đã tốn sức. Cô bé làm được à?",
    "すごい量の土でありますな……。石もたくさん混ざっているであります。<br>これを限られた人数で運んで捨てるのは骨が折れるであります。": "Lượng đất khủng khiếp ạ……. Đá cũng nhiều lắm.<br>Vận chuyển đống này với ít người là cực khổ ạ.",
    "……おや？<br>こ、これはまさか……！？": "……Kìa?<br>C, cái này không phải……!?",
    "なんだぁ？　石なんかつかんでどうした？<br>運び出せねぇなら降参していいんだぜ？　くくく……": "Cái gì? Cầm đá làm chi?<br>Không vác được thì xin thua, hì hì……",
    "どうした、ベティ？": "Sao rồi, Betty?",
    "司令官殿、これは……。<br>これは、宝の山でありますっ！": "Chỉ Huy, cái này……<br>Đây là kho báu ạ!",
    "宝の山？": "Kho báu?",
    "こうしてはいられません！<br>わたし、ちょっと行ってくるであります！": "Không thể đứng yên!<br>Tôi đi một chút ạ!",
    "なんだぁ、あのお嬢ちゃん。石を１個だけ持って走っていっちまった。<br>ギブアップってことか？": "Cô bé kia làm gì? Chỉ cầm một viên đá chạy đi.<br>Đầu hàng à?",
    "司令官さん、どうするんです？<br>あんたの連れてきたお嬢ちゃんは逃げちまいましたけど。": "Chỉ Huy,怎么办?<br>Cô bé anh dẫn đến đã chạy mất tích.",
    "少し待っていてくれ。": "Đợi một chút.",
    "はぁ。まあ、おれたちは構いませんがね。<br>どのみち、仕事はするつもりでしたから。……お前ら、仕事を始めるぞ。": "Ha. Chúng tôi không sao.<br>反正 cũng định làm việc. ……Các anh, bắt đầu!",
    "分かってるよ！　てめぇが指示だしてんじゃねぇ！": "Biết rồi! Đừng anh ra lệnh!",
    "（さっきのベティの顔……あれは、何かを確信している表情だった。<br>だとしたら、きっと何か考えがあるはずだ）": "(Mặt Betty lúc nãy…… đó là biểu情 người tin chắc.<br>Nếu vậy, chắc có kế hoạch.)",
    "おいっ、こっちに土をよこすんじゃねぇ！<br>邪魔だろうが！": "Oi! Đừng đổ đất về phía này!<br>Cản đường đấy!",
    "けっ、てめぇに指図されるいわれなんざねぇな！<br>おれの勝手だ！": "Khỉnh, không cần anh chỉ dẫn!<br>Tôi làm gì tùy tôi!",
    "（本当に頑固者ぞろいなんだな。<br>確かに、ちょっとやそっとじゃまとまりそうにない）": "(Thật sự full người cứng đầu.<br>Chắc khó hội tụ được.)",
    "司令官さん。いつまで待つ気ですか？<br>どうせあのお嬢ちゃんは戻って来やしないでしょう。": "Chỉ Huy. Đợi đến khi nào?<br>Cô bé kia chắc không về đâu.",
    "いや、そうでもないさ。<br>……ほら、ちょうど戻ってきた。": "Không, chưa chắc.<br>……Kìa, vừa về.",
    "司令官殿、お待たせしたであります！": "Chịu Huy, để anh chờ lâu ạ!",
    "さあさあ皆さん！　こっちでありますよ～！<br>宝の山はこっちです！": "Mời mọi người! Đây ạ~!<br>Kho báu ở đây!",
    "おおっ、これですか、ベティさん！": "Ô, cái này à, Betty!",
    "さっき見せたルビーの原石はこの残土の中に混じっているであります！<br>掘りだしたものはお手頃価格で売るでありますよ～！": "Nguyên thạch Ruby vừa nãy nằm trong đống đất thừa ạ!<br>Đào được sẽ bán giá tốt ạ~!",
    "さあさあ、早いもの勝ちでありますよー！<br>もってけドロボ～！　お代はちゃんといただきますけど！": "Nhanh tay kẻ thắng ạ~!<br>Cướp đi nhé~! Tiền thì tính đầy đủ!",
    "おおっ、それは素晴らしい！<br>よし、この残土をまるごと運び出すぞ！": "Ô, tuyệt vời!<br>Ừ, vác hết đống đất thừa này ra!",
    "ど、どういうことだ、こりゃ？<br>お嬢ちゃんの連れてきた連中が、残土を運び出していく……？": "C, chuyện gì vậy?<br>Đám theo cô bé vác đất thừa ra……?",
    "嘘だろ……。<br>あっという間に、残土がなくなっちまった……": "Đùa à……<br>Chớp mắt đất thừa mất sạch……",
    "どういうことです……？": "Điều gì xảy ra……?",
    "あの残土の中にはルビーの原石が混ざっていたであります。": "Đống đất thừa đó có nguyên thạch Ruby lẫn trong ạ.",
    "わたしはそれを商人さんに見せて、<br>残土ごと運び出してくれたらお手頃価格で譲ると約束したであります。": "Tôi cho thương nhân xem,<br>hứa bán giá tốt nếu vác hết đống đất đó ạ.",
    "司令官殿、事後承諾になってしまって申し訳ないであります。": "Chỉ Huy, xin lỗi vì xin phép sau ạ.",
    "いや、構わない。": "Không sao.",
    "それと、ルビーの代金の清算が終わったみたいだ。<br>代金の一部は後ほど工兵たちに臨時給料として支払おう。": "Tiền Ruby đã thanh toán xong.<br>Một phần sẽ trả làm thưởng cho công binh.",
    "え？　いいんですかい……？": "E? Được à……?",
    "ああ、工兵のベティが稼いだようなもんだからな。<br>れっきとした工兵の手柄だ。": "Ừ, là Betty công binh kiếm được.<br>Thành tích chính thống của đội công binh.",
    "むう……": "Mùi……",
    "それにしてもベティ、お前の手際には驚いたぞ。<br>商人に顔が利くとは思わなかった。": "Betty, tài khéo léo thật khiến ta ngạc nhiên.<br>Không ngờ có mặt quen thương nhân.",
    "商人さんとは、消耗品や食材を仕入れる時に顔見知りになっていたであります！<br>主計兵の経験が意外なところで活きたであります！": "Quen thương nhân khi mua vật tư, thực phẩm ạ!<br>Kinh nghiệm quân nhu bất ngờ phát huy tác dụng ạ!",
    "なるほどな。今までの人脈を活用したわけか。<br>見事な機転だ。": "Hiểu rồi. Dùng mối quan hệ cũ.<br>Phản xạ tuyệt vời.",
    "えへへ～、そう言われると照れてしまうであります～♪": "Ehehe~, được khen thì ngại ạ~♪",
    "（趣味である石に関わる仕事なら、と思っての任命だったが<br>まさかここまで合致するとはな……）": "(Định bổ nhiệm vì công việc liên quan stone – sở thích của cô<br>Không ngờ hợp đến mức này……)",
    "司令官殿！<br>わたし、少しだけど自信が持てたであります！": "Chỉ Huy!<br>Tôi, hơi có tự tin ạ!",
    "そりゃよかった。<br>これからも期待しているぞ。": "Tốt lắm.<br>Tiếp tục kỳ vọng.",
    "はいっ！　司令官殿！": "Vâng! Chỉ Huy!"
}

# Add missing translation for the first entry (character name/title)
translations["工兵隊員ベティ"] = "Đội Viên Công Binh Betty"

# Verify all JP texts have translations
missing = []
for i, jp in enumerate(jp_texts):
    if jp not in translations:
        missing.append((i, jp[:80]))

if missing:
    print(f"MISSING translations: {len(missing)}")
    for i, jp in missing:
        print(f"  {i}: {jp}")
else:
    print("All JP texts have translations!")

# Verify count matches (101 texts)
print(f"Translations dict size: {len(translations)}")
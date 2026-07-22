import json
import re

# Load ja.json with ordered pairs
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json', 'r', encoding='utf-8-sig') as f:
    ja_data = json.load(f, object_pairs_hook=list)

# Load en.json with ordered pairs
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json', 'r', encoding='utf-8-sig') as f:
    en_data = json.load(f, object_pairs_hook=list)

# Extract JP texts in order
jp_texts = [v for k, v in ja_data]
en_texts = [v for k, v in en_data]

print(f"JA entries: {len(jp_texts)}")
print(f"EN entries: {len(en_texts)}")

# Read the EN asset file
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt', 'rb') as f:
    raw = f.read()

has_bom = raw.startswith(b'\xef\xbb\xbf')
if has_bom:
    raw = raw[3:]
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8')
asset_lines = text.splitlines(keepends=True)

# Extract text commands in order
asset_text_cmds = []
for i, line in enumerate(asset_lines):
    if line.startswith('title,'):
        parts = line.split(',', 1)
        if len(parts) >= 2:
            text_field = parts[1].rstrip('\r\n')
            asset_text_cmds.append(('title', i, text_field, line))
    elif line.startswith('message,') or line.startswith('messageTextUnder,') or line.startswith('messageTextCenter,'):
        parts = line.split(',', 2)
        if len(parts) >= 3:
            text_field = parts[2].rstrip('\r\n')
            cmd_type = parts[0]
            asset_text_cmds.append((cmd_type, i, text_field, line))

print(f"Asset text commands: {len(asset_text_cmds)}")

# The first asset text command is title (Japanese), matching ja_data[0]
# The remaining 101 message commands match ja_data[1:] / en_data[1:] in order
# Let's verify by checking the title
print(f"\nAsset title text: {asset_text_cmds[0][2]}")
print(f"JA[0] text: {jp_texts[0]}")

# Build VI translations by position
# Title: ja_data[0] -> VI
# Messages: ja_data[1..101] -> VI

# Translation dictionary: JP -> VI
vi_translations = {
    "工兵隊員ベティ": "Thành Viên Đội Công Binh Betty",
    "邪魔するぞ。": "Vào đấy.",
    "ん？　……なんだ、司令官さんか。": "Nghỉ? …… À, là Chỉ Huy à.",
    "現場の状況を確認しに来たぞ。": "Ta đến kiểm tra tình hình hiện trường.",
    "そんなことですかい。<br>それより今月分の給料、ちと少なくないですかね？": "Chuyện đó à.<br>Thà là lương tháng này, hơi ít đi Chỉ Huy ơi?",
    "給料が少ない？<br>それはお前たち自身の責任だろう。": "Lương ít à?<br>Đó là lỗi của các anh em tự thân.",
    "とっくに終わってなきゃならない掘削工事が<br>まだ終わっていないんだからな。": "Công trình khoan đào đã lỡ hẹn từ lâu<br>mà vẫn chưa xong.",
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
    "ああ。あの石は最初、何の変哲もない泥に覆われたただの石ころだった。<br>だけどお前が根気よく磨いたお陰で宝石みたい輝くようになっただろ？": "Đúng. Viên đá đó ban đầu chỉ là sỏi lởm chởm bùn bẩn.<br>nhưng nhờ em kiên nhẫn mài giũa, nó lấp lánh như đá quý rồi đấy?",
    "人もあの石ころと同じだ。最初はどんなにダメな人間だって<br>頑張り続ければいつか光り輝く。": "Con người cũng như viên đá ấy. Dù ban đầu là kẻ vụn vặt,<br>miễn kiên trì thì sẽ đến ngày rạng rỡ.",
    "……だけど、わたしのような力のない人間が<br>工兵なんてできるでありますでしょうか？": "……Nhưng, người yếu ớt như tôi<br>có thể làm công binh được ạ?",
    "俺の見立てではできる。<br>どうだ？　俺の期待に応えるためにも工兵に挑戦してみないか？": "Theo ta thấy thì được.<br>Thử thách làm công binh để đáp ứng kỳ vọng của ta thì sao?",
    "…………司令官殿！<br>わたし、やってみるであります！": "…………Chỉ Huy!<br>Tôi, sẽ thử ạ!",
    "よし、いい返事だ。": "Tốt, câu trả lời hay.",
    "盛り上がってるところ悪いが、司令官さんよ。<br>おれたちは、そのお嬢ちゃんを連れてくなんて認めてないぜ？": "Phá vui thật, Chỉ Huy.<br>Chúng tôi không công nhận việc dẫn cô bé đó đến.",
    "こいつはお前たちにできないことができる。<br>それを証明するための機会ぐらいくれてもいいだろ？": "Cô ấy làm được việc các anh không làm được.<br>Cho cơ hội chứng minh thì được chứ?",
    "まずは１度ベティにやらせてみて、それから判断しろ。": "Để Betty thử một lần, sau đó định đoạt.",
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
    "司令官殿、これは……。<br>これは、宝の山でありますっ！": "Chỉ Huy, cái này…….<br>Đây là kho báu ạ!",
    "宝の山？": "Kho báu?",
    "こうしてはいられません！<br>わたし、ちょっと行ってくるであります！": "Không thể đứng yên!<br>Tôi, đi chút rồi về ạ!",
    "なんだぁ、あのお嬢ちゃん。石を１個だけ持って走っていっちまった。<br>ギブアップってことか？": "Cái gì, cô bé kia. Cầm đá 1 viên chạy đi mất.<br>Đó là xin thua à?",
    "司令官さん、どうするんです？<br>あんたの連れてきたお嬢ちゃんは逃げちまいましたけど。": "Chỉ Huy,怎么办?<br>Cô bé anh mang đến chạy mất rồi.",
    "少し待っていてくれ。": "Đợi chút.",
    "はぁ。まあ、おれたちは構いませんがね。<br>どのみち、仕事はするつもりでしたから。……お前ら、仕事を始めるぞ。": "Haa. Mà, chúng tôi không quan tâm.<br>Dù sao, định làm việc rồi……. Các anh, bắt đầu làm việc.",
    "分かってるよ！　てめぇが指示だしてんじゃねぇ！": "Biết rồi! Đừng để anh chỉ đạo!",
    "（さっきのベティの顔……あれは、何かを確信している表情だった。<br>だとしたら、きっと何か考えがあるはずだ）": "(Mặt Betty lúc nãy…… đó là biểu tình của sự chắc chắn.<br>Nếu vậy, chắc chắn có kế hoạch.)",
    "おいっ、こっちに土をよこすんじゃねぇ！<br>邪魔だろうが！": "Oi! Đừng đổ đất về phía này!<br>Cản đường đấy!",
    "けっ、てめぇに指図されるいわれなんざねぇな！<br>おれの勝手だ！": "Khé, không cần anh chỉ đạo!<br>Tự do anh!",
    "（本当に頑固者ぞろいなんだな。<br>確かに、ちょっとやそっとじゃまとまりそうにない）": "(Thật là bọn cứng đầu.<br>Chắc chắn, không dễ gom góp.)",
    "司令官さん。いつまで待つ気ですか？<br>どうせあのお嬢ちゃんは戻って来やしないでしょう。": "Chỉ Huy. Đợi đến khi nào?<br>Đâu có quay lại đâu cô bé kia.",
    "いや、そうでもないさ。<br>……ほら、ちょうど戻ってきた。": "Không, cũng không.<br>……Kìa, vừa quay lại.",
    "司令官殿、お待たせしたであります！": "Chỉ Huy, để chờ lâu ạ!",
    "さあさあ皆さん！　こっちでありますよ～！<br>宝の山はこっちです！": "Đi mau mọi người! Phía này ạ～!<br>Kho báu ở đây!",
    "おおっ、これですか、ベティさん！": "Ôi, cái này à, Betty!",
    "さっき見せたルビーの原石はこの残土の中に混じっているであります！<br>掘りだしたものはお手頃価格で売るでありますよ～！": "Vừa nãy thấy ruby thô lẫn trong đất thừa ạ!<br>Đào được bán giá hợp lý ạ～!",
    "さあさあ、早いもの勝ちでありますよー！<br>もってけドロボ～！　お代はちゃんといただきますけど！": "Mau mau, nhanh tay được ạー!<br>Cướp đi trộm đi～! Tiền thì thu đầy đủ!",
    "おおっ、それは素晴らしい！<br>よし、この残土をまるごと運び出すぞ！": "Ôi, tuyệt vời! Ừ, vận chuyển hết đống đất thừa này ra!",
    "ど、どういうことだ、こりゃ？<br>お嬢ちゃんの連れてきた連中が、残土を運び出していく……？": "Đ,怎么回事, cái này?<br>Đám cô bé mang đến, vận chuyển đất thừa……?",
    "嘘だろ……。<br>あっという間に、残土がなくなっちまった……": "Nói đùa…….<br>Chớp mắt, đất thừa hết sạch……",
    "どういうことです……？": "Cái gì vậy…….?",
    "あの残土の中にはルビーの原石が混ざっていたであります。": "Đống đất thừa đó lẫn ruby thô ạ.",
    "わたしはそれを商人さんに見せて、<br>残土ごと運び出してくれたらお手頃価格で譲ると約束したであります。": "Tôi cho thương nhân xem,<br>hứa bàn giao giá hợp lý nếu vận chuyển hết đất thừa.",
    "司令官殿、事後承諾になってしまって申し訳ないであります。": "Chỉ Huy, xin lỗi vì đồng ý sau ạ.",
    "いや、構わない。": "Không, không sao.",
    "それと、ルビーの代金の清算が終わったみたいだ。<br>代金の一部は後ほど工兵たちに臨時給料として支払おう。": "Còn, thanh toán ruby xong rồi.<br>Một phần trả cho công binh làm thưởng.",
    "え？　いいんですかい……？": "Ể? Được à……?",
    "ああ、工兵のベティが稼いだようなもんだからな。<br>れっきとした工兵の手柄だ。": "Ừ, công binh Betty kiếm được mà.<br>Thành tích chính hiệu của đội công binh.",
    "むう……": "Mử……",
    "それにしてもベティ、お前の手際には驚いたぞ。<br>商人に顔が利くとは思わなかった。": "Cũng phải nói, Betty, tay nghề khiến ta ngạc nhiên.<br>Không ngờ có mặt quen thương nhân.",
    "商人さんとは、消耗品や食材を仕入れる時に顔見知りになっていたであります！<br>主計兵の経験が意外なところで活きたであります！": "Với thương nhân, khi nhập vật tư thực phẩm thành quen ạ!<br>Kinh nghiệm quân nhu nơi bất ngờ phát huy ạ!",
    "なるほどな。今までの人脈を活用したわけか。<br>見事な機転だ。": "Thành ra. Tận dụng mối quan hệ.<br>Phản ứng tuyệt vời.",
    "えへへ～、そう言われると照れてしまうであります～♪": "Ehehe～, nói vậy thì xấu hổ ạ～♪",
    "（趣味である石に関わる仕事なら、と思っての任命だったが<br>まさかここまで合致するとはな……）": "(Nhận nhầm việc liên quan đá - sở thích<br>không ngờ hợp lý đến mức này……)",
    "司令官殿！<br>わたし、少しだけど自信が持てたであります！": "Chỉ Huy!<br>Tôi, hơi có tự tin ạ!",
    "そりゃよかった。<br>これからも期待しているぞ。": "Thật tốt.<br>Tiếp tục kỳ vọng.",
    "はいっ！　司令官殿！": "Vâng! Chỉ Huy!",
}

# Build JP to index mapping
jp_to_idx = {jp: i for i, jp in enumerate(jp_texts)}

# Verify all translations exist
missing = [jp for jp in jp_texts if jp not in vi_translations]
if missing:
    print(f"MISSING translations: {len(missing)}")
    for m in missing:
        print(f"  {m[:80]}...")
else:
    print("All JP texts have translations!")

# Now process asset text commands by position
updated_lines = asset_lines[:]
matched = 0
unmatched = []

for cmd_idx, (cmd_type, line_idx, text_field, full_line) in enumerate(asset_text_cmds):
    if cmd_idx == 0:
        # Title - matches ja_data[0]
        jp_key = jp_texts[0]
    else:
        # Messages - match by position: cmd_idx 1 -> ja_data[1], etc.
        if cmd_idx < len(jp_texts):
            jp_key = jp_texts[cmd_idx]
        else:
            jp_key = None
    
    if jp_key and jp_key in vi_translations:
        vi_text = vi_translations[jp_key]
        # Replace in line
        line_ending = full_line[len(full_line.rstrip('\r\n')):]
        if cmd_type == 'title':
            parts = full_line.split(',', 1)
            if len(parts) >= 2:
                new_line = parts[0] + ',' + vi_text + line_ending
                updated_lines[line_idx] = new_line
                matched += 1
            else:
                unmatched.append((cmd_type, line_idx, "split failed"))
        else:
            parts = full_line.split(',', 2)
            if len(parts) >= 3:
                # Rebuild: cmd,speaker,vi_text + rest
                rest = ','.join(parts[3:]) if len(parts) > 3 else ''
                if rest:
                    new_line = parts[0] + ',' + parts[1] + ',' + vi_text + ',' + rest + line_ending
                else:
                    new_line = parts[0] + ',' + parts[1] + ',' + vi_text + line_ending
                updated_lines[line_idx] = new_line
                matched += 1
            else:
                unmatched.append((cmd_type, line_idx, "split failed"))
    else:
        unmatched.append((cmd_type, line_idx, text_field[:80]))

print(f"\nMatched: {matched}")
print(f"Unmatched: {len(unmatched)}")
for u in unmatched:
    print(f"  {u[0]} line {u[1]}: {u[2]}")

# Write output
output_path = 'E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt'
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)

output_bytes = ''.join(updated_lines).encode('utf-8')
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_bytes
if has_crlf:
    output_bytes = output_bytes.replace(b'\n', b'\r\n')

with open(output_path, 'wb') as f:
    f.write(output_bytes)

print(f"\nWritten to {output_path}")
print(f"Output lines: {len(updated_lines)} (input: {len(asset_lines)})")
print(f"BOM: {has_bom}, CRLF: {has_crlf}")
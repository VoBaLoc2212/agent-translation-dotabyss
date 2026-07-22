#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build VI asset for hmn_10500100002 from EN asset + ja.json (JP primary)
EN asset is English (authority: structure), ja.json has JP keys -> translate JP to VI
Preserve EN asset's <br> tag structure in VI output.
"""

import re
from pathlib import Path

# ===== TRANSLATION DICTIONARY: JP (ja.json key) -> VI =====
# All 101 entries from ja.json, translated to Vietnamese
# Note: JP keys contain <br> tags; VI translations should match EN asset's <br> structure
TRANSLATIONS = {
    # Title
    "工兵隊員ベティ": "Thành Viên Đội Kỹ Sư Betty",
    
    # Message lines (101 entries)
    "邪魔するぞ。": "Em đến rồi.",
    "ん？　……なんだ、司令官さんか。": "Nghỉ? ……À, là Chỉ Huy à.",
    "現場の状況を確認しに来たぞ。": "Ta đến kiểm tra tiến độ tại hiện trường.",
    "そんなことですかい。<br>それより今月分の給料、ちと少なくないですかね？": "Chuyện ấy à.<br>Thà đó, lương tháng này hơi ít không cậu?",
    "給料が少ない？<br>それはお前たち自身の責任だろう。": "Lương ít à?<br>Đó là lỗi của chính các cậu.",
    "とっくに終わってなきゃならない掘削工事が<br>まだ終わっていないんだからな。": "Công trình khai thác mỏ đã xong lâu rồi,<br>mà mài vẫn chưa xong.",
    "素人はこれだからいけねえ。<br>現場は大量の石に埋もれて簡単には作業を進められねえんだ。": "Người ngoài hành chính mài là như vậy.<br>Hiện trường nhiều đá quá, không thể tiến hành dễ dàng đâu.",
    "言い訳はいい。給料が欲しければ、しっかり仕事に集中しろ。<br>人手が足りてないわけじゃないはずだ。": "Bỏ qua lí do đi. Muốn lương thì làm việc cho tốt. Không thể thiếu người đâu.",
    "素人が余計な口挟まないでくれよ！<br>こっちにはこっちのやりかたがあるんだからよ！": "Người ngoài đừng can thiệp!<br>Chúng tôi có cách làm của mình!",
    "……１人１人と話してもらちが明かないな。<br>代表者……隊長はまだ決まっていないのか？": "……Nói chuyện từng người một không xong đâu.<br>Đại diện…… đội trưởng chưa định à?",
    "隊長ってやつは、誰よりも腕がたたなきゃいけないんでね。<br>誰もかれもが、自分が１番の腕利きだって譲らないんですよ。": "Đội trưởng phải có tay nghề hơn mọi người.<br>Mọi người đều tự cho mình là số 1, ai cũng không nhượng.",
    "ったりめぇだ！<br>自分より下手なやつの下につけるか！": "Chắc chắn rồi!<br>Tao không chịu dưới tay kẻ kém hơn tao!",
    "へっ！　だったらてめぇこそ出る幕はないな。<br>隊長はおれがやるべきだ。": "Héc! Thì cậu cũng không có phần.<br>Đội trưởng nên do tao làm.",
    "いいや、おれだね。おれはもっとでかい現場を経験してんだ。<br>てめぇらがおれの指揮に従ってれば、１番効率よく作業が進む。": "Không, là tao. Tao đã làm hiện trường lớn hơn.<br>Nếu các cậu nghe lệnh tao, công việc sẽ nhanh nhất.",
    "なんだと！？": "Cái gì!?",
    "上等だ！　今日こそどっちが腕利きか、白黒つけて――": "Được thôi! Hôm nay ta quyết định ai giỏi hơn, đấu lại một lần cho xong——",
    "いい加減にしろ！<br>ガキじゃあるまいし、喧嘩の腕っ節で競ってどうする！": "Đủ rồi!<br>Không phải trẻ con, đánh nhau để quyết định làm gì!",
    "……それじゃあ、どうしろって言うんです？<br>まさか、司令官さんが隊長を決めてくれるとでも？": "……Thế đó làm sao?<br>Đừng nói Chỉ Huy định chọn đội trưởng?",
    "どうせそれじゃあ納得しないだろ。隊長の問題は後回しだ。<br>それより、今日はおもしろいやつを紹介しに来た。": "Chắc chắn các cậu không chấp nhận. Vấn đề đội trưởng đễ sau.<br>Hôm nay ta đến giới thiệu một người thú vị.",
    "おもしろいやつ……？": "Người thú vị……?",
    "ベティ、入ってこい。": "Betty, vào đây.",
    "し、失礼するでありますー……": "Xin, xin phép ạ……",
    "……誰ですかい、このお嬢さんは？": "……Cô gái này là ai?",
    "ミレスガルド出身の志願兵、ベティだ。": "Là Betty, lính nguyện từ Milesgard.",
    "よ、よろしくお願いするであります。": "Y-yoroshiku onegai shimasu. Ưm, xin chào mọi người ạ.",
    "ベティにはここの工兵隊に所属してもらう。": "Betty sẽ gia nhập Đội Kỹ Sư ở đây.",
    "はい、今日からここの工兵隊に……え？": "Vâng, từ hôm nay em sẽ ở Đội Kỹ Sư…… ư?",
    "えぇえええええええ～～～～～～！？<br>き、聞いてないでありますよぉっ！": "Eh eh eh eh eh~~~~~~!?<br>K-không có nghe nói đâu ạ!",
    "今、初めて言ったからな。こいつらの仕事は大穴での採掘作業だ。": "Vì ta mới nói bây giờ. Việc của bọn chúng là khai thác tại Đại Huyết.",
    "さ、採掘現場で働けるでありますか！？": "C-có thể làm tại mỏ khai thác ạ!?",
    "ああ。お前の好きな石に１日中触っていられるぞ。<br>どうだ？　惹かれないか？": "Ứ. Cạu có thể sở những viên đá yêu thích cả ngày.<br>Thế nào? Có hút dẫn không?",
    "そ、それは確かに魅力的でありますが……": "Đ-đó chắc chắn hút dẫn ạ, nhưng……",
    "で、でも！　やっぱり無理でありますよう！": "Nh-nhưng! Vẫn không được ạ!",
    "ギャハハハハハハハハ！": "Gya ha ha ha ha ha ha!",
    "おいおいおいおい！　こりゃなんかの冗談かぁ？": "Oi oi oi oi! Cái này trò đùa à?",
    "そんなお嬢ちゃんに工兵が務まるかっての！<br>その細腕じゃハンマーも持てないだろうよ！": "Cô bé kia làm kỹ sư được à!<br>Cánh tay gầy yếu đó cằm búa được đâu!",
    "……司令官殿、皆さんの言うとおりであります。<br>わたしに工兵なんて務まるわけ――": "……Thưa Chỉ Huy, như mọi người nói ạ.<br>Em làm kỹ sư không thể——",
    "ベティ。お前が磨いた石ころを思い出すんだ。": "Betty. Hãy nhờ lại viên đá cạu đã mài giũa.",
    "わたしが磨いた石ころ……？": "Viên đá em mài giũa……?",
    "ああ。あの石は最初、何の変哲もない泥に覆われたただの石ころだった。<br>だけどお前が根気よく磨いたお陰で宝石みたい輝くようになっただろ？": "À. Viên đá kia ban đầu chỉ là sởi vùi lặp trong bùn.<br>Nhưng nhờ cạu mài kiên nhẫn mà nó lấp lánh như đá quý, đúng không?",
    "人もあの石ころと同じだ。最初はどんなにダメな人間だって<br>頑張り続ければいつか光り輝く。": "Con người cũng như viên đá đó. Dù ban đầu bất cứ ai,<br>miễn là kiên trì thì sẽ tỏa sáng.",
    "……だけど、わたしのような力のない人間が<br>工兵なんてできるでありますでしょうか？": "……Nhưng, người yếu đuối như em<br>có thể làm kỹ sư được à?",
    "俺の見立てではできる。<br>どうだ？　俺の期待に応えるためにも工兵に挑戦してみないか？": "Theo ta thấy thì được.<br>Thử thách làm kỹ sư để đáp ứng kỳ vọng của ta thì sao?",
    "…………司令官殿！<br>わたし、やってみるであります！": "…………Thưa Chỉ Huy!<br>Em sẽ thử!",
    "よし、いい返事だ。": "Tốt, câu trả lời hay.",
    "盛り上がってるところ悪いが、司令官さんよ。<br>おれたちは、そのお嬢ちゃんを連れてくなんて認めてないぜ？": "Xin lỗi làm phiên lúc mọi người hào hứng, thưa Chỉ Huy.<br>Nhưng chúng tôi không đồng ý mang cô bé đó theo đâu?",
    "こいつはお前たちにできないことができる。<br>それを証明するための機会ぐらいくれてもいいだろ？": "Cô ấy làm được điều các cậu không làm được.<br>Cho một cơ hội để cô ấy chứng minh thì sao?",
    "まずは１度ベティにやらせてみて、それから判断しろ。": "Để Betty thử một lần, sau đó mới quyết định.",
    "それとも、工兵隊ってのはベティ１人いるだけで実力が<br>発揮できなくなるようなボンクラばかりか？": "Hay là Đội Kỹ Sư chỉ toàn vô dụng, chỉ cần có Betty là không làm được gì?",
    "おれたちをなめてるのか！？<br>あんたが司令官だからって、なんでも黙って聞いてると思うなよ！": "Các cậu khỉnh thường chúng tôi à!?<br>Đừng nghĩ cậu là Chỉ Huy gì đó nghe lời!",
    "ああ、そうさせてもらおうか。さっそく大穴に向かおう。<br>行くぞ、ベティ。": "Ứ, ta chấp nhận. Đi thẳng Đại Huyết ngay.<br>Đi thôi, Betty.",
    "は、はい！": "V-vâng!",
    "司令官さん……本気ですか？": "Thưa Chỉ Huy…… nói thật à?",
    "もちろんだ。": "Tất nhiên.",
    "……そこまで言うなら、止めはしませんがね。<br>お嬢ちゃんの面倒は、司令官さんがみてくださいよ。": "……Nói vậy thì không cán nữa.<br>Cô bé đó Chỉ Huy tự lo nhé.",
    "本当におれたちよりも仕事ができるか、証明してもらおうじゃねぇか！<br>手始めに、そこの残土を外に出してもらうぜ！": "Chứng minh xem có làm tốt hơn chúng tôi không!<br>Trước hết, đào đống đất đó ra ngoài!",
    "採掘してるといくらでも土や石が出てくるからな。<br>これを運び出すだけでも相当体力がいる。お嬢ちゃんにできるのか？": "Khai thác ra bao nhiêu đất đá cũng có.<br>Chỉ vác ra ngoài cũng mệt lắm. Cô bé làm được à?",
    "すごい量の土でありますな……。石もたくさん混ざっているであります。<br>これを限られた人数で運んで捨てるのは骨が折れるであります。": "Đất nhiều lắm ạ……. Đá cũng lắn nhiều.<br>Ít người vác đi ném rất khổ ạ.",
    "……おや？<br>こ、これはまさか……！？": "……Ồ?<br>C-có thể là……!?",
    "なんだぁ？　石なんかつかんでどうした？<br>運び出せねぇなら降参していいんだぜ？　くくく……": "Này? Cằm đá làm gì?<br>Không vác được thì chụi thua đi? Kuhuhu……",
    "どうした、ベティ？": "Sao rồi, Betty?",
    "司令官殿、これは……。<br>これは、宝の山でありますっ！": "Thưa Chỉ Huy, đây là…….<br>Đây là nuí vàng ngân ạ!",
    "宝の山？": "Nuí vàng ngân?",
    "こうしてはいられません！<br>わたし、ちょっと行ってくるであります！": "Không thể đừng yên!<br>Em đi một chút ạ!",
    "なんだぁ、あのお嬢ちゃん。石を１個だけ持って走っていっちまった。<br>ギブアップってことか？": "Cô bé kia sao? Chỉ cằm một viên đá chạy đi.<br>Đó là bỏ cuộc à?",
    "司令官さん、どうするんです？<br>あんたの連れてきたお嬢ちゃんは逃げちまいましたけど。": "Thưa Chỉ Huy, làm sao?<br>Cô bé cậu mang theo đã chạy rồi.",
    "少し待っていてくれ。": "Chờ một chút.",
    "はぁ。まあ、おれたちは構いませんがね。<br>どのみち、仕事はするつもりでしたから。……お前ら、仕事を始めるぞ。": "Hàa. Mà, chúng tôi không quan tâm.<br>Đường nào, việc cũng làm…… Các cậu, bắt đầu làm việc.",
    "分かってるよ！　てめぇが指示だしてんじゃねぇ！": "Biết rồi! Đừng phải cậu ra chỉ điển!",
    "（さっきのベティの顔……あれは、何かを確信している表情だった。<br>だとしたら、きっと何か考えがあるはずだ）": "(Khuôn mặt Betty vừa rồi…… đó là biểu tưởng tin tưởng. Nếu vậy, chắc có cách.)",
    "おいっ、こっちに土をよこすんじゃねぇ！<br>邪魔だろうが！": "Này! Đừng đẩy đất qua đây!<br>Cản trởng rồi!",
    "けっ、てめぇに指図されるいわれなんざねぇな！<br>おれの勝手だ！": "Khét, không cần cậu chỉ độ!<br>Tao làm tùy ý!",
    "（本当に頑固者ぞろいなんだな。<br>確かに、ちょっとやそっとじゃまとまりそうにない）": "(Thật sự là nhần kiên nhiều.<br>Chắc chắn, chỉ với chút đó không gộp được.)",
    "司令官さん。いつまで待つ気ですか？<br>どうせあのお嬢ちゃんは戻って来やしないでしょう。": "Thưa Chỉ Huy, chờ đến khi nào?<br>Đường nào cô bé kia quay lại đâu.",
    "いや、そうでもないさ。<br>……ほら、ちょうど戻ってきた。": "Không, cũng không.<br>……Này, vừa quay lại.",
    "司令官殿、お待たせしたであります！": "Thưa Chỉ Huy, để chồ ở ạ!",
    "さあさあ皆さん！　こっちでありますよ～！<br>宝の山はこっちです！": "Sào sào mọi người! Ở đây ạ〜!<br>Nuí vàng ngân ở đây!",
    "おおっ、これですか、ベティさん！": "Oá, cái này à, Betty!",
    "さっき見せたルビーの原石はこの残土の中に混じっているであります！<br>掘りだしたものはお手頃価格で売るでありますよ～！": "Nguyên thạch Ruby vừa rói là trong đống đất này ạ!<br>Đất được sẽ bán giá tốt ạ〜!",
    "さあさあ、早いもの勝ちでありますよー！<br>もってけドロボ～！　お代はちゃんといただきますけど！": "Sào sào, nhanh tay được ở đầy!<br>Mang đi, trốm đi! Tiền thì tính kỹ!",
    "おおっ、それは素晴らしい！<br>よし、この残土をまるごと運び出すぞ！": "Oá, tuyệt vời!<br>Yoshi, vác hết đống đất này ra!",
    "ど、どういうことだ、こりゃ？<br>お嬢ちゃんの連れてきた連中が、残土を運び出していく……？": "Đố, điều gì thế?<br>Bạn của cô bé vắc hết đất ra ngoài……?",
    "嘘だろ……。<br>あっという間に、残土がなくなっちまった……": "Nờ đâu…….<br>Nhất một phía, đất hết sạch……",
    "どういうことです……？": "Đây là chuyện gì……?",
    "あの残土の中にはルビーの原石が混ざっていたであります。": "Trong đống đất đó lắn nguyên thạch Ruby ạ.",
    "わたしはそれを商人さんに見せて、<br>残土ごと運び出してくれたらお手頃価格で譲ると約束したであります。": "Em cho thương nhân xem,<br>hú vác hết đống đất đi thì bán giá tốt ạ.",
    "司令官殿、事後承諾になってしまって申し訳ないであります。": "Thưa Chỉ Huy, xin lỗi vì chỉ báo cáo sau ạ.",
    "いや、構わない。": "Không sao.",
    "それと、ルビーの代金の清算が終わったみたいだ。<br>代金の一部は後ほど工兵たちに臨時給料として支払おう。": "Còn tiền Ruby đã thanh toán xong.<br>Một phần trả cho kỹ sư làm thưởng.",
    "え？　いいんですかい……？": "Ê? Được à……?",
    "ああ、工兵のベティが稼いだようなもんだからな。<br>れっきとした工兵の手柄だ。": "Ứ, do kỹ sư Betty kiếm được.<br>Là chiến công của Đội Kỹ Sư.",
    "むう……": "Mụ……",
    "それにしてもベティ、お前の手際には驚いたぞ。<br>商人に顔が利くとは思わなかった。": "Betty, tài tình của cậu khiến ta ngạc nhiên.<br>Không ngờ cậu quen thương nhân.",
    "商人さんとは、消耗品や食材を仕入れる時に顔見知りになっていたであります！<br>主計兵の経験が意外なところで活きたであります！": "Thương nhân quen khi em mua vật tư, thực phẩm ạ!<br>Kinh nghiệm quân nhu dùng được nơi không ngờ ạ!",
    "なるほどな。今までの人脈を活用したわけか。<br>見事な機転だ。": "Hiểu rồi. Dùng mối quan hệ cũ.<br>Phấn ứng nhanh nhạy.",
    "えへへ～、そう言われると照れてしまうであります～♪": "Ehehe〜, được khen thì ngậi ạ〜♪",
    "（趣味である石に関わる仕事なら、と思っての任命だったが<br>まさかここまで合致するとはな……）": "(Nhân việc liên quan đến đá - sớ thích của cô, ta giao cho cô.<br>Không ngờ hợp đến vậy……)",
    "司令官殿！<br>わたし、少しだけど自信が持てたであります！": "Thưa Chỉ Huy!<br>Em có chút tự tin ạ!",
    "そりゃよかった。<br>これからも期待しているぞ。": "Tốt lắm.<br>Tiếp tục kỳ vọng.",
    "はいっ！　司令官殿！": "Vâng! Thưa Chỉ Huy!",
}

# Title case helper for Vietnamese
def to_vietnamese_title_case(text):
    # Keep tags like <br> intact, capitalize words
    def cap_word(match):
        word = match.group(0)
        if word.startswith('<'):
            return word
        return word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper()
    return re.sub(r'<[^>]+>|[\w\']+', cap_word, text)

def preserve_br_structure(en_text_field, vi_translation):
    """
    Ensure VI translation has same <br> tag structure as EN text field.
    EN asset is the authority for <br> count and positions.
    """
    en_br_count = en_text_field.count('<br>')
    vi_br_count = vi_translation.count('<br>')
    
    if en_br_count == vi_br_count:
        return vi_translation
    
    # EN has more <br> than VI - need to insert <br> into VI
    # Strategy: split EN by <br>, split VI by sentences/clauses, interleave
    # For simplicity: if EN has <br> and VI has none, add <br> at the position
    # of the first sentence break in VI (after 。 or 。 or after reasonable length)
    if en_br_count > vi_br_count:
        # Find a good spot to insert <br> - after first sentence end
        # Look for 。 or 。 or ！ or ？ in VI
        for punct in ['。', '？', '！', '.', '?', '!']:
            idx = vi_translation.find(punct)
            if idx > 10:  # Not at start
                # Insert <br> after punctuation
                return vi_translation[:idx+1] + '<br>' + vi_translation[idx+1:]
        # Fallback: insert at middle
        mid = len(vi_translation) // 2
        # Find nearest space
        space_idx = vi_translation.find(' ', mid)
        if space_idx > 0:
            return vi_translation[:space_idx] + '<br>' + vi_translation[space_idx:]
        return vi_translation[:mid] + '<br>' + vi_translation[mid:]
    
    # VI has more <br> than EN - remove excess (shouldn't happen with our translations)
    return vi_translation

# Load EN asset file
en_path = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt")
en_raw = en_path.read_bytes()
en_text = en_raw.decode("utf-8-sig")
en_lines = en_text.splitlines(True)  # keep line endings

# Build JP keys list in order (from ja.json - matches EN asset text records)
ja_keys = list(TRANSLATIONS.keys())

# Now rebuild VI file by replacing text fields
vi_lines = []
text_record_idx = 0

# Commands that have text field to translate
TEXT_CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")

for line in en_lines:
    clean = line.lstrip('\ufeff').rstrip('\r\n')
    if any(clean.startswith(cmd) for cmd in TEXT_CMDS):
        # This is a text record - replace the text field
        if clean.startswith("title,"):
            # title,TEXT
            parts = clean.split(",", 1)
            if len(parts) == 2:
                if text_record_idx < len(ja_keys):
                    jp_key = ja_keys[text_record_idx]
                    vi_text = TRANSLATIONS.get(jp_key, parts[1])
                    # Title Case for title field
                    vi_text = to_vietnamese_title_case(vi_text)
                    # Preserve <br> structure from EN asset
                    vi_text = preserve_br_structure(parts[1], vi_text)
                    new_line = parts[0] + "," + vi_text
                else:
                    new_line = clean
            else:
                new_line = clean
        else:
            # message,Speaker,Text,ID,Voice,Chara (6 fields max split)
            parts = clean.split(",", 5)
            if len(parts) >= 3:
                if text_record_idx < len(ja_keys):
                    jp_key = ja_keys[text_record_idx]
                    vi_text = TRANSLATIONS.get(jp_key, parts[2])
                    # Replace ASCII commas in Vietnamese text with U+201A
                    vi_text = vi_text.replace(",", "‚")
                    # Preserve <br> structure from EN asset
                    vi_text = preserve_br_structure(parts[2], vi_text)
                    parts[2] = vi_text
                    new_line = ",".join(parts)
                else:
                    new_line = clean
            else:
                new_line = clean
        
        # Preserve original line ending
        ending = line[len(line.rstrip('\r\n')):]
        vi_lines.append(new_line + ending)
        text_record_idx += 1
    else:
        # Non-text line, keep as-is
        vi_lines.append(line)

print(f"Processed {text_record_idx} text records")

# Write VI output
vi_dir = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle")
vi_dir.mkdir(parents=True, exist_ok=True)
vi_path = vi_dir / "hmn_10500100002.txt"

# Preserve BOM and newline style
vi_content = "".join(vi_lines)
has_bom = en_raw.startswith(b'\xef\xbb\xbf')
vi_bytes = (b'\xef\xbb\xbf' + vi_content.encode('utf-8')) if has_bom else vi_content.encode('utf-8')
vi_path.write_bytes(vi_bytes)

print(f"Written VI asset to {vi_path}")
print(f"BOM preserved: {has_bom}")
newline_style = 'CRLF' if b'\r\n' in en_raw else 'LF'
print(f"Newline style preserved: {newline_style}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete translation script for hmn_10500100002
Builds JP->VI map, EN->JP reverse map, translates asset file.
"""

import json
import os

# File paths
JA_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/ja.json"
EN_JSON = "E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100002/en.json"
EN_ASSET = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
VI_OUTPUT = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100002.txt"
VI_JSON_OUT = "E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100002_full/vi.json"

# Vietnamese translations for JP keys (from ja.json)
JP_TO_VI = {
    "工兵隊員ベティ": "Kỹ Sư Quân Đội Betty",
    "邪魔するぞ。": "Tôi đến làm phiền chút.",
    "ん？　……なんだ、司令官さんか。": "Này? …À, hóa ra là Chỉ Huy quan à.",
    "現場の状況を確認しに来たぞ。": "Ta đến xem tiến độ công trường.",
    "そんなことですかい。<br>それより今月分の給料、ちと少なくないですかね？": "Chuyện đó à?<br>Hơn nữa tiền lương tháng này, có hơi ít không?",
    "給料が少ない？<br>それはお前たち自身の責任だろう。": "Lương ít?<br>Đó là lỗi của các bạn mình chứ.",
    "とっくに終わってなきゃならない掘削工事が<br>まだ終わっていないんだからな。": "Công trình khai thác đã lâu phải xong<br>mà đến giờ vẫn chưa xong.",
    "素人はこれだからいけねえ。<br>現場は大量の石に埋もれて簡単には作業を進められねえんだ。": "Người ngoài hành nghề mới nói chuyện dễ như vậy.<br>Công trường bị chôn vùi bởi khối lượng đá lớn, không thể tiến hành dễ dàng.",
    "言い訳はいい。給料が欲しければ、しっかり仕事に集中しろ。<br>人手が足りてないわけじゃないはずだ。": "Đừng biện minh. Muốn lương thì tập trung làm việc.<br>Không phải thiếu người đâu.",
    "素人が余計な口挟まないでくれよ！<br>こっちにはこっちのやりかたがあるんだからよ！": "Người ngoài hành nghề đừng can thiệp!<br>Chúng tôi có cách làm của mình!",
    "……１人１人と話してもらちが明かないな。<br>代表者……隊長はまだ決まっていないのか？": "…Nói chuyện với từng người một không xong khi nào.<br>Đại diện… Trưởng đội còn chưa định à?",
    "隊長ってやつは、誰よりも腕がたたなきゃいけないんでね。<br>誰もかれもが、自分が１番の腕利きだって譲らないんですよ。": "Trưởng đội phải giỏi hơn bất kỳ ai.<br>Ai nấy đều tự cho mình giỏi nhất, không ai nhường ai.",
    "ったりめぇだ！<br>自分より下手なやつの下につけるか！": "Tất nhiên!<br>Tao không chịu dưới tay kẻ kém hơn tao!",
    "へっ！　だったらてめぇこそ出る幕はないな。<br>隊長はおれがやるべきだ。": "Héc! Cái đó thì cậu cũng không có phần.<br>Trưởng đội phải là tao.",
    "いいや、おれだね。おれはもっとでかい現場を経験してんだ。<br>てめぇらがおれの指揮に従ってれば、１番効率よく作業が進む。": "Không, là tao. Tao đã trải qua công trường lớn hơn.<br>Nếu các ngươi nghe lệnh tao, công việc sẽ tiến triển hiệu quả nhất.",
    "なんだと！？": "Cái gì!?",
    "上等だ！　今日こそどっちが腕利きか、白黒つけて――": "Tuyệt! Hôm nay sẽ phân định rõ ai giỏi hơn—",
    "いい加減にしろ！<br>ガキじゃあるまいし、喧嘩の腕っ節で競ってどうする！": "Đừng nói đùa!<br>Không phải trẻ con, tranh giành bằng bạo lực để làm gì!",
    "……それじゃあ、どうしろって言うんです？<br>まさか、司令官さんが隊長を決めてくれるとでも？": "…Thế thì phải làm sao?<br>Không phải Chỉ Huy quan muốn tự chọn Trưởng đội chứ?",
    "どうせそれじゃあ納得しないだろ。隊長の問題は後回しだ。<br>それより、今日はおもしろいやつを紹介しに来た。": "Chắc chắn các ngươi không chấp nhận. Vấn đề Trưởng đội để sau.<br>Hôm nay ta đến giới thiệu một người thú vị.",
    "おもしろいやつ……？": "Người thú vị…?",
    "ベティ、入ってこい。": "Betty, vào đây.",
    "し、失礼するでありますー……": "Th-thưa, em xin phép…",
    "……誰ですかい、このお嬢さんは？": "…Cô gái này là ai?",
    "ミレスガルド出身の志願兵、ベティだ。": "Là tình nguyện viên từ Millesgard, Betty.",
    "よ、よろしくお願いするであります。": "Th-thưa em, mong được hợp tác.",
    "ベティにはここの工兵隊に所属してもらう。": "Betty sẽ gia nhập đội Kỹ Sư Quân Đoàn này.",
    "はい、今日からここの工兵隊に……え？": "Vâng, từ hôm nay em ở đội Kỹ Sư Quân… à?",
    "えぇえええええええ～～～～～～！？<br>き、聞いてないでありますよぉっ！": "Eeeeeeeeeeeeeeeee!?<br>K-không nghe nói đâu ạ!",
    "今、初めて言ったからな。こいつらの仕事は大穴での採掘作業だ。": "Vừa nói thôi. Việc của bọn chúng là khai thác ở Hố Lớn.",
    "さ、採掘現場で働けるでありますか！？": "C-có thể làm tại hiện trường khai thác ạ!?",
    "ああ。お前の好きな石に１日中触っていられるぞ。<br>どうだ？　惹かれないか？": "À. Em có thể chạm vào đá yêu thích cả ngày.<br>Thế nào? Có hứng thú không?",
    "そ、それは確かに魅力的でありますが……": "Đ-đó thật hấp dẫn ạ, nhưng…",
    "で、でも！　やっぱり無理でありますよう！": "Nh-nhưng! Vẫn không được ạ!",
    "ギャハハハハハハハハ！": "Gya ha ha ha ha ha ha ha!",
    "おいおいおいおい！　こりゃなんかの冗談かぁ？": "Oi oi oi oi! Cái này trò đùa à?",
    "そんなお嬢ちゃんに工兵が務まるかっての！<br>その細腕じゃハンマーも持てないだろうよ！": "Cô bé kia làm Kỹ Sư Quân à!<br>Cánh tay gầy như đó đỡ búa được à?",
    "……司令官殿、皆さんの言うとおりであります。<br>わたしに工兵なんて務まるわけ――": "…Thưa Chỉ Huy quan, như mọi người nói ạ.<br>Em làm Kỹ Sư Quân…",
    "ベティ。お前が磨いた石ころを思い出すんだ。": "Betty. Hãy nhớ tới viên đá em đánh bóng.",
    "わたしが磨いた石ころ……？": "Viên đá em đánh bóng…?",
    "ああ。あの石は最初、何の変哲もない泥に覆われたただの石ころだった。<br>だけどお前が根気よく磨いたお陰で宝石みたい輝くようになっただろ？": "À. Viên đá đó ban đầu chỉ là sỏi lấm tấm lót bùn.<br>Nhưng nhờ em kiên nhẫn đánh bóng, nó lóng lánh như đá quý đúng không?",
    "人もあの石ころと同じだ。最初はどんなにダメな人間だって<br>頑張り続ければいつか光り輝く。": "Con người cũng như viên đá ấy. Dù ban đầu có vô giá cỡ nào,<br>miễn kiên trì thì sẽ tỏa sáng.",
    "……だけど、わたしのような力のない人間が<br>工兵なんてできるでありますでしょうか？": "…Nhưng, người yếu đuối như em<br>có thể làm Kỹ Sư Quân được ạ?",
    "俺の見立てではできる。<br>どうだ？　俺の期待に応えるためにも工兵に挑戦してみないか？": "Theo ta thấy thì được.<br>Thế nào? Để đáp ứng kỳ vọng của ta, thử thách làm Kỹ Sư Quân đi.",
    "…………司令官殿！<br>わたし、やってみるであります！": "…………Thưa Chỉ Huy quan!<br>Em sẽ thử!",
    "よし、いい返事だ。": "Ừ, trả lời hay.",
    "盛り上がってるところ悪いが、司令官さんよ。<br>おれたちは、そのお嬢ちゃんを連れてくなんて認めてないぜ？": "Xin lỗi làm phiền lúc đang hứng, Chỉ Huy quan.<br>Chúng tôi không chấp nhận việc mang cô bé đó đi cùng.",
    "こいつはお前たちにできないことができる。<br>それを証明するための機会ぐらいくれてもいいだろ？": "Cô ấy làm được việc các ngươi không làm được.<br>Cho cơ hội chứng minh đó chứ?",
    "まずは１度ベティにやらせてみて、それから判断しろ。": "Để Betty thử một lần, sau đó mới kết luận.",
    "それとも、工兵隊ってのはベティ１人いるだけで実力が<br>発揮できなくなるようなボンクラばかりか？": "Hay đội Kỹ Sư Quân chỉ vì có Betty một mình mà không thể phát huy thực lực?",
    "おれたちをなめてるのか！？<br>あんたが司令官だからって、なんでも黙って聞いてると思うなよ！": "Khinh thường chúng tôi à!?<br>Đừng nghĩ vì cậu là Chỉ Huy quan mà gì cũng im lặng nghe!",
    "ああ、そうさせてもらおうか。さっそく大穴に向かおう。<br>行くぞ、ベティ。": "À, ta sẽ làm như vậy. Đi thẳng Hố Lớn ngay.<br>Đi thôi, Betty.",
    "は、はい！": "V-vâng!",
    "司令官さん……本気ですか？": "Chỉ Huy quan… nói thật à?",
    "もちろんだ。": "Tất nhiên.",
    "……そこまで言うなら、止めはしませんがね。<br>お嬢ちゃんの面倒は、司令官さんがみてくださいよ。": "…Nói như vậy thì không cản. Nhưng cô bé đó, Chỉ Huy quan tự lo nhé.",
    "本当におれたちよりも仕事ができるか、証明してもらおうじゃねぇか！<br>手始めに、そこの残土を外に出してもらうぜ！": "Chứng minh xem có làm tốt hơn chúng tôi không!<br>Đầu tiên, đưa đống đất thừa kia ra ngoài!",
    "採掘してるといくらでも土や石が出てくるからな。<br>これを運び出すだけでも相当体力がいる。お嬢ちゃんにできるのか？": "Khai thác thì đất đá không ngừng ra.<br>Chỉ vận chuyển cũng tốn sức lớn. Cô bé làm được à?",
    "すごい量の土でありますな……。石もたくさん混ざっているであります。<br>これを限られた人数で運んで捨てるのは骨が折れるであります。": "Lượng đất khổng lồ ạ…. Đá cũng lẫn nhiều.<br>Vận chuyển với ít người như này rất vất vả.",
    "……おや？<br>こ、これはまさか……！？": "…Này?<br>K-không lẽ…!?",
    "なんだぁ？　石なんかつかんでどうした？<br>運び出せねぇなら降参していいんだぜ？　くくく……": "Nà? Cầm đá làm gì?<br>Không chịu được thì xin thua cũng được? Kukuku…",
    "どうした、ベティ？": "Sao rồi, Betty?",
    "司令官殿、これは……。<br>これは、宝の山でありますっ！": "Thưa Chỉ Huy quan, đây…<br>Đây là núi kho báu ạ!",
    "宝の山？": "Núi kho báu?",
    "こうしてはいられません！<br>わたし、ちょっと行ってくるであります！": "Không thể ngồi yên!<br>Em đi chút rồi về ạ!",
    "なんだぁ、あのお嬢ちゃん。石を１個だけ持って走っていっちまった。<br>ギブアップってことか？": "Cô bé kia sao? Chỉ cầm 1 viên đá chạy đi.<br>Có phải xin thua không?",
    "司令官さん、どうするんです？<br>あんたの連れてきたお嬢ちゃんは逃げちまいましたけど。": "Chỉ Huy quan, định sao?<br>Cô bé cậu mang đi đã trốn.",
    "少し待っていてくれ。": "Chờ chút.",
    "はぁ。まあ、おれたちは構いませんがね。<br>どのみち、仕事はするつもりでしたから。……お前ら、仕事を始めるぞ。": "Hà. Mà, chúng tôi không quan tâm.<br>Đâu vào đường, định làm việc thôi…. Các ngươi, bắt đầu làm!",
    "分かってるよ！　てめぇが指示だしてんじゃねぇ！": "Biết rồi! Đừng phải cậu ra lệnh!",
    "（さっきのベティの顔……あれは、何かを確信している表情だった。<br>だとしたら、きっと何か考えがあるはずだ）": "(Mặt Betty lúc nãy… đó là biểu情 xác tín. Nếu vậy, chắc có kế hoạch.)",
    "おいっ、こっちに土をよこすんじゃねぇ！<br>邪魔だろうが！": "Oi, đừng ném đất sang đây!<br>Cản đường à!",
    "けっ、てめぇに指図されるいわれなんざねぇな！<br>おれの勝手だ！": "Khiếc, không cần cậu chỉ đạo!<br>Tao làm gì tùy tao!",
    "（本当に頑固者ぞろいなんだな。<br>確かに、ちょっとやそっとじゃまとまりそうにない）": "(Thật sự là bọn cứng đầu.<br>Chắc chắn, chút chút không gom được.)",
    "司令官さん。いつまで待つ気ですか？<br>どうせあのお嬢ちゃんは戻って来やしないでしょう。": "Chỉ Huy quan. Chờ đến khi nào?<br>Đâu vào đường cô bé đó quay lại.",
    "いや、そうでもないさ。<br>……ほら、ちょうど戻ってきた。": "Không, không phải.<br>…Này, vừa quay lại.",
    "司令官殿、お待たせしたであります！": "Thưa Chỉ Huy quan, để chờ ạ!",
    "さあさあ皆さん！　こっちでありますよ～！<br>宝の山はこっちです！": "Đi nào mọi người! Ở đây ạ~!<br>Núi kho báu ở đây!",
    "おおっ、これですか、ベティさん！": "Oh! Cái này à, Betty!",
    "さっき見せたルビーの原石はこの残土の中に混じっているであります！<br>掘りだしたものはお手頃価格で売るでありますよ～！": "Viên ruby thô lúc nãy lẫn trong đất thừa này ạ!<br>Đào ra sẽ bán giá hợp lý ạ~!",
    "さあさあ、早いもの勝ちでありますよー！<br>もってけドロボ～！　お代はちゃんといただきますけど！": "Đi nào, nhanh tay được rồi ạ~!<br>Cướp đi kẻ cướp~! Tiền thì thu đầy đủ!",
    "おおっ、それは素晴らしい！<br>よし、この残土をまるごと運び出すぞ！": "Oh, tuyệt vời!<br>Yoshi, vận chuyển hết đống đất thừa!",
    "ど、どういうことだ、こりゃ？<br>お嬢ちゃんの連れてきた連中が、残土を運び出していく……？": "Đ-dЭто gì cơ?<br>Bạn cùng cô bé mang đi vận chuyển đất thừa…?",
    "嘘だろ……。<br>あっという間に、残土がなくなっちまった……": "Náo à…. Trong chớp mắt, đất thừa mất sạch…",
    "どういうことです……？": "Đang làm gì vậy…?",
    "あの残土の中にはルビーの原石が混ざっていたであります。": "Đất thừa đó lẫn/ruby thô ạ.",
    "わたしはそれを商人さんに見せて、<br>残土ごと運び出してくれたらお手頃価格で譲ると約束したであります。": "Em cho thương nhân xem,<br>hứa nếu vận hết đất thừa thì bán giá hợp lý.",
    "司令官殿、事後承諾になってしまって申し訳ないであります。": "Thưa Chỉ Huy quan, xin lỗi vì xin phép sau ạ.",
    "いや、構わない。": "Không, không sao.",
    "それと、ルビーの代金の清算が終わったみたいだ。<br>代金の一部は後ほど工兵たちに臨時給料として支払おう。": "Và thanh toán tiền ruby xong. Phần tiền sẽ trả cho Kỹ Sư Quân làm thưởng.",
    "え？　いいんですかい……？": "E? Được à…?",
    "ああ、工兵のベティが稼いだようなもんだからな。<br>れっきとした工兵の手柄だ。": "À, là nhờ Kỹ Sư Quân Betty kiếm được. Là công lao chính đáng của Kỹ Sư Quân.",
    "むう……": "Mu…",
    "それにしてもベティ、お前の手際には驚いたぞ。<br>商人に顔が利くとは思わなかった。": "Dù sao, Betty, tài tình em khiến ta ngạc nhiên.<br>Không ngờ có mặt quen với thương nhân.",
    "商人さんとは、消耗品や食材を仕入れる時に顔見知りになっていたであります！<br>主計兵の経験が意外なところで活きたであります！": "Thương nhân, khi mua vật tiêu hao, thực phẩm quen mặt ạ!<br>Kinh nghiệm Quân Nhu bịch hoạt động kỳ diệu!",
    "なるほどな。今までの人脈を活用したわけか。<br>見事な機転だ。": "Thế à. Tận dụng mối quan hệ đến nay. Sự ứng biến tuyệt vời.",
    "えへへ～、そう言われると照れてしまうであります～♪": "Ehehe~, nói vậy em ngại ạ~♪",
    "（趣味である石に関わる仕事なら、と思っての任命だったが<br>まさかここまで合致するとはな……）": "(Nhiệm vụ liên quan đến đá - sở thích, nghĩ sẽ phù hợp<br>không ngờ hợp lý đến mức này……)",
    "司令官殿！<br>わたし、少しだけど自信が持てたであります！": "Thưa Chỉ Huy quan!<br>Em có chút tự tin ạ!",
    "そりゃよかった。<br>これからも期待しているぞ。": "Thế tốt. Tiếp tục mong chờ em.",
    "はいっ！　司令官殿！": "Vâng! Thưa Chỉ Huy quan!",
}

def normalize_for_matching(text):
    """Normalize text for matching: replace fullwidth chars with halfwidth"""
    # Replace fullwidth punctuation with halfwidth
    trans = str.maketrans({
        '，': ',',
        '。': '.',
        '！': '!',
        '？': '?',
        '～': '~',
        '　': ' ',
        '〈': '<',
        '〉': '>',
        '「': '"',
        '」': '"',
        '『': '"',
        '』': '"',
        '・': '·',
        '－': '-',
        '：': ':',
        '；': ';',
        '（': '(',
        '）': ')',
        '［': '[',
        '］': ']',
        '｛': '{',
        '｝': '}',
    })
    return text.translate(trans)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Loading JSON files...")
    ja_data = load_json(JA_JSON)
    en_data = load_json(EN_JSON)
    
    print(f"ja.json entries: {len(ja_data)}")
    print(f"en.json entries: {len(en_data)}")
    
    # Build EN->JP reverse map (normalize both for matching)
    en_to_jp = {}
    for jp_key, en_val in en_data.items():
        if en_val and en_val.strip():
            norm_en = normalize_for_matching(en_val.strip())
            en_to_jp[norm_en] = jp_key
    
    print(f"EN->JP map entries: {len(en_to_jp)}")
    
    # Build JP->VI map using our translations
    jp_to_vi = JP_TO_VI.copy()
    
    # Add any missing JP keys from ja.json with empty translation
    for jp_key in ja_data:
        if jp_key not in jp_to_vi:
            jp_to_vi[jp_key] = ""
    
    print(f"JP->VI map entries: {len(jp_to_vi)}")
    
    # Save vi.json
    os.makedirs(os.path.dirname(VI_JSON_OUT), exist_ok=True)
    with open(VI_JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(jp_to_vi, f, ensure_ascii=False, indent=4)
    print(f"Saved vi.json to {VI_JSON_OUT}")
    
    # Now translate the EN asset file
    print("\nReading EN asset file...")
    with open(EN_ASSET, 'r', encoding='utf-8-sig') as f:
        en_lines = f.readlines()
    
    print(f"EN asset lines: {len(en_lines)}")
    
    vi_lines = []
    translated_count = 0
    
    for i, line in enumerate(en_lines):
        # Preserve BOM and line endings
        if i == 0 and line.startswith('\ufeff'):
            line = line[1:]
            has_bom = True
        else:
            has_bom = False
        
        # Preserve CRLF
        ends_with_crlf = line.endswith('\r\n')
        ends_with_lf = line.endswith('\n')
        line = line.rstrip('\r\n')
        
        # Split into 6 fields
        parts = line.split(',', 5)
        if len(parts) == 6:
            # parts[2] is the text field (index 2)
            original_text = parts[2]
            norm_text = normalize_for_matching(original_text.strip())
            
            # Try to find translation
            vi_text = original_text
            if norm_text in en_to_jp:
                jp_key = en_to_jp[norm_text]
                if jp_key in jp_to_vi and jp_to_vi[jp_key]:
                    vi_text = jp_to_vi[jp_key]
                    # Preserve <br> suffix if present
                    if original_text.endswith('<br> ') and not vi_text.endswith('<br> '):
                        vi_text = vi_text + '<br> '
                    elif original_text.endswith('<br>') and not vi_text.endswith('<br>'):
                        vi_text = vi_text + '<br>'
                    elif original_text.endswith('<br> ') and vi_text.endswith('<br>'):
                        vi_text = vi_text + ' '
                    translated_count += 1
                else:
                    pass  # JP key found but no VI translation
            else:
                # Try partial matching for long texts
                pass
            
            parts[2] = vi_text
            new_line = ','.join(parts)
        else:
            new_line = line
        
        # Restore line ending
        if ends_with_crlf:
            new_line += '\r\n'
        elif ends_with_lf:
            new_line += '\n'
        
        vi_lines.append(new_line)
    
    print(f"Translated {translated_count} lines out of {len(en_lines)}")
    
    # Write VI output with BOM and CRLF
    os.makedirs(os.path.dirname(VI_OUTPUT), exist_ok=True)
    with open(VI_OUTPUT, 'w', encoding='utf-8-sig', newline='') as f:
        for line in vi_lines:
            f.write(line)
    
    print(f"Saved VI output to {VI_OUTPUT}")
    print(f"Line count match: {len(vi_lines)} == {len(en_lines)} -> {len(vi_lines) == len(en_lines)}")

if __name__ == '__main__':
    main()
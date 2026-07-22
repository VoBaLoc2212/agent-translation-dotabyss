#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build VI asset for hmn_10190100001 from JP-source EN asset, translating only text fields.

Strategy: per target line, replace the exact JP text-field substring with its VI
translation. All structural bytes (commas, tags, IDs, empty fields, trailing
delimiters) are preserved because only the inner text is replaced.
"""
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10190100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10190100001.txt"

# line_no -> (jp_key, vi_substitution)  (no ASCII commas inside vi text)
M = {
    25: ("見参！　前線基地の海賊娘！！",
         "Tiến Trận! Thiếu Nữ Hải Tặc Tiền Tuyến Căn Địa!!"),
    66: ("へっへっへ！　エルドラーナからの輸送隊か！<br>こいつは美味しい獲物だぜ！",
         "Hề hề hề! Một đoàn vận tải từ Eldorana sao! <br>Đồ này là chiến lợi phẩm ngon lành đây!"),
    77: ("運んでるもん、おとなしく全部おいていきな！<br>そうすりゃ命だけは助けてやらないこともないぜぇ？　ヒャハハ！",
         "Đồ các người đang chở‚ hãy ngoan ngoãn bỏ lại hết đi! <br>Làm vậy thì không phải là ta không tha mạng cho các người đâu nhé? Hyahaha!"),
    88: ("く、くそ……！<br>こんなところに野盗団がでるなんて……！",
         "Kh‚ khốn kiếp……! <br>Ai ngờ bọn cướp lại xuất hiện ở chốn này……!"),
    99: ("よ、よせ、抵抗するな！<br>悔しいが、輸送中の荷物を渡すしか……。",
         "K‚ khoan đã‚ đừng kháng cự! <br>Cay đắng thật nhưng chúng ta chỉ còn nước giao nộp hàng đang vận chuyển……."),
    110: ("ヒャハッ！<br>そうそう、変な気は起こさずに大人しく――。",
         "Hyahah! <br>Đúng rồi‚ ngoan ngoãn đứng yên‚ đừng nảy sinh ý định kỳ lạ――."),
    176: ("ひぃっ！？<br>お、おれの前髪が焦げちまったーーー！？",
         "Hỉ!? <br>M‚ mái tóc trước của ta cháy xém rồi―――!?"),
    195: ("今のは……銃弾！？<br>だ、誰だ！？　いったいどこから……！？",
         "Vừa rồi là…… đạn súng!? <br>A‚ ai đó!? Rốt cuộc từ đâu tới……!?"),
    219: ("――ここだ！", "――Ở đây!"),
    270: ("お……女ぁ！？", "O…… một cô gái!?"),
    279: ("おおっとぉ！　大人しくしてたほうが身のためだぞ。<br>アンタらが輸送隊に襲いかかるより、アタシの銃のほうが速い。",
         "Ôi chà! Các người nên ngoan ngoãn nếu muốn giữ mạng đấy. <br>Súng của ta bắn nhanh hơn bọn các người xông tới đoàn vận tải."),
    291: ("試してみるか？", "Muốn thử xem sao?"),
    302: ("ひいいいっ！！！", "Hỉỉiiii!!!"),
    380: ("なるほど、そんなことがあったのか。", "Ra là có chuyện như vậy."),
    389: ("はい！　そこからはルシータさんが護衛してくれて、<br>この前線基地まで問題なく辿り着けました。",
         "Vâng! Từ đó‚ Lucita đã hộ tống chúng tôi‚ <br>và chúng tôi đã đến tiền tuyến căn địa này mà không sự cố."),
    400: ("あれくらいお安いごようだよ。<br>アタシも前線基地にいくとこだったしさ。",
         "Chuyện nhỏ như vậy thôi. <br>Em cũng đang trên đường tới tiền tuyến căn địa mà."),
    411: ("義を見てせざるは勇無きなりってね！<br>おせっかいなのは、うちの血筋なんだ。",
         "'Thấy điều nghĩa mà không làm là không dũng cảm' đấy! <br>Ba má chuyện thiên hạ là dòng máu nhà em."),
    477: ("そういえば、おまえの先祖はエルドラーナ建国の<br>立役者って話だったな。",
         "Nhắc mới nhớ‚ tổ tiên của em từng là <br>nhân vật chủ chốt sáng lập Eldorana phải không."),
    488: ("そうさ！<br>アタシのご先祖さまは、伝説の海賊王！",
         "Đúng vậy! <br>Tổ tiên của em là Vua Hải Tặc huyền thoại!"),
    499: ("目指すはご先祖さまにも負けない、正義の海賊だっ！",
         "Em hướng tới là một hải tặc chính nghĩa không thua kém tổ tiên!"),
    510: ("ま、今は時代に合わせて商船の船長をやってるけどね。",
         "À‚ giờ em làm thuyền trưởng tàu thương mại cho hợp thời đại thôi."),
    515: ("正義の海賊か。おまえらしいな。<br>なんにしろ、物資はもちろん、人的被害がなくてよかった。",
         "Hải tặc chính nghĩa sao. Đúng như em. <br>Dù sao thì‚ vật tư thì khỏi nói‚ không có thương vong lại càng tốt."),
    517: ("おまえのおかげだ、ルシータ。ありがとうな。", "Là nhờ có em đấy‚ Lucita. Cảm ơn em."),
    528: ("へへっ、そんなに褒めるなよ～♪<br>褒めたって、なんにもでないぞ？",
         "Heheh‚ đừng khen em nhiều thế chứ~♪ <br>Có khen thì cũng chẳng được gì đâu?"),
    530: ("むしろこっちが謝礼のひとつでも出したいところだよ。<br>今度おまえのところの商船に、優先して依頼を振るとするか。",
         "Ngược lại‚ anh mới là người muốn đưa em chút quà cảm tạ. <br>Lần tới anh sẽ ưu tiên giao việc cho tàu thương mại của em."),
    541: ("ほんとかっ？　さっすが司令官、太っ腹ぁ♪<br>今後とも、うちの商会をよろしくー！",
         "Thật không? Đúng là Chỉ Huy‚ tâm hồn rộng lượng thật♪ <br>Về sau‚ hãy chiếu cố cho thương hội nhà em nhé!"),
    572: ("――数日後", "――Vài Ngày Sau"),  # inner of messageTextCenter <size> field
    624: ("お邪魔するよ～、司令官。", "Em xin phép làm phiền nhé~‚ Chỉ Huy."),
    626: ("ルシータか。どうしたんだ、急に？<br>今日はこれから、アウラと商談の予定なんだが。",
         "Lucita à. Sao đột ngột vậy‚ em? <br>Hôm nay anh có lịch bàn chuyện buôn bán với Aura."),
    682: ("いやいや、アタシのことは気にしないでよ。<br>それよりごめんな、せっかく時間空けてもらってたのにさ。",
         "Thôi thôi‚ đừng bận tâm đến em làm gì. <br>Dù sao cũng xin lỗi anh‚ đã trân trọng dành thời gian mà em lại thế này."),
    660: ("そのアウラなんだけど、急に議会の仕事でこれなくなっちゃったんだ。<br>アタシはその伝言役ってわけ。",
         "Về Aura đó‚ cô ấy đột nhiên có việc hội đồng nên không tới được. <br>Em tới làm người đưa lời nhắn."),
    662: ("ああ、そういうことか。それはわざわざご苦労だったな。", "À‚ ra là vậy. Em đã khó nhọc chạy tới tận đây."),
    684: ("まあ、無理もないだろ。<br>エルドラーナの評議会の議員ともなれば、急用も多いだろうし。",
         "Thôi‚ cũng không trách được. <br>Làm nghị viên hội đồng Eldorana thì việc gấp nhiều là cái chắc."),
    693: ("そうみたい。ま、あいつは少し苦労するくらいが<br>ちょうどいいんだ。",
         "Có vẻ vậy. À‚ một chút vất vả như thế <br>với cô ta lại vừa đẹp."),
    695: ("なんだ、珍しく辛らつだな。アウラが嫌いか？", "Sao thế‚ hôm nay mắng mỏ ghê gớm thế. Em ghét Aura à?"),
    704: ("嫌い、っていうのとはちょっと違うけどさ。<br>アウラのやつ、昔からアタシにちょっかいかけてくるんだよな。",
         "Không hẳn là ghét đâu. <br>Cái Aura đó từ xưa đã hay trêu chọc em."),
    706: ("ちょっかい？", "Trêu chọc em à?"),
    756: ("そうそう！<br>小さい頃なんか、お化けのカッコして脅かしてきたんだぞ！",
         "Đúng rồi! <br>Lúc nhỏ‚ nó còn giả ma để dọa em nữa!"),
    767: ("それ以来、アタシお化けが苦手でさー。", "Từ đó‚ em vốn dĩ đã sợ ma rồi."),
    769: ("なんだ、ルシータはお化けが苦手なのか。<br>意外な弱点だな。",
         "Hả‚ ra là Lucita sợ ma. <br>Điểm yếu bất ngờ đấy."),
    780: ("あ、言っとくけど、脅かされたのは、うんと小さい時のことだからな！",
         "Á‚ nói cho rõ là hồi đó em còn bé tí xíu thôi!"),
    782: ("そうなのか？", "Thế à?"),
    794: ("ああ！　今はもうお化けなんて怖くもなんともないぞ！", "Ừ! Giờ em chẳng sợ ma tí nào nữa!"),
    808: ("……たぶん。", "……Chắc vậy."),
    842: ("……ごほん！　それより司令官。今日の商談って、急ぎか？<br>なんだったら、アタシが代わりに聞いておこうか？",
         "……A-hem! Quan trọng hơn‚ Chỉ Huy. Cuộc bàn chuyện hôm nay có gấp không? <br>Nếu không thì để em nghe thay anh nhé?"),
    844: ("ルシータが？", "Lucita á?"),
    863: ("エルドラーナの人間として、顧客に不自由させるわけにはいかないしさ。",
         "Là người Eldorana‚ em không thể để khách hàng thiếu thốn được."),
    874: ("それとも……アタシじゃ、ダメかな？", "Hay là…… để em thì không được sao?"),
    876: ("…………。", "............"),
    887: ("あっ、いや！　ダメならいいんだ！<br>気にしないでくれ！",
         "Á‚ không! Không được thì thôi! <br>Đừng bận tâm về em!"),
    898: ("やっぱ、実績のあまりないアタシじゃ大きな取引は任せられないよな……。",
         "Như vậy thì‚ em ít thành tích quá nên không được giao dịch lớn đâu……."),
    900: ("いや、そんなことはない。<br>むしろ、今回はルシータが適任かもしれないな。",
         "Không‚ không phải vậy. <br>Trái lại‚ lần này Lucita có khi lại là người thích hợp đấy."),
    911: ("え？<br>アウラより、アタシのほうがいいのか……？",
         "Ê? <br>Em còn tốt hơn Aura sao……?"),
    913: ("驚くほどのことじゃないだろ。確かにアウラは確かに頭がいいし優秀なんだが、<br>なにかと余計なことをするだろ？",
         "Có gì đáng kinh ngạc đâu. Đúng là Aura thông minh và xuất sắc thật‚ <br>nhưng cô ta lúc nào chẳng làm thừa chuyện chứ?"),
    915: ("あいつの思いつきで、何度めんどくさいトラブルが起こったことか……。",
         "Biết bao lần ý thích nảy ra của cô ta gây ra rắc rối phiền phức……."),
    926: ("それはよく分かる。……いや、ほんとよく分かるよ。<br>司令官も苦労してるんだな。",
         "Em hiểu rõ điều đó…… Không‚ em thực sự rất hiểu. <br>Chỉ Huy cũng vất vả nhỉ."),
    928: ("その点、ルシータは堅実な仕事をしてくれるからな。<br>安心して依頼できる。",
         "Về điểm đó‚ Lucita làm việc rất chắc chắn. <br>Anh yên tâm giao việc cho em."),
    939: ("ほ、ほんとか？<br>アタシ、そんなこと言われたことないぞ……？",
         "R‚ rồi hả? <br>Chưa ai từng nói với em như vậy……?"),
    941: ("他人の評価など当てになるか。<br>俺は俺の目で見て、仕事相手を選ぶ。",
         "Đánh giá của thiên hạ làm gì có mà tin. <br>Anh chọn đối tác bằng chính mắt mình."),
    950: ("…………。", "............"),
    962: ("へへっ♪　そっかそっか～♪", "Heheh♪ Em hiểu rồi‚ em hiểu rồi~♪"),
    973: ("よーし！　そういうことなら、なんでも言ってくれ！<br>司令官からの仕事なら、最優先で受けるよ！",
         "Ưu! Đã thế thì‚ cứ việc sai bảo em gì cũng được! <br>Là việc từ Chỉ Huy thì em nhận ưu tiên tối cao!"),
    984: ("あっ、でも報酬はちゃんともらうぞ？<br>アタシは船のみんなの生活を守らなきゃいけないからなっ。",
         "Á‚ nhưng em vẫn thu đàng hoàng thù lao nhé? <br>Vì em phải lo cuộc sống cho mọi người trên tàu!"),
    986: ("もちろんだ。責任をもって仕事をするんだから、<br>正当な対価を払うのは当然だ。",
         "Đương nhiên. Vì em làm việc có trách nhiệm‚ <br>nên trả thù lao xứng đáng là lẽ đương nhiên."),
    988: ("それに下手に報酬をまけないのは、<br>仲間や部下の生活にも責任を持ってる証拠だろう。",
         "Hơn nữa‚ không chịu hạ thù lao rẻ mạt là <br>minh chứng em có trách nhiệm với đời sống của đồng đội và cấp dưới."),
    1000: ("ああ。<br>海賊船の乗組員ってのは、みんな家族みたいなもんだからな！",
         "Ừ. <br>Thủy thủ trên tàu hải tặc đều như gia đình vậy!"),
    1007: ("アタシの父さんや母さんも海賊稼業だし、<br>祖父さんも、そのまた爺さんもず～～っと海賊なんだ！",
         "Cha mẹ em cũng làm nghề hải tặc‚ <br>rồi ông nội‚ cụ nội cũng toàn là hải tặc suốt đời!"),
    1018: ("アタシは小さい頃から、ご先祖さまの海賊王の話を聞いてきたからさ。<br>ご先祖さまに恥ずかしくないよう、アタシも船の仲間を大事にしなきゃな！",
         "Từ nhỏ em đã nghe kể chuyện Vua Hải Tặc tổ tiên rồi. <br>Để khỏi làm tổ tiên xấu hổ‚ em cũng phải trân trọng bạn tàu của mình!"),
    1020: ("となると、おまえの夢は海賊王か？", "Thế thì ước mơ của em là Vua Hải Tặc sao?"),
    1032: ("それは……まだ分からない。ご先祖さまの時とは時代が違うし。<br>今はアタシも商船を経営してる。",
         "Chuyện đó…… em vẫn chưa rõ. Thời đại khác với thời tổ tiên. <br>Giờ em cũng đang kinh doanh tàu thương mại."),
    1043: ("でも、やるんだったら一番を目指すのがアタシの性分だ。<br>だから、差し当たっての目標はエルドラーナで一番の商船団かな！",
         "Nhưng đã làm thì em mang tính chấp nhất là số một. <br>Nên trước mắt‚ mục tiêu của em là hạm đội thương mại số một Eldorana!"),
    1045: ("ははっ、それはでかい目標だな。<br>だが、その意気は気に入った。",
         "Hahah‚ mục tiêu to thật đấy. <br>Nhưng anh thích cái khí thế đó."),
    1047: ("おまえが世界一になったら、俺がお得意様になってやってもいいぞ。",
         "Nếu em trở thành số một thế giới‚ anh cũng chẳng ngại làm khách hàng thân thiết của em."),
    1058: ("あははっ。言うねぇ、司令官。", "Ahahah. Chỉ Huy nói hay thật."),
    1066: ("それじゃあ、夢に向かって、まずは目の前の仕事をこなすとしますかっ。",
         "Vậy thì‚ hướng tới ước mơ―trước tiên hãy xử lý công việc trước mắt đã!"),
    1077: ("さあ、ご所望の品はなんだ？<br>食料でも資材でも、なんだって調達して見せるぞ！",
         "Nào‚ anh muốn món hàng gì? <br>Lương thực hay vật liệu‚ em cũng sẽ điều động được hết!"),
    1122: ("（司令官って、思ってたより優しいんだな。<br>　アタシのこと、アウラと比べたりせずにちゃんと見ててくれるし……）",
         "(Chỉ Huy hiền hơn em tưởng. <br>　Anh cũng nhìn nhận em đàng hoàng‚ không đem so sánh với Aura...)"),
    1133: ("（なんだろう……。<br>　なんだかむずがゆいような、ソワソワするような……）",
         "(Là sao ta……? <br>　Cảm giác như nhột nhột‚ bồi hồi không yên......)"),
    1144: ("（……大きな仕事を任されて緊張してるのかも。<br>　よし！　きっちりこなして、司令官の期待に応えるぞ！）",
         "(……Có lẽ em hồi hộp vì được giao trọng trách lớn. <br>　Được! Phải hoàn thành chỉn chu để xứng với kỳ vọng của Chỉ Huy!)"),
}

# Sanity: no ASCII comma inside any VI substitution
for ln, (jp, vi) in M.items():
    assert "," not in vi, f"ASCII comma in VI for line {ln}: {vi!r}"

data = EN.read_bytes()
has_crlf = b"\r\n" in data
text = data.decode("utf-8-sig")
lines = text.splitlines(True)

out_lines = []
translated = 0
for idx, line in enumerate(lines):
    line_no = idx + 1
    if line_no in M:
        jp, vi = M[line_no]
        assert jp in line, f"JP key not found on line {line_no}:\n{line}"
        new = line.replace(jp, vi, 1)
        assert new != line, f"no change on line {line_no}"
        out_lines.append(new)
        translated += 1
    else:
        out_lines.append(line)

out = "".join(out_lines)
out_bytes = ("\ufeff" + out).encode("utf-8")
VI.parent.mkdir(parents=True, exist_ok=True)
VI.write_bytes(out_bytes)

print(f"translated text records: {translated}")
print(f"total source lines: {len(lines)}")
print(f"crlf in source: {has_crlf}, BOM written: True")
print(f"VI written -> {VI}")

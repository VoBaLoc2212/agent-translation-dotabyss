import json
import re
import os

# Load JP source (ja.json) and EN novel translation (en.json)
with open('dotabyss-translation-main/translations/novels/hmn_10440100001/ja.json', 'r', encoding='utf-8') as f:
    ja_data = json.load(f)

with open('dotabyss-translation-main/translations/novels/hmn_10440100001/en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Load EN asset lines
with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'r', encoding='utf-8-sig') as f:
    en_asset_lines = [line.rstrip('\n\r') for line in f]

TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
en_asset_records = []
for i, line in enumerate(en_asset_lines):
    for cmd in TEXT_CMDS:
        if line.startswith(cmd):
            parts = line.split(',', 5)
            speaker = parts[1] if len(parts) > 1 else ''
            text_field = parts[2] if len(parts) > 2 else ''
            en_asset_records.append((i, cmd, speaker, text_field, line))
            break

print(f"EN asset text records: {len(en_asset_records)}")

# For EN-asset-is-English case:
# - ja.json maps JP -> JP (identity) or JP -> (empty?)
# - en.json maps JP -> EN
# - EN asset has EN text in text_field
# We need to match EN asset text to en.json values to find JP key, then translate JP->VI

# Build map: normalized EN novel text -> JP key
def normalize(text):
    if not text:
        return ''
    # Remove tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize commas
    text = text.replace('，', ',').replace('\u201a', ',')
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

en_novel_to_jp = {}
for jp_key, en_val in en_data.items():
    if en_val:
        norm = normalize(en_val)
        if norm:
            en_novel_to_jp[norm] = jp_key

print(f"EN novel entries with translations: {len(en_novel_to_jp)}")

# Also build reverse map for title: EN asset has JP title in speaker field
# ja.json for this file seems to be identity map, so title JP is in ja_data keys
# The title in EN asset is at line 19: title,これから大雨が降りますから！,
title_jp = en_asset_records[0][2]  # speaker field has JP title
print(f"Title JP from asset: {title_jp}")

# Full JP -> VI translation map
JP_TO_VI = {
    "これから大雨が降りますから！": "Sắp Có Mưa Lớn Rồi Đó!",
    "おおぉ……？　事務仕事が予定よりも早く終わった？<br>アリシア、終わっているよな？": "Ôi...? Việc văn phòng xong sớm hơn dự kiến à?<br>Alicia, em đã xong rồi chứ?",
    "はい！　終わっていますとも！<br>たくさん頑張っていただけて、わたしも嬉しいですっ！！": "Vâng! Em đã xong rồi ạ!<br>Thấy anh nỗ lực nhiều như vậy, em cũng vui lắm!!",
    "ほぼ２日間、缶詰になってしまったな……<br>せっかく早く終わったし、２人で外出して羽を伸ばすか？": "Gần hai ngày bị nhốt trong phòng...<br>Đã xong sớm thế, hai người ta ra ngoài giải tỏa một chút đi?",
    "いいですねぇ～。<br>お供させてください！": "Hay đấy~. Xin cho em đi theo anh nhé!",
    "さて、まずはマーケットでも行くか。<br>面白い掘り出し物が見つかるかもしれん。": "Được, trước tiên đi chợ đã. Có lẽ sẽ phát hiện được món đồ hay ho đấy.",
    "楽しみです！": "Mong quá!",
    "あ、そこのお２人さま、お待ちください！<br>これから外出ですよね？": "A, hai vị ơi, chờ một chút! Hai vị sắp ra ngoài à?",
    "はい。その予定ですけど……？": "Vâng. Có dự định là vậy nhưng...?",
    "でしたら、もう少しお時間をずらしたほうがよろしいですよ。<br>これから大雨が降りますから！": "Thế thì hai vị nên đổi giờ đi một chút. Vì sắp có mưa lớn rồi!",
    "あ、雨ですか？<br>こんなに天気が良いのに……？": "A, mưa à?<br>Trời đẹp như vậy mà...?",
    "一見、晴天のように見えますが、降る可能性は高いです！": "Bề ngoài trông như trời quang, nhưng khả năng mưa rất cao!",
    "どうします、司令官？　自信があるみたいですが……。": "Sao bây giờ, Chỉ Huy? Cô ấy có vẻ tự tin lắm mà...",
    "天気予報か。雲や風などで天気の変化を推測するものは<br>昔からいるが、その精度は高いとは言えないのが実情だ。": "Dự báo thời tiết à. Từ xưa có người đoán thời tiết qua mây gió,<br>thực tế độ chính xác không cao đâu.",
    "天気なんて気まぐれなものだからな。<br>いちいち気にしていたら、外出なんてできなくなる。": "Thời tiết vốn dĩ lừng lợ. Nếu chi tiết lo lắng thì không ra ngoài được đâu.",
    "アリシア、気にせず出掛けるぞ。<br>貴重な息抜きの時間を逃す手はない。": "Alicia, đừng lo, ta đi thôi.<br>Không thể bỏ lỡ thời gian giải trí quý giá này.",
    "は、はい――": "Vâng, vâng—",
    "すみません。ご忠告ありがとうございました。<br>お気持ちだけいただきますね。": "Xin lỗi. Cảm ơn lời nhắc nhở. Em chỉ nhận lòng thôi ạ.",
    "分かりました。どうか、お気をつけて――": "Mình hiểu rồi. Xin hai vị cẩn trọng—",
    "<size=48>――数１０分後</size>": "<size=48>——Vài Chục Phút Sau</size>",
    "<size=48>――翌日</size>": "<size=48>——Ngày Hôm Sau</size>",
    "昨日のお２人は、濡れずに済んだでしょうかね……": "Hôm qua hai vị có tránh được mưa không nhỉ...",
    "司令官！　いらっしゃいました！": "Chỉ Huy! Có mặt rồi!",
    "……いたか。": "...Có mặt đấy.",
    "あ、昨日の！<br>あの後、大丈夫でした？": "A, hôm qua kia!<br>Sau đó hai vị 괜찮았나요?",
    "いいや。お前の言う通り、ゲリラ豪雨に打たれて仲良く濡れネズミだったよ。<br>２人とも下着までぐっしょりだ。": "Không. Như cô nói, chúng ta bị mưa rầm bất chợt ướt sũng như chuột lội nước.<br>Hai người ướt sũng tận đồ lót.",
    "ひどい目に遭いました……ぐすん。": "Thảm quá... *nức nở*",
    "あらあら……大変でしたね。もっと強く引き留めておくべきでした。<br>至らず、申し訳ございません。": "Ôi thôi... Khổ lắm nhỉ. Lẽ ra nên giữ hai vị lại mạnh hơn.<br>Xin lỗi vì sơ suất.",
    "それはいいんだ。助言を無視したのは俺たちだし。<br>失礼な態度だったな。すまなかった。": "Không sao. Lời khuyên là do ta không nghe.<br>Thái độ thất thẩm. Xin lỗi.",
    "いえいえ～。お気になさらず！": "Không không~ Đừng để ý!",
    "それより、お前に尋ねたいことがあって探していたんだ。": "Thôi được. Ta tìm cô vì có chuyện muốn hỏi.",
    "なぜ雨になることが分かった？<br>あの口振りだと、かなり自信があったんだろう？": "Tại sao cô biết sẽ mưa?<br>Cách nói của cô có vẻ rất tự tin?",
    "まぁっ。司令官さまは私に興味を抱いてくださったんですね。<br>ありがとうございます。大変光栄です。": "Kyaa. Chỉ Huy có hứng thú với em à.<br>Cảm ơn. Vinh dự lắm.",
    "ん？　俺のことは知っていたのか。": "N? Cô đã biết ta à?",
    "はいっ。司令官さまは前線基地で一番の有名人ですから♪": "Vâng ạ. Chỉ Huy là người nổi tiếng nhất Căn Cứ Tiền Tuyến cơ mà♪",
    "申し遅れました。私はヤチヨと申します。<br>出身は東の国ホウライ、巫女の家系の者です。": "Lời chào muộn. Em là Yachiyo.<br>Quê ở đất nước phương Đông Hourai, dòng dõi nữ thần.",
    "巫女というのは、確か神に仕える呪い師のことだな。": "Nữ thần (miko) là... nhớ là pháp sư phục vụ thần đúng không?",
    "左様でございます。<br>司令官さまは博識でいらっしゃいますね。": "Đúng ạ.<br>Chỉ Huy thật博学 (rộng rãi kiến thức) nhỉ.",
    "（神に仕えるわりには、扇情的な格好をしているなぁ……）": "(Dù phục vụ thần mà ăn mặc gợi cảm thế... )",
    "司令官さま？　私の胸元に何か？": "Chỉ Huy? Có gì ở ngực em sao?",
    "なんでもない。話を続けてくれ。<br>その血筋は天候を読む力にも関係しているのか？": "Không có gì. Tiếp tục đi.<br>Dòng dõi đó có liên quan đến năng lực đọc thời tiết không?",
    "えぇ。当家は古来より龍神さまとご縁がございます。": "Vâng. Nhà em từ xưa có duyên với Thần Long.",
    "龍か。それも聞いたことがあるぞ。<br>確かドラゴンのことだろう？": "Long à. Ta nghe nói. Đó là Dragon (Long phương Tây) chứ?",
    "な、なななっ！？": "Na, na na na!?",
    "なんてことを言うんですかーーーーーーっ！！！": "Cô nói gì vậy-----------っ!!!",
    "おおっ……！？": "Oa...!?",
    "私たちの龍神さまをあんな火吹きトカゲもどきと一緒にするだなんてー！<br>不敬です！　不敬極まりない！": "Đưa Thần Long của chúng ta ra ngang ngửa với loài thằn lằn phun lửa giả tạo kia!<br>Bất kính! Bất kính tới cực điểm!",
    "龍神さまはドラゴンとは全然違います！　身体はすらりと長くカッコいい！<br>御髭は風にたなびいて優雅！": "Thần Long hoàn toàn khác Dragon! Thân hình thon dài, cool ngầu!<br>Râu ria bay trong gió,優雅 (nhã nhặn) lắm!",
    "神罰を与える手段だって野蛮な炎ではなく、<br>上品な雷だと言い伝えられています！": "Cách ban hành thần phạt cũng không phải lửa man rợ,<br>truyền thuyết là sấm sét thanh lịch!",
    "ずんぐりむっくりしているドラゴンとは違うのですー！": "Khác hẳn những con Dragon bụn bã, mập mạp!",
    "わ、分かった分かった！　悪かった！<br>ドラゴンと龍は全然違う！　覚えたから！！": "Được, được rồi! Ta sai!<br>Dragon và Long hoàn toàn khác! Nhớ rồi!!",
    "はいっ！　気を付けてくださいねっ！": "Vâng! Coi chừng nhé!",
    "あ、あぁ……それで、龍と縁のある家に生まれたことが、<br>天候を読む力とどう関係しているんだ？": "A, à... Vậy, sinh ra trong gia tộc có duyên với Long,<br>liên quan gì đến năng lực đọc thời tiết?",
    "私は、幼い頃からお天気を司る龍神さまを自身に宿しているんです。": "Em từ nhỏ đã dung nham Thần Long cai quản thời tiết trong người.",
    "な、なんだと！？<br>龍が人間の中に！？": "Na, đó là gì!?<br>Long trong người à!?",
    "えぇ♪　龍神さまの精神が入っている状態でして。": "Vâng♪ Thần trí Thần Long ngự trong em.",
    "小さい頃からつらいときも楽しいときも、<br>心の中でずっと一緒で、仲良くしていただいています。": "Từ nhỏ, lúc khổ lúc vui,<br>trong tim luôn cùng nhau, bình yên.",
    "昨日、雨が降ると予見できたのは、龍神さまのお声を聞いたからなんです。": "Hôm qua biết sẽ mưa là vì nghe tiếng Thần Long.",
    "うーむ。自分の中に住む龍が天候を予知しているのか――<br>これはとんでもなく有益な能力だぞ。": "Uhm. Long ngự trong người dự báo thời tiết à—<br>Năng lực hữu ích vô cùng đấy.",
    "そうですよね。雨が事前に降ると分かっていれば、<br>お出かけするときに傘を持っていくか悩まなくてすみますし。": "Đúng đấy. Biết trước sẽ mưa thì<br>ra ngoài không lo mang ô hay không.",
    "洗濯ものを干す時にも便利。<br>あ！　農家の方々は、ものすっごく助かりますよね。": "Phơi đồ cũng tiện. A! Nông dân thì giúp to lớn!",
    "あぁ。それに水害や風害の発生も事前に察知することもできるなら、<br>民の避難誘導も余裕をもって始められる。": "À. Nếu cả nước lũ, gió bão cũng biết trước thì<br>di dời dân chúng chủ động hơn.",
    "それだけでなく、戦術を決めるのにだって役立つ。<br>天候を読めるというのは、それだけ有益なんだ。": "Không chỉ vậy, quyết định chiến thuật cũng nhờ đó.<br>Đọc được thời tiết tức là lợi thế to lớn.",
    "本当にすごいお力ですね～。": "Năng lực tuyệt vời quá~.",
    "……あ、あのぉ～、たくさん褒めていただいている中で<br>申し上げにくいんですけどもぉ……": "...A, à... Đang được khen nhiều thế mà<br>nói ra khó quá...",
    "そんなに便利な力、というわけでもないんですよねぇ～……": "Không phải năng lực tiện lợi lắm đâu...",
    "んっ？　何かリスクでもあるのか？": "N? Có rủi ro gì à?",
    "……実は、龍神さまは大変気まぐれなのです。": "...Thực ra, Thần Long rất捉摸不定 (bàn bạc không định).",
    "予報を授けてはくださるんですけど、<br>それが当たらないことも、しばしば――": "Có cho dự báo, nhưng<br>thường sai—",
    "「雨が降る」だけ教えて、<br>「いつ降るのか」を教えてくださらないこともございます。": "Chỉ báo 'sẽ mưa',<br>không báo 'khi nào mưa'.",
    "早ければ数分後、遅ければ１週間後ということもありまして――": "Sớm thì vài phút, muộn thì một tuần sau—",
    "そ、それはもう、当たったとも言い難いような……？": "Th, thế coi như... khó nói là trúng...?",
    "けっこう意地悪だな――性格が良くなさそうだ。": "Hơi ác ý đấy—không thấy tốt bụng.",
    "うぅっ。否定は、できません……": "Ugh. Không thể phản biện...",
    "すごい力を持っているのに、ちょっと意地悪で気まぐれ……<br>どこかの誰かさんのような……？": "Có năng lực lớn mà hơi ác, hay thất thường...<br>Giống ai đó không biết...?",
    "おい待て。それは俺のことか？": "Oi đừng. Đó là nói ta à?",
    "さぁ、どうでしょ～？": "Sao biết được~?",
    "予報の精度が悪くて、皆さんに信用してもらえないことも多いんです。<br>むしろ、逆に迷惑がられることもあったりでして――": "Dự báo kém chính xác, mọi người không tin.<br>Ngược lại còn bị khiếu nại—",
    "最終的にはいづらくなってしまい、私は各地を転々としています。": "Cuối cùng khó ở, em phải lang thang khắp nơi.",
    "かわいそう……": "Khổ quá...",
    "ともかく、そういった事情で、私の天気予報は万能な力ではありません。": "Dù sao, vì vậy dự báo của em không phải toàn năng.",
    "前線基地の皆さんに受け入れられないようでしたら、ここからも去ります。": "Nếu Căn Cứ Tiền Tuyến không nhận em, em sẽ đi.",
    "いや、待て待て。そんなに卑屈になるな。": "Không, đợt đã. Đừng tự ti thế.",
    "完璧な力ではないみたいだが、凡人が空を見て予想するよりかは<br>確実に予報の精度が高いわけだろう？": "Không hoàn hảo, nhưng chắc chắn chính xác hơn người thường nhìn trời đoán?",
    "昨日、ヤチヨは雨が降ると言って、俺たちはゲリラ豪雨に打たれた。<br>お前が龍神の声を聞いている証拠だ。": "Hôm qua Yachiyo nói mưa, ta bị mưa rầm. Đó là bằng chứng cô nghe tiếng Thần Long.",
    "精度の高い天気予報が農業、災害防止、戦いの助けになることは<br>先ほど説明した通り。ヤチヨの力は人知を超えた有益な力で間違いない。": "Dự báo chính xác giúp nông nghiệp, phòng thiên tai, chiến đấu như đã nói.<br>Năng lực của Yachiyo hữu ích vượt hiểu lường.",
    "そ、そんなに褒めないでくださいっ！！　私の力ではなく、<br>龍神さまの力ですし――": "Đừng khen nhiều vậy!! Năng lực không phải của em,<br>là của Thần Long—",
    "気に入らない人間に龍神も力は貸さないだろう。ヤチヨが人間としても<br>優れている証拠だ。実際、話していて好感が持てる。": "Thần Long không cho người ghét mượn lực. Chứng minh Yachiyo là người tốt. Thực tế nói chuyện thấy dễ thương.",
    "あ、あわっ！？　こ、好感だなんて――<br>そ、そんなこと、男性から初めて言われましたよ……": "A, a wa!? Th, thiện cảm là gì—<br>Đ, lần đầu nam giới nói vậy...",
    "照れるな。事実なんだからな。<br>胸を張って前線基地にいろ。司令官である俺が許す。": "Đừng nhí nhảnh. Là sự thật.<br>Ngực cất cao ở Căn Cứ Tiền Tuyến. Chỉ Huy là ta cho phép.",
    "……！？<br>司令官さま、私の過去を、気にしてくださって――？": "...!?<br>Chỉ Huy, quan tâm quá khứ của em—?",
    "綺麗で可愛い方が相手だと、すぐそうやって～……<br>ヤチヨさん、気を付けてくださいね！": "Đối phương đẹp dễ thương thì liền vậy~...<br>Yachiyo-san, cẩn thận nhé!",
    "……": "...",
    "ヤチヨさん？　どうしたんです？": "Yachiyo-san? Sao vậy?",
    "あ、その……司令官さまが、女性に人気だというお話……<br>なんだか、とても分かってしまって……どうしましょう……♡": "À, đó... Chỉ Huy được nữ tính thích...<br>Cảm giác hiểu rõ lắm... Làm sao bây giờ...♡",
    "――ゴロゴロゴロ。": "——Gù gù gù.",
    "あれ？　なんだか急に雷の音が……？": "Ạ? Bỗng nghe tiếng sấm...?",
    "――ザァァアアアッ！": "——Xào xạc!",
    "わわわっ！？　すごいお天気雨ですよ！？": "Wa wa wa!? Mưa nắng dữ lắm!?",
    "しかもすごい大雨だな！？<br>急いで建物に入れ！　風邪を引くぞ！": "Mưa to lắm!?<br>Nhanh vào nhà! Sẽ 感冒 (ốm) đấy!",
    "は、はいっ！": "Vâng, vâng!",
    "ふぅっ……間一髪だったな。<br>ヤチヨも大丈夫だな？": "Phù... Chót vót.<br>Yachiyo cũng ổn chứ?",
    "はい。おかげさまで……": "Vâng. Nhờ anh...",
    "急な大雨だったな。龍神は何も言ってこなかったのか？": "Mưa rầm bất chợt. Thần Long không nói gì à?",
    "えぇ……変ですね。<br>私が雨に打たれそうなときは、いつも教えてくださるんですけど――": "Vâng... Lạ nhỉ.<br>Sắp bị mưa thì Thần Long luôn báo mà—",
    "それもあって昨日、司令官さまとアリシアさんには「降りそうです」と<br>お伝えすることができたんです。行き先が同じ方角でしたから。": "Vì vậy hôm qua em báo cho Chỉ Huy và Alicia-san 'có vẻ sẽ mưa'. Vì cùng hướng.",
    "やはり神様は気まぐれなんだな。": "Thần quả thật thất thường.",
    "だが、お前の力は大いに役立つ。<br>たまに天気予報を頼んでいいか？": "Nhưng năng lực cô rất hữu ích.<br>Đôi khi nhờ cô dự báo được không?",
    "はい、もちろんです！<br>精一杯頑張りますので、よろしくお願いいたします。司令官さま♪": "Vâng, đương nhiên!<br>Sẽ cố gắng hết sức, mong Chỉ Huy giúp đỡ♪",
}

print(f"JP_TO_VI entries: {len(JP_TO_VI)}")

# Match EN asset records to JP keys and translate
vi_translations = {}  # asset text_field -> vi_text
matched = 0
unmatched = []

for line_idx, cmd, speaker, text_field, full_line in en_asset_records:
    if cmd == 'title,':
        # Title: speaker field has JP title
        jp_key = speaker
        if jp_key in JP_TO_VI:
            vi_translations[text_field] = JP_TO_VI[jp_key]  # Use empty text_field as key for title
            matched += 1
        else:
            unmatched.append((line_idx, cmd, speaker, text_field))
    else:
        # Message: text_field has EN text, need to match to EN novel
        norm_asset = normalize(text_field)
        if norm_asset in en_novel_to_jp:
            jp_key = en_novel_to_jp[norm_asset]
            if jp_key in JP_TO_VI:
                vi_translations[text_field] = JP_TO_VI[jp_key]
                matched += 1
            else:
                unmatched.append((line_idx, cmd, speaker, text_field))
        else:
            # Try fuzzy matching with all en_novel entries
            found = False
            for en_novel_norm, jp_key in en_novel_to_jp.items():
                # Check if they're similar (asset text may be truncated in display)
                if en_novel_norm in norm_asset or norm_asset in en_novel_norm:
                    if jp_key in JP_TO_VI:
                        vi_translations[text_field] = JP_TO_VI[jp_key]
                        matched += 1
                        found = True
                        break
            if not found:
                unmatched.append((line_idx, cmd, speaker, text_field))

print(f"Matched: {matched}")
print(f"Unmatched: {len(unmatched)}")
for idx, cmd, spk, txt in unmatched[:10]:
    print(f"  Line {idx} ({cmd}): speaker={spk} text={txt[:60]}")

# Now rebuild VI lines
vi_lines = list(en_asset_lines)
replaced = 0

for line_idx, cmd, speaker, text_field, full_line in en_asset_records:
    if cmd == 'title,':
        if text_field in vi_translations:  # empty string key
            vi_text = vi_translations[text_field]
            parts = full_line.split(',', 5)
            if len(parts) >= 2:
                parts[1] = vi_text
                vi_lines[line_idx] = ','.join(parts)
                replaced += 1
    else:
        if text_field in vi_translations:
            vi_text = vi_translations[text_field]
            # Replace commas in VI text with U+201A
            vi_text = vi_text.replace(',', '\u201a')
            parts = full_line.split(',', 5)
            if len(parts) >= 3:
                parts[2] = vi_text
                vi_lines[line_idx] = ','.join(parts)
                replaced += 1

print(f"Replaced: {replaced} lines")

# Verify line count
assert len(vi_lines) == len(en_asset_lines), "Line count mismatch!"

# Verify BR counts
def count_br(text):
    return text.count('<br>')

br_mismatches = []
for line_idx, cmd, speaker, text_field, full_line in en_asset_records:
    if cmd == 'title,':
        if text_field in vi_translations:
            en_br = count_br(text_field)
            vi_br = count_br(vi_translations[text_field])
            if en_br != vi_br:
                br_mismatches.append((line_idx, cmd, en_br, vi_br))
    else:
        if text_field in vi_translations:
            en_br = count_br(text_field)
            vi_br = count_br(vi_translations[text_field])
            if en_br != vi_br:
                br_mismatches.append((line_idx, cmd, en_br, vi_br))

if br_mismatches:
    print(f"\nBR MISMATCHES ({len(br_mismatches)}):")
    for idx, cmd, en_br, vi_br in br_mismatches:
        print(f"  Line {idx} ({cmd}): EN={en_br} VI={vi_br}")
else:
    print("\nAll BR counts match!")

# Check ASCII commas in VI text
comma_issues = []
for line_idx, cmd, speaker, text_field, full_line in en_asset_records:
    if cmd == 'title,':
        if text_field in vi_translations:
            vi_text = vi_translations[text_field]
            if ',' in vi_text:
                comma_issues.append((line_idx, cmd, vi_text))
    else:
        if text_field in vi_translations:
            vi_text = vi_translations[text_field]
            if ',' in vi_text:
                comma_issues.append((line_idx, cmd, vi_text))

if comma_issues:
    print(f"\nASCII COMMA ISSUES ({len(comma_issues)}):")
    for idx, cmd, txt in comma_issues[:10]:
        print(f"  Line {idx} ({cmd}): {txt[:80]}")
else:
    print("\nNo ASCII commas in VI text fields!")

# Write output
output_path = 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'wb') as f:
    f.write(b'\xef\xbb\xbf')
    f.write('\r\n'.join(vi_lines).encode('utf-8'))
    f.write(b'\r\n')

print(f"\nWritten to {output_path}")
print(f"Lines: {len(vi_lines)}")
print(f"Size: {os.path.getsize(output_path)} bytes")
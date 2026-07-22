import json
import re

# Read ja.json (JP source)
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/ja.json', 'r', encoding='utf-8') as f:
    ja_novel = json.load(f)

# Read en.json (EN translation of JP)
with open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10500100001/en.json', 'r', encoding='utf-8') as f:
    en_novel = json.load(f)

# Read EN asset file (binary to preserve BOM and CRLF)
with open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt', 'rb') as f:
    en_asset_bytes = f.read()

# Detect BOM and encoding
has_bom = en_asset_bytes.startswith(b'\xef\xbb\xbf')
text = en_asset_bytes.decode('utf-8-sig')
has_crlf = '\r\n' in text

# Split lines keeping line endings
lines = text.splitlines(keepends=True)

# Text commands to translate
text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

# Normalize function for matching
def norm(s):
    s = s.replace('，', ',').replace('、', ',')
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', '', s)
    return s

# Build EN asset text field mapping
asset_texts = []  # (line_idx, cmd, text_field)
for i, line in enumerate(lines):
    raw = line.rstrip('\r\n')
    for cmd in text_cmds:
        if raw.startswith(cmd):
            if cmd == 'title,':
                parts = raw.split(',', 1)
                if len(parts) >= 2:
                    asset_texts.append((i, cmd, parts[1]))
            else:
                parts = raw.split(',', 5)
                if len(parts) >= 3:
                    asset_texts.append((i, cmd, parts[2]))
            break

# Build reverse mapping: EN (normalized) -> JP
en_to_jp = {}
for jp_key, en_val in en_novel.items():
    if en_val:
        en_to_jp[norm(en_val)] = jp_key

# For title field still in JP in EN asset, we need to match from ja.json
# The title in EN asset is "くすんだ石ころ" which matches ja.json key "くすんだ石ころ" 
# and en.json has empty string for it

# Also build JP text -> VI translation mapping
# First, let me translate all JP texts to Vietnamese

# Character voice notes:
# - ベティ (Betty): Female volunteer soldier, energetic, uses "であります" (desu/masu military style)
#   Self: わたし (watashi), addresses Commander as 司令官殿 (Shireikan-dono -> Chỉ Huy)
#   Tone: earnest, polite but energetic, gets discouraged easily but bounces back
# - 司令官/Commander (Chỉ Huy): Male protagonist
#   Self: 俺 (ore), addresses Betty as ベティ (Betty)
#   Tone: casual, supportive, slightly older brother vibe
# - アリシア (Alicia): Female officer, appears briefly
#   Self: 私/あたし?, addresses Commander as <user> (Commander)
# - <user>: Commander placeholder

# Translation glossary:
# - 司令官 / 司令官殿 / Commander / Lord Commander -> Chỉ Huy
# - ベティ / Betty -> Betty (keep name)
# - ミレスガルド / Milesgard -> Milesgard
# - 大穴 / Abyss -> Đại Huyệt
# - 前線基地 / Frontline Base -> Căn Cứ Tiền Tuyến
# - 工兵隊 / Engineer Corps -> Đội Kỹ Sư / Công Binh
# - 主計兵 / Quartermaster -> Binh Quân Nhu / Quản Lý Hậu Cần
# - 志願兵 / Volunteer -> 志願兵 / Thự Cầu Binh
# - 騎士 / Knight -> Kỵ Sĩ
# - 宝石 / Gem -> Bảo Thạch / Ngọc
# - 石 / Stone -> Đá / Viên Đá

# Vietnamese translations for each JP line
jp_to_vi = {
    "くすんだ石ころ": "Viên Đá Nhòe",
    "コンコン――": "Cốc cốc――",
    "入っていいぞ。": "Vào đi.",
    "はい！　失礼するであります！": "Dạ! Em xin phép ạ!",
    "お前が今日着任した志願兵か。": "Cậu là tân binh hôm nay mới đến đúng không.",
    "はいっ！　<br>ミレスガルド出身のベティであります！": "Dạ! Em là Betty đến từ Milesgard!",
    "はは、元気なやつだな。<br>前線基地への配属を希望しているみたいだが、どうしてだ？": "Haha, cô bé có tinh thần đấy.<br>Nghe nói cậu xin đến Căn Cứ Tiền Tuyến, tại sao lại như vậy?",
    "はい！　わたしの実家は代々騎士の家柄で<br>幼いころより父や兄の戦場での活躍を目の当たりにしてきたであります！": "Dạ! Gia đình em thời nào cũng là dòng họ Kỵ Sĩ.<br>Từ nhỏ em đã chứng kiến cha và anh trai hoạt huyết trên chiến trường!",
    "だからわたしも父や兄のような<br>立派な兵士になって活躍するのが目標なのであります！": "Vì vậy mục tiêu của em cũng là trở thành một chiến sĩ xuất sắc<br>như cha và anh trai, để có thể hoạt huyết!",
    "なるほど。家族にもさぞかし期待されているんだろうな。": "Thôi hiểu rồi. Gia đình cậu chắc chắn mong đợi lớn lắm chứ.",
    "え？　そ、それはそのぅ……": "Ẻ? Đó, đấy là… ừm…",
    "なんだ？": "Sao rồi?",
    "実は家族からは、兵士になることを反対されておりまして……": "Thực ra gia đình đã phản đối em làm binh sĩ…",
    "ほう。なぜだ？": "Ồ. Tại sao?",
    "わたしのような小柄な女性に<br>危険な戦場の任務など務まるはずはないと……": "Bọn họ nói với người nữ nhỏ nhắn như em<br>thì không thể gánh nổi nhiệm vụ chiến trường nguy hiểm……",
    "……なるほどな。だったらここに来たのは正解だな。": "……Thôi hiểu rồi. Vậy là cậu đến đúng chỗ rồi.",
    "え？": "Ẻ?",
    "ここは戦場の最前線。手柄を取るチャンスはそこかしこに転がっている。<br>ここで手柄をあげて家族に自分が兵士に相応しいと認めさせてやるといい。": "Đây là tiền tuyến chiến trường. Cơ hội lập công đến처处都有.<br>Cậu lập công ở đây rồi bắt gia đình nhận ra cậu xứng đáng làm binh sĩ đi.",
    "はっ、はいっ！　きっと司令官殿のご期待に応えてみせるであります！<br>それでは、失礼するであります！": "Dạ, vâng! Chắc chắn em sẽ đáp ứng được kỳ vọng của Chỉ Huy!<br>Thì em xin phép lui trước!",
    "とても元気で、いい子ですね。": "Thật là năng động, và là đứa trẻ tốt.",
    "ああ。ああいうやつがいると、場の空気がよくなる。": "Đúng. Có cô ấy ở đây không khí vui vẻ lên hẳn.",
    "活躍できるといいですね。": "Hy vọng cô ấy sẽ hoạt huyết được.",
    "そうだな。": "Đúng đấy.",
    "<size=48>――数か月後</size>": "<size=48>――Vài Tháng Sau</size>",
    "……というわけで、大穴内の掘削作業は現在、難航しております。<br>専門技術を持った工兵隊には期待していたのですが……": "……Vì vậy, công tác khai thác внутри Đại Huyệt hiện đang gặp khó khăn.<br>Đội Kỹ Sư có kỹ thuật chuyên môn本来很受期待, nhưng……",
    "蓋を開けてみれば、誰が隊長として現場を取り仕切るかで揉めてばかりで<br>仕事がろくに進まない状態です。": "Mở ra xem thì toàn tranh cãi ai làm đội trưởng chỉ huy hiện trường,<br>việc nào cũng không tiến triển được.",
    "……認めた相手の言うことしか聞かないってところか。<br>職人気質な連中ってのは、こういう時厄介だな。": "……Chỉ nghe theo người mình công nhận thôi à.<b>Những kẻ có tâm nghề</b> lúc này thật khó xử.",
    "隊長か……いっそ、俺が指名してしまうか？<br>いや、頭ごなしの行動をとればやつらはより反発するだけだな……": "Đội trưởng à…… có nên ta chỉ định luôn không?<br>Không, hành động quá mạnh tay chỉ làm bọn chúng phản kháng hơn thôi……",
    "……考えてもらちが明かないな。<br>ちょっと外の空気を吸ってくる。": "……Nghĩ mãi cũng không ra gì.<br>Ta ra ngoài hít chút không khí đã.",
    "荒くれ者揃いの工兵隊のまとめ役、か……<br>どうしたものか……　ん？": "Người dẫn dắt bọn kỹ sư thô bạo đó à……<br>Làm sao bây giờ…… Ể?",
    "はぁ……<br>どうしたらいいんだろう……": "Haa……<br>Làm sao bây giờ nhỉ……",
    "ベティ、久しぶりだな。": "Betty, lâu quá không gặp.",
    "あ、司令官殿……！？": "A, Chỉ Huy……!?",
    "まさか司令官殿に名前を憶えていてもらえたなんて……！<br>感激であります！": "Không ngờ Chỉ Huy còn nhớ tên em……!<br>Xúc động vô cùng!",
    "大げさだな。<br>それはそうと……なにかあったのか？": "Nói to đùng thật.<br>Để đó, có chuyện gì vậy?",
    "浮かない顔でため息ついてたろ？": "Mặt mũi buồn bã thở dài liên tục mà.",
    "……はは。バレちゃいましたか。<br>さすがは司令官殿であります。": "……Haha. Bị phát hiện rồi.<br>Thật xứng danh là Chỉ Huy.",
    "実は……モンスターを討伐する部隊に配属されたでありますが<br>洞窟の中で動けなくなって、仲間に迷惑をかけてしまいまして……": "Thực ra…… em được phân vào đội bài trừ quái vật,<br>nhưng trong hang động sợ quá không động đậy được, làm phiền đồng đội……",
    "動けなくなった？　ケガでもしたのか？": "Không động được? Có bị thương à?",
    "それが、そのぅ……わたし、暗い場所が苦手でして。<br>怖くて動けなくなってしまったのであります。": "Đó á, ừm…… em sợ chỗ tối.<br>Sợ hãi nên không thể di chuyển.",
    "それは難儀だな……<br>だったら配置転換を願い出ればどうだ？": "Đó khó xử……<br>Thì xin điều động không?",
    "そう思って、主計兵に配置換えしてもらったであります。<br>消耗品の管理や調理を担当する主計兵なら、お役に立てると思いまして。": "Em nghĩ vậy nên xin điều động làm Binh Quân Nhu.<br>Quản lý tiêu hao và nấu ăn, em nghĩ có thể giúp được.",
    "ですが、そこでも失敗を……": "Nhưng ở đó cũng thất bại……",
    "なんだ、料理が苦手なのか？": "Nào, nấu ăn dở à?",
    "いえ、料理はむしろ得意であります。<br>ですが……": "Không, nấu ăn em đúng là giỏi.<br>Nhưng……",
    "コース料理を振る舞ってしまい<br>戦場でこんなもの呑気に食べてられるか！　と怒られまして……": "Em làm ra bữa ăn nhiều món,<br>bị mắng 'Chiến trường nào có rảnh ăn uống kiểu này!'……",
    "コ、コース料理？": "B- bữa ăn nhiều món?",
    "おいしい食事で元気になってもらおうと思ったのが<br>仇となったであります。": "Nghĩ ăn ngon cho mọi người vui mà<br>đành ra thành việc xấu.",
    "そんなことが度々あった末に、ついには兵士失格だと言われ、<br>仕事を任せてもらえなくなったであります……": "Lặp đi lặp lại mấy lần đó, cuối cùng bị nói 'không xứng làm binh sĩ',<br>không ai giao việc cho em nữa……",
    "こんなダメダメ兵士、手柄を立てるなんて夢のまた夢であります。<br>故郷の両親に手紙でどう報告すれば……。はぁ……": "Binh sĩ vớ vẩn như em, lập công thì chỉ nằm trong mơ.<br>Về nhà viết thư cho cha mẹ báo tin thế nào nhỉ…… Haa……",
    "（これはかなり参ってるな。……ん？）": "(Cô bé này chán nản lắm…… Ể?)",
    "ゴシゴシ……": "Cọ xát cọ xát……",
    "ベティ。さっきから何をしているんだ？": "Betty. Từ mới nãy cậu đang làm gì vậy?",
    "ああ、すみません、つい癖で……。<br>これを磨いていたであります。": "A, xin lỗi, thói quen thôi…<br>Em đang磨 cái này.",
    "これは……石か？<br>なんでそんなことを。": "Cái này…… là đá à?<br>Tại sao lại làm vậy?",
    "わたしの趣味であります！": "Đây là sở thích của em!",
    "石を磨くことがか？": "Mài đá à?",
    "はい！": "Dạ!",
    "――キラッ": "――Lấp lánh",
    "ん？　その石、随分と光ってないか？": "Ể? Viên đá đó, sáng lắm á?",
    "えへっ、そーなんです。": "Eheh, đúng rồi.",
    "長年、土に埋もれて一見、くすんだ石ころも<br>丁寧に根気よく磨いてあげると宝石みたいに綺麗に輝くのであります！": "Viên đá nhòe bị chôn dưới đất nhiều năm,<br>chỉ cần mài kỹ, kiên nhẫn, cũng sẽ lấp lánh như bảo thạch!",
    "石と言えば、大穴にはきっと、<br>地上では見られない色々な石があると思うのです！": "Nói đến đá, em tin chắc ở Đại Huyệt chắc có<br>nhiều loại đá không thấy trên mặt đất!",
    "ああ。大穴には一体どんな石があるんだろう……": "A. Đại Huyệt đến cùng có đá gì nhỉ……",
    "…………": "…………",
    "……わわっ！？　す、すみません、１人ではしゃいでしまって！<br>司令官殿を前にして、つい自分だけの世界に！": "……Wa wa!? Đ-được, em xin lỗi, một mình hứng thú quá!<br>Trước mặt Chỉ Huy mà tự dưng bay bổng!",
    "いや、構わないさ。<br>夢中になれるものがあるってのはいいことだ。": "Không sao đâu.<br>Có thứ khiến người ta say mê là tốt.",
    "石のことなら何でも詳しいのか？": "Về đá thì cậu am hiểu hết à?",
    "もちろんであります！<br>ただこんな趣味、戦場では何の役にも立ちませんが……": "Tất nhiên!<br>Chỉ là sở thích này, trên chiến trường hoàn toàn vô dụng……",
    "……ベティ。": "……Betty.",
    "って、くよくよなんかしていられませんよね！<br>明日から、また頑張らないと！": "À, không thể chán nản mãi được!<br>Từ ngày mai em phải cố gắng lại!",
    "大丈夫なのか？": "Cậu ổn chứ?",
    "もちろんであります！　元気だけがわたしの取柄でありますから！<br>司令官殿も笑顔でファイトでありますよ！": "當然! Chỉ có tinh thần là điểm mạnh của em!<br>Chỉ Huy cũng phải cười tươi mà chiến đấu nhé!",
    "ふっ。そうだな。": "Phụ. Đúng đấy.",
    "では、これで失礼します！": "Thì em xin phép lui đây!",
    "……ちょっと待ってくれ。": "……Chờ một chút.",
    "はい？　何でしょう？": "Dạ? Có chuyện gì?",
    "ベティ、ちょっと俺に付き合ってくれないか？": "Betty, có thể đi cùng ta một chút không?",
    "？": "……?"
}

# Verify we have translations for all matched JP keys
print(f'Translation entries: {len(jp_to_vi)}')
print(f'JA novel entries: {len(ja_novel)}')
print(f'EN novel entries with text: {len([v for v in en_novel.values() if v])}')

# Check coverage
matched_jp_keys = set(en_to_jp.values())
for jp_key in matched_jp_keys:
    if jp_key not in jp_to_vi:
        print(f'MISSING TRANSLATION: {jp_key}')

# Also check title
title_jp = "くすんだ石ころ"
if title_jp not in jp_to_vi:
    print(f'MISSING TITLE: {title_jp}')

# Now build the VI output
vi_lines = lines[:]  # copy

# For each asset text record, replace the text field with VI translation
replaced = 0
for line_idx, cmd, asset_text in asset_texts:
    n = norm(asset_text)
    jp_key = None
    if n in en_to_jp:
        jp_key = en_to_jp[n]
    elif asset_text in ja_novel:  # title case - direct JP match
        jp_key = asset_text
    else:
        # Try partial match
        for en_norm, jp in en_to_jp.items():
            if n in en_norm or en_norm in n:
                jp_key = jp
                break
    
    if jp_key and jp_key in jp_to_vi:
        vi_text = jp_to_vi[jp_key]
        # Replace the text field in the line
        raw = vi_lines[line_idx].rstrip('\r\n')
        if cmd == 'title,':
            parts = raw.split(',', 1)
            if len(parts) >= 2:
                new_line = parts[0] + ',' + vi_text + (vi_lines[line_idx][len(raw):])
                vi_lines[line_idx] = new_line
                replaced += 1
        else:
            parts = raw.split(',', 5)
            if len(parts) >= 3:
                parts[2] = vi_text
                new_line = ','.join(parts) + (vi_lines[line_idx][len(raw):])
                vi_lines[line_idx] = new_line
                replaced += 1
    else:
        print(f'WARNING: Line {line_idx+1} ({cmd}) no translation for: {asset_text[:60]}')

print(f'Replaced {replaced}/{len(asset_texts)} text records')

# Join and write
output_text = ''.join(vi_lines)
# Ensure CRLF if original had CRLF
if has_crlf:
    output_text = output_text.replace('\n', '\r\n')

output_bytes = output_text.encode('utf-8')
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_bytes

# Write to work dir first for QA
import os
work_dir = 'E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100001_full'
os.makedirs(work_dir, exist_ok=True)

with open(os.path.join(work_dir, 'hmn_10500100001_vi.txt'), 'wb') as f:
    f.write(output_bytes)

print(f'Written to {work_dir}/hmn_10500100001_vi.txt')
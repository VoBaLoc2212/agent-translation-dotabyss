#!/usr/bin/env python3
"""
Build hmn_10440100001 VI translation.
Mixed JP-title / EN-message case.
EN-asset-is-English: en.json has English values.
"""
import re, json, os, sys

ROOT = "E:/AgentTranslation"
EN_PATH = f"{ROOT}/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt"
VI_PATH = f"{ROOT}/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt"
WORK = f"{ROOT}/dotabyss-rpg-vn-translator/work/hmn_10440100001_full"

# ---- Load EN asset ----
with open(EN_PATH, 'rb') as f:
    raw = f.read()

has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw[:200]

text = raw.decode('utf-8-sig')
lines = text.splitlines(keepends=True)
print(f"EN asset: {len(lines)} lines, BOM={has_bom}, CRLF={has_crlf}")

# ---- Enumerate text records ----
TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
records = []  # (line_no, cmd, line_text)
for i, ln in enumerate(lines):
    stripped = ln.strip('\r\n')
    if any(stripped.startswith(c) for c in TEXT_CMDS):
        cmd = stripped.split(',')[0]
        records.append((i, cmd, stripped))

print(f"Total text records: {len(records)}")
for idx, (ln_no, cmd, txt) in enumerate(records):
    print(f"  seq={idx+1:3d} line={ln_no:4d} cmd={cmd:20s} preview={txt[:80]}")

# Count by command
from collections import Counter
cmd_counts = Counter(cmd for _, cmd, _ in records)
print(f"\nCommand counts: {dict(cmd_counts)}")
print(f"  title={cmd_counts.get('title',0)} message={cmd_counts.get('message',0)} "
      f"messageTextUnder={cmd_counts.get('messageTextUnder',0)} "
      f"messageTextCenter={cmd_counts.get('messageTextCenter',0)}")

# ---- Translation dictionary ----
# Keyed by record sequence number (1-based)
# JP source for title from ja.json: これから大雨が降りますから！
# For each message, we translate JP→VI using the Japanese from ja.json as reference.
# The EN text is the structural authority.

VI = {}

# seq 1: title
# JP: これから大雨が降りますから！ => "Vì Sắp Có Mưa Lớn Rồi!"
VI[1] = "Vì Sắp Có Mưa Lớn Rồi!"

# ---- Character voice guide ----
# ヤチヨ (Yachiyo): Formal shrine maid, politeですます speech.
#   Calls Commander: 司令官さま → Ngài Chỉ Huy / Chỉ Huy
#   Self: 私 → tôi / em
# アリシア (Alicia): Commander's adjutant, familiar.
#   Calls Commander: 司令官 → Chỉ Huy
#   Self: わたし → em
# Commander (user): 俺 → tôi / anh
#   To Yachiyo: お前 → cô / em
#   To Alicia: アリシア → Alicia

# Terminology bank:
# 司令官/Commander → Chỉ Huy
# 司令官さま/Lord Commander → Ngài Chỉ Huy / Chỉ Huy
# 前線基地/Frontline Base → Căn Cứ Tiền Tuyến
# 龍神/Dragon God → Long Thần
# 巫女/shrine maiden → vu nữ
# ホウライ/Hourai → Hourai (proper noun)
# 龍/dragon (JP style) → Long / rồng thần
# ドラゴン/dragon (Western style) → dra-gôn (accepted loanword)

# seq 2: message,<user>,Oh...? The paperwork finished ahead of schedule? Alicia，you're done<br>too，right?<br> 
VI[2] = "Ồ...? Công việc giấy tờ xong sớm hơn dự định à? Alicia‚ em cũng xong<br>rồi đúng không?<br> "

# seq 3: message,アリシア,Yes! I'm all done! I'm so glad you worked so hard too!<br> ,300201000,vc_10440100001_001_01,chara_2
VI[3] = "Vâng! Em xong hết rồi ạ! Em rất vui vì anh đã làm việc chăm chỉ như vậy!<br> "

# seq 4: message,<user>,We've been cooped up for almost two days... Since we got done<br>early，how about we go out and blow off some steam?<br> 
VI[4] = "Suốt gần hai ngày trời trong phòng rồi... Tranh thủ xong sớm‚<br>hay là hai đứa mình ra ngoài xả hơi một chút?<br> "

# seq 5: message,アリシア,Sounds great! Please let me come with you!<br> ,300201000,vc_10440100001_002_01,chara_2
VI[5] = "Tuyệt quá! Cho em đi cùng với ạ!<br> "

# seq 6: message,<user>,Okay，first let's head to the Market. We might find some interesting<br>bargains.<br> 
VI[6] = "Được rồi‚ trước tiên ra Chợ xem sao.<br>Biết đâu lại mò được món hời.<br> "

# seq 7: message,アリシア,I can't wait!<br> ,300201000,vc_10440100001_003_01,chara_2
VI[7] = "Em mong quá!<br> "

# seq 8: message,？？？,Ah，you two，please wait a moment! You're about to go out，aren't<br>you?<br> ,104401000G,vc_10440100001_004_01,chara_1
VI[8] = "À‚ hai người kia‚ làm ơn đợi một chút! Hai người sắp ra ngoài phải<br>không ạ?<br> "

# seq 9: message,アリシア,Yes，we are... Why?<br> ,300201000,vc_10440100001_005_01,chara_2
VI[9] = "Vâng‚ bọn em định đi... Có chuyện gì sao?<br> "

# seq 10: message,？？？,In that case，you might want to put it off a bit. There is going to be a<br>heavy downpour!<br> ,104401000G,vc_10440100001_006_01,chara_1
VI[10] = "Vậy thì‚ hai người nên dời lại một chút thì hơn ạ.<br>Sắp có mưa rất to đấy!<br> "

# seq 11: message,アリシア,Oh，rain? But it's so sunny...?<br> ,300201000,vc_10440100001_007_01,chara_2
VI[11] = "Ồ‚ mưa sao? Nhưng trời đẹp thế này cơ mà...?<br> "

# seq 12: message,？？？,It looks clear now，but there is a high chance of rain!<br> ,104401000G,vc_10440100001_008_01,chara_1
VI[12] = "Nhìn thì trời đang quang đấy‚ nhưng khả năng mưa rất cao ạ!<br> "

# seq 13: message,アリシア,What do you think，Commander? She seems pretty confident...<br> ,300201000,vc_10440100001_009_01,chara_2
VI[13] = "Anh nghĩ sao‚ Chỉ Huy? Cô ấy có vẻ tự tin lắm...<br> "

# seq 14: message,<user>,A weather forecast? People have been predicting the weather from<br>clouds and wind for ages，but in reality，the accuracy isn't very high.<br> 
VI[14] = "Dự báo thời tiết hả? Từ xưa đã có người đoán thời tiết qua<br>mây và gió rồi‚ nhưng thực tế độ chính xác chẳng cao lắm đâu.<br> "

# seq 15: message,<user>,Weather's fickle anyway. If we let it bother us，we'd never get out.<br> 
VI[15] = "Thời tiết vốn thất thường mà. Cứ lo từng tí thì chẳng đi đâu được.<br> "

# seq 16: message,<user>,Alicia，let's go without worrying. We can't afford to miss this<br>precious break.<br> 
VI[16] = "Alicia‚ đi thôi đừng lo.<br>Lỡ mất khoảng thời gian nghỉ quý báu này thì phí lắm.<br> "

# seq 17: message,アリシア,Y-yes...<br> ,300201000,vc_10440100001_010_01,chara_2
VI[17] = "D-dạ...<br> "

# seq 18: message,アリシア,I'm sorry. Thank you for the warning. We appreciate the thought.<br> ,300201000,vc_10440100001_011_01,chara_2
VI[18] = "Xin lỗi ạ. Cảm ơn cô đã nhắc nhở. Chúng tôi xin ghi nhận tấm lòng.<br> "

# seq 19: message,？？？,I understand. Please take care—<br> ,104401000G,vc_10440100001_012_01,chara_1
VI[19] = "Em hiểu rồi ạ. Xin hãy đi đường cẩn thận—<br> "

# seq 20: messageTextCenter,,<size=48>—Several Dozen Minutes Later</size>,,,on
VI[20] = "<size=48>—Vài Chục Phút Sau</size>"

# seq 21: messageTextCenter,,<size=48>—The Next Day</size>,,,on
VI[21] = "<size=48>—Ngày Hôm Sau</size>"

# seq 22: message,？？？,I wonder if you two managed to stay dry yesterday...<br> ,104401000G,vc_10440100001_013_01,chara_1
VI[22] = "Không biết hôm qua hai người có tránh được mưa không nhỉ...<br> "

# seq 23: message,アリシア,Commander! There she is!<br> ,300201000,vc_10440100001_014_01,chara_2
VI[23] = "Chỉ Huy! Cô ấy kìa!<br> "

# seq 24: message,<user>,There you are.<br> 
VI[24] = "Ra là cô à.<br> "

# seq 25: message,？？？,Oh，it's you from yesterday! Were you okay after that?<br> ,104401000G,vc_10440100001_015_01,chara_1
VI[25] = "Ồ‚ là hai người hôm qua! Lúc đó hai người có sao không ạ?<br> "

# seq 26: message,<user>,No. Like you said，we got caught in the downpour and ended up a pair<br>of drowned rats—soaked right through to our underwear.<br> 
VI[26] = "Không. Đúng như cô nói‚ bọn tôi dính trận mưa như trút nước và thành<br>một đôi chuột lột—ướt sũng đến tận quần lót.<br> "

# seq 27: message,アリシア,It was awful... *sniff*<br> ,300201000,vc_10440100001_016_01,chara_2
VI[27] = "Kinh khủng lắm ạ... *hức*<br> "

# seq 28: message,？？？,Oh dear... That must have been dreadful. I should have tried harder to<br>make you stay. My apologies for my oversight.<br> ,104401000G,vc_10440100001_017_01,chara_1
VI[28] = "Trời ơi... Chắc hai người khổ sở lắm. Đáng lẽ em phải cố giữ hai người<br>lại mới phải. Em xin lỗi vì đã không chu toàn.<br> "

# seq 29: message,<user>,Don't worry about it. We were the ones who ignored your warning.<br>That was rude of us. Sorry.<br> 
VI[29] = "Đừng bận tâm. Là bọn tôi đã phớt lờ lời khuyên của cô.<br>Thái độ đó thật bất lịch sự. Xin lỗi nhé.<br> "

# seq 30: message,？？？,Not at all. Please don't give it another thought!<br> ,104401000G,vc_10440100001_018_01,chara_1
VI[30] = "Không sao đâu ạ! Xin đừng bận tâm!<br> "

# seq 31: message,<user>,Anyway，there's something I wanted to ask you，so I was looking for<br>you.<br> 
VI[31] = "Mà này‚ có chuyện tôi muốn hỏi cô‚<br>nên mới đi tìm đấy.<br> "

# seq 32: message,<user>,How did you know it was going to rain? The way you said it，you<br>sounded pretty sure of yourself，didn't you?<br> 
VI[32] = "Sao cô biết trời sắp mưa? Cái cách cô nói hôm qua‚<br>trông cô khá tự tin mà phải không?<br> "

# seq 33: message,？？？,Oh my! So the Lord Commander has taken an interest in me. Thank<br>you. I am greatly honored.<br> ,104401000G,vc_10440100001_019_01,chara_1
VI[33] = "Ồ trời! Vậy là Ngài Chỉ Huy đã để ý đến em sao. Cảm ơn<br>Ngài. Em vô cùng vinh hạnh.<br> "

# seq 34: message,<user>,Hm? You already knew who I was?<br> 
VI[34] = "Hử? Cô biết tôi à?<br> "

# seq 35: message,？？？,Yes! After all，the Lord Commander is the most famous person at the<br>Frontline Base!♪<br> ,104401000G,vc_10440100001_020_01,chara_1
VI[35] = "Vâng ạ! Dù sao thì Ngài Chỉ Huy cũng là người nổi tiếng nhất ở<br>Căn Cứ Tiền Tuyến mà!♪<br> "

# seq 36: message,ヤチヨ,I should have introduced myself earlier. I am Yachiyo. I come from a<br>family of shrine maidens in the eastern land of Hourai.<br> ,104401000G,vc_10440100001_021_01,chara_1
VI[36] = "Em đáng lẽ phải tự giới thiệu từ sớm mới phải. Em là Yachiyo ạ. Em xuất thân từ<br>gia đình vu nữ ở vùng đất phía đông Hourai.<br> "

# seq 37: message,<user>,A shrine maiden is，I'm pretty sure，a curse master who serves the<br>gods.<br> 
VI[37] = "Vu nữ‚ nếu tôi nhớ không nhầm‚ là pháp sư phục vụ<br>thần linh đúng không?<br> "

# seq 38: message,ヤチヨ,That is correct. The Lord Commander is indeed well-read.<br> ,104401000G,vc_10440100001_022_01,chara_1
VI[38] = "Đúng vậy ạ. Ngài Chỉ Huy quả là người uyên bác.<br> "

# seq 39: message,<user>,(For someone who serves the gods，she sure is dressed<br>provocatively...)<br> 
VI[39] = "(Phục vụ thần linh mà<br>ăn mặc gợi cảm thế này cơ à...)<br> "

# seq 40: message,ヤチヨ,Lord Commander? Is there something about my chest?<br> ,104401000G,vc_10440100001_023_01,chara_1
VI[40] = "Ngài Chỉ Huy? Ngực em có gì sao ạ?<br> "

# seq 41: message,<user>,It's nothing. Go on. Does that bloodline have anything to do with the<br>ability to read the weather?<br> 
VI[41] = "Không có gì. Cứ nói tiếp đi. Dòng máu đó có liên quan gì đến<br>khả năng đọc thời tiết không?<br> "

# seq 42: message,ヤチヨ,Yes. My family has been connected to the Dragon God since ancient<br>times.<br> ,104401000G,vc_10440100001_024_01,chara_1
VI[42] = "Vâng ạ. Gia tộc em đã có duyên với Long Thần<br>từ thời xa xưa.<br> "

# seq 43: message,<user>,A dragon，huh? I've heard of those. It's a dragon，right?<br> 
VI[43] = "Long à? Tôi cũng có nghe nói đến. Chắc là con rồng phương Đông đúng không?<br> "

# seq 44: message,ヤチヨ,Wh-what!<br> ,104401000G,vc_10440100001_025_01,chara_1
VI[44] = "C-cái gì!<br> "

# seq 45: message,ヤチヨ,How dare you say such a thing!<br> ,104401000G,vc_10440100001_026_01,chara_1
VI[45] = "Sao Ngài dám nói như vậy!<br> "

# seq 46: message,<user>,Whoa...!<br> 
VI[46] = "Ối...!<br> "

# seq 47: message,ヤチヨ,How dare you equate our Dragon God with a mere fire-breathing<br>lizard! That's blasphemy! Utter blasphemy!<br> ,104401000G,vc_10440100001_027_01,chara_1
VI[47] = "Sao Ngài dám ví Long Thần của chúng em với cái thằng thằn lằn phun lửa<br>đó chứ! Bất kính! Quá đỗi bất kính!<br> "

# seq 48: message,ヤチヨ,The Dragon God is completely different from a dragon! His body is<br>slender and long，and he looks cool! His beard flows in the wind，so elegant!<br> ,104401000G,vc_10440100001_028_01,chara_1
VI[48] = "Long Thần hoàn toàn khác với mấy con dra-gôn! Thân Ngài thon dài và đẹp lắm!<br>Râu Ngài tung bay trong gió‚ thật thanh tao!<br> "

# seq 49: message,ヤチヨ,And when he delivers divine punishment，it's not with barbaric<br>flames—it's said he uses refined lightning!<br> ,104401000G,vc_10440100001_029_01,chara_1
VI[49] = "Và khi ban hình phạt thần thánh‚ Ngài không dùng lửa dã man<br>đâu—mà người ta đồn Ngài dùng sấm sét thanh cao kia!<br> "

# seq 50: message,ヤチヨ,He's nothing like those squat，chubby dragons!<br> ,104401000G,vc_10440100001_030_01,chara_1
VI[50] = "Ngài chẳng giống mấy con dra-gôn lùn tịt mập ú kia chút nào đâu ạ!<br> "

# seq 51: message,<user>,O-okay，okay! My bad! Dragons and the Dragon God are completely<br>different! I've got it!<br> 
VI[51] = "Đ-được rồi được rồi! Tôi sai rồi! Dra-gôn và Long Thần hoàn toàn<br>khác nhau! Tôi nhớ rồi!<br> "

# seq 52: message,ヤチヨ,Yes! Please be careful!<br> ,104401000G,vc_10440100001_031_01,chara_1
VI[52] = "Vâng ạ! Xin hãy cẩn thận lời nói ạ!<br> "

# seq 53: message,<user>,Oh，uh... so being born into a family connected to the Dragon<br>God—how does that relate to your weather-reading ability?<br> 
VI[53] = "À‚ ờ... sinh ra trong gia đình có duyên với Long<br>Thần—thế thì liên quan thế nào đến khả năng đọc thời tiết của cô?<br> "

# seq 54: message,ヤチヨ,Since I was a child，I've had the Dragon God，who governs the<br>weather，dwelling within me.<br> ,104401000G,vc_10440100001_032_01,chara_1
VI[54] = "Từ nhỏ‚ em đã có Long Thần‚ vị thần cai quản<br>thời tiết‚ ngự trị trong người em rồi ạ.<br> "

# seq 55: message,<user>,Wh-what! A dragon inside a human!<br> 
VI[55] = "C-cái gì! Rồng thần ở trong người người à!<br> "

# seq 56: message,ヤチヨ,Yes!♪ The Dragon God's spirit resides within me.<br> ,104401000G,vc_10440100001_033_01,chara_1
VI[56] = "Vâng ạ!♪ Linh hồn của Long Thần ngự trong em.<br> "

# seq 57: message,ヤチヨ,Since I was little，through both hard times and good times，we have<br>always been together in my heart，and I have been on good terms with him.<br> ,104401000G,vc_10440100001_034_01,chara_1
VI[57] = "Từ khi em còn bé‚ cả khi khó khăn lẫn khi vui vẻ‚ chúng em<br>luôn ở bên nhau trong trái tim em‚ và em đã có mối quan hệ tốt đẹp với Ngài.<br> "

# seq 58: message,ヤチヨ,I was able to foresee yesterday's rain because I heard the Dragon<br>God's voice.<br> ,104401000G,vc_10440100001_035_01,chara_1
VI[58] = "Em có thể thấy trước cơn mưa hôm qua là vì em đã nghe được giọng của Long<br>Thần.<br> "

# seq 59: message,<user>,Hmm... So the dragon living inside you is predicting the<br>weather—that's an incredibly useful ability.<br> 
VI[59] = "Hừm... Vậy là con rồng sống trong người cô đang dự báo<br>thời tiết—đúng là năng lực hữu ích đáng kinh ngạc.<br> "

# seq 60: message,アリシア,That's right. If you know it's going to rain in advance，you won't have<br>to worry about whether to bring an umbrella when you go out.<br> ,300201000,vc_10440100001_036_01,chara_2
VI[60] = "Đúng vậy. Nếu biết trước trời sắp mưa‚ thì ra ngoài<br>khỏi phải lo có nên mang ô hay không.<br> "

# seq 61: message,アリシア,And it's handy for hanging laundry. Oh! It would be a huge help for<br>farmers，wouldn't it?<br> ,300201000,vc_10440100001_037_01,chara_2
VI[61] = "Với lại tiện cho việc phơi quần áo nữa. Ồ! Mà nó sẽ giúp ích rất nhiều cho<br>bà con nông dân nhỉ?<br> "

# seq 62: message,<user>,Yeah，and if you can detect floods and wind damage in advance，we<br>could start evacuating people with plenty of time to spare.<br> 
VI[62] = "Ừ‚ và nếu có thể phát hiện lũ lụt và thiệt hại do gió trước‚ chúng ta<br>có thể bắt đầu sơ tán dân sớm hơn nhiều.<br> "

# seq 63: message,<user>,Not only that，it helps with deciding tactics. Being able to read the<br>weather is that useful.<br> 
VI[63] = "Không chỉ thế‚ nó còn giúp ích cho việc quyết định chiến thuật. Đọc được<br>thời tiết hữu ích đến thế đấy.<br> "

# seq 64: message,アリシア,That really is an amazing power，isn't it!<br> ,300201000,vc_10440100001_038_01,chara_2
VI[64] = "Đúng là năng lực tuyệt vời mà nhỉ!<br> "

# seq 65: message,ヤチヨ,...Ah，umm，I hate to say this while you're all praising me，but...<br> ,104401000G,vc_10440100001_039_01,chara_1
VI[65] = "...À‚ ừm‚ em không muốn nói giữa lúc mọi người đang khen em đâu‚ nhưng mà...<br> "

# seq 66: message,ヤチヨ,It's not really that useful，actually...<br> ,104401000G,vc_10440100001_040_01,chara_1
VI[66] = "Thực ra nó cũng không hữu ích đến vậy đâu ạ...<br> "

# seq 67: message,<user>,Hm? Is there some risk involved?<br> 
VI[67] = "Hử? Có rủi ro gì sao?<br> "

# seq 68: message,ヤチヨ,...Well，you see，the Dragon God is extremely capricious.<br> ,104401000G,vc_10440100001_041_01,chara_1
VI[68] = "...Thực ra thì‚ Long Thần rất thất thường ạ.<br> "

# seq 69: message,ヤチヨ,It does grant me predictions，but they often don't come true—<br> ,104401000G,vc_10440100001_042_01,chara_1
VI[69] = "Ngài có ban cho em những dự báo‚ nhưng chúng thường không đúng—<br> "

# seq 70: message,ヤチヨ,Sometimes it only tells me 'it will rain' without telling me when.<br> ,104401000G,vc_10440100001_043_01,chara_1
VI[70] = "Có khi Ngài chỉ bảo em 'sắp mưa' thôi‚ chứ không nói khi nào.<br> "

# seq 71: message,ヤチヨ,It could be a few minutes later，or even a week later—<br> ,104401000G,vc_10440100001_044_01,chara_1
VI[71] = "Có thể là vài phút sau‚ hoặc thậm chí cả tuần sau—<br> "

# seq 72: message,アリシア,Th-then that's hardly a hit，is it...?<br> ,300201000,vc_10440100001_045_01,chara_2
VI[72] = "V-vậy thì cũng khó gọi là đúng nhỉ...?<br> "

# seq 73: message,<user>,Sounds pretty mean—doesn't seem like a nice personality.<br> 
VI[73] = "Nghe khá xấu tính đấy—có vẻ không phải tính cách tốt.<br> "

# seq 74: message,ヤチヨ,Ugh... I can't deny that...<br> ,104401000G,vc_10440100001_046_01,chara_1
VI[74] = "Ực... Em không thể phủ nhận điều đó...<br> "

# seq 75: message,アリシア,It's got incredible power，but it's a bit mean and capricious... Sounds<br>like a certain someone，doesn't it?<br> ,300201000,vc_10440100001_047_01,chara_2
VI[75] = "Nó có sức mạnh đáng kinh ngạc‚ nhưng hơi xấu tính và thất thường... Nghe<br>giống ai đó nhỉ?<br> "

# seq 76: message,<user>,Hey，wait. Are you talking about me?<br> 
VI[76] = "Này‚ khoan đã. Có phải đang nói về tôi không đấy?<br> "

# seq 77: message,アリシア,Hmm，I wonder?<br> ,300201000,vc_10440100001_048_01,chara_2
VI[77] = "Hừm‚ em không biết nữa?<br> "

# seq 78: message,ヤチヨ,My predictions are often inaccurate，so people don't trust me. In<br>fact，sometimes they find me a nuisance—<br> ,104401000G,vc_10440100001_049_01,chara_1
VI[78] = "Dự báo của em thường không chính xác‚ nên mọi người không tin tưởng em. Thực<br>ra‚ đôi khi họ còn thấy em phiền phức nữa—<br> "

# seq 79: message,ヤチヨ,Eventually it became hard for me to stay，so I've been traveling from<br>place to place.<br> ,104401000G,vc_10440100001_050_01,chara_1
VI[79] = "Cuối cùng em không thể ở lại được nữa‚<br>nên em đã đi hết nơi này đến nơi khác.<br> "

# seq 80: message,アリシア,That's so sad...<br> ,300201000,vc_10440100001_051_01,chara_2
VI[80] = "Tội nghiệp quá...<br> "

# seq 81: message,ヤチヨ,Anyway，that's why my weather forecasting isn't an all-powerful<br>ability.<br> ,104401000G,vc_10440100001_052_01,chara_1
VI[81] = "Dù sao thì‚ đó là lý do tại sao khả năng dự báo thời tiết của em<br>không phải là năng lực vạn năng.<br> "

# seq 82: message,ヤチヨ,If it seems I won't be accepted by the people at the Frontline Base，<br>I'll leave here too.<br> ,104401000G,vc_10440100001_053_01,chara_1
VI[82] = "Nếu như em không được mọi người ở Căn Cứ Tiền Tuyến chấp nhận‚<br>em cũng sẽ rời khỏi đây thôi.<br> "

# seq 83: message,<user>,No，hold on. Don't get so down on yourself.<br> 
VI[83] = "Không‚ khoan đã. Đừng tự ti như vậy.<br> "

# seq 84: message,<user>,It might not be a perfect ability，but surely your forecasts are more<br>accurate than ordinary people looking at the sky and guessing?<br> 
VI[84] = "Có thể không phải năng lực hoàn hảo‚ nhưng chắc chắn dự báo của cô<br>chính xác hơn người thường nhìn trời mà phỏng đoán chứ?<br> "

# seq 85: message,<user>,Yesterday you said it would rain，and we got soaked in that sudden<br>downpour. That's proof you're hearing the Dragon God's voice.<br> 
VI[85] = "Hôm qua cô nói trời sẽ mưa và bọn tôi đã ướt như chuột lột trong trận<br>mưa như trút đó. Đó là bằng chứng cô nghe được giọng của Long Thần.<br> "

# seq 86: message,<user>,As I said，accurate forecasts aid farming，disaster prevention，and<br>warfare. Yachiyo's power is invaluable and beyond human understanding.<br> 
VI[86] = "Như tôi đã nói‚ dự báo chính xác giúp ích cho nông nghiệp‚ phòng chống thiên tai và<br>chiến tranh. Năng lực của Yachiyo là vô giá và vượt quá hiểu biết của con người.<br> "

# seq 87: message,ヤチヨ,P-please don't praise me so much! It's not my power，it's the Dragon<br>God's power after all...<br> ,104401000G,vc_10440100001_054_01,chara_1
VI[87] = "X-xin đừng khen em quá lời! Đâu phải năng lực của em‚ đó là sức mạnh của Long<br>Thần mà...<br> "

# seq 88: message,<user>,The Dragon God wouldn't lend its power to someone it dislikes. That<br>proves you're a good person. I find you likable from talking to you.<br> 
VI[88] = "Long Thần sẽ không cho mượn sức mạnh cho người Ngài không thích đâu. Điều đó<br>chứng tỏ cô là người tốt. Tôi thấy cô dễ mến khi nói chuyện.<br> "

# seq 89: message,ヤチヨ,Ah，a-wah!? L-likable，you say— Th-that's the first time I've ever<br>been told that by a man...<br> ,104401000G,vc_10440100001_055_01,chara_1
VI[89] = "A‚ ơ-vui!? D-dễ mến— L-lần đầu tiên em được<br>đàn ông nói như vậy...<br> "

# seq 90: message,<user>,Don't be shy. It's the truth. Walk tall and stay at the Frontline Base.<br>I，your Commander，give you permission.<br> 
VI[90] = "Đừng ngại. Đó là sự thật mà. Hãy ngẩng cao đầu ở lại Căn Cứ Tiền Tuyến.<br>Ta—Chỉ Huy của cô—cho phép.<br> "

# seq 91: message,ヤチヨ,...!? Commander，you're concerned about my past...?<br> ,104401000G,vc_10440100001_056_01,chara_1
VI[91] = "...!? Chỉ Huy‚ Ngài quan tâm đến quá khứ của em sao...?<br> "

# seq 92: message,アリシア,When the other person is pretty and cute，you just can't help<br>yourself... Yachiyo，you'd better be careful!<br> ,300201000,vc_10440100001_057_01,chara_2
VI[92] = "Hễ đối phương xinh đẹp và dễ thương là anh lại thế đấy...<br>Yachiyo này‚ chị phải cẩn thận đấy!<br> "

# seq 93: message,ヤチヨ,...<br> ,104401000G,vc_10440100001_058_01,chara_1
VI[93] = "………<br> "

# seq 94: message,アリシア,Yachiyo? What's wrong?<br> ,300201000,vc_10440100001_059_01,chara_2
VI[94] = "Yachiyo? Có chuyện gì vậy?<br> "

# seq 95: message,ヤチヨ,Ah，well... about Commander being popular with women... I think I<br>understand all too well now... What am I going to do!♡<br> ,104401000G,vc_10440100001_060_01,chara_1
VI[95] = "A‚ ờ thì... chuyện Chỉ Huy được phụ nữ yêu thích ấy... Em nghĩ em<br>hiểu quá rõ rồi... Em phải làm sao đây!♡<br> "

# seq 96: message,,—*rumble，rumble，rumble*<br> 
VI[96] = "—*ầm‚ ầm‚ ầm*<br> "

# seq 97: message,アリシア,Huh? Suddenly I hear thunder...?<br> ,300201000,vc_10440100001_061_01,on
VI[97] = "Hả? Tự nhiên em nghe tiếng sấm...?<br> "

# seq 98: message,,—*whoosh!*<br> 
VI[98] = "—*ào ào!*<br> "

# seq 99: message,アリシア,Wawawa! What a sudden sunshower!<br> ,300201000,vc_10440100001_062_01,chara_2
VI[99] = "Wá wá wá! Mưa bóng mây dữ vậy!<br> "

# seq 100: message,<user>,And it's pouring! Hurry up and get inside! You'll catch a cold!<br> 
VI[100] = "Mà mưa to quá! Mau vào trong nhà đi! Cảm lạnh bây giờ!<br> "

# seq 101: message,ヤチヨ,Y-yes!<br> ,104401000G,vc_10440100001_063_01,chara_1
VI[101] = "V-vâng ạ!<br> "

# seq 102: message,<user>,*phew*... That was close. You're okay too，Yachiyo?<br> 
VI[102] = "*phù*... Suýt thì ướt. Cô cũng ổn chứ‚ Yachiyo?<br> "

# seq 103: message,ヤチヨ,Yes，thanks to you...<br> ,104401000G,vc_10440100001_064_01,chara_1
VI[103] = "Vâng‚ nhờ có Ngài...<br> "

# seq 104: message,<user>,That was a sudden downpour. Didn't the Dragon God give you any<br>warning?<br> 
VI[104] = "Đúng là trận mưa bất chợt.<br>Long Thần không báo cho cô gì sao?<br> "

# seq 105: message,ヤチヨ,Yes... it is strange. Whenever I am about to be caught in the rain，the<br>Dragon God always warns me，but...<br> ,104401000G,vc_10440100001_065_01,chara_1
VI[105] = "Vâng... lạ thật ạ. Mỗi khi em sắp bị mưa ướt‚<br>Long Thần luôn báo cho em cơ mà...<br> "

# seq 106: message,ヤチヨ,That is also why I could tell you and Alicia yesterday that 'it looks<br>like rain.' Because you were headed in the same direction.<br> ,104401000G,vc_10440100001_066_01,chara_1
VI[106] = "Đó cũng là lý do hôm qua em có thể báo cho Ngài và Alicia rằng 'có vẻ<br>sắp mưa.' Vì Ngài đi cùng hướng với em.<br> "

# seq 107: message,<user>,So the Dragon God really is whimsical after all.<br> 
VI[107] = "Vậy ra Long Thần quả thực là thất thường.<br> "

# seq 108: message,<user>,But your power is very useful. Can I ask you to provide weather<br>forecasts from time to time?<br> 
VI[108] = "Nhưng năng lực của cô rất hữu ích. Tôi có thể nhờ cô dự báo<br>thời tiết thỉnh thoảng không?<br> "

# seq 109: message,ヤチヨ,Yes，of course! I will do my best，so I am counting on you，<br>Commander!♪<br> ,104401000G,vc_10440100001_067_01,chara_1
VI[109] = "Vâng‚ tất nhiên rồi ạ! Em sẽ cố gắng hết sức‚ nên em trông cậy vào<br>Ngài‚ thưa Chỉ Huy!♪<br> "

# seq 110: message,,—Rumble，rumble，rumble.<br> 
VI[110] = "—Ầm‚ ầm‚ ầm.<br> "

# ---- Verification ----
assert len(VI) == len(records), f"VI entries {len(VI)} != records {len(records)}"

# Check no ASCII comma in VI text
for seq, vi in VI.items():
    comma_positions = []
    for j, ch in enumerate(vi):
        if ch == ',':
            comma_positions.append(j)
    if comma_positions:
        print(f"WARNING: seq {seq} has ASCII comma at positions {comma_positions}: {vi[:60]}")

# Count <br> per record for preflight
print("\n=== BR count preflight ===")
all_ok = True
for (ln_no, cmd, en_line), seq in zip(records, sorted(VI.keys())):
    vi_text = VI[seq]
    # For message lines: extract EN text field, count <br>
    fields_en = en_line.split(',', 5)
    fields_vi = vi_text  # This is the replacement text field
    
    if cmd == 'title':
        en_tf = fields_en[1] if len(fields_en) > 1 else ""
        # For title, compare whole field
        en_br = en_tf.count('<br>')
        vi_br = fields_vi.count('<br>')
    elif cmd == 'messageTextCenter' or cmd == 'messageTextUnder':
        # These have format: cmd,,<tag>text</tag>,,,flags
        # Find the text between commas
        if len(fields_en) >= 3:
            en_tf = fields_en[2]
        else:
            en_tf = ""
        en_br = en_tf.count('<br>')
        vi_br = fields_vi.count('<br>')
    else:  # message
        if len(fields_en) >= 3:
            en_tf = fields_en[2]
        else:
            en_tf = ""
        en_br = en_tf.count('<br>')
        vi_br = fields_vi.count('<br>')
    
    if en_br != vi_br:
        print(f"  BR MISMATCH seq={seq:3d} line={ln_no:4d} {cmd:20s} EN_br={en_br} VI_br={vi_br}")
        print(f"    EN: {en_tf[:80]}")
        print(f"    VI: {fields_vi[:80]}")
        all_ok = False

if all_ok:
    print("  All <br> counts match! ✓")
else:
    print(f"\n  ERROR: BR count mismatches found - exiting")
    sys.exit(1)

# ---- Build VI file ----
out_lines = []
idx = 0  # records index
seq = 1

for i, ln in enumerate(lines):
    stripped = ln.rstrip('\r\n')
    if idx < len(records) and i == records[idx][0]:
        # This line is a text record - replace
        _, cmd, _ = records[idx]
        vi_text = VI[seq]
        
        # Rebuild line
        if cmd == 'title':
            # title,JP_title -> title,VI_title
            parts = stripped.split(',', 1)
            parts[1] = vi_text
            rebuilt = ','.join(parts)
        elif cmd == 'messageTextCenter' or cmd == 'messageTextUnder':
            # cmd,,<text>,,,flags -> rebuild only the text field (parts[2])
            parts = stripped.split(',', 5)
            parts[2] = vi_text
            rebuilt = ','.join(parts)
        else:  # message
            parts = stripped.split(',', 5)
            parts[2] = vi_text
            rebuilt = ','.join(parts)
        
        ending = ln[len(ln.rstrip('\r\n')):]  # preserve original line ending
        out_lines.append(rebuilt + ending)
        idx += 1
        seq += 1
    else:
        out_lines.append(ln)

# Final assertions
assert idx == len(records), f"Used {idx} of {len(records)} records"
assert len(out_lines) == len(lines), f"Out {len(out_lines)} != In {len(lines)} lines"

# Write
out_text = ''.join(out_lines)
if has_bom:
    out_bytes = b'\xef\xbb\xbf' + out_text.encode('utf-8')
else:
    out_bytes = out_text.encode('utf-8')

os.makedirs(os.path.dirname(VI_PATH), exist_ok=True)
with open(VI_PATH, 'wb') as f:
    f.write(out_bytes)

print(f"\n✓ Written {VI_PATH} ({len(out_bytes)} bytes, {len(out_lines)} lines)")
print("Done!")

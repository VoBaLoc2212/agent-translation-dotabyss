#!/usr/bin/env python3
"""Build VI output for hmn_10470100003 (Merem fortune teller scene).
EN-asset-is-English case with mixed JP-title / EN-message.
86 text records: 1 title + 3 messageTextCenter + 82 message.
"""
import json, re, sys
from pathlib import Path

# --- Paths ---
ROOT = Path("E:/AgentTranslation")
EN_FILE = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10470100003.txt"
VI_FILE = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10470100003.txt"
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10470100003/ja.json"
WORK = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10470100003_full")

# --- Load JP source ---
with open(JA_JSON, 'r', encoding='utf-8') as f:
    ja_data = json.load(f)
jp_map = {}  # keyed by seq
jp_entries = [v for k, v in ja_data.items() if v.strip()]

# --- Read EN asset ---
with open(EN_FILE, 'r', encoding='utf-8-sig') as f:
    raw = f.read()

has_bom = raw.startswith('\ufeff')
lines = raw.splitlines(True)  # keep line endings
has_crlf = b'\r\n' in raw.encode('utf-8')

# Separate trailing <br> suffix from message body
def split_suffix(field):
    """Return (body, suffix) where suffix is trailing tags+whitespace."""
    m = re.search(r'(<[^>]+>\s*)+$', field)
    if m:
        return field[:m.start()], m.group(0)
    return field, ''

# --- VI translations by seq (1-indexed) ---
# Characters: メレム(Merem) - flustered but principled fortune teller, em/anh with Chỉ Huy
# <user> = Commander/Chỉ Huy
# クルル(Kururu) - childlike, calls Commander 'chủ nhân'
# ソフィア(Sofia) - shy girl
# マリナ(Marina) - playful wife, calls Commander 'phu quân'

VI = {
    # seq 1: title (JP in EN asset) - "占い師が導く運命の分かれ道"
    1: "Ngã Rẽ Định Mệnh Dẫn Lối Bởi Thầy Bói",
    
    # seq 2: messageTextCenter (first center card)
    2: "<size=48>——Tầng Nông Đại Huyệt—Nơi Xa Lạ</size>",
    
    # seq 3: message,メレム, *pant,pant*...
    3: "*hễ hả，hễ hả*... Chân tôi mỏi quá...<br> ",
    
    # seq 4: message,メレム, I was going to divine...
    4: "Tôi định bói xem mất bao lâu để ra khỏi Đại Huyệt...<br>A，tôi không có dụng cụ! Sao lại không có chứ! Huwaaaa!<br> ",
    
    # seq 5: message,<user>, Not being able to divine...
    5: "Không bói được mà khiến cậu bất lực thế à? Ừm，với độ<br>chính xác của cậu，tôi đành phải dựa vào cậu thôi.<br> ",
    
    # seq 6: message,メレム, Commander, it's fine to leave...
    6: "Chỉ Huy，cứ bỏ tôi lại cũng được thôi. Không có<br>bói toán，tôi chỉ là một chị gái vô dụng thôi...<br> ",
    
    # seq 7: message,<user>, There's no reason to abandon...
    7: "Không có lý do gì để bỏ rơi một chị gái hơi vô dụng nhưng dễ thương cả.<br>Thà rằng tôi muốn đưa cậu đi cùng.<br> ",
    
    # seq 8: message,メレム, Is that really okay...?
    8: "Thật ổn sao...? Tôi chẳng có dụng cụ bói toán nào cả...?<br> ",
    
    # seq 9: message,<user>, It's not that I believed...
    9: "Không phải tôi tin vào chậu thủy tinh hay đạo cụ ma thuật đâu. Tôi tin<br>là vì đó chính là lời cậu nói đấy，Merem.<br> ",
    
    # seq 10: message,メレム, ...Why did you trust me?
    10: "...Sao anh lại tin tôi vậy? Ý tôi là，bói của tôi chính xác thật，nhưng...<br> ",
    
    # seq 11: message,<user>, Well, it's true that they were accurate...
    11: "Ừm，đúng là chúng chính xác thật. Lúc đầu，tôi đã nghi ngờ cậu có<br>thể là gián điệp nào đó đấy，biết không.<br> ",
    
    # seq 12: message,メレム, E-Ehhhh! A spy!
    12: "Ố-Ốề! Gián điệp! Sao anh lại nghĩ thế chứ?<br> ",
    
    # seq 13: message,<user>, You saw through my relationship with Alicia...
    13: "Cậu đã nhìn thấu mối quan hệ của tôi với Alicia ngay lần đầu gặp mặt，<br>đúng không? Tôi đã nghĩ cậu đang ra vẻ là biết rõ tình hình.<br> ",
    
    # seq 14: message,メレム, So you came all this way...
    14: "Thế mà anh vẫn đi cùng tôi tới tận đây dù vẫn nghi ngờ tôi sao...?<br> ",
    
    # seq 15: message,<user>, I said 'at first,' didn't I?
    15: "Tôi đã nói là 'lúc đầu' mà，phải không? Khi cậu giảng đạo về việc tôi<br>nên thay đổi thói tán gái，tôi nhận ra cậu là một thầy bói tốt bụng.<br> ",
    
    # seq 16: message,メレム, B-but, I really thought...
    16: "N-nhưng，tôi thực sự nghĩ anh nên thay đổi cách sống của mình...<br> ",
    
    # seq 17: message,<user>, I don't mind. Lecturing someone...
    17: "Tôi không phiền đâu. Giảng đạo cho người được gọi là Chỉ Huy<br>cho thấy cậu đúng là một thầy bói đầy tinh thần đấy.<br> ",
    
    # seq 18: message,<user>, Not twisting the results that far...
    18: "Không bẻ cong kết quả đến mức đó... Cậu chỉ làm vậy nếu cậu<br>tự hào rằng bói toán của mình thực sự chính xác，đúng không?<br> ",
    
    # seq 19: message,メレム, If I didn't think I could get it right...
    19: "Nếu tôi không nghĩ mình có thể làm đúng，tôi đã chẳng thèm bói...<br> ",
    
    # seq 20: message,メレム, Besides, I've decided...
    20: "Hơn nữa，tôi đã quyết định rằng tôi tuyệt đối sẽ không đi theo những<br>người không tin vào bói toán và chỉ muốn lợi dụng nó.<br> ",
    
    # seq 21: message,<user>, Hoh, there were people like that?
    21: "Hố hố，có những người như thế à?<br> ",
    
    # seq 22: message,メレム, Yes, there are important people...
    22: "Vâng，có những người quan trọng，vì bói toán của tôi<br>chính xác，bắt tôi lặp đi lặp lại đến khi họ được kết quả như ý...<br> ",
    
    # seq 23: message,<user>, Yeah... I've heard...
    23: "Ừ... Tôi nghe nói có những thầy bói kiếm sống chỉ bằng cách<br>nói cho người quyền lực những gì họ muốn nghe.<br> ",
    
    # seq 24: message,メレム, Yes, exactly! I can't forgive that!
    24: "Đúng，chính xác! Tôi không thể tha thứ điều đó! Bói toán là để chỉ ra một<br>phần của số mệnh và làm kim chỉ nam cho con đường nên chọn!<br> ",
    
    # seq 25: message,メレム, To try and distort fate...
    25: "Cố gắng bóp méo số mệnh để phù hợp với bản thân... chẳng đời nào<br>một người như thế có thể đưa ra lời bói chính xác được!<br> ",
    
    # seq 26: message,<user>, The reason I felt I could trust...
    26: "Lý do tôi cảm thấy có thể tin những gì cậu nói，Merem，chính xác<br>là vì điều đó.<br> ",
    
    # seq 27: message,<user>, You believe in your own readings...
    27: "Cậu tin vào kết quả bói toán của mình hơn bất kỳ ai khác. Đó chính xác<br>là lý do tôi cũng cảm thấy có thể tin vào chúng.<br> ",
    
    # seq 28: message,<user>, The trustworthy fortune teller Merem...
    28: "Thầy bói đáng tin cậy Merem đã thấy vận may đang chờ đợi trong<br>Đại Huyệt này. Dĩ nhiên điều đó khiến tôi muốn tận mắt chứng kiến.<br> ",
    
    # seq 29: message,メレム, Commander...<br>
    29: "Chỉ Huy...<br> ",
    
    # seq 30: message,<user>, Well, it's not like I plan...
    30: "Ừm，cũng không phải tôi định thay đổi cách sống với phụ nữ đâu.<br> ",
    
    # seq 31: message,メレム, ... I really think you should work...
    31: "... Tôi thực sự nghĩ anh nên cải thiện chỗ đó đấy，biết chưa.<br> ",
    
    # seq 32: messageTextCenter (second center card)
    32: "<size=48>——Tầng Nông Đại Huyệt，Ngã Rẽ</size>",
    
    # seq 33: message,メレム, Waaah, it's another fork!
    33: "Waaa，lại một ngã rẽ nữa! Phải làm sao đây? Ai đó chỉ cho tôi<br>đường đi với... Chỉ Huy，bói giúp tôi đi...<br> ",
    
    # seq 34: message,<user>, It's not like I can tell fortunes...
    34: "Có phải tôi biết bói toán đâu...<br> ",
    
    # seq 35: message,<user>, That's it! Merem, can't you do...
    35: "Đúng rồi! Merem，cậu có thể bói mà không cần dụng cụ không? Như<br>tử vi hay tướng mạo học chẳng hạn...<br> ",
    
    # seq 36: message,メレム, Huh? Oh, yes, I can do any kind...
    36: "Hả? À，vâng，tôi có thể làm bất kỳ loại bói toán nào.<br> ",
    
    # seq 37: message,メレム, But with something unchangeable...
    37: "Nhưng với thứ không thể thay đổi như ngày sinh，tôi chỉ có thể thấy<br>cuộc đời tổng thể thôi... nên vô nghĩa ở đây đấy!<br> ",
    
    # seq 38: message,<user>, If unchangeable things won't work...
    38: "Nếu thứ không thay đổi không được，thì cậu có thể làm gì khác không?<br>Ví dụ，xem chỉ tay tôi thì sao?<br> ",
    
    # seq 39: message,メレム, Hand... palm reading, you say...
    39: "Tay... xem chỉ tay，anh nói vậy à...<br> ",
    
    # seq 40: message,<user>, It's not something that changes...
    40: "Nó không phải thứ thay đổi qua một đêm，nhưng cũng không bất biến.<br>Cậu có thể xem tương lai gần của tôi từ chỉ tay mà，đúng không Merem?<br> ",
    
    # seq 41: message,メレム, ... That is... ugh... maybe...
    41: "... Cái đó thì... ư... có lẽ... có thể được.<br> ",
    
    # seq 42: message,メレム, ...Dark Star, your fate is in great upheaval...
    42: "...Hắc Tinh，vận mệnh của ngươi đang biến chuyển lớn.<br>Lòng bàn tay ngươi cũng nên cho thấy một tương lai luôn thay đổi.<br> ",
    
    # seq 43: message,, Merem took the Commander's hand...
    43: "Merem nắm lấy tay Chỉ Huy và chầm chậm lướt những ngón tay lên đó.<br>Rồi cô lần theo những đường chỉ gần như vô hình.<br> ",
    
    # seq 44: message,メレム, Yes, the future hasn't changed...
    44: "Vâng，tương lai vẫn không thay đổi. Anh đã có được vận khí mạnh mẽ.<br>Anh sẽ gặp vận may lớn trong Đại Huyệt này.<br> ",
    
    # seq 45: message,メレム, ...That's the reading, but...
    45: "...Đó là kết quả bói，nhưng... Anh thấy thế nào...?<br> ",
    
    # seq 46: message,<user>, Yeah, you told me what I most wanted...
    46: "Ừ，cậu đã nói cho tôi điều tôi muốn nghe nhất.<br>Đúng như mong đợi ở cậu，Merem.<br> ",
    
    # seq 47: message,メレム, Ehhh! That was the same result...
    47: "Ểhhh! Kết quả đó giống hệt lần trước! Tôi đã chẳng nói gì mới cả!<br> ",
    
    # seq 48: message,<user>, That's just fine...
    48: "Như thế là tốt rồi.<br>Đi nào，Merem，lối rẽ bên trái này.<br> ",
    
    # seq 49: message,メレム, Huh? Why the left?
    49: "Hả? Sao lại là bên trái?<br> ",
    
    # seq 50: message,<user>, My gut.
    50: "Linh cảm của tôi.<br> ",
    
    # seq 51: message,メレム, 'Your gut?' ... Aaah, don't go...
    51: "'Linh cảm á?' ... Aaa，đừng đi mà Chỉ Huy，đợi tôi với!<br> ",
    
    # seq 52: message,, —After walking down an unfamiliar path...
    52: "—Sau một hồi đi trên con đường xa lạ，<br>họ nhanh chóng tìm thấy thứ mình đang tìm.<br> ",
    
    # seq 53: message,<user>, I see, as expected of Merem's fortune-telling...
    53: "Ra vậy，đúng như mong đợi ở tài bói toán của Merem—thực sự chính xác.<br>Nhìn kìa，viên đá lấp lánh trên mặt đất này.<br> ",
    
    # seq 54: message,メレム, This... is a magic stone, isn't it?
    54: "Cái này... là ma thạch，phải không?<br>Nó chứa một lượng ma lực kha khá nữa...<br> ",
    
    # seq 55: message,<user>, Yeah. No doubt there's an ore vein nearby...
    55: "Ừ. Không nghi ngờ gì nữa，có một mạch quặng gần đây.<br>Đây là một phát hiện lớn!<br> ",
    
    # seq 56: message,メレム, So this is the fortune you were destined...
    56: "Vậy đây là vận may mà anh định mệnh sẽ gặp phải à Chỉ Huy...<br>Nhưng sao anh biết nó ở đây...?<br> ",
    
    # seq 57: message,<user>, The reading said you'd still meet...
    57: "Lời bói nói rằng cậu vẫn sẽ gặp vận may，đúng không?<br> ",
    
    # seq 58: message,<user>, Then I thought that good fortune...
    58: "Vậy thì tôi đã nghĩ rằng vận may sẽ ở phía trước con đường tôi đã chọn.<br> ",
    
    # seq 59: message,メレム, Did you really trust me that much...?
    59: "Anh thực sự tin tôi nhiều đến thế sao...?<br> ",
    
    # seq 60: message,<user>, There's no reason to doubt...
    60: "Không có lý do gì để nghi ngờ.<br>Mọi lời bói của cậu cho đến giờ đều hoàn toàn chính xác.<br> ",
    
    # seq 61: message,<user>, And even if we found nothing...
    61: "Và dù chúng ta chẳng tìm thấy gì，cũng chẳng sao cả. Tôi đã được<br>ban phước với vận may được phiêu lưu cùng cậu rồi，Merem.<br> ",
    
    # seq 62: message,メレム, C-Commander... Yes, I enjoyed...
    62: "C-Chỉ Huy... Vâng，tôi cũng rất vui với cuộc phiêu lưu này.<br> ",
    
    # seq 63: message,<user>, I'm counting on you going forward...
    63: "Tôi trông cậy vào cậu từ giờ đấy，Merem. Tôi sẽ không yêu cầu cậu đưa ra<br>những lời bói thuận lợi chỉ vì cậu là thầy bói của tôi đâu.<br> ",
    
    # seq 64: message,<user>, Even if I don't like it...
    64: "Kể cả tôi không thích，hãy chỉ cho tôi con đường đến một tương lai<br>mà cậu cho là tốt. Dù tôi không hứa sẽ đi theo đâu.<br> ",
    
    # seq 65: message,メレム, Well... actually, I did a reading...
    65: "Ừm... thực ra，tôi đã bói ở dọc đường đấy. Tôi giữ bí mật vì<br>hơi ngượng，nhưng... anh muốn nghe không?<br> ",
    
    # seq 66: message,<user>, You've got me curious...
    66: "Cậu làm tôi tò mò rồi đấy. Nói đi.<br> ",
    
    # seq 67: message,メレム, Then—O Dark Star...
    67: "Vậy thì—Hỡi Hắc Tinh，kẻ sẽ trở thành trục của thế giới. Ta sẽ<br>vạch rõ số mệnh của ngươi. Theo lời bói của ta—<br> ",
    
    # seq 68: message,メレム, Our compatibility is... pretty good...
    68: "Sự hợp nhau của chúng ta... khá tốt đấy，tôi nghĩ vậy.<br> ",
    
    # seq 69: message,メレム, I think if we get closer...
    69: "Tôi nghĩ nếu chúng ta thân thiết hơn，sẽ có một tương lai tuyệt vời...<br>anh nghĩ sao?<br> ",
    
    # seq 70: message,<user>, I see. That's good to hear...
    70: "Ra vậy. Nghe tốt đấy. Vậy để tôi mời cậu cùng khám phá<br>Đại Huyệt nhé.<br> ",
    
    # seq 71: message,メレム, Call on me anytime...
    71: "Hãy gọi tôi bất cứ lúc nào anh cần. Dù là bói toán hay ma thuật，tôi sẽ giúp!<br> ",
    
    # seq 72: messageTextCenter (third center card)
    72: "<size=48>——Vài Ngày Sau，Tại Tiệm Bói Toán của Kẻ Thấu Thị Merem</size>",
    
    # seq 73: message,メレム, Now, please tell me what you'd like me to divine.
    73: "Nào，xin hãy cho tôi biết anh muốn tôi bói điều gì.<br> ",
    
    # seq 74: message,クルル, Hmm... Kururu wants to know...
    74: "Hmm... Kururu muốn biết liệu cô ấy có thể trở thành bạn tốt với<br>Chủ Nhân không.<br> ",
    
    # seq 75: message,メレム, ...Master... Commander, you mean?
    75: "...Chủ Nhân... ý cô là Chỉ Huy ạ? Rõ rồi，tôi sẽ bói.<br> ",
    
    # seq 76: message,ソフィア, It's not like I'm dying...
    76: "Không phải tôi rất muốn xem bói đâu，nhưng tôi hơi tò mò<br>về mức độ hợp nhau giữa tôi và Chỉ Huy...<br> ",
    
    # seq 77: message,メレム, ...Well, let's do the reading anyway...
    77: "...Thôi nào，cứ bói đi đã. Tôi không thể bảo đảm kết quả<br>đâu nhé.<br> ",
    
    # seq 78: message,マリナ, Nfufu, I know it's bound...
    78: "Nhu phù phù，tôi biết chắc là hoàn hảo rồi，nhưng cô có thể xem<br>vận tình yêu của tôi với Phu Quân tôi được không!♪<br> ",
    
    # seq 79: message,メレム, If you're going to decide the result yourself...
    79: "Nếu chị tự quyết kết quả rồi，thì không cần phải xem bói làm gì.<br>Đủ rồi. Buổi bói kết thúc. Hôm nay chúng tôi đóng cửa!<br> ",
    
    # seq 80: message,メレム, Everyone wants to see their compatibility...
    80: "Ai cũng muốn xem sự hợp nhau và vận tình yêu với<br>Chỉ Huy... Rốt cuộc người đàn ông đó dây dưa với bao nhiêu người vậy chứ!<br> ",
    
    # seq 81: message,<user>, Oh, Merem!
    81: "Ô，Merem!<br> ",
    
    # seq 82: message,メレム, C-Commander!
    82: "C-Chỉ Huy!<br> ",
    
    # seq 83: message,<user>, I came for a reading, but...
    83: "Tôi đến để xem bói，nhưng... tiệm đóng cửa rồi à?<br> ",
    
    # seq 84: message,メレム, ...No, I just finished a reading...
    84: "...Không，tôi vừa mới bói về anh xong. Sẽ hoàn toàn chính xác<br>đấy，nên hãy nghe cho kỹ.<br> ",
    
    # seq 85: message,<user>, Oh, yeah? What did it say?
    85: "Ồ，thế à? Nó nói gì?<br> ",
    
    # seq 86: message,メレム, The sign of woman troubles appears again today...
    86: "Hôm nay lại xuất hiện tướng đào hoa nạn rồi đấy. Đừng có đi chơi với<br>bất kỳ ai khác ngoài tôi...!<br> ",
}

# --- Build the VI file ---
text_cmds = ('title,', 'message,', 'messageTextCenter,', 'messageTextUnder,')
out_lines = []
seq = 0
errors = []

for ln in lines:
    stripped = ln.strip()
    if not stripped.startswith(text_cmds):
        out_lines.append(ln)
        continue
    
    seq += 1
    if seq not in VI:
        errors.append(f"Missing VI[{seq}]: {stripped[:80]}")
        out_lines.append(ln)
        continue
    
    vi_text = VI[seq]
    # Determine command type and field index
    if stripped.startswith('title,'):
        parts = ln.split(',', 2)  # title,JP_text\n or with ending
        # title is in JP in EN asset, so we replace the whole text after first comma
        # But we need to handle the ending properly
        cmd_part = 'title,'
        rest = ln[len(cmd_part):]
        # Find where the rest of the line starts - after title,
        # it's the text field, then possibly more
        out_lines.append(f"title,{vi_text}\n")
        continue
    elif stripped.startswith('messageTextCenter,'):
        # messageTextCenter,,<size=...>text</size>,,,on
        # parts: [cmd, empty, text, empty, empty, on]
        # split by max 6 to get all fields
        parts = ln.split(',', 5)
        # parts[2] is the text field
        parts[2] = vi_text
        out_lines.append(','.join(parts))
        continue
    elif stripped.startswith('message,'):
        # Need to carefully handle CRLF endings
        raw_ln = ln
        # Split by first 3 commas to get: message, speaker, text
        # But the text field may contain commas (fullwidth ， though)
        # Use maxsplit=3
        parts = ln.split(',', 3)
        # parts[0] = 'message', parts[1] = speaker name, parts[2] = text plus rest
        # Rebuild: parts=[message, speaker, vi_text<suffix>, ...]
        # The old text field may have trailing ,,vc_...,chara_X
        # We need to preserve everything after the text field
        # Split into: prefix (message,SPEAKER,), text, suffix (,,vc_...,chara_X\n)
        
        # Find the text field boundaries
        # Format: message,NAME,TEXT,,vc_...,chara_X\n
        # The TEXT field is after the 2nd comma, everything until we hit ",," (start of empty fields)
        # Better: use maxsplit to get parts after message,
        comma1 = ln.index(',')
        rest_after_cmd = ln[comma1+1:]
        comma2 = rest_after_cmd.index(',')
        speaker = rest_after_cmd[:comma2]
        text_and_rest = rest_after_cmd[comma2+1:]
        
        # Now check if the text field ends with <br> 
        # The pattern is: text<br> ,,vc_... or just text<br> ,,vc_
        # Find where the trailing ,, starts (the empty field separator)
        # text fields end with "<br> " as suffix
        
        # Let's find the text field boundary: it's from start of text_and_rest until the first ",,"
        # But the text may contain commas (fullwidth ones only)
        
        # Better: use the existing approach - find the 3rd comma's position
        # Actually, ln has format: message,SPEAKER,TEXT,,vc_...,chara_X
        # The TEXT is between 2nd and before ",," empty field marker
        # Let me use a simpler approach: find the first ",," after the text
        
        tf_start = len(f"message,{speaker},")
        rest = ln[tf_start:]
        
        # Find ",," which marks the start of the empty field+trailing metadata
        double_comma_pos = rest.find(',,')
        if double_comma_pos >= 0:
            old_text_field = rest[:double_comma_pos]
            after_text = rest[double_comma_pos:]  # ,,vc_...,chara_X\n
        else:
            # No double comma - the text might go to end
            old_text_field = rest.rstrip('\r\n')
            after_text = rest[len(old_text_field):]
        
        # Build new line
        new_line = f"message,{speaker},{vi_text}{after_text}"
        out_lines.append(new_line)
        continue
    else:
        errors.append(f"Unknown command at seq {seq}: {stripped[:60]}")
        out_lines.append(ln)

# --- Final checks ---
if errors:
    print("ERRORS found:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

# Verify record count
en_text_count = sum(1 for ln in lines if ln.strip().startswith(text_cmds))
vi_text_count = sum(1 for ln in out_lines if ln.strip().startswith(text_cmds))
assert en_text_count == vi_text_count == 86, f"Record count mismatch: EN={en_text_count}, VI={vi_text_count}"

# Verify line count
assert len(lines) == len(out_lines), f"Line count mismatch: {len(lines)} vs {len(out_lines)}"

# --- Verify <br> count per message field ---
br_errors = []
comma_errors = []
msg_seq = 0

for i, (en_ln, vi_ln) in enumerate(zip(lines, out_lines)):
    en_s = en_ln.strip()
    vi_s = vi_ln.strip()
    if not en_s.startswith(text_cmds):
        continue
    msg_seq += 1
    
    # Count <br> in the text field
    en_tf = ''
    vi_tf = ''
    
    if en_s.startswith('message,') or en_s.startswith('messageTextCenter,') or en_s.startswith('messageTextUnder,'):
        parts_en = en_s.split(',', 2)
        parts_vi = vi_s.split(',', 2)
        if len(parts_en) >= 3 and len(parts_vi) >= 3:
            en_tf = parts_en[2]
            vi_tf = parts_vi[2]
    elif en_s.startswith('title,'):
        en_tf = en_s[len('title,'):]
        vi_tf = vi_s[len('title,'):]
    
    if en_tf:
        en_br = en_tf.count('<br>')
        vi_br = vi_tf.count('<br>')
        if en_br != vi_br:
            br_errors.append(f"Seq {msg_seq}: EN<{en_br} VI<{vi_br}> EN={en_tf[:60]} VI={vi_tf[:60]}")
        
        # Check for ASCII comma in VI text field (inside text, not delimiter)
        # Isolate the actual translated text from trailing metadata
        # For message fields: text is everything before first ",,"
        # For messageTextCenter: text is between first ,, and last ,,
        vi_text_only = ''
        if vi_s.startswith('message,'):
            # Format: message,NAME,TEXT,,metadata
            # TEXT is between 2nd comma and first ",,"
            vi_text_only = vi_tf.split(',,')[0]
        elif vi_s.startswith('messageTextCenter,') or vi_s.startswith('messageTextUnder,'):
            # Format: messageTextCenter,,TEXT,,,on
            # TEXT is between 2nd comma and ",,,on"
            # vi_tf = parts[2] from split(',',5) which is TEXT,,,on
            # TEXT is everything before first ",,"
            vi_text_only = vi_tf.split(',,')[0]
        elif vi_s.startswith('title,'):
            vi_text_only = vi_tf
        
        if vi_text_only and ',' in vi_text_only:
            for ci, c in enumerate(vi_text_only):
                if c == ',':
                    comma_errors.append(f"Seq {msg_seq}: ASCII comma at pos {ci} in VI text: {vi_text_only[:80]}")

if br_errors:
    print(f"\nBR COUNT ERRORS ({len(br_errors)}):")
    for e in br_errors:
        print(f"  {e}")

if comma_errors:
    print(f"\nASCII COMMA ERRORS ({len(comma_errors)}):")
    for e in comma_errors:
        print(f"  {e}")

if br_errors or comma_errors:
    print("\nFIX ERRORS BEFORE WRITING!")
    sys.exit(1)

print(f"All checks passed. {msg_seq} text records verified.")
print(f"Lines: {len(lines)} EN → {len(out_lines)} VI")

# --- Write output ---
VI_FILE.parent.mkdir(parents=True, exist_ok=True)

# Preserve BOM
output = '\ufeff' + ''.join(out_lines)

# Normalize any CRLF issues - ensure consistent \r\n
# First ensure no \r\r\n
output = re.sub(r'\r+', '\r', output)

with open(VI_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(''.join(out_lines))

print(f"Written: {VI_FILE}")
print(f"Size: {VI_FILE.stat().st_size} bytes")

# --- Verify final output ---
with open(VI_FILE, 'r', encoding='utf-8-sig') as f:
    ver_lines = f.readlines()

# Count text records
vi_records = [l.strip() for l in ver_lines if l.strip().startswith(text_cmds)]
print(f"Final VI text records: {len(vi_records)}")

# Quick check for any remaining English
en_words = ['Commander', 'Abyss', 'Merem', 'prediction', 'divination']
found_en = []
for i, ln in enumerate(ver_lines, 1):
    if ln.strip().startswith(text_cmds):
        for w in en_words:
            if w in ln and 'Merem' in w:
                pass  # Proper names OK
            elif w in ln and w not in ['Merem']:
                # Check if it's in the text field specifically
                pass  # We'll check more carefully
                found_en.append((i, w, ln[:80]))

if found_en:
    print(f"\nPotential English leftovers ({len(found_en)}):")
    for ln_no, word, snippet in found_en:
        print(f"  L{ln_no} [{word}]: {snippet}")
else:
    print("No obvious English leftovers.")

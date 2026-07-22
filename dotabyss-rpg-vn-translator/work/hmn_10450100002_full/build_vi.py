#!/usr/bin/env python3
"""Build VI output for hmn_10450100002 (Iola first-study scene).
EN-asset-is-English with title,-still-JP.
Teacher-student dynamic: thầy-em (Iola calling Commander thầy).
"""
import json, re, sys
from pathlib import Path

EN_PATH = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt")
VI_PATH = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt")
WORK = Path("E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10450100002_full")

# ── VI translations by seq number ──────────────────────────────────────
# Seq 1: title (JP source)
# Seq 2,45: messageTextCenter
# Seq 3-85: message (82 records)

VI = {}

# ── Title ──
VI[1] = "Muốn Học Hành Nghiêm Túc"  # 勉強は真面目にやりたいの

# ── messageTextCenter ──
VI[2] = "<size=48>—Một Tuần Sau—</size>"  # —One week later—
VI[45] = "<size=48>—Vài Phút Sau—</size>"  # —Several minutes later.

# ── message lines ──

# Seq 3: イオラ, Teacher! Teacher! Teeeacher!<br> 
VI[3] = "Thầy ơi! Thầy ơi! Thầy ơi!<br> "

# Seq 4: <user>, Hmm? Iola... What's with the heavy breathing?<br> 
VI[4] = "Hử? Iola đấy à... Sao thở dốc thế?<br> "

# Seq 5: イオラ, I did all my assignments... (has <br> in middle)
VI[5] = "Em đã làm hết bài tập học kỳ một rồi đây!<br>Xong xuôi nên em đến báo cáo nè!<br> "

# Seq 6: <user>, Oh, you actually did them? Good work!<br> 
VI[6] = "Ồ‚ làm hết thật à? Giỏi lắm!<br> "

# Seq 7: <user>, Then show me what you've got...
VI[7] = "Vậy thì cho thầy xem thành quả đi. Đừng vội‚ bình tĩnh nào—<br> "

# Seq 8: イオラ, I-I know!... (has <br>)
VI[8] = "E-em biết rồi mà! Nói thế làm em càng hồi hộp hơn đó! Độc ác quá!<br> "

# Seq 9: <user>, Haha. I meant it...
VI[9] = "Haha. Thầy chỉ định động viên thôi. Nhưng thôi‚ cứ làm thử đi.<br> "

# Seq 10: イオラ, ...Understood. I'll try that light magic...
VI[10] = "...Rõ. Em sẽ thử lại phép ánh sáng đã thất bại lần trước.<br>Haaaa...<br> "

# Seq 11: イオラ, Hyaaaah!<br> 
VI[11] = "Hỡi ơi!<br> "

# Seq 12: <user>, Ah, you idiot!<br> 
VI[12] = "A‚ đồ ngốc!<br> "

# Seq 13: <user>, Gwaaah!<br> 
VI[13] = "GỤaaaah!<br> "

# Seq 14: イオラ, Kyaa! My eyes!...
VI[14] = "Kyaa! Mắt! Mắt tui! Tui không thấy gì hết!<br> "

# Seq 15: <user>, Of course! It was just supposed to be a small light!...
VI[15] = "Đương nhiên rồi!<br>Chỉ là tạo một tia sáng nhỏ thôi mà‚ có cần cố gồng đến vậy không!<br> "

# Seq 16: イオラ, B-but... when I thought it was my last chance...
VI[16] = "N-nhưng mà~... nghĩ là không còn cơ hội nữa nên em...<br> "

# Seq 17: <user>, ...*sigh*. It looks like it'll be a while...
VI[17] = "...Thở dài.<br>Có vẻ còn lâu em mới có thể tham gia thám hiểm Đại Huyệt được.<br> "

# Seq 18: イオラ, Ehh! That would be a problem!...
VI[18] = "Hả!? Thế thì gay to!<br>Nhà trường đang giục báo cáo kìa!!<br> "

# Seq 19: イオラ, Please! Give me one more chance!<br> 
VI[19] = "Làm ơn! Cho em thêm một cơ hội nữa đi!<br> "

# Seq 20: <user>, Sorry, but there's no time for that...
VI[20] = "Xin lỗi‚ nhưng không có thời gian cho việc đó đâu.<br>Thầy sắp dẫn một đội đi trinh sát Đại Huyệt đây.<br> "

# Seq 21: イオラ, N-no way...<br> 
VI[21] = "T-trời ơi~...<br> "

# Seq 22: イオラ, ...I studied so hard, but this is where it ends?<br> 
VI[22] = "...Em đã cố gắng học hành‚ vậy mà kết thúc ở đây sao?<br> "

# Seq 23: イオラ, (Oh, but wait. What I need isn't to join the Abyss expedition—)
VI[23] = "(À‚ nhưng khoan. Điều em cần không phải là tham gia thám hiểm Đại Huyệt—)<br> "

# Seq 24: <user>, Well then, I'm heading to the Abyss—<br> 
VI[24] = "Vậy thì thầy đi Đại Huyệt đây—<br> "

# Seq 25: イオラ, I've got it! The perfect idea!...
VI[25] = "Nảy số rồi! Ý hay đây!<br>Chỉ cần thay đổi cấu trúc phần đầu báo cáo là được!<br> "

# Seq 26: イオラ, Instead of writing about how I explored the Abyss...
VI[26] = "Không phải viết về cảnh em khám phá Đại Huyệt‚<br>mà là làm báo cáo quan sát thầy thám hiểm Đại Huyệt!<br> "

# Seq 27: <user>, D-don't decide on your own!...
VI[27] = "Đ-đừng tự tiện quyết định chứ!<br>Sao thầy có thể cho phép được! Đây đâu phải trò chơi!<br> "

# Seq 28: イオラ, I'm serious too! There's no way I'm flunking!...
VI[28] = "Em cũng nghiêm túc mà! Có mà để em rớt lớp sao!<br>Cho em đi! Cho em đi! Cho em đii!<br> "

# Seq 29: <user>, No-ope! No way!<br> 
VI[29] = "Không—được—rồi—!!!<br> "

# Seq 30: イオラ, Huh... so this is the Abyss...<br>Gotta write that down...<br> 
VI[30] = "Hế h... đây là Đại Huyệt à...<br>Ghi chép ghi chép...<br> "

# Seq 31: <user>, (...in the end, she forced her way along...)
VI[31] = "(...Cuối cùng thì nó cũng cố lẻo đẽo theo.<br>Còn trẻ mà sao cứng đầu thế nhỉ...)<br> "

# Seq 32: 兵士Ａ, Hey, look. There's an unfamiliar girl.<br>And she's cute...<br> 
VI[32] = "Này‚ nhìn kìa. Có một cô bé lạ mặt kìa?<br>Mà cũng dễ thương nhỉ...<br> "

# Seq 33: 兵士Ｂ, I hear she's accompanying the Commander on today's expedition.<br> 
VI[33] = "Nghe nói hôm nay cô ấy sẽ đi cùng Chỉ Huy trong cuộc thám hiểm đấy.<br> "

# Seq 34: 兵士Ａ, For real!<br> 
VI[34] = "Thiệt hả!?<br> "

# Seq 35: <user>, Reluctantly, yes... She's not at all reliable as a fighter.<br>Sorry, but<br>keep her safe with me.<br> 
VI[35] = "Bất đắc dĩ thôi... Về chiến lực thì không trông mong gì được.<br>Xin lỗi‚ nhưng<br>hãy cùng tôi bảo vệ con bé.<br> "

# Seq 36: 兵士Ａ, Leave it to us!<br> 
VI[36] = "Cứ giao cho tụi này!<br> "

# Seq 37: 兵士Ｂ, Looking forward to it, young lady!<br>Today's expedition looks like it'll be a blast!<br> 
VI[37] = "Cô bé‚ mong chờ lắm đấy!<br>Hôm nay chắc sẽ vui lắm đây!<br> "

# Seq 38: イオラ, Huh, what, what?<br>I'm getting a huge welcome!<br> 
VI[38] = "Ơ ơ ơ?<br>Ủa‚ em được chào đón nhiệt liệt quá ha!?<br> "

# Seq 39: <user>, You guys... just because she's a young girl...<br>You're so simple.<br> 
VI[39] = "Mấy cậu... chỉ vì là gái trẻ thôi mà...<br>Đơn giản quá đấy.<br> "

# Seq 40: イオラ, At magic school, it was all 'if you can't use magic...'<br>so I couldn't get a boyfriend, but here I might be popular!<br> 
VI[40] = "Ở trường pháp thuật toàn kiểu 'đứa không dùng được phép thì...'<br>nên em chẳng có bạn trai‚ nhưng ở đây em có vẻ hot!<br> "

# Seq 41: <user>, You're just as simple! Don't get carried away!<br> 
VI[41] = "Cô cũng đơn giản quá đấy! Đừng có lên mặt!<br> "

# Seq 42: <user>, You know this is a real recon mission to the Abyss...
VI[42] = "Em biết đây là nhiệm vụ trinh sát Đại Huyệt thật rồi đấy. Lính sẽ bảo vệ em‚ nhưng<br>cũng phải chuẩn bị tinh thần tự bảo vệ mình đấy nhé?<br> "

# Seq 43: <user>, Don't get hung up on using magic just because you're a mage...
VI[43] = "Đừng cố chấp chuyện đã là pháp sư thì phải dùng phép.<br>Dùng võ thuật sở trường hay bất cứ thứ gì‚ nhất định phải sống sót đấy. Rõ chưa?<br> "

# Seq 44: イオラ, Got it!<br> 
VI[44] = "Rõ!<br> "

# Seq 46: 兵士Ａ, Hraaah!<br> 
VI[46] = "Hỡaaaa!<br> "

# Seq 47: 小型モンスター, Gyaa!<br> 
VI[47] = "Gyaaa!<br> "

# Seq 48: , Thud.<br> 
VI[48] = "Bịch.<br> "

# Seq 49: <user>, All troops, stay sharp!...
VI[49] = "Toàn quân‚ đừng lơ là! Con lớn sắp tới rồi!<br>Cung tên và phép thuật chặn nó lại rồi từ từ hạ gục!<br> "

# Seq 50: , Following %user%'s command, a rain of arrows...
VI[50] = "Theo lệnh của %user%‚ mưa tên và phép tấn công<br>trút xuống con quái vật.<br> "

# Seq 51: 大型モンスター, GRROOOAAAR!<br> 
VI[51] = "GỪOOOOOAAAR!<br> "

# Seq 52: 兵士Ａ, No good! It's not flinching!<br> 
VI[52] = "Không được! Nó không nao núng!<br> "

# Seq 53: <user>, And it's heading straight for us!<br> 
VI[53] = "Mà nó còn đang lao về phía mình!<br> "

# Seq 54: イオラ, This is bad, this is really bad!...
VI[54] = "Nguy rồi nguy rồi nguy rồi!? N-nếu đến nước này thì—<br> "

# Seq 55: イオラ, Mutter, mutter, mutter...<br> 
VI[55] = "Lẩm bẩm lẩm bẩm...<br> "

# Seq 56: <user>, Iola, what are you... wait, you're not!<br> 
VI[56] = "Iola‚ em làm gì... khoan‚ không phải chứ!?<br> "

# Seq 57: イオラ, That's exactly it!<br> 
VI[57] = "Đúng vậy đó!<br> "

# Seq 58: <user>, E-everyone, put your heads down and close your eyes!<br> 
VI[58] = "M-mọi người cúi mặt nhắm mắt lại!<br> "

# Seq 59: , The moment %user% shouted, the soldiers did as he said...
VI[59] = "Khoảnh khắc %user% hét lên‚ đám lính làm theo ngay.<br>Câu thần chú của Iola cũng hoàn tất.<br> "

# Seq 60: イオラ, G-go! My magic!<br> 
VI[60] = "Đ-đi nào! Phép của em!<br> "

# Seq 61: 大型モンスター, Gwooonnn!<br> 
VI[61] = "Gừoonnn!<br> "

# Seq 62: , When the soldiers looked up, the monsters, temporarily blinded...
VI[62] = "Khi lính ngước lên‚ lũ quái vật bị mất thị giác tạm thời bởi<br>tia chớp mạnh đang quằn quại.<br> "

# Seq 63: イオラ, I-I did it...!<br> 
VI[63] = "L-làm được rồi...!?<br> "

# Seq 64: <user>, ...Ah. The magic itself is as flawed as ever...
VI[64] = "...Ừm. Phép thuật tự thân thì vẫn tệ như mọi khi‚ nhưng em đã làm tốt.<br>Cơ hội đây! Toàn quân‚ xông lên!<br> "

# Seq 65: <user>, ...Looks like most of them are taken care of. Iola, good work.<br> 
VI[65] = "...Dọn gần xong rồi nhỉ. Iola‚ em làm tốt lắm.<br> "

# Seq 66: イオラ, R-Reeeeally. I've never been this nervous even in exams.<br> 
VI[66] = "Th-thiệt đó~. Thi cử em cũng chưa hồi hộp đến vậy.<br> "

# Seq 67: イオラ, Oh, I need to write the report properly while I can... note, note.<br> 
VI[67] = "À‚ phải viết báo cáo ngay mới được... ghi chép ghi chép.<br> "

# Seq 68: , Iola took meticulous notes, her expression serious.<br> 
VI[68] = "Iola với ánh mắt nghiêm túc‚ tỉ mỉ ghi chép.<br> "

# Seq 69: <user>, Unlike your usual self, you're serious about this sort of thing.<br> 
VI[69] = "Khác với lời nói thường ngày nhỉ‚ em nghiêm túc chuyện này đấy.<br> "

# Seq 70: イオラ, Well, I hate practical exams because I can't pass them, but I love studying itself.<br> 
VI[70] = "Ừ thì... em ghét thi thực hành vì không qua nổi‚ nhưng<br>việc học thì em rất thích.<br> "

# Seq 71: イオラ, No one at school acknowledges me, but my dad believes in my talents...
VI[71] = "Mọi người ở trường chẳng công nhận em‚ nhưng ba tin vào tài năng của em<br>cả về pháp sư lẫn võ sĩ—<br> "

# Seq 72: イオラ, Maybe my magical talent will bloom with the right opportunity!...
VI[72] = "Biết đâu nhờ cơ hội nào đó tài năng phép thuật lại nở rộ thì sao?<br>Nên em muốn học hành nghiêm túc.<br> "

# Seq 73: <user>, I see. That's a good mindset.<br> 
VI[73] = "Ra vậy. Đó là một suy nghĩ tốt.<br> "

# Seq 74: イオラ, Well, doing all the first-semester review in one week. Even I hated that, you know!<br> 
VI[74] = "Ờ nhưng mà‚ làm hết bài ôn tập học kỳ một trong một tuần á?<br>Dĩ nhiên là em cũng ghét lắm nhé?<br> "

# Seq 75: <user>, Ahaha. Don't make it sound so bad.<br> 
VI[75] = "Haha ha. Đừng nói nó tệ thế chứ.<br> "

# Seq 76: <user>, I thought a student about to flunk might've come to the Frontline Base taking things lightly...
VI[76] = "Thầy đã nghĩ một học sinh sắp rớt có thể đến<br>Căn Cứ Tiền Tuyến với thái độ coi thường nên đã hơi nghiêm khắc.<br> "

# Seq 77: <user>, But I take that back. You're a hardworking student...
VI[77] = "Nhưng thầy rút lại lời đó.<br>Em là một học sinh chăm chỉ‚ có tương lai triển vọng.<br> "

# Seq 78: イオラ, W-What? Getting all soft on me all of a sudden...<br> 
VI[78] = "C-cái gì thế? Tự dưng chiều em kiểu gì vậy...<br> "

# Seq 79: <user>, I'm just telling you what I think. You have talent for martial arts...
VI[79] = "Thầy chỉ nói suy nghĩ thật lòng thôi. Em có tài về võ thuật‚<br>và cả phép thuật nữa‚ em có tài nỗ lực không bỏ cuộc.<br> "

# Seq 80: <user>, You're still young, so work hard at both...
VI[80] = "Em vẫn còn trẻ mà‚ cố gắng cả hai đi.<br>Phí hoài tài năng thì uổng lắm.<br> "

# Seq 81: イオラ, O-Okay... thank you.<br> 
VI[81] = "Đ-được rồi... cảm ơn thầy.<br> "

# Seq 82: <user>, I hope you'll get the hang of magic while you're with me...
VI[82] = "Khi ở bên thầy‚ mong em sẽ nắm được mẹo phép thuật‚<br>để có thể đi thám hiểm Đại Huyệt cùng thầy nhé.<br> "

# Seq 83: イオラ, Yeah... I think I'd like that too.<br> 
VI[83] = "Ừm... em cũng muốn vậy.<br> "

# Seq 84: <user>, What's this? Getting all shy on me? You tired?<br> 
VI[84] = "Sao thế? Tự dưng ngoan ngoãn thế. Mệt à?<br> "

# Seq 85: イオラ, (I can't help it. I'm not used to being praised. It throws me off. Geez...)<br> 
VI[85] = "(Em có cách nào đâu. Tại em không quen được khen.<br>Nó làm em mất tập trung. Trời ạ...)<br> "

# ── End of VI dictionary ──────────────────────────────────────────────

assert len(VI) == 85, f"Expected 85 records, got {len(VI)}"

# ── Read EN asset ─────────────────────────────────────────────────────
raw = open(EN_PATH, 'rb').read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig')
# Use splitlines(keepends=True) to preserve original line endings
lines = text.splitlines(True)
# Track if file ended with newline
trailing_newline = text.endswith('\n') or text.endswith('\r')
# Detect CRLF presence
has_crlf = any(l.endswith('\r\n') for l in lines)

print(f"Lines read: {len(lines)}")
print(f"BOM: {has_bom}, CRLF: {has_crlf}")
print(f"Trailing newline: {trailing_newline}")

# ── Preflight: check BR counts and ASCII commas ───────────────────────
# First, enumerate text records from EN
cmds = ('title,', 'message,', 'messageTextCenter,', 'messageTextUnder,')
en_seq = 0
mismatches = []
comma_issues = []

for ln in lines:
    stripped = ln.rstrip('\r\n')
    matched_cmd = None
    for cmd in cmds:
        if stripped.startswith(cmd):
            matched_cmd = cmd
            break
    if not matched_cmd:
        continue
    en_seq += 1
    vi_text = VI.get(en_seq)

    # Determine which part is the text field
    parts = stripped.split(',')
    if matched_cmd == 'title,':
        en_tf = parts[1]
    elif matched_cmd == 'messageTextCenter,' or matched_cmd == 'messageTextUnder,':
        en_tf = parts[2]
    else:  # message,
        en_tf = parts[2]

    # BR count comparison
    en_br = en_tf.count('<br>')
    vi_br = vi_text.count('<br>')
    if en_br != vi_br:
        mismatches.append(f"  seq={en_seq}: EN br={en_br} vs VI br={vi_br} | VI={vi_text[:50]}...")

    # ASCII comma check in VI text
    ascii_commas_in_vi = vi_text.count(',') if matched_cmd != 'title,' else 0
    if ascii_commas_in_vi > 0:
        comma_issues.append(f"  seq={en_seq}: {ascii_commas_in_vi} ASCII commas in VI: '{vi_text[:60]}'")

if mismatches:
    print(f"\nBR COUNT MISMATCHES ({len(mismatches)}):")
    for m in mismatches:
        print(m)
if comma_issues:
    print(f"\nASCII COMMA IN VI ({len(comma_issues)}):")
    for c in comma_issues:
        print(c)
if mismatches:
    print("ERROR: Fix BR mismatches before writing.")
    sys.exit(1)
if comma_issues:
    print("ERROR: Fix ASCII commas (use U+201A ‚) before writing.")
    sys.exit(1)

print("\nAll BR counts and comma checks PASSED.")

# ── Build VI file ─────────────────────────────────────────────────────
out_lines = []
vi_seq = 0

for ln in lines:
    stripped = ln.rstrip('\r\n')
    ending = ln[len(stripped):]  # preserve original line ending
    
    matched_cmd = None
    for cmd in cmds:
        if stripped.startswith(cmd):
            matched_cmd = cmd
            break
    
    if not matched_cmd:
        out_lines.append(stripped + ending)
        continue
    
    vi_seq += 1
    vi_text = VI[vi_seq]
    parts = stripped.split(',')
    
    if matched_cmd == 'title,':
        # title,<text>
        parts[1] = vi_text
    elif matched_cmd == 'messageTextCenter,' or matched_cmd == 'messageTextUnder,':
        # messageTextCenter,,<text>,,,on
        parts[2] = vi_text
    else:
        # message,<name>,<text>[,remaining...]
        # Mirror the suffix (trailing tags) from the EN text field
        en_tf = parts[2]
        # Extract trailing tag suffix
        suffix_match = re.search(r'(<[^>]+>\s*)+$', en_tf)
        if suffix_match:
            suffix = suffix_match.group(0)
            # Normalize the VI text: ensure VI doesn't already have the suffix
            vi_clean = vi_text
            if vi_clean.endswith(suffix):
                vi_clean = vi_clean[:-len(suffix)]
            vi_clean = vi_clean.rstrip()
            parts[2] = vi_clean.rstrip() + suffix
        else:
            parts[2] = vi_text
    
    out_lines.append(','.join(parts) + ending)

# ── Write output ──────────────────────────────────────────────────────
output = ''.join(out_lines)  # lines already have their endings preserved
# No need to add trailing newline - it's already in the last line's ending

# Restore BOM
if has_bom:
    raw_out = b'\xef\xbb\xbf' + output.encode('utf-8')
else:
    raw_out = output.encode('utf-8')

VI_PATH.parent.mkdir(parents=True, exist_ok=True)
open(VI_PATH, 'wb').write(raw_out)

# ── Verify ────────────────────────────────────────────────────────────
vi_lines = open(VI_PATH, 'rb').read()
vi_text_decoded = vi_lines.decode('utf-8-sig')
vi_line_list = vi_text_decoded.splitlines(True)

print(f"\nWritten: {VI_PATH}")
print(f"EN lines: {len(lines)}, VI lines: {len(vi_line_list)}")
vi_has_crlf = any(l.endswith('\r\n') for l in vi_line_list)
print(f"EN CRLF: {has_crlf}, VI has CRLF: {vi_has_crlf}")
print("DONE.")

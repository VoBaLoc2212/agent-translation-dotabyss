#!/usr/bin/env python3
"""
Build vi/hmn_10440100003.txt - Yachiyo & Dragon God scene

EN-asset-is-English with mixed JP-title/EN-message.
103 records: 1 title + 101 message + 1 messageTextCenter.
"""

import re, json
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN_PATH = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100003.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100003.txt"

# ── Read EN asset ──────────────────────────────────────────────
with open(EN_PATH, 'rb') as f:
    raw = f.read()
has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw
raw_text = raw.decode('utf-8-sig')
lines = raw_text.splitlines(True)

# ── Extract text records ───────────────────────────────────────
def extract_text_field(ln, cmd):
    """Extract text field and suffix from a command line.
    For message: content (without trailing <br> ) + suffix (includes <br> + tech fields)
    For title/center: content + suffix
    """
    cmd_len = len(cmd) + 1
    rest = ln[cmd_len:]
    
    if cmd == 'title':
        # title,<text>\r\n
        text_field = rest.rstrip('\r\n')
        suffix = rest[len(text_field):]
        return text_field, suffix
    
    # cmd,<speaker>,<text_field><suffix>
    name_comma = rest.find(',')
    if name_comma < 0:
        return rest.rstrip('\r\n'), ''
    
    text_part = rest[name_comma + 1:]
    
    if cmd == 'message':
        # The suffix is the trailing <br> + space + optional tech fields
        # Find: <br> \n  OR  <br> ,<tech_fields>\n
        # Try to locate the LAST <br> in the text
        br_idx = text_part.rfind('<br>')
        if br_idx >= 0:
            content = text_part[:br_idx]
            # suffix starts at <br>
            suffix = text_part[br_idx:]
            return content, suffix
        else:
            text_field = text_part.rstrip('\r\n')
            suffix = text_part[len(text_field):]
            return text_field, suffix
    
    # messageTextCenter or messageTextUnder
    tech_match = re.search(r',,,on[ \t]*\r?\n?', text_part)
    if tech_match:
        tech_start = tech_match.start()
        text_field = text_part[:tech_start]
        suffix = text_part[tech_start:]
    else:
        text_field = text_part.rstrip('\r\n')
        suffix = text_part[len(text_field):]
    
    return text_field, suffix

records = []
seq = 0
for ln in lines:
    s = ln.strip()
    if not s:
        continue
    if s.startswith('title,'):
        text_field, suffix = extract_text_field(ln, 'title')
        records.append((seq, 'title', text_field, suffix))
        seq += 1
    elif s.startswith('message,'):
        text_field, suffix = extract_text_field(ln, 'message')
        records.append((seq, 'message', text_field, suffix))
        seq += 1
    elif s.startswith('messageTextCenter,'):
        text_field, suffix = extract_text_field(ln, 'messageTextCenter')
        records.append((seq, 'messageTextCenter', text_field, suffix))
        seq += 1
    elif s.startswith('messageTextUnder,'):
        text_field, suffix = extract_text_field(ln, 'messageTextUnder')
        records.append((seq, 'messageTextUnder', text_field, suffix))
        seq += 1

print(f"Records: {len(records)}")

# ── VI Translations ────────────────────────────────────────────
VI = {}

VI[0] = "Đó Là Phước Lành Của Long Thần!"  # title

VI[1] = "――<user> và Yachiyo chạy hết mình qua những ngọn núi.<br>Nhưng tiếng gào thét của lũ quái vật phía sau chẳng hề nhỏ đi"
VI[2] = "*Há hác‚* *há hác...* *phù‚* *phù...*"
VI[3] = "Yachiyo‚ anh biết em vất vả rồi nhưng cố lên! Tin tưởng anh mà chạy tiếp"
VI[4] = "Vâng"
VI[5] = "Vừa động viên Yachiyo‚ <user> vừa liên tục<br>quan sát xung quanh"
VI[6] = "(Có thứ gì đó——thứ gì đó có thể xoay chuyển tình thế không!?<br>Phải tìm ra thứ gì đó trước khi Yachiyo kiệt sức và mất tinh thần——)"
VI[7] = "Tuy nhiên‚ trước khi kịp nghĩ ra cách lật ngược tình thế‚ hiểm cảnh đã ập đến.<br>Phía trước đã bị lũ quái vật chặn mất rồi"
VI[8] = "Gyahaha"
VI[9] = "Gyaaaa"
VI[10] = "...Chúng ta bị vây rồi"
VI[11] = "Dù có thoát khỏi vòng vây này‚ cũng chẳng còn sức để chạy trốn nữa.<br>Xin lỗi em‚ Yachiyo"
VI[12] = "Sao có thể... em mới là người——"
VI[13] = "(Em đã lôi Chỉ Huy vào chuyện này——đáng lẽ em mới là người có lỗi.<br>Người tốt bụng đã lo lắng chạy theo em lại gặp chuyện như thế này...)"
VI[14] = "Em buồn lắm... em xin lỗi"
VI[15] = "Yachiyo cúi mặt xuống‚ buông ra những lời ấy.<br>Ngay khoảnh khắc đó‚ trên đầu họ bắt đầu vang lên tiếng sấm ầm ầm"
VI[16] = "——Long Thần? Hả? Gì vậy"
VI[17] = "...? Có chuyện gì vậy? Nó đang bảo em điều gì à"
VI[18] = "Người bảo đừng hành động khinh suất"
VI[19] = "Grahhh"
VI[20] = "Trái ngược với hai người đang dừng lại‚ lũ quái vật bắt đầu tiến lên. Tên lính quèn được<br>tên đầu đàn sai khiến lao tới định vồ——khoảnh khắc ấy‚ một tia chớp lóe lên"
VI[21] = "*Rẹt*"
VI[22] = "Gyaaaa!?"
VI[23] = "Tia sét đánh chết một con quái vật. Yachiyo‚ <user>‚<br>và ngay cả lũ quái vật cũng đứng sững kinh ngạc"
VI[24] = "C-cái đó... chẳng lẽ là――?"
VI[25] = "Là phước lành của Long Thần! Người nói vẫn chưa xong đâu!<br>Người cũng bảo hãy giơ trượng lên chỉ vào kẻ cần tiêu diệt"
VI[26] = "*Rẹt*"
VI[27] = "Gyaaaa!?"
VI[28] = "Từ đó trở đi là một chiều. Sét đánh ập xuống từng đợt theo hướng Yachiyo giơ trượng.<br>Trước thảm họa thiên nhiên đầy uy lực‚ lũ quái vật không thể làm gì"
VI[29] = "Chẳng mấy chốc‚ lũ quái vật sợ hãi Yachiyo và tháo chạy"
VI[30] = "...Có vẻ như chúng ta đã thoát rồi"
VI[31] = "Tất cả là nhờ Long Thần——và cũng cảm ơn Chỉ Huy nữa"
VI[32] = "Không không‚ người được cứu là anh mới đúng"
VI[33] = "Đ-đó là nhờ Long Thần mà! Em chẳng làm gì cả...<br>lần đầu tiên em dùng sấm sét mà..."
VI[34] = "Nhân tiện‚ bây giờ em có dùng được không"
VI[35] = "...Em không biết nữa"
VI[36] = "Thử xem nào. Hòn đá kia có vẻ hợp đấy"
VI[37] = "...Dạ"
VI[38] = "Cô giơ trượng lên nhưng Long Thần chẳng đáp lại gì.<br>Giữa Yachiyo và <user> tràn ngập một bầu không khí kỳ lạ"
VI[39] = "C-có vẻ không được rồi. Quả nhiên Long Thần thất thường quá——"
VI[40] = "Để có được lòng tin của Long Thần thì chỉ có tu luyện mà thôi"
VI[41] = "Chia tay thì buồn lắm nhưng——em quyết định về quê nhà.<br>Chỉ Huy‚ xin hãy tha thứ cho em"
VI[42] = "Không được‚ ở lại bên cạnh anh. Đã chứng kiến sức mạnh tuyệt vời thế này‚<br>anh dễ dàng buông tay sao! Trong cuộc thám hiểm Đại Huyệt em nhất định sẽ là chiến lực lớn"
VI[43] = "Hơn nữa Yachiyo‚ em là một người con gái tốt. Dù không có sức mạnh của Long Thần‚<br>tất cả những ai biết rõ em đều công nhận em"
VI[44] = "Những bông hoa xinh đẹp như em càng nhiều càng tốt. Làm ơn‚ ở lại bên cạnh anh.<br>Để Căn Cứ Tiền Tuyến thêm vui tươi và rực rỡ‚ anh cần có em! Làm ơn"
VI[45] = "Ư.. th-thật gian quá mà Chỉ Huy~!?"
VI[46] = "Khi người nói thế này thì cứ như đang cua em vậy...<br>E-em‚ ngại quá đi..."
VI[47] = "(Thực ra anh cũng định cua em đấy chứ... nhưng rồi‚ một cú hích nữa thôi)"
VI[48] = "*Rẹt*"
VI[49] = "Á!?"
VI[50] = "Đột nhiên‚ một tia sét đánh xuống gần <user>"
VI[51] = "Đột nhiên em làm gì vậy Yachiyo"
VI[52] = "Không không không‚ không phải em! Không phải em đâu~!?"
VI[53] = "Hử? Thế Long Thần tự ý thả sét à"
VI[54] = "À thì‚ vâng——đại khái là thế——"
VI[55] = "(Hở...? Có gì đó lạ quá...?)"
VI[56] = "(Em cứ nghĩ dự báo thời tiết sai là do Long Thần thất thường<br>hoặc giận em lười tu luyện và đã bỏ rơi em... nhưng——)"
VI[57] = "(Nếu thế thì người đã chẳng cứu chúng ta khỏi lũ quái vật‚<br>phải không?)"
VI[58] = "(...Và sao lúc nãy lại đánh sét vào Chỉ Huy chứ)"
VI[59] = "——Khoảnh khắc ấy‚ Yachiyo có cảm giác như Long Thần đang ngự trong cơ thể mình<br>đã quay mặt đi một cách ngượng ngùng. Đồng thời‚ những cảnh trong quá khứ lướt qua tâm trí cô"
VI[60] = "Đừng ngại. Đó là sự thật mà.<br>...Ngẩng cao đầu ở lại Căn Cứ Tiền Tuyến. Anh – Chỉ Huy của em cho phép"
VI[61] = "Hễ gặp người con gái xinh đẹp dễ thương là anh lại thế đấy...<br>Yachiyo‚ cẩn thận đấy nhé"
VI[62] = "..."
VI[63] = "Yachiyo? Có chuyện gì vậy"
VI[64] = "À‚ ờm... chuyện Chỉ Huy được phụ nữ yêu thích ấy...<br>tự nhiên em hiểu ra hết rồi... phải làm sao đây... ♡"
VI[65] = "——Ầm ầm ầm"
VI[66] = "Hả? Sao tự nhiên có tiếng sấm...?"
VI[67] = "(Hồi đó cũng vậy‚ tự nhiên trời đổ mưa——)"
VI[68] = "Ra vậy. Hôm nay trời nắng cả ngày à. Biết được tin tốt rồi"
VI[69] = "Ừ. Sau khi xong việc anh có hẹn hò.<br>Nếu trời quang thì tính theo đường ra thảo nguyên ngắm sao... hề hề. Mong quá"
VI[70] = "(Hôm đó cũng vậy‚ tối đến mưa như trút nước...)"
VI[71] = "Thế‚ tối nay thế nào? Thực ra hôm nay anh cũng có hẹn——"
VI[72] = "...Ra rồi! Hôm nay nhất định là trời nắng!<br>Hãy cùng vui tươi lên nào~♪"
VI[73] = "(Hôm đó cũng thế...)"
VI[74] = "(L-Long Thần... chẳng lẽ người ghen với Chỉ Huy suốt thời gian qua!?<br>Vì em đã ngượng trước lời của Chỉ Huy!?)"
VI[75] = "Long Thần im lặng không nói gì.<br>Nhưng có cảm giác người đã hất mặt đi chỗ khác"
VI[76] = "(C-cái gì thế này——!?)"
VI[77] = "(Vì cái lý do đó!? Dự báo thời tiết cơ đấy!?<br>Em đã dự báo sai liên tục! Chỉ để làm phiền Chỉ Huy thôi ư!?)"
VI[78] = "Dù sao thì‚ làm ơn đấy Yachiyo! Đừng về Hourai nữa! Hãy ở lại bên cạnh anh"
VI[79] = "Dự báo có sai bao nhiêu lần cũng chẳng sao!<br>Nếu cùng đi chơi mà bị ướt thì lên giường sưởi ấm cho nhau là được"
VI[80] = "A-á...!?"
VI[81] = "Không được không được không được! Người nói thế thì em ngại lắm——"
VI[82] = "Hơn nữa‚ lại dự báo sai mất thôi~!!"
VI[83] = "<size=48>——Một Vài Ngày Sau</size>"  # messageTextCenter
VI[84] = "Yachiyo‚ hôm nay cũng như thường lệ nhé"
VI[85] = "Vâng!♪ Hôm nay là ngày giặt giũ lý tưởng đấy ạ~.<br>Cứ yên tâm phơi bên ngoài nhé"
VI[86] = "Ô-kê~. Có nhiều chuyện nhưng mừng là cháu đã quay lại.<br>Dù có lúc sai nhưng dù sao vẫn là chuẩn mà nhỉ♪"
VI[87] = "Hơn nữa‚ nhìn mặt cháu cười là lòng ta cũng quang đãng.<br>Cứ tiếp tục nhé‚ cô gái thời tiết"
VI[88] = "Vâng! Cảm ơn rất nhiều"
VI[89] = "(Tốt quá——em đã lấy can đảm để quay lại. Dự báo thời tiết cũng đúng hơn rồi‚<br>và mọi người đều chào đón em——)"
VI[90] = "(Cũng nhờ Chỉ Huy cả——<br>được kéo về thật tốt quá~. Hê hê hê♪)"
VI[91] = "(À‚ không được! Không được nghĩ về người ấy!<br>Bình tĩnh... bình tĩnh nào Yachiyo)"
VI[92] = "Ồ‚ Yachiyo. Em ở đây à"
VI[93] = "A!? Ch-Chỉ Huy..."
VI[94] = "(...Ực‚ không được. Gặp là em lại ngại...)"
VI[95] = "Anh đang tìm em đây. Sắp phải đi công tác xa nên<br>muốn em dự báo thời tiết. Được không"
VI[96] = "V-vâng. Dự báo chỗ xa thì không sao ạ...<br>Không ảnh hưởng đến mọi người ở Căn Cứ Tiền Tuyến mà"
VI[97] = "Ừ. Thế nhé‚ nhờ em đấy"
VI[98] = "Long Thần ơi Long Thần——xin hãy đáp lời"
VI[99] = "...Ra rồi! Trời nắng——"
VI[100] = "——Người bảo thế nên chắc là mưa đấy ạ"
VI[101] = "À‚ nhưng lần trước em đã lật ngược và trời lại nắng như dự báo nên——<br>lại lật ngược tiếp thì... hmm...?"
VI[102] = "...Thôi nào. Quả nhiên thời tiết vẫn thất thường như mọi khi"

assert len(VI) == len(records), f"Expected {len(records)} translations, got {len(VI)}"

# ── Preflight: check BR counts and ASCII commas ────────────────
print("\n── Preflight checks ──")
issues = []
for seq_num, cmd, en_content, suffix in records:
    vi = VI[seq_num]
    
    # Check ASCII comma in VI text
    if ',' in vi:
        issues.append(f"seq {seq_num}: ASCII comma in VI: [{vi[:60]}]")
    
    if cmd == 'message':
        # Compare BR count in content only (suffix BR is appended automatically)
        en_br_internal = en_content.count('<br>')
        vi_br_internal = vi.count('<br>')
        if en_br_internal != vi_br_internal:
            issues.append(f"seq {seq_num}: internal BR mismatch EN({en_br_internal}) vs VI({vi_br_internal}): [{vi[:80]}]")
    elif cmd == 'messageTextCenter':
        en_br = en_content.count('<br>')
        vi_br = vi.count('<br>')
        if en_br != vi_br:
            issues.append(f"seq {seq_num} (center): BR mismatch EN({en_br}) vs VI({vi_br})")

if issues:
    print(f"\n\u274c {len(issues)} preflight issues:")
    for iss in issues:
        print(f"  {iss}")
else:
    print("\u2705 All BR counts match!")
    print("\u2705 No ASCII commas in VI!")

# ── Build output lines ──────────────────────────────────────────
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
out_lines = []
record_idx = 0

for ln in lines:
    s = ln.strip()
    if not s:
        out_lines.append(ln)
        continue
    
    is_text_cmd = False
    for cmd_check in ['title', 'message', 'messageTextCenter', 'messageTextUnder']:
        if s.startswith(cmd_check + ','):
            is_text_cmd = True
            break
    
    if not is_text_cmd:
        out_lines.append(ln)
        continue
    
    seq_num, cmd, en_content, suffix = records[record_idx]
    vi = VI[seq_num]
    
    if cmd == 'title':
        # title,<text>\r\n
        cmd_prefix = 'title,'
        new_line = cmd_prefix + vi + suffix
    elif cmd == 'message':
        # message,<speaker>,<content><br> <tech_fields>\n
        cmd_prefix = ln[:len('message,')]
        rest = ln[len('message,'):]
        name_comma = rest.find(',')
        speaker = rest[:name_comma]
        new_line = cmd_prefix + speaker + ',' + vi + suffix
    elif cmd == 'messageTextCenter':
        cmd_prefix = ln[:len('messageTextCenter,')]
        rest = ln[len('messageTextCenter,'):]
        name_comma = rest.find(',')
        speaker = rest[:name_comma]
        new_line = cmd_prefix + speaker + ',' + vi + suffix
    elif cmd == 'messageTextUnder':
        cmd_prefix = ln[:len('messageTextUnder,')]
        rest = ln[len('messageTextUnder,'):]
        name_comma = rest.find(',')
        speaker = rest[:name_comma]
        new_line = cmd_prefix + speaker + ',' + vi + suffix
    
    out_lines.append(new_line)
    record_idx += 1

assert record_idx == len(records), f"Consumed {record_idx} records, expected {len(records)}"

# ── Write output ────────────────────────────────────────────────
output = ''.join(out_lines)
if has_crlf:
    output = output.replace('\r\n', '\n').replace('\n', '\r\n')
else:
    output = output.replace('\r\n', '\n')

output_bytes = output.encode('utf-8')
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_bytes

VI_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(VI_PATH, 'wb') as f:
    f.write(output_bytes)

print(f"\n\u2705 Written to {VI_PATH}")
print(f"  Input lines: {len(lines)}")
print(f"  Output lines: {len(out_lines)}")
print(f"  Records processed: {record_idx}")

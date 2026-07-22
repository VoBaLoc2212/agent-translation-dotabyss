#!/usr/bin/env python3
"""
Build VI output for hmn_10490100001 (Chloe/Sophia fan-service scene)
EN-asset-is-English case (title still JP). 88 records: 1 title + 86 message + 1 messageTextCenter.

Fixed: uses splitlines(True) for proper CRLF preservation.
"""

import json
import re
import sys
from pathlib import Path

WORK = Path(__file__).parent
ROOT = Path("E:/AgentTranslation")
EN_PATH = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100001.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100001.txt"
JA_PATH = ROOT / "dotabyss-translation-main/translations/novels/hmn_10490100001/ja.json"
EN_JSON_PATH = ROOT / "dotabyss-translation-main/translations/novels/hmn_10490100001/en.json"

# ── VI translations keyed by file-order sequential text-record index ──────────
# seq 0..87 matches the text-command lines in file order
# VI text uses fullwidth ，(U+FF0C) to avoid delimiter conflict with ASCII ,

VI = {
    0: "Fan Service Quá Hào Phóng……！",

    1: "Một đội kỵ sĩ phụ trách phòng vệ thị trấn đã chiến đấu để<br>đẩy lùi lũ quái vật đang tiến đến Thị Trấn Căn Cứ Tiền Tuyến từ Đại Huyệt.<br> ",

    2: "*thở dốc*!<br> ",

    3: "Chiến đấu đang thuận lợi đấy.<br>Quả nhiên kỵ sĩ rất đáng tin cậy trong trận phòng thủ.<br> ",

    4: "Phía trước là nơi dân lành sinh sống! Tôi tuyệt đối không để các người qua đây!<br> ",

    5: "Đặc biệt là Sophia——hôm nay cô ấy cũng làm tốt lắm——<br> ",

    6: "Kyaa! Chị Sophia! Chị Sophia! Chào，chào，chào，chào!<br> ",

    7: "Hả? Có chuyện gì với cái cô gái hành động kỳ lạ này vậy?<br> ",

    8: "Ưm... với một đòn này，tôi sẽ kết liễu số phận của con quái vật độc ác! *thở dốc*!<br> ",

    9: "Sẵn sàng，nào! Lửa! Sấm! Kaiser! Barrier! Raider! Laser! Charger!<br> ",

    10: "Ưm，tôi không dùng ma thuật lửa hay sấm sét，càng không phải Kaiser...<br> ",

    11: "Á! Cô ấy nhìn về phía này! Cảm ơn rất nhiều! Aaa，Kỵ Sĩ Sét Trắng<br>thật cao quý... Tôi mê cô ấy mất!<br> ",

    12: "Cái quái gì thế? Nó đang cổ vũ cho Sophia à? Sẽ gây cản trở<br>chiến đấu mất，phải ngăn nó lại——<br> ",

    13: "Fave của tôi đang sống ở đây，đang chiến đấu!<br>Lòng biết ơn dành cho fave tràn ra mất rồi!<br> ",

    14: "Pháp sư vẫy cây đũa phát sáng，và một luồng ánh sáng lấp lánh bao trùm<br>lấy Sophia.<br> ",

    15: "Ma Thuật Hỗ Trợ? ...Cảm ơn! Tôi rất biết ơn.<br> ",

    16: "Khoan đã，nhiều quá rồi đấy! Chắc chắn cô ấy vừa nói với tôi đúng không? Fan<br>service như thế này... Tôi đến Căn Cứ Tiền Tuyến thật tốt quá!<br> ",

    17: "Cô ấy là người dùng Ma Thuật Hỗ Trợ à...? Ờm，vậy cũng ổn nhỉ...<br> ",

    18: "Tôi có ma thuật có thể dùng cho fave của tôi...! Chỉ vậy thôi cũng cho cuộc đời tôi<br>ý nghĩa rồi!<br> ",

    19: "Có thực sự ổn không vậy...?<br> ",

    20: "*phù*... trận chiến kết thúc rồi，nhưng hãy cảnh giác. Sự lơ là của chúng ta<br>có thể khiến người dân gặp nguy hiểm.<br> ",

    21: "Ưm... C-Chị Sophia! Chị làm tốt lắm ạ!<br> ",

    22: "Em là người đã dùng Ma Thuật Hỗ Trợ lúc nãy phải không? Tôi cảm kích sự giúp đỡ<br>của em; cho tôi hỏi tên em được không?<br> ",

    23: "C-Cháu là Chloe ạ! Chị không cần phải nhớ cháu đâu，thực sự đấy ạ!<br> ",

    24: "Không đâu，tôi sẽ không quên đâu. Em cũng là đồng đội ở căn cứ này mà.<br> ",

    25: "Chị ấy đã nói chuyện trực tiếp với mình và còn gọi tên mình nữa...! Fan service<br>thế này quá hào phóng...!<br> ",

    26: "Chị Sophia! Cái này là quà cho chị ạ! Nếu không phiền chị!<br> ",

    27: "Ồ，một cái khăn và... ôi trời，một lá thư ư? Cái này cũng cho tôi sao...?<br> ",

    28: "Cháu biết có thể hơi thất lễ，nhưng cháu nhất định phải bày tỏ lòng biết ơn<br>với chị...!<br> ",

    29: "Thật dễ thương quá... Tôi sẽ xem sau nhé. Cái khăn cũng rất<br>hữu ích... *phù*.<br> ",

    30: "Chị Sophia lau mồ hôi sau trận chiến...! Mình thực sự được xem cảnh này miễn phí<br>sao!<br> ",

    31: "Em nói gì vậy? Em cũng đã chiến đấu cùng chúng tôi mà.<br> ",

    32: "Không không không! Ma thuật dùng cho fave——nếu gì thì cháu mới là người<br>phải trả tiền cho vinh dự này!<br> ",

    33: "Em giúp đỡ đồng đội một cách vô tư. Thái độ đó thật tuyệt vời.<br>Hãy tiếp tục chiến đấu cùng nhau nhé!<br> ",

    34: "V-vâng ạ! Cháu sẽ luôn là fan của chị，chị Sophia!<br> ",

    35: "Aa，ngay cả bóng lưng chị ấy khi đi cũng đẹp...!<br>Thật tốt vì mình đã chọn Sophia làm fave!<br> ",

    36: "Mong là quà không làm phiền chị ấy... Mình nghĩ đồ uống hay đồ ăn sẽ khó xử，<br>nên mình chọn khăn mới và thư hâm mộ...<br> ",

    37: "A，pháp sư ở đằng kia... Chloe，phải không? Cô đã nói đủ thứ chuyện kỳ lạ，<br>nhưng cô thích Sophia à?<br> ",

    38: "Á! Đó chắc chắn là Công Chúa Kỵ Sĩ nhỏ đã xuất trận lần đầu<br>hôm nay!<br> ",

    39: "Biểu cảm đó——vừa là sự nhẹ nhõm khi hoàn thành nhiệm vụ đầu tiên<br>vừa là sự bực bội vì không làm hoàn hảo——tôi có thể cổ vũ hết mình cho điều đó!<br> ",

    40: "Khoan，vậy không nhất thiết phải là Sophia sao?! Này! Chloe，nghe tôi nói này!<br> ",

    41: "Ối! Có phải ngài là người từ Căn Cứ Tiền Tuyến không ạ?<br> ",

    42: "Ừ，tôi là Chỉ Huy đây. Trước hết，để tôi hỏi cô một chuyện.<br> ",

    43: "Theo những gì tôi thấy，cô đang cổ vũ Sophia và những người khác. Vậy，<br>Chloe này... cô thích con gái à?<br> ",

    44: "Không，không ạ! Cháu chỉ đang ủng hộ các Công Chúa Kỵ Sĩ yêu thích của mình thôi!<br> ",

    45: "'Ủng hộ'...?<br> ",

    46: "Vâng ạ! Cháu chỉ là một pháp sư bình thường，giản dị thích ngắm nhìn<br>các nữ kỵ sĩ xinh đẹp! Đó là cháu，Chloe!<br> ",

    47: "Vậy 'Công Chúa Kỵ Sĩ' là các nữ kỵ sĩ xinh đẹp à. Ừm，tôi có thể hiểu tại sao<br>họ thu hút ánh nhìn của cô...<br> ",

    48: "Ngài cũng để ý đến Công Chúa Kỵ Sĩ sao? Ngài có khiếu thẩm mỹ đấy!<br>Mong được hợp tác nhé，Chỉ Huy!<br> ",

    49: "Ừ，được thôi，nhưng... Tôi nghĩ cô không hề bình thường đâu，Chloe ạ.<br> ",

    50: "<size=48>——Vài Ngày Sau——</size>",

    51: "Xin lỗi ạ，cháu nghe nói ngài muốn gặp cháu...?<br> ",

    52: "Ừ，Chloe. Cảm ơn đã đến.<br> ",

    53: "Chloe，chúng tôi nói chuyện một chút được không?<br> ",

    54: "Hả? Cả hai người cùng lúc? Có chuyện gì thế ạ?<br> ",

    55: "Hừm，không có tự giác sao.<br> ",

    56: "T-tự giác! Cháu chẳng làm gì cả mà!<br> ",

    57: "...Hừm. Vậy để tôi xác nhận nhé. Đây là báo cáo từ đội<br>thám hiểm.<br> ",

    58: "'Tôi có thể cảm nhận Chloe đang nhìn chằm chằm khi tôi ở trong doanh trại. Bất cứ khi nào<br>tôi để ý，cô ấy đang quan sát từ xa.'<br> ",

    59: "C-cái gì?! Ờ-ờm，cái đó là...<br> ",

    60: "'Khi tôi gọi hỏi xem cô ấy cần gì hay cố gắng đến gần，<br>cô ấy biến mất. Tôi muốn biết tại sao.'——Đó là nội dung báo cáo.<br> ",

    61: "Ố-Ối!? Ưm，cụ thể là ai đã nói vậy ạ?<br> ",

    62: "Một số người. Cô Rosa，cô Sophia，cô Eliza... Tất cả đều là<br>nữ kỵ sĩ.<br> ",

    63: "Vậy，Chloe，cô có nhớ gì không? Những báo cáo về việc cô nhìn chằm chằm<br>các nữ kỵ sĩ từ xa ấy.<br> ",

    64: "Cháu không thể nói là không nhớ，nhưng... Không phải cháu có ý xấu gì đâu ạ，<br>ngài biết đấy...<br> ",

    65: "Vậy là cô đã làm đúng như báo cáo nói?<br> ",

    66: "Nhưng ở Milesgard，cháu không gần các fave của mình thế này... Nên dĩ nhiên cháu<br>nhìn chằm chằm! Cháu không thể không nhìn!<br> ",

    67: "Nhưng，nhưng，cháu biết không nên làm phiền，nên cháu đã giữ khoảng cách.<br>Chạm vào fave là tuyệt đối cấm kỵ，nên cháu đã fangirl có chừng mực!<br> ",

    68: "Đó chính xác là điều đáng ngờ! Họ là đồng đội của cô，nên nếu cô<br>cần gì thì cứ nói chuyện bình thường đi!<br> ",

    69: "Nhìn fave không phải là việc vặt——nó như việc thở vậy，<br>nó cần thiết cho sự sống còn của cháu!<br> ",

    70: "Vậy là cô chỉ nhìn chằm chằm họ để giải trí dù chẳng có<br>lý do thực sự nào?<br> ",

    71: "Đúúng vậy ạ，cháu thành thật xin lỗiiii!<br> ",

    72: "Hu hu... làm fave của mình khó chịu là không thể tha thứ với một fan... Và<br>bây giờ mọi người đều nghĩ cháu là kẻ kỳ quặc...<br> ",

    73: "Ưm... vậy cháu sẽ bị cấm đến đây sao...? Cũng đương nhiên thôi vì<br>cháu đã làm phiền fave của mình，đúng không ạ?<br> ",

    74: "Hừm，cũng không phải họ phàn nàn rằng cô làm họ khó chịu<br>hay gì.<br> ",

    75: "Vâng，báo cáo thiên về việc họ lo lắng cho cô Chloe，<br>hoặc rằng họ vô tình gây rắc rối cho cô.<br> ",

    76: "Aaaa，tinh thần cao quý của các Công Chúa Kỵ Sĩ thật là<br>cao quý——cháu không thể hết cảm thấy tội lỗi được!<br> ",

    77: "Tôi có thể nói với họ rằng cô chỉ xem với tư cách fan và không có gì cả，<br>nhưng mấy nữ kỵ sĩ ở đây không thể ngừng lo lắng.<br> ",

    78: "Giờ，xử lý chuyện này thế nào đây...<br> ",

    79: "Hức... cháu chỉ muốn ủng hộ họ với tư cách fan thôi，mà lại thành<br>ra thế này...<br> ",

    80: "Chúng ta cần giải quyết mối lo của các nữ kỵ sĩ，nhưng việc em không<br>nghe mệnh lệnh của Chỉ Huy trong trận trước cũng là vấn đề lớn!<br> ",

    81: "Nếu em bị phân tâm bởi các nữ kỵ sĩ đến nỗi không thể làm theo<br>mệnh lệnh，một ngày nào đó em sẽ phạm sai lầm nghiêm trọng đấy.<br> ",

    82: "Ờ-ờm，đúng là khi fave ở ngay trước mặt cháu，cháu không thể<br>nghĩ về bất cứ điều gì khác...<br> ",

    83: "——Vậy nên! Tôi đề xuất một giải pháp triệt để!<br> ",

    84: "Ý chị là sao ạ...?<br> ",

    85: "Chloe này，chị muốn em hẹn hò với Chỉ Huy!<br> ",

    86: "...Hả? Tôi với Chloe ư!?<br> ",

    87: "Hẹn hò...? H-hẹn hò ạ!?<br> ",
}

assert len(VI) == 88, f"Expected 88 VI records, got {len(VI)}"

# ── Load sources ────────────────────────────────────────────────────────────
with open(JA_PATH, 'r', encoding='utf-8') as f:
    ja_map = json.load(f)

with open(EN_JSON_PATH, 'r', encoding='utf-8') as f:
    en_map = json.load(f)

# Build EN→JP reverse map for content-matching
def norm_en(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('，', ',').replace('\u3000', ' ')
    return s.strip()

en_to_jp = {}
for jp, en in en_map.items():
    if en:
        key = norm_en(en)
        en_to_jp[key] = jp

# ── Read EN asset ──────────────────────────────────────────────────────────
with open(EN_PATH, 'rb') as f:
    raw = f.read()

has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw

text = raw.decode('utf-8-sig')
lines = text.splitlines(True)  # Keep original line endings

TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

# ── Build output lines, replacing text fields with VI ──────────────────────
out_lines = []
seq = 0

for raw_line in lines:
    # Extract original ending
    ending = ''
    for ch in ('\r\n', '\r', '\n'):
        if raw_line.endswith(ch):
            ending = ch
            break
    ln = raw_line.rstrip('\r\n')

    cmd = None
    for tc in TEXT_CMDS:
        if ln.startswith(tc):
            cmd = tc.rstrip(',')
            break

    if cmd is None or seq >= len(VI):
        out_lines.append(raw_line)
        continue

    vi_text = VI[seq]

    if cmd == 'title':
        new_line = f"title,{vi_text}"
        out_lines.append(new_line + ending)
        seq += 1
        continue

    if cmd == 'messageTextCenter':
        parts = ln.split(',', 5)
        parts[2] = vi_text
        new_line = ','.join(parts)
        out_lines.append(new_line + ending)
        seq += 1
        continue

    # cmd == 'message':
    parts_all = ln.split(',')
    if len(parts_all) > 2:
        parts_all[2] = vi_text
        new_line = ','.join(parts_all)
        out_lines.append(new_line + ending)
    else:
        out_lines.append(raw_line)

    seq += 1

assert seq == 88, f"Processed {seq} records, expected 88"

# ── Write VI output ────────────────────────────────────────────────────────
out_text = ''.join(out_lines)
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(VI_PATH, 'wb') as f:
    if has_bom:
        f.write(b'\xef\xbb\xbf')
    f.write(out_text.encode('utf-8'))

print(f"✅ Written: {VI_PATH}")
print(f"   Records: {seq}")
print(f"   BOM: {has_bom}, CRLF: {has_crlf}")
print(f"   Total lines: {len(out_lines)}")

# ── Preflight: count <br> per text field vs EN ──────────────────────────────
print("\n── Preflight BR check ──")
br_errors = []
seq2 = 0
for raw_line in lines:
    ln = raw_line.rstrip('\r\n')
    cmd = None
    for tc in TEXT_CMDS:
        if ln.startswith(tc):
            cmd = tc.rstrip(',')
            break
    if cmd is None or seq2 >= len(VI):
        continue

    vi_text = VI[seq2]

    # Get EN text field for BR count
    if cmd == 'title':
        parts = ln.split(',', 1)
        en_text = parts[1] if len(parts) > 1 else ''
    elif cmd == 'messageTextCenter':
        parts = ln.split(',', 5)
        en_text = parts[2] if len(parts) > 2 else ''
    else:
        parts = ln.split(',')
        en_text = parts[2] if len(parts) > 2 else ''

    en_br = en_text.count('<br>')
    vi_br = vi_text.count('<br>')
    if en_br != vi_br:
        br_errors.append(f"  seq{seq2} ({cmd}): EN has {en_br} <br>, VI has {vi_br} | EN: {en_text[:50]} | VI: {vi_text[:50]}")

    seq2 += 1

if br_errors:
    print(f"❌ {len(br_errors)} BR mismatch(es):")
    for e in br_errors:
        print(e)
    sys.exit(1)
else:
    print("✅ All <br> counts match EN asset")

# ── Preflight: ASCII comma check ────────────────────────────────────────────
print("\n── Preflight ASCII comma check ──")
comma_errors = []
for seq_id, vi in VI.items():
    if ',' in vi:
        comma_errors.append(f"  seq{seq_id}: ASCII comma found: {vi[:60]}")
if comma_errors:
    print(f"❌ {len(comma_errors)} ASCII comma(s) in VI:")
    for e in comma_errors:
        print(e)
    sys.exit(1)
else:
    print("✅ No ASCII commas in VI text (using fullwidth ，)")

# ── Verify VI file is readable and has correct line count ────────────────────
print("\n── VI file verification ──")
vi_line_count = len(out_lines)
en_line_count = len(lines)
print(f"   EN lines: {en_line_count}")
print(f"   VI lines: {vi_line_count}")
if en_line_count == vi_line_count:
    print("✅ Line count matches EN")
else:
    print(f"⚠️  Line count mismatch: EN={en_line_count} VI={vi_line_count}")

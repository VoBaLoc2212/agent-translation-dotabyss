#!/usr/bin/env python3
"""
Build hmn_10480100001 VI output from EN asset (EN-asset-is-English with JP title).
Properly handles the trailing <br>  suffix on message lines.
EN asset <br> count is authoritative.
"""
import sys
from pathlib import Path

EN_ASSET = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt")
VI_PATH  = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt")

VI = {}

VI[0]  = "Chính Mày Là Kẻ Gây Ra Vụ Cướp"
VI[1]  = "Nào nào，hôm nay có cả đống hàng tốt đây！<br>Khách ơi，nhất định hãy ghé xem nhá！"
VI[2]  = "……Ừm。Chợ hôm nay cũng đông vui nhỉ。<br>Nếu sau việc này không có gì thì cũng muốn thong thả xem rồi về……"
VI[3]  = "Gyaa！？"
VI[4]  = "Hử……？"
VI[5]  = "Này！ Đưa tiền đây！"
VI[6]  = "Hiii，dừng lại！ Tôi đưa đây，đừng đá tôi……"
VI[7]  = "Gi，giữa ban ngày ban mặt mà đi cướp à！？"
VI[8]  = "Hê hê，chào tạm biệt！"
VI[9]  = "Khắc，đứng lại！"
VI[10] = "<size=48>Nàyyyyy！</size>"
VI[11] = "Guwaa！？"
VI[12] = "Chỉ Huy bất ngờ bị một cô gái lạ mặt lao vào đỡ。<br>Cứ thế bị khóa tay lại。"
VI[13] = "Chính mày là kẻ trắng trợn gây ra vụ cướp giữa ban ngày ban mặt hả？<br>Dám ra tay trước mặt Celeste đây à，gan nhỉ！"
VI[14] = "……Mày là cảnh vệ hả？ Đúng lúc quá！<br>Thằng cướp vừa chạy về hướng kia——"
VI[15] = "Tưởng không bị bắt sao，đồ ngốc này。<br>Hừ，nhờ mày mà chị đây kiếm được công lao đây！"
VI[16] = "Ngon lành quá……Chắc được thưởng luôn quá？ Hí hí hí。"
VI[17] = "Này，nghe tôi nói！"
VI[18] = "À ừ ừ hiểu rồi hiểu rồi。Đến mức giữa ban ngày cũng đi cướp，<br>chắc đói bụng lắm hả？ Vô đồn rồi khai đi，ngoan ngoãn nào。"
VI[19] = "Không phải！"
VI[20] = "Im đi nào thằng cướp à không，cục tiền thưởng。<br>Để xem，1-4-0-0，bắt giữ，chốt……"
VI[21] = "Th，thôi mà nghe tôi nói đã——！！！"
VI[22] = "（Cuối cùng cũng bị lôi vô đồn cảnh vệ mất rồi……）"
VI[23] = "Nào，lấy lời khai nhé。<br>Tên và ngày sinh，viết vô đây。"
VI[24] = "Nghe cho rõ đây，tôi không phải kẻ cướp。<br>Thủ phạm là người khác. Tôi thấy hắn chạy trốn。"
VI[25] = "Lại bào chữa nhàm chán nữa rồi……chịu thua đi mà？"
VI[26] = "Vì đó là sự thật nên biết sao được。<br>Cấp trên của cô đâu？"
VI[27] = "Bảo có việc nên đi ra ngoài rồi。"
VI[28] = "Mà này，gì đây？ Nhìn chị là con gái nên coi thường hả？<br>Đồ cướp mà lại bảo đàn bà không đáng nói chuyện chắc？"
VI[29] = "Không phải vậy。Tôi chỉ muốn cô gọi ai đó biết tôi thôi。<br>Ở đây ngoài cô ra không còn ai à？"
VI[30] = "Tiếc nhỉ。Tất cả đều đi hết rồi。"
VI[31] = "……Vậy thì đành nhờ cô vậy。Gọi chủ tiệm bị hại đến đi。<br>Họ sẽ chứng minh tôi vô tội。"
VI[32] = "Đã bảo rồi，bây giờ chỉ có mình chị nên không được。<br>Không thể để mày một mình được。"
VI[33] = "Cứ trói tôi vô ghế cũng được，đi đi。<br>Còn hơn ngồi đây tra hỏi mãi，tiến triển nhanh hơn nhiều đấy？"
VI[34] = "Nói thế chứ，chị đi là mày định trốn đúng không？<br>Trốn dây trói các kiểu đấy chứ gì。"
VI[35] = "Nếu lo thì nhốt tôi vô xà lim đi！<br>Nãy giờ chẳng tiến triển gì cả！？"
VI[36] = "Đương nhiên rồi！ Chị đây không có thời gian hầu trò hề của mày đâu！<br>Cũng không định để mày chạy thoát đâu！"
VI[37] = "Vì mày là cục tiền thưởng đem tiền đến cho chị mà。<br>Nên ngoan ngoãn nhận tội đi，trước khi công lao được xác nhận thì đừng hòng thoát。"
VI[38] = "Chị rất thích tiền。Nhưng ghét phiền phức và công việc。"
VI[39] = "Còn mày là cơ hội ngàn năm có một rơi xuống chỗ chị đây……！<br>Hí hí hí hí ♪"
VI[40] = "Mau nhận tội đi。Có hận thì，<br>hận cái sự ngu ngốc của mày để bị bắt bởi một cảnh vệ hư hỏng như chị đây đi。"
VI[41] = "（Nó tự nhận mình là đồ hư đấy à……<br>Làm ơn có ai đó ra dáng đến nhanh giúp tôi với……）"
VI[42] = "——Cạch。"
VI[43] = "Nàyyy，Celeste ơi。Nghe nói bắt được cướp ở chợ，thật không đấy？"  # BR FIX: remove <br>
VI[44] = "A，Đội trưởng！ Đúng là tai thính quá đi ♪"
VI[45] = "Đúng vậy！ Chị đây！ Chị đây bắt được！Phạm tội quả tang！ Màn bắt giữ chớp nhoáng！"  # BR FIX: remove <br>
VI[46] = "Ồ？ Không ngờ là mày，đồ trốn việc……"
VI[47] = "E hè hè hè hè。Có tiền thưởng không ạ？Có mà phải không ạ？"  # BR FIX: remove <br>
VI[48] = "Ừm，để ta xem nào。Mà，thằng cướp đâu rồi？"  # BR FIX: remove <br>
VI[49] = "Thằng này đây！ Nó khăng khăng bảo không làm，<br>nhưng chị sẽ moi ra ngay！"
VI[50] = "…………Chào。"
VI[51] = "…………"
VI[52] = "Gặp vài lần rồi nhỉ。Ông là Đội trưởng<br>Cảnh vệ phái từ Milesgard đến đúng không？"
VI[53] = "A，à，ờ，ờ……t，tại sao ngài lại ở đây ạ？"
VI[54] = "Vì chị bắt được nó đó！ Lao vào đỡ lúc nó đang chạy trốn！<br>Thế này——guwaaaa——！ Khóa chặt tay lại！"
VI[55] = "<size=48>ĐỒ，ĐỒ NGUUUUUUUUU XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ XUỐ！！！</size>"
VI[56] = "NGHEEE！？"
VI[57] = "Đ，Đội trưởng？ La to như thế<br>huyết áp sẽ tăng đấy ạ……？"  # BR FIX: add <br>
VI[58] = "Khỏi lo chuyện bao đồng！ Đồ ngu xuẩn này！<br>Mày có biết mày vừa làm gì không hả！？"
VI[59] = "Eeeee～……？ Gì ạ，kẻ cướp ấy mà——"
VI[60] = "Im mồm！ Bắt nhầm đấy！ Biết mày lười nhưng<br>không ngờ ngu thế này……Danh nghĩa Đội trưởng Cảnh vệ，phạt giảm lương！"
VI[61] = "Khôngggg！？ Sao lại thế——！？"
VI[62] = "À，không，Đội trưởng——không cần đến mức đó đâu。Phiền thật đấy nhưng<br>nếu chứng minh được tôi vô tội，thế là đủ rồi。"
VI[63] = "Hả……？Trời，anh——bộ anh là người tốt hả？ Anh là ai？"  # BR FIX: remove <br>
VI[64] = "（……Thằng này nịnh thật đấy）"
VI[65] = "Tấm lòng của ngài rất đáng quý，nhưng thế thì không làm gương cho kẻ khác được！<br>Xin hãy để tôi toàn quyền xử lý việc kỷ luật！"
VI[66] = "Đ，đâu ra thế——！？ Độc tài quá——！！"
VI[67] = "Im mồm！ Mau đi bắt thủ phạm thật đi！"
VI[68] = "Hii～！？ E，em đi đây——！"
VI[69] = "Chỉ Huy，thật có lỗi quá！！"
VI[70] = "Không sao。Mà này，con bé lúc nãy——tên là Celeste hả？<br>Nó là người thế nào？"
VI[71] = "Nó cũng tự xưng thế，đúng là một cảnh vệ hư hỏng hết chỗ nói……<br>Sống chỉ vì tiền với rượu，hạnh kiểm cũng tệ。Đúng là đồ không thể chịu nổi。"
VI[72] = "Vậy mà anh không đuổi nó，<br>chắc vì nó có tài đúng không？"  # BR FIX: add <br>
VI[73] = "……！？Sao ngài biết……？"  # BR FIX: remove <br>
VI[74] = "（……Quả nhiên là thế）"
VI[75] = "Nàyyyy！"
VI[76] = "Guwaa！？"
VI[77] = "（Lúc bị nó bắt，tôi không hề cảm nhận được gì<br>cho đến khi nó lao vào người）"  # BR FIX: add <br>
VI[78] = "（Tuy tôi không tự tin về võ lực，nhưng với tư cách Chỉ Huy tôi có khả năng nhận biết nguy hiểm。<br>Vậy mà tôi đã không nhận ra cú lao tới của nó）"
VI[79] = "（Nếu dùng được，có vẻ sẽ thành một nhân tài thú vị đây）"
VI[80] = "Ơ，Chỉ Huy？"
VI[81] = "Xin lỗi，không có gì。Tôi đi tìm Celeste đây。"
VI[82] = "（Nó bảo đi đuổi theo tên cướp nên chắc là ở chợ。<br>Đi xem sao。）"

assert len(VI) == 83, f"Expected 83 entries, got {len(VI)}"
for seq, vt in VI.items():
    if ',' in vt:
        print(f"ERROR: seq {seq} has ASCII comma: {vt[:50]!r}")
        sys.exit(1)

# ── READ EN ASSET ──
en_bytes = EN_ASSET.read_bytes()
has_bom = en_bytes[:3] == b'\xef\xbb\xbf'
text = en_bytes.decode('utf-8-sig')
lines = text.splitlines(keepends=True)

text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
en_records = [ln for ln in lines if ln.startswith(text_cmds)]
assert len(en_records) == 83, f"EN has {len(en_records)} text records"

seq = 0
out_lines = []
errors = []

for ln in lines:
    if not ln.startswith(text_cmds):
        out_lines.append(ln)
        continue

    # Determine line ending
    if ln.endswith('\r\n'):
        ending = '\r\n'
    elif ln.endswith('\n'):
        ending = '\n'
    else:
        ending = ''
    
    stripped = ln.rstrip('\r\n')
    vi_text = VI[seq]

    if ln.startswith('title,'):
        parts = stripped.split(',', 2)
        en_br = parts[1].count('<br>')
        vi_br = vi_text.count('<br>')
        if en_br != vi_br:
            errors.append(f"Seq {seq} (title) BR: EN={en_br} VI={vi_br}")
        parts[1] = vi_text
        rebuilt = ','.join(parts) + ending
        out_lines.append(rebuilt)
        seq += 1
        continue

    # message record
    parts = stripped.split(',', 5)
    en_text = parts[2]

    # Extract suffix (trailing <br> and any whitespace after it)
    suffix = ''
    if en_text.rstrip().endswith('<br>'):
        idx = en_text.rfind('<br>')
        suffix = en_text[idx:]
        internal_en = en_text[:idx]
    else:
        internal_en = en_text

    en_internal_br = internal_en.count('<br>')
    vi_br = vi_text.count('<br>')

    if en_internal_br != vi_br:
        errors.append(f"Seq {seq} BR: EN internal={en_internal_br} VI={vi_br} | VI: {vi_text[:80]}")

    parts[2] = vi_text + suffix
    rebuilt = ','.join(parts) + ending
    out_lines.append(rebuilt)
    seq += 1

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

assert seq == 83, f"Processed {seq} records"

output_str = ''.join(out_lines)
output_bytes = output_str.encode('utf-8')
if has_bom:
    output_bytes = b'\xef\xbb\xbf' + output_bytes

VI_PATH.parent.mkdir(parents=True, exist_ok=True)
VI_PATH.write_bytes(output_bytes)

print(f"Written {VI_PATH}")
print(f"Source lines: {len(lines)}")
print(f"Output lines: {len(out_lines)}")
print(f"Records processed: {seq}")
print("DONE: PASS")

#!/usr/bin/env python3
"""Generate VI translation output for hmn_10490100002.
77 records (1 title + 76 message). Field-index build.
Preserves BOM, CRLF, all technical fields.
"""
EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"
VI_PATH = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"

# ── Include the VI dict from check script ──
# (copy-pasted for standalone execution)
VI = {}

VI[0] = 'Knightvities ♪ Cùng Nào Cùng Lướt!'
VI[1] = 'Trời đẹp ghê，Chloe. Cứ như thời tiết hẹn hò vậy.<br> '
VI[2] = '………<br> '
VI[3] = 'Chloe ngượng ngùng nắm tay %user%，rồi gật đầu máy móc.<br> '
VI[4] = 'Ừ thì đang hẹn hò mà，hay đi mua sắm nhỉ.<br> '
VI[5] = '………<br> '
VI[6] = 'Nghe đây，hai người!<br> '
VI[7] = 'Úi! Alicia!<br> '
VI[8] = '………!?<br> '
VI[9] = 'Hãy thân thiết hơn đi...!<br>Đến mức chán luôn mấy chị kỵ sĩ ấy!<br> '
VI[10] = 'Tôi đang để ý đấy nhé! Thế，tôi xin phép!<br> '
VI[11] = 'Trời... Alicia còn giám sát cả mình. Hết đường trốn rồi...<br> '
VI[12] = '………<br> '
VI[13] = 'Nhiều đồ bán nhỉ. Có gì em thích không?<br> '
VI[14] = '………<br> '
VI[15] = 'Chloe run rẩy rồi lắc đầu.<br> '
VI[16] = '...Ờ，ừm. Đi dạo tí rồi ăn gì đó nhé.<br> '
VI[17] = '………<br> '
VI[18] = 'Mà tôi tự tiện gọi món rồi，không sao chứ?<br>Có món nào em không thích không?<br> '
VI[19] = '………<br> '
VI[20] = 'Vậy à，tốt rồi...<br> '
VI[21] = '...Này，đủ rồi đấy!<br> '
VI[22] = 'Hự!<br> '
VI[23] = 'Biết là bị ép hẹn hò nhưng không nói một câu nào là sao!<br> '
VI[24] = 'N-nhưng mà lần đầu em đi chơi với con trai，lại nắm tay nữa...<br>Thì...<br> '
VI[25] = 'Hồi hộp tim đập thình thịch—không thể nào nói chuyện tử tế<br>với anh được đâu，Chỉ Huy ơi...<br> '
VI[26] = '...Nếu vậy thì thôi. Để tôi nghĩ chủ đề nào đó<br>dễ nói hơn cho Chloe vậy.<br> '
VI[27] = 'Nào，Chloe，lúc rảnh em hay làm gì?<br> '
VI[28] = 'Dĩ nhiên là knightvities của em rồi!<br> '
VI[29] = '...Knightvities? Nhưng em là pháp sư mà，có phải kỵ sĩ đâu?<br> '
VI[30] = 'A，dân thường không hiểu được đâu ạ. Knightvities là hoạt động<br>ủng hộ kỵ sĩ mình yêu thích ý mà.<br> '
VI[31] = 'Là hoạt động fan yêu quý và ủng hộ kỵ sĩ mình thích—<br>từ trong bóng tối ra ánh sáng，không làm phiền mà vẫn cổ vũ nhiệt tình ạ.<br> '
VI[32] = 'Fan kỵ sĩ hả? Cũng hiểu được mà. Trong thị trấn cũng hay nghe người ta<br>bảo mê mấy chị ấy lúc diễu hành.<br> '
VI[33] = 'Vâng，có rất nhiều người cùng chí hướng!<br>Sở thích rất phổ biến luôn ạ!<br> '
VI[34] = 'Phổ biến thì chịu rồi...<br> '
VI[35] = 'Nói thật thì em đến căn cứ này cũng để ngắm thần tượng từ gần.<br>Em nộp đơn điều chuyển suốt đấy ạ.<br> '
VI[36] = 'Ra tận tiền tuyến chỉ để ngắm kỵ sĩ nữ?<br>Nguy hiểm tính mạng vì sở thích đấy，không sao à?<br> '
VI[37] = 'Không sao hết ạ! Lúc em báo tin điều chuyển，cộng đồng fan<br>chia làm hai ngả chúc mừng và ghen tị dữ lắm!<br> '
VI[38] = 'Lần trước là buổi live đầu tiên của em—rung động khi thấy thần tượng<br>tỏa sáng ngay trước mắt!<br> '
VI[39] = 'Thế còn có fanservice chính thức nữa...!<br>Quý giá tới mức suýt thì siêu thoại mất!<br> '
VI[40] = 'Đừng có siêu thoại. Sophia mà cũng lên mây chỉ vì được nói chuyện<br>thì tôi khổ lắm.<br> '
VI[41] = 'Mà này Chloe，em thích ai nhất? Tôi đoán là Sophia?<br> '
VI[42] = 'A，em không phải single-oshi—em là box-oshi của kỵ sĩ Milesgard ạ.<br> '
VI[43] = 'Nhưng nếu hỏi em theo ai nhất thì em là fan Eliza ạ. Mà em nhấn mạnh là<br>cố tình đấy nhé.<br> '
VI[44] = '"Fan Eliza" là gì?<br> '
VI[45] = 'Ừm，nghĩa là em đặc biệt hâm mộ chị Eliza ạ.<br> '
VI[46] = 'À，Eliza hả. Ừ，cô ấy đáng tin mà—hiểu sao làm fan rồi.<br> '
VI[47] = 'Hả-hả hả...! Dám nói về chị Eliza nhẹ nhàng trước fan chính chủ...!<br>May là em không phải dạng cấm đồng fan đấy，Chỉ Huy à!<br> '
VI[48] = 'Gì đâu không hiểu nổi，đừng có gán tội cho tôi! Tôi chỉ nói về đồng đội<br>thôi mà!<br> '
VI[49] = '... Ủa，nhìn kỹ thì cái em đeo bên hông—là thú nhồi bông Eliza<br>đúng không?<br> '
VI[50] = 'A，đúng rồi đúng rồi! Là Elushie đó! Em tự làm đấy ạ，mà cũng<br>tàm tạm nhỉ，hư hư hư...<br> '
VI[51] = 'Ừm tự làm thì vui thật，nhưng không phải hàng chính hãng nên<br>hơi khó ở chỗ không ủng hộ trực tiếp được thần tượng.<br> '
VI[52] = 'Cũng tại thiếu hàng chính hãng thôi ạ，nên em đành chấp nhận<br>cân bằng vậy.<br> '
VI[53] = 'Thì tụi này đâu có làm thú bông kỵ sĩ nữ. Mà nếu bán được...<br>nhỉ?<br> '
VI[54] = 'Chỉ một tin nhắn vu vơ mà bên chính thức động rồi...! Vui thì vui<br>nhưng sợ mấy fan nhóm khác chú ý quá...!<br> '
VI[55] = 'Ồ，kỵ sĩ khác cũng có fan à. Chloe không có kỵ sĩ yêu thích nào<br>ngoài Milesgard à?<br> '
VI[56] = 'Kỵ sĩ Milesgard là chính，nhưng em cũng đã tìm hiểu kỹ các group khác<br>mà. Dù gì thì chị Eliza cũng là người Perdion mà.<br> '
VI[57] = 'A，dĩ nhiên em không phải máu chó ăn tạp đâu!<br>Xin hiểu cho em nhé!<br> '
VI[58] = 'Có nhóm yêu thích không có nghĩa là em chê nhóm khác—em phản đối<br>chuyện đó. Mỗi nhóm đều có cái hay riêng mà.<br> '
VI[59] = 'Cộng đồng fan mà thấp kém đến mức tỉ thị với nhau<br>thì thần tượng cũng nhìn mình bằng ánh mắt kỳ thị đấy.<br> '
VI[60] = 'Vả lại，điều nhục nhất là thần tượng bị coi thường<br>vì chất lượng fan mà.<br> '
VI[61] = '...Nhiều từ không hiểu quá.<br>Thôi tôi cứ hiểu theo vibe vậy.<br> '
VI[62] = 'A，thế cũng được ạ! Xin lỗi，cứ nói đến knightvities là em lại<br>lỡ dài dòng quá...<br> '
VI[63] = 'Không，nghe khá thú vị đấy chứ. Kể thêm đi.<br> '
VI[64] = 'Hả! Chỉ Huy，bộ anh có năng khiếu à?<br>Muốn tham gia event tiếp theo với em không? Hàng đầu luôn nha?<br> '
VI[65] = 'Anh ở ngay chiến trường rồi，có ra tiền tuyến đâu.<br>Anh là Chỉ Huy mà.<br> '
VI[66] = 'Aaa，giọng điệu đó là không hiểu niềm vui live event rồi.<br>Được rồi，đầu tiên em sẽ dạy anh cách tìm công chúa kỵ sĩ ưng ý nhé...<br> '
VI[67] = '—Được rồi，dừng lại! Đến đó thôi ạ!<br> '
VI[68] = 'Hả，chị Alicia?<br> '
VI[69] = 'Có chuyện gì thế? Câu chuyện đang vui mà.<br> '
VI[70] = 'Phải đó，tụi em đang nói chuyện vui mà...<br> '
VI[71] = 'Nội dung câu chuyện toàn về các chị kỵ sĩ rồi kìa!<br>Phải làm Chỉ Huy quan tâm đến chuyện khác mới được chứ!<br> '
VI[72] = 'Úii! Phải rồi，lỡ mất kể về thần tượng suốt rồi!<br> '
VI[73] = 'Vậy là không được rồi! Chiến dịch hẹn hò tạm ngưng!<br> '
VI[74] = 'Này，Alicia? "Tạm ngưng" là chưa bỏ cuộc hả?<br> '
VI[75] = 'Dĩ nhiên rồi! Hẹn hò không xong thì chỉ còn cách cuối cùng thôi!<br>Hai người chuẩn bị tinh thần đi nhé!<br> '
VI[76] = 'Lại định bắt tụi em làm gì đây!<br> '

assert len(VI) == 77, f"Expected 77 entries, got {len(VI)}"

# ── Read EN asset ──
with open(EN_PATH, 'rb') as f:
    raw = f.read()

has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.split('\n')

# ── Build VI ──
out_lines = []
seq = 0
for ln in lines:
    # Strip CR from end if present
    orig_ending = '\r' if ln.endswith('\r') else ''
    ln_clean = ln.rstrip('\r')
    
    if not ln_clean.strip():
        out_lines.append(ln_clean + orig_ending)
        continue
    
    parts = ln_clean.split(',', 5)
    cmd = parts[0]
    
    if cmd == 'title' and seq == 0:
        # title,text
        new_ln = f"title,{VI[seq]}"
        seq += 1
    elif cmd == 'message' and len(parts) >= 3:
        # message,NAME,TEXT,...
        parts[2] = VI[seq]
        new_ln = ','.join(parts)
        seq += 1
    else:
        new_ln = ln_clean
    
    out_lines.append(new_ln + orig_ending)

assert seq == 77, f"Only processed {seq}/77 records"
assert len(out_lines) == len(lines), f"Line count mismatch: {len(out_lines)} vs {len(lines)}"

# ── Write output ──
output = '\n'.join(out_lines)
if has_bom:
    output = '\ufeff' + output

with open(VI_PATH, 'wb') as f:
    f.write(output.encode('utf-8'))

print(f"✅ Written {VI_PATH}")
print(f"   Records: {seq}, Lines: {len(out_lines)}, BOM: {has_bom}")
print(f"   CRLF in input: {has_crlf}")

# ── Quick structural check ──
with open(VI_PATH, 'rb') as f:
    vi_raw = f.read()
vi_text = vi_raw.decode('utf-8-sig')
vi_lines = vi_text.split('\n')

# Check line count matches
assert len(vi_lines) == len(lines), f"VI lines {len(vi_lines)} != EN lines {len(lines)}"

# Check BOM
vi_has_bom = vi_raw[:3] == b'\xef\xbb\xbf'
assert vi_has_bom == has_bom, f"BOM mismatch: VI={vi_has_bom} EN={has_bom}"

print("✅ Structural integrity: line count and BOM match EN asset.")
print("Done.")

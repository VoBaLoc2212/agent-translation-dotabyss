#!/usr/bin/env python3
"""Build VI for hmn_10490100002 (77 records: 1 title + 76 message).
EN-asset-is-English with JP title. Field-index build."""
import re, json, sys

EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"
VI_PATH = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10490100002.txt"

# ── VI Translations (seq 0=title, 1..76=message) ──
# Fullwidth ，(U+FF0C) inside text per EN asset convention.
# BR count per entry MUST match EN asset.

VI = {}

# seq 0: title — 騎士活♪ゴーゴーレッツゴー！
VI[0] = 'Knightvities ♪ Cùng Nào Cùng Lướt!'

# seq 1: Commander — br=1
VI[1] = 'Trời đẹp ghê，Chloe. Cứ như thời tiết hẹn hò vậy.<br> '

# seq 2: Chloe silence — br=1
VI[2] = '………<br> '

# seq 3: narration — br=1
VI[3] = 'Chloe ngượng ngùng nắm tay %user%，rồi gật đầu máy móc.<br> '

# seq 4: Commander — br=1
VI[4] = 'Ừ thì đang hẹn hò mà，hay đi mua sắm nhỉ.<br> '

# seq 5: Chloe silence — br=1
VI[5] = '………<br> '

# seq 6: Alicia — br=1
VI[6] = 'Nghe đây，hai người!<br> '

# seq 7: Commander — br=1
VI[7] = 'Úi! Alicia!<br> '

# seq 8: Chloe shock — br=1
VI[8] = '………!?<br> '

# seq 9: Alicia — br=2
VI[9] = 'Hãy thân thiết hơn đi...!<br>Đến mức chán luôn mấy chị kỵ sĩ ấy!<br> '

# seq 10: Alicia — br=1
VI[10] = 'Tôi đang để ý đấy nhé! Thế，tôi xin phép!<br> '

# seq 11: Commander — br=1
VI[11] = 'Trời... Alicia còn giám sát cả mình. Hết đường trốn rồi...<br> '

# seq 12: Chloe — br=1
VI[12] = '………<br> '

# seq 13: Commander — br=1
VI[13] = 'Nhiều đồ bán nhỉ. Có gì em thích không?<br> '

# seq 14: Chloe — br=1
VI[14] = '………<br> '

# seq 15: narration — br=1
VI[15] = 'Chloe run rẩy rồi lắc đầu.<br> '

# seq 16: Commander — br=1
VI[16] = '...Ờ，ừm. Đi dạo tí rồi ăn gì đó nhé.<br> '

# seq 17: Chloe — br=1
VI[17] = '………<br> '

# seq 18: Commander — br=2
VI[18] = 'Mà tôi tự tiện gọi món rồi，không sao chứ?<br>Có món nào em không thích không?<br> '

# seq 19: Chloe — br=1
VI[19] = '………<br> '

# seq 20: Commander — br=1
VI[20] = 'Vậy à，tốt rồi...<br> '

# seq 21: Commander — br=1
VI[21] = '...Này，đủ rồi đấy!<br> '

# seq 22: Chloe Eep — br=1
VI[22] = 'Hự!<br> '

# seq 23: Commander — br=1
VI[23] = 'Biết là bị ép hẹn hò nhưng không nói một câu nào là sao!<br> '

# seq 24: Chloe — br=2
VI[24] = 'N-nhưng mà lần đầu em đi chơi với con trai，lại nắm tay nữa...<br>Thì...<br> '

# seq 25: Chloe — br=2
VI[25] = 'Hồi hộp tim đập thình thịch—không thể nào nói chuyện tử tế<br>với anh được đâu，Chỉ Huy ơi...<br> '

# seq 26: Commander — br=2
VI[26] = '...Nếu vậy thì thôi. Để tôi nghĩ chủ đề nào đó<br>dễ nói hơn cho Chloe vậy.<br> '

# seq 27: Commander — br=1
VI[27] = 'Nào，Chloe，lúc rảnh em hay làm gì?<br> '

# seq 28: Chloe — br=1
VI[28] = 'Dĩ nhiên là knightvities của em rồi!<br> '

# seq 29: Commander — br=1
VI[29] = '...Knightvities? Nhưng em là pháp sư mà，có phải kỵ sĩ đâu?<br> '

# seq 30: Chloe — br=2
VI[30] = 'A，dân thường không hiểu được đâu ạ. Knightvities là hoạt động<br>ủng hộ kỵ sĩ mình yêu thích ý mà.<br> '

# seq 31: Chloe — br=2
VI[31] = 'Là hoạt động fan yêu quý và ủng hộ kỵ sĩ mình thích—<br>từ trong bóng tối ra ánh sáng，không làm phiền mà vẫn cổ vũ nhiệt tình ạ.<br> '

# seq 32: Commander — br=2
VI[32] = 'Fan kỵ sĩ hả? Cũng hiểu được mà. Trong thị trấn cũng hay nghe người ta<br>bảo mê mấy chị ấy lúc diễu hành.<br> '

# seq 33: Chloe — br=2
VI[33] = 'Vâng，có rất nhiều người cùng chí hướng!<br>Sở thích rất phổ biến luôn ạ!<br> '

# seq 34: Commander — br=1
VI[34] = 'Phổ biến thì chịu rồi...<br> '

# seq 35: Chloe — br=2
VI[35] = 'Nói thật thì em đến căn cứ này cũng để ngắm thần tượng từ gần.<br>Em nộp đơn điều chuyển suốt đấy ạ.<br> '

# seq 36: Commander — br=2
VI[36] = 'Ra tận tiền tuyến chỉ để ngắm kỵ sĩ nữ?<br>Nguy hiểm tính mạng vì sở thích đấy，không sao à?<br> '

# seq 37: Chloe — br=2
VI[37] = 'Không sao hết ạ! Lúc em báo tin điều chuyển，cộng đồng fan<br>chia làm hai ngả chúc mừng và ghen tị dữ lắm!<br> '

# seq 38: Chloe — br=2
VI[38] = 'Lần trước là buổi live đầu tiên của em—rung động khi thấy thần tượng<br>tỏa sáng ngay trước mắt!<br> '

# seq 39: Chloe — br=2
VI[39] = 'Thế còn có fanservice chính thức nữa...!<br>Quý giá tới mức suýt thì siêu thoại mất!<br> '

# seq 40: Commander — br=2
VI[40] = 'Đừng có siêu thoại. Sophia mà cũng lên mây chỉ vì được nói chuyện<br>thì tôi khổ lắm.<br> '

# seq 41: Commander — br=1
VI[41] = 'Mà này Chloe，em thích ai nhất? Tôi đoán là Sophia?<br> '

# seq 42: Chloe — br=1 (trailing <br> is before field separator)
VI[42] = 'A，em không phải single-oshi—em là box-oshi của kỵ sĩ Milesgard ạ.<br> '

# seq 43: Chloe — br=2
VI[43] = 'Nhưng nếu hỏi em theo ai nhất thì em là fan Eliza ạ. Mà em nhấn mạnh là<br>cố tình đấy nhé.<br> '

# seq 44: Commander — br=1
VI[44] = '"Fan Eliza" là gì?<br> '

# seq 45: Chloe — br=1 (trailing <br> before ,300201...)
VI[45] = 'Ừm，nghĩa là em đặc biệt hâm mộ chị Eliza ạ.<br> '

# seq 46: Commander — br=1
VI[46] = 'À，Eliza hả. Ừ，cô ấy đáng tin mà—hiểu sao làm fan rồi.<br> '

# seq 47: Chloe — br=2
VI[47] = 'Hả-hả hả...! Dám nói về chị Eliza nhẹ nhàng trước fan chính chủ...!<br>May là em không phải dạng cấm đồng fan đấy，Chỉ Huy à!<br> '

# seq 48: Commander — br=2
VI[48] = 'Gì đâu không hiểu nổi，đừng có gán tội cho tôi! Tôi chỉ nói về đồng đội<br>thôi mà!<br> '

# seq 49: Commander — br=2
VI[49] = '... Ủa，nhìn kỹ thì cái em đeo bên hông—là thú nhồi bông Eliza<br>đúng không?<br> '

# seq 50: Chloe — br=2
VI[50] = 'A，đúng rồi đúng rồi! Là Elushie đó! Em tự làm đấy ạ，mà cũng<br>tàm tạm nhỉ，hư hư hư...<br> '

# seq 51: Chloe — br=2
VI[51] = 'Ừm tự làm thì vui thật，nhưng không phải hàng chính hãng nên<br>hơi khó ở chỗ không ủng hộ trực tiếp được thần tượng.<br> '

# seq 52: Chloe — br=2
VI[52] = 'Cũng tại thiếu hàng chính hãng thôi ạ，nên em đành chấp nhận<br>cân bằng vậy.<br> '

# seq 53: Commander — br=2
VI[53] = 'Thì tụi này đâu có làm thú bông kỵ sĩ nữ. Mà nếu bán được...<br>nhỉ?<br> '

# seq 54: Chloe — br=2
VI[54] = 'Chỉ một tin nhắn vu vơ mà bên chính thức động rồi...! Vui thì vui<br>nhưng sợ mấy fan nhóm khác chú ý quá...!<br> '

# seq 55: Commander — br=2
VI[55] = 'Ồ，kỵ sĩ khác cũng có fan à. Chloe không có kỵ sĩ yêu thích nào<br>ngoài Milesgard à?<br> '

# seq 56: Chloe — br=2
VI[56] = 'Kỵ sĩ Milesgard là chính，nhưng em cũng đã tìm hiểu kỹ các group khác<br>mà. Dù gì thì chị Eliza cũng là người Perdion mà.<br> '

# seq 57: Chloe — br=2
VI[57] = 'A，dĩ nhiên em không phải máu chó ăn tạp đâu!<br>Xin hiểu cho em nhé!<br> '

# seq 58: Chloe — br=2
VI[58] = 'Có nhóm yêu thích không có nghĩa là em chê nhóm khác—em phản đối<br>chuyện đó. Mỗi nhóm đều có cái hay riêng mà.<br> '

# seq 59: Chloe — br=2
VI[59] = 'Cộng đồng fan mà thấp kém đến mức tỉ thị với nhau<br>thì thần tượng cũng nhìn mình bằng ánh mắt kỳ thị đấy.<br> '

# seq 60: Chloe — br=2
VI[60] = 'Vả lại，điều nhục nhất là thần tượng bị coi thường<br>vì chất lượng fan mà.<br> '

# seq 61: Commander — br=2
VI[61] = '...Nhiều từ không hiểu quá.<br>Thôi tôi cứ hiểu theo vibe vậy.<br> '

# seq 62: Chloe — br=2
VI[62] = 'A，thế cũng được ạ! Xin lỗi，cứ nói đến knightvities là em lại<br>lỡ dài dòng quá...<br> '

# seq 63: Commander — br=1
VI[63] = 'Không，nghe khá thú vị đấy chứ. Kể thêm đi.<br> '

# seq 64: Chloe — br=2
VI[64] = 'Hả! Chỉ Huy，bộ anh có năng khiếu à?<br>Muốn tham gia event tiếp theo với em không? Hàng đầu luôn nha?<br> '

# seq 65: Commander — br=2
VI[65] = 'Anh ở ngay chiến trường rồi，có ra tiền tuyến đâu.<br>Anh là Chỉ Huy mà.<br> '

# seq 66: Chloe — br=2
VI[66] = 'Aaa，giọng điệu đó là không hiểu niềm vui live event rồi.<br>Được rồi，đầu tiên em sẽ dạy anh cách tìm công chúa kỵ sĩ ưng ý nhé...<br> '

# seq 67: Alicia — br=1 (stop!)
VI[67] = '—Được rồi，dừng lại! Đến đó thôi ạ!<br> '

# seq 68: Chloe — br=1 (Huh, Alicia?)
VI[68] = 'Hả，chị Alicia?<br> '

# seq 69: Commander — br=1
VI[69] = 'Có chuyện gì thế? Câu chuyện đang vui mà.<br> '

# seq 70: Chloe — br=1 (That's right...)
VI[70] = 'Phải đó，tụi em đang nói chuyện vui mà...<br> '

# seq 71: Alicia — br=2 (The convo is about female knights!)
VI[71] = 'Nội dung câu chuyện toàn về các chị kỵ sĩ rồi kìa!<br>Phải làm Chỉ Huy quan tâm đến chuyện khác mới được chứ!<br> '

# seq 72: Chloe — br=1 (Ohh! That's right!)
VI[72] = 'Úii! Phải rồi，lỡ mất kể về thần tượng suốt rồi!<br> '

# seq 73: Alicia — br=1 (That's no good! Date op on hold!)
VI[73] = 'Vậy là không được rồi! Chiến dịch hẹn hò tạm ngưng!<br> '

# seq 74: Commander — br=1 (Hey Alicia? "For now" means...)
VI[74] = 'Này，Alicia? "Tạm ngưng" là chưa bỏ cuộc hả?<br> '

# seq 75: Alicia — br=2 (Of course! Final measure!)
VI[75] = 'Dĩ nhiên rồi! Hẹn hò không xong thì chỉ còn cách cuối cùng thôi!<br>Hai người chuẩn bị tinh thần đi nhé!<br> '

# seq 76: Chloe — br=1 (What are you going to make us do!)
VI[76] = 'Lại định bắt tụi em làm gì đây!<br> '

# ── verify count ──
assert len(VI) == 77, f"Expected 77 VI entries, got {len(VI)}"

# ── Preflight: check BR counts vs EN asset ──
print("═══ PREFLIGHT ═══")
print(f"VI entries: {len(VI)}")

# Load EN asset
with open(EN_PATH, 'rb') as f:
    raw = f.read()
has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.split('\n')
print(f"BOM: {has_bom}, CRLF: {has_crlf}, lines: {len(lines)}")

# Extract EN text fields and check BR counts
errors = []
seq = 0
en_texts = []
for i, ln in enumerate(lines):
    ln_raw = ln  # keep original ending
    ln_stripped = ln.rstrip('\r').strip()
    if not ln_stripped:
        continue
    
    parts = ln_stripped.split(',', 5)
    cmd = parts[0]
    
    if cmd == 'title':
        # title,text
        en_tf = ln_stripped[len('title,'):]
        if seq in VI:
            vi = VI[seq]
            en_br = en_tf.count('<br>')
            vi_br = vi.count('<br>')
            if en_br != vi_br:
                errors.append(f"  ## seq {seq} line {i+1} BR mismatch: en_br={en_br} vi_br={vi_br}")
            # Check ASCII comma in VI
            if ',' in vi:
                errors.append(f"  ## seq {seq} line {i+1} ASCII comma in VI!")
            en_texts.append((seq, 'title', en_tf))
        seq += 1
    
    elif cmd in ('messageTextUnder', 'messageTextCenter'):
        if len(parts) >= 3:
            en_tf = parts[2]
        else:
            en_tf = ''
        if seq in VI:
            vi = VI[seq]
            en_br = en_tf.count('<br>')
            vi_br = vi.count('<br>')
            if en_br != vi_br:
                errors.append(f"  ## seq {seq} line {i+1} BR mismatch: en_br={en_br} vi_br={vi_br}")
            if ',' in vi:
                errors.append(f"  ## seq {seq} line {i+1} ASCII comma in VI!")
            en_texts.append((seq, cmd, en_tf))
        seq += 1
    
    elif cmd == 'message':
        if len(parts) >= 3:
            en_tf = parts[2]
        else:
            en_tf = ''
        if seq in VI:
            vi = VI[seq]
            en_br = en_tf.count('<br>')
            vi_br = vi.count('<br>')
            if en_br != vi_br:
                errors.append(f"  ## seq {seq} line {i+1} BR mismatch: en_br={en_br} vi_br={vi_br}")
            if ',' in vi:
                errors.append(f"  ## seq {seq} line {i+1} ASCII comma in VI!")
            en_texts.append((seq, 'message', en_tf))
        seq += 1

print(f"\nRecords found: {seq}")
if errors:
    print("\nERRORS:")
    for e in errors:
        print(e)
    print(f"\nTotal errors: {len(errors)}")
    if errors:
        sys.exit(1)
else:
    print("\n✅ All BR counts match! No ASCII commas in VI text.")
    print("Ready to build.")

print(f"\nSequences in VI: {sorted(VI.keys())}")

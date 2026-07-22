#!/usr/bin/env python3
"""
Build VI translation for hmn_10460100001 (Elmia the Elf Bodyguard).
EN-asset-is-English case: replace EN text fields with VI translations.
"""
import re, json, sys
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10460100001.txt"
VI_ASSET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10460100001.txt"

# --- Vietnamese translations keyed by sequential text-record index (1-based) ---
# Record 1-75: 1 title + 74 message
VI_DICT = {}

# Seq 1: title
VI_DICT[1] = "Người Lính Gác Elf Cứng Nhắc"

# Seq 2-75: message records
VI_DICT[2] = "Xin lỗi vì lần nào cũng bắt cậu phải đến tận Căn Cứ Tiền Tuyến<br>để mua lại vũ khí tìm được ở Đại Huyệt."
VI_DICT[3] = "Khu vực này an ninh cũng chẳng tốt lắm‚ chắc vất vả lắm nhỉ?"
VI_DICT[4] = "Không không. Vì tôi được gặp những bảo vật đáng để liều mạng mà.<br>Cảm ơn cậu đã luôn chiếu cố."
VI_DICT[5] = "Vậy‚ lần này hàng mua ở đâu vậy?"
VI_DICT[6] = "À‚ ở trong cái hộp để ở đằng kia."
VI_DICT[7] = "Có vài món đẹp‚ nhưng cũng nhiều món bị gãy hoặc cong. Thành thật mà nói‚<br>hàng tốt xấu lẫn lộn."
VI_DICT[8] = "Cậu xem thử xem đáng giá bao nhiêu đi."
VI_DICT[9] = "Đã rõ. Vậy Elmia‚ nhờ cô đấy."
VI_DICT[10] = "Rõ‚ sếp."
VI_DICT[11] = "Hử...? Cô ấy lần trước đâu có ở đây. Nhân viên mới à?"
VI_DICT[12] = "Vâng.<br>Là vệ sĩ tôi mới thuê ở công ty thương mại tôi làm việc đấy."
VI_DICT[13] = "Ồ. Vận chuyển hàng quý giá là chuyến đi nguy hiểm.<br>Chắc ông đã thuê một vệ sĩ khá cừ khôi nhỉ."
VI_DICT[14] = "Tất nhiên. Cô ấy rất cừ khôi. Và còn có một kỹ năng đặc biệt hữu dụng nữa..."
VI_DICT[15] = "Kỹ năng đặc biệt?"
VI_DICT[16] = "Cây cung này... được thiết kế cầu kỳ đấy‚ nhưng chắc chẳng đáng giá bao nhiêu."
VI_DICT[17] = "Cây thương này... bị sứt một chút‚ nhưng giá trị thì không có gì phải phàn nàn.<br>Mài lại là có thể dùng trong thực chiến được đấy."
VI_DICT[18] = "Cây gậy này... khá có giá trị đấy.<br>Ở Đại Huyệt có thể kiếm được cả thứ này sao..."
VI_DICT[19] = "Ô hô... ngạc nhiên đấy!"
VI_DICT[20] = "Elmia... phải không? Cô có thể giám định vũ khí à?"
VI_DICT[21] = "Ừ. Tôi với vũ khí có duyên từ lâu rồi."
VI_DICT[22] = "Ồ? Nghe có vẻ thú vị đấy. Kể tôi nghe đi."
VI_DICT[23] = "Tôi không phiền đâu‚ nhưng... xin lỗi nhé‚ chẳng thú vị tí nào đâu."
VI_DICT[24] = "Tôi đến từ Eldorana. Trước đây tôi làm thủ kho ở đó."
VI_DICT[25] = "Dù là thủ kho‚ nhưng đó là một thị trấn yên bình nên<br>cũng chẳng có việc gì nhiều."
VI_DICT[26] = "Trong lúc rảnh‚ tôi phụ giúp sắp xếp hàng hóa linh tinh‚ và đó là<br>cách tôi trau dồi khả năng giám định vũ khí."
VI_DICT[27] = "Không bằng dân chuyên‚ nhưng tôi có thể dễ dàng nhận ra món nào có giá trị‚<br>dù chủ yếu chỉ giới hạn ở vũ khí thôi."
VI_DICT[28] = "Ồ‚ ra vậy. Dùng thời gian rảnh để nâng cao kỹ năng á?<br>Giỏi đấy chứ."
VI_DICT[29] = "Thấy chưa? Một câu chuyện nhạt nhẽo vô vị đúng không?"
VI_DICT[30] = "Hử? Đâu có. Tôi còn muốn nghe thêm nữa kìa."
VI_DICT[31] = "Đúng là người kỳ lạ."
VI_DICT[32] = "Vì đó là chuyện về công việc tôi chưa từng làm‚ nên thấy mới mẻ. Nhưng mà..."
VI_DICT[33] = "Tôi chỉ hơi thắc mắc‚ Elmia này‚ sao cô lại trở thành vệ sĩ cho một<br>thương nhân thế?"
VI_DICT[34] = "Đừng bận tâm mấy chuyện đó‚ sếp..."
VI_DICT[35] = "Elmia‚ cái kho cô từng làm việc yên bình phải không? Nhưng<br>canh gác hàng khai thác ở Căn Cứ Tiền Tuyến thì nguy hiểm rình rập."
VI_DICT[36] = "Bọn cướp nhắm vào kho báu sẽ để mắt tới‚ và<br>gần Đại Huyệt cũng có nhiều quái vật."
VI_DICT[37] = "Tôi không thể tưởng tượng nổi việc bỏ một công việc an toàn chỉ để làm cái này."
VI_DICT[38] = "Ờ‚ ờ thì... chuyện dài lắm‚ nói thế nào nhỉ‚<br>có những tình huống còn cao hơn núi và sâu hơn biển ấy..."
VI_DICT[39] = "Ờ‚ ờ... quên chuyện đó đi! Này‚ giám định xong rồi đây!"
VI_DICT[40] = "Đây là giá trị của số vũ khí anh mang tới. Tôi giám định<br>không hề thiên vị đâu‚ giá khá tốt đấy‚ phải không?"
VI_DICT[41] = "Để xem nào... hừm‚ Elmia‚ cô làm tốt đấy. Lý lẽ trong<br>bản định giá rất chắc chắn."
VI_DICT[42] = "Giám định viên không tồi. Tôi suýt muốn thuê cô ấy về chỗ mình."
VI_DICT[43] = "Nhưng... có rẻ quá không? Lần này đáng lẽ phải có một kiệt tác<br>tôi đề cử chứ."
VI_DICT[44] = "Kiệt tác? Tôi chẳng nhớ có thứ gì như vậy cả..."
VI_DICT[45] = "Tên là 'Lưỡi Kiếm Vô Tận Rìa Vũ Trụ'—một thanh kiếm thần mô phỏng<br>ánh sao‚ xé toạc vũ trụ như dải ngân hà!"
VI_DICT[46] = "Lần đầu tôi nghe tên một thanh kiếm như vậy đấy..."
VI_DICT[47] = "Ờ‚ dĩ nhiên rồi. Vì tôi tự đặt tên mà."
VI_DICT[48] = "Này‚ sếp..."
VI_DICT[49] = "'Mô phỏng‚' 'như thể‚' 'như'... Đó là một cái tên kiếm hoàn toàn mơ hồ‚<br>phải không?"
VI_DICT[50] = "Tôi đặt tên thế vì nó là một thanh kiếm quá đẹp‚ chắc chắn là<br>một kiệt tác có giá trị."
VI_DICT[51] = "Một lời giám định tay mơ sảng khoái đấy."
VI_DICT[52] = "Nhưng... tôi đâu có thấy thanh kiếm nào đẹp đến thế?"
VI_DICT[53] = "Này‚ hai người! Đằng kia kìa!"
VI_DICT[54] = "Đúng lũ ngốc! Bị trộm vũ khí mà<br>chẳng hề hay biết gì!"
VI_DICT[55] = "Để tao đổi cái này thành tiền cho!"
VI_DICT[56] = "Chào tạm biệt‚ lũ ngốc!"
VI_DICT[57] = "………"
VI_DICT[58] = "………"
VI_DICT[59] = "A! 'Lưỡi Kiếm Vô Tận Rìa Vũ Trụ' của tôi—thanh kiếm thần mô phỏng ánh<br>sao‚ xé toạc vũ trụ như dải ngân hà!?"
VI_DICT[60] = "Cô đang làm gì thế‚ vệ sĩ kia!"
VI_DICT[61] = "Tại anh cứ nói chuyện với tôi‚ nên tôi mất tập trung đấy!"
VI_DICT[62] = "Chết tiệt! Đáng lẽ thanh kiếm đó có thể bán giá cao!"
VI_DICT[63] = "Thật xui xẻo. Tôi thông cảm cho anh."
VI_DICT[64] = "Elmia‚ vì cô không hoàn thành nhiệm vụ vệ sĩ‚ nên tôi<br>sẽ cắt lương đấy."
VI_DICT[65] = "Tôi rút lại lời! Nhất định phải lấy lại hàng bị đánh cắp!"
VI_DICT[66] = "Đồ ăn trộm! Đứng lại đó!"
VI_DICT[67] = "Này! Anh tên gì?"
VI_DICT[68] = "Là %user%! Em có thể gọi tôi là Ngài %user%‚ Lãnh Chúa %user%‚ hoặc<br>Chỉ Huy."
VI_DICT[69] = "Tôi không phải cấp dưới của anh đâu. Tôi sẽ gọi anh là %user%."
VI_DICT[70] = "Hừm‚ bị một đứa trẻ gọi thẳng tên... hơi..."
VI_DICT[71] = "Anh thấy tôi chỗ nào mà bảo là trẻ con hả!?<br>Ngực tôi lép là do bẩm sinh đấy!"
VI_DICT[72] = "Tôi đã hơn 200 tuổi đấy nhé! Tôi còn lớn tuổi hơn anh đấy!?"
VI_DICT[73] = "Chết tiệt... sao ai cũng đối xử với tôi như trẻ con thế!?<br>Cứ cao với ngực to là giỏi à...!?"
VI_DICT[74] = "Này. Không nhanh lên là mất dấu bọn cướp đấy."
VI_DICT[75] = "Tại ai hả‚ tại ai!"


# --- Step 1: Read EN asset ---
raw = open(EN_ASSET, 'rb').read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.splitlines(True)  # keep line endings

# --- Step 2: Identify text records and verify count ---
TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')

# First pass: enumerate text records from the EN file
en_records = []
for ln in lines:
    stripped = ln.strip()
    if any(stripped.startswith(cmd) for cmd in TEXT_CMDS):
        en_records.append(stripped)

print(f"EN text record count: {len(en_records)}")
for i, r in enumerate(en_records, 1):
    print(f"  {i}: {r[:80]}...")

assert len(VI_DICT) == len(en_records), \
    f"VI_DICT count ({len(VI_DICT)}) != EN record count ({len(en_records)})"

# --- Step 3: Preflight BR and comma checks ---
print("\n--- PREFLIGHT ---")
errors = []
seq = 0
for ln in lines:
    stripped = ln.strip()
    if not any(stripped.startswith(cmd) for cmd in TEXT_CMDS):
        continue
    seq += 1
    vi = VI_DICT[seq]
    
    # Check for ASCII comma in VI text
    if ',' in vi:
        errors.append(f"Seq {seq}: ASCII comma found in VI: {vi[:50]}")
    
    # For message records: check <br> count excluding the text-only field
    # We'll do a more targeted check later

if errors:
    print("PREFLIGHT FAILED:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("PREFLIGHT PASSED: No ASCII commas in VI text.")

# --- Step 4: Build VI output ---
out_lines = []
seq = 0
line_count = 0

for ln in lines:
    stripped = ln.strip()
    
    if any(stripped.startswith(cmd) for cmd in TEXT_CMDS):
        seq += 1
        vi = VI_DICT[seq]
        
        # Determine which field to replace
        raw_ln = ln.rstrip('\r\n')
        ending = '\r\n' if ln.endswith('\r\n') else '\n'
        
        if stripped.startswith('title,'):
            # title,<text> — just replace everything after "title,"
            vi_line = f"title,{vi}"
            out_lines.append(vi_line + ending)
            line_count += 1
            continue
        
        # For message, messageTextUnder, messageTextCenter
        # Use field-index approach: split by ASCII comma, replace text field (idx 2), rejoin
        parts = raw_ln.split(',')
        if len(parts) >= 3:
            # Mirror the trailing tag suffix from the EN text field (e.g., '<br> ')
            en_text_field = parts[2]
            # Find trailing tag suffix (tag + optional whitespace at end)
            suffix = ''
            m = re.search(r'(<[^>]+>\s*)+$', en_text_field)
            if m:
                suffix = m.group(0)
            # Ensure VI has the same internal <br> count as EN content (before suffix)
            en_content_br = en_text_field[:m.start() if m else len(en_text_field)].count('<br>')
            vi_content_br = vi.count('<br>')
            if en_content_br != vi_content_br:
                print(f"WARNING: Seq {seq} internal <br> count mismatch: EN={en_content_br}, VI={vi_content_br}")
            parts[2] = vi + suffix
            vi_line_text = ','.join(parts)
        else:
            vi_line_text = raw_ln  # fallback: keep as-is
        out_lines.append(vi_line_text + ending)
        line_count += 1
        continue
    
    # Non-text line: keep as-is
    out_lines.append(ln)
    line_count += 1

# --- Step 5: Write VI output ---
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)

output_text = ''.join(out_lines)

output_bytes = (b'\xef\xbb\xbf' if has_bom else b'') + output_text.encode('utf-8')

# Write
open(VI_ASSET, 'wb').write(output_bytes)

# Verify line count
vi_raw = open(VI_ASSET, 'rb').read()
vi_text = vi_raw.decode('utf-8-sig')
vi_lines = vi_text.splitlines(True)
print(f"\nEN lines: {len(lines)}")
print(f"VI lines: {len(vi_lines)}")
print(f"VI text records replaced: {seq}")
print(f"Output: {VI_ASSET}")

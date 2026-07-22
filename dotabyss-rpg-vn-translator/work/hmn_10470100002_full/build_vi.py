#!/usr/bin/env python3
"""
Build VI asset: hmn_10470100002 (Merem fortune-teller scene)
EN-asset-is-English case, title still JP.
Field-index generator with seq-keyed VI_DICT.
"""
import json, re, sys, os
from pathlib import Path

# Paths
ROOT = Path("E:/AgentTranslation")
EN_PATH = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10470100002.txt"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10470100002.txt"
JA_PATH = ROOT / "dotabyss-translation-main/translations/novels/hmn_10470100002/ja.json"

# Load ja.json for title JP
with open(JA_PATH, "r", encoding="utf-8") as f:
    ja = json.load(f)

# Read EN asset lines with BOM/CRLF preservation
with open(EN_PATH, "rb") as f:
    raw = f.read()

has_bom = raw.startswith(b'\xef\xbb\xbf')
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.splitlines(keepends=True)  # preserves endings including empty lines

# Identify text commands and their sequence
TEXT_CMDS = ('title,', 'message,', 'messageTextCenter,', 'messageTextUnder,')
seq_record = []  # list of (seq, line_index, cmd, speaker, text_field, trailing_suffix)

for i, ln in enumerate(lines):
    stripped = ln.rstrip('\r\n')
    if not stripped:
        continue
    for cmd in TEXT_CMDS:
        if stripped.startswith(cmd):
            # Split on commas to locate fields
            parts = stripped.split(',')
            if cmd == 'title,':
                # title,<text>
                speaker = ''
                text_field = parts[1] if len(parts) > 1 else ''
                suffix = ''
            elif cmd == 'messageTextCenter,' or cmd == 'messageTextUnder,':
                # msgCenter,,<text>,,,on  -> parts[2] is text
                speaker = parts[1] if len(parts) > 1 else ''
                text_field = parts[2] if len(parts) > 2 else ''
                suffix = ''
            else:  # message,
                # message,<speaker>,<text>[,vc_id,chara_id]
                speaker = parts[1] if len(parts) > 1 else ''
                text_field = parts[2] if len(parts) > 2 else ''
                # Extract trailing suffix (tags + spaces)
                suffix_match = re.search(r'(<[^>]+>\s*)+$', text_field)
                suffix = suffix_match.group(0) if suffix_match else ''
                text_field = text_field[:-len(suffix)] if suffix else text_field
            seq_record.append((len(seq_record) + 1, i, cmd, speaker, text_field, suffix))
            break

total_records = len(seq_record)
print(f"Total text records: {total_records}")
for seq, li, cmd, sp, tf, suf in seq_record:
    print(f"  seq={seq:2d} line={li:4d} cmd={cmd:25s} speaker={sp[:20]:20s} br={tf.count('<br>')}")

# ========== VI_DICT: translations keyed by seq (1-indexed) ==========
# Rules: 
# - title seq 1: translate JP→VI Title Case
# - messageTextCenter seq 2: translate EN→VI Title Case  
# - message seq 3-71: translate EN→VI
# - Commander/<user> → keep <user> (EN source has <user>)
# - "Commander" in dialogue → "Chỉ Huy"
# - Merem uses polite tôi/Chỉ Huy, Commander uses tôi/cô
# - Monster A/B growls → localize
# - ASCII comma in VI → U+201A ‚

title_jp = seq_record[0][4]  # 占いに導かれし者たちの試練
title_vi = "Thử Thách Của Những Kẻ Được Dẫn Dắt Bởi Bói Toán"

center_text = seq_record[1][4]  # <size=48>—The Shallow Layers of the Abyss</size>
center_vi = '<size=48>—Tầng Nông Của Đại Huyệt</size>'

VI_DICT = {
    # --- title ---
    1: title_vi,
    # --- messageTextCenter ---
    2: center_vi,
    # --- message records seq 3..71 ---
    3: "Sự may mắn lớn mà bói toán của Merem nói tôi sẽ gặp ở Đại Huyệt!<br>Tôi không thể chờ để xem mình sẽ gặp gì!",
    4: "Kết quả bói toán chỉ là kim chỉ nam. Tùy mỗi<br>người quyết định con đường nào để đi.",
    5: "Hử? Không ổn rồi‚ có quái vật kia.",
    6: "Gừ...",
    7: "Hình như nó chưa phát hiện ra chúng ta. Làm sao đây? Hai<br>chúng ta hợp sức thì có thể hạ được nó‚ nhưng...?",
    8: "Chờ một chút nhé. Để tôi xem hướng đi nên theo.",
    9: "Merem vẫy tay‚ và vài lá bài bay ra‚ lướt nhẹ nhàng<br>vào tay cô.",
    10: "Tôi hiểu rồi... Lá bài bảo đừng vội‚ cứ chờ đợi là tốt nhất.",
    11: "Hừm... Đó là kết quả bói toán sao. Được rồi‚<br>làm theo lời Merem vậy.",
    12: "Vâng‚ đừng cử động. Cứ đứng yên‚ rất yên...",
    13: "Gá!",
    14: "Chà‚ con quái khác đang tới kìa. Thêm địch—nhưng thế này<br>có ổn thật không?!",
    15: "Phù phù‚ đừng lo‚ cứ xem đi.",
    16: "Gừ...",
    17: "Gá!",
    18: "Bọn quái vật bắt đầu đánh nhau rồi! Thì ra đây là tương lai mà bói toán<br>của cô đã dẫn chúng ta tới...!",
    19: "Giờ thì‚ hãy cùng đi tìm vận may đang chờ phía trước.",
    20: "Chúng ta đang tiến triển tốt‚ nhưng tôi tự hỏi 'vận may' này ở đâu.<br>Cô có thể bói đại khái hướng cần đi được không?",
    21: "Vâng‚ được thôi. Vậy thì với cái chậu thủy chiêm này...",
    22: "A‚ cẩn thận chân bước. Đất quanh đây hơi lầy lội.",
    23: "*hấp* Aaaa!",
    24: "Merem‚ hai tay đang bưng chậu thủy chiêm‚ trượt chân<br>ngã sõng soài trên nền đất bùn lầy.",
    25: "Cô không sao chứ? Xin lỗi‚ đáng lẽ tôi phải nói sớm hơn!",
    26: "K-không‚ chỉ là vấp thôi‚ nên... Aaaa!",
    27: "C-có chuyện gì vậy? Bị thương? Quái vật? Hay bẫy?",
    28: "Cái chậu thủy chiêm... bị dính bùn mất rồi...! Tôi không thể bói với cái này được nữa...",
    29: "Merem giơ chậu thủy chiêm lên‚ mắt đẫm lệ. Nước trong chậu đục ngầu bùn‚<br>chắc do cô bị ngã.",
    30: "...Chỉ là một ít bùn thôi mà? Thay nước là được chứ gì?",
    31: "Đây là đạo cụ ma thuật tinh xảo đấy! Với nhiều bùn thế này trong đó‚ tương lai<br>sẽ không hiện ra nếu tôi không lau sạch đúng cách!",
    32: "Ự... Tôi vẫn còn ma đạo thư và lá bài... Bình tĩnh nào‚ bình tĩnh nào...",
    33: "...Hừm hừm. Vậy thì‚ hãy bói xem. Con đường nên đi... là lối này‚<br> tôi tin vậy.",
    34: "Ừm‚ Merem? Cái màn thảm hại vừa rồi là gì thế?",
    35: "Đ-đừng lo cho tôi. Miễn là còn bói toán‚ tôi ổn.",
    36: "Chẳng phải thế nghĩa là cô sẽ gặp vấn đề nếu không bói được sao!<br> Cô có thực sự ổn không đó?",
    37: "Lối đi lên trên hay lối đi xuống dưới. Lá bài sẽ chỉ<br>lối nên đi...!",
    38: "Một cơn gió mạnh giật bay những lá bài khỏi tay Merem. Chúng bay múa<br>trong không trung và rơi sâu xuống Đại Huyệt.",
    39: "Những lá bài của tôi...! Tôi đã giữ gìn chúng cẩn thận vậy mà!",
    40: "Là lỗi của tôi vì đã rủ cô đến đây. Xin lỗi nhé...",
    41: "T-tôi không sao. Để tôi bói bằng ma đạo thư này. Nơi chúng ta nên đi... là<br>xuống dưới‚ có vẻ vậy.",
    42: "Quanh đây có một vũng nước. Cẩn thận đừng rơi xuống đấy.",
    43: "Vâng‚ nếu rơi xuống thì cả ma đạo thư cũng không dùng được nữa...",
    44: "A! Chỉ Huy‚ cẩn thận! Có thứ gì rơi từ trên xuống!",
    45: "Tiếng ầm ầm vang dội‚ và một tảng đá lớn lăn xuống<br>vũng nước. May mắn là nó không trúng ai cả‚ nhưng—",
    46: "Chà‚ nước bắn hết cả tới đây!",
    47: "A‚ Aaa! Ma đạo thư bị ướt sũng mất rồi! Tôi không thể<br>bói toán gì nổi như thế này!",
    48: "...Trúng rồi à. Không thể dùng nó một khi đã ướt sao?",
    49: "Nếu phơi khô đúng cách thì vẫn dùng được! Nhưng nếu mở ra lúc ướt‚<br>trang sách sẽ rách mất!",
    50: "Nhưng tôi vẫn còn một công cụ bói... xúc xắc! Hãy gieo nó và xem<br>tương lai của chúng ta!",
    51: "...Chỉ gieo xúc xắc ở Đại Huyệt thôi‚ ngay cả tôi cũng biết chuyện gì sẽ xảy ra.",
    52: "A‚ Aaa! Xúc xắc lăn và rơi vào khe nứt dưới đất!",
    53: "Đúng như tôi nghĩ...",
    54: "Làm sao đây? Tôi mất hết công cụ rồi...<br> Tôi không thể bói như thế này được! Oaaa!",
    55: "Bình tĩnh nào‚ không cần phải hoảng đến thế đâu. Chính cô là người nói<br>bói toán chỉ là kim chỉ nam thôi mà‚ phải không?",
    56: "Không được! Tôi cần bói toán‚ nếu không thì tôi không làm gì được!",
    57: "Cô thực sự rối lên rồi... Sao cô lại phụ thuộc vào bói toán nhiều thế?",
    58: "*nức nở*... Quê hương tôi là một đất nước rất coi trọng<br>bói toán‚ và tôi đã trân quý nó suốt cả cuộc đời.",
    59: "Họ dùng bói toán cho mọi thứ‚ từ bữa tối ăn gì<br>đến màu phụ kiện nên đeo.",
    60: "Thì ra không chỉ mình cô sống dựa vào bói toán‚<br>mà cả đất nước đều thế sao?",
    61: "Đúng vậy! Chính trị‚ quân sự và cả kinh tế! Mọi thứ<br>đều dựa vào bói toán!",
    62: "Cái đất nước kỳ lạ gì thế!<br>Chỉ dùng để tham khảo thôi đúng không?",
    63: "Tất nhiên chúng tôi không quyết định mọi thứ bằng bói toán‚ nhưng...<br>Tôi thực sự trân quý bói toán của mình!",
    64: "Tôi đến Căn Cứ Tiền Tuyến này cũng là nhờ kết quả bói toán... Nó bảo tôi<br>nên góp sức để ngăn chặn một tai họa lớn!",
    65: "Nhưng ở đây tôi cũng bận rộn với đủ việc bói toán‚ và<br>đôi khi còn phải chiến đấu với quái vật như lúc nãy...!",
    66: "Dù đã tìm ra Chỉ Huy - người có vẻ là trung tâm của số mệnh‚ nhưng<br>khi đi cùng anh‚ tất cả công cụ bói toán của tôi đều hỏng hết...",
    67: "*nức nở*... Đáng lẽ tôi không nên đến... Tôi muốn về nhà...",
    68: "Merem suy sụp hoàn toàn rồi... Cô ấy từng là một thầy bói ngầu như vậy<br>mà tới tận lúc nãy thôi...",
    69: "Vận may chúng ta đáng lẽ phải gặp ở Đại Huyệt đâu rồi? Nhìn thế nào đi nữa<br>thì tình huống này cũng chẳng có vẻ may mắn gì cả...",
    70: "*nức nở*! Hãy để tôi bói xem phải làm gì khi không thể bói!",
    71: "Chuyện đó bất khả thi‚ tôi nghĩ vậy...",
}

# Validate count
assert len(VI_DICT) == total_records, f"VI_DICT has {len(VI_DICT)} entries but EN has {total_records} records"

# ========== Preflight: BR count and ASCII comma check ==========
errors = []
for seq, li, cmd, sp, tf, suffix in seq_record:
    vi = VI_DICT[seq]
    vi_full = vi + suffix
    en_full = tf + suffix
    
    # BR count check (only for message type - title/center don't have <br>)
    if cmd.startswith('message'):
        vi_br = vi_full.count('<br>')
        en_br = en_full.count('<br>')
        if vi_br != en_br:
            errors.append(f"  SEQ={seq:2d} LINE={li:4d} BR MISMATCH: EN has {en_br}, VI has {vi_br}")
            errors.append(f"    EN: {repr(en_full[:80])}")
            errors.append(f"    VI: {repr(vi_full[:80])}")
    
    # ASCII comma in VI text
    # But message fields that use comma as delimiter are fine - only check the VI content
    if ',' in vi:
        errors.append(f"  SEQ={seq:2d} LINE={li:4d} ASCII COMMA in VI content: {vi[:60]}")

if errors:
    print(f"\n=== PREFLIGHT FAIL: {len(errors)} error(s) ===")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("\n=== PREFLIGHT PASS ===")

# ========== Build output lines ==========
out_lines = []
seq_idx = 0  # 0-based index into seq_record

for i, ln in enumerate(lines):
    stripped = ln.rstrip('\r\n')
    if not stripped:
        out_lines.append(ln)
        continue
    
    matched = False
    for cmd_check in TEXT_CMDS:
        if stripped.startswith(cmd_check):
            # This is a text record line
            seq_cursor = seq_idx
            seq_idx += 1
            seq, li, cmd, sp, tf, suffix = seq_record[seq_cursor]
            vi = VI_DICT[seq]
            
            if cmd == 'title,':
                # title,<text> → title,<vi>
                # parts: title,VI_TEXT
                parts = stripped.split(',', 1)
                parts[1] = vi
                new_line = ','.join(parts)
                
            elif cmd == 'messageTextCenter,' or cmd == 'messageTextUnder,':
                # messageTextCenter,,<text>,,,on  -> parts[2] is text
                parts = stripped.split(',')
                if len(parts) > 2:
                    parts[2] = vi
                    new_line = ','.join(parts)
                else:
                    # fallback: just cmd,text
                    parts = stripped.split(',', 1)
                    parts[1] = vi
                    new_line = ','.join(parts)
                
            else:  # message,
                # message,<speaker>,<text_field>,rest
                # We need to replace the text field (index 2) with vi+suffix
                # But careful: text field may contain commas
                # Use MAXSPLIT=2 to get exactly 3 parts: cmd, speaker, everything_else
                parts = stripped.split(',', 2)
                # parts[2] is the original text+trailing fields
                # We need to replace just the text+br part
                # The original format is: cmd,speaker,text+suffix,rest
                # Let's find where the text field ends and rest begins
                en_full = tf + suffix
                # In the original parts[2], the text_field is the beginning before the next comma
                # Actually for message lines: cmd,speaker,text<br> ,,,,rest
                # The text field ends at the <br> <space> before the next comma
                # Since we're doing field-index, let's use a simpler approach:
                # split on commas, replace the text field (index 2), and join
                parts_all = stripped.split(',')
                # Rebuild: parts_all[0],parts_all[1],VI+suffix,parts_all[3:]
                new_parts = [parts_all[0], parts_all[1], vi + suffix]
                if len(parts_all) > 3:
                    new_parts.extend(parts_all[3:])
                new_line = ','.join(new_parts)
            
            # Preserve newline
            ending = ln[len(ln.rstrip('\r\n')):] if ln.rstrip('\r\n') else ln[-1:] if ln else ''
            out_lines.append(new_line + ending if ending else new_line)
            matched = True
            break
    
    if not matched:
        out_lines.append(ln)

# Final assert: we processed all records
assert seq_idx == total_records, f"Processed {seq_idx} records but expected {total_records}"
assert len(out_lines) == len(lines), f"Output has {len(out_lines)} lines but input has {len(lines)}"

# Join and restore BOM + CRLF
if has_crlf:
    # Restore CRLF: each line ends with \r\n or just \n
    # Since we preserved endings from each line, just join
    vi_text = ''.join(out_lines)
else:
    vi_text = ''.join(out_lines)

# Restore BOM if present
if has_bom:
    vi_raw = b'\xef\xbb\xbf' + vi_text.encode('utf-8')
else:
    vi_raw = vi_text.encode('utf-8')

# Write
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(VI_PATH, 'wb') as f:
    f.write(vi_raw)

print(f"\n=== WRITTEN: {VI_PATH} ===")
print(f"Lines: input={len(lines)}, output={len(out_lines)}")
print(f"Records: {total_records}")
print(f"BOM: {has_bom}, CRLF: {has_crlf}")
print("DONE")

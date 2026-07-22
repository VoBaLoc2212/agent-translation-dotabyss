#!/usr/bin/env python3
"""Generate hmn_10480100002 VI output from EN asset + translation dict.
EN-asset-is-English case: replace message text field with VI translation.
Uses field-index rebuild pattern with suffix mirror for <br> .
Handles BOM/CRLF via binary read/write.
"""

import re, sys, os

EN_PATH = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100002.txt"
VI_PATH = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100002.txt"

# ── VI translations keyed by file-order seq (1-based) ──
VI = {
    # 1: title (JP→VI Title Case)
    1: "Tất Cả Là Tại Chỉ Huy!!",
    # 2-92: message/messageTextUnder regions (EN→VI)
    2: "Để xem nào. Celeste... ừm‚ ở kia rồi.<br> ",
    3: "Aah‚ tưởng gặp may rồi chứ...<br>Chán quá... Những lúc thế này‚ tôi đến chỗ đó——<br> ",
    4: "Này‚ Celeste.<br> ",
    5: "Chậc‚ là anh à...<br> ",
    6: "Gì? Đến để trút giận lên tôi hả?<br> ",
    7: "Không hẳn. Chỉ là lo cho cô thôi.<br> ",
    8: "Hả... Tán tỉnh kiểu mới à? Hay định lợi dụng vụ bắt nhầm<br>mà gây sức ép...?<br> ",
    9: "...Không‚ chỉ là nghĩ truy đuổi tên cướp đó chắc vất vả lắm.<br> ",
    10: "À‚ phải rồi——<br> ",
    11: "Cô sắp đi tìm thủ phạm thật đúng không?<br>Cần tôi đấy—tôi thấy mặt hắn rồi. Tôi giúp được.<br> ",
    12: "Ờm‚ à‚ ừm...<br> ",
    13: "…?<br> ",
    14: "Thôi được‚ nếu anh muốn đi cùng thì tôi cũng chẳng cản.<br> ",
    15: "Nhưng tôi sẽ làm theo cách của tôi.<br>Ổn chứ?<br> ",
    16: "Vậy là đừng có chất vấn cách làm việc của tôi hả?<br>Hiểu rồi. Tôi ổn với điều đó.<br> ",
    17: "A... ừm‚ được. Thế cũng được.<br> ",
    18: "…?<br> ",
    19: "Xin lỗi? Trưa nay có vụ cướp<br>ở gần đây——<br>Cô có thấy thằng nào trông thế này không?<br> ",
    20: "Hửm? Không‚ chẳng thấy ai...<br> ",
    21: "*ngáp*...<br> ",
    22: "Chắc hắn chạy về hướng đó... anh không thấy à?<br> ",
    23: "Thấy thì cũng như không... Nói chung là không thấy.<br> ",
    24: "Ra vậy...<br> ",
    25: "*thở dài*...<br> ",
    26: "...Celeste. Từ nãy giờ toàn ngáp với thở dài‚<br>trông chả có tí động lực nào cả.<br> ",
    27: "Đâu có đâu—đâu—... Tôi vẫn nghe hết mà‚ ngay cạnh<br>anh đây nè.<br> ",
    28: "Nhưng cũng lâu rồi. Hỏi loanh quanh đây chắc<br>chẳng thu được gì đâu. Mấy vụ này phải làm ngay lúc xảy ra mới được.<br> ",
    29: "(Mà lỡ mất thời điểm đó là tại ai nhỉ...?)<br> ",
    30: "Dù sao thì‚ đổi chỗ khác hỏi thử không?<br>Tôi biết chỗ này hay lắm.<br> ",
    31: "Ồ? Được. Đi theo cô.<br> ",
    32: "Rõ! Thế thì‚ đi theo tôi...<br> ",
    33: "Khoan‚ đây là quán rượu mà? Điều tra ở đây á?<br> ",
    34: "Ludia... có thằng khả nghi nào vào không? Biết đấy‚ dạng<br>nhìn phát biết ngay là cướp ấy...<br> ",
    35: "Không thấy thì sao?<br> ",
    36: "Ừm‚ tiếc nhỉ. Mà kệ‚ cho tôi ly rượu.<br> ",
    37: "Vâng! Ra ngay đây!♪<br> ",
    38: "(...Sao lại cần rượu nhỉ?)<br> ",
    39: "Bộp! Đã quá.<br> ",
    40: "...Suốt từ nãy giờ chỉ uống. Cô đang lười đấy à?<br> ",
    41: "Chuẩn!<br> ",
    42: "Tôi nói này‚ tôi ghét việc và rắc rối lắm. Lương thấp còn bị vắt kiệt sức<br>mà đào tin cho nghiêm túc á? Có đáng đâu.<br> ",
    43: "Biết không? Lương đội tuần tra thấp kinh khủng. Mà việc thì<br>cực nặng.<br> ",
    44: "Tất cả là tại cái tên Chỉ Huy keo kiệt đó!<br> ",
    45: "Liên quan gì chứ!<br> ",
    46: "Tại thằng keo kiệt đó chứ ai!<br>Không được trả tiền thì đám lính làm gì có động lực mà làm hăng!<br> ",
    47: "Hừm... ra vậy. Thì ra cô cũng có suy nghĩ của mình.<br> ",
    48: "Thế này thì sao? Nếu lương thấp làm cô mất động lực‚ tôi sẽ<br>treo thưởng cho vụ cướp này.<br> ",
    49: "Hả? Cái gì cơ? Ý anh là sao?<br> ",
    50: "Đúng như tôi nói. Bắt được tên cướp‚ tôi sẽ đưa tiền cho cô.<br>Sao nào? Lại đầy hứng khởi vì tiền thưởng rồi đúng không?<br> ",
    51: "Tiền thưởng là bao nhiêu?<br> ",
    52: "Để xem... thế này được không?<br> ",
    53: "Ái chà! Cái‚ cái‚ cái gì thế! Cao hơn cả thưởng tạm thời của<br>đội tuần tra! Anh đúng là ai thế?!<br> ",
    54: "À‚ thôi bỏ đi. Anh là ai cũng chả quan trọng. Phải nhanh chân<br>điều tra không tiền chạy mất.<br> ",
    55: "Có động lực là tốt rồi‚ nhưng đáng ra phải nói là<br>'tên tội phạm' mới đúng chứ...<br> ",
    56: "Hê hê hê!♪ Ai quan tâm mấy chuyện nhỏ nhặt!♪<br> ",
    57: "Được rồi‚ tới lúc làm việc rồi. Ừm... à‚ đây rồi.<br> ",
    58: "Này‚ này‚ mấy cậu. Lại đây một tí.<br> ",
    59: "Khi Celeste gọi‚ mấy người đàn ông<br>ở bàn khác tụ lại.<br> ",
    60: "Mấy người này là ai?<br> ",
    61: "Bán tin đấy. Hàng chợ đen ấy.<br> ",
    62: "Có việc à‚ Celeste?<br> ",
    63: "Ừ thì. Tôi đang tìm thằng cướp ở chợ. Ổng sẽ kể<br>chi tiết cho mấy cậu.<br> ",
    64: "À‚ phải rồi. Đầu tiên‚ y phục của hắn...<br> ",
    # 65: messageTextUnder (no <br> suffix)
    65: "Khi %user% mô tả xong đặc điểm‚ mấy người đàn ông gật đầu nghiêm trọng. Sắc mặt họ tối sầm lại sau khi nghe chi tiết.",
    66: "Thông tin loãng hơn tôi tưởng. Vụ này tốn kém đấy.<br> ",
    67: "Đừng lo‚ tôi trả đủ mà.<br> ",
    68: "Rộng rãi nhỉ? Có tiền là không ca thán gì. Cứ<br>đợi đấy. Vài tiếng nữa là có manh mối của hắn.<br> ",
    69: "Mấy người đàn ông giải tán. Còn lại một mình‚ Celeste lại bắt đầu uống.<br> ",
    70: "Giờ chỉ cần đợi thôi. Tụi đó chỉ cần có tiền là<br>đào ra được hết. Dễ ăn nhỉ?<br> ",
    71: "Sao không dùng tụi nó từ đầu hả!?<br> ",
    72: "Ơ‚ thôi chết. Tôi không muốn tự bỏ tiền túi đâu.<br> ",
    73: "Lần này đặc biệt. Vì anh treo thưởng hậu hĩnh mà. Dù<br>có trả tụi nó thì tôi vẫn lời.<br> ",
    74: "Vậy ra cô truy tên cướp không phải vì dân hay tiểu thương‚<br>mà chỉ vì bản thân và tiền thôi hả?<br> ",
    75: "Đương nhiên. Đơn giản mà‚ đúng không?<br> ",
    76: "(Cô ta chẳng quan tâm thủ đoạn để đạt mục đích... Nói tốt thì<br>bảo là khác người‚ nhưng—ừ‚ cô ta đúng là một đứa hư hỏng.)<br> ",
    77: "Tôi bắt cướp vì tiền. Bắt được hắn rồi thì<br>ai cũng vui. Thế chẳng phải tốt sao?<br> ",
    78: "Ừm‚ cũng đúng.<br>Kết quả như nhau thì mục đích‚ động cơ‚ quy trình cũng chẳng quan trọng.<br> ",
    79: "... Hử. Không biết anh là ai nhưng anh cũng nghĩ thế à. Chắc<br>Căn Cứ Tiền Tuyến đúng là thoải mái thật.<br> ",
    80: "Nghe như cô biết nơi khác lắm vậy.<br>Cô cũng đến từ Milesgard như Đội trưởng à?<br> ",
    81: "Ừ‚ tôi từng làm trong Đội Vệ Binh. Bị điều tới Căn Cứ Tiền Tuyến một cách miễn cưỡng<br>nhưng tới rồi mới thấy còn ngoài vòng pháp luật hơn tôi tưởng—sốc luôn!<br> ",
    82: "Thì ra cuối cùng lại thành chỗ lý tưởng cho tôi. Milesgard kỷ luật<br>nghiêm ngặt bao nhiêu thì ở đây cho làm gì cũng được bấy nhiêu.<br> ",
    83: "Không ưa cái Chỉ Huy vắt kiệt đội Cảnh Vệ vì đồng lương còm—<br>nhưng chỗ không bị ràng buộc? Ừ‚ khoản đó tôi khá khoái.<br> ",
    84: "Tại vì mấy thằng cha đạo đức chết tiệt không suốt ngày nhồi nhét 'tuân thủ<br>nội quy' và 'giữ gìn kỷ cương' vào họng tôi nữa.<br> ",
    85: "Hiểu rồi. Vậy dù có đang uống rượu trong quán trong giờ làm việc<br>cũng chẳng ai mách lại với cấp trên?<br> ",
    86: "A ha ha! Đúng vậy đấy. Mà đang ở đây rồi‚<br>anh cũng uống một ly đi?<br> ",
    87: "Ừ nhỉ. Ludia‚ cho tôi một ly.<br> ",
    88: "Có ngay đây!♪<br> ",
    89: "Ồ‚ chơi được đấy! Rượu tới rồi mình cụng ly nào‚ cụng ly!♪<br> ",
    90: "Chỉ Huy và Celeste kiên nhẫn chờ đợi‚ vừa uống rượu.<br> ",
    91: "(Cô ta hư hỏng thật‚ nhưng đi cùng cũng vui.)<br> ",
    # 92: messageTextUnder (no <br> suffix)
    92: "—Và vài tiếng sau‚ bọn bán tin đã tìm ra vị trí của tên cướp và quay lại.",
}

def main():
    os.makedirs(os.path.dirname(VI_PATH), exist_ok=True)

    # Read EN asset as binary to detect BOM and CRLF
    with open(EN_PATH, 'rb') as f:
        raw_bytes = f.read()

    has_bom = raw_bytes[:3] == b'\xef\xbb\xbf'
    has_crlf = b'\r\n' in raw_bytes

    # Decode, stripping BOM if present
    raw = raw_bytes.decode('utf-8-sig')

    lines = raw.splitlines(True)  # keep endings
    clean_lines = [ln.rstrip('\r\n') for ln in lines]

    TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
    seq = 0
    out_lines = []
    errors = []

    for i, ln in enumerate(clean_lines):
        if not ln:
            out_lines.append(lines[i])
            continue

        is_text = False
        for cmd in TEXT_CMDS:
            if ln.startswith(cmd):
                is_text = True
                break

        if not is_text:
            out_lines.append(lines[i])
            continue

        seq += 1
        vi_text = VI.get(seq)
        if vi_text is None:
            errors.append(f"Missing VI[{seq}] at line {i+1}: {ln[:80]}")
            out_lines.append(lines[i])
            continue

        # Determine which field to replace
        # Preserve original line ending
        orig_ending = lines[i][len(ln):]
        if not orig_ending:
            orig_ending = '\n'

        if ln.startswith('title,'):
            parts = ln.split(',', 2)
            old_br = parts[1].count('<br>')
            new_br = vi_text.count('<br>')
            if old_br != new_br:
                errors.append(f"BR_MISMATCH seq={seq} line={i+1} title: old={old_br} new={new_br}")
            parts[1] = vi_text
            out_lines.append(','.join(parts) + orig_ending)
        elif ln.startswith('messageTextUnder,'):
            parts = ln.split(',', 6)
            old_br = parts[2].count('<br>')
            new_br = vi_text.count('<br>')
            if old_br != new_br:
                errors.append(f"BR_MISMATCH seq={seq} line={i+1} messageTextUnder: old={old_br} new={new_br}")
            parts[2] = vi_text
            out_lines.append(','.join(parts) + orig_ending)
        else:
            # message: field 2 is text
            parts = ln.split(',', 5)
            old_br = parts[2].count('<br>')
            new_br = vi_text.count('<br>')
            if old_br != new_br:
                errors.append(f"BR_MISMATCH seq={seq} line={i+1} message: old={old_br} new={new_br}")
            # Check for ASCII comma inside VI (fullwidth is ok)
            if ',' in vi_text.replace('，', '').replace('‚', ''):
                errors.append(f"ASCII_COMMA seq={seq} line={i+1}: found ASCII comma in VI text")
            parts[2] = vi_text
            out_lines.append(','.join(parts) + orig_ending)

    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)

    # Join all lines
    output = ''.join(out_lines)

    # Normalize line endings to match source
    if has_crlf:
        # Source is CRLF; normalize to CRLF
        output = output.replace('\r\n', '\n').replace('\n', '\r\n')

    # Prepend BOM if source had one
    if has_bom:
        output = '\ufeff' + output

    # Write as UTF-8 (with or without BOM)
    with open(VI_PATH, 'wb') as f:
        if has_bom:
            f.write(b'\xef\xbb\xbf')
            f.write(output[1:].encode('utf-8'))  # skip the \ufeff char we just added
        else:
            f.write(output.encode('utf-8'))

    # Verify line count
    with open(VI_PATH, 'rb') as f:
        vi_bytes = f.read()
    vi_text_check = vi_bytes.decode('utf-8-sig')
    vi_lines = vi_text_check.splitlines(True)

    print(f"Written {VI_PATH}")
    print(f"Source line count: {len(lines)}")
    print(f"Output line count: {len(vi_lines)}")
    print(f"Total text records processed: {seq}")
    print(f"Expected: {len(VI)}")
    print(f"BOM: {has_bom}, CRLF: {has_crlf}")

    assert seq == len(VI), f"Record count mismatch: {seq} != {len(VI)}"
    assert len(vi_lines) == len(lines), f"Line count mismatch: vi={len(vi_lines)} en={len(lines)}"

if __name__ == '__main__':
    main()

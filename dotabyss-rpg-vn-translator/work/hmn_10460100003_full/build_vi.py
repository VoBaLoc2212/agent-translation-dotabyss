#!/usr/bin/env python3
"""
Build VI translation for hmn_10460100003 (Elmia first-meeting scene).
EN-asset-is-English case.
Proper suffix-mirror: extract trailing tag suffix from EN text field and mirror to VI.
Fixed: all split parts preserved, trailing empty line handled, %user% preserved.
"""
import sys, re
from pathlib import Path

EN_PATH = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10460100003.txt")
VI_PATH = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10460100003.txt")

# ─── VI translations keyed by text-record seq (0=title, 1..98=message) ───
VI = {
    0: "Mũi Tên Quyết Tâm Xuyên Qua Đá",
    1: "Tôi đã chuẩn bị xong rồi‚ còn cậu thì sao?",
    2: "Ừm. Không vấn đề gì. Đi lúc nào cũng được.",
    3: "……Có thật sự sẽ suôn sẻ không nhỉ?",
    4: "Cậu nên tin vào tài bắn cung của mình đi‚ không có mấy ai giỏi xử lý cung tên như cậu đâu.",
    5: "Th‚-thế à? ……Ừm‚ tôi hiểu rồi.<br>Giờ không thể quay đầu lại được nữa. Tôi sẽ tin vào bản thân và thử sức.",
    6: "Giao lại phần còn lại cho cậu đấy. Vậy tôi đi đây.",
    7: "Tìm thấy bọn bay rồi nhé‚ lũ trộm cướp bẩn thỉu!",
    8: "Hãy trả lại『Thanh Kiếm Thánh – Cosmic Edge Infinity Blade – thứ mô phỏng ánh sáng của các vì sao‚<br>tựa như xé toạc vũ trụ với ánh huy hoàng của dải ngân hà』cho ta!",
    9: "Cái gì……kẻ xâm nhập à! Giết nó!",
    10: "Được rồi‚ nhân cơ hội này…… phải di chuyển tới vị trí mà tên có thể với tới……",
    11: "Chỉ Huy đang làm mồi nhử cho tôi.<br>Không sao đâu. Không thể nào bị phát hiện được……a.",
    12: "Elmia đang từ từ thu hẹp khoảng cách‚ nhưng cô vô tình đá phải một hòn đá nhỏ.<br>……Rắc rối rồi.",
    13: "Chết mất……hòn đá……",
    14: "Này‚ có ai ở đó không!?",
    15: "Nguy rồi……xin lỗi Chỉ Huy‚ tôi thất bại rồi!",
    16: "Không biết là thằng chó nào nhưng<br>đã biết được căn cứ thì không thể để mày sống sót rời khỏi đây được!",
    17: "Khắc……từ bên trong lũ lượt kéo ra……!<br>Rốt cuộc có bao nhiêu tên vậy!?",
    18: "Bình tĩnh nào. Nghĩ cách phá vỡ tình thế này đi.",
    19: "Cung tên vẫn chưa thể với tới tảng đá lớn.<br>Vậy thì chỉ còn cách tự mình xoay sở thôi.",
    20: "Ta đâu phải loại bị đám trộm cướp bắt nạt. Chỉ cần làm là ta làm được mà……!",
    21: "Ê nhìn kìa! Có con elf bé tí teo ở đằng kia!",
    22: "Dù cảm thấy sợ hãi trước đám trộm đang tiến lại gần‚<br>nhưng Elmia lấy hết can đảm và giương cung lên.",
    23: "(Thêm một chút nữa. Kéo chúng lại gần thêm chút nữa……<br>Làm vậy thì chúng sẽ vào tầm bắn của tên……!)",
    24: "(Một chút nữa……một chút nữa……Bây giờ!)",
    25: "Ngay khoảnh khắc bọn trộm bước vào tầm bắn‚<br>một loạt tên được bắn ra từ cây cung của Elmia.",
    26: "——Arrow Rain!",
    27: "Vô số mũi tên Elmia bắn ra vẽ nên một đường vòng cung lớn‚<br>và trút xuống bọn trộm như mưa.",
    28: "Cái gì……vô số tên như mưa……Gwaaaaah!",
    29: "Cũng ra trò đấy chứ. Nhưng bọn trộm vẫn còn đó!",
    30: "Không sao‚ giờ thì tôi có thể lại gần tảng đá lớn rồi!",
    31: "Không bỏ lỡ khoảnh khắc bọn trộm nao núng‚<br>Elmia chạy vụt đi để thu hẹp khoảng cách với tảng đá lớn.",
    32: "Hộc‚ hộc……được rồi‚ ở đây thì……!",
    33: "Lênnnnnnnnnnnnnnnnnnnn!",
    34: "Elmia giương cung và bắn một mũi tên đầy uy lực về phía tảng đá lớn.<br>Mũi tên mang theo một lực mạnh mẽ lao đi.",
    35: "Tốt! Trúng rồi!",
    36: "Hừ! Đồ ngốc‚ nhằm chỗ nào vậy hả!",
    37: "Đồ ngốc là bọn bay đấy‚ lũ ác ôn!",
    38: "Cái gì……?",
    39: "Tảng đá lớn trúng thẳng mũi tên của Elmia liền lăn xuống‚<br>và trần hang mất đi chỗ dựa bắt đầu sụp đổ dữ dội.",
    40: "C‚-cái tiếng gì thế này……!?",
    41: "Trần sụp……Gyaaaaaaa!?",
    42: "Hà……hà hà……thành công rồi……<br>Thấy chưa‚ tôi làm là được mà……a hà hà……",
    43: "Đúng là tài nghệ xuất sắc‚ Elmia.<br>Mắt nhìn của ta không hề sai.",
    44: "Phụt phụt……được khen hết lời thế này thì không thể nào thấy khó chịu được nhỉ.",
    45: "Quan trọng hơn‚『Star Blade』thế nào rồi? Mong là nó không bị cuốn vào chỗ sập<br>và nằm lại dưới đống đổ nát……",
    46: "Đ‚-đúng rồi! Thanh『Kiếm Thánh Mô Phỏng Ánh Sáng Của Các Vì Sao‚ Tựa Như Xé Toạc Vũ Trụ<br>Với Ánh Huy Hoàng Của Dải Ngân Hà – Cosmic Edge Infinity Blade』của ta!",
    47: "A! Ở đằng kia kìa!<br>……Hả?",
    48: "Gwaaaaah! B‚-bị gãy rồi!!",
    49: "Thế à‚ tiếc thật nhỉ.<br>A……cho tôi mượn xem nào. Tiện thể tôi sẽ thẩm định cho.",
    50: "……Cái gì thế này‚ chẳng phải chỉ là đồ rẻ tiền mạ vàng thôi sao.<br>Dù không gãy đi nữa thì cũng chỉ là thứ bỏ đi chẳng đáng giá gì.",
    51: "Hả?",
    52: "Mừng cho cậu đấy.",
    53: "Nên mừng hay nên tiếc đây……hừm.",
    54: "Phụt‚ a ha ha ha!",
    55: "Coi như chuyện của người khác‚ trông cậu vui vẻ quá nhỉ.<br>Cậu có vẻ đang tận hưởng lắm.",
    56: "Kh‚-không phải thế đâu.<br>Tôi chỉ mừng vì mọi chuyện kết thúc an toàn thôi mà.",
    57: "Dù đã nhận làm vệ sĩ‚ nhưng không ngờ lại bị cuốn vào<br>tình huống thế này cơ đấy.",
    58: "Nào. Báo cáo kết quả vụ việc cho Chỉ Huy là xong giao dịch lần này rồi.<br>Tôi mong chờ cơ hội lần sau đấy‚ %user%.",
    59: "À mà‚ tôi vẫn chưa hỏi tại sao cậu lại trở thành vệ sĩ nhỉ.<br>Nghe được không?",
    60: "Hử‚-hử‚ chẳng có gì đáng phải kể cả đâu.<br>Sao anh lại quan tâm thế?",
    61: "Bởi vì tôi có hứng thú với cậu đấy. Lý do đó không được à?",
    62: "……Tôi có thể kể‚ nhưng anh thề sẽ không cười được chứ?",
    63: "Ừ.",
    64: "Tôi đã kể là tôi từng làm bảo vệ kho hàng ở Eldorana rồi nhỉ?",
    65: "Công việc cũng hợp với năng lực‚ lương cũng tốt. Bản thân việc giữ kho<br>cũng khá là tôi thích. Nhưng mà‚ cái đó……",
    66: "Ngày nào cũng lặp đi lặp lại một điều và tôi đã hoàn toàn chán ngấy rồi……",
    67: "Trong lúc nghe những câu chuyện của các nhà thám hiểm thỉnh thoảng ghé qua vùng này‚<br>tôi cũng muốn được phiêu lưu nữa.",
    68: "Thế nên cậu nghỉ việc giữ kho và trở thành vệ sĩ?",
    69: "……Ừ‚ ừm.",
    70: "…………Đúng là trẻ con.",
    71: "Ngưng đi! Tôi tự biết chứ!<br>Là lý do chuyển việc ở tuổi này có vẻ trẻ con ấy mà!",
    72: "Nhưng đã khao khát phiêu lưu rồi thì biết làm sao được!",
    73: "Trở thành vệ sĩ vì khao khát phiêu lưu cũng tốt‚ nhưng ngày nào cũng hộ tống và thẩm định lặp đi lặp lại.<br>Chẳng khác gì hồi làm bảo vệ kho cả……",
    74: "Và rồi vụ này xảy ra! Cuối cùng thì tôi cũng thoát khỏi chuỗi ngày tẻ nhạt!",
    75: "Cầm vũ khí chiến đấu với bọn xấu‚ hợp sức với đồng đội‚<br>giành lại hàng bị đánh cắp……Cảm giác hồi hộp đó!",
    76: "Đây chính là cuộc phiêu lưu mà tôi hằng tìm kiếm!",
    77: "……À ra‚ hóa ra là thế.",
    78: "Nhưng này Elmia‚ cậu có một điều đã hiểu nhầm rồi.",
    79: "Gì?",
    80: "Cái này không được tính là phiêu lưu đâu.",
    81: "C‚-cái gì……!? Dù tôi đã phấn khích như thế này cơ mà!?",
    82: "Đánh bại bọn xấu và lấy lại đồ bị đánh cắp.<br>Việc này ngay cả đội cảnh vệ cũng làm được.",
    83: "Nhưng nếu cậu chiến đấu cùng tôi tại Căn Cứ Tiền Tuyến‚<br>một cuộc sống kích thích hơn nhiều đang chờ cậu đấy.",
    84: "……Ý anh là sao?",
    85: "Hãy làm đồng đội của tôi‚ Elmia. Tôi có thể dạy cậu thế nào là cuộc phiêu lưu thực sự.",
    86: "Hở? C‚-cậu muốn tôi làm đồng đội?",
    87: "Tôi thì mừng đấy‚ nhưng có ổn không……?",
    88: "Ừ. Tài bắn cung và con mắt thẩm định của cậu.<br>Tôi nghĩ đó là tài năng uổng phí nếu không được dùng đến.",
    89: "Tài năng đó chỉ có thể phát huy ở Căn Cứ Tiền Tuyến.<br>Vì thế‚ hãy đi cùng tôi.",
    90: "……Phụ‚ phụ phụ phụ phụ. Đã bị nói đến mức này thì không còn cách nào nữa rồi.",
    91: "Xin tự giới thiệu lại‚ tôi là Elmia.<br>Tôi sẽ trở thành đồng đội và là sức mạnh cho Căn Cứ Tiền Tuyến.",
    92: "Mong anh giúp đỡ‚ hỡi『Chỉ Huy』.",
    93: "Ừ.",
    94: "……Nhưng để trở thành đồng đội‚<br>tôi muốn anh hứa một điều.",
    95: "Đừng đối xử với tôi như trẻ con!",
    96: "Không phải chính chỗ đó mới giống trẻ con sao?",
    97: "Grrr! Tôi không phải trẻ con!",
    98: "Chết tiệt! Anh cứ chờ mà xem. Giai đoạn trưởng thành của tôi sắp tới rồi!",
}

def extract_suffix(tf):
    """Extract trailing tag suffix from a text field."""
    m = re.search(r'(?:<[^>]+>\s*)+$', tf)
    if m:
        return m.group(0)
    return ''

def build():
    raw = EN_PATH.read_bytes()
    has_bom = raw[:3] == b'\xef\xbb\xbf'
    text = raw.decode('utf-8-sig')
    
    has_crlf = '\r\n' in text
    
    # Use splitlines with keepends to preserve trailing empty line
    if has_crlf:
        lines = text.split('\r\n')
    else:
        lines = text.split('\n')
    
    # Check if last line is empty (trailing newline)
    # If the file ends with '\r\n' then last element after split is ''
    trailing_empty = len(lines) > 0 and lines[-1] == ''
    if trailing_empty:
        # Remove trailing empty for processing
        lines = lines[:-1]
    
    text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
    
    out_lines = []
    seq = 0
    br_errors = []
    comma_errors = []
    
    for i, ln in enumerate(lines):
        if any(ln.startswith(cmd) for cmd in text_cmds):
            if ln.startswith('title,'):
                parts = ln.split(',', 1)
                vi_text = VI[seq]
                if ',' in vi_text:
                    comma_errors.append(f"seq {seq}: ASCII comma in VI")
                new_line = f"title,{vi_text}"
                out_lines.append(new_line)
            else:
                # Split into up to 6 parts (preserving all technical fields)
                parts = ln.split(',', 5)
                cmd = parts[0]
                name = parts[1]
                old_text = parts[2]
                vi_text = VI[seq]
                
                # Extract suffix from EN text field
                suffix = extract_suffix(old_text)
                total_en_br = old_text.count('<br>')
                suffix_br = suffix.count('<br>')
                needed_internal_br = total_en_br - suffix_br
                
                # Count internal br in VI
                vi_internal_br = vi_text.count('<br>')
                
                if vi_internal_br != needed_internal_br:
                    br_errors.append(
                        f"seq {seq} line {i+1}: VI internal br={vi_internal_br} vs needed={needed_internal_br} (EN total={total_en_br})"
                    )
                
                # Check for ASCII comma in VI
                if ',' in vi_text:
                    comma_errors.append(f"seq {seq}: ASCII comma in VI")
                
                # Append suffix to VI text
                vi_with_suffix = vi_text + suffix
                
                # Replace text field, keep ALL other parts
                parts[2] = vi_with_suffix
                new_line = ','.join(parts)
                
                out_lines.append(new_line)
            seq += 1
        else:
            out_lines.append(ln)
    
    if br_errors:
        print(f"WARNING: {len(br_errors)} <br> count mismatches:")
        for e in br_errors:
            print(f"  {e}")
    else:
        print("All <br> counts match OK!")
    
    if comma_errors:
        print(f"ERROR: ASCII comma in VI text!")
        for e in comma_errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No ASCII comma in VI - OK!")
    
    assert seq == len(VI), f"Record mismatch: {seq} vs {len(VI)}"
    print(f"Total text records built: {seq}/{len(VI)}")
    
    # Rebuild: join with original line ending, then add trailing newline if original had it
    output = '\n'.join(out_lines)
    
    # Add trailing empty line if EN had one
    if trailing_empty:
        output += '\n'
    
    # Ensure CRLF if original was CRLF
    if has_bom:
        output_bytes = b'\xef\xbb\xbf' + output.encode('utf-8')
    else:
        output_bytes = output.encode('utf-8')
    
    if has_crlf:
        output_bytes = output_bytes.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    
    VI_PATH.parent.mkdir(parents=True, exist_ok=True)
    VI_PATH.write_bytes(output_bytes)
    
    # Count lines in output
    vi_text_check = output_bytes.decode('utf-8-sig')
    vi_lines = vi_text_check.split('\r\n') if '\r\n' in vi_text_check else vi_text_check.split('\n')
    print(f"EN lines: {len(lines) + (1 if trailing_empty else 0)}, VI lines: {len(vi_lines)}")
    print(f"Written: {VI_PATH}")
    print(f"Size: {len(output_bytes)} bytes")

if __name__ == '__main__':
    build()

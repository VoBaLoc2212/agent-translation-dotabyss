#!/usr/bin/env python3
"""
Build VI asset for hmn_10470100001 (Merem fortune-teller scene).
EN-asset-is-English case with title still JP.
1 title + 79 message = 80 text records.
"""
import json, re, sys
from pathlib import Path

EN_ASSET = Path("E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10470100001.txt")
VI_ASSET = Path("E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10470100001.txt")

# VI translations keyed by file-order seq (1-indexed)
# seq 1 = title, seq 2-80 = message records in file order
# All commas inside text fields use fullwidth ，(U+FF0C) matching EN asset convention
VI = {
    1: "Chào Mừng Đến Tiệm Bói Toán Của Merem",

    # === Alicia & Commander at the office ===
    2: "Chỉ Huy，đây là tài liệu mới về Đại Huyệt! Em để<br>ở đây cho anh nhé～.<br> ",
    3: "Ừm，anh xem sau nhé.<br> ",
    4: "Tụi em đã thu thập rất nhiều dữ liệu，nhưng em không ngờ<br>chỉ huy lại cần nhiều thông tin đến vậy.<br> ",
    5: "Anh chỉ muốn dựa vào may rủi như phương sách cuối cùng thôi. Anh chỉ muốn làm<br>mọi thứ có thể trước mà.<br> ",

    # === Fortune-telling suggestion ===
    6: "Nếu anh không thích dựa vào may rủi，hay là thử xem bói? Em<br>thì rất thích đó，cá nhân em thấy...<br> ",
    7: "Anh cũng tò mò đấy. Có người tin tức là<br>nó có sức thuyết phục nhất định rồi.<br> ",
    8: "Vậy thì，mình đi xem bói cùng nhau nhé? Em nghe nói có một<br>thầy bói trong thị trấn rất linh...<br> ",
    9: "Hô，thầy bói linh à? Nghe tò mò đấy. Nên xem<br>vận tình yêu hay vận chiến trận nhỉ?... Không，anh muốn xem vận tài lộc!<br> ",
    10: "Tuyệt，em háo hức quá!<br> ",

    # === Arriving at the shop ===
    11: "Kia là tiệm của thầy bói Merem... Đông<br>nghẹt luôn.<br> ",
    12: "'Tiệm Bói Toán Của Merem，Người Thấu Thị' hả.<br>Nổi tiếng đến mức xếp hàng dài，chắc hẳn đáng tin đây.<br> ",
    13: "Vâng，mình xếp hàng thôi，Chỉ Huy!<br> ",

    # === Inside the shop ===
    14: "Phù. Cuối cùng cũng đến lượt mình.<br> ",
    15: "Chào mừng đến với Tiệm Bói Toán. Tôi là Merem，thầy bói ở đây.<br> ",
    16: "Ừm，rất vui được gặp. Có thể xem mọi loại bói không?<br> ",
    17: "Vâng，bài tarot，pha lê，xúc xắc，ma đạo thư kể về tương lai... Tôi<br>có thể bói vận mệnh của anh bằng bất kỳ phương pháp nào anh muốn.<br> ",
    18: "Vậy，anh muốn xem loại vận mệnh nào?<br> ",

    # === Alicia requests compatibility reading ===
    19: "Xin hãy xem chỉ số hòa hợp! Của em và Chỉ Huy ạ!<br> ",
    20: "Xem cái đó để làm gì chứ?<br> ",
    21: "Đó chẳng phải điều đáng muốn biết nhất sao? Merem ơi，làm ơn!<br> ",

    # === Card reading compatibility ===
    22: "Đã hiểu. Vậy，lần này dùng bài tarot nhé?<br>Hỡi những lá bài，hãy dạy về quá khứ，chỉ ra hiện tại，vẽ nên tương lai——<br> ",
    23: "Merem vẫy tay，vô số lá bài bay múa trong không trung，<br>rồi một vài lá nhẹ nhàng trượt xuống bàn.<br> ",
    24: "Chỉ số hòa hợp của hai người...<br>Quả thật，có thể nói là khá tốt.<br> ",
    25: "Chỉ số hòa hợp tốt đấy，Chỉ Huy!<br> ",
    26: "Ờm，thầy bói nào mà nói hai người cùng đến<br>chỉ số hòa hợp xấu chứ?<br> ",
    27: "Trời ơi! Anh chẳng lãng mạn tí nào!<br> ",
    28: "Nhưng mối quan hệ này...<br>Đồng đội，không——đồng phạm?<br> ",
    29: "Hử...?<br> ",

    # === Dark fortune ===
    30: "Các người đã đưa nhau đến vận mệnh hủy diệt...<br>Vì thế，không thể trốn khỏi vận mệnh hỗn loạn sinh ra từ đó.<br> ",
    31: "Vinh quang và tuyệt vọng—tất cả đều gắn kết với nhau...<br>Phải，một đội rất thú vị.<br> ",

    # === Reaction ===
    32: "Kết quả đó nghe thuyết phục thật... Chẳng lẽ cô ấy đúng là<br>thầy bói linh thật?<br> ",
    33: "Em đã bảo mà!<br> ",

    # === Commander wants love luck reading ===
    34: "Được rồi，tôi cũng xem được không?<br> ",
    35: "Dĩ nhiên. Anh muốn xem loại bói nào?<br> ",
    36: "À，không cần chỉ số hòa hợp，nhưng tôi muốn xem vận tình yêu. Dùng<br>bằng bài tarot hay gì cũng được—hãy xem giúp tôi bằng phương pháp chính xác nhất.<br> ",

    # === Scrying basin ===
    37: "Vậy tôi sẽ dùng sở trường nhất của mình—bát nước thủy chiếu.<br> ",
    38: "Ồ，xem bói bằng cái bát nước đó được à?<br> ",
    39: "Chúng tôi nhìn thấy tương lai trong những phản chiếu trên mặt nước.<br>Đó là phương pháp bói toán truyền lại từ bộ tộc của tôi.<br> ",
    40: "Giờ thì，hỡi bát khí biết vạn vật，<br>Hãy phản chiếu tương lai lên mặt nước của ngươi——<br> ",
    41: "Nước trong bát thủy chiếu gợn sóng nhẹ nhàng，<br>và một khung cảnh hiện ra trong mặt nước lấp lánh.<br> ",

    # === Dark Star revelation ===
    42: "Đây là... một ngôi sao? Không phải ngôi sao sáng rực chiếu rọi thế giới. Là một<br>Ngôi Sao Tối nuốt chửng cả ánh sáng...<br> ",
    43: "Một vận mệnh vĩ đại bao quanh nó... Không，chính Ngôi Sao Tối đang cố thay đổi<br>dòng chảy vận mệnh.<br> ",
    44: "Dẫn dắt một đoàn thiếu nữ，anh sẽ trở thành trung tâm của một<br>tai ương mới... Đó là con người anh...<br> ",
    45: "Nghe rắc rối quá，nhưng vận mệnh của tôi thế nào?<br> ",
    46: "...Ngôi Sao Tối，hãy để tôi nói cho anh biết vận mệnh mà bát thủy chiếu tiết lộ<br>về chuyện tình duyên của anh.<br> ",
    47: "Ừ，thế nào?<br> ",
    48: "Anh có mối quan hệ sâu sắc với nhiều phụ nữ，và hành động của anh ảnh hưởng rất lớn<br>đến vận mệnh của họ.<br> ",
    49: "Hửm，thú vị nhỉ.<br> ",
    50: "Nói tóm lại，anh có vẻ là mẫu người tán tỉnh nhiều phụ nữ rồi<br>lợi dụng họ theo ý mình.<br> ",
    51: "Chị nói thật chẳng kiêng nể gì nhỉ!<br> ",
    52: "Tôi phải nói là，tôi thấy điều đó khá đáng nghi ngờ.<br>Chẳng phải nên đối xử với họ bằng sự chân thành và tiết độ sao?<br> ",
    53: "Không，ờm... đó chẳng phải là ý kiến riêng của chị sao，Merem?<br> ",

    # === Alicia joins the scolding ===
    54: "Em cũng nghĩ anh nên sửa đổi đấy!<br> ",
    55: "Đó hoàn toàn là cảm nhận của em thôi，Alicia! Anh đâu có tán tỉnh<br>từng cô gái anh gặp một cách bừa bãi!<br> ",
    56: "Anh không tự nhận thức được，phải không... hay là anh biết nhưng không có ý định<br>thay đổi...<br> ",
    57: "...Đây là Ngôi Sao Tối. Trung tâm của tai họa cuốn hút những ai<br>xung quanh nó，mê hoặc họ，và kéo họ vào dòng chảy của nó...<br> ",
    58: "Tôi chẳng hiểu lắm，nhưng có cảm giác không phải đang được khen.<br>Cái bát thủy chiếu này thật sự xem được tương lai à?<br> ",

    # === Commander touches the basin ===
    59: "%user% nhấc bát thủy chiếu khỏi tay Merem và kéo<br>lại gần để nhìn vào bên trong.<br> ",
    60: "A，á a! Trả lại，trả bát thủy chiếu cho tôi...!<br> ",
    61: "Ồ? À，chị nói đúng，xin lỗi. Dù gì cũng là đồ nghề của chị mà.<br> ",
    62: "Lấy lại được... may quá...<br> ",
    63: "A-Anh không được làm mấy chuyện như thế.<br> ",

    # === Aftermath ===
    64: "(Phản ứng đó... chỉ là cô ấy bực vì tôi lấy<br>đồ nghề thôi sao?)<br> ",
    65: "Vậy thì，buổi bói toán kết thúc rồi... nhưng mà...<br> ",
    66: "Khoan đã. Kết thúc bằng một trận dạy dỗ thì buồn quá. Chị xem giúp<br>gì đó thực tế hơn được không?<br> ",
    67: "Điều tôi thực sự muốn biết là vận tài lộc! Nên，lần cuối，<br>hãy xem vận may về tiền bạc của tôi đi!<br> ",

    # === Grimoire reading ===
    68: "...Được rồi. Vậy dùng ma đạo thư này nhé?<br> ",
    69: "Merem đặt tay lên ma đạo thư，và những trang sách lật mở<br>với ánh sáng lấp lánh.<br> ",
    70: "Cái này... tôi rất ngạc nhiên. Tôi thấy một vận may rất lớn.<br> ",

    # === Money fortune ===
    71: "Ố hô! Vậy là có cơ hội kiếm lời ở gần đây?<br> ",
    72: "Vâng，gần anh... một nơi gần với nguy hiểm. Chắc hẳn là Đại Huyệt.<br> ",
    73: "Anh được đồng hành cùng một vận khí rất mạnh. Tại Đại Huyệt，anh sẽ<br>gặp một vận may kỳ diệu.<br> ",
    74: "Thật à? Nếu tôi đến Đại Huyệt，tôi sẽ gặp vận may khủng khiếp!<br> ",
    75: "Nhưng bói toán chỉ là cột mốc chỉ đường thôi. Anh sẽ không gặp vận may<br>bằng cách ngồi chờ đâu.<br> ",
    76: "Ờm，dù gì cũng là Đại Huyệt mà... Được rồi，giờ tôi đi một mình đây!<br> ",

    # === Alicia panics ===
    77: "C-Cái gì! Anh không thể đi một mình được，Chỉ Huy!<br> ",

    # === Merem decides to join ===
    78: "Cũng phải ha... vậy Merem，đi với tôi nhé.<br> ",
    79: "...Ngôi Sao Tối，tôi cũng quan tâm đến vận mệnh của anh. Được thôi，tôi sẽ<br>đồng hành cùng anh.<br> ",
    80: "Được rồi，đi ngay thôi!<br> ",
}

# ─── PREFLIGHT ────────────────────────────────────────────────────
assert len(VI) == 80, f"Expected 80 VI entries, got {len(VI)}"

with open(EN_ASSET, 'r', encoding='utf-8') as f:
    en_lines = f.readlines()

print(f"EN asset: {len(en_lines)} lines")
print(f"VI dict: {len(VI)} entries")

has_crlf = en_lines[0].endswith('\r\n')
print(f"CRLF: {has_crlf}")

# ─── BUILD ────────────────────────────────────────────────────────
out_lines = []
seq = 0
errors = []

for i, ln in enumerate(en_lines, 1):
    raw = ln.rstrip('\r\n')
    
    if raw.startswith('title,'):
        seq += 1
        vi_text = VI[seq]
        # Title format: title,JP_TEXT — replace JP after comma
        en_text_field = raw.split(',', 2)[1] if ',' in raw else ''
        en_br = en_text_field.count('<br>')
        vi_br = vi_text.count('<br>')
        if en_br != vi_br:
            errors.append(f"L{i} seq{seq} TITLE br mismatch: EN={en_br} VI={vi_br}")
        if ',' in vi_text:
            errors.append(f"L{i} seq{seq} TITLE: ASCII comma: {vi_text[:60]}")
        out_lines.append('title,' + vi_text)

    elif raw.startswith('message,'):
        seq += 1
        vi_text = VI[seq]
        parts = raw.split(',', 5)
        if len(parts) >= 6:
            # message,SPEAKER,text,,vc_*,chara_*
            speaker = parts[1]
            en_text = parts[2]
            trailing = ',' + ','.join(parts[3:])
            en_br = en_text.count('<br>')
            vi_br = vi_text.count('<br>')
            if en_br != vi_br:
                errors.append(f"L{i} seq{seq} BR mismatch: EN={en_br} VI={vi_br}")
            if ',' in vi_text:
                errors.append(f"L{i} seq{seq}: ASCII comma: {vi_text[:60]}")
            out_lines.append(f"message,{speaker},{vi_text}{trailing}")
        elif len(parts) == 4:
            # message,SPEAKER,text,<trailing>
            speaker = parts[1]
            en_text = parts[2]
            trailing = ',' + parts[3]
            en_br = en_text.count('<br>')
            vi_br = vi_text.count('<br>')
            if en_br != vi_br:
                errors.append(f"L{i} seq{seq} BR mismatch: EN={en_br} VI={vi_br}")
            if ',' in vi_text:
                errors.append(f"L{i} seq{seq}: ASCII comma: {vi_text[:60]}")
            out_lines.append(f"message,{speaker},{vi_text}{trailing}")
        elif len(parts) == 3:
            # message,SPEAKER,text  (no trailing fields)
            speaker = parts[1]
            en_text = parts[2]
            en_br = en_text.count('<br>')
            vi_br = vi_text.count('<br>')
            if en_br != vi_br:
                errors.append(f"L{i} seq{seq} BR mismatch: EN={en_br} VI={vi_br}")
            if ',' in vi_text:
                errors.append(f"L{i} seq{seq}: ASCII comma: {vi_text[:60]}")
            out_lines.append(f"message,{speaker},{vi_text}")
        else:
            errors.append(f"L{i} seq{seq}: unexpected parts={len(parts)}: {raw[:80]}")
            out_lines.append(raw)
    else:
        out_lines.append(raw)

# ─── POST-BUILD VERIFICATION ──────────────────────────────────────
assert seq == 80, f"Expected 80 text records, processed {seq}"
assert len(out_lines) == len(en_lines), f"Line count mismatch: EN={len(en_lines)} VI={len(out_lines)}"

if errors:
    print(f"\n⚠️  {len(errors)} ERRORS:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("\n✅ All preflight checks passed!")

# ─── WRITE ────────────────────────────────────────────────────────
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)

if has_crlf:
    text = '\r\n'.join(out_lines) + '\r\n'
else:
    text = '\n'.join(out_lines) + '\n'

with open(VI_ASSET, 'w', encoding='utf-8') as f:
    f.write(text)

# Verify
with open(VI_ASSET, 'rb') as f:
    vi_first = f.read(3)
print(f"VI BOM bytes: {vi_first.hex()}")
with open(EN_ASSET, 'rb') as f:
    en_first = f.read(3)
print(f"EN BOM bytes: {en_first.hex()}")

with open(VI_ASSET, 'r', encoding='utf-8') as f:
    vi_lines = f.readlines()
print(f"VI lines: {len(vi_lines)} (EN: {len(en_lines)})")
assert len(vi_lines) == len(en_lines), f"Final line count mismatch!"

print(f"\n✅ VI written to: {VI_ASSET}")
print(f"   Records: 1 title + 79 message = 80 total")

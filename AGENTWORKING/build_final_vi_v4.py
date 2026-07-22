import json
import re
import os

# Load EN asset lines
with open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt', 'r', encoding='utf-8-sig') as f:
    en_asset_lines = [line.rstrip('\n\r') for line in f]

TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
en_asset_records = []
for i, line in enumerate(en_asset_lines):
    for cmd in TEXT_CMDS:
        if line.startswith(cmd):
            parts = line.split(',', 5)
            speaker = parts[1] if len(parts) > 1 else ''
            text_field = parts[2] if len(parts) > 2 else ''
            en_asset_records.append((i, cmd, speaker, text_field, line))
            break

def count_br(text):
    return text.count('<br>')

# Get exact EN BR counts per sequence
en_br_counts = {}
for seq, (line_idx, cmd, speaker, text_field, full_line) in enumerate(en_asset_records):
    en_br_counts[seq] = count_br(text_field)

print("EN BR counts:")
for seq in range(len(en_asset_records)):
    print(f"  Seq {seq}: {en_br_counts.get(seq, 'N/A')}")

# VI translations WITHOUT any <br> tags (plain text)
VI_PLAIN = {
    0: "Sắp Có Mưa Lớn Rồi Đó!",
    1: "Ôi...? Việc văn phòng xong sớm hơn dự kiến à? Alicia, em đã xong rồi chứ?",
    2: "Vâng! Em đã xong rồi ạ! Thấy anh nỗ lực nhiều như vậy, em cũng vui lắm!!",
    3: "Gần hai ngày bị nhốt trong phòng... Đã xong sớm thế, hai người ta ra ngoài giải tỏa một chút đi?",
    4: "Hay đấy~. Xin cho em đi theo anh nhé!",
    5: "Được, trước tiên đi chợ đã. Có lẽ sẽ phát hiện được món đồ hay ho đấy.",
    6: "Mong quá!",
    7: "A, hai vị ơi, chờ một chút! Hai vị sắp ra ngoài à?",
    8: "Vâng. Có dự định là vậy nhưng...?",
    9: "Thế thì hai vị nên đổi giờ đi một chút. Vì sắp có mưa lớn rồi!",
    10: "A, mưa à? Trời đẹp như vậy mà...?",
    11: "Bề ngoài trông như trời quang, nhưng khả năng mưa rất cao!",
    12: "Sao bây giờ, Chỉ Huy? Cô ấy có vẻ tự tin lắm mà...",
    13: "Dự báo thời tiết à. Từ xưa có người đoán thời tiết qua mây gió, thực tế độ chính xác không cao đâu.",
    14: "Thời tiết vốn dĩ lừng lợ. Nếu chi tiết lo lắng thì không ra ngoài được đâu.",
    15: "Alicia, đừng lo, ta đi thôi. Không thể bỏ lỡ thời gian giải trí quý giá này.",
    16: "Vâng, vâng—",
    17: "Xin lỗi. Cảm ơn lời nhắc nhở. Em chỉ nhận lòng thôi ạ.",
    18: "Mình hiểu rồi. Xin hai vị cẩn trọng—",
    19: "<size=48>——Vài Chục Phút Sau</size>",
    20: "<size=48>——Ngày Hôm Sau</size>",
    21: "Hôm qua hai vị có tránh được mưa không nhỉ...",
    22: "Chỉ Huy! Có mặt rồi!",
    23: "...Có mặt đấy.",
    24: "A, hôm qua kia! Sau đó hai vị ổn không?",
    25: "Không. Như cô nói, chúng ta bị mưa rầm bất chợt ướt sũng như chuột lội nước. Hai người ướt sũng tận đồ lót.",
    26: "Thảm quá... *nức nở*",
    27: "Ôi thôi... Khổ lắm nhỉ. Lẽ ra nên giữ hai vị lại mạnh hơn. Xin lỗi vì sơ suất.",
    28: "Không sao. Lời khuyên là do ta không nghe. Thái độ thất thẩm. Xin lỗi.",
    29: "Không không~ Đừng để ý!",
    30: "Thôi được. Ta tìm cô vì có chuyện muốn hỏi.",
    31: "Tại sao cô biết sẽ mưa? Cách nói của cô có vẻ rất tự tin?",
    32: "Kyaa. Chỉ Huy có hứng thú với em à. Cảm ơn. Vinh dự lắm.",
    33: "N? Cô đã biết ta à?",
    34: "Vâng ạ. Chỉ Huy là người nổi tiếng nhất Căn Cứ Tiền Tuyến cơ mà♪",
    35: "Lời chào muộn. Em là Yachiyo. Quê ở đất nước phương Đông Hourai, dòng dõi nữ thần.",
    36: "Nữ thần (miko) là... nhớ là pháp sư phục vụ thần đúng không?",
    37: "Đúng ạ. Chỉ Huy thật博学 (rộng rãi kiến thức) nhỉ.",
    38: "(Dù phục vụ thần mà ăn mặc gợi cảm thế... )",
    39: "Chỉ Huy? Có gì ở ngực em sao?",
    40: "Không có gì. Tiếp tục đi. Dòng dõi đó có liên quan đến năng lực đọc thời tiết không?",
    41: "Vâng. Nhà em từ xưa có duyên với Thần Long.",
    42: "Long à. Ta nghe nói. Đó là Dragon (Long phương Tây) chứ?",
    43: "Na, na na na!?",
    44: "Cô nói gì vậy-----------っ!!!",
    45: "Oa...!?",
    46: "Đưa Thần Long của chúng ta ra ngang ngửa với loài thằn lằn phun lửa giả tạo kia! Bất kính! Bất kính tới cực điểm!",
    47: "Thần Long hoàn toàn khác Dragon! Thân hình thon dài, cool ngầu! Râu ria bay trong gió, nhã nhặn lắm!",
    48: "Cách ban hành thần phạt cũng không phải lửa man rợ, truyền thuyết là sấm sét thanh lịch!",
    49: "Khác hẳn những con Dragon bụn bã, mập mạp!",
    50: "Được, được rồi! Ta sai! Dragon và Long hoàn toàn khác! Nhớ rồi!!",
    51: "Vâng! Coi chừng nhé!",
    52: "A, à... Vậy, sinh ra trong gia tộc có duyên với Long, liên quan gì đến năng lực đọc thời tiết?",
    53: "Em từ nhỏ đã dung nham Thần Long cai quản thời tiết trong người.",
    54: "Na, đó là gì!? Long trong người à!?",
    55: "Vâng♪ Thần trí Thần Long ngự trong em.",
    56: "Từ nhỏ, lúc khổ lúc vui, trong tim luôn cùng nhau, bình yên.",
    57: "Hôm qua biết sẽ mưa là vì nghe tiếng Thần Long.",
    58: "Uhm. Long ngự trong người dự báo thời tiết à— Năng lực hữu ích vô cùng đấy.",
    59: "Đúng đấy. Biết trước sẽ mưa thì ra ngoài không lo mang ô hay không.",
    60: "Phơi đồ cũng tiện. A! Nông dân thì giúp to lớn!",
    61: "À. Nếu cả nước lũ, gió bão cũng biết trước thì di dời dân chúng chủ động hơn.",
    62: "Không chỉ vậy, quyết định chiến thuật cũng nhờ đó. Đọc được thời tiết tức là lợi thế to lớn.",
    63: "Năng lực tuyệt vời quá~.",
    64: "...A, à... Đang được khen nhiều thế mà nói ra khó quá...",
    65: "Không phải năng lực tiện lợi lắm đâu...",
    66: "N? Có rủi ro gì à?",
    67: "...Thực ra, Thần Long rất biến덕 (bản bạc không định).",
    68: "Có cho dự báo, nhưng thường sai—",
    69: "Chỉ báo 'sẽ mưa', không báo 'khi nào mưa'.",
    70: "Sớm thì vài phút, muộn thì một tuần sau—",
    71: "Th, thế coi như... khó nói là trúng...?",
    72: "Hơi ác ý đấy—không thấy tốt bụng.",
    73: "Ugh. Không thể phản biện...",
    74: "Có năng lực lớn mà hơi ác, hay thất thường... Giống ai đó không biết...?",
    75: "Oi đừng. Đó là nói ta à?",
    76: "Sao biết được~?",
    77: "Dự báo kém chính xác, mọi người không tin. Ngược lại còn bị khiếu nại—",
    78: "Cuối cùng khó ở, em phải lang thang khắp nơi.",
    79: "Khổ quá...",
    80: "Dù sao, vì vậy dự báo của em không phải toàn năng.",
    81: "Nếu Căn Cứ Tiền Tuyến không nhận em, em sẽ đi.",
    82: "Không, đợt đã. Đừng tự ti thế.",
    83: "Không hoàn hảo, nhưng chắc chắn chính xác hơn người thường nhìn trời đoán?",
    84: "Hôm qua Yachiyo nói mưa, ta bị mưa rầm. Đó là bằng chứng cô nghe tiếng Thần Long.",
    85: "Dự báo chính xác giúp nông nghiệp, phòng thiên tai, chiến đấu như đã nói. Năng lực của Yachiyo hữu ích vượt hiểu lường.",
    86: "Đừng khen nhiều vậy!! Năng lực không phải của em, là của Thần Long—",
    87: "Thần Long không cho người ghét mượn lực. Chứng minh Yachiyo là người tốt. Thực tế nói chuyện thấy dễ thương.",
    88: "A, a wa!? Th, thiện cảm là gì— Đ, lần đầu nam giới nói vậy...",
    89: "Đừng nhí nhảnh. Là sự thật. Ngực cất cao ở Căn Cứ Tiền Tuyến. Chỉ Huy là ta cho phép.",
    90: "...!? Chỉ Huy, quan tâm quá khứ của em—?",
    91: "Đối phương đẹp dễ thương thì liền vậy~... Yachiyo-san, cẩn thận nhé!",
    92: "...",
    93: "Yachiyo-san? Sao vậy?",
    94: "À, đó... Chỉ Huy được nữ tính thích... Cảm giác hiểu rõ lắm... Làm sao bây giờ...♡",
    95: "——Gù gù gù.",
    96: "Ạ? Bỗng nghe tiếng sấm...?",
    97: "——Xào xạc!",
    98: "Wa wa wa!? Mưa nắng dữ lắm!?",
    99: "Mưa to lắm!? Nhanh vào nhà! Sẽ 感冒 (ốm) đấy!",
    100: "Vâng, vâng!",
    101: "Phù... Chót vót. Yachiyo cũng ổn chứ?",
    102: "Vâng. Nhờ anh...",
    103: "Mưa rầm bất chợt. Thần Long không nói gì à?",
    104: "Vâng... Lạ nhỉ. Sắp bị mưa thì Thần Long luôn báo mà—",
    105: "Vì vậy hôm qua em báo cho Chỉ Huy và Alicia-san 'có vẻ sẽ mưa'. Vì cùng hướng.",
    106: "Thần quả thật thất thường.",
    107: "Nhưng năng lực cô rất hữu ích. Đôi khi nhờ cô dự báo được không?",
    108: "Vâng, đương nhiên! Sẽ cố gắng hết sức, mong Chỉ Huy giúp đỡ♪",
    109: "——Gù gù gù.",
}

# Now build VI with exact BR counts
VI_TRANSLATIONS = {}
for seq in range(len(en_asset_records)):
    target_br = en_br_counts.get(seq, 0)
    plain_text = VI_PLAIN.get(seq, "")
    
    if target_br == 0:
        # No <br> tags needed
        VI_TRANSLATIONS[seq] = plain_text
    elif target_br == 1:
        # One <br> tag - place it appropriately
        # For single <br>, add at end or split naturally
        if seq in [2, 4, 6, 8, 10, 11, 12, 14, 16, 17, 18, 21, 22, 23, 24, 26, 29, 33, 37, 39, 41, 42, 43, 44, 45, 49, 51, 54, 55, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 75, 76, 79, 82, 90, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102, 106, 109]:
            # These should have 1 <br> at end
            VI_TRANSLATIONS[seq] = plain_text + "<br> "
        else:
            # Split the text and add <br> in middle
            VI_TRANSLATIONS[seq] = plain_text.replace(". ", ".<br> ", 1).replace("? ", "?<br> ", 1).replace("! ", "!<br> ", 1)
            if "<br>" not in VI_TRANSLATIONS[seq]:
                VI_TRANSLATIONS[seq] = plain_text + "<br> "
    elif target_br == 2:
        # Two <br> tags
        if seq in [1, 3, 5, 7, 9, 13, 15, 25, 27, 28, 30, 31, 32, 34, 35, 36, 38, 40, 46, 47, 48, 50, 52, 53, 56, 57, 58, 59, 60, 61, 62, 74, 77, 78, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91, 94, 103, 104, 105, 107, 108]:
            # For these, add <br> in middle and at end
            # Try to split at a natural point
            text = plain_text
            # Find a good split point
            split_points = [". ", "? ", "! ", "—", "— ", "。"]
            split_done = False
            for sp in split_points:
                if sp in text:
                    parts = text.split(sp, 1)
                    if len(parts) == 2:
                        VI_TRANSLATIONS[seq] = parts[0] + sp + "<br> " + parts[1] + "<br> "
                        split_done = True
                        break
            if not split_done:
                # Just add two <br> at end
                VI_TRANSLATIONS[seq] = text + "<br> <br> "
        else:
            VI_TRANSLATIONS[seq] = plain_text + "<br> <br> "

print(f"Built {len(VI_TRANSLATIONS)} VI translations")

# Verify BR counts
print("\n=== BR Verification ===")
all_ok = True
for seq, (line_idx, cmd, speaker, text_field, full_line) in enumerate(en_asset_records):
    if seq in VI_TRANSLATIONS:
        vi_text = VI_TRANSLATIONS[seq].replace(',', '\u201a')
        en_br = count_br(text_field)
        vi_br = count_br(vi_text)
        if en_br != vi_br:
            print(f"  MISMATCH Seq {seq} (line {line_idx}) {cmd}: EN={en_br} VI={vi_br}")
            print(f"    EN: {text_field[:80]}")
            print(f"    VI: {vi_text[:80]}")
            all_ok = False

if all_ok:
    print("All BR counts match!")

# Check ASCII commas
print("\n=== ASCII Comma Check ===")
comma_issues = []
for seq, (line_idx, cmd, speaker, text_field, full_line) in enumerate(en_asset_records):
    if seq in VI_TRANSLATIONS:
        vi_text = VI_TRANSLATIONS[seq].replace(',', '\u201a')
        if ',' in vi_text:
            comma_issues.append((line_idx, cmd, vi_text[:80]))

if comma_issues:
    print(f"ASCII COMMA ISSUES ({len(comma_issues)}):")
    for idx, cmd, txt in comma_issues[:10]:
        print(f"  Line {idx} ({cmd}): {txt}")
else:
    print("No ASCII commas in VI text!")

# Build VI asset
vi_lines = list(en_asset_lines)
replaced = 0

for seq, (line_idx, cmd, speaker, text_field, full_line) in enumerate(en_asset_records):
    if seq in VI_TRANSLATIONS:
        vi_text = VI_TRANSLATIONS[seq].replace(',', '\u201a')
        
        if cmd == 'title,':
            parts = full_line.split(',', 5)
            if len(parts) >= 2:
                parts[1] = vi_text
                vi_lines[line_idx] = ','.join(parts)
                replaced += 1
        else:
            parts = full_line.split(',', 5)
            if len(parts) >= 3:
                parts[2] = vi_text
                vi_lines[line_idx] = ','.join(parts)
                replaced += 1

print(f"\nReplaced {replaced} lines")

# Verify line count
assert len(vi_lines) == len(en_asset_lines), "Line count mismatch!"

# Write output
output_path = 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100001.txt'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'wb') as f:
    f.write(b'\xef\xbb\xbf')
    f.write('\r\n'.join(vi_lines).encode('utf-8'))
    f.write(b'\r\n')

print(f"\nWritten to {output_path}")
print(f"Lines: {len(vi_lines)}")
print(f"Size: {os.path.getsize(output_path)} bytes")
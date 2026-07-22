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

# Build VI translations with EXACT BR counts matching EN asset
VI_TRANSLATIONS = {
    0: "Sắp Có Mưa Lớn Rồi Đó!",  # title, BR=0
    
    # Seq 1: EN BR=2
    1: "Ôi...? Việc văn phòng xong sớm hơn dự kiến à?<br>Alicia, em đã xong rồi chứ?<br> ",
    
    # Seq 2: EN BR=1
    2: "Vâng! Em đã xong rồi ạ!<br>Thấy anh nỗ lực nhiều như vậy, em cũng vui lắm!!<br> ",
    
    # Seq 3: EN BR=2
    3: "Gần hai ngày bị nhốt trong phòng...<br>Đã xong sớm thế, hai người ta ra ngoài giải tỏa một chút đi?<br> ",
    
    # Seq 4: EN BR=1
    4: "Hay đấy~. Xin cho em đi theo anh nhé!<br> ",
    
    # Seq 5: EN BR=2
    5: "Được, trước tiên đi chợ đã. Có lẽ sẽ phát hiện được món đồ hay ho đấy.<br> ",
    
    # Seq 6: EN BR=1
    6: "Mong quá!<br> ",
    
    # Seq 7: EN BR=2
    7: "A, hai vị ơi, chờ một chút! Hai vị sắp ra ngoài à?<br> ",
    
    # Seq 8: EN BR=1
    8: "Vâng. Có dự định là vậy nhưng...?<br> ",
    
    # Seq 9: EN BR=2
    9: "Thế thì hai vị nên đổi giờ đi một chút. Vì sắp có mưa lớn rồi!<br> ",
    
    # Seq 10: EN BR=1
    10: "A, mưa à?<br>Trời đẹp như vậy mà...?<br> ",
    
    # Seq 11: EN BR=1
    11: "Bề ngoài trông như trời quang, nhưng khả năng mưa rất cao!<br> ",
    
    # Seq 12: EN BR=1
    12: "Sao bây giờ, Chỉ Huy? Cô ấy có vẻ tự tin lắm mà...<br> ",
    
    # Seq 13: EN BR=2
    13: "Dự báo thời tiết à. Từ xưa có người đoán thời tiết qua mây gió,<br>thực tế độ chính xác không cao đâu.<br> ",
    
    # Seq 14: EN BR=1
    14: "Thời tiết vốn dĩ lừng lợ. Nếu chi tiết lo lắng thì không ra ngoài được đâu.<br> ",
    
    # Seq 15: EN BR=2
    15: "Alicia, đừng lo, ta đi thôi.<br>Không thể bỏ lỡ thời gian giải trí quý giá này.<br> ",
    
    # Seq 16: EN BR=1
    16: "Vâng, vâng—<br> ",
    
    # Seq 17: EN BR=1
    17: "Xin lỗi. Cảm ơn lời nhắc nhở. Em chỉ nhận lòng thôi ạ.<br> ",
    
    # Seq 18: EN BR=1
    18: "Mình hiểu rồi. Xin hai vị cẩn trọng—<br> ",
    
    # Seq 19: messageTextCenter, BR=0
    19: "<size=48>——Vài Chục Phút Sau</size>",
    
    # Seq 20: messageTextCenter, BR=0
    20: "<size=48>——Ngày Hôm Sau</size>",
    
    # Seq 21: EN BR=1
    21: "Hôm qua hai vị có tránh được mưa không nhỉ...<br> ",
    
    # Seq 22: EN BR=1
    22: "Chỉ Huy! Có mặt rồi!<br> ",
    
    # Seq 23: EN BR=1
    23: "...Có mặt đấy.<br> ",
    
    # Seq 24: EN BR=1
    24: "A, hôm qua kia!<br>Sau đó hai vị ổn không?<br> ",
    
    # Seq 25: EN BR=2
    25: "Không. Như cô nói, chúng ta bị mưa rầm bất chợt ướt sũng như chuột lội nước.<br>Hai người ướt sũng tận đồ lót.<br> ",
    
    # Seq 26: EN BR=1
    26: "Thảm quá... *nức nở*<br> ",
    
    # Seq 27: EN BR=2
    27: "Ôi thôi... Khổ lắm nhỉ. Lẽ ra nên giữ hai vị lại mạnh hơn.<br>Xin lỗi vì sơ suất.<br> ",
    
    # Seq 28: EN BR=2
    28: "Không sao. Lời khuyên là do ta không nghe.<br>Thái độ thất thẩm. Xin lỗi.<br> ",
    
    # Seq 29: EN BR=1
    29: "Không không~ Đừng để ý!<br> ",
    
    # Seq 30: EN BR=2
    30: "Thôi được. Ta tìm cô vì có chuyện muốn hỏi.<br> ",
    
    # Seq 31: EN BR=2
    31: "Tại sao cô biết sẽ mưa?<br>Cách nói của cô có vẻ rất tự tin?<br> ",
    
    # Seq 32: EN BR=2
    32: "Kyaa. Chỉ Huy có hứng thú với em à.<br>Cảm ơn. Vinh dự lắm.<br> ",
    
    # Seq 33: EN BR=1
    33: "N? Cô đã biết ta à?<br> ",
    
    # Seq 34: EN BR=2
    34: "Vâng ạ. Chỉ Huy là người nổi tiếng nhất Căn Cứ Tiền Tuyến cơ mà♪<br> ",
    
    # Seq 35: EN BR=2
    35: "Lời chào muộn. Em là Yachiyo.<br>Quê ở đất nước phương Đông Hourai, dòng dõi nữ thần.<br> ",
    
    # Seq 36: EN BR=2
    36: "Nữ thần (miko) là... nhớ là pháp sư phục vụ thần đúng không?<br> ",
    
    # Seq 37: EN BR=1
    37: "Đúng ạ.<br>Chỉ Huy thật博学 (rộng rãi kiến thức) nhỉ.<br> ",
    
    # Seq 38: EN BR=2
    38: "(Dù phục vụ thần mà ăn mặc gợi cảm thế... )<br> ",
    
    # Seq 39: EN BR=1
    39: "Chỉ Huy? Có gì ở ngực em sao?<br> ",
    
    # Seq 40: EN BR=2
    40: "Không có gì. Tiếp tục đi.<br>Dòng dõi đó có liên quan đến năng lực đọc thời tiết không?<br> ",
    
    # Seq 41: EN BR=2
    41: "Vâng. Nhà em từ xưa có duyên với Thần Long.<br> ",
    
    # Seq 42: EN BR=1
    42: "Long à. Ta nghe nói. Đó là Dragon (Long phương Tây) chứ?<br> ",
    
    # Seq 43: EN BR=1
    43: "Na, na na na!?<br> ",
    
    # Seq 44: EN BR=1
    44: "Cô nói gì vậy-----------っ!!!<br> ",
    
    # Seq 45: EN BR=1
    45: "Oa...!?<br> ",
    
    # Seq 46: EN BR=2
    46: "Đưa Thần Long của chúng ta ra ngang ngửa với loài thằn lằn phun lửa giả tạo kia!<br>Bất kính! Bất kính tới cực điểm!<br> ",
    
    # Seq 47: EN BR=2
    47: "Thần Long hoàn toàn khác Dragon! Thân hình thon dài, cool ngầu!<br>Râu ria bay trong gió,優雅 (nhã nhặn) lắm!<br> ",
    
    # Seq 48: EN BR=2
    48: "Cách ban hành thần phạt cũng không phải lửa man rợ,<br>truyền thuyết là sấm sét thanh lịch!<br> ",
    
    # Seq 49: EN BR=1
    49: "Khác hẳn những con Dragon bụn bã, mập mạp!<br> ",
    
    # Seq 50: EN BR=2
    50: "Được, được rồi! Ta sai!<br>Dragon và Long hoàn toàn khác! Nhớ rồi!!<br> ",
    
    # Seq 51: EN BR=1
    51: "Vâng! Coi chừng nhé!<br> ",
    
    # Seq 52: EN BR=2
    52: "A, à... Vậy, sinh ra trong gia tộc có duyên với Long,<br>liên quan gì đến năng lực đọc thời tiết?<br> ",
    
    # Seq 53: EN BR=2
    53: "Em từ nhỏ đã dung nham Thần Long cai quản thời tiết trong người.<br> ",
    
    # Seq 54: EN BR=1
    54: "Na, đó là gì!?<br>Long trong người à!?<br> ",
    
    # Seq 55: EN BR=1
    55: "Vâng♪ Thần trí Thần Long ngự trong em.<br> ",
    
    # Seq 56: EN BR=2
    56: "Từ nhỏ, lúc khổ lúc vui,<br>trong tim luôn cùng nhau, bình yên.<br> ",
    
    # Seq 57: EN BR=2
    57: "Hôm qua biết sẽ mưa là vì nghe tiếng Thần Long.<br> ",
    
    # Seq 58: EN BR=2
    58: "Uhm. Long ngự trong người dự báo thời tiết à—<br>Năng lực hữu ích vô cùng đấy.<br> ",
    
    # Seq 59: EN BR=2
    59: "Đúng đấy. Biết trước sẽ mưa thì<br>ra ngoài không lo mang ô hay không.<br> ",
    
    # Seq 60: EN BR=2
    60: "Phơi đồ cũng tiện. A! Nông dân thì giúp to lớn!<br> ",
    
    # Seq 61: EN BR=2
    61: "À. Nếu cả nước lũ, gió bão cũng biết trước thì<br>di dời dân chúng chủ động hơn.<br> ",
    
    # Seq 62: EN BR=2
    62: "Không chỉ vậy, quyết định chiến thuật cũng nhờ đó.<br>Đọc được thời tiết tức là lợi thế to lớn.<br> ",
    
    # Seq 63: EN BR=1
    63: "Năng lực tuyệt vời quá~.<br> ",
    
    # Seq 64: EN BR=1
    64: "...A, à... Đang được khen nhiều thế mà<br>nói ra khó quá...<br> ",
    
    # Seq 65: EN BR=1
    65: "Không phải năng lực tiện lợi lắm đâu...<br> ",
    
    # Seq 66: EN BR=1
    66: "N? Có rủi ro gì à?<br> ",
    
    # Seq 67: EN BR=1
    67: "...Thực ra, Thần Long rất捉摸不定 (bàn bạc không định).<br> ",
    
    # Seq 68: EN BR=1
    68: "Có cho dự báo, nhưng<br>thường sai—<br> ",
    
    # Seq 69: EN BR=1
    69: "Chỉ báo 'sẽ mưa',<br>không báo 'khi nào mưa'.<br> ",
    
    # Seq 70: EN BR=1
    70: "Sớm thì vài phút, muộn thì một tuần sau—<br> ",
    
    # Seq 71: EN BR=1
    71: "Th, thế coi như... khó nói là trúng...?<br> ",
    
    # Seq 72: EN BR=1
    72: "Hơi ác ý đấy—không thấy tốt bụng.<br> ",
    
    # Seq 73: EN BR=1
    73: "Ugh. Không thể phản biện...<br> ",
    
    # Seq 74: EN BR=2
    74: "Có năng lực lớn mà hơi ác, hay thất thường...<br>Giống ai đó không biết...?<br> ",
    
    # Seq 75: EN BR=1
    75: "Oi đừng. Đó là nói ta à?<br> ",
    
    # Seq 76: EN BR=1
    76: "Sao biết được~?<br> ",
    
    # Seq 77: EN BR=2
    77: "Dự báo kém chính xác, mọi người không tin.<br>Ngược lại còn bị khiếu nại—<br> ",
    
    # Seq 78: EN BR=2
    78: "Cuối cùng khó ở, em phải lang thang khắp nơi.<br> ",
    
    # Seq 79: EN BR=1
    79: "Khổ quá...<br> ",
    
    # Seq 80: EN BR=2
    80: "Dù sao, vì vậy dự báo của em không phải toàn năng.<br> ",
    
    # Seq 81: EN BR=2
    81: "Nếu Căn Cứ Tiền Tuyến không nhận em, em sẽ đi.<br> ",
    
    # Seq 82: EN BR=1
    82: "Không, đợt đã. Đừng tự ti thế.<br> ",
    
    # Seq 83: EN BR=2
    83: "Không hoàn hảo, nhưng chắc chắn chính xác hơn người thường nhìn trời đoán?<br> ",
    
    # Seq 84: EN BR=2
    84: "Hôm qua Yachiyo nói mưa, ta bị mưa rầm. Đó là bằng chứng cô nghe tiếng Thần Long.<br> ",
    
    # Seq 85: EN BR=2
    85: "Dự báo chính xác giúp nông nghiệp, phòng thiên tai, chiến đấu như đã nói.<br>Năng lực của Yachiyo hữu ích vượt hiểu lường.<br> ",
    
    # Seq 86: EN BR=2
    86: "Đừng khen nhiều vậy!! Năng lực không phải của em,<br>là của Thần Long—<br> ",
    
    # Seq 87: EN BR=2
    87: "Thần Long không cho người ghét mượn lực. Chứng minh Yachiyo là người tốt. Thực tế nói chuyện thấy dễ thương.<br> ",
    
    # Seq 88: EN BR=2
    88: "A, a wa!? Th, thiện cảm là gì—<br>Đ, lần đầu nam giới nói vậy...<br> ",
    
    # Seq 89: EN BR=2
    89: "Đừng nhí nhảnh. Là sự thật.<br>Ngực cất cao ở Căn Cứ Tiền Tuyến. Chỉ Huy là ta cho phép.<br> ",
    
    # Seq 90: EN BR=1
    90: "...!?<br>Chỉ Huy, quan tâm quá khứ của em—?<br> ",
    
    # Seq 91: EN BR=2
    91: "Đối phương đẹp dễ thương thì liền vậy~...<br>Yachiyo-san, cẩn thận nhé!<br> ",
    
    # Seq 92: EN BR=1
    92: "...<br> ",
    
    # Seq 93: EN BR=1
    93: "Yachiyo-san? Sao vậy?<br> ",
    
    # Seq 94: EN BR=2
    94: "À, đó... Chỉ Huy được nữ tính thích...<br>Cảm giác hiểu rõ lắm... Làm sao bây giờ...♡<br> ",
    
    # Seq 95: EN BR=1
    95: "——Gù gù gù.<br> ",
    
    # Seq 96: EN BR=1
    96: "Ạ? Bỗng nghe tiếng sấm...?<br> ",
    
    # Seq 97: EN BR=1
    97: "——Xào xạc!<br> ",
    
    # Seq 98: EN BR=1
    98: "Wa wa wa!? Mưa nắng dữ lắm!?<br> ",
    
    # Seq 99: EN BR=1
    99: "Mưa to lắm!?<br>Nhanh vào nhà! Sẽ 感冒 (ốm) đấy!<br> ",
    
    # Seq 100: EN BR=1
    100: "Vâng, vâng!<br> ",
    
    # Seq 101: EN BR=1
    101: "Phù... Chót vót.<br>Yachiyo cũng ổn chứ?<br> ",
    
    # Seq 102: EN BR=1
    102: "Vâng. Nhờ anh...<br> ",
    
    # Seq 103: EN BR=2
    103: "Mưa rầm bất chợt. Thần Long không nói gì à?<br> ",
    
    # Seq 104: EN BR=2
    104: "Vâng... Lạ nhỉ.<br>Sắp bị mưa thì Thần Long luôn báo mà—<br> ",
    
    # Seq 105: EN BR=2
    105: "Vì vậy hôm qua em báo cho Chỉ Huy và Alicia-san 'có vẻ sẽ mưa'. Vì cùng hướng.<br> ",
    
    # Seq 106: EN BR=1
    106: "Thần quả thật thất thường.<br> ",
    
    # Seq 107: EN BR=2
    107: "Nhưng năng lực cô rất hữu ích.<br>Đôi khi nhờ cô dự báo được không?<br> ",
    
    # Seq 108: EN BR=2
    108: "Vâng, đương nhiên!<br>Sẽ cố gắng hết sức, mong Chỉ Huy giúp đỡ♪<br> ",
    
    # Seq 109: EN BR=1 (extra narration)
    109: "——Gù gù gù.<br> ",
}

print(f"VI translations: {len(VI_TRANSLATIONS)}")

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
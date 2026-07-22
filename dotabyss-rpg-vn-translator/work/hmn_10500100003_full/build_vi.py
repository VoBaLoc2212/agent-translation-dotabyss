#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build VI asset for hmn_10500100003 using field-index approach.
EN asset is English; ja.json has JP keys.
We translate JP->VI and replace the text field in EN asset lines.
"""
from pathlib import Path
import json

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10500100003"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# Load ja.json for JP text order (skip title at index 0)
with open(ROOT / "dotabyss-translation-main/translations/novels/hmn_10500100003/ja.json", "r", encoding="utf-8") as f:
    ja_data = json.load(f)

ja_texts = list(ja_data.keys())
title_jp = ja_texts[0]
msg_jp = ja_texts[1:]  # 123 messages

print(f"ja.json entries: {len(ja_texts)} (title + {len(msg_jp)} messages)")

# Vietnamese translations for each JP message in order
# IMPORTANT: Use <br> for line breaks, not literal \n
# Replace ASCII commas with U+201A
vi_translations = [
    # 1
    "Thế rồi, nhờ Betty mà chúng ta cũng được lãnh thêm tiền lương tạm thời.<br>Cố gắng làm việc cho bằng được nhé?",
    # 2
    "Đã hiểu. Nhưng mà có những việc thì dù có gấp gáp đến mấy<br>cũng không thể giải quyết được đâu.",
    # 3
    "Cái gì, thế?",
    # 4
    "Đó là một khối đá nham. Có nhiều lớp đá cực kỳ cứng chồng chất lên nhau.<br>Việc bẻ gãy chúng đang tốn nhiều thời gian lắm……",
    # 5
    "Nguyên lai là đá nham sao……<br>Tốc độ đào bốc không tăng lên như dự kiến ban đầu là do cái đó à.",
    # 6
    "Chính xác.",
    # 7
    "Đá nham…… phải không, Chỉ Huy?",
    # 8
    "Ồ? Có ý tưởng gì đó à, Betty?",
    # 9
    "K, không, không phải ý đó……",
    # 10
    "Betty, không có gì phải e ngại đâu. Hãy nói suy nghĩ của em ra.",
    # 11
    "……Đúng đấy. Nếu im lặng tại chỗ thì sẽ giống hệt như trước nữa.<br>Còn em mình, có lẽ cũng có thể làm được gì đó……",
    # 12
    "Anh công binh ơi!<br>Xin hãy dẫn em đến chỗ khối đá nham!",
    # 13
    "Chắc chắn em sẽ làm được thôi!",
    # 14
    "……Vậy à? Cô bé kia dùng đôi cánh tay mảnh khảnh đó,<br>muốn bẻ gãy khối đá nham mà ngay cả chúng tao cũng chẳng làm gì được à?",
    # 15
    "Ga ha ha ha! Đâu có làm được đâu!<br>Khác hẳn với việc bắt thương nhân gánh đất đấy!",
    # 16
    "Được nhờ em mà lãnh thêm tiền lương tạm tính là tạ ơn rồi. Nhưng từ đây về sau là việc của chúng tao. Cô bé hãy về nhà tránh cho bị thương đi.",
    # 17
    "Em không về đâu!",
    # 18
    "Na, là gì chứ!",
    # 19
    "……Thật sự em không có lực tay cũng không có thể lực.<br>Nhưng mà thứ cần thiết cho khai thác không chỉ là hoàn toàn sức mạnh thô bạo thôi!",
    # 20
    "Vì vậy…… mọi người, lần này hãy tin tưởng em,<br>xin hãy chờ một chút nữa!",
    # 21
    "Bảo chờ à? Không có thời gian cho việc đó……",
    # 22
    "Được thôi, chờ một chút mà sao. Khi Betty đang hành động thì chúng ta cứ nghỉ ngơi một tí đi.",
    # 23
    "……Hiểu rồi. Chỉ trong lúc nghỉ ngơi thôi, chỗ này giao cho em.",
    # 24
    "Cảm ơn Chỉ Huy ạ!<br>Em sẽ ngay lập tức chuẩn bị ngay!",
    # 25
    "Phờ phờ……<br>Nếu hình dạng này thì thêm lực từ phía này sẽ bẻ gãy sạch sẽ……",
    # 26
    "Chỉ Huy ơi.<br>Cô bé kia đang trèo lên trên khối đá nham làm gì vậy?",
    # 27
    "Chắc chắn rồi. Nhưng tao nghĩ có thể mong đợi được.<br>Betty có kỹ thuật và kiến thức mà tao lẫn mày đều không có.",
    # 28
    "U um…… Nhưng mà như này thì đá nham bên trong……<br>Yoshi! Thì ra là thế!",
    # 29
    "Cái gì? Cô bé kia khéo dùng cơ thể nhỏ bé<br>lẻn vào khe hở giữa đá và đá!?",
    # 30
    "Betty!? Muốn làm gì vậy!?",
    # 31
    "Chỉ là em lẻn vào sâu bên trong để phá vỡ toàn bộ đá nham bên trong<br>thôi nên không cần lo lắng ạ!",
    # 32
    "Phá vỡ toàn bộ đá nham à!?",
    # 33
    "Mọi người ơi!<br>Giờ em sẽ phá phá đá nham, xin mọi người hãy tách ra xa một chút ạ!",
    # 34
    "Ba, phá phá……!?",
    # 35
    "Đi thôi ạ!<br>Ba~! Hai~! Một…… Bùng ạ!",
    # 36
    "Bùm────!",
    # 37
    "*Khò khè, khò khè*…! Th, thật là bụi bặm!",
    # 38
    "Cái gì cũng không thấy!?",
    # 39
    "Khụt, cuối cùng bụi cũng tản, tầm nhìn cũng mở ra rồi nhưng……<br>Cô, đây là cái gì!?",
    # 40
    "Kìa, đá nham……! Tan thành mảnh vụn……!?",
    # 41
    "Chúng tao mất mấy ngày cũng không phá hủy được khối đá nham mà trong tích tắc……",
    # 42
    "Đâ, nhưng mà cô bé kia ở đâu rồi!?",
    # 43
    "Betty!",
    # 44
    "Phù!<br>Đã thành công ạ!",
    # 45
    "Cô bé, bình an không……! Tốt quá!<br>Nhưng mà em đã làm gì vậy!?",
    # 46
    "Là vũ nổ.<br>Em am hiểu việc xử lý chất nổ ạ.",
    # 47
    "Ba, vũ nổ……!? Hè, hè hè hè<br>Th, thật ngầu nhỉ!",
    # 48
    "E hén ạ!",
    # 49
    "Nói e hén mà cô bé kia<br>mặt bùn bẩn trông thấy!",
    # 50
    "Đó là mọi người cũng như nhau thôi~",
    # 51
    "Ồ, vậy à?<br>Ga ha ha ha, lần này tao thua một màn!",
    # 52
    "Chỉ Huy! Hoàn thành nhiệm vụ ạ!<br>Khối đá nham cản đường đã được nghiền nát ạ!",
    # 53
    "Xuất sắc, Betty.<br>Nhưng không ngờ em lại biết xử lý chất nổ chứ.",
    # 54
    "Quay lại, tài năng của Betty là phát huy được ở đơn vị này nhỉ.",
    # 55
    "Ẻ? Ý là Chỉ Huy từ ban đầu<br>đã biết em phù hợp với công binh……?",
    # 56
    "Tất nhiên. Các cậu cũng nghĩ thế chứ?",
    # 57
    "Đương nhiên!<br>Betty là thành viên xuất sắc của đội công binh!",
    # 58
    "Đã hoàn toàn hòa nhập rồi nhỉ.<br>Không hổ là Betty.",
    # 59
    "Chỉ Huy……",
    # 60
    "Kể từ vụ đó, đội công binh似乎 không còn gây rắc rối,<br>việc đào bốc cũng tiến triển suôn sẻ nhỉ.",
    # 61
    "À. Betty cũng có vẻ hòa nhập rồi, may quá.<br>Nhắc nhớ, đội công binh đến hôm nay đấy.",
    # 62
    "Có chuyện gì muốn nói thì là chuyện gì nhỉ?",
    # 63
    "Cục, cục",
    # 64
    "A, chắc là đến rồi.<br>Mời vào.",
    # 65
    "Chỉ Huy, chào ạ!",
    # 66
    "Xin phép quấy rối, Chỉ Huy.",
    # 67
    "Làm phiền Chỉ Huy.<br>Đám đông xin lỗi nhé.",
    # 68
    "À, đến đúng lúc.<br>Betty, thế nào?",
    # 69
    "Dạ!<br>Đội công binh mọi người rất tốt bụng, mỗi ngày đều vui ạ!",
    # 70
    "Đó là tốt.<br>Vậy, hôm nay đội công binh tổng động viên làm gì?",
    # 71
    "Chuyện đó…… thực ra, quyết định chọn đội trưởng chính thức.",
    # 72
    "Ẻ? Vậy à ạ?<br>Em tưởng chỉ đến chào Chỉ Huy thôi.",
    # 73
    "Hiểu rồi. Vậy, đội trưởng chọn ai?",
    # 74
    "Nghĩ sẽ nhờ Betty.",
    # 75
    "……Hả?",
    # 76
    "E e e e e!? T, ta ạ!?<br>C, chuyện đó em làm không nổi ạ!",
    # 77
    "Đừng nói thế, nhận lời được không?",
    # 78
    "Kết quả bàn bạc của toàn thể.<br>Phù hợp nhất là Betty đấy.",
    # 79
    "Giao cho người khác, chắc chắn cãi vã!",
    # 80
    "Kiến thức nổ của Betty nâng cao hiệu suất công việc,<br>còn biết phân biệt đá quý.",
    # 81
    "Betty không nhìn ai qua kính màu.<br>Không ai phù hợp hơn.",
    # 82
    "Cuối cùng, mồ hôi bùn bẩn thế nào,<br>nhìn nụ cười cởi mở của Betty, mệt một ngày bay sạch.",
    # 83
    "Mọi người……",
    # 84
    "……Vậy thì, Betty đã là người không thể thiếu của đội công binh.<br>Làm trưởng đội để gìn giữ sự đoàn kết là hay nhất?",
    # 85
    "(Nguyên lai. Cần để gom kẻ bùn nhọn không phải quyền uy,<br>mà là nụ cười cởi mở của Betty.)",
    # 86
    "Vậy thì, Betty sao?<br>Đội trưởng, nhận lời không?",
    # 87
    "Ta……?<br>Nhưng, ta có làm được không……?",
    # 88
    "Lo lắng không xứng thì từ nay mà mài giũa.<br>Sau này nguyên thạch cũng sẽ sáng như ngọc.",
    # 89
    "Như ngọc……",
    # 90
    "Hiểu rồi! Chắc chắn em sẽ thành đội trưởng xuất sắc!<br>Vì vậy, mọi người…… xin hãy cùng em cố gắng nhé!",
    # 91
    "Ừ! Cậy vào cậu, đội trưởng!",
    # 92
    "Kết局 đẹp, may quá.<br>Đào bốc cũng ổn định.",
    # 93
    "Chỉ Huy.<br>Thực ra từ đầu đã dự đoán được kết cục này?",
    # 94
    "Betty chiếu sáng xung quanh,<br>có thể thành cờ hiệu cho đội công binh luôn cãi vã.",
    # 95
    "Tao chỉ nghĩ, Betty ở gần thứ thích thì sẽ cố gắng được.",
    # 96
    "Không ngờ dùng nổ giải quyết vấn đề,<br>còn gom cả đội công binh nữa.",
    # 97
    "Thôi, coi như vậy.",
    # 98
    "Chỉ Huy!",
    # 99
    "Ồ, Betty à.<br>Có chuyện gì?",
    # 100
    "Chỉ Huy! Dẫn em gặp những đồng đội tuyệt vời nhất,<br>cảm ơn ạ!",
    # 101
    "Ừm? Profesionมา nói chuyện đó à?",
    # 102
    "Vì…… em ở đâu cũng bị coi như gánh nặng,<br>không hiểu mình đến tiền tuyến làm gì.",
    # 103
    "Nhưng Chỉ Huy đã đẩy lưng em……",
    # 104
    "Nhờ đó, em rụt rè hoàn toàn,<br>cũng dám bước chân đầu tiên!",
    # 105
    "Chỉ Huy, biết ơn đến mấy cũng không hết!",
    # 106
    "Ha ha, nói quá. Tao không làm gì đâu.<br>Đường của mày, do chính mày bước ra.",
    # 107
    "Vậy hãy tự tin. Mày là kẻ tuyệt vời.",
    # 108
    "U u~~!<br>Em sẽ theo Chỉ Huy trọn đời ạ!",
    # 109
    "Đó là tin vui.<br>Chỉ… từ nay dùng nổ thì báo trước nhé?",
    # 110
    "Mày đôi khi quá lớn gan, ngay tao cũng giật mình.<br>Cái đó thật sự bất ngờ……",
    # 111
    "A…… Chẳng lẽ Chỉ Huy lo lắng cho em ạ?",
    # 112
    "Mà…… đấy.<br>Cho đến khi mày xuất hiện từ khói bụi, thật lòng tao không yên chút nào.",
    # 113
    "Lo lắng…… cho em ạ. Vậy à.<br>E hén, e he he he~♪",
    # 114
    "……Nói làm lo lắng mà, cười cái gì vậy mày.",
    # 115
    "Kho, lỗiLost ạ.<br>Vừa nãy mặt không nhịn cười được.",
    # 116
    "Kẻ lạ lùng thật……<br>Mà, gì thì gì, từ nay tao vẫn cậy vào mày.",
    # 117
    "Rõ ạ! Vì trở thành sức lực của Chỉ Huy,<br>ngay giữa lửa giữa nước em cũng sẽ lao đến ạ!",
    # 118
    "A, nhưng mà…… chỉ có trong bóng tối thôi, xin được miễn ạ.",
    # 119
    "Và cả, Chỉ Huy ạ.",
    # 120
    "Ừm? Cái gì?",
    # 121
    "Em sẽ tỏa sáng rực rỡ hơn nữa ạ!<br>Vì vậy, từ nay về sau xin hãy luôn quan sát em ạ!",
    # 122
    "À.<br>Cố lên nhé, tiểu đội trưởng công binh nhỏ bé.",
    # 123
    "Dạ, ạ!",
]

# Title
title_vi = "Tiểu Đội Trưởng Công Binh Nhỏ Bé"

# Verify count
assert len(vi_translations) == len(msg_jp), f"Count mismatch: {len(vi_translations)} vs {len(msg_jp)}"

# Replace ASCII commas in VI text with U+201A
for i, t in enumerate(vi_translations):
    if ',' in t:
        vi_translations[i] = t.replace(',', '‚')

# Read EN asset preserving BOM and CRLF
raw = EN.read_bytes()
assert raw[:3] == b'\xef\xbb\xbf', "EN source must have BOM"
text = raw.decode('utf-8-sig')
lines = text.splitlines(True)

out = []
msg_idx = 0
for idx, line in enumerate(lines, 1):
    cleaned = line.rstrip('\r\n')
    if cleaned.startswith('title,'):
        parts = cleaned.split(',', 1)
        assert len(parts) == 2
        new = 'title,' + title_vi
        trailer = line[len(cleaned):]
        out.append(new + trailer)
    elif cleaned.startswith(('message,', 'messageTextUnder,', 'messageTextCenter,')):
        parts = cleaned.split(',', 5)
        assert len(parts) >= 3, f"Line {idx}: {line!r}"
        if msg_idx < len(vi_translations):
            parts[2] = vi_translations[msg_idx]
            msg_idx += 1
        new = ','.join(parts)
        trailer = line[len(cleaned):]
        out.append(new + trailer)
    else:
        out.append(line)

assert msg_idx == len(vi_translations), f"Used {msg_idx} translations, expected {len(vi_translations)}"

out_bytes = b'\xef\xbb\xbf' + ''.join(out).encode('utf-8')
VI.parent.mkdir(parents=True, exist_ok=True)
VI.write_bytes(out_bytes)

print(f"Translated {msg_idx} messages + title -> {VI}")
print(f"Total lines: {len(out)} (EN had {len(lines)})")

# Verify
if len(out) == len(lines):
    print("LINE COUNT MATCH: PASS")
else:
    print(f"LINE COUNT MISMATCH: EN={len(lines)} VI={len(out)}")

with open(VI, 'rb') as f:
    content = f.read()
    if content[:3] == b'\xef\xbb\xbf':
        print("BOM: PASS")
    if b'\r\n' in content:
        print("CRLF: PASS")
    else:
        print("CRLF: MISSING")
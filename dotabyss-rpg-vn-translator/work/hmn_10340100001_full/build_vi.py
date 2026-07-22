#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build VI asset for hmn_10340100001 by field-index replace.

Case: EN-asset-is-English (ja.json is identity map → JP recovered from ja.json order;
en.json holds the English text; EN asset text fields are ENGLISH, title field is JP).
Approach: translate title JP->VI (Title Case) and every message EN->VI, while
mirroring the exact trailing "<br> " suffix and preserving ALL other bytes
(BOM, CRLF, field count, delimiters, IDs, tags, voice keys).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(r"E:/AgentTranslation")
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10340100001.txt"
VI = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10340100001.txt"
WORK = ROOT / "dotabyss-rpg-vn-translator/work/hmn_10340100001_full"

# Line number -> VI text field (INCLUDES the authoritative trailing "<br> " suffix
# for message records; title has no suffix). Comma inside VI text uses U+201A (‚).
VI_TEXT = {
    17: "Đây Là Đồng Phục Đấy!",
    27: "Gõ cửa‚ gõ cửa.<br> ",
    29: "…Ai thế? Thôi kệ đi‚ vào đi.<br> ",
    37: "Xin phép làm phiền!<br> ",
    101: "Em là Carla của Đội Cảnh Vệ Cộng Hòa Eldorana!<br>Hôm nay em chính thức nhận nhiệm vụ tại đơn vị Căn Cứ Tiền Tuyến này!<br> ",
    110: "Em sẽ dồn toàn tâm toàn ý cho nhiệm vụ!<br>Rất mong được sát cánh cùng anh!<br> ",
    115: "À‚ phải rồi‚ có quân tiếp viện từ quân chủ lực Eldorana<br>mà. Ta đã được báo cáo rồi.<br> ",
    117: "Em trông lễ phép và chân thành. Thái độ nghiêm túc với nhiệm vụ<br>của em thể hiện rõ ràng. Em như một chiến binh tốt đấy.<br> ",
    119: "Có thêm binh sĩ được huấn luyện là một sự giúp đỡ lớn.<br>Ta sẽ trông cậy vào em đấy.<br> ",
    128: "Dạ‚ Chỉ Huy! Em thấy hân hạnh!<br> ",
    147: "Nhưng mà… dù lời nói và hành động của em nghiêm túc‚<br>sao lại mặc bộ đồ đó?<br> ",
    172: "Đồng phục này là trang phục nữ chính thức của Đội Cảnh Vệ Cộng Hòa<br>Eldorana đấy!<br> ",
    174: "…P‐phải rồi à?<br>Tiện thể‚ cho ta hỏi sao lại là đồ bơi nhỉ?<br> ",
    185: "Vâng! Đội Cảnh Vệ Cộng Hòa Eldorana chủ yếu đảm nhiệm nhiệm vụ<br>chống hải tặc!<br> ",
    194: "Chiến trường chính của chúng em là trên biển và dọc bờ biển‚<br>nên đã chọn đồng phục phù hợp với môi trường ấy.<br> ",
    199: "Ra vậy‚ hóa ra nó có ý nghĩa thật.<br>Thế nhưng‚ cũng khá là hiếm thấy.<br> ",
    208: "Em xin lỗi nếu trông có phần khó coi‚ nhưng đây là đồng phục chúng em tự hào‚<br>nên mong ngài thứ lỗi.<br> ",
    210: "Không… nào có khó coi đâu‚ trái lại còn đẹp mắt nữa…<br>Ư… Carla này‚ em không thấy xấu hổ sao?<br> ",
    219: "…Với tư cách là một quân nhân‚ em không được phép đưa ra ý kiến<br>cá nhân về đồng phục.<br> ",
    221: "…Em khéo lảng tránh đấy.<br> ",
    223: "Nhưng mà‚ một bộ đồng phục đáng tự hào‚ hử?<br>Ra vậy‚ ra vậy‚ nghe cũng hay đấy.<br> ",
    234: "Dạ…? Ý ngài là sao…?<br> ",
    238: "Thế tức là Carla đang mặc đồng phục chính thức.<br>Vậy tức là không có vấn đề gì khi ta kiểm tra kỹ nhỉ?<br> ",
    250: "K‐kiểm tra cơ ạ!?<br> ",
    254: "À không‚ tại lần đầu ta thấy bộ đồng phục này.<br>Nhân cơ hội này ta muốn nhìn kỹ một chút.<br> ",
    265: "K‐kỹ một chút…!?<br> ",
    267: "Ừ‚ chầm chậm và thong thả.<br>…Đã là đồng phục rồi‚ thì chẳng sao đúng không?<br> ",
    278: "C‐có chứ! Với tư cách là thành viên Đội Cảnh Vệ Cộng Hòa Eldorana‚<br>em luôn mặc đồng phục đúng quy cách!<br> ",
    280: "Vậy thì để ta xem nào.<br> ",
    291: "D‐dạ‚ Chỉ Huy.<br>Mời ngài cứ tự nhiên…<br> ",
    325: "Hmm… ta hiểu rồi…<br> ",
    335: "Ư‐ưm‚<br>việc ngài nhìn sát thế này…<br> ",
    337: "Có vấn đề gì sao?<br>Nhìn kỹ đồng phục từ cự ly gần thì có gì đâu?<br> ",
    348: "Không phải là sai…<br>Chỉ là em nghĩ ngài có chán không thôi.<br> ",
    350: "Không‚ ta đang có khoảng thời gian rất viên mãn.<br>Nhưng mà cái này… to thật đấy…<br> ",
    361: "To!?<br>C‐Chỉ Huy‚ ngài làm cái gì thế!?<br> ",
    363: "Là vật trang trí trên mũ của em đấy.<br>To nhỉ‚ có ý nghĩa gì không?<br> ",
    375: "A… v‐vâng. Vật trang trí này<br>tượng trưng cho biển Eldorana mang lại muôn vàn phước lành…<br> ",
    377: "Hừm‚ ta hiểu rồi.<br>Nhưng cái này… cũng khá là hoành tráng đấy.<br> ",
    388: "C‐cái gì hoành tráng cơ ạ!?<br> ",
    390: "Là cái khiên của em đấy.<br>Món đồ tốt đấy‚ phải không?<br> ",
    401: "C‐cái trang bị này được thiết kế cho chiến đấu trên biển‚ ưu tiên<br>sự nhẹ và linh hoạt…<br> ",
    413: "…Em không nghĩ nó to đến thế… ngài đang nói về<br>cái khiên đúng không…?<br> ",
    415: "Đương nhiên là nói về khiên rồi. Và trên hết… cái này khổng lồ thật.<br> ",
    426: "Cái gì khổng lồ cơ…?<br> ",
    430: "Rõ ràng quá còn gì? Ngực của Carla.<br> ",
    472: "Chỉ Huy! Xin ngài đừng đùa nữa!<br> ",
    475: "Ồ‚ đúng rồi nhỉ. Xin lỗi‚ ta không nhịn được trêu em một chút.<br> ",
    494: "L‐lần này em sẽ bỏ qua‚ nhưng xin ngài hãy cẩn thận hơn sau này.<br> ",
    496: "Ta hiểu rồi. Ừ‚ ta sẽ cẩn thận.<br> ",
    502: "Thế nhé‚ ta đã nhận được thông báo điều chuyển của em‚ nhưng vì sao một<br>sĩ quan quân đội Eldorana lại đến căn cứ này?<br> ",
    514: "C‐chuyện đó là…<br> ",
    526: "Có tin báo rằng hải tặc E‐Eldorana có thể đang ở Căn Cứ<br>Tiền Tuyến…<br> ",
    537: "Em được phái đến đây chủ yếu để bắt giữ bọn họ‚ và‚ ờ…<br> ",
    539: "Bắt giữ hải tặc‚ hử.<br> ",
    554: "Ta đã nhận được thông báo trước từ Eldorana về việc điều động một<br>nữ cảnh vệ tên là Carla.<br> ",
    556: "Nhưng ta không hề nghe nói hải tặc là lý do. Đáng lẽ chỉ là một đợt<br>chi viện quân tiếp viện thông thường.<br> ",
    571: "Nhân tiện‚ em được báo nhiệm vụ này kéo dài khoảng bao lâu?<br> ",
    582: "Ư‐ưm‚ em nghe nói Căn Cứ Tiền Tuyến này luôn thiếu<br>nhân lực‚ nên…<br> ",
    584: "Quân tiếp viện luôn được chào đón‚ nhưng em hơi khác một chút đấy‚ Carla.<br> ",
    586: "Nếu em đến vì nhiệm vụ‚ thì làm xong rồi về luôn sao?<br> ",
    598: "Không‚ em được lệnh tại đây hoàn thành nhiệm vụ một thời<br>gian.<br> ",
    600: "Ra vậy… ta trông cậy vào em đấy.<br> ",
    615: "(Một đợt điều động không thời hạn‚ một nhiệm vụ như bị gắn ép vào.<br> ",
    617: "(Và cô gái nghiêm túc này đành phải chịu đựng sự quấy rối tình dục<br>trắng trợn của ta‚ hử.<br> ",
    619: "(Có gì đó khuất tất ở đây rồi.)<br> ",
    634: "Được rồi‚ vậy ta đi thôi.<br> ",
    645: "Dạ‚ đi đâu ạ?<br> ",
    647: "Còn phải hỏi? Tiệc chào mừng em đấy‚ Carla.<br> ",
    649: "Eldorana là quốc gia của những người đi biển. Mời thành viên mới uống một<br>chén là dấu hiệu của sự hiếu khách đúng không?<br> ",
    651: "Ta muốn đón em theo phong tục của em. Đi quán rượu cùng cạn chén<br>thôi.<br> ",
    663: "Chỉ Huy! Ngài biết về đất nước em rồi!<br> ",
    665: "Đương nhiên. Sao nào? Em đi cùng ta chứ?<br> ",
    699: "Vâng! Em rất sẵn lòng đi cùng ngài‚ Chỉ Huy!<br> ",
}

# Preflight assertions
raw = EN.read_bytes()
assert raw[:3] == b"\xef\xbb\xbf", "EN source lost BOM"
assert b"\r\n" in raw, "EN source not CRLF"
text = raw.decode("utf-8-sig")
lines = text.split("\r\n")
if lines and lines[-1] == "":
    lines = lines[:-1]

# Count EN text records & assert VI count matches
cmds = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
en_recs = [(i + 1, l) for i, l in enumerate(lines) if l.startswith(cmds)]
assert len(VI_TEXT) == len(en_recs), f"VI count {len(VI_TEXT)} != EN records {len(en_recs)}"

# Per-line <br> count + comma assert + apply
out_lines = []
for i, l in enumerate(lines, 1):
    if i in VI_TEXT:
        vi = VI_TEXT[i]
        # ASCII comma must NOT appear inside VI text field
        assert "," not in vi, f"ASCII comma in VI line {i}: {vi!r}"
        if l.startswith("title,"):
            parts = l.split(",", 1)
            assert len(parts) == 2, f"title parse fail L{i}"
            new = "title," + vi
            # title must keep 2 fields
        else:
            parts = l.split(",")
            assert len(parts) >= 3, f"message parse fail L{i}: {l!r}"
            old_tf = parts[2]
            old_br = old_tf.count("<br>")
            new_br = vi.count("<br>")
            assert old_br == new_br, f"BR mismatch L{i}: en={old_br} vi={new_br}"
            new = ",".join([parts[0], parts[1], vi] + parts[3:])
        out_lines.append(new)
    else:
        out_lines.append(l)

VI_PATH = VI
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
out = "\r\n".join(out_lines) + "\r\n"
VI_PATH.write_bytes(b"\xef\xbb\xbf" + out.encode("utf-8"))

print(f"WROTE {VI_PATH} lines={len(out_lines)} records={len(VI_TEXT)}")

# Draft manifest (verifier will inject independent_verify into both artifacts)
manifest = {
    "scene": "hmn_10340100001",
    "source_language": "ja",
    "target_language": "vi",
    "asset_case": "EN-asset-is-English; title field still JP",
    "record_counts": {"title": 1, "message": 73, "messageTextUnder": 0, "messageTextCenter": 0, "total": 74},
    "addressing_matrix": {
        "Commander": "Chỉ Huy (and first-person 'ta' in inner monologue / 'anh' to Carla)",
        "Carla (カーラ)": "em/anh to Commander; self-name kept as Carla in dialogue",
    },
    "terminology": {
        "エルドラーナ共和国警備隊": "Đội Cảnh Vệ Cộng Hòa Eldorana",
        "前線基地": "Căn Cứ Tiền Tuyến",
        "水着": "đồ bơi",
        "盾": "khiên",
        "制服": "đồng phục",
        "セクハラ/sexual harassment": "quấy rối tình dục",
    },
    "notes": [
        "Title translated JP->VI Title Case: これは制服ですっ！ -> Đây Là Đồng Phục Đấy!",
        "All message text fields were English in the EN asset; translated EN->VI.",
        "ja.json is an identity map; JP source recovered from ja.json key order, EN text from en.json/asset.",
        "Trailing '<br> ' suffix mirrored per record; fullwidth comma converted to U+201A (‚).",
        "H18 content (sexual-harassment banter) translated directly per confirmed 18+ project rule.",
        "Speaker labels (カーラ, <user>) kept byte-identical per field-1 rule.",
    ],
    "status": "PENDING_VERIFY",
}
(WORK / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("WROTE manifest.json")

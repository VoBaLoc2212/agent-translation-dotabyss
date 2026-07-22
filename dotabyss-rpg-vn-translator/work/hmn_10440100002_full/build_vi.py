#!/usr/bin/env python3
"""Build VI translation for hmn_10440100002 (Yachiyo weather-forecast scene).
EN-asset-is-English. Uses suffix-mirror pattern.
IMPORTANT: All Vietnamese text uses ‚ (U+201A) instead of ASCII comma inside text fields.
"""
import json, re, sys
from pathlib import Path

WORK = Path(__file__).parent
ROOT = Path("E:/AgentTranslation")
EN_ASSET = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100002.txt"
JA_JSON = ROOT / "dotabyss-translation-main/translations/novels/hmn_10440100002/ja.json"
VI_PATH = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100002.txt"

COMMA = "\u201A"  # U+201A SINGLE LOW-9 QUOTATION MARK (replaces ASCII comma inside text)

ja_map = json.loads(JA_JSON.read_text(encoding="utf-8"))
jp_keys = list(ja_map.keys())
print(f"ja.json entries: {len(jp_keys)}")

raw = EN_ASSET.read_bytes()
has_crlf = b"\r\n" in raw
text = raw.decode("utf-8-sig")
lines = text.split("\n")
print(f"Total lines: {len(lines)}, CRLF: {has_crlf}")

# ====== VI TRANSLATIONS (per-seq, 0-99) ======
# Content only - trailing tag suffix is auto-mirrored from EN source.
# Use ‚ (U+201A) instead of ASCII comma inside text fields.
# Use fullwidth ， also OK since EN source uses it.
VI = {}

VI[0]  = "Thưa Rồng Thần{COMMA} Xin Hãy Ban Lời Tiên Tri!"  # title
VI[1]  = "<size=48>――Vài Ngày Sau</size>"  # messageTextCenter
VI[2]  = "Ồ{COMMA} tìm ra cậu rồi{COMMA} Yachiyo.<br>Hôm nay cũng xem dự báo thời tiết được không?"  # 踊り子
VI[3]  = "Vâng{COMMA} tất nhiên rồi ạ♪"  # ヤチヨ
VI[4]  = "Thì bọn chị muốn xem dự báo đến khoảng trưa mai{COMMA}<br>để còn biết đường phơi quần áo chứ hỏng hết thì khổ."  # 市民
VI[5]  = "Để em xin ý kiến Rồng Thần xem sao ạ."  # ヤチヨ
VI[6]  = "Rồng Thần ơi{COMMA} Rồng Thần――xin hãy đáp lời.<br>Vì những người này{COMMA} xin ban cho một lời tiên tri――"  # ヤチヨ
VI[7]  = "……Vâng{COMMA} ra rồi!!"  # ヤチヨ
VI[8]  = "Từ hôm nay đến ngày mai{COMMA} trời sẽ quang đãng!<br>Thời tiết cực kỳ thích hợp để giặt giũ đó ạ♪"  # ヤチヨ
VI[9]  = "Mừng quá nhỉ."  # 市民
VI[10] = "Hôm nay phơi được y phục rồi!<br>Kịp cho vở diễn ngày mai nên mừng quá đi."  # 踊り子
VI[11] = "Thì ra là vậy. Cả ngày nay sẽ nắng nhỉ. Biết được tin tốt rồi."  # <user>
VI[12] = "A{COMMA} Chỉ Huy! Hôm nay có dự định ra ngoài sao ạ?"  # ヤチヨ
VI[13] = "Ừ. Sau khi xong việc ta có hẹn hò đấy.<br>Nếu trời nắng thì tính ngắm sao trên thảo nguyên…… phụt phụt phụt. Mong quá."  # <user>
VI[14] = "Thật ngại vì đã chen ngang{COMMA} nhưng xin đừng đặt quá nhiều niềm tin<br>vào dự báo của cháu……"  # ヤチヨ
VI[15] = "Ừ ừ. Nhưng mà đến giờ vẫn đúng mà{COMMA}<br>chắc không sao đâu nhỉ."  # 市民
VI[16] = "Dạo này tôi hay nhờ dự báo để kiểm tra độ chính xác{COMMA}<br>thì phần lớn đều đúng cả{COMMA} chắc không vấn đề gì đâu."  # <user>
VI[17] = "Ừ ừ! Em tin chị mà! Em đi giặt đồ vội đây!"  # 踊り子
VI[18] = "(Xin hãy chính xác mà không có vấn đề gì……)"  # ヤチヨ
VI[19] = "(Mà mình lo lắng quá rồi nhỉ{COMMA} Rồng Thần ơi♪)"  # ヤチヨ
VI[20] = "<size=48>――Đêm Hôm Ấy</size>"  # messageTextCenter
VI[21] = "<size=48>――Sáng Hôm Sau</size>"  # messageTextCenter
VI[22] = "M-mọi người…… cháu xin lỗi……<br>Có vẻ như đã không chính xác rồi…… m-mọi người có sao không ạ?"  # ヤチヨ
VI[23] = "……Đang ở trên thảo nguyên thì tự nhiên mưa ào xuống.<br>Ướt như chuột lột rồi."  # <user>
VI[24] = "Tôi thì không sao.<br>Vì được bảo đừng tin quá nên tôi để ý bên ngoài mà."  # 踊り子
VI[25] = "Còn tôi thì đống đồ phơi chiều nay hỏng hết rồi……"  # 市民
VI[26] = "X-xin lỗi ạ……"  # ヤチヨ
VI[27] = "Không không{COMMA} biết sao được. Tại tôi không chịu nghe lời cảnh báo thôi mà."  # 市民
VI[28] = "Vì trông cậy vào em cả{COMMA} nên từ giờ vẫn nhờ em nhé♪"  # 踊り子
VI[29] = "Vâng! Lần này nhất định…… làm được ạ♪"  # ヤチヨ
VI[30] = "Mà tối nay thì sao? Thực ra hôm nay cũng có hẹn đấy――"  # <user>
VI[31] = "Tối nay tôi cũng có việc nên muốn nghe thử～."  # 踊り子
VI[32] = "Rõ!<br>Vậy thì――Rồng Thần ơi{COMMA} xin hãy đáp lời!"  # ヤチヨ
VI[33] = "……Ra rồi! Hôm nay nhất định sẽ nắng đấy ạ!<br>Hãy vui tươi thật tươi lên nào♪"  # ヤチヨ
VI[34] = "<size=48>――Đêm Hôm Ấy</size>"  # messageTextCenter
VI[35] = "H{COMMA} hả…… ư?"  # ヤチヨ
VI[36] = "<size=48>――Sáng Hôm Sau</size>"  # EXTRA center card
VI[37] = "X-xin lỗiiiiiiii～！！！！"  # ヤチヨ
VI[38] = "C-cái gì thế…… Hôm nay thì sao hả!? Tôi phải tổ chức lại buổi hẹn đấy!"  # <user>
VI[39] = "Hôm nay nhất định! Hôm nay nhất định sẽ nắng{COMMA}<br>Rồng Thần đã phán vậy ạ!"  # ヤチヨ
VI[40] = "Thiệt hả trời……"  # 市民
VI[41] = "Thôi thôi{COMMA} lỡ rồi thì nghe thử lần nữa xem?"  # 踊り子
VI[42] = "Tại{COMMA} tại saooooo～!?"  # ヤチヨ
VI[43] = "<size=48>――Sáng Hôm Sau</size>"  # EXTRA center card
VI[44] = "Hổ thẹn quá ạ……"  # ヤチヨ
VI[45] = "Quả nhiên biết trước thời tiết là chuyện không tưởng nhỉ."  # 市民
VI[46] = "Hừm…… thôi thì{COMMA} lúc nào rảnh lại ghé nghe vậy. Cảm ơn nhé."  # 踊り子
VI[47] = "Tôi cũng về làm việc thôi――<br>Yachiyo{COMMA} chẳng qua là trật một lần thôi mà{COMMA} đừng lo lắng quá nhé. Bye."  # <user>
VI[48] = "(……Mọi người{COMMA} đi hết rồi. Buồn ơi là buồn……)"  # ヤチヨ
VI[49] = "(Nhưng không có thời gian để nản lòng! Rồng Thần đang<br>dõi theo mọi việc mình làm mà! Chăm chỉ thì ắt sẽ có chuyện tốt lành――)"  # ヤチヨ
VI[50] = "Yachiyo. Lâu rồi không gặp. Cô còn nhớ tôi không?"  # 兵士
VI[51] = "Dạ? Ờm{COMMA} anh là…… hình như đã gặp anh trước đây thì phải."  # ヤチヨ
VI[52] = "À{COMMA} anh là người lính đã từng đích thân đến cảm ơn em trước đây!<br>Phải không ạ?"  # ヤチヨ
VI[53] = "Vâng! Nhờ nghe dự báo bão sét trước nhiệm vụ mà tôi đã thoát chết đấy.<br>Lúc đó thực sự rất cảm ơn cô."  # 兵士
VI[54] = "Không dám ạ. Em giúp được thì thực sự tốt quá! Hôm nay anh có chuyện gì thế ạ?"  # ヤチヨ
VI[55] = "Tôi muốn nhờ cô dự báo cho ngày mai và ngày kia.<br>Tôi sắp đi viễn chinh với Chỉ Huy nên cần biết trước."  # 兵士
VI[56] = "Đi đường núi thì nhanh xong việc{COMMA} nhưng tôi muốn tránh thời tiết xấu……<br>Nếu mưa thì sẽ chọn đường vòng…… Ngày mai trời có nắng không?"  # 兵士
VI[57] = "Em sẽ hỏi thử ạ! ……Rồng Thần ơi{COMMA} xin hãy giúp!"  # ヤチヨ
VI[58] = "……Nắng{COMMA} đấy ạ!!!!"  # ヤチヨ
VI[59] = "Rõ! Vậy tôi sẽ đề nghị Chỉ Huy đi đường núi."  # 兵士
VI[60] = "Vâng! Xin hãy cẩn thận ạ!"  # ヤチヨ
VI[61] = "――Nhưng{COMMA}<br>trời lại đổ mưa trên con đường mà Chỉ Huy và những người lính đã chọn."  # narration
VI[62] = "Em xin lỗi……!!!!"  # ヤチヨ
VI[63] = "Yachiyo xin lỗi không ngừng{COMMA} nhưng Chỉ Huy và những người lính bảo vệ và động viên cô ấy{COMMA} nói rằng đó không phải lỗi của cô."  # messageTextUnder
VI[64] = "Tuy nhiên{COMMA} chuyện dự báo của Yachiyo cứ sai liên tiếp đã thành lời đồn{COMMA} và những kẻ ác ý bắt đầu xì xào sau lưng cô{COMMA} gọi cô là 'đồ vô dụng'."  # messageTextUnder
VI[65] = "Và rồi{COMMA} Yachiyo――"  # messageTextUnder
VI[66] = "Tạm biệt{COMMA} mọi người ở Căn Cứ Tiền Tuyến."  # ヤチヨ
VI[67] = "Kết thúc một chuyến đi thật cô đơn biết mấy nhỉ――Rồng Thần ơi."  # ヤチヨ
VI[68] = "Nhưng em không thể mãi nản lòng được!<br>Em sẽ đi tu luyện lại{COMMA} và một ngày nào đó{COMMA} nhất định――!"  # ヤチヨ
VI[69] = "<size=48>――Trên Núi{COMMA} Bên Ngoài Căn Cứ Tiền Tuyến</size>"  # messageTextCenter
VI[70] = "Yachiyo! Tốt quá{COMMA} theo kịp rồi!"  # <user>
VI[71] = "Chỉ Huy!? Sao ngài lại ở chỗ này……?"  # ヤチヨ
VI[72] = "Nghe tin em xuống tinh thần nên tôi đi tìm đấy. Người gác cổng nói<br>em rời khỏi căn cứ đi về phía núi{COMMA} nên tôi vội đuổi theo ngay."  # <user>
VI[73] = "Không lẽ{COMMA} em định rời khỏi Căn Cứ Tiền Tuyến<br>luôn sao?"  # <user>
VI[74] = "……Đúng vậy ạ."  # ヤチヨ
VI[75] = "Đừng lo về mấy lời đồn nhảm đó làm gì.<br>Đó chỉ là mấy kẻ không biết gì về em nói linh tinh thôi."  # <user>
VI[76] = "Nhưng mà quả thật em đã gây rắc rối cho mọi người ạ."  # ヤチヨ
VI[77] = "Hơn nữa{COMMA} em cũng không hiểu được nguyên nhân nữa.<br>Tại sao dự báo của em lại sai nhiều đến thế chứ――"  # ヤチヨ
VI[78] = "Dù biết rằng Rồng Thần có khi thất thường nên dự báo sai lệch{COMMA}<br>nhưng chưa bao giờ tệ đến thế này. Em đúng là một miko thất bại."  # ヤチヨ
VI[79] = "Vậy nên em sẽ về quê tu luyện thêm lần nữa.<br>Em sẽ tiếp tục hành trình sau khi tỷ lệ chính xác của dự báo đã hồi phục."  # ヤチヨ
VI[80] = "Thực sự không còn cách nào khác sao?<br>Coi việc về quê là giải pháp cuối cùng{COMMA} thử tìm hiểu nguyên nhân thêm xem sao?"  # <user>
VI[81] = "Nhưng mà em…… em đã phụ sự kỳ vọng của người lính đã tin tưởng em."  # ヤチヨ
VI[82] = "Em biết nản lòng là không tốt{COMMA} nhưng nghĩ đến cảm xúc của người đó{COMMA}<br>thì nhất quyết không thể ở lại được…………!"  # ヤチヨ
VI[83] = "Ngược lại rồi{COMMA} Yachiyo. Nếu em cứ thế mà biến mất{COMMA}<br>người lính đó sẽ mãi tự trách mình đấy."  # <user>
VI[84] = "Hắn sẽ nghĩ rằng tại hắn đã làm tổn thương em――đấy."  # <user>
VI[85] = "Có lẽ là vậy thật ạ……"  # ヤチヨ
VI[86] = "Tôi cũng sẽ buồn nếu em đi mất đấy. Vì em là người vui vẻ và tốt bụng mà.<br>Có thể suy nghĩ lại được không?"  # <user>
VI[87] = "Tình cảm của ngài thực sự rất đáng quý ạ. Nhưng dù vậy{COMMA} em vẫn――"  # ヤチヨ
VI[88] = "(Vô ích sao…… Hử?)"  # <user>
VI[89] = "Giíii!"  # モンスターＡ
VI[90] = "Quái vật á!? Mà bọn này là loại đi bầy đàn mà――"  # <user>
VI[91] = "Chỉ Huy nhìn quanh.<br>Em có thể cảm nhận được nhiều con quái vật đang tiến đến từ xa."  # narration
VI[92] = "Gừooooo!"  # モンスターＢ
VI[93] = "Mà cả con đầu đàn cũng ở đây nữa sao! Chết tiệt!"  # <user>
VI[94] = "Chỉ Huy{COMMA} lui ra sau! Họa!"  # ヤチヨ
VI[95] = "Gíii!?"  # モンスターＡ
VI[96] = "Yachiyo dùng gậy đánh vào con quái vật gần nhất{COMMA}<br>khiến nó bất tỉnh."  # narration
VI[97] = "Chỉ Huy{COMMA} chúng ta chạy trước khi bị bao vây!"  # ヤチヨ
VI[98] = "Được rồi! Căn cứ ở hướng đó! Chạy mau!"  # <user>
VI[99] = "Theo lệnh{COMMA} Yachiyo bắt đầu chạy.――Nhưng bọn quái vật cũng đuổi theo.<br>Một cuộc rượt đuổi trên núi bắt đầu."  # narration

# Replace placeholders
for seq in VI:
    VI[seq] = VI[seq].replace("{COMMA}", COMMA)

assert len(VI) == 100, f"Expected 100 VI entries, got {len(VI)}"
print(f"VI entries: {len(VI)}")

# ========== Suffix mirror build ==========
TEXT_CMDS = ("title,", "message,", "messageTextCenter,", "messageTextUnder,")
out_lines = []
seq = 0
trailing_suffix_re = re.compile(r"((?:<[^>]+>\s*)+)$")

for ln in lines:
    stripped = ln.strip("\r\n ")
    cmd_prefix = None
    for cmd in TEXT_CMDS:
        if stripped.startswith(cmd):
            cmd_prefix = cmd
            break

    if cmd_prefix is None:
        out_lines.append(ln.rstrip("\r"))
        continue

    parts = ln.rstrip("\r").split(",")
    
    if cmd_prefix == "title,":
        parts[1] = VI[seq]
        out_line = ",".join(parts)
    elif cmd_prefix == "message,":
        en_tf = parts[2]
        m = trailing_suffix_re.search(en_tf)
        if m:
            suffix = m.group(1)
            parts[2] = VI[seq] + suffix
        else:
            parts[2] = VI[seq]
        out_line = ",".join(parts)
    else:
        # messageTextCenter, messageTextUnder: no suffix mirror (already have </size> or plain text)
        parts[2] = VI[seq]
        out_line = ",".join(parts)

    out_lines.append(out_line)
    seq += 1

assert seq == 100, f"Expected 100 text records, processed {seq}"

# ========== Preflight ==========
print("\n=== PREFLIGHT ====")
br_issues = []
comma_issues = []
for i, ln in enumerate(lines):
    stripped = ln.strip("\r\n ")
    for cmd in TEXT_CMDS:
        if stripped.startswith(cmd):
            en_parts = ln.rstrip("\r").split(",")
            vi_parts = out_lines[i].rstrip("\r\n").split(",")
            tf_idx = 1 if cmd == "title," else 2
            
            if tf_idx < len(en_parts) and tf_idx < len(vi_parts):
                en_tf = en_parts[tf_idx]
                vi_tf = vi_parts[tf_idx]
                en_br = en_tf.count("<br>")
                vi_br = vi_tf.count("<br>")
                if en_br != vi_br:
                    br_issues.append(f"L{i+1} {cmd.strip(',')} EN br={en_br} VI br={vi_br}")
                
                # Check for ASCII comma in VI text field (delimiter comma, not U+201A)
                if "," in vi_tf:
                    comma_issues.append(f"L{i+1} ASCII comma in VI")
            break

if br_issues:
    print(f"BR MISMATCHES ({len(br_issues)}):")
    for issue in br_issues:
        print(f"  {issue}")
else:
    print("All <br> counts match! ✓")

if comma_issues:
    print(f"ASCII COMMA IN VI ({len(comma_issues)}):")
    for issue in comma_issues:
        print(f"  {issue}")
else:
    print("No ASCII commas in VI text fields! ✓")

if br_issues or comma_issues:
    print("\n*** PREFLIGHT FAILED ***")
    sys.exit(1)

# ========== Write ==========
VI_PATH.parent.mkdir(parents=True, exist_ok=True)
output = "\n".join(out_lines)
if has_crlf:
    output = output.replace("\n", "\r\n")
    output = re.sub(r"\r\r\n", "\r\n", output)
if not output.endswith("\r\n" if has_crlf else "\n"):
    output += "\r\n" if has_crlf else "\n"

bom = b"\xef\xbb\xbf"
VI_PATH.write_bytes(bom + output.encode("utf-8"))
print(f"\n✓ VI written to {VI_PATH}")
print(f"Output lines: {len(out_lines)} (input: {len(lines)})")
print("DONE")

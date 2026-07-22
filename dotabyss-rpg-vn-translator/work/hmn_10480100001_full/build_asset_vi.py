#!/usr/bin/env python3
"""
Translate hmn_10480100001 (Celeste first-meeting): JP→VI.
EN-asset-is-English case with mixed JP title / EN messages.
Uses ordinal alignment: ja.json entry N → asset record N.
Properly mirrors EN asset `<br> ` suffix and replaces ASCII commas with U+201A.
"""
import json, re, sys, os

ROOT = "E:/AgentTranslation"
EN_ASSET = f"{ROOT}/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt"
VI_ASSET = f"{ROOT}/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10480100001.txt"
JA_JSON = f"{ROOT}/dotabyss-translation-main/translations/novels/hmn_10480100001/ja.json"
EN_JSON = f"{ROOT}/dotabyss-translation-main/translations/novels/hmn_10480100001/en.json"

# Load JP novel (identity map)
with open(JA_JSON, 'r', encoding='utf-8') as f:
    ja_raw = json.load(f)
with open(EN_JSON, 'r', encoding='utf-8') as f:
    en_raw = json.load(f)

ja_keys = list(ja_raw.keys())
en_vals = [en_raw.get(k, "") for k in ja_keys]
print(f"ja.json entries: {len(ja_keys)}, en.json non-empty: {sum(1 for v in en_vals if v)}")

# Read EN asset
with open(EN_ASSET, 'rb') as f:
    raw_bytes = f.read()
has_bom = raw_bytes.startswith(b'\xef\xbb\xbf')
has_crlf = b'\r\n' in raw_bytes
text = raw_bytes.decode('utf-8-sig')
en_lines = text.splitlines(True)
print(f"EN asset: {len(en_lines)} lines, BOM={has_bom}, CRLF={has_crlf}")

# Parse text records
text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
records = []
for i, line in enumerate(en_lines):
    for cmd in text_cmds:
        if line.startswith(cmd):
            parts = line.split(',', 5)
            if cmd == 'title,':
                tf = parts[1].rstrip('\r\n') if len(parts) > 1 else ''
            else:
                tf = parts[2].rstrip('\r\n') if len(parts) > 2 else ''
            records.append((i, cmd, parts, tf, line))
            break
print(f"Text records: {len(records)} (1 title + {len(records)-1} message)")

# ═══════════════════════════════════════════════════════════════
# VI TRANSLATIONS — JP source → Vietnamese
# ═══════════════════════════════════════════════════════════════
# All translations go HERE. Each entry's text will have the EN asset's
# trailing `<br> ` suffix appended automatically, and ASCII commas will
# be replaced with U+201A (‚) automatically.
# DO NOT add `<br> ` suffixes in the translations below — the build code
# handles suffix mirroring.

VI_BY_SEQ = {}

VI_BY_SEQ[0] = "Chính Mày Là Kẻ Cướp Đúng Không?"  # title

# Seq 1: Stall vendor hawking
VI_BY_SEQ[1] = "Nào nào！ Hôm nay cũng có đầy hàng ngon đây này！<br>Khách ơi‚ mời ghé xem nhé！"

# Seq 2: Commander observing market
VI_BY_SEQ[2] = "……Ừm. Chợ hôm nay cũng nhộn nhịp nhỉ.<br>Nếu sau này không có việc thì tha hồ mà dạo xem rồi về……"

# Seq 3: Gyahh! (vendor scream)
VI_BY_SEQ[3] = "Giá á！？"

# Seq 4: Hm...? (Commander)
VI_BY_SEQ[4] = "Hử……？"

# Seq 5: Robber demands money
VI_BY_SEQ[5] = "Này！ Đưa tiền đây！"

# Seq 6: Vendor pleads
VI_BY_SEQ[6] = "Hii ơi‚ dừng lại！ Tôi đưa mà‚ đừng đá……"

# Seq 7: Commander shocked
VI_BY_SEQ[7] = "Giữa‚ giữa ban ngày ban mặt mà đi cướp á！？"

# Seq 8: Robber escapes
VI_BY_SEQ[8] = "Hê hê‚ chào nhé！"

# Seq 9: Commander chases
VI_BY_SEQ[9] = "Khỉ‚ đứng lại！"

# Seq 10: Celeste attacks (Raaaagh!)
VI_BY_SEQ[10] = "<size=48>Này y y y ！</size>"

# Seq 11: Gwaah!
VI_BY_SEQ[11] = "Gụa ！？"

# Seq 12: Narration - tackled
VI_BY_SEQ[12] = "Chỉ Huy bất ngờ bị một cô gái lạ mặt lao vào tông.<br>Cứ thế bị khóa tay gọn lỏn."

# Seq 13: Celeste accuses
VI_BY_SEQ[13] = "Giữa ban ngày ban mặt‚ mày là thằng ăn cướp hả？<br>Dám ra tay trước mặt Celeste đây hả‚ gan nhỉ！"

# Seq 14: Commander responds
VI_BY_SEQ[14] = "……Cô là cảnh vệ hả？ Vừa hay！<br>Thằng cướp vừa chạy về hướng kia——"

# Seq 15: Celeste boasts
VI_BY_SEQ[15] = "Tưởng không bị bắt hả‚ đồ ngốc này？<br>Thì nhờ mày mà tao có công lao rồi nhé！"

# Seq 16: Celeste money thoughts
VI_BY_SEQ[16] = "Ngon quá……chắc có thưởng chứ hả？ Mư phụ phụ."

# Seq 17: Commander protests
VI_BY_SEQ[17] = "Này‚ nghe tao nói này！"

# Seq 18: Celeste dismisses
VI_BY_SEQ[18] = "Ờ ờ biết rồi biết rồi. Ban ngày ra đường cướp giật‚<br>chắc đói bụng quá nhỉ？ Lời khai để về đồn khai‚ ngoan nào."

# Seq 19: Commander "No!"
VI_BY_SEQ[19] = "Không phải！"

# Seq 20: Celeste filing
VI_BY_SEQ[20] = "Im đi thằng cướp—à nhầm‚ cậu bé tiền thưởng.<br>Để xem nào…… 1-4-0-0‚ bắt giữ‚ xong……"

# Seq 21: Commander pleads
VI_BY_SEQ[21] = "L-Làm ơn hãy nghe tôi nói——！！!"

# Seq 22: Commander inner thought
VI_BY_SEQ[22] = "(Cuối cùng vẫn bị lôi vào đồn cảnh vệ……)"

# Seq 23: Celeste taking statement
VI_BY_SEQ[23] = "Rồi‚ lấy lời khai nhé！<br>Tên và ngày tháng năm sinh‚ viết vào đây."

# Seq 24: Commander insists
VI_BY_SEQ[24] = "Nghe tôi nói đi. Tôi không phải thằng cướp.<br>Thủ phạm là người khác. Tôi thấy hắn chạy trốn."

# Seq 25: Celeste dismisses
VI_BY_SEQ[25] = "Lại còn bào chữa nhảm nhí nữa hả…… Cứng đầu vừa thôi？"

# Seq 26: Commander reasons
VI_BY_SEQ[26] = "Sự thật là vậy thì biết làm sao.<br>Cô không có cấp trên à？"

# Seq 27: Celeste
VI_BY_SEQ[27] = "Họ có việc ra ngoài rồi."

# Seq 28: Celeste offended
VI_BY_SEQ[28] = "Mà này‚ gì vậy？ Nhìn tao là con gái nên coi thường à？<br>Cái thằng cướp như mày‚ tính nói đàn bà không đáng nghe hả？"

# Seq 29: Commander explains
VI_BY_SEQ[29] = "Đâu phải. Tôi chỉ muốn cô gọi ai đó biết tôi thôi.<br>Ở đây ngoài cô ra không còn ai à？"

# Seq 30: Celeste
VI_BY_SEQ[30] = "Tiếc nhỉ. Toàn bộ đều đi hết rồi."

# Seq 31: Commander suggests
VI_BY_SEQ[31] = "……Vậy đành nhờ cô vậy. Gọi chủ tiệm bị hại đến đi.<br>Ông ấy sẽ chứng minh tôi vô tội."

# Seq 32: Celeste refuses
VI_BY_SEQ[32] = "Bảo rồi‚ giờ chỉ có tao thôi nên không được.<br>Không thể để mày một mình được."

# Seq 33: Commander insists
VI_BY_SEQ[33] = "Cô có thể trói tôi vào ghế cũng được. Cứ đi nhanh lên.<br>Hơn hẳn ngồi đây tra hỏi mãi đấy chứ？"

# Seq 34: Celeste suspicious
VI_BY_SEQ[34] = "Nói thế chứ định chờ tao đi rồi trốn đúng không？<br>Bẻ khóa lồng à."

# Seq 35: Commander frustrated
VI_BY_SEQ[35] = "Lo thì nhốt tôi vào xà lim đi！<br>Từ nãy đến giờ chả giải quyết được gì cả！？"

# Seq 36: Celeste stubborn
VI_BY_SEQ[36] = "Đương nhiên rồi！ Tao chả có thời gian rảnh mà hầu chuyện mày đâu！<br>Và cũng chả định tha mày đâu！"

# Seq 37: Celeste greedy
VI_BY_SEQ[37] = "Mày là cục tiền thưởng đến mang tiền cho tao mà.<br>Nên nếu mày không chịu nhận tội để tao chắc công‚ thì đừng hòng đi đâu."

# Seq 38: Celeste
VI_BY_SEQ[38] = "Tao rất thích tiền. Nhưng ghét phiền phức và làm việc."

# Seq 39: Celeste
VI_BY_SEQ[39] = "Còn mày là cơ hội ngàn năm có một rơi xuống đầu tao……！<br>Mư phù phù phù ♪"

# Seq 40: Celeste
VI_BY_SEQ[40] = "Mau nhận tội đi. Có oán thì hãy<br>trách cái ngu của mày vì bị một tên cảnh vệ hư hỏng như tao bắt nhé."

# Seq 41: Commander thinking
VI_BY_SEQ[41] = "(Con nhỏ này tự nhận mình hư hỏng luôn rồi……<br>Làm ơn có ai đó ra tay đi……)"

# Seq 42: Door sound
VI_BY_SEQ[42] = "——Kách."

# Seq 43: Guard Captain — EN has NO internal br, just suffix
VI_BY_SEQ[43] = "Woooii‚ Celeste ơi. Nghe nói bắt được thằng cướp ở chợ hả‚ thật không？"

# Seq 44: Celeste greets Captain
VI_BY_SEQ[44] = "A‚ Đội Trưởng Cảnh Vệ！ Tin nhanh thế ♪"

# Seq 45: Celeste boasts — EN has NO internal br
VI_BY_SEQ[45] = "Vâng！ Chính con！ Con bắt được！ Quả tang！ Màn bắt giữ chớp nhoáng！"

# Seq 46: Captain surprised
VI_BY_SEQ[46] = "Hở？ Không ngờ cái thằng lười biếng như mày lại……"

# Seq 47: Celeste asks bonus — EN has NO internal br
VI_BY_SEQ[47] = "Hê hê hê hê hê. Có thưởng gì không ạ？ Có đúng không ạ？"

# Seq 48: Captain — EN has NO internal br
VI_BY_SEQ[48] = "Ừm‚ để tao cân nhắc. Thế thằng cướp đâu rồi？"

# Seq 49: Celeste presents
VI_BY_SEQ[49] = "Thằng này đây ạ！ Nó cứ khăng khăng không làm‚<br>nhưng con sẽ moi ra ngay！"

# Seq 50: Commander "Yo"
VI_BY_SEQ[50] = "…………Chào."

# Seq 51: Captain silent
VI_BY_SEQ[51] = "…………"

# Seq 52: Commander recognizes
VI_BY_SEQ[52] = "Gặp vài lần rồi nhỉ. Đội Trưởng Cảnh Vệ của<br>đội cảnh vệ phái từ Milesgard phải không？"

# Seq 53: Captain panics
VI_BY_SEQ[53] = "A‚ cái đó‚ ờ‚ ờ…… s-sao ngài lại ở đây？"

# Seq 54: Celeste explains
VI_BY_SEQ[54] = "Tại con bắt được ạ！ Con lao vào tông lúc nó định chạy！<br>Thế này——quụ ơ ơ ơ！ Khóa tay chặt cứng！"

# Seq 55: Captain explodes
VI_BY_SEQ[55] = "<size=48>ĐỒ ĐẦN—Ộ—Ộ—Ộ—Ộ—Ộ—Ờ—Ờ—Ờ—Ờ————！！！！</size>"

# Seq 56: Celeste shocked
VI_BY_SEQ[56] = "Ngẹ hé ！？"

# Seq 57: Celeste worries — EN has internal br (2 total)
VI_BY_SEQ[57] = "Đ-Đội Trưởng？ La to thế huyết áp lên đấy ạ……<br>？"

# Seq 58: Captain scolds
VI_BY_SEQ[58] = "Khỏi lo vớ vẩn！ Đồ ngu này！<br>Mày có biết mày vừa làm cái gì không hả！？"

# Seq 59: Celeste confused
VI_BY_SEQ[59] = "Ể ể ể……？ Gì cơ‚ thằng cướp——"

# Seq 60: Captain punishes
VI_BY_SEQ[60] = "Im mồm！ Bắt nhầm rồi！ Biết mày làm việc không nhiệt tình‚ nhưng ngu tới mức này……<br>Nhân danh Đội Trưởng Cảnh Vệ‚ phạt giảm lương！"

# Seq 61: Celeste wails
VI_BY_SEQ[61] = "Khônggggg ！？ Sao lại thếếế ！？"

# Seq 62: Commander intercedes
VI_BY_SEQ[62] = "À‚ không‚ Đội Trưởng——không cần làm tới vậy đâu. Phiền thật đấy‚ nhưng<br>nếu được chứng minh vô tội là tôi ổn rồi."

# Seq 63: Celeste surprised
VI_BY_SEQ[63] = "Hả……？<br>Trời‚ anh——bộ anh là người tốt hay sao？ Anh là ai？"

# Seq 64: Commander thinks
VI_BY_SEQ[64] = "(……Đúng là cơ hội chủ nghĩa mà)"

# Seq 65: Captain insists on punishment
VI_BY_SEQ[65] = "Tấm lòng của ngài rất đáng quý‚ nhưng như thế không làm gương cho kẻ khác được！<br>Xin hãy để tôi toàn quyền xử lý việc kỷ luật！"

# Seq 66: Celeste protests
VI_BY_SEQ[66] = "S-Sao thế——！？ Độc đoán quá——！！"

# Seq 67: Captain dismisses
VI_BY_SEQ[67] = "Im đi！ Mau đi bắt thủ phạm thật đi！"

# Seq 68: Celeste scurries
VI_BY_SEQ[68] = "Hiiii ！？ C-Con đi đây ạ——！"

# Seq 69: Captain apologizes to Commander
VI_BY_SEQ[69] = "Chỉ Huy‚ thật xin lỗi ngài ！！"

# Seq 70: Commander asks about Celeste
VI_BY_SEQ[70] = "Không sao. Mà nãy con nhỏ đó——tên Celeste hả？<br>Nó là loại người nào？"

# Seq 71: Captain explains
VI_BY_SEQ[71] = "Chính nó cũng tự nhận‚ đúng là một tên cảnh vệ hư hỏng……<br>Tiền‚ rượu là lẽ sống‚ hạnh kiểm cũng tệ. Đúng là đồ không thể tin nổi."

# Seq 72: Commander knows
VI_BY_SEQ[72] = "Vậy mà anh không đuổi nó‚ chắc vì nó có tài phải không？"

# Seq 73: Captain shocked
VI_BY_SEQ[73] = "……！？<br>Sao ngài biết……？"

# Seq 74: Commander
VI_BY_SEQ[74] = "(……Quả nhiên mà)"

# Seq 75: Celeste flashback attack
VI_BY_SEQ[75] = "Này y y！"

# Seq 76: Commander flashback
VI_BY_SEQ[76] = "Gụa ！？"

# Seq 77: Commander analysis
VI_BY_SEQ[77] = "(Lúc bị nó bắt‚ tao hoàn toàn không cảm nhận được gì cho tới khi nó nhảy vào.)"

# Seq 78: Commander analysis 2
VI_BY_SEQ[78] = "(Tao không tự tin về võ lực‚ nhưng với tư cách Chỉ Huy‚ tao có khả năng cảnh giác.<br>Thế mà tao lại không nhận ra cú lao tới của nó.)"

# Seq 79: Commander thinks
VI_BY_SEQ[79] = "(Nếu sử dụng tốt‚ có vẻ sẽ thành một nhân tài thú vị đây.)"

# Seq 80: Captain asks
VI_BY_SEQ[80] = "Ơ‚ Chỉ Huy？"

# Seq 81: Commander replies
VI_BY_SEQ[81] = "Xin lỗi‚ không có gì đâu. Tôi đi tìm Celeste một lát."

# Seq 82: Commander narration
VI_BY_SEQ[82] = "(Nó bảo đi đuổi thằng cướp‚ chắc ở chợ.<br>Đi xem sao.)"

# ── Verify all records translated ──
assert len(VI_BY_SEQ) == len(records), f"Expected {len(records)} translations, got {len(VI_BY_SEQ)}"
for seq in range(len(records)):
    assert seq in VI_BY_SEQ, f"Missing translation for seq {seq}"
print(f"\nAll {len(records)} translations defined")

# ═══════════════════════════════════════════════════════════════
# BUILD VI ASSET — field-index with suffix mirror
# ═══════════════════════════════════════════════════════════════

def count_br(s):
    return s.count('<br>')

def fix_commas(s):
    """Replace ASCII commas inside VI text with U+201A ‚ (single low-9 quotation mark)."""
    # Strategy: Replace ASCII commas, but NOT inside HTML tags
    result = []
    in_tag = False
    for ch in s:
        if ch == '<':
            in_tag = True
        elif ch == '>':
            in_tag = False
        if ch == ',' and not in_tag:
            result.append('\u201a')
        else:
            result.append(ch)
    return ''.join(result)

# Build output by replacing lines in the list
out_lines_list = list(en_lines)  # copy
errors = []
br_errors = []
comma_fixes = []

for seq, (line_idx, cmd, parts, tf, raw_line) in enumerate(records):
    vi_raw = VI_BY_SEQ[seq]
    
    if cmd == 'title,':
        # title,VALUE
        vi_text = fix_commas(vi_raw)
        old_line_end = parts[1][len(parts[1].rstrip('\r\n')):]  # preserves \r\n
        new_line = f"title,{vi_text}{old_line_end}"
        out_lines_list[line_idx] = new_line
        
        # BR check
        en_tf = parts[1].rstrip('\r\n')
        vi_br = count_br(vi_text)
        en_br = count_br(en_tf)
        if vi_br != en_br:
            br_errors.append(f"Seq {seq} L{line_idx}: title EN br={en_br} vs VI br={vi_br}")
    else:
        # message,SPEAKER,CONTENT,...,...
        en_tf = tf  # text field (minus trailing \r\n)
        
        # Find the trailing suffix
        suffix_match = re.search(r'((?:<[^>]+>\s*)+)$', en_tf)
        suffix = suffix_match.group(1) if suffix_match else ''
        
        # Fix commas in VI text
        vi_text = fix_commas(vi_raw)
        
        # Mirror the EN suffix
        vi_full = vi_text + suffix
        
        # Build the new line - preserve original line ending
        new_parts = list(parts[0:-1])  # all except last (which has \r\n)
        new_parts.append(vi_full)
        new_line = ','.join(new_parts)
        # Get original line ending from original parts[-1] or raw_line
        orig_ending = parts[-1][len(parts[-1].rstrip('\r\n')):] if parts[-1].rstrip('\r\n') != parts[-1] else ''
        if not orig_ending:
            # Check raw_line for ending
            stripped = raw_line.rstrip('\r\n')
            orig_ending = raw_line[len(stripped):]
        new_line += orig_ending
        out_lines_list[line_idx] = new_line
        
        # Count BRs in EN vs VI (total including suffix)
        vi_br = count_br(vi_full)
        en_br = count_br(en_tf)
        if vi_br != en_br:
            br_errors.append(f"Seq {seq} L{line_idx}: EN br={en_br} vs VI br={vi_br} | en=[{en_tf[:40]}] vi=[{vi_full[:40]}]")
        
        # Check if ASCII commas were fixed
        if ',' in vi_raw:
            comma_fixes.append(f"Seq {seq} L{line_idx}: fixed commas in [{vi_raw[:40]}]")

# Join as single string
output_text = ''.join(out_lines_list)

# ═══════════════════════════════════════════════════════════════
# PREFLIGHT CHECKS
# ═══════════════════════════════════════════════════════════════
print("\n=== PREFLIGHT CHECKS ===")

new_lines = output_text.splitlines(True)
new_records = sum(1 for l in new_lines if any(l.startswith(c) for c in text_cmds))
assert new_records == len(records), f"Record count mismatch: {new_records} vs {len(records)}"
print(f"Record count: {new_records}/{len(records)} ✓")

assert len(new_lines) == len(en_lines), f"Line count mismatch: {len(new_lines)} vs {len(en_lines)}"
print(f"Line count: {len(new_lines)}/{len(en_lines)} ✓")

if comma_fixes:
    print(f"ASCII commas fixed: {len(comma_fixes)} occurrences (→ U+201A ‚)")
else:
    print(f"No ASCII commas to fix ✓")

if br_errors:
    print(f"\nBR COUNT ERRORS ({len(br_errors)}):")
    for e in br_errors[:20]:
        print(f"  ✗ {e}")
    if len(br_errors) > 20:
        print(f"  ... and {len(br_errors)-20} more")
    sys.exit(1)
else:
    print(f"All <br> counts: {count_br(text)} EN → {count_br(output_text)} VI ✓")

# Check that VI asset has no remaining ASCII commas in text fields
remaining_commas = 0
for line in output_text.splitlines(True):
    for cmd in text_cmds:
        if line.startswith(cmd):
            if cmd == 'title,':
                tf = line.split(',', 1)[1].rstrip('\r\n') if ',' in line else ''
            else:
                parts = line.split(',', 3)
                tf = parts[2].rstrip('\r\n') if len(parts) > 2 else ''
            if ',' in tf:
                # Check if it's inside tags
                in_tag = False
                has_real_comma = False
                for ch in tf:
                    if ch == '<': in_tag = True
                    elif ch == '>': in_tag = False
                    elif ch == ',' and not in_tag:
                        has_real_comma = True
                        break
                if has_real_comma:
                    print(f"  ⚠  Remaining ASCII comma: [{tf[:60]}]")
                    remaining_commas += 1

if remaining_commas:
    print(f"\n⚠ {remaining_commas} lines still have ASCII commas (may be in tags)")
else:
    print(f"No remaining ASCII commas in VI ✓")

# ═══════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════════
os.makedirs(os.path.dirname(VI_ASSET), exist_ok=True)
out_bytes = output_text.encode('utf-8-sig')
# Fix any \r\r\n doubling
out_bytes = out_bytes.replace(b'\r\r\n', b'\r\n')

with open(VI_ASSET, 'wb') as f:
    f.write(out_bytes)

file_size = os.path.getsize(VI_ASSET)
print(f"\n✓ Written: {VI_ASSET} ({file_size} bytes)")

# Verify re-read
with open(VI_ASSET, 'rb') as f:
    verify = f.read()
bom_check = b'\xef\xbb\xbf'
print(f"✓ Re-read: {len(verify)} bytes, BOM={verify[:3]==bom_check}")
crlf_check = b'\r\n'
print(f"  CRLF={crlf_check in verify}")

if errors:
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)

print("\n=== BUILD COMPLETE ===")

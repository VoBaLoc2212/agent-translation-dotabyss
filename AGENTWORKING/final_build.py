import json
import os
import re

# ============================================================
# COMPLETE VIETNAMESE TRANSLATION DICTIONARY FOR hmn_10500100001
# Key = exact EN asset text field (including <br> suffix)
# Value = Vietnamese translation
# ============================================================

VI = {
    # 1. Title (JP text in EN asset -> VI Title Case)
    "くすんだ石ころ": "Viên Đá Nhòe",
    
    # 2-80. Message texts (EN -> VI)
    "There was a knock at the door.<br> ": "Có tiếng gõ cửa.<br> ",
    "Come in.<br> ": "Vào đi.<br> ",
    "Yes! Pardon the intrusion!<br> ": "Vâng! Xin phép ạ!<br> ",
    "So you're the volunteer who arrived today.<br> ": "Ngươi là tân binh vừa đến hôm nay à.<br> ",
    "Yes! I am Betty of Milesgard!<br> ": "Vâng! Em là Betty từ Milesgard ạ!<br> ",
    "Haha，you're a lively one. I heard you requested assignment to the<br>Frontline Base—why's that?<br> ": "Haha, nhỏ này nhiệt tình đấy. Nghe nói ngươi xin về Căn Cứ Tiền Tuyến, tại sao vậy?<br> ",
    "Yes! My family has been knights for generations. Since childhood，I've<br>witnessed my father and brother's heroic deeds on the battlefield!<br> ": "Vâng! Gia gia em đời đời quân nhân, từ nhỏ em đã chứng kiến cha anh em anh oai phong trên chiến trường!<br> ",
    "That's why my goal is to become a great soldier like my father and<br>brother，and to make a name for myself!<br> ": "Vì thế mục tiêu của em là trở thành binh sĩ xuất sắc như cha anh, để tên tuổi em được biết đến!<br> ",
    "I see. Your family must be expecting great things from you.<br> ": "Thôi hiểu. Gia đình chắc mong to lớn ở em lắm.<br> ",
    "Huh? Th-that is... um...<br> ": "Ủa? Thì th-thì là ừm...<br> ",
    "What's wrong?<br> ": "Sự việc thế nào?<br> ",
    "Actually，my family has opposed my becoming a soldier...<br> ": "Thực ra... gia đình em phản đối em làm binh sĩ...<br> ",
    "Oh? Why is that?<br> ": "Ồ? Tại sao vậy?<br> ",
    "They said that a small woman like me could never handle dangerous<br>battlefield duties...<br> ": "Bọn họ nói con gái nhỏ nhạy như em không thể gánh nổi nhiệm vụ chiến trường nguy hiểm...<br> ",
    "...I see. Then you came to the right place.<br> ": "...Hiểu rồi. Đến đây là đúng chỗ.<br> ",
    "Huh?<br> ": "Ủa?<br> ",
    "This is the front line. Chances to prove yourself are everywhere. Earn<br>merits here and show your family you've got what it takes.<br> ": "Đây là tiền tuyến. Cơ hội dựng công khắp nơi. Làm công đến đây để gia đình thấy em xứng đáng làm binh sĩ.<br> ",
    "Yes，sir! I will surely meet your expectations，Commander! Now，I<br>shall take my leave!<br> ": "Vâng, ạ! Em chắc chắn sẽ đáp ứng kỳ vọng của Chỉ Huy! Em xin phép lui!<br> ",
    "She is quite spirited，and seems like a fine girl.<br> ": "Cô ấy rất hăng hái, lại còn là cô gái tốt.<br> ",
    "Yeah. Having someone like that around really lifts the mood.<br> ": "Ừ. Có người như thế không khí nơi đây dễ chịu hơn.<br> ",
    "I hope she does well!<br> ": "Hy vọng cô ấy làm tốt!<br> ",
    "Yeah.<br> ": "Ừ.<br> ",
    "<size=48>—A few months later.</size>": "<size=48>—Vài Tháng Sau</size>",
    "So，excavation inside the Abyss is proving difficult. We had high<br>hopes for the Engineer Corps with their specialized skills，but...<br> ": "Vậy thì... khai quật trong Đại Huyệt đang gặp khó khăn. Đội Kỹ Sư chuyên môn ta kỳ vọng cao nhưng...<br> ",
    "When we actually looked into it，they've been fighting endlessly over<br>who should take charge as captain，and work has hardly progressed.<br> ": "Mở ra xem thì toàn tranh giành ai làm đội trưởng dẫn việc, công việc không tiến được chút nào.<br> ",
    "So they'll only listen to someone they acknowledge. These<br>craftsman-types can be a real handful at times like this.<br> ": "Chỉ nghe người mình công nhận thôi. Nhóm thủ công kiểu này lúc khó xử lắm.<br> ",
    "The captain，huh... Should I just appoint one myself? No，if I take a<br>high-handed approach，they'll only resist more...<br> ": "Đội trưởng à... có nên ta chỉ định luôn không? Không, đập đầu cho bọn nó chỉ khiến bọn nó phản kháng mạnh hơn thôi...<br> ",
    "Thinking about it isn't getting me anywhere. I'm going out to get some<br>fresh air.<br> ": "Tưởng cũng chẳng ra gì. Ta ra ngoài hít chút không khí cho thoáng.<br> ",
    "A leader for that rowdy bunch of engineers，huh... What to do... Hmm?<br> ": "Cầm đầu đám kỹ sư man rợ ấy à... Làm sao cho ổn... Ủa?<br> ",
    "*sigh*... What should I do...<br> ": "*Thở dài*... Làm sao bây giờ...<br> ",
    "Betty，long time no see.<br> ": "Betty, lâu không gặp.<br> ",
    "Ah, Lord Commander...!?<br> ": "A, Chỉ Huy...!?<br> ",
    "To think you remembered my name，Lord Commander... I'm deeply<br>honored!<br> ": "Không ngờ Chỉ Huy nhớ tên em... Em xúc động lắm ạ!<br> ",
    "You're exaggerating. But anyway... Did something happen?<br> ": "Nói lớn thật. Thôi không nói nữa... Có chuyện gì à?<br> ",
    "You were sighing with a gloomy face，weren't you?<br> ": "Người ta đang thở dài mặt mũi chán nản mà.<br> ",
    "...Haha，you caught me. That's the Lord Commander for you.<br> ": "...Haha, bị bắt quả tang. Thiệt là Chỉ Huy ạ.<br> ",
    "Actually... I was assigned to a monster-hunting squad，but I froze up<br>in a cave and caused trouble for my comrades.<br> ": "Thực ra... em được phân vào đội săn quái, nhưng trong hang động sợ tới mức đóng băng, làm phiền đồng đội...<br> ",
    "You froze? Were you injured?<br> ": "Đóng băng? Có bị thương không?<br> ",
    "Well，um... I'm not good with dark places. I got scared and couldn't<br>move.<br> ": "Đó, ừm... em sợ chỗ tối. Sợ nên không nhúc nhích được.<br> ",
    "That's tough... If so, why not request a transfer?<br> ": "Khó xử nhỉ... Thế thì xin điều động đi.<br> ",
    "That's why I had myself reassigned as a quartermaster. I thought that<br>as a quartermaster handling supplies and cooking, I could be of use.<br> ": "Đó là em xin điều động làm Binh Quân Nhu. Em nghĩ Binh Quân Nhu lo vật tư nấu ăn thì có ích.<br> ",
    "But even there，I failed...<br> ": "Nhưng ngay đó cũng thất bại...<br> ",
    "What，you're bad at cooking?<br> ": "Cái gì, nấu ăn dở à?<br> ",
    "No，cooking is actually my strong suit. But...<br> ": "Không, nấu ăn là điểm mạnh của em. Nhưng...<br> ",
    "I served a full-course meal，and they got angry，saying，'Who's got<br>the leisure to eat something like this on the battlefield!'<br> ": "Em trình bày món ăn đầy đủ, bọn nó giận: 'Ai có rảnh ăn mấy thứ này trên chiến trường!'<br> ",
    "A f-full-course meal?<br> ": "M-món ăn đầy đủ?<br> ",
    "I thought a tasty meal would cheer them up，but it backfired.<br> ": "Em nghĩ ăn ngon cho vui, thế mà lỡ làm hại.<br> ",
    "After a string of such failures，I was eventually told I was a failure as<br>a soldier，and they stopped giving me any tasks...<br> ": "Lỗi lầm liên tục, cuối cùng bị nói là binh sĩ thất bại, không giao việc gì nữa...<br> ",
    "A useless soldier like me earning merits? A pipe dream. How can I<br>write home? *sigh*...<br> ": "Binh sĩ vô dụng như em dựng công? Mộng tưởng. Viết thư về nhà sao? *Thở dài*...<br> ",
    "(She's really down... Huh?)<br> ": "(Cô ấy chán nản lắm... Ủa?)<br> ",
    "She scrubbed at the stone.<br> ": "Cô ấy chà xát viên đá.<br> ",
    "Betty, what have you been doing?<br> ": "Betty, ngươi đang làm gì vậy?<br> ",
    "Ah, sorry, it's a habit... I was polishing this.<br> ": "A, lỡ, thói quen thôi... Em đang mài cái này.<br> ",
    "This... is a stone? Why would you do that?<br> ": "Cái này... là đá? Tại sao làm vậy?<br> ",
    "It's my hobby!<br> ": "Sở thích của em!<br> ",
    "Polishing stones?<br> ": "Mài đá?<br> ",
    "Yes!<br> ": "Vâng!<br> ",
    "The stone sparkled.<br> ": "Viên đá lấp lánh.<br> ",
    "Huh? That stone, it's shining awfully bright, isn't it?<br> ": "Ủa? Viên đá đó, chẳng lẽ sáng lắm à?<br> ",
    "Eheh! That's right.<br> ": "Ê hê! Đúng rồi.<br> ",
    "Even a dull pebble buried in the earth for years can shine like a<br>beautiful gem if you polish it carefully and patiently!<br> ": "Viên sỏi nhòe chôn dưới đất nhiều năm, mài kỹ kiên nhẫn cũng sáng đẹp như ngọc báu!<br> ",
    "Speaking of stones, I am sure there are all sorts of stones in the<br>Abyss that you cannot see on the surface!<br> ": "Nói đến đá, chắc trong Đại Huyệt có đủ loại đá mặt đất không thấy!<br> ",
    "Ah... I wonder just what kind of stones are in the Abyss...<br> ": "A... Đại Huyệt có đá gì nhỉ...<br> ",
    "...<br> ": "…<br> ",
    "Wah! I-I'm sorry, I got carried away all by myself! In front of the Lord<br>Commander，I ended up lost in my own world...<br> ": "Ủa wa!? L-lỗi, em tự Say một mình! Trước mặt Chỉ Huy...<br> ",
    "No, it's fine. Having something you can get so into is a good thing.<br> ": "Không, ổn thôi. Có thứ gì đó để say mê là tốt.<br> ",
    "So you know all about stones, then?<br> ": "Vậy ngươi am hiểu đá hết à?<br> ",
    "Of course! But a hobby like this is completely useless on the<br>battlefield...<br> ": "Tất nhiên! Nhưng sở thích này trên chiến trường hoàn toàn vô dụng...<br> ",
    "...Betty.<br> ": "...Betty.<br> ",
    "I mean, I cannot be moping around, right! I have to work hard again<br>starting tomorrow!<br> ": "Đ-đúng, không thể chán nản! Ngày mai phải nỗ lực lại!<br> ",
    "Are you sure you're okay?<br> ": "Ngươi chắc chắn ổn à?<br> ",
    "Of course! Enthusiasm is the only thing I have going for me! So you<br>too must give it your all with a smile, Lord Commander!<br> ": "Tất nhiên! Chỉ có nhiệt huyết là của em! Vậy Chỉ Huy cũng phải nở nụ cười mà chiến đấu!<br> ",
    "Heh. Yeah, I guess so.<br> ": "Hê. Ừ, thôi được.<br> ",
    "Well then, I shall take my leave!<br> ": "Vậy em xin phép lui!<br> ",
    "...Hold on a second.<br> ": "...Chờ đã.<br> ",
    "Yes? What is it?<br> ": "Dạ? Vấn đề gì ạ?<br> ",
    "Betty, would you come with me for a bit?<br> ": "Betty, ngươi theo ta một chút được không?<br> ",
    "...?<br> ": "...?<br> ",
}

# Verify count
print(f"Translation dictionary: {len(VI)} entries")
assert len(VI) == 80, f"Expected 80, got {len(VI)}"
print("✓ All 80 translations present")

# Build VI asset file
def build_vi():
    en_path = 'E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt'
    with open(en_path, 'rb') as f:
        en_bytes = f.read()
    
    has_bom = en_bytes.startswith(b'\xef\xbb\xbf')
    text = en_bytes.decode('utf-8-sig')
    has_crlf = '\r\n' in text
    lines = text.splitlines(keepends=True)
    
    text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
    
    asset_texts = []
    for i, line in enumerate(lines):
        for cmd in text_cmds:
            if line.startswith(cmd):
                raw = line.rstrip('\r\n')
                if cmd == 'title,':
                    parts = raw.split(',', 2)
                    en_text = parts[1] if len(parts) > 1 else ''
                    speaker = ''
                else:
                    parts = raw.split(',', 3)
                    en_text = parts[2] if len(parts) > 2 else ''
                    speaker = parts[1] if len(parts) > 1 else ''
                
                ending = ''
                if line.endswith('\r\n'):
                    ending = '\r\n'
                elif line.endswith('\n'):
                    ending = '\n'
                
                asset_texts.append({
                    'line_idx': i,
                    'cmd': cmd.rstrip(','),
                    'speaker': speaker,
                    'en_text': en_text,
                    'raw_line': line,
                    'ending': ending,
                    'parts': parts,
                })
                break
    
    print(f"Total text records: {len(asset_texts)}")
    assert len(asset_texts) == 80, f"Expected 80 records, got {len(asset_texts)}"
    
    # Build VI output
    vi_lines = lines[:]
    translated = 0
    
    for at in asset_texts:
        en_text = at['en_text']
        cmd = at['cmd']
        
        vi_text = VI.get(en_text)
        if vi_text is None:
            print(f"ERROR: No translation for line {at['line_idx']+1}: {en_text[:80]}")
            vi_text = en_text
        else:
            translated += 1
        
        # Replace ASCII commas in VI text with U+201A
        vi_text_fixed = vi_text.replace(',', '\u201a')
        
        # Rebuild line
        raw = at['raw_line'].rstrip('\r\n')
        if cmd == 'title':
            parts = raw.split(',', 2)
            parts[1] = vi_text_fixed
            new_raw = ','.join(parts)
        else:
            parts = raw.split(',', 3)
            parts[2] = vi_text_fixed
            new_raw = ','.join(parts)
        
        vi_lines[at['line_idx']] = new_raw + at['ending']
    
    print(f"Translated {translated}/{len(asset_texts)} records")
    assert translated == len(asset_texts)
    
    # Write VI output
    vi_path = 'E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt'
    output_text = ''.join(vi_lines)
    output_bytes = output_text.encode('utf-8')
    if has_bom:
        output_bytes = b'\xef\xbb\xbf' + output_bytes
    
    os.makedirs(os.path.dirname(vi_path), exist_ok=True)
    with open(vi_path, 'wb') as f:
        f.write(output_bytes)
    
    print(f"Written VI: {vi_path}")
    print(f"BOM: {has_bom}, CRLF: {has_crlf}, Lines: {len(vi_lines)}")
    assert len(vi_lines) == len(lines), "Line count mismatch!"
    
    # Write work copy
    work_dir = 'E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100001_full'
    os.makedirs(work_dir, exist_ok=True)
    work_vi = os.path.join(work_dir, 'hmn_10500100001_vi.txt')
    with open(work_vi, 'wb') as f:
        f.write(output_bytes)
    print(f"Work copy: {work_vi}")
    
    # Focused diff
    diff_path = os.path.join(work_dir, 'focused_diff.md')
    with open(diff_path, 'w', encoding='utf-8') as f:
        f.write("# Focused Diff: hmn_10500100001\n\n")
        f.write("| Line | Command | Speaker | EN Text | VI Text |\n")
        f.write("|------|---------|---------|---------|--------|\n")
        for at in asset_texts:
            line_no = at['line_idx'] + 1
            en = at['en_text'].replace('\n', '\\n').replace('|', '\\|')
            vi = VI.get(at['en_text'], '').replace('\n', '\\n').replace('|', '\\|')
            f.write(f"| {line_no} | {at['cmd']} | {at['speaker']} | {en[:60]} | {vi[:60]} |\n")
    print(f"Focused diff: {diff_path}")
    
    # Manifest
    manifest = {
        "scene": "hmn_10500100001",
        "total_lines": len(lines),
        "text_records": len(asset_texts),
        "translated_records": translated,
        "title_cmd": sum(1 for a in asset_texts if a['cmd'] == 'title'),
        "message_cmd": sum(1 for a in asset_texts if a['cmd'] == 'message'),
        "messageTextCenter_cmd": sum(1 for a in asset_texts if a['cmd'] == 'messageTextCenter'),
        "messageTextUnder_cmd": sum(1 for a in asset_texts if a['cmd'] == 'messageTextUnder'),
        "bom_preserved": has_bom,
        "crlf_preserved": has_crlf,
        "encoding": "utf-8-sig",
        "delimiter": ",",
        "comma_replacement": "U+201A",
        "source_type": "EN-asset-is-English",
        "notes": "Title field JP→VI Title Case. messageTextCenter Title Case. EN→VI for messages. Speaker labels (field 1) kept JP verbatim. All 6 fields preserved. <br> suffix mirrored on message fields.",
    }
    manifest_path = os.path.join(work_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Manifest: {manifest_path}")
    
    # QA log
    qa_log = {
        "scene": "hmn_10500100001",
        "total_text_records": len(asset_texts),
        "translated_records": translated,
        "preflight_checks": {
            "line_count_match": len(vi_lines) == len(lines),
            "bom_preserved": has_bom,
            "crlf_preserved": has_crlf,
            "all_records_translated": translated == len(asset_texts),
        },
        "independent_verify": "PENDING",
    }
    qa_path = os.path.join(work_dir, 'qa_log.json')
    with open(qa_path, 'w', encoding='utf-8') as f:
        json.dump(qa_log, f, ensure_ascii=False, indent=2)
    print(f"QA log: {qa_path}")

if __name__ == "__main__":
    build_vi()
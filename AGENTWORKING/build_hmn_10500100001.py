import os
import json

# Translation dictionary: EN asset text -> VI translation
VI = {
    # Title
    "くすんだ石ころ": "Viên Đá Nhòe",
    # Message text center
    "<size=48>—A few months later.</size>": "<size=48>—Vài Tháng Sau</size>",
    # Messages
    "There was a knock at the door.<br> ": "Có tiếng gõ cửa.<br> ",
    "Come in.<br> ": "Vào đi.<br> ",
    "Yes! Pardon the intrusion!<br> ": "Vâng! Phiền rắc chút ạ!<br> ",
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
    "So，excavation inside the Abyss is proving difficult. We had high<br>hopes for the Engineer Corps with their specialized skills，but...<br> ": "Vậy thì... khai quật trong Đại Huyệt đang gặp khó khăn. Đội Kỹ Sư chuyên môn ta kỳ vọng cao nhưng...<br> ",
    "When we actually looked into it，they've been fighting endlessly over<br>who should take charge as captain，and work has hardly progressed.<br> ": "Mở ra xem thì toàn tranh giành ai làm đội trưởng dẫn việc, công việc không tiến được chút nào.<br> ",
    "So they'll only listen to someone they acknowledge. These<br>craftsman-types can be a real handful at times like this.<br> ": "Chỉ nghe người mình công nhận thôi. Nhóm thủ công kiểu này lúc khó xử lắm.<br> ",
    "The captain，huh... Should I just appoint one myself? No，if I take a<br>high-handed approach，they'll only resist more...<br> ": "Đội trưởng à... có nên ta chỉ định luôn không? Không, đập đầu cho bọn nó chỉ khiến bọn nó phản kháng mạnh hơn thôi...<br> ",
    "Thinking about it isn't getting me anywhere. I'm going out to get some<br>fresh air.<br> ": "Tưởng cũng chẳng ra gì. Ta ra ngoài hít chút không khí cho thoáng.<br> ",
    "A leader for that rowdy bunch of engineers，huh... What to do... Hmm?<br> ": "Cầm đầu đám kỹ sư man rợ ấy à... Làm sao cho ổn... Ủa?<br> ",
    "*sigh*... What should I do...<br> ": "*Thở dài*... Làm sao bây giờ...<br> ",
    "Betty，long time no see.<br> ": "Betty, lâu không gặp.<br> ",
    "Ah, Lord Commander...!?<br> ": "A, Chỉ Huy...!?<br> ",
    "To think you remembered my name, Lord Commander... I'm deeply<br>honored!<br> ": "Không ngờ Chỉ Huy nhớ tên em... Em xúc động lắm ạ!<br> ",
    "You're exaggerating. But anyway... Did something happen?<br> ": "Nói lớn thật. Thôi không nói nữa... Có chuyện gì à?<br> ",
    "You were sighing with a gloomy face, weren't you?<br> ": "Người ta đang thở dài mặt mũi chán nản mà.<br> ",
    "...Haha, you caught me. That's the Lord Commander for you.<br> ": "...Haha, bị bắt quả tang. Thiệt là Chỉ Huy ạ.<br> ",
    "Actually... I was assigned to a monster-hunting squad, but I froze up<br>in a cav...<br> ": "Thực ra... em được phân vào đội săn quái, nhưng trong hang động sợ tới mức đóng băng, làm phiền đồng đội...<br> ",
    "You froze? Were you injured?<br> ": "Đóng băng? Có bị thương không?<br> ",
    "Well, um... I'm not good with dark places. I got scared and couldn't<br>move.<br> ": "Đó, ừm... em sợ chỗ tối. Sợ nên không nhúc nhích được.<br> ",
    "That's tough... If so, why not request a transfer?<br> ": "Khó xử nhỉ... Thế thì xin điều động đi.<br> ",
    "That's why I had myself reassigned as a quartermaster. I thought that<br>as a quartermaster handling supplies and cooking, I could be of use.<br> ": "Em đã xin làm Binh Quân Nhu quản lý tiêu hao và nấu nướng, nghĩ vai này có ích.<br> ",
    "But even there，I failed...<br> ": "Nhưng nơi đó cũng thất bại...<br> ",
    "What, you're bad at cooking?<br> ": "Sao, nấu ăn dở à?<br> ",
    "No, cooking is actually my strong suit. But...<br> ": "Không, nấu ăn em giỏi đấy. Nhưng...<br> ",
    "I served a full-course meal，and they got angry，saying，'Who's got<br>the leisure to eat something like this on the battlefield!'<br> ": "Em bày tiệc đầy đủ, bị mắng 'Đâu có rảnh ăn đồ này trên chiến trường!'<br> ",
    "A f-full-course meal?<br> ": "Tiệc, tiệc đầy đủ à?<br> ",
    "I thought a tasty meal would cheer them up, but it backfired.<br> ": "Em nghĩ ăn ngon cho vui, ai ngờ hại người.<br> ",
    "After a string of such failures, I was eventually told I was a failure as<br>a soldier, and they stopped giving me any tasks...<br> ": "Lần nào cũng thế, cuối cùng bị bảo 'binh sĩ thất격', không giao việc gì nữa...<br> ",
    "A useless soldier like me earning merits? A pipe dream. How can I<br>write home?...<br> ": "Binh sĩ vô dụng như em dựng công? Vô vọng. Về nhà báo cha mẹ thế nào đây?...<br> ",
    "(She's really down... Huh?)<br> ": "(Cô ấy chán nản lắm... Ủa?)<br> ",
    "She scrubbed at the stone.<br> ": "Cô ấy chà xát viên đá.<br> ",
    "Betty. What have you been doing?<br> ": "Betty. Em làm gì vậy?<br> ",
    "Ah, sorry, it's a habit... I was polishing this.<br> ": "A, xin lỗi, thói quen... Em đang mài này.<br> ",
    "This... is a stone? Why would you do that?<br> ": "Đây... là đá à? Mài làm gì?<br> ",
    "It's my hobby!<br> ": "Sở thích của em ạ!<br> ",
    "Polishing stones?<br> ": "Mài đá à?<br> ",
    "Yes!<br> ": "Vâng ạ!<br> ",
    "The stone sparkled.<br> ": "Viên đá lóe sáng.<br> ",
    "Huh? That stone, it's shining awfully bright, isn't it?<br> ": "Ủa? Viên đá đó sáng lóa ánh à?<br> ",
    "Eheh! That's right.<br> ": "Ehe, đúng rồi.<br> ",
    "Even a dull pebble buried in the earth for years can shine like a<br>beautiful gem if you polish it carefully and patiently!<br> ": "Viên sỏi nhòe nhạt chôn dưới đất nhiều năm, mài cẩn thận kiên nhẫn cũng lấp lánh như bảo thạch!<br> ",
    "Speaking of stones, I am sure there are all sorts of stones in the<br>Abyss that you can't see on the surface...<br> ": "Nói đến đá, chắc Đại Huyệt có nhiều loại đá không thấy trên mặt đất...<br> ",
    "Yeah. I wonder what kind of stones are in the Abyss...<br> ": "Ừ. Đại Huyệt có đá gì ta cũng tò mò...<br> ",
    "......<br> ": "…………<br> ",
    "W-wah!? I-I'm sorry, I got carried away all by myself! In front of the<br>Lord Comma...<br> ": "W-wah!? X-xin lỗi, em say sưa một mình! Trước mặt Chỉ Huy...<br> ",
    "No, it's fine. Having something you can get so into is a good thing.<br> ": "Không sao. Có thứ mình say mê là tốt.<br> ",
    "So you know all about stones, then?<br> ": "Vậy em rành về đá hết à?<br> ",
    "Of course! But a hobby like this is completely useless on the<br>battlefield...<br> ": "Tự nhiên ạ! Nhưng sở thích này trên chiến trường không ích gì...<br> ",
    "...Betty.<br> ": "...Betty.<br> ",
    "No, I can't just mope around! Starting tomorrow, I'll work hard again!<br> ": "Không, không thể buồn bã mãi! Từ mai em sẽ cố gắng lại!<br> ",
    "Are you okay?<br> ": "Được chứ?<br> ",
    "Of course! Enthusiasm is the only thing I have going for me! So you<br>too must...<br> ": "Chắc chắn! Em chỉ có nhiệt huyết thôi! Chỉ Huy cũng phải...<br> ",
    "Heh. Yeah, I guess so.<br> ": "Hự. Ừ, cũng đúng.<br> ",
    "Well then, I shall take my leave!<br> ": "Vậy em xin phép lui!<br> ",
    "...Hold on a second.<br> ": "...Chờ đã.<br> ",
    "Yes? What is it?<br> ": "Vâng? Có chi ạ?<br> ",
    "Betty, would you come with me for a bit?<br> ": "Betty, em đi cùng ta chút được không?<br> ",
    "?<br> ": "?<br> ",
}

# Source and destination paths
en_path = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt"
vi_path = "E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10500100001.txt"
work_dir = "E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10500100001_full"

def build_vi():
    # Read EN asset as binary to preserve BOM and CRLF
    with open(en_path, 'rb') as f:
        en_bytes = f.read()
    
    has_bom = en_bytes.startswith(b'\xef\xbb\xbf')
    text = en_bytes.decode('utf-8-sig')
    has_crlf = '\r\n' in text
    lines = text.splitlines(keepends=True)  # preserve line endings
    
    # Find all text records
    text_cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
    asset_texts = []
    
    for i, line in enumerate(lines):
        for cmd in text_cmds:
            if line.startswith(cmd):
                raw = line
                ending = ''
                if raw.endswith('\r\n'):
                    ending = '\r\n'
                    raw = raw[:-2]
                elif raw.endswith('\n'):
                    ending = '\n'
                    raw = raw[:-1]
                
                if cmd == 'title,':
                    parts = raw.split(',', 2)
                    en_text = parts[1] if len(parts) > 1 else ''
                    speaker = ''
                else:
                    parts = raw.split(',', 3)
                    en_text = parts[2] if len(parts) > 2 else ''
                    speaker = parts[1] if len(parts) > 1 else ''
                
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
    
    print(f"Total text records found: {len(asset_texts)}")
    
    # Verify count
    expected = 80
    assert len(asset_texts) == expected, f"Expected {expected} records, got {len(asset_texts)}"
    
    # Build VI lines
    vi_lines = lines[:]
    translated_count = 0
    
    for at in asset_texts:
        en_text = at['en_text']
        cmd = at['cmd']
        
        # Look up translation
        vi_text = VI.get(en_text)
        
        if vi_text is None:
            # Try without trailing <br> for message fields
            if en_text.endswith('<br> '):
                key = en_text[:-5]
                vi_text = VI.get(key)
                if vi_text and not vi_text.endswith('<br> '):
                    vi_text = vi_text.rstrip() + '<br> '
        
        if vi_text is None:
            print(f"WARNING: No translation for line {at['line_idx']+1}: {en_text[:60]}...")
            vi_text = en_text
        else:
            translated_count += 1
        
        # Replace commas in VI text with U+201A
        vi_text_fixed = vi_text.replace(',', '\u201a')
        
        # Rebuild line
        raw = at['raw_line'].rstrip('\r\n')
        if cmd == 'title':
            parts = raw.split(',', 2)
            parts[1] = vi_text_fixed
            new_raw = ','.join(parts)
        elif cmd in ('message', 'messageTextUnder', 'messageTextCenter'):
            parts = raw.split(',', 3)
            parts[2] = vi_text_fixed
            new_raw = ','.join(parts)
        else:
            new_raw = raw
        
        vi_lines[at['line_idx']] = new_raw + at['ending']
    
    print(f"Translated {translated_count}/{len(asset_texts)} records")
    assert translated_count == len(asset_texts), f"Only {translated_count}/{len(asset_texts)} translated"
    
    # Write VI output preserving BOM and CRLF
    output_text = ''.join(vi_lines)
    output_bytes = output_text.encode('utf-8')
    if has_bom:
        output_bytes = b'\xef\xbb\xbf' + output_bytes
    
    os.makedirs(os.path.dirname(vi_path), exist_ok=True)
    with open(vi_path, 'wb') as f:
        f.write(output_bytes)
    
    print(f"Written VI output to: {vi_path}")
    print(f"BOM preserved: {has_bom}")
    print(f"CRLF preserved: {has_crlf}")
    print(f"Line count: {len(vi_lines)} (EN: {len(lines)})")
    assert len(vi_lines) == len(lines), "Line count mismatch!"
    
    # Write work copy
    os.makedirs(work_dir, exist_ok=True)
    work_vi = os.path.join(work_dir, "hmn_10500100001_vi.txt")
    with open(work_vi, 'wb') as f:
        f.write(output_bytes)
    print(f"Work copy: {work_vi}")
    
    # Generate focused diff
    diff_path = os.path.join(work_dir, "focused_diff.md")
    with open(diff_path, 'w', encoding='utf-8') as f:
        f.write("# Focused Diff: hmn_10500100001\n\n")
        f.write("| Line | Command | Speaker | EN Text | VI Text |\n")
        f.write("|------|---------|---------|---------|--------|\n")
        for at in asset_texts:
            line_no = at['line_idx'] + 1
            en = at['en_text'].replace('\n', '\\n').replace('|', '\\|')
            vi = VI.get(at['en_text'], VI.get(at['en_text'].rstrip('<br> '), ''))
            vi = vi.replace('\n', '\\n').replace('|', '\\|')
            f.write(f"| {line_no} | {at['cmd']} | {at['speaker']} | {en[:60]} | {vi[:60]} |\n")
    print(f"Focused diff: {diff_path}")
    
    # Generate manifest.json
    manifest = {
        "scene": "hmn_10500100001",
        "total_lines": len(lines),
        "text_records": len(asset_texts),
        "translated_records": translated_count,
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
        "notes": "Title field JP->VI Title Case. messageTextCenter Title Case. EN->VI for messages. Speaker labels (field 1) kept JP verbatim. All 6 fields preserved. <br> suffix mirrored on message fields.",
    }
    manifest_path = os.path.join(work_dir, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Manifest: {manifest_path}")
    
    # Generate QA log (pre-verification)
    qa_log = {
        "scene": "hmn_10500100001",
        "total_text_records": len(asset_texts),
        "translated_records": translated_count,
        "preflight_checks": {
            "line_count_match": len(vi_lines) == len(lines),
            "bom_preserved": has_bom,
            "crlf_preserved": has_crlf,
            "all_records_translated": translated_count == len(asset_texts),
        },
        "independent_verify": "PENDING",
    }
    qa_path = os.path.join(work_dir, "qa_log.json")
    with open(qa_path, 'w', encoding='utf-8') as f:
        json.dump(qa_log, f, ensure_ascii=False, indent=2)
    print(f"QA log: {qa_path}")

if __name__ == "__main__":
    build_vi()
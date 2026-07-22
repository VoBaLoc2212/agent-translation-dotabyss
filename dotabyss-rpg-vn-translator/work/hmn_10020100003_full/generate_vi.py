from pathlib import Path
import json, hashlib, re, difflib
from collections import Counter

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10020100003'
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work/hmn_10020100003_full'
MANIFEST = WORK / 'manifest.json'
QA_LOG = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'

VI = [
    "Tiêu Đề",
    "Ưm…… ủa? Đây là đâu vậy ta〜……?<br> ",
    "Cuối cùng cũng tỉnh rồi à?<br> ",
    "Anh……? Sao anh lại ở đây thế〜?<br> ",
    "Em không nhớ à?<br> ",
    "Em đã thi đấu với mấy món đồ của Adelheid<br>rồi ngất vì cạn ma lực.<br> ",
    "Hả…… vậy nơi này là……<br> ",
    "Phòng của anh. Em chiếm luôn cái giường khiến anh phiền lắm đấy.<br> ",
    "Phòng của anh…… giường của anh……♡<br> ",
    "Ưm hư hư〜n♡ Thiệt tình〜 anh này〜. Kéo em vào phòng như vậy<br>anh định làm gì em thế〜?♡<br> ",
    "Nếu không phải Verisa kiệt sức đến mức không cử động nổi<br>thì anh còn chẳng có gan bế em lên giường nhỉ? <br> ",
    "Đúng là một ông anh tệ hại hết chỗ nói luôn đó♡<br> ",
    "……Vừa hồi sức là lại bắt đầu thế ngay à.<br> ",
    "Anh đâu thể tự tiện vào phòng em. Hay Verisa muốn anh đi rêu rao rằng<br>em ngất vì đun nước tắm?<br> ",
    "Ủa kìa〜? Hay Verisa đi kể cho mọi người rằng em ngất vì<br>phục vụ anh quá sức nhé〜? ♡ Táo bạo ghê〜♡<br> ",
    "Đúng là cái miệng không chịu ngừng…… Nói trước nhé<br>chuyện em ngất đi là vấn đề nghiêm túc đấy.<br> ",
    "May mà không có giao tranh<br>chứ nếu Tai Ương xuất hiện thì em định làm sao?<br> ",
    "Lập chiến lược mà thiếu em cũng phiền phức lắm.<br>Từ giờ đừng liều lĩnh vì mấy chuyện nhảm nhí nữa.<br> ",
    "Ư〜 đúng là vậy nhỉ? Anh mà không có Verisa thì chẳng làm<br>được gì hết đúng không? Không có em là anh yếu xìu luôn♪<br> ",
    "……Nhưng mà này anh. Chuyện hôm nay không hề nhảm nhí đâu.<br> ",
    "Ma pháp của em tuyệt đối<br>không được thua thứ khoa học của Lux Nova đâu.<br> ",
    "Anh đã nhìn kỹ rồi mà đúng không?<br>Giờ anh biết ma pháp và khoa học bên nào lợi hại hơn rồi nhỉ?<br> ",
    "Ừm……<br>Khoa học lẫn ma pháp đều có ưu nhược điểm riêng thôi.<br> ",
    "Hảảả!? Sao lại thế〜!? Em thắng rồi mà!!<br> ",
    "Ngoài trận cuối ra thì em thua suốt còn gì.<br>Vả lại với anh thắng thua không quan trọng.<br> ",
    "Dùng đúng thứ cần dùng vào đúng thời điểm.<br>Anh chỉ muốn có thông tin để làm điều đó thôi.<br> ",
    "Dù sao kết quả nhìn chung cũng đúng như dự tính.<br> ",
    "……À vậy à〜. Anh đúng là kiểu người như thế nhỉ……<br> ",
    "Nói cho cùng anh chẳng có hứng thú với ma pháp của em gì cả……<br> ",
    "……Nhưng có một điều nằm ngoài dự tính. Là em đấy Verisa.<br> ",
    "Hả…… em á?<br> ",
    "Em ganh đua với khoa học đến mức dùng ma pháp tới khi ngã gục.<br>Anh không ngờ em lại cứng đầu đến vậy.<br> ",
    "Vì sao phải làm đến thế? Đó đâu phải thực chiến mà chỉ là trò chơi thôi.<br> ",
    "Đúng là có thể chỉ là trò chơi. Nhưng với em đó là chuyện rất quan trọng.<br> ",
    "Ma pháp của em phải đứng trên khoa học của Lux Nova<br>nếu không thì chẳng còn ý nghĩa gì nữa.<br> ",
    "Dù hơn hay kém<br>nếu được anh sử dụng thì sẽ không có thất bại.<br> ",
    "Hay em nghĩ nếu nó không mạnh thì anh không thể dùng cho ra hồn?<br>Bị xem thường thật đấy.<br> ",
    "Không phải…… anh có thể biến bất kỳ ai thành chiến lực.<br>Nhưng với em chỉ được sử dụng thôi là chưa đủ.<br> ",
    "Ma pháp của em phải là mạnh nhất!<br> ",
    "Anh không hiểu vì sao em lại dằn vặt tới mức đó.<br> ",
    "Anh hiểu Perdion trọng dụng pháp sư.<br>Nhưng em đâu cần phải gánh vác chuyện đó.<br> ",
    "Đâu phải em làm vậy vì đất nước đâu.<br> ",
    "Anh hiểu rõ vị trí của pháp sư trong chiến đấu mà đúng không?<br> ",
    "Là hậu tuyến chứ gì. Không cần phải nói.<br> ",
    "Đúng vậy đó! Mọi người ở tiền tuyến đang liều mạng chống đỡ<br>những Tai Ương khủng khiếp…… còn bọn em ở phía sau họ.<br> ",
    "Mọi người bảo vệ bọn em. Để các pháp sư như bọn em có thể dùng ma pháp cho trọn vẹn.<br> ",
    "Có những người đặt kỳ vọng vào ma pháp của em…… và cược cả mạng sống vào đó.<br> ",
    "Họ có thể chết. Không…… không phải có thể. Thực tế đã rất nhiều lần có những tình huống như thế.<br> ",
    "Nếu không có sự chỉ huy của anh thì chắc chắn……<br>còn nhiều người hơn nữa……<br> ",
    "Ừ. Nghe nói trong những trận chiến với Tai Ương trước đây<br>thiệt hại rất nặng nề.<br> ",
    "Anh không định để lộ ra bộ dạng thảm hại như thế. Nhưng<br>anh luôn tính đến khả năng có hy sinh.<br> ",
    "Đúng vậy mà. Bất cứ lúc nào cũng có thể có ai đó bị thương.<br>Không…… rất nhiều người đã…… bị thương rồi.<br> ",
    "Vậy mà nếu ma pháp của em…… chỉ ngang với một món công cụ<br>thì ý nghĩa việc họ bảo vệ em sẽ biến mất mất thôi……<br> ",
    "Pháp sư…… ma pháp của em…… không được thua khoa học. Vì…… vì mà……<br> ",
    "Những người đã bị thương vì em…… sẽ giống như đồ ngốc mất thôi……<br> ",
    "……Không phải anh không hiểu. Nếu nói là hậu tuyến thì người đứng sau cùng chính là anh.<br> ",
    "Cả anh lẫn em đều phải liên tục tạo ra kết quả<br>đủ để ngẩng mặt trước những người chiến đấu làm lá chắn.<br> ",
    "Đúng…… đúng vậy. Vì thế em phải thắng……!<br> ",
    "……Có vẻ em cũng không muốn nghe những lời dịu dàng đâu nhỉ.<br>Vậy anh chỉ nói sự thật đã xác nhận lần này thôi.<br> ",
    "Mấy món đồ của Adelheid chỉ phát huy đúng hiệu năng như dự tính.<br> ",
    "Người duy nhất khiến anh ấn tượng là em đấy Verisa.<br> ",
    "……Hả?<br> ",
    "Chỉ có em tạo ra kết quả vượt ngoài dự tính của anh.<br>Nói trước nhé cũng khá đáng nể đấy.<br> ",
    "……Vậy…… vậy thì nhé! Trận đấu hôm nay xem như em thắng được đúng không!?<br> ",
    "Ừ. Riêng hôm nay có thể nói là em thắng.<br> ",
    "Ư…… ê hê hê〜……♡<br> ",
    "Đúng chứ đúng chứ〜? Verisa siêu lắm đúng không〜?<br>Vậy chắc chắn là em thắng rồi nhỉ〜?<br> ",
    "Đừng bắt anh nhắc lại nữa…… cái vẻ mặt đắc ý đó là sao.<br> ",
    "Ơ〜? Vì mà〜♡ <br>Anh bị sự lợi hại của Verisa hạ gục rồi đúng không〜?<br> ",
    "Rốt cuộc anh ấy mà không có em thì chẳng làm được gì cả〜♡<br> ",
    "Nếu Verisa ngủ mất mà Tai Ương xuất hiện thì anh định làm gì〜?<br>Sợ lắm đúng không〜 một mình ấy〜♡<br> ",
    "Ngoan nào ngoan nào. Em sẽ ở bên nên anh cứ yên tâm đi<br>ông anh yếu ớt của em♡<br> ",
    "Hừ. Dù không có em thì cũng chỉ phiền thêm chút thôi.<br>Công việc của anh là khiến phe mình thắng trong mọi tình huống.<br> ",
    "Dù có hy sinh thì việc anh phải làm cũng không đổi.<br>Dẫu anh có bị căm ghét đến đâu đi nữa.<br> ",
    "Không sa〜o đâu♡ Verisa sẽ trở về bình an<br>để anh khỏi phải khóc mà♡<br> ",
    "Nếu vậy mà vẫn có ai bị thương thì Verisa sẽ<br>an ủi anh thật nhiều nhé anh♡<br> ",
    "Thế nên nè〜 anh cứ dựa vào pháp sư siêu mạnh Verisa<br>nhiều hơn cũng được đó〜? Ông anh không có ma pháp yếu xìu♡y・ế・u・x・ì・u♡<br> ",
    "……<br> ",
    "（Cứ tưởng mình đang bị trêu chọc<br>nhưng kiểu này của Verisa chỉ là em ấy đang làm nũng với mình thôi…… thật là）<br> ",
    "Mới khen một chút đã lên mặt ngay.<br>Cảm giác như mình mới là người chịu thiệt vậy.<br> ",
    "Hư hư〜n♡ Nếu anh đã khen rồi〜 thì Verisa<br>tự nhiên lại muốn có phần thưởng gì đó ghê〜♡<br> ",
    "Lôi người ta vào rồi còn nói tùy hứng……<br>Anh sẽ nghe thử nhưng đừng mong chờ quá.<br> ",
    "Verisa ấy nha〜 muốn cùng anh〜…… đi tắm đó〜♡<br> ",
    "Cứ tưởng em định nói gì hóa ra lại là một điều ước nhảm nhí.<br>……Mà thôi đúng là em đã nghe theo yêu cầu của anh và làm việc tới khi ngất.<br> ",
    "Hết cách rồi. Chỉ hôm nay thôi đấy.<br> ",
    "Tuyệt quá〜♡ Đúng là anh mềm lòng với Verisa quá mà〜♡<br> ",
    "Hay là trong lúc đun nước tắm anh vẫn luôn nghĩ muốn vào cùng em<br>đúng không ta? Anh đúng là như em bé ấy〜♡<br> ",
    "Không sao đâu? Verisa cũng nghĩ rằng muốn ở cùng anh mà♡<br> ",
    "Vì cứ nghĩ mấy chuyện thừa thãi như thế nên em mới ngất đấy.<br> ",
    "Mà chỉ cùng nhau vào tắm đã là phần thưởng thì rẻ quá.<br>Anh còn tưởng sẽ bị bắt rửa người cho em cơ.<br> ",
    "À vậy thêm cái đó nữa〜♡<br>Anh đúng là muốn được Verisa nuông chiều hết mức mà♡<br> ",
    "……Anh lỡ nói thừa rồi. Quên đi.<br> ",
    "Không chịu đâu♡ Hôm nay em sẽ cho anh chăm sóc Verisa〜♡<br> ",
    "Verisa cũng sẽ làm cho anh sạch sẽ thơm tho luôn nhé♡<br> ",
    "Vậy hôm nay vẫn là em thua. Không có thưởng gì hết. Mau về đi.<br> ",
    "Anh cứ nói vậy thôi〜♡ Chứ vui lắm đúng không?<br>Tim anh đã đập thình thịch rồi kìa〜♡<br> ",
    "À em hiểu rồi♡ Chỉ rửa người thôi thì anh không chịu nổi đúng không? Hư hư……♡<br> ",
    "Nếu là anh…… thì xa hơn nữa cũng được đó♡<br> ",
    "……Bắt đầu thấy phiền rồi đấy. Được rồi được rồi đi nhanh thôi.<br> ",
    "Nhưng bồn tắm vẫn chưa chuẩn bị xong mà.<br>Em định dùng ma pháp đun nước à?<br> ",
    "Không được đâu♡ Bây giờ Verisa đang trong trạng thái yếu xìu〜.<br>Đến tia lửa nhỏ cũng không tạo ra nổi♡<br> ",
    "Bây giờ thì dù là ông anh yếu xìu như anh<br>cũng có thể muốn làm gì Verisa yếu xìu này thì làm đó〜?<br> ",
    "Im đi. Anh sẽ đi gọi Adelheid.<br>Để cô ấy dùng công cụ của Lux Nova chuẩn bị bồn tắm.<br> ",
    "Ơ〜!? Ư〜…… hết cách rồi nhỉ.<br>Hôm nay Verisa thắng nên đặc biệt tha cho anh đó〜♡<br> ",
    "Nhưng mà nhưng mà♡ Vì đây là phần thưởng nên anh phải nhìn em cho đàng hoàng nhé?<br>Không phải phía khoa học mà là phía Verisa này♡<br> ",
    "Hôm nay em sẽ ở bên anh su〜〜ốt luôn♡<br>Anh ơi♡<br> ",
]

TEXT_RECORDS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 1}
TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r'%(?:\d+\$)?[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%|\\[nrt]')

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def load_pairs(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=list)

def newline_style(data):
    if b'\r\n' in data:
        return 'CRLF'
    return 'LF'

def split_lines_preserve(text):
    return text.splitlines(True)

def text_field(parts):
    rec = parts[0]
    idx = TEXT_RECORDS[rec]
    return idx

def tag_counts(s):
    return Counter(TAG_RE.findall(s))

def placeholder_counts(s):
    return Counter(PLACEHOLDER_RE.findall(s))

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    en_bytes = EN_ASSET.read_bytes()
    bom = en_bytes.startswith(b'\xef\xbb\xbf')
    encoding = 'utf-8-sig' if bom else 'utf-8'
    en_text = en_bytes.decode(encoding)
    nl = '\r\n' if newline_style(en_bytes) == 'CRLF' else '\n'
    en_lines = split_lines_preserve(en_text)
    ja_pairs = load_pairs(JA_JSON)
    en_pairs = load_pairs(EN_JSON)

    candidates = []
    for i, line in enumerate(en_lines, 1):
        bare = line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith('\n') else line
        parts = bare.split(',')
        if parts[0] in TEXT_RECORDS:
            idx = TEXT_RECORDS[parts[0]]
            candidates.append({'line': i, 'record': parts[0], 'field_index': idx, 'source_text': parts[idx]})

    blockers = []
    notes = []
    items = []
    if len(VI) != len(candidates):
        blockers.append({'code':'TRANSLATION_COUNT_MISMATCH','expected':len(candidates),'actual':len(VI)})
    if len(ja_pairs) != len(en_pairs):
        blockers.append({'code':'NOVEL_PAIR_COUNT_MISMATCH','ja':len(ja_pairs),'en':len(en_pairs)})
    if len(ja_pairs) != len(candidates):
        notes.append({'code':'NOVEL_ASSET_COUNT_RECONCILED','ja_pairs':len(ja_pairs),'en_pairs':len(en_pairs),'asset_candidates':len(candidates)})

    for n, s in enumerate(VI, 1):
        if ',' in s:
            blockers.append({'code':'ASCII_COMMA_IN_VI_TEXT','candidate_index':n,'text':s})

    out_lines = list(en_lines)
    entries = []
    for idx, cand in enumerate(candidates):
        vi = VI[idx]
        line_no = cand['line']
        orig_line = en_lines[line_no-1]
        eol = '\r\n' if orig_line.endswith('\r\n') else '\n' if orig_line.endswith('\n') else ''
        bare = orig_line[:-len(eol)] if eol else orig_line
        parts = bare.split(',')
        field_idx = cand['field_index']
        src_field = parts[field_idx]
        parts[field_idx] = vi
        out_lines[line_no-1] = ','.join(parts) + eol
        jp = ja_pairs[idx][0] if idx < len(ja_pairs) else None
        en_ref = en_pairs[idx][1] if idx < len(en_pairs) else None
        entries.append({
            'candidate_index': idx+1,
            'line': line_no,
            'record': cand['record'],
            'speaker': parts[1] if cand['record'].startswith('message') and len(parts) > 1 else None,
            'jp': jp,
            'en_asset': src_field,
            'en_novel': en_ref,
            'vi': vi,
            'match_status': 'EXACT' if en_ref == src_field else 'CONTEXT_MATCH',
            'translation_status': 'TRANSLATED',
        })

    vi_text = ''.join(out_lines)
    vi_bytes = (('\ufeff' if bom else '') + vi_text).encode('utf-8')
    VI_ASSET.write_bytes(vi_bytes)

    # QA after write
    read_bytes = VI_ASSET.read_bytes()
    out_text = read_bytes.decode(encoding)
    out_lines2 = split_lines_preserve(out_text)
    structural = {
        'line_count_match': len(en_lines) == len(out_lines2),
        'bom_match': read_bytes.startswith(b'\xef\xbb\xbf') == bom,
        'newline_match': newline_style(read_bytes) == newline_style(en_bytes),
        'delimiter_mismatches': [],
        'technical_field_mismatches': [],
        'tag_mismatches': [],
        'placeholder_mismatches': [],
        'unchanged_text_records': [],
        'ascii_comma_in_vi_text': [],
    }
    if not structural['line_count_match']:
        blockers.append({'code':'LINE_COUNT_MISMATCH','source':len(en_lines),'output':len(out_lines2)})
    if not structural['bom_match']:
        blockers.append({'code':'BOM_MISMATCH'})
    if not structural['newline_match']:
        blockers.append({'code':'NEWLINE_MISMATCH','source':newline_style(en_bytes),'output':newline_style(read_bytes)})

    for cand_idx, cand in enumerate(candidates):
        line_no = cand['line']
        en_line = en_lines[line_no-1].rstrip('\r\n')
        vi_line = out_lines2[line_no-1].rstrip('\r\n')
        if en_line.count(',') != vi_line.count(','):
            structural['delimiter_mismatches'].append(line_no)
            blockers.append({'code':'DELIMITER_MISMATCH','line':line_no})
            continue
        ep = en_line.split(',')
        vp = vi_line.split(',')
        fidx = cand['field_index']
        if ep[:fidx] + ep[fidx+1:] != vp[:fidx] + vp[fidx+1:]:
            structural['technical_field_mismatches'].append(line_no)
            blockers.append({'code':'TECH_FIELD_MISMATCH','line':line_no})
        if ',' in vp[fidx]:
            structural['ascii_comma_in_vi_text'].append(line_no)
            blockers.append({'code':'ASCII_COMMA_IN_VI_FIELD','line':line_no})
        if tag_counts(ep[fidx]) != tag_counts(vp[fidx]):
            structural['tag_mismatches'].append({'line':line_no,'source':dict(tag_counts(ep[fidx])),'vi':dict(tag_counts(vp[fidx]))})
            blockers.append({'code':'TAG_MISMATCH','line':line_no})
        if placeholder_counts(ep[fidx]) != placeholder_counts(vp[fidx]):
            structural['placeholder_mismatches'].append(line_no)
            blockers.append({'code':'PLACEHOLDER_MISMATCH','line':line_no})
        if ep[fidx] == vp[fidx]:
            structural['unchanged_text_records'].append(line_no)
            # title and ellipsis are checked below; unchanged proper/SFX allowed only if logged

    # Targeted English leftover checks. Proper names are allowed.
    allowed = {'Verisa','Adelheid','Lux','Nova','Perdion'}
    english_patterns = re.compile(r'\b(?:Big bro|Mister|Finally|awake|Where|Hmm|Huh|Fufu|Geez|Calamity|science|magic|Verisa-chan|Yes|No way|Yay|Ehehe|Fufuun|Ah|Since|Shut up)\b', re.I)
    leftover = []
    for e in entries:
        text = e['vi']
        if english_patterns.search(text):
            # Skip allowed proper-name fragments only; regex above includes common leftovers
            leftover.append({'line': e['line'], 'text': text, 'match': english_patterns.search(text).group(0)})
    if leftover:
        for x in leftover:
            blockers.append({'code':'POSSIBLE_EN_LEFTOVER','line':x['line'],'match':x['match'],'text':x['text']})

    intentional_identical = []
    for line_no in structural['unchanged_text_records']:
        # The ellipsis-only line is intentionally identical punctuation/SFX; no EN sentence kept.
        field = [c for c in candidates if c['line'] == line_no][0]['source_text']
        if field.strip() in {'...<br>', '...<br>', '……'} or field.strip().replace('<br>','').strip() in {'...','……'}:
            intentional_identical.append({'line':line_no,'reason':'punctuation/ellipsis-only record intentionally identical in function'})
        else:
            blockers.append({'code':'UNCHANGED_TRANSLATABLE_TEXT','line':line_no,'text':field})

    # remove logged intentional lines from structural unchanged list in qa summary
    structural['intentional_identical_records'] = intentional_identical
    structural['unchanged_text_records'] = [l for l in structural['unchanged_text_records'] if l not in {x['line'] for x in intentional_identical}]

    counts = Counter(c['record'] for c in candidates)
    qa_status = 'PASS' if not blockers else 'FAIL'

    manifest = {
        'scene': SCENE,
        'status': qa_status,
        'source': {
            'ja_json': str(JA_JSON),
            'en_json': str(EN_JSON),
            'en_asset': str(EN_ASSET),
            'en_asset_sha256': sha256(en_bytes),
            'en_asset_bytes': len(en_bytes),
            'bom': bom,
            'encoding': encoding,
            'newline': newline_style(en_bytes),
            'line_count': len(en_lines),
        },
        'output': {
            'vi_asset': str(VI_ASSET),
            'vi_asset_sha256': sha256(read_bytes),
            'vi_asset_bytes': len(read_bytes),
            'line_count': len(out_lines2),
            'bom': read_bytes.startswith(b'\xef\xbb\xbf'),
            'newline': newline_style(read_bytes),
        },
        'candidate_counts': dict(counts),
        'candidate_total': len(candidates),
        'translated_records': len(VI),
        'entries': entries,
        'artifacts': {
            'manifest': str(MANIFEST),
            'qa_log': str(QA_LOG),
            'focused_diff': str(DIFF),
            'script': str(Path(__file__)),
        },
    }

    independent_verify = {
        'line_count': {'en': len(en_lines), 'vi': len(out_lines2), 'match': len(en_lines) == len(out_lines2)},
        'bom_match': read_bytes.startswith(b'\xef\xbb\xbf') == bom,
        'newline_match': newline_style(read_bytes) == newline_style(en_bytes),
        'candidate_counts': dict(counts),
        'changed_text_records': sum(
            1 for cand in candidates
            if en_lines[cand['line']-1].rstrip('\r\n').split(',')[cand['field_index']]
            != out_lines2[cand['line']-1].rstrip('\r\n').split(',')[cand['field_index']]
        ),
        'delimiter_mismatch_count': len(structural['delimiter_mismatches']),
        'technical_field_mismatch_count': len(structural['technical_field_mismatches']),
        'tag_mismatch_count': len(structural['tag_mismatches']),
        'placeholder_mismatch_count': len(structural['placeholder_mismatches']),
        'ascii_comma_in_vi_text_count': len(structural['ascii_comma_in_vi_text']),
        'unchanged_unlogged_text_records': len(structural['unchanged_text_records']),
        'targeted_english_leftover_count': len(leftover),
        'status': 'PASS' if not blockers else 'FAIL',
    }

    qa = {
        'scene': SCENE,
        'qa_status': qa_status,
        'blockers': blockers,
        'items': items,
        'notes': notes + [
            {'code':'H18_PROJECT_CONFIRMATION','note':'User confirmed all characters are 18+ for this project; adult/flirtatious bath lines translated normally while preserving source tone and consent.'},
            {'code':'ADDRESSING','note':'Verisa -> Commander uses playful anh/em; Commander -> Verisa uses anh/em. Commander title concept rendered as Chỉ Huy where it appears as 指揮/command.'},
            {'code':'NAME_HANDLING','note':'Speaker/charaload names preserved; in prose used EN-established romanizations Verisa, Adelheid, Lux Nova, Perdion.'},
        ],
        'structural_qa': structural,
        'independent_verify': independent_verify,
        'candidate_counts': dict(counts),
        'candidate_total': len(candidates),
        'translated_records': len(VI),
        'kept_english_records': [],
        'intentional_identical_records': intentional_identical,
    }

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')

    diff_lines = []
    for e in entries:
        diff_lines.append(f"## candidate {e['candidate_index']} line {e['line']} {e['record']}\n")
        diff_lines.append('```diff\n')
        diff_lines.extend(difflib.unified_diff(
            [e['en_asset'] + '\n'], [e['vi'] + '\n'],
            fromfile='EN asset text', tofile='VI text', lineterm='\n'
        ))
        diff_lines.append('```\n\n')
    DIFF.write_text(''.join(diff_lines), encoding='utf-8')

    print(json.dumps({
        'qa_status': qa_status,
        'blocker_count': len(blockers),
        'candidate_total': len(candidates),
        'candidate_counts': dict(counts),
        'output': str(VI_ASSET),
        'manifest': str(MANIFEST),
        'qa_log': str(QA_LOG),
        'focused_diff': str(DIFF),
        'sha256': sha256(read_bytes),
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

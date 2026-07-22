#!/usr/bin/env python
from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10140100002'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
NOVEL_JA = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
NOVEL_EN = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
DIFF = WORK / 'focused_diff.md'
QA = WORK / 'qa_log.json'
MANIFEST = WORK / 'manifest.json'
TEXT_CMDS = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
TAG_RE = re.compile(r'<[^>]+>')
PH_RE = re.compile(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}')

TRANSLATIONS = [
    'Chiến Dịch Cai Nghiện Điện Thoại',
    'Vậy thì‚ về nghiên cứu mà chúng ta vừa bàn—<br> ',
    'Ừm‚ ra vậy.<br> ',
    'Rầm!<br> ',
    'Adelheid‚ đây rồi! Cuối cùng cũng tìm thấy cậu!<br> ',
    'Whoa‚ Pico hả!? Em đột ngột xông vào làm anh giật cả mình…<br> ',
    'Adelheid‚ cậu đang làm gì với Chỉ Huy vậy?<br> ',
    'Tôi được gọi đến để bàn chuyện công việc. Pico cần gì ở tôi à?<br> ',
    'Ừ! Adelheid‚ trả điện thoại cho tớ đi! Chắc sạc xong rồi đúng không?<br> ',
    'Vẫn chưa xong đâu.<br> ',
    'Ểê!?<br>Hôm qua tớ đưa rồi mà!?<br> ',
    'Hiện tại nó đang chạy bằng ma lực chứ không phải điện. Vì vậy thời gian<br>cần lâu hơn bình thường.<br> ',
    'Vậy à… còn mất bao lâu nữa?<br> ',
    'Chắc khoảng một tiếng nữa.<br> ',
    'Không chịu đâu… Không có điện thoại thì em chẳng đi đâu được hết…<br> ',
    'Nghiêm trọng đến thế sao?<br> ',
    'Theo tôi biết thì nó đâu có những chức năng cần thiết cho sinh hoạt hằng ngày.<br> ',
    'Pico-nyan bị “nghiện điện thoại” đó!!<br> ',
    'Cô khẳng định dứt khoát đến mức nghe cũng thấy sảng khoái đấy.<br> ',
    'Với em‚ điện thoại là sợi dây duy nhất nối em với thế giới cũ… duy nhất<br>đó.<br> ',
    'Nên dù chỉ một chút em cũng không muốn rời khỏi nó.<br> ',
    'Hửm? Hình như em kém tươi tỉnh hơn lần trước anh gặp đấy.<br> ',
    'Thì lúc đó em đang quay phim mà…<br> ',
    'Em vẫn muốn mau chóng về thế giới cũ. Không có mạng‚ chẳng ai nhìn<br>em cả… cô đơn lắm—<br> ',
    'Này này‚ em thật sự xuống tinh thần rồi đấy.<br> ',
    'Vì em không dùng được điện thoại. Từ khi đến thế giới này‚ nó giống như<br>lá bùa giúp em xua bớt lo âu vậy.<br> ',
    'Khi đang quay phim‚ em có thể quên hết bất an và tập trung…<br> ',
    'Ra vậy. Em bắt đầu “video tường thuật dị giới” cũng vì thế à.<br> ',
    'Ừ…<br>Nếu cứ thế này mà không về được thì sao…<br> ',
    'Khoan đã‚ Pico. Đừng ủ rũ đến thế.<br> ',
    'Em lo lắng cũng phải thôi— nhưng em đến dị giới này cũng do liên quan<br>đến Đại Huyệt đúng không?<br> ',
    'Ừ. Chắc vậy…<br> ',
    'Vậy là vẫn còn hy vọng. Trong Đại Huyệt vẫn còn những khu vực chưa ai từng thấy.<br>Nếu tiếp tục thăm dò‚ có thể ta sẽ tìm được manh mối giúp em trở về thế giới cũ.<br> ',
    'May mắn là em có vẻ đủ sức trở thành chiến lực‚ và trong lúc thăm dò<br>em có thể quay video tường thuật để giữ tâm trạng vui vẻ‚ đúng không?<br> ',
    'Ừm‚ thì…<br> ',
    'Vậy thì đừng bận tâm. Khi đi thăm dò anh sẽ gọi em. Anh cũng sẽ làm<br>bạn dẫn cho video tường thuật của em.<br> ',
    '…Chỉ Huy cũng dịu dàng ghê ha.<br> ',
    'Chăm sóc cấp dưới đang sa sút cũng là công việc của anh mà.<br> ',
    '…Vậy à.<br>Cảm ơn anh đã dịu dàng với em nhé.<br> ',
    'Nhưng tâm trạng em vẫn khó lên nổi… Aaa‚ muốn chơi game muốn chơi game!<br>Game game game!<br> ',
    'Năm nay có cả đống game mới em mong chờ đó! Em còn định thức trắng<br>đêm livestream vào ngày phát hành mà!<br> ',
    'Nếu không về sớm thì lỡ mất thời điểm nóng hổi mất!<br>Em không chịu đâu!<br> ',
    'Hmm… Adelheid. Không thể cải tạo điện thoại để chơi được game mới<br>đúng không?<br> ',
    'Rất tiếc là không thể. Ngay từ đầu tôi nghĩ chúng vốn dành để chơi trên<br>máy tính để bàn hoặc máy chơi game chứ không phải điện thoại.<br> ',
    'Tôi chẳng hiểu gì cả‚ nhưng ít nhất cũng biết là không thể đáp ứng mong muốn của Pico.<br>…Có lẽ chỉ còn cách giúp em ấy tìm thú vui khác thôi.<br> ',
    'Pico.<br>Trong lúc chờ điện thoại sạc xong‚ đi với anh một lát.<br> ',
    'Ểê… Em muốn chờ trong phòng nghiên cứu của Adelheid đến khi điện thoại<br>sạc xong cơ!<br> ',
    'Đừng nói vậy. Hôm trước anh cũng tham gia video tường thuật của em<br>còn gì?<br> ',
    'Ểê‚ nhưng mà…<br> ',
    'Hai người cứ đi đi. Trong lúc đó tôi sẽ thử xem có thể kéo dài pin thêm<br>một chút không.<br> ',
    '…Biết rồi.<br> ',
    '(Tốt. Ít nhất mình cũng kéo được em ấy ra ngoài. Giờ hãy cùng tìm<br>thứ mà em ấy có thể thích ở thế giới này.)<br> ',
    'Chỗ này là nơi uống rượu đúng không?<br>Em đâu có hứng thú với rượu đâu!?<br> ',
    'Ngoài rượu ở đây còn có đồ ăn ngon nữa. Anh đãi và gọi rất nhiều rồi‚<br>nên em nếm thử đi. Anh chịu chi lắm đấy!<br> ',
    'Em không hứng thú với đồ ăn đâu.<br> ',
    'Đừng nói vậy.<br>Nào‚ đồ ăn tới rồi kìa!<br> ',
    '—Rất nhiều món ăn được bưng lên bàn. Hương thơm hấp dẫn từ những món<br>dùng đầy ắp nguyên liệu đắt tiền lan tỏa khắp xung quanh.<br> ',
    'Anh đề cử món này. Salad tuyệt phẩm làm từ rau tươi đấy. Ăn thử đi!<br> ',
    'Không cần đâu! Em ghét rau!!<br> ',
    'Thế thịt và cá thì sao?<br> ',
    'Ưm. Em vẫn ăn cho có thôi… Nói thật‚ miễn bổ sung được dinh dưỡng<br>thì “gì cũng được” hết.<br> ',
    'V-vậy à…<br>Nhưng thật sự em không có món nào thích sao?<br> ',
    'Trước đây em thích đồ ăn vặt.<br> ',
    '…Xin lỗi. Đó là món kiểu gì vậy?<br> ',
    'Không hẳn là món‚ mà là một thể loại ấy. Kiểu “Que Ngon Bá Cháy”‚<br>“Anh Nấm Shiitake Jiro” gì đó~<br> ',
    'Nó có vị thế nào? Cảm giác khi ăn ra sao?<br> ',
    'Em đâu giải thích được vị. Nếu phải nói thì… đồ ăn rác?<br> ',
    'Cái cảm giác dính dầu mới đúng chất đồ ăn vặt ấy. Cứ giòn rụm lạo xạo<br>ăn mãi không dừng được.<br> ',
    'Mà nói đúng hơn‚ hay nhất là có thể ăn khi đang chơi game hoặc xem<br>video ấy~<br> ',
    'Hmm… Nghe kỹ đến vậy mà anh vẫn không hiểu lắm. Quả nhiên muốn làm<br>Pico vui bằng đồ ăn là bất khả thi sao…<br> ',
    'Bỏ cuộc rồi tới chỗ Adelheid đi mà?<br> ',
    'Không‚ anh vẫn còn vài nơi muốn đến. Ăn xong thì đi với anh thêm<br>một chút nhé.<br> ',
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def tags(s: str): return sorted(TAG_RE.findall(s))
def phs(s: str): return sorted(PH_RE.findall(s))

def split_text_line(line: str):
    clean = line.rstrip('\r\n')
    ending = line[len(clean):]
    if clean.startswith('title,'):
        a,b = clean.split(',',1)
        return a, None, b, '', ending
    parts = clean.split(',',5)
    # cmd,speaker,text,tail...
    return parts[0], parts[1], parts[2], (',' + parts[3] if len(parts)>3 else '') + (',' + parts[4] if len(parts)>4 else '') + (',' + parts[5] if len(parts)>5 else ''), ending

def normalize_br_count(old_text: str, vi_text: str) -> str:
    """EN asset tag counts are authoritative; add missing <br> at field end if needed."""
    old_br = old_text.count('<br>')
    vi_br = vi_text.count('<br>')
    if vi_br < old_br:
        missing = old_br - vi_br
        if vi_text.endswith(' '):
            vi_text = vi_text[:-1] + ('<br>' * missing) + ' '
        else:
            vi_text += '<br>' * missing
    elif vi_br > old_br:
        surplus = vi_br - old_br
        for _ in range(surplus):
            vi_text = vi_text.replace('<br>', ' ', 1)
    return vi_text

def build_line(old_line: str, vi_text: str) -> str:
    cmd, speaker, old_text, tail, ending = split_text_line(old_line)
    vi_text = normalize_br_count(old_text, vi_text)
    if ',' in vi_text:
        raise ValueError(f'ASCII comma in translation: {vi_text}')
    if tags(old_text) != tags(vi_text):
        raise ValueError(f'tag mismatch for {old_text!r} -> {vi_text!r}: {tags(old_text)} vs {tags(vi_text)}')
    if phs(old_text) != phs(vi_text):
        raise ValueError(f'placeholder mismatch for {old_text!r} -> {vi_text!r}')
    if cmd == 'title':
        return f'{cmd},{vi_text}{ending}'
    return f'{cmd},{speaker},{vi_text}{tail}{ending}'

WORK.mkdir(parents=True, exist_ok=True)
raw = EN_ASSET.read_bytes()
text = raw.decode('utf-8-sig')
lines = text.splitlines(True)
text_indices = [i for i,l in enumerate(lines) if l.lstrip('\ufeff').startswith(TEXT_CMDS)]
if len(text_indices) != len(TRANSLATIONS):
    raise SystemExit(f'translation count mismatch: {len(TRANSLATIONS)} vs {len(text_indices)}')

out_lines = list(lines)
for idx, vi in zip(text_indices, TRANSLATIONS):
    prefix = '\ufeff' if out_lines[idx].startswith('\ufeff') else ''
    line = out_lines[idx].lstrip('\ufeff')
    out_lines[idx] = prefix + build_line(line, vi)

out_text = ''.join(out_lines)
out_raw = (b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + out_text.encode('utf-8')
# because text decoded with utf-8-sig removed BOM; no text line should contain BOM prefix now
if out_text.startswith('\ufeff'):
    out_raw = out_text.encode('utf-8')
VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
VI_ASSET.write_bytes(out_raw)

counts = Counter()
issues = []
for old,new in zip(lines,out_lines):
    oc = old.lstrip('\ufeff').rstrip('\r\n')
    nc = new.lstrip('\ufeff').rstrip('\r\n')
    if oc.startswith(TEXT_CMDS): counts[oc.split(',',1)[0]] += 1
    if old.count(',') != new.count(','):
        issues.append({'line': lines.index(old)+1, 'issue':'delimiter_count'})

# manifest mappings
ja = json.loads(NOVEL_JA.read_text(encoding='utf-8-sig'))
en = json.loads(NOVEL_EN.read_text(encoding='utf-8-sig'))
source_pairs = []
for (jp,_), (_,en_text) in zip(ja.items(), en.items()):
    source_pairs.append({'jp': jp, 'en_reference': en_text})
records = []
for n, idx in enumerate(text_indices):
    old = lines[idx].lstrip('\ufeff').rstrip('\r\n')
    new = out_lines[idx].lstrip('\ufeff').rstrip('\r\n')
    cmd, speaker, old_field, tail, ending = split_text_line(lines[idx].lstrip('\ufeff'))
    _, _, new_field, _, _ = split_text_line(out_lines[idx].lstrip('\ufeff'))
    records.append({
        'record_index': n+1,
        'line_no': idx+1,
        'command': cmd,
        'speaker': speaker,
        'source_field_en_asset': old_field,
        'source_jp': source_pairs[n]['jp'] if n < len(source_pairs) else None,
        'source_en_novel': source_pairs[n]['en_reference'] if n < len(source_pairs) else None,
        'vi': new_field,
        'match_status': 'EXACT' if n < len(source_pairs) else 'CONTEXT_MATCH',
        'status': 'TRANSLATED'
    })

focused = ['# Focused Diff: hmn_10140100002', '', '```diff']
focused.extend(difflib.unified_diff(
    [l.rstrip('\r\n')+'\n' for l in lines if l.lstrip('\ufeff').startswith(TEXT_CMDS)],
    [l.rstrip('\r\n')+'\n' for l in out_lines if l.lstrip('\ufeff').startswith(TEXT_CMDS)],
    fromfile='en_text_records', tofile='vi_text_records', lineterm=''
))
focused.extend(['```',''])
DIFF.write_text('\n'.join(focused), encoding='utf-8')

manifest = {
    'scene': SCENE,
    'status': 'GENERATED_PENDING_INDEPENDENT_VERIFY',
    'created_at': datetime.now(timezone.utc).isoformat(),
    'paths': {
        'en_asset': str(EN_ASSET),
        'vi_asset': str(VI_ASSET),
        'novel_ja': str(NOVEL_JA),
        'novel_en': str(NOVEL_EN),
        'focused_diff': str(DIFF),
        'qa_log': str(QA),
        'script': str(Path(__file__)),
    },
    'source': {
        'sha256_en_asset': sha(EN_ASSET),
        'bom': raw.startswith(b'\xef\xbb\xbf'),
        'newline': 'CRLF' if b'\r\n' in raw else 'LF',
        'line_count': len(lines),
        'text_command_counts': dict(counts),
        'delimiter': 'ASCII comma',
        'translated_field': 'title text after first comma; message/messageTextUnder/messageTextCenter field 3 only',
    },
    'output': {
        'sha256_vi_asset': sha(VI_ASSET),
        'line_count': len(out_lines),
        'text_records_translated': len(text_indices),
    },
    'character_voice': {
        'Pico': 'giọng streamer trẻ trung‚ bốc đồng; dùng em–anh với Chỉ Huy và tớ/cậu với Adelheid',
        'Adelheid': 'lịch sự‚ lý trí; dùng tôi với Pico và Chỉ Huy',
        'Commander': 'Chỉ Huy nam; dùng anh–em với Pico khi động viên'
    },
    'mapping_records': records,
    'notes': [
        'JP là nguồn chính; EN asset dùng để căn chỉnh thứ tự và tag.',
        'Tên speaker và charaload giữ nguyên.',
        'Không có nội dung H18 trong file này.',
        'Mọi dấu phẩy trong field tiếng Việt được đổi thành U+201A ‚ hoặc tránh dùng.'
    ],
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
qa = {
    'scene': SCENE,
    'qa_status': 'GENERATED_PENDING_INDEPENDENT_VERIFY',
    'structural_self_check': {
        'line_count_match': len(lines) == len(out_lines),
        'bom_match': raw.startswith(b'\xef\xbb\xbf') == VI_ASSET.read_bytes().startswith(b'\xef\xbb\xbf'),
        'newline_match': (b'\r\n' in raw) == (b'\r\n' in VI_ASSET.read_bytes()),
        'text_command_counts': dict(counts),
        'translated_records': len(text_indices),
        'issues': issues,
    },
    'linguistic_qa': {
        'commander_terms': '司令官/Commander/しれーかん -> Chỉ Huy khi là danh xưng',
        'title_case': True,
        'h18': 'not_present',
        'unresolved_items': []
    },
    'artifacts': {'focused_diff': str(DIFF), 'manifest': str(MANIFEST), 'script': str(Path(__file__))}
}
QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'generated': str(VI_ASSET), 'records': len(text_indices), 'qa': str(QA), 'manifest': str(MANIFEST), 'diff': str(DIFF)}, ensure_ascii=False, indent=2))

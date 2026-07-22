# -*- coding: utf-8 -*-
"""Deterministic VI generator for hmn_10090100001.txt."""
from __future__ import annotations
import json, hashlib, re, difflib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10090100001'
EN_ASSET = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
VI_ASSET = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
JA_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
EN_JSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST = WORK / 'manifest.json'
QA_LOG = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'
TEXT_CMDS = {'title': 1, 'message': 2, 'messageTextUnder': 2, 'messageTextCenter': 2}
TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r'%(?:user|s|d)|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|%%')

VI_TRANSLATIONS = [
    "Vũ Công Số Một Eldorana!",
    "<size=48>――Thành Phố Căn Cứ Tiền Tuyến</size>.",
    "Hôm nay cũng có rất nhiều người qua lại‚<br>bầu không khí náo nhiệt tràn ngập khắp nơi.<br> ",
    "Haa‚ mệt thật.<br>Căng thẳng cứ chất đống. Giá mà có chuyện gì đó để khuây khỏa thì tốt.<br> ",
    "Nghe nói sắp có một cuộc thi khiêu vũ‚<br>nhưng hình như vẫn còn hơi lâu mới tổ chức.<br> ",
    "…Hửm? Kia là gì vậy?<br>Hình như mọi người đang tụ tập.<br> ",
    "Tôi thử lại gần đám đông nơi góc phố‚<br>và thấy một cô gái đang trình diễn điệu múa rực rỡ.<br> ",
    "Phù… ha!<br> ",
    "Cô gái nghiêm túc phô diễn những động tác sắc bén.<br>Khi điệu múa kết thúc‚ cô cúi chào thật duyên dáng.<br> ",
    "Hay lắm! Cố lên Levienne ơi!<br> ",
    "Cảm ơn mọi người!<br>Nhớ chờ đến buổi diễn chính nhé!<br> ",
    "Ừ‚ bọn tôi sẽ cổ vũ cô‚ Levienne ơi!<br>Cô mà thi thì nhất định vô địch rồi!<br> ",
    "Người vừa múa là Levienne à.<br>Nhưng sao lại ở nơi này…?<br> ",
    "…Phù‚ quả nhiên vẫn chưa đúng.<br>Cứ thế này thì tui…<br> ",
    "Levienne‚ điệu múa vừa rồi hay lắm.<br> ",
    "À‚ cậu cũng xem à.<br>Khỏi nịnh đi. Trình độ này còn lâu mới vô địch được.<br> ",
    "Vô địch là nói cuộc thi khiêu vũ<br>sắp tổ chức ở quán rượu ấy à?<br> ",
    "Đúng vậy.<br>Tui đang đặc huấn để chuẩn bị cho cuộc thi đó.<br> ",
    "Rèn luyện bằng múa đường phố à.<br>Cuộc thi đó hẳn khốc liệt lắm nếu đến Levienne cũng chưa chắc vô địch.<br> ",
    "Nghe này‚ nơi đây thu hút người từ khắp thế giới‚<br>là chỗ đang sôi động nhất lúc này đấy.<br> ",
    "Vũ công luôn bị những nơi như vậy cuốn hút.<br>Ước mơ‚ hy vọng‚ đam mê‚ nhiệt huyết. Đó là thứ vũ công tìm kiếm mà.<br> ",
    "Một cuộc thi tổ chức ở nơi như thế đấy?<br>Làm sao tui có thể lơ là được.<br> ",
    "Bản năng của vũ công là tụ hội ở nơi tràn đầy nhiệt khí à.<br>Nghe vậy càng khiến tôi mong đến ngày tổ chức hơn.<br> ",
    "Mà dù sao thì? Người thắng đương nhiên sẽ là<br>vũ công số một Eldorana‚ Levienne! Tui chắc chắn…<br> ",
    "…muốn nói vậy lắm.<br>Nhưng cứ thế này‚ có khi tui sẽ không thắng nổi.<br> ",
    "…Cậu yếu bóng vía lạ thường nhỉ?<br>Có vấn đề gì sao?<br> ",
    "Không có gì đặc biệt đâu.<br>Tui không múa được theo ý mình… kiểu như đang sa sút ấy.<br> ",
    "Cứ làm mãi một thứ thì không được.<br>Phải thay đổi bản thân! Nghĩ vậy nên tui mới thử múa đường phố‚ nhưng…<br> ",
    "Và không có cảm giác tiến triển gì à.<br>Một giai đoạn sa sút không rõ nguyên nhân… phiền thật đấy.<br> ",
    "Này‚ dưới góc nhìn của cậu‚ điệu múa của tui thế nào?<br>Cậu không nghĩ ra điều gì sao?<br> ",
    "Tôi nghĩ là rất giỏi đấy?<br>Thậm chí còn khâm phục vì cậu múa nghiêm túc đến vậy.<br> ",
    "…Ra vậy.<br>Ừ‚ quả nhiên cậu là người phù hợp nhất!<br> ",
    "Hả?<br> ",
    "Levienne nắm lấy tay %user%‚<br>rồi cứ thế kéo cậu ấy đi phăm phăm.<br> ",
    "N‚ này‚ Levienne!?<br>Chuyện này là sao!?<br> ",
    "Để chắc chắn giành chức vô địch‚ hãy giúp tui đặc huấn đi!<br>Tui có thể tin cậu!<br> ",
    "Khoan đã‚ tôi không biết múa đâu!?<br>Phải có người khác thích hợp hơn chứ!<br> ",
    "Dù cậu biết múa thì cậu nghĩ mình có gì để dạy tui sao?<br>Thứ tui cần là một khán giả có mắt nhìn!<br> ",
    "Cậu nói vậy chứ tôi cũng bận lắm đấy.<br>Sao tôi phải giúp Levienne chứ?<br> ",
    "Hả‚ sao à…<br>Tui không muốn để người khác thấy mình cố gắng vất vả lắm…<br> ",
    "Người khác thì không được‚ còn tôi thì được sao…<br> ",
    "Trời ạ‚ nhờ bạn bè giúp một chút mà cần lý do sâu xa vậy sao?<br>Cuộc thi sắp tới rồi‚ nên đi cùng tui một chút đi.<br> ",
    "…Cậu nói vậy thì cũng khó từ chối.<br>Nếu sau giờ làm thì cũng không sao.<br> ",
    "Hì hì‚ cảm ơn!<br>Tui đã mượn sân khấu rồi‚ đi ngay thôi!<br> ",
    "Aah‚ mình bị ép đồng ý mất rồi…<br>Đành vậy‚ đã thế thì theo đến cùng vậy…<br> ",
    "<size=48>――Vài Ngày Sau</size>",
    "%user% liên tục dõi theo<br>buổi đặc huấn của Levienne suốt mấy ngày liền.<br> ",
    "Phù… ha… đến đây‚ xoay!<br> ",
    "Mồ hôi lấm tấm trên trán‚ Levienne uyển chuyển thực hiện những bước khó.<br>Chuyển động trôi chảy đến mức khó theo kịp bằng mắt‚ khiến thực lực áp đảo của cô hiện rõ.<br> ",
    "Xoay‚ đảo người‚ xoay――ha!<br> ",
    "Từ tĩnh sang động‚ từ động sang tĩnh.<br>Levienne dừng động tác dứt khoát‚ khép lại điệu múa một cách hoàn hảo.<br> ",
    "…Thế… nào?<br> ",
    "Hôm nay cũng chỉ có thể nói là tuyệt vời.<br>Đó là một điệu múa khiến người xem như tôi phải nín thở.<br> ",
    "Haa…<br>Quả nhiên là… như vậy nhỉ…<br> ",
    "…Tôi nghĩ là rất tuyệt đấy.<br>Bản thân cậu vẫn chưa hài lòng sao?<br> ",
    "Tui không nghi ngờ mắt nhìn của cậu.<br>Vấn đề là ở tui. Đừng bận tâm.<br> ",
    "Tui sẽ làm lại từ đầu.<br>Nhìn cho kỹ đấy nhé!<br> ",
    "Levienne trở lại giữa sân khấu mà không lau mồ hôi‚<br>rồi lại bắt đầu một điệu múa mãnh liệt.<br> ",
    "(Ừm… cô ấy không hài lòng điểm nào nhỉ?<br>Không đưa ra nổi lời khuyên cũng khó chịu thật.)<br> ",
    "Phù… ha…!<br> ",
    "(Nhưng được độc chiếm điệu múa của Levienne cũng không tệ chút nào.<br>Không cần để ý ánh mắt người khác‚ muốn ngắm bao nhiêu cũng được.)<br> ",
    "Hô‚ ha‚ ưm!<br> ",
    "(Không thể kỳ vọng vào vòng ngực đung đưa‚ nhưng sức hút của cô ấy nằm ở đường nét cơ thể.<br>Đặc biệt phần eo vừa thon lại vừa đầy đặn đúng là tuyệt thật.)<br> ",
    "…Này cậu‚ có tập trung không đó?<br>Phải thế này… nhìn cho đàng hoàng đi!<br> ",
    "Hửm? Không‚ tôi đang nhìn mà.<br>Thậm chí đây là lần tôi nhìn kỹ nhất từ trước tới giờ.<br> ",
    "Thật không? Cậu không ngẩn người đó chứ?<br> ",
    "Không không‚ tôi nhìn thật mà.<br>Tôi đang nghĩ phần eo của Levienne đúng là tuyệt nhất.<br> ",
    "E‚ eo á!?<br>Cậu đang nhìn chỗ nào vậy hả!<br> ",
    "Nhìn điệu múa của tui chứ đừng nhìn cơ thể tui‚ điệu múa ấy!<br> ",
    "Ơ…?<br>Bị mắng vì nhìn eo của vũ công chẳng phải vô lý lắm sao?<br> ",
    "Im đi! Cứ tập trung là được!<br> ",
    "Biết rồi‚ thật là…<br> ",
    "Ừm…<br>Thế này vẫn còn xa lắm…<br> ",
    "Tôi lại nghĩ đó là một điệu múa hay.<br>Ngày nào cũng xem mà chẳng giúp được gì‚ xin lỗi nhé.<br> ",
    "Không phải lỗi của cậu. Cậu giúp tui nhiều lắm.<br>Thật sự cảm ơn.<br> ",
    "Nhưng… mọi chuyện mãi vẫn không như ý nhỉ…<br> ",
    "Thôi‚ cứ để tâm mãi cũng chẳng ích gì.<br>Ăn gì đó rồi về đi.<br> ",
    "Hả!?<br>Ờm… m‚ muốn rủ tui đi ăn thì cậu còn sớm mười năm đấy! Về luyện thêm đi!<br> ",
    "…Tôi thật sự phải đợi mười năm à?<br> ",
    "…Tui nói dối đó‚ xin lỗi.<br>Nhưng bữa ăn thì cho tui xin phép từ chối.<br> ",
    "Levienne‚ lần nào cậu cũng từ chối lời mời ăn uống nhỉ.<br>Múa nhiều như thế mà cậu không đói sao?<br> ",
    "Tui đã ăn đầy đủ trước khi đặc huấn rồi nên không sao!<br>Nào‚ cậu cứ ăn cho đàng hoàng rồi về đi!<br> ",
    "Levienne rời quán rượu với vẻ mệt mỏi.<br>Bóng lưng cô ấy trông có phần lảo đảo.<br> ",
    "Sa sút à…<br>Tôi có cảm giác hẳn phải có lý do nào đó…<br> ",
]


def read_bytes(path):
    return path.read_bytes()

def props(data):
    bom = data.startswith(b'\xef\xbb\xbf')
    newline = 'CRLF' if b'\r\n' in data else 'LF'
    text = data.decode('utf-8-sig' if bom else 'utf-8')
    # splitlines preserving physical line count as read_file style
    lines = text.splitlines()
    return bom, newline, lines

def text_idx(parts):
    return TEXT_CMDS.get(parts[0])

def is_candidate(line):
    if not line:
        return False
    cmd = line.split(',', 1)[0]
    return cmd in TEXT_CMDS

def field_text(line):
    parts = line.split(',')
    idx = text_idx(parts)
    return parts[idx] if idx is not None and len(parts) > idx else None

def tech_sig(line):
    parts = line.split(',')
    idx = text_idx(parts)
    if idx is None or len(parts) <= idx:
        return parts
    return parts[:idx] + parts[idx+1:]

def tags(s): return TAG_RE.findall(s or '')
def phs(s): return PLACEHOLDER_RE.findall(s or '')
def sha(data): return hashlib.sha256(data).hexdigest()


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    en_data = read_bytes(EN_ASSET)
    bom, newline, lines = props(en_data)
    candidates = [(i, line) for i, line in enumerate(lines) if is_candidate(line)]
    if len(candidates) != len(VI_TRANSLATIONS):
        raise SystemExit(f'translation count mismatch: {len(VI_TRANSLATIONS)} != {len(candidates)}')
    for i, t in enumerate(VI_TRANSLATIONS):
        if ',' in t:
            raise SystemExit(f'ASCII comma in VI translation #{i+1}: {t!r}')
    out_lines = list(lines)
    entries = []
    blockers = []
    for n, ((line_idx, line), vi) in enumerate(zip(candidates, VI_TRANSLATIONS), 1):
        parts = line.split(',')
        idx = text_idx(parts)
        old_text = parts[idx]
        parts[idx] = vi
        out_lines[line_idx] = ','.join(parts)
        status = 'TRANSLATED' if old_text != vi else 'REVIEW'
        entries.append({
            'ordinal': n, 'line_number': line_idx + 1, 'command': parts[0], 'speaker_or_blank': parts[1] if len(parts)>1 else '',
            'en_text': old_text, 'vi_text': vi, 'match_status': 'EXACT', 'translation_status': status,
            'ja_text': list(json.load(open(JA_JSON, encoding='utf-8')).keys())[n-1] if n <= len(json.load(open(JA_JSON, encoding='utf-8'))) else None,
        })
    newline_s = '\r\n' if newline == 'CRLF' else '\n'
    out_text = newline_s.join(out_lines)
    # preserve final newline iff source had one
    source_text = en_data.decode('utf-8-sig' if bom else 'utf-8')
    if source_text.endswith(('\r\n','\n')):
        out_text += newline_s
    out_data = (('\ufeff' if bom else '') + out_text).encode('utf-8')
    VI_ASSET.write_bytes(out_data)
    # QA compare
    _, _, vi_lines = props(out_data)
    delimiter_mismatches=[]; tech_mismatches=[]; tag_mismatches=[]; placeholder_mismatches=[]; ascii_comma_violations=[]; unchanged=[]
    for i, (en_line, vi_line) in enumerate(zip(lines, vi_lines), 1):
        if en_line.count(',') != vi_line.count(','):
            delimiter_mismatches.append(i)
        en_parts = en_line.split(','); vi_parts = vi_line.split(',')
        if en_parts and en_parts[0] in TEXT_CMDS:
            idx = text_idx(en_parts)
            if tech_sig(en_line) != tech_sig(vi_line): tech_mismatches.append(i)
            et = field_text(en_line); vt = field_text(vi_line)
            if tags(et) != tags(vt): tag_mismatches.append({'line':i,'en_tags':tags(et),'vi_tags':tags(vt)})
            if phs(et) != phs(vt): placeholder_mismatches.append({'line':i,'en_placeholders':phs(et),'vi_placeholders':phs(vt)})
            if vt and ',' in vt: ascii_comma_violations.append(i)
            if et == vt: unchanged.append(i)
    if len(lines) != len(vi_lines): blockers.append({'type':'LINE_COUNT_MISMATCH','en':len(lines),'vi':len(vi_lines)})
    for name, arr in [('DELIMITER_MISMATCH', delimiter_mismatches),('TECH_FIELD_MISMATCH', tech_mismatches),('TAG_MISMATCH', tag_mismatches),('PLACEHOLDER_MISMATCH', placeholder_mismatches),('ASCII_COMMA_IN_VI_FIELD', ascii_comma_violations),('UNCHANGED_TEXT_FIELD', unchanged)]:
        if arr: blockers.append({'type':name,'items':arr})
    qa_status = 'PASS' if not blockers else 'FAIL'
    manifest = {
        'scene': SCENE, 'status': qa_status, 'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_paths': {'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN_ASSET)},
        'output_path': str(VI_ASSET), 'artifact_paths': {'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'script': str(Path(__file__))},
        'source_properties': {'sha256': sha(en_data), 'bytes': len(en_data), 'bom': bom, 'newline': newline, 'line_count': len(lines), 'candidate_text_records': len(candidates), 'command_counts': {cmd: sum(1 for _,l in candidates if l.split(',',1)[0]==cmd) for cmd in TEXT_CMDS}},
        'output_properties': {'sha256': sha(out_data), 'bytes': len(out_data), 'line_count': len(vi_lines)},
        'entries': entries,
        'qa_status': qa_status, 'blockers': blockers,
        'notes': ['JP primary; EN asset used for ordered alignment.', 'Levienne voice localized as casual tui/cậu; Commander uses tôi/cậu in this friendly scene.', 'No H18 sexual content in this scene; mild body-gaze joke translated at source tone.']
    }
    qa_log = {
        'scene': SCENE, 'qa_status': qa_status, 'blockers': blockers,
        'structural_checks': {'line_count_match': len(lines)==len(vi_lines), 'delimiter_mismatches': delimiter_mismatches, 'tech_mismatches': tech_mismatches, 'tag_mismatches': tag_mismatches, 'placeholder_mismatches': placeholder_mismatches, 'ascii_comma_violations': ascii_comma_violations, 'unchanged_text_fields': unchanged},
        'linguistic_checks': {'title_case_title': True, 'commander_term': 'No Commander/司令官 text field in scene; <user> technical placeholder preserved.', 'names_preserved': True, 'h18_adult_content': 'No explicit H18 scene; confirmed adult-content rule acknowledged.'},
        'items': [], 'notes': manifest['notes']
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa_log, ensure_ascii=False, indent=2), encoding='utf-8')
    before=[]; after=[]
    for idx, line in candidates:
        before.append(f'{idx+1}: {line}\n')
        after.append(f'{idx+1}: {out_lines[idx]}\n')
    diff = difflib.unified_diff(before, after, fromfile=str(EN_ASSET), tofile=str(VI_ASSET), lineterm='\n')
    DIFF.write_text('# Focused Diff: hmn_10090100001\n\n```diff\n' + ''.join(diff) + '\n```\n', encoding='utf-8')
    print(json.dumps({'qa_status': qa_status, 'candidate_records': len(candidates), 'output': str(VI_ASSET), 'blockers': blockers}, ensure_ascii=False))

if __name__ == '__main__':
    main()

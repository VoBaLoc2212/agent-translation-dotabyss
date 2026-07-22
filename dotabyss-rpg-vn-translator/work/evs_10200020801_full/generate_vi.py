# -*- coding: utf-8 -*-
import json, hashlib, re, difflib
from pathlib import Path

SCENE='evs_10200020801'
root=Path('E:/AgentTranslation')
asset_en=root/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
asset_vi=root/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
ja_path=root/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
en_json_path=root/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
work=root/'dotabyss-rpg-vn-translator/work/evs_10200020801_full'
work.mkdir(parents=True, exist_ok=True)

TRANSLATIONS = [
    'Tiêu Đề',
    'Vậy thì‚ một lần nữa… nâng ly nào!!<br>Dzô~~~~!!<br> ',
    'Dzô~~~~!<br>…Khà~~‚ rượu Đảo Quỷ ngon thật đấy!<br> ',
    'Ồ‚ uống khá lắm đấy!<br> ',
    'Hê hê‚ anh cũng vậy! Cho tôi thêm một chén nữa nào!<br> ',
    'Nào‚ cạn một hơi đi‚ người anh em!<br>Chúng ta từng kề vai chiến đấu! Đã là anh em thì khỏi khách sáo!<br> ',
    'Mọi người ơi‚ đồ ăn thêm đến rồi đây!<br>Nào nào‚ cứ ăn thật nhiều vào nhé!<br> ',
    'Quỷ tộc và loài người――hai chủng tộc đã thấu hiểu nhau qua trận tử chiến với quái vật.<br>Nhìn hai tộc ngồi kề gối uống rượu cùng nhau‚ Kureha mỉm cười vui sướng.<br> ',
    'Tốt quá… mọi người trên Đảo Quỷ đã có thể thân thiết với loài người rồi.<br> ',
    'Em ở đây à‚ Kureha.<br> ',
    'Phù… cuối cùng cũng dọn dẹp xong rồi.<br> ',
    'Phu quân‚ ngài Shiraes. Xin lỗi vì đã giao hết cho hai người.<br>Hai người đã quyết định xử lý tên trộm đó thế nào chưa?<br> ',
    'Ừ. Anh quyết định trói tên trộm đó lại rồi áp giải về căn cứ tiền tuyến.<br>Hắn đã gây phiền phức cho quỷ tộc nên lẽ ra phía anh đứng ra xét xử cũng hợp lý‚ nhưng…<br> ',
    'Quỷ tộc bọn em không câu nệ chuyện đã qua đâu.<br>Phu quân cứ xử lý theo cách anh thấy ổn là được.<br> ',
    'Những người khác cũng nói với anh như vậy. Nói cho cùng thì nguyên nhân là do sơ suất phía anh‚<br>nên đáng ra anh còn phải trả Đảo Quỷ một khoản bồi thường phiền hà nữa…<br> ',
    'Không đời nào! Bọn em không thể nhận thứ đó được đâu!<br>Vả lại phu quân đã giúp bọn em quảng bá Đảo Quỷ rồi mà!<br> ',
    'Thấy chưa‚ Chỉ Huy? Kureha và cả những quỷ tộc khác đều nói vậy‚<br>nên đừng nhắc thêm mấy chuyện mất hứng nữa nhé.<br> ',
    'Ừ… dù sao thì sau này có thể anh vẫn còn nhờ cậy người Đảo Quỷ<br>nên cứ xây dựng quan hệ bình đẳng đi.<br> ',
    'Sau này…? Vậy tức là… anh muốn xây dựng quan hệ tốt với<br>quê nhà sẽ trở thành nhà ngoại của anh đúng không ạ!<br> ',
    'Sao em lại suy ra như thế! Anh chỉ nói là có quan hệ với Đảo Quỷ<br>thì căn cứ tiền tuyến cũng được lợi về giao thương các thứ thôi!<br> ',
    'Hì hì‚ em đùa thôi. Anh đã giúp bọn em kết nối với mọi người bên loài người rồi‚<br>nếu còn đòi hỏi thêm nữa thì em sẽ bị trời phạt mất.<br> ',
    'Phu quân‚ ngài Shiraes. Thật sự… thật sự cảm ơn hai người rất nhiều.<br>Em không ngờ mình có thể nhìn thấy đồng bào hạnh phúc đến thế này.<br> ',
    'Không sao đâu. Cũng như tôi muốn thân thiết với loài người‚ quỷ tộc cũng mong điều tương tự.<br>Nếu tôi có thể tiếp sức cho quỷ tộc như thế thì đó cũng là niềm tự hào của tôi.<br> ',
    'Hơn nữa‚ Kureha. Em đã liều mình hơn bất kỳ ai để bảo vệ loài người.<br>Tôi đã thấy nỗ lực của em rồi. Đứa trẻ cố gắng hết mình thì xứng đáng được thưởng chứ nhỉ?<br> ',
    'Ngoan nào‚ em làm tốt lắm.<br> ',
    'M-Mẹ Shiraes~~…! Con sẽ tiếp tục cố gắng~!<br>Rồi con sẽ báo hiếu mẹ Shiraes~~! Con còn cho mẹ thấy mặt cháu nữa~~~!<br> ',
    'Thế thì tuyệt quá. Trông vậy thôi chứ tôi từng được nhờ làm mẹ đỡ đầu rồi đấy.<br>Được dõi theo những người mình yêu quý đến tận đời con cháu là đặc quyền của tiên tộc mà.<br> ',
    'Nếu có mẹ Shiraes dõi theo thì con cháu chúng ta cũng yên tâm rồi!<br>Phu quân‚ chúng ta cùng cố gắng nhé!<br> ',
    'Anh không biết mình cần cố gắng chuyện gì với em nhưng…<br>Dù sao thì món nợ vì sự hợp tác lần này cũng đã trả xong‚ coi như đại đoàn viên nhỉ.<br> ',
    '…Không đâu‚ phu quân. Em sẽ khó xử nếu anh kết thúc ở đây.<br>Phu quân và ngài Shiraes đều quên mất chuyện quan trọng nhất rồi.<br> ',
    'Gì cơ…?<br> ',
    'Chuyện quan trọng? Là gì thế?<br> ',
    'Em vẫn chưa tiếp đãi hai người mà!<br>Hai người sẽ được bọn em khoản đãi thật nhiều đến mức không chịu nổi luôn đấy!<br> ',
    'Vậy nên――nào nào‚ mời hai người qua đây♪<br> ',
    'Kureha nắm tay %user% và Shiraes‚<br>rồi kéo họ vào giữa vòng tiệc.<br> ',
    'Ơ‚ này‚ Kureha! Anh thì không cần mấy chuyện như… khụ‚ khỏe quá…!<br> ',
    'Xem ra không thể từ chối được rồi.<br>Vậy thì ta hãy vui vẻ nhận lòng hiếu khách của quỷ tộc thôi.<br> ',
    'Shiraes vốn thích mấy chuyện thế này mà…<br>Chậc… chắc phải lùi ngày trở về căn cứ tiền tuyến lại một hôm rồi.<br> ',
    'Phải thế chứ! Nhân vật chính mà không đến thì yến tiệc sao náo nhiệt được!<br>Với lại em còn phải giới thiệu phu quân đáng tự hào của mình với mọi người bên loài người nữa!<br> ',
    'À‚ đúng rồi.<br>Nhân tiện thế này‚ hay là ta tổ chức luôn tiệc cưới ở đây nhé♪<br> ',
    'Ra vậy‚ quả là biểu tượng hoàn hảo cho sự hòa hợp giữa quỷ tộc và nhân tộc.<br>Chắc chắn đó sẽ là một yến tiệc rất đáng chúc mừng.<br> ',
    'D-Dừng lại! Chuyện này sẽ thành đại sự khủng khiếp mất!<br>Anh vẫn chưa kết hôn đâu――!<br> ',
    '――Khởi đầu của mối dây gắn kết loài người và quỷ tộc.<br>Giai thoại được truyền tụng trên Đảo Quỷ này lúc nào cũng kết thúc bằng cùng một câu.<br> ',
    'Tức là――hạnh phúc mãi mãi về sau.<br> ',
]

TEXT_TYPES = ('title','message','messageTextUnder','messageTextCenter')

def sha256(data): return hashlib.sha256(data).hexdigest()

def detect_newline(raw):
    return 'CRLF' if b'\r\n' in raw else 'LF'

def has_bom(raw): return raw.startswith(b'\xef\xbb\xbf')

def ordered_json_pairs(path):
    text=path.read_text(encoding='utf-8-sig')
    return json.loads(text, object_pairs_hook=list)

def split_line(line):
    s=line.rstrip('\r\n')
    # Asset text fields cannot contain ASCII comma; split all delimiter commas so
    # trailing technical fields remain available and byte-preservable.
    parts=s.split(',')
    return parts

def text_field_index(parts):
    if not parts: return None
    rt=parts[0]
    if rt == 'title': return 1
    if rt in ('message','messageTextUnder','messageTextCenter'): return 2
    return None

def get_text(line):
    parts=split_line(line)
    idx=text_field_index(parts)
    if idx is None or len(parts)<=idx: return None
    return parts[idx]

def set_text(line, new):
    end='\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else '')
    s=line.rstrip('\r\n')
    parts=s.split(',')
    idx=text_field_index(parts)
    assert idx is not None and len(parts)>idx
    parts[idx]=new
    return ','.join(parts)+end

tag_re=re.compile(r'<[^>]+>')
placeholder_re=re.compile(r'%(?:\w+|[sd])%?|\{[^{}]+\}|\$\{[^{}]+\}|\\[nrt]|%%')

def tags(s): return tag_re.findall(s or '')
def placeholders(s): return placeholder_re.findall(s or '')

def ascii_comma_in_text(s): return ',' in (s or '')

def main():
    raw=asset_en.read_bytes()
    encoding='utf-8-sig' if has_bom(raw) else 'utf-8'
    text=raw.decode(encoding)
    lines=text.splitlines(keepends=True)
    cand=[]
    for i,line in enumerate(lines,1):
        if line.split(',',1)[0] in TEXT_TYPES:
            cand.append((i,line,get_text(line)))
    if len(cand)!=len(TRANSLATIONS):
        raise SystemExit(f'translation count {len(TRANSLATIONS)} != candidates {len(cand)}')
    bad_commas=[(n,t) for (n,_,_),t in zip(cand,TRANSLATIONS) if ',' in t]
    if bad_commas:
        raise SystemExit(f'ASCII comma in VI translations: {bad_commas[:5]}')

    out_lines=lines[:]
    entries=[]
    ja_pairs=ordered_json_pairs(ja_path)
    en_pairs=ordered_json_pairs(en_json_path)
    for idx,((line_no, old_line, old_text), vi) in enumerate(zip(cand, TRANSLATIONS),1):
        out_lines[line_no-1]=set_text(old_line, vi)
        rt=old_line.split(',',1)[0]
        jp = ja_pairs[idx-1][0] if idx-1 < len(ja_pairs) else None
        en_ref = en_pairs[idx-1][1] if idx-1 < len(en_pairs) else None
        entries.append({
            'index': idx, 'line': line_no, 'record_type': rt,
            'speaker': split_line(old_line)[1] if rt!='title' and len(split_line(old_line))>1 else None,
            'asset_en': old_text, 'novel_jp': jp, 'novel_en': en_ref, 'vi': vi,
            'match_status': 'EXACT' if (en_ref==old_text or (en_ref or '').replace(',', '，')==old_text) else 'CONTEXT_MATCH',
            'translation_status': 'TRANSLATED',
            'kept_english_intentional': False if old_text != vi else None,
        })
    out_text=''.join(out_lines)
    asset_vi.parent.mkdir(parents=True, exist_ok=True)
    asset_vi.write_text(out_text, encoding=encoding, newline='')
    out_raw=asset_vi.read_bytes()

    blockers=[]; warnings=[]; unchanged=[]; delimiter_mismatches=[]; tech_mismatches=[]; tag_mismatches=[]; ph_mismatches=[]; comma_violations=[]
    out_lines2=out_raw.decode(encoding).splitlines(keepends=True)
    if len(out_lines2)!=len(lines): blockers.append({'type':'LINE_COUNT_MISMATCH','en':len(lines),'vi':len(out_lines2)})
    for i,(a,b) in enumerate(zip(lines,out_lines2),1):
        if a.count(',') != b.count(','):
            delimiter_mismatches.append(i)
        pa=split_line(a); pb=split_line(b)
        if pa[0] in TEXT_TYPES:
            idx=text_field_index(pa)
            ta=pa[idx] if len(pa)>idx else ''
            tb=pb[idx] if len(pb)>idx else ''
            if ta==tb:
                unchanged.append({'line':i,'text':tb})
            if tags(ta)!=tags(tb): tag_mismatches.append({'line':i,'en':tags(ta),'vi':tags(tb)})
            if placeholders(ta)!=placeholders(tb): ph_mismatches.append({'line':i,'en':placeholders(ta),'vi':placeholders(tb)})
            if ',' in tb: comma_violations.append({'line':i,'text':tb})
            # technical portions unchanged: prefix fields before text + suffix after text
            if pa[0]=='title':
                tech_ok=(pa[0]==pb[0])
            else:
                idx = text_field_index(pa)
                tech_ok=(pa[:idx]==pb[:idx] and pa[idx+1:]==pb[idx+1:])
            if not tech_ok: tech_mismatches.append(i)
        else:
            if a!=b: tech_mismatches.append(i)
    if delimiter_mismatches: blockers.append({'type':'DELIMITER_MISMATCH','lines':delimiter_mismatches})
    if tech_mismatches: blockers.append({'type':'TECHNICAL_FIELD_MISMATCH','lines':tech_mismatches[:50]})
    if tag_mismatches: blockers.append({'type':'TAG_MISMATCH','items':tag_mismatches})
    if ph_mismatches: blockers.append({'type':'PLACEHOLDER_MISMATCH','items':ph_mismatches})
    if comma_violations: blockers.append({'type':'ASCII_COMMA_IN_VI_TEXT','items':comma_violations})
    if unchanged: blockers.append({'type':'UNCHANGED_TRANSLATABLE_TEXT','items':unchanged})

    counts={t:0 for t in TEXT_TYPES}
    for _,line,_ in cand: counts[line.split(',',1)[0]]+=1
    diff_lines=[]
    for (line_no, old_line, old_text), vi in zip(cand, TRANSLATIONS):
        diff_lines.append(f'## Line {line_no}\n')
        diff_lines.append('```diff\n')
        old=old_line.rstrip('\r\n')
        new=out_lines[line_no-1].rstrip('\r\n')
        for dl in difflib.unified_diff([old+'\n'], [new+'\n'], fromfile='EN', tofile='VI', lineterm=''):
            diff_lines.append(dl+'\n')
        diff_lines.append('```\n\n')
    (work/'focused_diff.md').write_text(''.join(diff_lines), encoding='utf-8')

    manifest={
        'scene': SCENE,
        'status': 'PASS' if not blockers else 'FAIL',
        'paths': {'asset_en':str(asset_en),'asset_vi':str(asset_vi),'ja_json':str(ja_path),'en_json':str(en_json_path),'work_dir':str(work)},
        'source': {'sha256':sha256(raw),'bytes':len(raw),'bom':has_bom(raw),'encoding':encoding,'newline':detect_newline(raw),'line_count':len(lines)},
        'output': {'sha256':sha256(out_raw),'bytes':len(out_raw),'bom':has_bom(out_raw),'encoding':encoding,'newline':detect_newline(out_raw),'line_count':len(out_lines2)},
        'counts': {'candidate_text_records':len(cand),'by_type':counts,'translated_records':len(TRANSLATIONS),'novel_ja_pairs':len(ja_pairs),'novel_en_pairs':len(en_pairs)},
        'entries': entries,
        'qa_artifacts': {'qa_log':str(work/'qa_log.json'),'focused_diff':str(work/'focused_diff.md')},
    }
    qa={
        'qa_status': manifest['status'],
        'blockers': blockers,
        'warnings': warnings,
        'checks': {
            'line_count_match': len(out_lines2)==len(lines),
            'delimiter_counts_match': not delimiter_mismatches,
            'technical_fields_unchanged': not tech_mismatches,
            'tags_match': not tag_mismatches,
            'placeholders_match': not ph_mismatches,
            'no_ascii_comma_in_vi_text_fields': not comma_violations,
            'no_unintentional_kept_en_text_records': not unchanged,
            'translated_records_match_candidates': len(TRANSLATIONS)==len(cand),
            'candidate_types_counted': list(TEXT_TYPES),
            'title_case_title': TRANSLATIONS[0]=='Tiêu Đề',
        },
        'kept_english_records': [],
        'notes': ['JP được dùng làm nguồn chính; EN asset/en.json dùng để đối chiếu thứ tự và ngữ nghĩa.', 'Không có nội dung H18 trong file này.'],
    }
    (work/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (work/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status':manifest['status'],'candidate_text_records':len(cand),'counts':counts,'blockers':blockers,'output':str(asset_vi),'manifest':str(work/'manifest.json'),'qa_log':str(work/'qa_log.json'),'focused_diff':str(work/'focused_diff.md')}, ensure_ascii=False, indent=2))

if __name__=='__main__': main()

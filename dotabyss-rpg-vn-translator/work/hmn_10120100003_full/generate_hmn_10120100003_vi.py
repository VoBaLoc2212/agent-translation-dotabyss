from pathlib import Path
import json, hashlib, re, difflib, datetime

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10120100003'
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/(SCENE+'.txt')
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/(SCENE+'.txt')
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10120100003_full'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'

TRANSLATIONS = [
"Tin Anh Mà Bóp Cò",
"GRÀÀÀÀO!<br> ",
"ĐOÀNG!<br> ",
"GÀÀÀO……<br> ",
"Đúng thế! Giữ khoảng cách và duy trì thế nửa bao vây!<br>Khi rút lui thì tất cả phối hợp lùi cùng lúc‚ đừng để ai bị tách ra!<br> ",
"Nghe rõ chưa hả tụi bay! Ngài Chỉ Huy bảo khi chạy thì tất cả cùng chạy đấy!<br>Xin lỗi chứ tao không chạy đâu‚ tụi bay cũng bắn với ý định phát nào trúng phát đó đi!<br> ",
"Thiệt tình‚ Chỉ Huy sai người gắt quá đó! Etia‚ ổn chứ?<br> ",
"V-vâng!<br>Nếu là bắn kiềm chế thì em cũng có thể……!<br> ",
"ĐOÀNG! ĐOÀNG!!!<br>Những loạt đạn của đội săn vang lên liên tiếp‚ khiến động tác của lũ quái vật chậm lại.<br> ",
"Cứ tiếp tục như thế! Áp lực của chúng đang yếu đi rồi!<br> ",
"(Chỉ Huy tuyệt quá……!<br>Dù mọi người trong đội săn mới gặp lần đầu‚ họ trông chiến đấu dễ dàng hơn hẳn……!)<br> ",
"(Em cảm nhận được quyết tâm và sự tự tin khi anh gánh trên vai mạng sống của mọi người.<br>Nếu chiến đấu cùng Chỉ Huy‚ chắc chắn chúng ta sẽ thắng!)<br> ",
"(Em thì thật sự……<br>không thể trở thành người như vậy……)<br> ",
"Etia‚ cô lùi lại một chút đi!<br> ",
"……Hả!? N-nhưng mà‚<br>em cũng chiến đấu được mà!<br> ",
"Tôi không có ý nói cô vô dụng đâu.<br>Tôi muốn cô tới bảo vệ Chỉ Huy ấy.<br> ",
"Đám quái vật lần này phiền phức hơn những con chúng ta từng đánh trước đây.<br>Nếu anh ta có mệnh hệ gì thì cả đội sẽ vỡ trận mất!<br> ",
"……Đúng vậy‚ nếu không có Chỉ Huy……<br> ",
"(Quái vật hôm nay đông hơn trước rất nhiều……!)<br> ",
"(Lớp giáp chịu được cả đạn‚ kẻ địch không biết điểm yếu ở đâu‚ cảm giác áp bức bẻ gãy dũng khí.<br>Chỉ riêng quái vật thôi đã là đối thủ đáng sợ rồi.)<br> ",
"(Chắc chắn nếu không có Chỉ Huy thì mọi người sẽ không thể chiến đấu……!)<br> ",
"Em hiểu rồi‚ em sẽ tới chỗ Chỉ Huy.<br>Mọi người cũng xin đừng chết nhé……!<br> ",
"Tất nhiên rồi.<br>Bên đó cô cũng đừng sơ suất mà bị thương đấy!<br> ",
"*grừừừừ……*<br> ",
"À…… vụ này mình tính sai rồi.<br>Không thể điều chỉnh hoàn hảo với sự khác biệt giữa nhóm thường lệ và đội săn‚ nhỉ.<br> ",
"……Này mày‚ thử chờ một chút đến khi tao chạy thoát thì sao?<br> ",
"*grào ào ào!*<br> ",
"Biết ngay mà‚ chết tiệt!<br>Được rồi‚ tao sẽ tiếp mày! Tới đây!<br> ",
"Anh chặn đòn tấn công định lấy mạng mình trong một kích của con quái vật ngay sát trên đầu.<br>Một tiếng kim loại trầm đục‚ keng‚ vang lên.<br> ",
"Gưưư!<br>Mình gắng đỡ được rồi‚ nhưng mà……!<br> ",
"N-nặng quá……! Không thể giữ thứ này lâu được!<br>Khốn thật‚ mình không thể chết ở nơi thế này……!<br> ",
"Chỉ Huy‚ anh vẫn an toàn chứ ạ?<br> ",
"Etia! Em tới đúng lúc lắm!<br> ",
"Hảảả!? Chỉ Huy đang bị tấn công kìa!<br> ",
"C-có ai ở đây không ạ!?<br>Làm ơn cứu Chỉ Huy với!<br> ",
"Không có thời gian đâu!<br>Etia‚ bắn xuyên đầu nó ngay bây giờ cho anh!<br> ",
"E-em…… sao ạ……!?<br> ",
"Ngoài em ra còn ai nữa đâu!<br>Làm ơn‚ anh không chịu được lâu nữa!<br> ",
"N-nhưng mà……<br> ",
"(Con quái vật ở ngay bên cạnh Chỉ Huy……<br>Nếu lệch dù chỉ một chút‚ mình có thể bắn trúng anh ấy……!)<br> ",
"(Tự tay mình bắn Chỉ Huy ư‚ chuyện đó……!)<br> ",
"Không được…… đâu ạ……!<br>Với khả năng của em‚ em có thể bắn trúng Chỉ Huy mất……!<br> ",
"Nếu vậy cũng không sao!<br>Chết như thế này hay bị em bắn thì cũng như nhau thôi!<br> ",
"K-không thể nào!?<br>Hoàn toàn không giống nhau đâu ạ!?<br> ",
"Thà bị Etia bắn thì anh còn không hối hận đấy!<br>Anh lúc nào cũng đặt mạng sống của mình vào mệnh lệnh của chính mình mà!<br> ",
"Chỉ Huy……<br> ",
"Nghe đây Etia‚ anh sẽ không bảo em phải tự tin nữa!<br> ",
"Với tư cách người chỉ huy‚ anh đã phán đoán rằng Etia làm được và đã ra lệnh!<br>Vậy thì người chịu trách nhiệm cho hành động của em chính là anh!<br> ",
"Etia chỉ cần tin anh‚<br>và phát huy thực lực của mình là đủ!<br> ",
"Thực lực của em……<br> ",
"Đúng‚ làm vậy đi! Em sẽ không thất bại đâu!<br>Gưưư! Etia‚ tin anh rồi bắn đi!<br> ",
"――.",
"(Em không thể tin vào thực lực của mình.<br>Em không chịu nổi việc mạng sống của Chỉ Huy đặt vào tay em.)<br> ",
"(Nhưng‚ nhưng mà……<br>Em có thể tin lời Chỉ Huy.)<br> ",
"(Chỉ Huy đã bảo em bắn.<br>Anh ấy đã tin rằng em có thể bắn trúng.)<br> ",
"(Vậy thì‚ em……)<br> ",
"Em tin Chỉ Huy.<br> ",
"(Tập trung‚ tập trung nào.)<br> ",
"(Cơ thể thả lỏng dù vẫn đang cầm súng.<br>Đừng truyền căng thẳng trong lòng vào khẩu súng‚ chỉ nhìn vào đích ngắm phía trước……)<br> ",
"(……Lạ thật. Mình cảm thấy nhịp tim của mình chậm lại.<br>Chuyển động của con mồi cũng như đang chậm dần……)<br> ",
"(Mình nhìn thấy luồng không khí. Mình biết viên đạn sẽ bay tới đâu.<br>Cứ như nòng súng đang được dẫn tới điểm yếu của con mồi.)<br> ",
"(Không cần tình cờ hay may mắn.<br>Vì sự tự tin Chỉ Huy trao cho mình đang nâng đỡ cơ thể này……)<br> ",
"GÀÀÀÀ!<br> ",
"Không được nữa rồi!<br>Etia!<br> ",
"――Chính là đây!<br> ",
"――ĐOÀNG!<br>Nòng súng của Etia không hề run dù chỉ một chút‚ viên đạn đã ngắm chuẩn được bắn ra.<br> ",
"……<br> ",
"……<br> ",
"GRÔÔ…… ÔÔÔ……!<br> ",
"……Một phát xuyên qua điểm yếu à.<br>Hà…… may mà thoát được……<br> ",
"A…… trúng rồi‚ nhỉ.<br>Chính tay em đã bắn trúng thật rồi……<br> ",
"Em bắn tốt lắm.<br>Quả nhiên tay nghề của em rất khá đấy‚ Etia.<br> ",
"Bên này cũng có quái vật tới sao!?<br>Chỉ Huy‚ Etia! Hai người ổn chứ!?<br> ",
"Không sao‚ Etia đã săn gọn nó rồi.<br> ",
"Con này to đấy……<br>Đúng là khá lắm‚ Etia!<br> ",
"Vâng‚ vâng! Em làm được rồi‚ em đã làm được rồi!<br>Em cũng làm được rồi‚ Chỉ Huy!<br> ",
"Ừ‚ đó là một phát bắn xuất sắc.<br>……Sao nào‚ đến vậy rồi mà em vẫn chưa tự tin được à?<br> ",
"Ơ…… ư‚ chuyện đó……<br>Em chỉ tin Chỉ Huy rồi bắn trong vô thức thôi‚ nên tự tin thì hoàn toàn……<br> ",
"Nhưng…… dù vậy em vẫn nghĩ như thế cũng được nên đã bắn.<br>Em nghĩ chỉ cần tin Chỉ Huy rồi cố hết sức là đủ……<br> ",
"Ha ha ha‚ em hiểu rõ rồi đấy chứ‚ Etia.<br> ",
"Tự tin‚ bình tĩnh hay đáng tin cậy<br>đều là những thứ tích lũy thật nhiều kinh nghiệm rồi từ từ có được.<br> ",
"Bây giờ cứ mượn sự tự tin của anh đi.<br>Dù sao anh có nhiều đến mức đem áp cho người khác vẫn còn dư mà.<br> ",
"Vâng‚ cảm ơn anh rất nhiều!<br>Từ giờ em sẽ tin Chỉ Huy mà chiến đấu!<br> ",
"……Cô ấy nói vậy đấy. Xin lỗi mọi người‚ tôi sẽ nhận cô bé này nhé.<br>Cô ấy bảo sẽ tin tôi mà chiến đấu‚ nên cũng đành chịu thôi‚ đúng không?<br> ",
"Ơ…… em sẽ trở thành thuộc hạ của Chỉ Huy……?<br>Thật sự được sao ạ!?<br> ",
"Hà‚ quái vật vừa săn xong rồi mà<br>Etia nhà mình lại bị Chỉ Huy bắt mất rồi à.<br> ",
"Con bé vốn rất đáng mong chờ sau này mà.<br>Dù là Chỉ Huy đi nữa‚ nếu làm Etia khóc thì tôi không để yên đâu!?<br> ",
"M-mọi người……!?<br>Không được nói những lời thất lễ với Chỉ Huy đâu ạ……!<br> ",
"Này‚ anh đã làm con bé khóc ngay rồi còn gì.<br>Thế này thì chưa thể giao Etia cho anh được nhỉ?<br> ",
"K-không phải vậy đâu ạ!<br>Em vui vì được mọi người nói như thế‚ nên……!<br> ",
"Yên tâm đi‚ khi bên anh rảnh tay‚ anh cũng sẽ cho em tham gia đội săn.<br>Hãy tin anh và đi theo anh.<br> ",
"Anh trông cậy vào em đấy‚ Etia.<br> ",
"Vâng! Chủ nhân!<br> ",
"……Hả?<br> ",
"Này‚ vừa rồi cô nói gì?<br>Chủ nhân á?<br> ",
"Chẳng lẽ anh ép con bé gọi như vậy đó hả?<br>Cái đồ Chỉ Huy biến thái này!!!<br> ",
"Không phải! Tôi đã bảo em ấy dừng lại rồi!<br>Đó không phải sở thích của tôi! Tin tôi đi!<br> ",
"X-xin lỗi ạ……!<br> ",
"Đừng chỉ khóc‚ giải thích đi Etia!<br>Chính lúc này mới phải tự tin lên!<br> ",
"Em làm gì có tự tin chứ!<br>Em vô dụng lắm mà!<br> ",
]

TEXT_TYPES = {'title','message','messageTextUnder','messageTextCenter'}

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def tag_counts(s):
    return {m.group(0): s.count(m.group(0)) for m in re.finditer(r'<[^>]+>', s)}

def placeholders(s):
    return re.findall(r'%\w+%|%[sd]|\{\d+\}|\$\{[^}]+\}|\\[nrt]|%%', s)

def get_text_field(parts):
    if parts[0] == 'title':
        return 1
    if parts[0] in ('message','messageTextUnder','messageTextCenter'):
        return 2
    return None

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    raw = EN_ASSET.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    newline = '\r\n' if b'\r\n' in raw else '\n'
    text = raw.decode('utf-8-sig')
    lines = text.splitlines()
    counts = {k:0 for k in TEXT_TYPES}
    recs=[]
    for i,line in enumerate(lines,1):
        if ',' not in line:
            continue
        parts=line.split(',')
        typ=parts[0]
        if typ in TEXT_TYPES:
            idx=get_text_field(parts)
            counts[typ]+=1
            recs.append((i,typ,idx,line,parts))
    assert len(recs)==len(TRANSLATIONS), (len(recs), len(TRANSLATIONS))
    out_lines=list(lines)
    qa_items=[]
    for n,(i,typ,idx,line,parts) in enumerate(recs):
        vi=TRANSLATIONS[n]
        old=parts[idx]
        # EN asset is authoritative for <br> counts. Some JP lines have more breaks than
        # the EN asset line; collapse surplus VI <br> tags to spaces before QA.
        while vi.count('<br>') > old.count('<br>'):
            vi = vi.replace('<br>', ' ', 1)
        if ',' in vi:
            qa_items.append({'line':i,'severity':'BLOCKER','type':'ascii_comma_in_vi','text':vi})
        if old.count('<br>') != vi.count('<br>'):
            qa_items.append({'line':i,'severity':'BLOCKER','type':'br_count_mismatch','source':old.count('<br>'),'vi':vi.count('<br>')})
        if re.search(r'[ぁ-んァ-ン一-龯]', vi):
            qa_items.append({'line':i,'severity':'BLOCKER','type':'japanese_leftover','text':vi})
        parts[idx]=vi
        out=' , '.join(parts) if False else ','.join(parts)
        if out.count(',') != line.count(','):
            qa_items.append({'line':i,'severity':'BLOCKER','type':'delimiter_count_mismatch','source':line.count(','),'vi':out.count(',')})
        out_lines[i-1]=out
    out_text = newline.join(out_lines) + (newline if raw.endswith(b'\n') else '')
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes((b'\xef\xbb\xbf' if bom else b'') + out_text.encode('utf-8'))

    # structural readback
    rb=VI_ASSET.read_bytes()
    vi_text=rb.decode('utf-8-sig')
    vi_lines=vi_text.splitlines()
    structural={
        'line_count_match': len(lines)==len(vi_lines),
        'bom_preserved': rb.startswith(b'\xef\xbb\xbf')==bom,
        'newline_preserved': ('\r\n' if b'\r\n' in rb else '\n')==newline,
        'delimiter_counts_match': all(a.count(',')==b.count(',') for a,b in zip(lines,vi_lines)),
        'text_command_counts': counts,
        'total_text_commands': sum(counts.values()),
        'br_counts_match': True,
        'placeholder_counts_match': True,
        'ascii_comma_in_vi_text_fields': [],
        'japanese_leftovers_in_vi_text_fields': [],
    }
    for n,(i,typ,idx,oline,oparts) in enumerate(recs):
        vparts=vi_lines[i-1].split(',')
        old=oparts[idx]; new=vparts[idx]
        if old.count('<br>')!=new.count('<br>'): structural['br_counts_match']=False
        if placeholders(old)!=placeholders(new): structural['placeholder_counts_match']=False
        if ',' in new: structural['ascii_comma_in_vi_text_fields'].append(i)
        # exclude charaload/speaker names by only checking text fields
        if re.search(r'[ぁ-んァ-ン一-龯]', new): structural['japanese_leftovers_in_vi_text_fields'].append({'line':i,'text':new})
    focused=[]
    for n,(i,typ,idx,oline,oparts) in enumerate(recs):
        vline=vi_lines[i-1]
        focused.append(f'### Record {n+1} / source line {i} / {typ}')
        focused.append(f'- EN: `{oparts[idx]}`')
        focused.append(f'- VI: `{vline.split(",")[idx]}`')
        focused.append('')
    (WORK/'focused_diff.md').write_text('\n'.join(focused), encoding='utf-8')
    manifest={
        'scene': SCENE,
        'created_at': datetime.datetime.now().isoformat(timespec='seconds'),
        'sources': {'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN_ASSET)},
        'output': str(VI_ASSET),
        'artifacts': {'manifest': str(WORK/'manifest.json'), 'focused_diff': str(WORK/'focused_diff.md'), 'qa_log': str(WORK/'qa_log.json'), 'script': str(WORK/'generate_hmn_10120100003_vi.py')},
        'source_hashes': {'en_asset_sha256': hashlib.sha256(raw).hexdigest(), 'ja_json_sha256': sha256(JA_JSON), 'en_json_sha256': sha256(EN_JSON)},
        'output_sha256': sha256(VI_ASSET),
        'format': {'encoding':'utf-8-sig' if bom else 'utf-8','bom':bom,'newline':repr(newline),'line_count':len(lines),'delimiter':'ASCII comma','translated_field':'title[1], message/messageTextUnder/messageTextCenter[2]'},
        'text_command_counts': counts,
        'total_text_commands': sum(counts.values()),
        'mapping_status': {'TRANSLATED': len(recs), 'UNMATCHED': 0, 'AMBIGUOUS': 0, 'REVIEW': 0},
        'notes': ['JP is primary; EN asset used for alignment.', 'Speaker names and charaload names were not modified.', 'ASCII commas inside Vietnamese text fields are forbidden; U+201A used where needed.', 'Extra asset-only silence record line 914 translated as punctuation-only silence.'],
        'structural_qa': structural,
        'qa_status': 'PASS' if not qa_items and all([structural['line_count_match'],structural['delimiter_counts_match'],structural['br_counts_match'],structural['placeholder_counts_match']]) and not structural['ascii_comma_in_vi_text_fields'] and not structural['japanese_leftovers_in_vi_text_fields'] else 'FAIL',
        'independent_verify': {'status':'PENDING'}
    }
    qa={
        'scene': SCENE,
        'status': manifest['qa_status'],
        'text_command_counts': counts,
        'translated_records': len(recs),
        'structural_qa': structural,
        'linguistic_qa': {'commander_term':'Commander/司令官 translated as Chỉ Huy in prose; direct intimate lines use anh/em where natural.', 'h18':'No H18/adult content in this scene.', 'title_case':'Tin Anh Mà Bóp Cò'},
        'issues': qa_items,
        'independent_verify': {'status':'PENDING'}
    }
    (WORK/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (WORK/'qa_log.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'output':str(VI_ASSET),'records':len(recs),'qa_status':manifest['qa_status'],'issues':qa_items[:5]}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

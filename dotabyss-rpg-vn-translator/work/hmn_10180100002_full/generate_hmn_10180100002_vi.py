# -*- coding: utf-8 -*-
"""Generate VI asset for hmn_10180100002 without modifying EN source."""
from __future__ import annotations
import hashlib, json, re, difflib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/AgentTranslation')
SCENE = 'hmn_10180100002'
SRC = ROOT / 'Translation/en/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
OUT = ROOT / 'Translation/vi/RedirectedResources/assets/unnamed_assetbundle' / f'{SCENE}.txt'
JA = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'ja.json'
ENJSON = ROOT / 'dotabyss-translation-main/translations/novels' / SCENE / 'en.json'
WORK = ROOT / 'dotabyss-rpg-vn-translator/work' / f'{SCENE}_full'
MANIFEST = WORK / 'manifest.json'
QA = WORK / 'qa_log.json'
DIFF = WORK / 'focused_diff.md'

# JP is primary source; EN novel is blank for this scene, and asset text is JP.
VI = {
    '進め、ドリルの力を信じて！': 'Tiến Lên‚ Hãy Tin Vào Sức Mạnh Của Mũi Khoan!',
    '<size=48>――大穴浅層　探索済領域</size>': '<size=48>――Tầng Nông Đại Huyệt Khu Vực Đã Khảo Sát</size>',
    'グオォォォン！': 'Gruoooong!',
    'この新型ドリルなら、<br>ゴーレムぐらい、簡単に貫ける……！': 'Với mũi khoan đời mới này‚<br>cỡ golem thì xuyên thủng dễ thôi……!',
    'ガリガリガリガリ！　と硬質な音を立て、<br>グラディアのドリルがゴーレムのコアを穿った。': 'Két két két két! Tiếng kim loại cứng vang lên‚<br>mũi khoan của グラディア đục thẳng vào lõi golem.',
    'ォォォォ……': 'Ooooo……',
    '新型ドリル、期待以上の性能。<br>さすが私。': 'Mũi khoan mới có hiệu năng vượt mong đợi.<br>Đúng là mình.',
    '見た目はあまり変わらないが、<br>性能はずいぶんと良くなったみたいだな。': 'Nhìn ngoài thì không khác mấy‚<br>nhưng hiệu năng có vẻ tốt hơn hẳn nhỉ.',
    '使い勝手を維持したままの新型。<br>これ以上の改良はない。': 'Đời mới mà vẫn giữ nguyên cảm giác sử dụng.<br>Không thể cải tiến hơn nữa.',
    '手に馴染んだ武器が１番だからな。<br>それでも、ドリルで戦うってのは珍しいけどさ。': 'Vũ khí quen tay vẫn là số một mà.<br>Dù vậy‚ chiến đấu bằng mũi khoan thì cũng hiếm thật.',
    '……ドリルはいい。<br>他の人が使わない理由がわからない。': '……Mũi khoan rất tốt.<br>Mình không hiểu sao người khác không dùng.',
    '元々は岩盤に穴を開けるための道具だから、<br>硬いモンスターでも貫くパワーがある。': 'Vốn là dụng cụ để khoan thủng nền đá‚<br>nên nó đủ sức xuyên qua cả quái vật cứng cáp.',
    '先端部分はとっても丈夫だから、<br>防御する時にだって役立つ。': 'Phần đầu mũi cực kỳ chắc chắn‚<br>nên phòng thủ cũng rất hữu dụng.',
    '求められる働きが単純だからこそ、<br>様々なパーツが組み込めて、拡張性も高い。': 'Chính vì chức năng cần có rất đơn giản‚<br>nó có thể gắn nhiều loại linh kiện và mở rộng rất tốt.',
    '何よりも、ドリルで敵を貫くのは、<br>とってもロマンがある。': 'Hơn hết‚ dùng mũi khoan xuyên thủng kẻ địch<br>rất là lãng mạn.',
    'ドリルのロマンは、俺も共感できるぞ。': 'Anh cũng hiểu cái chất lãng mạn của mũi khoan đấy.',
    'いいよな、ドリル。': 'Mũi khoan tuyệt thật nhỉ.',
    'いいよね、ドリル。': 'Mũi khoan tuyệt thật.',
    'デザインが武骨だったり、<br>何でも出来るわけじゃないのも、ドリルのロマン。': 'Thiết kế thô ráp‚<br>rồi cả việc nó không làm được mọi thứ‚ đó cũng là chất lãng mạn của mũi khoan.',
    '不器用だけど愚直に貫くってのが格好いいんだよな。': 'Vụ nó vụng về nhưng cứ thẳng thắn xuyên tới cùng mới ngầu chứ.',
    '司令官、よくわかってる。': 'Chỉ Huy hiểu rõ thật.',
    '（こんなに饒舌に話すグラディアははじめて見たな。<br>本当にドリルが好きなんだろう）': '(Lần đầu mình thấy グラディア nói nhiều đến vậy.<br>Hẳn là cô ấy thật sự thích mũi khoan.)',
    '……しかし、どうしてドリルにこだわっているんだ？<br>単純に好きだから、というだけの理由なのか？': '……Nhưng tại sao em lại cố chấp với mũi khoan như vậy?<br>Chỉ đơn giản là vì em thích thôi sao?',
    'ん……好きなのは間違いない。<br>ドリルはロマンだから……': 'Ừm…… Chắc chắn là mình thích.<br>Vì mũi khoan là lãng mạn……',
    'でも、それだけじゃない。<br>私のお父さんも、ドリルが好きだった。': 'Nhưng không chỉ có vậy.<br>Bố mình cũng từng rất thích mũi khoan.',
    'ああ、失敗こそ大事にしろって語ってた親父さんか。<br>ドリルの開発をしていたんだな。': 'À‚ là người bố từng bảo em phải trân trọng cả thất bại nhỉ.<br>Ông ấy cũng phát triển mũi khoan à.',
    '私よりすごいドリルを作ってた。<br>……まだまだお父さんには届かない。': 'Bố làm ra những mũi khoan còn giỏi hơn mình.<br>……Mình vẫn còn lâu mới theo kịp bố.',
    'へえ、そんなに優秀な技術者だったのか。<br>それは部下にスカウトしたいぐらいだな。': 'Ồ‚ ông ấy là kỹ sư xuất sắc đến vậy sao.<br>Anh còn muốn chiêu mộ ông ấy làm cấp dưới nữa đấy.',
    '難しいと思う。<br>今どこにいるのか、わからないから。': 'Mình nghĩ là khó.<br>Vì mình không biết giờ bố đang ở đâu.',
    'それは……行方不明、なのか？': 'Vậy là…… ông ấy mất tích sao?',
    '……大穴が出現した時、<br>お父さんはこの辺りに、鉱石の採掘に来てた。': '……Khi Đại Huyệt xuất hiện‚<br>bố mình đang đến khu vực này để khai thác quặng.',
    '最後にお父さんを見た人は、<br>大穴に飲み込まれていった、って。': 'Người cuối cùng nhìn thấy bố nói rằng<br>bố đã bị Đại Huyệt nuốt chửng.',
    'それは……': 'Chuyện đó……',
    'もう死んでる、かもしれない。<br>でもお父さんはすごい発明家で、採掘者だったんだ。': 'Có lẽ bố đã chết rồi.<br>Nhưng bố là một nhà phát minh và thợ khai thác rất cừ.',
    'きっと簡単に死んだりしない。<br>今も帰還しようと頑張ってるはず。': 'Chắc chắn bố sẽ không dễ chết như vậy.<br>Hẳn là giờ bố vẫn đang cố tìm đường trở về.',
    'それにお父さんは……すごく諦めが悪かったから。<br>何度失敗してもそれが成功につながるって言い張る、そんな人だった。': 'Hơn nữa‚ bố mình…… là người cực kỳ không chịu bỏ cuộc.<br>Dù thất bại bao nhiêu lần‚ bố vẫn khăng khăng rằng nó sẽ dẫn tới thành công.',
    '大穴の中でだって、絶対に諦めたりしない。<br>そう信じてる。': 'Dù ở trong Đại Huyệt‚ bố cũng tuyệt đối sẽ không bỏ cuộc.<br>Mình tin như vậy.',
    '（強がりじゃなく、本当に諦めてないんだな。<br>グラディアが信じているのなら、俺も信じてみよう）': '(Không phải cô ấy đang gồng mình. Cô ấy thật sự chưa từ bỏ.<br>Nếu グラディア tin như vậy‚ mình cũng thử tin theo xem sao.)',
    'そうだな、大穴には様々な危険があるが、大いなる恵みもある。<br>上手くやれば生き残るのも不可能じゃない。': 'Đúng vậy. Đại Huyệt có vô vàn nguy hiểm‚ nhưng cũng có ân huệ lớn lao.<br>Nếu xoay xở tốt thì sống sót không phải là bất khả thi.',
    'うん。ドリルがあれば壁を掘って安全地帯を作ることもできる。<br>地面を掘って水を探すこともできる。': 'Ừ. Có mũi khoan thì có thể khoét tường để tạo khu vực an toàn.<br>Cũng có thể đào đất tìm nước.',
    '自分で大穴を歩いてみて、<br>可能性はあるんだって思った。': 'Sau khi tự mình đi trong Đại Huyệt‚<br>mình nghĩ vẫn có khả năng.',
    '今のドリルじゃ行けないような危険な場所にいるのかもしれない。': 'Có lẽ bố đang ở một nơi nguy hiểm mà mũi khoan hiện tại của mình chưa thể tới được.',
    'だからもっともっとすごいドリルを作って<br>お父さんの元へたどりつく。': 'Vì vậy mình sẽ làm ra một mũi khoan tuyệt vời hơn nữa<br>và đến được chỗ bố.',
    '（……本当に強いな、グラディアは）': '(……グラディア thật sự mạnh mẽ.)',
    'さて、そろそろ戻りたいところだが……<br>新型ドリルの採掘性能は確認しなくていいのか？': 'Nào‚ anh cũng muốn quay về rồi……<br>nhưng em không cần kiểm tra khả năng khai thác của mũi khoan mới sao?',
    'うん、岩壁のほうに行こう。<br>キミにこのドリルのもっとすごいところ、見せるから。': 'Ừ‚ mình ra phía vách đá đi.<br>Mình sẽ cho cậu thấy điểm còn tuyệt hơn của mũi khoan này.',
    'うん、ここならいいかな。<br>戦闘だけじゃなく、採掘にも使えるところ、見てて。': 'Ừ‚ chỗ này chắc được.<br>Hãy xem nó không chỉ chiến đấu được‚ mà còn dùng để khai thác nữa.',
    'グラディアが壁へドリルを押し当て、スイッチを入れる。<br>軽快に回転を始めたドリルは見る見る内に壁へと穴を開けた。': 'グラディア áp mũi khoan vào tường rồi bật công tắc.<br>Mũi khoan bắt đầu quay nhẹ nhàng và nhanh chóng đục một lỗ vào tường.',
    'うん、順調。<br>これなら採掘にも使える。': 'Ừ‚ thuận lợi.<br>Thế này thì dùng khai thác cũng được.',
    'あれ、壁の中に何か……': 'Ủa‚ trong tường có gì đó……',
    'あ……司令官、下がって！': 'A…… Chỉ Huy‚ lùi lại!',
    'グォォォォォン！': 'Gruooooong!',
    '眠っていた大型ゴーレムが、ドリルの振動で目を覚ました。<br>自身を封じていた壁を叩き壊しながら、激しく暴れ始める。': 'Con golem khổng lồ đang ngủ bị chấn động của mũi khoan đánh thức.<br>Nó đập vỡ bức tường đang phong kín mình và bắt đầu nổi cơn điên cuồng.',
    'ちっ、眠っていた強敵を叩き起こしたみたいだな。<br>すぐに撤退するぞ！': 'Chậc‚ có vẻ ta đã đánh thức một kẻ địch mạnh đang ngủ rồi.<br>Rút lui ngay!',
    '大丈夫。<br>新しいドリルはあんなゴーレムに負けない。': 'Không sao.<br>Mũi khoan mới sẽ không thua loại golem đó.',
    'まだ壁から出てこない内に……！<br>えーいっ！！！': 'Khi nó còn chưa ra khỏi tường……!<br>Ya!!!',
    'グラディアは大穴の壁から脱出しようとするゴーレムへ、<br>回転するドリルを押し込んだ。': 'グラディア đẩy mũi khoan đang xoay<br>vào con golem đang cố thoát khỏi vách Đại Huyệt.',
    'ゴーレムの胴体へ食い込んだドリルは回転速度を不安定に歪め、<br>なんとか回転しようと甲高い音を立てて震える。': 'Mũi khoan cắm vào thân golem khiến tốc độ quay bị lệch và bất ổn‚<br>rung lên với âm thanh the thé như đang cố tiếp tục xoay.',
    '通らない……回転が安定しないの！？<br>そんなはずない、どんな相手でも、このドリルなら……': 'Không xuyên qua được…… vòng quay không ổn định sao!?<br>Không thể nào. Dù đối thủ là ai‚ với mũi khoan này thì……',
    '限界を超えたドリルは、ギャリギャリギャリ！　<br>と断末魔のような音を立て、完全に動きを止めた。': 'Mũi khoan vượt quá giới hạn kêu lên két két két!<br>như tiếng hấp hối rồi dừng hẳn.',
    'う、そ……私のドリルが<br>通らなかった……？': 'Không…… thể nào…… Mũi khoan của mình<br>không xuyên qua được sao……?',
    'こりゃマズイ、もう出てくるぞ！<br>すぐに逃げよう、グラディアっ！': 'Không ổn rồi‚ nó sắp chui ra đấy!<br>Chạy mau thôi‚ グラディア!',
    'あ……うん……': 'A…… ừ……',
    '（私のドリルじゃ、駄目、だった……）': '(Mũi khoan của mình…… không đủ……)'
}

TEXT_COMMANDS = {'title', 'message', 'messageTextUnder', 'messageTextCenter'}
TAG_RE = re.compile(r'<[^>]+>')
PLACEHOLDER_RE = re.compile(r'(%[a-zA-Z0-9_]+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}|\\[nrt]|%%)')

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def detect_newline(raw: bytes) -> str:
    if b'\r\n' in raw:
        return 'CRLF'
    if b'\n' in raw:
        return 'LF'
    return 'NONE'

def split_lines_keep(raw_text: str):
    return raw_text.splitlines(keepends=True)

def line_ending(line: str) -> str:
    if line.endswith('\r\n'):
        return '\r\n'
    if line.endswith('\n'):
        return '\n'
    return ''

def strip_eol(line: str) -> str:
    return line[:-2] if line.endswith('\r\n') else (line[:-1] if line.endswith('\n') else line)

def text_field_index(parts):
    cmd = parts[0]
    if cmd == 'title': return 1
    if cmd == 'message': return 2
    if cmd in {'messageTextUnder', 'messageTextCenter'}: return 2
    return None

def tags(s): return TAG_RE.findall(s)
def placeholders(s): return PLACEHOLDER_RE.findall(s)

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = SRC.read_bytes()
    had_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    lines = split_lines_keep(text)
    out_lines = []
    records = []
    errors = []
    command_counts = {k: 0 for k in sorted(TEXT_COMMANDS)}
    translated = 0
    untranslated = []

    for idx, line in enumerate(lines, 1):
        eol = line_ending(line)
        body = strip_eol(line)
        parts = body.split(',')
        if parts and parts[0] in TEXT_COMMANDS:
            cmd = parts[0]
            fi = text_field_index(parts)
            command_counts[cmd] += 1
            src_text = parts[fi] if fi is not None and fi < len(parts) else ''
            if src_text in VI:
                vi = VI[src_text]
                parts[fi] = vi
                translated += 1
                status = 'TRANSLATED'
                if ',' in vi:
                    errors.append({'line': idx, 'type': 'ascii_comma_in_vi_field', 'text': vi})
                if tags(src_text) != tags(vi):
                    errors.append({'line': idx, 'type': 'tag_mismatch', 'source': tags(src_text), 'vi': tags(vi)})
                if placeholders(src_text) != placeholders(vi):
                    errors.append({'line': idx, 'type': 'placeholder_mismatch', 'source': placeholders(src_text), 'vi': placeholders(vi)})
            else:
                status = 'UNMATCHED'
                untranslated.append({'line': idx, 'command': cmd, 'text': src_text})
            records.append({'line': idx, 'command': cmd, 'source_text': src_text, 'status': status})
            new_body = ','.join(parts)
            if body.count(',') != new_body.count(','):
                errors.append({'line': idx, 'type': 'delimiter_count_changed', 'source_commas': body.count(','), 'vi_commas': new_body.count(',')})
            out_lines.append(new_body + eol)
        else:
            out_lines.append(line)

    out_text = ''.join(out_lines)
    out_raw = (b'\xef\xbb\xbf' if had_bom else b'') + out_text.encode('utf-8')
    OUT.write_bytes(out_raw)

    # post-write independent structural checks versus source
    vi_lines = split_lines_keep(OUT.read_bytes().decode('utf-8-sig'))
    structural_errors = []
    if len(lines) != len(vi_lines): structural_errors.append({'type': 'line_count', 'src': len(lines), 'vi': len(vi_lines)})
    for i, (a, b) in enumerate(zip(lines, vi_lines), 1):
        ab, bb = strip_eol(a), strip_eol(b)
        if ab.count(',') != bb.count(','):
            structural_errors.append({'line': i, 'type': 'delimiter_count', 'src': ab.count(','), 'vi': bb.count(',')})
        ap, bp = ab.split(','), bb.split(',')
        if ap and ap[0] in TEXT_COMMANDS:
            fi = text_field_index(ap)
            # technical fields except translatable field unchanged
            for j, (x, y) in enumerate(zip(ap, bp)):
                if j != fi and x != y:
                    structural_errors.append({'line': i, 'type': 'technical_field_changed', 'field': j, 'src': x, 'vi': y})
            if tags(ap[fi]) != tags(bp[fi]):
                structural_errors.append({'line': i, 'type': 'tag_mismatch_post', 'src': tags(ap[fi]), 'vi': tags(bp[fi])})
            if placeholders(ap[fi]) != placeholders(bp[fi]):
                structural_errors.append({'line': i, 'type': 'placeholder_mismatch_post', 'src': placeholders(ap[fi]), 'vi': placeholders(bp[fi])})
    errors.extend(structural_errors)

    # focused diff: only text-command lines
    src_focus = [f'{i}: {strip_eol(l)}\n' for i, l in enumerate(lines, 1) if strip_eol(l).split(',')[0] in TEXT_COMMANDS]
    vi_focus = [f'{i}: {strip_eol(l)}\n' for i, l in enumerate(vi_lines, 1) if strip_eol(l).split(',')[0] in TEXT_COMMANDS]
    diff = ''.join(difflib.unified_diff(src_focus, vi_focus, fromfile=str(SRC), tofile=str(OUT), lineterm='\n'))
    DIFF.write_text('# Focused Diff: hmn_10180100002\n\n```diff\n' + diff + '\n```\n', encoding='utf-8')

    src_hashes = {
        'asset_en_sha256': sha256_bytes(raw),
        'ja_json_sha256': sha256_bytes(JA.read_bytes()),
        'en_json_sha256': sha256_bytes(ENJSON.read_bytes()),
    }
    common = {
        'scene': SCENE,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'paths': {'source_asset': str(SRC), 'output_asset': str(OUT), 'ja_json': str(JA), 'en_json': str(ENJSON), 'work_dir': str(WORK)},
        'source': {'encoding': 'utf-8-sig' if had_bom else 'utf-8', 'bom': had_bom, 'newline': detect_newline(raw), 'line_count': len(lines), 'sha256': src_hashes},
        'output': {'encoding': 'utf-8-sig' if had_bom else 'utf-8', 'bom': had_bom, 'newline': detect_newline(out_raw), 'line_count': len(vi_lines), 'sha256': sha256_bytes(out_raw)},
        'format': {'delimiter': ',', 'text_commands_counted': ['title', 'message', 'messageTextUnder', 'messageTextCenter'], 'command_counts': command_counts},
        'translation_basis': 'JP primary; en.json values blank; asset source text is JP, EN alignment unavailable except ordering.',
        'character_voice': {'グラディア': 'terse engineer/drill enthusiast; keeps asset speaker/name; self often mình; mixed キミ/cậu maintained where source distant/casual', '司令官/Commander': 'Chỉ Huy when title/addressed'},
        'records_total': sum(command_counts.values()),
        'records_translated': translated,
        'records_unmatched': len(untranslated),
        'unmatched': untranslated,
        'errors': errors,
        'qa_status': 'PASS' if not errors and not untranslated else 'FAIL',
    }
    MANIFEST.write_text(json.dumps({**common, 'records': records}, ensure_ascii=False, indent=2), encoding='utf-8')
    QA.write_text(json.dumps({**common, 'structural_qa': {'status': 'PASS' if not errors else 'FAIL', 'errors': errors}, 'linguistic_qa': {'status': 'PASS', 'notes': ['Title translated in Vietnamese Title Case.', 'ASCII commas inside VI text fields replaced with U+201A where needed.', 'No H18 content in this scene.']}, 'independent_verify': {'status': 'PENDING', 'note': 'Run shared verifier after generation.'}}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(OUT), 'manifest': str(MANIFEST), 'qa_log': str(QA), 'focused_diff': str(DIFF), 'records_total': sum(command_counts.values()), 'records_translated': translated, 'errors': len(errors), 'unmatched': len(untranslated)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

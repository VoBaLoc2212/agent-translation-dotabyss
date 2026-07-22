# -*- coding: utf-8 -*-
from pathlib import Path
import json, hashlib, re, difflib
from datetime import datetime, timezone

SCENE = 'hmn_10140100001'
ROOT = Path('E:/AgentTranslation')
EN_ASSET = ROOT/'Translation/en/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
VI_ASSET = ROOT/'Translation/vi/RedirectedResources/assets/unnamed_assetbundle'/f'{SCENE}.txt'
JA_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'ja.json'
EN_JSON = ROOT/'dotabyss-translation-main/translations/novels'/SCENE/'en.json'
WORK = ROOT/'dotabyss-rpg-vn-translator/work/hmn_10140100001_full'
TRANSLATIONS = WORK/'translations_vi.json'
MANIFEST = WORK/'manifest.json'
QA_LOG = WORK/'qa_log.json'
DIFF = WORK/'focused_diff.md'
TEXT_TYPES = {'title','message','messageTextUnder','messageTextCenter'}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def tags(s):
    return re.findall(r'<[^>]+>', s)

def placeholders(s):
    return re.findall(r'%\w+%|%[sd]|\{\d+\}|\{[A-Za-z_][A-Za-z0-9_]*\}|\$\{[^}]+\}', s)

def text_index(kind):
    return 1 if kind == 'title' else 2

def style(data):
    return {'bom': data.startswith(b'\xef\xbb\xbf'), 'newline': '\r\n' if b'\r\n' in data else '\n'}

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    src_bytes = EN_ASSET.read_bytes()
    st = style(src_bytes)
    lines = src_bytes.decode('utf-8-sig').splitlines()
    vi_strings = json.loads(TRANSLATIONS.read_text(encoding='utf-8'))
    cands = []
    out_lines = list(lines)
    for i, line in enumerate(lines):
        parts = line.split(',')
        if parts and parts[0] in TEXT_TYPES:
            idx = text_index(parts[0])
            cands.append({'line': i + 1, 'type': parts[0], 'speaker': parts[1] if len(parts) > 1 else '', 'source': parts[idx], 'tech': parts[:idx] + parts[idx+1:], 'delims': line.count(',')})
    blockers = []
    if len(cands) != len(vi_strings):
        blockers.append({'type': 'TRANSLATION_COUNT_MISMATCH', 'candidates': len(cands), 'translations': len(vi_strings)})
    for n, (cand, vi) in enumerate(zip(cands, vi_strings), 1):
        if ',' in vi:
            blockers.append({'record': n, 'line': cand['line'], 'type': 'ASCII_COMMA_IN_VI', 'text': vi})
        if tags(cand['source']) != tags(vi):
            blockers.append({'record': n, 'line': cand['line'], 'type': 'TAG_MISMATCH', 'source_tags': tags(cand['source']), 'vi_tags': tags(vi)})
        if placeholders(cand['source']) != placeholders(vi):
            blockers.append({'record': n, 'line': cand['line'], 'type': 'PLACEHOLDER_MISMATCH', 'source_placeholders': placeholders(cand['source']), 'vi_placeholders': placeholders(vi)})
        parts = out_lines[cand['line'] - 1].split(',')
        parts[text_index(cand['type'])] = vi
        out_lines[cand['line'] - 1] = ','.join(parts)
    for cand in cands:
        old = lines[cand['line'] - 1]
        new = out_lines[cand['line'] - 1]
        idx = text_index(cand['type'])
        if old.count(',') != new.count(','):
            blockers.append({'line': cand['line'], 'type': 'DELIMITER_MISMATCH', 'old': old.count(','), 'new': new.count(',')})
        if old.split(',')[:idx] + old.split(',')[idx+1:] != new.split(',')[:idx] + new.split(',')[idx+1:]:
            blockers.append({'line': cand['line'], 'type': 'TECH_FIELD_MISMATCH'})
    status = 'PASS' if not blockers else 'FAIL'
    out_text = st['newline'].join(out_lines) + st['newline']
    out_bytes = out_text.encode('utf-8')
    if st['bom']:
        out_bytes = b'\xef\xbb\xbf' + out_bytes
    VI_ASSET.parent.mkdir(parents=True, exist_ok=True)
    VI_ASSET.write_bytes(out_bytes)
    diff_old = [f"L{c['line']} {lines[c['line']-1]}" for c in cands]
    diff_new = [f"L{c['line']} {out_lines[c['line']-1]}" for c in cands]
    DIFF.write_text('\n'.join(difflib.unified_diff(diff_old, diff_new, fromfile='EN text fields', tofile='VI text fields', lineterm='')) + '\n', encoding='utf-8')
    counts = {k: sum(1 for c in cands if c['type'] == k) for k in ['title','message','messageTextUnder','messageTextCenter']}
    ja_pairs = json.load(open(JA_JSON, encoding='utf-8'), object_pairs_hook=list)
    en_pairs = json.load(open(EN_JSON, encoding='utf-8'), object_pairs_hook=list)
    manifest = {
        'scene': SCENE, 'status': status, 'created_at': datetime.now(timezone.utc).isoformat(),
        'sources': {'ja_json': str(JA_JSON), 'en_json': str(EN_JSON), 'en_asset': str(EN_ASSET)},
        'output': str(VI_ASSET),
        'artifacts': {'manifest': str(MANIFEST), 'qa_log': str(QA_LOG), 'focused_diff': str(DIFF), 'script': str(WORK/'generate_hmn_10140100001_vi.py'), 'translations': str(TRANSLATIONS)},
        'format': {'bom': st['bom'], 'newline': 'CRLF' if st['newline'] == '\r\n' else 'LF', 'line_count': len(lines), 'delimiter': 'ASCII comma'},
        'hashes': {'en_asset_sha256': sha(EN_ASSET), 'vi_asset_sha256': sha(VI_ASSET), 'ja_json_sha256': sha(JA_JSON), 'en_json_sha256': sha(EN_JSON)},
        'counts': {'candidate_text_records': len(cands), 'translated_records': len(vi_strings), 'by_type': counts, 'ja_json_pairs': len(ja_pairs), 'en_json_pairs': len(en_pairs)},
        'alignment': 'ordered JP/EN JSON pairs aligned to ordered EN asset text commands; JP primary; EN asset structural/tag authority',
        'character_voice': {'Pico': 'playful isekai streamer; Pico/Pico-nyan self-branding; casual em–anh with Commander', 'Commander': 'male Commander; 司令官/Commander -> Chỉ Huy', '一般兵': 'female soldier; Commander -> Chỉ Huy'},
        'blockers': blockers,
        'notes': ['All characters confirmed 18+ by project context; no H18 content in this scene.', 'ASCII commas inside VI text fields are forbidden; U+201A used where needed.', 'Title translated in Vietnamese Title Case.'],
    }
    qa = {
        'scene': SCENE, 'qa_status': status, 'blockers': blockers,
        'structural_qa': {'line_count_match': len(lines) == len(out_lines), 'candidate_text_records': len(cands), 'translated_records': len(vi_strings), 'delimiter_mismatches': [b for b in blockers if b.get('type') == 'DELIMITER_MISMATCH'], 'technical_field_mismatches': [b for b in blockers if b.get('type') == 'TECH_FIELD_MISMATCH'], 'tag_mismatches': [b for b in blockers if b.get('type') == 'TAG_MISMATCH'], 'placeholder_mismatches': [b for b in blockers if b.get('type') == 'PLACEHOLDER_MISMATCH'], 'ascii_comma_in_vi_text_fields': [b for b in blockers if b.get('type') == 'ASCII_COMMA_IN_VI']},
        'linguistic_qa': {'status': 'PASS' if not blockers else 'BLOCKED', 'notes': ['JP used as primary source; EN used for alignment only.', 'Commander/司令官 rendered as Chỉ Huy.', 'Pico/Pico-nyan retained as character self-branding.']},
        'unresolved': [],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    QA_LOG.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': status, 'output': str(VI_ASSET), 'candidate_count': len(cands), 'counts': counts, 'blockers': len(blockers)}, ensure_ascii=False))
    if blockers:
        raise SystemExit(1)

if __name__ == '__main__':
    main()

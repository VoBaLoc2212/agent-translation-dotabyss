#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild VI assets deterministically using EN asset as structural authority.
Applies JP->VI dictionaries to EN asset files while preserving <br> counts and suffixes exactly.
"""
import sys
import json
import re
from pathlib import Path

def build_fullwidth_to_halfwidth_table():
    mapping = {}
    for i in range(0xFF01, 0xFF5F):
        mapping[i] = i - 0xFEE0
    mapping[0x3000] = 0x0020
    return {k: v for k, v in mapping.items()}

FULLWIDTH_TO_HALFWIDTH = build_fullwidth_to_halfwidth_table()

def normalize_for_mapping(s: str) -> str:
    s = s.lower()
    s = s.translate(FULLWIDTH_TO_HALFWIDTH)
    s = re.sub(r'<br\s*/?>', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', '', s)
    return s

def build_vi_asset(root: Path, scene: str):
    en_asset = root / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{scene}.txt"
    vi_asset = root / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{scene}.txt"
    vi_json = root / "dotabyss-rpg-vn-translator/work" / f"{scene}_full/vi.json"
    en_json = root / "dotabyss-translation-main/translations/novels" / scene / "en.json"
    
    if not (en_asset.exists() and vi_json.exists() and en_json.exists()):
        print(f"[{scene}] Missing required files, skipping.")
        return False
        
    try:
        vi_map = json.loads(vi_json.read_text(encoding='utf-8-sig'))
        en_map = json.loads(en_json.read_text(encoding='utf-8-sig'))
    except Exception as e:
        print(f"[{scene}] Error parsing JSON: {e}")
        return False
    
    norm_en_to_vi = {}
    for jp_key in set(en_map.keys()) & set(vi_map.keys()):
        en_val = en_map[jp_key]
        vi_val = vi_map[jp_key]
        key = normalize_for_mapping(en_val)
        norm_en_to_vi[key] = vi_val
        
    jp_to_vi = {k: v for k, v in vi_map.items()}
    
    en_bytes = en_asset.read_bytes()
    has_bom = en_bytes.startswith(b'\xef\xbb\xbf')
    text = en_bytes.decode('utf-8-sig').replace('\r\r\n', '\r\n')
    lines = text.splitlines(keepends=True)
    
    cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
    out_lines = []
    
    for line in lines:
        if line.endswith('\r\n'):
            ending = '\r\n'
            line_core = line[:-2]
        elif line.endswith('\n'):
            ending = '\n'
            line_core = line[:-1]
        else:
            ending = ''
            line_core = line
            
        stripped = line_core.lstrip('\ufeff')
        if not any(stripped.startswith(c) for c in cmds):
            out_lines.append(line_core + ending)
            continue
            
        if stripped.startswith('title,'):
            parts = line_core.split(',', 1)
            if len(parts) >= 2:
                text_field = parts[1]
                if text_field in jp_to_vi:
                    new_text_field = jp_to_vi[text_field].replace(',', '‚')
                else:
                    new_text_field = text_field.replace(',', '‚')
                parts[1] = new_text_field
                out_lines.append(','.join(parts) + ending)
            else:
                out_lines.append(line_core + ending)
        else:
            parts = line_core.split(',', 5)
            if len(parts) < 3:
                out_lines.append(line_core + ending)
                continue
                
            text_field = parts[2]
            key = normalize_for_mapping(text_field)
            
            if key in norm_en_to_vi:
                vi_val = norm_en_to_vi[key]
                en_prefix_match = re.match(r'^(<[^>]+>)+', text_field)
                en_prefix = en_prefix_match.group(0) if en_prefix_match else ''
                en_suffix_match = re.search(r'(?:<[^>]+>\s*)+$', text_field)
                en_suffix = en_suffix_match.group(0) if en_suffix_match else ''
                
                vi_clean = re.sub(r'<[^>]+>', '', vi_val).replace(',', '‚')
                en_inner = text_field[len(en_prefix):]
                if en_suffix:
                    en_inner = en_inner[:-len(en_suffix)]
                en_inner_br = en_inner.count('<br')
                
                new_text_field = en_prefix + vi_clean + ('<br>' * en_inner_br) + en_suffix
            else:
                new_text_field = text_field.replace(',', '‚')
                
            parts[2] = new_text_field
            out_lines.append(','.join(parts) + ending)
            
    out_text = ''.join(out_lines)
    out_bytes = out_text.encode('utf-8')
    if has_bom:
        out_bytes = b'\xef\xbb\xbf' + out_bytes
    
    vi_asset.parent.mkdir(parents=True, exist_ok=True)
    vi_asset.write_bytes(out_bytes)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: build_vi_assets.py <root_dir> <scene1> [scene2 ...]")
        sys.exit(1)
        
    root_dir = Path(sys.argv[1])
    scenes = sys.argv[2:]
    
    success = 0
    for s in scenes:
        if build_vi_asset(root_dir, s):
            success += 1
            
    if success == len(scenes):
        sys.exit(0)
    else:
        sys.exit(1)

#!/usr/bin/env python3
"""
build_asset_vi_hmn_10480100003.py — Deterministic VI asset builder.
EN-asset-is-English case (mixed JP-title / EN-message).
Iterates ALL lines, only modifies text-command lines.
"""
import sys, re
from pathlib import Path

ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10480100003"
EN = ROOT / "Translation/en/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"
VI_TARGET = ROOT / "Translation/vi/RedirectedResources/assets/unnamed_assetbundle" / f"{SCENE}.txt"

# --- Load VI_DICT parts ---
sys.path.insert(0, str(Path(__file__).parent))
VI_DICT = {}
for part in ["build_vi_part1.py", "build_vi_part2.py", "build_vi_part3.py"]:
    exec(open(Path(__file__).parent / part).read())
    # VI_PART1, VI_PART2, VI_PART3 are defined
VI_DICT.update(VI_PART1)
VI_DICT.update(VI_PART2)
VI_DICT.update(VI_PART3)

# --- Read EN asset ---
raw = EN.read_bytes()
has_bom = raw[:3] == b'\xef\xbb\xbf'
has_crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig')
lines = text.splitlines(True)

# --- Enumerate text records with seq ---
TEXT_CMDS = ("title,", "message,", "messageTextCenter,", "messageTextUnder,")
seq_of_line = {}  # line_idx -> seq
seq = 0
for idx, ln in enumerate(lines):
    if ln.startswith(TEXT_CMDS):
        seq += 1
        seq_of_line[idx] = seq

total_records = seq
assert len(VI_DICT) == total_records, f"VI_DICT has {len(VI_DICT)} entries but EN has {total_records} records"
print(f"Total text records: {total_records}")

# --- Preflight: check all seq present ---
for s in range(1, total_records + 1):
    assert s in VI_DICT, f"Missing VI_DICT entry for seq={s}"
# Preflight: no ASCII comma in VI
for s, vt in VI_DICT.items():
    assert ',' not in vt, f"ASCII comma in seq={s}: {vt[:50]} — use U+201A"
print("Preflight ASCII-comma check: PASS")

# --- Build output ---
OUT = []
translated = 0
br_errors = []

for idx, ln in enumerate(lines):
    if idx in seq_of_line:
        s = seq_of_line[idx]
        vi_text = VI_DICT[s]
        raw_line = ln.rstrip('\r\n')
        cmd = raw_line.split(',', 1)[0]
        
        if cmd == 'title':
            parts = raw_line.split(',', 1)
            new_line = f"title,{vi_text}"
        
        elif cmd == 'message':
            parts = raw_line.split(',', 5)
            old_tf = parts[2]
            # Detect suffix
            slist = re.findall(r'(<[^>]+>\s*)+$', old_tf)
            suffix_match = re.search(r'(<[^>]+>\s*)+$', old_tf)
            suffix = suffix_match.group(0) if suffix_match else ''
            
            # Build new text field
            if vi_text.rstrip().endswith('<br>') or not suffix:
                new_tf = vi_text
            else:
                new_tf = vi_text + suffix
            
            parts[2] = new_tf
            new_line = ','.join(parts)
            
            en_br = old_tf.count('<br>')
            vi_br = new_tf.count('<br>')
            if en_br != vi_br:
                br_errors.append(f"seq={s}: EN has {en_br} <br>, VI has {vi_br}")
        
        else:  # messageTextCenter, messageTextUnder
            # Format: cmd,SPEAKER,TEXT,,,flags
            parts = raw_line.split(',', 3)
            old_tf = parts[2]
            if '--' in vi_text:
                # Ensure center card text is standalone
                suffix_match = re.search(r'(<[^>]+>\s*)+$', old_tf)
                suffix = suffix_match.group(0) if suffix_match else ''
                if suffix and not vi_text.rstrip().endswith('</size>'):
                    new_tf = vi_text + suffix
                else:
                    new_tf = vi_text
                parts[2] = new_tf
                new_line = ','.join(parts)
            else:
                parts[2] = vi_text
                new_line = ','.join(parts)
            
            en_br = old_tf.count('<br>')
            vi_br = parts[2].count('<br>')
            if en_br != vi_br:
                br_errors.append(f"seq={s}: EN has {en_br} <br>, VI has {vi_br}")
        
        # Preserve original trailing CRLF
        trailing = ln[len(ln.rstrip('\r\n')):]
        OUT.append(new_line + trailing)
        translated += 1
    else:
        OUT.append(ln)

if br_errors:
    print(f"\nBR count errors ({len(br_errors)}):")
    for e in br_errors:
        print(f"  {e}")
    sys.exit(1)

print(f"BR count check: PASS")

# --- Write VI output ---
out_text = ''.join(OUT)
if has_bom:
    out_bytes = b'\xef\xbb\xbf' + out_text.encode('utf-8')
else:
    out_bytes = out_text.encode('utf-8')

# Normalize CRLF
if has_crlf:
    out_bytes = out_bytes.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    out_bytes = out_bytes.replace(b'\r\r\n', b'\r\n')

VI_TARGET.parent.mkdir(parents=True, exist_ok=True)
VI_TARGET.write_bytes(out_bytes)
print(f"Written: {VI_TARGET} ({len(OUT)} lines, file is {len(out_bytes)} bytes)")
print(f"Translated: {translated}/{total_records} text records")

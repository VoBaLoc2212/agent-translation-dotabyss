import json, re, sys
from pathlib import Path

WORK = Path(r"E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10430100002_full")
EN = Path(r"E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100002.txt")
OUT = Path(r"E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10430100002.txt")

VI = {}
for p in ["vi_part1.json","vi_part2.json","vi_part3.json"]:
    VI.update(json.load(open(WORK/p, encoding="utf-8")))
assert len(VI) == 96, f"expected 96 got {len(VI)}"

def norm(s):
    s = s.replace("\uff0c", ",")
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("\u3000", "")
    return "".join(s.split())

raw = EN.read_bytes()
text = raw.decode("utf-8-sig")
lines = text.splitlines(keepends=True)
cmds = ["title,","message,","messageTextUnder,","messageTextCenter,"]

# per-seq: EN content (without trailing suffix) and suffix
seq_data = {}
seq = 0
for ln in lines:
    if not any(ln.startswith(c) for c in cmds):
        continue
    seq += 1
    parts = ln.split(",")
    tf = parts[1] if ln.startswith("title,") else parts[2]
    tf = tf.rstrip("\r\n")
    m = re.search(r"(?:<[^>]+>\s*)+$", tf)
    suffix = m.group(0) if m else ""
    content = tf[:len(tf)-len(suffix)] if suffix else tf
    seq_data[seq] = (content, suffix)

# map normalized content -> VI
content_to_vi = {}
for s, v in VI.items():
    content, suffix = seq_data[int(s)]
    k = norm(content)
    assert k not in content_to_vi, f"dup key {k}"
    content_to_vi[k] = v

out = []
used = set()
for ln in lines:
    cmd = None
    for c in cmds:
        if ln.startswith(c):
            cmd = c[:-1]; break
    if not cmd:
        out.append(ln); continue
    parts = ln.split(",")
    idx = 1 if cmd == "title" else 2
    tf = parts[idx].rstrip("\r\n")
    m = re.search(r"(?:<[^>]+>\s*)+$", tf)
    suffix = m.group(0) if m else ""
    content = tf[:len(tf)-len(suffix)] if suffix else tf
    k = norm(content)
    if k not in content_to_vi:
        print("NO MATCH:", repr(content)); sys.exit(1)
    vi = content_to_vi[k]
    used.add(k)
    assert "," not in vi, f"ASCII comma in VI: {vi}"
    if vi.count("<br>") != content.count("<br>"):
        print(f"INTERNAL BR MISMATCH EN={content.count('<br>')} VI={vi.count('<br>')} :: {content!r} -> {vi!r}")
        sys.exit(1)
    ending = parts[idx][len(parts[idx].rstrip("\r\n")):]
    parts[idx] = vi + suffix + ending
    out.append(",".join(parts))

assert len(used) == len(content_to_vi), f"unused {len(content_to_vi)-len(used)}"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(raw[:3] + "".join(out).encode("utf-8"))
print("WROTE", OUT, "lines", len(out))

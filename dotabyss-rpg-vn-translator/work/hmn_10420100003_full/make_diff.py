# -*- coding: utf-8 -*-
import json
W = "dotabyss-rpg-vn-translator/work/hmn_10420100003_full/"
recs = json.load(open(W+"recs.json", encoding="utf-8"))
def load(f):
    return open(f, 'rb').read().decode('utf-8-sig').split('\r\n')
en = load("Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100003.txt")
vi = load("Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100003.txt")
def tf(ln, c):
    if c == 'title':
        p = ln.split(',', 1); return p[1] if len(p) > 1 else ''
    p = ln.split(',', 3); return p[2] if len(p) > 2 else ''
seq = 0
diff = []
for i, (a, b) in enumerate(zip(en, vi), 1):
    c = a.split(',', 1)[0]
    if c in ('title','message','messageTextUnder','messageTextCenter'):
        r = recs[seq]; seq += 1
        et = tf(a, c); vt = tf(b, c)
        if et != vt:
            jp = r['jp'] if r['jp'] != '(n/a)' else '(n/a — translated from EN)'
            diff.append("L%d [%s/%s]\n  JP : %s\n  EN : %s\n  VI : %s\n" % (i, c, (r['name'] or 'NARR'), jp, et, vt))
open(W+"focused_diff.md", "w", encoding="utf-8").write(
    "# focused_diff — hmn_10420100003\n\n%d changed text records (113 total).\n\n" % len(diff) + "\n".join(diff))
print("wrote", len(diff), "diffs")

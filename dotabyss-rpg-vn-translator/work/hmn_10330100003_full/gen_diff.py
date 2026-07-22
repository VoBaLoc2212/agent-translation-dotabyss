#!/usr/bin/env python
import re, json
ROOT="E:/AgentTranslation"
EN=f"{ROOT}/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100003.txt"
VI=f"{ROOT}/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100003.txt"
ENJSON=f"{ROOT}/dotabyss-translation-main/translations/novels/hmn_10330100003/en.json"

def load_lines(p):
    raw=open(p,'rb').read()
    t=raw.decode('utf-8-sig')
    return [ln[:-1] if ln.endswith('\r') else ln for ln in t.split('\n')]

en=load_lines(EN); vi=load_lines(VI)
en_map=json.load(open(ENJSON,encoding='utf-8-sig'))

def norm(s):
    s=re.sub(r'<[^>]+>','',s)
    s=s.replace('，',',').replace('、',',').replace(' ','')
    return s

# en.json: EN value -> JP key
en_to_ja={norm(v):k for k,v in en_map.items() if v}

def jp_of(en_textfield):
    jk=en_to_ja.get(norm(en_textfield))
    return jk if jk else "(n/a — SFX/namecry/interjection)"

lines=[]
lines.append("# Focused Diff — hmn_10330100003")
lines.append("")
lines.append("Case: EN-asset-is-English. JP meaning recovered from ja.json/en.json; EN asset adopted as Viet base then translated; EN asset is structural authority (delimiters, `<br>` count, `<user>`, BOM, CRLF preserved). JP column recovered from en.json (EN value -> JP key).")
lines.append("")
lines.append("| # | EN asset (structural authority) | VI output | JP source (en.json) |")
lines.append("|---|---|---|---|")

for i in range(len(en)):
    if en[i].startswith("title,"):
        et=en[i].split(",",1)[1]
        vt=vi[i].split(",",1)[1]
        jk=en_to_ja.get(norm(et),"(identity)")
        lines.append(f"| T (L{i+1}) | {et.strip()} | {vt.strip()} | {jk} |")
        break

for i in range(len(en)):
    if en[i].startswith("message,"):
        ep=en[i].split(",",5)
        vp=vi[i].split(",",5)
        et=ep[2]; vt=vp[2]
        jk=jp_of(et)
        lines.append(f"| L{i+1} | {et.rstrip()} | {vt.rstrip()} | {jk} |")

out="\n".join(lines)+"\n"
open(f"{ROOT}/dotabyss-rpg-vn-translator/work/hmn_10330100003_full/focused_diff.md",'w',encoding='utf-8').write(out)
na=sum(1 for l in lines if "(n/a" in l)
print(f"wrote focused_diff.md: {len(lines)} lines, {na} (n/a) rows")

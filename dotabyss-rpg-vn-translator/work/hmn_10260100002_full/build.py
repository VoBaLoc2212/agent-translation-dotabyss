# -*- coding: utf-8 -*-
import sys, importlib.util
EN_ASSET='E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100002.txt'
OUT='E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100002.txt'
spec=importlib.util.spec_from_file_location('t','E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10260100002_full/translations_vi.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
T=m.T

raw=open(EN_ASSET,'rb').read()
has_bom=raw[:3]==b'\xef\xbb\xbf'
has_crlf=b'\r\n' in raw
text=raw.decode('utf-8-sig')
lines=text.split('\r\n')

problems=[]
newlines=[]
for i,l in enumerate(lines,1):
    cmd=l.split(',',1)[0]
    if i in T:
        vi=T[i]
        assert ',' not in vi, f"ASCII comma in VI line {i}"
        if cmd=='title':
            p=l.split(',',1); src=p[1]; p[1]=vi; nl=','.join(p)
        else:
            p=l.split(',',5); src=p[2]; p[2]=vi; nl=','.join(p)
        if src.count('<br>')!=vi.count('<br>'):
            problems.append((i,src.count('<br>'),vi.count('<br>')))
        newlines.append(nl)
    else:
        newlines.append(l)

if problems:
    for i,a,b in problems: print(f"BR MISMATCH L{i}: src={a} vi={b}")
    sys.exit("Fix <br> counts before writing.")

body=('\r\n' if has_crlf else '\n').join(newlines)
out=(b'\xef\xbb\xbf' if has_bom else b'')+body.encode('utf-8')
import os; os.makedirs(os.path.dirname(OUT),exist_ok=True)
open(OUT,'wb').write(out)
print("WROTE",OUT,"lines",len(newlines),"translated",len(T))

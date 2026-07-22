import json
raw=open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100002.txt','rb').read()
t=raw.decode('utf-8-sig'); lines=t.split('\r\n')
ja=json.load(open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10260100002/ja.json',encoding='utf-8'))
en=json.load(open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10260100002/en.json',encoding='utf-8'))
ja_keys=list(ja.keys())
recs=[]
for i,l in enumerate(lines,1):
    cmd=l.split(',',1)[0]
    if cmd=='title':
        recs.append((i,cmd,'',l.split(',',1)[1]))
    elif cmd in ('message','messageTextCenter','messageTextUnder'):
        p=l.split(',',5); recs.append((i,cmd,p[1],p[2]))
assert len(recs)==len(ja_keys), (len(recs),len(ja_keys))
out=[]
for idx,(ln,cmd,spk,tf) in enumerate(recs):
    jak=ja_keys[idx]
    out.append(f"L{ln}\t[{cmd}|{spk}]\nJA={jak!r}\nEN={tf!r}\n")
open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10260100002_aligned.txt','w',encoding='utf-8').write("\n".join(out))
print("done",len(recs))

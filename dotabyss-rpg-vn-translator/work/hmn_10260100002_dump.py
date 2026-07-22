import json
raw=open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10260100002.txt','rb').read()
t=raw.decode('utf-8-sig'); lines=t.split('\r\n')
ja=json.load(open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10260100002/ja.json',encoding='utf-8'))
en=json.load(open('E:/AgentTranslation/dotabyss-translation-main/translations/novels/hmn_10260100002/en.json',encoding='utf-8'))
# normalize fullwidth comma to ascii for matching
def norm(s): return s.replace('\uff0c',',')
en2ja={norm(v):k for k,v in en.items()}
out=[]
for i,l in enumerate(lines,1):
    cmd=l.split(',',1)[0]
    if cmd=='title':
        tf=l.split(',',1)[1]; spk=''
    elif cmd in ('message','messageTextCenter','messageTextUnder'):
        p=l.split(',',5); tf=p[2]; spk=p[1]
    else:
        continue
    jak=en2ja.get(norm(tf),'??')
    out.append(f"L{i}\t[{cmd}|{spk}]\nEN={tf!r}\nJA={jak!r}\n")
open('E:/AgentTranslation/dotabyss-rpg-vn-translator/work/hmn_10260100002_dump.txt','w',encoding='utf-8').write("\n".join(out))
print("done",len(out))

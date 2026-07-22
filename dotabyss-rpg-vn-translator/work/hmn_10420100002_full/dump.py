import json,re
BASE='E:/AgentTranslation/'
en=json.load(open(BASE+'dotabyss-translation-main/translations/novels/hmn_10420100002/en.json',encoding='utf-8'))
def norm(s):
    s=s.replace('，',',')
    s=re.sub(r'<[^>]+>','',s)
    s=s.replace('\u3000','').replace(' ','')
    return s.strip()
en_to_ja={norm(v):k for k,v in en.items() if v}
raw=open(BASE+'Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100002.txt','rb').read().decode('utf-8-sig')
lines=raw.split('\r\n')
seq=0
out=[]
for i,ln in enumerate(lines,1):
    if ln.startswith('title,'):
        seq+=1
        out.append(f'#{seq} L{i} TITLE\n  T: {ln[6:]}')
    elif ln.startswith('message,'):
        seq+=1
        parts=ln.split(',')
        name=parts[1]; text=parts[2]
        ja=en_to_ja.get(norm(text),'(n/a)')
        out.append(f'#{seq} L{i} [{name}] br={text.count("<br>")}\n  EN: {text}\n  JA: {ja}')
out.append(f'TOTAL {seq}')
open(BASE+'dotabyss-rpg-vn-translator/work/hmn_10420100002_full/dump.txt','w',encoding='utf-8').write('\n'.join(out))
print('done',seq)

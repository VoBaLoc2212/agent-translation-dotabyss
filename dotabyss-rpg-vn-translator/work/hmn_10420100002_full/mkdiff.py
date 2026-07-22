import re
BASE='E:/AgentTranslation/'
en=__import__('json').load(open(BASE+'dotabyss-translation-main/translations/novels/hmn_10420100002/en.json',encoding='utf-8'))
def norm(s):
    s=s.replace('，',','); s=re.sub(r'<[^>]+>','',s); s=s.replace('\u3000','').replace(' ',''); return s.strip()
en_to_ja={norm(v):k for k,v in en.items() if v}
def rd(p): return open(p,'rb').read().decode('utf-8-sig').split('\r\n')
enl=rd(BASE+'Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100002.txt')
vil=rd(BASE+'Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10420100002.txt')
out=['# Focused Diff — hmn_10420100002 (JP primary / EN alignment / VI output)\n']
seq=0
for e,v in zip(enl,vil):
    if e.startswith('title,'):
        seq+=1
        out.append(f'## #{seq} title\nJP: {e[6:]}\nVI: {v[6:]}\n')
    elif e.startswith('message,'):
        seq+=1
        ep=e.split(','); vp=v.split(',')
        ja=en_to_ja.get(norm(ep[2]),'(n/a)')
        out.append(f'## #{seq} [{ep[1]}]\nJP: {ja}\nEN: {ep[2]}\nVI: {vp[2]}\n')
open(BASE+'dotabyss-rpg-vn-translator/work/hmn_10420100002_full/focused_diff.md','w',encoding='utf-8').write('\n'.join(out))
print('done',seq)

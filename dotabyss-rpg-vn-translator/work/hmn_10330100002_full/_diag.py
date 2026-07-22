import re
raw = open('Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10330100002.txt', 'rb').read()
text = raw.decode('utf-8-sig')
lines = text.split('\r\n')
cmds = ('title,', 'message,', 'messageTextUnder,', 'messageTextCenter,')
n = 0
for i, ln in enumerate(lines, 1):
    if ln.startswith(cmds):
        n += 1
        body = ln.split(',', 5)[2] if not ln.startswith('title,') else ln.split(',', 1)[1]
        body = re.sub(r'(?:<br>\s*)+$', '', body)
        print(n, i, 'br=%d' % body.count('<br>'), '|', body[:68])
print('TOTAL', n)

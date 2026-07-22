#!/usr/bin/env python3
"""Check EN asset file structure."""
import os

en_path = "E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10440100003.txt"

with open(en_path, 'rb') as f:
    raw = f.read()

print("File size: " + str(len(raw)))
print("BOM present: " + str(raw[:3] == b'\xef\xbb\xbf'))
print("CRLF present: " + str(b'\r\n' in raw))
lf_only = b'\n' in raw and b'\r\n' not in raw
print("LF only (no CR): " + str(lf_only))

# Find first newline
idx = raw.find(b'\n')
if idx >= 0:
    print("First newline at byte " + str(idx))
    print("Bytes around it: " + str(raw[max(0,idx-2):idx+2]))

# Decode and count
text = raw.decode('utf-8-sig')
lines = text.splitlines(True)
print("Total lines (splitlines): " + str(len(lines)))

title_c = 0
msg_c = 0
center_c = 0
under_c = 0
for i, ln in enumerate(lines, 1):
    s = ln.strip()
    if s.startswith('title,'):
        title_c += 1
        parts = s.split(',', 2)
        text_field = parts[1] if len(parts) > 1 else ''
        print("L{}: title -> [{}]".format(i, text_field))
    elif s.startswith('messageTextCenter,'):
        center_c += 1
        print("L{}: messageTextCenter".format(i))
    elif s.startswith('messageTextUnder,'):
        under_c += 1
        print("L{}: messageTextUnder".format(i))
    elif s.startswith('message,'):
        msg_c += 1

print("")
print("title=" + str(title_c) + ", message=" + str(msg_c) + ", center=" + str(center_c) + ", under=" + str(under_c))
print("Total records: " + str(title_c + msg_c + center_c + under_c))

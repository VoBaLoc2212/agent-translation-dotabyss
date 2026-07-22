"""Check for unchanged text records."""
en = open('E:/AgentTranslation/Translation/en/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt', 'r', encoding='utf-8-sig').readlines()
vi = open('E:/AgentTranslation/Translation/vi/RedirectedResources/assets/unnamed_assetbundle/hmn_10450100002.txt', 'r', encoding='utf-8-sig').readlines()

cmd_prefixes = ('title,', 'message,', 'messageTextCenter,', 'messageTextUnder,')
unchanged = []

for i, (en_ln, vi_ln) in enumerate(zip(en, vi), 1):
    en_s = en_ln.rstrip('\r\n')
    vi_s = vi_ln.rstrip('\r\n')
    
    # Check if this is a text command
    cmd = None
    for p in cmd_prefixes:
        if en_s.startswith(p) or vi_s.startswith(p):
            cmd = p
            break
    if not cmd:
        continue
    
    # Compare text fields only
    en_parts = en_s.split(',')
    vi_parts = vi_s.split(',')
    
    if cmd == 'title,':
        en_tf = en_parts[1] if len(en_parts) > 1 else ''
        vi_tf = vi_parts[1] if len(vi_parts) > 1 else ''
    else:
        en_tf = en_parts[2] if len(en_parts) > 2 else ''
        vi_tf = vi_parts[2] if len(vi_parts) > 2 else ''
    
    if en_tf == vi_tf:
        unchanged.append((i, en_tf[:60]))

if unchanged:
    print(f"UNCHANGED TEXT RECORDS ({len(unchanged)}):")
    for line_no, text in unchanged:
        print(f"  L{line_no}: {text}")
else:
    print("All text records changed. No UNCHANGED warnings.")

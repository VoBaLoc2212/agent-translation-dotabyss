import json, re
from pathlib import Path
ROOT = Path("E:/AgentTranslation")
SCENE = "hmn_10400100001"
asset = ROOT / "Translation" / "vi" / "RedirectedResources" / "assets" / "unnamed_assetbundle" / (SCENE + ".txt")
data = asset.read_bytes()
text = data.decode("utf-8-sig")
lines = text.split("\r\n")
CMDS = ("title,", "message,", "messageTextUnder,", "messageTextCenter,")
TAGSUF = re.compile(r"(?:<[^>]+>\s*)+$")
rows = []
for i, ln in enumerate(lines, 1):
    for c in CMDS:
        if ln.startswith(c):
            if c == "title,":
                parts = ln.split(",", 1)
                tf = parts[1] if len(parts) > 1 else ""
            elif c.startswith("messageText"):
                parts = ln.split(",", 5)
                tf = parts[2] if len(parts) > 2 else ""
            else:
                parts = ln.split(",", 5)
                tf = parts[2] if len(parts) > 2 else ""
                m = TAGSUF.search(tf)
                tf = tf[:m.start()] if m else tf
            cmd = c.rstrip(",")
            rows.append((i, cmd, tf))
            break
out = []
out.append("# Focused Diff — " + SCENE)
out.append("")
out.append(f"Text records: {len(rows)} (title=1, message=98, messageTextCenter=3)")
out.append("")
out.append("| Line | Cmd | VI Text |")
out.append("|---|---|---|")
for i, cmd, tf in rows:
    t = tf.replace("|", "/").replace("\n", " ")
    out.append(f"| {i} | {cmd} | {t} |")
out.append("")
Path(ROOT / "dotabyss-rpg-vn-translator" / "work" / (SCENE + "_full") / "focused_diff.md").write_text("\n".join(out), encoding="utf-8")
print("wrote focused_diff.md rows=", len(rows))

#!/usr/bin/env python3
"""Stage the 13 unposted pool videos: download, cover, frames for caption grounding."""
import json, os, subprocess
from PIL import Image, ImageDraw

WS = os.path.expanduser("~/workspace/luvetta_shop")
POST = os.path.join(WS, "posting")
os.makedirs(POST, exist_ok=True)
GWS = "/opt/hatch/bin/hatch_gws_cli"

ORDER = [  # posting order: oldest upload first among unposted
    ("Loan", "01.mp4"), ("Loan", "02.mp4"), ("Loan", "03.mp4"), ("Loan", "04.mp4"),
    ("DiemKieu", "16-11.mp4"),
    ("Hoan", "1"), ("Hoan", "2"), ("Hoan", "3"), ("Hoan", "4"),
    ("Loan", "05.mp4"), ("Loan", "06.mp4"),
    ("Hoan", "5"), ("Hoan", "6"),
]
dl = json.load(open(os.path.join(WS, "tmp_videos", "downloads.json")))["drive"]
by_key = {(d["person"], d["name"]): d for d in dl}

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", p], capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])

staged = []
for person, name in ORDER:
    info = by_key[(person, name)]
    fname = name if name.endswith(".mp4") else name + ".mp4"
    dest = os.path.join(POST, f"{person}__{fname}")
    if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
        r = subprocess.run([GWS, "drive", "files", "get", "--params",
                            json.dumps({"fileId": info["id"], "alt": "media"}),
                            "--output", dest], capture_output=True, text=True)
    ok = os.path.exists(dest) and os.path.getsize(dest) > 0
    print(person, name, "download:", "ok" if ok else "FAIL", flush=True)
    if not ok:
        continue
    d = dur(dest)
    cover = dest.replace(".mp4", ".cover.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{d*0.3:.2f}", "-i", dest,
                    "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "3", cover],
                   capture_output=True)
    frames = []
    for frac in (0.15, 0.5, 0.85):
        fp = f"/tmp/stage_{person}_{name}_{int(frac*100)}.png".replace("/", "_")
        fp = os.path.join("/tmp", f"stage_{person}_{abs(hash(name))%9999}_{int(frac*100)}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{d*frac:.2f}", "-i", dest,
                        "-frames:v", "1", "-vf", "scale=270:-2", fp], capture_output=True)
        frames.append(fp)
    staged.append({"person": person, "name": name, "id": info["id"], "path": dest,
                   "cover": cover, "dur": round(d, 2), "frames": frames})

# contact sheets: 5 videos per sheet, 3 frames each in a row
for si in range(0, len(staged), 5):
    group = staged[si:si+5]
    rows = []
    for s in group:
        tiles = []
        for fp in s["frames"]:
            img = Image.open(fp).convert("RGB")
            tiles.append(img)
        h = max(t.height for t in tiles)
        row = Image.new("RGB", (270*3 + 130, h), (15, 15, 15))
        ImageDraw.Draw(row).text((4, h//2), f"{s['person']}/{s['name']}", fill=(255, 255, 0))
        for i, t in enumerate(tiles):
            row.paste(t, (130 + i*270, 0))
        rows.append(row)
    sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height for r in rows)), (0, 0, 0))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    out = f"/tmp/pool_sheet_{si//5+1}.png"
    sheet.save(out)
    print("sheet:", out, sheet.size, flush=True)

json.dump(staged, open(os.path.join(POST, "staged.json"), "w"), indent=1)
print("STAGED", len(staged))

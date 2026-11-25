#!/usr/bin/env python3
"""Fingerprint videos (duration + frame aHashes) and cross-match Drive vs IG."""
import io, json, os, subprocess
from PIL import Image

BASE = os.path.expanduser("~/workspace/luvetta_shop/tmp_videos")
data = json.load(open(os.path.join(BASE, "downloads.json")))

def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", path], capture_output=True, text=True)
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return None

def frame_hash(path, at_sec):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{at_sec:.2f}", "-i", path,
                        "-frames:v", "1", "-vf", "scale=320:-2", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True)
    if not r.stdout:
        return None
    img = Image.open(io.BytesIO(r.stdout)).convert("L").resize((16, 16))
    px = list(img.getdata())
    mean = sum(px) / len(px)
    bits = 0
    for i, p in enumerate(px):
        if p > mean:
            bits |= (1 << i)
    return bits

def fingerprint(item):
    dur = duration(item["path"])
    if dur is None:
        return {**item, "dur": None, "h1": None, "h2": None}
    h1 = frame_hash(item["path"], dur * 0.3)
    h2 = frame_hash(item["path"], dur * 0.7)
    return {**item, "dur": round(dur, 2), "h1": h1, "h2": h2}

def ham(a, b):
    if a is None or b is None:
        return 999
    return bin(a ^ b).count("1")

drive = []
for it in data["drive"]:
    fp = fingerprint(it)
    drive.append(fp)
    print("DRIVE", fp["person"], fp["name"], "dur", fp["dur"], flush=True)

ig = []
for it in data["ig"]:
    fp = fingerprint(it)
    ig.append(fp)
    print("IG", fp["post_id"], "dur", fp["dur"], flush=True)

matches = []
for d in drive:
    best = None
    for g in ig:
        if d["dur"] is None or g["dur"] is None:
            continue
        dd = abs(d["dur"] - g["dur"])
        h = min(ham(d["h1"], g["h1"]), ham(d["h1"], g["h2"]),
                ham(d["h2"], g["h1"]), ham(d["h2"], g["h2"]))
        score = (dd, h)
        if best is None or (h, dd) < (best["ham"], best["dur_diff"]):
            best = {"ig_post_id": g["post_id"], "ig_created": g["created_at"],
                    "ig_dur": g["dur"], "dur_diff": round(dd, 2), "ham": h}
    if best:
        if best["dur_diff"] <= 2.0 and best["ham"] <= 20:
            verdict = "DUPLICATE_STRONG"
        elif best["dur_diff"] <= 2.0 and best["ham"] <= 45:
            verdict = "POSSIBLE"
        else:
            verdict = "NEW"
        matches.append({"person": d["person"], "name": d["name"], "drive_id": d["id"],
                        "drive_dur": d["dur"], "best": best, "verdict": verdict})

json.dump({"drive": drive, "ig": ig, "matches": matches},
          open(os.path.join(BASE, "fingerprints.json"), "w"), indent=1, default=str)
print("\n=== RESULTS ===")
for m in matches:
    print(f"{m['verdict']:16s} {m['person']}/{m['name']} (dur {m['drive_dur']}s) vs IG {m['best']['ig_post_id']} "
          f"{m['best']['ig_created']} (dur {m['best']['ig_dur']}s, ddiff {m['best']['dur_diff']}, ham {m['best']['ham']})")

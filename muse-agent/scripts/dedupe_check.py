#!/usr/bin/env python3
"""Luvetta: download Drive source videos + IG posted videos, fingerprint, cross-match."""
import json, os, subprocess, sys, urllib.request

BASE = os.path.expanduser("~/workspace/luvetta_shop/tmp_videos")
DRIVE_DIR = os.path.join(BASE, "drive")
IG_DIR = os.path.join(BASE, "ig")
os.makedirs(DRIVE_DIR, exist_ok=True)
os.makedirs(IG_DIR, exist_ok=True)
GWS = "/opt/hatch/bin/hatch_gws_cli"

FOLDERS = {
    "Hoan": "1kIdt90zVTbke2IWIBLyIACB4hap_4x5J",
    "Loan": "1TwQP83uMjxqCHaiLZ2lLNnigZg_RknWS",
    "DiemKieu": "1YpsRJqMn8BhAGL0weA1bzU_v9zOSyJaG",
    "Ha": "1S3W-yA4yZlF42lbCJtyWIN5GgMr-d2jB",
}

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def list_folder(fid):
    r = run([GWS, "drive", "files", "list", "--params",
             json.dumps({"q": f"'{fid}' in parents and trashed=false",
                         "fields": "files(id,name,mimeType,size,modifiedTime)",
                         "pageSize": 50})])
    return json.loads(r.stdout).get("files", [])

def download_drive(file_id, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "cached"
    r = run([GWS, "drive", "files", "get", "--params",
             json.dumps({"fileId": file_id, "alt": "media"}), "--output", dest])
    return "ok" if os.path.exists(dest) and os.path.getsize(dest) > 0 else f"FAIL {r.stdout[-200:]} {r.stderr[-200:]}"

def download_url(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "cached"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        return "ok"
    except Exception as e:
        return f"FAIL {e}"

drive_files = []
for person, fid in FOLDERS.items():
    for f in list_folder(fid):
        if not (f.get("mimeType") or "").startswith("video/"):
            continue
        name = f["name"] if f["name"].endswith(".mp4") else f["name"] + ".mp4"
        dest = os.path.join(DRIVE_DIR, f"{person}__{name}")
        st = download_drive(f["id"], dest)
        print(f"DRIVE {person}/{f['name']} -> {st}", flush=True)
        drive_files.append({"person": person, "name": f["name"], "id": f["id"],
                            "size": int(f.get("size", 0)), "modified": f.get("modifiedTime"),
                            "path": dest})

ig_posts = json.load(open("/tmp/ig_posts_all.json"))["posts"]
ig_files = []
for p in ig_posts:
    url = p.get("video_url")
    dest = os.path.join(IG_DIR, f"{p['post_id']}.mp4")
    st = download_url(url, dest) if url else "NO_URL"
    print(f"IG {p['post_id']} {p['created_at']} -> {st}", flush=True)
    ig_files.append({"post_id": p["post_id"], "created_at": p["created_at"],
                     "caption": (p.get("post_caption") or "")[:80], "path": dest,
                     "url": p.get("url")})

json.dump({"drive": drive_files, "ig": ig_files},
          open(os.path.join(BASE, "downloads.json"), "w"), indent=1)
print("DOWNLOADS DONE", len(drive_files), "drive,", len(ig_files), "ig")

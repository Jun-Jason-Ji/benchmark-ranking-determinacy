"""Fetch the public RT-1 TF SavedModel checkpoints SIMPLER evaluates, from the Open X-Embodiment bucket.

The bucket is public over plain HTTPS, so this needs no gsutil and no credentials. Objects are listed
through the JSON API and fetched one by one, with resume: a partially downloaded file is continued rather
than restarted, so an interrupted run (or a reboot, which this project has seen twice) costs nothing.

Which checkpoints and why:
  rt-1-x          published SIMPLER value 0.567 on pick-coke-can -- the validation gate, high enough
                  above the floor that a broken pipeline cannot accidentally reproduce it
  rt-1-converged  published 0.857 sim / 0.853 real
  rt-1-15pct      published 0.710 sim / 0.920 real
The last two are the pair whose published real and simulated orderings disagree in sign (real -0.067,
sim +0.147) and whose checkpoints are both public -- the one reproducible real-vs-sim ranking reversal
on this task. rt-2-x is in the same disagreement set but has no public checkpoint.

Usage: python scripts/fetch_rt1_checkpoints.py [--dest third_party/SimplerEnv/checkpoints] [--only NAME]
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUCKET = "gdm-robotics-open-x-embodiment"
BASE = "open_x_embodiment_and_rt_x_oss"
# rt-1-x is published as a single zip object; the RT-1 variants are published as object directories.
ZIPPED = {"rt-1-x"}
CKPTS = {
    "rt-1-x": "rt_1_x_tf_trained_for_002272480_step",
    "rt-1-converged": "rt_1_tf_trained_for_000400120",
    "rt-1-15pct": "rt_1_tf_trained_for_000058240",
    "rt-1-begin": "rt_1_tf_trained_for_000001120",
}


def list_objects(prefix):
    out, token = [], None
    while True:
        q = {"prefix": prefix, "fields": "items(name,size),nextPageToken", "maxResults": "1000"}
        if token:
            q["pageToken"] = token
        url = f"https://storage.googleapis.com/storage/v1/b/{BUCKET}/o?" + urllib.parse.urlencode(q)
        with urllib.request.urlopen(url, timeout=60) as r:
            d = json.loads(r.read())
        out += [(i["name"], int(i["size"])) for i in d.get("items", [])]
        token = d.get("nextPageToken")
        if not token:
            return out


def fetch(name, size, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    have = dest.stat().st_size if dest.exists() else 0
    if have == size:
        return "ok"
    url = f"https://storage.googleapis.com/{BUCKET}/" + urllib.parse.quote(name)
    for attempt in range(5):
        try:
            req = urllib.request.Request(url)
            if have:
                req.add_header("Range", f"bytes={have}-")
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "ab" if have else "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
            got = dest.stat().st_size
            if got == size:
                return "ok"
            have = got  # short read: resume from where we stopped
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f"    retry {attempt + 1}/5 after {type(e).__name__}: {e}", flush=True)
            have = dest.stat().st_size if dest.exists() else 0
            time.sleep(3 * (attempt + 1))
    return f"FAILED ({dest.stat().st_size if dest.exists() else 0}/{size} bytes)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default="third_party/SimplerEnv/checkpoints")
    ap.add_argument("--only", action="append", choices=sorted(CKPTS),
                    help="fetch just these (repeatable); default is everything but rt-1-begin")
    args = ap.parse_args()
    dest_root = ROOT / args.dest
    names = args.only or ["rt-1-x", "rt-1-converged", "rt-1-15pct"]
    bad = 0
    for label in names:
        d = CKPTS[label]
        if label in ZIPPED:
            import zipfile
            obj = f"{BASE}/{d}.zip"
            objs = list_objects(obj)
            if not objs:
                print(f"{label}: object {obj} not found", flush=True)
                bad += 1
                continue
            size = objs[0][1]
            zp = dest_root / f"{d}.zip"
            print(f"{label} ({d}.zip): {size / 1e6:.0f} MB", flush=True)
            r = fetch(obj, size, zp)
            if r != "ok":
                print(f"  {d}.zip: {r}", flush=True)
                bad += 1
                continue
            if not (dest_root / d / "saved_model.pb").exists():
                with zipfile.ZipFile(zp) as z:
                    z.extractall(dest_root)
            print(f"{label}: done", flush=True)
            continue
        prefix = f"{BASE}/{d}/"
        objs = list_objects(prefix)
        if not objs:
            print(f"{label}: no objects under {prefix}", flush=True)
            bad += 1
            continue
        total = sum(s for _, s in objs)
        print(f"{label} ({d}): {len(objs)} objects, {total / 1e6:.0f} MB", flush=True)
        for name, size in objs:
            rel = name[len(prefix):]
            if not rel:
                continue
            r = fetch(name, size, dest_root / d / rel)
            if r != "ok":
                print(f"  {rel}: {r}", flush=True)
                bad += 1
        print(f"{label}: done", flush=True)
    print("RT1_FETCH_DONE" if not bad else f"RT1_FETCH_INCOMPLETE ({bad} problems)", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

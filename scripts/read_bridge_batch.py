"""Read the first N episodes of a public BridgeData V2 RLDS shard with bounded HTTP range
requests (no TensorFlow runtime), verify CRC32C, and save numeric fields per episode.

Usage: python scripts/read_bridge_batch.py --n 40 [--shard 0] [--out data/bridge_sysid]

Per episode: state (T,7) = [x,y,z,roll,pitch,yaw,gripper] of the end-effector in the robot
base frame (as used by SIMPLER tools/sysid), world_vector (T,3), rotation_delta (T,3) rpy,
open_gripper (T,), instruction, plus a manifest with byte offsets and SHA-256 per record.
Record k of shard 0 very likely equals SIMPLER's TFDS iteration id k (unshuffled read), but
that equality is not guaranteed by the format and is recorded as an assumption.
"""
import argparse
import hashlib
import json
import struct
import sys
import time
from pathlib import Path

import numpy as np
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from read_bridge_sample import example_class, masked_crc  # noqa: E402

BASE = "https://storage.googleapis.com/gresearch/robotics/bridge/0.1.0/bridge-train.tfrecord-{shard:05d}-of-01024"


def fetch(url, start, end, etag=None):
    headers = {"Range": f"bytes={start}-{end}"}
    if etag:
        headers["If-Match"] = etag
    for attempt in range(4):
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(15, 120)) as r:
                r.raise_for_status()
                if r.status_code != 206 or not r.headers.get("Content-Range", "").startswith(f"bytes {start}-{end}/"):
                    raise RuntimeError("Server did not honor the bounded range request")
                data = r.raw.read(end - start + 2)
                if len(data) != end - start + 1:
                    raise RuntimeError("Unexpected byte count")
                return data, r.headers.get("ETag")
        except (requests.RequestException, RuntimeError) as e:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--out", default="data/bridge_sysid")
    ap.add_argument("--max-record-mb", type=int, default=96)
    ap.add_argument("--name-offset", type=int, default=0, help="episode file index offset (e.g. 30 when continuing from another shard)")
    args = ap.parse_args()
    url = BASE.format(shard=args.shard)
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / f"manifest_shard{args.shard:05d}.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else \
        dict(url=url, records=[], assumption="record index == SIMPLER TFDS iteration id (unshuffled read); not guaranteed")
    done = {r["record"] for r in manifest["records"]}
    Example = example_class()
    offset = manifest["records"][-1]["end"] + 1 if manifest["records"] else 0
    etag = manifest.get("etag")
    for k in range(len(manifest["records"]), args.n):
        try:
            header, etag_now = fetch(url, offset, offset + 11, etag)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 416:
                print(f"end of shard reached after {k} records", flush=True)
                manifest["eof"] = True
                manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
                break
            raise
        etag = etag or etag_now
        length, length_crc = struct.unpack("<QI", header)
        if masked_crc(header[:8]) != length_crc:
            raise ValueError(f"record {k}: length CRC mismatch")
        if not 0 < length <= args.max_record_mb * 1024 * 1024:
            raise ValueError(f"record {k}: length {length} outside limit")
        body, _ = fetch(url, offset + 12, offset + 12 + length + 3, etag)
        payload, expected = body[:-4], struct.unpack("<I", body[-4:])[0]
        if masked_crc(payload) != expected:
            raise ValueError(f"record {k}: payload CRC mismatch")
        msg = Example()
        msg.ParseFromString(payload)
        feats = msg.features.feature

        def floats(key, width):
            a = np.asarray(feats[key].float_list.value, dtype=np.float32).reshape(-1, width)
            if not np.isfinite(a).all():
                raise ValueError(f"record {k}: non-finite {key}")
            return a

        state = floats("steps/observation/state", 7)
        world = floats("steps/action/world_vector", 3)
        rot = floats("steps/action/rotation_delta", 3)
        grip = np.asarray(feats["steps/action/open_gripper"].int64_list.value, dtype=np.int64)
        term = np.asarray(feats["steps/is_terminal"].int64_list.value, dtype=np.int64)
        instr_vals = feats["steps/observation/natural_language_instruction"].bytes_list.value
        instr = instr_vals[0].decode("utf-8", "replace") if len(instr_vals) else ""
        T = len(state)
        if not (len(world) == len(rot) == len(grip) == T):
            raise ValueError(f"record {k}: unaligned lengths")
        np.savez_compressed(out / f"ep_{args.name_offset + k:03d}.npz", state=state, world_vector=world, rotation_delta=rot,
                            open_gripper=grip, is_terminal=term, instruction=np.array(instr))
        rec = dict(record=k, file_index=args.name_offset + k, start=offset, end=offset + 12 + length + 3, bytes=12 + length + 4,
                   sha256=hashlib.sha256(header + body).hexdigest(), steps=int(T), instruction=instr,
                   state_first=state[0].round(4).tolist(), state_last=state[-1].round(4).tolist())
        manifest["records"].append(rec)
        manifest["etag"] = etag
        manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
        offset = rec["end"] + 1
        print(f"record {k}: {T} steps, {rec['bytes']/1e6:.1f} MB, '{instr}'", flush=True)
    print(f"done: {len(manifest['records'])} records in {out}")


if __name__ == "__main__":
    main()

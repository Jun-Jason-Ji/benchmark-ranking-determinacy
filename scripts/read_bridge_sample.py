"""Read exactly one public RLDS TFRecord using bounded HTTP ranges.

This is an ingestion smoke test. It is not a calibration fit, benchmark trial,
or a reproduction of SIMPLER's iteration-index-based episode selection.
"""
import hashlib
import json
import struct
from pathlib import Path

import google_crc32c
import numpy as np
import requests
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/calibration_smoke"
URL = "https://storage.googleapis.com/gresearch/robotics/bridge/0.1.0/bridge-train.tfrecord-00000-of-01024"


def example_class():
    """Build the standard tensorflow.Example wire schema (no TensorFlow runtime)."""
    fd = descriptor_pb2.FileDescriptorProto(name="local_tf_example.proto", package="tensorflow", syntax="proto3")

    def field(msg, name, number, dtype, repeated=False, type_name=None):
        f = msg.field.add(name=name, number=number, type=dtype, label=3 if repeated else 1)
        if type_name:
            f.type_name = type_name
        return f

    for name, dtype in [("BytesList", 12), ("FloatList", 2), ("Int64List", 3)]:
        m = fd.message_type.add(name=name)
        field(m, "value", 1, dtype, repeated=True)
    m = fd.message_type.add(name="Feature")
    m.oneof_decl.add(name="kind")
    for i, (name, kind) in enumerate([("bytes_list", "BytesList"), ("float_list", "FloatList"), ("int64_list", "Int64List")], 1):
        field(m, name, i, 11, type_name=".tensorflow." + kind).oneof_index = 0
    m = fd.message_type.add(name="Features")
    entry = m.nested_type.add(name="FeatureEntry")
    entry.options.map_entry = True
    field(entry, "key", 1, 9)
    field(entry, "value", 2, 11, type_name=".tensorflow.Feature")
    field(m, "feature", 1, 11, repeated=True, type_name=".tensorflow.Features.FeatureEntry")
    m = fd.message_type.add(name="Example")
    field(m, "features", 1, 11, type_name=".tensorflow.Features")
    pool = descriptor_pool.DescriptorPool()
    pool.Add(fd)
    return message_factory.GetMessageClass(pool.FindMessageTypeByName("tensorflow.Example"))


def fetch_range(start, end, etag=None):
    headers = {"Range": f"bytes={start}-{end}"}
    if etag:
        headers["If-Match"] = etag
    with requests.get(URL, headers=headers, stream=True, timeout=(15, 90)) as r:
        r.raise_for_status()
        prefix = f"bytes {start}-{end}/"
        if r.status_code != 206 or not r.headers.get("Content-Range", "").startswith(prefix):
            raise RuntimeError("Server did not honor the bounded range request")
        data = r.raw.read(end - start + 2)
        if len(data) != end - start + 1:
            raise RuntimeError("Unexpected byte count")
        return data, r.headers.get("ETag")


def masked_crc(data):
    crc = google_crc32c.value(data)
    return (((crc >> 15) | (crc << 17)) + 0xA282EAD8) & 0xFFFFFFFF


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    header, etag = fetch_range(0, 11)
    length, length_crc = struct.unpack("<QI", header)
    if masked_crc(header[:8]) != length_crc:
        raise ValueError("Length CRC32C mismatch")
    if not 0 < length <= 64 * 1024 * 1024:
        raise ValueError(f"First episode length {length} exceeds the 64 MiB ingestion limit")
    body, body_etag = fetch_range(12, 12 + length + 3, etag)
    payload, expected_crc = body[:-4], struct.unpack("<I", body[-4:])[0]
    if etag != body_etag or masked_crc(payload) != expected_crc:
        raise ValueError("Source changed or payload CRC32C mismatch")
    raw = header + body
    (OUT / "bridge_first_episode.tfrecord").write_bytes(raw)
    message = example_class()()
    message.ParseFromString(payload)
    features = message.features.feature
    schema = {}
    for key, feature in features.items():
        kind = feature.WhichOneof("kind")
        schema[key] = dict(kind=kind, length=len(getattr(feature, kind).value))

    def floats(key, width):
        f = features[key]
        if f.WhichOneof("kind") != "float_list":
            raise ValueError(f"Unexpected feature kind for {key}")
        array = np.asarray(f.float_list.value, dtype=np.float32).reshape(-1, width)
        if not np.isfinite(array).all():
            raise ValueError(f"Non-finite values in {key}")
        return array

    state = floats("steps/observation/state", 7)
    world = floats("steps/action/world_vector", 3)
    rotation = floats("steps/action/rotation_delta", 3)
    if not len(state) == len(world) == len(rotation):
        raise ValueError("Unaligned action and state lengths")
    np.savez_compressed(OUT / "bridge_first_episode_numeric.npz", state=state,
                        action_world_vector=world, action_rotation_delta=rotation)
    record = dict(status="passed", evidence="real_demonstration_ingestion_only", url=URL,
                  etag=etag, byte_range=[0, len(raw)-1], bytes_downloaded=len(raw),
                  sha256=hashlib.sha256(raw).hexdigest(), crc32c_verified=True,
                  steps=len(state), fields=schema,
                  limitations=["First record in first shard; not original SIMPLER iteration ID 0.",
                               "No calibration fit, success-rate label, or new robot evaluation.",
                               "Pose/action convention and timing still require protocol validation."])
    (ROOT / "research_audit/bridge_sample_ingestion.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in record.items() if k != "fields"}, indent=2))


if __name__ == "__main__":
    main()

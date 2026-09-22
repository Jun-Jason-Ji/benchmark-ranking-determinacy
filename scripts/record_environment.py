"""Record actual local hardware, package versions, source revisions and assets."""
import hashlib
import importlib.metadata
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def command(args):
    p = subprocess.run(args, capture_output=True, text=True, timeout=30)
    return dict(exit_code=p.returncode, stdout=p.stdout.strip(), stderr=p.stderr.strip())


def main():
    record = dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(),
                  platform=platform.platform(), python=platform.python_version(),
                  evidence="hardware_and_environment_audit")
    record["nvidia_smi"] = command(["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
                                     "--format=csv,noheader"])
    record["packages"] = {p: importlib.metadata.version(p) for p in
                          ["numpy", "scipy", "torch", "sapien", "mani_skill", "gymnasium"]}
    record["sources"] = {}
    for subdir in ["third_party/SimplerEnv", "third_party/SimplerEnv/ManiSkill2_real2sim",
                   "third_party/SimplerEnv-ms3"]:
        repo = str(ROOT / subdir)
        record["sources"][subdir] = command(["git", "-c", "safe.directory=" + repo,
                                            "-C", repo, "rev-parse", "HEAD"])
    import torch
    record["torch_cuda"] = dict(available=torch.cuda.is_available(), runtime=torch.version.cuda)
    if torch.cuda.is_available():
        record["torch_cuda"]["device"] = torch.cuda.get_device_name(0)
        # Real kernel launch verifies architecture compatibility, not just visibility.
        x = torch.arange(16, dtype=torch.float32, device="cuda")
        record["torch_cuda"]["kernel_check_sum"] = (x * x).sum().item()
    entries = []
    asset_root = ROOT / "data/maniskill-assets/data"
    for f in sorted(asset_root.rglob("*")):
        if f.is_file():
            entries.append(dict(path=f.relative_to(asset_root).as_posix(), bytes=f.stat().st_size,
                                sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    record["asset_files"] = len(entries)
    record["asset_total_bytes"] = sum(x["bytes"] for x in entries)
    out = ROOT / "results/environment"
    out.mkdir(parents=True, exist_ok=True)
    (out / "asset_manifest.json").write_text(json.dumps(entries, indent=2), encoding="utf-8")
    (out / "hardware_and_versions.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()

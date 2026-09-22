"""Compare our reproduction of the official SIMPLER protocol against the published table.

scripts/queue_ms2_official_protocol.py runs each bridge task on the original stack exactly as
scripts/octo_bridge.sh does: the full 24-configuration census under three fixed policy seeds (init_rng 0, 2, 4),
72 episodes per policy and task. The published sim numbers live in
third_party/SimplerEnv/simpler_env/utils/metrics.py (SIMPLER_PERF) and have the same denominator.

A close match validates our whole original-stack pipeline (WSL, CPU physics, lavapipe rendering through the
fake-semaphore Vulkan layer, our own HTTP Octo servers) against the reference implementation. A mismatch that
is within the per-seed spread we measure is itself informative: it bounds how reproducible the published
numbers are.

Usage: python scripts/analyze_official_protocol.py
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "third_party/SimplerEnv/simpler_env/utils/metrics.py"
OUT_ROOT = ROOT / "results/controller_sweep_ms2_official"
SEEDS = [0, 2, 4]
TASK_ENV = {"widowx_put_eggplant_in_basket": "PutEggplantInBasketScene-v0",
            "widowx_spoon_on_towel": "PutSpoonOnTableClothInScene-v0",
            "widowx_carrot_on_plate": "PutCarrotOnPlateInScene-v0",
            "widowx_stack_cube": "StackGreenCubeOnYellowCubeBakedTexInScene-v0"}
POLICIES = ["octo-small", "octo-base"]


def published():
    """SIMPLER_PERF from the pinned metrics.py, parsed as a literal (the module is never imported)."""
    src = METRICS.read_text(encoding="utf-8")
    m = re.search(r"SIMPLER_PERF\s*=\s*(\{.*?\n\})", src, re.S)
    if not m:
        return {}
    try:
        return ast.literal_eval(m.group(1))
    except Exception:
        return {}


def load(policy, env, seed):
    f = OUT_ROOT / f"seed{seed}" / policy / env / "nominal.jsonl"
    d = {}
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                d.setdefault(r["episode_id"], int(bool(r["success"])))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/controller_sweep_ms2_official/FINDING_official_protocol.md")
    args = ap.parse_args()
    pub = published()
    L = ["# 官方协议复现：24 构型全普查 × 3 个固定种子（72 集）对表 SIMPLER 公布值", "",
         "运行方式与 `scripts/octo_bridge.sh` 一致：`--obj-episode-range 0 24`，`init_rng ∈ {0, 2, 4}`，"
         "每个种子在整轮内固定（`--policy-seed-fixed`）。平台为原版栈（ManiSkill2_real2sim + SAPIEN 2.2.2，"
         "WSL、CPU 物理、lavapipe 渲染经 vk_fakesemfd 层），策略由本项目的 HTTP Octo 服务器提供。"
         "公布值取自固定版本的 `simpler_env/utils/metrics.py`。", "",
         "| 任务 | 策略 | 种子 0 | 种子 2 | 种子 4 | 合并 (n/72) | 公布值 | 差 |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    rows = []
    for task, env in TASK_ENV.items():
        for p in POLICIES:
            per, allv = [], []
            for s in SEEDS:
                d = load(p, env, s)
                per.append(f"{np.mean(list(d.values())):.3f} ({len(d)})" if d else "–")
                allv += list(d.values())
            if not allv:
                continue
            ours = float(np.mean(allv))
            ref = pub.get(task, {}).get(p)
            diff = f"{ours - ref:+.3f}" if ref is not None else "–"
            rows.append((task, p, ours, ref))
            L.append(f"| {task} | {p} | {per[0]} | {per[1]} | {per[2]} | {ours:.3f} ({len(allv)}) | "
                     f"{ref if ref is not None else '–'} | {diff} |")
    L.append("")
    paired = [(o, r) for _, _, o, r in rows if r is not None]
    if paired:
        diffs = np.array([o - r for o, r in paired])
        L += ["## 读法", "",
              f"- {len(paired)} 个（任务 × 策略）单元中，我们与公布值的平均差 {diffs.mean():+.3f}，"
              f"平均绝对差 {np.abs(diffs).mean():.3f}，最大 {np.abs(diffs).max():.3f}。",
              "- 对照本项目测得的种子噪声（茄子 64 构型：单种子 95% 半宽 ±0.108，3 个种子 ±0.062）："
              "落在该范围内的差异说明公布值本身带着同量级、未被报告的不确定性，而非流水线错误。",
              "- 这也是原版栈流水线（WSL + CPU 渲染 + 自建策略服务器）对参考实现的一次端到端验证。", ""]
    text = "\n".join(L)
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

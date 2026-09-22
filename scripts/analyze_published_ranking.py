"""Descriptive audit of published SIMPLER aggregates, not a significance test."""
import csv
import itertools
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research_audit"


def main():
    tasks = defaultdict(list)
    with (OUT / "simpler_published_scores.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["public_checkpoint_candidate"] == "True":
                tasks[row["task"]].append(row)
    pairs = []
    for task, policies in tasks.items():
        for a, b in itertools.combinations(policies, 2):
            real = Decimal(a["real_success_reported"]) - Decimal(b["real_success_reported"])
            sim = Decimal(a["sim_success_reported"]) - Decimal(b["sim_success_reported"])
            status = "opposite_sign" if real * sim < 0 else (
                "tie_in_at_least_one_domain" if real * sim == 0 else "same_sign")
            pairs.append(dict(task=task, policy_i=a["policy"], policy_j=b["policy"],
                              published_real_difference=str(real), published_sim_difference=str(sim),
                              descriptive_status=status))
    with (OUT / "published_pairwise_audit.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)
    reversals = [r for r in pairs if r["descriptive_status"] == "opposite_sign"]
    ties = sum(r["descriptive_status"] == "tie_in_at_least_one_domain" for r in pairs)
    summary = dict(public_checkpoint_pairs=len(pairs), opposite_sign_pairs=len(reversals),
                   ties_in_at_least_one_domain=ties,
                   interpretation="Descriptive rounded aggregate signs only; no trial-level inference.")
    (OUT / "published_pairwise_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = ["# SIMPLER 已发表均值的排序核查", "", "这是已发表表格的描述性分析，不是新实验或显著性检验。",
             "", f"排除无公开权重的 RT-2-X 后，共 {len(pairs)} 个任务内策略对；"
             f"{len(reversals)} 对的模拟与真实均值差值符号相反，{ties} 对在至少一域出现均值平局。",
             "", "| 任务 | 策略 i | 策略 j | 真实均值差 | 仿真均值差 |",
             "|---|---|---|---:|---:|"]
    for r in reversals:
        lines.append(f"| {r['task']} | {r['policy_i']} | {r['policy_j']} | "
                     f"{r['published_real_difference']} | {r['published_sim_difference']} |")
    lines += ["", "不能将这些对称为已统计确认的真实排序反转：原表为取整后的成功率，"
              "本次尚未建立每格试验次数、场景分层和逐试验结果。策略对共享策略与任务，彼此不独立。",
              "", "此表仅用于协议审计与问题定位；若据此选择任务，需如实标记为已查看开发信息，"
              "不能将这些同源标签重新称为未触碰测试集。正式验证必须冻结新的划分及分析规则。",
              "", "数据来源及 SHA-256 见 simpler_manifest.json；全部策略对见 published_pairwise_audit.csv。"]
    (OUT / "published_pairwise_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

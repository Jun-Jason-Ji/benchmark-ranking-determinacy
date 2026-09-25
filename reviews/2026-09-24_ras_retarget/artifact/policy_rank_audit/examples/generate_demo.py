"""Generate explicitly synthetic CSV examples; no simulator is invoked."""
import csv
from pathlib import Path

root=Path(__file__).resolve().parent
counts={"A":{"nominal":[5,4,6,5],"stress":[4,5,4,6]},
        "B":{"nominal":[1,2,0,1],"stress":[1,0,2,1]},
        "C":{"nominal":[1,2,0,1],"stress":[6,5,4,5]}}
rows=[]
for policy,conditions in counts.items():
    for condition,successes in conditions.items():
        for replicate,k in enumerate(successes):
            for configuration in range(6):
                rows.append(dict(task="synthetic_pick",policy=policy,condition=condition,
                                 configuration=f"c{configuration}",replicate=f"run{replicate}",
                                 success=int(configuration<k)))
for name,selected in (("complete.csv",rows),("incomplete.csv",rows[:-1])):
    with (root/name).open("w",newline="",encoding="utf-8") as stream:
        writer=csv.DictWriter(stream,fieldnames=["task","policy","condition","configuration","replicate","success"])
        writer.writeheader();writer.writerows(selected)
print("Wrote 144-row complete and 143-row incomplete synthetic examples.")

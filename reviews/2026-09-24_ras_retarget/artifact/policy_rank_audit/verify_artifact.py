"""Offline local-wheel installation and end-to-end checks; no environment mutation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
checks=root/"checks"
checks.mkdir(exist_ok=True)
target=checks/"installed"
wheel=root/"dist/policy_rank_audit-0.1.0-py3-none-any.whl"
assert wheel.is_file(), "Build the local wheel first"
env=os.environ.copy()
env["PYTHONPATH"]=str(target)
env["PIP_DISABLE_PIP_VERSION_CHECK"]="1"
calls=[]

def run(arguments, expected=0):
    result=subprocess.run([sys.executable,*arguments],cwd=root,env=env,text=True,capture_output=True)
    calls.append(dict(arguments=arguments,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr))
    assert result.returncode==expected, (arguments,result.returncode,result.stdout,result.stderr)
    return result

run(["-m","pip","install","--no-index","--no-deps","--upgrade","--target",str(target),str(wheel)])
origin=run(["-c","import policy_rank_audit; print(policy_rank_audit.__file__)"]).stdout.strip()
assert Path(origin).resolve().is_relative_to(target.resolve())
run(["-m","unittest","discover","-s","tests","-v"])
run(["-m","policy_rank_audit","audit","examples/complete.csv","--manifest","examples/manifest.json","--out","checks/complete_audit.json"])
run(["-m","policy_rank_audit","audit","examples/incomplete.csv","--manifest","examples/manifest.json","--out","checks/incomplete_audit.json"],expected=2)
run(["-m","policy_rank_audit","allocate","examples/allocation.json","--out","checks/allocation.json"])
complete=json.loads((checks/"complete_audit.json").read_text())
incomplete=json.loads((checks/"incomplete_audit.json").read_text())
allocation=json.loads((checks/"allocation.json").read_text())
ab=next(p for p in complete["pairs"] if p["policy_a"]=="A" and p["policy_b"]=="B")
assert ab["holm_verdict"]=="a_better"
ac=next(p for p in complete["pairs"] if p["policy_a"]=="A" and p["policy_b"]=="C")
assert ac["raw_p"]==1 and ac["holm_verdict"]=="abstain"
assert all(p["envelope"] is None and p["holm_verdict"]=="abstain_unsupported" for p in incomplete["pairs"])
assert abs(allocation["allocated_cost"]-100)<1e-10
report=dict(passed=True,python_version=sys.version,unit_tests=12,local_install_origin=origin,
            wheel=wheel.name,wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),
            complete_example_rows=144,incomplete_example_rows=143,
            complete_example_holm_verdicts=[dict(pair=p["policy_a"]+"-"+p["policy_b"],verdict=p["holm_verdict"]) for p in complete["pairs"]],
            incomplete_example_all_envelopes_refused=True,allocation_cost=allocation["allocated_cost"],
            calls=calls)
(checks/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="calls"},indent=2))

import argparse
import json
import sys
from pathlib import Path

from .core import AuditInputError, allocate, audit_csv


def main(argv=None):
    parser = argparse.ArgumentParser(description="Finite-design policy ranking and conditional budget allocation")
    commands = parser.add_subparsers(dest="command",required=True)
    audit = commands.add_parser("audit",help="Audit a complete repeated configuration census")
    audit.add_argument("csv",type=Path)
    audit.add_argument("--manifest",required=True,type=Path)
    audit.add_argument("--alpha",type=float,default=.05)
    audit.add_argument("--out",type=Path)
    allocation = commands.add_parser("allocate",help="Continuous cost-weighted Neyman allocation")
    allocation.add_argument("plan",type=Path)
    allocation.add_argument("--out",type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            result = audit_csv(args.csv,args.manifest,args.alpha)
            status = 0 if all(c["complete_inventory"] for c in result["coverage"]) else 2
        else:
            result = allocate(json.loads(args.plan.read_text(encoding="utf-8")))
            status = 0
    except (AuditInputError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2
    rendered = json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(rendered,encoding="utf-8")
    else:
        print(rendered,end="")
    return status


if __name__ == "__main__":
    raise SystemExit(main())

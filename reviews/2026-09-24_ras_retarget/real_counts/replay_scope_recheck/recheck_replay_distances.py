"""Read-only remeasurement of stored replay positions with strict input coverage.

No simulation executes, and no historical result is overwritten. Outputs are
written only next to this script. Requires NumPy. To pin a subsequent recheck to
the same input bytes, pass --verify-inputs after the initial successful run.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[3]
SCOPES = [
    {"id":"ms3_grid","directory":"results/replay_sysid_100/grid","mode":"equal_ratio_groups","stack":"ManiSkill3"},
    {"id":"ms2_grid","directory":"results/replay_sysid_ms2/grid","mode":"equal_ratio_groups","stack":"ManiSkill2 (original stack)"},
    {"id":"ms2_extended_scale","directory":"results/replay_sysid_ms2/iso_ratio_v1","mode":"equal_ratio_groups","stack":"ManiSkill2 (original stack)"},
    {"id":"ms3_torque","directory":"results/replay_sysid_100/sweep_v1","mode":"torque","stack":"ManiSkill3"},
    {"id":"ms2_torque","directory":"results/replay_sysid_ms2/sweep_v1","mode":"torque","stack":"ManiSkill2 (original stack)"},
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return path.relative_to(WORKSPACE).as_posix()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-inputs",action="store_true")
    args=parser.parse_args()
    old_manifest = None
    if args.verify_inputs:
        old_manifest=json.loads((HERE/"INPUT_MANIFEST.json").read_text(encoding="utf-8"))
        for entry in old_manifest["files"]:
            path=WORKSPACE/entry["path"]
            if not path.is_file() or sha(path)!=entry["sha256"]:
                raise RuntimeError(f"Missing or changed frozen input: {entry['path']}")

    files={}
    def register(path,scope_id,kind):
        key=rel(path)
        if not path.is_file():
            raise RuntimeError(f"Missing required input (no silent intersection): {key}")
        if key not in files:
            files[key]={"path":key,"sha256":sha(path),"bytes":path.stat().st_size,"kind":kind,"scopes":[]}
        if scope_id not in files[key]["scopes"]:
            files[key]["scopes"].append(scope_id)
        return files[key]

    scope_outputs=[]
    for spec in SCOPES:
        scope_id=spec["id"]
        directory=WORKSPACE/spec["directory"]
        meta_path=directory/"run_meta.json"
        register(meta_path,scope_id,"run_metadata")
        meta=json.loads(meta_path.read_text(encoding="utf-8"))
        expected=meta["demo_ids"]
        assert len(expected)==meta["n_demos"]==98
        assert len(set(expected))==98
        settings=meta["conditions"]
        selected=["nominal","force_x0.5"] if spec["mode"]=="torque" else list(settings)
        for name in selected:
            assert name in settings, (scope_id,name)
        arrays={}
        gt_reference={}
        condition_rows=[]
        for name in selected:
            record_path=directory/f"{name}.jsonl"
            register(record_path,scope_id,"episode_records")
            records=[json.loads(line) for line in record_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            observed=[r["episode_id"] for r in records]
            if len(observed)!=len(set(observed)):
                raise RuntimeError(f"Duplicate demo records: {record_path}")
            missing=sorted(set(expected)-set(observed))
            extra=sorted(set(observed)-set(expected))
            if missing or extra:
                raise RuntimeError(f"Record inventory mismatch: {record_path}; missing={missing}; extra={extra}")
            by_id={r["episode_id"]:r for r in records}
            for demo in expected:
                path=directory/f"{name}_ep{demo:03d}.npz"
                register(path,scope_id,"trajectory_npz")
                with np.load(path,allow_pickle=False) as contents:
                    data={key:np.array(contents[key],copy=True) for key in ("sim_p","sim_q","gt_p","gt_q")}
                p,q=data["sim_p"],data["sim_q"]
                if p.ndim!=2 or p.shape[1]!=3 or q.shape!=(len(p),4) or len(p)!=by_id[demo]["steps"]:
                    raise RuntimeError(f"Unexpected trajectory shape/step count: {path}")
                if not all(np.isfinite(value).all() for value in data.values()):
                    raise RuntimeError(f"Nonfinite trajectory: {path}")
                if data["gt_p"].shape!=p.shape or data["gt_q"].shape!=q.shape:
                    raise RuntimeError(f"Ground-truth shape mismatch: {path}")
                if demo not in gt_reference:
                    gt_reference[demo]=(data["gt_p"],data["gt_q"])
                elif not(np.array_equal(gt_reference[demo][0],data["gt_p"]) and np.array_equal(gt_reference[demo][1],data["gt_q"])):
                    raise RuntimeError(f"Different recorded demonstration under different conditions: {path}")
                arrays[(name,demo)]=(p,q,path)
            condition_rows.append({"condition":name,"settings":settings[name],"expected_demos":98,"observed_demos":len(observed),"missing_demos":[],"extra_demos":[]})

        if spec["mode"]=="torque":
            groups=[{"id":"halved_torque_vs_nominal","names":["nominal","force_x0.5"],"relative_damping_to_stiffness_ratio":1.,"delay_steps":0}]
        else:
            grouped={}
            for name in selected:
                c=settings[name]
                if c.get("force_scale",1.)!=1.:
                    continue
                ratio=round(c.get("damping_scale",1.)/c.get("stiffness_scale",1.),6)
                delay=int(c.get("delay_steps",0))
                grouped.setdefault((ratio,delay),[]).append(name)
            groups=[{"id":f"d_over_k_relative_{ratio}_delay_{delay}","names":names,
                     "relative_damping_to_stiffness_ratio":ratio,"delay_steps":delay}
                    for (ratio,delay),names in sorted(grouped.items()) if len(names)>1]

        best_euclidean=None
        best_coordinate=None
        group_outputs=[]
        for group in groups:
            group_euc=None
            group_coord=None
            pairs=[]
            for a,b in itertools.combinations(group["names"],2):
                unchanged_p,unchanged_q,unchanged_pose,changed=0,0,0,[]
                pair_euc=None
                pair_coord=None
                for demo in expected:
                    pa,qa,path_a=arrays[(a,demo)]
                    pb,qb,path_b=arrays[(b,demo)]
                    if pa.shape!=pb.shape or qa.shape!=qb.shape:
                        raise RuntimeError(f"Unaligned trajectories: {a}, {b}, demo {demo}")
                    delta=pa-pb
                    norms=np.linalg.norm(delta,axis=1)
                    euc_t=int(np.argmax(norms));euc=float(norms[euc_t])
                    coord_t,coord_axis=[int(v) for v in np.unravel_index(np.abs(delta).argmax(),delta.shape)]
                    coord=float(abs(delta[coord_t,coord_axis]))
                    assert coord<=euc+1e-18 and euc<=math.sqrt(3)*coord+1e-18
                    equal_p=pa.dtype==pb.dtype and pa.tobytes()==pb.tobytes()
                    equal_q=qa.dtype==qb.dtype and qa.tobytes()==qb.tobytes()
                    unchanged_p+=equal_p;unchanged_q+=equal_q;unchanged_pose+=equal_p and equal_q
                    base={"demo_id":demo,"condition_a":a,"condition_b":b,"settings_a":settings[a],"settings_b":settings[b],
                          "path_a":rel(path_a),"path_b":rel(path_b),"sha256_a":files[rel(path_a)]["sha256"],"sha256_b":files[rel(path_b)]["sha256"],
                          "group":group["id"]}
                    event_euc={**base,"metres":euc,"millimetres":euc*1000,"micrometres":euc*1e6,
                               "time_index_zero_based":euc_t,"delta_xyz_metres":delta[euc_t].tolist()}
                    event_coord={**base,"metres":coord,"millimetres":coord*1000,"micrometres":coord*1e6,
                                 "time_index_zero_based":coord_t,"axis_zero_based":coord_axis,"delta_xyz_metres":delta[coord_t].tolist()}
                    if pair_euc is None or euc>pair_euc["metres"]:pair_euc=event_euc
                    if pair_coord is None or coord>pair_coord["metres"]:pair_coord=event_coord
                    if not(equal_p and equal_q):
                        changed.append({"demo_id":demo,"position_bitwise_equal":equal_p,"quaternion_bitwise_equal":equal_q,
                                        "maximum_euclidean_metres":euc,"maximum_absolute_coordinate_metres":coord})
                pair={"condition_a":a,"condition_b":b,"n_demos":98,"position_bitwise_equal":unchanged_p,
                      "quaternion_bitwise_equal":unchanged_q,"pose_bitwise_equal":unchanged_pose,
                      "max_euclidean":pair_euc,"max_coordinate":pair_coord}
                if spec["mode"]=="torque":pair["changed_demonstrations"]=changed
                pairs.append(pair)
                if group_euc is None or pair_euc["metres"]>group_euc["metres"]:group_euc=pair_euc
                if group_coord is None or pair_coord["metres"]>group_coord["metres"]:group_coord=pair_coord
            group_outputs.append({**group,"pair_count":len(pairs),"pairs":pairs,"max_euclidean":group_euc,"max_coordinate":group_coord})
            if best_euclidean is None or group_euc["metres"]>best_euclidean["metres"]:best_euclidean=group_euc
            if best_coordinate is None or group_coord["metres"]>best_coordinate["metres"]:best_coordinate=group_coord
        scope_outputs.append({**spec,"metadata_sha256":files[rel(meta_path)]["sha256"],"expected_demo_ids":expected,
                              "missing_input_allowance":0,"complete":True,"condition_inventory":condition_rows,
                              "groups":group_outputs,"max_euclidean":best_euclidean,"max_coordinate":best_coordinate})
        print(f"{scope_id}: max Euclidean = {best_euclidean['millimetres']:.12g} mm; coordinate = {best_coordinate['millimetres']:.12g} mm",flush=True)

    if old_manifest is not None:
        assert set(files)=={f["path"] for f in old_manifest["files"]}, "Input inventory changed"
    entries=[files[k] for k in sorted(files)]
    manifest={"schema_version":1,"workspace_relative_paths":True,"missing_input_allowance":0,"file_count":len(entries),"files":entries}
    (HERE/"INPUT_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    with (HERE/"INPUT_SHA256SUMS.txt").open("w",encoding="utf-8",newline="\n") as stream:
        for item in entries:stream.write(item["sha256"]+"  "+item["path"]+"\n")
    result={"schema_version":1,"measurement":"Maximum over matched demonstration/time/condition pairs of the Euclidean norm of stored sim_p displacement; componentwise maxima retained only for provenance.",
            "coordinate_system":"The simulator's stored end-effector position coordinates, in metres; no image-pixel or joint-space metric.",
            "bitwise_definition":"Identical dtype, shape and array bytes for sim_p and sim_q separately; no claim about unrecorded joint or torque states.",
            "missing_input_allowance":0,"script_sha256":sha(Path(__file__)),"input_manifest_sha256":sha(HERE/"INPUT_MANIFEST.json"),
            "checks":{"five_scopes_complete":True,"duplicate_demo_records":0,"missing_demo_records":0,"missing_npz_files":0,
                      "unaligned_shapes":0,"nonfinite_arrays":0,"ground_truth_mismatches":0,"euclidean_coordinate_norm_inequalities":True},
            "scopes":scope_outputs}
    (HERE/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    with (HERE/"SUMMARY.csv").open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=["scope","euclidean_mm","coordinate_mm","demo_id","condition_a","condition_b","time_index_zero_based"])
        writer.writeheader()
        for s in scope_outputs:
            e=s["max_euclidean"]
            writer.writerow(dict(scope=s["id"],euclidean_mm=e["millimetres"],coordinate_mm=s["max_coordinate"]["millimetres"],
                                 demo_id=e["demo_id"],condition_a=e["condition_a"],condition_b=e["condition_b"],time_index_zero_based=e["time_index_zero_based"]))
    print(f"Complete: {len(entries)} input files pinned; no missing inputs tolerated.",flush=True)


if __name__=="__main__":
    main()

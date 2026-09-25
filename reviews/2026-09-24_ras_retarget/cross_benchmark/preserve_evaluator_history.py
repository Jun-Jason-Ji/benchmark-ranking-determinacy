from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
s=(p/'run_native_policies.py').read_text()
s=s.replace("task_object = base.cube if hasattr(base, 'cube') else base.obj\ninitial = dict(qpos=tensor(base.agent.robot.get_qpos()), cube_pose=tensor(task_object.pose.raw_pose))", "initial = dict(qpos=tensor(base.agent.robot.get_qpos()), cube_pose=tensor(base.cube.pose.raw_pose))")
s=s.replace("elif hasattr(base,'goal_region'): initial['goal_pose']=tensor(base.goal_region.pose.raw_pose)\n",'')
q=p/'run_native_policies_v1.py'
q.write_text(s,encoding='utf-8',newline='\n')
sha=hashlib.sha256(q.read_bytes()).hexdigest()
assert sha=='8a4ce14d3fd7aa2e5476c857781a599252b116e53d3f5916d8ba76facacd90fd'
print(sha)

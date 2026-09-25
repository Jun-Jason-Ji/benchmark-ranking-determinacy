"""Fresh, nominal-settled Bridge environment per episode; no installed-file edits."""
from contextlib import contextmanager
from pathlib import Path
import gc,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
import controller_sweep as sweep
import numpy as np
import torch
import gymnasium as gym


def state_hash(state):
    return hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()


def joint_properties(controller):
    return {key:[float(np.asarray(sweep.to_json(getattr(joint,key))).reshape(-1)[0])
                 for joint in controller.joints]
            for key in ['stiffness','damping','force_limit','friction']}


def controller_properties(controller):
    return {key:list(map(float,np.broadcast_to(getattr(controller.config,key),len(controller.joints))))
            for key in ['stiffness','damping','force_limit']}


def contact_properties(base):
    # Read only actual per-body mass and collision material properties.
    result={}
    for name,actor in base.objs.items():
        bodies=[]
        for body in actor._bodies:
            shapes=[]
            for shape in body.get_collision_shapes():
                material=shape.get_physical_material()
                shapes.append({key:float(getattr(material,key)) for key in
                               ['static_friction','dynamic_friction','restitution']})
            bodies.append(dict(mass=float(body.mass),collision_materials=shapes))
        result[name]=bodies
    return result


@contextmanager
def fresh_reset_episode(env_id,episode_id,condition,render_backend):
    """Yield (new env, canonical initial obs, audit); close it on every exit.

    Caller must acquire base/controller references only inside the context and
    create its external delay queue anew for the episode. No policy is called.
    Supported conditions deliberately exclude contact/gripper changes.
    """
    from mani_skill.envs.tasks.digital_twins.bridge_dataset_eval import base_env as bridge
    if condition not in ['nominal','fitted']:raise ValueError(condition)
    expected_scale=(1.,1.) if condition=='nominal' else (2.,.5)
    started=time.perf_counter()
    # This also restores nominal contact/model-density class configuration.
    sweep.apply_condition(bridge.WidowX250SBridgeDatasetFlatTable,{})
    env=gym.make(env_id,obs_mode='rgb+segmentation',num_envs=1,
                 sim_backend='cpu',render_backend=render_backend)
    audit={}
    try:
        base=env.unwrapped
        assert base.control_freq==5 and base.sim_freq==500
        assert base.scene is not None and base.agent is not None
        arm=base.agent.controller.controllers['arm']
        gripper=base.agent.controller.controllers['gripper']
        nominal_arm=controller_properties(arm)
        assert np.allclose(nominal_arm['stiffness'],sweep.NOMINAL['arm_stiffness'])
        assert np.allclose(nominal_arm['damping'],sweep.NOMINAL['arm_damping'])
        obs,_=env.reset(seed=int(episode_id),options={'episode_id':torch.tensor([int(episode_id)])})
        before=sweep.to_json(base.get_state_dict())
        rgb=obs['sensor_data']['3rd_view_camera']['rgb'][0].detach().cpu().numpy().copy()
        gripper_before=joint_properties(gripper)
        contact_before=contact_properties(base)
        arm.config.stiffness=[v*expected_scale[0] for v in sweep.NOMINAL['arm_stiffness']]
        arm.config.damping=[v*expected_scale[1] for v in sweep.NOMINAL['arm_damping']]
        arm.config.force_limit=list(sweep.NOMINAL['arm_force_limit'])
        arm.set_drive_property()
        after=sweep.to_json(base.get_state_dict())
        assert before==after,'Assigning gains changed canonical state'
        built=controller_properties(arm);actual=joint_properties(arm)
        for key in ['stiffness','damping','force_limit']:
            assert np.allclose(built[key],actual[key],rtol=2e-6,atol=1e-5),(key,built,actual)
        assert joint_properties(gripper)==gripper_before
        assert contact_properties(base)==contact_before
        assert arm.articulation is base.agent.robot
        assert arm.scene is base.scene
        audit.update(dict(episode_id=int(episode_id),condition=condition,
            seed=int(episode_id),state=before,state_sha256=state_hash(before),
            image_sha256=hashlib.sha256(rgb.tobytes()).hexdigest(),image_shape=list(rgb.shape),
            nominal_settling_completed_before_condition=True,physics_steps_after_condition=0,
            built_controller=built,actual_joints=actual,gripper=gripper_before,
            object_contact=contact_before,control_freq=5,sim_freq=500,
            delay_steps=0 if condition=='nominal' else 1,
            active_controller_references_new_scene=True,
            initialization_seconds=time.perf_counter()-started))
        yield env,obs,audit
    finally:
        env.close()
        audit['closed_scene_and_agent_cleared']=env.unwrapped.scene is None and env.unwrapped.agent is None
        assert audit['closed_scene_and_agent_cleared']
        gc.collect()

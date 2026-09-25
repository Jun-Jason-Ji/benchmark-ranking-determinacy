"""Record exact external-check runtime files without modifying installed packages."""
import hashlib, importlib.metadata, json, platform, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PACKAGE=ROOT/'.venv-windows-ms3/Lib/site-packages'
paths=[PACKAGE/'mani_skill/envs/tasks/tabletop/pick_cube.py',
       PACKAGE/'mani_skill/envs/tasks/tabletop/push_cube.py',
       PACKAGE/'mani_skill/envs/sapien_env.py',
       PACKAGE/'mani_skill/agents/robots/panda/panda.py',
       PACKAGE/'mani_skill/agents/controllers/pd_joint_pos.py',
       PACKAGE/'mani_skill/agents/controllers/pd_ee_pose.py',
       PACKAGE/'mani_skill/agents/controllers/utils/kinematics.py',
       HERE/'physx_runtime/PhysXGpu_64.dll',HERE/'physx_windows_dll.zip']
files={str(p.relative_to(ROOT)).replace('\\','/'):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
       for p in paths if p.exists()}
report=dict(platform=platform.platform(),python=platform.python_version(),
            versions={k:importlib.metadata.version(k) for k in ['torch','mani_skill','sapien','gymnasium','numpy','scipy']},
            gpu=subprocess.run(['nvidia-smi','--query-gpu=name,memory.total,driver_version','--format=csv,noheader'],capture_output=True,text=True).stdout.strip(),
            public_model_revision=json.loads((HERE/'hf_dataset_metadata.json').read_text())['sha'],
            source_files=files, runtime_library_source='https://github.com/sapien-sim/physx-precompiled/releases/tag/105.1-physx-5.3.1.patch0',
            process_local_activation='ctypes load official PhysX GPU DLL then sapien.physx._enable_gpu(); no installed module patch')
(HERE/'ENVIRONMENT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))

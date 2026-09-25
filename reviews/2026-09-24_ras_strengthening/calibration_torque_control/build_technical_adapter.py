"""Derive independent technical files without editing the frozen source study."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'calibration_reset_validation'
V3=HERE.parent/'calibration_confirmation_v3'

adapter=(BASE/'fresh_reset.py').read_text()
adapter=adapter.replace('Fresh, nominal-settled Bridge environment per episode; no installed-file edits.',
    'Separate half-torque control; fresh nominal-settled Bridge environment per episode.')
adapter=adapter.replace("['nominal','fitted']", "['nominal','forcehalf']")
adapter=adapter.replace("expected_scale=(1.,1.) if condition=='nominal' else (2.,.5)",
    "force_scale=1. if condition=='nominal' else .5")
adapter=adapter.replace("[v*expected_scale[0] for v in sweep.NOMINAL['arm_stiffness']]", "list(sweep.NOMINAL['arm_stiffness'])")
adapter=adapter.replace("[v*expected_scale[1] for v in sweep.NOMINAL['arm_damping']]", "list(sweep.NOMINAL['arm_damping'])")
adapter=adapter.replace("arm.config.force_limit=list(sweep.NOMINAL['arm_force_limit'])",
    "arm.config.force_limit=[v*force_scale for v in sweep.NOMINAL['arm_force_limit']]")
adapter=adapter.replace("'Assigning gains changed canonical state'", "'Assigning torque limit changed canonical state'")
adapter=adapter.replace("delay_steps=0 if condition=='nominal' else 1,", "delay_steps=0,force_limit_scale=force_scale,")
assert 'expected_scale' not in adapter and "'fitted'" not in adapter
(HERE/'fresh_reset_torque.py').write_text(adapter,encoding='utf-8')

runner=(V3/'execute_cell.py').read_text()
runner=runner.replace('V3 isolated scene initialization; one fresh environment per episode.',
    'Independent secondary half-torque control; one fresh environment per episode.')
runner=runner.replace('within a frozen, reset-validated V3 study', 'within a separately frozen, reset-validated secondary study')
runner=runner.replace("sys.path.insert(0,str(RESET))", "sys.path.insert(0,str(HERE))")
runner=runner.replace("choices=['nominal','fitted']", "choices=['forcehalf']")
runner=runner.replace('V3-controlled-initialization','SECONDARY-controlled-initialization-half-torque')
runner=runner.replace('V3 is not validated/frozen','Secondary torque study is not validated/frozen')
runner=runner.replace('from fresh_reset import','from fresh_reset_torque import')
runner=runner.replace("RESET/'fresh_reset.py'", "HERE/'fresh_reset_torque.py'")
runner=runner.replace("delay=0 if condition=='nominal'else 1", "delay=0")
runner=runner.replace("'fresh environment; nominal settling; then arm condition applied without physics advance'",
    "'fresh environment; nominal settling; then arm force limits halved without physics advance'")
runner=runner.replace("check(initial['delay_steps']==delay,'Adapter delay mismatch')", """check(initial['delay_steps']==delay,'Adapter delay mismatch')
            check(initial['force_limit_scale']==.5,'Adapter force limit scale mismatch')
            for key,expected in [('stiffness',sweep.NOMINAL['arm_stiffness']),('damping',sweep.NOMINAL['arm_damping']),('force_limit',[v*.5 for v in sweep.NOMINAL['arm_force_limit']])]:
                check(np.allclose(initial['built_controller'][key],expected,rtol=2e-6,atol=1e-5),'Unexpected controller parameter: '+key)
                check(np.allclose(initial['actual_joints'][key],expected,rtol=2e-6,atol=1e-5),'Unexpected physical drive parameter: '+key)""")
runner=runner.replace("initialization_protocol='fresh_nominal_settled_then_condition'", "initialization_protocol='fresh_nominal_settled_then_half_torque'")
assert "'fitted'" not in runner
(HERE/'execute_cell.py').write_text(runner,encoding='utf-8')

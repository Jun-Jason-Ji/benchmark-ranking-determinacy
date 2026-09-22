"""Explicit, process-local adapter for exploratory Windows ManiSkill3 runs.

Changes IK from Pinocchio to ManiSkill's existing torch Jacobian solver on CPU.
This changes control behavior and is NOT an original SIMPLER reproduction.
The PCI parsing fix enables the existing host-copy image path for CPU physics.
No installed package files or system settings are changed.
"""
def apply_compatibility():
    import mani_skill
    if mani_skill.__version__ != "3.0.1":
        raise RuntimeError("Re-audit this compatibility adapter for the installed ManiSkill version")
    from mani_skill.agents.controllers.utils.kinematics import Kinematics
    from mani_skill.envs.utils.system import backend
    Kinematics._setup_cpu = Kinematics._setup_gpu
    original_parser = backend.parse_backend_device_id

    def parse_device(value):
        if value is not None and value.startswith("pci:"):
            return value, None
        return original_parser(value)

    backend.parse_backend_device_id = parse_device
    return dict(ik="upstream_torch_jacobian_solver_on_cpu",
                pci_parser="preserve_full_pci_address", benchmark_equivalent=False)

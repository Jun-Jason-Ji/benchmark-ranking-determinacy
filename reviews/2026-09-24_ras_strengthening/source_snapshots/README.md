# Read-only implementation snapshots

These six unchanged ManiSkill 3.0.1 source files are inputs to the frozen calibration
integrity audit. They are not a simulator installation. Original license and third-party
notices accompany them. They were read from the recorded local installation; no source
file was patched. Hashes identify the exact inspected version.

For CPU reproduction, extract the research packages into a NEW EMPTY working directory,
then run `materialize_audit_sources.py` from the strengthening directory. It creates only
the exact source paths required by the frozen analyzer, refuses a Git checkout or an
existing Python environment, and never overwrites differing files. It does not install
or execute ManiSkill. The frozen analysis then needs NumPy/SciPy, not a GPU.

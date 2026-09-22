@echo off
setlocal
set ROOT=E:\research\the_world
set MS_ASSET_DIR=%ROOT%\data\maniskill-assets
set PYTHONIOENCODING=utf-8
cd /d %ROOT%
echo ==== %DATE% %TIME% download shards 1-3
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\read_bridge_batch.py --shard 1 --n 30 --name-offset 30 --out data\bridge_sysid
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\read_bridge_batch.py --shard 2 --n 30 --name-offset 60 --out data\bridge_sysid
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\read_bridge_batch.py --shard 3 --n 10 --name-offset 90 --out data\bridge_sysid
echo ==== %DATE% %TIME% replay sweep_v1 (100 demos)
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\replay_bridge_sysid.py --episodes 100 --preset sweep_v1 --output-dir results\replay_sysid_100
echo ==== %DATE% %TIME% replay grid (100 demos)
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\replay_bridge_sysid.py --episodes 100 --grid --output-dir results\replay_sysid_100
"%ROOT%\.venv-windows-ms3\Scripts\python.exe" scripts\check_iso_invariance.py --dir results\replay_sysid_100\grid
echo REPLAY100_DONE

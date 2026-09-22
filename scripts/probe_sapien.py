"""Isolated renderer probe. Run separately because native driver errors can abort."""
import argparse
import json
import os
import platform
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
record = {
    "platform": platform.platform(),
    "VK_ICD_FILENAMES": os.environ.get("VK_ICD_FILENAMES"),
    "status": "started",
}
output = Path(args.output)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(record, indent=2))
print("Starting SAPIEN import and renderer probe", flush=True)
try:
    import sapien.core as sapien
    engine = sapien.Engine()
    record["physics_engine"] = "created"
    output.write_text(json.dumps(record, indent=2))
    renderer = sapien.SapienRenderer(offscreen_only=True)
    engine.set_renderer(renderer)
    scene = engine.create_scene()
    camera = scene.add_camera("probe", 64, 64, 1, 0.01, 10)
    scene.update_render()
    camera.take_picture()
    color = (camera.get_float_texture("Color") if hasattr(camera, "get_float_texture")
             else camera.get_picture("Color"))
    record.update(status="passed", image_shape=list(color.shape))
except Exception as error:
    record.update(status="failed", error_type=type(error).__name__, error=str(error))
    raise
finally:
    output.write_text(json.dumps(record, indent=2))
    print(json.dumps(record, indent=2), flush=True)

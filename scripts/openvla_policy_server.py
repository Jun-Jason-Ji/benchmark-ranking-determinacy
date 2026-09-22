"""Local HTTP policy server for OpenVLA-7B (openvla/openvla-7b) on Windows CUDA, 4-bit (nf4) via
bitsandbytes so it fits in 8 GB. Same HTTP API as octo_policy_server.py (POST /reset, POST /step, GET /health)
so controller_sweep.py can drive it unchanged (policy name: "openvla-7b-4bit").

Pre/post-processing follows the SimplerEnv-OpenVLA wrapper (widowx_bridge setup):
  * image -> PIL RGB (processor resizes to 224), prompt "In: What action should the robot take to {instr}?\nOut:"
  * predict_action(..., unnorm_key="bridge_orig", do_sample=False) -> 7-dim [dx,dy,dz,droll,dpitch,dyaw,gripper]
  * rotation rpy -> axis-angle via transforms3d euler2axangle (static xyz); gripper binarised 2*(g>0.5)-1
The 4-bit quantised model is a different policy from the bf16 release; it is used as a second model family
for ranking-sensitivity experiments, not as a reproduction of published OpenVLA numbers.
"""
import argparse
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

os.environ.setdefault("HF_HOME", r"E:\models\hf")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import numpy as np


class OpenVLAPolicy:
    def __init__(self, model_id="openvla/openvla-7b", quant="4bit", unnorm_key="bridge_orig"):
        import torch
        from PIL import Image
        from transformers import AutoModelForVision2Seq, AutoProcessor, BitsAndBytesConfig
        self.torch, self.Image = torch, Image
        t0 = time.perf_counter()
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        kw = dict(trust_remote_code=True, low_cpu_mem_usage=True)
        kw["torch_dtype"] = torch.bfloat16  # non-quantised parts (vision backbone, projector) must match the bf16 inputs/compute dtype
        if quant == "4bit":
            kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_quant_type="nf4")
        elif quant == "8bit":
            kw["quantization_config"] = BitsAndBytesConfig(load_in_8bit=True)
        else:
            kw["torch_dtype"] = torch.bfloat16
        self.vla = AutoModelForVision2Seq.from_pretrained(model_id, device_map="cuda:0", **kw).eval()
        self.load_seconds = time.perf_counter() - t0
        self.unnorm_key = unnorm_key
        self.quant = quant
        self.lock = threading.Lock()
        self.instruction = None
        self.step_count = 0

    def reset(self, instruction, seed=0, config=None):
        self.instruction = instruction
        self.step_count = 0

    def step(self, image_u8):
        from transforms3d.euler import euler2axangle
        torch = self.torch
        t0 = time.perf_counter()
        img = self.Image.fromarray(np.ascontiguousarray(image_u8)).convert("RGB")
        prompt = f"In: What action should the robot take to {self.instruction}?\nOut:"
        inputs = self.processor(prompt, img).to("cuda:0", dtype=torch.bfloat16)
        with torch.inference_mode():
            raw = self.vla.predict_action(**inputs, unnorm_key=self.unnorm_key, do_sample=False)
        raw = np.asarray(raw, dtype=np.float64).reshape(-1)
        world = raw[:3]
        ax, ang = euler2axangle(*raw[3:6])
        rot = np.asarray(ax, dtype=np.float64) * float(ang)
        gripper = 2.0 * float(raw[6] > 0.5) - 1.0
        action = np.concatenate([world, rot, [gripper]])
        self.step_count += 1
        return {"action": action.tolist(), "raw_action": raw.tolist(), "inference_seconds": time.perf_counter() - t0, "history_len": 1, "from_chunk": False}


def make_handler(policy, meta):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, code, payload):
            body = json.dumps(payload).encode()
            self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

        def do_GET(self):
            self._json(200, dict(meta, step_count=policy.step_count)) if self.path == "/health" else self._json(404, {"error": "unknown path"})

        def do_POST(self):
            n = int(self.headers.get("Content-Length", "0")); body = self.rfile.read(n)
            try:
                if self.path == "/reset":
                    req = json.loads(body)
                    with policy.lock:
                        policy.reset(req["instruction"], int(req.get("seed", 0)), req.get("config"))
                    self._json(200, {"ok": True})
                elif self.path == "/step":
                    shape = tuple(int(v) for v in self.headers["X-Shape"].split(","))
                    img = np.frombuffer(body, dtype=np.uint8).reshape(shape)
                    with policy.lock:
                        self._json(200, policy.step(img))
                else:
                    self._json(404, {"error": "unknown path"})
            except Exception as e:
                self._json(500, {"error": f"{type(e).__name__}: {e}"})
    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openvla/openvla-7b")
    ap.add_argument("--quant", default="4bit", choices=["4bit", "8bit", "bf16"])
    ap.add_argument("--port", type=int, default=8771)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    import torch
    policy = OpenVLAPolicy(args.model, args.quant)
    tw = time.perf_counter()
    policy.reset("warmup")
    for _ in range(2):
        policy.step(np.zeros((480, 640, 3), dtype=np.uint8))
    meta = dict(model=f"openvla-7b-{args.quant}", hf_id=args.model, quant=args.quant, torch=torch.__version__,
                gpu=torch.cuda.get_device_name(0), vram_alloc_gb=round(torch.cuda.memory_allocated() / 1e9, 2),
                load_seconds=policy.load_seconds, jit_warmup_seconds=time.perf_counter() - tw,
                rotation_convention="transforms3d.euler2axangle(roll,pitch,yaw) static xyz", unnorm_key=policy.unnorm_key,
                variants="reset config accepted but ignored (no history/ensemble in OpenVLA)")
    print(json.dumps(meta), flush=True)
    print(f"READY {args.host}:{args.port}", flush=True)
    ThreadingHTTPServer((args.host, args.port), make_handler(policy, meta)).serve_forever()


if __name__ == "__main__":
    main()

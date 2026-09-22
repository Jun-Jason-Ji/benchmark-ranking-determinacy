import os
os.environ.setdefault("HF_HOME", r"E:\models\hf")
from huggingface_hub import snapshot_download
p = snapshot_download("openvla/openvla-7b", allow_patterns=["*.json", "*.py", "*.safetensors", "*.txt", "*.model", "tokenizer*"], max_workers=4)
print("OPENVLA_DOWNLOAD_DONE", p, flush=True)

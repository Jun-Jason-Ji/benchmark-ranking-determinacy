# Octo 推理延迟：CPU（Windows）vs GPU（WSL2）

日期：2026-09-18。机器：i9-14900HX（24 核）、RTX 5060 Laptop 8 GB、驱动 616.92。
计时脚本：`scripts/time_policy_server.py`，同一张 640×480 真实渲染帧，服务器侧计时为纯推理（含前后处理），往返为 Windows 客户端 HTTP 往返。

| 服务器 | 框架栈 | 负载状态 | 每步推理（服务器侧） | 往返 |
|---|---|---|---:|---:|
| octo-small CPU | Windows, jax 0.4.20 CPU | 仅本进程 + 一个仿真 | 0.33 s | — |
| octo-small CPU | 同上 | 两个 CPU 服务器 + 两个 GPU 服务器 + 两个仿真 | 0.63 s | 1.26 s |
| octo-small GPU | WSL2, jax 0.5.3 + CUDA 12 插件 | CPU 扫描仍在跑 | 0.106 s | 0.134 s |
| octo-small GPU | 同上 | CPU 扫描已停，扫描中实测 | ≈0.058 s | — |
| octo-base CPU | Windows, jax 0.4.20 CPU | 两个 CPU 服务器 + 两个仿真 | ≈0.9 s | — |
| octo-base GPU | WSL2, jax 0.5.3 + CUDA 12 插件 | 两条 GPU 扫描同时跑 | 0.076 s | 0.097 s |

一集 60 步（含 CPU 物理仿真约 1.2 s）：octo-small GPU ≈ 5.8 s，octo-base GPU ≈ 8.3 s；CPU 阶段分别约 29 s 和 56 s。

## 为什么必须走 WSL2

- JAX 没有 Windows 原生 CUDA 轮子；TensorFlow 2.11 起也不再支持 Windows 原生 GPU。这台机器此前跑通的 GPU 任务是 PyTorch。
- Octo 钉死的 jax 0.4.20 及后来试的 0.4.30 都不认识 Blackwell（计算能力 12.0）：XLA 把 PTX 目标降到 Hopper 专用的 `sm_90a`，ptxas 报 “cannot be compiled to future architecture”。
- jax 0.5.3（CUDA 12.8 轮子）原生支持 Blackwell。连带升级：flax 0.10.4、orbax 0.11、tensorflow-cpu 2.18（只用于读文件）。
- Octo 源码两处补丁（`third_party/octo`，git diff 可见）：`jax.random.KeyArray` 改为 `jax.Array`；`distrax` 改为离散头采样处的延迟导入，避免 tensorflow_probability 在模块加载时要求 tf_keras。扩散头不用 distrax。
- WSL 对外网络不稳（PyPI、HuggingFace 间歇超时），服务器以离线模式读取 Windows 侧 HF 缓存 `E:\models\hf`。

## 数值一致性提醒

CPU 与 GPU 后端的浮点数值不同，同一 episode_id 的 rollout 可能分叉（胡萝卜任务 ep 0：CPU 成功、GPU 失败）。因此正式扫描全部在 GPU 后端重跑（`results/controller_sweep_gpu`），CPU 阶段已完成的条件（`results/controller_sweep`）只作为跨后端复现对照，不与 GPU 结果混合统计。

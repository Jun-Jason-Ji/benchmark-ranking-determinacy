# 真实校准数据入口验证

2026-09-18 已读取官方 SIMPLER 系统辨识脚本指向的公开 `bridge/0.1.0` 与 `fractal20220817_data/0.1.0` 元数据。

| 数据 | 训练集元数据大小 | 训练分片数 | 本轮实际下载 |
|---|---:|---:|---|
| Bridge | 365,981,955,835 字节 | 1024 | 元数据，以及首分片第 1 条记录 |
| fractal | 119,258,547,932 字节 | 1024 | 仅元数据 |

来源：`https://storage.googleapis.com/gresearch/robotics/{dataset}/0.1.0/`，对应源码为 `third_party/SimplerEnv/tools/sysid/prepare_sysid_dataset.py`，版本见执行记录。大小指数据集元数据记录值，不是本轮流量。

本次 Bridge 样本共 38 个时间步，下载 15,903,486 字节。TFRecord 长度与数据 CRC32C 均通过，两个分段请求 ETag 一致；完整记录的 SHA-256 见 `bridge_sample_ingestion.json`。

读取到的数值数组：状态 `(38,7)`，平移动作 `(38,3)`，旋转动作 `(38,3)`；均为有限值。保存至 `data/calibration_smoke/bridge_first_episode_numeric.npz`。原始 TFRecord 也保留，方便独立解码核对。

这是**已有真实示范的读取测试**。还没有拟合参数、判断这条轨迹适合校准哪些参数，也没有得到任何新真机成功率。源码按 TFDS 迭代序号选的第 0 条轨迹，与这里固定分片的第 1 条记录不保证相同。后续应固定分片、记录与帧标识，核验坐标变换、动作时间对齐、控制器版本和数据拆分后再使用。

读取器 `scripts/read_bridge_sample.py` 使用标准 TensorFlow Example 的 protobuf wire schema，但不加载 TensorFlow 运行时。它强制 HTTP 206 与 Content-Range，限制单记录 64 MiB，防止服务器忽略 Range 后下载整片。解析后的字段数量与数据集 schema 对照保存在 JSON。

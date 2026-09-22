# 执行与复现记录

执行日期：2026-09-18。

- Python：3.12.14；NumPy：2.3.5；Windows 11。
- 单元测试：`python -m unittest test_model -v`，8/8 通过。
- 实验：首轮约 5.49 秒，补充描述性 Wilson 区间后重跑约 5.36 秒。
- 逐试验输出：证据实验 54,000 条、机制实验 5,400 条，包含全部随机试验。
- 图表：SVG XML 解析成功；另由 `scripts/plot_pilot.py` 从相同 CSV 生成 Matplotlib PNG/PDF，已查看 PNG，文字、坐标和图例无裁切。原始 SVG 未作浏览器截图检查。
- 配置在运行前冻结；两次运行的配置、主种子与全部逐试验 CSV 保持不变。
- 第二次运行增加汇总列与代码 SHA-256，没有重选样本或改动原始数值。
- 初次通过受限执行器写输出时出现 `PermissionError`；特定脚本的提权执行获得批准后写入成功。没有安装全局包，没有更改系统或自启动设置。

逐试验 CSV 的两次 SHA-256 均一致：

```text
evidence_trials.csv
8cfb12016e926f4ea3cf65d67c911c9f9c12d8f3501436fb10c532c5a36e1655

mechanism_trials.csv
b9d9036da96ab14a1be9550818e8e5cae1bc8bc1ecd15e1fcb5add6c155b0051
```

名义 alpha=0.05、预算16的主集合方法没有观察到错误声明，但条件风险的 Wilson 95% 上界仍分别为：random 2.48%、D-opt 2.12%、c-opt 2.07%。这只是各固定条件下的描述性二项区间，不是跨预算、跨算法或选择后整体有效的区间。

结果仅支撑这个预设合成模型内的机制与实现检查。下一步真实机器人证据须独立完成。

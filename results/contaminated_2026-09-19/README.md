# 污染数据隔离（2026-09-19 03:15–04:35）

原因：Octo HTTP 策略服务器的观测历史与动作集成状态是进程级全局的，没有会话 id。03:15 起原版 SIMPLER 栈的扫描进程与 ManiSkill3 队列作业共用了 8767/8768（以及两次短暂的 8769 静态测试），两边策略看到交错的帧与对方的指令。

隔离内容（原文件中已删除对应记录）：
- 勺子任务（controller_sweep_gpu）：octo-small@hist1 fric_x0.4 ep≥24；octo-small nominal ≥48、force_x0.5 ≥48、dens_x0.5 ≥24、fric_x0.4 ≥24（8769 短暂污染，保守处理）
- 第二种子集（controller_sweep_gpu_rep）：octo-base dens_x0.5 全部；octo-base@hist1 iso_x0.25 全部
- 原版栈茄子扫描（controller_sweep_ms2）：全部（另有 robot 变体与叠加两处设置错误）
- analysis_spoon_hist1_96.md（基于污染数据生成）

处理：受影响作业重新排队；服务器加入会话隔离后才允许多客户端共用。

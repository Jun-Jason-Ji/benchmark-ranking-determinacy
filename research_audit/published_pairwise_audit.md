# SIMPLER 已发表均值的排序核查

这是已发表表格的描述性分析，不是新实验或显著性检验。

排除无公开权重的 RT-2-X 后，共 62 个任务内策略对；5 对的模拟与真实均值差值符号相反，3 对在至少一域出现均值平局。

| 任务 | 策略 i | 策略 j | 真实均值差 | 仿真均值差 |
|---|---|---|---:|---:|
| google_robot_pick_coke_can | rt-1-converged | rt-1-15pct | -0.067 | 0.147 |
| google_robot_move_near | rt-1-begin | octo-base | -0.333 | 0.008 |
| google_robot_close_drawer | rt-1-converged | rt-1-x | 0.185 | -0.030 |
| google_robot_close_drawer | rt-1-15pct | rt-1-x | 0.148 | -0.224 |
| widowx_carrot_on_plate | octo-base | octo-small | 0.167 | -0.014 |

不能将这些对称为已统计确认的真实排序反转：原表为取整后的成功率，本次尚未建立每格试验次数、场景分层和逐试验结果。策略对共享策略与任务，彼此不独立。

此表仅用于协议审计与问题定位；若据此选择任务，需如实标记为已查看开发信息，不能将这些同源标签重新称为未触碰测试集。正式验证必须冻结新的划分及分析规则。

数据来源及 SHA-256 见 simpler_manifest.json；全部策略对见 published_pairwise_audit.csv。

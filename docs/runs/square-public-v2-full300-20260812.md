# 1:1 Public Full300 技术报告

> 项目级架构、每条算法/Agent/AIGC 路线、前后端时序、成本状态机与完整复现说明见
> [`square-public-v2-full300-20260812-detailed.md`](square-public-v2-full300-20260812-detailed.md)。

> 日期：2026-08-12
> 数据集：`retarget_square_public_v2`
> 两轮证据：Pilot60 + 独立 Held-out240
> 最终聚合：`full300-agent-complete-v2`，300/300 Task、1,200/1,200 传统候选、18/18 arm 完整
> 校准状态：质量分、Proxy A/B 与模型 Judge 均为未经过人工 A/B/C 标定的自动证据

## 1. 结论

当前最值得继续推进的路线是 **Qwen3-VL-4B conditional Agent + 四个固定传统候选 + 受控外部生成门禁**。

- Full300 自动质量均分 `75.305`，Proxy Success `93.00%`，距离后验 Proxy-argmax 均分上界仅 `0.119`。
- 相比无 Agent generation selector，质量提高 `3.672` 分，Proxy Success 提高 `15.00` 个百分点。
- 相比 always-on 4B，conditional 少调用 `28/300` 次（`272` 对 `300`），选择质量几乎相同。
- Qwen3-VL-8B 没有胜过 4B：质量低 `0.537` 分，观测活跃能耗高约 `54%`。
- SmolVLM2 更快，但质量、成功率和结构化响应可靠性都明显较差；不应作为主 Judge。
- 四个传统方法中没有全场景赢家。Direct Warp 最稳地保留全部信息；Crop 的成功率最高但会裁掉完整主体；Seam 慢约一个数量级；Mesh 当前质量最低。

这不是“生成模型替代传统方法”的结论。Agent 只对每个 Task 已冻结的 `direct_warp / crop / seam / mesh` 四张候选排序，并决定使用传统结果、请求外部 AIGC、转人工或失败；它不跳过候选、不改参数、不在评测后补候选。

## 2. 数据与公平性

### 2.1 完整分母

| Split | 图片/Task | 候选 | 场景配额 | 比例压力 |
|---|---:|---:|---|---|
| Pilot | 60 | 240 | 10/10/10/10/7/7/6 | hard1 40 / hard2 12 / extreme 8 |
| Held-out | 240 | 960 | 40/40/40/40/27/26/27 | hard1 104 / hard2 86 / extreme 50 |
| Full | **300** | **1,200** | 50/50/50/50/34/33/33 | hard1 144 / hard2 98 / extreme 58 |

七类场景依次为中文密集海报、单商品、多商品商业混合、多人物、肖像、结构/建筑、复杂混合。Full300 包含 266 张 Wikimedia Commons 与 34 张 Open Images V7 图片；300/300 有作者、许可证、归因、来源 URL、raw/materialized SHA-256，像素物化后无 EXIF/GPS。程序化图片只保留在 fixture 测试，不进入任何真实分母。

许可证统计：CC BY 2.0 45、CC BY 3.0 12、CC BY 4.0 6、CC BY-SA 2.0 23、CC BY-SA 3.0 11、CC BY-SA 4.0 102、CC0 16、Public Domain 85。199 张需署名，101 张为 Public Domain/CC0。

### 2.2 两轮而非半轮比较

- Pilot60 用于验证链路、选择 Agent 模型与触发策略。
- Held-out240 使用不同图片独立冻结，完整运行同四方法、同 evaluator、同 Agent 路线。
- `full300-agent-complete-v2` 只聚合两轮均存在且分母完整的 18 个 arm；任一缺 Task 的 arm 会被拒绝。
- 旧报告和 Smol v1 失败证据均保留，新版本使用新 ID，不覆盖旧 Run。

## 3. 完整技术路线

1. 逐图来源/许可/安全审计，物化 1024 方形目标 Task。
2. 共享 CPU 保护分析：PPOCRv3 + 中文 CRNN、YuNet、YOLOX、Logo 区域候选、显著性与结构线；同一 Task 的四方法消费同一 AnalysisArtifact。
3. 固定生成四候选：Direct Warp、保护式 Crop、保护式 Seam、受约束 Mesh。
4. Evaluation Replay：解码/尺寸硬检查，OCR、人脸、人物、商品、Logo、结构、保真、完整性和性能指标。
5. 无 Agent 对照：固定方法、generation selector、规则 router、proxy ranker。
6. Agent 对照：Qwen3-VL-4B、Qwen3-VL-8B、SmolVLM2；各跑 always-on 与 conditional；结构化 JSON 失败时确定性安全回退。
7. 外部生成 planner：只有 Agent 请求、传统候选不可靠、逐图 egress 允许、预算允许时才进入付费队列。
8. 人工 A/B/C 评审暂缓；Codex 只做 14 个困难 Task 的非盲诊断抽审，不冒充人工标定。

## 4. 四种传统方法：Full300

| 方法 | 质量均分 | Proxy Success | 总 wall | 总 CPU | 峰值 RSS* | 5 CNY/CPUh 场景 |
|---|---:|---:|---:|---:|---:|---:|
| direct_warp | **71.057** | 77.33% | **62.18s** | **70.56s** | 1,126.9MiB | **0.0980 CNY** |
| crop | 70.287 | **79.33%** | 66.91s | 75.48s | 1,126.9MiB | 0.1048 CNY |
| seam | 69.639 | 76.67% | 1,672.96s | 1,909.14s | 1,126.9MiB | 2.6516 CNY |
| mesh | 65.844 | 65.67% | 64.60s | 77.22s | 1,126.9MiB | 0.1072 CNY |

\* RSS 是同一 Run 进程观测峰值，不是隔离后的单方法常驻内存。

Held-out 分层说明了为什么总均值不够：

| 难度 | Direct | Crop | Seam | Mesh |
|---|---:|---:|---:|---:|
| hard1 | 78.90 / 97.1% | 74.71 / 95.2% | 76.59 / 95.2% | 70.64 / 82.7% |
| hard2 | 66.94 / 69.8% | **69.51 / 76.7%** | 66.20 / 68.6% | 62.48 / 52.3% |
| extreme | 58.29 / 42.0% | **60.24 / 50.0%** | 57.60 / 42.0% | 57.59 / 36.0% |

单元格为“质量均分 / Proxy Success”。Extreme 仍明显未解决，不能用 hard1 的高成功率掩盖。

场景最高自动均分：中文海报 Direct 76.82、复杂混合 Direct 76.53、结构/建筑 Crop 65.63、多人物 Crop 72.00、多商品 Direct 70.31、肖像 Crop 72.46、单商品 Direct 70.66。肖像的 Crop 数值必须谨慎：视觉抽审发现其可能保留脸部却截断下半身，Proxy 会高估这种干净但不完整的裁剪。

## 5. Agent 与无 Agent：Full300

| 路线 | Calls | Schema | 质量均分 | Proxy Success | Regret | Call p50/p95 | 已观测 tokens |
|---|---:|---:|---:|---:|---:|---:|---:|
| 后验 Proxy argmax 上界 | 0 | n/a | **75.424** | 92.67% | 0.000 | n/a | 0 |
| 无 Agent selector | 0 | n/a | 71.633 | 78.00% | 3.791 | n/a | 0 |
| Rules / Proxy router | 0 | n/a | 73.701 | 86.00% | 1.723 | n/a | 0 |
| Qwen3-VL-4B always | 300 | 298/300 | **75.327** | **93.00%** | **0.097** | 6.125/13.481s | 1,247,550 / 299 calls |
| **Qwen3-VL-4B conditional** | **272** | **270/272** | **75.305** | **93.00%** | **0.119** | **6.154/13.497s** | **1,142,294 / 271 calls** |
| Qwen3-VL-8B always | 300 | 299/300 | 74.768 | 92.33% | 0.656 | 7.433/10.759s | 1,084,338 / 299 calls |
| Qwen3-VL-8B conditional | 272 | 271/272 | 74.768 | 92.33% | 0.656 | 7.493/10.866s | 982,791 / 271 calls |
| SmolVLM2 v2 always | 300 | 280/300 | 70.782 | 79.67% | 4.642 | 4.334/7.777s | 629,996 / 281 calls |
| SmolVLM2 v2 conditional | 272 | 255/272 | 71.326 | 80.33% | 4.097 | 4.323/7.798s | 576,079 / 256 calls |

Token 总量只在每次调用都有 usage 时才可称完整总量；表中明确写“已观测”，缺失调用没有按 0 填充。Conditional 的 272 次调用中，Qwen4B/Qwen8B 各有 271 次缓存命中；该回放证明选择一致性，表中时延仍采用生产中真实调用的冻结等价时延。

模型固定 revision：

- Qwen3-VL-4B `ebb281ec70b05090aa6165b016eac8ec08e71b17`
- Qwen3-VL-8B `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`
- SmolVLM2-2.2B `482adb537c021c86670beed01cd58990d01e72e4`

## 6. GPU、能耗和成本

以下是 gu27 RTX 3090 的约 1 秒 `nvidia-smi` 采样积分。Full300 数值是 Pilot 与 Held-out 实验窗口之和；Qwen Held-out 窗口包含冷启动、always 和缓存式 conditional，因此 `energy_coverage=unknown`，不能伪装成隔离的单臂计费。Smol 还混合了唯一一次 v2 重试，明确为 partial。

| 模型实验窗口 | Active GPU | Active Wh | Window Wh | 峰值显存 | 5 CNY/GPUh 场景 | 每个 Proxy-success** |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3-VL-4B | 1,011.18s | **73.16Wh** | 128.84Wh | 19,711MiB | **1.4044 CNY** | **约 0.00503 CNY** |
| Qwen3-VL-8B | 1,350.24s | 112.64Wh | 164.54Wh | 19,747MiB | 1.8753 CNY | 约 0.00677 CNY |
| SmolVLM2 v1+v2 | 907.15s | 55.37Wh | 104.90Wh | 22,249MiB | 1.2599 CNY | 不给精确值（混合重试窗口） |

\** 只是 5 CNY/GPU-hour 的基础设施情景折算，不是云厂商账单或模型 API 价格。

4B 比 8B 的自动质量更高，活跃能耗低约 35%，因此 8B 没有形成足够收益。Smol 参数更小却在 vLLM 0.90 显存预留下峰值更高，说明“参数少”不能直接等同“服务显存低”。

## 7. 外部生成与文字回贴

Full300 四路投票共请求 70 个唯一 Task：Pilot 10、Held-out 60。逐图 egress 和预算门禁后只有 Pilot 的 4 张公开结构图可进入 SeedDream 队列；计划成本 `1.20–2.40 CNY`，远低于 100 CNY 上限。Held-out 240 张全部 `api_egress_allowed=false`，因此即使 Agent 请求也选择 0 次付费调用。

本轮实际 SeedDream provider calls 为 0、付费支出为 0。原因不是省略链路：Provider、预算预留、HTTPS/SSRF、幂等、缓存、输出尺寸/解码/哈希验证已有 fake-server 测试；真实 key 曾出现在工具日志，按安全规则视为失效，未用它发起付费请求。轮换 key 后只需执行已冻结的 4-call Pilot 计划，预计仍为 1.20–2.40 CNY。

AnyText2 做过一个公开 1024²、30-step 受控 Smoke：纯采样 13.88s、冷启动 58.81s、峰值显存 11,373MiB；目标文字 OCR 召回和序列相似度均为 0，判业务失败。5 CNY/GPUh 冷启动情景约 0.0816 CNY，但 cost per usable result 为 `null`。自研不透明文字回贴单区阶段 0.0084s、目标字符召回/相似度 0.75，仍有底层文字残片和拼接边界，也不进入生产路由。

## 8. 代表图与视觉结论

交付包 `representative_images/` 包含七张高清 contact sheet，每个场景各一张；每张同时展示两个困难 Task 的源图与四种 1024² 候选，并带自动分数。它们是已实际查看过的抽审图，不是为了报告临时挑选的“最好看结果”。

主要视觉结论：

- Direct Warp 常是宽松标准下最可理解的结果，但人物、瓶体、圆形商品和建筑会被拉宽/压扁。
- Crop 构图自然，却会删除完整人物、商品、周边文案或多人队列；“局部干净”不等于主体完整。
- Seam 在大比例压力下会弯曲文字、人脸和结构，且成本最高。
- Mesh 会产生局部人脸、人体、商品与结构形变，当前实现不适合作主路线。
- 自动 Proxy 能发现许多明显 Crop/Mesh 失败，但对完整主体截断和全局比例变形处罚不足。

因此本报告允许在“主体信息可理解、无明显缺字/缺主体/严重变形”的放宽标准下给不错分数，但不会把 Proxy A/B 写成人工业务通过。

## 9. V7 里程碑状态

| 里程碑 | 状态 | 本轮后还需做什么 |
|---|---|---|
| M0 | 完成 | 数据/插件契约、配置、注册表、CLI、测试均已有；不用重做 |
| M1 | 完成并扩展 | 真实 Smoke12、Pilot60、Held-out240、Full300 已冻结；不用再用 fixture 冒充真实 Smoke |
| M2 | 完成 | 四真实方法、共享完整 OCR/人脸/人物/商品/Logo 候选/结构检测已运行；Logo 是保护区域候选，不宣称品牌识别 |
| M3 | 完成 | Generation、Replay、日志、性能、资源、成本和自动报告可回放 |
| M4 | 完成 | 高清网页评审、指引、A/B/C/Skip、追加事件和断点恢复已有；本轮按要求不做人工评分 |
| M5 | 自动部分完成 | 硬检查、Top-1、Oracle、Regret、scene/difficulty 报告已完成；人工校准后的 Bad Pass/False Reject 仍待 M6 标签 |
| M6 | 明确暂缓 | 按用户要求暂不做人工指引与人工评分实验 |
| M7 | Judge 实验完成 | 三模型 always/conditional、失败回退、Token/时延/能耗完成；Protection Agent 的语义消歧 Generation 对照尚未做 |
| M8 | 部分完成 | SeedDream adapter/fake 测试和 AnyText2 Smoke 完成；轮换 key 后真实 4-call Smoke、通用 WorkflowBackend 正式接入仍待做 |
| M9 | 部分完成 | CLI、Streamlit、高清 FastAPI 评审复用服务层；完整异步 retarget Job/取消/结果 API 尚未完成 |

因此，之前要求的高清 UI、清晰字体、详细 Reviewer 指引、高清原图读取和完整共享保护分析已经关闭了 M2a/M4 的对应工作，不需要再重复做。下一阶段真正有价值的工作是人工校准 M5/M6、Protection Agent 生成对照、轮换 SeedDream key 后的 4-call Smoke，以及完整 M9 Job API。

## 10. 可复现证据

关键不可变报告：

- Pilot：`runs/square-public-v2-pilot60-20260812/benchmarks/pilot60-agent-complete-v4/report.json`
- Held-out：`runs/square-public-v2-heldout240-20260812/benchmarks/heldout240-agent-complete-v2/report.json`
- Full300：`runs/full300-square-public-v2-20260812/benchmarks/full300-agent-complete-v2/report.json`
- Held-out strata：`runs/square-public-v2-heldout240-20260812/benchmarks/heldout240-strata-v1/strata.csv`
- 资源：`runs/square-public-v2-heldout240-20260812/benchmarks/heldout240-agent-resource-cost-v2/resource-costs.csv`
- 生成计划：`runs/.../generation-plans/*multiagent-generation-plan-v1/plan.json`
- 视觉抽审：`docs/reviews/square-public-v2-heldout240-codex-review.md`

复现聚合：

```powershell
.\.venv\Scripts\python.exe scripts\aggregate_benchmark_rounds.py `
  --spec configs\full300_benchmark_aggregation_v2.json `
  --output-dir runs\full300-square-public-v2-20260812\benchmarks `
  --report-id <new-id>
.\.venv\Scripts\ruff.exe check src tests scripts
.\.venv\Scripts\python.exe -m pytest -q
```

最终验证：Ruff 全通过；`142 passed in 26.41s`；Held-out Run audit `PASS`，候选预算 `960/960`、哈希/尺寸/transform `960/960`、共享分析和四方法 Task 组 `240/240`。没有 Commit、Push、PR、图片上传、SSH 写残留服务或付费 API 调用。

# 1:1 Public Pilot60 自动评测记录

> 日期：2026-08-12
> 状态：Pilot60 完整；held-out240 已于同日独立冻结并完成 Generation/Evaluation
> 校准状态：自动 Proxy 与模型判断均未用人工 A/B/C 标定

## 完整分母

- Dataset：`retarget_square_public_v2` Pilot split，60 张真实、公开、逐图审计图片。
- Target：60 个唯一 `1024x1024` Task。
- 场景：10/10/10/10/7/7/6。
- Aspect pressure：40 hard1 / 12 hard2 / 8 extreme。
- Generation Run：`square-public-v2-pilot60-20260812`，240/240 四方法候选成功。
- Evaluation Replay：`auto-proxy-v1p1-pilot60-20260812`，240/240 完成。
- 完整 Benchmark：`pilot60-agent-complete-v4`，拒绝任何缺 Task 的 arm；v2/v3/v4 依次增补 token 完整性、覆盖和精确 schema/cache count，旧报告均保留且不覆盖。

## 四种传统方法

| 方法 | Proxy 均分 | Proxy A | Proxy A/B | p50 | p95 | 总 CPU |
|---|---:|---:|---:|---:|---:|---:|
| direct_warp | 73.999 | 33.33% | 83.33% | 0.218s | 0.275s | 14.31s |
| crop | 72.112 | 20.00% | 80.00% | 0.232s | 0.309s | 14.61s |
| seam | 72.543 | 30.00% | 85.00% | 4.557s | 8.459s | 358.55s |
| mesh | 69.238 | 15.00% | 80.00% | 0.226s | 0.268s | 15.48s |

Codex 对 60 个 Task 的七类总览做了逐张非盲视觉抽审。结论仅作未校准证据：

- `direct_warp` 最稳定地保留完整内容，但宽图中的人物、建筑和商品会被横向压缩；
- `crop` 常有更自然的局部构图，但在多人、多商品和密集文字图中会丢边缘主体或文字；
- `seam` 偶尔兼顾覆盖范围，但慢约一个数量级，并会弯折脸、文字和结构线；
- `mesh` 很快，但主体、结构线和人脸的局部形变更常见；
- extreme 分层确实困难，不能用 hard1 的总体均值掩盖。

## Agent 与无 Agent

后验 Proxy Argmax 上界为 77.406；这是看完四个自动分数后的评测上限，不是在线可部署方法。Agent 输入包含自动指标，因此 Agent 结果必须同时报告到该上界的 regret，不能只和较弱规则基线比较。

| Policy | Calls | Schema | Proxy 均分 | A/B | Regret | E2E p50/p95 | 外部生成请求 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 无 Agent Generation selector | 0 | n/a | 74.456 | 81.67% | 2.950 | 0.219/0.276s | 0 |
| rules router | 0 | n/a | 76.040 | 90.00% | 1.365 | 0.230/4.759s | 3 |
| Qwen3-VL-4B always | 60 | 100% | **77.317** | **93.33%** | **0.089** | 6.091/12.539s | 4 |
| Qwen3-VL-4B conditional | 54 | 100% | **77.317** | **93.33%** | **0.089** | 5.987/12.539s | 4 |
| Qwen3-VL-8B always | 60 | 100% | 76.825 | 93.33% | 0.580 | 7.480/12.830s | 4 |
| Qwen3-VL-8B conditional | 54 | 100% | 76.825 | 93.33% | 0.580 | 7.400/12.830s | 4 |
| SmolVLM2 v2 always | 60 | 93.33% | 72.556 | 80.00% | 4.850 | 4.756/11.129s | 9 |
| SmolVLM2 v2 conditional | 54 | 92.59% | 73.152 | 80.00% | 4.254 | 4.473/10.703s | 9 |

Smol 的 4 个任务在两次独立 Run 中都无法生成合规结构化响应；policy 用冻结传统候选安全回退，所以 Task 分母仍是 60/60，但模型响应覆盖不是 100%。失败的 v1/v2 Run 均保留，没有用无限重试筛掉失败。

Conditional Replay 使用 always-on 的冻结响应缓存来保证判断一致；表中的 Agent latency 是生产中若实际调用模型的等价时延，不是本地缓存读取耗时。

`pilot60-agent-complete-v4` 同时冻结请求尝试数、精确 schema/cache count 和服务端 token 使用量。Qwen3-VL-4B always/conditional 分别为 72/65 次尝试、254,193/229,549 个完整观测 token；Qwen3-VL-8B 为 62/56 次尝试、218,716/197,602 个完整观测 token。SmolVLM2 的部分响应没有服务端 usage 字段，所以完整 token 总量保持 `null`，另用 observation coverage 字段报告已观测部分，避免把缺失误写成 0。

## GPU、能耗与基础设施成本

观测来自 gu27 单张 RTX 3090、约一秒间隔的 `nvidia-smi` 采样；能耗是数值积分，不是外接功率计。

| 模型 | 能耗覆盖 | Active GPU | Active Wh | 峰值显存 | 5 CNY/GPUh 场景 | 每 Task |
|---|---|---:|---:|---:|---:|---:|
| Qwen3-VL-4B | complete | 203.045s | 14.223Wh | 19,181MiB | 0.2820 CNY | 0.00470 CNY |
| Qwen3-VL-8B | complete | 274.053s | 22.144Wh | 19,747MiB | 0.3806 CNY | 0.00634 CNY |
| SmolVLM2 v2 | explicit_partial | 180.026s | 10.474Wh | 22,247MiB | 0.2500 CNY | 0.00417 CNY |

Smol 观测混合了 v1 完整回放和 v2 失败项重试，因此不得把该成本当成一次完整 v2 Run。完整场景费率保存在 `pilot60-agent-resource-cost-v3`，包含 1/2/5/10 CNY/GPU-hour 四档。

## 生成路由与预算

`pilot60-multiagent-generation-plan-v1` 合并 rules、Qwen4B、Qwen8B、Smol conditional 的唯一模型票：

- 10 个 Task 至少被一条路线请求生成；
- 4 个通过逐图 API egress 门禁并进入队列；
- 4 次单输出 SeedDream 预计 1.20--2.40 CNY，最坏仍远低于 100 CNY 总额度；
- 实际调用数为 0，实际供应商成本保持 `null`。

4 个可出域 Task 都是结构/建筑图。Codex 复核发现它们已有可理解、无明显主体缺失的传统候选；是否仍花费生成成本需要把“Agent 请求”与“最终质量/成本 veto”分开。当前更重要的硬阻塞是旧 SeedDream key 已泄露到工具日志并被视为失效，未获得轮换 key 前不得调用。

## 本地 AnyText2 与文字回贴

AnyText2 只做了一个公开、非敏感、单输出受控 Smoke，不外推为数据集结论：

- 1024²、30 steps、seed 2812；纯采样 13.88s，冷启动总 wall 58.81s；
- 峰值显存 11,373MiB；供应商成本 0；
- 5 CNY/GPU-hour 场景冷启动成本约 0.0816 CNY；
- 目标文字“大连冬聚”的 OCR 字符召回和序列相似度均为 0，视觉结果不合格。

全量 15 区文字回贴 v1 造成明显重叠和错位，判失败。定向单区、柔边整块覆盖 v2 耗时 0.0084s，目标字符召回和序列相似度均提升到 0.75，但仍有底层生成文字残片和可见拼接边界，因此仍不能进入生产路由。代码保留了可测试的 `foreground_alpha` 与 `opaque_patch` 两种合成模式，失败图片和指标只保存在 Git 忽略目录。

## 可复现命令

```powershell
.venv\Scripts\retarget-agent.exe audit runs\square-public-v2-pilot60-20260812
.venv\Scripts\retarget-agent.exe benchmark report runs\square-public-v2-pilot60-20260812 `
  --evaluation-id auto-proxy-v1p1-pilot60-20260812 `
  --benchmark-id <new-id> `
  --route-id <repeat-for-complete-arms>
.venv\Scripts\python.exe scripts\report_benchmark_strata.py --run-dir runs\square-public-v2-pilot60-20260812 `
  --evaluation-id auto-proxy-v1p1-pilot60-20260812 `
  --source-manifest datasets\retarget_square_public_v2\source_manifest.csv `
  --benchmark-id <new-id>
.venv\Scripts\python.exe scripts\report_resource_costs.py `
  --benchmark-report runs\square-public-v2-pilot60-20260812\benchmarks\pilot60-agent-complete-v4\report.json `
  --observation <arm-id=resource-observation.json> `
  --report-id <new-id>
```

## 当前边界

- 这些分数是自动路由 Proxy，不是人工 A/B/C，也不是独立感知质量真值。
- Pilot 用于选路线；最终结论采用同方法的 held-out240 完整分母与 Pilot+Held-out 的 Full300 聚合，不用 Pilot 单独外推。
- 真实 SeedDream 输出尚未产生；任何预计成本都不能写成实际成本。
- AnyText2 和文字回贴各只有一个技术 Smoke，不能按 60 张成功率报告。

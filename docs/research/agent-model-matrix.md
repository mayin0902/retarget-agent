# Retarget Agent 远程视觉 Agent 模型矩阵

访问日期：2026-08-11
状态：研究与执行建议；尚未下载模型、连接 SSH、启动推理或产生实测结果。

## 结论

本项目的视觉路由 Agent 应固定比较三种模型，而不是在试验过程中临时更换：

1. `Qwen/Qwen3-VL-4B-Instruct`：主候选。中文、OCR、商品和空间理解与本项目最匹配，
   BF16 单 24 GB 卡有充足余量。
2. `Qwen/Qwen3-VL-8B-Instruct`：同架构能力上界。BF16 权重约 16.33 GiB，单 24 GB 卡
   在单图、batch 1、短上下文和受控像素预算下可试，但必须以启动时峰值显存实测为准。
3. `HuggingFaceTB/SmolVLM2-2.2B-Instruct`：不同架构的低资源对照。官方称视频推理约
   5.2 GB GPU RAM，但官方语言标签为 English，因此它是速度/资源对照，不应预设为中文海报主路由器。

完整比较还必须保留两个无 VLM 对照臂：`no_agent_fixed_traditional` 和
`rules_only_router`。三种模型都先完整跑完 `pilot60`；只有在 60/60 完成、无持续 OOM、输出契约可用后，
才冻结版本、Prompt 和阈值并开始 `held-out240`。Round 1 一旦开始，不允许中途替换模型或只跑“看起来有利”
的图片。这样最终每个模型都有同一 300 张数据上的路由记录，共 **900 条模型路由记录**。

严格 JSON 不是模型卡承诺的模型原生保证。应由 vLLM structured outputs 的 JSON Schema 约束，
再由本地 Pydantic/JSON Schema 二次校验；失败重试也必须计入时延、成功率和资源指标。

## 已核实模型

| 实验角色 | 精确模型 ID 与建议冻结 revision | 架构 / 参数 | 官方许可证 | 官方仓库/权重信息 | 图像与语言能力 | 24 GB 单卡判断 |
|---|---|---|---|---|---|---|
| 主候选 | `Qwen/Qwen3-VL-4B-Instruct@ebb281ec70b05090aa6165b016eac8ec08e71b17` | Dense `Qwen3VLForConditionalGeneration`；4,437,815,808 参数 | Apache-2.0 | Hub API 报告 BF16、8,875,719,344 bytes 存储 | 单图/多图/视频/文本；Qwen 官方称 OCR 支持 32 种语言 | **稳妥**。BF16 权重下界约 8.27 GiB，尚需为视觉编码、KV cache、CUDA runtime 和激活留空间 |
| 能力上界 | `Qwen/Qwen3-VL-8B-Instruct@0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | Dense `Qwen3VLForConditionalGeneration`；8,767,123,696 参数 | Apache-2.0 | Hub API 报告 BF16、17,534,339,512 bytes 存储 | 与 4B 相同输入接口和官方 OCR/视觉能力声明 | **有条件可行**。BF16 权重下界约 16.33 GiB；必须 batch 1、单图、短上下文、限制输入像素，并做真实 OOM 预检 |
| 轻量异构对照 | `HuggingFaceTB/SmolVLM2-2.2B-Instruct@482adb537c021c86670beed01cd58990d01e72e4` | `SmolVLMForConditionalGeneration`；Idefics3 路线，SigLIP 图像编码器 + SmolLM2 解码器；2,246,784,880 参数 | Apache-2.0 | 模型卡宣称视频推理约 5.2 GB GPU RAM | 图片/多图/视频/文本；官方语言标签 English；官方 OCRBench 72.9 | **宽裕**。适合测低时延/低显存下限，但中文能力必须实测，不能由英文 benchmark 外推 |

参数量、revision、dtype 和存储字节来自 Hugging Face 官方 Hub API：
[Qwen 4B API](https://huggingface.co/api/models/Qwen/Qwen3-VL-4B-Instruct)、
[Qwen 8B API](https://huggingface.co/api/models/Qwen/Qwen3-VL-8B-Instruct)、
[SmolVLM2 API](https://huggingface.co/api/models/HuggingFaceTB/SmolVLM2-2.2B-Instruct)。
许可证、用途与模型说明分别见官方模型卡：
[Qwen 4B](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)、
[Qwen 8B](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct)、
[SmolVLM2 2.2B](https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct)。

上表的 GiB 权重值是 `参数量 × 2 bytes` 的工程下界换算，不是官方峰值显存承诺。实际峰值还受图片 token、
Prompt 长度、KV cache、attention backend、CUDA graph 和并发数影响。仓库磁盘体积不能直接当作显存峰值。

## 为什么选择 Instruct，而不是 Thinking 或社区量化版

路由任务要求短、稳定、可校验的决策，不需要长思维链。Qwen 官方同时提供 Instruct 和 Thinking 版本，
本矩阵只使用 Instruct，以减少输出 token、时延和解析分支。主比较使用官方 BF16 权重，避免把模型规模效应与
社区量化误差混在一起。

Qwen 也发布官方 FP8 checkpoint，但官方仓库给出的高效 FP8 vLLM 部署示例明确标注 H100+；当前目标硬件是
RTX 4090/3090。因此 FP8 只能在后端兼容性、输出一致性和指标回归通过后作为单独的 `quantization` 实验，
不得悄悄替代 8B BF16 主臂。[Qwen 官方部署说明](https://github.com/QwenLM/Qwen3-VL#deployment)

## 官方能力与版本边界

### Qwen3-VL

Qwen 官方仓库明确说明：

- Qwen3-VL 需要 `transformers>=4.57.0`；
- vLLM 需要 `vllm>=0.11.0` 才支持 Qwen3-VL；
- 新视觉处理路径使用 `qwen-vl-utils==0.0.14`，Qwen3-VL 的 `image_patch_size=16`；
- 图片支持本地路径、URL 和 base64；可用 `resized_height`/`resized_width` 或
  `min_pixels`/`max_pixels` 控制视觉输入；
- 官方推荐 FlashAttention 2 以提升速度并降低多图/视频时的显存占用；
- 官方称 OCR 覆盖 32 种语言，并改善模糊、倾斜、低光和长文档结构解析。

来源：[Qwen3-VL 官方 README：Quickstart、图像处理与 Deployment](https://github.com/QwenLM/Qwen3-VL/blob/main/README.md)。
Hugging Face 官方 Transformers 文档也列出图片张量与 `image_grid_thw` 输入：
[Qwen3-VL Transformers 文档](https://huggingface.co/docs/transformers/model_doc/qwen3_vl)。

模型配置的原生 256K 上下文不是消费级 24 GB 卡应采用的部署目标。Agent 路由只需要一张受控预览图、短 Prompt
和约 256 个输出 token；使用 256K 只会无意义地扩大 KV cache 和 OOM 风险。

### SmolVLM2

SmolVLM2 官方模型卡声明它支持图片、多图、视频与文本输入，许可证为 Apache-2.0，基于 Idefics3，
并给出约 5.2 GB GPU RAM 的视频推理声明。模型卡同时把语言标为 English，因此其中文海报结果只能作为实测值，
不能根据 OCRBench 或 TextVQA 分数推断。

模型卡未给出一个明确的 PyPI 数值最低版本，只要求最新 Transformers；官方发布博客使用
`v4.49.0-SmolVLM-2` 分支。为了不维护两套环境，本项目应让三个模型共用满足 Qwen 要求的
`transformers>=4.57.0`，并把最终实际解析版本写入 Run manifest。

来源：[SmolVLM2 官方模型卡](https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct)、
[Hugging Face 官方发布博客](https://huggingface.co/blog/smolvlm2)。vLLM 的版本化支持表已列出
`Qwen3VLForConditionalGeneration` 与 `SmolVLMForConditionalGeneration`：
[vLLM 0.11 supported models](https://docs.vllm.ai/en/v0.11.0/models/supported_models.html)。

## 结构化决策契约

Qwen 的官方 chat template 支持工具签名及 JSON arguments，但普通 `generate()` 并没有“必然符合任意 JSON Schema”
的官方保证。vLLM 官方 structured outputs 才提供 `choice`、`regex`、`json` 和 `grammar` 约束；其中 `json`
要求输出遵守提供的 JSON Schema。当前 API 使用 `structured_outputs`；旧 `guided_json` 字段在 v0.12.0 被移除。

来源：[vLLM Structured Outputs](https://docs.vllm.ai/en/v0.15.0/features/structured_outputs/)、
[vLLM 当前配置文档](https://docs.vllm.ai/en/stable/api/vllm/config/structured_outputs/)。

建议三种模型共用同一最小契约：

```json
{
  "route": "traditional|generative",
  "traditional_method": "crop|seam|warp|protect_then_crop",
  "needs_text_repaste": true,
  "risk_flags": ["text_loss", "subject_cut", "face_distortion", "logo_loss"],
  "confidence": 0.0,
  "reason_codes": ["enum_only"]
}
```

`reason_codes` 必须是冻结枚举，不接收自由文本作为评分输入。响应处理顺序固定为：schema 约束生成 → 本地验证 →
至多一次结构重试 → 失败时进入冻结的安全回退。必须记录原始响应、解析结果、重试次数、回退原因和最终 route。
模型自报 `confidence` 只用于校准，不能直接作为“质量分”。

## 统一的单 24 GB 配置

以下是待远端预检的工程建议，不是已执行命令或官方显存承诺：

| 配置项 | 冻结建议 | 原因 |
|---|---:|---|
| dtype | BF16；若某卡/后端不支持则整个对应硬件臂统一 FP16 | 保持质量比较，不把量化混入主实验 |
| 每请求图像 | 1 | 路由只分析当前 source |
| 并发 / `max_num_seqs` | 1 | 先保证 8B 在 24 GB 上完整跑完 |
| `max_model_len` | 4096 | 足够容纳约 1 MP 图片 token、短 Prompt 和 256 输出 token |
| Agent 预览像素上限 | 1,048,576 pixels；最小 65,536 | 三模型输入一致，避免默认超大图片使时延/显存不可控 |
| 输出上限 | 256 tokens | 路由是分类与短结构输出 |
| sampling | greedy / temperature 0；固定 seed | 降低重复运行方差 |
| `limit_mm_per_prompt` | image=1, video=0 | 禁止意外多图/视频占用 |
| CUDA graph | 首轮统一 eager；若三臂都稳定，再另做 graph 性能实验 | 降低 8B 启动显存风险，并保持比较一致 |
| 校验重试 | 最多 1 次 | 防止坏输出形成无限循环 |

Qwen 官方解释 `max_pixels` 是单图总像素预算，并建议按显存和场景限制输入；因此固定 1 MP 是项目工程选择，
不是官方最优值。[Qwen 图片像素控制说明](https://github.com/QwenLM/Qwen3-VL/blob/main/README.md#process-images)

8B 预检失败时按以下固定顺序处理，并在开始 Round 0 前完成：

1. 确认没有其他进程占用同卡；
2. 保持同一 BF16 权重，先使用 eager、batch 1、4096 context、1 MP；
3. 若仍 OOM，将**所有三个模型臂**的预览上限统一降到 786,432 pixels，再重做预检，避免只给 8B 更低清输入；
4. 若仍 OOM，统一降到 3072 context；
5. 仍失败则把 8B BF16 标记为 `preflight_unavailable_on_24gb`，不要在 Round 0 中途换社区量化版冒充同一实验臂。

## Round 0 / Round 1 部署矩阵

硬件信息 `gu28: 3×RTX 4090 24 GB`、`gu27: 2×RTX 3090 24 GB` 来自当前项目上下文，
尚未在本研究任务中通过 SSH 复核。

### Preflight（不进入质量统计）

用 7 个 scene category 各一张本地、可出域到远端的公开图片，对三个 endpoint 逐一验证：模型 revision、
依赖锁、单图输入、JSON Schema、固定 seed、峰值显存、无重试和一次故意触发的结构重试。任何模型未通过时，
先修配置或在 Round 0 开始前正式撤销该实验臂；不能开始后只跑一半。

### Round 0：冻结 `pilot60`

| 主机 / GPU | 服务或工作 | 输入数 | 产物与用途 |
|---|---|---:|---|
| `gu28:GPU0` | Qwen3-VL 4B BF16 Agent | 60 | 60 条路由、JSON 有效率、重试率、质量 regret、p50/p95 时延、峰值显存 |
| `gu28:GPU1` | Qwen3-VL 8B BF16 Agent | 60 | 同上；不得降低单独的图片清晰度获取显存优势 |
| `gu28:GPU2` | SmolVLM2 2.2B BF16 Agent | 60 | 同上；单列中文密集海报表现 |
| `gu27:GPU0` | 固定 4B 跨硬件性能复跑 | 60 | 与 4090 相同 revision/输入/Prompt；只比较 3090 vs 4090 时延和资源，不重复计入质量样本 |
| `gu27:GPU1` | 固定 8B 跨硬件性能复跑 | 60 | 同上；同时验证 8B 在另一类 24 GB 卡上的完整性 |
| CPU | no-agent 固定传统 + rules-only router | 60×2 | 无 VLM 对照；与模型 Agent 使用同一候选与指标 |

Round 0 的模型推理为 `3×60 + 2×60 = 300` 次，其中质量比较仍只有每模型 60 个独立 source/task，
不能把跨硬件复跑当作新增样本。Round 0 结束后冻结模型 revision、依赖 lock、Prompt hash、schema hash、
像素预算、路由阈值和 paid API 门禁。

### Round 1：冻结 `held-out240`

| 主机 / GPU | 服务或工作 | 输入数 | 产物与用途 |
|---|---|---:|---|
| `gu28:GPU0` | 冻结 Qwen3-VL 4B Agent | 240 | 与 pilot60 合并为完整 full300 |
| `gu28:GPU1` | 冻结 Qwen3-VL 8B Agent | 240 | 与 pilot60 合并为完整 full300 |
| `gu28:GPU2` | 冻结 SmolVLM2 2.2B Agent | 240 | 与 pilot60 合并为完整 full300 |
| `gu27:GPU0` | 确定性候选/自动质量指标 worker | 240 对应任务 | 不再重复 Agent 质量样本；释放 4090 只做路由 |
| `gu27:GPU1` | OCR、检测、AIGC 回贴与资源采样 worker | 240 对应任务 | 与 Agent endpoint 隔离，避免争抢显存污染 Agent 时延 |
| CPU | no-agent 固定传统 + rules-only router | 240×2 | 与 pilot 合并为两个完整 full300 对照臂 |

Round 1 三个模型产生 `3×240=720` 条新路由；与 Round 0 合计为 **3×300=900 条**。跨硬件性能
只在 Round 0 做全 60 复跑，避免为同一质量事实重复消耗 600 次推理。若需要 3090 的 held-out 时延，另建明确的
hardware benchmark，不混入主质量 Run。

## 防止多 Agent 把付费生图成本乘三

三种 Agent 必须完整跑 300 张路由，但不应让每个 Agent 独立重复调用相同的 SeedDream 生成请求。生成候选以
`source_sha256 + target + generation_model + prompt_hash + seed + generation_config_hash` 为缓存键；多个 Agent
路由到同一个生成配置时复用同一候选和实际账单记录。这样比较的是路由政策，而不是因为模型数量把 API 成本乘三。

如果某 Agent 路由到一个尚未生成且会突破冻结预算的样本，应记录 `budget_blocked` 并执行相同的传统安全回退，
不能静默删掉该任务。公开报告需要同时给出 route coverage、唯一生成请求数、缓存复用数、预算阻断数和端到端分数。

## Agent 指标与选型门禁

每个模型至少报告以下量化指标；不能以 Codex 主观审阅代替它们：

| 维度 | 指标 | 口径 |
|---|---|---|
| 完整性 | completion rate | 成功产生最终路由的 task / 300；必须保留失败和回退 |
| 契约 | first-pass / final JSON validity | 第一次即合法，以及一次重试后最终合法的比例 |
| 路由质量 | route regret | `同一 task 最佳可用候选分 - Agent 最终选择候选分`，越低越好 |
| 方法选择 | top-1 agreement / paired win rate | 与冻结指标 oracle 的方法一致率；相对 no-agent 的逐 task 胜率 |
| 生成门禁 | generation precision / recall / coverage | 以冻结的“传统失败且生成有收益”标签计算；无实际生成证据时不得声称 recall |
| 中文风险 | chinese_dense_poster 分层指标 | 单列 JSON、文字缺失风险判断和最终质量，不被英文场景均值掩盖 |
| 时延 | preprocess、prefill、decode、end-to-end p50/p95 | warm-up 与正式请求分开；重试计入端到端 |
| 效率 | images/s、tokens/s、GPU-seconds/task | 同一并发和同一输入像素预算 |
| 资源 | 峰值/均值 VRAM、GPU utilization、CPU RAM | 按 endpoint 和 GPU 型号分层，不混合 4090/3090 |
| 成本 | local GPU cost、paid API actual/estimated | 未知单价保持 unknown；不得伪造为 0 |

主 Agent 的选择顺序应是：先过 300/300 完整性和契约门禁，再比较 held-out240 的 route regret 与端到端质量，
最后用时延、显存和成本破同分。不能因为 4B 更快就忽略质量，也不能因为 8B 自报更高 confidence 就认为它更好。

## 建议锁定的实验臂

最终主报告使用以下五臂，名称和含义不可漂移：

1. `no_agent_fixed_traditional`：无 Agent，冻结的传统技术 Top-1。
2. `rules_only_router`：仅使用 OCR/人脸/商品/Logo/几何风险规则，不运行 VLM。
3. `agent_qwen3vl_4b`：Qwen3-VL 4B + 相同规则特征 + JSON Schema。
4. `agent_qwen3vl_8b`：Qwen3-VL 8B + 相同规则特征 + JSON Schema。
5. `agent_smolvlm2_2p2b`：SmolVLM2 + 相同规则特征 + JSON Schema。

“相同规则特征”意味着三种模型读取同一份 OCR/检测摘要和同一张 1 MP Agent preview；不能给某个模型额外标注。
Open Images evaluator-only annotations 也不得注入 Agent 输入。该矩阵能分开回答三个问题：Agent 是否优于无 Agent、
更大 Qwen 是否值得额外资源、异构轻量模型在速度收益下损失多少中文与复杂版式判断能力。

## 事实与推断边界

- 模型 ID、revision、参数量、dtype、许可证、配置、官方版本要求和公开 benchmark 是一手来源事实。
- “4B 稳妥、8B 有条件可行、Smol 宽裕”、1 MP/4096 配置以及 gu28/gu27 调度是工程推断，必须由远端
  preflight 和 Run telemetry 验证。
- 目前没有任何远端实测，因此本文不能作为“模型已部署”“单卡已通过”或“某 Agent 更好”的证据。
- 只有完成固定 60/240 split、保存版本/Prompt/schema/hash/telemetry，并对 full300 报告缺失任务后，
  才能形成正式比较结论。

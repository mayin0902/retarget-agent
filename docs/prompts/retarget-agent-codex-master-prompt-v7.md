# retarget-agent 快速实验版：三阶段增量 Grill、四候选重定向、条件式 Agent、外部 AIGC 与服务接口开发总提示词（V7）

> 使用方法：在 `G:\Projects\retarget-agent` 中打开本地 Codex，将本文从“提示词正文开始”到结尾一次性粘贴。首次粘贴后，后续上下文应主要从 `AGENTS.md`、`CONTEXT.md`、discovery、ADR、实验记录和 Git 历史延续，不要反复依赖聊天历史。

---

# 提示词正文开始

你当前位于项目根目录：

```text
G:\Projects\retarget-agent
```

项目名称：`retarget-agent`。

这是一个新的 Python 图片重定向实验平台仓库。你不能假设自己知道用户在其他目录做过什么，也不能把聊天之外的任何历史实现、实验数字或初步结论当作本仓库事实。本提示词会从零解释业务问题、重定向方法体系和 Agent 设计；你应据此快速检查仓库、记录必要假设，并连续实现一个小内核、插件化、可回放、可增量扩展的实验就绪 MVP。

你在本项目中的角色不是只负责写代码的执行器，而是：

1. 需求发现者；
2. 架构与数据契约设计者；
3. 对实验公平性和结论可靠性进行质疑的技术评审者；
4. 在本提示词授权范围内持续编码、测试并跑通 Smoke 的实现者；
5. 帮助用户建立可复现工程习惯的协作伙伴。

当前阶段以尽快得到真实实验结果为第一优先级。本提示词由用户粘贴并要求执行，即视为已经批准“实验就绪 MVP”：轻量 M0-M4 加 12 张 Smoke。执行方式不是取消需求审查，而是采用三阶段增量 Grill：开工前完成 Grill A 轻量预检，M2 四方法接入后完成 Grill B 自动契约审查，Smoke 后完成 Grill C 正式实验冻结。除真正阻塞项外，应连续编码、测试、生成四种真实候选、接通人工评审并运行 Smoke；不要在每个里程碑之间停下来等待重复批准。

只有以下事项仍需暂停询问：受保护素材是否可复制或出域、付费 API 真实调用、SSH 远端写操作或大规模资源占用、不可逆或破坏性操作、Commit/Push/PR，以及会改变四候选实验定义的重大决策。普通本地依赖安装、项目目录内代码修改、公开小型 fixture、CPU Smoke 和测试不应被无关开放问题阻塞。

---

## 一、用户背景与协作方式

请把以下信息作为你与用户协作时的长期背景，而不是产品需求字段：

1. 用户当前从事 AIGC 图片处理方向的实习，主力语言是 Python。
2. 用户具有 AIGC、多模态、计算机视觉、模型复现、科研和实验分析背景，已经接触或使用过 PyTorch、OpenCV、ComfyUI、FastAPI、LangGraph 等工具。
3. 用户的软件工程、Git、Windows 环境管理和大型项目架构经验相对有限。你不能只给出抽象建议，应在需要执行时提供可复制的 Windows PowerShell 命令，并解释命令目的、预期输出和常见失败点。
4. 用户希望先快速建立最小可运行闭环，再增量增加数据集、方法、评分器、人工指引、Agent、模型和服务接口，不希望一开始建设过重的平台。
5. 用户需要同时兼顾实习交付、算法效果验证和个人学习。因此：
   - 不要为了“架构完整”引入当前阶段用不到的复杂基础设施；
   - 但也不要把所有代码堆进一个脚本，导致后续无法接入新方法或新数据集；
   - 每个重要设计都要用清楚、直白的中文解释“为什么现在需要”“不做会怎样”“以后怎样扩展”。
6. 用户希望你主动指出冲突和风险，而不是无条件认同用户最初的想法。
7. 用户倾向以真实运行和人工看图结果判断能力。代码生成不等于完成，能导入不等于能运行，自动指标高不等于业务图片可用。

你输出时应避免：

- 一次抛出几十个没有优先级的问题；
- 使用大量未解释的架构术语；
- 把候选方案写成已经实现；
- 把旧项目或外部实验的状态自动继承为本仓库状态；
- 给出仅适用于 Linux、却没有 Windows 对应说明的操作步骤；
- 用占位实现、永远成功的 mock 或伪结果冒充里程碑完成。

---

## 二、实习业务背景与本仓库边界

### 2.1 更大的业务背景

用户所在实习方向研究面向公司素材货仓和不同流量场景的图片素材自适应处理能力。更大的业务愿景包括：

1. 开发者一次录入图片素材后，可适配多个展示区域和目标比例；
2. 对人物、商品、主体、中文文字、Logo、价格、按钮和角标等重要内容进行保护；
3. 在简单场景中尽量使用低成本、稳定、确定性的处理；
4. 在内置方法无法满足时，允许通过统一插件协议接入外部自定义方法；
5. 后续还可能探索基于商品/SPU 等信息生成图文素材，以及根据业务场景自动装修素材。

### 2.2 本仓库当前范围

`retarget-agent` 当前只聚焦于“图片重定向实验闭环”，不是一次性覆盖完整素材生成平台。当前重点是：

- 任意目标宽高和比例；
- 重要内容保护；
- 多方法候选生成；
- 候选冻结和离线回放；
- 自动检测、质量评分和路线选择；
- 人工评审与人工指引；
- 性能、资源、成本和错误记录；
- 条件式 Agent 与外部自定义方法的插件边界。
- 可由 CLI、Streamlit 和 FastAPI 共同调用的统一应用服务接口；
- Seedream 等外部 AIGC API 与用户自研 Python/ComfyUI 工作流的受控接入、评测和回退。

以下内容属于后续方向，不能在第一阶段自行扩大实现：

- 完整的 SPU 图文素材自动生成；
- 公司现网接入；
- 正式 Java 工程；
- 大规模分布式调度；
- 生产级权限、计费和多租户系统；
- 全量大数据集训练；
- 一开始就部署所有视觉模型或生成模型。

### 2.3 当前重要路线假设

当前要验证的主方案是：

```text
源图与目标尺寸
→ YOLO/OCR/显著性/结构分析形成一份共享保护信息
→ Direct Warp、Crop、Seam、Mesh 四种低成本方法全部生成候选
→ 硬检查、软评分与确定性排序
→ 结果明确时直接输出 Top-1 + 其余三张候选
→ 保护语义有歧义时按需调用 Protection Agent
→ 候选难分或需要判断是否回退时按需调用 Judge Agent
→ 四种传统候选均不可靠且通过费用、配额与素材出域门禁时，才进入外部 AIGC/自研工作流/人工处理回退
→ 通过统一应用服务返回 Top-1、全部备选、状态、评测和可追溯引用
```

文字检测框和 Logo 区域在本仓库中首先作为“必须保护的内容信息”参与裁剪、Seam 和 Mesh；文字提取、去字、重新排版与回贴不属于当前详细开发范围。必须预留通用的 `PostProcessor`、`ExternalAIGCProvider` 和 `WorkflowBackend` 边界，未来可以接入用户自己的重排、文字或生成式工作流，但不得让这些后续能力反向污染当前四候选核心协议。

首轮离线实验固定运行四种方法，Agent 不负责预先押注唯一方法，也不负责规划 Crop、Seam、Mesh 的算子组合。将来若真实性能数据证明四种全跑不适合生产，可以另行实验“先 Warp + Crop、再按规则补跑 Seam + Mesh”的确定性级联，但它不能替代四候选完整实验基线。

这只是当前高优先级方案，不是不可修改的最终架构。需求发现和实验若证明其他路线更优，可以通过 ADR 更新决策。

---

## 三、事实状态、设计前提与待解决问题

### 3.1 状态使用规则

所有内容必须使用以下状态之一：

- 【已确认】：需求或决策已经由用户明确确认；
- 【候选方案】：值得设计或实验，但尚未决定采用；
- 【待验证】：需要真实实验、数据或运行结果支持；
- 【已实现】：代码真实存在于明确的位置，但未必完成测试；
- 【已测试】：已经在明确环境、数据和版本下真实运行；
- 【未测试】：存在代码或配置，但没有可靠运行证据；
- 【已被替代】：旧结论或旧实现已由新版本取代；
- 【存在冲突】：不同要求或证据之间不一致，需要用户决策。

不得把【候选方案】写成【已确认】，不得把“用户提过一种方法”写成【已实现】，不得把“生成了代码”写成【已测试】。本提示词介绍的方法是目标设计空间；真实实现状态只能通过当前仓库文件、Git 历史和实际测试命令确认。

### 3.2 本项目需要解决的技术问题

1. 输入图片与目标画布可能存在很大的横竖比例差异，仅做等比缩放无法铺满画布，仅做普通裁剪又可能删除关键内容。
2. 图片可能包含单人肖像、多人物、单商品、多商品、中文海报、价格、Logo、按钮、角标、建筑直线和复杂背景。不同内容对“裁掉、压缩、拉伸、弯曲”的容忍度不同。
3. 不能只回答“哪里显著”，还要分别表示：
   - `ImportanceMap`：哪些像素、区域或对象必须优先保留；
   - `ToleranceMap`：哪些位置允许删除、压缩、拉伸或弯曲，以及允许程度。
4. 人脸、人体关键部位、精细商品结构、文字和 Logo 即使只受轻微破坏，也可能导致候选不可用；纯背景即使大幅删除，也可能完全可接受。
5. 因此，删除比例、缩放比例、网格位移等 `transform_log` 只是风险证据，不能直接当作最终质量结论。
6. 单一方法不可能覆盖所有场景。平台要生成若干互补候选，并让确定性规则、评分器、Agent 和人工评审在同一套冻结候选上进行公平比较。
7. Agent 的价值不是“再实现一次 Crop、Seam 或 Mesh”，也不是在生成前押注一个方法；它只在检测结果存在语义歧义时补充保护优先级，在四张候选难以自动排序时进行比较，并在传统候选都不可靠时判断应回退到外部 AIGC、人工复核还是返回失败。
8. 人工指引能够改变可行解空间，因此必须和完全自动模式分开运行、分开保存、分开统计。

### 3.3 当前仓库事实边界

1. 首次进入仓库时，先通过只读检查确认真实状态，不得依据本提示词推断已经实现了任何方法。
2. 不主动扫描或复制其他项目目录；需要迁移旧实现时，必须先由用户明确提供路径和授权范围。
3. 本提示词不提供历史实验分数，也不要求你复述历史结果。每个正式结论必须来自本仓库中可复现的数据集、配置、代码版本、候选产物和评审记录。

---

## 四、可用环境与资源假设

1. 个人开发端通常是 Windows，项目路径为 `G:\Projects\retarget-agent`。
2. 本地环境可能没有可用 GPU，因此 M0-M4 的基础闭环必须能在 CPU 环境开发和测试；GPU 功能应为可选能力，不能让无 GPU 环境连数据校验和人工评审都无法运行。
3. 用户有时可使用远程 GPU 节点，并可能获得 `2 × RTX 4090 24 GB`。具体节点、账号和可用性不能写死在公开配置中，应通过本地配置或环境变量接入。
4. 后续模型选型需要明确区分：
   - 单张 24 GB 是否可运行；
   - 双张 24 GB 是否需要模型并行；
   - 是否需要 CPU offload、量化、分块或降分辨率；
   - 冷启动时间、单图推理时间和峰值显存；
   - 权重许可和商用限制。
5. 任何外部 API 都可能涉及费用、配额、合规和素材出域风险。没有明确批准时，不得上传公司真实素材或调用付费 API。
6. GPU/NPU、Token 和 API 费用字段在早期可以为 nullable，但不得伪造为 0；未知应明确记为 unknown/null，并说明采集条件。

### 4.1 SSH 远程 GPU 开发与调试授权边界

本提示词明确允许 Codex 在进入 M7/M8 且按第 6.2 节取得远端写操作授权后，使用用户明确提供或本机已经配置的 SSH 主机别名连接远程 GPU，部署并调试真实的 Protection/Judge 模型、自研工作流和模型服务。该授权不等于允许任意修改远端系统，也不等于产品 Agent 可以获得 Shell 权限。

首次连接某个节点时，Codex 应先进行只读检查并向用户报告：

- 主机别名和操作系统；
- `nvidia-smi` 可见 GPU 型号、数量、显存和当前占用；
- CUDA/驱动、Python、Conda/venv、磁盘空间；
- 项目目录、已有环境、已有模型缓存；
- 当前其他用户或任务占用情况；
- Git、网络与模型下载是否可用。

远程操作必须遵守：

1. 只使用用户明确提供或本机已配置的 SSH alias，不猜测 IP、账号、端口或密码。
2. 不在命令、配置、日志或 Git 中写入账号、IP、私钥、Token、Cookie 和 API Key。
3. 未经明确批准，不修改系统级 CUDA/驱动，不全局安装依赖，不停止其他用户进程，不删除共享缓存。
4. 使用独立项目目录和独立 Conda/venv；依赖与启动命令必须可复现。
5. 先检查空闲 GPU，再选择单卡、双卡、量化、offload 或缩略图输入方案；不得假设 `2 × 4090` 始终空闲。
6. 长任务应支持断开 SSH 后继续、日志持续落盘、失败可恢复；不得只依赖一个前台终端。
7. 远程实验结果同步回本地时，只同步代码、配置、脱敏日志、指标和允许保存的公开测试产物。
8. 公司真实素材不得上传到个人或未经授权的 GPU 节点；远程调试使用公开集、程序化 fixture、脱敏集或获准数据。
9. SSH 只用于开发、部署、诊断和基准测试；正式运行时 Agent/Workflow 应暴露受控 Python 或 HTTP 接口，不允许产品模型执行 Shell。
10. 每次基准必须保存节点别名的脱敏标识、GPU/驱动/CUDA、环境锁、模型版本、启动参数、Git commit、输入规格和结果。

### 4.2 远程 Agent 调试顺序

真实模型接入建议按以下顺序执行，并分别标记【已实现】与【已测试】：

1. 本地使用固定 JSON fixture 验证 `AgentPlugin` schema、超时和降级；
2. 远程启动真实多模态模型服务，先用公开小图验证健康检查和结构化输出；
3. 通过本地到远程的受控 HTTP 连接或 SSH 端口转发调试，不把 Shell 暴露给产品 Agent；
4. 分别测试 Protection Prompt 和 Judge Prompt；首版可共享一个模型服务，但调用记录和 Prompt 版本必须独立；
5. 对同一冻结输入比较无 Agent、4B、8B、条件式和 Always-on；
6. 测量冷/热启动、模型加载、首 Token/首响应、完整推理、峰值显存、失败率和结构化输出合法率；
7. 断开连接、超时或远程服务不可用时，验证确定性 Hard Ranker/人工复核降级。

远程部署和调试不是 M0-M4 的前置条件；没有 GPU 时，数据、CLI、评审和 Replay 基础闭环仍须可运行。

---

## 五、仓库级技能与快速启动原则

按以下顺序执行，但技能配置不得无故阻塞实验：

1. 检查仓库根目录、Git 状态、当前分支、已有文件、`AGENTS.md` 和 `.agents/skills/`。
2. 若 `$setup-matt-pocock-skills` 已安装且可用，读取其真实 `SKILL.md` 后完成最小工程配置；若未安装、名称不同或执行失败，记录原因并采用普通 Codex 工作流继续，不为此暂停 M0-M4。
3. 无论是否安装专用技能，都必须执行第 7.2 节定义的 Grill A/B/C。若 `$grill-with-docs`、`grilling`、`domain-modeling` 已安装，可用于维护术语、决策和 ADR；若未安装则用普通检查、测试和 Markdown 文档完成同等产物，不能跳过 Grill，也不能因技能缺失阻塞编码或 Smoke。
4. Issue tracker 默认选择 GitHub；项目采用精简 single-context 布局：根目录 `CONTEXT.md`，以及按需创建的 `docs/adr/`、`docs/discovery/`。
5. 使用根目录 `AGENTS.md` 保存长期工程约束，但不要先写大篇文档再实现算法。

如果技能名称、目录或调用方式与预期不同，应读取实际说明并如实记录，不得假装已经运行；只要不影响数据安全、四方法定义和实验可复现性，就使用可用替代流程继续推进。

---

## 六、快速实验授权与暂停门禁

### 6.1 已授权范围

用户粘贴本提示词并要求 Codex 执行，即视为一次性批准：

```text
批准实验就绪MVP：连续完成轻量M0-M4并运行12张Smoke；无阻塞时不要逐阶段等待确认
```

Codex可以在项目目录内连续完成：

- 创建或修改 Python 源码、配置、测试、CLI、Streamlit MVP 和必要文档；
- 安装 M0-M4 所需的普通 Python 依赖；
- 建立文件夹/CSV 数据集适配、统一插件协议和可回放产物结构；
- 接入并真实运行 `direct_warp / crop / seam / mesh`；
- 使用公开小型 fixture、用户明确指定的本地非敏感图片或程序化图片；
- 运行单元测试、集成测试、回归测试和 12 张 Smoke；
- 修复 Smoke 暴露的问题，直到达到实验就绪验收标准；
- Smoke 通过后准备 36 张第一轮正式实验的配置、命令和检查清单。

M0、M1、M2、M3、M4 之间不需要再次请求批准。每完成一个阶段应记录状态和测试证据，但应继续推进下一阶段。

### 6.2 仍需暂停询问的事项

只有遇到以下情况才暂停：

- 数据范围、保护级别或许可证不明，继续操作可能复制、覆盖或外传受保护素材；
- 需要真实调用付费 API、消耗配额或把图片发送到外部服务；
- 需要首次进行 SSH 远端写操作、安装环境、占用 GPU 或传输数据；
- 需要修改系统级 CUDA/驱动、结束他人进程、删除或覆盖重要数据；
- 需要 Commit、Push、创建 PR、发布 Tag 或执行其他外部写操作；
- 需要改变固定四候选、A/B/C 口径、数据划分或正式实验预算等核心定义；
- 缺失的信息会造成不可逆的数据契约或使实验失去可比性。

非阻塞问题使用明确默认值，登记为【待验证】，继续实施。不得因为 Agent 模型、Seedream、ComfyUI、FastAPI、完整 OCR/显著性模型或未来生产架构尚未确定而阻塞首轮四方法实验。

### 6.3 速度纪律

- 首次执行 Grill A 短预检，最多提出 0～3 个真正阻塞问题；没有阻塞问题就直接编码。
- 不开展九轮串行、逐轮等待回复的前置 Grill；必须执行第 7.2 节的三阶段增量 Grill。
- Grill A 和 Grill B 默认由 Codex 连续完成；Grill C 是进入 36 张正式实验前唯一必须通过的 Grill 门禁。
- Grill 检查与代码、测试和 Smoke 相互提供证据，不把能够通过安全默认值解决的问题改造成等待用户回复的门禁。
- 不先建设 MLflow、DVC、OpenTelemetry、消息队列、Kubernetes、PostgreSQL 或完整微服务。
- 不用占位候选冒充真实方法；可以简化工程外围，但四种候选必须是真实可运行实现。
- 不要求 M5-M9 完成后才做实验；Smoke 通过后立即执行轻量 Grill C，冻结口径后进入 36 张第一轮正式基线。
- 每次遇到选择，优先采用“可回放、可替换、今天能跑”的最小实现。

---

## 七、需求发现的工作方式

### 7.1 提问规则

使用中文提问，但把问题分为“阻塞实验”和“可后补”两类。首次预检最多提出 0～3 个真正阻塞轻量 M0-M4 或 Smoke 的问题；可采用安全默认值的问题直接登记后继续做，不要一次问几十个问题。

已经在本提示词中标为【已确认】且不存在冲突的内容，不要换一种说法重复询问。你可以：

- 简要复述并登记为已确认；
- 指出它与其他要求的冲突；
- 询问实现边界或验收阈值；
- 提出更小的默认实现。

每个真正需要用户回答的问题应简短包含：

1. 问题编号；
2. 需要用户决定什么；
3. 为什么该决定影响架构、效果、成本、实验公平性或里程碑；
4. 2～4 个互斥选项；
5. 你的推荐选项及理由；
6. 如果暂时不决定，可采用的默认值；
7. 当前状态：【待确认】、【待验证】或【存在冲突】。

### 7.2 三阶段增量 Grill 协议

不开展九轮前置拷问。Grill 是必须执行的工程与实验审查，但分散到最能获得真实证据的三个检查点。每次 Grill 只处理当前阶段会改变正确性或实验可比性的问题，不提前讨论尚未进入里程碑的全部细节。

每个 Grill 的结论只能是：

- `PASS`：当前阶段可继续；
- `PASS_WITH_OPEN_ITEMS`：存在不影响当前阶段正确性和可比性的【待验证】项，登记后继续；
- `BLOCKED`：继续会造成数据风险、四方法定义错误、系统性假实现、不可回放或正式实验失去可比性，必须暂停并提出至多 3 个聚合问题。

#### Grill A：开工前轻量预检

**时机**：首次进入仓库后、M0 编码前。

**目标**：防止在错误仓库、错误数据、错误方法来源或不安全素材上开工；不负责一次性确定完整生产架构。

**必须检查**：

1. 仓库、分支、未提交修改、已有代码、测试和文档的真实状态；
2. Warp、Crop、Seam、Mesh 和评审 UI 的实际来源、许可证、可复用程度与测试证据；
3. Smoke 输入、输出、12 张图片来源、两个目标比例和数据安全边界；
4. Python 版本、CPU 可运行性、依赖安装方式和基础启动命令；
5. 四固定候选、共享分析、A/B/C/Skip、产物落盘和失败隔离的最小默认定义；
6. 现有要求之间是否存在会立即导致返工的冲突。

**产物**：`docs/discovery/grill-a-preflight.md`，至少记录仓库事实、已确认项、默认值、风险、开放项、至多 3 个阻塞问题和结论状态。

**推进规则**：若为 `PASS` 或 `PASS_WITH_OPEN_ITEMS`，立即连续实施 M0-M2，不等待用户再次批准；只有命中第 6.2 节或无法确定四方法真实来源、数据安全与输入输出时才可标记 `BLOCKED`。

#### Grill B：M2 后自动契约审查

**时机**：四方法已接入并能在 2～3 张程序化 fixture 上运行后，进入完整 M3/M4 与 12 张 Smoke 前。

**目标**：防止“代码能跑”被误当成“四候选实验已经成立”。这一步主要依赖代码检查和自动测试，不要求用户逐项审批。

**必须检查**：

1. `direct_warp / crop / seam / mesh` 都是真实实现，不是复制图、占位图、永远成功的 mock 或改名后的同一方法；
2. 四方法使用同一版本 `AnalysisArtifact`、同一 Task、同一输出尺寸契约和可解释的公平候选预算；
3. 每种方法保存稳定 method ID、参数、输入引用、transform log、错误状态、阶段时延和版本信息；
4. 单方法失败不阻塞其他方法，失败不会伪装成功；
5. 输出尺寸、坐标变换、缓存键、重复运行、断点恢复和配置哈希有自动测试；
6. Protection 信息、领域对象、Provider/Workflow 预留边界没有侵入或改变四候选核心语义；
7. CLI、Runner、存储和后续 UI 使用同一数据契约，不存在三套不兼容逻辑；
8. 关键简化和已知算法限制已明确标为【候选方案】或【待验证】。

**产物**：`docs/discovery/grill-b-contract-audit.md` 加相应单元、契约或集成测试证据，列出每项 `PASS/FAIL/OPEN`、修复记录和总状态。

**推进规则**：发现局部问题时直接修复并复跑审查；`PASS` 或不影响 Smoke 可解释性的 `PASS_WITH_OPEN_ITEMS` 后继续 M3-M4 和 Smoke。若某方法系统性不可运行、方法语义错误或契约无法公平比较，则标记 `BLOCKED`，M2 不得宣称完成，也不得跳过该方法进入正式四方法实验。

#### Grill C：Smoke 后正式实验冻结

**时机**：12 张 Smoke 已生成、评审链路和统计已验证后，启动 36 张第一轮正式基线前。

**目标**：把 Smoke 暴露的问题转化为固定的正式实验定义，避免跑完 288 个候选后才发现数据、参数或评分口径变化。

**必须检查并冻结**：

1. `retarget_baseline36_v1` 的 source-level manifest、split、哈希、许可证/安全状态和排除规则；
2. 每张源图的两个目标比例、任务 ID 和生成预算；
3. 四方法代码版本、配置、共享分析版本、随机种子策略和依赖环境；
4. A/B/C/Skip 的可操作定义、失败原因字典、最佳候选规则和 Skip 分母规则；
5. UI 版本、方法名显示、候选展示顺序或随机化记录、评审者与断点恢复方式；
6. 第一轮必须报告的各方法 A、A+B、C、Skip、技术成功率、Any-method/Oracle、失败原因、P50/P95 和峰值内存；
7. Smoke 中的系统性失败是否已修复，残余问题是否只影响个别 Task 且有明确处理规则；
8. 正式 Run ID、输出目录、只追加/不覆盖策略、启动命令和复现清单。

**产物**：`docs/discovery/grill-c-experiment-freeze.md`、冻结的 dataset/config manifest 及实验就绪报告。冻结后如需改变图片、任务、目标比例、方法实现、参数或评分口径，必须创建新版本或新 Run，不得静默覆盖。

**推进规则**：Grill C 是进入 36 张正式实验前的必要门禁，但不等于强制等待一轮形式化回复。若所有核心项已有明确答案且证据通过，Codex 可记录 `PASS` 后直接启动正式实验；若存在会改变正式统计的歧义、数据未冻结、四方法系统性失败或评分口径冲突，必须标记 `BLOCKED`，集中提出至多 3 个问题。非核心开放项可以 `PASS_WITH_OPEN_ITEMS`，但必须说明为何不影响本轮公平比较。

### 7.3 后续增量需求发现顺序

1. 准备 M5-M6 时再确认自动排序阈值和人工指引；
2. 准备 M7 时再确认 Protection/Judge Agent、候选模型、SSH、成本和安全降级；
3. 准备 M8-M9 时再确认 Seedream、ComfyUI、自研 Workflow、FastAPI、付费、出域和接口策略。

需求发现文档持续更新，但不得成为运行四方法 Smoke 的串行前置工作。Agent、SSH、Seedream、ComfyUI、自研工作流和 FastAPI 不属于 Grill A-C 的首轮实验通过条件。

### 7.4 必须主动挑战的内容

不要只顺从用户表述。至少检查：

- 目标是否自相矛盾；
- MVP是否过大；
- 插件接口是否为了未来而过度抽象；
- 指标能否真实反映业务效果；
- 是否把“启用的方法中任一达到 A”与“系统 Top-1 达到 A”混为一谈；
- 数据是否可能泄漏；
- 数据集许可证是否允许下载、缓存、商用和再分发；
- 同一源图的不同目标尺寸是否发生训练/验证/测试泄漏；
- 内置方法、Agent 路由和外部方法的比较是否采用可解释且公平的任务与评审口径；
- 人工指引是否污染完全自动实验；
- 评审显示方法名是否造成偏差，以及是否需要记录显示顺序或提供可选盲评模式；
- transform log 是否被错误当成最终质量；
- 自动评价是否过度偏好删除少、纯色背景或低形变；
- 性能、资源和成本指标能否在不同机器复现；
- 公司电脑只测试、不开发的流程是否真正可执行；
- 任何准备接入的外部实现、数据和统计是否具备明确来源与可复现条件；
- FastAPI、CLI 和 Streamlit 是否真正调用同一应用服务，而不是三套业务逻辑；
- 外部 API 技术成功是否被误写成图片质量成功；
- Seedream/ComfyUI 重试是否可能重复生成、重复计费或覆盖产物；
- 客户端是否能通过路径、Provider 名、费用或出域字段绕过服务端策略；
- 自研工作流是否保存模板、节点绑定、模型、custom nodes 和产物血缘；
- 是否有人脸、文字或 Logo 的“一票否决”规则需要单独定义；
- 是否需要将输入图、目标比例、方法版本、随机种子和依赖锁定才能重放。

### 7.5 每个实现检查点的输出

每完成 M0、M1、M2、M3、M4 或一次实验运行后，简要输出并写入文档：

- 本轮新增确认；
- 本轮新增待验证；
- 本轮仍开放的问题；
- 发现的冲突；
- 对架构或里程碑的影响；
- 下一步准备实现或验证的内容；
- 本轮修改了哪些文档。

状态更新后应继续执行下一步；除非命中第六节暂停门禁，不要把检查点更新当成等待用户批准的理由。

---

## 八、项目总体目标

目标是建设一个小内核、插件化、可回放、可审计的图片重定向实验平台，用于：

1. 接入不同图片数据集和任意目标尺寸；
2. 让一张源图对应多个目标尺寸任务；
3. 对每个 Task 批量运行 Direct Warp、Crop、Seam、Mesh 四种低成本重定向方法；
4. 保存 Top-1 和全部候选；
5. 保存候选图片、分析结果、Mask、transform log、配置快照、版本、随机种子、性能、费用、错误和重试；
6. 支持人工 A/B/C/Skip 评审；
7. 支持人工框选保护区域、优先保留区域、允许删除区域和目标锚点；
8. 支持添加、删除和条件调用不同 Agent；
9. 支持用已经冻结的候选重放新的硬规则、评分器、排序器、成本模型和 Agent；
10. 支持未来通过同一 `CandidateMethod` 协议接入用户自己的外部重定向方法；
11. 支持公司电脑只下载稳定版本并接入新的本地图片集，无须修改 Python 源代码；
12. 通过统一应用服务供 CLI、Streamlit、FastAPI 和未来公司调用方复用，不把业务逻辑写死在任何界面；
13. 支持 Seedream 等外部 AIGC API，以及用户自研 Python/ComfyUI/远程 HTTP 工作流，在统一权限、版本、错误、性能、成本和质量协议下接入；
14. 让每项实验能够回答：哪个方法适合什么场景、成功率如何、为什么失败、耗时和成本是多少、Top-1 路由比 Oracle 差多少。

第一阶段统一使用 Python，不建立 Java 工程。FastAPI 是协议稳定后的必需服务接口交付，但不是轻量 M0-M4、Smoke 或第一轮正式四方法实验的前置条件；CLI、Streamlit 和 FastAPI 最终必须复用同一个 `RetargetApplicationService`。

---

## 九、已经确认的业务原则

以下内容视为当前有效约束；如果发现技术冲突，应标记并在最近的 Grill A/B/C 检查点提出，而不是静默修改。

1. 默认返回 Top-1 加全部备选。
2. A 为高质量；B 算业务成功，但系统应尽量提高 A 率，不能依靠大量 B 抬高成功率；C 为失败；Skip 不进入评分分母。
3. “启用的方法中任一方法达到 A”表示候选集合/Any-method/Oracle 达到 A，不等于系统自动选择的 Top-1 达到 A。二者必须分别报告。
4. 人物肖像、精细商品、Logo 等细节场景使用 Precision 倾向。
5. 多人物、中文海报、电商宣传页等复杂场景优先保证重要内容覆盖，使用 Coverage 倾向。
6. 普通单主体、风景和一般商品使用 Balanced 策略。
7. 场景策略影响权重和路由，但不能通过更换评分标准人为美化某种方法。
8. transform log 只是风险证据，不等于失败结论。
9. 大幅删除纯背景可以通过；轻微破坏人脸、核心文字、商品关键结构或 Logo 可能直接失败。
10. 需要区分 ImportanceMap 与 ToleranceMap：前者描述保留优先级，后者描述可删除、可变形和不可变形程度。
11. 人工评审与人工指引必须分开统计。
12. 有人工指引的结果不得混入完全自动成功率。
13. 训练、验证、测试必须按 `source_id` 分组；同一源图的不同目标尺寸和不同方法不得拆到不同集合。
14. 方法失败必须记录，但一种方法失败不能阻塞同一任务的其他方法。
15. 自动指标不能代替人工评价；人工评价也不能替代可复现的检测、性能和成本记录。
16. 公司真实素材、内部地址、Token、Cookie、内部接口和含公司素材的运行结果不得进入 GitHub。
17. 新路线进入正式方案前，应记录适用场景、输入输出、优势、失败案例、资源成本、实现难度、实际评测、接入方式和当前状态。

---

## 十、建议的最小技术骨架

以下是候选骨架。轻量 M0-M4 可直接按最小实现落地，并在 Grill A、Grill B 与 Smoke 过程中修正；不需要等待所有长期需求讨论结束：

- Python 3.11；
- Pydantic 数据契约；
- YAML 实验配置；
- SQLite 保存追加式事件、人工评审、决策和 Agent 调用记录；
- 普通文件目录保存原图引用、候选、Mask、分析产物和可视化；
- Typer 或 argparse 提供 CLI；
- Streamlit 提供 MVP 人工审图与矩形指引；
- pytest 进行契约、单元、集成和回归测试；
- Pillow、OpenCV、NumPy 实现初始确定性方法；
- psutil 记录 CPU 时间和内存；
- GPU 存在时可选记录峰值显存、设备信息和同步后的推理耗时；
- 通过配置快照、依赖版本、Git commit 和输入哈希保证可复现；
- 暂不引入 LangGraph、消息队列、Kubernetes、PostgreSQL 和完整 OpenTelemetry；
- FastAPI 在 CLI 和数据协议稳定后接入，并作为后续必需的服务接口交付；
- 外部厂商 API 使用 Provider Adapter，不把请求字段、鉴权、轮询和计费逻辑散落在 Runner 中；
- 用户自研 Python/ComfyUI/远程模型服务使用 WorkflowBackend Adapter，不让工作流节点细节进入领域对象。

核心业务代码不得写在 Streamlit 页面中。CLI、Streamlit 和未来 FastAPI 必须调用同一个应用层。

SQLite 主要保存结构化事件和索引，不要把大图片二进制直接塞进 SQLite。图片、Mask 和可视化使用文件存储，并在记录中保存相对路径、哈希和媒体信息。

---

## 十一、必须保留的插件边界

主 Runner 只能依赖协议，不直接写死具体模型、数据集或算法。

至少设计：

- `DatasetAdapter`：把不同来源转成统一任务；
- `Analyzer`：主体、文字、Logo、显著性、结构线、场景类型等分析；
- `CandidateMethod`：生成一个或多个候选；
- `Evaluator`：计算硬约束、质量、风险、性能和成本指标；
- `SelectorPolicy`：根据候选和策略选择 Top-1；
- `AgentPlugin`：在受控插入点进行理解、复核或路由；
- `ArtifactStore`：保存候选、Mask、可视化和配置快照；
- `EventStore`：保存运行、评审、决策和追加事件；
- `InstrumentationHook`：采集阶段时延、资源、错误与重试。
- `RetargetApplicationService`：向 CLI、Streamlit 和 FastAPI 暴露统一用例；
- `ExternalAIGCProvider`：适配 Seedream 等厂商生成 API 的提交、轮询、取回、费用与错误；
- `WorkflowBackend`：适配本地 Python、ComfyUI HTTP 和用户自研远程 HTTP 工作流；
- `JobStore`：保存异步任务状态、幂等键和结果引用，首版可以复用 SQLite/EventStore。

在 Grill B 的契约审查中还需要判断是否应独立设计：

- `FallbackPolicy`；
- `MetricRegistry`；
- `ModelProvider`：Agent 模型的本地/远程推理服务抽象；
- `PostProcessor`：仅作为未来接入用户自定义后处理的边界；
- `CachePolicy`。

不要为了接口数量好看而拆分。只有生命周期、数据边界或替换频率确实不同，才建立独立协议。

新增数据集不得修改 Runner。

新增外部厂商或自研工作流同样不得修改 Runner 或 FastAPI endpoint；只能新增 Provider/Backend Adapter、注册实现并添加私有配置。Seedream 是首个建议验证的 `ExternalAIGCProvider`，不是写死在核心领域模型中的唯一服务。

新增 Direct Warp、Crop、Seam、Mesh 的实现版本或外部方法时，不得修改 Runner 主控制流，只能：

1. 新增插件实现；
2. 注册插件；
3. 在 YAML 中启用；
4. 必要时增加该插件自己的参数 schema。

增删 Agent 应尽量只改配置。

Agent 首版只保留三个受控职责点：

- `protection_resolution`：确定性 Analyzer 完成后，对疑难主体、商品、文字和可牺牲背景做语义优先级消歧；
- `candidate_judging`：四种候选完成硬检查与软评分后，在难分候选之间进行排序；
- `fallback_decision`：传统候选均不可靠或指标—视觉冲突时，判断外部 AIGC、人工复核或失败回退。

Agent 是否调用由确定性触发策略、SelectorPolicy 或 FallbackPolicy 决定。Agent 不得无约束接管整个流水线，必须有：

- 明确输入和输出 schema；
- 超时；
- 解析失败处理；
- 费用和时延记录；
- 不可用时的确定性降级；
- 是否改变 Top-1 的审计记录。

---

## 十二、Generation、Evaluation Replay 与 Human Review 必须分开

### 12.1 Generation Run

负责：

- 读取 `TaskSpec`；
- 加载并校验源图；
- 运行确定性 Analyzer 分析原图；
- 在检测/显著性/OCR 存在语义歧义时，按配置调用 Protection Agent；
- 冻结带版本和来源的 `AnalysisArtifact`；
- 读取可选人工指引；
- 标准模式固定调用 Direct Warp、Crop、Seam、Mesh 四种方法生成候选；
- 冻结候选图片；
- 保存随机种子、算法版本、模型版本、配置和 transform log；
- 保存阶段性能、错误和重试；
- 不因单个方法失败而终止整个任务。

### 12.2 Evaluation Replay

直接读取被冻结候选，反复运行：

- 新的硬规则；
- 新的质量指标；
- 新的排序器；
- LightGBM/XGBoost 等学习式排序；
- Judge Agent；
- Agent 触发阈值；
- FallbackPolicy 与 Unnecessary AIGC 判定；
- 新的成本模型；
- 新的 A/B/C 映射；
- 新的报告口径。

除非候选生成算法、输入、人工指引或随机种子发生改变，否则 Evaluation Replay 不得重新生成候选。

### 12.3 Human Review

人工评审是对冻结候选或冻结 Decision 的追加式评价事件，不应修改候选图片本身。人工评审至少记录：

- reviewer_id 或匿名本地标识；
- task_id、candidate_id、method_id；
- A/B/C/Skip；
- 最佳候选；
- 失败原因；
- 显示顺序；
- 是否显示方法名；
- 评审时间；
- supersedes_event_id；
- 软件版本和评分规范版本。

---

## 十三、第一版领域对象

请在 Grill B 的契约审查中检查字段和所有权边界，至少包括：

- `DatasetDescriptor`；
- `SourceRecord`；
- `TargetSpec`；
- `TaskSpec`；
- `AnalysisArtifact`；
- `HumanGuidance`；
- `CandidateRecord`；
- `TransformRecord`；
- `MetricBundle`；
- `DecisionRecord`；
- `ReviewEvent`；
- `StageEvent`；
- `ProtectionDecision`；
- `AgentDecision`；
- `FallbackDecision`；
- `AgentCallRecord`；
- `RunManifest`；
- `ReplayManifest`；
- `ExternalCallRecord`；
- `WorkflowInvocationRecord`；
- `ServiceJobRecord`；
- `QualityDimensionRecord`；
- `ProviderCapability`。

至少明确以下标识之间的关系：

```text
dataset_id
  └─ source_id
      └─ task_id = source_id + target_id
          └─ candidate_id = task_id + method/version/run信息
              ├─ metric记录
              ├─ decision引用
              └─ review事件
```

`ReviewEvent` 采用追加式事件，不覆盖旧评分。修改评分时新增事件，并用 `supersedes_event_id` 关联旧事件。

`CandidateRecord` 至少需要考虑：

- candidate_id；
- task_id；
- method_id 和 method_version；
- run_id；
- 输入与输出哈希；
- 输出相对路径；
- 宽高和格式；
- seed；
- 配置快照引用；
- transform log 引用；
- generation_status；
- failure_type 和脱敏错误摘要；
- 是否使用人工指引；
- 是否调用外部 API；
- 生成阶段性能。

`AgentCallRecord` 至少保存：

- agent_id 和版本；
- 插入点；
- 模型/服务版本；
- prompt 版本；
- 输入摘要或哈希；
- 原始响应；
- 解析后 JSON；
- 调用是否成功；
- 错误类型；
- 时延；
- Token；
- 估算费用；
- 是否改变最终 Top-1；
- 失败后采用的降级策略。

原始响应可能包含敏感信息时，需要可配置的脱敏和不落盘策略。

`ExternalCallRecord / WorkflowInvocationRecord` 至少保存：

- provider/backend ID、版本和 capability 版本；
- task、candidate、job 和调用链 ID；
- 输入图片、Mask、Prompt/工作流模板和参数哈希；
- 提交、排队、推理、轮询、下载、后处理和总时延；
- 请求次数、重试、超时、供应商状态码和归一化错误类型；
- seed、输出数量、输出哈希和供应商返回 ID 的脱敏引用；
- 输入/输出计费单位、估算费用、实际费用、币种和账单来源；
- 素材是否出域、所使用的合规策略和授权结果；
- 技术调用是否成功、图像是否可解码、业务质量是否达到 A/B；
- 缓存、幂等键和是否发生重复计费。

技术调用成功与业务图片成功必须分开：HTTP 200、任务完成或图片成功下载，只能标记 `technical_success=true`，不能自动记为 A/B。

---

## 十四、MVP 数据集与来源审计

为了快速进入实验，数据集分四级，不能把所有数据准备都变成 Smoke 的前置条件：

| 阶段 | 建议规模 | 任务/候选数 | 目的 | 能否得出正式结论 |
|---|---:|---:|---|---|
| `retarget_smoke_v1` | 12 张源图 × 2 个目标比例 | 24 Task / 96 个四方法候选 | 检查输入、四方法、日志、UI、统计和断点恢复 | 否 |
| `retarget_baseline36_v1` | 36 张源图 × 2 个目标比例 | 72 Task / 288 个候选 | 第一轮正式四方法基线 | 可以，但需标注样本量 |
| `retarget_pilot60_v1` | 60 张源图 × 2 个目标比例 | 120 Task / 480 个候选 | 稳定 Pilot、阈值和失败类型分析 | 可以，优先用于后续路线决策 |
| Main | 300 张源图 × 2 个目标比例 | 600 Task / 2400 个候选 | Pilot 稳定后的主实验 | 可以 |

公司约 130 张真实图片应继续作为独立最终测试集，不用于选择方法参数、评分阈值、Prompt、Agent 模型或工作流。公司数据不得为了本地 Smoke 或远程调试而出域。

12 张 Smoke 只要求尽快覆盖明显不同的输入：文字海报、单商品、多元素电商图、多人物、人物肖像、风景/建筑或强结构线。若公开图片的许可证审计来不及完成，可先使用用户明确允许的本地非敏感图片和程序化 fixture，不要因下载大型数据集延迟 Smoke。

36 张第一轮正式基线建议覆盖：

- 6 张中文密集文字海报；
- 6 张单商品电商宣传图；
- 6 张多商品、价格、Logo、按钮、角标混合宣传图；
- 6 张多人物、遮挡或人物分散图片；
- 4 张人物肖像；
- 4 张风景、建筑、明显直线或几何结构图片；
- 4 张多主体、多文字、复杂背景混合困难图。

公开数据候选：

- RetargetMe；
- PKU PosterLayout；
- CGL-Dataset v2；
- COCO 多人物子集；
- 具有明确许可证的其他公开图片；
- 程序化生成的中文海报与电商压力测试图片。

以上仅为候选，不得凭记忆认定其最新许可证、商用条件或再分发权限。若要形成审计结论，应优先查官方页面、官方仓库、论文附录或正式许可证文件，并记录访问日期和证据链接。

必须先生成数据来源审计表：

- 数据源；
- 场景覆盖；
- 总体规模；
- 计划抽样数量；
- 预计下载体量；
- 官方来源；
- 许可证名称与原文证据；
- 是否允许研究使用；
- 是否允许商用；
- 是否允许再分发；
- 是否允许修改后再分发；
- 是否只保存下载脚本和 manifest；
- 当前结论；
- 未解决风险；
- 审计日期。

许可证不明确时：

- 不把图片提交 Git；
- 不默认允许再分发或商用；
- 只实现 Adapter、下载说明和本地 materialize 流程；
- 必要时用程序化生成图片补齐可公开 Smoke fixture；
- 在报告中把结论标为 unknown，而不是猜测。

不要直接下载几十 GB 完整数据集。先抽样并验证 Adapter、许可证、哈希、场景覆盖和评审流程。

---

## 十五、图片集—目标尺寸格式

必须支持一个源图映射多个目标尺寸，不靠修改代码添加尺寸。

运行时数据集根目录应包含：

```text
dataset.yaml
images/
sources.csv
targets.csv
tasks.csv
annotations/    # 可选
guidance/       # 可选
```

要求：

1. `source_id`、`target_id`、`task_id` 只使用小写英文、数字、下划线和短横线。
2. 图片文件名不要使用空格或汉字；图片内部可以有中文文字。
3. `image_path` 使用相对于数据集根目录的路径。
4. 每个 `source_id` 唯一。
5. `target_id` 采用语义名加尺寸，例如 `sq_1000x1000`。
6. 每一行 `tasks.csv` 代表一个“源图—目标尺寸”任务。
7. `task_id` 推荐为 `source_id__target_id`。
8. 所有尺寸使用像素，width 在前，height 在后。
9. 一张源图的所有任务必须属于同一个 split。
10. `sources.csv` 保存 SHA-256；校验失败应停止该图片任务并报告，不继续产生不可复现结果。
11. 数据集一旦用于正式实验就视为不可变；修改图片、任务、标注或尺寸应创建 v2，而不是静默覆盖 v1。
12. 数据集验证器应生成 `dataset_fingerprint`。
13. 新数据集接入必须只需要准备这些文件并运行 CLI，不得改 Python 代码。
14. Windows 路径进入 manifest 前应规范为相对 POSIX 风格路径或明确的跨平台规则。
15. 必须防止 `..`、绝对路径和符号链接逃逸数据集根目录。
16. 应校验图片真实宽高、格式、可解码性、重复文件、重复任务、未知 source/target、禁用记录和 split 泄漏。
17. `annotations/` 与 `guidance/` 的版本、坐标系、归一化方式和目标尺寸关系必须写入 schema。

建议目标尺寸示例：

```text
sq_1000x1000
portrait_1080x1440
portrait_1080x1920
landscape_1200x628
landscape_1920x1080
```

Smoke、36 张正式基线和 60 张 Pilot 都不必让每张图跑 5 个尺寸。首轮每张选择 2 个差异明显的比例：

- 原图偏竖：`1:1 + 1.91:1`；
- 原图偏横：`1:1 + 9:16`；
- 原图接近方形：`16:9 + 9:16`。

---

## 十六、重定向方法体系：共享分析与四种固定候选

本节不是“可能用到的方法名清单”，而是本项目要实现和比较的核心方案。标准 Generation Run 对每个 Task 固定生成四种互补候选：`direct_warp`、`crop`、`seam`、`mesh`。四种方法消费同一份共享分析和保护信息，彼此独立运行；某一种失败不能阻塞其他三种，也不能由 Agent 在生成前取消。

首版不把 `Crop + Seam`、`Crop + Mesh`、`Seam + Scaling` 或三算子链作为第五、第六种核心方法。若以后需要研究组合算子，应作为新的独立实验和插件进入，给出单独消融、候选预算和 ADR，不能混入四候选基线后宣称仍是同一实验。

标准配置的核心语义应接近：

```yaml
methods:
  - direct_warp
  - crop
  - seam
  - mesh
generation_mode: all_four
selector: hard_ranker
agents:
  protection:
    mode: conditional
  judge:
    mode: conditional
fallback:
  external_aigc_enabled: false
```

四种方法可以并行以降低墙钟时延，也可以在资源有限时串行，但候选集合和配置必须相同。第一阶段不能通过“某张看起来简单就少跑两种方法”减少实验成本；将来生产级联需作为独立策略对照。

### 16.1 统一输入、坐标系和候选输出

每个 `CandidateMethod` 至少接收：

- `TaskSpec`：源图、目标宽高、目标比例、任务 ID；
- `AnalysisArtifact`：检测框、分割 Mask、文字区域、显著性、结构线、`ImportanceMap`、`ToleranceMap`、场景类别和置信度；
- `HumanGuidance | None`：可选人工保护、偏好保留、允许删除和目标锚点；
- `MethodConfig`：方法版本、参数、候选数、资源预算和随机种子；
- `ExecutionContext`：缓存、产物目录、超时、设备和日志上下文。

必须统一约定：

1. 所有框、点、Mask 和网格明确使用源图像素坐标、归一化坐标或目标坐标中的哪一种。
2. 边界采用闭区间还是半开区间、`x/y` 与 `row/column` 的顺序、宽高的方向必须写入 schema。
3. 在缩放、裁剪和形变后，保护区域要通过明确的变换映射到当前阶段坐标，不能继续使用旧坐标。
4. 每个分析结果都记录来源插件、模型/算法版本、置信度和是否经人工确认。
5. 缺失某个 Analyzer 时，方法可以声明降级运行、跳过或失败；不能默默把空 Mask 当成“图中没有重要内容”。

标准四候选 Run 中，每个方法默认产生一张主候选。参数搜索或多变体实验可以产生多个 `CandidateRecord`，但必须使用单独的 Run 类型和候选预算，不能与标准四候选结果混合。每条记录必须包含：

- `candidate_id`、`task_id`、`method_id`、`method_version`；
- 完整目标尺寸的候选图；
- 实际参数与配置哈希；
- 所消费的分析产物和 Mask 引用；
- 分阶段 `transform_log`；
- `SUCCESS / UNSAFE / FAILED / NEEDS_MANUAL_REVIEW` 状态；
- 警告、异常、时延、CPU/内存和可选 GPU 指标；
- 候选图哈希和可回放信息。

`SUCCESS` 只表示方法成功产生了尺寸正确、可解码的候选，不等于人工 A 或业务可用。`UNSAFE` 表示产生了图，但违反明确保护约束或出现严重几何风险；`FAILED` 表示没有有效产物；`NEEDS_MANUAL_REVIEW` 表示规则无法可靠判断。

### 16.2 共享分析层：YOLO 是保护信息来源，不是裁剪算法

推荐把分析过程拆成可替换的 `Analyzer` 插件，而不是把 YOLO、OCR 或显著性硬编码进某一个 Crop 类。初始分析图可以包含：

1. `ImageMetadataAnalyzer`
   - 读取真实宽高、EXIF 方向、色彩模式、Alpha、文件格式和可解码性；
   - 计算源比例、目标比例和比例变化强度。
2. `ObjectAnalyzer`
   - 可由 YOLO 检测或分割模型实现；
   - 输出人物、商品和通用对象的框或实例 Mask；
   - 保留类别、置信度、面积、是否贴边、是否被遮挡等信息；
   - YOLO 版本、类别映射和阈值必须配置化，不能写死在 Runner。
3. `FaceOrKeyRegionAnalyzer`
   - 可选地补充人脸、头部、人体关键部位或商品核心区域；
   - 用于避免“大框整体保留了，但脸或商品细节仍被切断”的情况。
4. `TextRegionAnalyzer`
   - 当前只负责输出文字区域和可选识别置信度，用于保护文字；
   - 不在当前范围内承担文字提取、去字、重新排版或回贴。
5. `LogoRegionAnalyzer`
   - 输出 Logo 区域或由数据集标注直接提供；
   - 检测器缺失时允许从人工/数据集标注读取。
6. `SaliencyAnalyzer`
   - 提供连续显著性热图，补足固定类别检测器没有覆盖的主体；
   - 显著性不能自动升级为硬保护，因为它也可能把高对比背景误当主体。
7. `GeometryAnalyzer`
   - 检测长直线、建筑边缘、规则商品轮廓和其他对弯曲敏感的结构；
   - 主要服务于 Mesh 风险控制。
8. `SceneProfileAnalyzer`
   - 输出 `precision / coverage / balanced` 及置信度；
   - 可以由人工标签、规则或模型提供，但三种来源必须分开记录。

分析融合层将上述结果转成统一保护表示：

- `must_keep`：人脸、核心商品、关键 Logo、人工硬保护等不可裁断区域；
- `prefer_keep`：一般主体、次要文字、显著区域等尽量保留区域；
- `removable`：人工或高置信规则明确允许优先删除的背景；
- `rigid_region`：可以移动或整体缩放，但不应发生非刚性扭曲的区域；
- `line_constraints`：应保持直线或相对方向的结构；
- `ImportanceMap`：保留代价；
- `ToleranceMap`：删除、压缩和形变容忍度。

融合时至少遵守：

1. `must_keep` 与 `removable` 冲突时，`must_keep` 优先并记录冲突。
2. 对检测框或 Mask 可按类别与分辨率进行适量膨胀，避免裁剪线贴着人脸、文字或商品边缘；膨胀量必须记录。
3. 硬约束与软权重分开保存，不能把所有保护都压成一个二值 Mask。
4. 低置信检测不应自动成为一票否决，但应抬高不确定性并可能触发 Agent 或人工复核。
5. 不同模型的坐标和输入缩放必须还原到原图坐标后再融合。

`Protection Agent` 只能在确定性 Analyzer 已经给出对象、OCR、显著性和结构结果以后按需调用。它输出对象 ID、语义优先级、核心/次要关系、可牺牲背景和置信度，不直接绘制像素级 Mask，也不凭自然语言坐标替代检测与分割。融合层把其结构化语义绑定回已有框、Mask 和热图；若绑定失败或置信度不足，保留原始分析并提高不确定性。

### 16.3 方法 A：Direct Warp，非等比直接缩放基线

定义：把源图从 `(W, H)` 直接重采样到 `(Wt, Ht)`，横向缩放因子为 `sx = Wt/W`，纵向缩放因子为 `sy = Ht/H`。

作用：

- 它几乎总能低成本地产生尺寸正确的图；
- 它是判断“目标比例本身会造成多大几何压力”的必要基线；
- 它不应因为实现简单而从评测中删除。

必须记录：

- `sx`、`sy`、`max(sx/sy, sy/sx)`；
- 拉伸风险先验 `D_stretch = abs(log((Wt/Ht) / (W/H)))`；
- 插值方式；
- 人脸、商品、文字框的纵横比变化；
- 结构线角度和局部形状风险。

主要风险：人物、圆形商品、Logo 和文字会整体被拉宽或压扁。比例差较大时可以由规则标记高风险并触发视觉复核，但仍保留候选用于比较，不能只因 `sx != sy` 或 `D_stretch` 较大就删除产物。风景或抽象背景可能容忍较大拉伸，而人脸、圆形 Logo、规则商品与文字通常更敏感。

### 16.4 方法 B：Crop，共享保护信息驱动的智能裁剪

这里的“YOLO + Crop”不是 YOLO 自己完成裁剪，而是 YOLO/OCR/显著性/人工标注提供保护对象，`crop` 插件搜索满足目标比例的裁剪窗口。中心裁剪可以作为同一插件的 `center_baseline` 参数变体用于消融，但标准四候选中的 `crop` 应使用保护式窗口搜索。

建议流程：

1. 将目标比例映射为原图坐标中的候选窗口比例。
2. 枚举或优化多个候选窗口：中心、九宫格锚点、对象中心、显著性中心、人工 `target_anchor`，以及必要的多尺度窗口。
3. 对每个窗口计算硬约束：
   - 是否完整包含 `must_keep`；
   - 是否切穿人脸、文字、Logo、商品核心或实例 Mask；
   - 输出分辨率是否足够；
   - 是否越界。
4. 对可行窗口计算软评分。建议的概念形式为：

```text
crop_score
= must_keep_coverage
+ prefer_keep_coverage
+ saliency_coverage
+ composition_score
+ target_anchor_score
- cut_object_penalty
- text_logo_cut_penalty
- excessive_crop_penalty
- empty_or_unbalanced_penalty
```

5. 使用非极大抑制或窗口差异阈值保留 1～K 个真正不同的候选，避免输出大量几乎相同的裁剪。
6. 等比缩放选中窗口到目标尺寸，并重新计算保护对象在结果中的覆盖、裁断情况与边界安全距离。

需要配置化：

- 必须完整保留的类别与最小置信度；
- 各类别权重；
- 框/Mask 膨胀像素或比例；
- 窗口搜索步长、最大候选数和最小差异；
- `precision / coverage / balanced` 三类场景的权重模板；
- 无可行窗口时是 `UNSAFE`、转下一方法还是请求人工指引。

关键要求：

- 多人物或多个商品不能只保护最高置信度对象；
- 保护大框整体覆盖不代表局部关键部位安全；
- 不允许为了满足裁剪窗口而静默降低 `must_keep`；
- 当所有重要内容的联合包围框与目标比例不兼容时，应明确报告“裁剪不可行”；Seam 和 Mesh 仍独立完成自己的候选，最终由 Selector/Judge 判断是否存在可用结果。

Crop 的风险不是“总共裁掉多少”，而是“裁掉了什么”。应记录按 Importance 加权的内容损失、每个区域的保留率、裁剪窗口与保护边界距离。裁掉大面积 P3 纯背景可以是低风险；只碰到少量 P0 人脸、核心文字或 Logo 也可能是高风险。

### 16.5 方法 C：Seam，共享保护约束下的内容感知接缝雕刻

Seam Carving 通过反复删除或插入一条从图像一端贯穿到另一端的低能量连续接缝来改变宽高。它不是普通裁剪：删除可以分散在多个背景区域，但也可能沿着低纹理的人脸、衣服或商品内部穿过，因此必须使用保护信息。

推荐能量概念：

```text
E_total
= E_forward_or_gradient
+ lambda_importance * ImportanceMap
+ lambda_keep * must_keep_or_prefer_keep
- lambda_tolerance * ToleranceMap
- lambda_drop * removable
```

其中：

- `E_forward_or_gradient` 估计删除接缝后新邻接边缘产生的视觉代价；
- `ImportanceMap` 和保护 Mask 提高重要区域能量，使接缝避开；
- `ToleranceMap` 和 `removable` 降低可删除背景能量；
- Keep 与 Drop 冲突时 Keep 必须优先。

建议流程：

1. 判断需要改变的轴和数量；横向改宽寻找竖直 seam，纵向改高寻找水平 seam。
2. 每删除或插入若干 seam 后重新计算能量、保护区域坐标和风险指标。
3. 设置每个轴的最大 Seam 预算。阈值必须由实验校准；达到预算仍未完成目标时，允许 Seam 插件用一次明确记录的最终尺寸对齐步骤生成候选，但必须把剩余非等比缩放风险写入同一 transform log，不能伪装成纯 Seam 无失真。
4. 删除 seam 前检查与 `must_keep` 的交叠；若不存在安全路径，立即停止该轴并返回剩余比例差，而不是穿过硬保护区域。
5. Seam 插入应记录复制或插值来源，避免多次插入导致纹理重复；第一版可以优先实现删除，插入作为独立能力验收。
6. 输出每条或每批 seam 的累计日志、保护命中、能量统计和阶段缩略可视化。

主要适用场景：存在连续低价值背景、主体较集中、只需中小幅改变比例。

主要失败风险：

- 接缝穿过低纹理人脸、人体或商品；
- 多人物之间背景不够，无法安全删除足够宽度；
- 建筑直线、文字和规则纹理出现弯折；
- 插入造成重复纹理；
- 极端比例变化累计形变过大。

Seam 评价重点是接缝穿过了什么，而不是接缝数量本身。必须统计接缝与 P0/P1、文字笔画、人脸关键区域、商品边缘、结构线的交叠，以及位移是否主要集中在 P2/P3 背景。接缝很多或累计位移很大只能提高风险，不能单独等同于业务失败。

### 16.6 方法 D：Mesh，共享保护约束下的网格形变

Mesh Warp 将图像划分为规则或自适应网格，通过移动网格顶点把外边界变成目标矩形，再对每个网格单元进行纹理映射。与 Direct Warp 相比，它允许背景承担更多压缩，而主体区域尽量保持局部形状。

建议优化目标包含：

```text
E_mesh
= lambda_boundary * E_target_boundary
+ lambda_smooth * E_neighbor_smoothness
+ lambda_shape * E_cell_shape
+ lambda_rigid * E_protected_region_rigidity
+ lambda_line * E_line_preservation
+ lambda_importance * E_importance_weighted_distortion
+ lambda_anchor * E_target_anchor
```

约束含义：

- `E_target_boundary`：外边界必须匹配目标画布；
- `E_neighbor_smoothness`：相邻顶点位移不能无规律跳变；
- `E_cell_shape`：限制网格单元剪切和极端纵横比；
- `E_protected_region_rigidity`：覆盖人脸、商品、文字、Logo 的网格尽量保持相似变换或局部刚性；
- `E_line_preservation`：建筑边缘和规则直线尽量保持直；
- `E_importance_weighted_distortion`：重要区域承担更少形变，允许背景承担更多；
- `E_target_anchor`：用户或策略指定的主体目标位置。

建议流程：

1. 根据图像大小建立网格，并把保护对象、Mask、结构线和锚点映射到网格单元。
2. 求解顶点位移；具体求解器可以替换，但目标函数、约束和收敛状态必须可记录。
3. 检查网格单元是否翻折、面积接近零、超出边界或出现过大剪切。
4. 使用三角形或四边形纹理映射生成目标图。
5. 把每个对象区域的局部尺度、旋转、剪切、面积变化和最大位移写入日志。

主要适用场景：需要连续压缩或扩展、背景可形变、又不能直接裁掉全部内容的任务。

主要失败风险：人物肢体和商品结构弯曲、文字倾斜、直线弯折、网格翻折、边界波浪和局部模糊。Mesh 输出尺寸正确不代表求解安全；出现不可逆的翻折、空洞或解码错误属于硬失败。局部 Jacobian、剪切或位移较大但只落在无纹理背景时，应作为风险证据结合最终视觉判断，不能仅凭数值判死刑。

### 16.7 外部自定义方法与后续后处理接口

需要预留一个通用 `CandidateMethod` 注册入口，使用户未来可以接入自己的重排、生成或其他方法。外部方法只要满足统一输入输出、错误隔离、产物冻结和日志协议，就可以在显式实验或回退 Run 中作为候选参与评测。

外部能力分为三种，不能混成一个大接口：

1. `ExternalAIGCProvider`
   - 面向 Seedream 等厂商 API；
   - 负责鉴权、请求映射、提交、轮询、结果下载、超时、重试、计费与供应商错误归一化；
   - 不负责平台中的候选排序和 A/B/C 评价。
2. `WorkflowBackend`
   - 面向用户自己实现的本地 Python、ComfyUI HTTP 或远程 HTTP 工作流；
   - 负责 workflow template、输入节点绑定、运行、状态查询、结果收集与版本；
   - 产品运行时只允许调用受控 Python/HTTP 接口，不执行任意 Shell。
3. `PostProcessor`
   - 面向候选生成后的可选文字回贴、合成、修补或清晰化；
   - 输入和输出都必须形成新的产物与血缘记录；
   - 不能覆盖原始 Candidate，也不能让后处理结果冒充原方法输出。

建议由两个通用 `CandidateMethod` Adapter 连接上述后端：

```text
ExternalAIGCCandidateMethod
  └─ ExternalAIGCProvider（seedream_api / other_vendor）

WorkflowCandidateMethod
  └─ WorkflowBackend（local_python / comfyui_http / remote_http）
```

Seedream 首版 Provider 的具体 URL、模型名、请求字段和计费规则必须在实现时依据用户实际获得的官方 API 文档与账户能力确认，不得凭记忆写死。平台层只冻结稳定语义：输入图、目标尺寸、可选 Mask/Prompt、seed、输出数、超时、费用上限、合规策略和返回候选。

自研 ComfyUI 接入不得把整份 workflow JSON 写死在 Python 代码中。建议保存：

- `workflow_id / workflow_version`；
- 模板 JSON 的文件引用和 SHA-256；
- 逻辑输入名到节点 ID/字段的绑定；
- 必需 custom nodes、模型和版本清单；
- 输入上传、Prompt 提交、轮询和输出节点规则；
- ComfyUI 服务版本、工作流 seed 和实际参数；
- 队列等待、执行、下载和后处理时延；
- 缺节点、缺模型、服务不可达、队列超时和输出缺失的归一化错误。

本地 Python 工作流必须通过显式 callable/协议接入，声明依赖、设备、输入输出和超时；不能让 Runner `import` 任意路径或执行任意用户字符串。远程自研模型建议部署为 HTTP 服务，再由 `remote_http` Backend 接入。SSH 只用于部署和调试该服务，不作为产品每次推理的隐式执行机制。

如未来需要在重定向后继续处理文字或其他资产，可使用 `PostProcessor` 边界。当前 M0-M4 只定义协议，不展开具体文字模型；M8 才真实验证 Seedream Provider 与至少一种自研 WorkflowBackend。

### 16.8 候选预算与方法公平性

1. 标准 Run 固定四种方法各一张主候选；参数搜索必须使用独立 Run，并设置每 Task 的候选上限、总时延上限和资源预算。
2. 不允许一个方法产生几十个候选、另一个方法只产生一个候选后，直接比较 Any-method 成功率而不报告候选预算。
3. Top-1 排序必须在记录完整的候选集合上进行；方法失败也要保留失败记录。
4. 参数搜索、人工指引和自动运行必须使用不同的 Run 类型，不能混在正式测试指标中。
5. 四种方法必须消费同一版本的 AnalysisArtifact；如果 Protection Agent 改变了保护语义，四种候选必须作为一个新的 Generation Run 共同重生成，不能只重跑其中某一种后与旧候选混比。

### 16.9 推荐的稳定方法 ID

在第一次正式 Run 前通过 ADR 冻结方法 ID。推荐使用语义名称，不把实验顺序写进永久 ID：

| method_id | 算子链 | 主要目的 |
|---|---|---|
| `direct_warp` | 非等比缩放 | 几何形变基线 |
| `crop` | 共享保护 + 候选窗口搜索 + 等比缩放 | 尽量无形变地保留关键内容 |
| `seam` | 保护式 Seam + 明示的尺寸对齐 | 在低价值区域分散改变尺寸 |
| `mesh` | 受约束网格形变 | 将形变更多分配给可变形背景 |
| `external_*` | 外部插件声明 | 后续用户自定义方法 |

同一 `method_id` 的算法行为发生不兼容变化时必须提升 `method_version`。参数变体使用 `variant_id` 或配置哈希区分，不要复制出一批含糊的方法名。

---

## 十七、Agent 详细设计：按需保护消歧、候选择优与失败回退

### 17.1 先区分两个“Agent”

本项目中有两个不同概念，Codex 不得混淆：

1. **Codex 开发 Agent**：当前与你对话、检查仓库、Grill 需求、设计、写代码、运行测试和更新文档的开发协作者。它必须遵守开发门禁和里程碑范围。
2. **retarget-agent 产品 Agent**：未来运行在图片重定向平台内部，对疑难保护语义、四张冻结候选的排序以及失败回退进行条件式判断的业务组件。

产品 Agent 不负责直接编辑像素，不重新实现 YOLO、Crop、Seam 或 Mesh，不在生成前选择唯一方法，也不能绕过 Runner 任意调用代码。它只读取结构化上下文与受控图片输入，输出经过 schema 校验的语义或选择决策；真正的分析、候选生成、保存和回退执行始终由 Analyzer、CandidateMethod、Evaluator、SelectorPolicy 和 Runner 完成。

### 17.2 产品 Agent 的目标与非目标

产品 Agent 只解决三类问题：

1. **Protection Agent：疑难主体保护理解**
   - 多人物时谁是核心人物；
   - 多商品时哪个是主商品，哪些是装饰或陪衬；
   - 哪些文字是品牌、价格、核心卖点或次要装饰文字；
   - 哪些现有检测对象属于 P0/P1/P2/P3，哪些背景可牺牲；
   - 检测、OCR、显著性或人工标注冲突时怎样确定语义优先级。
2. **Judge Agent：候选择优**
   - 四张候选中哪些关键内容完整、哪些出现可见失真；
   - transform log 风险很高但肉眼可接受，或日志低风险但视觉异常时怎样处理；
   - 候选评分接近或指标冲突时，哪一张最适合作为 Top-1；
   - Top-1 是 A、B、C 还是无法可靠判断。
3. **Fallback Decision：失败回退判断**
   - 四种传统候选是否确实都不可靠；
   - 应返回最保守的 B、进入人工复核、声明失败，还是允许调用外部 AIGC 方法；
   - 是否存在“传统候选本来可用，却被规则误杀”的不必要回退。

产品 Agent 不应：

- 自己读写任意文件路径、执行 Shell 或安装依赖；
- 动态生成并执行 Python 代码；
- 擅自修改 `must_keep` 硬约束；
- 选择跳过 Direct Warp、Crop、Seam 或 Mesh 中任意一个标准候选；
- 规划方法顺序、算子组合、参数搜索或生成重试；
- 因为模型“觉得好看”而覆盖明确的文字、Logo、人脸或商品保护失败；
- 静默调用付费或外部模型；
- 把 OCR 识别到的图片文字当成系统指令；
- 在没有日志和版本记录的情况下改变 Top-1。

### 17.3 推荐主循环与状态机

推荐状态如下：

```text
RECEIVED
→ VALIDATED
→ DETERMINISTIC_ANALYZED
→ PROTECTION_RESOLVED（仅语义歧义时）
→ ANALYSIS_FROZEN
→ FOUR_CANDIDATES_GENERATED
→ CHECKED_AND_SCORED
→ CLEAR_DECISION ?
    ├─ YES → SELECTED_BY_RULES
    └─ NO  → JUDGED（条件式）
→ FALLBACK_DECIDED（仅无可靠候选时）
→ SELECTED
→ COMPLETED
```

允许的终止或分支状态：

- `NEEDS_MANUAL_REVIEW`：没有足够证据安全自动决定；
- `FAILED`：输入、分析或所有方法均失败，且无合法降级；
- `PARTIAL_COMPLETED`：部分方法失败，但仍有合法候选与完整失败记录；
- `FALLBACK_REQUIRED`：四种候选均不可靠，等待外部 AIGC/人工策略处理；
- `AGENT_UNAVAILABLE`：Agent 超时、模型不可用或解析失败，进入确定性降级。

Runner 而不是 LLM 控制状态转换。Agent 只能对已有对象和候选输出允许的结构化标签与决策；它不能动态增加候选、修改图像或启动未授权 API。

### 17.4 三个受控职责点

#### A. `protection_resolution`：Protection Agent

调用位置：确定性对象检测、OCR、显著性、Logo/人脸/结构分析以后，`AnalysisArtifact` 冻结以前。

输入：原图缩略图、检测对象 ID 与框/Mask、OCR 区域和文本摘要、显著性图、冲突标记、`scene_profile`、可选人工标注。

职责：

- 只对已有对象做核心/次要、主商品/陪衬、核心文案/装饰文字、可牺牲背景的语义判断；
- 输出 P0/P1/P2/P3、可删除/可形变/局部刚性等结构化标签和置信度；
- 不新增像素坐标，不直接画 Mask，不修改源图，不选择重定向方法；
- 无法绑定到已有对象时返回 unresolved，而不是编造对象。

触发示例：多人物或多商品核心不明；OCR、显著性和检测结果冲突；保护区域占比过高且需要优先级；复杂海报元素密集。单一明确主体、简单风景或高置信标注不调用。

该 Agent 的决定会改变四种方法消费的保护信息，因此修改后必须产生新的 AnalysisArtifact 和新的 Generation Run，不能只在 Evaluation Replay 中假装替换。

#### B. `candidate_judging`：Judge Agent

调用位置：四种候选全部冻结并完成确定性检查与软评分以后。

输入至少包括：

- 原图；
- 四张候选的固定编号对比板；
- P0/P1/P2/P3 与可疑区域叠加图；
- OCR、主体、Logo、结构线前后对比；
- Direct Warp/Crop/Seam/Mesh 的 transform log 摘要；
- 可疑局部放大图；
- 硬失败、软风险、规则排名和前两名差距。

职责：比较核心内容保留、可见几何失真、构图与业务可用性，输出完整排名、Top-1、A/B/C 倾向、置信度和 reason codes。Judge 不修改候选，也不触发参数搜索。

触发示例：前两名分差很小；多个评分器排序冲突；日志高风险但视觉看起来正常；日志低风险但专用检测发现异常；所有候选都处于临界区。若某候选明显安全且显著领先，则由规则直接选择。

#### C. `fallback_decision`：失败回退判断

调用位置：没有可靠 A/B 候选，或 Judge 仍无法安全选择时。

允许输出：

- `USE_BEST_TRADITIONAL`：选择最保守、业务仍可接受的 B；
- `CALL_EXTERNAL_AIGC`：允许后续外部 AIGC CandidateMethod 处理；
- `REQUEST_MANUAL_REVIEW`：请求人工复核或指引；
- `RETURN_FAILURE`：没有合法自动结果。

首版可以由 Judge Agent 同一次调用同时给出 fallback 建议，也可以由确定性 FallbackPolicy 执行。无论哪种方式，Agent 只给决策，Runner 才能检查费用、素材出域、配额和权限后真正调用外部方法。M0-M7 不实现或真实调用 Seedream；M8 才实现 Provider/Workflow Adapter，并在凭据、付费和合规门禁满足后进行真实验证。

### 17.5 场景策略影响判断标准，不影响四种方法是否生成

- **Precision**：对人脸、人物细节、精细商品、Logo 和规则形状的误放更保守；日志—视觉冲突更容易触发 Judge；置信度不足时优先人工或外部回退。
- **Coverage**：优先保证多人物、主商品、品牌、价格和核心文字完整；允许 P2/P3 装饰或背景大幅变化；不能因为总裁剪量或总形变量大就直接淘汰。
- **Balanced**：确定性规则和软评分优先，只有候选接近或证据冲突时调用 Agent。

四种方法在三类场景下都要生成。场景只影响保护融合、风险权重、自动放行阈值和 Agent 触发概率，不允许 Agent 通过跳过某种方法抬高成功率或降低成本。

### 17.6 结构化 Agent 输出，不接受自由文本控制程序

Protection Agent 建议输出：

```json
{
  "schema_version": "1.0",
  "task_id": "poster_0001__landscape_1200x628",
  "scene_profile": "coverage",
  "core_element_ids": ["person_1", "product_1", "text_2"],
  "region_priorities": [
    {"region_id": "person_1", "importance": "P0", "tolerance": "rigid"},
    {"region_id": "text_4", "importance": "P2", "tolerance": "removable"}
  ],
  "unresolved_region_ids": [],
  "confidence": 0.88,
  "reason_codes": ["main_product_near_primary_person"]
}
```

Judge Agent 建议输出：

```json
{
  "schema_version": "1.0",
  "task_id": "poster_0001__landscape_1200x628",
  "candidate_ranking": ["crop", "mesh", "seam", "direct_warp"],
  "best_candidate": "crop",
  "grade": "A",
  "business_usable": true,
  "core_content_preserved": true,
  "visible_distortion": "minor",
  "removed_content_importance": "low",
  "selection_confidence": 0.91,
  "metric_visual_conflict": true,
  "reason_codes": ["large_background_removal_but_core_content_intact"],
  "fallback_action": "NONE"
}
```

这些只是 schema 示例，不是已经校准的阈值。所有 `candidate_id` 和 `region_id` 必须来自输入白名单；未知 ID、重复排名、缺候选、非法等级、越权动作或无法解析 JSON 都应被拒绝并记录。自然语言理由只供审计，Runner 只执行 schema 校验后的枚举值。

### 17.7 硬规则、评分器和 Agent 的权限顺序

推荐权限顺序：

```text
数据与尺寸合法性
> 可验证的核心内容缺失/改变
> 图像损坏、网格翻折等确定性算法错误
> 自动质量评分
> Agent 比较判断
> 成本与时延偏好
```

硬门控必须缩小到证据明确、业务上不可接受的错误，例如输出损坏、核心人物/商品明显缺失、核心文字内容缺失或不可读、明确严重的人脸/Logo/商品变形、可见断裂或 Mesh 翻折。裁剪面积大、Seam 数量多、累计位移大、全局拉伸高、局部 Jacobian 异常但视觉不可见，都只能作为风险和 Agent 触发信号，不能单独硬失败。

Agent 可以解释和权衡软指标，也可以在“日志高风险但删除的只是背景”时挽救规则的保守误拒；它不能推翻可验证的核心内容缺失或图像损坏。对于“变化很小但切断人脸/文字/Logo”的情况，专用检测证据仍应优先。

硬规则结果必须包含 reason code 和证据引用，例如对象 ID、覆盖率、网格单元或裁剪边界，避免只给出一个不可追踪的布尔值。

### 17.8 Agent 触发策略：默认条件式，不是每张图都调用

建议支持以下实验模式：

1. `all_outputs`：四张全部输出，不自动选 Top-1，Agent 0%。
2. `hard_ranker`：四张全部生成，由硬检查和固定软分数选 Top-1，Agent 0%。
3. `protection_agent_only`：只在保护语义歧义时调用 Protection Agent，选择仍由 Hard Ranker 完成。
4. `judge_agent_only`：保护信息完全由确定性规则产生，只在候选难分时调用 Judge Agent。
5. `conditional_agent`：Protection 和 Judge 均按触发条件调用，作为推荐生产模式。
6. `always_on_agent`：每个 Task 都调用 Protection 与 Judge，仅用于消融和质量上界，不作为默认生产模式。
7. `seedream_only`：全部走外部 AIGC，仅作为 M8 成本/质量对照，不属于当前实现范围。

条件式触发可以包括：

- 多人物、多商品或复杂海报的核心元素不明确；
- 检测、OCR、显著性或数据集标注冲突；
- 保护区域占比过高且必须决定优先级；
- Top-1 与第二名分差过小；
- 硬规则与软评分冲突；
- 不同评分器排序冲突；
- 所有候选都出现中高风险；
- 日志风险与最终视觉证据冲突；
- Agent 的预计收益高于调用成本阈值。

Protection 触发规则属于 Generation 配置；Judge 与 fallback 触发规则属于 Replay 配置。二者必须分开版本化。Agent 目标调用率可以先把 10%～30% 作为待验证情景，但最终必须通过选择性风险—覆盖率曲线确定，不能为了达到预设比例而调用。

### 17.9 失败降级，不由 Agent 重试生成

Agent 不允许在首版提出换方法、改参数、扩候选或重新生成。Protection Agent 超时或解析失败时，使用原始确定性保护信息继续生成四张候选，并标记 `protection_uncertain`；Judge Agent 不可用时，使用 Hard Ranker。如果 Hard Ranker 也没有可靠候选，则按照配置进入人工复核、返回失败或显式外部回退，不能随便返回第一张图。

人工添加 `must_keep / removable / target_anchor` 属于新的 guided Generation Run，必须与自动模式分开统计。外部 AIGC 生成也属于新的 CandidateMethod/Generation Run，不能伪装成 Evaluation Replay。

### 17.10 Agent 记录对象

`AgentCallRecord` 至少保存：

- `agent_call_id`、`agent_run_id`、`task_id`、职责点和调用序号；
- agent/plugin ID 与版本；
- 模型提供方、模型版本和解码参数；
- system/user Prompt 版本与模板哈希；
- 输入引用、图片/候选哈希和脱敏摘要；
- 原始响应或受策略允许的保存形式；
- 解析后结构化 JSON；
- schema 校验结果和非法动作原因；
- 调用是否成功、超时和重试；
- 时延、Token、估算费用；
- Agent 建议、Runner 实际采用的保护/选择/回退决策以及两者差异；
- 是否改变 Top-1；
- 改变后经人工评价是改善、无变化还是恶化。

不得只保存最终自然语言理由，否则无法回放、调试和量化 Agent 的真实贡献。

### 17.11 Agent 评测必须拆成三类实验

#### 选择能力 Replay

四种方法先生成完全相同的冻结候选集合。在不重新生成图片的情况下，对比：

- All Outputs；
- Hard Ranker；
- conditional Judge Agent；
- always-on Judge Agent；
- Oracle。

该实验主要回答“Agent 是否更会选”，不掺入候选生成差异。

#### Protection Agent 生成实验

使用相同 Task、相同四种方法和相同参数，分别以确定性保护、条件式 Protection Agent、Always-on Protection Agent 生成三套候选。比较：

- 核心对象/文字优先级正确率；
- 四方法 Any-method A 与 A+B；
- 各方法重要内容保留率；
- Agent 调用率、时延、Token 和费用；
- Agent 引入的有益/有害保护变更；
- 因保护信息改变而出现的候选质量变化。

因为 Protection Agent 改变了 AnalysisArtifact，这组实验必须新建 Generation Run，不能在冻结候选上 Replay。

#### 端到端条件式 Agent 与回退实验

四种传统方法仍然固定全部生成，只改变保护消歧、候选择优和回退策略，比较：

- Top-1 A 与 A+B；
- Any-method/Oracle；
- Protection/Judge Agent 各自调用率；
- 总时延、CPU/GPU、Token 和费用；
- 无安全候选率；
- 人工复核率；
- 外部 AIGC 回退率与不必要回退率；
- 每张 A 图或每张成功图成本。

该实验回答“Agent 是否缩小四方法 Oracle 与自动 Top-1 的差距，并减少不必要的外部 AIGC/人工处理”。它不回答“Agent 是否选对了生成路线”，因为 Agent 不负责预选路线。

### 17.12 Agent 专属指标

至少报告：

- `Protection Agent Call Rate`；
- `Judge Agent Call Rate`；
- `Fallback Decision Rate`；
- `Schema Valid Rate`；
- `Parse Failure Rate`；
- `Timeout Rate`；
- `Illegal Action Rate`；
- `Top-1 Change Rate`；
- `Beneficial Change Rate`；
- `Harmful Change Rate`；
- `Manual Review Rate`；
- `External AIGC Fallback Rate`；
- `Unnecessary AIGC Rate`；
- `Average Agent Latency/Tokens/Cost`；
- `Routing Regret`；
- `Cost per A` 与 `Cost per Success`。

Agent“经常改变结果”不等于 Agent 有价值；必须用人工标签判断改变是否真正改善。

还必须绘制自动放行的风险—覆盖率曲线或 `auto-pass coverage vs. auto-pass precision` 曲线。在给定 Bad Pass Rate 上限时，比较 Hard Ranker、Conditional Agent 和 Always-on Agent 能安全自动处理多少 Task。Agent 调用率不是越高越好，而应与增益、风险和成本共同解释。

### 17.13 Agent 成本与回本条件

按任务计费或共享设备情景下，Agent 的平均边际成本可先估算为：

```text
C_agent_per_image
= p_call * H * t / (3600 * u)
```

其中 `p_call` 是调用比例，`H` 是加速卡有效费用（元/小时），`t` 是单次判断秒数，`u` 是有效利用率。若按调用计费，则直接使用实际账单，不套该公式。

若外部 AIGC 单次成本为 `C_fallback`，无 Agent 和有 Agent 的回退率分别为 `f0`、`f1`，Agent 仅从节省外部生成费用角度回本需要：

```text
C_agent_per_image < C_fallback * (f0 - f1)
```

还要单独报告固定基础设施成本。独占常驻机器的月租、折旧和空闲时间不能按“实际推理几秒”消失；低流量时应使用 `固定月成本 / 月处理量` 计入每图成本。因此必须分别比较：共享公司 NPU、按需服务、弹性启动、项目独占常驻四种口径，不得只报告理想边际成本。

Agent 的主要经济价值不是理解每一张图，而是缩小 `Oracle Success - Top-1 Success`，减少 Bad Pass、人工复核与不必要 AIGC。默认生产方案是条件式 Agent；Always-on 仅作实验对照。

### 17.14 安全、隐私和可复现边界

1. OCR 文本、图片元数据和文件名全部视为不可信数据，不能作为指令拼接进高权限 Prompt。
2. Agent 只看完成任务所需的缩略图、结构化摘要和候选，不读取 `.env`、Token、Cookie、Git 凭据或公司内部目录。
3. 外部模型调用必须由显式配置和素材合规策略允许；公司素材默认不得出域。
4. Prompt、模型和规则版本变化必须产生新的 Replay 或 Agent Run，不能覆盖旧决策。
5. 自然语言解释仅供审计；系统执行以 schema 校验后的结构化动作和 Runner 状态为准。

### 17.15 Codex 在进入 M7 前必须把 Agent 问清楚的事项

这些事项不阻塞 M0-M6；在开始真实 Agent 开发、SSH 部署或 M7 实验前，至少要与用户确认：

1. 哪些检测冲突和场景复杂度触发 Protection Agent；
2. Protection Agent 可以修改哪些语义字段，哪些像素级信息永远不能生成或覆盖；
3. `precision / coverage / balanced` 的来源与保护优先级；
4. 哪些证据属于不可覆盖硬失败，哪些只是软风险；
5. Judge 的分差、冲突和临界区触发阈值；
6. 条件式调用与 always-on 对照规模；
7. Agent 最大时延、Token、费用和超时降级；
8. 无安全候选时返回保守 B、外部 AIGC、人工复核还是失败；
9. 外部回退的价格、合规、配额和素材出域门禁；
10. Agent 原始输入/响应在公司数据场景如何脱敏保存；
11. 为什么 Protection Agent 需要新 Generation Run，而 Judge 可在 Replay 中重复运行；
12. 如何定义 beneficial/harmful change、Unnecessary AIGC 和 Bad Pass；
13. 首版真实模型候选与小/大模型对照；若只用规则模拟协议，只能标为协议/基线实现，不能宣称已验证模型 Agent 效果。

### 17.16 Agent 模型实验矩阵与部署策略

以下为【候选方案】，不是已经确认可部署或已经测试的事实。需求发现结束前必须核对模型真实版本、许可证、权重获取、图像输入限制、结构化输出能力和目标硬件实测。

| 实验角色 | 候选模型/策略 | 默认用途 | 需要回答的问题 |
|---|---|---|---|
| 无 Agent 基线 | Hard Ranker | 生产降级与成本下界 | 不使用 VLM 时 Top-1、Bad Pass 和 Routing Regret 如何 |
| 轻量 Agent | `Qwen3-VL-4B` 候选 | Protection/Judge 条件式首选实验 | 单卡 24 GB、缩略图/拼图、结构化输出和时延是否可接受 |
| 大模型对照 | `Qwen3-VL-8B` 候选 | 语义理解和排序质量对照 | 相比 4B 的真实增益能否覆盖显存、时延和成本 |
| 条件式生产候选 | 4B 或实测更优模型 | 仅疑难 Task 调用 | 在给定 Bad Pass 上限下能安全自动处理多少 Task |
| 质量上界 | Always-on 8B | 只作消融 | Always-on 相比 Conditional 的上界与额外成本 |

模型名称仅表示第一批实验候选。若仓库实现时已有更合适的同类模型，Codex 可以提出替换，但必须给出版本、官方来源、许可证、资源需求和同数据对照，不能静默替换。

每个候选至少比较：

- BF16/FP16 与可用的 8-bit/4-bit；
- 单张 24 GB 与双张 24 GB；
- 单图、多图拼板和“全图 + 可疑局部裁片”输入；
- 原始分辨率、受控缩略图和分块策略；
- 常驻服务与逐次加载；
- Protection Prompt 与 Judge Prompt；
- 确定性 JSON 约束、schema 合法率和非法对象 ID；
- Conditional 与 Always-on；
- 本地协议 fixture、远程真实模型和模型不可用降级。

首版优先让 Protection 与 Judge 共享一个真实模型服务、使用两个独立 Prompt/Schema，以减少部署复杂度；只有性能或资源证据表明分开更好时才拆成两个常驻服务。模型是否能在单卡 24 GB 运行、是否需要量化或双卡，必须以远程实测为准，不得仅按参数量推断。

模型晋级不能只看主观“感觉更聪明”。至少比较：Protection 优先级正确率、Judge Top-1 A/A+B、Routing Regret、Beneficial/Harmful Change、Bad Pass、Schema Valid、P50/P95、峰值显存、调用成本和 Cost per Success。

---

## 十八、评价、排序与报告口径

### 18.1 评价单位

必须区分：

- Source：一张源图；
- Task：一张源图到一个目标尺寸；
- Candidate：某方法对某 Task 的一次输出；
- Method：算法及其版本；
- Run：固定数据、配置、代码和环境的一次候选生成；
- Replay：基于冻结候选的一次重新评价；
- Decision：一次 Top-1 选择；
- Review：一次人工评价事件。

### 18.2 人工等级

第一版使用：

- A：高质量，可直接用于目标业务场景；
- B：基本可用，算业务成功，但存在可接受瑕疵；
- C：不可用或关键内容受损；
- Skip：当前无法可靠判断、素材异常或评审者选择跳过，不进入评分分母。

Grill C 必须冻结 A/B/C 的可操作细则和失败原因字典，例如：

- 主体缺失；
- 人脸/人体破坏；
- 商品结构破坏；
- 文字缺失或乱码；
- Logo 破坏；
- 关键内容被裁切；
- 几何扭曲；
- 构图明显失衡；
- 边缘/合成瑕疵；
- 清晰度下降；
- 其他。

### 18.3 必报指标

至少报告：

- A Rate；
- A+B Rate；
- B Among Success；
- C Rate；
- Skip Count 与 Skip Rate；
- Any-method A / Any-method Success；
- Oracle A / Oracle Success；
- 自动 Top-1 A / Top-1 Success；
- Routing Regret；
- Bad Pass Rate；
- B Share 与 B Among Success；
- Protection/Judge Agent Call Rate；
- External AIGC Fallback Rate；
- Unnecessary AIGC Rate；
- 各方法覆盖率和失败率；
- 不同 scene_profile 的分层结果；
- 自动模式与人工指引模式的分离结果。

指标按开发阶段逐步启用，不得因自动排序器尚未完成而推迟四方法正式基线：

- **M0-M4 / 36 张第一轮正式基线**：至少报告各方法 A、A+B、C、Skip、技术完成率、Any-method/Oracle A、Any-method/Oracle Success、人工最佳候选分布、失败原因、Conservative False Reject、Dangerous False Pass、P50/P95 和峰值内存。
- **M5 以后**：在冻结候选上增加自动 Top-1、Routing Regret、Bad Pass、评分校准和不同 Selector 对照。
- **M7 以后**：增加 Agent 调用、改选、有益/有害改变、时延和成本。
- **M8 以后**：增加 AIGC Rescue、Hallucination、Protected-content Regression、技术/业务成功率和 Cost per Success。

第一轮正式基线的目标是回答“四种方法各自效果如何、合起来能覆盖多少任务、主要失败在哪里”，不是等待完整自动路由系统完成。

其中：

```text
Any-method/Oracle 成功
= 同一 Task 的候选集合中至少一个候选达到指定等级

Top-1 成功
= 系统实际选择的候选达到指定等级

Routing Regret
= Oracle 可成功但 Top-1 未成功的任务比例或数量
```

不要用 Any-method 的高成功率替代系统 Top-1 能力。

排序器不应只压成一个不可解释的 100 分。至少分别估计或保存 `P(A)`、`P(A+B)` 与 `P(C)`，先控制场景允许的 `P(C)` 上限，再在安全候选中优先最大化 `P(A)`；没有可靠 A 时才选择最好的 B，全部不可靠才进入回退。

### 18.4 场景自适应评价

至少支持三类策略：

- Precision：人物肖像、精细商品、Logo；
- Coverage：多人物、中文海报、复杂电商宣传页；
- Balanced：普通单主体、一般商品、风景。

需要在 Grill C 中确定：

- scene_profile 是人工标注、规则判断还是模型预测；
- 不同策略改变哪些指标权重；
- 哪些缺陷是一票否决；
- 权重变化是否会导致跨场景不可比较；
- 是否同时保存统一总分与策略分。

### 18.5 变换日志与视觉结论

四种方法至少记录：

- Direct Warp：`sx/sy`、`D_stretch`、重要区域纵横比变化；
- Crop：裁剪窗口、每个 P0/P1/P2/P3 区域保留率、按重要性加权的内容损失、主体边界距离；
- Seam：每条或每批 Seam、P0/P1 交叠、文字/人脸/商品边缘命中、累计位移、结构线变化、最终尺寸对齐；
- Mesh：顶点位移场、单元 Jacobian、翻折、局部横纵缩放/剪切、保护区刚性误差、直线弯曲。

但它们只是风险特征。最终质量必须结合重要区域损伤、视觉结果和人工评价。不能设置“变换超过某个数值就必然失败”的未经验证规则。

重点记录两类错误：

- `Conservative False Reject`：日志/规则认为危险，但人工认为 A/B；
- `Dangerous False Pass`：日志/规则认为安全，但人工认为 C。

### 18.6 Top-1 与全部备选的输出合同

标准决策必须同时返回自动结果和完整候选引用，例如：

```json
{
  "best_result": "mesh.webp",
  "alternatives": ["direct_warp.webp", "crop.webp", "seam.webp"],
  "selection_confidence": 0.88,
  "selector_id": "conditional_agent_v1",
  "agent_called": true,
  "aigc_used": false,
  "fallback_reason": null
}
```

若四种方法有失败，`alternatives` 只列有效候选，同时必须在 DecisionRecord 中引用完整的成功/失败记录。接口直接把四张全部给用户选择时，Any-method Success 很有业务价值；接口必须自动返回一张时，Top-1 Success 与 Routing Regret 才是自动化能力的核心指标。

### 18.7 生成式候选专项质量评价

Seedream 或自研生成式工作流除通用 A/B/C 外，必须保存单独的 `QualityDimensionRecord`。第一版维度至少包括：

| 维度 | 检查重点 | 典型严重问题 |
|---|---|---|
| 核心内容保真 | 主人物、商品、Logo、关键物体是否保持身份、数量和结构 | 主体改变、缺失、重复 |
| 未编辑区域一致性 | 不应变化的区域是否保持 | 背景或主体被无故重绘 |
| 幻觉与增删 | 是否凭空新增、删除或复制对象 | 幽灵人物、重复商品、多余物体 |
| 文字可靠性 | 核心文案、价格、品牌和字形是否完整可读 | 乱码、错字、漏字、Logo 文字变化 |
| 人脸/人体/商品几何 | 五官、肢体、商品轮廓、规则结构是否自然 | 局部结构异常、形状融化 |
| 边界与融合 | Mask、回贴和新旧区域边界是否自然 | 接缝、光晕、色差、硬边 |
| 构图与目标比例适配 | 是否真正完成目标比例重排 | 主体拥挤、大片无意义空白、重心失衡 |
| 清晰度与细节 | 局部纹理和分辨率是否稳定 | 模糊、过锐、纹理重复或融化 |
| 风格一致性 | 光照、色彩、材质和画面风格是否统一 | 局部风格突变、AI 感明显 |
| 业务可用性 | 是否可直接使用、轻修后使用或不可用 | 任何关键业务信息不可靠 |

每个维度建议记录 `PASS / MINOR / MAJOR / FAIL / UNKNOWN`、reason codes、证据区域和评审者/评价器版本。A/B/C 是业务总判定，不应通过简单平均掩盖一票否决项。核心人物、主商品、核心文字或 Logo 出现明确错误时，即使整体好看也不能判 A；是否直接判 C 由场景策略和业务规则确认。

生成式路线至少报告：

```text
AIGC Rescue Rate
= 传统四候选均失败的 Task 中，AIGC 达到 A/B 的比例

AIGC A Uplift
= 接入 AIGC 后端到端 Top-1 A Rate - 仅传统路线 Top-1 A Rate

AIGC Success Uplift
= 接入 AIGC 后端到端 Top-1 A+B Rate - 仅传统路线 Top-1 A+B Rate

Hallucination Rate
= 出现新增、删除、重复或幽灵主体的生成式 Candidate 比例

Protected-content Regression Rate
= AIGC 破坏原本受保护核心内容的生成式 Candidate 比例

External Technical Success Rate
= 成功得到尺寸正确且可解码结果的外部调用比例

External Business Success Rate
= 外部调用最终达到人工 A/B 的 Task 比例
```

技术成功率、候选质量成功率和端到端 Top-1 成功率必须分开。供应商 API 返回成功不等于图片业务成功；AIGC 生成了 A/B 也不等于 Selector 选中了它。

如果一个 Task 生成 K 个 seed 或 K 张图，还必须同时报告：

- 单次生成 A、A+B 成功率；
- `Best-of-K/Oracle` A、A+B；
- 自动选中 A、A+B；
- 每个成功 Task 的平均生成次数；
- 每个成功 Task 的真实费用和总时延；
- 固定 seed 的可复现性与供应商不可复现说明。

不同 K 不得只比较 Best-of-K 成功率。标准公平表必须并列候选预算、请求次数、像素/Token 计费量和 Cost per Success。

### 18.8 自动评价器与人工金标准

自动质量评价建议分层，而不是依赖单一审美模型：

1. 硬可验证检查：尺寸、解码、Alpha、全黑/全白、输出缺失、Mask 越界；
2. 专用一致性检查：OCR 文案、Logo/对象数量、主体相似性、人脸/关键区域、未编辑区域像素或特征一致性；
3. 几何与画质检查：结构线、局部形变、模糊、接缝和重复纹理；
4. 多模态 Judge：只在专用指标冲突或临界时进行整体业务判断；
5. 人工 A/B/C 与维度标签：作为最终业务金标准和版本晋级依据。

任何自动评价器也必须版本化，并在冻结候选上 Replay。评价器升级时要报告它相对人工标签的准确率、宏平均 F1、对 C 的召回、Bad Pass、分场景混淆矩阵和校准曲线，不能只报告与人工总分相关系数。

### 18.9 版本晋级、回滚与持续迭代门槛

每个方法、Agent 模型、Prompt、Provider、Workflow、Selector 和 Evaluator 都必须有稳定 ID、语义版本、配置哈希和回归结果。新版本只能在固定验证集通过后成为默认版本。

正式阈值由 Pilot 确认；在此之前至少遵守以下门槛：

1. 固定回归集不能出现新的 P0 核心内容破坏；
2. `Bad Pass Rate` 不得超过已确认业务上限；
3. Top-1 A 或 A+B 必须有可解释提升，不能只提高 Any-method/Oracle；
4. Agent 的 Beneficial Change 必须明显多于 Harmful Change；
5. AIGC 必须提高 Rescue Rate，并单独控制 Hallucination 和 Protected-content Regression；
6. P95 时延、峰值显存、吞吐、API 配额和 Cost per Success 不得突破预算；
7. 结果应按 `source_id` 分组计算置信区间或进行配对比较，不能把同图多尺寸当作独立样本夸大显著性；
8. 公司最终测试集不得参与阈值、Prompt、模型或工作流选择；
9. 未通过门槛的版本保留为实验版本，不覆盖当前默认；
10. 默认版本升级后仍保留上一稳定配置和产物索引，支持一键回放或配置回滚。

报告至少包含“基线 → 候选版本”的质量、风险、性能和成本差异，以及退化 Task 清单。不能因为总体平均提高而隐藏人物、文字、Logo 或复杂海报子集的明显退化。

---

## 十九、性能、资源与成本指标

从数据契约阶段就预留，但按里程碑逐步实现：

- wall-clock latency；
- CPU time；
- 峰值 RSS 内存；
- GPU 型号、数量和峰值显存；
- 冷启动与热启动；
- 模型加载时间与纯推理时间；
- 输入分辨率、输出分辨率；
- 成功、失败、超时和重试；
- API 调用次数；
- 输入/输出 Token 或图像计费单位；
- 估算费用与实际费用；
- 每任务成本；
- 每个成功任务成本；
- Agent 调用率；
- 外部方法调用率；
- 缓存命中率。

性能测试必须保存环境信息，并区分：

- 单图延迟与批处理吞吐；
- 模型已加载与未加载；
- CPU、单 GPU、双 GPU；
- 不同图像尺寸；
- 是否包含 I/O、预处理、后处理和模型加载。

未知数据记为 null/unknown，不得记为 0。

四种方法并行时，墙钟时延概念上为：

```text
T_total
= T_analysis
+ max(T_warp, T_crop, T_seam, T_mesh)
+ T_rule
+ I_protection * T_protection_agent
+ I_judge * T_judge_agent
+ I_fallback * T_external_generation_path
```

`T_external_generation_path` 可以是一个 Seedream 调用，也可以是自研 Workflow 后再进入另一个 Provider 的受控顺序回退；实际调用了几步就记录几步，不能只保留最后成功步骤。并行只降低墙钟时间，不减少 CPU 总消耗，因此还要记录 CPU core-seconds、线程数、P50/P95/P99、单张与批量吞吐、缓存命中/未命中、冷/热启动。

成本必须分三种口径：

1. **直接可变成本**：CPU/NPU 实际占用、Agent Token/推理、外部 AIGC、存储和网络；
2. **基础设施成本**：机器购买折旧或月租、空闲资源、电力/机房、常驻服务与监控；
3. **运营总成本**：直接成本 + 基础设施 + 人工评审/指引 + 维护。

最终报告 `Cost per Successful Image = 全部运营成本 / A+B 成功图片数`，并同时报告 `Cost per A`。低流量下不得只用边际推理秒数忽略独占常驻设备的固定成本。

对外服务和外部工作流还必须拆分记录：

```text
T_service_total
= T_request_validate
+ T_upload_or_materialize
+ T_queue_wait
+ T_analysis
+ T_candidates
+ T_agent
+ T_external_submit
+ T_external_queue
+ T_external_infer
+ T_external_download
+ T_postprocess
+ T_persist
+ T_response_serialize
```

只在对应阶段发生时计入，并保存 span/event；不得只给一个总耗时。对于异步接口，`POST` 返回 job 的接口延迟与 Job 完成总时延要分开。外部 Provider 至少统计：限流率、配额拒绝率、超时率、重试率、重复调用率、供应商技术成功率、下载失败率和业务成功率。

吞吐和并发测试至少覆盖：单任务、批量任务、2/4/8 并发的候选情景；具体并发值应按机器资源调整并记录。不能通过并发造成显存 OOM、API 重复计费或 SQLite 写锁后仍宣称吞吐提升。

---

## 二十、统一服务接口与外部 AIGC/自研工作流接入

### 20.1 两类“接口”必须分开

1. **内部插件接口**：`Analyzer`、`CandidateMethod`、`AgentPlugin`、`ExternalAIGCProvider`、`WorkflowBackend` 等，用于替换实现。
2. **对外应用接口**：`RetargetApplicationService` 及其 CLI、Streamlit、FastAPI Adapter，用于提交任务、查询结果、Replay、评审和人工指引。

FastAPI endpoint 不直接调用 OpenCV、Seedream 或 ComfyUI；它只校验请求、调用应用服务并返回 DTO。CLI 和 Streamlit 同样不得复制业务逻辑。

推荐调用关系：

```text
CLI / Streamlit / FastAPI
        ↓
RetargetApplicationService
        ↓
Runner / Replay / Review Use Cases
        ↓
CandidateMethod / Agent / Provider / WorkflowBackend
```

### 20.2 `RetargetApplicationService` 最小用例

应用层至少提供：

- `submit_retarget_job`：提交自动或指定实验模式的重定向任务；
- `get_job_status`：查询阶段、进度、错误与可恢复状态；
- `get_job_result`：返回 Top-1、全部有效备选、失败记录和指标引用；
- `cancel_job`：在安全边界内请求取消尚未完成的外部/工作流任务；
- `submit_evaluation_replay`：在冻结候选上运行新评价器、Selector 或 Judge；
- `submit_guided_run`：使用版本化人工指引创建新的 Generation Run；
- `append_review_event`：追加 A/B/C/Skip、最佳候选和失败原因；
- `list_capabilities`：列出已注册方法、Provider、Workflow、支持的输入和当前健康状态。

第一版可以在单进程中使用 SQLite + 文件存储 + 简单后台执行器，不必引入消息队列。接口协议仍按异步 Job 设计，以兼容 Seedream、ComfyUI 和远程模型的排队/轮询。CLI 可以提供 `--wait`，但不得因此让领域接口只能同步阻塞。

### 20.3 FastAPI 最小端点

端点名称可以在 ADR 中调整，但语义至少覆盖：

| 方法与路径 | 用途 |
|---|---|
| `POST /v1/retarget/jobs` | 提交源图、目标尺寸和运行策略，返回 `job_id` |
| `GET /v1/retarget/jobs/{job_id}` | 查询状态、阶段、进度和脱敏错误 |
| `GET /v1/retarget/jobs/{job_id}/result` | 读取 Top-1、全部备选、指标和回退信息 |
| `POST /v1/evaluation-replays` | 对冻结候选提交 Replay |
| `POST /v1/guided-runs` | 使用人工指引创建新 Generation Run |
| `POST /v1/reviews` | 追加人工评审事件 |
| `GET /v1/capabilities` | 查看方法、Provider、Workflow 与限制 |
| `GET /health/live` | 进程存活检查 |
| `GET /health/ready` | 存储和必需组件就绪检查；可选后端异常应显示 degraded，不必拖垮四候选核心 |

批量数据集运行仍优先使用 CLI；FastAPI 首版不必承载大型数据上传和分布式批处理。不得为了“有接口”一开始就建设网关、Kubernetes、消息队列或多租户计费。

### 20.4 请求协议

请求至少包含：

```json
{
  "request_id": "client-generated-idempotency-key",
  "source": {"artifact_id": "source_123"},
  "target": {"width": 1200, "height": 628, "format": "webp"},
  "run_mode": "traditional_all_four",
  "scene_profile": "auto",
  "guidance_id": null,
  "selector_id": "conditional_agent_v1",
  "external_policy": {
    "enabled": false,
    "provider_allowlist": ["seedream_api"],
    "workflow_allowlist": [],
    "max_outputs": 1,
    "max_cost": null,
    "allow_data_egress": false
  },
  "metadata": {}
}
```

需要支持上传文件与已登记 `artifact_id` 两种输入，但必须统一物化为受控 Artifact；不能让客户端提交任意服务器文件路径或 `file://` URL。远程 URL 输入若以后开放，必须经过域名、大小、MIME、超时和 SSRF 防护，首版可不支持。

推荐 `run_mode`：

- `traditional_all_four`：只运行四种传统候选；
- `conditional_fallback`：四候选 + 条件式 Agent + 受控外部回退；
- `external_benchmark`：明确指定 Provider/Workflow 的独立实验，不伪装成生产回退；
- `guided`：使用人工指引的新 Generation Run。

`methods` 不应由公网请求任意注入 Python 类名。只能选择服务端已注册并被配置允许的稳定 ID。外部 Provider、Workflow、最大输出数、费用和出域必须同时通过服务端策略，客户端请求不能自行绕过。

### 20.5 结果协议

结果必须返回 Top-1 加全部备选，并明确传统、Agent 与外部回退路径：

```json
{
  "job_id": "job_01",
  "task_id": "poster_0001__landscape_1200x628",
  "status": "COMPLETED",
  "best_result": {
    "candidate_id": "candidate_mesh_01",
    "method_id": "mesh",
    "artifact_id": "artifact_result_01",
    "grade_prediction": "A",
    "selection_confidence": 0.88
  },
  "alternatives": [
    {"candidate_id": "candidate_crop_01", "method_id": "crop", "artifact_id": "artifact_result_02"},
    {"candidate_id": "candidate_seam_01", "method_id": "seam", "artifact_id": "artifact_result_03"},
    {"candidate_id": "candidate_warp_01", "method_id": "direct_warp", "artifact_id": "artifact_result_04"}
  ],
  "failed_methods": [],
  "decision": {
    "selector_id": "conditional_agent_v1",
    "protection_agent_called": false,
    "judge_agent_called": true,
    "external_fallback_called": false,
    "reason_codes": ["metric_visual_conflict_resolved"]
  },
  "metrics_ref": "metrics_01",
  "run_id": "run_01",
  "replay_id": "replay_01"
}
```

服务响应不能暴露本地绝对路径、SSH 主机、内部 Provider ID、Token 或含敏感信息的原始错误。图片通过受控 `artifact_id`、本地应用可解析引用或以后确认的下载机制提供。

若外部回退被调用，`best_result` 可以引用 `external_seedream` 或已注册 Workflow 的候选；`alternatives` 仍保留所有有效传统候选和按策略允许展示的外部候选，`failed_methods` 则保存完整失败记录。不得用外部结果覆盖或删除四候选产物，也不得把 Provider 名伪装成 `crop/seam/mesh`。

### 20.6 `ExternalAIGCProvider` 契约

建议协议语义：

```python
class ExternalAIGCProvider(Protocol):
    provider_id: str
    provider_version: str

    def capabilities(self) -> ProviderCapability: ...
    def submit(self, request: ExternalGenerationRequest) -> ProviderJob: ...
    def get_status(self, job: ProviderJob) -> ProviderStatus: ...
    def fetch_outputs(self, job: ProviderJob) -> list[ProviderOutput]: ...
    def cancel(self, job: ProviderJob) -> CancelResult: ...
```

是否原生同步、异步、支持取消或幂等，由 capability 声明；Adapter 向平台提供统一语义。Provider 不得返回一个裸 URL 后结束：若 URL 会过期，应在授权条件下立即下载、校验、冻结并计算哈希。

统一请求至少包含：

- 输入 Artifact、目标宽高和格式；
- 可选 Mask、保护摘要、Prompt 模板版本和 Prompt 参数；
- seed、输出数量、质量/步数等提供方允许的受控参数；
- deadline、最大重试、最大费用；
- 素材出域策略和授权结果；
- `request_id / task_id / run_id` 及幂等键。

统一错误至少区分：

- `AUTH_ERROR`；
- `QUOTA_EXCEEDED`；
- `RATE_LIMITED`；
- `POLICY_BLOCKED`；
- `DATA_EGRESS_DENIED`；
- `INVALID_REQUEST`；
- `PROVIDER_UNAVAILABLE`；
- `TIMEOUT`；
- `OUTPUT_MISSING`；
- `OUTPUT_INVALID`；
- `COST_LIMIT_EXCEEDED`；
- `UNKNOWN_PROVIDER_ERROR`。

重试只适用于经过确认的临时错误，并使用退避和抖动；不能对内容政策拒绝、无效请求或费用超限盲目重试。若 Provider 不支持幂等，平台必须在 EventStore 中阻止同一逻辑请求因网络重试重复计费。

### 20.7 Seedream Provider 首版要求

实现 Seedream Adapter 时必须：

1. 以用户实际 API 文档、账户区域和可用模型为准，保存核对日期；
2. `provider_id` 建议为 `seedream_api`，具体模型和 API 版本另存，不塞进永久 ID；
3. Base URL、模型名、认证头和请求字段通过私有 ProviderConfig 映射；
4. API Key 只从环境变量或公司批准的密钥机制读取，不进入 YAML、日志和 Git；
5. 支持平台输入图、目标尺寸、Prompt、seed/输出数的能力映射；不支持的能力明确拒绝或降级，不能静默忽略；
6. 保存请求模板哈希、Prompt 版本、实际参数、供应商任务 ID 的脱敏引用、输出哈希和费用；
7. 区分提交失败、排队失败、生成失败、结果下载失败、解码失败和人工 C；
8. 只在 `conditional_fallback` 的四候选均不可靠时自动调用；`external_benchmark` 可直接调用但必须单独统计；
9. 默认 `allow_data_egress=false`；公司真实素材只有在明确合规授权时才允许调用；
10. 在相同任务上比较单次生成、Best-of-K、Top-1、Rescue Rate、Hallucination、P95 和实际 Cost per Success。

不要在没有真实 API 凭据和明确付费批准时发起调用。可以先用契约 fixture 或本地 fake server 验证协议，但必须标记为【协议已测试】，不能标记 Seedream【已测试】。

### 20.8 `WorkflowBackend` 契约

建议协议语义：

```python
class WorkflowBackend(Protocol):
    backend_id: str
    backend_version: str

    def capabilities(self) -> WorkflowCapability: ...
    def validate(self, spec: WorkflowSpec) -> ValidationResult: ...
    def submit(self, request: WorkflowRequest) -> WorkflowJob: ...
    def get_status(self, job: WorkflowJob) -> WorkflowStatus: ...
    def fetch_outputs(self, job: WorkflowJob) -> list[WorkflowOutput]: ...
    def cancel(self, job: WorkflowJob) -> CancelResult: ...
```

首版至少考虑三种 Backend：

- `local_python`：调用仓库内已注册、受契约约束的 Python Workflow；
- `comfyui_http`：通过 ComfyUI API 上传输入、提交版本化 JSON、轮询队列并取回指定输出；
- `remote_http`：调用用户在远程 GPU 上部署的自研模型/工作流服务。

每个 Workflow 必须有独立 `workflow_id / workflow_version`，并声明：

- 任务类型和支持的输入；
- 目标尺寸、Mask、文字资产或其他可选能力；
- 参数 schema 与默认值；
- 模型、custom nodes 和依赖清单；
- 工作流模板/代码哈希；
- 设备和资源需求；
- 超时、候选数和费用口径；
- 输出节点、格式和产物语义；
- 是否会把数据发送到外部服务。

工作流内部可以是“去文字 → 重排 → 主体/文字回贴 → 修补”等用户自研链路，但平台只通过声明的输入输出和血缘记录接入。若工作流产生多阶段图片、Mask 或文字资产，应分别冻结 Artifact，不能只保留最终图导致无法诊断。

### 20.9 配置示例

```yaml
service:
  api_enabled: true
  api_version: v1
  job_backend: sqlite
  max_upload_mb: 30

external_aigc:
  enabled: false
  providers:
    seedream_api:
      adapter: seedream
      base_url_env: SEEDREAM_BASE_URL
      api_key_env: SEEDREAM_API_KEY
      model_env: SEEDREAM_MODEL
      timeout_s: 180
      max_retries: 2
      allow_data_egress: false

workflows:
  enabled: true
  backends:
    comfy_relayout_v1:
      adapter: comfyui_http
      base_url_env: COMFYUI_BASE_URL
      workflow_path: configs/workflows/comfy_relayout_v1.json
      binding_path: configs/workflows/comfy_relayout_v1.bindings.yaml
    local_relayout_v1:
      adapter: local_python
      entrypoint: retarget_agent.workflows.local_relayout_v1

fallback:
  enabled: false
  order: [comfy_relayout_v1, seedream_api]
  require_all_traditional_unreliable: true
  max_outputs_per_task: 1
  max_cost_per_task: null
```

公开配置只保存环境变量名和非敏感默认值。真实 URL、Token、公司内部路径、额度和敏感工作流参数放在 Git 忽略的私有配置中。

### 20.10 接口安全、幂等与错误恢复

至少要求：

- 上传大小、像素数、MIME 和解码限制；
- 文件名不作为可信路径；
- 请求、任务和外部调用幂等；
- 超时、取消和断点恢复；
- 并发与费用上限；
- 外部 URL 和错误脱敏；
- 不在响应中返回服务器绝对路径；
- Provider/Workflow allowlist；
- 失败方法隔离；
- 任务状态追加式记录；
- Job 完成后结果可重取，不因客户端断线丢失；
- 可选后端故障时四候选基础服务仍可就绪；
- OpenAPI schema、示例请求和契约测试随代码版本发布。

首版身份认证、网关和公司统一鉴权方式需要在接入真实业务前确认；本地 Demo 可以只监听 loopback，但不得默认把无鉴权接口暴露到公网。

---

## 二十一、人工评审与人工指引

### 21.1 人工评审 MVP

Streamlit 第一版至少应：

- 显示源图和目标尺寸；
- 显示方法名；
- 显示 Top-1 和全部候选；
- 支持 A/B/C/Skip；
- 支持选择最佳候选；
- 支持多选失败原因和可选备注；
- 自动保存；
- 支持断点恢复；
- 支持修改旧评分但以新事件追加；
- 页面可滚动；
- 全屏时底部按钮可访问；
- 记录显示顺序；
- Skip 不进入最终评分分母。

显示方法名可能造成评审偏差，但这是用户当前明确需要。Grill C 必须记录方法名显示和候选顺序；可在后续讨论是否增加可选盲评模式，不得擅自取消方法名。

### 21.2 人工指引

至少考虑：

- `must_keep` 矩形；
- `prefer_keep` 矩形；
- `removable` 矩形；
- `target_anchor`；
- 后续可扩展多边形、点和分割 Mask。

人工指引必须记录：

- 创建者；
- 创建时间；
- 坐标系；
- 来源图哈希；
- 指引版本；
- 花费时间；
- 是否用于候选生成、排序或两者。

自动与指引实验必须分开运行或至少拥有明确 mode 字段，分别报告：

- 自动成功率；
- 指引后成功率；
- 人工挽救率；
- 平均指引时间；
- 哪类场景最值得人工介入。

---

## 二十二、输出目录与可回放要求

候选输出结构建议：

```text
runs/{run_id}/
├── run.json
├── events.sqlite
├── config/
├── candidates/
│   └── {task_id}/
│       └── {method_id}/
│           ├── candidate.png
│           └── candidate.json
├── analysis/
├── masks/
├── visualizations/
├── decisions/
├── replays/
└── reports/
```

需要在 Grill B 中审查最终结构，并在 Grill C 中冻结正式 Run 的目录和覆盖策略，但必须满足：

- 所有候选保留，不被 Top-1 覆盖；
- 结构化记录使用相对路径；
- 每个产物有哈希或可追溯引用；
- 决策与候选分离；
- Generation 和 Replay 使用不同 ID；
- 同一 Run 不静默覆盖；
- 中断后可以识别已完成、失败和待运行项；
- 配置、代码版本和依赖环境可追溯；
- 公司数据路径不会进入公开报告。

---

## 二十三、方法与实验递进里程碑

以下里程碑分为两条执行轨：

- **快速实验轨 M0-M4**：本提示词已一次性授权，连续完成并运行 12 张 Smoke；这是当前最高优先级。
- **增量能力轨 M5-M9**：获得四方法人工标签后按证据逐步增加，不阻塞首轮正式实验。

快速实验轨按以下主流程连续推进：

```text
Grill A 开工前轻量预检
→ M0 最小数据/插件契约
→ M1 接入 12 张 Smoke 数据
→ M2 四种真实候选全部生成
→ Grill B 自动契约审查并修复
→ M3 候选、日志、时延和统计落盘
→ M4 A/B/C/Skip 审图与断点恢复
→ 运行 12 张 Smoke 并修复
→ Grill C 冻结正式实验
→ 直接进入 36 张正式基线
```

Grill A/B/C 是快速实验轨内部的质量检查点，不是新增三个大型里程碑。不得为了 M5-M9 的完整设计扩张 M0-M4，也不得把 Grill 扩成完整生产架构评审。接口先稳定在最小可替换边界，细节可以在冻结候选和人工标签出现后增量演进。

### M0：仓库与数据契约

- 精简 `AGENTS.md`、`CONTEXT.md`；只有发生实质取舍时才写 ADR；
- Python 包骨架；
- 插件协议；
- Pydantic 数据对象；
- 配置加载；
- 注册表；
- 基础测试；
- `.gitignore`；
- CLI 入口骨架。

### M1：数据集与验证

- Folder/CSV `DatasetAdapter`；
- `dataset.yaml`、`sources.csv`、`targets.csv`、`tasks.csv`；
- 路径、图片、尺寸、ID、哈希、重复任务和 split 泄漏校验；
- dataset fingerprint；
- 2～3 张程序化单元测试图片与 12 张 Smoke 清单；
- 至少两个目标尺寸；
- `dataset validate` CLI；
- 接入新数据集无需修改代码。

### M2：确定性候选生成

第一批范围受本提示词的固定四方法定义约束，并由 Grill B 审查是否真实、公平和可回放；实现时建议拆成可验收的两个子阶段：

1. M2a 共享分析层：
   - `ImageMetadataAnalyzer`；
   - 对象/文字/Logo/显著性 Analyzer 的统一输出协议；
   - `must_keep / prefer_keep / removable / rigid_region`；
   - `ImportanceMap / ToleranceMap`；
   - 同一源图分析可被多个目标尺寸 Task 复用，但目标相关融合结果必须正确版本化。
2. M2b 四种固定候选：
   - `direct_warp`：非等比直接缩放；
   - `crop`：共享保护驱动的窗口搜索与等比缩放；
   - `seam`：保护式 Seam 与显式尺寸对齐；
   - `mesh`：带局部刚性和结构线约束的网格形变；
   - 每种标准输出一张主候选，并保存各自 transform log；
   - 没有可行解时返回 `UNSAFE` 或 `NEEDS_MANUAL_REVIEW`，不能伪装成功。

共同要求：四个方法插件注册、坐标变换可测试、同一 AnalysisArtifact、公平候选预算、中断恢复和缓存、单方法失败隔离。M2 可以分 PR 实现，但只有四种方法都是真实可运行实现时，才能宣称“四候选 M2 完成”；不允许用永远成功的假实现或组合算子代替缺失方法。

### M3：指标、回放和性能

- Generation Run；
- Evaluation Replay；
- StageTimer；
- CPU、内存、可选 GPU 显存；
- 冷启动/热启动；
- 错误和重试；
- 运行配置快照；
- 候选和日志可回放；
- 自动统计报告。

### M4：人工评审 MVP

- Streamlit；
- 源图、目标尺寸、方法名、Top-1 和全部候选；
- A/B/C/Skip；
- 最佳候选；
- 失败原因；
- 自动保存；
- 断点恢复；
- 页面滚动；
- 全屏按钮可访问；
- Skip 不进入评分统计；
- 评审修改采用追加事件。

### M0-M4 实验就绪验收

完成 Grill C 并满足以下条件，即进入 36 张第一轮正式基线，不再等待 M5-M9：

1. 12 张源图 × 2 个目标比例可形成 24 个合法 Task；
2. 每个 Task 都实际尝试 `direct_warp / crop / seam / mesh`，正常情况产生 96 个候选；单方法失败有明确状态且不阻塞其他方法；
3. 输出尺寸、方法 ID、参数、共享分析引用、transform log、运行配置、错误和阶段时延可追溯；
4. 四种方法不是占位图、复制图或永远成功的 mock；
5. UI 能显示源图、目标尺寸和方法名，完成 A/B/C/Skip、最佳候选、失败原因、自动保存、页面滚动和断点恢复；
6. Skip 不进入评分分母；旧候选可被重新统计，无需重新生成；
7. 自动产生 Smoke 摘要：候选生成完成率、各方法异常率、评审完成度、A/A+B、Any-method Success 和 P50/P95；Smoke 数值只用于查流程，不作为算法结论；
8. README 或运行文档提供从环境安装、数据校验、生成、启动 UI 到导出报告的可复制命令；
9. 相关单元/契约/集成测试通过；已知限制明确记录；
10. 36 张数据集的 manifest、冻结方式和启动命令已经准备好。
11. Grill A、Grill B、Grill C 均有可追溯产物；Grill B 不存在四方法真实性或公平性 FAIL，Grill C 对正式数据、方法版本、参数和评分口径给出 `PASS` 或不影响公平性的 `PASS_WITH_OPEN_ITEMS`。

如果 Smoke 仅有少量非阻塞失败，应先隔离失败 Task、记录问题并继续验证其余流程，再集中修复；不要因为单张异常推倒整个 MVP。若四方法中的某个实现系统性不可运行，则 M2 未完成，不能跳过该方法进入正式四方法比较。

### M5：硬检查与排序器

- 尺寸/解码、可验证核心内容缺失、网格翻折等真正硬失败；
- 裁剪量、Seam 数、位移、拉伸、Jacobian 等风险特征，不直接等同失败；
- Precision/Coverage/Balanced 的软评分模板；
- Oracle；
- Top-1；
- Any-method Success；
- Routing Regret；
- A Rate、A+B Rate、B Among Success、Bad Pass Rate；
- scene_profile 分层；
- 冻结候选上的排序器对比；
- transform log 作为特征而不是最终标签。

### M6：人工指引

- `must_keep`；
- `prefer_keep`；
- `removable`；
- `target_anchor`；
- 指引前后分开统计；
- 人工挽救率和指引时间。

### M7：Agent

- Runner 控制的状态机和三个受控职责点；
- 按需 Protection Agent：只对已有检测对象做语义优先级消歧；
- 按需 Judge Agent：对四张冻结候选排序、评级并识别日志—视觉冲突；
- FallbackDecision：选择传统 B、外部 AIGC、人工复核或失败；
- `all_outputs / hard_ranker / protection_agent_only / judge_agent_only / conditional_agent / always_on_agent` 实验模式；
- Prompt、结构化输入输出、模型、Token、费用和实际执行动作日志；
- 超时、解析失败、非法对象 ID 和费用超限时的确定性安全降级；
- Judge 选择能力 Replay 与 Protection Agent 新 Generation Run 分开；
- Agent 不得跳过四种方法、修改方法参数、扩候选或重试生成；
- Protection/Judge 调用率、Top-1 改变率、有益/有害改变率、Bad Pass、人工复核率与 Cost per Success。

### M8：外部 AIGC 与用户自定义方法接入

- 实现 `ExternalAIGCProvider`、`WorkflowBackend` 与两个通用 CandidateMethod Adapter；
- 验证第三方或用户自定义方法只通过 Provider/Backend 注册即可接入，不修改 Runner 主控制流；
- Seedream Provider：先通过 fixture/fake server 完成协议测试，取得凭据和付费批准后才允许真实 Smoke；
- 至少接入一种用户自研 WorkflowBackend：`local_python` 或 `comfyui_http`；远程 GPU 工作流优先部署为 `remote_http`；
- ComfyUI 保存模板 JSON、bindings、custom nodes/模型清单、版本和输出节点；
- 统一保存输入、输出、中间产物、版本、错误、性能、成本、幂等和素材出域决策；
- 外部方法失败时不影响其他候选；
- 外部方法与内置方法使用相同任务、评审等级和统计口径；
- Seedream 或其他生成式兜底只能在四种传统候选均不可靠且通过费用、配额、素材出域门禁时调用；
- 记录 AIGC Fallback Rate、Unnecessary AIGC Rate、Rescue Rate、Hallucination、Protected-content Regression、技术成功率、业务成功率、P50/P95、实际费用和每张成功图成本；
- 单次生成与 Best-of-K/自动 Top-1 使用相同候选预算口径；
- 文字或其他后处理能力只验证接口边界，不在本里程碑展开具体方案。

### M9：统一应用服务与 FastAPI

- `RetargetApplicationService` 成为 CLI、Streamlit 和 FastAPI 的共同应用层；
- 异步 `ServiceJobRecord`、状态查询、取消、断点恢复和结果重取；
- `POST /v1/retarget/jobs`、Job 状态/结果、Replay、Guided Run、Review、Capabilities 和 Health；
- 上传文件与 `artifact_id` 两类输入；禁止任意服务器路径；
- Top-1 + 全部备选 + 失败方法 + Decision/Metric 引用的稳定响应；
- OpenAPI schema、请求/响应示例、错误模型与版本策略；
- Provider/Workflow allowlist、幂等、超时、并发、费用和出域门禁；
- 可选外部后端不可用时，四候选基础服务仍能运行并显示 degraded；
- FastAPI endpoint 不包含算法和供应商业务逻辑；
- 本地 loopback Demo 和契约测试；真实公司鉴权与网关留待生产接入确认。

M0-M4 应一次性连续完成。M5-M9 不属于首轮四方法正式实验的前置条件；除非用户另行要求，否则不得在 Smoke 通过前优先开发 Agent、Seedream、ComfyUI、自研生成工作流或 FastAPI。

---

## 二十四、测试策略最低要求

设计和实现每个里程碑时都要定义验收测试。至少考虑：

1. 单元测试：ID、路径、哈希、schema、坐标转换、注册表；
2. 契约测试：每个插件对统一输入输出协议的遵守；
3. 集成测试：数据集校验到候选落盘的最小闭环；
4. 回归测试：固定小图和固定输出/指标；
5. 失败测试：损坏图片、缺失文件、错误哈希、方法异常、数据库锁、Agent 超时；
6. 跨平台测试：至少保证 Windows PowerShell 主路径；
7. UI 测试或人工检查清单：滚动、全屏、Skip、断点恢复、重复评分；
8. 数据泄漏测试：source_id 分组、路径逃逸、敏感路径和 Git 忽略；
9. 重放测试：Replay 不修改或重新生成 Candidate；
10. 可复现测试：固定 seed、配置和版本得到可解释结果；
11. Provider 契约测试：fake server 覆盖成功、排队、限流、超时、无效输出、过期 URL、重试和幂等；
12. Workflow 契约测试：local Python/ComfyUI 的能力校验、缺节点、缺模型、队列失败、中间产物和输出节点；
13. FastAPI 契约测试：OpenAPI、上传限制、Job 状态、Top-1 + alternatives、错误脱敏、取消和结果重取；
14. 安全测试：路径逃逸、任意 URL、Provider 绕过、费用/出域绕过、Prompt 注入和敏感字段泄漏；
15. 远程 Smoke：公开 fixture 上验证 SSH 部署后的 Agent/Workflow HTTP 健康检查、断连降级和 P50/P95；
16. 质量回归测试：传统与生成式维度标签、Hallucination、Protected-content Regression 和版本晋级门槛。

只有实际执行过的命令和结果才能标为【已测试】。如果因为环境原因未运行，应明确写【未测试】和原因。

---

## 二十五、GitHub、个人电脑与公司电脑分工

### 25.1 个人开发电脑

个人电脑是唯一开发端，负责：

- 修改代码和公开文档；
- 创建分支；
- 运行 Codex 和测试；
- 检查 Git Diff；
- Commit、Push、PR、合并和发布 Tag。

但 Codex 未经用户明确要求，不得自行 Commit、Push、创建 PR、合并或发布。

### 25.2 GitHub

GitHub 是代码与公开工程事实的基线，可保存：

- Python 代码；
- 测试；
- `AGENTS.md`；
- `CONTEXT.md`；
- ADR；
- 数据格式定义；
- 公开数据下载脚本；
- FastAPI/OpenAPI schema、接口示例和契约测试；
- Provider/Workflow Adapter 代码；
- 不含密钥、内部 URL 和受保护参数的 ComfyUI workflow 模板与 bindings；
- 自研 Python 工作流的通用代码、依赖说明和公开 fixture；
- 不含受保护内容的实验配置和报告；
- 小型、许可证允许再分发的 fixture；
- 通用技术方案、Review 和 Runbook。

不得保存：

- 公司真实图片；
- 公司内部 URL；
- Token、Cookie、密钥和账号信息；
- 受保护的内部接口和源码；
- 公司运行结果原图；
- 真实 Provider Base URL、API Key、额度、账单明细和内部模型服务地址；
- 含公司模型/节点路径或受保护节点参数的私有 Workflow 配置；
- `private_context/`；
- 本地大模型权重；
- 大型下载数据集；
- `runs/` 输出；
- 含公司素材的截图或日志。

即使仓库是 Private，也不得把受保护内容当作可随意上传。

### 25.3 公司电脑

公司电脑是只读测试端：

- 只下载 `main` 上稳定 Release 或指定 Tag；
- 只安装依赖和运行程序；
- 只在仓库外准备公司测试数据；
- 只生成本地运行结果和评审结果；
- 不修改源代码；
- 不创建开发分支；
- 不 Commit；
- 不 Push；
- 不把公司素材、内部路径和含素材日志上传 GitHub。

公司电脑默认不得把真实素材发送到 Seedream、个人远程 GPU、公共 ComfyUI 或其他外部服务。只有公司合规和用户明确授权、且 ProviderConfig 的 `allow_data_egress` 门禁通过时才允许外部调用。公司内部批准的模型服务也应通过私有 Provider/Workflow 配置接入，不把内部地址提交 Git。

公司电脑可以在仓库外创建 dataset manifest、guidance 和 runs，因为这些属于测试输入输出，不等于修改源代码。

公司发现问题后，只向开发端传递允许外传的脱敏信息，例如：

- 软件版本；
- dataset_id；
- task_id；
- 执行命令；
- 错误类型；
- 脱敏日志；
- 预期与实际差异；
- 不包含受保护素材的最小复现条件。

如果截图或日志含公司素材，只保留在公司环境。

---

## 二十六、Git 忽略要求

请规划 `.gitignore`，至少忽略：

```text
.env
.venv/
__pycache__/
*.pyc
local_data/
private_context/
runs/
models/
checkpoints/
*.pt
*.pth
*.ckpt
*.safetensors
```

还应覆盖：

- SQLite 临时文件；
- Streamlit 本地状态；
- 测试缓存；
- 覆盖率输出；
- 构建产物；
- IDE 本地文件；
- OS 临时文件；
- 本地密钥与凭证；
- Provider 私有配置、API 调用原始响应和账单缓存；
- ComfyUI/远程 Workflow 的本地上传缓存、队列产物和含敏感路径的配置覆盖；
- 大型数据集与下载缓存。

不要忽略：

- `AGENTS.md`；
- `CONTEXT.md`；
- `docs/`；
- `configs/`；
- `src/`；
- `tests/`；
- `.agents/skills/`，除非用户后来明确决定技能不进入仓库；
- 数据格式模板；
- 小型且允许再分发的测试 fixture。

---

## 二十七、快速预检包与后续完整文档

### 27.1 Grill A 开工前快速预检包

开始编码前只需在终端和精简文档中确认：

1. 当前仓库、分支、未提交修改和现有代码的真实状态；
2. 可复用的 Warp、Crop、Seam、Mesh 或评审 UI 是否存在，以及许可证/来源；
3. Smoke 输入路径、输出路径、12 张图片来源和目标比例；
4. 公司受保护素材、密钥、内部地址和输出的隔离方式；
5. Python 版本与 CPU 可运行环境；
6. M0-M4 的最小交付、默认值、已知风险和至多 3 个阻塞问题。

将上述结果写入 `docs/discovery/grill-a-preflight.md`。Grill A 为 `PASS` 或 `PASS_WITH_OPEN_ITEMS` 后立即进入 M0；尚未影响 M0-M4 的问题标记为【待验证】，不要等待回答。

### 27.2 随项目增量维护的完整信息

下列内容仍需维护，但按相关里程碑逐步补齐，不作为 Smoke 前置文档：

- `docs/discovery/grill-b-contract-audit.md` 与 `docs/discovery/grill-c-experiment-freeze.md`；
- 四方法、共享分析、数据对象、Generation/Replay/Review 和人工评审；
- 自动指标、Top-1、Oracle、Routing Regret 和版本晋级；
- 人工指引；
- Protection/Judge Agent、模型矩阵与 SSH；
- Seedream、WorkflowBackend、生成式质量评价；
- `RetargetApplicationService`、FastAPI、错误和权限协议；
- 性能、成本、隐私、Git、公司电脑测试和生产集成。

文档中的结论必须标记为【已确认】【待验证】【候选方案】或【存在冲突】。默认值必须可配置、可追溯、可在后续 Replay 或新 Generation Run 中替换。

---

## 二十八、执行边界与连续推进规则

本提示词已经授权轻量 M0-M4 和 12 张 Smoke，无需用户再次发送批准短句。开始后：

1. 读取 `AGENTS.md`、`CONTEXT.md`、必要技能说明和 Git 状态；
2. 执行 Grill A，给出不超过一屏的预检结果与执行顺序；
3. Grill A 未阻塞时直接实施 M0-M2；
4. M2 的 2～3 张 fixture 跑通后执行 Grill B，以自动测试和代码证据审查四方法真实性、公平性和可回放性；
5. Grill B 的局部 FAIL 直接修复并复查，通过后连续推进 M3-M4；
6. 使用真实可运行代码和真实测试，不用 mock 候选冒充四方法完成；
7. 每个检查点简短汇报证据，但不等待批准；
8. M4 后立即运行 12 张 Smoke，修复阻塞问题并复跑；
9. Smoke 通过后执行 Grill C，冻结 36 张数据、目标比例、方法/参数版本、A/B/C/Skip 和正式实验报告口径；
10. Grill C 通过后生成实验就绪报告，并直接启动用户已经提供数据的 36 张正式基线；
11. 不替用户 Commit、Push、创建 PR 或调用付费/出域服务，除非用户明确要求；
12. 不在 Smoke 前自行扩大到 M5-M9。

当用户只提供部分真实图片时，先用已有图片和程序化 fixture 完成流程，不要空等完整数据；但正式 36 张结论必须使用冻结的正式 manifest，不能混入临时 Smoke 图片后假装同一数据版本。

---

## 二十九、你现在应执行的第一组动作

现在按以下顺序开始，并持续做到实验就绪：

1. 只读检查工作目录、Git 状态、当前分支、最近提交、已有代码、配置、测试、数据和 `.agents/skills/`；
2. 识别现有四方法与评审 UI 的可复用程度，区分【已实现】【已测试】【候选方案】【未测试】；
3. 执行 Grill A，输出简短预检并写入 `docs/discovery/grill-a-preflight.md`：仓库事实、M0-M4 实施顺序、默认值、风险和至多 3 个阻塞问题；
4. Grill A 未阻塞时立即创建最小项目骨架与数据契约，不等待用户回复；
5. 接入数据集验证与 12 张 Smoke manifest；
6. 接入并真实运行 Direct Warp、Crop、Seam、Mesh，保存候选和 transform log；
7. 在 2～3 张 fixture 上执行 Grill B，写入 `docs/discovery/grill-b-contract-audit.md`，修复四方法真实性、契约、公平性、失败隔离和可回放问题；
8. 接通 Generation、Replay、StageTimer、统计和 Streamlit A/B/C/Skip 评审；
9. 运行测试与 12 张 Smoke，修复失败并复跑；
10. 执行 Grill C，冻结正式数据、目标比例、方法/参数版本和评分口径，写入 `docs/discovery/grill-c-experiment-freeze.md`；
11. 输出实验就绪报告：三次 Grill 状态、完成项、测试命令与结果、Smoke 数量、失败项、已知限制、正式实验命令；
12. 若 Grill C 通过、36 张正式数据已就绪且不存在合规或成本门禁，继续生成第一轮正式四方法候选；若尚未就绪，停在“代码已实验就绪”，只请求缺失的数据路径或 manifest。

首次回复不需要提出 6～10 个问题，也不需要等待多轮需求发现。Grill A/B 默认自动推进；Grill C 只有发现会影响正式实验统计的核心冲突时才暂停。除非命中暂停门禁，否则在同一任务中开始真实实施。

现在开始执行，目标是尽快看到可评审的四方法真实图片和第一张统计表。

# 提示词正文结束

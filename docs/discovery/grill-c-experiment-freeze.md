# Grill C：正式实验冻结门禁

> 检查时间：2026-08-10（Asia/Shanghai）  
> 依据：V7、实际全局 `grilling` SKILL、`retarget_smoke_real_hd_v1` 与 Run `smoke-real-hd-v1-20260810`  
> 结论：`BLOCKED`

`BLOCKED` 只阻止 36 张第一轮正式实验，不回滚已经完成的 M0-M4 或真实 Smoke
Generation。当前不存在四方法真实性、候选预算、可回放性、技术失败或许可证不明问题；
阻塞来自正式统计所必需的人工标签与正式数据尚未冻结。

## 已冻结的事实

1. 标准方法集与显示顺序固定为 `direct_warp / crop / seam / mesh`，每个 Task 各尝试一次主候选；方法名显示，技术 Top-1 标为未校准。
2. 四方法版本均为 `1.0.0`，共享同一个 AnalysisArtifact；当前 Smoke 参数冻结在 `configs/smoke_real_hd.yaml`，任何变更都必须产生新 config hash、Run ID 和重新冻结记录。
3. `shared_protection:2.0.0` 在 required 模式运行 gradient/contrast/center 显著性、PPOCRv3+中文 CRNN、YuNet、YOLOX 和 Logo 候选检测。模型资产逐项固定许可证、URL、SHA-256 与字节数；12 个源图分析均无降级 warning。Logo 能力是区域保护，不宣称品牌身份识别。
4. 方法参数固定草案：Direct Warp Lanczos；Crop grid 48、scales 1.0/0.94/0.88；Seam max 24、protection 18、tolerance 3；Mesh 12×12、protection gain 1.8、minimum cell fraction 0.25。
5. 运行目录按 Run ID 追加；已有 Run 不静默覆盖。Candidate 冻结后，Replay 与 Review 使用独立 ID/事件，不能重新生成后冒充同一候选。
6. 当前高清真实 Smoke 数据集 ID 是 `retarget_smoke_real_hd_v1`；旧 `retarget_smoke_real_v1` 和程序化 fixture Run 只保留为历史技术证据，不进入当前高清审图统计。
7. 高清 Smoke fingerprint 为 `3c90bf434a6588297fb30109e5e910564c9a9d1e9f008ea9694c57e626faedfa`；12 张来源均有逐图官方许可与 SHA-256 审计，目标尺寸为 1024×1024、1536×800、864×1536，每图选择两个非平凡比例。
8. 高清 Smoke Generation 为 24/24 Task、96/96 候选尝试、0 FAILED，Run contract audit `PASS`；Replay `smoke-real-hd-replay-v1` 已从冻结候选成功产生。

## A/B/C/Skip 与评审口径草案

- **A**：重要人物、商品、文字/Logo 和结构均保留，比例与构图没有明显不可接受问题，可直接用于目标画布。
- **B**：核心内容可用，但存在轻微裁切、尺度、布局、形变或接缝问题，需要小幅人工修正。
- **C**：核心内容丢失、文字/Logo 破坏、人物/商品明显变形、结构弯曲、可见接缝或构图错误，不能使用。
- **Skip**：样本或评审条件不足以形成有效质量判断；不进入 A/B/C 评分分母，也不算成功或失败。
- 每位 reviewer 对每个候选保留一个当前有效事件；修改采用新事件 `supersedes` 旧事件，不修改历史行。
- 每个 Task 最多一个最佳候选，且最佳候选必须为 A 或 B；显示顺序与 `method_name_visible=true` 一并记录。
- C 可多选失败原因：`content_cutoff`、`text_or_logo_damage`、`person_or_product_distortion`、`structure_bending`、`layout_imbalance`、`important_content_too_small`、`visible_seam_or_artifact`、`wrong_target_composition`、`technical_failure`、`other`。

正式报告草案固定包含：各方法技术完成率与异常率、A、A+B、C、Skip、评分完成度、
Top-1 A/Success、Any-method/Oracle A、Any-method/Oracle Success、人工最佳方法分布、失败
原因、Candidate P50/P95 与峰值 RSS。Skip 只报告数量，不进入评分分母。Smoke 数值只验证
流程，不作为算法结论。

## Smoke 暴露的问题与处理

- 原 `cn-poster-01` 虽许可明确，但缩略图人工检查发现中文文字密度不足；已在任何真实 Run 启动前用作者 Own-work、CC BY-SA 3.0 的中文活动海报替换，并生成新的 dataset fingerprint。
- 96 个候选无系统性技术失败。候选总览显示 Crop 与形变方法存在可见差异，四方法不是占位图或复制图。
- 视觉总览也表明极端比例下存在真实构图与形变取舍；这需要 A/B/C 人工标签量化，不能由自动技术成功率替代。

## 阻塞正式 36 张实验的核心项

1. **高清真实 Smoke 人工评审尚未完成。** 当前 `0/96` 高清候选有人工 A/B/C/Skip 事件，因此 A、A+B、Any-method Success、最佳候选分布和失败原因仍为空。新版 Streamlit 页面已做自动测试和真实浏览器视觉验收，但必须由实际 reviewer 完成审图后重新生成报告。
2. **`retarget_baseline36_v1` 数据未提供/冻结。** 当前没有 36 张正式源图、逐图许可证审计、SHA-256、72 个目标 Task 或 dataset fingerprint。已准备 `datasets/retarget_baseline36_v1/README.md` 和 `configs/baseline36.example.yaml`，但不得把占位模板称为正式 manifest，也不得混入 Smoke 或 fixture 后启动 288 候选。

## 通过条件与下一条命令

完成真实 Smoke 人工审图并提供/物化 36 张审计数据后：

```powershell
.\.venv\Scripts\retarget-agent.exe review ui runs\smoke-real-hd-v1-20260810
.\.venv\Scripts\retarget-agent.exe report runs\smoke-real-hd-v1-20260810
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_baseline36_v1
.\.venv\Scripts\retarget-agent.exe run generate configs\baseline36.example.yaml
```

只有重新检查确认人工统计非空、正式 dataset fingerprint 固定且无许可/计数冲突后，Grill C
才能改为 `PASS` 或不影响公平性的 `PASS_WITH_OPEN_ITEMS`。当前不得启动 36 张正式 Run。

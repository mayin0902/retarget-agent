# retarget-agent Context

## Purpose

`retarget-agent` 是一个小内核、插件化、可回放、可审计的图片重定向实验平台。当前目标是先建立四种确定性方法的真实候选生成与人工评审闭环，再依据冻结候选和人工证据扩展排序器、Agent、外部 AIGC 与服务接口。

## Ubiquitous language

- **Source**：一张源图及其稳定 `source_id`、哈希和来源记录。
- **Target**：目标画布规格，宽在前、高在后。
- **Task**：一个 Source 到一个 Target 的重定向任务；`task_id = source_id__target_id`。
- **AnalysisArtifact**：同一 Task 的四方法共享且版本化的保护分析；包含区域、ImportanceMap 与 ToleranceMap 引用。
- **Candidate**：某个方法对某个 Task 的一次冻结输出；技术成功不等于业务 A/B。
- **Generation Run**：固定数据、配置、代码、分析和 seed 的候选生成。
- **Replay**：读取冻结候选重新评价或选择；不得重新生成候选。
- **Decision**：从完整候选集合中形成的一次 Top-1 选择及其证据。
- **Review**：对冻结 Candidate 的追加式人工 A/B/C/Skip 事件。
- **Any-method/Oracle**：同一 Task 至少有一个候选达到指定等级；不等于 Top-1 成功。
- **ImportanceMap**：像素或区域的保留代价。
- **ToleranceMap**：像素或区域对删除、压缩和形变的容忍程度。
- **must_keep / prefer_keep / removable / rigid_region**：硬保留、软保留、优先可删除、尽量保持局部刚性的区域语义。

## Current invariant

标准 Run 固定尝试 `direct_warp`、`crop`、`seam`、`mesh`，各一张主候选。四方法使用同一 `AnalysisArtifact` 和输出尺寸合同；失败记录属于候选集合的一部分，不能静默跳过或伪装成功。

程序化图片只属于 `tests/fixtures`，必须记录 `fixture_type` 和测试目的；它们不能进入真实 Smoke 或正式实验统计。真实 Smoke 的唯一数据集 ID 是 `retarget_smoke_real_v1`。

## Current evidence (2026-08-10)

- Grill A：`PASS_WITH_OPEN_ITEMS`；Grill B：`PASS_WITH_OPEN_ITEMS`。
- M0-M4 轻量闭环已实现：数据校验、四个真实方法、Generation、Replay、计时/内存、报告、Streamlit/FastAPI A/B/C/Skip 追加评审和断点恢复。
- `retarget_smoke_real_hd_v1`：12 个逐图许可审计的 Wikimedia Commons 高清小样本，24 Task；Run `smoke-real-hd-v1-20260810` 完成 96/96 方法尝试，contract audit `PASS`，无技术失败。旧低清 Run 只保留为历史技术证据。
- 共享保护分析已接入本地 OCR、人脸、商品/对象和 Logo 候选检测；FastAPI Review Adapter 已实现。Ruff 通过，pytest `28 passed`（Python 3.13.9）；Python 3.11 尚未在本机实测。
- Grill C：`BLOCKED`。真实 Smoke 人工评分仍为 0/96，且 `retarget_baseline36_v1` 的 36 张正式数据、许可审计和 fingerprint 尚未提供/冻结，因此不得启动正式 288 候选 Run。

## Current non-goals

当前仍不实现学习式排序、产品 Agent、Seedream、ComfyUI、生产鉴权、分布式调度或大规模训练。FastAPI 当前只承载本机单 Run 人工评审，不等于 M9 的完整异步 Job 服务已经完成。

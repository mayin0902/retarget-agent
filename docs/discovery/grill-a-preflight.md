# Grill A：开工前轻量预检

> 检查时间：2026-08-10（Asia/Shanghai）  
> 结论：`PASS_WITH_OPEN_ITEMS`  
> 适用范围：轻量 M0-M4 与 `retarget_smoke_v1`

## 仓库事实

- 【已确认】Git 根目录是 `G:/Projects/retarget-agent`，当前为尚无 Commit 的初始 `main` 分支；远端是 `https://github.com/mayin0902/retarget-agent.git`。
- 【已确认】开工前除 `.git/` 外仅有 `docs/prompts/retarget-agent-codex-master-prompt-v7.md`；没有 `AGENTS.md`、`CONTEXT.md`、Python 包、配置、测试、数据或运行产物。
- 【已确认】现有工作区只有未跟踪的 `docs/`；不存在需要保留或兼容的旧实现。
- 【不存在】`direct_warp`、`crop`、`seam`、`mesh` 与 Streamlit 评审 UI；因此不存在可继承的实现、测试结果或源码许可证结论。
- 【已确认】V7 正文第 7-2639 行已完整读取。全局 `grilling` 的实际 `SKILL.md` 已读取，本次用“事实调查 → 决策树 → 当前前沿”组织 Grill A/B/C；V7 明确授权的安全默认值替代旧式逐轮等待。
- 【待验证】`setup-matt-pocock-skills` 文件存在但未暴露为本轮可调用技能，且声明 `disable-model-invocation: true`。本仓库直接采用 V7 已确认的 GitHub issue tracker 与 single-context 布局，不声称该技能已执行。

## 环境事实

- 【已确认】Windows 11；CPU 为 Intel Core i9-13900HX（24 核/32 线程），内存约 16 GB。M0-M4 只依赖 CPU 路径。
- 【已确认】默认解释器是 `D:/miniconda/python.exe`，Python 3.13.9；本机没有 Python 3.11，`uv` 未安装。
- 【候选方案】创建仓库内 `.venv`，使用现有 Python 3.13 完成本轮实测；项目声明 Python `>=3.11,<3.14`。Python 3.11 兼容性保留为后续 CI/环境验证项，不能在本轮标为已测试。
- 【候选方案】使用 Pydantic、PyYAML、Pillow、NumPy、OpenCV、psutil、Typer、Streamlit 与 pytest。算法实现由本仓库从零编写，不复制其他仓库代码；安装后记录解析版本。

## Grill 决策树与安全默认值

1. **仓库与长期上下文**
   - 【已确认】创建精简 `AGENTS.md` 与根 `CONTEXT.md`；Issue tracker 默认为 GitHub，领域文档采用 single-context。
2. **四候选真实性与公平性**
   - 【已确认】每个 Task 固定尝试 `direct_warp / crop / seam / mesh`，各输出一张主候选，消费同一版本 `AnalysisArtifact`；某方法失败不得阻塞其他方法。
   - 【候选方案】Direct Warp 使用非等比重采样；Crop 使用保护/显著性加权窗口搜索；Seam 使用逐接缝动态规划与显式最终尺寸对齐；Mesh 使用单调受约束网格和分片映射。四者必须保存不同且可检查的 transform log。
3. **共享分析**
   - 【候选方案】M0-M4 使用图像元数据、梯度/对比度显著性与可选数据集矩形标注形成 `must_keep / prefer_keep / removable / rigid_region`、`ImportanceMap` 和 `ToleranceMap`。不存在检测器时明确记录降级来源，不把空分析解释成“没有重要内容”。
4. **Smoke 数据与安全**
   - 【已确认】不扫描、复制或上传其他项目/公司素材；不调用外部 API。
   - 【候选方案】在 `local_data/retarget_smoke_v1` 程序化生成 12 张非敏感图片，覆盖海报、商品、多元素、多人物、肖像、风景/建筑等流程压力场景；每张生成两个差异明显的目标比例，共 24 Task/96 次方法尝试。
   - 【已确认】`local_data/` 与 `runs/` 默认 Git 忽略；程序化生成脚本和 manifest schema 可版本化，运行图片及输出不提交。
5. **评审与可回放**
   - 【已确认】A/B/C/Skip、最佳候选、失败原因和显示顺序作为追加式事件保存；Skip 不进入评分分母。
   - 【已确认】Generation、Replay 和 Human Review 使用分离 ID/记录；同一 Run 不静默覆盖。
6. **执行顺序**
   - 【已确认】M0 → M1 → M2 → Grill B → M3 → M4 → 12 张 Smoke → Grill C；不提前实现 M5-M9。

## 风险与开放项

| 状态 | 项目 | 当前处理 |
|---|---|---|
| 【待验证】 | Python 3.11 不在本机 | 在隔离的 3.13 环境实测；文档明确 3.11 尚未测试。 |
| 【待确认】 | 仓库项目许可证尚未选择 | 不擅自添加项目 LICENSE；依赖和实现来源单独记录。 |
| 【待确认】 | `retarget_baseline36_v1` 图片、哈希与许可证审计尚未提供 | 不阻塞 M0-M4/Smoke；Grill C 只能冻结模板并在正式 Run 门禁处明确状态。 |
| 【待验证】 | 简化显著性、Seam 预算和网格约束的业务质量 | 通过 Smoke 检查流程与失败模式，不把 Smoke 自动指标当作算法效果结论。 |

## 阻塞问题

无。当前没有素材出域、付费调用、SSH 写入、不可逆操作或四候选定义冲突。

## 结论

`PASS_WITH_OPEN_ITEMS`。开放项不影响本轮代码正确性、数据安全或四候选 Smoke 的可比性，立即进入 M0-M2；所有【已测试】状态必须由本仓库实际命令和输出产生。

## 2026-08-10 更正：真实 Smoke 定义

- 【已被替代】上文把 12 张程序化图片作为 `retarget_smoke_v1` 的决定，只适用于当时的技术闭环默认值，不再满足真实场景 Smoke 定义。
- 【已确认】程序化图片只属于 `tests/fixtures` 下的单元、契约、回归和算法压力测试；`runs/grill-b-mini-v1` 保留为 Grill B 技术证据，但不得进入真实 Smoke 审图或质量统计。
- 【已确认】真实 Smoke 的唯一数据集 ID 改为 `retarget_smoke_real_v1`，必须包含 12 张真实世界、非敏感、逐图许可证可审计的公开图片，并使用新的 Run ID 产生 24 Task/96 次方法尝试。
- 【已确认】旧 Run、旧 Candidate 和原有 fingerprint 不删除、不覆盖；更正通过新数据版本、新配置与新 Run 追加实现。

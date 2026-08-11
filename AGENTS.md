# retarget-agent 工作约定

## 开始前

1. 读取 `CONTEXT.md`、相关 `docs/adr/`、`docs/discovery/` 和 Git 状态。
2. `docs/prompts/retarget-agent-codex-master-prompt-v7.md` 是当前主执行基线。
3. 不从其他仓库继承实现、测试状态或实验结论；迁移前必须获得明确授权。

## 当前范围

- 快速实验轨：Grill A → M0-M4 → 12 张 Smoke → Grill C。
- 标准 Generation Run 对每个 Task 固定尝试 `direct_warp`、`crop`、`seam`、`mesh`。
- 四方法消费同一版本 `AnalysisArtifact`，单方法失败不得阻塞其他方法。
- `tests/fixtures` 的程序化图片只用于单元、契约、回归和压力测试，不得计入真实 Smoke。
- 真实 Smoke 数据集固定使用 `retarget_smoke_real_v1`：12 张真实世界、非敏感、逐图许可证可审计的公开图片；其指标仍只用于检查流程，不作为正式算法质量结论。
- M5-M9 不得在 Smoke 前抢跑；只保留不会污染核心协议的最小边界。

## 事实与状态

- 只把存在的代码标为【已实现】，只把实际运行且有命令输出的内容标为【已测试】。
- Generation、Evaluation Replay 和 Human Review 必须分开记录。
- transform log 是风险证据，不是最终视觉质量结论。
- Any-method/Oracle 与系统 Top-1 必须分开报告。

## 数据与安全

- 公司素材、密钥、内部 URL、模型权重和含敏感内容的运行产物不得进入 Git。
- `local_data/`、`private_context/`、`runs/`、模型缓存和私有配置默认忽略。
- 外部 API、素材出域、SSH 写操作和付费调用必须另行明确批准。
- 路径进入 manifest 前使用数据集根目录下的相对 POSIX 路径；拒绝绝对路径、`..` 和逃逸符号链接。

## 工程与测试

- Python 支持范围为 3.11-3.13；当前机器的实际测试版本必须记录。
- CLI、Streamlit 和未来 FastAPI 复用 `RetargetApplicationService`，界面层不得复制算法逻辑。
- 新方法通过 `CandidateMethod` 注册，不修改 Runner 的四方法主控制流。
- 修改后运行相关单元/契约/集成测试；里程碑结束记录命令、结果、失败和未测试项。
- 未经用户明确要求，不 Commit、Push、创建 PR、Merge、Rebase 或删除分支。

## Agent skills

### Issue tracker

Issue tracker 使用 GitHub；尚未授权时只读取，不创建或修改 issue。详见 `docs/agents/issue-tracker.md`。

### Triage labels

使用默认五类 triage label。详见 `docs/agents/triage-labels.md`。

### Domain docs

采用根 `CONTEXT.md` + `docs/adr/` 的 single-context 布局。详见 `docs/agents/domain.md`。

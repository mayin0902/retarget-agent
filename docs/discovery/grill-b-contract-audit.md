# Grill B：M2 四候选契约审查

> 审查时间：2026-08-10（Asia/Shanghai）  
> 审查 Run：`runs/grill-b-mini-v1`  
> 数据：3 张程序化 Source、6 Task、24 次方法尝试  
> 结论：`PASS_WITH_OPEN_ITEMS`

## 事实证据

```powershell
.\.venv\Scripts\python.exe -m pytest -q
# 15 passed in 24.10s

.\.venv\Scripts\retarget-agent.exe audit runs\grill-b-mini-v1
# status: PASS；10 项自动契约检查全部 PASS
```

- 【已测试】数据 fingerprint：`f22dc3a29053da7b8f0778e225b29b0a97989f68b16b65ce8837117b8f05f82c`。
- 【已测试】6 个 Task 均产生 4 条 CandidateRecord，共 24/24；没有 FAILED。
- 【已测试】Direct Warp、Seam、Mesh 各 6 个 `SUCCESS`；Crop 为 2 个 `SUCCESS`、4 个 `UNSAFE`。`UNSAFE` 仍保留尺寸正确的候选与“无法包含全部 must_keep”的证据，未伪装为安全成功。
- 【已测试】24 个候选的图片哈希、可解码性、目标尺寸、transform 哈希和方法 ID 全部通过。
- 【已测试】每个 Task 的四个 Candidate 共用且只引用一个 `analysis_artifact_id`。
- 【已测试】每个 Task 的四张输出哈希均为 4/4 不同；没有复制图、占位图或改名后的同一输出。
- 【已测试】故障注入令 Seam 对 2 个 Task 全部抛错，Run 得到 2 个 FAILED 和 6 个有效候选，验证单方法失败隔离。
- 【已测试】同一 `run_id`、同一 config 与 dataset 重复运行时复用现有 Candidate，图片 mtime 不变；config 或 dataset fingerprint 变化会拒绝复用。
- 【已测试】CLI、Runner、SQLite 事件、文件存储和后续 UI 共用 Pydantic Candidate/Run/Decision/Review 契约。

## 方法真实性与公平性

| 检查 | 状态 | 证据 |
|---|---|---|
| 固定四方法 | PASS | `direct_warp / crop / seam / mesh` 每 Task 各一次。 |
| Direct Warp 语义 | PASS | OpenCV 非等比重采样，记录 `sx/sy/D_stretch/anisotropy`。 |
| Crop 语义 | PASS | 枚举多尺度/多锚点目标比例窗口，以 Importance 与 must_keep 约束选择，再等比缩放。 |
| Seam 语义 | PASS | 动态规划逐条寻找梯度 + Importance - Tolerance 的低能量接缝，实际删除后再显式尺寸对齐。 |
| Mesh 语义 | PASS | Importance/Tolerance 加权的单调矩形网格分配，OpenCV remap；记录网格、Jacobian 与 foldover。 |
| 共享分析 | PASS | 四方法消费同一 Task 的同一 NPY ImportanceMap/ToleranceMap 与 RegionRecord 集合。 |
| 候选预算 | PASS | 标准 Run 每方法固定一张；参数搜索没有混入。 |
| 状态语义 | PASS | 技术产出与业务质量分开；`SUCCESS` 仅表示尺寸/解码成功，Crop 约束冲突为 `UNSAFE`。 |
| 失败隔离 | PASS | 自动故障注入测试通过。 |
| 回放基础 | PASS | config、依赖、Python、输入/输出哈希、分析、transform、Candidate、Decision 与事件可追溯。 |
| 外部边界污染 | PASS | Provider/Workflow/PostProcessor 仅有无供应商字段的 Protocol；未调用外部服务。 |

## 视觉抽查

【已测试】人工查看 `poster-price-logo__wide-256x134` 的四张候选：

- Direct Warp 显示明显的全局纵向压缩；
- Crop 保持标题几何，但裁掉价格区域，并正确标为 `UNSAFE`；
- Seam 在背景分散删除后仍有显式最终对齐风险；
- Mesh 对不同网格区间分配不同宽度，结果与 Direct Warp、Seam 均不同。

该抽查只证明实现路径和失败语义真实，不代表算法质量达到 A/B。

## 修复记录

1. 初始 lint 发现长行与未使用导入，已修复并复跑 Ruff。
2. 增加自动 `audit` 命令，验证候选预算、哈希、尺寸、transform、共享分析、非占位输出和 Decision 引用。
3. 增加故障注入与重复 Run 测试，覆盖失败隔离和不覆盖候选。

## OPEN 项

| 状态 | 项目 | 为什么不阻塞 Smoke |
|---|---|---|
| 【已关闭】 | 共享分析缺少完整 OCR、人脸与商品/Logo 区域检测。 | `shared_protection:2.0.0` 已在 `smoke-real-hd-v1-20260810` 以 required 模式运行 PPOCRv3+中文 CRNN、YuNet、YOLOX 与 Logo 候选检测；12 个源图均有统一 analyzer ID 且无降级 warning。 |
| 【待验证】 | Seam 每轴有预算，极端比例会显式执行最终非等比尺寸对齐。 | 预算、实际 seam 数和最终 anisotropy 已落盘，不冒充纯 Seam。 |
| 【待验证】 | Mesh 是保持水平/竖直网格线的可分离单调网格，不是通用 ARAP 求解器。 | 它是真实空间变化 Mesh，且网格/Jacobian/foldover 可审计；业务效果交给人工评审。 |
| 【待验证】 | `technical_risk_v1` 未经人工标签校准。 | 仅用于 M4 导航，Decision 明示 `uncalibrated_technical_risk_only`；不作为 M5 路由结论。 |

## 结论

`PASS_WITH_OPEN_ITEMS`。没有四方法真实性、公平候选预算、失败隔离、输出合同或可回放方面的 FAIL；M3-M4、高清 12 张 Smoke 与完整保护检测已经完成，剩余 OPEN 项仍按各自边界处理。

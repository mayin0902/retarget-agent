# Real Smoke run `smoke-real-v1-20260810`

> 执行日期：2026-08-10（Asia/Shanghai）  
> 数据集：`retarget_smoke_real_v1`  
> dataset fingerprint：`77a449cfec707de9b68746765d44e1a6cd047f5582a8ec60a08201397c38cb0d`

## 数据与来源审计

- 真实图片 12 张、Task 24 个、固定方法尝试 96 次。
- 场景分层：中文密集文字海报 2、单商品 2、多商品商业混合 2、多人物 2、人物肖像 1、风景/建筑/结构线 1、复杂困难图 2。
- 许可证：Public Domain 2、CC BY 4.0 2、CC BY-SA 2.0 1、CC BY-SA 3.0 1、CC BY-SA 4.0 6；12/12 允许修改和再分发，0 项许可证不明。
- 每张图片均保存官方 File 标识、固定下载 URL、官方来源、许可证、访问日期、SHA-256、场景、文件名、再分发状态、作者、署名、权利边界和尺寸。
- 图片位于 Git 忽略的 `local_data/retarget_smoke_real_v1/images/`；Git 只保存 materializer、manifest、研究和署名说明。
- 物化后的人工总览发现原 `cn-poster-01` 中文文字密度不足；正式运行前改为作者以 CC BY-SA 3.0 发布的 `2012大连冬聚海报.jpg`。预视觉物化文件保留在本地备份目录，没有覆盖任何 Run。
- 每个 Source 从 square 1:1、wide 1.92:1、portrait 0.5625:1 中选择相对原图最远的两个比例；24 个目标的最小对数比例压力为 0.288，大于 0.25 门槛。

## 实际命令与结果

```powershell
.\.venv\Scripts\python.exe scripts\materialize_real_smoke.py
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_smoke_real_v1
.\.venv\Scripts\retarget-agent.exe run generate configs\smoke_real.yaml
.\.venv\Scripts\retarget-agent.exe audit runs\smoke-real-v1-20260810
.\.venv\Scripts\retarget-agent.exe replay run runs\smoke-real-v1-20260810 --replay-id smoke-replay-v1
.\.venv\Scripts\retarget-agent.exe report runs\smoke-real-v1-20260810
```

结果：

- Dataset validation：`valid=true`，24 Task，0 error，0 warning。
- Generation：`COMPLETED`，24/24 Task，96/96 方法尝试，失败候选 0。
- Run contract audit：`PASS`；96/96 输出的哈希/尺寸与 transform 合同通过；24/24 Task 共享同一分析且四候选均为 4/4 不同字节输出。
- Replay：`smoke-replay-v1` 成功读取 96 个冻结候选，没有重新生成或覆盖候选。
- 四方法技术完成率均为 100%，异常率均为 0。
- 候选 wall time：P50 `0.0483s`，P95 `0.7421s`；峰值 RSS `178,618,368 bytes`；CPU 基线，无 GPU 调用。
- Streamlit 直接加载真实 Run：0 页面异常、4 个候选评分控件、3 个底部操作按钮；追加事件、编辑 supersedes、Skip 分母和断点恢复另有自动测试。

## 视觉与评审状态

- 源图总览：`local_data/retarget_smoke_real_v1/source_overview.png`。
- 24 Task 候选总览：`runs/smoke-real-v1-20260810/visualizations/smoke_overview.png`。
- 自动视觉检查确认每个 Task 的 Direct Warp、Crop、Seam、Mesh 均有可见输出；Crop 与形变方法存在明确构图差异，四方法并非占位或同图复制。
- 本轮没有把模型视觉检查冒充人工 A/B/C。当前真实 Run 的人工评审完成度是 `0/96`，因此 A、A+B、Any-method Success 和最佳候选分布均不得报告为质量结论。
- 旧 `runs/grill-b-mini-v1` 与其他程序化 fixture 结果只作为技术测试证据，不纳入本报告的真实 Smoke 审图统计。

## 已知限制

- 共享保护分析仍是 M0-M4 的梯度/对比度/中心先验，不是完整 OCR、人脸、商品或 Logo 检测。
- `technical_risk_v1` 未校准，只用于生成链路 Top-1 展示，不是 M5 路由器或算法质量结论。
- CC 图片中的人物、商标和广告元素仅限本地算法 Smoke；公开候选、缩略图或 Run 需重新做发布场景权利审查。
- 本机实际测试 Python 3.13.9；Python 3.11 尚未在本机实测。

## 最终代码验证

```powershell
.\.venv\Scripts\ruff.exe check src tests scripts
.\.venv\Scripts\python.exe -m pytest -q
```

结果：Ruff `All checks passed`；pytest `22 passed in 19.25s`。

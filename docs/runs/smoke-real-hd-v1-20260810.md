# smoke-real-hd-v1-20260810

> 日期：2026-08-10（Asia/Shanghai）  
> 数据集：`retarget_smoke_real_hd_v1`  
> Run 状态：`COMPLETED`  
> Contract audit：`PASS`

## 目的

替代旧 216–384px Smoke 候选作为人工审图对象；旧 Run 不删除、不覆盖，只保留为
低分辨率技术证据。新 Run 同时把共享保护分析从轻量显著性升级为本地完整检测管线。

## 冻结输入与输出

- 12 张真实世界公开图，场景计数保持 2/2/2/2/1/1/2。
- source audit：12/12 官方来源与许可证已复核，0 项 license unclear。
- dataset fingerprint：`3c90bf434a6588297fb30109e5e910564c9a9d1e9f008ea9694c57e626faedfa`。
- 24 Task、96 候选；`direct_warp/crop/seam/mesh` 各 24 次。
- 96/96 有可解码 PNG，0 FAILED；每 Task 4/4 输出哈希不同。
- 尺寸分布：16 张 1024×1024、44 张 1536×800、36 张 864×1536。
- Crop：10 SUCCESS、14 UNSAFE；UNSAFE 是 must-keep 约束冲突证据，不是异常退出。
- Replay：`smoke-real-hd-replay-v1` 成功。

## 共享保护检测证据

所有 12 个源图使用同一组 analyzer ID，且 AnalysisArtifact warning 为空：

- `face_yunet:8f2383e4dd3c`
- `text_ppocrv3:03f550c6b406`
- `text_crnn_cn:c760bf82d684`
- `object_yolox:c5c2d13e59ae`
- `logo_candidate_cv:2.0.0`

按 12 个唯一源图去重统计：OCR text 211、人脸 44、人物 25、商品 13、其他目标 3、
Logo 候选 114。OCR 产物包含识别字符串、检测置信度、识别置信度与四边形；人脸包含
框和五点坐标；目标包含 COCO class/semantic type；Logo 候选只表示需保护的紧凑视觉
标识区域，不表示品牌身份识别。

## 性能与质量边界

- Candidate wall time：P50 0.315s，P95 7.877s。
- peak RSS：2,145,308,672 bytes；CPU 基线，无 GPU 指标。
- 1940 年《孟丽君》海报官方原图仅 310×450；输出画布是高清尺寸，但不能恢复源文件
  不存在的细节，UI 与数据说明均明确该限制。
- 0/96 人工评分；技术完成率不能替代 A/B/C 视觉质量结论。

## UI 视觉验收

- Streamlit 组件测试通过；真实浏览器 1280×720 视口无横向溢出。
- body 字号 18px、font weight 500；主标题约 42px。
- 候选为 2×2 卡片；首任务 1024×1024 PNG 以约 324×324 清晰下采样显示，不再放大
  低分辨率候选。
- C 级选择会启用失败原因；底部保存/上一条/下一条始终可见。
- 修复主题 font weight 后，浏览器 console 0 error / 0 warning。
- 后续 FastAPI Review Web Adapter 已接入同一 `RetargetApplicationService`；桌面基础字号
  17px、候选原图 1024/1536 级直出，支持全屏、下载、本机草稿自动保存与追加式提交。
- FastAPI 页面在桌面、768px 和 390px 视口完成真实浏览器验收，无横向溢出或 console
  error；该验收未向真实 Run 提交测试评分。

## 实际命令

```powershell
.\.venv\Scripts\python.exe scripts\materialize_analyzer_models.py
.\.venv\Scripts\python.exe scripts\materialize_real_smoke_hd.py
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_smoke_real_hd_v1
.\.venv\Scripts\retarget-agent.exe run generate configs\smoke_real_hd.yaml
.\.venv\Scripts\retarget-agent.exe audit runs\smoke-real-hd-v1-20260810
.\.venv\Scripts\retarget-agent.exe replay run runs\smoke-real-hd-v1-20260810 --replay-id smoke-real-hd-replay-v1
.\.venv\Scripts\retarget-agent.exe report runs\smoke-real-hd-v1-20260810
```

## 当前门禁

Grill C 仍为 `BLOCKED`，但只因为真实 reviewer 尚未完成 96 个候选评分，以及
`retarget_baseline36_v1` 未冻结。高清生成、完整保护检测和评审 UI 不再是阻塞项。

最新回归：`ruff check src tests scripts` 全通过；`pytest -q` 为 `28 passed`。

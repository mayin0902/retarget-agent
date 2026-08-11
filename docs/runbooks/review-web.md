# 本地网页评审 Runbook

## 启动

在项目根目录执行：

```powershell
.\.venv\Scripts\retarget-agent.exe review web runs\smoke-real-hd-v1-20260810
```

终端出现 `Review website: http://127.0.0.1:8765` 后，用浏览器打开该地址。结束评审服务时
回到终端按 `Ctrl+C`。不要用 `0.0.0.0` 暴露到网络；当前工具没有生产级登录和权限控制。

## Reviewer 操作顺序

1. 输入固定 Reviewer ID；同一 ID 会恢复自己的最新非 superseded 评分。
2. 先看源图，再逐一全屏检查四张候选；技术 Top-1 不是标准答案。
3. 每张显式选择 A、B、C 或 Skip。C 必须至少选择一个失败原因。
4. 只有 A/B 候选可以选为任务最佳；没有合格候选时保持“不选择”。
5. “仅保存”停在当前任务；“保存并进入下一任务”会追加事件并继续。

页面卡片读取 Run 中的原尺寸文件，不生成低清缩略图。浏览器显示的是等比缩放预览；可用
“全屏查看原图”或“下载高清原图”检查文字、人脸、商品轮廓与细线。

## HTTP 接口

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/health/live` | 进程存活 |
| GET | `/health/ready` | Run 与媒体就绪状态 |
| GET | `/v1/review-workspace?reviewer_id=...` | 脱敏任务、候选和断点评分 |
| POST | `/v1/reviews` | 完整追加一个 Task 的四候选评分 |
| GET | `/v1/media/sources/{task_id}` | 受控源图读取 |
| GET | `/v1/media/candidates/{candidate_id}` | 受控候选读取 |

交互式接口说明位于 `/api/docs`。媒体端点只接受当前 Run 中已索引的稳定 ID，不接受绝对
路径、相对路径或远程 URL。

## 存储与恢复

评分、原因和备注的未提交草稿会实时自动保存在当前浏览器；刷新或意外关闭后可恢复。点击
保存后，完整 Task 评分写入 Run 的 `events.sqlite`，编辑会创建带 `supersedes_event_id` 的
新事件，不覆盖旧事件。切换任务前页面会提示是否放弃本机草稿；服务停止后，用相同命令、
浏览器和 Reviewer ID 即可恢复。

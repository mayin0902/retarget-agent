# ADR 0002: 单 Run、本机优先的 Review Web Adapter

- 状态：Accepted
- 日期：2026-08-11

## 背景

Streamlit 已证明 A/B/C/Skip 追加式评审闭环可用，但大图密度、响应式布局、精细交互和
接口复用受到限制。真实 Smoke 已完成 24 Task、96 个高清候选生成，当前需要让 Reviewer
以清晰、可恢复、可审计的网页完成评分。

## 决策

新增 `create_review_app(run_dir)` 作为 FastAPI Review Adapter 的唯一公共入口。一个进程只
绑定一个冻结 Generation Run：

1. 浏览器通过同源 `/v1/review-workspace` 读取脱敏后的任务 DTO；
2. 图片只能通过 Task ID 或 Candidate ID 访问，客户端不能传服务器路径；
3. `/v1/reviews` 只校验请求 DTO，然后调用 `RetargetApplicationService.save_task_reviews`；
4. A/B/C/Skip、最佳候选、失败原因、supersedes 和 SQLite 追加规则继续由 Review Use Case
   维护，网页不成为第二份事实源；
5. 前端使用仓库内原生 HTML/CSS/JavaScript，无 CDN、Node 构建或外部字体依赖；
6. CLI 默认监听 `127.0.0.1`。非回环地址没有生产鉴权，不作为部署方案。

## 结果

- Streamlit 保留为兼容 Adapter；FastAPI 网页成为人工 Smoke 评分的推荐入口。
- 媒体文件保留在 Git 忽略的 Run 目录，HTTP 响应使用固定 SHA-256 ETag。
- 这只完成 M9 中的本地 Review Web Adapter 切片，不代表异步重定向 Job、上传、鉴权、
  Provider/Workflow 服务化或生产部署已经完成。


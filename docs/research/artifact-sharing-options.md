# Smoke 数据与运行产物共享方案：GitHub Release 与 Hugging Face Dataset

> 调研日期：2026-08-11
> 范围：仅比较 GitHub Release 与 Hugging Face Dataset；容量判断使用已知本地规模，不对本地文件内容作额外推断。
> 已知规模分两个口径：全部 `runs/` 约 2.0 GiB、1178 个文件；单个重点 HD Run 约 1.85 GiB、535 个文件；`local_data/` 约 31.4 MiB、73 个文件。核心样本为 `retarget_smoke_real_hd_v1` 的 12 张真实图片、24 个 Task、96 个候选。

## 结论

两种平台在容量上都能承载这些资产，但不应把所有内容放到同一个地方：

1. **12 张真实源图、任务比例、来源/许可证/哈希审计：推荐 Hugging Face Dataset。** 这是可浏览、可版本化、可被程序加载的图像评测小数据集，符合 Dataset Hub 面向社区复用的数据语义。
2. **冻结的完整 Smoke Run、96 个候选、报告和必要日志：推荐 GitHub Release。** 将其作为与代码 Commit/Tag 对齐的运行证据快照，而不是塞进普通 Git 历史。
3. **不推荐把全部 `runs/` 原样上传为 1178 个 Release 附件。** GitHub 每个 Release 最多 1000 个附件；而且单附件必须小于 2 GiB。全部 `runs/` 的文件数超过附件数边界、总量也略高于单附件边界，必须先清理并归档。单个重点 HD Run 约 1.85 GiB/535 文件，理论上可做成一个 `<2 GiB` 的归档，但必须以归档后的实际字节数为准；拆成两个独立归档更稳妥。
4. **不推荐把整个 `runs/` 当作 Hugging Face Dataset。** 运行日志、事件库、中间缓存和调试资产不是可复用的数据集样本。只有当 96 个候选与人工标签被整理成稳定的 benchmark schema 后，才适合另建一个结果/偏好数据集。

最终建议采用：

```text
GitHub 代码仓库
├── 代码、配置、下载脚本、manifest、许可证审计、Run Markdown 报告
├── 链接到 Hugging Face Dataset 的不可变 revision
└── 链接到 GitHub Release 的 Tag 与 SHA-256

Hugging Face Dataset: retarget_smoke_real_hd_v1
└── 12 张源图 + 24 个目标比例任务 + 每图来源/许可证/哈希元数据

GitHub Release: smoke-real-hd-v1-20260810
└── 已清理的完整 Run，多包归档 + SHA256SUMS + 恢复说明
```

## 平台限制与适用语义

### GitHub Release

GitHub 将 Release 定义为基于 Git Tag 的、可供他人使用的“可部署软件迭代”，并明确建议使用 Release 分发不宜进入普通 Git 的大文件。[GitHub：About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)、[GitHub：About large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

截至调研日，官方硬边界是：

- 每个 Release 最多 **1000 个附件**；
- 每个附件必须 **小于 2 GiB**；
- Release 的**总大小和带宽使用没有官方限额**。[GitHub：Release storage and bandwidth quotas](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases#storage-and-bandwidth-quotas)

普通 Git 对超过 50 MiB 的文件发出警告，阻止超过 100 MiB 的文件；GitHub 建议仓库最好小于 1 GB，并强烈建议小于 5 GB。因此，无论是约 1.85 GiB 的重点 HD Run，还是约 2.0 GiB 的全部运行目录，都不应直接进入代码仓库历史。[GitHub：About size limits on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#about-size-limits-on-github)

Git LFS 虽然技术上可用，但 GitHub Free/Pro 的单文件上限为 2 GB，Team 为 4 GB，Enterprise Cloud 为 5 GB；它还把二进制生命周期耦合到代码仓库。对一次性冻结的 Run，Release 比 LFS 更合适。[GitHub：About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)

若代码仓库为私有仓库，只有具有仓库读取权限的人能够查看 Release；Release 不是私有仓库中的独立公开下载区。要公开共享而继续保持当前代码仓库私有，应使用独立的公开仓库或 Hugging Face 公共 Dataset。GitHub 官方说明“任何具有仓库读取权限的人”可以查看 Release。[GitHub：Who can view releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases#about-releases)

**对本项目的判断：**

- 单个重点 HD Run 的 535 个文件虽未超过 1000 附件上限，但逐文件上传不利于完整性校验和恢复；建议清理后打成一个经实测 `<2 GiB` 的归档，或更稳妥地拆成两个约 0.9–1.0 GiB 的独立归档。
- 若分享全部 `runs/`，1178 个文件不能逐个作为 Release 附件；建议拆成多个约 1.0–1.5 GiB 的独立归档。归档后只需少量附件，不会触及 1000 附件限制。
- Release 应绑定产生该 Run 的确切代码 Commit/Tag，并在说明中写明 Run ID、数据集 fingerprint、方法版本、生成命令和恢复命令。
- 建议上传独立的 `SHA256SUMS`；GitHub Release Asset API 本身也返回 `digest`、大小和下载计数，但项目自己的校验文件更便于离线验证。[GitHub：REST API endpoints for release assets](https://docs.github.com/en/rest/releases/assets)

建议的 Release 附件结构：

```text
retarget-smoke-real-hd-v1-run-tasks-001-012.tar.zst
retarget-smoke-real-hd-v1-run-tasks-013-024.tar.zst
retarget-smoke-real-hd-v1-run-metadata.tar.zst
SHA256SUMS
RESTORE.md
```

每个包都应可独立解包；不建议使用必须集齐所有分片才能解开的裸二进制切片。创建 Release 时，官方 GitHub CLI 支持把多个文件直接附加到指定 Tag。[GitHub CLI：`gh release create`](https://cli.github.com/manual/gh_release_create)

### Hugging Face Dataset

Hugging Face Dataset 是带 Git 版本历史的数据仓库，面向数据发现、浏览、加载和社区复用；Hub 的 Xet 后端对大二进制做分块和去重。[Hugging Face：Repositories](https://huggingface.co/docs/hub/en/repositories)、[Hugging Face：Upload files to the Hub](https://huggingface.co/docs/huggingface_hub/en/guides/upload)

截至调研日，官方容量与结构边界是：

- 免费用户/组织：公共存储为 **best-effort**，私有存储包含 **100 GB**；PRO 公共存储最多含 10 TB、私有存储含 1 TB 后按量付费。公共免费存储在最初几 GB 之后要求内容具有真实社区价值，并不构成无限容量保证。[Hugging Face：Storage plans](https://huggingface.co/docs/hub/en/storage-limits#storage-plans)
- 模型和数据集没有单仓库总大小硬上限，但会计入账号总存储额度。
- 官方建议每仓库少于 100,000 个文件；**单目录最多 10,000 个文件**；建议单文件小于 200 GB，单文件硬上限为 500 GB。
- HTTP 上传时建议每次 Commit 少于 100 个文件；`upload_folder()` 和 `hf upload` 会自动拆分大文件夹提交并支持中断后重跑。[Hugging Face：Repository limitations and recommendations](https://huggingface.co/docs/hub/en/storage-limits#repository-limitations-and-recommendations)、[Hugging Face：Upload a large folder](https://huggingface.co/docs/huggingface_hub/en/guides/upload#upload-a-large-folder)

已知的 31.4 MiB/73 文件、单个重点 HD Run 的约 1.85 GiB/535 文件，以及全部 `runs/` 的约 2.0 GiB/1178 文件，都远低于 Hugging Face 的文件数和存储边界，也在免费私有 100 GB 配额内；因此**技术容量不是阻碍，数据语义和再分发权才是决策重点**。

Hugging Face 官方建议：小型图像数据集直接保留原图最实用，可用 `metadata.csv`、`metadata.jsonl` 或 `metadata.parquet` 将文件名与标签、框、说明等元数据关联；WebDataset 主要用于大规模图像流式访问。12 张图片无需打成 WebDataset。[Hugging Face：Image Dataset](https://huggingface.co/docs/hub/en/datasets-image)、[Hugging Face：Uploading datasets](https://huggingface.co/docs/hub/en/datasets-adding#file-formats)

建议的数据集结构：

```text
README.md                 # Dataset Card、范围、预期用途、限制
data/images/              # 仅含许可允许再分发的 12 张源图
metadata.jsonl            # 一图一行：来源、许可、哈希、场景等
tasks.jsonl               # 24 个目标比例 Task
sources.csv               # 官方来源与许可证审计
SHA256SUMS
```

Dataset Card 应记录许可、数据来源、创建过程、预期用途、局限和潜在偏差；其 YAML 元数据可以声明 license、language、size 等字段。[Hugging Face：Dataset Cards](https://huggingface.co/docs/hub/en/datasets-cards)

可见性选择：

- **公开 Dataset**：适合许可证明确允许再分发、希望其他人复现和复用的 12 图 Smoke；按受支持的图像+元数据结构可获得 Dataset Viewer。
- **私有 Dataset**：适合先做内部审核；其他用户访问会得到 404，组织仓库成员按组织权限访问。免费账号有 100 GB 私有存储，但私有数据的 Data Studio 仅对 PRO、Team 或 Enterprise 开放。[Hugging Face：Repository visibility](https://huggingface.co/docs/hub/en/repositories-settings#repository-visibility)、[Hugging Face：Data Studio availability](https://huggingface.co/docs/hub/en/datasets-adding#data-studio)
- **Gated Dataset**：适合公开展示 Dataset Card、但要求用户登录并提交联系信息后才允许下载的研究数据；可自动或人工审批。Gating 是访问控制，不会赋予原本不存在的再分发权。[Hugging Face：Gated datasets](https://huggingface.co/docs/hub/en/datasets-gated)

上传工具应使用当前官方推荐的 `hf upload` 或 `HfApi.upload_folder()`；`hf_xet` 已默认集成，提供分块去重、并行上传和可恢复重跑。旧的 `upload_large_folder()` 已弃用，不应为本项目新写脚本。[Hugging Face：Upload files to the Hub](https://huggingface.co/docs/huggingface_hub/en/guides/upload)

## 资产级决策

| 资产 | GitHub Release | Hugging Face Dataset | 推荐 |
|---|---|---|---|
| 12 张真实源图 | 能放，但不便按样本浏览和查询 | 与图像 Dataset 语义高度匹配 | **HF Dataset** |
| 24 个目标比例 Task | 可作为 Release 元数据 | 可作为 `tasks.jsonl`，与源图稳定关联 | **HF Dataset** |
| 96 个生成候选 | 适合作为冻结 Run 的证据 | 只有整理成带方法、参数、评分标签的 benchmark 后才适合 | **当前放 Release** |
| 报告、审计、环境摘要 | 适合绑定代码 Tag | 可只保留与样本相关的精简元数据 | **Release + Git 内 Markdown** |
| 日志、事件库、调试中间资产 | 清理敏感字段后可选择性打包 | 不符合 Dataset 样本语义 | **仅必要部分放 Release** |
| 经人工评分的候选与偏好标签 | 可随 Run 冻结 | 若 schema 稳定且允许公开，可另建评测/偏好 Dataset | **完成审计后再决定** |

## 上传前门禁

以下条件未全部满足时，不应执行公开上传：

1. **逐图再分发核对**：每张图片的 `official_source`、`source_url`、`license`、`access_date`、`sha256` 与 `redistribution_status` 齐全，且 `redistribution_status` 明确允许目标平台上的再分发。仅“可公开访问”不等于“可重新托管”。
2. **许可义务落地**：需要署名、保留声明或 ShareAlike 的图片，应在 Dataset Card、`sources.csv`、归档内说明中满足对应要求；多许可证数据集不要用一个宽泛的顶层许可证掩盖逐样本差异。
3. **派生物审计**：候选图来自源图变换，仍需检查原图许可对派生和再分发的要求；私有或 gated 可见性不是缺失许可的补救措施。
4. **运行内容清理**：排除绝对本机路径、用户名、访问令牌、请求头、缓存、模型权重、无关中间文件；检查 SQLite/JSONL/日志中的 Reviewer ID、备注和潜在个人信息。
5. **完整性和复现**：生成 `SHA256SUMS`，记录代码 Commit、数据集 revision/fingerprint、Run ID、任务数、候选数、生成命令、解包/恢复命令。
6. **实际边界复核**：对归档后的每个 Release 附件重新测量字节大小，确保严格 `<2 GiB`；不要依据源目录约 1.85/2.0 GiB 的估算判断压缩包是否合规。
7. **先私有试传**：先创建 Draft Release 或私有 Dataset，下载回本地验证哈希、目录结构和 README，再决定公开。

## 明确不推荐

- 不把 `runs/`、`local_data/` 取消忽略后直接提交普通 Git。
- 不把全部 `runs/` 的 1178 个文件逐个挂到同一个 Release；重点 HD Run 的 535 个文件也应归档后发布，而不是逐附件上传。
- 不把全部约 2.0 GiB 的 `runs/` 打成一个包并依赖压缩率“碰线”；单个重点 HD Run 若采用单包，也必须确认归档成品严格小于 2 GiB。
- 不将缓存、虚拟环境、模型权重或未经筛选的事件数据库混入共享包。
- 不因 Hugging Face 有 100 GB 私有额度，就把非数据集性质的所有运行垃圾放进 Dataset 仓库。
- 不把 private/gated 当作许可证不明确素材的再分发授权。
- 不在命令、脚本、README 或 Release Notes 中写入 GitHub/Hugging Face Token。

## 建议执行顺序

1. 完成本地逐图许可证与再分发审计；不合格图片只保留下载脚本、来源 URL 和哈希，不上传像素文件。
2. 从 `local_data/` 建立严格 allowlist 的 Dataset staging 目录，只放 12 张图与必要元数据；先创建私有 HF Dataset 验证 Viewer、哈希和下载。
3. 从 `runs/` 建立经过清理的 Release staging 目录；把 24 个 Task 按独立可解包的多个归档分组，并生成 `SHA256SUMS`。
4. 创建与代码 Commit 对齐的 Git Tag 和 Draft Release，上传归档后下载回验；确认无敏感信息再发布。
5. 在 Git 仓库的 Run Markdown 报告中记录 HF Dataset 的不可变 revision 和 Release Tag/附件哈希，避免只链接可变的 `main`。

这份结论只确认平台容量、产品语义和推荐结构；是否可以公开发布具体图片，最终取决于本项目逐图许可证审计与运行内容清理结果。

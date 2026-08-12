# 1:1 公开图像重定向基准：数据源与许可调研

访问日期：2026-08-11
状态：【候选方案】，尚未冻结 300 张逐图 manifest，未下载大型数据集，也未形成任何正式质量结论。

## 结论

建议新建 `retarget_square_public_v1`，固定 **300 张真实公开图片、每图仅一个
1536×1536（1:1）Task**。其中 60 张作为可见的 calibration/pilot 子集，剩余
240 张作为冻结后才评分的 held-out eval 子集。四个确定性方法需要完整运行
300 张，即 1200 个候选；Agent 或 AIGC 只运行路由命中的子集，但端到端系统仍应
在全部 300 张上报告结果。

公开主基准的数据像素建议只来自两条可逐图审计且支持小样本下载的官方链路：

1. **Wikimedia Commons**：负责中文文字海报、商业混合图以及需要精细挑选的困难图；
2. **Open Images V7 validation**：负责商品、人物、结构和多主体图片，并利用其公开
   bbox/segmentation 标注做与生成链路隔离的评测参考。

V7 列出的 RetargetMe、PKU PosterLayout、CGL-Dataset v2 和 COCO 不应直接进入
可公开再分发的 v1 核心像素包：前三者没有在当前官方页面中给出足以确认公开修改、
商用和再分发的明确数据许可证；COCO 只统一许可 annotations，COCO Consortium
明确表示它不拥有图片版权。它们可以作为本地研究或逐图额外审计后的补充集，但不能
因为“能下载”就推定“能公开发布”。

## V7 候选源审计

| 数据源 | 官方规模/内容 | 官方许可证据 | 研究使用 | 修改/商用/像素再分发 | 本项目结论 |
|---|---|---|---|---|---|
| RetargetMe | 官方下载页提供 37 张论文分析图；source-only 包约 60 MB，并提供旧方法结果和用户数据 | 官方页称向 research community 提供并要求引用，但未给出标准许可证或逐图许可条款。[项目页](https://people.csail.mit.edu/mrub/retargetme/)；[下载页](https://people.csail.mit.edu/mrub/retargetme/download.html) | 【可用于本地研究】 | 【未知】；不得把“freely available for research”解释为公开商用或再分发授权 | 仅作本地兼容性/历史比较；不进入公开像素包 |
| PKU PosterLayout | 9,974 poster-layout pairs、905 张 canvas；官方仓库要求签署 Release Agreement 后邮件申请 | 官方 README 明确要求签署协议，仓库根目录没有公开数据 LICENSE。[官方 README](https://raw.githubusercontent.com/PKU-ICST-MIPL/PosterLayout-CVPR2023/main/README.md)；[CVPR 官方页面](https://cvpr.thecvf.com/virtual/2023/poster/21729) | 【需先取得并遵守协议】 | 【未知】；必须阅读实际签署协议，不能公开镜像 | 不进入 v1；可在获批后做 Git 外本地补充实验 |
| CGL-Dataset v2 | 60,548 train + 1,035 test，中文广告海报、文本内容和布局标注 | 作者官方 RADM 仓库指向 Tianchi 与独立测试数据链接，但 README 和仓库根目录未提供数据 LICENSE；Tianchi 也说明应在具体数据许可证下使用。[RADM 官方仓库](https://github.com/JD-GenX/RADM)；[Tianchi 数据页](https://tianchi.aliyun.com/dataset/142692)；[Tianchi 许可指南](https://tianchi.aliyun.com/specials/promotion/license) | 【未知，需登录后核对实际条款】 | 【未知】；社区镜像的存在不构成授权证据 | 不下载全集、不进入 v1；先向发布方取得书面条款 |
| COCO 2017 | 118K train / 5K val，人物/物体检测、分割和 keypoints；官方支持按同步方式下载 | annotations 和网站为 CC BY 4.0；官方同时明确 COCO 不拥有图片版权，图片使用必须服从 Flickr 条款并由使用者承担责任。[COCO Terms 源文件](https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/termsofuse.htm)；[下载说明](https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/download.htm) | 【可以，需遵守图片逐图权利】 | 【不能整体推定】；要逐图回查 Flickr license、作者和 landing page | 可作 reserve source；v1 首选 Open Images 以减少重复审计链 |
| Open Images V7 | 约 9M 图片；1.9M 有 dense annotations；约 16M bbox、600 类，复杂场景平均约 8.3 个物体 | annotations 为 CC BY 4.0；图片被列为 CC BY 2.0，但官方要求使用者逐图复核。[官方说明与许可](https://storage.googleapis.com/openimages/web/factsfigures_v7.html#licenses) | 【允许】 | 【逐图复核后允许】；保留作者、landing page、license 和修改说明 | **v1 主来源**；只取 validation 固定 ID 小样本 |
| Wikimedia Commons | 海量逐文件许可媒体；每张 File page 记录作者、来源和许可 | Commons 说明开放内容通常可复用，但每张要求不同且 WMF 不保证许可正确；还可能有商标、人格、隐私等非版权限制。[官方复用指南](https://commons.wikimedia.org/wiki/Commons%3AReusing_content_outside_Wikimedia/en)；[非版权限制](https://commons.wikimedia.org/wiki/Commons%3ANon-copyright_restrictions) | 【逐图审计后允许】 | 【逐图审计后允许】；BY-SA 派生输出必须遵守 ShareAlike | **v1 主来源**；中文海报与商业困难图优先 |

以上“商用”只指版权许可证层面的许可，不等于某张含人脸、商标、建筑或产品图片
在所有司法辖区都适合商业使用。CC BY 4.0 的正式条款明确不授予人格/隐私权和商标权，
也禁止暗示背书；同类边界适用于这里的风险判断。[CC BY 4.0 legal code，2(b)](https://creativecommons.org/licenses/by/4.0/legalcode)

## 冻结的完整基准定义

### 数量、split 与目标

| 项目 | 固定值 |
|---|---:|
| dataset id | `retarget_square_public_v1` |
| source 数 | 300 |
| target | `square-1536x1536`，仅 1:1 |
| task 数 | 300 |
| calibration/pilot | 60 sources；允许调阈值、Prompt 和路由规则 |
| held-out eval | 240 sources；冻结方法、参数、Prompt、Agent 和指标后才运行 |
| 四确定性方法候选 | 300 × 4 = 1200 |
| AIGC 候选 | 仅 Agent 路由命中的 source；数量和最高成本在 Run 前冻结 |

`pilot60` 是 `retarget_square_public_v1` 的固定子集，不复制图像。正式报告必须分别给出
pilot60、held-out240 和 full300；主要方法结论以 held-out240 为准，full300 用于说明
整个公开基准的实际端到端表现。

300 张沿用 V7 的七类分层比例：

| scene_category | full300 | pilot60 | 选择要点 |
|---|---:|---:|---|
| `chinese_dense_poster` | 50 | 10 | 至少 15 个文字区域，或 CJK 字符数 ≥80，文字覆盖率 ≥20%；含多字号/多区块 |
| `single_product_promo` | 50 | 10 | 一个主商品占画面 20%–70%；至少有包装文字、品牌区或宣传文字之一 |
| `multi_product_commercial` | 50 | 10 | 至少 4 个商品实例，并含价格、Logo、按钮、角标、货架标签中的至少两类 |
| `multi_person` | 50 | 10 | 至少 3 人，或有 group-of；优先遮挡、人物分散、边缘人物和不同尺度 |
| `portrait` | 34 | 7 | 1 个主脸/人物，避免证件照式居中单色背景；包含头发、手部、服饰等边界压力 |
| `landscape_architecture_structure` | 33 | 7 | 强直线、重复几何、透视消失点、桥梁/立面/室内结构或地平线 |
| `complex_mixed` | 33 | 6 | 多主体 + 多文字 + 复杂背景；至少满足下述三个困难条件 |
| **合计** | **300** | **60** |  |

`complex_mixed` 的困难条件为：可见主体 ≥5、OCR 区域 ≥5、人物 ≥2、商品/Logo
区域 ≥2、至少三个象限含 must-keep 内容、高频边缘/纹理覆盖 ≥35%、存在遮挡或截断、
存在明显透视结构线。场景可以有次级标签，但 primary scene 必须唯一，以免一张图在
分层统计里重复计数。

### 来源配额

建议冻结为 125 张 Commons + 175 张 Open Images V7 validation：

| scene_category | Commons | Open Images | 合计 |
|---|---:|---:|---:|
| 中文密集海报 | 50 | 0 | 50 |
| 单商品宣传 | 10 | 40 | 50 |
| 多商品商业混合 | 30 | 20 | 50 |
| 多人物 | 10 | 40 | 50 |
| 肖像 | 4 | 30 | 34 |
| 结构线 | 8 | 25 | 33 |
| 复杂混合 | 13 | 20 | 33 |
| **合计** | **125** | **175** | **300** |

Open Images validation/test 的 bbox 是针对已有正标签的穷举人工框，官方说明 validation
和 test 的框均为人工绘制；这些标注适合保留为 evaluator-only 证据，不应注入候选生成
链路，避免让某一方法获得数据集专属标注优势。[Open Images V7 数据说明](https://storage.googleapis.com/openimages/web/factsfigures_v7.html)

### 目标比例压力和清晰度门槛

令 `pressure = max(width/height, height/width)`；所有图片都远离 1:1：

| 难度 | pressure | full300 比例 | 目的 |
|---|---:|---:|---|
| `aspect_hard_1` | [1.50, 2.00) | 30% | 常见竖海报/横幅 |
| `aspect_hard_2` | [2.00, 3.00) | 50% | 明显裁切或形变压力 |
| `aspect_extreme` | [3.00, 4.00] | 20% | 极窄/极宽困难样本 |

每个 scene 内横图/竖图尽量各半，差不超过 1；不纳入 `pressure < 1.50` 的近方形图片。
常规图片要求短边 ≥1024、长边 ≥1600；历史中文海报允许最多 6 张低分辨率例外，但必须
标记 `source_resolution_limited=true`，其清晰度指标不得把上采样当作恢复细节。

### 去重与内容安全

- 与现有 12 张 Smoke 做 SHA-256 和 pHash 去重；Smoke 可以继续做管线证据，但不能在
  main300 重复贡献质量统计。
- 数据集内部先按原始 SHA-256 去重，再以归一化 pHash/Hamming 距离人工复核近重复；
  同一事件连拍、同一海报不同分辨率只留一个。
- 排除色情、医疗病灶、事故伤亡、仇恨、明显私人空间、身份证件、精确住址和其他敏感
  信息；公开人物图不做身份、年龄、族裔或其他敏感属性推断。
- 默认排除明显未成年人特写。多人公共场景若可能包含未成年人，必须单独标记并优先换图。
- 含人物、商标和 Logo 的图片记录 `personality_rights_status`、`trademark_status` 与
  `non_copyright_restrictions`；未知不等于不存在。

## 可复现 materialize 方案

### Git 中保存的文件

```text
datasets/retarget_square_public_v1/
├── README.md
├── selection_policy.yaml
├── source_manifest.csv
├── source_audit.csv
├── commons_file_titles.txt
├── openimages_validation_ids.txt
├── targets.csv
├── tasks.csv
└── ATTRIBUTION.md
scripts/
└── materialize_square_public_v1.py
```

图像仍放在 Git 忽略目录：

```text
local_data/retarget_square_public_v1/
├── raw_cache/
├── images/
├── evaluator_annotations/
├── audit_rows.json
└── dataset.yaml
```

`source_manifest.csv` 除项目现有字段外，至少固定：

```text
source_id, split, scene_category, secondary_tags, difficulty_tier,
upstream_dataset, upstream_id, upstream_split, official_source,
source_url, license_evidence_url, license, license_url, author,
attribution, access_date, upstream_revision_timestamp, upstream_hash,
raw_sha256, materialized_sha256, expected_width, expected_height,
source_aspect, orientation, local_filename, redistribution_status,
modification_notice, personality_rights_status, trademark_status,
non_copyright_restrictions, source_resolution_limited,
public_release_eligible, api_egress_allowed
```

`raw_sha256` 对应官方源原始字节；`materialized_sha256` 对应去除 EXIF/GPS 后的工作副本。
两者都记录，避免“清隐私元数据”破坏可复现性却没有证据。不得把 GPS、相机序列号或绝对
本机路径写入可公开 manifest。

### Commons 下载链路

1. 候选发现可以使用 Commons 分类或 MediaSearch，但冻结时必须写入确切 `File:` title，
   不能每次动态搜索后随机取前 N 张。
2. 对每个 title 调用 MediaWiki Action API：

```text
https://commons.wikimedia.org/w/api.php
  ?action=query&format=json&prop=imageinfo
  &iiprop=timestamp|url|size|sha1|mime|extmetadata
  &iiextmetadatafilter=LicenseShortName|LicenseUrl|Artist|Credit|Attribution|Permission|GPSLatitude|GPSLongitude
  &titles=File:...
```

`imageinfo` 官方文档说明可返回 timestamp、URL、尺寸、SHA-1、MIME 和 extmetadata；
CommonsMetadata 文档列出 `LicenseShortName`、`LicenseUrl`、`Artist`、`Credit`、
`Attribution` 等字段，同时警告 multi-license 字段可能不可靠。因此多重许可文件必须
人工查看 File page 后明确选择实际采用的一条许可证。[API:Imageinfo](https://www.mediawiki.org/wiki/API%3AImageinfo)；[CommonsMetadata](https://www.mediawiki.org/wiki/Extension%3ACommonsMetadata)
3. 许可证 allowlist 仅接受 `Public domain`、`CC0`、`CC BY 2.0/3.0/4.0`、
   `CC BY-SA 2.0/3.0/4.0`；拒绝 unknown、NC、ND、fair-use、仅 GFDL 或页面有版权争议
   但未解决的文件。
4. 下载 API 返回的原始 URL；验证 host、Content-Type、最大字节、解码尺寸和 upstream
   SHA-1，再计算原始 SHA-256。

Commons 官方复用指南强调每张图许可条件可能不同、复用者需自行验证；CC BY-SA 变形
输出还要以相同或兼容条款发布。[Commons 许可复用说明](https://commons.wikimedia.org/wiki/Commons%3AReusing_content_outside_Wikimedia/licenses/en)

### Open Images 下载链路

1. 只读取 validation 的官方 image IDs、bbox/class metadata 和 image information；
   过滤得到候选后，把精确 ID 冻结在 `openimages_validation_ids.txt`。
2. `source_manifest.csv` 记录 Open Images 官方 image-information 中的 `ImageID`、
   `OriginalURL`、`OriginalLandingURL`、`License`、`Author`、`Title`、`OriginalMD5`。
   官方下载页明确公布这些字段。[Open Images 下载与格式](https://storage.googleapis.com/openimages/web/download_v7.html)
3. 发布资格要求 `License` 精确为 CC BY 2.0、原始 landing page 可访问并显示同一许可，
   作者/标题一致；不满足者剔除，不用“Open Images 大多数都开放”代替逐图证据。
4. 仅用官方 `downloader.py` 按固定 `$SPLIT/$IMAGE_ID` 列表从 CVDF 下载。官方说明该脚本
   专门支持只取少量固定 ID，无需下载 1.9M 图片全集。[官方按 ID 下载步骤](https://storage.googleapis.com/openimages/web/download_v7.html)
5. 校验官方 MD5（若有）、解码尺寸和本地 SHA-256；只抽取选中 ID 的 evaluator bbox/
   segmentation，不能把全量 annotations 复制进发布包。

### 共同校验与失败策略

materializer 必须：

- 只接受 allowlist HTTPS host 和相对 POSIX 本地路径，拒绝绝对路径、`..` 和符号链接逃逸；
- 对 300 张逐行校验许可证、作者、来源页、尺寸、hash、scene 数量、split 数量、横竖比例和
  difficulty 数量；
- 下载到临时文件，验证成功后原子移动；中断后按 hash 续传；
- 从公开工作副本清除 EXIF/GPS，但保存 raw/materialized 两个 hash 和
  `modification_notice=metadata removed; pixels unchanged`；
- 生成 `dataset_fingerprint`，由排序后的 manifest、targets、tasks 和工作副本 SHA-256
  共同计算；
- 网络不可用、license evidence 消失、hash 改变或 scene 配额不足时失败退出，绝不拿
  fixture 或旧 Smoke 冒充 main300；
- 已冻结 v1 后任何换图、改标注或改 target 均创建 v2，不静默覆盖。

## 发布与许可证门禁

1. Git 只保存脚本、manifest、审计表、ATTRIBUTION 和说明；原始/工作图像不进入普通
   Git 历史。
2. 若发布 Hugging Face Dataset，dataset card 必须声明 **mixed per-file licenses**，
   每行保留作者、来源页、许可证链接和修改说明，不能用仓库的单一许可证覆盖图片权利。
3. 所有 CC BY/CC BY-SA 图片的 retarget 候选都属于经过 transform 的版本，发布时必须
   标注修改；CC BY-SA 派生图还需使用相同或兼容许可证。CC BY 4.0 正式条款要求分享时
   保留作者、许可和源 URI，并标明修改。[CC BY 4.0，3(a)](https://creativecommons.org/licenses/by/4.0/legalcode)
4. 含人物/商标并不因 CC 许可而自动“商业安全”；公开数据集只声称研究评测用途和版权
   许可审计通过，不声称获得肖像代言或商标授权。
5. 将任何图片发往外部 AIGC API 是独立的数据出域动作。只有
   `api_egress_allowed=true`、Provider 条款已核对且 Run 级预算门禁通过的行才能发送；
   “可公开下载”不自动等于“可以交给任意第三方处理”。

## 最小规模与统计口径

- **36 张**：保持与 V7 baseline 的兼容，但每个小类只有 4–6 张，只适合早期基线，不足以
  支撑稳定的细分类排序。
- **60 张**：本次建议的最小可用 pilot；每类 6–10 张，可定位失败类型、校准 Agent 和
  指标，但若某方法成功率约 50%，总体二项比例的 95% 误差约为 ±12.7%，不能当最终结论。
- **300 张**：V7 Main 的完整公开规模；总体 50% 比例的近似 95% 误差降至 ±5.7%，并可
  用 source-level paired bootstrap 报告方法间差异。细分类仍应报告置信区间，不只给均值。

评测单位必须是 source/task，而不是把一个 source 的多个候选当独立样本。确定性方法在
300 张上完整评分；AIGC 方法若只运行路由子集，应同时报告：

1. routed coverage（命中数/300）；
2. 路由子集上的 AIGC 条件质量；
3. 未命中时回退到传统 Top-1 后的端到端 full300 质量；
4. 总调用成本/300、每次成功生成成本和每个质量提升点的增量成本。

不能把“只在最难、且传统方法失败的图片上运行 AIGC”的条件分数与传统方法 full300 均值
直接比较，也不能把自动 OCR/检测器自身输出称作人工 ground truth。Open Images 官方标注可
作为 evaluator-only 参考；Commons 的自动保护区域仍应标记 `annotation_origin=auto`。

## 建议执行顺序

1. 先冻结 selection policy 与 60 张 pilot 的精确 ID/title，完成逐图许可和缩略图审计；
2. materialize 60 张并验证 60 个 1:1 Task，不调用付费 API；
3. 用 pilot 校准自动指标、Agent 路由和预算上限；
4. 按同一规则补齐 held-out240，冻结 300 张 fingerprint；
5. 冻结方法/参数/Prompt 后运行四确定性方法 full300，再按预声明门禁运行少量 AIGC；
6. 发布前再次复核 attribution、EXIF/GPS、人格/商标风险和派生图 ShareAlike 条款。

这套顺序既不下载几十 GB 的完整上游数据，也不会用许可证未知的海报数据冒充可公开
benchmark；最终得到的是一个可复现的小型公开评测子集，而不是上游大型数据集的镜像。

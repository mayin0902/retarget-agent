# `retarget_smoke_real_v1` 真实 Smoke 来源研究

- 审计日期：2026-08-10
- 研究范围：仅核对 V7 允许的公开候选源及逐图官方来源；不下载大型数据集。
- 结论：最终清单为 **12 张**，场景分层为 `2/2/2/2/1/1/2`；每张均有 Wikimedia Commons 官方 File 页与可解析原图 URL，许可证均为明确的 Public Domain、CC BY 或 CC BY-SA，不含 `unknown/unclear`。
- 使用边界：图片只物化到 Git 忽略的本地数据目录，用于算法 Smoke；Git 只保存脚本、manifest、来源审计和说明。物化脚本应在下载时重新读取 File 页/API 元数据并计算 **SHA-256**，不得把 Commons 的 SHA-1 当作项目要求的 SHA-256。

## 为什么不直接从 V7 的四个大数据源抽取

1. [RetargetMe 官方下载页](https://people.csail.mit.edu/mrub/retargetme/download.html)允许下载源图与重定向结果，但官方页面未给出覆盖每张图的许可证、商用或再分发条款；其[项目页](https://people.csail.mit.edu/mrub/retargetme/)说数据面向研究社区并要求引用，这不等于逐图再分发许可。因此本次不选。
2. [PKU PosterLayout 官方仓库](https://github.com/PKU-ICST-MIPL/PosterLayout-CVPR2023)要求签署 Release Agreement 后邮件申请数据。未取得并审阅协议前，不把其图片纳入可物化的 12 张清单。
3. [CGL-Dataset v2 官方数据卡](https://huggingface.co/datasets/creative-graphic-design/CGL-Dataset-v2/blob/main/README.md)明确写明本地 loader 元数据未指定数据集许可证，要求用户核对上游条款。因此本次不选。
4. [COCO 官方站](https://cocodataset.org/)提供数据与工具，但图片来源于 Flickr，单张权利不能由 COCO API/代码许可证替代；[Flickr 官方 API 条款](https://www.flickr.com/help/terms/api)也要求遵守每位图片所有者设置的许可。本次为避免额外逐图回溯，改用 Commons File 页已逐图展示许可的图片。

Wikimedia Commons 是 V7 “具有明确许可证的其他公开图片”路径。以下每项均以 Commons 官方 File 页为许可证与作者事实源；原图 URL 由官方 MediaWiki `imageinfo` 接口解析。File title 是固定解析标识，即使 upload URL 的内容寻址路径日后变化，materialize 脚本也可再次通过 API 解析。

## 最终 12 张候选

共同访问日期均为 **2026-08-10**。所有 CC BY/CC BY-SA 文件在再分发或修改时必须署名、链接许可证并标注修改；CC BY-SA 的衍生作品还必须采用相同或兼容许可证。Public Domain 项无需法定署名，但项目仍应保留来源和创作者/机构记录。

### 1. 中文密集文字海报（2）

#### CN-POSTER-01

- 固定 ID：`File:2012大连冬聚海报.jpg`
- 拟用本地文件名：`cn_poster_01_dalian_2012.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:2012%E5%A4%A7%E8%BF%9E%E5%86%AC%E8%81%9A%E6%B5%B7%E6%8A%A5.jpg)
- 固定小样本 URL：[960px JPEG](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/2012%E5%A4%A7%E8%BF%9E%E5%86%AC%E8%81%9A%E6%B5%B7%E6%8A%A5.jpg/960px-2012%E5%A4%A7%E8%BF%9E%E5%86%AC%E8%81%9A%E6%B5%B7%E6%8A%A5.jpg)
- 官方来源/作者：Ranyv（燃玉）在 File 页声明为自有作品。
- 许可证：[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0)
- 再分发/修改：允许；须署名 Ranyv（燃玉）、链接许可证、标注修改，并采用相同或兼容许可证。
- 场景理由：物化后的人工缩略图检查确认其包含活动名、时间、地点、报名 URL 和组织文字，中文文字密度明显高于原候选《十字街头》，因此在真实 Run 前完成显式替换。

#### CN-POSTER-02

- 固定 ID：`File:Poster of the film Meng Lijun 1940 China.jpg`
- 拟用本地文件名：`cn_poster_02_meng_lijun_1940.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Poster_of_the_film_Meng_Lijun_1940_China.jpg)
- 原图 URL：[310×450 JPEG](https://upload.wikimedia.org/wikipedia/commons/2/22/Poster_of_the_film_Meng_Lijun_1940_China.jpg)
- 官方来源/作者：国华影业公司；File 页记录 1940 年中国电影《孟丽君》海报。
- 许可证：[Public domain：PD-China + PD-1996/URAA-US（证据在 File 页 Licensing）](https://commons.wikimedia.org/wiki/File:Poster_of_the_film_Meng_Lijun_1940_China.jpg#Licensing)
- 再分发/修改：允许；公有领域。保留来源记录。
- 场景理由：竖版历史电影海报，中文片名、演职员/制作信息与人物画面同框；与 CN-POSTER-01 的构图和字体分布不同。

> 两张均是作品文件本身获得明确许可的海报，不使用“只有照片获得 CC、画面内现代海报版权未核清”的实拍。CN-POSTER-01 是作者以 `Own work` 发布的数字海报；CN-POSTER-02 是具有中美公有领域依据的历史印刷品。

### 2. 单商品宣传图（2）

#### SINGLE-01

- 固定 ID：`File:Wristwatch.jpg`
- 拟用本地文件名：`single_01_wristwatch.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Wristwatch.jpg)
- 原图 URL：[1227×1059 JPEG](https://upload.wikimedia.org/wikipedia/commons/6/69/Wristwatch.jpg)
- 官方来源/作者：上传者 Mohylek 的自有作品；File 页描述为一只腕表。
- 许可证：[Public domain / PD-self（权利人全球释放）](https://commons.wikimedia.org/wiki/File:Wristwatch.jpg#Licensing)
- 再分发/修改：允许，无条件；建议保留 Mohylek 与 File 页记录。
- 场景理由：单一腕表为明确主商品、背景简洁，适合检查商品外形和表盘圆形结构在极端比例下是否变形。

#### SINGLE-02

- 固定 ID：`File:Packshot - Tomme du Berry au pesto (24382897667).jpg`
- 拟用本地文件名：`single_02_tomme_packshot.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Packshot_-_Tomme_du_Berry_au_pesto_(24382897667).jpg)
- 原图 URL：[5614×3158 JPEG](https://upload.wikimedia.org/wikipedia/commons/f/f5/Packshot_-_Tomme_du_Berry_au_pesto_%2824382897667%29.jpg)
- 官方来源/作者：missbutterflies；Commons File 页记录 Flickr photo ID `24382897667`，并经 FlickreviewR 复核许可。
- 许可证：[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0)
- 再分发/修改：允许；署名 missbutterflies、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：单块奶酪 packshot 为主商品，横版浅景深构图与腕表不同，可检查主商品边界、包装/标签和留白。

### 3. 多商品、价格、Logo、按钮或角标混合图（2）

#### ECOM-01

- 固定 ID：`File:SPAR kolonial mat varehandel hyller (Supermarket interior GROCERY store aisle shelves) Frokostblandinger gryn müsli Axa frukt energi 4-korn blåbær (cereals muesli) etc Tjøme NORWAY 2023-08-31 IMG 1095.jpg`
- 拟用本地文件名：`ecom_01_spar_cereal_shelf.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:SPAR_kolonial_mat_varehandel_hyller_(Supermarket_interior_GROCERY_store_aisle_shelves)_Frokostblandinger_gryn_m%C3%BCsli_Axa_frukt_energi_4-korn_bl%C3%A5b%C3%A6r_(cereals_muesli)_etc_Tj%C3%B8me_NORWAY_2023-08-31_IMG_1095.jpg)
- 原图 URL：[7709×5781 JPEG](https://upload.wikimedia.org/wikipedia/commons/6/6a/SPAR_kolonial_mat_varehandel_hyller_%28Supermarket_interior_GROCERY_store_aisle_shelves%29_Frokostblandinger_gryn_m%C3%BCsli_Axa_frukt_energi_4-korn_bl%C3%A5b%C3%A6r_%28cereals_muesli%29_etc_Tj%C3%B8me_NORWAY_2023-08-31_IMG_1095.jpg)
- 官方来源/作者：Wolfmann 自有作品。
- 许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- 再分发/修改：允许；署名 Wolfmann、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：Commons 官方描述明确包含多种包装商品、货架价签、SPAR 与 AXA 等 Logo/品牌信息，适合文字、价格和重复商品边缘压力测试。
- 权利边界：CC 许可覆盖摄影版权，不授予商标使用或代言权；仅用于本地算法 Smoke，不用于对外营销。

#### ECOM-02

- 固定 ID：`File:Electronic shelf labels on spice products in Adcoops supermarket, United Arab Emirates.jpg`
- 拟用本地文件名：`ecom_02_adcoops_spice_esl.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Electronic_shelf_labels_on_spice_products_in_Adcoops_supermarket,_United_Arab_Emirates.jpg)
- 原图 URL：[4284×5712 JPEG](https://upload.wikimedia.org/wikipedia/commons/c/c2/Electronic_shelf_labels_on_spice_products_in_Adcoops_supermarket%2C_United_Arab_Emirates.jpg)
- 官方来源/作者：Maheshod98 自有作品。
- 许可证：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0)
- 再分发/修改：允许；署名 Maheshod98、链接许可证并标注修改。
- 场景理由：纵向货架近景同时包含多种香料包装、商品文字、品牌与电子价格标签；与 ECOM-01 的横向大货架构图形成互补。
- 权利边界：CC 许可覆盖摄影版权，不授予商标使用或代言权；仅用于本地算法 Smoke，不用于对外营销。

### 4. 多人物图片（2）

#### PEOPLE-01

- 固定 ID：`File:People Walking on Torrance Beach.jpg`
- 拟用本地文件名：`people_01_torrance_beach.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:People_Walking_on_Torrance_Beach.jpg)
- 原图 URL：[3449×2586 JPEG](https://upload.wikimedia.org/wikipedia/commons/3/36/People_Walking_on_Torrance_Beach.jpg)
- 官方来源/作者：DylanMoz49 自有作品。
- 许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- 再分发/修改：允许；署名 DylanMoz49、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：多名人物沿海岸线分布，人物尺度、间距和地平线清晰，可检查裁剪是否漏人以及人体比例是否失真。
- 人物权边界：CC 许可解决摄影版权，不等于单独的肖像/人格权许可；只做本地算法 Smoke，不作广告或身份推断。

#### PEOPLE-02

- 固定 ID：`File:Group of people and children at a picnic (AM 86638-1).jpg`
- 拟用本地文件名：`people_02_auckland_picnic_1938.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Group_of_people_and_children_at_a_picnic_(AM_86638-1).jpg)
- 原图 URL：[1275×950 JPEG](https://upload.wikimedia.org/wikipedia/commons/6/65/Group_of_people_and_children_at_a_picnic_%28AM_86638-1%29.jpg)
- 官方来源/作者：Tudor Washington Collins（1898–1970），Auckland Museum 馆藏/API 记录。
- 许可证：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0)，指定署名 Auckland Museum。
- 再分发/修改：允许；署名 Auckland Museum、链接许可证并标注修改。
- 场景理由：1938 年多人野餐群像，成人、儿童和婴儿紧密排列，与 PEOPLE-01 的分散远景形成差异，可测试多张脸和肢体的保护。
- 人物权边界：CC 许可解决摄影版权，不等于单独的人格权许可；仅本地算法 Smoke，不作身份识别或营销。

### 5. 人物肖像（1）

#### PORTRAIT-01

- 固定 ID：`File:Man classic portrait.jpg`
- 拟用本地文件名：`portrait_01_man_classic.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Man_classic_portrait.jpg)
- 原图 URL：[2327×3500 JPEG](https://upload.wikimedia.org/wikipedia/commons/d/dc/Man_classic_portrait.jpg)
- 官方来源/作者：Viktoria Borodinova 自有作品。
- 许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- 再分发/修改：允许；署名 Viktoria Borodinova、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：纵向单人经典肖像，脸部、头发、肩部轮廓和背景留白明确，适合检查面部比例与构图中心保持。
- 人物权边界：CC 许可解决摄影版权，不等于单独的肖像/人格权许可；仅本地算法 Smoke，不作广告、身份识别或敏感属性推断。

### 6. 风景、建筑或明显结构线（1）

#### STRUCTURE-01

- 固定 ID：`File:Hussaini Suspension Bridge.jpg`
- 拟用本地文件名：`structure_01_hussaini_bridge.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Hussaini_Suspension_Bridge.jpg)
- 原图 URL：[3240×4320 JPEG](https://upload.wikimedia.org/wikipedia/commons/0/0d/Hussaini_Suspension_Bridge.jpg)
- 官方来源/作者：Taseer Beyg 自有作品。
- 许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- 再分发/修改：允许；署名 Taseer Beyg、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：423 级悬索桥形成强透视、平行绳索和重复桥板线条，背景同时含山谷与水面；可显著暴露 seam/mesh 的折线和几何扭曲。

### 7. 多主体、多文字、复杂背景困难图（2）

#### HARD-01

- 固定 ID：`File:Shibuya Crossing in Tokyo.jpg`
- 拟用本地文件名：`hard_01_shibuya_crossing_night.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Shibuya_Crossing_in_Tokyo.jpg)
- 原图 URL：[5067×3801 JPEG](https://upload.wikimedia.org/wikipedia/commons/9/94/Shibuya_Crossing_in_Tokyo.jpg)
- 官方来源/作者：Christophe95 自有作品。
- 许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- 再分发/修改：允许；署名 Christophe95、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：夜间十字路口同时含大量行人、车辆、建筑、发光屏幕、Logo 和日文/英文标识，是多尺度主体与密集高对比文字的困难样本。
- 权利边界：CC 许可覆盖摄影版权，不授予画面中商标、广告素材或人物的额外权利；仅本地算法 Smoke，不对外营销。

#### HARD-02

- 固定 ID：`File:Krabi Walking Street.jpg`
- 拟用本地文件名：`hard_02_krabi_walking_street.jpg`
- 官方页：[Wikimedia Commons File 页](https://commons.wikimedia.org/wiki/File:Krabi_Walking_Street.jpg)
- 原图 URL：[4032×3024 JPEG](https://upload.wikimedia.org/wikipedia/commons/2/23/Krabi_Walking_Street.jpg)
- 官方来源/作者：Christophe95 自有作品。
- 许可证：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0)
- 再分发/修改：允许；署名 Christophe95、链接许可证、标注修改，衍生作品相同/兼容许可。
- 场景理由：夜市街景包含多名行人、摊位商品、灯光、招牌文字和纵深背景；与涩谷的城市大屏/路口结构不同，可覆盖小摊密集遮挡与暖色照明。
- 权利边界：CC 许可覆盖摄影版权，不授予画面中商标、招牌作品或人物的额外权利；仅本地算法 Smoke，不对外营销。

## 场景计数与许可证审计结果

| 场景 | 数量 | 最终 ID |
|---|---:|---|
| 中文密集文字海报 | 2 | CN-POSTER-01～02 |
| 单商品宣传图 | 2 | SINGLE-01～02 |
| 多商品、价格、Logo、按钮或角标混合图 | 2 | ECOM-01～02 |
| 多人物图片 | 2 | PEOPLE-01～02 |
| 人物肖像 | 1 | PORTRAIT-01 |
| 风景、建筑或明显结构线 | 1 | STRUCTURE-01 |
| 多主体、多文字、复杂背景困难图 | 2 | HARD-01～02 |
| **总计** | **12** |  |

许可证统计：Public Domain 2 张、CC BY 4.0 2 张、CC BY-SA 2.0 1 张、CC BY-SA 3.0 1 张、CC BY-SA 4.0 6 张；**12/12 均允许复制、修改和再分发，0 张许可证不明**。人物与商标限制不改变摄影版权结论，但必须保留上述仅限本地算法 Smoke 的用途边界。

## 备选（不计入最终 12 张）

1. `File:Poster of the film Cross Roads 1937 China.jpg` — [官方页](https://commons.wikimedia.org/wiki/File:Poster_of_the_film_Cross_Roads_1937_China.jpg)。PD-China + PD-1996/URAA-US；已完成下载与视觉检查，但实际中文文字密度不足，故降为备选而不计入 12 张。
2. `File:Productshot.jpg` — [官方页](https://commons.wikimedia.org/wiki/File:Productshot.jpg)，Daniellaguips，CC BY-SA 4.0。自然场景化妆品产品照；只有人工确认画面确为单一主商品后才可替换 SINGLE 槽位。
3. `File:Shibuya crossing night.jpg` — [官方页](https://commons.wikimedia.org/wiki/File:Shibuya_crossing_night.jpg)，Hide1228，CC BY-SA 4.0。可替换 HARD-01，保持夜间人群与广告屏困难覆盖。
4. `File:Modern Architecture (9870592334).jpg` — [官方页](https://commons.wikimedia.org/wiki/File:Modern_Architecture_(9870592334).jpg)，Gary Todd，CC0。可替换 STRUCTURE-01，覆盖北京现代建筑的直线、玻璃幕墙与几何结构。

## 明确排除的候选

- `File:Chinese Food Safety Poster.jpg` 与 `File:2017福州三中社巡-社团海报.jpg`：Commons 对摄影文件本身给出明确 CC，但页面未分别证明画面内现代海报作品的完整授权链；不进入最终 12 张。
- `File:苏康码（苏州宣传海报）.jpg`：File 页的公有领域断言不足以完成中国与美国两地的严格权利链审计；排除。
- 任何只出现在二手图库、博客、Pinterest、IMDb 或搜索缩略图中的版本：不是本研究的官方事实源；不得由 materialize 脚本下载。

## Materialize 实施要求

1. 仅使用上表固定 File title 调用官方 MediaWiki API：`action=query&prop=imageinfo&iiprop=url|extmetadata&titles=File:...`；不要抓取二手镜像。
2. 下载前校验 API 返回的 `descriptionurl` 仍为对应 Commons File 页，`LicenseShortName` 与本审计一致，且 URL 的主机为 `upload.wikimedia.org`。
3. 下载到 Git 忽略目录后计算 SHA-256，并写入 manifest 的 `source_url`、`official_source`、`license`、`access_date`、`sha256`、`scene_category`、`local_filename`、`redistribution_status`。
4. CC BY/CC BY-SA 项生成 `ATTRIBUTION.md` 或等价审计表；所有重定向结果属于修改/衍生用途，必须标注修改，CC BY-SA 产物如再分发须遵守 ShareAlike。
5. 对人物、商标和广告画面维持“本地算法 Smoke、非营销、非身份识别”的用途限定。若未来要提交图片、公开缩略图或对外发布 Run，必须重新做发布场景的权利与隐私审查。
6. Materialize 后必须生成人工缩略图总览，逐张确认：文件可解码、场景槽位正确、两张中文海报确有足够文字密度、两张单商品图仅有一个主商品、无意外敏感内容；任一失败时使用备选并创建新的 dataset 版本，不静默替换。

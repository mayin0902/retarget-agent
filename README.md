# retarget-agent

可回放、可审计的图片重定向实验平台。当前开发基线是 Direct Warp、保护式 Crop、保护式 Seam 和受约束 Mesh 四候选闭环。

## Windows quick start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\retarget-agent.exe --help
```

## Programmatic fixtures

程序化图片只用于单元、契约、回归和算法压力测试，不计入真实场景 Smoke：

```powershell
.\.venv\Scripts\python.exe scripts\materialize_fixtures.py
.\.venv\Scripts\retarget-agent.exe dataset validate tests\fixtures\generated\retarget_fixture_v1
```

每张 fixture 的 `fixture_type` 和测试目的记录在
`tests/fixtures/programmatic_fixture_catalog.csv`。旧 fixture Run 只保留为技术证据。

## Audited real-world Smoke

真实 Smoke 图片下载到 Git 忽略目录。脚本在下载前重新核对 Wikimedia Commons
官方 File 身份与许可证，再验证固定 URL、SHA-256 和尺寸：

```powershell
.\.venv\Scripts\python.exe scripts\materialize_analyzer_models.py
.\.venv\Scripts\python.exe scripts\materialize_real_smoke_hd.py
.\.venv\Scripts\retarget-agent.exe dataset validate local_data\retarget_smoke_real_hd_v1
.\.venv\Scripts\retarget-agent.exe run generate configs\smoke_real_hd.yaml
.\.venv\Scripts\retarget-agent.exe audit runs\smoke-real-hd-v1-20260810
.\.venv\Scripts\retarget-agent.exe replay run runs\smoke-real-hd-v1-20260810 --replay-id smoke-real-hd-replay-v1
.\.venv\Scripts\retarget-agent.exe review web runs\smoke-real-hd-v1-20260810
.\.venv\Scripts\retarget-agent.exe report runs\smoke-real-hd-v1-20260810
```

推荐的 FastAPI 网页评审支持高清原图、全屏预览、响应式大字号页面、详细评分指引、四候选
A/B/C/Skip、最佳候选、C 级失败原因、本机草稿自动保存、断点恢复和追加式修改；Skip 不进入评分分母。打开
`http://127.0.0.1:8765` 即可使用。旧 Streamlit Adapter 仍可通过
`.\.venv\Scripts\retarget-agent.exe review ui <run-dir>` 启动。详细说明见
`docs/runbooks/review-web.md`。真实来源清单与署名要求位于
`datasets/retarget_smoke_real_hd_v1/`。旧 `retarget_smoke_real_v1` 与 Run
`smoke-real-v1-20260810` 保留为低分辨率历史证据，不进入新的高清审图统计。

共享保护分析在本地 CPU 上运行 PPOCRv3 + 中文 CRNN、YuNet、YOLOX 和紧凑视觉
标识候选检测。模型许可证、URL、SHA-256 和字节数记录在
`datasets/analyzer_models_v1/model_manifest.csv`；模型字节保存在 Git 忽略目录。

候选生成、Replay、评审和报告不会调用外部生成 API 或上传图片。只有显式运行真实
Smoke materializer 时会只读调用 Wikimedia Commons 官方 API 并下载清单中的 12 个
小样本；不会下载完整数据集。

## Verification

```powershell
.\.venv\Scripts\ruff.exe check src tests scripts
.\.venv\Scripts\python.exe -m pytest -q
```

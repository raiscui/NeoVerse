# WORKLOG

## [2026-03-22 12:30:00 UTC] 任务名称: 用 pixi 管理依赖并切换 Hugging Face 镜像

### 任务内容
- 新增 `pixi.toml` 和 `pixi.lock`, 把项目依赖收敛到 `pixi` 管理。
- 新增 `.envrc`, 让 Hugging Face 下载默认走 `hf-mirror`。
- 修改 `diffsynth/__init__.py`, 在包初始化最早阶段补默认 `HF_ENDPOINT`。
- 更新 `README.md`, 把安装、模型下载、Gradio 启动流程改为 `pixi` 工作流。
- 更新 `.gitignore`, 忽略 `.pixi` 与 `.direnv`。

### 完成过程
- 先盘点仓库里所有 Hugging Face 下载入口, 确认只改 README 不够。
- 用 Context7 和 Exa 查 `pixi` manifest、feature、PyTorch index、镜像 endpoint 的写法。
- 首轮实现时尝试把 `gsplat` 作为 Git 源码依赖放进 `pixi`, 动态验证发现 `pixi lock` 会因为构建阶段拿不到 `torch` 而失败。
- 回退旧假设后, 转而验证 PyPI 发布版 `gsplat==1.5.3`, 确认 wheel 已包含仓库代码实际使用的关键模块。
- 用最小样本分别验证 `cu121` / `cu128` 组合在 `gsplat==1.5.3` 条件下都能 `pixi lock` 成功。
- 把主仓库 manifest 切换到 wheel 方案后, 主仓库 `pixi lock` 成功, 并生成了正式 `pixi.lock`。

### 总结感悟
- `pixi + PyPI torch + Git 源码扩展` 这类组合, 最大风险不是版本冲突, 而是构建元数据阶段看不到运行时依赖。
- 如果上游已经发布了能覆盖所需 API 的 wheel, 优先用 wheel 往往比死磕源码构建更稳。
- 把镜像默认值同时放在 `pixi`、`.envrc` 和代码入口, 才能覆盖不同启动路径。

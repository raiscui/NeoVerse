# 笔记: pixi 迁移与 Hugging Face 镜像

## [2026-03-22 11:40:00 UTC] 初步调研

### 仓库现状

- `README.md` 当前要求手动创建 conda 环境, 分 CUDA 12.1 和 CUDA 12.8 两套 `pip install` 命令。
- `requirements.txt` 保存了大部分 Python 依赖, 但 `torch`、`torchvision`、`torch-scatter`、`gsplat` 仍在 README 里单独安装。
- `diffsynth/models/downloader.py`、`diffsynth/utils/__init__.py`、`diffsynth/prompters/omnigen_prompter.py`、`diffsynth/models/omnigen.py`、`diffsynth/extensions/ImageQualityMetric/__init__.py`、`diffsynth/extensions/ImageQualityMetric/open_clip/pretrained.py` 中存在 Hugging Face 下载调用。

### Context7: pixi 关键信息

- `pixi.toml` 支持 `[dependencies]`、`[pypi-dependencies]`、`[tasks]`、`[activation]`、`[system-requirements]`。
- 可以用 `[feature.<name>.dependencies]` / `[feature.<name>.pypi-dependencies]` 表达不同环境。
- 可以用 `[pypi-options] extra-index-urls = ["https://download.pytorch.org/whl/cu121"]` 配置额外 pip index。
- `pypi` 包支持单包级别 `index = "https://download.pytorch.org/whl/cu118"` 的写法。

### Exa 调研: Hugging Face 镜像

- `huggingface_hub` 生态常用 `HF_ENDPOINT=https://hf-mirror.com` 切换镜像。
- 关键注意点: `HF_ENDPOINT` 需要在导入 `huggingface_hub` 之前就存在, 否则库可能仍保留默认 endpoint。
- `hf download`、`snapshot_download`、`hf_hub_download` 都会沿用该 endpoint 机制。

### 当前判断

- 代码里许多 Hugging Face 调用并没有显式传 endpoint, 所以最稳的是在公共入口尽早设置默认 `HF_ENDPOINT`, 但又允许用户覆盖。
- 对这个仓库来说, `pixi` 更适合作为开发和运行入口, `requirements.txt` 可保留作为兼容清单, 但 README 应该改成以 `pixi` 为主。

## [2026-03-22 12:30:00 UTC] 最终收敛结果

### 现象

- `pixi` 可以正确识别 `default`、`cuda121`、`cuda128` 三个环境。
- `pixi lock` 在主仓库上已经成功生成 `pixi.lock`。
- `pixi.lock` 中已经锁住本次需要的关键版本:
  - `gsplat 1.5.3`
  - `torch 2.3.1+cu121`
  - `torch 2.7.1+cu128`
  - `torch-scatter 2.1.2+pt23cu121`
  - `torch-scatter 2.1.2+pt27cu128`

### 被证据推翻的旧假设

- 旧假设: `gsplat` 必须固定到 Git commit 才能满足仓库代码。
- 推翻证据:
  - Git 源码依赖在 `pixi lock` 下稳定失败, 错误是构建元数据阶段 `ModuleNotFoundError: No module named 'torch'`。
  - `gsplat==1.5.3` 的 PyPI wheel 已包含:
    - `gsplat/rendering.py`
    - `gsplat/strategy/*`
    - `gsplat/cuda/_torch_impl.py`
  - 用 `gsplat==1.5.3` 做最小样本时, `cu121` 与 `cu128` 的 `pixi lock` 均成功。

### 最终决定

- `pixi.toml` 采用 PyPI wheel `gsplat==1.5.3`, 不再走 Git 源码依赖。
- `cuda121` / `cuda128` 继续沿用 PyTorch 官方 wheel 源。
- `torch-scatter` 继续用 feature 级 `find-links` 绑定到 PYG 对应轮子页。
- `HF_ENDPOINT` 默认值同时放在:
  - `pixi` activation
  - `.envrc`
  - `diffsynth/__init__.py`

### 验证结论

- 静态证据:
  - `pixi.toml` 已落盘。
  - `pixi.lock` 已生成并锁定关键版本。
  - README 已改成 `pixi` + `hf-mirror` 工作流。
- 动态证据:
  - `pixi task list` 成功列出任务。
  - `pixi lock` 在主仓库成功。
- 未完成部分:
  - `pixi run -e cuda121 ...` / `pixi run -e cuda128 ...` 的运行级 import 验证在本轮没有等到完成输出, 主要卡在大环境首次安装阶段。

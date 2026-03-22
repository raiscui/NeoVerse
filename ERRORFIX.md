# ERRORFIX

## [2026-03-22 12:30:00 UTC] 错误修复: pixi + gsplat 依赖求解失败

### 问题
- `pixi project environment list`、`pixi task list`、`pixi lock` 首先因为 `python = "==3.10.*"` 写法报 manifest 语法错误。
- 修完语法后, `pixi lock` 又因为 `gsplat` Git 源码依赖在构建元数据阶段拿不到 `torch` 而失败。

### 原因
- `pixi` 的 conda 依赖和 PyPI 依赖版本语法不同, `python` 在 `[dependencies]` 里要写成 `3.10.*`。
- `gsplat` Git 源码包没有把 `torch` 声明为构建依赖, 导致 `pixi/uv` 在准备 metadata 时直接报 `ModuleNotFoundError: No module named 'torch'`。

### 修复
- 把 `python = "==3.10.*"` 改成 `python = "3.10.*"`。
- 放弃 `gsplat` Git 源码依赖, 改用已验证包含所需 API 的 `gsplat==1.5.3` PyPI wheel。
- 删除 `no-build-isolation` 和 Git `gsplat` 相关配置, 保留 `torch` / `torchvision` / `torch-scatter` 的显式锁定。

### 验证
- `pixi task list` 成功列出任务。
- 主仓库 `pixi lock` 成功生成 `pixi.lock`。
- `pixi.lock` 中已锁住:
  - `gsplat 1.5.3`
  - `torch 2.3.1+cu121`
  - `torch 2.7.1+cu128`
  - `torch-scatter 2.1.2+pt23cu121`
  - `torch-scatter 2.1.2+pt27cu128`

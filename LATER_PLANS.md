# LATER_PLANS

## [2026-03-22 12:30:00 UTC] 后续补充验证

- 在一台带宽和空闲时间更充足的机器上, 完整跑一次:
  - `pixi run -e cuda121 python -c "import torch, gsplat, diffsynth"`
  - `pixi run -e cuda128 python -c "import torch, gsplat, diffsynth"`
- 有 GPU 资源时, 进一步补 `pixi run app` 与最小 `inference.py --help` / 样例推理验证, 把运行级证据补齐。

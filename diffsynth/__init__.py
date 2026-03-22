import os


def _configure_huggingface_endpoint():
    # `huggingface_hub` 会在导入阶段缓存 endpoint.
    # 这里尽早补默认值, 让直接运行脚本时也默认走镜像, 同时保留用户显式覆盖能力.
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


_configure_huggingface_endpoint()

from .data import *
from .models import *
from .prompters import *
from .schedulers import *
from .pipelines import *
from .controlnets import *

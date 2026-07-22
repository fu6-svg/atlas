"""Test package setup for Project Atlas."""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

# 让测试可以从仓库根目录导入 src 里的模块
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

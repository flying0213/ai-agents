"""让项目根目录的两个薄入口可以被公开测试导入。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""让学生测试与教师验收使用同一个候选实现开关。"""

import pytest

from examples import direct, reference, shallow
from variant import make_variant as student


def pytest_addoption(parser):
    parser.addoption(
        "--impl",
        choices=("student", "direct", "shallow", "reference"),
        default="student",
        help="选择 make_variant 实现；默认运行学生实现",
    )


@pytest.fixture
def make_variant(request):
    """测试必须通过函数参数接收此 fixture，不要直接 import 实现。"""
    implementations = {
        "student": student,
        "direct": direct,
        "shallow": shallow,
        "reference": reference,
    }
    return implementations[request.config.getoption("--impl")]

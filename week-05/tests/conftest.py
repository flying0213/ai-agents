"""教师提供的候选切换：测试通过 fixture 接收函数，不直接 import 实现。"""

import pytest

import examples


def pytest_addoption(parser):
    parser.addoption(
        "--impl",
        choices=("student", "reference", "broken"),
        default="student",
        help="选择 W5 候选实现；默认检查 operations.py 中的学生实现",
    )


def selected_function(request, name):
    choice = request.config.getoption("--impl")
    if choice == "student":
        import operations

        return getattr(operations, name)
    return getattr(examples, choice + "_" + name)


@pytest.fixture
def pop_last(request):
    return selected_function(request, "pop_last")


@pytest.fixture
def positive_squares(request):
    return selected_function(request, "positive_squares")


@pytest.fixture
def positive_square_map(request):
    return selected_function(request, "positive_square_map")

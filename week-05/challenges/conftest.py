"""综合选做单独验收；只有显式运行 challenges 才装配这些 fixture。"""

from importlib import import_module

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--challenge-impl",
        choices=("student", "reference", "broken"),
        default="student",
        help="选择 W5 综合选做候选；默认检查 challenges/work.py",
    )


def selected_function(request, name):
    choice = request.config.getoption("--challenge-impl")
    module_name = "work" if choice == "student" else "examples"
    module = import_module("challenges." + module_name)
    function_name = name if choice == "student" else choice + "_" + name
    return getattr(module, function_name)


@pytest.fixture
def summarize_values(request):
    return selected_function(request, "summarize_values")


@pytest.fixture
def apply_changes(request):
    return selected_function(request, "apply_changes")


@pytest.fixture
def compare_measurements(request):
    return selected_function(request, "compare_measurements")

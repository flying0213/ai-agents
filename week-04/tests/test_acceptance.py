"""教师公开验收：结果正确，还要保留旧配置和后续修改的独立性。"""

from copy import deepcopy

import pytest


# 预期逐份独立写出，不调用被测程序来生成答案。
CASES = [
    (
        {"seed": 42, "sample_sizes": [1000, 10000, 100000]},
        2026,
        2,
        500000,
        {"seed": 2026, "sample_sizes": [1000, 10000, 500000]},
    ),
    (
        {"seed": 7, "sample_sizes": [120]},
        99,
        0,
        240,
        {"seed": 99, "sample_sizes": [240]},
    ),
    (
        {"seed": 21, "sample_sizes": [500, 1500, 2500, 3500]},
        11,
        1,
        900,
        {"seed": 11, "sample_sizes": [500, 900, 2500, 3500]},
    ),
    (
        {"seed": 314, "sample_sizes": [800, 800, 1600]},
        2718,
        0,
        3200,
        {"seed": 2718, "sample_sizes": [3200, 800, 1600]},
    ),
]


@pytest.fixture(params=CASES, ids=("baseline", "single-item", "middle-item", "repeated-values"))
def case(request):
    # 每个测试重新建立输入与预期，故障实现不能污染下一次测试。
    return deepcopy(request.param)


def test_changes_only_requested_values(make_variant, case):
    source, seed, index, replacement, expected = case

    result = make_variant(source, seed, index, replacement)

    assert result == expected


def test_keeps_original_content(make_variant, case):
    source, seed, index, replacement, _ = case
    before = deepcopy(source)

    make_variant(source, seed, index, replacement)

    assert source == before


def test_dictionary_and_sample_list_are_independent(make_variant, case):
    source, seed, index, replacement, _ = case

    result = make_variant(source, seed, index, replacement)

    assert result is not source
    assert result["sample_sizes"] is not source["sample_sizes"]


def test_later_result_changes_do_not_change_source(make_variant, case):
    source, seed, index, replacement, _ = case
    before = deepcopy(source)
    result = make_variant(source, seed, index, replacement)

    result["seed"] = seed + 1
    result["sample_sizes"][index] = replacement + 1
    result["sample_sizes"].append(2000)

    assert source == before


def test_two_calls_can_be_modified_separately(make_variant, case):
    source, seed, index, replacement, expected = case
    before = deepcopy(source)

    first = make_variant(source, seed, index, replacement)
    second = make_variant(source, seed, index, replacement)

    assert first == expected
    assert second == expected
    assert first == second
    assert first is not second
    assert first["sample_sizes"] is not second["sample_sizes"]

    first["seed"] = seed + 1
    first["sample_sizes"][index] = replacement + 1
    first["sample_sizes"].append(250000)

    assert second == expected
    assert source == before


def test_unchanged_parameters_still_create_independent_results(make_variant, case):
    source, _, index, _, _ = case
    before = deepcopy(source)
    seed = source["seed"]
    replacement = source["sample_sizes"][index]

    first = make_variant(source, seed, index, replacement)
    second = make_variant(source, seed, index, replacement)

    assert first == before
    assert second == before
    assert first is not source
    assert second is not source
    assert first is not second
    assert first["sample_sizes"] is not source["sample_sizes"]
    assert second["sample_sizes"] is not source["sample_sizes"]
    assert first["sample_sizes"] is not second["sample_sizes"]

    first["sample_sizes"][index] = replacement + 1

    assert second == before
    assert source == before

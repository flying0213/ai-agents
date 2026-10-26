"""可修改的小测试示例：另选输入，保留自己的预期与解释。

测试通过参数接收课程 fixture，--impl 才能切换候选实现。
不要直接 from operations import pop_last 绕过这个开关。
"""

import numpy as np


def test_my_pop_example(pop_last):
    items = [7, 4]

    result = pop_last(items)

    assert result == 4
    assert items == [7]


def test_my_pop_example_with_zero_tail(pop_last):
    # 我选的输入：[10, -7, 0]；预测：返回 0，原列表变为 [10, -7]。
    items = [10, -7, 0]

    result = pop_last(items)

    assert result == 0
    assert items == [10, -7]


def test_my_positive_squares_example(positive_squares):
    # 我选的输入：[-4, 0, 2, 2, 5]；预测：返回 [4, 4, 25]，原列表不变。
    values = [-4, 0, 2, 2, 5]
    before = values.copy()

    result = positive_squares(values)

    assert result == [4, 4, 25]
    assert values == before


def test_my_positive_squares_numpy_example(positive_squares):
    # 我选的输入：np.array([-1, 3, 0, 3])；预测：返回 [9, 9]，原数组不变。
    values = np.array([-1, 3, 0, 3], dtype=int)
    before = values.copy()

    result = positive_squares(values)

    assert result == [9, 9]
    np.testing.assert_array_equal(values, before)


def test_my_positive_square_map_example(positive_square_map):
    # 我选的输入：{"x": -1, "y": 0, "z": 3, "w": 3}；
    # 预测：返回 {"z": 9, "w": 9}，原字典及键顺序不变。
    record = {"x": -1, "y": 0, "z": 3, "w": 3}
    before = record.copy()

    result = positive_square_map(record)

    assert result == {"z": 9, "w": 9}
    assert list(result) == ["z", "w"]
    assert record == before
    assert list(record) == list(before)

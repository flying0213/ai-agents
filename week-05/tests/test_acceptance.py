"""W5 公开验收：分别检查原对象、返回内容与新结果的独立性。"""

import numpy as np
import pytest


@pytest.mark.parametrize(
    "initial, expected_item, expected_remaining",
    [
        ((1, 2, 2, -1), -1, [1, 2, 2]),
        ((8,), 8, []),
        ((0,), 0, []),
        ((-3, -5), -5, [-3]),
        ((), None, []),
    ],
    ids=("several", "single", "zero", "negative", "empty"),
)
def test_pop_last_returns_item_and_changes_input(
    pop_last, initial, expected_item, expected_remaining
):
    items = list(initial)

    result = pop_last(items)

    assert result == expected_item
    assert items == expected_remaining


def test_pop_last_can_be_called_repeatedly(pop_last):
    items = [7, 4]

    assert pop_last(items) == 4
    assert pop_last(items) == 7
    assert pop_last(items) is None
    assert items == []


@pytest.mark.parametrize("container", ("list", "array"))
@pytest.mark.parametrize(
    "initial, expected",
    [
        ((1, 2, 2, -1), [1, 4, 4]),
        ((0, -2, 3, 0, 1), [9, 1]),
        ((3,), [9]),
        ((0,), []),
        ((-3, -1, 0), []),
        ((), []),
    ],
    ids=("order-and-repeats", "zeros-and-negatives", "single", "zero", "no-positive", "empty"),
)
def test_positive_squares_returns_list_without_changing_input(
    positive_squares, container, initial, expected
):
    values = list(initial) if container == "list" else np.array(initial, dtype=int)
    before = values.copy()

    result = positive_squares(values)

    assert isinstance(result, list)
    assert result == expected
    assert result is not values
    if container == "list":
        assert values == before
    else:
        np.testing.assert_array_equal(values, before)


def test_positive_squares_results_do_not_share_a_list(positive_squares):
    values = [2, 0, 1]

    first = positive_squares(values)
    second = positive_squares(values)
    first.append(99)

    assert first == [4, 1, 99]
    assert second == [4, 1]
    assert first is not second
    assert values == [2, 0, 1]


@pytest.mark.parametrize(
    "initial_pairs, expected",
    [
        ((("a", 1), ("b", 2), ("c", 2), ("d", -1)), {"a": 1, "b": 4, "c": 4}),
        ((("z", 3), ("zero", 0), ("a", 1), ("minus", -2)), {"z": 9, "a": 1}),
        ((("only", 5),), {"only": 25}),
        ((("zero", 0), ("minus", -2)), {}),
        ((), {}),
    ],
    ids=("repeated-values", "keep-key-order", "single", "no-positive", "empty"),
)
def test_positive_square_map_returns_new_dict_and_keeps_input(
    positive_square_map, initial_pairs, expected
):
    record = dict(initial_pairs)
    before = record.copy()

    result = positive_square_map(record)

    assert isinstance(result, dict)
    assert result == expected
    assert list(result) == list(expected)
    assert result is not record
    assert record == before
    assert list(record) == list(before)


def test_positive_square_map_results_can_be_changed_independently(positive_square_map):
    record = {"first": 2, "second": -1}

    first = positive_square_map(record)
    second = positive_square_map(record)
    first["first"] = 99
    first["new"] = 7

    assert second == {"first": 4}
    assert first is not second
    assert record == {"first": 2, "second": -1}

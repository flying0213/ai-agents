"""按输入、输出与副作用验收；可用 -k 选择某一道题。"""

import numpy as np
import pytest


@pytest.mark.parametrize(
    "values, unique, counts, repeated",
    [
        ([3, 1, 3, 0, -1, 1, 3], [3, 1, 0, -1], {3: 3, 1: 2, 0: 1, -1: 1}, {1, 3}),
        ([], [], {}, set()),
        ([5, 5, 5], [5], {5: 3}, {5}),
        ([0, -2, 0, -2, 1], [0, -2, 1], {0: 2, -2: 2, 1: 1}, {0, -2}),
        ([8, -3, 2], [8, -3, 2], {8: 1, -3: 1, 2: 1}, set()),
        ([0], [0], {0: 1}, set()),
    ],
    ids=("mixed", "empty", "same", "zero-negative", "first-order", "single-zero"),
)
def test_summarize_values_content(summarize_values, values, unique, counts, repeated):
    before = values.copy()
    result = summarize_values(values)

    assert isinstance(result, dict)
    assert set(result) == {"unique", "counts", "repeated"}
    assert isinstance(result["unique"], list)
    assert isinstance(result["counts"], dict)
    assert isinstance(result["repeated"], set)
    assert result["unique"] == unique
    assert result["counts"] == counts
    assert result["repeated"] == repeated
    assert result["unique"] is not values
    assert values == before


@pytest.mark.parametrize("values", [[], [3, 1, 3]])
def test_summarize_values_results_are_independent(summarize_values, values):
    before = values.copy()
    first = summarize_values(values)
    second = summarize_values(values)

    assert first is not second
    assert first["unique"] is not second["unique"]
    assert first["counts"] is not second["counts"]
    assert first["repeated"] is not second["repeated"]
    first["unique"].append(99)
    first["counts"][99] = 2
    first["repeated"].add(99)
    assert 99 not in second["unique"]
    assert 99 not in second["counts"]
    assert 99 not in second["repeated"]
    assert values == before


@pytest.mark.parametrize(
    "original, updates, removals, record, changed",
    [
        (
            {"a": 1, "b": 2, "c": 3},
            [("b", 20), ("d", 4), ("b", 22)],
            ["c", "missing"],
            {"a": 1, "b": 22, "d": 4},
            {"b", "c", "d"},
        ),
        ({}, [], [], {}, set()),
        ({"a": 1}, [], [], {"a": 1}, set()),
        ({"a": 1}, [("a", 2), ("a", 1)], [], {"a": 1}, set()),
        ({}, [("temp", 7)], ["temp"], {}, set()),
        ({"a": 1}, [("a", 1)], ["missing", "missing"], {"a": 1}, set()),
        ({"a": 0}, [], ["a", "a"], {}, {"a"}),
        ({}, [("zero", 0)], [], {"zero": 0}, {"zero"}),
        ({"a": 1}, [("a", 8)], ["a"], {}, {"a"}),
        ({"x": -3}, [("b", 0), ("b", -2), ("c", 4)], [], {"x": -3, "b": -2, "c": 4}, {"b", "c"}),
    ],
    ids=(
        "mixed",
        "empty",
        "no-operations",
        "change-back",
        "add-then-remove",
        "no-op-and-missing",
        "remove-zero-twice",
        "add-zero",
        "update-before-remove",
        "last-update-wins",
    ),
)
def test_apply_changes_final_record_and_changed(
    apply_changes, original, updates, removals, record, changed
):
    before_original = original.copy()
    before_updates = updates.copy()
    before_removals = removals.copy()
    result = apply_changes(original, updates, removals)

    assert isinstance(result, dict)
    assert set(result) == {"record", "changed"}
    assert isinstance(result["record"], dict)
    assert isinstance(result["changed"], set)
    assert result["record"] == record
    assert result["changed"] == changed
    assert result["record"] is not original
    assert original == before_original
    assert updates == before_updates
    assert removals == before_removals


@pytest.mark.parametrize("original", [{}, {"a": 1}])
def test_apply_changes_results_are_independent(apply_changes, original):
    before = original.copy()
    first = apply_changes(original, [], [])
    second = apply_changes(original, [], [])

    assert first is not second
    assert first["record"] is not second["record"]
    assert first["changed"] is not second["changed"]
    first["record"]["extra"] = 99
    first["changed"].add("extra")
    assert "extra" not in second["record"]
    assert "extra" not in second["changed"]
    assert original == before


@pytest.mark.parametrize(
    "ids, baseline_values, current_values, threshold, delta, alerts, normal, dtype",
    [
        (["a", "b", "c", "d"], [10, 20, 30, 40], [11, 18, 30, 45], 2, [1, -2, 0, 5], ["d"], {"a": 11, "b": 18, "c": 30}, np.int64),
        ([], [], [], 0, [], [], {}, np.int8),
        (["z", "a", "m", "b"], [0, 0, 0, 0], [3, -3, 2, -2], 2, [3, -3, 2, -2], ["z", "a"], {"m": 2, "b": -2}, np.int32),
        (["z", "a", "m"], [1, 1, 1], [1, 2, 0], 0, [0, 1, -1], ["a", "m"], {"z": 1}, np.int64),
        (["down", "up"], [120, -120], [-120, 120], 200, [-240, 240], ["down", "up"], {}, np.int8),
        (["up", "down"], [0, 255], [255, 0], 254, [255, -255], ["up", "down"], {}, np.uint8),
        (["z", "a"], [-1000000, 1000000], [1000000, -1000000], 2000000, [2000000, -2000000], [], {"z": 1000000, "a": -1000000}, np.int64),
        (["only"], [7], [7], 0, [0], [], {"only": 7}, np.int64),
    ],
    ids=("mixed", "empty", "two-directions-and-boundary", "zero-threshold", "signed-small-dtype", "unsigned-small-dtype", "value-limits-and-boundary", "same-single"),
)
def test_compare_measurements_content(
    compare_measurements,
    ids,
    baseline_values,
    current_values,
    threshold,
    delta,
    alerts,
    normal,
    dtype,
):
    baseline = np.array(baseline_values, dtype=dtype)
    current = np.array(current_values, dtype=dtype)
    before_ids = ids.copy()
    before_baseline = baseline.copy()
    before_current = current.copy()
    result = compare_measurements(ids, baseline, current, threshold)

    assert isinstance(result, dict)
    assert set(result) == {"delta", "alerts", "normal"}
    assert isinstance(result["delta"], np.ndarray)
    assert result["delta"].ndim == 1
    assert np.issubdtype(result["delta"].dtype, np.integer)
    np.testing.assert_array_equal(result["delta"], np.array(delta, dtype=np.int64))
    assert isinstance(result["alerts"], list)
    assert result["alerts"] == alerts
    assert isinstance(result["normal"], dict)
    assert result["normal"] == normal
    assert result["delta"] is not baseline
    assert result["delta"] is not current
    assert not np.shares_memory(result["delta"], baseline)
    assert not np.shares_memory(result["delta"], current)
    assert result["alerts"] is not ids
    assert ids == before_ids
    np.testing.assert_array_equal(baseline, before_baseline)
    np.testing.assert_array_equal(current, before_current)


@pytest.mark.parametrize("empty", [False, True], ids=("nonempty", "empty"))
def test_compare_measurements_results_are_independent(compare_measurements, empty):
    ids = [] if empty else ["alert", "normal"]
    baseline = np.array([] if empty else [0, 7], dtype=np.int16)
    current = np.array([] if empty else [3, 7], dtype=np.int16)
    first = compare_measurements(ids, baseline, current, 2)
    second = compare_measurements(ids, baseline, current, 2)
    second_delta = second["delta"].copy()
    second_alerts = second["alerts"].copy()
    second_normal = second["normal"].copy()

    assert first is not second
    assert first["delta"] is not second["delta"]
    assert first["alerts"] is not second["alerts"]
    assert first["normal"] is not second["normal"]
    assert not np.shares_memory(first["delta"], second["delta"])
    if not empty:
        first["delta"][0] = 99
    first["alerts"].append("extra")
    first["normal"]["extra"] = 99
    np.testing.assert_array_equal(second["delta"], second_delta)
    assert second["alerts"] == second_alerts
    assert second["normal"] == second_normal
    assert ids == ([] if empty else ["alert", "normal"])
    np.testing.assert_array_equal(baseline, [] if empty else [0, 7])
    np.testing.assert_array_equal(current, [] if empty else [3, 7])

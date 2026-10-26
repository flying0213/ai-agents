"""B 题自选输入：通过同名 fixture 接收实现，不直接导入任一候选。"""


def test_my_apply_changes_case(apply_changes):
    original = {"x": 1, "y": 2}
    updates = [("x", 5), ("z", 3), ("x", 1)]
    removals = ["y"]

    before_original = original.copy()
    result = apply_changes(original, updates, removals)

    # x 先改成 5 又改回 1，不算最终变化；y 被删除、z 被新增。
    assert result == {"record": {"x": 1, "z": 3}, "changed": {"y", "z"}}
    assert original == before_original
    assert updates == [("x", 5), ("z", 3), ("x", 1)]
    assert removals == ["y"]

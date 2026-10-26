"""W5 综合选做：按合同完成函数，使用 challenges 中的公开测试验收。"""


def summarize_values(values):
    """整理普通整数列表；不修改输入。

    返回 {"unique": 首次出现顺序的去重列表,
          "counts": 每个整数的出现次数字典,
          "repeated": 出现次数大于 1 的整数集合}。
    空输入返回 {"unique": [], "counts": {}, "repeated": set()}。
    每次调用产生独立结果，结果中的列表、字典、集合可以单独修改。
    """
    raise NotImplementedError("请实现 summarize_values")


def apply_changes(original, updates, removals):
    """在新字典上应用修改清单；三个输入均不修改。

    original 为字符串键、整数值的字典。
    updates 为按顺序执行的 (键, 值) 元组列表，后一次更新覆盖前一次。
    所有更新完成后，再按 removals 删除；缺失键与重复删除均可忽略。
    返回 {"record": 新字典, "changed": 最终相对 original 变化的键集合}。
    改回原值、新增后又删除都不算最终变化；字典键顺序不作要求。
    每次调用产生独立结果。
    """
    raise NotImplementedError("请实现 apply_changes")


def compare_measurements(ids, baseline, current, threshold):
    """对齐两次测量；不修改输入，返回独立的新结果。

    ids 为无重复的字符串列表；baseline、current 为等长的一维整数
    NumPy 数组；值范围为 [-1000000, 1000000]；threshold 为非负整数。
    返回 {"delta": 新的一维整数数组 current - baseline,
          "alerts": abs(delta) > threshold 的编号列表，保留输入顺序,
          "normal": 其余编号到 current 值的字典}。
    恰好等于阈值属于正常；空输入也要返回三个对应的空容器。
    先把 NumPy 整数转成 Python int 再计算，避免小 dtype 溢出。
    """
    raise NotImplementedError("请实现 compare_measurements")

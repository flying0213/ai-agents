"""W5 学生实现：先读 EXPERIMENT.txt，再与 Agent 完成三个函数。"""


def pop_last(items):
    """原地删除整数列表的最后一项并返回它；空列表返回 None。"""
    if not items:
        return None
    return items.pop()


def positive_squares(values):
    """返回正数项平方组成的新列表，保留顺序与重复项，不改输入。

    values 是普通整数列表或一维整数 NumPy 数组。
    空输入或没有正数时返回空列表。
    """
    # item > 0 排除 0 与负数；int(...) 把 NumPy 整数转为 Python int。
    # 在循环外新建结果列表，保证每次调用得到互不共享的新列表。
    result = []
    for item in values:
        if item > 0:
            result.append(int(item) ** 2)
    return result


def positive_square_map(record):
    """返回保留正数值并取平方的新字典，不改原字典。

    record 的键是字符串，值是整数；保留键的原相对顺序。
    空输入或没有正数值时返回空字典。
    """
    # 逐项读原字典，只把 value > 0 的键写入新字典，值为原值的平方。
    result = {}
    for key, value in record.items():
        if value > 0:
            result[key] = int(value) ** 2
    return result

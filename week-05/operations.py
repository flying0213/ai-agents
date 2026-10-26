"""W5 学生实现：先读 EXPERIMENT.txt，再与 Agent 完成三个函数。"""


def pop_last(items):
    """原地删除整数列表的最后一项并返回它；空列表返回 None。"""
    raise NotImplementedError("请实现 pop_last：核对返回值和原列表")


def positive_squares(values):
    """返回正数项平方组成的新列表，保留顺序与重复项，不改输入。

    values 是普通整数列表或一维整数 NumPy 数组。
    空输入或没有正数时返回空列表。
    """
    raise NotImplementedError("请实现 positive_squares：筛选、变换并收集")


def positive_square_map(record):
    """返回保留正数值并取平方的新字典，不改原字典。

    record 的键是字符串，值是整数；保留键的原相对顺序。
    空输入或没有正数值时返回空字典。
    """
    raise NotImplementedError("请实现 positive_square_map：按键值对遍历")

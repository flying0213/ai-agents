"""课堂对照：两份故障和已经演示过的按层复制实现。

用同一份测试比较这些实现；不要为了让故障通过而修改预期。
"""


def direct(source, seed, index, replacement):
    """故障：只增加名字，字典和列表仍然共享。"""
    variant = source
    variant["seed"] = seed
    variant["sample_sizes"][index] = replacement
    return variant


def shallow(source, seed, index, replacement):
    """故障：复制字典，但 sample_sizes 列表仍然共享。"""
    variant = source.copy()
    variant["seed"] = seed
    variant["sample_sizes"][index] = replacement
    return variant


def reference(source, seed, index, replacement):
    """参考：本题列表里只有不可变整数，复制到列表这一层足够。"""
    variant = source.copy()
    variant["sample_sizes"] = source["sample_sizes"].copy()
    variant["seed"] = seed
    variant["sample_sizes"][index] = replacement
    return variant

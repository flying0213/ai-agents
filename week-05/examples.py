"""公开的参考实现与故障对照；与 operations.py 中的学生实现分开。"""


def reference_pop_last(items):
    if len(items) == 0:
        return None
    return items.pop()


def reference_positive_squares(values):
    result = []
    for value in values:
        if value > 0:
            result.append(int(value) ** 2)
    return result


def reference_positive_square_map(record):
    result = {}
    for key, value in record.items():
        if value > 0:
            result[key] = value ** 2
    return result


def broken_pop_last(items):
    """返回值看似正确，却没有完成原地删除。"""
    if len(items) == 0:
        return None
    return items[-1]


def broken_positive_squares(values):
    """把‘正数’误写为‘非负数’；没有零的例子可能看不出错误。"""
    return [int(value) ** 2 for value in values if value >= 0]


def broken_positive_square_map(record):
    """最终内容看似正确，却改了输入，并返回了原字典。"""
    for key in list(record):
        if record[key] > 0:
            record[key] = record[key] ** 2
        else:
            record.pop(key)
    return record

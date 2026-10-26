"""综合选做的公开参考实现，以及各有一个明确错误的故障实现。"""

import numpy as np


def reference_summarize_values(values):
    unique = []
    counts = {}
    for value in values:
        if value not in counts:
            unique.append(value)
            counts[value] = 0
        counts[value] += 1
    repeated = {value for value, count in counts.items() if count > 1}
    return {"unique": unique, "counts": counts, "repeated": repeated}


def reference_apply_changes(original, updates, removals):
    record = original.copy()
    for key, value in updates:
        record[key] = value
    for key in removals:
        record.pop(key, None)

    changed = set()
    for key in original.keys() | record.keys():
        if key not in original or key not in record or original[key] != record[key]:
            changed.add(key)
    return {"record": record, "changed": changed}


def reference_compare_measurements(ids, baseline, current, threshold):
    delta = np.array(
        [int(after) - int(before) for before, after in zip(baseline, current)],
        dtype=np.int64,
    )
    alerts = []
    normal = {}
    for name, change, value in zip(ids, delta, current):
        if abs(int(change)) > threshold:
            alerts.append(name)
        else:
            normal[name] = int(value)
    return {"delta": delta, "alerts": alerts, "normal": normal}


def broken_summarize_values(values):
    """去重后进行了排序，丢失了首次出现顺序。"""
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return {
        "unique": sorted(set(values)),
        "counts": counts,
        "repeated": {value for value, count in counts.items() if count > 1},
    }


def broken_apply_changes(original, updates, removals):
    """把‘操作过的键’当作‘最终发生变化的键’。"""
    record = original.copy()
    changed = set()
    for key, value in updates:
        record[key] = value
        changed.add(key)
    for key in removals:
        record.pop(key, None)
        changed.add(key)
    return {"record": record, "changed": changed}


def broken_compare_measurements(ids, baseline, current, threshold):
    """只检测正向变化，负向变化即使很大也被当作正常。"""
    delta = np.array(
        [int(after) - int(before) for before, after in zip(baseline, current)],
        dtype=np.int64,
    )
    alerts = []
    normal = {}
    for name, change, value in zip(ids, delta, current):
        if change > threshold:
            alerts.append(name)
        else:
            normal[name] = int(value)
    return {"delta": delta, "alerts": alerts, "normal": normal}

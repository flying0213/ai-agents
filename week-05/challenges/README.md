# W5 综合练习：与 Agent 合作完成一项数据任务

三题互相独立，可以任选一题。每题按一次 **20～30 分钟的合作活动**准备：约 5 分钟读条件、预测结果，10～15 分钟实现与测试，5～10 分钟核对边界、解释一段处理过程。完成得快就继续下一题，不需要等计时结束。

这里使用本周已经见过的 list、dict、set、数组、遍历与筛选。函数壳已经提供，可以由 Agent 编写实现；本人负责确认条件与结论。

课堂展示使用 [`demo.ipynb`](demo.ipynb)：每题先用 Markdown 展示条件与预期，再给出独立的完整 Python 参考解答、运行结果和边界例子。教师可停在题目处，让大家先做，再向下展示解答。沿用 `week-05/.venv` kernel，无需建立另一个环境。

## 开始方式与共同约定

- 在 `challenges/work.py` 完成选中的函数，不必实现另外两题。
- 三题只处理各自约定的合法输入，不要求添加异常处理、文件读写或界面。
- 所有输入保持不变；返回新结果，之后修改结果不会影响输入，两次调用的结果也不能相互干扰。
- list 的顺序按题目要求比较；set 只比较元素内容，不比较显示顺序；字典只比较键值，不以显示顺序评分。
- 先预测示例，再自行选择一份不同输入。可让 Agent 计算和解释，本人核对预期从哪里来。
- 测试在 Terminal 运行。Notebook Run All、本周基础题通过，都不代表综合题已经通过。

以下所有命令均在 `week-05/` 执行，沿用本周已建立的环境。

## A｜保留首次顺序，统计重复情况

**目标：** 同一份数据，同时整理成适合查看、计数和成员判断的三种结果。

入口：`summarize_values(values)`。

### 条件

- `values` 是普通 Python 整数列表，可以为空，允许零、负数与重复值。
- 返回字典，固定包含三个键：
  - `unique`：新列表，按每个值**第一次出现的顺序**保留一次。
  - `counts`：新字典，键为出现过的整数，值为它出现的次数。
  - `repeated`：新 set，包含出现次数大于 1 的值。

### 应得到的结论

```python
values = [3, 1, 3, 0, -1, 1, 3]

# summarize_values(values) 应返回：
{
    "unique": [3, 1, 0, -1],
    "counts": {3: 3, 1: 2, 0: 1, -1: 1},
    "repeated": {1, 3},
}
# values 保持原样。
```

空列表的结果为 `{"unique": [], "counts": {}, "repeated": set()}`。

### 验收与本人核对

- 首次出现顺序正确；每个值的次数正确；重复值没有漏记或误记。
- 所有频数相加等于输入长度；全相同、全不同、含零与负数、空输入都有结果。
- 选一个值，说明它何时进入 unique、如何累计 counts、为什么进入或没有进入 repeated。
- 核对：直接用 `list(set(values))`，是否承诺了题目要求的首次顺序？

```bash
uv run --locked pytest -q challenges -k summarize --challenge-impl=student
```

## B｜应用一批修改，报告最终变化

**目标：** 在保留原记录的同时处理修改清单，区分“操作过”与“最终改变”。

入口：`apply_changes(original, updates, removals)`。

### 条件

- `original` 是字符串键、整数值的普通字典。
- `updates` 是按顺序排列的 `(键, 新值)` tuple 列表；键可以重复，同一键最后一次更新生效。新键可以加入。
- `removals` 是待删除键的字符串列表；键可以重复，缺失键忽略。
- **先依次更新，再执行删除**；出现在两份清单中的键最终删除。
- 返回字典，固定包含：
  - `record`：执行完所有操作的新字典。
  - `changed`：相比 original，最终新增、删除或值改变的键组成的 set。
- 更新后又改回原值，不算最终变化；原本不存在的键新增后又删除，也不算最终变化。

### 应得到的结论

```python
original = {"a": 1, "b": 2, "c": 3}
updates = [("b", 20), ("d", 4), ("b", 22)]
removals = ["c", "missing"]

# apply_changes(original, updates, removals) 应返回：
{
    "record": {"a": 1, "b": 22, "d": 4},
    "changed": {"b", "c", "d"},
}
# 三份输入都保持原样。
```

再预测这组边界：

```python
original = {"a": 1}
updates = [("a", 9), ("a", 1), ("new", 5)]
removals = ["new", "missing"]
# 最终 record 为 {"a": 1}，changed 为 set()。
```

### 验收与本人核对

- 后一次更新覆盖前一次；删除发生在全部更新之后；缺失键和重复删除不报错。
- changed 比较最终记录与原记录，不等于“修改清单中出现过的键”。
- 空记录、空清单、更新后删除、改回原值均符合上述规则。
- 选择一个键，按清单顺序追踪它的值，解释它最后是否属于 changed。

```bash
uv run --locked pytest -q challenges -k apply_changes --challenge-impl=student
```

## C｜对齐两次测量，找出超出阈值的变化

**目标：** 保持编号与数据的对应关系，区分变化量和变化幅度。

入口：`compare_measurements(ids, baseline, current, threshold)`。

### 条件

- `ids` 是不重复的字符串编号列表。
- `baseline`、`current` 是两个等长的一维整数 NumPy 数组，长度与 ids 相同；三者可以同时为空。
- 每个测量值在 -1,000,000 到 1,000,000 之间；threshold 是非负整数。
- 同一位置表示同一编号的两次测量。
- 变化量为 `current - baseline`；**变化量的绝对值大于 threshold 才算异常**，等于阈值属于正常。
- 返回字典，固定包含：
  - `delta`：新的一维整数数组，每项为对应位置的变化量。
  - `alerts`：异常编号的新列表，保持输入相对顺序。
  - `normal`：正常编号及其 current 值组成的新字典。

### 应得到的结论

```python
ids = ["a", "b", "c", "d"]
baseline = np.array([10, 20, 30, 40])
current = np.array([11, 18, 30, 45])
threshold = 2

# compare_measurements(...) 应返回：
{
    "delta": np.array([1, -2, 0, 5]),
    "alerts": ["d"],
    "normal": {"a": 11, "b": 18, "c": 30},
}
# b 的变化幅度恰好是 2，因此正常；所有输入保持原样。
```

空输入返回空整数数组、空 alerts 列表和空 normal 字典。

### 验收与本人核对

- 正向与负向的大幅变化都能被发现；等于阈值不进入 alerts。
- 编号和对应数据没有错位；正常记录保存的是新测量值，而不是变化量。
- 空输入、全部正常、全部异常与阈值为零均有明确结果。
- 选一个负向异常，逐步说明如何从两次测量得到 delta，再进入 alerts；构造一组输入检查 `>` 与 `>=` 的区别。

```bash
uv run --locked pytest -q challenges -k compare_measurements --challenge-impl=student
```

## 与 Agent 合作的提示词

将选中的题目原文与以下提示一起交给 Agent：

```text
我选 W5 综合题……。先读题目和给定测试，不要马上实现。
用题目示例和我选的另一份输入，和我核对完整预期结果：……。
确认后在 challenges/work.py 实现这一题，并在 challenges/test_my_cases.py
用同名 fixture 加入我的输入和预期，不直接导入参考实现。
测试函数名包含所选题的关键字 summarize、apply_changes 或 compare_measurements，
例如 test_my_summarize_case，确保题目命令的 -k 也能选中我的测试。
不要修改教师测试。运行这一题的验收，给我实际结果和 diff。
最后沿一个元素或键带我读实现，指出原输入是否改变，以及一个容易混淆的边界。
```

完成后，本人重跑题目对应的 student 命令，留下这份不同输入的预期、实际结果和一条边界解释。无需长报告或完整聊天记录。

## 参考与故障对照

- `work.py`：学生实现；初始函数壳会报未实现。
- `demo.ipynb`：可直接演示的题目、完整参考解答与核对过程；示例通过不代表 work.py 已完成。
- `examples.py`：教师公开参考与已知故障。
- `conftest.py`：按模式选择函数的工具；`test_tasks.py`：给定验收。
- 每题的测试通过同名函数参数接收实现；可让 Agent 参照给定测试写自己的用例。

```bash
# 检查全部公开参考：应通过。
uv run --locked pytest -q challenges --challenge-impl=reference

# 查看已知故障：应被具体断言拒绝，可加 -k 只看选中的题。
uv run --locked pytest -q challenges --challenge-impl=broken
```

本周默认的 `uv run --locked pytest -q` 与已有 CI 继续检查原来的三道基础题。综合题单独验收，未选择的题不会阻碍基础任务通过。

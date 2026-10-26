# W5｜演示与微练习答案

`demo.ipynb` 的示例全部预先写好。第一次从干净 kernel 顺序运行；课堂停在微练习处，让学生先预测，再修改一处。微练习的原代码是可运行起点，原版 Run All 不表示学生已经完成修改。

默认路线：主 Notebook 从头到小练习 8 → `challenges/demo.ipynb` 的 A 题 → 第三课时回 `operations.py` 与 Terminal。B、C 供提前完成者继续探索。

## 恢复与观察

- 每格演示或微练习都自行初始化所用数据；需要恢复时，重跑该格完整代码。
- 不把上一格的 `append`、`pop` 结果带进下一格；第二课时及推导式部分也有自己的初态。
- `np` 来自最初的 `import numpy as np`；重启 kernel 后从开头运行。
- set 的显示和遍历顺序、`set.pop()` 取到谁不作固定答案；核对元素内容、数量与成员关系。
- `a.dtype` 的具体整数宽度可以随平台变化，不以 `int64` 等具体名字作跨平台验收条件。

## 各段的已知结果

- deepcopy：source 为 `{'values': [1, 2, 3]}`，other 为 `{'values': [9, 2, 3]}`；不展开复制原理。
- 四类对象：list、dict、数组各有 4 项，set 有 3 项；数组形状 `(4,)`。
- 取值：`xs[0]`、`a[0]` 为 1，`record['b']` 为 2；`2 in unique` 与 `'b' in record` 为 True，`2 in record` 为 False。
- 增加：list 最终 `[10, 2, 2, -1, 5]`；dict 的 b 变为20、增加 e=5；set 有四个元素 `{1, 2, -1, 5}`；原数组 `[10, 2, 2, -1]`，新数组 `[10, 2, 2, -1, 5]`。
- 删除：list 取出 -1 后剩 `[1, 2, 2]`；dict 取出 b 的值2并删去该键；set 先删2，再移除任意剩余元素；`np.delete` 返回 `[2, 2, -1]`，原数组不变。
- 遍历：dict 默认取得键；`.items()` 取得键值对。例子中的 zip 输出 a/1、b/2，不展开迭代器或不等长输入。
- 平方循环：`[1, 4, 4, 1]`；正数平方：`[1, 4, 4]`。
- 推导式：list 为 `[1, 4, 4]`，set 内容为 `{1, 4}`，dict 为 `{'a': 1, 'b': 4, 'c': 4}`，数组内容为 `[1, 4, 4]`；原输入保持。

## 微练习答案

### 1｜数量与重复值

- 起点输出：列表4项，集合3项。
- 一种修改：`xs = [1, 2, 2, 2]`；`unique = set(xs)` 后，数量分别为4和2。
- 看点：set 消除重复元素，不是替列表删掉一个位置。

### 2｜键与值

- 起点输出：`2`、`True`、`False`。
- 将 `key = "b"` 改为 `key = "d"`，输出 `-1`、`True`、`False`。
- 看点：存在值2，不代表字典中存在键2。

### 3｜原对象与返回值

- 起点：xs 为 `[1, 2, 2, -1, 5]`，returned 为 `None`。
- 修改为 `returned = xs.pop()`：xs 为 `[1, 2, 2]`，returned 为 `-1`。
- 看点：不能写成“方法只修改、函数才返回”；pop 同时完成两件事。

### 4｜数组追加

- 起点：原数组长度4，新数组长度5。
- 改为 `grown = np.append(a, 0)`：a 仍为 `[1, 2, 2, -1]`，grown 为 `[1, 2, 2, -1, 0]`。
- 看点：`np.append` 是模块函数，产生新数组；`a` 不会因为这次调用自动变长。

### 5｜键值对的显示

将循环体改为 `print(value, key)`，四行依次为：

```text
1 a
2 b
2 c
-1 d
```

- 看点：循环接收键和值，与打印顺序是两件事。

### 6｜逐项变换

将 `result.append(item ** 2)` 改为 `result.append(item * 10)`。

- result 为 `[10, 20, 20, -10]`，xs 为 `[1, 2, 2, -1]`。
- 看点：先在循环外建立结果列表，每轮只加入当前结果；不把结果列表建立在循环体内。

### 7｜正数与非负数

- 起点输入 `[1, 0, 2, -1]`，输出 `[1, 4]`。
- 改为 `if item >= 0:`，输出 `[1, 0, 4]`。
- 看点：原固定例子没有0，区分 `> 0` 与 `>= 0` 需要换一份输入。这与正式任务中的错误实现相呼应。

### 8｜字典推导式筛选

将条件改为 `if v >= 2`：

```python
result = {k: v ** 2 for k, v in record.items() if v >= 2}
```

- 结果 `{'b': 4, 'c': 4}`；record 保持原样。
- 看点：筛选依据是原值 v，平方计算发生在保留之后；重复的值2不会让不同键合并。

## 正式任务交接

- 函数任务与验收以 `EXPERIMENT.txt` 为准，不能用 Notebook 已运行代替作业完成。
- 先展示错误候选如何触发断言，再给学生操作；读一条失败的输入、预期和实际结果。
- 保留本地测试作为 CI 网络受阻时的退路；不在课堂临时搭建工作流。

## 综合题：选一题展开，其他留作拓展

- 投屏打开 [`challenges/demo.ipynb`](challenges/demo.ipynb)：先展示题目与输入，停下来给学生操作，再向下展示参考代码、运行结果和边界。题目文字与完整函数分开成 cell，不需要临场从文件里找答案。
- 题内先顺序运行；已跑过函数定义后，样例核对与边界核对两类 cell 都能回头单独重跑。
- 完整条件与结论在 [`challenges/README.md`](challenges/README.md)，验收使用的参考实现在 `challenges/examples.py`。
- A 顺序去重与频数统计：同一个值在 unique 只出现一次，在 counts 累计，在 repeated 中按次数判断。
- B 应用修改：沿一个键追踪“更新 → 再更新 → 删除”，最后与原记录比较；恢复原值、新增后删除不算最终变化。
- C 两次测量：沿一个编号核对位置、变化量、绝对值与阈值；等于阈值正常，正负向都可能异常。
- 约 5 分钟预测另一份输入，10～15 分钟 Agent 实现与测试，5～10 分钟本人核对、解释。提前完成就继续，不把等待当作教学时间。
- 综合题验收只在显式指定 challenges 时运行；不要把基础 CI 的绿色当作选做已通过。

## 参考材料

本 Notebook 例子与练习按本课程对象和操作重新编写。教学组织参考短例子、预测、运行与小改的方式：

- [Software Carpentry：Lists](https://swcarpentry.github.io/python-novice-gapminder/11-lists.html)、[For Loops](https://swcarpentry.github.io/python-novice-gapminder/12-for-loops.html)
- [University of Helsinki Python MOOC：Lists](https://programming-26.mooc.fi/part-4/3-lists/)、[List comprehensions](https://programming-26.mooc.fi/part-11/1-list-comprehensions/)
- [Python 3.12 数据结构](https://docs.python.org/zh-cn/3.12/tutorial/datastructures.html)、[NumPy 入门](https://numpy.org/doc/stable/user/absolute_beginners.html)

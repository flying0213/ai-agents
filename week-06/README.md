# W6｜函数、调用与可见性

打开 `demo.ipynb`，先看每个场景的需求和输入输出，再预测、运行错误代码，修复后组装成函数。

已有仓库的同步、个人练习副本的保存与运行步骤见 [W6 学生指南](https://wxyinucas.github.io/teaching-hub/#/terms/2026-fall/courses/ai-agents/weeks/week-06/guide)。同步整个 `week-06/`，保留同目录的配置与环境文件。

## 启动

更新已有的 ai-agents 仓库，以下命令从仓库根目录执行，进入本周目录：

```bash
cd week-06
uv sync --locked
code .
```

在 VS Code 打开 `demo.ipynb`，选择本目录 `.venv` 的 Python kernel。

也可以在本周目录启动 Jupyter 网页版：

```bash
uv run --locked python -m ipykernel install --user --name ai-agents-week-06 --display-name "W6 Python 3.12"
uv run --locked jupyter notebook demo.ipynb
```

网页中选择 **W6 Python 3.12**。启动终端在使用期间保持运行。

## 每个场景的六格

1. **场景与需求**：确认要做什么、输入是什么、结果应是什么。
2. **输入**：恢复本场景数据，留下自己的预测。
3. **Playground**：运行有缺陷的代码，修改、加 `print`，观察中间状态。可见性问题所需的函数边界保留。
4. **函数组装**：将修复结果放入给定函数壳。
5. **单元检查**：运行断言，检验换输入、连续调用与数据是否按要求共享或隔离。
6. **参考**：点击展开静态文字答案，不会自动执行。

**初始代码有错，函数壳尚未实现，因此初始检查应失败。** 按场景运行；直接 Run All 会停在第一个错误，不表示环境安装失败。调试时修复实现，保留给定断言和单元检查。

需要恢复时，从本场景输入格重新运行，再运行 Playground、组装和检查。场景五尤其要先恢复输入：星号导入已经覆盖的名字，不会因你删掉那行源代码而自动复原。

六个场景依次是：修正临时阈值、独立累计、递归求和与日志、分轮收集数据、生成实验配置、保存快照与分叉。最后一个场景可以与 Agent 合作，先预测父子实例和旧快照的变化，再核验结果。

## 文件职责

- `demo.ipynb`：全部题目、错误 Playground、函数壳、检查与折叠参考。
- `defaults.py`：第 5 题给定配置，保持原文件。
- `pyproject.toml`、`uv.lock`、`.python-version`：本周独立环境。

本周不改 W2～W5 的代码、环境和 CI；完成情况以本 Notebook 中实际修复后的检查为依据。

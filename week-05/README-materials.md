# W5｜数据操作与遍历

本周使用已经 clone 的 `ai-agents` 仓库，在 `week-05/` 建立独立环境；不改 W2～W4 的代码、依赖和报告，不进入另一个课程仓库。

## 取得材料

在 VS Code 的 Terminal 中查看已有 remote：

```bash
cd ~/course/w02-workbench
git remote -v
git status -sb
```

从地址为 `wxyinucas/ai-agents` 的教师 remote 更新，只选择符合当前情况的一条：

- 教师 remote 叫 `upstream`：`git pull --no-rebase upstream main`。
- 尚未配置个人 remote，教师 remote 仍叫 `origin`：`git pull --no-rebase origin main`。

有本地修改、合并冲突或更新报错时，让 Agent 先解释 Git 状态，再协助保留已有成果、完成更新。不重新 clone，不删除原目录或丢弃已有提交。

## 打开本周环境与 Notebook

```bash
cd ~/course/w02-workbench/week-05
uv sync --locked
code .
```

本目录的 `pyproject.toml`、`uv.lock` 管理 Python 3.12、NumPy、pytest 和 Notebook kernel。不要让 Agent 在仓库根目录重建环境。

打开 [`demo.ipynb`](demo.ipynb)，在右上角选择 `week-05/.venv` 的 Python kernel。各段已经给出初始化与完整示例；先预测输出，再运行，随后按“小练习”修改一处并核对。每个独立实验都从该段的初态开始。

Python／Jupyter 扩展或 kernel 选择受阻时，把实际界面交给 Agent 定位。Notebook 环境暂时不能用时，可在本周目录执行 `uv run --locked python`，逐段运行相同代码；任务验收仍使用 Terminal。

## 文件职责

- [`demo.ipynb`](demo.ipynb)：完整短示例、分段小练习与核对目标。
- [`TEACHER-NOTES.md`](TEACHER-NOTES.md)：微练习答案、预期输出与恢复位置，公开供核对。
- [`EXPERIMENT.txt`](EXPERIMENT.txt)：三道任务的精确规格与验收规则。
- [`operations.py`](operations.py)：学生与 Agent 要完成的三个函数壳。
- [`examples.py`](examples.py)：公开参考与已知故障，只读对照。
- `tests/conftest.py`：按 `--impl` 选择验收对象的课程工具，不修改。
- `tests/test_acceptance.py`：教师公开验收，不修改预期来获得通过。
- `tests/test_student.py`：一条可扩充的学生测试示例；在这里增加自己的用例。
- [`challenges/demo.ipynb`](challenges/demo.ipynb)：三道独立综合题的课堂展示，每题按“题目 → 完整参考解答 → 运行核对”推进；条件与验收见 [`challenges/README.md`](challenges/README.md)。
- `../.github/workflows/week-05.yml`：远端重复运行同一套本地测试，不负责部署。

## 最后的三道任务

先读 `EXPERIMENT.txt`，分别明确“原输入是否改变”和“返回什么”。

- `pop_last(items)`：原地取出列表最后一项并返回；空列表返回 `None`。
- `positive_squares(values)`：从整数列表或一维整数数组生成新 Python 列表，保留正数的平方、原顺序与重复项，原输入保持。
- `positive_square_map(record)`：生成新字典，保留正值对应的键及平方值，保留这些键的相对顺序，原字典保持。

可以用循环或推导式；不检查源码是否出现某个关键字。函数壳由课程提供，本周不要求从头设计接口，也不添加未约定的非法输入处理。

可以先给 Agent：

```text
阅读 EXPERIMENT.txt、operations.py 与测试，先不要实现。
请和我核对三个函数的输入、原对象是否改变、返回什么。
我先预测一组结果，你再帮我在 tests/test_student.py 补一个不同输入的测试。
测试通过函数参数接收课程 fixture，不直接 import 某个候选实现。
确认预期后，只实现 operations.py；不修改教师测试和工具。
```

## 先认识测试反馈

在 `week-05/` 逐条执行：

```bash
uv run --locked pytest -q --impl=reference
uv run --locked pytest -q --impl=broken
uv run --locked pytest -q --impl=student
```

`--impl` 是本周增加的 pytest 选项：

- `reference` 应通过，检查公开参考实现。
- `broken` 应出现能解释的断言失败，检查已知故障；红色是这次演示的预期结果。
- `student` 检查 `operations.py`，也是省略开关时的默认值。函数壳尚未实现时出现 `NotImplementedError` 正常。

测试通过参数名 `pop_last`、`positive_squares`、`positive_square_map` 接收被检查的函数。直接 import 参考函数，会绕过 `--impl` 选择，不能验收自己的实现。

挑一条失败说明：给了什么输入，哪条承诺没满足，预期和实际有什么不同。导入失败、环境错误和没有运行测试，不等于发现了程序的逻辑错误。

## 实现并亲自重跑

与 Agent 完成 `operations.py` 后，本人执行：

```bash
uv run --locked pytest -q --impl=student
git diff -- operations.py tests/test_student.py
```

检查不只看输出：`pop_last` 必须真的改变原列表；另外两个函数必须保持原输入。再换一组输入，例如含零、重复项或筛选后为空的情况，核对测试是否覆盖了自己关心的行为。

## 保存到个人远端，查看 CI

CI 是 GitHub 在远端运行同一套测试。先在仓库根目录确认 `origin` 是自己的仓库，不是教师的 `wxyinucas/ai-agents`。个人 remote 尚未配置时，先按 W3 Guide 完成接续；当前仍可做全部本地练习，不另建一个 W5 仓库。

```bash
cd ~/course/w02-workbench
git remote -v
git status -sb
git add -- week-05/operations.py week-05/tests/test_student.py
git diff --cached
git commit -m "Complete W5 data operation exercises"
git push origin main
```

先核对暂存区，包括原先已经暂存的其他文件。自己的 Notebook 记录按需另存，不把 `.venv/`、缓存或凭证提交到仓库。push 受阻时让 Agent 解释实际状态，不 force push。

在个人 GitHub 仓库打开 **Actions → W5 data operations**：

1. 首次使用 fork 时，若页面要求启用 Actions，由仓库本人点击启用；手动 **Run workflow** 选择 `student`，或在后续修改并 push 后查看新检查。不强制 fork 或提交 PR。
2. 对照本次提交编号，打开运行记录中的 **Run student acceptance tests**，确认检查的是自己的实现。
3. 失败时打开日志，区分环境／启动失败与断言失败；修复后重新提交，查看新提交的检查。

教师原仓库的普通提交默认检查 `reference`，用于核验公开材料。**教师仓库的绿色不表示学生函数壳已完成。** 个人仓库普通 push 默认检查 `student`；手动运行可以明确选择 `student`、`reference` 或 `broken`，结果必须连同模式一起阅读。

工作流只申请仓库内容读取权限，不需要填写 Secret、不部署网站、不要求学生编写 YAML。账户／组织禁用 Actions、网络或依赖下载失败时，不临场修改安全策略；保留错误并先在本地运行同一条 `uv run --locked pytest -q --impl=student`。本地通过不冒充远端已经通过。

## 核对与延伸

讲练或基础任务完成后，可进入 [`challenges/`](challenges/README.md)，任选“顺序去重与频数统计”“应用一批记录修改”或“比较两次测量”。三题由 Agent 协助实现，本人负责预测另一组输入、运行测试并解释边界；不要求全部完成。它们必须显式运行单独的验收命令，不影响本周默认测试与 CI。

完成后保留代码、测试结果和一次失败修正。公开参考答案可以用来核对，但本人仍需说明一次操作改变了什么、返回了什么，以及一个循环每轮处理了什么。

本材料的示例和题组为本课程自制，组织方式参考下列公开资料；不要求注册其他课程、重装 Anaconda 或迁移平台：

- [Software Carpentry：Lists](https://swcarpentry.github.io/python-novice-gapminder/11-lists.html)、[For Loops](https://swcarpentry.github.io/python-novice-gapminder/12-for-loops.html)：短示例、逐段练习与参考答案。
- [赫尔辛基大学 Python MOOC：Lists](https://programming-26.mooc.fi/part-4/3-lists/)、[List comprehensions](https://programming-26.mooc.fi/part-11/1-list-comprehensions/)：数据操作、函数与方法、循环到推导式的展开。
- [NumPy 官方入门](https://numpy.org/doc/stable/user/absolute_beginners.html)：数组创建、索引和属性。

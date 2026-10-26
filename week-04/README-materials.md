# W4｜追加实验与配置隔离

导师需要保留昨天的投针方案，再生成可独立调整的新方案。本周与 Agent 先写有依据的测试、拒绝共享错误，再实现 `make_variant` 和核验。完整规格见 [EXPERIMENT.txt](EXPERIMENT.txt)，操作步骤见课程网站的 W4 Guide。

本目录是已有 `ai-agents` 仓库中的独立 uv 项目，不需要第二次 clone、`uv init` 或 `git init`，不改 W2/W3 环境与报告。

## 环境与材料

更新教师材料后，在学生已有仓库执行：

```bash
cd ~/course/w02-workbench/week-04
uv sync --locked
code .
```

Python 3.12、pytest、ipykernel 由本目录的配置与锁文件管理。VS Code 打开 `demo.ipynb`，选择本周 `.venv` 的 kernel；Python、Jupyter 扩展由 VS Code 安装。本周不引入 matplotlib 或 LaTeX。

- `variant.py`：学生函数壳，初始抛出 `NotImplementedError`。
- `examples.py`：直接共享 `direct`、浅复制 `shallow` 两份故障，以及课堂已展示的 `reference`，只读对照。
- `demo.ipynb`：教师演示 cell 组，学生可以复现，不替代作业。
- `tests/conftest.py`：教师测试辅助，提供 `make_variant` fixture 和候选切换。
- `tests/test_acceptance.py`：教师独立公开验收，按多组合法输入检查公开承诺。
- `tests/test_student.py`：学生与 Agent 写的测试，初始只有说明，没有占位测试。

只修改函数、学生测试与自己的记录，不修改教师工具或预期来获得通过。

## --impl 如何切换

`--impl` 是本周增加的 pytest 扩展选项，不是原生参数：

| 值 | 实际检查的函数 |
| --- | --- |
| `student`（默认） | `variant.py` 中的学生实现 |
| `direct` | `examples.py` 中的直接共享故障 |
| `shallow` | `examples.py` 中的浅复制故障 |
| `reference` | `examples.py` 中的参考实现 |

每个测试通过函数参数接收 fixture，例如签名 `def test_my_case(make_variant):`，在函数体中调用这个参数。不要直接 import 某个候选，否则开关无法切换你实际检查的对象。

## 先写测试，再实现

读规格，另选合法输入、独立写出答案，与 Agent 编写学生测试。写好后：

```bash
uv run --locked pytest -q tests/test_student.py --impl=reference
uv run --locked pytest -q tests/test_student.py --impl=direct
uv run --locked pytest -q tests/test_student.py --impl=shallow
```

参考应通过，故障应有能解释的断言失败。导入、环境报错不算发现共享；`no tests ran` 表示还没有自己的测试。参考也失败时，先检查测试依据，不接受“任何实现都会失败”的测试。

再实现 `variant.py`，亲自执行：

```bash
uv run --locked pytest -q tests/test_student.py --impl=student
uv run --locked pytest -q tests/test_acceptance.py --impl=student
```

教师与学生测试分开运行；教师验收通过不等于已编写自己的测试。默认 `uv run --locked pytest -q` 只收集本目录测试，不去运行 W2/W3。

必做包括同参数两次调用：起始内容相等、身份不同；改第一份后，第二份与 source 保持。用独立预期或 deepcopy 保存旧内容，不用 `before = source` 代替快照。

选做“参数完全不变”：先证明内容比较可能漏错，再用身份或后续操作拒绝共享。隔离约定仍是必做要求，选做的是构造、解释这个反例。

## 保存与边界

沿用同一 Git 历史，保存已检查的函数、学生测试和简短实际证据。不要求新分支、模拟远端、PR、CI 或长报告；本人输出与教师记录注明来源。

配置测试不证明随机实验的结果稳定，也不证明 π 估计一定更准确。

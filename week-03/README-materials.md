# W3 学生材料｜独立实验与报告

这是一个“让 Agent 实现实验、用证据检查结果”的小项目，不是教师参考答案。
材料源文件由 `ai-agents/week-03/` 统一维护。沿用 W2 已经 clone 的 `~/course/w02-workbench` 仓库，通过 Git 获取材料，直接在本周目录实现：

```bash
cd ~/course/w02-workbench
git pull --no-rebase origin main
cd week-03
code .
```

在 VS Code 中让 Agent 先阅读 `EXPERIMENT.txt`、公开测试、`rebuild.sh` 和 `report.tex`。
仓库与已有 Git 历史继续使用；无需第二次 clone、跨目录复制或在 `week-03/` 中执行 `git init`。
W2 的根目录代码不是 W3 的代码基线。本目录必须有自己的 `pyproject.toml`、`uv.lock` 和 `.venv/`，不修改根项目的依赖配置，也不使用根目录的环境运行 W3。
以后教师更新材料时，仍通过 Git 合入更新；按 Guide 配置个人 remote 后，教师仓库保留为 `upstream`，更新从该 remote 获取。

## 材料与职责

- `EXPERIMENT.txt`：自然语言需求、固定接口、实际输出和选做任务。
- `report.tex`：报告骨架；空模板也可以编译，图表生成后自动插入。
- `rebuild.sh`：师生共用的重建入口；先实验，再图表，最后编译 PDF。失败就停止。
- `tests/`：公开测试。不要修改测试来获得通过；检查失败原因并改实现。

Agent 需要在 `week-03/` 中生成独立的 `pyproject.toml`、`uv.lock`、`experiment.py` 和 `render_results.py`。
本周 uv 项目使用 Python 3.12（`requires-python = ">=3.12,<3.13"`），声明自己的 matplotlib 和 pytest 依赖，不加入 W2 根项目的 workspace。
若使用 `uv init`，在本目录执行 `uv init --bare --python 3.12 --no-workspace --vcs none`；`--no-workspace` 防止它把本周目录加入根项目并修改 W2 的 `pyproject.toml`。
在本周 `pyproject.toml` 中声明以下测试配置，使 pytest 只读取本周配置和 `tests/`：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

只固定这两个 Python 入口和需求中列出的接口，其余内部结构可以自己选择。
不要把 API Key 写进项目。

教师的可运行演示另放在 [`../demos/week-03-buffon/`](../demos/week-03-buffon/)，可以观察或在本地复现；它不覆盖本目录，也不改变学生的实现和验收要求。

```text
ai-agents/week-03/
├── EXPERIMENT.txt
├── README-materials.md
├── report.tex
├── rebuild.sh
├── tests/
├── pyproject.toml       # Agent 生成：Python 3.12、matplotlib、pytest
├── uv.lock             # uv sync 生成
├── experiment.py       # Agent 实现：真实投针与 CSV
└── render_results.py   # Agent 实现：由 CSV 生成图表
```

## 按这个顺序试跑

1. 安装好编译引擎与 LaTeX Workshop，先编译 `report.tex`。此时没有实验结果也正常。
2. 先读需求和测试，找一个可手算的预期值并说明依据；确认后，让 Agent 在 `week-03/` 建立独立 uv 项目并实现两个入口。
3. 安装依赖并生成锁文件，运行实验，再运行公开测试。
4. 重建整份报告，打开 PDF 与 CSV 核对。

```bash
uv sync
uv run --locked python experiment.py
uv run --locked pytest -q
bash rebuild.sh
```

上面的命令都在 `week-03/` 中运行；先确认本目录已有独立的 `pyproject.toml`，再执行 `uv sync` 生成本周的锁文件与环境。尚未建立本周项目时，不先运行 `uv run`，以免它向上找到 W2 根项目。
W2 根目录的测试与这份报告实验互不替代，本周只运行 `week-03/tests/`。
公开测试检查：固定针位的相交判断、手算的估计值、部分非法输入、同环境同参数同种子的可复现性，以及 CSV 与 `simulate` 返回值、估计公式是否一致。
这些测试尚未证明取样均匀、彼此独立，或 seed 没在循环内重设；它们也不验收图表与 PDF。
图像和 PDF 的内容仍由你打开检查；“存在文件”不代表内容正确。
测试没有要求估计值精确等于圆周率，也没有要求样本越多误差必定越小。

## 默认参数与生成文件

- 起始配置 `seed=42`；投针数为 `1000, 10000, 100000`。
- 针长 `0.5`，平行线间距 `1.0`。
- 每组独立实验开始时初始化随机数生成器一次；不要放在投针循环里。
- 默认一轮生成 `results.csv`、`results-table.tex`、`results-params.tex`、`results.png` 和 `report.pdf`。
- PDF 要展示实际参数和实际结果，不把默认参数写死为展示内容。

`rebuild.sh` 先进入自身所在目录，因此从外部运行它也会在项目目录生成结果。
两个 Python 入口把输出写到当前工作目录；这也让测试可以在临时目录中检查 CSV，而不覆盖你的结果。
选择实现 CLI 参数后，例如 `bash rebuild.sh --seed 7`，参数会透传给 `experiment.py`。
维护时可以更换入口的 seed，并在原有三组基础上增加更大的 n；CSV 和报告必须记录实际值。
公开测试读取 CSV 中的实际参数，不会要求维护后的结果仍使用 seed 42。

## 保存与维护

确认测试、图表、参数和 PDF 都一致后，再检查 `.gitignore` 与 Git diff。本周文件的提交属于沿用的整个 `ai-agents` 仓库，不在本目录创建嵌套仓库；已有 W2 commit 继续保留。
通常忽略 `.venv/`、缓存和 LaTeX 中间文件；不要提交 API Key。
保留需求、模板、脚本、测试、代码和依赖锁文件，便于别人重建。
是否额外提交生成结果，按 Guide 的提交要求处理。

选做拓展统一见 [W3 Guide](https://github.com/wxyinucas/teaching-hub/blob/main/terms/2026-fall/courses/ai-agents/weeks/week-03/guide.md)。选一个现有项目的工具或代码问题，让 Agent 带路定位并核验解释。
只读探索即可，不要求增加功能或安装另一种 Agent，也不作为下一周的前提。
